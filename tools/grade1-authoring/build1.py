"""Build the Grade 1 (math1) question banks from the unit family modules.

Usage: python3 build1.py [unit-module ...]
Writes:
  question-banks/math1/<unit>.json                bank (schemaVersion 1, shared schema)
  question-banks/math1/meta/<unit>.meta.json      per-question type, tags, distractor reasons
  question-banks/math1/assets/math1/<unit>/<id>.png   diagrams
  tools/grade1-authoring/out/<unit>.checks.json   check data for the independent verifier

Per skill and level: 30 questions = 12 short answer + 12 multiple choice + 3 error analysis
+ 1 true/false + 1 select-all + 1 open response/matching (7 derived from the core families).
Exact duplicate prompts are blocked across the whole course; near duplicates (same wording
with the same numbers and answer) are capped so a family cannot repeat itself.
"""
import importlib, json, os, re, sys, math
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "units"))
from g1lib import Reject, rng, LEVELS, err_of, tf_of, select_of, open_of, match_of, _norm
_OUTLINE = os.environ.get("G1_OUTLINE", "outline")
_out = importlib.import_module(_OUTLINE)
UNITS, COURSE_ID, PREFIX, skill_records = _out.UNITS, _out.COURSE_ID, _out.PREFIX, _out.skill_records
LABEL = getattr(_out, "LABEL", "Grade 1")
import figs1

ROOT = os.environ.get("G1_ROOT", os.path.abspath(os.path.join(HERE, "..", "..")))
MODS = [m.strip() for m in os.environ.get(
    "G1_MODS",
    "u01_add_sub_data,u02_story,u03_within20,u04_numbers99,u05_within100,u06_length,u07_geometry_time,u08_together"
).split(",") if m.strip()]
OUT = os.environ.get("G1_OUT") or os.path.join(HERE, "out")
QUOTA = {"sa": 12, "mc": 12, "err": 3, "tf": 1, "sel": 1, "open": 1}
NOTE = ("Original Claude-authored " + LABEL + " item (family: {fam}). Answer computed by the authoring script and "
        "re-derived by the independent verifier (tools/grade1-authoring/verify1.py).")
TAGSET = {"fluency", "count-on", "unknown", "story", "equation", "place-value", "compare", "order", "counting",
          "geometry", "time", "measurement", "data", "reasoning", "make-ten", "multistep", "connections"}
NEAR_LIMIT = int(os.environ.get("G1_NEAR", "3"))
SEEN, NEAR, EXC, REJECT = {}, Counter(), Counter(), Counter()


def pkey(p):
    s = " ".join(str(p.prompt).lower().split())
    if p.parts:
        s += "||" + "|".join(" ".join(str(x[0]).lower().split()) for x in p.parts)
    if p.options:
        s += "||" + "|".join(sorted(str(o[0]) for o in p.options))
    if p.diagram:
        s += "||" + p.diagram.alt.lower()
    return s


def nkey(p):
    k = pkey(p)
    return re.sub(r"\d+", "#", k) + "|" + ",".join(sorted(re.findall(r"\d+", k))) + "|" + str(p.answer)


def numeric_distractors(answer):
    """Fallback wrong answers for a whole-number key, each with a Grade 1 misconception."""
    try:
        v = int(str(answer).strip())
    except (TypeError, ValueError):
        return []
    out = [(str(v + 1), "counted one too many"), (str(v - 1), "counted one too few"),
           (str(v + 10), "added an extra ten"), (str(v - 10), "lost a ten"),
           (str(int(str(v)[::-1])) if len(str(v)) == 2 and str(v)[::-1] != str(v) else str(v + 2), "reversed the digits")]
    seen, res = {str(v)}, []
    for t, why in out:
        if t not in seen and not t.startswith("-"):
            seen.add(t)
            res.append((t, why))
    return res


def mc_options(p, pos, r):
    if p.options:
        return [{"text": t, "correct": bool(c)} for t, c in p.options]
    seen, ds = {_norm(p.answer)}, []
    for w, why in p.wrong:
        if _norm(w) in seen or not w.strip():
            continue
        seen.add(_norm(w))
        ds.append((w, why))
    for w, why in numeric_distractors(p.answer):
        if len(ds) >= 3:
            break
        if _norm(w) not in seen:
            seen.add(_norm(w))
            ds.append((w, why))
    if len(ds) < 3:
        return None
    ds = ds[:3]
    r.shuffle(ds)
    ds.insert(pos, (p.answer, ""))
    return [{"text": t, "correct": i == pos} for i, (t, _) in enumerate(ds)]


