"""Grade 2 derived formats (error analysis, true/false, select-all, open response).

The Grade 1 generators build these from a domain fact factory; Grade 2 reuses that machinery
with Grade 2 fact pools (regrouping, place value to 1,000, money, time to five minutes,
measurement, shapes and arrays) so every skill and level gets all four extra formats.
"""
import extras
from extras import err_family, tf_family, sel_family, open_family, DOMAINS
from g1lib import FN, need, pick

THINGS = ["stickers", "marbles", "shells", "beads", "cards", "tiles", "books", "buttons"]


def _fact2(domain, r, L):
    """One verifiable Grade 2 fact: dict(prompt, answer, chk, steps, wrong, claim)."""
    if domain == "oa":
        kind = r.randrange(4)
        if kind == 0:
            a_o = r.randint(2, 9)
            b_o = r.randint(10 - a_o, 9)
            a = r.randint(2, 6) * 10 + a_o
            b = r.randint(1, 4) * 10 + b_o
            ans = a + b
            return {"prompt": f"{a} + {b} = ?", "answer": str(ans), "chk": FN("add", a=a, b=b),
                    "steps": [f"Add the ones: {a_o} + {b_o} = {a_o + b_o}, which is 1 ten and {a_o + b_o - 10} ones.",
                              f"Add the tens: {a} + {b} = {ans}."],
                    "wrong": [(str(ans - 10), "forgot to add the new ten"), (str(ans + 10), "added an extra ten"),
                              (str(abs(a - b)), "subtracted instead of adding")],
                    "claim": f"{a} + {b} = {ans}"}
        if kind == 1:
            b = r.randint(11, 39)
            a = r.randint(b + 11, 99)
            ans = a - b
            return {"prompt": f"{a} \u2212 {b} = ?", "answer": str(ans), "chk": FN("sub", a=a, b=b),
                    "steps": [f"Break apart a ten to subtract: {a} \u2212 {b} = {ans}."],
                    "wrong": [(str(a + b), "added instead of subtracting"), (str(ans + 10), "did not break apart a ten"),
                              (str(abs(ans - 10)), "subtracted one ten too few")],
                    "claim": f"{a} \u2212 {b} = {ans}"}
        if kind == 2:
            total = r.randint(30, 90)
            part = r.randint(10, total - 10)
            ans = total - part
            return {"prompt": f"{part} + ___ = {total}. What number completes the sentence?", "answer": str(ans),
                    "chk": FN("missing_part", total=total, part=part),
                    "steps": [f"Subtract the part you know: {total} \u2212 {part} = {ans}."],
                    "wrong": [(str(total + part), "added instead of subtracting"), (str(ans + 10), "counted one ten too many"),
                              (str(part), "gave the part that was already known")],
                    "claim": f"{part} + {ans} = {total}"}
        step = r.choice([5, 10, 100])
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
        h, t, o = r.randint(1, 9), r.randint(0, 9), r.randint(0, 9)
        n = h * 100 + t * 10 + o
        if kind == 0:
            which = r.choice(["hundreds", "tens", "ones"])
            val = {"hundreds": h * 100, "tens": t * 10, "ones": o}[which]
            digit = {"hundreds": h, "tens": t, "ones": o}[which]
            return {"prompt": f"In {n}, what is the value of the digit in the {which} place?", "answer": str(val),
                    "chk": FN("digit_value3", n=n, which=which),
                    "steps": [f"The digit in the {which} place is {digit}.", f"Its value is {val}."],
                    "wrong": [(str(digit), "gave the digit, not its value"), (str(val * 10), "used the next place"),
                              (str(val // 10 if val >= 10 else val + 1), "used the place to the right")],
                    "claim": f"The {which} digit of {n} is {digit}"}
        if kind == 1:
            step = r.choice([10, 100])
            return {"prompt": f"What is {step} less than {n}?", "answer": str(n - step),
                    "chk": FN("sub", a=n, b=step),
                    "steps": [f"Taking away {step} changes the {'hundreds' if step == 100 else 'tens'} place."],
                    "wrong": [(str(n + step), "added instead of subtracting"), (str(n - step - step if n - step - step > 0 else n - 1),
                              "took away too much"), (str(n - 1), "counted back by one")],
                    "claim": f"{n} \u2212 {step} = {n - step}"}
        if kind == 2:
            a, b = n, r.randint(100, 999)
            need(a != b)
            big = max(a, b)
            return {"prompt": f"Which number is greater, {a} or {b}?", "answer": str(big),
                    "chk": FN("which_number", a=a, b=b, which="greater"),
                    "steps": ["Compare the hundreds, then the tens, then the ones."],
                    "wrong": [(str(min(a, b)), "picked the lesser number"), (str(big + 100), "changed a digit"),
                              (str(big + 10), "changed the tens digit")],
                    "claim": f"{a} and {b} are both three-digit numbers"}
        down = n // 10 * 10
        up = down + 10
        need(n % 10 != 5)
        return {"prompt": f"Round {n} to the nearest ten.", "answer": str(down if n - down < 10 else up),
                "chk": FN("round10", n=n),
                "steps": [f"{n} is between {down} and {up}.", "It is closer to the answer."],
                "wrong": [(str(up if n - down < 10 else down), "rounded the wrong way"),
                          (str(n), "did not round"), (str(down + 10), "rounded up too far")],
                "claim": f"{n} rounds to the nearest ten"}

    if domain == "md":
        kind = r.randrange(4)
        if kind == 0:
            d, q = r.randint(1, 6), r.randint(0, 3)
            cents = d * 10 + q * 25
            return {"prompt": f"How much money is {d} dimes and {q} quarters?", "answer": f"{cents}\u00a2",
                    "chk": FN("money_cents", cents=cents),
                    "steps": [f"{d} dimes is {d * 10}\u00a2 and {q} quarters is {q * 25}\u00a2.", f"The total is {cents}\u00a2."],
                    "wrong": [(f"{cents + 10}\u00a2", "counted a dime twice"), (f"{cents + 25}\u00a2", "counted an extra quarter"),
                              (f"{d * 10 + q}\u00a2", "counted quarters as pennies")],
                    "claim": f"{d} dimes and {q} quarters make {cents}\u00a2"}
        if kind == 1:
            h = r.randint(1, 12)
            m = r.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
            return {"prompt": "What time is shown on the clock?", "answer": f"{h}:{m:02d}",
                    "chk": FN("clock", h=h, m=m),
                    "steps": [f"The hour hand is between {h} and {(h % 12) + 1}.", f"The time is {h}:{m:02d}."],
                    "wrong": [(f"{h}:{(m + 5) % 60:02d}", "moved the minute hand too far"),
                              (f"{(h % 12) + 1}:{m:02d}", "moved the hour hand"),
                              (f"{(h % 12) + 1}:{(m + 5) % 60:02d}", "moved both hands")],
                    "claim": f"The clock shows {h}:{m:02d}"}
        if kind == 2:
            n = r.randint(3, 12)
            return {"prompt": f"An object is {n} centimeter cubes long. How many centimeters long is it?", "answer": str(n),
                    "chk": FN("count", n=n),
                    "steps": [f"Count the centimeter cubes: {n}."],
                    "wrong": [(str(n + 1), "counted one too many"), (str(n - 1 if n > 1 else n + 2), "counted one too few")],
                    "claim": f"The object is {n} centimeters long"}
        a, b = r.randint(5, 20), r.randint(5, 20)
        need(a != b)
        return {"prompt": f"One ribbon is {a} inches and another is {b} inches. How much longer is the longer ribbon?",
                "answer": str(abs(a - b)), "chk": FN("tape_diff", a=a, b=b),
                "steps": [f"Subtract the shorter length: {max(a, b)} \u2212 {min(a, b)} = {abs(a - b)}."],
                "wrong": [(str(a + b), "added the lengths"), (str(max(a, b)), "gave the longer length"),
                          (str(abs(a - b) + 1), "counted one too many")],
                "claim": f"The ribbons are {a} and {b} inches long"}

    kind = r.randrange(4)
    if kind == 0:
        sides = r.choice([3, 4, 5, 6])
        kinds = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon"}
        k = kinds[sides]
        return {"prompt": f"How many sides does a {k} have?", "answer": str(sides),
                "chk": FN("polygon_sides", kind=k),
                "steps": [f"A {k} has {sides} sides."],
                "wrong": [(str(sides + 1), "counted one side too many"), (str(sides - 1), "counted one side too few"),
                          (str(sides + 2), "counted two sides too many")],
                "claim": f"A {k} has {sides} sides"}
    if kind == 1:
        parts = r.choice([2, 3, 4])
        word = {2: "halves", 3: "thirds", 4: "fourths"}[parts]
        return {"prompt": f"A shape is cut into {parts} equal parts. What are the parts called?", "answer": word,
                "chk": FN("part_name", parts=parts),
                "steps": [f"{parts} equal parts are called {word}."],
                "wrong": [({2: "thirds", 3: "fourths", 4: "halves"}[parts], "used the wrong fraction word"),
                          ("quarters" if parts != 4 else "halves", "used another fraction word"),
                          ("eighths", "used a fraction word that does not match")],
                "claim": f"{parts} equal parts are {word}"}
    if kind == 2:
        rows, cols = r.randint(2, 5), r.randint(2, 6)
        return {"prompt": f"An array has {rows} rows and {cols} in each row. How many dots in all?", "answer": str(rows * cols),
                "chk": FN("array_total", rows=rows, cols=cols),
                "steps": [f"{rows} rows of {cols} is {rows * cols}."],
                "wrong": [(str(rows + cols), "added the rows and columns"), (str(rows * cols - rows), "left out a row"),
                          (str(rows * cols + cols), "added an extra row")],
                "claim": f"{rows} rows of {cols} is {rows * cols}"}
    n = r.randint(10, 99)
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
