"""Grade 1 derived question formats: error analysis, true/false, select-all, open response.

The Grade 5 derived wrappers only accept picture-free, single-line core items, which would
leave the picture-heavy Grade 1 skills with no open-response or select-all questions at all.
These generators build the extra formats directly from a small domain fact factory instead,
so every skill and level gets 3 error analysis, 1 true/false, 1 select-all and 1 open
response that are appropriate to its mathematical domain and need no diagram.

Domains: oa (operations), nbt (place value), md (measurement and data), g (geometry and time).
"""
import random
from g1lib import Item, Reject, need, pick, name, FN, KEY, fam, _norm

DOMAINS = {"oa", "nbt", "md", "g"}
SHAPE_SIDES = {"triangle": 3, "square": 4, "rectangle": 4, "hexagon": 6}
SOLIDS = ["cube", "cylinder", "sphere", "cone"]


def _fact(domain, r, L):
    """One verifiable fact: dict(prompt, answer, chk, steps, wrong, claim)."""
    if domain == "oa":
        kind = r.randrange(4)
        top = 20 if L else 10
        if kind == 0:
            a, b = r.randint(1, top - 1), r.randint(1, 3)
            need(a + b <= top)
            return {"prompt": f"{a} + {b} = ?", "answer": str(a + b), "chk": FN("add", a=a, b=b),
                    "steps": [f"Start at {a} and add {b}.", f"{a} + {b} = {a + b}."],
                    "wrong": [(str(a + b + 1), "counted one too many"), (str(a + b - 1), "counted one too few"),
                              (str(abs(a - b)), "subtracted instead of adding")],
                    "claim": f"{a} + {b} = {a + b}"}
        if kind == 1:
            a = r.randint(2, top)
            b = r.randint(1, a)
            return {"prompt": f"{a} − {b} = ?", "answer": str(a - b), "chk": FN("sub", a=a, b=b),
                    "steps": [f"Start at {a} and take away {b}.", f"{a} − {b} = {a - b}."],
                    "wrong": [(str(a + b), "added instead of subtracting"), (str(a - b + 1), "counted one too many"),
                              (str(b), "gave the number taken away")],
                    "claim": f"{a} − {b} = {a - b}"}
        if kind == 2:
            total = r.randint(3, top)
            part = r.randint(1, total - 1)
            return {"prompt": f"{total} − {part} = ?", "answer": str(total - part),
                    "chk": FN("missing_part", total=total, part=part),
                    "steps": [f"The whole is {total} and one part is {part}.", f"{total} − {part} = {total - part}."],
                    "wrong": [(str(total + part), "added instead of subtracting"), (str(part), "gave the part, not the rest"),
                              (str(total - part + 1), "counted one too many")],
                    "claim": f"{total} − {part} = {total - part}"}
        a, b = r.randint(1, 5), r.randint(1, 5)
        return {"prompt": f"{a} + {b} = ?", "answer": str(a + b), "chk": FN("add", a=a, b=b),
                "steps": [f"Add {a} and {b}.", f"{a} + {b} = {a + b}."],
                "wrong": [(str(a + b + 2), "counted two too many"), (str(a - b) if a > b else str(a + b + 1), "used the wrong operation"),
                          (str(b), "gave one addend")],
                "claim": f"{a} + {b} = {a + b}"}

    if domain == "nbt":
        kind = r.randrange(4)
        if kind == 0:
            tens, ones = r.randint(1, 9), r.randint(0, 9)
            return {"prompt": f"What number is {tens} tens and {ones} ones?", "answer": str(tens * 10 + ones),
                    "chk": FN("tens_ones", tens=tens, ones=ones),
                    "steps": [f"{tens} tens is {tens * 10}.", f"{tens * 10} + {ones} = {tens * 10 + ones}."],
                    "wrong": [(str(ones * 10 + tens), "reversed the tens and ones"), (str(tens + ones), "added the digits"),
                              (str(tens * 10 + ones + 10), "added an extra ten")],
                    "claim": f"{tens} tens and {ones} ones is {tens * 10 + ones}"}
        if kind == 1:
            a, b = r.randint(11, 99), r.randint(11, 99)
            need(a != b)
            return {"prompt": f"Which is greater, {a} or {b}?", "answer": str(max(a, b)),
                    "chk": FN("which_number", a=a, b=b, which="greater"),
                    "steps": ["Compare the tens first, then the ones.", f"{max(a, b)} is greater than {min(a, b)}."],
                    "wrong": [(str(min(a, b)), "picked the smaller number"), (str(abs(a - b)), "gave the difference"),
                              (str(a + b), "added the numbers")],
                    "claim": f"{max(a, b)} is greater than {min(a, b)}"}
        if kind == 2:
            n, k = r.randint(10, 89), r.randint(1, 5)
            return {"prompt": f"What is 10 more than {n}?", "answer": str(n + 10 * k if False else n + 10),
                    "chk": FN("add", a=n, b=10),
                    "steps": ["Add one more ten.", f"{n} + 10 = {n + 10}."],
                    "wrong": [(str(n + 1), "added one instead of ten"), (str(n - 10), "went back ten"),
                              (str(n + 100), "added one hundred")],
                    "claim": f"10 more than {n} is {n + 10}"}
        tens, ones = r.randint(1, 9), r.randint(1, 9)
        return {"prompt": f"How many ones are in {tens} tens and {ones} ones?", "answer": str(ones),
                "chk": FN("ones_of", n=tens * 10 + ones, tens=tens),
                "steps": [f"{tens} tens make {tens * 10}.", f"The ones digit is {ones}."],
                "wrong": [(str(tens), "gave the tens digit"), (str(tens * 10), "gave the value of the tens"),
                          (str(tens * 10 + ones), "gave the whole number")],
                "claim": f"{tens} tens and {ones} ones is {tens * 10 + ones}"}

    if domain == "md":
        kind = r.randrange(3)
        a, b = r.randint(2, 12), r.randint(2, 12)
        need(a != b)
        if kind == 0:
            return {"prompt": f"One string is {a} cubes long. Another is {b} cubes long. Which is longer?",
                    "answer": "the first string" if a > b else "the second string",
                    "chk": FN("longer_ab", a=a, b=b),
                    "steps": [f"Compare the lengths: {a} and {b}.", f"{max(a, b)} is longer than {min(a, b)}."],
                    "wrong": [("the first string", "picked the other string"), ("the second string", "picked the other string"),
                              ("they are the same", "said the lengths are equal")],
                    "claim": f"{a} cubes is longer than {b} cubes" if a > b else f"{b} cubes is longer than {a} cubes"}
        if kind == 1:
            cats = ["red", "blue", "green"]
            counts = r.sample(range(2, 10), 3)
            best = max(counts)
            return {"prompt": f"The tally chart shows red {counts[0]}, blue {counts[1]}, green {counts[2]}. Which has the most?",
                    "answer": cats[counts.index(best)],
                    "chk": FN("most_of", labels=cats, counts=counts),
                    "steps": [f"Compare the counts: {counts[0]}, {counts[1]}, {counts[2]}.", f"{cats[counts.index(best)]} has the most."],
                    "wrong": [(c, "chose a smaller count") for c in cats if c != cats[counts.index(best)]][:3],
                    "claim": f"{cats[counts.index(best)]} has the most"}
        total = a + b
        return {"prompt": f"A ribbon is {a} cubes long. Another is {b} cubes long. How many cubes in all?",
                "answer": str(total), "chk": FN("add", a=a, b=b),
                "steps": [f"Put the lengths together: {a} + {b}.", f"{a} + {b} = {total}."],
                "wrong": [(str(abs(a - b)), "subtracted instead of adding"), (str(total + 1), "counted one too many"),
                          (str(max(a, b)), "gave the longer length")],
                "claim": f"{a} + {b} = {total}"}

    # geometry and time
    kind = r.randrange(4)
    if kind == 0:
        shape = pick(r, list(SHAPE_SIDES))
        return {"prompt": f"How many sides does a {shape} have?", "answer": str(SHAPE_SIDES[shape]),
                "chk": FN("shape_sides", kind=shape),
                "steps": [f"Count the sides of a {shape}.", f"A {shape} has {SHAPE_SIDES[shape]} sides."],
                "wrong": [(str(SHAPE_SIDES[shape] + 1), "counted one side too many"),
                          (str(SHAPE_SIDES[shape] - 1), "counted one side too few"),
                          (str(SHAPE_SIDES[shape] + 2), "counted two sides too many")],
                "claim": f"A {shape} has {SHAPE_SIDES[shape]} sides"}
    if kind == 1:
        shape = pick(r, ["triangle", "hexagon", "circle"])
        return {"prompt": f"Which shape has {SHAPE_SIDES.get(shape, 0)} sides?" if shape != "circle" else "Which shape has no straight sides?",
                "answer": shape, "chk": FN("shape_attr_name", sides=SHAPE_SIDES.get(shape, 0)),
                "steps": [f"A {shape} matches this rule.", f"The answer is {shape}."],
                "wrong": [(s, "chose a shape that does not match") for s in ["square", "triangle", "hexagon"] if s != shape][:3],
                "claim": f"A {shape} has {SHAPE_SIDES.get(shape, 0)} sides"}
    if kind == 2:
        h = r.randint(1, 12)
        m = r.choice([0, 30])
        return {"prompt": f"A clock shows {h}:{m:02d}. How many minutes after {h} o'clock is that?",
                "answer": str(m), "chk": FN("clock_minutes", h=h, m=m),
                "steps": [f"The minute hand points to {m} minutes.", f"The time is {h}:{m:02d}."],
                "wrong": [(str(30 if m == 0 else 0), "mixed up the minute hand"), (str(h), "gave the hour"),
                          (str(60), "gave a full hour")],
                "claim": f"{h}:{m:02d} is {m} minutes after {h} o'clock"}
    return {"prompt": "How many minutes are in half an hour?", "answer": "30", "chk": FN("half_hour"),
            "steps": ["An hour is 60 minutes.", "Half of 60 is 30."],
            "wrong": [("60", "gave a full hour"), ("15", "halved twice"), ("20", "used a different split")],
            "claim": "Half an hour is 30 minutes"}


