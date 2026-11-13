"""Coverage report for the Grade 3 banks: standards -> skills, and per skill the counts by level, format, question type
and diagrams. Writes docs/math3/COVERAGE.md and docs/math3/coverage.csv."""
import csv, json, os, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from outline import UNITS, STANDARDS, skill_records, COURSE_ID

rows, by_std = [], defaultdict(list)
for i, u in enumerate(UNITS, 1):
    bank = json.load(open(os.path.join(ROOT, "question-banks", COURSE_ID, u["id"] + ".json"), encoding="utf-8"))["questions"]
    meta = json.load(open(os.path.join(ROOT, "question-banks", COURSE_ID, "meta", u["id"] + ".meta.json"), encoding="utf-8"))
    for r in skill_records(u):
        qs = [q for q in bank if q["skillId"] == r["id"]]
        lv = Counter(q["level"] for q in qs)
        fm = Counter(q["format"] for q in qs)
        qt = Counter(meta[q["id"]]["questionType"] for q in qs)
        rows.append({"unit": f"{i}. {u['name']}", "skillId": r["id"], "skill": r["name"], "standards": " ".join(r["standards"]), "target": r["target"],
                     "remedial": lv["cp2"], "standard": lv["cp1"], "advanced": lv["honors"], "short-answer": fm["short-answer"], "multiple-choice": fm["multiple-choice"],
                     "select-all": fm["select-all"], "open-response": fm["open-response"], "diagrams": sum(1 for q in qs if q.get("diagram")),
                     "word problems": qt["word-problem"], "visual": qt["visual"], "error analysis": qt["error-analysis"], "reasoning": qt["explain"] + qt["true-false"] + qt["compare-strategies"],
                     "multi-step": qt["multi-step"]})
        for s in r["standards"]:
            by_std[s].append(r["id"])
os.makedirs(os.path.join(ROOT, "docs", "math3"), exist_ok=True)
with open(os.path.join(ROOT, "docs", "math3", "coverage.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
L = ["# 3rd Grade Math (math3) coverage", "", f"{len(UNITS)} units · {len(rows)} skills · {sum(r['remedial'] + r['standard'] + r['advanced'] for r in rows):,} practice questions · "
     f"{len(by_std)}/{len(STANDARDS)} Grade 3 leaf standards covered.", "", "## Standards → skills", "", "| Standard | Skills |", "|---|---|"]
for s in STANDARDS:
    L.append(f"| {s} | {', '.join(by_std.get(s, ['**NOT COVERED**']))} |")
L += ["", "## Skills", "", "| Skill | Standards | R / S / A | SA / MC / select / open | Diagrams | Word | Visual | Error analysis | Reasoning | Multi-step |", "|---|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    L.append(f"| {r['skillId']}: {r['skill']} | {r['standards']} | {r['remedial']} / {r['standard']} / {r['advanced']} | {r['short-answer']} / {r['multiple-choice']} / {r['select-all']} / {r['open-response']} | "
             f"{r['diagrams']} | {r['word problems']} | {r['visual']} | {r['error analysis']} | {r['reasoning']} | {r['multi-step']} |")
open(os.path.join(ROOT, "docs", "math3", "COVERAGE.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(L[2])
