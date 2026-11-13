"""Targeted deduplication of the Grade 1 banks.

Only items whose question identity (prompt + options + answer + picture description) also
appears in a *different* skill are touched; everything else is left exactly as built. For each
redundant copy we try, in order:

  A. a fresh draw from the same family the item came from (new numbers, original wording);
  B. a fresh draw re-presented in another task form (new numbers and new wording);
  C. the same fact re-presented in another task form, without the picture.

One copy of every identity is always kept, so deliberate fluency repetition inside a skill is
untouched. Usage: python3 dedupe1.py [unit_id ...]   (env G1_DRY=1 reports without writing)
"""
import importlib, json, os, re, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "units"))
import build1, forms, figs1
from build1 import Builder, MODS, mc_options
from dupstats import ident, shape, norm
from g1lib import Diagram, Reject, rng
from outline import UNITS, COURSE_ID, skill_records

ROOT = build1.ROOT
DRY = os.environ.get("G1_DRY") == "1"
CAND = int(os.environ.get("G1_CAND", "40"))


def bank_path(u):
    return os.path.join(ROOT, "question-banks", COURSE_ID, u["id"] + ".json")


def meta_path(u):
    return os.path.join(ROOT, "question-banks", COURSE_ID, "meta", u["id"] + ".meta.json")


def checks_path(u):
    return os.path.join(HERE, "out", u["id"] + ".checks.json")


def jload(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def jdump(p, obj):
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)


def fam_of(unit_mod, checks, q):
    fam = checks[q["id"]].get("family", "")
    ms = list(re.finditer(r"fam(\d+)", fam))
    sm = re.search(r"-s(\d+)-", q["id"])
    if not ms or not sm:
        return None
    idx = int(ms[-1].group(1)) - 1
    rec_idx = int(sm.group(1))
    fams = unit_mod.SKILLS[rec_idx]["fams"]
    return fams[idx] if 0 <= idx < len(fams) else None


def emit_variant(b, rec, L, p, fmt, qid, fname):
    """Emit candidate p as the given format; returns (q, meta, chk) or None if incompatible."""
    if fmt == "multiple-choice":
        if p.answer is None:
            return None
        if not p.options and mc_options(p, 0, rng("probe", qid)) is None:
            return None
        pos = 0
        if p.options:
            pos = [i for i, (t, c) in enumerate(p.options) if c][0]
        return b.emit(rec, L, 0, p, fmt, fname, rng("pos", qid), pos, qid=qid)
    if fmt == "short-answer":
        if p.answer is None or p.options or p.parts:
            return None
        return b.emit(rec, L, 0, p, fmt, fname, rng("pos", qid), qid=qid)
    return None


def rewrite_item(q, meta, check, used_texts):
    src = dict(q)
    src["_meta"] = meta
    out = forms.rewrite(src, check, used_texts)
    return out[0] if out else None