# ------------------------------------------------------------------ formats
def err_family(domain):
    def f(r, L):
        need(domain in DOMAINS)
        for k in range(20):
            fct = _fact(domain, r, L)
            cands = [w for w, why in fct["wrong"] if _norm(w) != _norm(fct["answer"])]
            if cands:
                break
        else:
            raise Reject()
        shown = pick(r, cands)
        nm = name(r)
        return Item(f"{nm} solved this problem.\n{fct['prompt']}\n{nm} answered: {shown}\nFind the mistake. What is the correct answer?",
                    fct["answer"], [f"The answer {shown} is not correct."] + fct["steps"] + [f"The correct answer is {fct['answer']}."],
                    [(w, why) for w, why in fct["wrong"] if _norm(w) != _norm(shown)],
                    check=fct["chk"], qtype="error-analysis", tags={"error-analysis", "reasoning"},
                    mode="sa", misconception=f"answered {shown}")
    f.__name__ = f"err_{domain}"
    f.levels, f.mode, f.qtype = [0, 1, 2], "sa", "error-analysis"
    return f


def tf_family(domain):
    def f(r, L):
        fct = _fact(domain, r, L)
        truthful = r.random() < 0.45
        shown = fct["answer"] if truthful else pick(r, [w for w, _ in fct["wrong"] if _norm(w) != _norm(fct["answer"])])
        reason = fct["steps"][-1].rstrip(".")
        opts = [(f"True. {reason}." if truthful else f"True. {shown} is the correct answer.", truthful)]
        if truthful:
            opts += [(f"False. The correct answer is {w}.", False)
                     for w, _ in fct["wrong"] if _norm(w) != _norm(fct["answer"])][:3]
        else:
            opts.append((f"False. The correct answer is {fct['answer']}.", True))
            opts += [(f"False. The correct answer is {w}.", False)
                     for w, _ in fct["wrong"] if _norm(w) not in (_norm(fct["answer"]), _norm(shown))][:2]
        if len(opts) != 4 or len({_norm(t) for t, _ in opts}) != 4:
            raise Reject()
        r.shuffle(opts)
        good = [t for t, c in opts if c][0]
        return Item(f"True or false? {fct['claim']}\nAnswer shown: {shown}\nChoose the best response.", good,
                    fct["steps"] + ([f"The answer {shown} is correct."] if truthful else
                                    [f"The answer {shown} is not correct; it should be {fct['answer']}."]),
                    [], check=FN("tf", inner=fct["chk"], shown=shown, answer=fct["answer"]),
                    qtype="true-false", tags={"reasoning"}, options=opts, mode="mc")
    f.__name__ = f"tf_{domain}"
    f.levels, f.mode, f.qtype = [0, 1, 2], "mc", "true-false"
    return f


