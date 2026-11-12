"""Unit 4: Numerical Expressions and Patterns (expressions-patterns)."""
from g5lib import *

UNIT_ID = "numerical-expressions-patterns"


def ev(e):
    """Generator-side evaluator: exact, grouping symbols allowed. (The verifier has its own.)"""
    e = e.replace("[", "(").replace("]", ")").replace("{", "(").replace("}", ")").replace("×", "*").replace("÷", "/").replace("−", "-")
    import re
    e = re.sub(r"(\d+)", r"F(\1)", e)
    v = eval(e, {"F": F})
    return F(v)


def ltr(e):
    """Value obtained by working strictly left to right, ignoring grouping and precedence (a common error)."""
    import re
    toks = re.findall(r"\d+|[+\-×÷]", e.replace("−", "-"))
    v = F(int(toks[0]))
    for i in range(1, len(toks), 2):
        o, n = toks[i], F(int(toks[i + 1]))
        v = v + n if o == "+" else v - n if o == "-" else v * n if o == "×" else v / n
    return v


def nice(v):
    return v.denominator == 1 and v >= 0


def show(e):
    return e.replace("-", "−")


# ============================================================== S1 Order of Operations with Grouping Symbols
def make_expr(r, L):
    a, b, c, d = [r.randint(2, 12) for _ in range(4)]
    if L == 0:
        forms = [f"{a} × ({b} + {c})", f"({a} + {b}) × {c}", f"{a} + {b} × {c}", f"({a * c} + {b * c}) ÷ {c}", f"{a + b + c} − ({b} + {c})"]
    elif L == 1:
        forms = [f"{a} × [{b} + ({c} × {d})]", f"[({a} + {b}) × {c}] − {d}", f"{a * d} ÷ ({d} × 1) + {b} × {c}", f"({a} + {b}) × ({c} + {d})", f"{a} × {b} − ({c} + {d})"]
    else:
        forms = [f"{{{a} × [{b} + ({c} − 1)]}} ÷ 1", f"{a * b * c} ÷ [{b} × ({c} + 0)]", f"{{[{a} + {b}] × {c}}} − {d} × 2", f"{a} + {{{b} × [{c} + ({d} ÷ 1)]}}",
                 f"[{a * 4} − ({b} + {c})] × {d}"]
    e = pick(r, forms)
    v = ev(e)
    need(nice(v) and v < 2000)
    return e, v


@fam("012")
def o_eval(r, L):
    e, v = make_expr(r, L)
    flat = e.replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace("(", "").replace(")", "")
    bad = [W(dec(ltr(flat)), "ignored the grouping symbols and worked left to right") if nice(ltr(flat)) else None,
           W(dec(ev(flat)), "ignored the grouping symbols") if nice(ev(flat)) else None,
           W(dec(v + pick(r, [1, 2, 10])), "made an arithmetic slip"), W(dec(v * 2), "doubled a step")]
    bad = [x for x in bad if x]
    return Item(f"Evaluate: {show(e)}", dec(v), ["Work inside the innermost grouping symbols first: ( ), then [ ], then { }.",
                f"Then multiply and divide from left to right, then add and subtract. The value is {dec(v)}."],
                bad, EX(e.replace("−", "-")), qtype="procedural", claim=f"{show(e)} =")


@fam("012")
def o_diff(r, L):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    e1, e2 = f"{a} × ({b} + {c})", f"{a} × {b} + {c}"
    if L == 2:
        d = r.randint(2, 5)
        e1, e2 = f"[{a} + {b}] × ({c} + {d})", f"{a} + {b} × {c} + {d}"
    v1, v2 = ev(e1), ev(e2)
    need(v1 != v2)
    return Item(f"How much greater is {e1} than {e2}?", dec(abs(v1 - v2)),
                [f"{e1} = {dec(v1)} and {e2} = {dec(v2)}.", f"{dec(max(v1, v2))} − {dec(min(v1, v2))} = {dec(abs(v1 - v2))}."],
                [W(dec(v1), "gave the value of the first expression"), W(dec(v2), "gave the value of the second expression"), W("0", "thought the grouping symbols do not change the value")],
                EX(f"({e1})-({e2})" if v1 > v2 else f"({e2})-({e1})"), qtype="compare-strategies", tags={"reasoning"})


