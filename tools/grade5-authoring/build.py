"""Build the Grade 5 (math5) question banks from the unit family modules.

Usage: python3 build.py [unit-module ...]          (default: all units, in order; always deterministic)
Writes (repository-relative):
  question-banks/math5/<unit>.json                 bank (schemaVersion 1, the shared schema)
  question-banks/math5/meta/<unit>.meta.json       per-question type, tags, distractor reasons, misconception
  question-banks/assets/math5/<unit>/<qid>.png     diagrams (rendered from SVG drawn by figs.py)
  tools/grade5-authoring/out/<unit>.checks.json    check data for the independent verifier
Per skill and level: 30 questions = 12 short answer + 12 multiple choice (core families) + 3 error analysis
+ 1 true/false with reasoning + 1 select all + 1 open response / matching. Extras are derived from the core families.
"""
import importlib, io, json, os, re, subprocess, sys, math
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "units"))
from g5lib import Reject, rng, LEVELS, err_of, tf_of, select_of, open_of, match_of, _norm
from outline import UNITS, COURSE_ID, PREFIX, skill_records
import figs

ROOT = os.environ.get("G5_ROOT", os.path.abspath(os.path.join(HERE, "..", "..")))
MODS = ["u01_place_value", "u02_mult_div", "u03_decimals", "u04_expressions", "u05_fraction_add", "u06_fraction_mult",
        "u07_measurement", "u08_volume", "u09_coordinate", "u10_shapes", "u11_data"]
QUOTA = {"sa": 12, "mc": 12, "err": 3, "tf": 1, "sel": 1, "open": 1}
NOTE = ("Original Claude-authored Grade 5 item (family: {fam}). Answer computed by the authoring script and re-derived by the "
        "independent verifier (tools/grade5-authoring/verify.py).")
TAGSET = {"modeling", "misconception", "challenge", "graph", "reasoning", "error-analysis", "connections", "multiple-representations", "multistep"}
SEEN, NEAR, EXC = {}, Counter(), Counter()


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
    return re.sub(r"\d+", "#", k) + "|" + ",".join(sorted(re.findall(r"\d+", k)))


def mc_options(p, pos, r):
    if p.options:
        return [{"text": t, "correct": bool(c)} for t, c in p.options]
    seen, ds = {_norm(p.answer)}, []
    for w, _ in p.wrong:
        if _norm(w) in seen or not w.strip():
            continue
        seen.add(_norm(w))
        ds.append(w)
    if len(ds) < 3:
        return None
    ds = ds[:3]
    r.shuffle(ds)
    ds.insert(pos, p.answer)
    return [{"text": t, "correct": i == pos} for i, t in enumerate(ds)]


SING = {"meters": "meter", "liters": "liter", "kilometers": "kilometer", "centimeters": "centimeter", "pounds": "pound", "feet": "foot",
        "inches": "inch", "yards": "yard", "miles": "mile", "cups": "cup", "quarts": "quart", "pints": "pint", "gallons": "gallon",
        "ounces": "ounce", "grams": "gram", "kilograms": "kilogram", "milliliters": "milliliter", "millimeters": "millimeter",
        "hours": "hour", "minutes": "minute", "units": "unit", "boxes": "box", "buses": "bus", "vans": "van", "cars": "car",
        "pieces": "piece", "days": "day", "weeks": "week", "tons": "ton", "seconds": "second", "cartons": "carton", "bouquets": "bouquet",
        "rows": "row", "students": "student", "cards": "card", "marbles": "marble", "crayons": "crayon", "books": "book"}
SING.update({"sandwiches": "sandwich", "pizzas": "pizza", "pans": "pan", "pies": "pie", "bags": "bag", "servings": "serving", "feeders": "feeder"})
PLUR = {v: k for k, v in SING.items()}
_SING_RE = re.compile(r"(?<![\d.,/])(1) (" + "|".join(SING) + r")\b")
_FRAC_RE = re.compile(r"(?<![\d/])(?<!\d )(\d+)/(\d+) (" + "|".join(SING) + r")\b")
_MIX_RE = re.compile(r"(?<![\d/])(\d+) (\d+)/(\d+) (" + "|".join(PLUR) + r")\b")