def sel_family(domain, k_true=2, k_false=2):
    def f(r, L):
        good, bad, table = [], [], {}
        for k in range(60):
            if len(good) >= k_true and len(bad) >= k_false:
                break
            fct = _fact(domain, r, L)
            make_good = len(good) < k_true and (len(bad) >= k_false or r.random() < 0.5)
            if make_good:
                text = f"{fct['prompt']} → {fct['answer']}"
                shown = fct["answer"]
                ok = True
            else:
                cands = [w for w, _ in fct["wrong"] if _norm(w) != _norm(fct["answer"])]
                if not cands:
                    continue
                shown = pick(r, cands)
                text = f"{fct['prompt']} → {shown}"
                ok = False
            if text in table or len(text) > 95:
                continue
            table[text] = {"inner": fct["chk"], "shown": shown}
            (good if ok else bad).append(text)
        if len(good) < k_true or len(bad) < k_false:
            raise Reject()
        opts = [(t, True) for t in good] + [(t, False) for t in bad]
        r.shuffle(opts)
        return Item("Select ALL the problems that are matched with the correct answer.", None,
                    ["Work each problem and compare with the answer shown."] +
                    [f"{t}: {'correct' if ok else 'not correct'}." for t, ok in opts],
                    [], options=opts, check=FN("claims", table=table), qtype="explain",
                    tags={"reasoning"}, mode="sel")
    f.__name__ = f"sel_{domain}"
    f.levels, f.mode, f.qtype = [0, 1, 2], None, "explain"
    return f


def open_family(domain, n=4):
    def f(r, L):
        parts, seen, steps = [], set(), []
        for k in range(n * 12):
            if len(parts) == n:
                break
            fct = _fact(domain, r, L)
            key = _norm(fct["prompt"])
            if key in seen:
                continue
            seen.add(key)
            parts.append((fct["prompt"], fct["answer"], fct["chk"]))
            steps.append(f"({chr(96 + len(parts))}) " + " ".join(fct["steps"][-2:]))
        if len(parts) != n:
            raise Reject()
        return Item("Answer each part. Show your work.", None, steps, parts=parts,
                    qtype="multi-step", tags={"multistep"})
    f.__name__ = f"open_{domain}"
    f.levels, f.mode, f.qtype = [0, 1, 2], None, "multi-step"
    return f


def extras_for(domain):
    domain = domain if domain in DOMAINS else "oa"
    return {"err": err_family(domain), "tf": tf_family(domain),
            "sel": sel_family(domain), "open": open_family(domain)}
