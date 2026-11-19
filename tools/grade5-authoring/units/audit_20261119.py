"""Grade 5 audit 2026-11-19, batch 5B: items added after the 30 per skill and level (ids end -gNN).

 #4  two multi-step Advanced items in context for every skill (MS)
 #5  two connected four-part constructed-response tasks per unit, Standard and Advanced (CR)
 #12 the decimal point and powers of ten, with place-value charts (5.NBT.A.2)
 #13 fair share from a line plot: redistribute the total equally (5.MD.B.2)
 #14 a figure item for each of the 17 skills that had none
 #17 a new family for each skill and level the verifier flagged as thin

Every item carries an exact check that verify.py re-runs, like the core families. build.py calls added(unit, skill, level)."""
from g5lib import *

# ------------------------------------------------------------------------------------------------ helpers
def xm(v):
    """Expression text for a value as students see it (a mixed number shows its whole and its fraction)."""
    v = F(v)
    if v.denominator == 1 or v < 1:
        return frac(v)
    w = v.numerator // v.denominator
    return f"({w}+{frac(v - w)})"


def round_to(x, place):
    """Round half up to tenths, hundredths or ones."""
    q = {"ones": 1, "tenths": 10, "hundredths": 100}[place]
    return F(int(F(x) * q + F(1, 2)), q)


def ms(prompt, answer, steps, expr, unit=None, form=None, wrong=(), consts=(), diagram=None):
    it = Item(prompt, answer, steps, [W(w, why) for w, why in wrong], EX(expr, unit=unit, form=form), qtype="multi-step",
              tags={"multistep", "realworld"}, diagram=diagram, mode="sa")
    if consts:
        it.consts = list(consts)
    return it


def adv(f):
    """An Advanced-only multi-step family."""
    f.levels, f.mode, f.qtype = [2], "sa", "multi-step"
    return f


def part(prompt, answer, expr, unit=None, form=None):
    return (prompt, answer, EX(expr, unit=unit, form=form))


def cr(lead, parts, steps):
    need(len(parts) == 4)
    return Item(lead + " Answer each part. Show your work.", None, steps, parts=parts, qtype="multi-step", tags={"multistep", "realworld"})


def ul(n, one, many=None):
    return f"{comma(n)} {one if n == 1 else (many or one + 's')}"


# ================================================================================================ #4 Advanced multi-step
# Place value
@adv
def ms_pv1(r, L):
    a = r.randint(3, 9); n = pick(r, [10, 100, 1000]); k = r.randint(2, 5)
    who = name(r)
    tot = a * n * k
    return ms(f"{who} has {k} boxes. Each box holds {comma(n)} bags, and each bag holds {a} marbles. How many marbles does {who} have?",
              comma(tot), [f"One box: {a} × {comma(n)} = {comma(a * n)} marbles.", f"{k} boxes: {comma(a * n)} × {k} = {comma(tot)} marbles."],
              f"{a}*{n}*{k}", wrong=[(comma(a * n), "found one box only"), (comma(a * k), "forgot the bags in each box")])


@adv
def ms_pv2(r, L):
    x = F(r.randint(12, 980), 100); e = r.randint(1, 3); k = r.randint(2, 6)
    p = 10 ** e
    sup = "¹²³"[e - 1]
    return ms(f"A bead weighs {dec(x)} grams. A pack has 10{sup} beads, and a jar holds {k} packs. What is the weight, in grams, of the beads in the jar?",
              f"{dec(x * p * k)} grams", [f"10{sup} = {comma(p)}, so one pack weighs {dec(x)} × {comma(p)} = {dec(x * p)} grams: the decimal point moves {e} place{'s' if e > 1 else ''} right.",
                                            f"{k} packs: {dec(x * p)} × {k} = {dec(x * p * k)} grams."],
              f"{dec(x)}*10^{e}*{k}", unit="grams", wrong=[(f"{dec(x * p)} grams", "found one pack only"), (f"{dec(x * k)} grams", "forgot the 10" + sup)])


@adv
def ms_pv3(r, L):
    a = F(r.randint(1001, 9999), 1000); b = F(r.randint(101, 999), 100)
    return ms(f"A runner ran {dec(a)} kilometers on Monday and {dec(b)} kilometers on Tuesday. How many kilometers did she run in all? Line up the place values before you add.",
              f"{dec(a + b)} kilometers", [f"{dec(a)} + {dec(b)} = {dec(a + b)}.", "Add thousandths, hundredths, tenths, then ones."], f"{dec(a)}+{dec(b)}", unit="kilometers",
              wrong=[(f"{dec(a - b) if a > b else dec(b - a)} kilometers", "subtracted")])


@adv
def ms_pv4(r, L):
    vals = sorted({F(r.randint(1001, 1999), 1000) for _ in range(4)})
    need(len(vals) == 4)
    names = [name(sub(r, i)) for i in range(4)]
    need(len(set(names)) == 4)
    order = r.sample(range(4), 4)
    lines = ", ".join(f"{names[i]} {dec(vals[order.index(i)])} meters" for i in range(4))
    big, small = max(vals), min(vals)
    return ms(f"Long-jump distances: {lines}. How much farther was the longest jump than the shortest?",
              f"{dec(big - small)} meters", [f"Compare place by place: the longest is {dec(big)} meters and the shortest is {dec(small)} meters.",
                                           f"{dec(big)} − {dec(small)} = {dec(big - small)} meters."],
              f"{dec(big)}-{dec(small)}", unit="meters", wrong=[(f"{dec(big + small)} meters", "added")])


@adv
def ms_pv5(r, L):
    p = [F(r.randint(105, 995), 100) for _ in range(3)]
    tot = sum(round_to(x, "tenths") for x in p)
    return ms(f"Three packages weigh {dec(p[0])}, {dec(p[1])} and {dec(p[2])} pounds. Round each weight to the nearest tenth, then add the rounded weights.",
              f"{dec(tot)} pounds", [f"Rounded: {', '.join(dec(round_to(x, 'tenths')) for x in p)}.", f"Sum: {dec(tot)} pounds."],
              f"{dec(round_to(p[0], 'tenths'))}+{dec(round_to(p[1], 'tenths'))}+{dec(round_to(p[2], 'tenths'))}", unit="pounds",
              consts=[round_to(x, "tenths") for x in p], wrong=[(f"{dec(sum(p))} pounds", "added without rounding")])


# Multiplication and division
@adv
def ms_md1(r, L):
    rows, seats, price = r.randint(21, 48), r.randint(24, 38), r.randint(12, 25)
    return ms(f"A theater has {rows} rows with {seats} seats in each row. Tickets cost ${price}. How much money is collected if every seat is sold?",
              f"${comma(rows * seats * price)}", [f"Seats: {rows} × {seats} = {comma(rows * seats)}.", f"Money: {comma(rows * seats)} × ${price} = ${comma(rows * seats * price)}."],
              f"{rows}*{seats}*{price}", unit="$", wrong=[(f"${comma(rows * seats)}", "found the seats only")])


@adv
def ms_md2(r, L):
    n, c = r.randint(18, 32), r.randint(38, 62); bud = pick(r, [1000, 1200, 1500, 2000])
    est = round(n, -1) * round(c, -1)
    ok = "yes" if n * c <= bud else "no"
    return ms(f"A class of {n} students goes on a trip that costs ${c} per student. The class has ${comma(bud)}. Estimate the cost by rounding each number to the nearest ten, then find the exact cost. What is the exact cost?",
              f"${comma(n * c)}", [f"Estimate: {round(n, -1)} × {round(c, -1)} = {comma(est)}.", f"Exact: {n} × {c} = {comma(n * c)}, so ${comma(n * c)} ({'enough' if ok == 'yes' else 'not enough'} money)."],
              f"{n}*{c}", unit="$", wrong=[(f"${comma(est)}", "gave the estimate")])


