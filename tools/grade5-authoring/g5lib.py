"""Grade 5 authoring helpers: exact number formatting, the problem record, family registration, derived extras.

Every family is a function f(r, L) -> Item, where r is a seeded random.Random and L is the level
(0 = Remedial/cp2, 1 = Standard/cp1, 2 = Advanced/honors). A family raises Reject for an unusable draw.
Each Item carries a `check` that the independent verifier (verify.py) evaluates WITHOUT importing this module.
"""
import hashlib, random, re
from fractions import Fraction as F
from decimal import Decimal

LEVELS = ["cp2", "cp1", "honors"]
LABEL = {"cp2": "Remedial", "cp1": "Standard", "honors": "Advanced"}
NAMES = ["Ava", "Ben", "Carmen", "Dev", "Elena", "Femi", "Grace", "Hiro", "Isla", "Jamal", "Kai", "Lena", "Marco", "Nia",
         "Omar", "Priya", "Quinn", "Rosa", "Sam", "Tariq", "Uma", "Leo", "Wren", "Yusuf", "Zoe", "Mateo", "Aisha", "Noah",
         "Sofia", "Liam", "Mei", "Diego", "Hana", "Eli", "Maya", "Jonah", "Lucia", "Ravi", "Tessa", "Oscar"]
# question types (stored in meta; the bank schema only knows 4 formats)
QTYPES = {"procedural", "conceptual", "visual", "word-problem", "multi-step", "error-analysis", "true-false", "matching",
          "ordering", "fill-blank", "compare-strategies", "explain", "real-world", "diagram", "numerical"}


class Reject(Exception):
    pass


def need(cond):
    if not cond:
        raise Reject()


def rng(*parts):
    h = hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()
    return random.Random(int(h[:16], 16))


def pick(r, seq):
    return seq[r.randrange(len(seq))]


def name(r):
    return pick(r, NAMES)


# ------------------------------------------------------------------ exact formatting
def is_term(x):
    x = F(x)
    d = x.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1


def comma(n):
    n = int(n)
    return f"{n:,}" if abs(n) >= 1000 else str(n)


def dec(x, places=None):
    """Exact decimal text: 3.45, 0.5, 12 (no trailing zeros unless places given). Integers get commas."""
    x = F(x)
    need(is_term(x))
    d = Decimal(x.numerator) / Decimal(x.denominator)
    if places is not None:
        q = Decimal(1).scaleb(-places)
        s = format(d.quantize(q), "f")
    else:
        s = format(d.normalize(), "f")
        if "." in s:
            s = s.rstrip("0").rstrip(".")
    if "." in s:
        a, b = s.split(".")
        return comma(int(a)) + "." + b if a not in ("", "-0") else s
    return comma(int(s))


def money(x):
    x = F(x)
    return "$" + dec(x, 2) if x.denominator != 1 else "$" + dec(x, 2)


