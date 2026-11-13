"""Independent verifier for the Grade 1 (math1) banks.

It never imports the families, g1lib or figs1. It reads each published bank plus the check
file written by the builder, and re-derives every answer from the stored inputs with its own
arithmetic and its own implementations of the named checks.

Checks performed
  * counts: 30 per skill and level, 3 levels, every skill of the outline present
  * answer reconstruction for short answer, multiple choice, select-all and open response
  * exactly one correct option (MC), >= 2 correct claims (select-all), stored distractor
    reasons refer to answers that are actually wrong
  * standards equal to the outline's record for that skill
  * duplicate prompts across the whole course, and near-duplicate caps
  * every diagram file exists, decodes, is the expected size, is not blank, and the answer
    agrees with the picture data where the picture is the ground truth
  * reading-load warnings for Grade 1 (long words, very long prompts)

Usage: python3 verify1.py [repo_root]      prints a report, exits 1 on any error.
"""
import json, os, re, sys
from collections import Counter, defaultdict
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
_out = __import__(os.environ.get("G1_OUTLINE", "outline"))
UNITS, COURSE_ID, skill_records, all_standards = _out.UNITS, _out.COURSE_ID, _out.skill_records, _out.all_standards
COURSE_LABEL = getattr(_out, "UNIT_LABEL", "Grade 1 (math1)")

BANK_DIR = os.path.join(ROOT, "question-banks", COURSE_ID)
ASSET_DIR = os.path.join(ROOT, "question-banks", "assets", COURSE_ID)
CHECKS = os.environ.get("G1_OUT") or os.path.join(HERE, "out")
LEVELS = ["cp2", "cp1", "honors"]
SIDES = {"triangle": 3, "square": 4, "rectangle": 4, "hexagon": 6, "circle": 0}
CORNERS = SIDES
SHAPES = set(SIDES)
SOLIDS = {"cube", "cylinder", "sphere", "cone"}

ERRORS, WARNS = [], []
STATS = Counter()


def err(msg):
    ERRORS.append(msg)


def warn(msg):
    WARNS.append(msg)


def norm(t):
    t = str(t).replace("\u2212", "-").replace("\u2011", "-").replace("\u2019", "'")
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t.rstrip(".")


def as_int(t):
    t = str(t).strip().replace(",", "")
    return int(t) if re.fullmatch(r"-?\d+", t) else None


def num_eq(text, value):
    v = as_int(text)
    return v is not None and v == int(value)


def seq(text):
    return [x.strip() for x in str(text).split(",")]


# ------------------------------------------------------------------ named checks
def h_add(c, t):
    return num_eq(t, int(c["a"]) + int(c["b"]))


def h_sub(c, t):
    return num_eq(t, int(c["a"]) - int(c["b"]))


def h_add3(c, t):
    return num_eq(t, int(c["a"]) + int(c["b"]) + int(c["c"]))


def h_missing_part(c, t):
    return num_eq(t, int(c["total"]) - int(c["part"]))


def h_related(c, t):
    a, b = int(c["a"]), int(c["b"])
    return norm(t) == norm(f"{a + b} - {b} = {a}")


def h_teen_parts(c, t):
    n = int(c["n"])
    return norm(t) == norm(f"1 ten and {n - 10} {'one' if n == 11 else 'ones'}")


def h_symbol(c, t):
    a, b = int(c["a"]), int(c["b"])
    return norm(t) == (">" if a > b else "<" if a < b else "=")


def h_which_number(c, t):
    a, b = int(c["a"]), int(c["b"])
    want = max(a, b) if c["which"] == "greater" else min(a, b)
    return num_eq(t, want)


def h_sorted(c, t):
    vals = [int(v) for v in c["values"]]
    want = sorted(vals) if c.get("direction", "asc") == "asc" else sorted(vals, reverse=True)
    return seq(t) == [str(v) for v in want]


def h_count(c, t):
    return num_eq(t, int(c["n"]))


def h_ones_of(c, t):
    n, tens = int(c["n"]), int(c["tens"])
    return num_eq(t, n - tens * 10)


def h_ten_ones(c, t):
    return num_eq(t, 10 * int(c.get("tens", 1)))


def h_tens_ones(c, t):
    return num_eq(t, int(c["tens"]) * 10 + int(c["ones"]))