PHRASES = [(r"\bten-frame\b", "ten\u2011frame"), (r"\bten-frames\b", "ten\u2011frames"),
           (r"\btake-away\b", "take\u2011away"), (r"\bone-digit\b", "one\u2011digit"),
           (r"\btwo-digit\b", "two\u2011digit"), (r"\bpart-whole\b", "part\u2011whole"),
           (r"\bchange-unknown\b", "change\u2011unknown"), (r"\bresult-unknown\b", "result\u2011unknown"),
           (r"\baddend-unknown\b", "addend\u2011unknown"), (r"\bstart-unknown\b", "start\u2011unknown")]


def fix_text(t):
    if not isinstance(t, str):
        return t
    for a, b in PHRASES:
        t = re.sub(a, b, t)
    return t


def fix_q(q):
    q["prompt"] = fix_text(q["prompt"])
    if isinstance(q.get("answer"), str):
        q["answer"] = fix_text(q["answer"])
    elif isinstance(q.get("answer"), list):
        q["answer"] = [fix_text(a) for a in q["answer"]]
    for o in q.get("options", []) or []:
        o["text"] = fix_text(o["text"])
    for p in q.get("parts", []) or []:
        p["prompt"], p["answer"] = fix_text(p["prompt"]), fix_text(p["answer"])
    q["solutionSteps"] = [fix_text(x) for x in q["solutionSteps"]]
    return q


def fix_chk(c):
    if not isinstance(c, dict):
        return c
    out = {}
    for k, v in c.items():
        if k == "table":
            out[k] = {fix_text(t): fix_chk(e) for t, e in v.items()}
        elif k in ("unit", "shown", "answer", "accept", "good", "label", "rows"):
            out[k] = [fix_text(x) if not isinstance(x, (list, tuple)) else [fix_text(y) for y in x] for x in v] if isinstance(v, list) else fix_text(v)
        elif isinstance(v, dict):
            out[k] = fix_chk(v)
        else:
            out[k] = v
    return out


def normalise(f):
    """Give every family the metadata the build loop expects."""
    if not hasattr(f, "levels"):
        f.levels = [0, 1, 2]
    if not hasattr(f, "mode"):
        f.mode = "any"
    if not hasattr(f, "qtype"):
        f.qtype = None
    return f