@fam("012", mode="mc")
def o_parens(r, L):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    d = r.randint(2, 6) if L else None
    if L == 0:
        good, target = f"({a} + {b}) × {c}", (a + b) * c
        cands = [f"{a} + ({b} × {c})", f"{a} + {b} × {c}", f"({a} × {b}) + {c}"]
        bare = f"{a} + {b} × {c}"
    else:
        good, target = f"{a} × ({b} + {c}) − {d}", a * (b + c) - d
        cands = [f"({a} × {b}) + {c} − {d}", f"{a} × {b} + ({c} − {d})", f"{a} × ({b} + {c} − {d})"]
        bare = f"{a} × {b} + {c} − {d}"
    vals = {ev(x.replace("−", "-")) for x in cands}
    need(F(target) not in vals and len(vals) == 3)
    opts = [(show(good), True)] + [(show(x), False) for x in cands]
    r.shuffle(opts)
    return Item(f"Where should parentheses go so that the expression equals {target}? {show(bare)}", show(good),
                ["Try each placement and evaluate.", f"{show(good)} = {target}."], check=FN("same_value", target=str(target)), options=opts, mode="mc",
                qtype="explain", tags={"reasoning"})


@fam("012", mode="mc")
def o_first(r, L):
    a, b, c, d = [r.randint(2, 9) for _ in range(4)]
    e = pick(r, [f"{a * 3} − [{b} × ({c} + {d})]", f"{a} + {b} × ({c * d} ÷ {d})", f"[{a} + ({b} − 1)] × {c}", f"{{{a} × [{b} + ({c} − 1)]}} + {d}"]) if L else pick(r, [f"{a} × ({b} + {c})", f"({a} + {b}) × {c}", f"{a * c} ÷ ({c} − 1)"])
    import re
    inner = re.findall(r"\(([^()]*)\)", e)[0]
    good = show(inner)
    others = re.findall(r"\d+ [×÷+\-−] \d+", e.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("{", "").replace("}", ""))
    bad = [show(x) for x in others if show(x) != good]
    bad = list(dict.fromkeys(bad))
    tail = ["Work from left to right without grouping.", "It does not matter which step is first."]
    bad = (bad + tail)[:3]
    need(len(bad) == 3)
    return mc_key(f"What is the first step to evaluate {show(e)}?", good, bad, ["Start with the innermost grouping symbols.", f"First compute {good}."], r=r, qtype="conceptual")


@fam("012", mode="mc")
def o_greatest(r, L):
    a, b, c = r.sample(range(2, 10), 3)
    exprs = [f"{a} + {b} × {c}", f"({a} + {b}) × {c}", f"{a} × {b} + {c}", f"{a} × ({b} + {c})"]
    vals = [ev(x) for x in exprs]
    need(len(set(vals)) == 4)
    best = exprs[vals.index(max(vals))]
    opts = [(x, x == best) for x in exprs]
    r.shuffle(opts)
    return Item("Which expression has the greatest value?", best, ["Evaluate each: " + "; ".join(f"{x} = {dec(v)}" for x, v in zip(exprs, vals)) + ".", f"The greatest is {best}."],
                check=FN("extreme_expr", exprs=exprs, which="max"), options=opts, mode="mc", qtype="compare-strategies", tags={"reasoning"})


@fam("2")
def o_fraction(r, L):
    a, b = r.randint(2, 9), r.randint(2, 9) * 10
    d = pick(r, [2, 4, 5])
    v = a * b + F(a, d)
    return Item(f"Evaluate: ({a} × {b}) + ({a} × 1/{d})", mixed(v), [f"{a} × {b} = {a * b}; {a} × 1/{d} = {frac(F(a, d))}.", f"{a * b} + {frac(F(a, d))} = {mixed(v)}."],
                [W(mixed(F(a * b + 1, 1) / d + 0) if False else mixed(a * (b + 1)), "treated 1/d as 1"), W(mixed(a * b + F(1, d)), "multiplied only one part by the factor"), W(mixed(a * b), "left out the second product")],
                EX(f"({a}*{b})+({a}*1/{d})", form="mixed"), qtype="procedural", tags={"connections"})


@fam("12", mode="mc")
def o_steps(r, L):
    a, b, c, d = [r.randint(2, 9) for _ in range(4)]
    e = f"{a} × [{b} + ({c} × {d})]"
    s1, s2, s3 = f"{c} × {d} = {c * d}", f"{b} + {c * d} = {b + c * d}", f"{a} × {b + c * d} = {a * (b + c * d)}"
    lab = ["A", "B", "C"]
    order = [0, 1, 2]
    r.shuffle(order)
    need(order != [0, 1, 2])
    steps = [s1, s2, s3]
    shown = "  ".join(f"{lab[i]}) {steps[order[i]]}" for i in range(3))
    pos = {order[i]: lab[i] for i in range(3)}
    good = ", ".join(pos[k] for k in range(3))
    import itertools
    bad = [", ".join(p) for p in itertools.permutations(lab) if ", ".join(p) != good]
    r.shuffle(bad)
    return mc_key(f"Put the steps for evaluating {e} in order. {shown}", good, bad[:3], ["Parentheses first, then brackets, then multiply.", f"Order: {good}."], r=r, qtype="ordering")


