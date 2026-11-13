"""Curriculum-alignment audit for the Grade 2 banks.

This is a rule-based screen, not a substitute for a teacher reading every item.  It
answers three questions per question:

  topic    does the question family belong to the skill it is filed under?
  range    does the item respect the skill's stated number range ("within 100")?
  structure does the item respect the stated regrouping structure ("without
           regrouping", "compose a new ten")?

Generic domain drill (`domain_facts_items`) is treated as off-topic in every skill
that names a specific topic, because that is the filler ChatGPT flagged in Grade 1.

Usage: python3 align_audit.py            (report + docs/math2/ALIGNMENT.md)
       python3 align_audit.py --quiet    (counts only)
"""
import glob
import importlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
BANKS = os.path.join(DEV, "question-banks", "math2")
CHECKS = os.path.join(HERE, "out")
OUT = os.path.join(DEV, "docs", "math2", "ALIGNMENT.md")
os.environ.setdefault("G1_OUTLINE", "outline2")
outline = importlib.import_module(os.environ["G1_OUTLINE"])

TOPICS = [
    ("domain_facts_items", {"generic"}),
    ("story_match", {"story", "equations"}),
    ("story", {"story"}),
    ("two_step", {"story"}),
    ("tape", {"compare", "story"}),
    ("equation", {"equations"}),
    ("equal_sign", {"equations"}),
    ("true_false", {"equations"}),
    ("partition_numbers", {"partwhole"}),
    ("missing_addend", {"partwhole"}),
    ("make_ten_fill", {"partwhole"}),
    ("compare_groups", {"compare"}),
    ("count_on_difference", {"compare"}),
    ("fluency", {"add_sub"}),
    ("fact_family", {"add_sub"}),
    ("mixed_facts", {"add_sub"}),
    ("doubles", {"add_sub", "equal_groups"}),
    ("add3", {"add_sub"}),
    ("add2", {"add_sub"}),
    ("add_items", {"add_sub"}),
    ("sub3", {"add_sub"}),
    ("sub2", {"add_sub"}),
    ("sub_items", {"add_sub"}),
    ("ten_frame", {"add_sub"}),
    ("strategy", {"add_sub"}),
    ("numberline", {"numberline", "add_sub"}),
    ("skip_count", {"counting", "numberline"}),
    ("count_collection", {"counting"}),
    ("count_items", {"counting"}),
    ("count", {"counting"}),
    ("baseten", {"place_value"}),
    ("place3", {"place_value"}),
    ("place_items", {"place_value"}),
    ("tens_ones", {"place_value"}),
    ("ones", {"place_value"}),
    ("digit", {"place_value"}),
    ("expanded", {"place_value"}),
    ("ruler", {"length"}),
    ("measure", {"length"}),
    ("length", {"length"}),
    ("clock", {"time"}),
    ("time", {"time"}),
    ("money", {"money"}),
    ("coin", {"money"}),
    ("polygon", {"geometry"}),
    ("shape", {"geometry"}),
    ("solid", {"geometry"}),
    ("thirds", {"fractions"}),
    ("equal_parts", {"fractions"}),
    ("partition", {"fractions", "geometry"}),
    ("fraction", {"fractions"}),
    ("tally", {"data"}),
    ("graph", {"data"}),
    ("lineplot", {"data"}),
    ("array", {"equal_groups"}),
    ("repeated_add", {"equal_groups"}),
    ("even_odd", {"equal_groups"}),
    ("round", {"rounding"}),
    ("estimate", {"rounding"}),
]

