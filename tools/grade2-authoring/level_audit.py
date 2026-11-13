"""Level-escalation audit for the Grade 2 banks.

For every skill and every question family it compares the three levels
(Remedial / Standard / Advanced) on three independent measures read from the
published question text:

  size     largest number a question works with
  regroup  share of written add/sub expressions that need carrying or borrowing
  steps    largest number of operations in a written expression

A skill escalates when the mean size grows at every step up and the model
size is at least 20% larger at Advanced than at Remedial.  The report is
written to docs/math2/LEVELS.md so the split can be checked without rerunning
the generator.
"""
import glob
import json
import os
import re
from collections import defaultdict
from statistics import mean

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
BANKS = os.path.join(DEV, "question-banks", "math2")
OUT = os.path.join(DEV, "docs", "math2", "LEVELS.md")
LEVELS = [("cp2", "Remedial"), ("cp1", "Standard"), ("honors", "Advanced")]
EXPR = re.compile(r"(\d+)\s*([+\-\u00d7x])\s*(\d+)")
NUM = re.compile(r"\d+")


def measure(q):
    text = f"{q.get('prompt', '')} {q.get('answer', '')}"
    nums = [int(n) for n in NUM.findall(text)]
    size = max(nums) if nums else 0
    regroup, steps = None, 1
    for a, op, b in EXPR.findall(q.get("prompt", "")):
        a, b = int(a), int(b)
        steps = max(steps, 2) if steps == 2 else 1
        flag = ((a % 10) + (b % 10) >= 10 or (a % 100) + (b % 100) >= 100) if op == "+" \
            else (a % 10 < b % 10 or a % 100 < b % 100)
        regroup = flag if regroup is None else (regroup or flag)
    exprs = EXPR.findall(q.get("prompt", ""))
    steps = 2 if len(exprs) > 1 else 1
    return size, regroup, steps


def main():
    skills, fams = defaultdict(lambda: defaultdict(list)), defaultdict(lambda: defaultdict(list))
    for path in sorted(glob.glob(os.path.join(BANKS, "*.json"))):
        bank = json.load(open(path, encoding="utf-8"))
        if "questions" not in bank:
            continue
        for q in bank["questions"]:
            parts = q["id"].split("-")
            skill, level = parts[2], parts[3]
            m = measure(q)
            skills[(bank["unitId"], skill)][level].append(m)
            raw = (q.get("sourceNotes") or "").split("family: ")[-1].split(")")[0]
            num = re.match(r"fam\d+", raw)
            raw = re.sub(r"(fam\d+_)+", r"\1", raw)
            fam = (num.group(0) if num else raw.split("_")[0]) + \
                  ("_facts" if "_facts" in raw else "") + "_" + raw.rsplit("_", 1)[-1]
            fams[fam][level].append(m)

    def agg(rows):
        if not rows:
            return None, None, None
        sizes = mean(r[0] for r in rows)
        reg = [r[1] for r in rows if r[1] is not None]
        return sizes, (100 * sum(reg) / len(reg) if reg else None), mean(r[2] for r in rows)

    def flat(series):
        if None in series:
            return True, ""
        if not series[0] < series[1] < series[2]:
            return True, ""
        return (series[2] < 1.2 * max(series[0], 1)), ""

    lines = ["# Grade 2 level escalation", "",
             "Read from the published question text of every bank (no regenerating needed):",
             "`size` is the mean largest number in a question, `regroup` the share of written",
             "add/sub expressions that need carrying or borrowing, `steps` the mean number of",
             "written operations.  A level split counts as real when size rises at each step and",
             "Advanced is at least 20% larger than Remedial.", "",
             "| Unit | Skill | R size/regroup/steps | S | A | verdict |",
             "| --- | --- | --- | --- | --- | --- |"]
    flat_skills = []
    for (unit, skill), levels in sorted(skills.items()):
        cells, sizes = [], []
        for code, _ in LEVELS:
            size, reg, stp = agg(levels.get(code, []))
            sizes.append(size)
            cells.append("—" if size is None else
                         f"{size:.0f} / " + ("—" if reg is None else f"{reg:.0f}%") + f" / {stp:.2f}")
        is_flat, _ = flat(sizes)
        verdict = "flat" if is_flat else "escalates"
        if is_flat:
            flat_skills.append(f"{unit} {skill}")
        lines.append(f"| {unit} | {skill} | " + " | ".join(cells) + f" | {verdict} |")

    lines += ["", "## Families", "",
              "| Family | R size | S size | A size | R regroup | S regroup | A regroup |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    flat_fams = []
    for fam, levels in sorted(fams.items()):
        cells, sizes = [], []
        for code, _ in LEVELS:
            size, reg, _ = agg(levels.get(code, []))
            sizes.append(size)
            cells.append(("—" if size is None else f"{size:.0f}") +
                         " | " + ("—" if reg is None else f"{reg:.0f}%"))
            cells[-1] = cells[-1]
        regs = []
        for code, _ in LEVELS:
            _, reg, _ = agg(levels.get(code, []))
            regs.append(reg)
        is_flat, _ = flat(sizes)
        if is_flat:
            flat_fams.append(fam)
        lines.append(f"| {fam} | " + " | ".join("—" if s is None else f"{s:.0f}" for s in sizes) +
                     " | " + " | ".join("—" if r is None else f"{r:.0f}%" for r in regs) + " |")

    lines += ["", f"Skills: {len(skills)}, flat: {len(flat_skills)}. "
                  f"Families: {len(fams)}, flat: {len(flat_fams)}.", ""]
    if flat_fams:
        lines.append("Flat families: " + ", ".join(sorted(flat_fams)))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")

    print(f"skills {len(skills)} flat {len(flat_skills)} | families {len(fams)} flat {len(flat_fams)}")
    for fam in sorted(flat_fams)[:40]:
        levels = fams[fam]
        print("  flat:", fam, [None if not levels.get(c) else round(mean(r[0] for r in levels[c])) for c, _ in LEVELS])


if __name__ == "__main__":
    main()
