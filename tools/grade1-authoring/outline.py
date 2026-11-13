"""Grade 1 (math1) outline: single source of truth loaded from course-outlines/grade1.json.

8 units, 27 sections, 93 skills. Skill IDs are `<unit-id>-skill-NN` and must stay stable.
Standards for a skill come from the section that lists it (the source's Grade 1 section
listings); a skill not listed in any section inherits the unit standards.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUTLINE = os.path.join(ROOT, "course-outlines", "grade1.json")

COURSE_ID = "math1"
PREFIX = "m1"

# short, stable file/ID tokens for each unit (do not change: they appear in question IDs)
ABBR = {
    "adding-subtracting-working-data": "ad",
    "addition-subtraction-story-problems": "sp",
    "adding-subtracting-within-20": "t20",
    "numbers-to-99": "n99",
    "adding-within-100": "h100",
    "length-measurement-120": "len",
    "geometry-time": "geo",
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
    """[{id, index, name, standards}] for one unit, 1-based two-digit index."""
    out = []
    for i, name in enumerate(unit["skills"], 1):
        stds = unit["standards_by_skill"].get(name) or unit["standards"]
        out.append({"id": f"{unit['id']}-skill-{i:02d}", "index": i, "name": name, "standards": list(stds)})
    return out


def all_standards():
    seen = []
    for u in UNITS:
        for r in skill_records(u):
            for s in r["standards"]:
                if s not in seen:
                    seen.append(s)
    return seen