SKILL_RULES = [
    (r"graph|tally|line plot|chart|data|categor", {"data"}),
    (r"money|coin|dollar|cent|quarter|dime|nickel|penny|pennies|bills", {"money"}),
    (r"time|clock|hour|minute|a\.m\.|p\.m\.", {"time"}),
    (r"length|measur|ruler|centimet|inch|feet|foot|meter|unit|tool", {"length"}),
    (r"shape|polygon|triangle|quadrilateral|pentagon|hexagon|octagon|side|corner|vertice|face|solid|cube|partition.*equal|equal part|fraction|half|halves|third|fourth|share", {"geometry", "fractions"}),
    (r"array|equal group|row|column|odd|even|repeated addition", {"equal_groups"}),
    (r"round|estimate", {"rounding"}),
    (r"number line|interval|distance|jump", {"numberline", "counting"}),
    (r"place.value|digit|expanded|hundred|ten|regroup|compose a hundred|thousand|blocks|base-ten", {"place_value"}),
    (r"skip count|count by|count to|count within|count objects|collection", {"counting"}),
    (r"compare|order|greater|least|greatest|less than|more than", {"compare", "place_value"}),
    (r"story|word problem|situation|problem", {"story", "add_sub", "compare"}),
    (r"add|sum|plus|combine|join|total", {"add_sub", "story", "partwhole"}),
    (r"subtract|difference|minus|take away|separate|left|decompos", {"add_sub", "story", "compare"}),
    (r"fluen|recall|mental|fact|jump|efficient", {"add_sub"}),
    (r"equation|equal sign|unknown", {"equations", "add_sub", "partwhole", "story"}),
]

STRUCT = [
    (r"without regroup|no regroup|without composing|without decomposing|without carrying|without borrowing", "no"),
    (r"compose a new ten|compose a new hundred|decompose a ten|decompose a hundred|regroup|trade one ten|carrying|borrowing", "yes"),
]


WORD_TOPICS = {
    "money": ["coin", "dime", "nickel", "quarter", "penny", "pennies", "cent", "\u00a2", "dollar", "$"],
    "time": ["clock", "hour hand", "minute hand", "a.m.", "p.m.", "time shown", "what time"],
    "length": ["centimeter", "centimeters", "meter", "meters", "inch", "inches", "feet", "foot",
               "ruler", "yardstick", "longer", "shorter", "how long", "length", "long", "unit",
               "tool", "fits best", "paper clips", "tiles long"],
    "geometry": ["shape", "triangle", "square", "rectangle", "pentagon", "hexagon", "trapezoid",
                 "quadrilateral", "sides", "corners", "vertices", "polygon", "cube", "face"],
    "fractions": ["equal parts", "halves", "thirds", "fourths", "sixths", "eighths", "fraction",
                  "shaded", "one half", "one third", "one fourth"],
    "data": ["graph", "line plot", "diagram", "tally", "chart", "x marks", "marks", "most often", "least often",
             "pictograph", "fewest", "most", "next to", "categories"],
    "equal_groups": ["array", "rows", "columns", "fact family", "row of", "groups of", "equal groups", "even", "odd",
                     "repeated addition", "dots", "pairs", "double"],
    "place_value": ["tens", "ones place", "hundreds", "place value", "place-value", "expanded", "digit",
                    "tens and", "blocks", "base-ten", "base ten", "plus 10", "plus 100", "10 more",
                    "100 more", "10 less", "100 less", "hundred more", "hundred less"],
    "counting": ["count by", "skip count", "what number is missing", "pattern"],
    "compare": ["greater", "least", "greatest", "in order", "compare", "more than", "fewer than",
                "closer to", "order from"],
    "rounding": ["round", "nearest ten", "nearest hundred", "closest to"],
    "numberline": ["number line", "jump", "start at", "arrow", "point to", "tick"],
}

EQUATION = re.compile(r"^\s*\d+\s*[+\u2212\-]\s*\d+\s*=\s*\?")


def text_topics(prompt, answer):
    low = prompt.lower()
    got = {k for k, words in WORD_TOPICS.items()
           if any(re.search(rf"\b{re.escape(w)}", low) if len(w) <= 5 else w in low for w in words)}
    if not got and (EQUATION.match(prompt) or " = ?" in prompt):
        got = {"add_sub"}
    if "how many" in low and not got:
        got = {"add_sub", "story"}
    return got or {"add_sub"}


def topics_for(family):
    for token, topics in TOPICS:
        if token in family:
            return topics
    return {"generic"}