# ============================================================== S2 Writing Numerical Expressions
PHRASES = [("add {a} and {b}, then multiply by {c}", "{c} × ({a} + {b})", ["{c} × {a} + {b}", "{a} + {b} × {c}", "{a} × {b} + {c}"]),
           ("multiply {a} by {b}, then subtract {c}", "{a} × {b} − {c}", ["{a} × ({b} − {c})", "{c} − {a} × {b}", "({a} − {c}) × {b}"]),
           ("subtract {c} from {a}, then divide by {d}", "({a} − {c}) ÷ {d}", ["{a} − {c} ÷ {d}", "{c} − {a} ÷ {d}", "{d} ÷ ({a} − {c})"]),
           ("triple the sum of {a} and {b}", "3 × ({a} + {b})", ["3 × {a} + {b}", "3 + {a} + {b}", "({a} + {b}) ÷ 3"]),
           ("half of the difference of {a} and {c}", "({a} − {c}) ÷ 2", ["{a} − {c} ÷ 2", "2 × ({a} − {c})", "({a} + {c}) ÷ 2"]),
           ("the sum of {a} and the product of {b} and {c}", "{a} + {b} × {c}", ["({a} + {b}) × {c}", "{a} × {b} + {c}", "{a} + {b} + {c}"])]


def phrase(r, L):
    a, b, c, d = r.randint(5, 20), r.randint(2, 12), r.randint(2, 9), r.randint(2, 5)
    t, good, bad = pick(r, PHRASES if L else PHRASES[:4])
    kw = dict(a=a + c * d, b=b, c=c, d=d) if "÷ {d}" in good else dict(a=a + c, b=b, c=c, d=d)
    if "÷ 2" in good:
        kw["a"] = c + 2 * r.randint(1, 9)
    return t.format(**kw), good.format(**kw), [x.format(**kw) for x in bad]


@fam("012", mode="mc")
def w_words(r, L):
    t, good, bad = phrase(r, L)
    vals = [ev(x.replace("−", "-")) for x in [good] + bad]
    need(len(set(vals)) == 4 and vals[0].denominator == 1)
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Item(f"Which expression means “{t}”?", good, ["Do the first action described, then use grouping symbols so it happens first.", f"The expression is {good}."],
                check=FN("same_value", target=good.replace("−", "-")), options=opts, mode="mc", qtype="conceptual", tags={"multiple-representations"})


@fam("012")
def w_value(r, L):
    t, good, bad = phrase(r, L)
    v = ev(good.replace("−", "-"))
    need(v.denominator == 1 and v > 0)
    wv = [ev(x.replace("−", "-")) for x in bad]
    it = Item(f"Write an expression for “{t}.” Then find its value.", dec(v), [f"Expression: {good}.", f"Value: {dec(v)}."],
              [W(dec(x), "wrote the operations in the wrong order") for x in wv if x.denominator == 1 and x > 0], EX(good.replace("−", "-")), qtype="procedural")
    it.consts = [2, 3]
    return it


CTX_EXPR = [("{n} buys {a} packs of {b} stickers and gives away {c} stickers. Which expression shows how many stickers {n} has left?", "{a} × {b} − {c}", ["{a} × ({b} − {c})", "({a} + {b}) − {c}", "{c} − {a} × {b}"]),
            ("A class has {a} tables with {b} students at each and {c} more students on the rug. Which expression shows the number of students?", "{a} × {b} + {c}", ["{a} × ({b} + {c})", "{a} + {b} + {c}", "({a} + {c}) × {b}"]),
            ("{n} has ${a} and earns ${b} each week for {c} weeks. Which expression shows how much money {n} will have?", "{a} + {b} × {c}", ["({a} + {b}) × {c}", "{a} × {b} + {c}", "{a} + {b} + {c}"]),
            ("{a} cookies are shared equally by {c} friends after {b} are eaten. Which expression shows how many each friend gets?", "({a} − {b}) ÷ {c}", ["{a} − {b} ÷ {c}", "{a} ÷ {c} − {b}", "({a} + {b}) ÷ {c}"])]