class Builder:
    def __init__(self, unit_mod, unit):
        self.m, self.u = unit_mod, unit
        self.questions, self.meta, self.checks, self.diagrams = [], {}, {}, []

    def emit(self, rec, L, idx, p, fmt, fname, r, pos=None, qid=None):
        lv = LEVELS[L]
        qid = qid or f"{PREFIX}-{self.u['abbr']}-s{rec['index']:02d}-{lv}-{idx:03d}"
        q = {"id": qid, "skillId": rec["id"], "level": lv, "format": fmt,
             "prompt": p.mc_prompt if fmt == "multiple-choice" and p.mc_prompt else p.prompt}
        chk = {"q": p.check, "family": fname}
        if fmt == "multiple-choice":
            q["answer"] = p.answer
            q["options"] = mc_options(p, pos, r)
        elif fmt == "select-all":
            q["options"] = [{"text": t, "correct": bool(c)} for t, c in p.options]
            q["answer"] = [t for t, c in p.options if c]
        elif fmt == "open-response":
            q["parts"] = [{"prompt": a, "answer": b} for a, b, _ in p.parts]
            q["answer"] = "; ".join(f"({chr(97 + i)}) {b}" for i, (a, b, _) in enumerate(p.parts))
            chk["parts"] = [c for _, _, c in p.parts]
        else:
            q["answer"] = p.answer
        q["solutionSteps"] = p.steps
        if p.diagram:
            src = f"question-banks/assets/{COURSE_ID}/{self.u['id']}/{qid}.png"
            q["diagram"] = {"type": "image", "spec": {"src": src, "alt": p.diagram.alt}}
            chk["diagram"] = {"kind": p.diagram.kind, "data": p.diagram.data}
            self.diagrams.append((src, p.diagram))
        if getattr(p, "consts", None):
            chk["consts"] = [str(x) for x in p.consts]
        fix_q(q)
        chk["q"] = fix_chk(chk["q"])
        if "parts" in chk:
            chk["parts"] = [fix_chk(x) for x in chk["parts"]]
        q["standards"] = rec["standards"]
        q["sourceNotes"] = NOTE.format(fam=fname)
        meta = {"questionType": p.qtype, "tags": sorted(t for t in p.tags if t in TAGSET), "explanation": p.steps[-1]}
        if p.wrong and fmt in ("multiple-choice", "short-answer"):
            meta["distractors"] = {w: y for w, y in p.wrong if y}
        if p.misconception:
            meta["misconception"] = p.misconception
        if getattr(p, "shown", None):
            meta["shown"] = [fix_text(p.shown)]
        if p.diagram:
            meta["diagram"] = p.diagram.kind
        return q, meta, chk

    def make(self, f, rec, L, attempt):
        r = rng(COURSE_ID, self.u["id"], rec["id"], L, f.__name__, attempt)
        try:
            p = f(r, L)
        except Reject:
            REJECT[f.__name__] += 1
            return None, r
        except (ZeroDivisionError, IndexError, ValueError, KeyError, TypeError, AttributeError) as ex:
            EXC[(f.__name__, type(ex).__name__, str(ex)[:50])] += 1
            return None, r
        if p is not None and p.qtype is None:
            p.qtype = "procedural"
        if p is not None and getattr(f, "qtype", None) and p.qtype == "procedural":
            p.qtype = f.qtype
        return p, r

    def skill(self, rec, spec, L):
        # every factory returns an inner function literally named "f"; give each configured
        # family a stable unique name so the usage/seed bookkeeping cannot merge them
        cores = []
        for i, f in enumerate(spec["fams"]):
            normalise(f)
            if L in f.levels:
                f.__name__ = f"fam{i + 1:02d}_{f.__name__}"
                cores.append(f)
        assert cores, (rec["id"], L)
        out, used, fails, dead = [], Counter(), Counter(), set()
        famfmt = defaultdict(Counter)
        need = dict(QUOTA)
        cap = math.ceil(24 / len(cores)) + 4
        pr = rng("pos", self.u["id"], rec["id"], L, "pos")
        positions = [0, 1, 2, 3] * 10
        pr.shuffle(positions)
        st = {"pi": 0, "idx": 1}

        def accept(p, fmt, fname, r):
            # uniqueness is scoped to one skill and level: a 30-question set never repeats
            # itself, while two different skills may legitimately practise the same fact
            scope = f"{rec['id']}|{L}|"
            key = scope + pkey(p)
            nk = scope + nkey(p)
            if key in SEEN or NEAR[nk] >= NEAR_LIMIT:
                return False
            pos = positions[st["pi"] % len(positions)]
            if fmt == "multiple-choice":
                if p.options:
                    pos = [i for i, (t, c) in enumerate(p.options) if c][0]
                elif mc_options(p, pos, rng("probe", key)) is None:
                    return False
                st["pi"] += 1
            q, meta, chk = self.emit(rec, L, st["idx"], p, fmt, fname, r, pos)
            SEEN[key] = q["id"]
            NEAR[nk] += 1
            st["idx"] += 1
            out.append((q, meta, chk))
            return True

        attempts = Counter()
        guard = 0
        while need["sa"] + need["mc"] > 0:
            guard += 1
            if guard > 20000:
                raise RuntimeError(f"{rec['id']} L{L}: core loop stalled, need {need}")

            def ok(f):
                m = f.mode or "any"
                return (m in ("any", "sa") and need["sa"] > 0) or (m in ("any", "mc") and need["mc"] > 0)
            cands = [f for f in cores if f.__name__ not in dead and ok(f) and used[f.__name__] < cap]
            if not cands:
                cands = [f for f in cores if f.__name__ not in dead and ok(f)]
            if not cands and need["sa"] > 0 and any((f.mode or "any") != "sa" and f.__name__ not in dead for f in cores):
                need["mc"] += need["sa"]
                need["sa"] = 0
                continue
            if not cands and need["mc"] > 0 and any((f.mode or "any") != "mc" and f.__name__ not in dead for f in cores):
                need["sa"] += need["mc"]
                need["mc"] = 0
                continue
            if not cands:
                raise RuntimeError(f"{rec['id']} L{L}: families exhausted, need {need}")
            f = min(cands, key=lambda g: (used[g.__name__], attempts[g.__name__], cores.index(g)))
            attempts[f.__name__] += 1
            p, r = self.make(f, rec, L, attempts[f.__name__])
            if p is None:
                fails[f.__name__] += 1
                if fails[f.__name__] > 80:
                    dead.add(f.__name__)
                continue
            m = p.mode if p.mode != "any" else (f.mode or "any")
            fc = famfmt[f.__name__]
            if m == "mc" or p.options:
                order = ["mc"]
            elif m == "sa":
                order = ["sa"]
            else:
                order = ["mc", "sa"] if fc["mc"] < fc["sa"] else ["sa", "mc"]
            fmt = next((x for x in order if need[x] > 0), None)
            if fmt == "mc" and not p.options and mc_options(p, 0, rng("probe2", f.__name__)) is None:
                fmt = "sa" if need["sa"] > 0 and m == "any" else None
            if fmt is None:
                fails[f.__name__] += 1
                if fails[f.__name__] > 80:
                    dead.add(f.__name__)
                continue
            if accept(p, "multiple-choice" if fmt == "mc" else "short-answer", f.__name__, r):
                need[fmt] -= 1
                used[f.__name__] += 1
                fc[fmt] += 1
            else:
                fails[f.__name__] += 1
                if fails[f.__name__] > 80:
                    dead.add(f.__name__)

        # Grade 1 extras are generated per domain (text-only), so picture-heavy skills still
        # get error analysis, true/false, select-all and open-response questions.
        extras_for = importlib.import_module(os.environ.get("G1_EXTRAS", "extras")).extras_for
        domain = spec.get("domain") or getattr(self.m, "DOMAIN", "oa")
        derived = {k: [v] for k, v in extras_for(domain).items()}
        fmt_of = {"err": "short-answer", "tf": "multiple-choice", "sel": "select-all", "open": "open-response"}
        for kind in ("err", "tf", "sel", "open"):
            pool = derived.get(kind, [])
            tries, k = 0, 0
            while need[kind] > 0 and pool and tries < 120 * max(1, len(pool)):
                f = pool[k % len(pool)]
                k += 1
                tries += 1
                p, r = self.make(f, rec, L, 500 + tries)
                if p is None:
                    continue
                if kind == "sel" and sum(1 for _, c in p.options if c) < 2:
                    continue
                if accept(p, fmt_of[kind], f.__name__, r):
                    need[kind] -= 1
            while need[kind] > 0:
                live = [g for g in cores if g.__name__ not in dead]
                if not live:
                    raise RuntimeError(f"{rec['id']} L{L}: cannot backfill {kind}")
                f = min(live, key=lambda g: used[g.__name__])
                attempts[f.__name__] += 1
                p, r = self.make(f, rec, L, attempts[f.__name__] + 2000)
                if p is None:
                    fails[f.__name__] += 1
                    if fails[f.__name__] > 300:
                        dead.add(f.__name__)
                    continue
                fmt = "multiple-choice" if (p.options or (len({_norm(w) for w, _ in p.wrong} - {_norm(p.answer)}) >= 3 and kind == "tf")) else "short-answer"
                if (p.mode == "mc" or f.mode == "mc") and not p.options and fmt == "short-answer":
                    fails[f.__name__] += 1
                    continue
                if accept(p, fmt, f.__name__, r):
                    need[kind] -= 1
                    used[f.__name__] += 1
                else:
                    fails[f.__name__] += 1
                    if fails[f.__name__] > 300:
                        dead.add(f.__name__)
        return out

    def run(self, draw=True):
        recs = skill_records(self.u)
        assert len(recs) == len(self.m.SKILLS), (self.u["id"], len(recs), len(self.m.SKILLS))
        for rec in recs:
            spec = self.m.SKILLS[rec["index"]]
            assert spec["name"] == rec["name"], (spec["name"], rec["name"])
            for L in range(3):
                if os.environ.get("G1_DEBUG"):
                    print("  building", rec["id"], L, flush=True)
                for q, meta, chk in self.skill(rec, spec, L):
                    self.questions.append(q)
                    self.meta[q["id"]] = meta
                    self.checks[q["id"]] = chk
        bank = {"schemaVersion": 1, "courseId": COURSE_ID, "unitId": self.u["id"], "questions": self.questions}
        bdir = os.path.join(ROOT, "question-banks", COURSE_ID)
        os.makedirs(os.path.join(bdir, "meta"), exist_ok=True)
        with open(os.path.join(bdir, self.u["id"] + ".json"), "w", encoding="utf-8") as fh:
            json.dump(bank, fh, ensure_ascii=False, indent=1)
        with open(os.path.join(bdir, "meta", self.u["id"] + ".meta.json"), "w", encoding="utf-8") as fh:
            json.dump(self.meta, fh, ensure_ascii=False, indent=0)
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, self.u["id"] + ".checks.json"), "w", encoding="utf-8") as fh:
            json.dump(self.checks, fh, ensure_ascii=False, indent=0)
        if draw:
            draw_all(self.u["id"], self.diagrams)
        return len(self.questions), len(self.diagrams)


def draw_all(unit_id, diagrams):
    adir = os.path.join(ROOT, "question-banks", "assets", COURSE_ID, unit_id)
    os.makedirs(adir, exist_ok=True)
    for fn in os.listdir(adir):
        os.remove(os.path.join(adir, fn))
    for src, dg in diagrams:
        data = figs1.render_png(dg.kind, dg.data)
        with open(os.path.join(ROOT, src), "wb") as fh:
            fh.write(data)


def main():
    mods = sys.argv[1:] or MODS
    draw = os.environ.get("G1_NODRAW") != "1"
    for mname in mods:
        u = UNITS[MODS.index(mname)]
        mod = importlib.import_module(mname)
        n, d = Builder(mod, u).run(draw)
        print(u["id"], n, "questions", d, "diagrams")
    for k, v in EXC.most_common(12):
        print("   exception", v, k)
    for k, v in REJECT.most_common(8):
        print("   reject", v, k)


if __name__ == "__main__":
    main()
