"""Grade 2 (math2) outline: loaded from course-outlines/grade2.json, the authoritative source.

9 units, 27 sections, 89 skills. Skill IDs are `<unit-id>-skill-NN` and must stay stable.
Standards for a skill come from every section that lists it; a skill not listed in any
section inherits the unit standards.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUTLINE = os.path.join(ROOT, "course-outlines", "grade2.json")

COURSE_ID = "math2"
PREFIX = "m2"
LABEL = "Grade 2"
UNIT_LABEL = "Grade 2 (math2)"

ABBR = {
    "adding-subtracting-working-data": "ad",
    "adding-subtracting-100": "h100",
    "measuring-length": "len",
    "number-line-addition-subtraction": "nl",
    "numbers-to-1000": "n1k",
    "geometry-time-money": "gtm",
    "adding-subtracting-1000": "t1k",
    "equal-groups": "eg",
    "putting-it-all-together": "all",
}

with open(OUTLINE, encoding="utf-8") as fh:
    SRC = json.load(fh)

UNITS = []
for _u in SRC["units"]:
    _sections = _u.get("sections") or []
    _by_skill = {}
    for _s in _sections:
        for _name in _s.get("skills", []):
            _by_skill.setdefault(_name, [])
            for _std in _s.get("standards", []):
                if _std not in _by_skill[_name]:
                    _by_skill[_name].append(_std)
    UNITS.append({
        "id": _u["id"],
        "name": _u["name"],
        "abbr": ABBR[_u["id"]],
        "skills": list(_u["skills"]),
        "standards": list(_u.get("standards") or []),
        "standards_by_skill": _by_skill,
        "sections": _sections,
        "days": (_u.get("estimatedDays"), _u.get("estimatedDaysMax")),
    })

UNIT_BY_ID = {u["id"]: u for u in UNITS}
SKILL_COUNT = sum(len(u["skills"]) for u in UNITS)


def skill_records(unit):
    out = []
    for i, nm in enumerate(unit["skills"], 1):
        stds = unit["standards_by_skill"].get(nm) or unit["standards"]
        out.append({"id": f"{unit['id']}-skill-{i:02d}", "index": i, "name": nm, "standards": list(stds)})
    return out


def all_standards():
    seen = []
    for u in UNITS:
        for r in skill_records(u):
            for s in r["standards"]:
                if s not in seen:
                    seen.append(s)
    return seen