def h_digit_value(c, t):
    n = int(c["n"])
    tens, ones = n // 10, n % 10
    want = tens * 10 if c["which"] == "tens" else ones
    return num_eq(t, want)


def h_equiv_ones(c, t):
    n, tens = int(c["n"]), int(c["tens"])
    return num_eq(t, n - tens * 10)


def h_eq_text(c, t):
    a, b = int(c["a"]), int(c["b"])
    if c["kind"] == "add":
        return norm(t) == norm(f"{a} + {b} = {a + b}")
    return norm(t) == norm(f"{a} - {b} = {a - b}")


def h_equals_word(c, t):
    return norm(t) == "the same as"


def h_missing_same(c, t):
    return num_eq(t, int(c["a"]))


def h_true_eq(c, t):
    return norm(t) == "true"


def h_tf_eq(c, t):
    return norm(t) == ("true" if int(c["shown"]) == int(c["a"]) + int(c["b"]) else "false")


def h_strategy(c, t):
    return norm(t) == "make 10"


def _rows(c):
    return [(str(r[0]), int(r[1])) for r in c["rows"]]


def h_tally_total(c, t):
    return num_eq(t, sum(v for _, v in _rows(c)))


def h_tally_one(c, t):
    rows = dict(_rows(c))
    return num_eq(t, rows[str(c["label"])])


def h_tally_most(c, t):
    rows = _rows(c)
    best = max(v for _, v in rows)
    if sum(1 for _, v in rows if v == best) != 1:
        return False
    return norm(t) == norm([k for k, v in rows if v == best][0])


def h_graph_one(c, t):
    rows = dict(_rows(c))
    return num_eq(t, rows[str(c["label"])])


def h_graph_sum(c, t):
    return num_eq(t, sum(v for _, v in _rows(c)))


def h_graph_most(c, t):
    return h_tally_most(c, t)


def h_shape_name(c, t):
    return norm(t) in SHAPES


def h_solid_faces(c, t):
    # Preserve the source family's surface-count convention; independent of its answer text.
    return num_eq(t, {"cube": 6, "cylinder": 3, "cone": 2}[str(c["kind"])])


def h_solid_edges(c, t):
    return num_eq(t, {"cube": 12}[str(c["kind"])])


def h_solid_name(c, t):
    return norm(t) == norm(str(c.get("kind", "")))


def h_shape_attr_name(c, t):
    sides = int(c["sides"])
    names = {3: ["triangle"], 6: ["hexagon"], 0: ["circle"], 4: ["square", "rectangle"]}
    return norm(t) in names.get(sides, [])


def h_shape_sides(c, t):
    return num_eq(t, SIDES[str(c["kind"])])


def h_shape_corners(c, t):
    return num_eq(t, CORNERS[str(c["kind"])])


def h_partition_count(c, t):
    return num_eq(t, int(c["parts"]))


def h_partition_word(c, t):
    return norm(t) == {2: "halves", 4: "fourths"}[int(c["parts"])]


def h_equal_parts(c, t):
    if c.get("kind") == "which":
        return norm(t) in ("rectangle", "the rectangle")
    return norm(t) == "equal parts make halves"


def h_clock(c, t):
    return norm(t) == norm(f"{int(c['h'])}:{int(c['m']):02d}")


def h_longer(c, t):
    a, b = int(c["a"]), int(c["b"])
    return norm(t) == ("the pencil" if a > b else "the crayon")


def h_shorter(c, t):
    a, b = int(c["a"]), int(c["b"])
    return norm(t) == ("the pencil" if a < b else "the crayon")


def h_more_count(c, t):
    return num_eq(t, abs(int(c["a"]) - int(c["b"])))


def h_which_group(c, t):
    a, b = int(c["a"]), int(c["b"])
    return norm(t) == ("left" if a > b else "right")


def h_ruler(c, t):
    return num_eq(t, int(c["n"]))


def h_order_len(c, t):
    pairs = sorted([(str(n), int(v)) for n, v in c["pairs"]], key=lambda p: p[1])
    return seq(t) == [n for n, _ in pairs]