@adv
def ms_md3(r, L):
    per, d = r.randint(6, 9), r.randint(3, 9); c = r.randint(6, 20); q = d * c; tot = per * q
    return ms(f"A baker made {comma(tot)} cookies. She packs {per} cookies in each box and ships the boxes in cartons of {d} boxes. How many cartons does she ship?",
              str(c), [f"Boxes: {comma(tot)} ÷ {per} = {q}.", f"Cartons: {q} ÷ {d} = {c}."], f"{tot}/{per}/{d}",
              wrong=[(str(q), "gave the boxes, not the cartons"), (str(tot // d), "divided by the carton size only")])


@adv
def ms_md4(r, L):
    d = r.randint(12, 36); q = r.randint(14, 60); extra = r.randint(1, d - 1); tot = d * q + extra
    return ms(f"A farm packs {comma(tot)} eggs into cartons of {d}. Full cartons are sold for $3 each. How much money is that for the full cartons?",
              f"${comma(3 * q)}", [f"{comma(tot)} ÷ {d} = {q} R {extra}, so {q} full cartons.", f"{q} × $3 = ${comma(3 * q)}."],
              f"({tot}-{extra})/{d}*3", unit="$", consts=[extra], wrong=[(f"${comma(3 * (q + 1))}", "counted the partly full carton")])


@adv
def ms_md5(r, L):
    per = r.randint(12, 30); q = r.randint(6, 20); extra = r.randint(1, per - 1); people = per * q + extra; cost = r.randint(80, 150)
    return ms(f"{comma(people)} people are going on a trip. Each bus holds {per} people and costs ${cost} to rent. What is the cost of the buses if everyone rides?",
              f"${comma((q + 1) * cost)}", [f"{comma(people)} ÷ {per} = {q} R {extra}; the {extra} extra people need one more bus, so {q + 1} buses.",
                                           f"{q + 1} × ${cost} = ${comma((q + 1) * cost)}."],
              f"({q}+1)*{cost}", unit="$", consts=[q], wrong=[(f"${comma(q * cost)}", "ignored the remainder")])


# Decimal operations
@adv
def ms_do1(r, L):
    a, b, c = F(r.randint(1205, 4999), 100), F(r.randint(305, 1999), 100), F(r.randint(2000, 9000), 100)
    need(c > a + b - 50 and c != a + b)
    return ms(f"Rosa buys a book for ${dec(a, 2)} and a game for ${dec(b, 2)}. She pays with ${dec(c, 2) if c >= a + b else dec(a + b + 10, 2)}. How much change does she get?",
              money((c if c >= a + b else a + b + 10) - a - b), [f"Total: ${dec(a, 2)} + ${dec(b, 2)} = ${dec(a + b, 2)}.", f"Change: subtract the total from what she paid."],
              f"{dec(c if c >= a + b else a + b + 10)}-{dec(a)}-{dec(b)}", unit="$", wrong=[(money(a + b), "gave the total")])


@adv
def ms_do2(r, L):
    p, n, m = F(r.randint(105, 899), 100), r.randint(3, 9), r.randint(2, 6)
    return ms(f"Pens cost ${dec(p, 2)} each and notebooks cost twice as much as a pen. Ana buys {n} pens and {m} notebooks. What is the total cost?",
              money(p * n + 2 * p * m), [f"Pens: {n} × ${dec(p, 2)} = {money(p * n)}.", f"Notebooks: {m} × ${dec(2 * p, 2)} = {money(2 * p * m)}.", f"Total: {money(p * n + 2 * p * m)}."],
              f"{dec(p)}*{n}+2*{dec(p)}*{m}", unit="$", wrong=[(money(p * (n + m)), "used the pen price for notebooks")])


@adv
def ms_do3(r, L):
    l, w = F(r.randint(21, 89), 10), F(r.randint(11, 49), 10); c = F(r.randint(105, 495), 100)
    return ms(f"A rectangular patio is {dec(l)} meters long and {dec(w)} meters wide. Tile costs ${dec(c, 2)} per square meter. What does tile for the patio cost?",
              money(l * w * c) if (l * w * c * 100).denominator == 1 else (_ for _ in ()).throw(Reject()),
              [f"Area: {dec(l)} × {dec(w)} = {dec(l * w)} square meters.", f"Cost: {dec(l * w)} × ${dec(c, 2)} = {money(l * w * c)}."],
              f"{dec(l)}*{dec(w)}*{dec(c)}", unit="$", wrong=[(money((l + w) * c), "added length and width")])


@adv
def ms_do4(r, L):
    k = r.randint(3, 8); each = F(r.randint(125, 980), 100); tip = r.randint(2, 9)
    tot = each * k + tip
    return ms(f"{k} friends share a meal. The food costs ${dec(each * k, 2)}, and they leave a tip of ${tip}. They split the whole bill equally. How much does each friend pay?",
              money(tot / k) if (tot / k * 100).denominator == 1 else (_ for _ in ()).throw(Reject()),
              [f"Whole bill: ${dec(each * k, 2)} + ${tip} = {money(tot)}.", f"Each: {money(tot)} ÷ {k} = {money(tot / k)}."],
              f"({dec(each * k)}+{tip})/{k}", unit="$", wrong=[(money(each), "forgot to share the tip")])


@adv
def ms_do5(r, L):
    rib = F(r.randint(20, 90), 10); piece = pick(r, [F(3, 10), F(4, 10), F(5, 10), F(6, 10), F(25, 100)])
    n = rib / piece
    need(n.denominator == 1)
    return ms(f"Sam has {dec(rib)} meters of ribbon. Sam cuts it into pieces {dec(piece)} meter long and ties 2 pieces on each gift. How many gifts can Sam wrap?",
              str(int(n) // 2), [f"Pieces: {dec(rib)} ÷ {dec(piece)} = {int(n)}.", f"Gifts: {int(n)} ÷ 2 = {int(n) // 2}" + (" (one piece is left over)." if int(n) % 2 else ".")],
              f"({dec(rib)}/{dec(piece)}-{int(n) % 2})/2", consts=[int(n) % 2], wrong=[(str(int(n)), "gave the pieces, not the gifts")])


@adv
def ms_do6(r, L):
    wage = F(r.randint(900, 1500), 100); h = r.randint(4, 12); save = F(r.randint(1500, 4000), 100)
    return ms(f"Kai earns ${dec(wage, 2)} an hour and works {h} hours. He spends ${dec(save, 2)} on shoes. How much of his pay is left?",
              money(wage * h - save) if wage * h > save else (_ for _ in ()).throw(Reject()), [f"Pay: {h} × ${dec(wage, 2)} = {money(wage * h)}.", f"Left: {money(wage * h)} − ${dec(save, 2)} = {money(wage * h - save)}."],
              f"{dec(wage)}*{h}-{dec(save)}", unit="$", wrong=[(money(wage * h), "forgot the shoes")])


# Expressions and patterns
@adv
def ms_ne1(r, L):
    a, b, c, d, e = r.randint(2, 9), r.randint(2, 9), r.randint(2, 6), r.randint(2, 20), r.randint(2, 5)
    v = (a + b) * c - d
    need(v > 0 and v % e == 0)
    return ms(f"Evaluate {{[({a} + {b}) × {c}] − {d}}} ÷ {e}. Then add the value to 15.", str(v // e + 15),
              [f"Parentheses: {a} + {b} = {a + b}.", f"Brackets: {a + b} × {c} = {(a + b) * c}.", f"Braces: {(a + b) * c} − {d} = {v}; {v} ÷ {e} = {v // e}.", f"Add to 15: {v // e + 15}."],
              f"(({a}+{b})*{c}-{d})/{e}+15", wrong=[(str((a + b * c - d) // e + 15) if (a + b * c - d) % e == 0 and a + b * c > d else str(v + 15), "skipped a grouping step")])


@adv
def ms_ne2(r, L):
    a, b, k = r.randint(4, 15), r.randint(3, 12), r.randint(2, 5)
    return ms(f"Leo had {a} stickers and got {b} more. Then his number of stickers became {k} times as many as that. Write an expression, then find how many stickers Leo has now.",
              str((a + b) * k), [f"Expression: {k} × ({a} + {b}).", f"{k} × {a + b} = {(a + b) * k}."], f"{k}*({a}+{b})",
              wrong=[(str(k * a + b), "multiplied only the first number")])


@adv
def ms_ne3(r, L):
    a, b, k = r.randint(120, 900), r.randint(10, 99), r.randint(3, 9)
    return ms(f"Without finding either value, how many times as large is {k} × ({comma(a)} + {b}) as {comma(a)} + {b}? Then check by finding both values: what is the larger value?",
              comma(k * (a + b)), [f"{k} × ({comma(a)} + {b}) is {k} times as large as {comma(a)} + {b}.", f"Check: {comma(a)} + {b} = {comma(a + b)}; × {k} = {comma(k * (a + b))}."],
              f"{k}*({a}+{b})", wrong=[(comma(a + b), "found the smaller value")])


@adv
def ms_ne4(r, L):
    s, a, n = r.randint(1, 9), r.randint(3, 9), r.randint(6, 10)
    return ms(f"A pattern starts at {s} and adds {a} each time. A second pattern starts at 0 and adds {2 * a}. Add term number {n} of each pattern. What is the sum?",
              str(s + a * (n - 1) + 2 * a * (n - 1)), [f"First pattern, term {n}: {s} + {a} × {n - 1} = {s + a * (n - 1)}.", f"Second pattern, term {n}: {2 * a} × {n - 1} = {2 * a * (n - 1)}.", f"Sum: {s + a * (n - 1) + 2 * a * (n - 1)}."],
              f"{s}+{a}*({n}-1)+{2 * a}*({n}-1)", wrong=[(str(s + a * n + 2 * a * n), "counted one term too many")])


@adv
def ms_ne5(r, L):
    a, b, n = r.randint(2, 6), 0, r.randint(5, 9)
    k = r.randint(2, 4)
    return ms(f"Pattern A starts at 0 and adds {a}. Pattern B starts at 0 and adds {a * k}. When pattern A reaches {a * n}, what number is pattern B at, and how many times as large is it?",
              str(a * k * n), [f"Pattern A reaches {a * n} after {n} steps.", f"Pattern B after {n} steps: {a * k} × {n} = {a * k * n}, which is {k} times {a * n}."],
              f"{a * k}*{a * n}/{a}", wrong=[(str(a * n + a * k), "added the rules")])


# Fraction addition and subtraction
def _fr(r, dens=(2, 3, 4, 5, 6, 8, 10, 12)):
    d = pick(r, dens)
    return F(r.randint(1, d - 1), d)


@adv
def ms_fa1(r, L):
    a, b = _fr(r), _fr(r); need(a.denominator != b.denominator and a + b < 2)
    who = name(r)
    return ms(f"{who} walked {frac(a)} mile to school and {frac(b)} mile to the library. Find the least common denominator, then find the total distance in simplest form.",
              f"{mixed(a + b)} mile{'s' if a + b > 1 else ''}", [f"Common denominator: {a.denominator * b.denominator // __import__('math').gcd(a.denominator, b.denominator)}.", f"{frac(a)} + {frac(b)} = {mixed(a + b)}."],
              f"{frac(a)}+{frac(b)}", unit="miles" if a + b > 1 else "mile", form="mixed")


@adv
def ms_fa2(r, L):
    a, b, c = _fr(r), _fr(r), _fr(r); need(len({a.denominator, b.denominator, c.denominator}) >= 2 and a + b + c < 3)
    return ms(f"A recipe uses {frac(a)} cup of oats, {frac(b)} cup of raisins and {frac(c)} cup of nuts. How many cups is that in all?",
              f"{mixed(a + b + c)} cup{'s' if a + b + c > 1 else ''}", [f"{frac(a)} + {frac(b)} = {mixed(a + b)}.", f"{mixed(a + b)} + {frac(c)} = {mixed(a + b + c)}."],
              f"{frac(a)}+{frac(b)}+{frac(c)}", unit="cups" if a + b + c > 1 else "cup", form="mixed")


@adv
def ms_fa3(r, L):
    a, b = _fr(r), _fr(r); need(a.denominator != b.denominator and a + b < 1)
    rest = 1 - a - b
    return ms(f"Mia painted {frac(a)} of a fence on Saturday and {frac(b)} of it on Sunday. What fraction of the fence is still unpainted?",
              frac(rest), [f"Painted: {frac(a)} + {frac(b)} = {frac(a + b)}.", f"Unpainted: 1 − {frac(a + b)} = {frac(rest)}."],
              f"1-{frac(a)}-{frac(b)}", form="frac", wrong=[(frac(a + b), "gave the painted part")])


@adv
def ms_fa4(r, L):
    w1, w2 = r.randint(3, 8), r.randint(1, 3); a, b = _fr(r, (2, 3, 4, 6, 8)), _fr(r, (2, 3, 4, 6, 8))
    x, y = w1 + a, w2 + b; need(x > y and a < b and a.denominator != b.denominator)
    return ms(f"A board is {mixed(x)} feet long. Jo cuts off {mixed(y)} feet, then cuts the rest into 2 equal pieces. How long is each piece?",
              f"{mixed((x - y) / 2)} feet" if (x - y) / 2 >= 1 else f"{mixed((x - y) / 2)} foot",
              [f"{mixed(x)} − {mixed(y)} = {mixed(x - y)} feet (regroup a whole).", f"{mixed(x - y)} ÷ 2 = {mixed((x - y) / 2)}."],
              f"({mixed(x).replace(' ', '+')}-({mixed(y).replace(' ', '+')}))/2", unit="feet" if (x - y) / 2 >= 1 else "foot", form="mixed")


@adv
def ms_fa5(r, L):
    a, b, c = _fr(r), _fr(r), _fr(r); need(len({a, b, c}) == 3)
    tot = a + b + c
    bm = lambda x: F(round(x * 2), 2)
    est = bm(a) + bm(b) + bm(c)
    return ms(f"Estimate {frac(a)} + {frac(b)} + {frac(c)} by rounding each fraction to 0, 1/2 or 1, then find the exact sum. What is the exact sum?",
              mixed(tot), [f"Estimate: {mixed(bm(a))} + {mixed(bm(b))} + {mixed(bm(c))} = {mixed(est)}.", f"Exact: {mixed(tot)}, close to the estimate."],
              f"{frac(a)}+{frac(b)}+{frac(c)}", form="mixed", wrong=[(mixed(est), "gave the estimate")])


@adv
def ms_fa6(r, L):
    t = r.randint(3, 6); a, b = _fr(r, (4, 8, 3, 6)), _fr(r, (4, 8, 3, 6)); need(a + b < t and a.denominator != b.denominator)
    return ms(f"A pitcher holds {t} liters of juice. Kim pours {frac(a)} liter and Ben pours {frac(b)} liter. How much juice is left?",
              f"{mixed(t - a - b)} liters", [f"Poured: {frac(a)} + {frac(b)} = {mixed(a + b)} liters.", f"Left: {t} − {mixed(a + b)} = {mixed(t - a - b)} liters."],
              f"{t}-{frac(a)}-{frac(b)}", unit="liters", form="mixed")


# Fraction multiplication and division
@adv
def ms_fm1(r, L):
    a, b = r.randint(3, 20), r.randint(3, 8); need(a % b)
    return ms(f"{a} pounds of rice are shared equally among {b} families. Each family uses 1 pound. How much rice does each family have left?",
              f"{mixed(F(a, b) - 1)} pound{'s' if F(a, b) - 1 > 1 else ''}" if F(a, b) > 1 else (_ for _ in ()).throw(Reject()),
              [f"Each family gets {a} ÷ {b} = {mixed(F(a, b))} pounds.", f"Left: {mixed(F(a, b))} − 1 = {mixed(F(a, b) - 1)}."],
              f"{a}/{b}-1", unit="pounds" if F(a, b) - 1 > 1 else "pound", form="mixed")


@adv
def ms_fm2(r, L):
    n = r.randint(3, 9); a = _fr(r, (3, 4, 5, 8)); k = r.randint(2, 4)
    return ms(f"Each of {n} students drinks {frac(a)} liter of water in the morning and the same amount after lunch. How many liters is that in all?",
              f"{mixed(n * a * 2)} liters", [f"One student: {frac(a)} × 2 = {mixed(2 * a)} liters.", f"{n} students: {n} × {mixed(2 * a)} = {mixed(n * a * 2)} liters."],
              f"{n}*{frac(a)}*2", unit="liters", form="mixed")


@adv
def ms_fm3(r, L):
    a, b = _fr(r, (2, 3, 4, 5, 6)), _fr(r, (2, 3, 4, 5, 8)); c = r.randint(12, 60)
    need((c * a * b).denominator == 1)
    return ms(f"There are {c} students. {frac(a)} of them play a sport, and {frac(b)} of those play soccer. How many students play soccer?",
              str(c * a * b), [f"{frac(b)} of {frac(a)} = {frac(a * b)}.", f"{frac(a * b)} × {c} = {c * a * b} students."],
              f"{c}*{frac(a)}*{frac(b)}", wrong=[(str(c * a), "found the sport players only")])


@adv
def ms_fm4(r, L):
    l, w = r.randint(2, 6) + _fr(r, (2, 4)), r.randint(1, 4) + _fr(r, (2, 4)); c = r.randint(2, 9)
    need((l * w * c).denominator == 1)
    return ms(f"A garden bed is {mixed(l)} yards by {mixed(w)} yards. Soil costs ${c} per square yard. How much does soil for the bed cost?",
              f"${l * w * c}", [f"Area: {mixed(l)} × {mixed(w)} = {mixed(l * w)} square yards.", f"Cost: {mixed(l * w)} × ${c} = ${l * w * c}."],
              f"({mixed(l).replace(' ', '+')})*({mixed(w).replace(' ', '+')})*{c}", unit="$")


@adv
def ms_fm5(r, L):
    h = r.randint(40, 72); f1, f2 = pick(r, [F(3, 4), F(2, 3), F(5, 6)]), pick(r, [F(3, 2), F(5, 4), F(4, 3)])
    need((h * f1).denominator == 1 and (h * f2).denominator == 1)
    return ms(f"A tree is {h} inches tall. A bush is {frac(f1)} as tall as the tree, and a pole is {mixed(f2)} times as tall as the tree. How much taller is the pole than the bush?",
              f"{h * f2 - h * f1} inches", [f"Bush: {frac(f1)} × {h} = {h * f1} (less than {h}, since {frac(f1)} < 1).", f"Pole: {mixed(f2)} × {h} = {h * f2} (more, since {mixed(f2)} > 1).", f"Difference: {h * f2 - h * f1} inches."],
              f"{h}*({mixed(f2).replace(' ', '+')})-{h}*{frac(f1)}", unit="inches")


@adv
def ms_fm6(r, L):
    n, d = r.randint(2, 6), pick(r, [2, 3, 4, 5]); k = r.randint(2, 4)
    return ms(f"A coach has {n} pounds of trail mix. She makes bags of 1/{d} pound each and gives {k} bags to each player. How many players get bags?",
              str(n * d // k) if (n * d) % k == 0 else (_ for _ in ()).throw(Reject()),
              [f"Bags: {n} ÷ 1/{d} = {n * d}.", f"Players: {n * d} ÷ {k} = {n * d // k}."], f"{n}*{d}/{k}", wrong=[(str(n * d), "gave the bags")])


@adv
def ms_fm7(r, L):
    t = r.randint(2, 5); a = pick(r, [F(1, 2), F(1, 3), F(1, 4)]); share = r.randint(2, 6)
    need((t * a / share).denominator <= 24)
    return ms(f"A recipe uses {frac(a)} cup of sugar per batch. Lena makes {t} batches, then shares all the cookies equally among {share} friends. How much sugar went into the share for each friend?",
              f"{mixed(t * a / share)} cup", [f"Sugar: {t} × {frac(a)} = {mixed(t * a)} cups.", f"Each share: {mixed(t * a)} ÷ {share} = {mixed(t * a / share)} cup."],
              f"{t}*{frac(a)}/{share}", unit="cup", form="mixed") if t * a / share < 1 else (_ for _ in ()).throw(Reject())


# Measurement
@adv
def ms_mc1(r, L):
    return _mc1(r.randint(3, 9), r.randint(1, 11), r.randint(3, 6))


def _mc1(ft, inch, n):
    tot = (12 * ft + inch) * n
    it = Item(f"Each shelf board is {ft} feet {inch} inches long. How many inches of board are needed for {n} shelves?", f"{tot} inches",
              [f"One board: {ft} × 12 + {inch} = {12 * ft + inch} inches.", f"{n} boards: {12 * ft + inch} × {n} = {tot} inches."],
              [W(f"{(ft + inch) * n} inches", "added feet and inches as if they were the same unit")], EX(f"({ft}*12+{inch})*{n}", unit="inches"),
              qtype="multi-step", tags={"multistep", "realworld"}, mode="sa")
    it.consts = [12]
    return it


@adv
def ms_mc2(r, L):
    gal, cup = r.randint(2, 5), r.randint(1, 3)
    cups = gal * 16
    return ms(f"A cooler holds {gal} gallons of lemonade. How many {cup}-cup servings can be poured from it? (1 gallon = 16 cups)",
              str(cups // cup) if cups % cup == 0 else (_ for _ in ()).throw(Reject()), [f"{gal} gallons = {gal} × 16 = {cups} cups.", f"Servings: {cups} ÷ {cup} = {cups // cup}."],
              f"{gal}*16/{cup}", wrong=[(str(gal * 4), "used quarts instead of cups")])


@adv
def ms_mc3(r, L):
    m, cm = r.randint(2, 9), r.randint(15, 95)
    tot = m * 100 + cm
    k = r.randint(3, 6)
    return ms(f"A ribbon is {m} meters {cm} centimeters long. It is cut into {k} equal pieces. How many centimeters long is each piece?",
              f"{dec(F(tot, k))} centimeters", [f"{m} meters {cm} centimeters = {tot} centimeters.", f"{tot} ÷ {k} = {dec(F(tot, k))} centimeters."],
              f"({m}*100+{cm})/{k}", unit="centimeters") if F(tot, k).denominator in (1, 2, 4, 5, 10) else (_ for _ in ()).throw(Reject())


@adv
def ms_mc4(r, L):
    lb, oz = r.randint(2, 6), r.randint(2, 14); n = r.randint(3, 8)
    tot = (16 * lb + oz) * n
    it = Item(f"Each bag of flour weighs {lb} pounds {oz} ounces. A truck carries {n} bags. How many ounces of flour is that? (1 pound = 16 ounces)", f"{comma(tot)} ounces",
              [f"One bag: {lb} × 16 + {oz} = {16 * lb + oz} ounces.", f"{n} bags: {16 * lb + oz} × {n} = {comma(tot)} ounces."],
              [W(f"{(lb + oz) * n} ounces", "added pounds and ounces as if they were the same unit")], EX(f"({lb}*16+{oz})*{n}", unit="ounces"),
              qtype="multi-step", tags={"multistep", "realworld"}, mode="sa")
    return it


# Volume
@adv
def ms_vo1(r, L):
    l, w, h, k = r.randint(2, 5), r.randint(2, 5), r.randint(2, 4), r.randint(2, 4)
    return ms(f"A box is packed with unit cubes {l} long, {w} wide and {h} high. A second box holds {k} times as many cubes. How many cubes does the second box hold?",
              f"{l * w * h * k} cubes", [f"First box: {l} × {w} × {h} = {l * w * h} cubes.", f"Second: {l * w * h} × {k} = {l * w * h * k} cubes."], f"{l}*{w}*{h}*{k}", unit="cubes")


@adv
def ms_vo2(r, L):
    l, w, h = r.randint(3, 6), r.randint(2, 5), r.randint(2, 5); rm = r.randint(1, l * w - 1)
    return ms(f"A prism of unit cubes is {l} cubes long, {w} cubes wide and {h} cubes tall. {rm} cubes are taken off the top layer. How many cubes are left?",
              f"{l * w * h - rm} cubes", [f"Full prism: {l} × {w} × {h} = {l * w * h}.", f"Left: {l * w * h} − {rm} = {l * w * h - rm} cubes."], f"{l}*{w}*{h}-{rm}", unit="cubes")


@adv
def ms_vo3(r, L):
    l, w, h = r.randint(4, 12), r.randint(3, 9), r.randint(2, 8); fill = r.randint(1, h - 1) if h > 2 else 1
    return ms(f"A fish tank is {l} inches long, {w} inches wide and {h} inches tall. Water fills it to a height of {fill} inches. How many more cubic inches of water fit before it is full?",
              f"{l * w * (h - fill)} cubic inches", [f"Full: {l} × {w} × {h} = {l * w * h}.", f"Water: {l} × {w} × {fill} = {l * w * fill}.", f"More: {l * w * (h - fill)} cubic inches."],
              f"{l}*{w}*({h}-{fill})", unit="cubic inches")


@adv
def ms_vo4(r, L):
    a = [r.randint(2, 6) for _ in range(3)]; b = [r.randint(2, 6) for _ in range(3)]
    va, vb = a[0] * a[1] * a[2], b[0] * b[1] * b[2]
    return ms(f"A step is made of two rectangular prisms: one {a[0]} ft by {a[1]} ft by {a[2]} ft, and one {b[0]} ft by {b[1]} ft by {b[2]} ft. Concrete costs $3 per cubic foot. What does the concrete cost?",
              f"${3 * (va + vb)}", [f"Volumes: {va} and {vb} cubic feet; total {va + vb}.", f"Cost: {va + vb} × $3 = ${3 * (va + vb)}."],
              f"({a[0]}*{a[1]}*{a[2]}+{b[0]}*{b[1]}*{b[2]})*3", unit="$", consts=[3])


@adv
def ms_vo5(r, L):
    l, w, h = pick(r, [12, 16, 18, 20, 24]), pick(r, [8, 10, 12]), pick(r, [6, 8, 10]); s = pick(r, [2, 4])
    need(l % s == 0 and w % s == 0 and h % s == 0)
    return ms(f"A crate is {l} inches long, {w} inches wide and {h} inches tall. How many {s}-inch cubes fit inside with no gaps?",
              str((l // s) * (w // s) * (h // s)), [f"Along each edge: {l // s}, {w // s} and {h // s} cubes.", f"{l // s} × {w // s} × {h // s} = {(l // s) * (w // s) * (h // s)} cubes."],
              f"({l}/{s})*({w}/{s})*({h}/{s})", wrong=[(str(l * w * h), "gave the volume in cubic inches")])


# Coordinate plane
@adv
def ms_cp1(r, L):
    x, y, dx, dy = r.randint(1, 5), r.randint(1, 5), r.randint(1, 4), r.randint(1, 4)
    return ms(f"Start at the origin. Move {x} units right and {y} units up to point A. From A, move {dx} units right and {dy} units up to point B. What is the sum of the coordinates of B?",
              str(x + dx + y + dy), [f"A = ({x}, {y}).", f"B = ({x + dx}, {y + dy}).", f"Sum: {x + dx} + {y + dy} = {x + dx + y + dy}."], f"{x}+{dx}+{y}+{dy}")


@adv
def ms_cp2(r, L):
    x1, y1, x2 = r.randint(1, 4), r.randint(1, 8), r.randint(5, 9)
    return ms(f"Point P is at ({x1}, {y1}) and point Q is at ({x2}, {y1}). A third point R is straight above Q, the same distance from Q as Q is from P. What is the y-coordinate of R?",
              str(y1 + x2 - x1), [f"PQ = {x2} − {x1} = {x2 - x1} units.", f"R is {x2 - x1} above Q: y = {y1} + {x2 - x1} = {y1 + x2 - x1}."], f"{y1}+{x2}-{x1}")


@adv
def ms_cp3(r, L):
    h = (r.randint(1, 4), r.randint(1, 4)); s = (r.randint(5, 9), r.randint(5, 9)); bl = r.randint(2, 5)
    d = abs(s[0] - h[0]) + abs(s[1] - h[1])
    return ms(f"On a town map, home is at ({h[0]}, {h[1]}) and school is at ({s[0]}, {s[1]}). Streets run along the grid lines, and each unit is {bl} blocks. How many blocks is the shortest walk from home to school?",
              f"{d * bl} blocks", [f"Across: {s[0]} − {h[0]} = {s[0] - h[0]} units; up: {s[1]} − {h[1]} = {s[1] - h[1]} units.", f"{d} units × {bl} = {d * bl} blocks."],
              f"(({s[0]}-{h[0]})+({s[1]}-{h[1]}))*{bl}", unit="blocks")


@adv
def ms_cp4(r, L):
    a, b, n = r.randint(2, 5), r.randint(2, 4), r.randint(4, 8)
    return ms(f"Rule A: start at 0 and add {a}. Rule B: start at 0 and add {a * b}. The ordered pairs (A, B) are graphed. What is the y-coordinate of the point whose x-coordinate is {a * n}?",
              str(a * b * n), [f"x = {a * n} is step {a * n} ÷ {a} = {n} of Rule A.", f"Rule B at step {n}: {a * b} × {n} = {a * b * n}."], f"{a * b}*{a * n}/{a}")


# Shapes
@adv
def ms_cs1(r, L):
    n, s, k = pick(r, [5, 6, 8]), r.randint(3, 12), r.randint(2, 5)
    nm = {5: "pentagon", 6: "hexagon", 8: "octagon"}[n]
    return ms(f"A garden is shaped like a regular {nm} with sides of {s} meters. Fencing costs ${k} per meter. What does fencing around the garden cost?",
              f"${n * s * k}", [f"A regular {nm} has {n} equal sides: perimeter {n} × {s} = {n * s} meters.", f"Cost: {n * s} × ${k} = ${n * s * k}."], f"{n}*{s}*{k}", unit="$", consts=[n])


@adv
def ms_cs2(r, L):
    a, b = r.randint(30, 80), r.randint(20, 70); c = 180 - a - b
    need(c > 0 and len({a, b, c}) == 3)
    kind = "right" if 90 in (a, b, c) else "obtuse" if max(a, b, c) > 90 else "acute"
    return ms(f"A triangle has angles of {a}° and {b}°. Find the third angle. (The angles of a triangle add to 180°.)", f"{c}°",
              [f"180 − {a} − {b} = {c}.", f"The triangle is {kind}."], f"180-{a}-{b}", unit="°", consts=[180])


@adv
def ms_cs3(r, L):
    l, w = r.randint(6, 15), r.randint(2, 5)
    return ms(f"A rectangle and a square have the same perimeter. The rectangle is {l} cm long and {w} cm wide. How long is each side of the square?",
              f"{dec(F(2 * (l + w), 4))} cm", [f"Rectangle perimeter: 2 × ({l} + {w}) = {2 * (l + w)} cm.", f"Square side: {2 * (l + w)} ÷ 4 = {dec(F(2 * (l + w), 4))} cm."],
              f"2*({l}+{w})/4", unit="cm", consts=[4])


@adv
def ms_cs4(r, L):
    s, n = r.randint(3, 9), r.randint(3, 6)
    return ms(f"Every square is a rhombus. A rhombus-shaped tile has sides of {s} inches. A border is made from {n} tiles placed side by side in a row. How long is the border?",
              f"{s * n} inches", [f"Each tile is {s} inches wide along the row.", f"{n} × {s} = {s * n} inches."], f"{s}*{n}", unit="inches")


# Data
@adv
def ms_dd(r, L, k):
    vals = sorted(pick(r, [F(1, 4), F(1, 2), F(3, 4), 1, F(5, 4), F(3, 2)]) for _ in range(r.randint(6, 9)))
    tot = sum(vals); n = len(vals)
    lo, hi = min(vals), max(vals)
    alt = "Line plot of rainfall in inches from 0 to 1 1/2 in fourths. X marks: " + ", ".join(f"{mixed(v)}" for v in vals) + "."
    dg = Diagram("lineplot", {"values": [mixed(v) for v in vals], "lo": "0", "hi": "1 1/2", "den": 4, "title": "Rainfall (inches)", "unit": "inches"}, alt)
    if k == 0:
        return ms("The line plot shows rainfall on several days. If the total rain had fallen equally on each day, how much would fall each day?", f"{mixed(tot / n)} inches" if tot / n >= 1 else f"{mixed(tot / n)} inch",
                  [f"Total: {mixed(tot)} inches over {n} days.", f"Equal share: {mixed(tot)} ÷ {n} = {mixed(tot / n)}."], f"({'+'.join(xm(v) for v in vals)})/{n}",
                  unit="inches" if tot / n >= 1 else "inch", form="mixed", diagram=dg, consts=[n])
    return ms("The line plot shows rainfall on several days. How much more rain fell on all the days together than on the wettest day?", f"{mixed(tot - hi)} inches",
              [f"Total: {mixed(tot)} inches; wettest day: {mixed(hi)}.", f"{mixed(tot)} − {mixed(hi)} = {mixed(tot - hi)} inches."], f"({'+'.join(xm(v) for v in vals)})-{xm(hi)}",
              unit="inches", form="mixed", diagram=dg)


@adv
def ms_dd1(r, L):
    return ms_dd(r, L, 1)


@adv
def ms_dd2(r, L):
    return ms_dd(r, L, 0)


ms_dd3, ms_dd4 = ms_dd2, ms_dd1


# ================================================================================================ #5 constructed response
def _cr_levels(levels):
    def deco(f):
        f.levels, f.mode, f.qtype = levels, None, "multi-step"
        return f
    return deco


@_cr_levels([1, 2])
def cr_pv(r, L):
    p = F(r.randint(105, 495), 100) if L == 1 else F(r.randint(1005, 4995), 1000)
    n = 10 if L == 1 else 100
    one, many = ("sticker", "stickers") if L == 1 else ("gallon of gas", "gallons of gas")
    return cr(f"A store sells stickers for ${dec(p)} each." if L == 1 else f"Gas costs ${dec(p)} per gallon.",
              [part(f"What is the cost of {n} {many}?", money(p * n), f"{dec(p)}*{n}", unit="$"),
               part(f"What is the cost of 1,000 {many}?", money(p * 1000), f"{dec(p)}*1000", unit="$"),
               part(f"Round the price of one {one} to the nearest tenth of a dollar.", f"${dec(round_to(p, 'tenths'), 2)}", f"{dec(round_to(p, 'tenths'))}", unit="$"),
               part(f"Using the rounded price, estimate the cost of {n} {many}.", money(round_to(p, 'tenths') * n), f"{dec(round_to(p, 'tenths'))}*{n}", unit="$")],
              [f"(a) Multiplying by {n} moves the decimal point {len(str(n)) - 1} places right.", "(b) × 1,000 moves it 3 places right.", "(c) Look at the hundredths digit.", "(d) Multiply the rounded price."])


@_cr_levels([1, 2])
def cr_md(r, L):
    per = r.randint(12, 24) if L == 1 else r.randint(24, 48); q = r.randint(10, 30); ex = r.randint(1, per - 1); tot = per * q + ex
    cost = r.randint(3, 9)
    return cr(f"A school orders {comma(tot)} pencils. They come in packs of {per}, and each pack costs ${cost}.",
              [part("How many full packs is that?", str(q), f"({tot}-{ex})/{per}"),
               part("How many pencils are left over, not making a full pack?", str(ex), f"{tot}-{per}*{q}"),
               part("How many packs must be bought to get at least that many pencils?", str(q + 1), f"({tot}-{ex})/{per}+1"),
               part("How much do those packs cost?", f"${(q + 1) * cost}", f"(({tot}-{ex})/{per}+1)*{cost}", unit="$")],
              [f"(a) {comma(tot)} ÷ {per} = {q} R {ex}.", f"(b) The remainder is {ex}.", f"(c) {q} packs are not enough, so {q + 1}.", f"(d) {q + 1} × ${cost}."])


@_cr_levels([1, 2])
def cr_do(r, L):
    p1, p2 = F(r.randint(125, 499), 100), F(r.randint(105, 299), 100); n1, n2 = r.randint(2, 5), r.randint(2, 6); pay = 20 if L == 1 else 50
    tot = p1 * n1 + p2 * n2
    need(tot < pay)
    return cr(f"At a market, apples cost ${dec(p1, 2)} per pound and pears cost ${dec(p2, 2)} per pound. Jada buys {n1} pounds of apples and {n2} pounds of pears and pays with ${pay}.",
              [part("How much do the apples cost?", money(p1 * n1), f"{dec(p1)}*{n1}", unit="$"),
               part("How much do the pears cost?", money(p2 * n2), f"{dec(p2)}*{n2}", unit="$"),
               part("What is the total cost?", money(tot), f"{dec(p1)}*{n1}+{dec(p2)}*{n2}", unit="$"),
               part("How much change does she get?", money(pay - tot), f"{pay}-{dec(p1)}*{n1}-{dec(p2)}*{n2}", unit="$")],
              ["(a) price × pounds.", "(b) price × pounds.", "(c) Add the two costs.", f"(d) Subtract the total from ${pay}."])


@_cr_levels([1, 2])
def cr_ne(r, L):
    a, b = r.randint(2, 5), r.randint(3, 6)
    return cr(f"Pattern A starts at 0 and adds {a}. Pattern B starts at 0 and adds {a * b}.",
              [part("What number does Pattern A reach 4 steps after 0?", str(4 * a), f"4*{a}"),
               part("What number does Pattern B reach 4 steps after 0?", str(4 * a * b), f"4*{a * b}"),
               part("Each term of Pattern B is how many times the matching term of Pattern A?", str(b), f"{a * b}/{a}"),
               part(f"Evaluate {b} × (4 × {a}) and check that it matches your answer for Pattern B.", str(4 * a * b), f"{b}*(4*{a})")],
              [f"(a) {a}, {2 * a}, {3 * a}, {4 * a}.", f"(b) {a * b}, …, {4 * a * b}.", f"(c) {a * b} ÷ {a} = {b}.", f"(d) {b} × {4 * a} = {4 * a * b}."])


@_cr_levels([1, 2])
def cr_fa(r, L):
    a, b = (F(1, 2), F(1, 3)) if L == 1 else (F(2, 5), F(1, 4))
    c = F(1, 12) if L == 1 else F(1, 6)
    return cr(f"A class garden is planted with tomatoes in {frac(a)} of it and beans in {frac(b)} of it.",
              [part("What fraction of the garden is tomatoes and beans together?", mixed(a + b), f"{frac(a)}+{frac(b)}", form="mixed"),
               part("How much more of the garden is tomatoes than beans?", frac(a - b), f"{frac(a)}-{frac(b)}", form="frac"),
               part(f"Peppers take {frac(c)} of the garden. What fraction is tomatoes, beans and peppers together?", mixed(a + b + c), f"{frac(a)}+{frac(b)}+{frac(c)}", form="mixed"),
               part("The rest of the garden is for flowers. What fraction is for flowers?", frac(1 - (a + b + c)), f"1-({frac(a)}+{frac(b)}+{frac(c)})", form="frac")],
              ["(a) Use a common denominator.", "(b) Subtract with a common denominator.", "(c) Add the third fraction.", "(d) Subtract the total from 1 whole."])


@_cr_levels([1, 2])
def cr_fm(r, L):
    l, w = (F(3, 4), F(2, 3)) if L == 1 else (F(5, 2), F(4, 3)); k = 3 if L == 1 else 6
    return cr(f"A rectangular rug is {mixed(l)} yard long and {mixed(w)} yard wide." if L == 1 else f"A rectangular rug is {mixed(l)} yards long and {mixed(w)} yards wide.",
              [part("What is the area of the rug?", f"{mixed(l * w)} square yard{'s' if l * w > 1 else ''}", f"{frac(l)}*{frac(w)}", unit="square yards" if l * w > 1 else "square yard", form="mixed"),
               part(f"A second rug is {k} times as long and just as wide. What is its area?", f"{mixed(l * w * k)} square yards", f"{k}*{frac(l)}*{frac(w)}", unit="square yards", form="mixed"),
               part(f"How many more square yards is the second rug than the first?", f"{mixed(l * w * (k - 1))} square yard{'s' if l * w * (k - 1) != 1 else ''}", f"{k}*{frac(l)}*{frac(w)}-{frac(l)}*{frac(w)}", unit="square yards" if l * w * (k - 1) != 1 else "square yard", form="mixed"),
               part(f"The second rug is cut into pieces of 1/4 square yard. How many pieces?", str(l * w * k * 4) if (l * w * k * 4).denominator == 1 else (_ for _ in ()).throw(Reject()), f"{k}*{frac(l)}*{frac(w)}*4")],
              ["(a) Multiply the side lengths.", f"(b) {k} times the length gives {k} times the area.", "(c) Subtract.", "(d) Divide by 1/4: multiply by 4."])


@_cr_levels([1, 2])
def cr_mc(r, L):
    ft = r.randint(4, 9); inch = r.randint(2, 10); n = r.randint(3, 5)
    tot = (12 * ft + inch) * n
    it = cr(f"Each wooden plank is {ft} feet {inch} inches long. A builder needs {n} planks.",
            [part("How many inches long is one plank?", f"{12 * ft + inch} inches", f"{ft}*12+{inch}", unit="inches"),
             part(f"How many inches of plank are needed for {n} planks?", f"{tot} inches", f"({ft}*12+{inch})*{n}", unit="inches"),
             part("How many whole feet is that?", f"{tot // 12} feet", f"(({ft}*12+{inch})*{n}-{tot % 12})/12", unit="feet"),
             part("How many inches are left over after the whole feet?", f"{tot % 12} inches" if tot % 12 != 1 else "1 inch", f"({ft}*12+{inch})*{n}-12*{tot // 12}", unit="inches" if tot % 12 != 1 else "inch")],
            ["(a) 1 foot = 12 inches.", "(b) Multiply by the number of planks.", "(c) Divide by 12.", "(d) The remainder."])
    need(tot % 12 != 0)
    it.consts = [12, tot % 12, tot // 12]
    return it


@_cr_levels([1, 2])
def cr_vo(r, L):
    l, w, h = r.randint(4, 10), r.randint(3, 8), r.randint(2, 6); e = r.randint(2, 4)
    return cr(f"A storage box is {l} feet long, {w} feet wide and {h} feet tall.",
              [part("What is the area of the base?", f"{l * w} square feet", f"{l}*{w}", unit="square feet"),
               part("What is the volume of the box?", f"{l * w * h} cubic feet", f"{l}*{w}*{h}", unit="cubic feet"),
               part(f"A second box has the same base and is {e} feet taller. What is its volume?", f"{l * w * (h + e)} cubic feet", f"{l}*{w}*({h}+{e})", unit="cubic feet"),
               part("What is the combined volume of the two boxes?", f"{l * w * h + l * w * (h + e)} cubic feet", f"{l}*{w}*{h}+{l}*{w}*({h}+{e})", unit="cubic feet")],
              ["(a) B = l × w.", "(b) V = B × h.", "(c) Same base, new height.", "(d) Add the volumes."])


@_cr_levels([1, 2])
def cr_cp(r, L):
    x1, y1 = r.randint(1, 3), r.randint(1, 3); dx, dy = r.randint(3, 6), r.randint(2, 5)
    return cr(f"On a map grid, the library is at ({x1}, {y1}). The park is {dx} units to the right of the library, and the pool is {dy} units above the park.",
              [part("What is the x-coordinate of the park?", str(x1 + dx), f"{x1}+{dx}"),
               part("What is the y-coordinate of the pool?", str(y1 + dy), f"{y1}+{dy}"),
               part("Walking along grid lines, how many units is it from the library to the pool?", str(dx + dy), f"{dx}+{dy}"),
               part("If each unit is 50 meters, how many meters is that walk?", f"{50 * (dx + dy)} meters", f"({dx}+{dy})*50", unit="meters")],
              [f"(a) {x1} + {dx}.", f"(b) {y1} + {dy}.", "(c) Right, then up.", "(d) Multiply by 50."])


@_cr_levels([1, 2])
def cr_cs(r, L):
    s = r.randint(3, 9); l = s + r.randint(2, 6)
    it = cr(f"A square has sides of {s} cm. A rectangle is {l} cm long and {s} cm wide.",
            [part("What is the perimeter of the square?", f"{4 * s} cm", f"4*{s}", unit="cm"),
             part("What is the perimeter of the rectangle?", f"{2 * (l + s)} cm", f"2*({l}+{s})", unit="cm"),
             part("How much greater is the perimeter of the rectangle?", f"{2 * (l + s) - 4 * s} cm", f"2*({l}+{s})-4*{s}", unit="cm"),
             part("How many right angles are there in the two shapes in all?", "8", "4+4")],
            ["(a) 4 equal sides.", "(b) 2 lengths + 2 widths.", "(c) Subtract.", "(d) Every square is a rectangle: 4 right angles each."])
    it.consts = [4]
    return it


@_cr_levels([1, 2])
def cr_dd(r, L):
    vals = sorted(pick(r, [F(1, 8), F(1, 4), F(3, 8), F(1, 2), F(5, 8), F(3, 4)]) for _ in range(6 if L == 1 else 8))
    need(len(set(vals)) >= 3)
    tot = sum(vals); n = len(vals)
    alt = "Line plot of the amount of water in beakers, in liters, from 0 to 3/4 in eighths. X marks: " + ", ".join(frac(v) for v in vals) + "."
    it = cr("The line plot shows the water in some beakers, in liters.",
            [part("How many beakers are there?", str(n), "+".join("1" for _ in vals)),
             part("How much water is in the beakers in all?", f"{mixed(tot)} liter{'s' if tot > 1 else ''}", "+".join(frac(v) for v in vals), unit="liters" if tot > 1 else "liter", form="mixed"),
             part("What is the difference between the most and least water in one beaker?", f"{frac(max(vals) - min(vals))} liter", f"{frac(max(vals))}-{frac(min(vals))}", unit="liter", form="frac"),
             part("If the water were shared equally among the beakers, how much would each hold?", f"{frac(tot / n)} liter", f"({'+'.join(xm(v) for v in vals)})/{n}", unit="liter", form="frac")],
            ["(a) Count the X marks.", "(b) Add the values.", "(c) Greatest − least.", "(d) Total ÷ number of beakers."],)
    it.diagram = Diagram("lineplot", {"values": [frac(v) for v in vals], "lo": "0", "hi": "3/4", "den": 8, "title": "Water in beakers (liters)", "unit": "liters"}, alt)
    it.consts = [n]
    return it


# ================================================================================================ #12 decimal point and powers of ten
@fam("012")
def pt_shift(r, L):
    x = F(r.randint(11, 999), 100) if L < 2 else F(r.randint(101, 9999), 1000)
    e = r.randint(1, 3); op = pick(r, ["×", "÷"])
    y = x * 10 ** e if op == "×" else x / 10 ** e
    need(len(dec(y).partition(".")[2]) <= 4)
    sup = "¹²³"[e - 1]
    digits = dec(x).replace(".", "")
    alt = f"Place-value chart showing {dec(x)}."
    s = dec(x)
    w, _, f = s.partition(".")
    places = ["thousands", "hundreds", "tens", "ones", "tenths", "hundredths", "thousandths"]
    dg = {}
    for i, ch in enumerate(reversed(w.replace(",", ""))):
        dg[places[3 - i]] = ch
    for i, ch in enumerate(f):
        dg[places[4 + i]] = ch
    used = [p for p in places if p in dg or p in ("ones", "tenths", "hundredths")]
    return Item(f"The chart shows {dec(x)}. What is {dec(x)} {op} 10{sup}?", dec(y),
                [f"10{sup} = {comma(10 ** e)}.", f"{'Multiplying' if op == '×' else 'Dividing'} by 10{sup} moves each digit {e} place{'s' if e > 1 else ''} to the {'left' if op == '×' else 'right'}: the decimal point moves {e} place{'s' if e > 1 else ''} {'right' if op == '×' else 'left'}.", f"{dec(x)} {op} 10{sup} = {dec(y)}."],
                [W(dec(x * 10 ** e if op == '÷' else x / 10 ** e), "moved the decimal point the wrong way"), W(dec(x * 10 ** (e - 1) if op == '×' else x / 10 ** (e - 1)) if e > 1 else dec(x * 10 ** (e + 1) if op == '×' else x / 10 ** (e + 1)), "moved it the wrong number of places"),
                 W(dec(x * 10 * e) if op == '×' else dec(x / (10 * e)), "multiplied the exponent by 10")],
                EX(f"{dec(x)}{'*' if op == '×' else '/'}10^{e}", form="dec"), qtype="visual",
                diagram=Diagram("place_chart", {"places": used, "digits": dg}, alt))


@fam("012")
def pt_which_power(r, L):
    return _which_power(F(r.randint(11, 999), 100), r.randint(1, 3))


def _which_power(x, e):
    y = x * 10 ** e
    it = Item(f"{dec(x)} × 10 to what power = {dec(y)}? Give the exponent.", str(e),
              [f"The decimal point moved from {dec(x)} to {dec(y)}: {e} place{'s' if e > 1 else ''} to the right.", f"So the exponent is {e} (10 multiplied {e} time{'s' if e > 1 else ''})."],
              [W(str(e + 1), "counted the digits"), W(str(10 ** e) if e > 1 else "100", "gave the power of ten, not the exponent"), W(str(e + 2), "miscounted the places")],
              EX(f"{e}"), qtype="conceptual", tags={"reasoning"})
    it.consts = [e]
    return it


# ================================================================================================ #13 fair share from a line plot
@fam("012")
def lp_fair_share(r, L):
    den = pick(r, [2, 4]) if L == 0 else pick(r, [4, 8])
    n = r.randint(4, 6) if L == 0 else r.randint(6, 9)
    vals = sorted(F(r.randint(1, 2 * den), den) for _ in range(n))
    tot = sum(vals)
    need((tot / n).denominator <= 16 and len(set(vals)) >= 2)
    hi = max(F(2), max(vals))
    alt = f"Line plot titled Juice in each jar (cups), from 0 to {mixed(hi)} in steps of 1/{den}. X marks: " + ", ".join(mixed(v) for v in vals) + "."
    dg = Diagram("lineplot", {"values": [mixed(v) for v in vals], "lo": "0", "hi": mixed(hi), "den": den, "title": "Juice in each jar (cups)", "unit": "cups"}, alt)
    ans = f"{mixed(tot / n)} cup{'s' if tot / n > 1 else ''}"
    it = Item("The line plot shows how much juice is in each jar. If all the juice were poured out and shared equally among the jars, how much would each jar hold?", ans,
              [f"Total: {' + '.join(mixed(v) for v in vals)} = {mixed(tot)} cups.", f"There are {n} jars: {mixed(tot)} ÷ {n} = {mixed(tot / n)}."],
              [W(f"{mixed(tot)} cups", "gave the total"), W(f"{mixed(max(vals) - min(vals))} cup{'s' if max(vals) - min(vals) > 1 else ''}", "found the range"), W(f"{mixed(vals[n // 2])} cup{'s' if vals[n // 2] > 1 else ''}", "took the middle value")],
              EX(f"({'+'.join(xm(v) for v in vals)})/{n}", unit="cups" if tot / n > 1 else "cup", form="mixed"), qtype="visual", tags={"realworld"}, diagram=dg)
    it.consts = [n]
    return it


# ================================================================================================ #14 figures for skills with none, #17 more families
@fam("012")
def fig_powers_chart(r, L):          # place value s2 (also #12)
    return pt_shift(r, L)


@fam("012")
def fig_estimate_area(r, L):         # mult/div s2
    return _est_area(r.randint(21, 89), r.randint(21, 89))


def _est_area(a, b):
    ra, rb = round(a, -1), round(b, -1)
    need(ra != a and rb != b)
    dg = Diagram("area_model", {"rows": [str(rb)], "cols": [str(ra)], "cells": [[comma(ra * rb)]]}, f"Area model with side lengths {ra} and {rb} and area {comma(ra * rb)}.")
    return Item(f"Estimate {a} × {b} by rounding each factor to the nearest ten. The area model shows the rounded factors. Is the exact product greater or less than the estimate, and what is the estimate?",
                comma(ra * rb), [f"{a} rounds to {ra}; {b} rounds to {rb}.", f"Estimate: {ra} × {rb} = {comma(ra * rb)} (the exact product {comma(a * b)} is {'greater' if a * b > ra * rb else 'less'})."],
                [W(comma(a * b), "gave the exact product"), W(comma(ra + rb), "added the rounded factors"), W(comma(ra * (rb + 10)), "rounded a factor the wrong way")],
                EX(f"{ra}*{rb}"), qtype="visual", diagram=dg)


@fam("012")
def fig_remainder_tape(r, L):        # mult/div s5
    per, q = r.randint(4, 9), r.randint(3, 7); ex = r.randint(1, per - 1); tot = per * q + ex
    alt = f"Tape diagram: {tot} students split into groups of {per}: {q} full groups and {ex} left over."
    dg = Diagram("tape", {"parts": q + 1, "shaded": q, "total_label": f"{tot} students", "each": "", "note": f"{q} full vans of {per}, {ex} left"}, alt)
    return Item(f"{tot} students are going on a trip in vans that hold {per} students each. The tape diagram shows the vans. How many vans are needed so every student rides?", str(q + 1),
                [f"{tot} ÷ {per} = {q} R {ex}.", f"The {ex} students left over need one more van: {q + 1} vans."],
                [W(str(q), "ignored the remainder"), W(f"{q} R {ex}", "gave the quotient and remainder"), W(str(ex), "gave the remainder")],
                EX(f"({tot}-{ex})/{per}+1", form="whole"), qtype="visual", tags={"realworld"}, diagram=dg)


@fam("012")
def fig_money_tape(r, L):            # decimals s6
    p = F(r.randint(125, 899), 100); n = r.randint(3, 5)
    alt = f"Tape diagram with {n} equal parts, each labeled ${dec(p, 2)}."
    dg = Diagram("tape", {"parts": n, "shaded": n, "each": f"${dec(p, 2)}", "total_label": "?", "note": ""}, alt)
    return Item(f"The tape diagram shows {n} tickets that cost ${dec(p, 2)} each. What is the total cost?", money(p * n),
                [f"{n} equal parts of ${dec(p, 2)}.", f"{n} × ${dec(p, 2)} = {money(p * n)}."],
                [W(money(p + n), "added"), W(money(p * (n - 1)), "counted one part too few"), W(money(p * n * 10), "misplaced the decimal point")],
                EX(f"{dec(p)}*{n}", unit="$"), qtype="visual", tags={"realworld"}, diagram=dg)


@fam("012")
def fig_order_ops(r, L):             # expressions s1 (#17 cp2 thin too)
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 5)
    alt = f"Two tables: ({a} + {b}) × {c} and {a} + {b} × {c}, with their steps."
    rows = [[f"({a} + {b}) × {c}", f"{a + b} × {c}", "?"], [f"{a} + {b} × {c}", f"{a} + {b * c}", str(a + b * c)]]
    dg = Diagram("table", {"header": ["Expression", "First step", "Value"], "rows": rows}, alt)
    return Item(f"The table shows two expressions. The second is done for you. What is the value of ({a} + {b}) × {c}?", str((a + b) * c),
                [f"Parentheses first: {a} + {b} = {a + b}.", f"{a + b} × {c} = {(a + b) * c}."],
                [W(str(a + b * c), "ignored the parentheses"), W(str(a * c + b), "multiplied the wrong number"), W(str(a + b + c), "added all three")],
                EX(f"({a}+{b})*{c}"), qtype="visual", diagram=dg)


@fam("012")
def fig_write_expr(r, L):            # expressions s2
    a, b = r.randint(2, 9), r.randint(3, 12)
    alt = f"Tape diagram: {a} equal parts, each labeled {b} + 4."
    dg = Diagram("tape", {"parts": a, "shaded": a, "each": f"{b} + 4", "total_label": "?", "note": ""}, alt)
    return Item(f"The tape diagram has {a} equal parts, each {b} + 4. Write the value of the expression {a} × ({b} + 4).", str(a * (b + 4)),
                [f"Each part is {b} + 4 = {b + 4}.", f"{a} × {b + 4} = {a * (b + 4)}."],
                [W(str(a * b + 4), "multiplied only the first term"), W(str(a + b + 4), "added"), W(str(a * b), "left out the 4")],
                EX(f"{a}*({b}+4)"), qtype="visual", diagram=dg)


@fam("012", mode="mc")
def fig_interpret(r, L):             # expressions s3
    a, b, k = r.randint(100, 900), r.randint(10, 99), r.randint(2, 9)
    alt = f"Two tapes: one labeled {a} + {b}, and one {k} times as long labeled {k} × ({a} + {b})."
    dg = Diagram("tape", {"parts": k, "shaded": 1, "each": f"{a} + {b}", "total_label": f"{k} × ({a} + {b})", "note": ""}, alt)
    return mc_key(f"The tape shows {k} × ({a} + {b}). Without calculating, how does it compare with {a} + {b}?", f"It is {k} times as large.",
                  [f"It is {k} more.", f"It is {k} times as small.", "They are equal."],
                  [f"The tape is {k} copies of {a} + {b}.", f"So it is {k} times as large."], qtype="visual", diagram=dg, r=r)


@fam("012")
def fig_mixed_line(r, L):            # fraction add s4
    d = pick(r, [2, 4, 3]); w = r.randint(1, 3); a = w + F(r.randint(1, d - 1), d); b = F(r.randint(d + 1, 2 * d), d)
    need(b != F(2))
    hi = int(a + b) + 1
    alt = f"Number line from 0 to {hi} in steps of 1/{d}, with a jump from {mixed(a)} of {mixed(b)}."
    dg = Diagram("number_line", {"lo": "0", "hi": str(hi), "den": d, "label_every": d, "jumps": [[frac(a), frac(a + b)]]}, alt)
    return Item(f"The number line starts at {mixed(a)} and jumps forward {mixed(b)}. Where does it land? Write a mixed number.", mixed(a + b),
                [f"{mixed(a)} + {mixed(b)}.", f"= {mixed(a + b)}."],
                [W(mixed(a + b - F(1, d)), "landed one tick short"), W(mixed(a + b + 1), "counted an extra whole"), W(frac(a + b), "left it as an improper fraction")],
                EX(f"{frac(a)}+{frac(b)}", form="mixed"), qtype="visual", diagram=dg)


@fam("012")
def fig_frac_tape(r, L):             # fraction add s6 (+#17 cp2)
    a, b = _fr(r, (2, 4, 8)), _fr(r, (2, 4, 8)); need(a + b < 1 and a.denominator != b.denominator)
    d = max(a.denominator, b.denominator)
    alt = f"Fraction bar in {d}ths: {frac(a)} shaded for Monday and {frac(b)} for Tuesday."
    dg = Diagram("fraction_bars", {"bars": [{"parts": d, "shaded": int(a * d), "label": frac(a)}, {"parts": d, "shaded": int(b * d), "label": frac(b)}]}, alt)
    return Item(f"Ty read {frac(a)} of a book on Monday and {frac(b)} on Tuesday. The bars show each day. What fraction of the book has Ty read?", frac(a + b),
                [f"Use {d}ths: {frac(a)} = {int(a * d)}/{d}, {frac(b)} = {int(b * d)}/{d}.", f"Sum: {frac(a + b)}."],
                [W(f"{a.numerator + b.numerator}/{a.denominator + b.denominator}", "added numerators and denominators"), W(frac(abs(a - b)) if a != b else "1/2", "subtracted"), W(frac(1 - a - b), "found the part left")],
                EX(f"{frac(a)}+{frac(b)}", form="frac"), qtype="visual", tags={"realworld"}, diagram=dg)


@fam("012")
def fig_scaling(r, L):               # fraction mult s5
    n = r.randint(6, 12); f = pick(r, [F(1, 2), F(2, 3), F(3, 4), F(3, 2), F(4, 3)])
    need((n * f).denominator == 1)
    hi = int(max(n, n * f)) + 2
    alt = f"Number line from 0 to {hi} with two jumps from 0: one to {n}, and one to {mixed(f)} × {n}, which is marked with a question mark."
    dg = Diagram("number_line", {"lo": "0", "hi": str(hi), "den": 1, "label_every": 1, "jumps": [["0", str(n)], ["0", str(n * f)]]}, alt)
    return Item(f"The number line shows a jump to {n}, and a second jump that is {mixed(f)} times as long. Where does the second jump end? ({mixed(f)} × {n})", str(n * f),
                [f"{mixed(f)} is {'less' if f < 1 else 'more'} than 1, so the product is {'less' if f < 1 else 'more'} than {n}.", f"{mixed(f)} × {n} = {n * f}."],
                [W(str(n + f) if (n + f).denominator == 1 else mixed(n + f), "added"), W(str(n), "said it does not change"), W(mixed(n / f), "divided")],
                EX(f"{xm(f)}*{n}"), qtype="visual", diagram=dg)


@fam("012")
def fig_fm_word(r, L):               # fraction mult s7 (also fm s3 cp2 thin)
    n = r.randint(2, 6); a = _fr(r, (2, 3, 4)); need((n * a).denominator <= 4)
    alt = f"Tape diagram: {n} equal parts, each {frac(a)} pound."
    dg = Diagram("tape", {"parts": n, "shaded": n, "each": frac(a), "total_label": "?", "note": ""}, alt)
    return Item(f"Each of {n} bags holds {frac(a)} pound of seed. The tape shows the bags. How many pounds of seed are there in all?", f"{mixed(n * a)} pound{'s' if n * a > 1 else ''}",
                [f"{n} × {frac(a)} = {frac(n * a)}.", f"= {mixed(n * a)} pound{'s' if n * a > 1 else ''}."],
                [W(f"{mixed(n + a)} pounds", "added"), W(f"{frac(a)} pound", "gave one bag"), W(f"{mixed(F(n, a.denominator))} pound{'s' if F(n, a.denominator) > 1 else ''}", "multiplied by the denominator only")],
                EX(f"{n}*{frac(a)}", unit="pounds" if n * a > 1 else "pound", form="mixed"), qtype="visual", tags={"realworld"}, diagram=dg)


@fam("012")
def fig_frac_area(r, L):             # fraction mult s3 (#17 cp2)
    a, b = pick(r, [F(1, 2), F(1, 3), F(2, 3), F(3, 4), F(1, 4)]), pick(r, [F(1, 2), F(2, 5), F(3, 5), F(1, 3), F(3, 4)])
    alt = f"Unit square split into {a.denominator} by {b.denominator} parts; {a.numerator} by {b.numerator} are shaded."
    dg = Diagram("area_grid", {"rows": a.denominator, "cols": b.denominator, "sh_rows": a.numerator, "sh_cols": b.numerator, "mode": "overlap"}, alt)
    return Item(f"The unit square is shaded to show {frac(a)} × {frac(b)}. What is the product?", frac(a * b),
                [f"The square has {a.denominator * b.denominator} equal parts; {a.numerator * b.numerator} are shaded twice.", f"{frac(a)} × {frac(b)} = {a.numerator * b.numerator}/{a.denominator * b.denominator} = {frac(a * b)}."],
                [W(frac(a + b) if a + b < 2 else mixed(a + b), "added"), W(f"{a.numerator + b.numerator}/{a.denominator * b.denominator}", "added the numerators"), W(frac(a / b) if a != b else "1", "divided")],
                EX(f"{frac(a)}*{frac(b)}", form="frac"), qtype="visual", diagram=dg)


@fam("012")
def fig_weight_table(r, L):          # measurement s2
    lb = r.randint(4, 12)
    rows = [[str(i), str(16 * i)] for i in range(1, 4)] + [[str(lb), "?"]]
    dg = Diagram("table", {"header": ["Pounds", "Ounces"], "rows": rows}, f"Table: 1 pound = 16 ounces, 2 pounds = 32 ounces, 3 pounds = 48 ounces, {lb} pounds = ?")
    it = Item(f"Use the table. How many ounces are in {lb} pounds?", f"{16 * lb} ounces", ["Each pound is 16 ounces.", f"{lb} × 16 = {16 * lb} ounces."],
              [W(f"{lb + 16} ounces", "added"), W(f"{12 * lb} ounces", "used 12, as for feet"), W(f"{lb} ounces", "did not convert")],
              EX(f"{lb}*16", unit="ounces"), qtype="visual", diagram=dg)
    return it


@fam("012")
def fig_metric_line(r, L):           # measurement s3 (#17 cp2)
    m = F(r.randint(11, 49), 10)
    dg = Diagram("number_line", {"lo": "0", "hi": "5", "den": 10, "label_every": 10, "jumps": [["0", frac(m)]]}, f"Number line in meters from 0 to 5 in tenths, with a jump to {dec(m)}.")
    return Item(f"The number line shows a jump of {dec(m)} meters. How many centimeters is that?", f"{dec(m * 100)} centimeters",
                ["1 meter = 100 centimeters.", f"{dec(m)} × 100 = {dec(m * 100)} centimeters."],
                [W(f"{dec(m * 10)} centimeters", "multiplied by 10"), W(f"{dec(m * 1000)} centimeters", "multiplied by 1,000"), W(f"{dec(m / 100)} centimeters", "divided")],
                EX(f"{dec(m)}*100", unit="centimeters"), qtype="visual", diagram=dg)


@fam("012")
def fig_vol_word(r, L):              # volume s5 (+ volume s4 cp2 thin)
    l, w, h = r.randint(3, 9), r.randint(2, 6), r.randint(2, 6)
    dg = Diagram("prism", {"l": l, "w": w, "h": h, "lt": f"{l} ft", "wt": f"{w} ft", "ht": f"{h} ft"}, f"Rectangular prism {l} feet long, {w} feet wide and {h} feet tall.")
    return Item(f"A garden box is shown. How many cubic feet of soil fill it?", f"{l * w * h} cubic feet",
                [f"V = l × w × h.", f"{l} × {w} × {h} = {l * w * h} cubic feet."],
                [W(f"{l + w + h} cubic feet", "added"), W(f"{l * w} cubic feet", "found the base only"), W(f"{2 * (l * w + l * h + w * h)} cubic feet", "found the surface area")],
                EX(f"{l}*{w}*{h}", unit="cubic feet"), qtype="visual", tags={"realworld"}, diagram=dg)


@fam("012")
def fig_comp_two(r, L):              # volume s4 cp2
    a = [r.randint(2, 5) for _ in range(3)]; b = [r.randint(2, 5) for _ in range(3)]
    b[1] = a[1]
    lab = lambda x: {"l": x[0], "w": x[1], "h": x[2], "lt": f"{x[0]} units", "wt": f"{x[1]} units", "ht": f"{x[2]} units"}
    dg = Diagram("composite", {"a": lab(a), "b": lab(b)}, f"Two rectangular prisms side by side with the same depth: {a[0]} by {a[1]} by {a[2]} units and {b[0]} by {b[1]} by {b[2]} units.")
    return Item(f"The figure is made of two rectangular prisms, {a[0]} × {a[1]} × {a[2]} and {b[0]} × {b[1]} × {b[2]} units. What is its volume?", f"{a[0] * a[1] * a[2] + b[0] * b[1] * b[2]} cubic units",
                [f"First: {a[0] * a[1] * a[2]}; second: {b[0] * b[1] * b[2]}.", f"Total: {a[0] * a[1] * a[2] + b[0] * b[1] * b[2]} cubic units."],
                [W(f"{a[0] * a[1] * a[2]} cubic units", "found one prism"), W(f"{(a[0] + b[0]) * (a[1] + b[1]) * (a[2] + b[2])} cubic units", "added edges first"), W(f"{sum(a) + sum(b)} cubic units", "added the edges")],
                EX(f"{a[0]}*{a[1]}*{a[2]}+{b[0]}*{b[1]}*{b[2]}", unit="cubic units"), qtype="visual", diagram=dg)


@fam("012", mode="mc")
def fig_axes(r, L):                  # coordinate s1
    x, y = r.randint(1, 8), r.randint(1, 8)
    dg = Diagram("coord", {"xmax": 10, "ymax": 10, "points": [{"x": x, "y": y, "label": "P"}]}, f"Coordinate grid from 0 to 10 with point P at ({x}, {y}).")
    return mc_key("On the grid, what does the first number of the ordered pair tell you about point P?", f"How far P is to the right of the origin, along the x-axis ({x}).",
                  [f"How far P is above the origin ({x}).", "Which quadrant P is in.", f"The distance from P to the origin ({x + y})."],
                  ["The first coordinate is the x-coordinate: distance along the x-axis.", f"P is at ({x}, {y})."], qtype="visual", diagram=dg, r=r)


@fam("012")
def fig_plot_read(r, L):             # coordinate s2 cp2 thin
    pts = {k: (r.randint(1, 9), r.randint(1, 9)) for k in "ABC"}
    need(len(set(pts.values())) == 3)
    k = pick(r, "ABC"); x, y = pts[k]
    dg = Diagram("coord", {"xmax": 10, "ymax": 10, "points": [{"x": v[0], "y": v[1], "label": n} for n, v in pts.items()]}, "Coordinate grid with points " + ", ".join(f"{n} at ({v[0]}, {v[1]})" for n, v in pts.items()) + ".")
    return Item(f"What is the sum of the coordinates of point {k}?", str(x + y), [f"{k} is at ({x}, {y}).", f"{x} + {y} = {x + y}."],
                [W(str(x * y), "multiplied"), W(str(abs(x - y)), "subtracted"), W(str(x), "used only x")],
                EX(f"{x}+{y}"), qtype="visual", diagram=dg)


@fam("012")
def fig_pattern_table(r, L):         # coordinate s4 cp1/honors thin
    a, k = r.randint(1, 4), r.randint(2, 4)
    rows = [[str(a * i), str(a * k * i)] for i in range(1, 4)] + [[str(a * 5), "?"]]
    dg = Diagram("table", {"header": ["x (add " + str(a) + ")", "y (add " + str(a * k) + ")"], "rows": rows}, "Table of two patterns: " + "; ".join(f"x {r_[0]}, y {r_[1]}" for r_ in rows) + ".")
    return Item(f"The table shows ordered pairs from two patterns. What is y when x is {a * 5}?", str(a * k * 5),
                [f"Each y is {k} times its x.", f"{k} × {a * 5} = {a * k * 5}."],
                [W(str(a * 5 + a * k), "added the rules"), W(str(a * k * 4), "used the 4th pair"), W(str(a * 5 * (k + 1)), "multiplied by the wrong number")],
                EX(f"{a * k}/{a}*{a * 5}"), qtype="visual", diagram=dg)


@fam("012", mode="mc")
def fig_quad_props(r, L):            # shapes s3 thin
    which = r.randint(0, 3)
    shapes = [("square", [[0, 0], [4, 0], [4, 4], [0, 4]], "4 equal sides and 4 right angles"),
              ("rectangle", [[0, 0], [6, 0], [6, 3], [0, 3]], "2 pairs of parallel sides and 4 right angles, but not all sides equal"),
              ("rhombus", [[0, 0], [4, 0], [6, 3], [2, 3]], "4 equal sides but no right angles"),
              ("trapezoid", [[0, 0], [7, 0], [5, 3], [2, 3]], "exactly 1 pair of parallel sides")]
    good, pts, why = shapes[which]
    pts = [[x, y] for x, y in pts]
    dg = Diagram("shape", {"pts": pts}, f"A quadrilateral with {why}.")
    bad = [s for s, _, _ in shapes if s != good][:3]
    return mc_key(f"The quadrilateral has {why}. What is the most specific name for it?", good, bad,
                  [f"It has {why}.", f"So it is a {good}."], qtype="visual", diagram=dg, r=r)


@fam("012", mode="mc")
def fig_hierarchy(r, L):             # shapes s4
    rows = [["quadrilateral", "4 sides"], ["trapezoid", "1+ parallel pair"], ["parallelogram", "2 parallel pairs"],
            ["rectangle", "+ 4 right angles"], ["rhombus", "+ 4 equal sides"], ["square", "both of those"]]
    dg = Diagram("table", {"header": ["Shape", "Has"], "rows": rows}, "Hierarchy of quadrilaterals, from most general to most specific: quadrilateral, trapezoid, parallelogram, rectangle and rhombus, square.")
    q = r.randint(0, 2)
    if q == 0:
        return mc_key("Use the hierarchy. Which statement is always true?", "Every square is a rhombus.", ["Every rhombus is a square.", "Every rectangle is a square.", "Every trapezoid is a parallelogram."],
                      ["A square has 4 equal sides, so it fits the definition of a rhombus.", "A rhombus need not have right angles."], qtype="visual", diagram=dg, r=r)
    if q == 1:
        return mc_key("Use the hierarchy. Which shape is both a rectangle and a rhombus?", "square", ["parallelogram", "trapezoid", "quadrilateral"],
                      ["A square has 4 right angles and 4 equal sides.", "So it is both."], qtype="visual", diagram=dg, r=r)
    return mc_key("Use the hierarchy. Which statement is always true?", "Every rectangle is a parallelogram.", ["Every parallelogram is a rectangle.", "Every quadrilateral is a trapezoid.", "Every rhombus is a rectangle."],
                  ["A rectangle has 2 pairs of parallel sides.", "Not every parallelogram has right angles."], qtype="visual", diagram=dg, r=r)


@fam("012")
def fig_data_multi(r, L):            # data s4
    return lp_fair_share(r, L)


# ================================================================================================ registry
UNIT = {"place-value-number-sense": "pv", "multi-digit-multiplication-division": "md", "decimal-operations": "do", "numerical-expressions-patterns": "ne",
        "fraction-addition-subtraction": "fa", "fraction-multiplication-division": "fm", "measurement-conversions": "mc", "volume-three-dimensional-figures": "vo",
        "coordinate-plane-graphing": "cp", "classifying-two-dimensional-figures": "cs", "data-line-plots-problem-solving": "dd"}
CR = {"pv": (cr_pv, 1), "md": (cr_md, 5), "do": (cr_do, 6), "ne": (cr_ne, 4), "fa": (cr_fa, 6), "fm": (cr_fm, 4), "mc": (cr_mc, 4), "vo": (cr_vo, 5),
      "cp": (cr_cp, 3), "cs": (cr_cs, 3), "dd": (cr_dd, 4)}
# skill -> families with one item at every level they list (#12, #13, #14, #17)
FIG = {("pv", 2): [pt_shift, pt_shift], ("md", 2): [fig_estimate_area], ("md", 5): [fig_remainder_tape], ("do", 6): [fig_money_tape],
       ("ne", 1): [fig_order_ops], ("ne", 2): [fig_write_expr], ("ne", 3): [fig_interpret], ("fa", 4): [fig_mixed_line], ("fa", 6): [fig_frac_tape],
       ("fm", 3): [fig_frac_area], ("fm", 5): [fig_scaling], ("fm", 7): [fig_fm_word], ("mc", 2): [fig_weight_table], ("mc", 3): [fig_metric_line],
       ("vo", 4): [fig_comp_two], ("vo", 5): [fig_vol_word], ("cp", 1): [fig_axes], ("cp", 2): [fig_plot_read], ("cp", 4): [fig_pattern_table],
       ("cs", 3): [fig_quad_props], ("cs", 4): [fig_hierarchy], ("dd", 3): [lp_fair_share, lp_fair_share], ("dd", 4): [fig_data_multi]}


def added(unit_id, skill, L):
    u = UNIT[unit_id]
    out = []
    for f in FIG.get((u, skill), []):
        if L in f.levels:
            out.append((f, 1))
    cf, cs = CR[u]
    if skill == cs and L in cf.levels:
        out.append((cf, 1))
    if L == 2:
        out.append((globals()[f"ms_{u}{skill}"], 2))
    # merge repeats of one family into one entry with a count
    merged = {}
    for f, n in out:
        merged[f] = merged.get(f, 0) + n
    return list(merged.items())