def skill_topics(name):
    got = set()
    low = name.lower()
    for pattern, topics in SKILL_RULES:
        if re.search(pattern, low):
            got |= topics
    return got or {"generic"}


def expr_numbers(check):
    fn = check.get("fn")
    if fn in ("add", "sub"):
        return int(check["a"]), int(check["b"]), fn
    if fn in ("add3",):
        return None
    if fn == "sub3":
        return int(check["a"]), int(check["b"]), "sub"
    return None


def main():
    quiet = "--quiet" in sys.argv
    skill_name = {}
    for u in outline.UNITS:
        for rec in outline.skill_records(u):
            skill_name[rec["id"]] = rec["name"]

    flags = defaultdict(list)
    checked = 0
    by_unit = Counter()
    for path in sorted(glob.glob(os.path.join(CHECKS, "*.checks.json"))):
        unit = os.path.basename(path).replace(".checks.json", "")
        checks = json.load(open(path, encoding="utf-8"))
        bank = json.load(open(os.path.join(BANKS, unit + ".json"), encoding="utf-8"))
        for q in bank["questions"]:
            checked += 1
            name = skill_name.get(q["skillId"], "")
            want = skill_topics(name)
            fam = checks[q["id"]].get("family", "")
            check = checks[q["id"]].get("q") or {}
            extra = " ".join(str(o.get("text", "")) for o in (q.get("options") or []))
            for entry in (check.get("table") or {}):
                extra += " " + entry
            parts = check.get("parts")
            for part in (parts if isinstance(parts, list) else []):
                extra += " " + str(part[0] if isinstance(part, (list, tuple)) else part)
            have = text_topics(q["prompt"] + " " + extra, q["answer"])
            if not (have & want) and "generic" not in want:
                if have == {"add_sub"} and re.search(r"add|subtract|sum|difference|fluen|solve|problem|equation|compare|order",
                                                     name.lower()):
                    pass
                elif fam.startswith(("err_", "tf_", "sel_", "open_", "domain_facts")):
                    flags["generic filler under a specific skill"].append((q["id"], name, q["prompt"][:70]))
                else:
                    flags["question topic does not match the skill"].append((q["id"], name, fam, q["prompt"][:70]))

            m = re.search(r"within (\d[\d,]*)", name.lower())
            if m:
                limit = int(m.group(1).replace(",", ""))
                nums = [int(x) for x in re.findall(r"\d+", q["prompt"] + " " + str(q["answer"]))]
                if nums and max(nums) > limit:
                    flags["number outside the skill's stated range"].append(
                        (q["id"], name, max(nums), limit))
            st = None
            for pattern, kind in STRUCT:
                if re.search(pattern, name.lower()):
                    st = kind
                    break
            expr = expr_numbers(check)
            if st and expr and expr[0] is not None:
                a, b, fn = expr
                if fn == "add":
                    got = (a % 10 + b % 10 >= 10) or (a % 100 + b % 100 >= 100)
                else:
                    got = (a % 10 < b % 10) or (a % 100 < b % 100)
                if (st == "no" and got) or (st == "yes" and not got):
                    flags["regrouping structure does not match the skill"].append(
                        (q["id"], name, f"{a} {fn} {b}", "needs regrouping" if got else "no regrouping"))
            if flags and any(q["id"] in [x[0] for x in v] for v in flags.values()):
                by_unit[unit] += 1

    lines = ["# Grade 2 curriculum alignment", "",
             f"{checked} questions screened against their skill names. Rule-based candidates, not",
             "confirmed defects; a candidate can be a wording mismatch rather than a wrong task.", ""]
    for key in sorted(flags):
        lines.append(f"* **{key}**: {len(flags[key])}")
    lines.append("")
    for key in sorted(flags):
        lines += [f"## {key} ({len(flags[key])})", ""]
        for row in flags[key][:15]:
            lines.append("* " + " | ".join(str(x) for x in row))
        lines.append("")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    print(f"screened {checked}; " + "; ".join(f"{k}: {len(v)}" for k, v in sorted(flags.items())))


if __name__ == "__main__":
    main()