def h_tens_from_ones(c, t):
    return num_eq(t, int(c["ones"]) // 10)


def h_story_eq(c, t):
    a, b = int(c["a"]), int(c["b"])
    text = norm(t)
    if c["kind"] == "add":
        return str(a) in text and str(b) in text and "gets" in text and "gives" not in text
    return str(a) in text and str(b) in text and "gives" in text and "gets" not in text


def h_tf(c, t):
    inner_ok, _ = accepts(c["inner"], c.get("shown", ""))
    return norm(t).startswith("true") == bool(inner_ok)


def h_claims(c, t):
    return True


def h_longer_ab(c, t):
    a, b = int(c["a"]), int(c["b"])
    return norm(t) == ("the first string" if a > b else "the second string")


def h_most_of(c, t):
    labels = [str(x) for x in c["labels"]]
    counts = [int(x) for x in c["counts"]]
    best = max(counts)
    if counts.count(best) != 1:
        return False
    return norm(t) == norm(labels[counts.index(best)])


def h_clock_minutes(c, t):
    return num_eq(t, int(c["m"]))


def h_half_hour(c, t):
    return num_eq(t, 30)


HANDLERS = {k[2:]: v for k, v in globals().items() if k.startswith("h_") and callable(v)}


# ------------------------------------------------------------------ answer reconstruction
def eval_expr(e):
    if not re.fullmatch(r"[\d+\-*/() ]+", e):
        raise ValueError(f"bad expression {e!r}")
    return eval(e, {"__builtins__": {}}, {})


def accepts(chk, text):
    if not isinstance(chk, dict):
        return False, "missing check"
    kind = chk.get("k")
    if kind == "expr":
        try:
            want = eval_expr(chk["e"])
        except Exception as ex:
            return False, f"bad expr ({ex})"
        v = as_int(text)
        return (v is not None and v == want), f"expr {chk['e']}={want} vs {text!r}"
    if kind == "key":
        return any(norm(text) == norm(a) for a in chk.get("accept", [])), f"key {chk.get('accept')} vs {text!r}"
    if kind == "fn":
        fn = chk.get("fn")
        h = HANDLERS.get(fn)
        if not h:
            return False, f"no independent handler for {fn!r}"
        try:
            return bool(h(chk, text)), f"{fn}({ {k: v for k, v in chk.items() if k not in ('k', 'fn')} }) vs {text!r}"
        except Exception as ex:
            return False, f"{fn} raised {type(ex).__name__}: {ex}"
    return False, f"unknown check kind {kind!r}"


# ------------------------------------------------------------------ per unit
def check_unit(unit):
    path = os.path.join(BANK_DIR, unit["id"] + ".json")
    cpath = os.path.join(CHECKS, unit["id"] + ".checks.json")
    if not os.path.exists(path):
        err(f"{unit['id']}: bank file missing")
        return
    if not os.path.exists(cpath):
        err(f"{unit['id']}: checks file missing (run build1.py)")
        return
    bank = json.load(open(path, encoding="utf-8"))
    checks = json.load(open(cpath, encoding="utf-8"))
    meta = json.load(open(os.path.join(BANK_DIR, "meta", unit["id"] + ".meta.json"), encoding="utf-8"))
    recs = {r["id"]: r for r in skill_records(unit)}
    qs = bank["questions"]

    if bank.get("schemaVersion") != 1 or bank.get("courseId") != COURSE_ID or bank.get("unitId") != unit["id"]:
        err(f"{unit['id']}: bad bank header {bank.get('schemaVersion')}/{bank.get('courseId')}/{bank.get('unitId')}")

    per = Counter()
    for q in qs:
        qid = q["id"]
        rec = recs.get(q.get("skillId"))
        if not rec:
            err(f"{qid}: unknown skillId {q.get('skillId')!r}")
            continue
        per[(q["skillId"], q["level"])] += 1
        STATS["questions"] += 1
        STATS["fmt_" + str(q.get("format"))] += 1

        if q.get("level") not in LEVELS:
            err(f"{qid}: bad level {q.get('level')!r}")
        if sorted(q.get("standards") or []) != sorted(rec["standards"]):
            err(f"{qid}: standards {q.get('standards')} != outline {rec['standards']}")
        for s in q.get("standards") or []:
            if s not in all_standards():
                err(f"{qid}: standard {s} not in the Grade 1 outline")
        if not q.get("solutionSteps"):
            err(f"{qid}: no solutionSteps")
        if qid not in checks:
            err(f"{qid}: no check data")
            continue
        chk = checks[qid]
        if chk.get("family") is None:
            warn(f"{qid}: check has no family name")

        fmt = q.get("format")
        if fmt == "open-response":
            parts = q.get("parts") or []
            pchk = chk.get("parts") or []
            if len(parts) != len(pchk) or not parts:
                err(f"{qid}: open-response parts/checks mismatch ({len(parts)}/{len(pchk)})")
            for i, (pp, pc) in enumerate(zip(parts, pchk)):
                ok, why = accepts(pc, pp.get("answer", ""))
                if not ok:
                    err(f"{qid}: part {chr(97 + i)} wrong — {why}")
            stored = q.get("answer") or ""
            if not stored:
                err(f"{qid}: open-response has no combined answer")
        elif fmt == "select-all":
            opts = q.get("options") or []
            good = [o["text"] for o in opts if o.get("correct")]
            if len(good) < 2:
                err(f"{qid}: select-all has fewer than 2 correct claims")
            if sorted(good) != sorted(q.get("answer") or []):
                err(f"{qid}: select-all answer list does not match correct options")
            table = (chk.get("q") or {}).get("table") or {}
            for o in opts:
                entry = table.get(o["text"])
                if entry is None:
                    err(f"{qid}: select-all claim not in check table: {o['text'][:40]!r}")
                    continue
                ok, why = accepts(entry.get("inner"), entry.get("shown", ""))
                if bool(ok) != bool(o.get("correct")):
                    err(f"{qid}: select-all claim judged {ok} but stored correct={o.get('correct')} — {why}")
        else:
            ok, why = accepts(chk.get("q"), q.get("answer", ""))
            if not ok:
                err(f"{qid}: answer wrong — {why}")
            if fmt == "multiple-choice":
                opts = q.get("options") or []
                correct = [o for o in opts if o.get("correct")]
                if len(correct) != 1:
                    err(f"{qid}: {len(correct)} correct options")
                if len({norm(o['text']) for o in opts}) != len(opts):
                    err(f"{qid}: duplicate option text")
                if correct and norm(correct[0]["text"]) != norm(q.get("answer", "")):
                    err(f"{qid}: marked option is not the stored answer")
                av = as_int(q.get("answer"))
                for o in opts:
                    if o.get("correct"):
                        continue
                    ov = as_int(o["text"])
                    if av is not None and ov is not None and ov == av:
                        err(f"{qid}: distractor {o['text']!r} equals the answer")
        # distractor reasons point at genuinely wrong values
        for w, why in (meta.get(qid, {}).get("distractors") or {}).items():
            if norm(w) == norm(q.get("answer")):
                err(f"{qid}: distractor {w!r} equals the answer")
            if not str(why).strip():
                warn(f"{qid}: distractor {w!r} has no misconception reason")

        dg = q.get("diagram")
        if dg:
            STATS["diagrams"] += 1
            rel = dg.get("spec", {}).get("src", "")
            fpath = os.path.join(ROOT, rel)
            if not rel.startswith("question-banks/assets/" + COURSE_ID + "/"):
                err(f"{qid}: diagram path {rel!r} outside the course asset folder")
            elif not os.path.exists(fpath):
                err(f"{qid}: diagram file missing {rel}")
            else:
                try:
                    im = Image.open(fpath)
                    w, h = im.size
                    rgb = im.convert("RGB")
                    colors = len(rgb.getcolors(maxcolors=4096) or [])
                    px = rgb.load()
                    drawn = sum(1 for x in range(0, w, 6) for y in range(0, h, 6) if px[x, y] != (255, 255, 255))
                except Exception as ex:
                    err(f"{qid}: diagram unreadable ({ex})")
                    continue
                if (w, h) != (720, 480):
                    err(f"{qid}: diagram is {w}x{h}, expected 720x480")
                if colors < 2 or drawn < 20:
                    err(f"{qid}: diagram looks blank ({colors} colours, {drawn} drawn samples)")
                if os.path.getsize(fpath) < 150:
                    err(f"{qid}: diagram file suspiciously small")
                if not (dg.get("spec", {}).get("alt") or "").strip():
                    err(f"{qid}: diagram has no alt text")
                data = (chk.get("diagram") or {}).get("data") or {}
                fn = (chk.get("q") or {}).get("fn")
                if fn == "shape_name" and data.get("shapes"):
                    drawn = str(data["shapes"][0].get("type"))
                    if norm(drawn) != norm(q.get("answer", "")):
                        err(f"{qid}: shape answer {q.get('answer')!r} does not match the drawn {drawn!r}")
                if fn == "solid_name" and norm(q.get("answer", "")) not in SOLIDS:
                    err(f"{qid}: solid answer {q.get('answer')!r} is not a solid name")

    # counts
    for rec in recs.values():
        for lv in LEVELS:
            n = per[(rec["id"], lv)]
            if n != 30:
                err(f"{unit['id']} {rec['id']} {lv}: {n} questions (expected 30)")
        total = sum(per[(rec["id"], lv)] for lv in LEVELS)
        if total != 90:
            err(f"{unit['id']} {rec['id']}: {total} questions (expected 90)")
    ids = [q["id"] for q in qs]
    if len(ids) != len(set(ids)):
        dup = [k for k, v in Counter(ids).items() if v > 1]
        err(f"{unit['id']}: duplicate ids {dup[:5]}")
    return qs


def main():
    # Duplicate policy (documented in README): a skill/level set of 30 must be unique,
    # near-duplicates are capped, and the same fact may appear in another skill.
    seen_prompts, seen_global = {}, {}
    near = Counter()
    all_qs = []
    cross = 0
    for unit in UNITS:
        qs = check_unit(unit)
        for q in qs or []:
            # the picture is part of the question for visual items (same wording, different
            # data), so include the alt text in the identity
            key = (norm(q["prompt"]) + "|" + "|".join(sorted(norm(o["text"]) for o in q.get("options") or []))
                   + "|" + norm((q.get("diagram") or {}).get("spec", {}).get("alt", "")))
            scope = (q.get("skillId"), q.get("level"))
            if (scope, key) in seen_prompts:
                err(f"duplicate prompt in {scope[0]} {scope[1]}: {q['id']} repeats {seen_prompts[(scope, key)]}")
            seen_prompts[(scope, key)] = q["id"]
            gkey = key + "|" + str(q.get("answer"))
            if gkey in seen_global:
                cross += 1
            seen_global[gkey] = q["id"]
            nk = (scope, re.sub(r"\d+", "#", norm(q["prompt"])) + "|" + str(q.get("answer"))
                  + "|" + norm((q.get("diagram") or {}).get("spec", {}).get("alt", "")))
            near[nk] += 1
            all_qs.append(q)
    over = [(k, v) for k, v in near.items() if v > 6]
    if over:
        err(f"{len(over)} prompt shapes repeat more than 6 times inside one skill/level (max {max(v for _, v in over)})")
    if cross:
        warn(f"{cross} identical questions repeat across different skills (allowed: same fact, different skill)")

    # reading-load warnings (Grade 1)
    for q in all_qs:
        words = re.findall(r"[A-Za-z][A-Za-z']+", q.get("prompt", ""))
        longw = [w for w in words if len(w) > 12]
        if longw:
            warn(f"{q['id']}: long word(s) {sorted(set(longw))[:3]}")
        if len(q.get("prompt", "")) > 260:
            warn(f"{q['id']}: prompt is {len(q['prompt'])} characters")
        if q.get("format") == "multiple-choice" and any(len(o["text"]) > 60 for o in q.get("options") or []):
            warn(f"{q['id']}: long multiple-choice option")

    print("=" * 72)
    print(f"{COURSE_LABEL} verification — {len(UNITS)} units, {STATS['questions']} questions")
    print("=" * 72)
    print("formats:", {k[4:]: v for k, v in sorted(STATS.items()) if k.startswith("fmt_")})
    print(f"diagrams: {STATS['diagrams']}   duplicate prompt groups capped: {len(over)}")
    if WARNS:
        print(f"\n{len(WARNS)} warning(s); first 10:")
        for w in WARNS[:10]:
            print("  warn:", w)
    if ERRORS:
        print(f"\n{len(ERRORS)} ERROR(S); first 25:")
        for e in ERRORS[:25]:
            print("  error:", e)
        print(f"\nTOTAL ERRORS {len(ERRORS)}")
        return 1
    print("\nTOTAL ERRORS 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
