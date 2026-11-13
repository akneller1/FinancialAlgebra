"""Grade 2 derived formats (error analysis, true/false, select-all, open response).

The Grade 1 generators build these from a domain fact factory; Grade 2 reuses that machinery
with Grade 2 fact pools (regrouping, place value to 1,000, money, time to five minutes,
measurement, shapes and arrays) so every skill and level gets all four extra formats.
"""
import extras
from extras import err_family, tf_family, sel_family, open_family, DOMAINS
from g1lib import FN, need, pick

THINGS = ["stickers", "marbles", "shells", "beads", "cards", "tiles", "books", "buttons"]


def _b(L, lo, mid, hi):
    return (lo, mid, hi)[max(0, min(2, int(L)))]


def _fact2(domain, r, L):
    """One verifiable Grade 2 fact, scaled to the level.

    Remedial stays inside one place value with small numbers, Standard works with
    two-digit regrouping or three-digit numbers, Advanced uses the largest numbers
    in the grade (three digits, carrying across two places, hundreds rounding).
    """
    if domain == "oa":
        kind = r.randrange(4)
        if kind == 0:  # addition that carries
            b_o = r.randint(2, 9)
            a_o = r.randint(10 - b_o, 9)
            if L == 0:
                a, b = r.randint(1, 3) * 10 + a_o, b_o
            elif L == 1:
                a, b = r.randint(2, 8) * 10 + a_o, r.randint(1, 4) * 10 + b_o
            else:
                a = r.randint(1, 8) * 100 + r.randint(1, 8) * 10 + a_o
                b = r.randint(1, 4) * 100 + r.randint(1, 8) * 10 + b_o
            ans = a + b
            carry = a_o + b_o - 10
            steps = [f"Add the ones: {a_o} + {b_o} = {a_o + b_o}, which is 1 ten and {carry} ones."]
            steps.append(f"Add the tens: {a} + {b} = {ans}." if L < 2
                         else f"Add the tens and hundreds: {a} + {b} = {ans}.")
            return {"prompt": f"{a} + {b} = ?", "answer": str(ans), "chk": FN("add", a=a, b=b),
                    "steps": steps,
                    "wrong": [(str(ans - 10), "forgot to add the new ten"), (str(ans + 10), "added an extra ten"),
                              (str(abs(a - b)), "subtracted instead of adding")],
                    "claim": f"{a} + {b} = {ans}"}
        if kind == 1:  # subtraction that borrows
            a_o = r.randint(0, 7)
            b_o = r.randint(a_o + 1, 9)
            if L == 0:
                a, b = r.randint(2, 6) * 10 + a_o, b_o
            elif L == 1:
                tens = r.randint(3, 9)
                a, b = tens * 10 + a_o, r.randint(1, tens - 1) * 10 + b_o
            else:
                a = r.randint(2, 9) * 100 + r.randint(0, 9) * 10 + a_o
                b = r.randint(1, (a // 100) - 1 if a >= 300 else 1) * 100 + r.randint(0, 9) * 10 + b_o
            ans = a - b
            return {"prompt": f"{a} \u2212 {b} = ?", "answer": str(ans), "chk": FN("sub", a=a, b=b),
                    "steps": [f"Break apart a ten to subtract: {a} \u2212 {b} = {ans}."],
                    "wrong": [(str(abs(a - b) + 100 if abs(a - b) > 99 else a + b), "added instead of subtracting"),
                              (str(ans + 10), "did not break apart a ten"),
                              (str(abs(ans - 10)), "subtracted one ten too few")],
                    "claim": f"{a} \u2212 {b} = {ans}"}
        if kind == 2:  # unknown part
            total = r.randint(11, _b(L, 20, 99, 999))
            part = r.randint(2, total - 1)
            ans = total - part
            return {"prompt": f"{part} + ___ = {total}. What number completes the sentence?", "answer": str(ans),
                    "chk": FN("missing_part", total=total, part=part),
                    "steps": [f"Subtract the part you know: {total} \u2212 {part} = {ans}."],
                    "wrong": [(str(total + part), "added instead of subtracting"),
                              (str(ans + 10), "counted one ten too many"), (str(part), "gave the part that was already known")],
                    "claim": f"{part} + {ans} = {total}"}
        step = _b(L, 10, 5, 100)
        if L == 2:
            start = r.randint(1, 6) * 100 + r.randint(1, 9) * 10
        else:
            start = step * r.randint(2, 9)
        seqv = [start + step * k for k in range(5)]
        i = r.randint(1, 4)
        missing = seqv[i]
        return {"prompt": f"Count by {step}s: " + ", ".join("___" if k == i else str(v) for k, v in enumerate(seqv)) +
                          ". What number is missing?", "answer": str(missing),
                "chk": FN("skip_seq", values=seqv, missing=missing, step=step),
                "steps": [f"Each number is {step} more than the one before.", f"The missing number is {missing}."],
                "wrong": [(str(missing + step), "went one step too far"), (str(missing - step), "went back one step"),
                          (str(missing + 1), "counted by one")],
                "claim": f"The pattern counts by {step}s"}

    if domain == "nbt":
        kind = r.randrange(4)
        if L == 0:
            t, o = r.randint(1, 9), r.randint(0, 9)
            n, places = t * 10 + o, ["tens", "ones"]
            h = 0
        elif L == 1:
            h, t, o = r.randint(1, 4), r.randint(0, 9), r.randint(0, 9)
            n, places = h * 100 + t * 10 + o, ["hundreds", "tens", "ones"]
        else:
            h, t, o = r.randint(5, 9), r.randint(0, 9), r.randint(0, 9)
            n, places = h * 100 + t * 10 + o, ["hundreds", "tens", "ones"]
        if kind == 0:
            which = r.choice(places)
            val = {"hundreds": h * 100, "tens": t * 10, "ones": o}[which]
            digit = {"hundreds": h, "tens": t, "ones": o}[which]
            return {"prompt": f"In {n}, what is the value of the digit in the {which} place?", "answer": str(val),
                    "chk": FN("digit_value3", n=n, which=which),
                    "steps": [f"The digit in the {which} place is {digit}.", f"Its value is {val}."],
                    "wrong": [(str(digit), "gave the digit, not its value"), (str(val * 10), "used the next place"),
                              (str(val // 10 if val >= 10 else val + 1), "used the place to the right")],
                    "claim": f"The {which} digit of {n} is {digit}"}
        if kind == 1:
            step = r.choice([10, 100]) if L == 2 else 10
            return {"prompt": f"What is {step} less than {n}?", "answer": str(n - step),
                    "chk": FN("sub", a=n, b=step),
                    "steps": [f"Taking away {step} changes the {'hundreds' if step == 100 else 'tens'} place."],
                    "wrong": [(str(n + step), "added instead of subtracting"),
                              (str(n - step - step if n - step - step > 0 else n - 1), "took away too much"),
                              (str(n - 1), "counted back by one")],
                    "claim": f"{n} \u2212 {step} = {n - step}"}
        if kind == 2:
            b = r.randint(*((10, 99) if L == 0 else (100, 999)))
            a = n
            if L == 2:
                b = h * 100 + r.randint(0, 9) * 10 + r.randint(0, 9)
            need(a != b)
            big = max(a, b)
            return {"prompt": f"Which number is greater, {a} or {b}?", "answer": str(big),
                    "chk": FN("which_number", a=a, b=b, which="greater"),
                    "steps": ["Compare the hundreds, then the tens, then the ones."],
                    "wrong": [(str(min(a, b)), "picked the lesser number"), (str(big + 100), "changed a digit"),
                              (str(big + 10), "changed the tens digit")],
                    "claim": f"{a} and {b} are both numbers to compare"}
        if L == 2:
            need(n % 50 != 25)
            low = n // 100 * 100
            return {"prompt": f"Round {n} to the nearest hundred.", "answer": str(low if n - low < 50 else low + 100),
                    "chk": FN("round100", n=n),
                    "steps": [f"{n} is between {low} and {low + 100}.",
                              f"It is closer to {low if n - low < 50 else low + 100}."],
                    "wrong": [(str(low + 100 if n - low < 50 else low), "rounded the wrong way"),
                              (str(n), "did not round"), (str(low), "rounded down without checking")],
                    "claim": f"{n} rounds to the nearest hundred"}
        down = n // 10 * 10
        up = down + 10
        need(n % 10 != 5)
        return {"prompt": f"Round {n} to the nearest ten.", "answer": str(down if n - down < 5 else up),
                "chk": FN("round10", n=n),
                "steps": [f"{n} is between {down} and {up}.", "It is closer to the answer."],
                "wrong": [(str(up if n - down < 5 else down), "rounded the wrong way"),
                          (str(n), "did not round"), (str(down + 10), "rounded up too far")],
                "claim": f"{n} rounds to the nearest ten"}

    if domain == "md":
        kind = r.randrange(4)
        if kind == 0:
            if L == 0:
                d, q = r.randint(1, 5), 0
            elif L == 1:
                d, q = r.randint(1, 6), r.randint(0, 3)
            else:
                d, q = r.randint(5, 9) + 10, r.randint(1, 3)
            cents = d * 10 + q * 25
            return {"prompt": f"How much money is {d} {'dime' if d == 1 else 'dimes'}"
                              + (f" and {q} {'quarter' if q == 1 else 'quarters'}" if q else "") + "?",
                    "answer": f"{cents}\u00a2",
                    "chk": FN("money_cents", cents=cents),
                    "steps": [f"{d} dimes is {d * 10}\u00a2"
                              + (f" and {q} quarters is {q * 25}\u00a2." if q else "."), f"The total is {cents}\u00a2."],
                    "wrong": [(f"{cents + 10}\u00a2", "counted a dime twice"), (f"{cents + 25}\u00a2", "counted an extra quarter"),
                              (f"{d * 10 + q}\u00a2", "counted quarters as pennies")],
                    "claim": f"{d} dimes" + (f" and {q} quarters" if q else "") + f" make {cents}\u00a2"}
        if kind == 1:
            h = r.randint(1, 12)
            m = r.choice([0, 30]) if L == 0 else r.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
            return {"prompt": "What time is shown on the clock?", "answer": f"{h}:{m:02d}",
                    "chk": FN("clock", h=h, m=m),
                    "steps": [f"The hour hand is between {h} and {(h % 12) + 1}.", f"The time is {h}:{m:02d}."],
                    "wrong": [(f"{h}:{(m + 5) % 60:02d}", "moved the minute hand too far"),
                              (f"{(h % 12) + 1}:{m:02d}", "moved the hour hand"),
                              (f"{(h % 12) + 1}:{(m + 5) % 60:02d}", "moved both hands")],
                    "claim": f"The clock shows {h}:{m:02d}"}
        if kind == 2:
            n = r.randint(*((3, 9) if L == 0 else (10, 19) if L == 1 else (20, 99)))
            return {"prompt": f"An object is {n} centimeter cubes long. How many centimeters long is it?", "answer": str(n),
                    "chk": FN("count", n=n),
                    "steps": [f"Count the centimeter cubes: {n}."],
                    "wrong": [(str(n + 1), "counted one too many"), (str(n - 1 if n > 1 else n + 2), "counted one too few")],
                    "claim": f"The object is {n} centimeters long"}
        a = r.randint(*((5, 20) if L == 0 else (20, 99) if L == 1 else (100, 400)))
        b = r.randint(*((5, 20) if L == 0 else (20, 99) if L == 1 else (100, 400)))
        need(a != b)
        return {"prompt": f"One ribbon is {a} centimeters and another is {b} centimeters. How much longer is the longer ribbon?",
                "answer": str(abs(a - b)), "chk": FN("tape_diff", a=a, b=b),
                "steps": [f"Subtract the shorter length: {max(a, b)} \u2212 {min(a, b)} = {abs(a - b)}."],
                "wrong": [(str(a + b), "added the lengths"), (str(max(a, b)), "gave the longer length"),
                          (str(abs(a - b) + 1), "counted one too many")],
                "claim": f"The ribbons are {a} and {b} centimeters long"}

    kind = r.randrange(4)
    if kind == 0:
        sides = r.choice([3, 4] if L == 0 else [3, 4, 5, 6] if L == 1 else [3, 4, 5, 6, 8])
        kinds = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 8: "octagon"}
        k = kinds[sides]
        return {"prompt": f"How many sides does a {k} have?", "answer": str(sides),
                "chk": FN("polygon_sides", kind=k),
                "steps": [f"A {k} has {sides} sides."],
                "wrong": [(str(sides + 1), "counted one side too many"), (str(sides - 1), "counted one side too few"),
                          (str(sides + 2), "counted two sides too many")],
                "claim": f"A {k} has {sides} sides"}
    if kind == 1:
        parts = r.choice([2, 4] if L == 0 else [2, 3, 4] if L == 1 else [2, 3, 4, 6, 8])
        word = {2: "halves", 3: "thirds", 4: "fourths", 6: "sixths", 8: "eighths"}[parts]
        others = [w for p, w in {2: "halves", 3: "thirds", 4: "fourths", 6: "sixths", 8: "eighths"}.items() if p != parts]
        return {"prompt": f"A shape is cut into {parts} equal parts. What are the parts called?", "answer": word,
                "chk": FN("part_name", parts=parts),
                "steps": [f"{parts} equal parts are called {word}."],
                "wrong": [(others[0], "used the wrong fraction word"), (others[1], "used another fraction word"),
                          (others[2] if len(others) > 2 else "tenths", "used a fraction word that does not match")],
                "claim": f"{parts} equal parts are {word}"}
    if kind == 2:
        lo, hi = (2, 3) if L == 0 else (2, 6) if L == 1 else (3, 9)
        rows, cols = r.randint(lo, hi), r.randint(lo, hi)
        return {"prompt": f"An array has {rows} rows and {cols} in each row. How many dots in all?", "answer": str(rows * cols),
                "chk": FN("array_total", rows=rows, cols=cols),
                "steps": [f"{rows} rows of {cols} is {rows * cols}."],
                "wrong": [(str(rows + cols), "added the rows and columns"), (str(rows * cols - rows), "left out a row"),
                          (str(rows * cols + cols), "added an extra row")],
                "claim": f"{rows} rows of {cols} is {rows * cols}"}
    n = r.randint(*((10, 20) if L == 0 else (20, 99) if L == 1 else (100, 999)))
    ans = "even" if n % 2 == 0 else "odd"
    return {"prompt": f"Is {n} even or odd?", "answer": ans, "chk": FN("even_odd", n=n),
            "steps": [f"The ones digit is {n % 10}.", f"{n} is {ans}."],
            "wrong": [("odd" if ans == "even" else "even", "read the ones digit incorrectly"),
                      ("even" if ans == "even" else "odd", "counted the tens digit"),
                      ("neither" if ans == "even" else "both", "did not decide")],
            "claim": f"{n} is {ans}"}


extras._fact = _fact2


def extras_for(domain):
    domain = domain if domain in DOMAINS else "oa"
    return {"err": err_family(domain), "tf": tf_family(domain),
            "sel": sel_family(domain), "open": open_family(domain)}