def frac(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def mixed(x):
    x = F(x)
    if x.denominator == 1:
        return comma(x.numerator)
    if x < 1:
        return frac(x)
    w, rem = divmod(x.numerator, x.denominator)
    return f"{w} {rem}/{x.denominator}"


def fr_raw(n, d):
    """Unsimplified fraction text."""
    return f"{n}/{d}"


def num(x):
    """Whole number with commas, else mixed number."""
    return mixed(x)


def plural(n, word, pl=None):
    return f"{word}" if F(n) == 1 else (pl or word + "s")


# ------------------------------------------------------------------ checks (data only; evaluated by verify.py)
def EX(expr, unit=None, form=None):
    """Arithmetic expression over the numbers shown in the problem. form: 'mixed'|'frac'|'dec'|'whole'|None."""
    d = {"k": "expr", "e": expr}
    if unit:
        d["unit"] = unit
    if form:
        d["form"] = form
    return d


def KEY(*accept):
    return {"k": "key", "accept": list(accept)}


def FN(fn, **kw):
    assert "k" not in kw, "the key k is reserved for the check kind"
    d = {"k": "fn", "fn": fn}
    d.update(kw)
    return d


# ------------------------------------------------------------------ diagrams
class Diagram:
    """kind + data; figs.render(kind, data) draws the SVG; alt text is written from the same data."""
    def __init__(self, kind, data, alt):
        self.kind, self.data, self.alt = kind, data, alt


# ------------------------------------------------------------------ the problem record
class Item:
    def __init__(self, prompt, answer, steps, wrong=(), check=None, qtype="procedural", tags=(), diagram=None,
                 options=None, parts=None, mode="any", misconception=None, mc_prompt=None, claim=None):
        self.prompt = prompt
        self.answer = answer if answer is None else str(answer)
        self.steps = list(steps)
        self.wrong = wrongs(answer, wrong) if answer is not None else [(str(w[0]), w[1]) if isinstance(w, tuple) else (str(w), "") for w in wrong]
        self.check = check
        self.qtype = qtype
        self.tags = set(tags)
        self.diagram = diagram
        self.options = options       # authored choices: [(text, correct)]
        self.parts = parts           # [(prompt, answer, check)]
        self.mode = mode             # 'any' | 'sa' | 'mc'
        self.misconception = misconception
        self.mc_prompt = mc_prompt
        self.claim = claim           # short "problem" text used by select-all / true-false extras
        need(answer is not None or parts or options)
        if check is None and options is None and not parts:
            raise ValueError("item without check")


def W(text, why=""):
    return (str(text), why)


# ------------------------------------------------------------------ family registry
def fam(levels="012", mode="any", qtype=None):
    def deco(f):
        f.levels = [int(c) for c in levels]
        f.mode = mode
        f.qtype = qtype
        return f
    return deco


def _norm(t):
    return re.sub(r"\s+", " ", str(t).strip().lower().replace(",", ""))


def sub(r, k):
    return rng("sub", r.random(), k)


def err_of(core, who=None):
    """Error analysis: show a classmate's misconception answer (with its documented reason) and ask for the fix."""
    def f(r, L):
        p = core(r, L)
        cands = [(w, y) for w, y in p.wrong if y and _norm(w) != _norm(p.answer)]
        need(cands and p.answer is not None and not p.options and not p.parts)
        w, y = pick(r, cands)
        nm = who or name(r)
        it = Item(f"{nm} solved this problem.\n{p.prompt}\n{nm} answered: {w}\nFind the mistake. What is the correct answer?",
                  p.answer, [f"Mistake: {y}."] + p.steps + [f"The correct answer is {p.answer}, not {w}."],
                  [x for x in p.wrong if _norm(x[0]) != _norm(w)], p.check, qtype="error-analysis",
                  tags=p.tags | {"error-analysis", "misconception"}, diagram=p.diagram, mode="sa", misconception=y)
        it.shown = w
        it.consts = getattr(p, "consts", [])
        return it
    f.__name__ = core.__name__ + "_error"
    f.levels, f.mode, f.qtype = core.levels, "sa", "error-analysis"
    return f


def tf_of(core):
    """True or false with reasoning: a claimed answer (correct or a documented misconception) and four reasoned choices."""
    def f(r, L):
        p = core(r, L)
        need(p.answer is not None and not p.options and not p.parts and not p.diagram and len(p.prompt) < 150 and "\n" not in p.prompt)
        ws = [w for w, y in p.wrong if _norm(w) != _norm(p.answer)]
        uniq = []
        for w in ws:
            if _norm(w) not in [_norm(u) for u in uniq]:
                uniq.append(w)
        need(len(uniq) >= 3)
        truthful = r.random() < 0.45
        shown = p.answer if truthful else uniq[0]
        reason = p.steps[-1].rstrip(".")
        opts = [(f"True. {reason}." if truthful else f"True. {shown} is the correct answer.", truthful)]
        if truthful:
            opts += [(f"False. The correct answer is {w}.", False) for w in uniq[:3]]
        else:
            opts.append((f"False. The correct answer is {p.answer}.", True))
            opts += [(f"False. The correct answer is {w}.", False) for w in uniq[1:3]]
        need(len(opts) == 4 and len({_norm(t) for t, _ in opts}) == 4)
        r.shuffle(opts)
        claim = p.claim or p.prompt
        good = [t for t, c in opts if c][0]
        it = Item(f"True or false? {claim}\nAnswer shown: {shown}\nChoose the best response.", good,
                  p.steps + ([f"The answer {shown} is correct."] if truthful else [f"The answer {shown} is not correct; it should be {p.answer}."]),
                  check=FN("tf", inner=p.check, shown=shown, answer=p.answer), qtype="true-false", tags=p.tags | {"reasoning"},
                  options=opts, mode="mc")
        return it
    f.__name__ = core.__name__ + "_tf"
    f.levels, f.mode, f.qtype = core.levels, "mc", "true-false"
    return f


def open_of(core, lead="Answer each part. Show your work.", n=4):
    def f(r, L):
        parts, seen, steps = [], set(), []
        for k in range(n * 8):
            if len(parts) == n:
                break
            try:
                p = core(sub(r, k), L)
            except Reject:
                continue
            if p.answer is None or p.options or p.parts or p.diagram or _norm(p.prompt) in seen or "\n" in p.prompt:
                continue
            seen.add(_norm(p.prompt))
            parts.append((p.prompt, p.answer, p.check))
            steps.append(f"({chr(96 + len(parts))}) " + " ".join(p.steps[-2:]))
        need(len(parts) == n)
        return Item(lead, None, steps, parts=parts, qtype="multi-step", tags={"multistep"})
    f.__name__ = core.__name__ + "_open"
    f.levels, f.mode, f.qtype = core.levels, None, "multi-step"
    return f


def match_of(core, n=4):
    """Matching: four problems, each matched to its answer (open response with one answer per part)."""
    g = open_of(core, "Match each problem with its answer. Write the answer next to each letter.", n)

    def f(r, L):
        it = g(r, L)
        it.qtype = "matching"
        return it
    f.__name__ = core.__name__ + "_match"
    f.levels, f.mode, f.qtype = core.levels, None, "matching"
    return f


def select_of(core, k_true=2, k_false=2):
    """Select all: 'problem → answer' claims, some correct, some with a documented misconception answer."""
    def f(r, L):
        good, bad, table = [], [], {}
        for k in range(40):
            if len(good) >= k_true and len(bad) >= k_false:
                break
            try:
                p = core(sub(r, k), L)
            except Reject:
                continue
            if p.answer is None or p.options or p.parts or p.diagram or "\n" in p.prompt or len(p.claim or p.prompt) > 95:
                continue
            short = p.claim or p.prompt
            if len(good) < k_true and (len(bad) >= k_false or r.random() < 0.5):
                t, ok, a = f"{short} → {p.answer}", True, p.answer
            else:
                ws = [w for w, _ in p.wrong if _norm(w) != _norm(p.answer)]
                if not ws:
                    continue
                a = pick(r, ws)
                t, ok = f"{short} → {a}", False
            if t in table:
                continue
            table[t] = {"inner": p.check, "shown": a}
            (good if ok else bad).append(t)
        need(len(good) == k_true and len(bad) == k_false)
        opts = [(t, True) for t in good] + [(t, False) for t in bad]
        r.shuffle(opts)
        return Item("Select ALL the problems that are matched with the correct answer.", None,
                    ["Work each problem and compare with the answer shown."] + [f"{t}: {'correct' if ok else 'not correct'}." for t, ok in opts],
                    options=opts, check=FN("claims", table=table), qtype="explain", tags={"reasoning"})
    f.__name__ = core.__name__ + "_sel"
    f.levels, f.mode, f.qtype = core.levels, None, "explain"
    return f


def mc_key(prompt, good, bad, steps, qtype="conceptual", tags=(), diagram=None, r=None, why=None):
    """Authored multiple choice with a text key (verified against an authored key)."""
    opts = [(good, True)] + [(b, False) for b in bad]
    need(len({_norm(t) for t, _ in opts}) == len(opts) and len(opts) >= 3)
    if r:
        r.shuffle(opts)
    return Item(prompt, good, steps, check=KEY(good), qtype=qtype, tags=tags, diagram=diagram, options=opts, mode="mc",
                misconception=why)


def value_of(t):
    """Numeric value of a plain answer text ('$1.50', '2 1/3', '1,200 feet'), or None."""
    m = re.fullmatch(r"\$?(\d[\d,]*(?:\.\d+)?)(?: (\d+)/(\d+))?(?:/(\d+))?(\s+[a-zA-Z ]+)?", str(t).strip())
    if not m:
        return None
    a, n, d, d2, unit = m.groups()
    v = F(a.replace(",", ""))
    if n:
        v += F(int(n), int(d))
    if d2:
        v /= int(d2)
    return (v, "$" if str(t).strip().startswith("$") else "")


def wrongs(answer, cands):
    """Keep distinct misconception answers that differ from the key (in text AND in value)."""
    out, seen = [], {_norm(answer)}
    va = value_of(answer)
    vals = {va} if va else set()
    for w in cands:
        t = w if isinstance(w, tuple) else (w, "")
        if _norm(t[0]) in seen or not str(t[0]).strip():
            continue
        vw = value_of(t[0])
        if vw is not None and vw in vals:
            continue
        if vw is not None:
            vals.add(vw)
        seen.add(_norm(t[0]))
        out.append(t)
    return out
