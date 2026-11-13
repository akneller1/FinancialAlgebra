"""Cross-skill duplication statistics for the Grade 1 banks.

An item is identified by what a student actually sees: prompt, option texts, answer and
picture description. Two items with the same identity in two different skills are an exact
cross-skill duplicate; the same identity inside one skill/level is a hard error (verify1).
"""
import json, os, re, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("G1_OUT") or os.path.join(HERE, "out")
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
_out = __import__(os.environ.get("G1_OUTLINE", "outline"))
UNITS, COURSE_ID = _out.UNITS, _out.COURSE_ID


def norm(t):
    return re.sub(r"\s+", " ", str(t).strip().lower().replace(",", ""))


def ident(q):
    s = norm(q["prompt"])
    if q.get("options"):
        s += "||" + "|".join(sorted(norm(o["text"]) for o in q["options"]))
    if q.get("parts"):
        s += "||" + "|".join(norm(p["prompt"]) for p in q["parts"])
    s += "||" + norm(q.get("answer", ""))
    s += "||" + norm((q.get("diagram") or {}).get("spec", {}).get("alt", ""))
    return s


def shape(q):
    """Digit-masked identity: 'near duplicate' family of surface forms."""
    s = re.sub(r"\d+", "#", ident(q))
    return s


def load():
    out = []
    for u in UNITS:
        bank = json.load(open(os.path.join(ROOT, "question-banks", COURSE_ID, u["id"] + ".json"), encoding="utf-8"))
        chk = json.load(open(os.path.join(OUT, u["id"] + ".checks.json"), encoding="utf-8"))
        for q in bank["questions"]:
            q["_unit"] = u["id"]
            q["_fam"] = chk.get(q["id"], {}).get("family", "?")
            q["_id"] = ident(q)
            q["_shape"] = shape(q)
        out += bank["questions"]
    return out


def stats(qs, verbose=True):
    tot = len(qs)
    by_id = defaultdict(list)
    for q in qs:
        by_id[q["_id"]].append(q)
    dup_items = {k: v for k, v in by_id.items() if len({x["skillId"] for x in v}) > 1}
    dup_count = sum(len(v) for v in dup_items.values())
    excess = sum(len(v) - 1 for v in dup_items.values())
    # visually equivalent: same picture and same answer, different skills
    vis = defaultdict(set)
    for q in qs:
        alt = norm((q.get("diagram") or {}).get("spec", {}).get("alt", ""))
        if alt:
            vis[(alt, norm(q.get("answer", "")))].add(q["skillId"])
    vis_pairs = {k: v for k, v in vis.items() if len(v) > 1}
    # near: same masked shape AND same answer, different skills
    near = defaultdict(set)
    for q in qs:
        near[q["_shape"]].add(q["skillId"])
    near_groups = {k: v for k, v in near.items() if len(v) > 1}
    res = {"total": tot, "dup_items": dup_count, "dup_rate": dup_count / tot,
           "excess": excess, "dup_groups": len(dup_items), "unique_items": tot - dup_count,
           "vis_groups": len(vis_pairs), "near_groups": len(near_groups)}
    if verbose:
        print(f"total {tot}  exact-dup items {dup_count} ({dup_count/tot:.1%})  excess copies {excess}")
        print(f"distinct identities {len(by_id)}   visual-equivalent groups {len(vis_pairs)}   near-shape groups {len(near_groups)}")
    return res, dup_items, vis_pairs


def report(qs, dup_items, path):
    by_unit = Counter(); by_skill = Counter(); by_fam = Counter(); by_level = Counter(); by_fmt = Counter()
    for k, v in dup_items.items():
        for q in v:
            by_unit[q["_unit"]] += 1
            by_skill[q["skillId"]] += 1
            by_fam[q["_fam"]] += 1
            by_level[q["level"]] += 1
            by_fmt[q["format"]] += 1
    data = {"units": dict(by_unit), "skills": dict(by_skill), "families": dict(by_fam),
            "levels": dict(by_level), "formats": dict(by_fmt)}
    json.dump(data, open(path, "w"), indent=1)
    print("\ntop families in duplicate groups:")
    for k, v in by_fam.most_common(10):
        print(f"  {v:5d}  {k}")
    print("\ntop skills in duplicate groups:")
    for k, v in by_skill.most_common(8):
        print(f"  {v:5d}  {k}")
    return data


if __name__ == "__main__":
    qs = load()
    res, dup, vis = stats(qs)
    report(qs, dup, os.path.join(OUT, "dup_before.json"))
