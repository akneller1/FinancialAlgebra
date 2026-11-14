"""Add supporting pictures to text-described visual items (2026-11-14).

Each picture is drawn ONLY from numbers parsed out of the item's own prompt, so the
picture and the words always agree; the prompt, answer and checks are not changed.
Items that ask students to *make* a graph (how many symbols to draw) are skipped on
purpose: a finished picture would give the answer away.

Usage: python3 add_visuals.py <classroom repo> <FinancialAlgebra repo>
"""
import json, os, re, subprocess, sys
from fractions import Fraction as F

CLS, FA = sys.argv[1], sys.argv[2]
sys.path[:0] = [os.path.join(FA, "tools/grade2-authoring"), os.path.join(FA, "tools/grade3-authoring"),
                os.path.join(FA, "tools/grade5-authoring")]
import figs2  # noqa: E402  (grade 2 renderer: picgraph, bargraph1, partition, grid …)
from figs import svg, text, rect, line, poly, INK, FILL, esc  # noqa: E402
import figs3  # noqa: E402

LOG = []


def png(svg_s, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out = subprocess.run(["rsvg-convert", "-z", "1.25"], input=svg_s.encode(), capture_output=True, check=True).stdout
    open(path, "wb").write(out)


def attach(q, root, rel, svg_s, alt):
    png(svg_s, os.path.join(root, rel))
    q["diagram"] = {"type": "image", "spec": {"src": rel, "alt": alt}}
    LOG.append((q["id"], rel))


# ---------------------------------------------------------------- Grade 2: graph data told in words
PAIR = re.compile(r"([A-Za-z]+) (\d+)")


def g2_graph(q, root):
    m = re.search(r"A (bar|picture) graph shows ([^.?]+)\.", q["prompt"])
    if not m:
        return False
    kind, body = m.group(1), m.group(2)
    pairs = PAIR.findall(body)
    cats, vals = [c for c, _ in pairs], [int(v) for _, v in pairs]
    assert ", ".join(f"{c} {v}" for c, v in zip(cats, vals)) == body.strip(), (q["id"], body)
    if kind == "bar":
        top = max(vals) if max(vals) <= 12 else (max(vals) + 1) // 2 * 2
        s = figs2.render("bargraph1", {"title": "", "cats": cats, "vals": vals, "top": max(top, 5), "ylabel": "Number"})
        alt = "A bar graph with a scale of 1. " + "; ".join(f"{c}: {v}" for c, v in zip(cats, vals)) + "."
    else:
        s = figs2.render("picgraph", {"title": "", "cats": cats, "symbols": vals, "key": 1, "icon": "star", "unit": ""})
        alt = "A picture graph. Each picture stands for 1. " + "; ".join(f"{c}: {v} pictures" for c, v in zip(cats, vals)) + "."
    attach(q, root, f"question-banks/assets/math2/graphs-data/{q['id']}.png", s, alt)
    return True


# ---------------------------------------------------------------- Grade 3: half of one symbol
def g3_half(q, root):
    m = re.search(r"each symbol stands for (\d+)\. What does half of one symbol stand for", q["prompt"])
    if not m:
        return False
    k = int(m.group(1))
    body = text(230, 34, "Picture Graph Key", 18, weight="800")
    body += figs3._icon("star", 70, 70, 44) + text(150, 102, f"= {k}", 24, anchor="start", weight="800")
    body += figs3._icon("star", 270, 70, 44).replace('fill="#ffc533"', 'fill="none" stroke-dasharray="3 3" opacity="0.45"')
    body += figs3._icon("star", 270, 70, 44, frac=F(1, 2)) + text(350, 102, "= ?", 24, anchor="start", weight="800")
    attach(q, root, f"question-banks/assets/math3/graphs-measurement-data/{q['id']}.png", svg(460, 140, body),
           f"A picture graph key. One whole star stands for {k}. Half of a star is marked with a question mark.")
    return True


# ---------------------------------------------------------------- Grade 4: rectangle cut into equal parts
def g4_split(q, root):
    m = re.search(r"A rectangle is cut into (\d+) equal parts, and (\d+) of the parts (?:is|are) shaded\. "
                  r"Then each part is cut into (\d+) smaller equal parts", q["prompt"])
    if not m:
        return False
    a, b, c = map(int, m.groups())
    s = figs3.partition({"shape": "rect", "cuts": "v", "widths": [1] * a, "shade": list(range(b)), "color": "green"})
    attach(q, root, f"question-banks/assets/math4/fractions-equivalent-fractions/{q['id']}.png", s,
           f"A rectangle cut into {a} equal parts with {b} shaded, before each part is cut into {c} smaller parts.")
    return True


# ---------------------------------------------------------------- Grade 4: area of half a symmetric figure
def g4_sym(q, root):
    m = re.search(r"The part of the figure on one side of the line has an area of (\d+) (square \w+)", q["prompt"])
    if not m:
        return False
    n, unit = m.group(1), m.group(2)
    # an arrow-shaped figure, symmetric about the dashed vertical line x = 230
    L = [(230, 30), (90, 140), (170, 140), (170, 250), (230, 250)]
    R = [(2 * 230 - x, y) for x, y in L]
    body = poly(L, FILL["green"]) + poly(R, "#ffffff")
    body += line(230, 14, 230, 266, INK, 2.5, 'stroke-dasharray="8 6"')
    body += text(230, 290, "line of symmetry", 14, weight="700")
    body += text(230, 318, f"Shaded half: {n} {unit.replace('square ', 'sq ').replace('centimeters', 'cm').replace('inches', 'in.')}", 17, weight="800")
    attach(q, root, f"question-banks/assets/math4/geometry-angles-symmetry/{q['id']}.png", svg(460, 334, body),
           f"A figure with a dashed vertical line of symmetry. The shaded left half is labeled {n} {unit}. The right half is unshaded.")
    return True


# ---------------------------------------------------------------- Grade 6: hundred grid
def g6_grid(q, root):
    m = re.search(r"(\d+) of (?:the )?100 squares (?:on a grid )?are shaded", q["prompt"])
    if not m:
        return False
    n = int(m.group(1))
    sz, x0, y0 = 26, 20, 20
    body = ""
    for i in range(100):
        r, c = divmod(i, 10)
        body += rect(x0 + c * sz, y0 + r * sz, sz, sz, FILL["orange"] if i < n else "#ffffff", INK, 1.2)
    body += rect(x0, y0, 10 * sz, 10 * sz, "none", INK, 2.5)
    s = svg(300, 300, body)
    attach(q, root, f"question-banks/assets/math6/ratios-rates-percent-proportions/{q['id']}.png", s,
           f"A 10 by 10 grid of 100 squares with {n} squares shaded.")
    return True


JOBS = [
    (FA, "question-banks/math2/graphs-data.json", g2_graph, r"\(family: sp_text_"),
    (FA, "question-banks/math3/graphs-measurement-data.json", g3_half, r"\(family: pg_half\)"),
    (FA, "math4/fractions-equivalent-fractions.json", g4_split, r"\(family: ue_split_parts"),
    (FA, "math4/geometry-angles-symmetry.json", g4_sym, r"\(family: sy_fold_measure"),
    (CLS, "question-banks/math6/ratios-rates-percent-proportions.json", g6_grid, r"\(family: s6_grid\)"),
]

for root, rel, fn, fam in JOBS:
    p = os.path.join(root, rel)
    raw = open(p, encoding="utf-8").read()
    d = json.loads(raw)
    qs = d["questions"] if isinstance(d, dict) else d
    hit = 0
    for q in qs:
        if q.get("diagram") or not re.search(fam, q.get("sourceNotes", "")):
            continue
        hit += fn(q, root)
    indent = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=indent)
        if raw.endswith("\n"):
            f.write("\n")
    print(f"{rel}: {hit} pictures added")
print("total", len(LOG))
