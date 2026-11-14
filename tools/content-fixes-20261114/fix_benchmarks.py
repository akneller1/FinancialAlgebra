"""Repair Grade 5 benchmark-estimation items (families b_sum, b_sum_error, b_sum_tf) whose
numbers make the benchmark estimate misleading (2026-11-14).

Example of the problem: "Use benchmarks to estimate 1/3 − 2/9" was keyed 1/2, but the exact
answer is 1/9. Rule now: each fraction is within 1/6 of its benchmark (0, 1/2 or 1) and the
estimate is within 1/4 of the exact answer. Bad items keep their id, skill, level and keyed
estimate; the two fractions change, and every place that depends on them (prompt, steps, the
"exact answer" distractor or student answer, check data) is rewritten from the new numbers.
"""
import json, random, re, sys, itertools
from fractions import Fraction as F

ROOT = sys.argv[1]
BANK = f"{ROOT}/math5/fraction-addition-subtraction.json"
CHECKS = f"{ROOT}/tools/grade5-authoring/out/fraction-addition-subtraction.checks.json"


def bench(x):
    return F(round(x * 2), 2)  # same rule as the generator


def fs(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    w, r = divmod(v.numerator, v.denominator)
    return f"{w} {F(r, v.denominator)}" if w else f"{v.numerator}/{v.denominator}"


def pf(s):
    s = s.strip()
    return int(s.split()[0]) + F(s.split()[1]) if " " in s else F(s)


def fair(x):
    return x * 4 not in (1, 3) and abs(x - bench(x)) <= F(1, 6)


def calc(a, op, b):
    est = bench(a) + bench(b) if op == "+" else bench(a) - bench(b)
    return est, (a + b if op == "+" else a - b)


def good(a, op, b):
    est, ex = calc(a, op, b)
    return fair(a) and fair(b) and abs(est - ex) <= F(1, 4) and est >= 0


PROB = re.compile(r"estimate (\d+/\d+) ([+−]) (\d+/\d+)\.")
bank = json.load(open(BANK, encoding="utf-8"))
checks = json.load(open(CHECKS, encoding="utf-8"))
qs = [q for q in bank["questions"] if re.search(r"family: b_sum(_error|_tf)?\)", q["sourceNotes"])]
used = {PROB.search(q["prompt"]).groups() for q in qs}
POOL = [F(n, d) for d in (5, 6, 7, 8, 9, 10, 12) for n in range(1, d) if F(n, d).denominator == d and fair(F(n, d))]
rng = random.Random(20261114)
changed = []

for q in qs:
    sa, op, sb = PROB.search(q["prompt"]).groups()
    a, b = F(sa), F(sb)
    if good(a, op, b):
        continue
    est, ex = calc(a, op, b)
    pairs = [(x, y) for x, y in itertools.product(POOL, POOL)
             if x.denominator != y.denominator and (op == "+" or x > y)
             and good(x, op, y) and calc(x, op, y)[0] == est and (fs(x), op, fs(y)) not in used]
    na, nb = rng.choice(pairs)
    used.add((fs(na), op, fs(nb)))
    nex = calc(na, op, nb)[1]
    old_p = f"{sa} {op} {sb}"
    q["prompt"] = q["prompt"].replace(old_p, f"{fs(na)} {op} {fs(nb)}")
    steps = [f"{fs(na)} is about {fs(bench(na))} and {fs(nb)} is about {fs(bench(nb))}.",
             f"{fs(bench(na))} {op} {fs(bench(nb))} = {fs(est)}."]
    fam = re.search(r"family: (b_sum\w*)\)", q["sourceNotes"]).group(1)
    ck = checks[q["id"]]["q"]
    if fam == "b_sum":
        q["solutionSteps"] = steps
        for o in q.get("options", []):
            if o["text"] == fs(ex) and not o["correct"]:
                o["text"] = fs(nex)
        ck.update(a=fs(na), b=fs(nb), op=op)
    elif fam == "b_sum_error":
        m = re.search(r"answered: (.+)\n", q["prompt"])
        shown = m.group(1)
        if pf(shown) == ex:  # the student found the exact answer
            q["prompt"] = q["prompt"].replace(f"answered: {shown}\n", f"answered: {fs(nex)}\n")
            shown = fs(nex)
        assert pf(shown) != est
        q["solutionSteps"] = [q["solutionSteps"][0]] + steps + [f"The correct answer is {fs(est)}, not {shown}."]
        ck.update(a=fs(na), b=fs(nb), op=op)
    else:  # b_sum_tf
        m = re.search(r"Answer shown: (.+)\n", q["prompt"])
        shown = m.group(1)
        if pf(shown) == ex:
            q["prompt"] = q["prompt"].replace(f"Answer shown: {shown}\n", f"Answer shown: {fs(nex)}\n")
            shown = fs(nex)
        for o in q.get("options", []):
            o["text"] = o["text"].replace(f"{fs(ex)} is the correct answer", f"{shown} is the correct answer")
            if o["text"] == f"False. The correct answer is {fs(ex)}.":
                o["text"] = f"False. The correct answer is {fs(nex)}."
        truth = pf(shown) == est
        q["solutionSteps"] = steps + [f"The answer {shown} is correct." if truth else f"The answer {shown} is not correct; it should be {fs(est)}."]
        ck["inner"].update(a=fs(na), b=fs(nb), op=op)
        ck["shown"] = shown
    changed.append((q["id"], fam, old_p, f"{fs(na)} {op} {fs(nb)}", fs(est), f"exact {fs(nex)}"))

for path, data, ind in ((BANK, bank, 1), (CHECKS, checks, 0)):
    raw = open(path, encoding="utf-8").read()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=ind)
        if raw.endswith("\n"):
            f.write("\n")
for c in changed:
    print(*c, sep=" | ")
print(len(changed), "items repaired")
