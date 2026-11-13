"""Unit 5: Factors, Multiples, and Number Patterns (4.OA.B.4, 4.OA.C.5)."""
from g4lib import *

UNIT_ID = "factors-multiples-patterns"
PRIMES = [p for p in range(2, 100) if all(p % k for k in range(2, int(p ** 0.5) + 1))]
SHAPES = ["circle", "square", "triangle", "star", "hexagon", "diamond"]


def factors(n):
    return [k for k in range(1, n + 1) if n % k == 0]


def pick_n(r, L, minf=4):
    pool = {0: range(8, 37), 1: range(12, 73), 2: range(30, 101)}[L]
    c = [n for n in pool if len(factors(n)) >= minf]
    return pick(r, c)


def lst(xs):
    return ", ".join(str(x) for x in xs)


# ============================================================== S1 Factors and Factor Pairs
@fam("012", mode="mc")
def fa_list(r, L):
    n = pick_n(r, L)
    fs = factors(n)
    nonf = [k for k in range(2, n) if n % k]
    b1 = fs[1:-1]
    b2 = sorted(fs + [pick(r, nonf)])
    b3 = [x for x in fs if x != fs[len(fs) // 2]]
    return Item(f"Which list shows all the factors of {n}?", lst(fs), ["Find every pair of whole numbers with a product of " + str(n) + ".", "Factor pairs: " + "; ".join(f"{a} × {n // a}" for a in fs if a * a <= n) + ".", f"The factors are {lst(fs)}."],
                [W(lst(b1), "left out 1 and the number itself"), W(lst(b2), "included a number that is not a factor"), W(lst(b3), "missed a factor")],
                FN("factor_list", n=n), qtype="conceptual")


@fam("012")
def fa_count(r, L):
    n = pick_n(r, L, 3)
    fs = factors(n)
    return Item(f"How many factors does {n} have?", str(len(fs)), [f"List the factor pairs of {n}: " + "; ".join(f"{a} × {n // a}" for a in fs if a * a <= n) + ".", f"The factors are {lst(fs)}. That is {len(fs)} factors."],
                [W(str(len(fs) - 2), "left out 1 and the number itself"), W(str(len(fs) + 1), "counted a number twice or included a number that is not a factor"), W(str(len(fs) - 1), "missed a factor"), W(str(len([a for a in fs if a * a <= n])), "counted the factor pairs instead of the factors") if len([a for a in fs if a * a <= n]) not in (len(fs) - 1, len(fs) - 2) else W(str(n), "gave the number")],
                FN("factor_count", n=n), claim=f"Number of factors of {n}")


@fam("012")
def fa_pair_missing(r, L):
    n = pick_n(r, L)
    fs = [a for a in factors(n) if a * a <= n]
    a = pick(r, fs[1:] if len(fs) > 1 else fs)
    pairs = "; ".join(f"{x} and {'___' if x == a else n // x}" for x in fs)
    return Item(f"The factor pairs of {n} are listed. Fill in the blank: {pairs}", str(n // a), [f"The two numbers in each pair multiply to {n}.", f"{a} × {n // a} = {n}."],
                [W(str(n - a), "subtracted instead of dividing"), W(str(n // a + 1), "made a division fact mistake"), W(str(n * a), "multiplied instead of dividing"), W(str(a), "repeated the first factor") if a * a != n else W(str(a + 1), "made a fact mistake")],
                EX(f"{n} ÷ {a}"), qtype="fill-blank")


@fam("012", mode="mc")
def fa_is_factor(r, L):
    n = pick_n(r, L)
    fs = [x for x in factors(n) if 1 < x < n]
    nonf = [k for k in range(2, min(n, 20)) if n % k]
    need(len(nonf) >= 3)
    not_ = r.random() < 0.4 and len(fs) >= 3
    if not_:
        good, bad = pick(r, nonf), r.sample(fs, 3)
        return Item(f"Which number is NOT a factor of {n}?", str(good), [f"A factor divides {n} with no remainder.", f"{n} ÷ {good} = {n // good} R {n % good}, so {good} is not a factor."],
                    [W(str(x), f"{x} × {n // x} = {n}, so it is a factor") for x in bad], FN("not_factor", n=n), qtype="conceptual")
    good, bad = pick(r, fs), r.sample(nonf, 3)
    return Item(f"Which number is a factor of {n}?", str(good), [f"A factor divides {n} with no remainder.", f"{good} × {n // good} = {n}, so {good} is a factor."],
                [W(str(x), f"{n} ÷ {x} has a remainder") for x in bad], FN("is_factor", n=n), qtype="conceptual")


@fam("012")
def fa_array(r, L):
    R, C = r.randint(2, 6), r.randint(3, 12)
    need(R != C)
    n = R * C
    alt = f"An array of dots with {R} rows and {C} dots in each row."
    return Item(f"The array shows {n} dots in {R} equal rows. This shows that {R} and what other number are a factor pair of {n}?", str(C), [f"The array has {R} rows of {C}.", f"{R} × {C} = {n}, so {R} and {C} are a factor pair."],
                [W(str(n), "gave the total"), W(str(R), "repeated the number of rows"), W(str(C + 1), "miscounted the columns"), W(str(n - R), "subtracted instead of dividing")],
                FN("array_div", rows=R, cols=C), qtype="visual", diagram=Diagram("array", {"rows": R, "cols": C}, alt), tags={"modeling"})


@fam("12", mode="mc")
def fa_common(r, L):
    for _ in range(40):
        a, b = pick_n(r, L), pick_n(r, L)
        cf = [x for x in factors(a) if b % x == 0 and x > 1]
        only = [x for x in factors(a) + factors(b) if (a % x == 0) != (b % x == 0) and x > 1]
        neither = [x for x in range(2, 20) if a % x and b % x]
        if a != b and cf and len(only) >= 2 and neither:
            break
    else:
        raise Reject()
    good = pick(r, cf)
    bad = r.sample(only, 2) + [pick(r, neither)]
    return Item(f"Which number is a factor of both {a} and {b}?", str(good), [f"{good} divides {a} ({good} × {a // good}) and {b} ({good} × {b // good}).", f"So {good} is a factor of both."],
                [W(str(x), "it is not a factor of both numbers") for x in bad], FN("common_factor", a=a, b=b), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def fa_rows(r, L):
    n = pick_n(r, L)
    fs = [x for x in factors(n) if 1 < x < n]
    nonf = [k for k in range(2, min(n, 16)) if n % k]
    need(len(fs) >= 3 and nonf)
    thing = pick(r, ["chairs", "desks", "plants", "photos", "tiles"])
    good = pick(r, nonf)
    return Item(f"{name(r)} wants to arrange {n} {thing} in equal rows with none left over. Which number of rows will NOT work?", f"{good} rows",
                [f"The number of rows must be a factor of {n}.", f"{n} ÷ {good} leaves a remainder of {n % good}, so {good} rows will not work."],
                [W(f"{x} rows", f"{x} × {n // x} = {n}, so this works") for x in r.sample(fs, 3)], FN("not_factor", n=n), qtype="real-world", tags={"modeling"})


# ============================================================== S2 Multiples
@fam("012")
def mu_list(r, L):
    k = r.randint(2, 9) if L < 2 else r.randint(6, 12)
    c = 5 if L < 2 else 6
    seq = [k * i for i in range(1, c + 1)]
    return Item(f"List the first {words(c)} multiples of {k}, starting with {k}. Separate the numbers with commas.", lst(seq), [f"Skip count by {k}, or multiply {k} by 1, 2, 3, and so on.", f"{lst(seq)}."],
                [W(lst([k * i for i in range(2, c + 2)]), "skipped the first multiple"), W(lst([x for x in factors(k * 12)][:c]), "listed factors instead of multiples"), W(lst(seq[:-1] + [seq[-1] + 1]), "made a counting mistake")],
                FN("pattern_list", start=str(k), op="add", step=str(k), count=c), claim=f"First {words(c)} multiples of {k}")


@fam("012", mode="mc")
def mu_is_multiple(r, L):
    k = r.randint(3, 9)
    hi = {0: 60, 1: 100, 2: 100}[L]
    good = k * r.randint(4 if L else 2, hi // k)
    bad = []
    for _ in range(30):
        x = good + r.randint(-12, 12)
        if x > k and x % k and x not in bad:
            bad.append(x)
    need(len(bad) >= 3)
    if r.random() < 0.35:
        g2 = bad[0]
        b2 = [k * m for m in r.sample(range(2, hi // k + 1), 3)]
        return Item(f"Which number is NOT a multiple of {k}?", str(g2), [f"A multiple of {k} can be divided by {k} with no remainder.", f"{g2} ÷ {k} = {g2 // k} R {g2 % k}, so {g2} is not a multiple of {k}."],
                    [W(str(x), f"{k} × {x // k} = {x}") for x in b2], FN("not_multiple", m=k), qtype="conceptual")
    return Item(f"Which number is a multiple of {k}?", str(good), [f"A multiple of {k} is the product of {k} and a whole number.", f"{k} × {good // k} = {good}."],
                [W(str(x), f"{x} ÷ {k} has a remainder") for x in bad[:3]], FN("is_multiple", m=k), qtype="conceptual")


@fam("012")
def mu_nth(r, L):
    k = r.randint(3, 9) if L < 2 else r.randint(6, 12)
    n = r.randint(4, 9) if L == 0 else r.randint(7, 12)
    it = Item(f"What is the {ordinal(n)} multiple of {k}? (The first multiple of {k} is {k}.)", str(k * n), [f"The {ordinal(n)} multiple of {k} is {n} × {k}.", f"{n} × {k} = {k * n}."],
                [W(str(k * (n + 1)), "counted one multiple too many"), W(str(k * (n - 1)), "started counting at 0"), W(str(k + n), "added instead of multiplying"), W(str(k * n + 1), "made a fact mistake")],
                EX(f"{n} × {k}"), claim=f"The {ordinal(n)} multiple of {k}")
    it.consts = [n]
    return it


@fam("12", mode="mc")
def mu_common(r, L):
    a, b = r.sample([2, 3, 4, 5, 6, 8, 9, 10], 2)
    cm = [x for x in range(max(a, b), 101) if x % a == 0 and x % b == 0]
    onlya = [x for x in range(a, 101, a) if x % b]
    onlyb = [x for x in range(b, 101, b) if x % a]
    neither = [x for x in range(11, 90) if x % a and x % b]
    need(cm and onlya and onlyb and neither)
    good = pick(r, cm[:3])
    return Item(f"Which number is a multiple of both {a} and {b}?", str(good), [f"{good} = {a} × {good // a} and {good} = {b} × {good // b}.", f"So {good} is a multiple of both."],
                [W(str(pick(r, onlya)), f"it is a multiple of {a} only"), W(str(pick(r, onlyb)), f"it is a multiple of {b} only"), W(str(pick(r, neither)), "it is not a multiple of either number")],
                FN("common_multiple", a=a, b=b), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def mu_factor_link(r, L):
    k = r.randint(3, 9)
    m = r.randint(3, 12)
    need(m != k)
    n = k * m
    good = f"{k} is a factor of {n}"
    return Item(f"{n} is a multiple of {k}. Which statement must also be true?", good, [f"{n} = {k} × {m}.", f"Because {n} is a multiple of {k}, {k} is a factor of {n}."],
                [W(f"{n} is a factor of {k}", "switched factor and multiple"), W(f"{k} is a multiple of {n}", "switched factor and multiple"), W(f"{k + 1} is a factor of {n}" if n % (k + 1) else f"{n + 1} is a multiple of {k}", "this statement is not true")],
                FN("fm_statement"), qtype="conceptual", tags={"reasoning", "connections"})


@fam("012")
def mu_count_between(r, L):
    k = r.randint(3, 9)
    lo = r.randint(5, 30)
    hi = lo + r.randint(15, 30 if L == 0 else 50)
    need(lo % k and hi % k and hi <= 100)
    ms = [x for x in range(lo, hi + 1) if x % k == 0]
    need(2 <= len(ms) <= 9)
    return Item(f"How many multiples of {k} are between {lo} and {hi}?", str(len(ms)), [f"List the multiples of {k} between {lo} and {hi}: {lst(ms)}.", f"There are {len(ms)}."],
                [W(str(len(ms) + 1), "counted a number outside the range"), W(str(len(ms) - 1), "missed a multiple"), W(str(ms[0]), "gave the first multiple instead of counting"), W(str((hi - lo) // k + 2), "estimated instead of listing")],
                FN("count_multiples", m=k, lo=lo, hi=hi), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def mu_packs(r, L):
    k = r.randint(4, 12)
    thing = pick(r, ["hot dog buns", "juice boxes", "markers", "tennis balls", "stickers", "pencils"])
    good = k * r.randint(3, 100 // k)
    bad = []
    for _ in range(40):
        x = good + r.randint(-15, 15)
        if x > k and x % k and x not in bad:
            bad.append(x)
    need(len(bad) >= 3)
    return Item(f"A store sells {thing} only in packs of {k}. Which total number of {thing} could {name(r)} buy?", str(good), [f"The total must be a multiple of {k}.", f"{k} × {good // k} = {good}, so {good} works ({good // k} packs)."],
                [W(str(x), f"{x} is not a multiple of {k}") for x in bad[:3]], FN("is_multiple", m=k), qtype="real-world", tags={"modeling"})


# ============================================================== S3 Prime and Composite Numbers
def pc_range(L):
    return {0: (2, 30), 1: (10, 60), 2: (30, 100)}[L]


def comp(r, L, odd=False):
    lo, hi = pc_range(L)
    c = [n for n in range(max(lo, 4), hi + 1) if n not in PRIMES and (not odd or n % 2)]
    return pick(r, c)


def prime(r, L):
    lo, hi = pc_range(L)
    return pick(r, [p for p in PRIMES if lo <= p <= hi])


@fam("012", mode="mc")
def pc_classify(r, L):
    isp = r.random() < 0.5
    n = prime(r, L) if isp else comp(r, L, odd=r.random() < 0.6)
    if isp:
        need(n > 2)
        good = f"Prime, because its only factors are 1 and {n}"
        bad = [f"Composite, because {n} is an odd number" if n % 2 else f"Composite, because {n} is an even number", f"Composite, because it has the factors 1 and {n}", f"Prime, because {n} is an odd number" if n % 2 else "Prime, because all even numbers are prime"]
        steps = [f"Look for a factor pair of {n} other than 1 × {n}. There is no other pair.", f"{n} has exactly two factors, 1 and {n}, so it is prime."]
    else:
        a = min(k for k in range(2, n) if n % k == 0)
        good = f"Composite, because {a} × {n // a} = {n}"
        bad = [f"Prime, because its only factors are 1 and {n}", f"Prime, because {n} is an odd number" if n % 2 else "Prime, because 2 is prime", f"Composite, because {n} is an odd number" if n % 2 else f"Composite, because {n + 1} is prime"]
        steps = [f"{a} × {n // a} = {n}.", f"{n} has more than two factors, so it is composite."]
    return Item(f"Is {n} prime or composite? Choose the answer with the correct reason.", good, steps, [W(b, "the reason is not correct") for b in bad], FN("prime_reason", n=n), qtype="explain", tags={"reasoning"})


@fam("012", mode="mc")
def pc_which_prime(r, L):
    good = prime(r, L)
    bad = set()
    while len(bad) < 3:
        bad.add(comp(r, L, odd=r.random() < 0.7))
    return Item("Which number is prime?", str(good), ["A prime number has exactly two factors: 1 and itself.", f"{good} has only the factors 1 and {good}."],
                [W(str(x), f"{min(k for k in range(2, x) if x % k == 0)} × {x // min(k for k in range(2, x) if x % k == 0)} = {x}") for x in sorted(bad)], FN("is_prime_opt"), qtype="conceptual")


@fam("012", mode="mc")
def pc_which_composite(r, L):
    good = comp(r, L, odd=True)
    lo, hi = pc_range(L)
    ps = [p for p in PRIMES if lo <= p <= hi and p != 2]
    bad = r.sample(ps, 3)
    a = min(k for k in range(2, good) if good % k == 0)
    return Item("Which number is composite?", str(good), ["A composite number has more than two factors.", f"{a} × {good // a} = {good}, so {good} is composite."],
                [W(str(x), f"{x} is prime") for x in bad], FN("is_composite_opt"), qtype="conceptual")


@fam("012")
def pc_count(r, L):
    lo = r.randint(*{0: (1, 10), 1: (10, 40), 2: (40, 80)}[L])
    hi = lo + r.randint(10, 20)
    ps = [p for p in PRIMES if lo < p < hi]
    need(2 <= len(ps) <= 6 and lo not in PRIMES and hi not in PRIMES)
    return Item(f"How many prime numbers are between {lo} and {hi}?", str(len(ps)), [f"Check each number between {lo} and {hi} for factors other than 1 and itself.", f"The primes are {lst(ps)}. There are {len(ps)}."],
                [W(str(len(ps) + 1), "counted a composite number as prime"), W(str(len(ps) - 1), "missed a prime number"), W(str(len([x for x in range(lo + 1, hi) if x % 2])), "counted all the odd numbers") if len([x for x in range(lo + 1, hi) if x % 2]) not in (len(ps) + 1, len(ps) - 1, len(ps)) else W(str(len(ps) + 2), "counted composite numbers as prime")],
                FN("count_primes", lo=lo, hi=hi), qtype="conceptual", claim=f"Number of primes between {lo} and {hi}")


@fam("012", mode="mc")
def pc_list(r, L):
    lo = r.randint(*{0: (1, 10), 1: (10, 40), 2: (40, 75)}[L])
    hi = lo + r.randint(12, 22)
    ps = [p for p in PRIMES if lo < p < hi]
    need(3 <= len(ps) <= 6 and lo not in PRIMES and hi not in PRIMES)
    oddc = [x for x in range(lo + 1, hi) if x % 2 and x not in PRIMES and x > 1]
    need(oddc)
    b1 = sorted(ps + [pick(r, oddc)])
    b2 = ps[:-1] if r.random() < 0.5 else ps[1:]
    b3 = [x for x in range(lo + 1, hi) if x % 2]
    need(b3 != ps and b3 != b1)
    return Item(f"Which list shows all the prime numbers between {lo} and {hi}?", lst(ps), ["Cross out every number that has a factor other than 1 and itself.", f"The primes are {lst(ps)}."],
                [W(lst(b1), "included a composite number"), W(lst(b2), "missed a prime number"), W(lst(b3), "listed all the odd numbers")], FN("prime_list", lo=lo, hi=hi), qtype="conceptual")


@fam("12", mode="mc")
def pc_counterexample(r, L):
    good = comp(r, L, odd=True)
    lo, hi = pc_range(L)
    ps = r.sample([p for p in PRIMES if lo <= p <= hi and p > 2], 2)
    ev = pick(r, [x for x in range(max(lo, 4), hi, 2)])
    a = min(k for k in range(2, good) if good % k == 0)
    return Item(f"{name(r)} says, “All odd numbers are prime.” Which number shows that this statement is false?", str(good),
                ["Look for an odd number that is composite.", f"{good} is odd, and {a} × {good // a} = {good}, so it is not prime."],
                [W(str(ps[0]), "this odd number is prime, so it agrees with the statement"), W(str(ps[1]), "this odd number is prime, so it agrees with the statement"), W(str(ev), "this number is even, so it does not test the statement")],
                FN("odd_composite"), qtype="explain", tags={"reasoning", "challenge"})


@fam("12")
def pc_sum(r, L):
    lo = r.randint(10, 40) if L == 1 else r.randint(40, 85)
    hi = lo + r.randint(6, 12)
    ps = [p for p in PRIMES if lo < p < hi]
    need(len(ps) == 2 and lo not in PRIMES and hi not in PRIMES)
    return Item(f"There are exactly two prime numbers between {lo} and {hi}. What is their sum?", str(sum(ps)), [f"The primes between {lo} and {hi} are {ps[0]} and {ps[1]}.", f"{ps[0]} + {ps[1]} = {sum(ps)}."],
                [W(str(ps[1] - ps[0]), "subtracted instead of adding"), W(str(sum(ps) + 2), "used a composite number"), W(str(ps[0] * ps[1]), "multiplied instead of adding"), W(str(lo + hi), "added the endpoints")],
                FN("prime_sum", lo=lo, hi=hi), qtype="multi-step", tags={"multistep"})


# ============================================================== S4 Number Patterns and Rules
def add_rule(r, L):
    step = r.randint(2, 9) if L == 0 else r.randint(6, 25) if L == 1 else r.randint(12, 60)
    start = r.randint(1, 20) if L < 2 else r.randint(5, 80)
    sub_ = r.random() < 0.3
    if sub_:
        start = start + step * 8
        return start, -step
    return start, step


def seq_of(start, step, n):
    return [start + step * i for i in range(n)]


def rule_text(step):
    return f"add {step}" if step > 0 else f"subtract {-step}"


@fam("012")
def np_next(r, L):
    start, step = add_rule(r, L)
    s = seq_of(start, step, 5)
    return Item(f"The rule is “{rule_text(step)}.” What is the next number? {lst(s[:4])}, ___", str(s[4]), [f"Apply the rule to the last number: {s[3]} {'+' if step > 0 else '−'} {abs(step)}.", f"The next number is {s[4]}."],
                [W(str(s[3] - step), "applied the rule in the wrong direction"), W(str(s[4] + (1 if step > 0 else -1)), "made a computation mistake"), W(str(s[3] + 2 * step), "applied the rule twice"), W(str(s[3]), "repeated the last number")],
                FN("pattern_term", start=str(start), op="add", step=str(step), n=5), claim=f"Next number after {lst(s[:4])}")


@fam("012")
def np_generate(r, L):
    start, step = add_rule(r, L)
    s = seq_of(start, step, 5)
    return Item(f"Start at {start}. Use the rule “{rule_text(step)}.” Write the first five numbers in the pattern, separated by commas.", lst(s), ["The first number is the starting number. Apply the rule four times.", f"{lst(s)}."],
                [W(lst(seq_of(start + step, step, 5)), "left out the starting number"), W(lst(seq_of(start, -step, 5)) if start - 4 * abs(step) > 0 or step < 0 else lst(seq_of(start, step + 1, 5)), "used the wrong rule"), W(lst(s[:4] + [s[4] + 1]), "made a computation mistake")],
                FN("pattern_list", start=str(start), op="add", step=str(step), count=5), qtype="procedural")


@fam("012", mode="mc")
def np_rule(r, L):
    start, step = add_rule(r, L)
    s = seq_of(start, step, 4)
    good = rule_text(step)
    bad = [rule_text(-step), rule_text(step + (1 if step > 0 else -1)), f"multiply by {max(2, round(s[1] / s[0]))}" if s[0] else "multiply by 2"]
    need(not (s[0] and s[1] % s[0] == 0 and s[2] == s[1] * (s[1] // s[0])))
    return Item(f"What is the rule for this pattern? {lst(s)}, ...", good, [f"Compare neighbors: {s[1]} − {s[0]} = {s[1] - s[0]}, {s[2]} − {s[1]} = {s[2] - s[1]}.", f"Each number is {abs(step)} {'more' if step > 0 else 'less'} than the one before, so the rule is “{good}.”"],
                [W(bad[0], "went in the wrong direction"), W(bad[1], "found the wrong difference"), W(bad[2], "only checked the first two numbers")], FN("rule_of", seq=s), qtype="conceptual")


FEATURES = ["All the numbers are odd.", "All the numbers are even.", "The numbers alternate between odd and even.", "The numbers alternate between even and odd."]


def feature_of(start, step):
    if step % 2 == 0:
        return FEATURES[0] if start % 2 else FEATURES[1]
    return FEATURES[2] if start % 2 else FEATURES[3]


@fam("012", mode="mc")
def np_feature(r, L):
    step = r.randint(2, 9) if L < 2 else r.randint(11, 30)
    start = r.randint(1, 12)
    s = seq_of(start, step, 6)
    good = feature_of(start, step)
    return Item(f"A pattern starts at {start} and follows the rule “add {step}”: {lst(s)}, ... Which statement is true about the numbers in this pattern?", good,
                [f"{start} is {'odd' if start % 2 else 'even'}, and adding {'an even' if step % 2 == 0 else 'an odd'} number {'keeps a number odd or even' if step % 2 == 0 else 'switches between odd and even'}.", good],
                [W(f, "this does not describe the pattern") for f in FEATURES if f != good], FN("pattern_feature", start=start, step=step), qtype="explain", tags={"reasoning"})


@fam("12")
def np_nth(r, L):
    step = r.randint(3, 9) if L == 1 else r.randint(6, 15)
    start = r.randint(1, 12)
    n = r.randint(8, 12) if L == 1 else r.randint(15, 25)
    v = start + step * (n - 1)
    return Item(f"A pattern starts at {start} and follows the rule “add {step}.” What is the {ordinal(n)} number in the pattern?", str(v),
                [f"To reach the {ordinal(n)} number, the rule is used {n - 1} times.", f"{start} + {n - 1} × {step} = {v}."],
                [W(str(start + step * n), f"added {step} one time too many"), W(str(step * n), "left out the starting number"), W(str(start + step * (n - 2)), f"added {step} one time too few"), W(str(start + n), "added the position instead of using the rule")],
                FN("pattern_term", start=str(start), op="add", step=str(step), n=n), qtype="multi-step", tags={"reasoning", "challenge"})


@fam("012")
def np_missing(r, L):
    start, step = add_rule(r, L)
    s = seq_of(start, step, 5)
    i = r.randint(1, 3)
    shown = ", ".join("___" if j == i else str(x) for j, x in enumerate(s))
    return Item(f"The same amount is added or subtracted each time. Find the missing number: {shown}", str(s[i]), [f"The numbers change by {abs(step)} each time (they {'increase' if step > 0 else 'decrease'}).", f"The missing number is {s[i - 1]} {'+' if step > 0 else '−'} {abs(step)} = {s[i]}."],
                [W(str(s[i] + 1), "made a computation mistake"), W(str(s[i - 1] - step), "went in the wrong direction"), W(str((s[i - 1] + s[i + 1]) // 2 + step) , "used the wrong difference")],
                FN("pattern_term", start=str(start), op="add", step=str(step), n=i + 1), qtype="fill-blank")


@fam("012")
def np_multiply(r, L):
    k = pick(r, [2, 2, 3] if L == 0 else [2, 3, 4, 5] if L == 1 else [3, 4, 5, 10])
    start = r.randint(1, 5) if L < 2 else r.randint(2, 9)
    s = [start * k ** i for i in range(5)]
    need(s[4] <= 9999)
    return Item(f"The rule is “multiply by {k}.” What is the next number? {', '.join(comma(x) for x in s[:4])}, ___", comma(s[4]), [f"Multiply the last number by {k}: {comma(s[3])} × {k}.", f"The next number is {comma(s[4])}."],
                [W(comma(s[3] + k), "added instead of multiplying"), W(comma(s[3] + (s[3] - s[2])), "added the last difference instead of multiplying"), W(comma(s[4] * k), "multiplied twice"), W(comma(s[3] * (k + 1)), "used the wrong factor")],
                FN("pattern_term", start=str(start), op="mul", step=str(k), n=5), claim=f"Next number after {', '.join(comma(x) for x in s[:4])} (multiply by {k})")


@fam("012")
def np_table(r, L):
    k = r.randint(2, 9) if L < 2 else r.randint(6, 12)
    add = L == 0 and r.random() < 0.4
    ins = sorted(r.sample(range(2, 13), 4))
    outs = [x + k if add else x * k for x in ins]
    i = r.randrange(1, 4)
    rule = f"add {k}" if add else f"multiply by {k}"
    rows = [[str(a), "?" if j == i else str(b)] for j, (a, b) in enumerate(zip(ins, outs))]
    alt = "An input and output table. " + "; ".join(f"input {a}, output {b}" for a, b in rows) + "."
    return Item(f"The table follows the rule “{rule}.” What number replaces the question mark?", str(outs[i]), [f"Apply the rule to the input {ins[i]}.", f"{ins[i]} {'+' if add else '×'} {k} = {outs[i]}."],
                [W(str(ins[i] * k if add else ins[i] + k), "used the wrong operation"), W(str(outs[i - 1] + k) if outs[i - 1] + k != outs[i] else str(outs[i] + 1), "added to the output above instead of using the rule"), W(str(outs[i] + (1 if add else k)), "made a computation mistake")],
                EX(f"{ins[i]} {'+' if add else '×'} {k}"), qtype="visual", diagram=Diagram("table", {"header": ["Input", "Output"], "rows": rows}, alt), tags={"modeling"})


@fam("2")
def np_two_step(r, L):
    k, c = r.randint(2, 3), r.randint(1, 5)
    start = r.randint(1, 5)
    s = [start]
    for _ in range(4):
        s.append(s[-1] * k + c)
    return Item(f"The rule is “multiply by {k}, then add {c}.” What is the next number? {lst(s[:4])}, ___", str(s[4]), [f"{s[3]} × {k} = {s[3] * k}.", f"{s[3] * k} + {c} = {s[4]}."],
                [W(str(s[3] * k), f"forgot to add {c}"), W(str((s[3] + c) * k), "added before multiplying"), W(str(s[3] + (s[3] - s[2])), "added the last difference"), W(str(s[3] + k + c), "added instead of multiplying")],
                EX(f"{s[3]} × {k} + {c}"), qtype="multi-step", tags={"challenge", "multistep"})


# ============================================================== S5 Shape Patterns and Pattern Features
def unit_seq(r, L):
    n = 3 if L == 0 else r.randint(3, 4)
    u = r.sample(SHAPES, n if r.random() < 0.6 else n - 1)
    while len(u) < n:
        u.insert(r.randrange(len(u) + 1), pick(r, u))
    need(len(set(u)) >= 2 and u[0] != u[-1])
    return u


@fam("012", mode="mc")
def sp_next(r, L):
    u = unit_seq(r, L)
    k = len(u) * 2 + r.randint(0, len(u) - 1)
    seq = [u[i % len(u)] for i in range(k)]
    good = u[k % len(u)]
    others = [s for s in SHAPES if s != good]
    bad = [s for s in dict.fromkeys(u) if s != good] + [s for s in others if s not in u]
    alt = "A row of shapes: " + ", ".join(seq) + ", then a question mark."
    return Item("The shapes repeat in the same order. Which shape comes next?", good, [f"The part that repeats is: {', '.join(u)}.", f"After {seq[-1]} comes {good}."],
                [W(b, "did not follow the repeating part") for b in bad[:3]], FN("seq_at", unit=u, n=k + 1), qtype="visual", diagram=Diagram("shape_seq", {"seq": seq + ["?"]}, alt))


@fam("012", mode="mc")
def sp_nth(r, L):
    u = unit_seq(r, L)
    n = r.randint(10, 20) if L == 0 else r.randint(21, 40) if L == 1 else r.randint(41, 99)
    good = u[(n - 1) % len(u)]
    bad = [s for s in dict.fromkeys(u) if s != good] + [s for s in SHAPES if s not in u]
    rem = n % len(u)
    return Item(f"A pattern repeats these shapes in order: {', '.join(u)}. What is the {ordinal(n)} shape in the pattern?", good,
                [f"The pattern repeats every {len(u)} shapes. {n} ÷ {len(u)} = {n // len(u)} R {rem}.", f"A remainder of {rem} means the {ordinal(n)} shape matches shape number {rem if rem else len(u)} in the repeating part: {good}."],
                [W(b, "did not use the remainder to find the position") for b in bad[:3]], FN("seq_at", unit=u, n=n), qtype="conceptual", tags={"reasoning"})


@fam("012")
def sp_count(r, L):
    u = unit_seq(r, max(L, 1))
    n = len(u) * r.randint(2, 4) + r.randint(1, len(u) - 1)
    tgt = pick(r, sorted(set(u)))
    cnt = sum(1 for i in range(n) if u[i % len(u)] == tgt)
    per = u.count(tgt)
    return Item(f"A pattern repeats these shapes in order: {', '.join(u)}. In the first {n} shapes, how many are {tgt}s?", str(cnt),
                [f"Each group of {len(u)} shapes has {per} {tgt}{'s' if per != 1 else ''}. {n} shapes make {n // len(u)} full groups and {n % len(u)} extra shapes.", f"Count the {tgt}s: {cnt}."],
                [W(str(per * (n // len(u))) if per * (n // len(u)) != cnt else str(cnt + 1), "did not count the extra shapes"), W(str(cnt + 1) if per * (n // len(u)) != cnt else str(cnt + 2), "counted one too many"), W(str(n // len(u)) if n // len(u) not in (cnt, per * (n // len(u))) else str(cnt + 3), "counted the groups instead of the shapes"), W(str(n), "gave the total number of shapes")],
                FN("seq_count", unit=u, n=n, shape=tgt), qtype="conceptual", tags={"reasoning"})


def tiles_case(r, L):
    rows = r.randint(1, 3)
    c0 = r.randint(1, 2)
    extra = r.randint(0, 2)
    figs_ = [[rows, c0 + i, extra] for i in range(3)]
    cnt = [f[0] * f[1] + f[2] for f in figs_]
    alt = "Three figures made of square tiles. " + " ".join(f"Figure {i + 1} has {c} tiles." for i, c in enumerate(cnt))
    return figs_, cnt, rows, Diagram("tile_figs", {"figures": figs_}, alt)


@fam("012")
def sp_tiles_next(r, L):
    figs_, cnt, step, dg = tiles_case(r, L)
    n = 4 if L == 0 else r.randint(5, 6) if L == 1 else r.randint(8, 12)
    v = cnt[0] + step * (n - 1)
    return Item(f"The figures grow in a pattern. If the pattern continues, how many tiles will be in Figure {n}?", str(v),
                [f"The figures have {lst(cnt)} tiles. Each figure has {step} more tile{'s' if step != 1 else ''} than the one before.", f"Keep adding {step} until Figure {n}: {v} tiles."],
                [W(str(cnt[2] + step) if n != 4 else str(v + step), "found the wrong figure"), W(str(v - step), "stopped one figure early"), W(str(cnt[2] * 2), "doubled the last figure"), W(str(v + 1), "miscounted")],
                FN("tile_fig", figures=figs_, n=n), qtype="visual", diagram=dg, tags={"modeling"})


@fam("012", mode="mc")
def sp_tiles_rule(r, L):
    figs_, cnt, step, dg = tiles_case(r, L)
    good = f"add {step}"
    return Item("Count the tiles in each figure. What is the rule for the number of tiles?", good, [f"The figures have {lst(cnt)} tiles.", f"Each figure has {step} more than the one before, so the rule is “{good}.”"],
                [W(f"add {step + 1}", "found the wrong difference"), W(f"multiply by {max(2, step)}" if cnt[1] != cnt[0] * max(2, step) or cnt[2] != cnt[1] * max(2, step) else "multiply by 5", "only checked the first two figures"), W(f"add {cnt[0]}" if cnt[0] != step else f"add {step + 2}", "used the number of tiles in Figure 1")],
                FN("rule_of", seq=cnt), qtype="visual", diagram=dg)


@fam("012", mode="mc")
def sp_tiles_feature(r, L):
    figs_, cnt, step, dg = tiles_case(r, L)
    good = feature_of(cnt[0], step)
    return Item(f"The figures have {lst(cnt)} tiles. If the pattern continues, which statement is true about the number of tiles in the figures?", good,
                [f"Figure 1 has {cnt[0]} tile{'s' if cnt[0] != 1 else ''} and each new figure adds {step}.", good], [W(f, "this does not describe the pattern") for f in FEATURES if f != good],
                FN("pattern_feature", start=cnt[0], step=step), qtype="explain", diagram=dg, tags={"reasoning"})


@fam("12")
def sp_which_figure(r, L):
    figs_, cnt, step, dg = tiles_case(r, L)
    n = r.randint(6, 12) if L == 1 else r.randint(13, 25)
    v = cnt[0] + step * (n - 1)
    return Item(f"The figures grow in a pattern. If the pattern continues, which figure number will have exactly {v} tiles?", str(n),
                [f"Figure 1 has {cnt[0]} tile{'s' if cnt[0] != 1 else ''} and each figure adds {step}.", f"({v} − {cnt[0]}) ÷ {step} = {n - 1} more steps, so it is Figure {n}."],
                [W(str(n - 1), "counted the steps but forgot Figure 1"), W(str(n + 1), "counted one figure too many"), W(str(v // step) if v // step not in (n, n - 1, n + 1) else str(n + 2), "divided without subtracting the first figure"), W(str(v), "gave the number of tiles")],
                FN("tile_fig_index", figures=figs_, count=v), qtype="multi-step", diagram=dg, tags={"reasoning", "challenge"})


SKILLS = {
    1: dict(name="Factors and Factor Pairs", fams=[fa_list, fa_count, fa_pair_missing, fa_is_factor, fa_array, fa_common, fa_rows]),
    2: dict(name="Multiples", fams=[mu_list, mu_is_multiple, mu_nth, mu_common, mu_factor_link, mu_count_between, mu_packs]),
    3: dict(name="Prime and Composite Numbers", fams=[pc_classify, pc_which_prime, pc_which_composite, pc_count, pc_list, pc_counterexample, pc_sum]),
    4: dict(name="Number Patterns and Rules", fams=[np_next, np_generate, np_rule, np_feature, np_nth, np_missing, np_multiply, np_table, np_two_step]),
    5: dict(name="Shape Patterns and Pattern Features", fams=[sp_next, sp_nth, sp_count, sp_tiles_next, sp_tiles_rule, sp_tiles_feature, sp_which_figure]),
}
