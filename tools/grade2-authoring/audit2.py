"""Content audit for the Grade 2 banks: does each prompt ask for what the check computes?

The mathematical verifier re-derives every answer from the stored inputs, which proves the
arithmetic is self-consistent but not that the *wording* asks for that quantity. This audit
looks for the mismatches a human reviewer finds:

  * a counting question ("how many ...") whose answer is a word,
  * a naming question ("what shape ...") whose answer is a number,
  * "1 tens" / "1 ones" style agreement errors,
  * ambiguous place-value wording ("how many ones are in 9 tens and 3 ones?"),
  * story problems whose unknown does not match the stored answer,
  * comparison wording ("how many fewer") answered with the larger quantity.

Usage: python3 audit2.py [--examples N]
"""
import json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from outline2 import UNITS, COURSE_ID

SHAPES = {"triangle", "square", "rectangle", "hexagon", "pentagon", "quadrilateral",
          "circle", "trapezoid", "cube", "cylinder", "sphere", "cone"}
COUNTY = re.compile(r"\b(how many|count|how much|total|find the total|number of)\b", re.I)
NAMEY = re.compile(r"\b(what shape|which shape|name the shape|what solid|which solid|name the solid|what is the name)\b", re.I)
LONGNUM = re.compile(r"^-?\$?\d[\d,]*\s*(cent|cm|in|inch|feet|foot|unit)?", re.I)


def is_number(a):
    a = str(a).strip()
    if re.fullmatch(r"-?\d[\d,]*", a) or re.fullmatch(r"\$?\d+(\.\d+)?", a):
        return True
    # money answers such as "75¢" or "75 cents" are numeric
    return bool(re.fullmatch(r"\$?\d+(\.\d+)?\s*(\u00a2|cents?)", a))


def audit():
    issues = defaultdict(list)
    for u in UNITS:
        bank = json.load(open(os.path.join(ROOT, "question-banks", COURSE_ID, u["id"] + ".json"), encoding="utf-8"))
        for q in bank["questions"]:
            p, a = q["prompt"], str(q.get("answer", ""))
            low = p.lower()
            expr = bool(re.fullmatch(r"\d+(\s*[+x\u00d7]\s*\d+)+", a))
            if (COUNTY.search(low) and not is_number(a) and not expr
                    and not re.match(r"^\d+:\d\d", a) and a.lower() not in ("even", "odd")):
                if re.search(r"(which|write|choose).*(repeated addition|expression|equation)", low):
                    continue
                if not re.search(r"how many (sides|corners|faces)", low) or not is_number(a):
                    issues["count_question_non_number"].append((q["id"], p[:90], a))
            if NAMEY.search(low) and not is_number(a) and a.strip().lower() not in SHAPES:
                issues["name_question_not_shape"].append((q["id"], p[:90], a))
            if re.search(r"\b1 (tens|ones|hundreds|parts|groups|rows)\b", low):
                issues["number_agreement"].append((q["id"], p[:90], a))
            if re.search(r"how many ones (are )?in \d+ tens", low) or re.search(r"how many (ones|tens) (does|are in) \d+", low):
                issues["ambiguous_place_value"].append((q["id"], p[:90], a))
            m = re.search(r"had some .{0,30}?\. .{0,40}?gave .{0,20}?(\d+) more\. .{0,30}?now .{0,20}?has (\d+)", low)
            if m and is_number(a):
                gave, total = int(m.group(1)), int(m.group(2))
                if int(str(a).replace(",", "")) != total - gave:
                    issues["story_start_unknown"].append((q["id"], p[:100], a))
            if re.search(r"how many (fewer|less)|how much (shorter|smaller)", low) and is_number(a):
                nums = [int(x) for x in re.findall(r"\b\d+\b", p)]
                if nums and int(a) >= max(nums):
                    issues["comparison_wording"].append((q["id"], p[:90], a))
    return issues


def main():
    n = int(sys.argv[sys.argv.index("--examples") + 1]) if "--examples" in sys.argv else 3
    issues = audit()
    total = 0
    for k in sorted(issues):
        rows = issues[k]
        total += len(rows)
        print(f"\n{k}: {len(rows)}")
        for qid, p, a in rows[:n]:
            print(f"   {qid} | {p!r} -> {a!r}")
    print(f"\nTOTAL FLAGGED {total}")


if __name__ == "__main__":
    main()