PHRASES = [(r"What number do the base\u2011ten blocks show\?", "What number is shown by the base\u2011ten blocks?"),
           (r"What decimal do the blocks show\?", "What decimal is shown by the blocks?"),
           (r"How much do they weigh together\?", "What is their total weight?"),
           (r"How many miles do the buses travel in all\?", "What is the total number of miles the buses travel?"),
           (r"Which attribute do ALL (\w+) have\?", r"Which attribute is true for ALL \1?"),
           (r"Which attribute do (.+?) ALL share\?", r"Which attribute is shared by ALL of these: \1?"),
           (r"\bbooks go on each shelf", "books are placed on each shelf"),
           (r"\bgo up to the point", "move up to the point"),
           (r"\bhow many X's go above", "how many X marks belong above"),
           (r"X's", "X marks"),
           (r"instead of an estimate", "instead of estimating"),
           (r"\bdo you plot\b", "can you plot"),
           (r"How do you change", "How can you change"),
           (r"\b(\d+)ths\b", lambda m: {"6": "sixths", "8": "eighths", "10": "tenths", "12": "twelfths", "4": "fourths", "9": "ninths", "5": "fifths", "7": "sevenths"}[m.group(1)]),
           (r"Right/left", "Moving right or left"), (r"up/down", "moving up or down"),
           (r"Which attribute do (\w+) and (\w+) share that (\w+) do not always have\?", r"Which attribute is shared by \1 and \2 but not always by \3?"),
           (r"fencing go around it", "fencing are needed to surround it"),
           (r"\bB's rule\b", "the rule for Pattern B"), (r"\bA's rule\b", "the rule for Pattern A"),
           (r"\b([Aa])n? (?=[\d$])", lambda m: ("One " if m.group(1) == "A" else "one ")),
           (r"left over do not make another", "left over cannot make another"),
           (r"Gaps and overlaps do not change the count\.", "Gaps and overlaps leave the count unchanged."),
           (r"that do not overlap", "that share no space"),
           (r"How much do (.+?) cost\?", r"What is the cost of \1?"), (r"What do (\d+) sheets cost\?", r"What is the cost of \1 sheets?"),
           (r"What do both cost\?", "What is the cost of both?"), (r"How much more did (\w+) do than (\w+)\?", r"How much more was done by \1 than by \2?"),
           (r"\bof a (pizza|pie|cake|pan|bag|book|jar|box|gift|movie)\b", r"of one \1"), (r"\b([Oo])f a (?=[a-z]{3,})", r"\1f the "),
           (r"\b([Aa])nd a (?=[a-z]{3,})", r"\1nd one "), (r"\bwith a common\b", "using a common"), (r"\bwith a (?=[a-z]{3,})", "that has a "),
           (r"\bfor a (shelf|bow)\b", r"to make a \1"), (r"\b1/(\d+)s\b", r"pieces of size 1/\1"),
           (r"\bdid not go down\b", "did not move down"), (r"the known prism's volume", "the volume of the known prism"), (r"grouping symbols do not change the value", "grouping symbols leave the value unchanged"), (r"Both (\d)s have", r"Both digits \1 have"),
           (r"forgot to subtract a regrouped ten / added an extra ten", "added an extra regrouped ten"), (r"\b(\d)s in the\b", r"digits \1 in the")]
NBH = "\u2011"   # non-breaking hyphen: the site's math display turns ASCII '-' into a minus sign


def polish(t):
    t = re.sub(r"(?<=[A-Za-z0-9])-(?=[A-Za-z])|(?<=[A-Za-z])-(?=[A-Za-z0-9])", NBH, t)
    for a, b in PHRASES:
        t = re.sub(a, b, t)
    t = re.sub(r"\b([Aa]) (?=(?:8|11|18)(?![\d,./])|8\d)", lambda m: m.group(1) + "n ", t)
    return t


def fix_text(t):
    if not isinstance(t, str):
        return t
    t = polish(t)
    t = _SING_RE.sub(lambda m: m.group(1) + " " + SING[m.group(2)], t)
    t = _FRAC_RE.sub(lambda m: f"{m.group(1)}/{m.group(2)} " + (SING[m.group(3)] if int(m.group(1)) < int(m.group(2)) else m.group(3)), t)
    t = _MIX_RE.sub(lambda m: f"{m.group(1)} {m.group(2)}/{m.group(3)} {PLUR[m.group(4)]}", t)
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
    """Keep check data in step with fix_text (units in expected answers, claim tables)."""
    if not isinstance(c, dict):
        return c
    out = {}
    for k, v in c.items():
        if k == "table":
            out[k] = {fix_text(t): fix_chk(e) for t, e in v.items()}
        elif k in ("unit", "shown", "answer", "accept", "good"):
            out[k] = [fix_text(x) for x in v] if isinstance(v, list) else fix_text(v)
        elif isinstance(v, dict):
            out[k] = fix_chk(v)
        else:
            out[k] = v
    return out


