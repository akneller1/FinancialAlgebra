"""Write the course outline, manifest entries, curriculum map, coverage table and game-eligibility list for math1."""
import csv, glob, json, os, re, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "units"))
from outline import UNITS, COURSE_ID, STANDARDS, skill_records
import importlib
import build as B

outline = {"schemaVersion": 1, "id": COURSE_ID, "name": "1st Grade Mathematics", "shortName": "Grade 1", "status": "development",
           "description": f"Twelve units covering every Common Core / Massachusetts Grade 1 mathematics standard (20 leaf standards plus the 1.NBT.B.2 statement and its parts a, b and c), {sum(len(u['skills']) for u in UNITS)} skills with observable learning targets.",
           "source": {"title": "Common Core State Standards for Mathematics, Grade 1 (identical codes in the Massachusetts 2017 Mathematics Curriculum Framework)",
                      "note": "Replaces the earlier scope-and-sequence outline (8 units, 93 skills), as was done for Grade 2. Skill source of truth: tools/grade1-authoring/outline.py."},
           "standards": STANDARDS,
           "units": [{"id": u["id"], "name": u["name"], "description": u["blurb"], "status": "development", "skills": [s[0] for s in u["skills"]],
                      "skillStandards": [s[1] for s in u["skills"]], "targets": [s[2] for s in u["skills"]]} for u in UNITS]}
json.dump(outline, open(os.path.join(ROOT, "course-outlines", "grade1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

man = {"version": 1, "banks": [{"courseId": COURSE_ID, "unitId": u["id"], "path": f"question-banks/{COURSE_ID}/{u['id']}.json", "approved": False, "preview": True} for u in UNITS]}
json.dump(man, open(os.path.join(ROOT, "question-banks", COURSE_ID, "manifest.json"), "w"), indent=1)

cmap, rows, games = {"courseId": COURSE_ID, "units": []}, [], {}
for i, u in enumerate(UNITS):
    mod = importlib.import_module(B.MODS[i])
    bank = json.load(open(os.path.join(ROOT, "question-banks", COURSE_ID, u["id"] + ".json"), encoding="utf-8"))
    meta = json.load(open(os.path.join(ROOT, "question-banks", COURSE_ID, "meta", u["id"] + ".meta.json"), encoding="utf-8"))
    chk = bank_ck = json.load(open(os.path.join(ROOT, "question-banks", COURSE_ID, "checks", u["id"] + ".json"), encoding="utf-8"))
    per = defaultdict(Counter)
    for q in bank["questions"]:
        per[q["skillId"]][q["level"]] += 1
    gu = {"textMC": [q["id"] for q in bank["questions"] if meta[q["id"]]["game"]["textMC"]],
          "numeric": [q["id"] for q in bank["questions"] if meta[q["id"]]["game"]["numeric"]]}
    games[u["id"]] = gu
    ue = {"id": u["id"], "name": u["name"], "abbr": u["abbr"], "skills": []}
    for rec in skill_records(u):
        fams = [f.__name__ for f in mod.SKILLS[rec["index"]]["fams"]]
        ue["skills"].append({"id": rec["id"], "name": rec["name"], "standards": rec["standards"], "target": rec["target"],
                             "misconception": rec["misconception"], "support": rec["fix"], "families": fams,
                             "questions": dict(per[rec["id"]]), "checkItems": sum(1 for q in chk["questions"] if q["skillId"] == rec["id"])})
        rows.append([u["id"], rec["id"], rec["name"], " ".join(rec["standards"]), per[rec["id"]]["cp2"], per[rec["id"]]["cp1"], per[rec["id"]]["honors"],
                     sum(per[rec["id"]].values()), len(fams)])
    cmap["units"].append(ue)
json.dump(cmap, open(os.path.join(ROOT, "docs", COURSE_ID, "curriculum-map.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(games, open(os.path.join(ROOT, "docs", COURSE_ID, "game-eligibility.json"), "w"), indent=0)
with open(os.path.join(ROOT, "docs", COURSE_ID, "coverage.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["unit", "skillId", "skill", "standards", "remedial_cp2", "standard_cp1", "advanced_honors", "total", "families"])
    w.writerows(rows)
print("ok", len(rows), "skills")