def main():
    want = sys.argv[1:] or [u["id"] for u in UNITS]
    units = {u["id"]: u for u in UNITS}
    banks, metas, checkss, mods = {}, {}, {}, {}
    for u in UNITS:
        banks[u["id"]] = jload(bank_path(u))
        metas[u["id"]] = jload(meta_path(u))
        checkss[u["id"]] = jload(checks_path(u))
        mods[u["id"]] = importlib.import_module(MODS[UNITS.index(u)])
        for q in banks[u["id"]]["questions"]:
            q["_id"] = ident(q)

    counts = Counter(q["_id"] for u in UNITS for q in banks[u["id"]]["questions"])
    skills_of = defaultdict(set)
    for u in UNITS:
        for q in banks[u["id"]]["questions"]:
            skills_of[q["_id"]].add(q["skillId"])
    # every identity that appears in more than one skill: keep the first copy in outline order
    owner, dupes = {}, []
    for u in UNITS:
        for q in banks[u["id"]]["questions"]:
            if len(skills_of[q["_id"]]) > 1:
                if q["_id"] in owner:
                    dupes.append((u["id"], q))
                else:
                    owner[q["_id"]] = (u["id"], q["id"])

    shapes = Counter()          # within-skill masked-prompt counts (cap 6, as verify1)
    texts = defaultdict(set)    # within-skill wording used, for the re-presentation layer
    for u in UNITS:
        for q in banks[u["id"]]["questions"]:
            scope = (q["skillId"], q["level"])
            shapes[(scope, shape(q))] += 1
            texts[scope].add(norm(q["prompt"]))

    print(f"items {sum(len(b['questions']) for b in banks.values())}  redundant copies {len(dupes)}")
    stats = Counter()
    builders = {u["id"]: Builder(mods[u["id"]], units[u["id"]]) for u in UNITS}
    reccache = {}

    def recs_for(uid):
        if uid not in reccache:
            reccache[uid] = {r["id"]: r for r in skill_records(units[uid])}
        return reccache[uid]

    for uid, q in dupes:
        u, b, L = units[uid], builders[uid], ["cp2", "cp1", "honors"].index(q["level"])
        rec = recs_for(uid)[q["skillId"]]
        fmt, old_id = q["format"], q["_id"]
        scope = (q["skillId"], q["level"])
        fam = fam_of(mods[uid], checkss[uid], q)
        new, diag = None, None
        if q.get("diagram") and checkss[uid][q["id"]].get("diagram"):
            dd = checkss[uid][q["id"]]["diagram"]
            diag = Diagram(dd["kind"], dd["data"], q["diagram"]["spec"].get("alt", ""))

        def try_emit(p):
            cand = emit_variant(b, rec, L, p, fmt, q["id"], checkss[uid][q["id"]].get("family", "fam"))
            if cand is None:
                return None
            cq, cmeta, cchk = cand
            cid = ident(cq)
            if counts[cid] or cid == old_id:
                return None
            if shapes[(scope, shape(cq))] >= 6:
                return None
            return cand

        if fam is not None:
            for k in range(1, CAND + 1):
                try:
                    p = fam(rng("dedupe", q["id"], "A", k), L)
                except Exception:
                    p = None
                if p is not None:
                    cand = try_emit(p)
                    if cand:
                        new = cand
                        stats["A"] += 1
                        break
                rr = rng("dedupe", q["id"], "B", k)
                try:
                    p = fam(rr, L)
                except Exception:
                    p = None
                if p is None:
                    continue
                rw = forms.rewrite({"prompt": p.prompt, "answer": p.answer, "solutionSteps": p.steps,
                                    "_meta": {"questionType": p.qtype}}, p.check, texts[scope], rr,
                                   diagram=p.diagram)
                if rw is None:
                    continue
                cand = try_emit(rw)
                if cand:
                    new = cand
                    stats["B"] += 1
                    break

        if new is None:
            for k in range(1, 10):
                rr = rng("dedupe", q["id"], "C", k)
                rw = forms.rewrite({"prompt": q["prompt"], "answer": q.get("answer"),
                                    "solutionSteps": q.get("solutionSteps") or [],
                                    "_meta": metas[uid].get(q["id"], {})},
                                   checkss[uid][q["id"]]["q"], texts[scope], rr, diagram=diag)
                if rw is None:
                    continue
                cand = try_emit(rw)
                if cand:
                    new = cand
                    stats["C"] += 1
                    break

        if not new:
            if os.environ.get("G1_DBG") and stats["unresolved"] < 14:
                ck = checkss[uid][q["id"]]["q"]
                print("UNRES", q["id"], fmt, "fam=", getattr(fam, "__name__", None),
                      "diag=", bool(diag), "templates=", len(forms.templates(ck, rng("x", q["id"]))),
                      "|", q["prompt"][:70].replace("\n", " / "))
            stats["unresolved"] += 1
            stats["un_" + str(checkss[uid][q["id"]].get("q", {}).get("fn") or checkss[uid][q["id"]].get("q", {}).get("k"))] += 1
            continue

        cq, cmeta, cchk = new
        counts[old_id] -= 1
        counts[ident(cq)] += 1
        qs = banks[uid]["questions"]
        i = next(i for i, x in enumerate(qs) if x["id"] == q["id"])
        old_png = None
        if q.get("diagram"):
            old_png = os.path.join(ROOT, q["diagram"]["spec"]["src"])
        cq["_id"] = ident(cq)
        qs[i] = cq
        metas[uid][cq["id"]] = cmeta
        checkss[uid][cq["id"]] = cchk
        texts[scope].add(norm(cq["prompt"]))
        shapes[(scope, shape(cq))] += 1
        if cq.get("diagram"):
            src = os.path.join(ROOT, cq["diagram"]["spec"]["src"])
            os.makedirs(os.path.dirname(src), exist_ok=True)
            with open(src, "wb") as fh:
                fh.write(figs1.render_png(cchk["diagram"]["kind"], cchk["diagram"]["data"]))
        elif old_png and os.path.exists(old_png):
            os.remove(old_png)

    print("replacements:", dict(stats))
    if DRY:
        print("dry run: nothing written")
        return
    for u in UNITS:
        if u["id"] not in want:
            continue
        for q in banks[u["id"]]["questions"]:
            q.pop("_id", None)
        jdump(bank_path(u), banks[u["id"]])
        jdump(meta_path(u), metas[u["id"]])
        jdump(checks_path(u), checkss[u["id"]])
    print("wrote", len(want), "units")


if __name__ == "__main__":
    main()