class Builder:
    def __init__(self, unit_mod, unit):
        self.m, self.u = unit_mod, unit
        self.questions, self.meta, self.checks, self.diagrams = [], {}, {}, []

    def emit(self, rec, L, idx, p, fmt, fname, r, pos=None):
        lv = LEVELS[L]
        qid = f"{PREFIX}-{self.u['abbr']}-s{rec['index']:02d}-{lv}-{idx:03d}"
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
        meta = {"questionType": p.qtype, "tags": sorted(t for t in p.tags if t in TAGSET),
                "explanation": p.steps[-1]}
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
            return None, r
        except (ZeroDivisionError, IndexError, ValueError, KeyError, TypeError, AttributeError) as ex:
            EXC[(f.__name__, type(ex).__name__, str(ex)[:60])] += 1
            return None, r
        if p is not None and p.qtype is None:
            p.qtype = "procedural"
        if p is not None and getattr(f, "qtype", None) and p.qtype == "procedural":
            p.qtype = f.qtype
        return p, r

    def skill(self, rec, spec, L):
        cores = [f for f in spec["fams"] if L in f.levels]
        assert cores, (rec["id"], L)
        out, used, fails, dead = [], Counter(), Counter(), set()
        famfmt = defaultdict(Counter)
        need = dict(QUOTA)
        cap = math.ceil(24 / len(cores)) + 2
        pr = rng("pos", self.u["id"], rec["id"], L)
        positions = [0, 1, 2, 3] * 8
        pr.shuffle(positions)
        st = {"pi": 0, "idx": 1}

        def accept(p, fmt, fname, r, kind):
            key = pkey(p)
            nk = nkey(p) + "|" + str(p.answer)
            if key in SEEN or NEAR[nk] >= 1:
                return False
            pos = positions[st["pi"] % len(positions)]
            if fmt == "multiple-choice":
                if p.options:
                    pos = [i for i, (t, c) in enumerate(p.options) if c][0]
                elif mc_options(p, pos, rng("probe", key)) is None:
                    return False
                else:
                    st["pi"] += 1
            q, meta, chk = self.emit(rec, L, st["idx"], p, fmt, fname, r, pos)
            SEEN[key] = q["id"]
            NEAR[nk] += 1
            st["idx"] += 1
            out.append((q, meta, chk))
            return True

        # core: short answer + multiple choice
        attempts = Counter()
        while need["sa"] + need["mc"] > 0:
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
                if fails[f.__name__] > 60:
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
            if fmt == "mc" and not p.options and len({_norm(w) for w, _ in p.wrong} - {_norm(p.answer)}) < 3:
                fmt = "sa" if need["sa"] > 0 and m == "any" else None
            if fmt is None:
                fails[f.__name__] += 1
                if fails[f.__name__] > 60:
                    dead.add(f.__name__)
                continue
            if accept(p, "multiple-choice" if fmt == "mc" else "short-answer", f.__name__, r, "core"):
                need[fmt] -= 1
                used[f.__name__] += 1
                fc[fmt] += 1
            else:
                fails[f.__name__] += 1
                if fails[f.__name__] > 60:
                    dead.add(f.__name__)
        # derived extras
        plain = [f for f in cores if (f.mode or "any") != "mc"]
        derived = {"err": [err_of(f) for f in plain], "tf": [tf_of(f) for f in plain],
                   "sel": [select_of(f) for f in plain], "open": [match_of(f) if i % 2 else open_of(f) for i, f in enumerate(plain)]}
        for extra in spec.get("extra", []):
            if L in extra.levels:
                derived.setdefault(extra.kind, []).insert(0, extra)
        fmt_of = {"err": "short-answer", "tf": "multiple-choice", "sel": "select-all", "open": "open-response"}
        for kind in ("err", "tf", "sel", "open"):
            pool = derived.get(kind, [])
            tries = 0
            k = 0
            while need[kind] > 0 and pool and tries < 60 * max(1, len(pool)):
                f = pool[k % len(pool)]
                k += 1
                tries += 1
                p, r = self.make(f, rec, L, 500 + tries)
                if p is None:
                    continue
                fmt = fmt_of[kind]
                if kind == "sel" and sum(1 for _, c in p.options if c) < 2:
                    continue
                if accept(p, fmt, f.__name__, r, kind):
                    need[kind] -= 1
            # backfill a failed extra with more core items, so every skill and level still has 30
            while need[kind] > 0:
                live = [g for g in cores if g.__name__ not in dead]
                if not live:
                    raise RuntimeError(f"{rec['id']} L{L}: cannot backfill {kind}")
                f = min(live, key=lambda g: used[g.__name__])
                attempts[f.__name__] += 1
                p, r = self.make(f, rec, L, attempts[f.__name__] + 2000)
                if p is None:
                    fails[f.__name__] += 1
                    if fails[f.__name__] > 200:
                        dead.add(f.__name__)
                    continue
                fmt = "multiple-choice" if (p.options or (len({_norm(w) for w, _ in p.wrong} - {_norm(p.answer)}) >= 3 and kind == "tf")) else "short-answer"
                if (p.mode == "mc" or f.mode == "mc") and not p.options and fmt == "short-answer":
                    fails[f.__name__] += 1
                    continue
                if accept(p, fmt, f.__name__, r, "backfill"):
                    need[kind] -= 1
                    used[f.__name__] += 1
                else:
                    fails[f.__name__] += 1
                    if fails[f.__name__] > 200:
                        dead.add(f.__name__)
        return out

    def run(self, draw=True):
        recs = skill_records(self.u)
        assert len(recs) == len(self.m.SKILLS), (self.u["id"], len(recs), len(self.m.SKILLS))
        for rec in recs:
            spec = self.m.SKILLS[rec["index"]]
            assert spec["name"] == rec["name"], (spec["name"], rec["name"])
            for L in range(3):
                if os.environ.get("G5_DEBUG"):
                    print("  building", rec["id"], L, flush=True)
                for q, meta, chk in self.skill(rec, spec, L):
                    self.questions.append(q)
                    self.meta[q["id"]] = meta
                    self.checks[q["id"]] = chk
        bank = {"schemaVersion": 1, "courseId": COURSE_ID, "unitId": self.u["id"], "questions": self.questions}
        bdir = os.path.join(ROOT, "question-banks", COURSE_ID)
        os.makedirs(os.path.join(bdir, "meta"), exist_ok=True)
        json.dump(bank, open(os.path.join(bdir, self.u["id"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(self.meta, open(os.path.join(bdir, "meta", self.u["id"] + ".meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
        json.dump(self.checks, open(os.path.join(HERE, "out", self.u["id"] + ".checks.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        if draw:
            draw_all(self.u["id"], self.diagrams)
        return len(self.questions), len(self.diagrams)


def draw_all(unit_id, diagrams):
    from PIL import Image
    adir = os.path.join(ROOT, "question-banks", "assets", COURSE_ID, unit_id)
    os.makedirs(adir, exist_ok=True)
    for fn in os.listdir(adir):
        os.remove(os.path.join(adir, fn))
    for src, dg in diagrams:
        s = figs.render(dg.kind, dg.data)
        png = subprocess.run(["rsvg-convert", "-z", "1.25"], input=s.encode(), capture_output=True, check=True).stdout
        im = Image.open(io.BytesIO(png)).convert("RGB").quantize(colors=96, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        im.save(os.path.join(ROOT, src), optimize=True)


def main():
    mods = sys.argv[1:] or MODS
    draw = os.environ.get("G5_NODRAW") != "1"
    # prompts already published by the other units of this course stay off limits (cross-unit duplicates)
    for mname in MODS:
        if mname in mods:
            continue
        u = UNITS[MODS.index(mname)]
        bf = os.path.join(ROOT, "question-banks", COURSE_ID, u["id"] + ".json")
        if os.path.exists(bf):
            for q in json.load(open(bf, encoding="utf-8"))["questions"]:
                SEEN[" ".join(q["prompt"].lower().split())] = q["id"]
    for mname in mods:
        u = UNITS[MODS.index(mname)]
        mod = importlib.import_module(mname)
        n, d = Builder(mod, u).run(draw)
        print(u["id"], n, "questions", d, "diagrams")
    for k, v in EXC.most_common(15):
        print("   exception", v, k)


if __name__ == "__main__":
    main()