@fam("012", mode="mc")
def w_context(r, L):
    a, b, c = r.randint(3, 9), r.randint(4, 12), r.randint(2, 9)
    t, good, bad = pick(r, CTX_EXPR)
    if "÷" in good:
        a = b + c * r.randint(2, 9)
    kw = dict(a=a, b=b, c=c, n=name(r))
    good, bad = good.format(**kw), [x.format(**kw) for x in bad]
    vals = [ev(x.replace("−", "-")) for x in [good] + bad]
    need(len(set(vals)) == 4)
    opts = [(good, True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    return Item(t.format(**kw), good, ["Decide which action happens first and group it.", f"{good}."], check=FN("same_value", target=good.replace("−", "-")), options=opts, mode="mc",
                qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def w_to_words(r, L):
    t, good, bad = phrase(r, L)
    others = [p for p in PHRASES if p[1] != PHRASES[[p[1] for p in PHRASES].index(next(pp[1] for pp in PHRASES if t.startswith(pp[0].split("{")[0])))][1]] if False else None
    a, b, c = r.randint(5, 20), r.randint(2, 12), r.randint(2, 9)
    e = f"{c} × ({a} + {b})"
    goodw = f"add {a} and {b}, then multiply by {c}"
    badw = [f"multiply {c} by {a}, then add {b}", f"add {c} and {a}, then multiply by {b}", f"multiply {a} by {b}, then add {c}"]
    return mc_key(f"Which words describe the expression {e}?", goodw, badw, ["The parentheses show what happens first.", f"{e} means: {goodw}."], r=r, qtype="conceptual", tags={"multiple-representations"})


# ============================================================== S3 Interpreting Expressions Without Evaluating
@fam("012")
def i_times(r, L):
    a, b = r.randint(120, 9999), r.randint(100, 999)
    k = r.randint(2, 9)
    form = pick(r, ["+", "−"]) if L else "+"
    base = f"{comma(a)} + {comma(b)}" if form == "+" else f"{comma(max(a, b))} − {comma(min(a, b))}"
    return Item(f"Without calculating, how many times as large is {k} × ({base}) as {base}?", str(k),
                [f"{k} × ({base}) means {k} groups of ({base}).", f"So it is {k} times as large."],
                [W(str(k + 1), "added the factor"), W(f"1/{k}", "thought multiplying makes it smaller"), W(comma(a), "tried to compare the numbers inside")],
                FN("expr_ratio", a=f"{k}*({base.replace('−', '-')})", b=base.replace("−", "-")), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def i_which(r, L):
    a, b = r.randint(120, 999), r.randint(100, 999)
    k = r.randint(2, 6)
    base = f"{a} + {b}"
    good = f"{k} × ({base})"
    bad = [f"{k} × {a} + {b}", f"({base}) ÷ {k}", f"{a} + {b} + {k}"]
    word = {2: "twice", 3: "three times", 4: "four times", 5: "five times", 6: "six times"}[k]
    opts = [(good, True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    return Item(f"Without calculating, which expression is {word} as large as {base}?", good, [f"Multiplying the whole sum by {k} makes it {word} as large.", f"{good}."],
                check=FN("expr_times", base=base, mult=k), options=opts, mode="mc", qtype="conceptual", tags={"reasoning"})


@fam("012")
def i_change(r, L):
    a, b = r.randint(3, 40), r.randint(10, 90)
    k = pick(r, [2, 3, 4, 10]) if L < 2 else pick(r, [2, 3, 5, 10])
    if L == 2 and r.random() < 0.5:
        return Item(f"In {a} × {b * k}, the {b * k} is replaced by {b}. How many times as large is the new product as the old one? Write a fraction.", f"1/{k}",
                    [f"{b} is 1/{k} of {b * k}.", f"So the product becomes 1/{k} as large."],
                    [W(str(k), "thought the product grows"), W(f"1/{k + 1}", "miscounted"), W(str(b * k - b), "found the difference of the numbers")],
                    FN("expr_ratio", a=f"{a}*{b}", b=f"{a}*{b * k}"), qtype="conceptual", tags={"reasoning", "challenge"})
    return Item(f"In {a} × {b}, the {b} is replaced by {b * k}. How many times as large is the new product as the old one?", str(k),
                [f"{b * k} is {k} times {b}.", f"So the product is {k} times as large."],
                [W(str(b * k - b), "found how much the factor increased"), W(str(k * a), "multiplied the wrong numbers"), W(f"1/{k}", "reversed the comparison")],
                FN("expr_ratio", a=f"{a}*{b * k}", b=f"{a}*{b}"), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def i_compare(r, L):
    a, b = r.randint(120, 999), r.randint(100, 999)
    k = r.randint(2, 9)
    op = pick(r, ["×", "÷"]) if L else "×"
    e1 = f"{k} × ({a} + {b})" if op == "×" else f"({comma(a * k)} + {comma(b * k)}) ÷ {k}"
    e2 = f"{a} + {b}" if op == "×" else f"{comma(a * k)} + {comma(b * k)}"
    good = f"{e1} is {k} times as large as {e2}." if op == "×" else f"{e1} is 1/{k} as large as {e2}."
    bad = [f"{e1} is {k} more than {e2}." if op == "×" else f"{e1} is {k} less than {e2}.", f"The two expressions are equal.",
           f"{e2} is {k} times as large as {e1}." if op == "×" else f"{e1} is {k} times as large as {e2}."]
    return mc_key(f"Without calculating, which statement is true?", good, bad,
                  [f"{e1} {'multiplies' if op == '×' else 'divides'} the whole sum by {k}.", good], r=r, qtype="explain", tags={"reasoning"})


@fam("012")
def i_fill(r, L):
    a, b = r.randint(20, 99), r.randint(20, 99)
    k = r.randint(2, 9)
    return Item(f"Fill in the blank without calculating: ___ × ({a} + {b}) is {k} times as large as {a} + {b}.", str(k),
                [f"To make something {k} times as large, multiply it by {k}.", f"The blank is {k}."],
                [W(str(a + b), "found the sum"), W(str(k * (a + b)), "calculated instead of reasoning"), W(f"1/{k}", "made it smaller")],
                FN("expr_ratio_blank", a=a, b=b, mult=k), qtype="fill-blank", tags={"reasoning"})


@fam("012")
def i_how_much(r, L):
    a, b = r.randint(12, 99), r.randint(12, 99)
    k = r.randint(2, 8)
    j = k + (1 if L < 2 else r.randint(1, 3))
    s = a + b
    return Item(f"Without multiplying, how much greater is {j} × ({a} + {b}) than {k} × ({a} + {b})?", str((j - k) * s),
                [f"{j} groups of ({a} + {b}) is {j - k} more group{'s' if j - k > 1 else ''} than {k} groups.", f"{j - k} × ({a} + {b}) = {j - k} × {s} = {(j - k) * s}."],
                [W(str(j - k), "gave the number of extra groups, not their value"), W(str(j * s), "found the larger product"), W(str(s), "used one group") if j - k > 1 else W(str(2 * s), "counted two groups")],
                EX(f"{j}*({a}+{b})-{k}*({a}+{b})"), qtype="explain", tags={"reasoning"})


# ============================================================== S4 Generating Numerical Patterns
MODE = {"m": "frac"}


def pat(r, L):
    MODE["m"] = "frac"
    if L == 0:
        return "add", r.randint(0, 10), r.randint(2, 9)
    if L == 1:
        return pick(r, [("add", r.randint(0, 30), r.randint(3, 15)), ("mul", r.randint(1, 4), pick(r, [2, 3]))])
    kind = r.randrange(3)
    if kind == 2:
        MODE["m"] = "dec"
        return "add", F(r.randint(1, 20), 10), F(r.randint(2, 9), 10)
    return [("add", F(r.randint(0, 4)), pick(r, [F(1, 2), F(1, 4), F(3, 4)])), ("mul", r.randint(1, 5), pick(r, [2, 3, 10]))][kind]


def terms(op, s, k, n):
    out = [F(s)]
    for _ in range(n - 1):
        out.append(out[-1] + k if op == "add" else out[-1] * k)
    return out


def ft(v):
    v = F(v)
    return dec(v) if MODE["m"] == "dec" else mixed(v)


def rule_text(op, k):
    return f"Add {ft(F(k))}" if op == "add" else f"Multiply by {k}"


@fam("012")
def p_term(r, L):
    op, s, k = pat(r, L)
    n = r.randint(5, 8)
    t = terms(op, s, k, n)
    need(t[-1] < 100000)
    return Item(f"A pattern starts at {ft(F(s))}. The rule is “{rule_text(op, k)}.” What is term {n}?", ft(t[-1]),
                [f"Terms: {', '.join(ft(x) for x in t)}.", f"Term {n} is {ft(t[-1])}."],
                [W(ft(t[-2]), "stopped one term early"), W(ft(t[-1] + k if op == 'add' else t[-1] * k), "went one term too far"), W(ft(F(s) + F(k) * n) if op == "add" else ft(F(s) * k * n), "multiplied the rule by the term number without starting from the first term")],
                FN("pattern_term", start=ft(F(s)).replace(" ", "+") if " " in ft(F(s)) else ft(F(s)), op=op, step=str(k), n=n), qtype="procedural")


@fam("012")
def p_list(r, L):
    op, s, k = pat(r, L)
    t = terms(op, s, k, 5)
    need(t[-1] < 100000)
    ans = ", ".join(ft(x) for x in t)
    return Item(f"Start at {ft(F(s))} and use the rule “{rule_text(op, k)}.” List the first 5 terms. Separate them with commas.", ans,
                [f"Begin with {ft(F(s))} and apply the rule 4 times.", ans],
                [W(", ".join(ft(x) for x in terms(op, s, k, 6)[1:]), "did not include the starting number"),
                 W(", ".join(ft(x) for x in terms("add" if op == "mul" else "mul", s, k, 5)) if op == "mul" or k > 1 else ", ".join(ft(x) for x in terms(op, s, k + 1, 5)), "used the wrong operation")],
                FN("pattern_list", start=str(s), op=op, step=str(k), count=5), qtype="procedural")


@fam("012", mode="mc")
def p_rule(r, L):
    op, s, k = pat(r, L)
    t = terms(op, s, k, 4)
    good = rule_text(op, k)
    alts = [rule_text("add", t[1] - t[0]), rule_text("mul", 2), rule_text("add", F(k) + 1), rule_text("add", F(k) - 1 if F(k) > 1 else F(k) * 2), rule_text("mul", 3)]
    bad = [a for a in dict.fromkeys(alts) if a != good and not (a == rule_text("add", t[1] - t[0]) and op == "add")]
    # a rule is wrong only if it fails to produce the sequence
    def fits(rt):
        if rt.startswith("Add"):
            dd = t[1] - t[0]
            return rt == rule_text("add", dd) and all(t[i + 1] - t[i] == dd for i in range(3))
        m = int(rt.split()[-1])
        return all(t[i + 1] == t[i] * m for i in range(3))
    bad = [b for b in bad if not fits(b)][:3]
    need(len(bad) == 3 and fits(good))
    return mc_key(f"What is the rule for the pattern {', '.join(ft(x) for x in t)}, … ?", good, bad,
                  ["Compare each term with the one before it.", f"The rule is “{good}.”"], r=r, qtype="conceptual")


@fam("012")
def p_table(r, L):
    op, s, k = pat(r, L)
    t = terms(op, s, k, 6)
    need(t[-1] < 100000)
    shown = [ft(x) for x in t[:4]] + ["?"]
    alt = f"Table showing terms 1 to 5 of a pattern: {', '.join(shown)}."
    return Item("The table shows a pattern. What number belongs in place of “?” (term 5)?", ft(t[4]),
                [f"The rule is “{rule_text(op, k)}.”", f"Term 5 = {ft(t[4])}."],
                [W(ft(t[5]), "went one term too far"), W(ft(t[3]), "repeated term 4"), W(ft(t[3] + 1), "added 1 instead of using the rule")],
                FN("pattern_term", start=str(s), op=op, step=str(k), n=5), qtype="visual",
                diagram=Diagram("two_tables", {"rows": [["Pattern", shown]]}, alt))


@fam("012")
def p_word(r, L):
    s, k = r.randint(2, 30), r.randint(2, 12)
    n = r.randint(5, 10)
    t = terms("add", s, k, n)
    ctx = pick(r, [("{nm} has {s} stamps and adds {k} stamps each week.", "stamps", "week"), ("A plant is {s} centimeters tall and grows {k} centimeters each week.", "centimeters", "week"),
                   ("{nm} saves ${s} and then saves ${k} more each month.", "dollars", "month")])
    nm = name(r)
    unit = ctx[1]
    ans = f"${comma(t[-1])}" if unit == "dollars" else f"{comma(t[-1])} {unit}"
    return Item(ctx[0].format(nm=nm, s=s, k=k) + f" How many {'dollars' if unit == 'dollars' else unit} after {n - 1} {ctx[2]}s?", ans,
                [f"Start: {s}. Add {k} for each of {n - 1} {ctx[2]}s.", f"{s} + {n - 1} × {k} = {comma(t[-1])}."],
                [W(f"${comma(t[-1] + k)}" if unit == "dollars" else f"{comma(t[-1] + k)} {unit}", "counted the starting amount as a week of adding"),
                 W(f"${comma(k * (n - 1))}" if unit == "dollars" else f"{comma(k * (n - 1))} {unit}", "forgot the starting amount"),
                 W(f"${comma(s * (n - 1))}" if unit == "dollars" else f"{comma(s * (n - 1))} {unit}", "multiplied the starting amount")],
                EX(f"{s}+{n - 1}*{k}", unit="$" if unit == "dollars" else unit), qtype="real-world", tags={"modeling"})


# ============================================================== S5 Relationships Between Two Patterns
def two_rules(r, L):
    a = r.randint(1, 6) if L < 2 else r.randint(2, 9)
    m = pick(r, [2, 3, 4]) if L < 2 else pick(r, [2, 3, 4, 5, 6])
    return a, a * m, m


@fam("012")
def rel_times(r, L):
    a, b, m = two_rules(r, L)
    A, B = terms("add", 0, a, 5), terms("add", 0, b, 5)
    return Item(f"Pattern A starts at 0 and adds {a}. Pattern B starts at 0 and adds {b}. Each term in Pattern B is how many times the matching term in Pattern A? (Use terms after the first.)", str(m),
                [f"A: {', '.join(map(str, map(int, A)))}. B: {', '.join(map(str, map(int, B)))}.", f"Each B term is {m} times the A term, because {b} = {m} × {a}."],
                [W(str(b - a), "found the difference of the rules"), W(f"1/{m}", "compared A to B instead"), W(str(b), "gave Pattern B's rule")],
                FN("pattern_ratio", a=a, b=b), qtype="conceptual", tags={"reasoning"})


@fam("012")
def rel_pair(r, L):
    a, b, m = two_rules(r, L)
    n = r.randint(3, 6)
    x, y = a * (n - 1), b * (n - 1)
    return Item(f"Pattern A: start at 0, add {a}. Pattern B: start at 0, add {b}. Write the ordered pair (A term, B term) for term {n}.", f"({x}, {y})",
                [f"Term {n} of A is {x}; term {n} of B is {y}.", f"Ordered pair: ({x}, {y})."],
                [W(f"({y}, {x})", "switched the order of the coordinates"), W(f"({a * n}, {b * n})", "counted one term too many"), W(f"({x}, {x + b})", "added B's rule to the A term")],
                FN("pattern_pair", a=a, b=b, n=n), qtype="procedural", tags={"connections"})


@fam("012", mode="mc")
def rel_statement(r, L):
    a, b, m = two_rules(r, L)
    good = f"Each term in Pattern B is {m} times the matching term in Pattern A."
    bad = [f"Each term in Pattern A is {m} times the matching term in Pattern B.", f"Each term in Pattern B is {b - a} more than the matching term in Pattern A.",
           f"Each term in Pattern B is {m} more than the matching term in Pattern A."]
    A, B = terms("add", 0, a, 5), terms("add", 0, b, 5)
    alt = f"Table: Pattern A {', '.join(map(str, map(int, A)))}; Pattern B {', '.join(map(str, map(int, B)))}."
    return mc_key("Look at the two patterns in the table. Which statement is true?", good, bad, [f"Compare matching terms: {int(A[2])} and {int(B[2])}, {int(A[3])} and {int(B[3])}.", good],
                  qtype="explain", tags={"reasoning"}, r=r,
                  diagram=Diagram("two_tables", {"rows": [["Pattern A", [str(int(x)) for x in A]], ["Pattern B", [str(int(x)) for x in B]]]}, alt))


@fam("012")
def rel_missing(r, L):
    a, b, m = two_rules(r, L)
    A, B = terms("add", 0, a, 6), terms("add", 0, b, 6)
    j = r.randint(3, 5)
    Bs = [str(int(x)) for x in B]
    Bs[j] = "?"
    alt = f"Table: Pattern A {', '.join(map(str, map(int, A)))}; Pattern B {', '.join(Bs)}."
    return Item("Use the relationship between the two patterns. What number belongs in place of “?”", str(int(B[j])),
                [f"Each B term is {m} times the A term above it.", f"{m} × {int(A[j])} = {int(B[j])}."],
                [W(str(int(A[j]) + b), "added B's rule to the A term"), W(str(int(B[j]) + b), "skipped a term"), W(str(int(A[j]) * a), "used the wrong multiplier")],
                FN("pattern_term", start="0", op="add", step=str(b), n=j + 1), qtype="visual",
                diagram=Diagram("two_tables", {"rows": [["Pattern A", [str(int(x)) for x in A]], ["Pattern B", Bs]]}, alt))


@fam("12", mode="mc")
def rel_why(r, L):
    a, b, m = two_rules(r, L)
    good = f"Both start at 0, and Pattern B adds {b} each time, which is {m} times the {a} that Pattern A adds."
    bad = [f"Pattern B adds {b - a} more than Pattern A each time.", f"Pattern B started with a bigger number.", f"Pattern A multiplies by {m} each time."]
    return mc_key(f"Pattern A: start at 0, add {a}. Pattern B: start at 0, add {b}. Why is every B term {m} times the matching A term?", good, bad,
                  ["Think about how many times each rule has been used.", good], r=r, qtype="explain", tags={"reasoning"})


@fam("012", mode="mc")
def rel_which_pair(r, L):
    a, b, m = two_rules(r, L)
    n = r.randint(2, 6)
    good = f"({a * n}, {b * n})"
    bad = [f"({b * n}, {a * n})", f"({a * n}, {b * n + a})", f"({a * n + 1}, {b * n})"]
    opts = [(good, True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    return Item(f"Pattern A starts at 0 and adds {a}; Pattern B starts at 0 and adds {b}. Which ordered pair (A, B) could come from these patterns?", good,
                [f"Every pair has the form (A, {m} × A) with A a multiple of {a}.", f"{good} fits."],
                check=FN("pattern_pair_any", a=a, b=b), options=opts, mode="mc", qtype="conceptual", tags={"connections"})


@fam("012")
def w_context_value(r, L):
    a, b, c = r.randint(3, 9), r.randint(4, 12), r.randint(2, 9)
    t, good, bad = pick(r, CTX_EXPR)
    if "÷" in good:
        a = b + c * r.randint(2, 9)
    kw = dict(a=a, b=b, c=c, n=name(r))
    good, bad = good.format(**kw), [x.format(**kw) for x in bad]
    q = t.format(**kw).split(" Which expression")[0]
    ask = {"left": "How many stickers are left?", "students": "How many students are there?", "money": "How much money will there be?", "each": "How many cookies does each friend get?"}
    k = "left" if "stickers" in q else "students" if "students" in q else "money" if "$" in q else "each"
    v = ev(good.replace("−", "-"))
    need(v.denominator == 1 and v > 0)
    ans = f"${dec(v)}" if k == "money" else dec(v)
    return Item(f"{q} {ask[k]}", ans, [f"Expression: {good}.", f"Value: {ans}."],
                [W(f"${dec(x)}" if k == "money" else dec(x), "grouped the operations the wrong way") for x in (ev(y.replace("−", "-")) for y in bad) if x.denominator == 1 and x > 0],
                EX(good.replace("−", "-")), qtype="word-problem", tags={"modeling"})


@fam("012")
def w_blank(r, L):
    a, b, c = r.randint(5, 20), r.randint(2, 12), r.randint(2, 9)
    kind = pick(r, ["mult", "sub"])
    if kind == "mult":
        words, expr, blank = f"add {a} and {b}, then multiply by {c}", f"___ × ({a} + {b})", c
    else:
        words, expr, blank = f"multiply {b} by {c}, then subtract {a}", f"{b} × {c} − ___", a
    return Item(f"The words “{words}” are written as {expr}. What number goes in the blank?", str(blank),
                ["Match each number in the words to its place in the expression.", f"The blank is {blank}."],
                [W(str(a if blank != a else b), "matched the wrong number"), W(str(blank + 1), "miscounted"), W(str(a + b), "added the numbers")],
                FN("blank_is", words=words, expr=expr), qtype="fill-blank", tags={"multiple-representations"})


SKILLS = {
    1: dict(name="Order of Operations with Grouping Symbols", fams=[o_eval, o_diff, o_parens, o_first, o_greatest, o_fraction, o_steps]),
    2: dict(name="Writing Numerical Expressions", fams=[w_words, w_value, w_context, w_to_words, w_context_value, w_blank]),
    3: dict(name="Interpreting Expressions Without Evaluating", fams=[i_times, i_which, i_change, i_compare, i_fill, i_how_much]),
    4: dict(name="Generating Numerical Patterns", fams=[p_term, p_list, p_rule, p_table, p_word]),
    5: dict(name="Relationships Between Two Patterns", fams=[rel_times, rel_pair, rel_statement, rel_missing, rel_why, rel_which_pair]),
}
