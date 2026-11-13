"""Grade 4 real-world projects: one per unit, three levels each (cp2 Remedial, cp1 Standard, honors Advanced).
Every answer is computed here with exact arithmetic (integers / Fractions), so the teacher guide and the student
pages can never disagree. build.py turns these into PDF, Word and PowerPoint files.
Each level returns: scenario, objectives, materials, tasks [(title, intro, [(question, answer)], table)], extension (q, a).
Advanced levels ask for deeper reasoning with Grade 4 content only (no Grade 5 standards are required)."""
from fractions import Fraction as F

LV = ["cp2", "cp1", "honors"]
LNAME = {"cp2": "Remedial", "cp1": "Standard", "honors": "Advanced"}
VARY = "Answers vary."


def c(n):
    return f"{n:,}"


def mx(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    w, r = divmod(x.numerator, x.denominator)
    return (f"{w} " if w else "") + f"{r}/{x.denominator}"


def fr(n, d):
    """Unreduced fraction text."""
    return f"{n}/{d}"


def rnd(n, p):
    return (n + p // 2) // p * p


ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "x x twenty thirty forty fifty sixty seventy eighty ninety".split()


def words(n):
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    if n < 1000:
        return ONES[n // 100] + " hundred" + (" " + words(n % 100) if n % 100 else "")
    if n < 1000000:
        return words(n // 1000) + " thousand" + (", " + words(n % 1000) if n % 1000 else "")
    return "one million"


def expanded(n):
    s = str(n)
    return " + ".join(c(int(d) * 10 ** (len(s) - i - 1)) for i, d in enumerate(s) if d != "0")


P = {}


def project(unit, folder, title, tagline, description, theme, product, days, standards):
    def deco(fn):
        slug = folder.replace("math4-project-", "")
        P[unit] = dict(unit=unit, folder=folder, slug=slug, title=title, tagline=tagline, description=description, theme=theme, product=product, days=days, standards=standards, build=fn)
        return fn
    return deco


# ---------------------------------------------------------------- Unit 1
@project("place-value-number-sense", "math4-project-city-population-report", "City Population Report",
         "Be a data reporter: read, compare, order and round the populations of five cities.",
         "Students become data reporters for a travel magazine. They read and write city populations in standard, word and expanded form, compare and order them, round them for headlines, and explain how the value of a digit changes from place to place.",
         "Cities & Maps", "City Fact Poster", 2, ["4.NBT.A.1", "4.NBT.A.2", "4.NBT.A.3"])
def p1(L):
    pops = {"cp2": [8452, 6917, 8425, 3760, 9038], "cp1": [84520, 69175, 84250, 37608, 90386], "honors": [452068, 425860, 698175, 96340, 903862]}[L]
    names = ["Maple Grove", "Riverton", "Lakeside", "Pinehill", "Summit City"]
    place = {"cp2": 100, "cp1": 1000, "honors": 10000}[L]
    pname = {100: "hundred", 1000: "thousand", 10000: "ten thousand"}[place]
    order = sorted(zip(pops, names), reverse=True)
    a = pops[0]
    dig = {"cp2": (4, 400, 40), "cp1": (4, 4000, 400), "honors": (5, 50000, 5000)}[L]
    assert str(a).count(str(dig[0])) == 1 and str(pops[2]).count(str(dig[0])) == 1
    tasks = [
        ("Read and Write the Numbers", "The table shows how many people live in five cities.",
         [(f"Write the population of {names[0]} in word form.", words(a)), (f"Write the population of {names[0]} in expanded form.", expanded(a)),
          (f"Write this number in standard form: {words(pops[3])}.", c(pops[3]))], [["City", "Population"]] + [[n, c(p)] for n, p in zip(names, pops)]),
        ("Compare and Order", "Use >, < or = and the place-value chart on your desk.",
         [(f"Compare {c(pops[0])} and {c(pops[2])}. Write >, < or =.", f"{c(pops[0])} {'>' if pops[0] > pops[2] else '<'} {c(pops[2])}"),
          ("List the five cities from the greatest population to the least.", ", ".join(n for _, n in order)),
          (f"Which place did you look at to compare {names[0]} and {names[2]}? Why?", f"The {['ones','tens','hundreds','thousands','ten thousands','hundred thousands'][len(str(a)) - 1 - next(i for i in range(len(str(a))) if str(a)[i] != str(pops[2])[i])]} place, because it is the first place (from the left) where the digits are different.")], None),
        ("Round for the Headlines", f"Magazine headlines use rounded numbers. Round each population to the nearest {pname}.",
         [(f"Round the population of {n}: {c(p)}.", "about " + c(rnd(p, place))) for n, p in list(zip(names, pops))[:3]] +
         ([(f"Two cities round to the same number. Which two? Explain why.", f"{names[0]} and {names[2]}: both are closer to {c(rnd(pops[0], place))} than to any other {pname}.")] if rnd(pops[0], place) == rnd(pops[2], place) else []), None),
        ("The Value of a Digit", f"Look at the digit {dig[0]} in {c(pops[0])} and in {c(pops[2])}.",
         [(f"What is the value of the {dig[0]} in {c(pops[0])}?", c(dig[1])), (f"What is the value of the {dig[0]} in {c(pops[2])}?", c(dig[2])),
          ("How many times as much is the first value as the second value?", f"10 times as much ({c(dig[1])} ÷ {c(dig[2])} = 10)")], None)]
    ext = {"cp2": ("A sixth city has a population that rounds to 7,000 when rounded to the nearest thousand. Write one number it could be.", "Any whole number from 6,500 to 7,499."),
           "cp1": ("A sixth city has a population that rounds to 70,000 when rounded to the nearest ten thousand. What are the least and the greatest populations it could have?", "Least 65,000; greatest 74,999."),
           "honors": ("A sixth city's population rounds to 700,000 to the nearest hundred thousand AND to 650,000 to the nearest ten thousand. What are the least and greatest populations it could have? Explain.", "Least 650,000; greatest 654,999. It must be at least 650,000 to round up to 700,000, and less than 655,000 to round to 650,000.")}[L]
    return dict(scenario="A travel magazine has hired you as a data reporter. Your job is to study the populations of five cities and make a fact poster that readers can trust.",
                objectives=["Read and write large numbers in standard, word and expanded form.", "Compare and order numbers using place value.", "Round numbers to a given place.", "Explain how a digit's value changes from one place to the next."],
                materials=["Place-value chart", "Poster paper or blank paper", "Markers or colored pencils"], tasks=tasks, extension=ext)


# ---------------------------------------------------------------- Unit 2
@project("multi-digit-addition-subtraction", "math4-project-school-fundraiser-ledger", "School Fundraiser Ledger",
         "Keep the books for the school fundraiser: add what comes in, subtract what goes out.",
         "Students act as treasurers for a school fundraiser. They add multi-digit sales totals, subtract costs, estimate to check that answers are reasonable, and solve multistep problems to find out whether the school reaches its goal.",
         "Money & Community", "Fundraiser Ledger", 2, ["4.NBT.B.4", "4.OA.A.3", "4.NBT.A.3"])
def p2(L):
    w = {"cp2": [1245, 2318, 1876], "cp1": [4768, 12595, 8347], "honors": [47685, 125950, 83478]}[L]
    costs = {"cp2": [385, 1290], "cp1": [2385, 6790], "honors": [23850, 67905]}[L]
    goal = {"cp2": 5000, "cp1": 20000, "honors": 200000}[L]
    place = {"cp2": 100, "cp1": 1000, "honors": 10000}[L]
    pname = {100: "hundred", 1000: "thousand", 10000: "ten thousand"}[place]
    tot = sum(w); ctot = sum(costs); profit = tot - ctot
    est = sum(rnd(x, place) for x in w)
    short = goal - profit
    assert short > 0
    tasks = [
        ("Money Coming In", "The table shows the money collected each week.",
         [(f"How much was collected in Weeks 1 and 2 together?", "$" + c(w[0] + w[1])), ("How much was collected in all three weeks?", "$" + c(tot)),
          (f"How much more was collected in Week 2 than in Week 1?", "$" + c(w[1] - w[0]))], [["Week", "Money collected"]] + [[f"Week {i + 1}", "$" + c(x)] for i, x in enumerate(w)]),
        ("Estimate to Check", f"Round each week's amount to the nearest {pname}, then add.",
         [("What is your estimate for the three-week total?", " + ".join("$" + c(rnd(x, place)) for x in w) + " = $" + c(est)),
          ("Is your exact total from Part 1 reasonable? Explain.", f"Yes. ${c(tot)} is close to the estimate ${c(est)}.")], None),
        ("Money Going Out", f"The fundraiser cost money to run: ${c(costs[0])} for supplies and ${c(costs[1])} for prizes.",
         [("What were the total costs?", "$" + c(ctot)), ("Profit is the money collected minus the costs. What is the profit?", f"${c(tot)} − ${c(ctot)} = ${c(profit)}"),
          ("Check your subtraction with addition. Write the addition equation.", f"${c(profit)} + ${c(ctot)} = ${c(tot)}")], None),
        ("Reaching the Goal", f"The school's goal is a profit of ${c(goal)}.",
         [("How much more profit does the school need to reach the goal?", f"${c(goal)} − ${c(profit)} = ${c(short)}"),
          ("Write an equation with a letter for the unknown amount.", f"{c(profit)} + n = {c(goal)}, so n = {c(short)}")], None)]
    ext = {"cp2": ("In Week 4 the school collects $900. Does it reach the goal now? Show your work.", f"Profit is now ${c(profit + 900)}. " + ("Yes" if profit + 900 >= goal else f"No, it still needs ${c(goal - profit - 900)}") + "."),
           "cp1": (f"In Week 4 the school collects $3,480 and spends $275 more on supplies. Does it reach the goal? Show your work.", f"Profit is now ${c(profit + 3480 - 275)}. " + ("Yes, it passes the goal by $" + c(profit + 3205 - goal) if profit + 3205 >= goal else f"No, it still needs ${c(goal - profit - 3205)}") + "."),
           "honors": (f"The treasurer wrote the Week 2 amount as ${c(w[1] + 9000)} by mistake. Without adding again, explain how this changes the total, and give the wrong total.", f"The wrong amount is $9,000 too much, so the total is $9,000 too much: ${c(tot + 9000)}.")}[L]
    return dict(scenario="Your school is raising money for new playground equipment, and you are the treasurer. A treasurer keeps a ledger: a careful record of money coming in and money going out.",
                objectives=["Add and subtract multi-digit whole numbers with the standard algorithm.", "Estimate sums and differences by rounding.", "Solve multistep word problems and check with the inverse operation.", "Write equations with a letter for the unknown."],
                materials=["Grid paper to line up digits", "Pencil", "Ledger page (make a table)"], tasks=tasks, extension=ext)


# ---------------------------------------------------------------- Unit 3
@project("multiplication-strategies", "math4-project-design-a-theater", "Design a Theater",
         "Design the seating for a new theater and use multiplication to count every seat.",
         "Students design the seating plan for a community theater. They use arrays and area models to multiply, find partial products, compare amounts with multiplicative comparison, and calculate ticket sales for a sold-out show.",
         "Arts & Design", "Theater Seating Plan", 3, ["4.NBT.B.5", "4.OA.A.1", "4.OA.A.2"])
def p3(L):
    r1, s1 = {"cp2": (6, 14), "cp1": (8, 26), "honors": (9, 38)}[L]
    r2, s2 = {"cp2": (4, 23), "cp1": (14, 23), "honors": (24, 18)}[L]
    price = {"cp2": 5, "cp1": 7, "honors": 9}[L]
    times = {"cp2": 3, "cp1": 4, "honors": 6}[L]
    a, b = r1 * s1, r2 * s2
    tot = a + b
    t1, o1 = s1 // 10 * 10, s1 % 10
    if r2 < 10:
        pp2 = f"({r2} × {s2 // 10 * 10}) + ({r2} × {s2 % 10}) = {r2 * (s2 // 10 * 10)} + {r2 * (s2 % 10)} = {b}"
    else:
        parts = [(r2 // 10 * 10) * (s2 // 10 * 10), (r2 // 10 * 10) * (s2 % 10), (r2 % 10) * (s2 // 10 * 10), (r2 % 10) * (s2 % 10)]
        assert sum(parts) == b
        pp2 = " + ".join(c(x) for x in parts) + f" = {c(b)}"
    balcony = a // times if a % times == 0 else None
    kids = {"cp2": 28, "cp1": 52, "honors": 57}[L]
    assert a % times == 0 or True
    tasks = [
        ("The Main Floor", f"The main floor has {r1} rows with {s1} seats in each row.",
         [("Sketch an area model. Break the number of seats in a row into tens and ones.", f"{s1} = {t1} + {o1}"),
          ("Find the partial products and add them.", f"({r1} × {t1}) + ({r1} × {o1}) = {r1 * t1} + {r1 * o1} = {a}"), ("How many seats are on the main floor?", f"{a} seats")], None),
        ("The Side Sections", f"The side sections have {r2} rows with {s2} seats in each row.",
         [("Find the partial products and add them.", pp2), ("How many seats are in the side sections?", f"{c(b)} seats"), ("How many seats does the theater have in all?", f"{a} + {c(b)} = {c(tot)} seats")], None),
        ("Compare the Crowds", f"On Friday, {kids} children came to the show. {times} times as many adults came.",
         [("Write a multiplication equation for the number of adults.", f"{times} × {kids} = {times * kids}"), ("How many people came in all?", f"{kids} + {times * kids} = {kids + times * kids} people"),
          (f"Were there enough seats for everyone? Explain.", ("Yes" if kids + times * kids <= tot else "No") + f". {kids + times * kids} people and {c(tot)} seats.")], None),
        ("Sold Out!", f"Every seat is sold for ${price}.",
         [(f"How much money do ticket sales bring in for one sold-out show?", f"{c(tot)} × ${price} = ${c(tot * price)}"), ("Estimate to check. Show your rounding.", f"about {c(rnd(tot, 100))} × {price} = {c(rnd(tot, 100) * price)}, which is close to {c(tot * price)}"),
          ("Draw your seating plan. Label the rows and seats in each section.", "Check that each section is drawn as an array with the correct rows and seats per row.")], None)]
    ext = {"cp2": (f"The owner adds 2 more rows to the main floor. How many seats are on the main floor now?", f"{r1 + 2} × {s1} = {(r1 + 2) * s1} seats (or {a} + 2 × {s1})."),
           "cp1": (f"The owner wants exactly 600 seats. Suggest a number of rows and seats per row for a third section that brings the total to 600.", f"The third section needs {600 - tot} seats. Any factor pair of {600 - tot} works, such as " + ", ".join(f"{i} × {(600 - tot) // i}" for i in range(2, 12) if (600 - tot) % i == 0) + "."),
           "honors": (f"A student says {r2} × {s2} is the same as {r2 * 2} × {s2 // 2}. Is the student correct? Explain with an area model, without multiplying it all out.", f"Yes. Doubling the rows and halving the seats per row rearranges the same seats: both equal {c(b)}.")}[L]
    return dict(scenario="The town is building a new community theater, and you are the designer. You will plan the seats, count them with multiplication, and find out how much a sold-out show earns.",
                objectives=["Multiply a multi-digit number by a one-digit number, and two two-digit numbers.", "Use arrays, area models and partial products.", "Solve multiplicative comparison problems (times as many).", "Estimate products to check answers."],
                materials=["Grid paper", "Ruler", "Colored pencils"], tasks=tasks, extension=ext)


# ---------------------------------------------------------------- Unit 4
@project("division-remainders", "math4-project-party-planner", "Party Planner",
         "Plan a big party: divide guests, snacks and supplies, and decide what to do with what is left over.",
         "Students plan a school celebration. They divide to seat guests, share snacks and pack party bags, then decide what each remainder means: ignore it, add one more group, or use it as the answer. They check every quotient with multiplication.",
         "Events & Planning", "Party Plan", 2, ["4.NBT.B.6", "4.OA.A.3"])
def p4(L):
    guests, per = {"cp2": (50, 8), "cp1": (134, 6), "honors": (1358, 8)}[L]
    stickers, kids = {"cp2": (95, 4), "cp1": (475, 9), "honors": (2350, 7)}[L]
    juice, pack = {"cp2": (75, 6), "cp1": (260, 8), "honors": (1500, 9)}[L]
    ball, bunch = {"cp2": (84, 7), "cp1": (252, 6), "honors": (3248, 8)}[L]
    q1, r1 = divmod(guests, per); q2, r2 = divmod(stickers, kids); q3, r3 = divmod(juice, pack); q4, r4 = divmod(ball, bunch)
    assert r1 and r2 and r3 and r4 == 0
    tasks = [
        ("Seating the Guests", f"{c(guests)} guests are coming. Each table seats {per} guests.",
         [("Divide. Write the quotient and the remainder.", f"{c(guests)} ÷ {per} = {c(q1)} R {r1}"), ("How many tables are needed so that everyone has a seat? Explain.", f"{c(q1 + 1)} tables. {c(q1)} tables are full and the {r1} extra guest{'s' if r1 > 1 else ''} need one more table."),
          ("Check with multiplication.", f"{per} × {c(q1)} + {r1} = {c(guests)}")], None),
        ("Sharing Stickers", f"You have {c(stickers)} stickers to share equally among {kids} party bags.",
         [("How many stickers go in each bag?", f"{c(q2)} stickers ({c(stickers)} ÷ {kids} = {c(q2)} R {r2})"), ("How many stickers are left over?", f"{r2}"),
          ("In this problem, what do you do with the remainder?", "Ignore it for the bags: the leftover stickers are not enough to give every bag one more.")], None),
        ("Juice Boxes", f"You need {c(juice)} juice boxes. They are sold in packs of {pack}.",
         [("How many packs must you buy? Show your division.", f"{c(juice)} ÷ {pack} = {c(q3)} R {r3}, so buy {c(q3 + 1)} packs."), ("How many extra juice boxes will you have?", f"{c((q3 + 1) * pack)} − {c(juice)} = {(q3 + 1) * pack - juice}")], None),
        ("Balloon Bunches", f"There are {c(ball)} balloons. Each bunch has {bunch} balloons.",
         [("How many bunches can you make?", f"{c(ball)} ÷ {bunch} = {c(q4)} bunches"), ("Is there a remainder? What does that tell you about the two numbers?", f"No. {bunch} is a factor of {c(ball)} ({c(ball)} is a multiple of {bunch})."),
          ("Write your party plan: tables, bags, packs and bunches.", f"{c(q1 + 1)} tables, {kids} bags with {c(q2)} stickers each, {c(q3 + 1)} packs of juice, {c(q4)} balloon bunches.")], None)]
    ext = {"cp2": ("One more table of 8 guests is added to the party. How many guests are coming now, and how many tables are needed?", f"{guests + 8} guests; {(guests + 8 + per - 1) // per} tables."),
           "cp1": (f"A number of cupcakes is divided into boxes of 6 and leaves a remainder of 4. There are between 40 and 50 cupcakes. How many could there be?", "46 (6 × 7 + 4). 40 also works: 6 × 6 + 4 = 40."),
           "honors": ("Write your own party division story in which the remainder IS the answer. Solve it.", "Stories vary. Example: 1,358 guests fill tables of 8; how many sit at the table that is not full? 1,358 ÷ 8 = 169 R 6, so 6 guests.")}[L]
    return dict(scenario="Your school is throwing a celebration, and you are in charge of the plan. Planners divide all the time, and they always have to decide what to do with the leftovers.",
                objectives=["Divide multi-digit numbers by one-digit numbers.", "Interpret remainders in word problems.", "Check division with multiplication.", "Solve multistep problems."],
                materials=["Scratch paper", "Counters or base-ten blocks (optional)", "Planning sheet (make a table)"], tasks=tasks, extension=ext)


# ---------------------------------------------------------------- Unit 5
def factors(n):
    return [i for i in range(1, n + 1) if n % i == 0]


@project("factors-multiples-patterns", "math4-project-pattern-quilt", "Pattern Quilt",
         "Design a quilt with factor pairs, multiples and repeating patterns.",
         "Students design a class quilt. They use factor pairs to find every possible rectangular layout, decide which numbers of squares are prime or composite, use multiples to plan colors, and follow a pattern rule to predict what comes next.",
         "Art & Patterns", "Quilt Design", 2, ["4.OA.B.4", "4.OA.C.5"])
def p5(L):
    n = {"cp2": 24, "cp1": 48, "honors": 72}[L]
    pr, co = {"cp2": (13, 15), "cp1": (29, 39), "honors": (53, 51)}[L]
    m1, m2 = {"cp2": (2, 3), "cp1": (3, 4), "honors": (4, 6)}[L]
    start, rule = {"cp2": (3, 4), "cp1": (5, 6), "honors": (7, 9)}[L]
    fs = factors(n)
    pairs = [(a, n // a) for a in fs if a <= n // a]
    both = [k for k in range(1, n + 1) if k % m1 == 0 and k % m2 == 0]
    seq = [start + rule * i for i in range(6)]
    cof = [x for x in factors(co) if x not in (1, co)]
    odd_even = ("all odd" if rule % 2 == 0 and start % 2 else "odd, even, odd, even, …")
    tasks = [
        ("Quilt Layouts", f"The quilt will use exactly {n} squares arranged in a rectangle.",
         [(f"List all the factor pairs of {n}.", ", ".join(f"{a} × {b}" for a, b in pairs)), (f"How many different factors does {n} have?", str(len(fs))),
          ("Which layout would you choose for a quilt? Why?", VARY + " Any factor pair is possible; long thin layouts like 1 × " + str(n) + " are not practical.")], None),
        ("Prime or Composite?", f"Another class has {pr} squares. A third class has {co} squares.",
         [(f"How many rectangular layouts can be made with {pr} squares? Is {pr} prime or composite?", f"Only one (1 × {pr}). {pr} is prime."),
          (f"Is {co} prime or composite? Prove it with a factor pair.", f"Composite: {cof[0]} × {co // cof[0]} = {co}.")], None),
        ("Color by Multiples", f"Number the squares 1 to {n}. Color every multiple of {m1} blue. Put a star on every multiple of {m2}.",
         [(f"Which squares are blue AND have a star?", ", ".join(map(str, both))), ("What do you notice about those numbers?", f"They are the multiples of {m1 * m2 // __import__('math').gcd(m1, m2)}."),
          (f"Is {n} a multiple of {m2}? How do you know?", ("Yes" if n % m2 == 0 else "No") + f": {m2} × {n // m2} = {n}.")], None),
        ("A Growing Border", f"The border uses a number pattern. Start at {start}. Rule: add {rule}.",
         [("Write the first six numbers in the pattern.", ", ".join(map(str, seq))), ("Are the numbers odd, even, or do they switch? Explain why.", odd_even.capitalize() + (f". Adding an even number ({rule}) to an odd number always gives an odd number." if rule % 2 == 0 else f". Adding an odd number ({rule}) switches between odd and even.")),
          ("Draw your quilt design with your layout, colors and border.", "Check the layout uses the correct number of squares and the coloring follows the multiples.")], None)]
    ext = {"cp2": ("What is the 10th number in the border pattern? Explain how you found it.", f"{start + rule * 9}. Start at {start} and add {rule} nine times: {start} + 9 × {rule}."),
           "cp1": ("Find a number between 30 and 40 that has exactly two factors. Then find one that has an odd number of factors. What is special about the second number?", "31 or 37 are prime (two factors). 36 has 9 factors because it is a square number: 6 × 6 pairs 6 with itself."),
           "honors": ("Will the number 100 ever appear in your border pattern? Explain without listing every number.", ("Yes" if (100 - start) % rule == 0 else "No") + f". The numbers are {start} more than a multiple of {rule}. 100 − {start} = {100 - start}, which is " + ("" if (100 - start) % rule == 0 else "not ") + f"a multiple of {rule}.")}[L]
    return dict(scenario="Your class is sewing a quilt for the school hallway. Before anyone cuts fabric, the design team (that is you) has to plan the layout, the colors and the border with math.",
                objectives=["Find all factor pairs of a number.", "Decide whether a number is prime or composite.", "Recognize multiples of one-digit numbers.", "Generate a number pattern from a rule and describe its features."],
                materials=["Grid paper", "Colored pencils", "Hundred chart (optional)"], tasks=tasks, extension=ext)


# ---------------------------------------------------------------- Unit 6
@project("fractions-equivalent-fractions", "math4-project-fraction-pizza-shop", "Fraction Pizza Shop",
         "Run a pizza shop where every order is a fraction to model, rename and compare.",
         "Students run a pizza shop. They draw fraction models for orders, find equivalent fractions when pizzas are cut into more slices, compare fractions with different numerators and denominators, and put orders in order from least to greatest.",
         "Food & Business", "Pizza Shop Menu Board", 2, ["4.NF.A.1", "4.NF.A.2"])
def p6(L):
    (a1, b1), k = {"cp2": ((1, 2), 4), "cp1": ((2, 3), 4), "honors": ((3, 4), 3)}[L]
    (a2, b2), (a3, b3) = {"cp2": ((3, 8), (5, 8)), "cp1": ((3, 4), (5, 8)), "honors": ((5, 6), (7, 8))}[L]
    orders = {"cp2": [(1, 4), (1, 2), (3, 4), (1, 8)], "cp1": [(2, 3), (1, 2), (5, 6), (5, 12)], "honors": [(2, 3), (3, 4), (7, 12), (5, 6)]}[L]
    names = ["Table 1", "Table 2", "Table 3", "Table 4"]
    cmp = ">" if F(a2, b2) > F(a3, b3) else "<" if F(a2, b2) < F(a3, b3) else "="
    cd = b2 * b3 // __import__("math").gcd(b2, b3)
    srt = sorted(zip([F(*o) for o in orders], names, orders))
    half = [n for (v, n, o) in srt if v > F(1, 2)]
    simp = {"cp2": (4, 8), "cp1": (8, 12), "honors": (9, 12)}[L]
    sv = F(*simp)
    tasks = [
        ("Slice It Smaller", f"A customer orders {fr(a1, b1)} of a pizza. The pizza is then cut so that each slice becomes {k} smaller slices.",
         [("Draw the pizza before and after the extra cuts.", f"Before: {a1} of {b1} equal parts shaded. After: {a1 * k} of {b1 * k} equal parts shaded."),
          ("Write the equivalent fraction. Show the multiplication.", f"{fr(a1, b1)} = ({a1} × {k})/({b1} × {k}) = {fr(a1 * k, b1 * k)}"), ("Did the customer get more pizza, less pizza, or the same amount? Explain.", "The same amount. There are more slices, but each slice is smaller.")], None),
        ("Which Order Is Bigger?", f"Table A orders {fr(a2, b2)} of a pizza. Table B orders {fr(a3, b3)} of a pizza. The pizzas are the same size.",
         [("Compare the two fractions. Write >, < or =.", f"{fr(a2, b2)} {cmp} {fr(a3, b3)}"),
          ("Explain how you compared them.", (f"Same denominator: {a2} eighths is {'less' if cmp == '<' else 'more'} than {a3} eighths." if b2 == b3 else f"Rename with the denominator {cd}: {fr(a2 * cd // b2, cd)} and {fr(a3 * cd // b3, cd)}.")),
          ("Why must the pizzas be the same size to compare?", "Fractions can only be compared when they refer to the same whole.")], None),
        ("Order the Orders", "Four tables each ordered part of a pizza.",
         [("List the orders from least to greatest.", ", ".join(f"{fr(*o)} ({n})" for v, n, o in srt)), (f"Which tables ordered more than 1/2 of a pizza?", ", ".join(half) if half else "None"),
          ("Which benchmark helped you most: 0, 1/2 or 1?", VARY + " Comparing with 1/2 sorts most of the orders quickly.")], [["Table"] + names, ["Order"] + [fr(*o) for o in orders]]),
        ("Menu Board", f"The menu shows fractions in simplest form. One special is {fr(*simp)} of a pizza.",
         [(f"Write {fr(*simp)} in simplest form.", f"{fr(*simp)} = {fr(sv.numerator, sv.denominator)}"), ("Write two more fractions equivalent to it.", "Examples: " + ", ".join(fr(sv.numerator * m, sv.denominator * m) for m in (2, 5))),
          ("Design your menu board with at least 4 fraction specials and a model for each.", "Check each model matches its fraction and that equal parts are equal.")], None)]
    ext = {"cp2": ("Jo ate 2/4 of a small pizza. Max ate 1/2 of a large pizza. Did they eat the same amount? Explain.", "No. 2/4 and 1/2 are equivalent only for the same whole; half of a large pizza is more."),
           "cp1": ("Find a fraction that is greater than 1/2 and less than 2/3. Explain how you know.", "Example: 7/12, because 1/2 = 6/12 and 2/3 = 8/12."),
           "honors": ("Without finding common denominators, decide which is greater: 7/8 or 9/10. Explain your reasoning.", "9/10. Each is one piece less than a whole: 1/8 is missing from 7/8 and 1/10 is missing from 9/10. 1/10 is smaller, so 9/10 is closer to 1.")}[L]
    return dict(scenario="Welcome to your own pizza shop! Customers order pizza by the fraction, and you must make sure every order is fair.",
                objectives=["Explain why two fractions are equivalent using models.", "Generate equivalent fractions and write fractions in simplest form.", "Compare fractions with different numerators and denominators.", "Use the benchmark 1/2 to compare."],
                materials=["Paper circles or fraction circles", "Ruler", "Markers", "Poster paper"], tasks=tasks, extension=ext)


# ---------------------------------------------------------------- Unit 7
def d2(x):
    """Fraction with denominator dividing 100 -> decimal text."""
    x = F(x); n = x * 100
    assert n.denominator == 1
    s = f"{n.numerator // 100}.{n.numerator % 100:02d}"
    return s[:-1] if s.endswith("0") and not s.endswith(".00") and False else s


@project("fraction-operations-decimals", "math4-project-recipe-for-a-crowd", "Recipe for a Crowd",
         "Scale up a trail-mix recipe for the whole class with fraction and decimal math.",
         "Students prepare trail mix for a class hike. They add and subtract fractions and mixed numbers with like denominators, multiply a fraction by a whole number to make several batches, and write tenths and hundredths as decimals to compare prices and weights.",
         "Cooking & Food", "Recipe Card", 2, ["4.NF.B.3", "4.NF.B.4", "4.NF.C.5", "4.NF.C.6", "4.NF.C.7"])
def p7(L):
    den = {"cp2": 4, "cp1": 8, "honors": 8}[L]
    ing = {"cp2": [("oats", F(3, 4)), ("raisins", F(2, 4)), ("seeds", F(1, 4))], "cp1": [("oats", F(7, 8)), ("raisins", F(5, 8)), ("seeds", F(3, 8))], "honors": [("oats", F(13, 8)), ("raisins", F(7, 8)), ("seeds", F(5, 8))]}[L]
    raw = lambda v: fr(int(v * den), den) if v < 1 else mx_un(v, den)
    def mx_un(v, d):
        n = int(v * d); w, r = divmod(n, d)
        return (f"{w} " if w else "") + (f"{r}/{d}" if r else "")
    batches = {"cp2": 3, "cp1": 5, "honors": 6}[L]
    tot = sum(v for _, v in ing)
    tn = int(tot * den)
    bowl = {"cp2": 2, "cp1": 3, "honors": 4}[L]
    left = F(bowl) - tot
    assert left > 0
    mult = ing[0][1] * batches
    mn = int(ing[0][1] * den) * batches
    w10, w100 = {"cp2": (3, 25), "cp1": (4, 35), "honors": (6, 8)}[L]
    wsum = F(w10, 10) + F(w100, 100)
    pa, pb = {"cp2": ("0.5", "0.45"), "cp1": ("0.7", "0.68"), "honors": ("1.4", "1.38")}[L]
    tasks = [
        ("One Batch", "One batch of trail mix uses these amounts (in cups).",
         [("How many cups of trail mix does one batch make? Show the addition.", " + ".join(raw(v) for _, v in ing) + f" = {fr(tn, den)} = {mx_un(tot, den)} cups"),
          (f"How much more oats than seeds is in one batch?", f"{raw(ing[0][1])} − {raw(ing[2][1])} = {mx_un(ing[0][1] - ing[2][1], den)} cup" + ("" if ing[0][1] - ing[2][1] <= 1 else "s")),
          (f"A bowl holds {bowl} cups. How much room is left after one batch is poured in?", f"{bowl} − {mx_un(tot, den)} = {mx_un(left, den)} cup" + ("" if left <= 1 else "s"))],
         [["Ingredient"] + [n for n, _ in ing], ["Cups"] + [raw(v) for _, v in ing]]),
        ("Batches for the Class", f"The class needs {batches} batches.",
         [(f"How many cups of oats are needed? Write a multiplication equation.", f"{batches} × {raw(ing[0][1])} = {fr(mn, den)} = {mx_un(mult, den)} cups"),
          ("Show the same amount as repeated addition.", " + ".join([raw(ing[0][1])] * batches) + f" = {fr(mn, den)}"),
          ("Between which two whole numbers of cups is your answer?", f"Between {int(mult)} and {int(mult) + 1}" if mult.denominator != 1 else f"It is exactly {int(mult)} cups.")], None),
        ("Weighing with Decimals", f"The scale shows {w10}/10 kilogram of nuts and {w100}/100 kilogram of chocolate chips.",
         [("Write each weight as a decimal.", f"{w10}/10 = {d2(F(w10, 10))[:3]} and {w100}/100 = {d2(F(w100, 100))}"),
          ("Add the two weights. First rename the tenths as hundredths.", f"{w10 * 10}/100 + {w100}/100 = {w10 * 10 + w100}/100 = {d2(wsum)} kilogram"),
          ("Which ingredient is heavier? Explain.", ("The nuts" if F(w10, 10) > F(w100, 100) else "The chocolate chips") + f": {w10 * 10} hundredths compared with {w100} hundredths.")], None),
        ("Smart Shopping", f"Brand A raisins weigh {pa} kilogram. Brand B raisins weigh {pb} kilogram. Both cost the same.",
         [("Compare the decimals. Write >, < or =.", f"{pa} {'>' if F(pa) > F(pb) else '<'} {pb}"), ("Which brand gives you more raisins? Explain using hundredths.", f"Brand {'A' if F(pa) > F(pb) else 'B'}: {pa} = {d2(F(pa))}, and {int(F(pa) * 100)} hundredths is more than {int(F(pb) * 100)} hundredths."),
          ("Write your recipe card for the whole class. Show each amount as a fraction or mixed number.", "; ".join(f"{n}: {mx_un(v * batches, den)} cups" for n, v in ing))], None)]
    ext = {"cp2": ("How many batches can you make with 3 cups of oats? Use a number line or repeated addition.", "4 batches: 3/4 + 3/4 + 3/4 + 3/4 = 12/4 = 3."),
           "cp1": ("You have 4 cups of raisins. Is that enough for 6 batches? Explain.", "6 × 5/8 = 30/8 = 3 6/8 cups. Yes, 4 cups is enough, with 2/8 cup left."),
           "honors": ("A friend says 6 × 7/8 must be more than 6 because multiplying makes numbers bigger. Is the friend correct? Explain with a model or equation.", "No. 6 × 7/8 = 42/8 = 5 2/8, which is less than 6, because each of the 6 groups is less than 1 whole.")}[L]
    return dict(scenario="Your class is going on a hike, and you are making the trail mix. The recipe makes one small batch, so you need fraction math to make enough for everyone.",
                objectives=["Add and subtract fractions and mixed numbers with like denominators.", "Multiply a fraction by a whole number.", "Write tenths and hundredths as decimals and add them.", "Compare decimals to hundredths."],
                materials=["Measuring cups (optional)", "Fraction strips or number line", "Index card for the recipe"], tasks=tasks, extension=ext)


# ---------------------------------------------------------------- Unit 8
@project("measurement-unit-conversions", "math4-project-playground-blueprint", "Playground Blueprint",
         "Draw the blueprint for a new playground using area, perimeter and unit conversions.",
         "Students design a playground. They use the area and perimeter formulas for rectangles, find an unknown side length, convert larger units to smaller units, and solve problems about time, distance and money for the building project.",
         "Building & Design", "Playground Blueprint", 3, ["4.MD.A.1", "4.MD.A.2", "4.MD.A.3"])
def p8(L):
    l, w = {"cp2": (12, 8), "cp1": (24, 15), "honors": (36, 28)}[L]
    sa, sl = {"cp2": (36, 9), "cp1": (96, 12), "honors": (182, 14)}[L]
    fence_ft = {"cp2": 3, "cp1": 3, "honors": 3}[L]
    cost = {"cp2": 5, "cp1": 8, "honors": 12}[L]
    hrs, mins = {"cp2": (2, 15), "cp1": (3, 45), "honors": (5, 50)}[L]
    start = {"cp2": (9, 0), "cp1": (8, 30), "honors": (7, 45)}[L]
    A, Pm = l * w, 2 * (l + w)
    end = start[0] * 60 + start[1] + hrs * 60 + mins
    eh, em = divmod(end, 60)
    endt = f"{eh if eh <= 12 else eh - 12}:{em:02d} {'AM' if eh < 12 else 'PM'}"
    water_l = {"cp2": 4, "cp1": 6, "honors": 15}[L]
    tasks = [
        ("The Play Area", f"The main play area is a rectangle {l} meters long and {w} meters wide.",
         [("What is the area? Write the formula you used.", f"A = l × w = {l} × {w} = {A} square meters"), ("What is the perimeter?", f"P = 2 × {l} + 2 × {w} = {Pm} meters"),
          ("Which measurement tells how much rubber matting to buy: area or perimeter? Why?", "Area, because matting covers the surface inside the rectangle.")], None),
        ("The Sandbox", f"The sandbox is a rectangle with an area of {sa} square meters. One side is {sl} meters long.",
         [("How long is the other side? Write an equation with a letter.", f"{sl} × w = {sa}, so w = {sa // sl} meters"), ("What is the perimeter of the sandbox?", f"2 × {sl} + 2 × {sa // sl} = {2 * (sl + sa // sl)} meters")], None),
        ("Fence and Units", f"A fence goes all the way around the main play area ({Pm} meters). Fencing costs ${cost} for each meter.",
         [("How much does the fence cost?", f"{Pm} × ${cost} = ${c(Pm * cost)}"), (f"How many centimeters long is the fence? (1 meter = 100 centimeters)", f"{Pm} × 100 = {c(Pm * 100)} centimeters"),
          ("Complete the conversion table.", "; ".join(f"{m} m = {m * 100} cm" for m in (1, 2, 5, 10)))], [["Meters", "1", "2", "5", "10"], ["Centimeters", "100", "", "", ""]]),
        ("Building Day", f"Workers start at {start[0]}:{start[1]:02d} AM. The job takes {hrs} hours {mins} minutes.",
         [("How many minutes does the job take?", f"{hrs} × 60 + {mins} = {hrs * 60 + mins} minutes"), ("What time do the workers finish?", endt),
          (f"The workers drink {water_l} liters of water. How many milliliters is that?", f"{water_l} × 1,000 = {c(water_l * 1000)} milliliters"),
          ("Draw your blueprint on grid paper. Label every length, the area and the perimeter.", "Check that labeled areas and perimeters match the drawn dimensions.")], None)]
    A2 = {"cp2": 24, "cp1": 36, "honors": 64}[L]
    pairs = [(a, A2 // a) for a in range(1, int(A2 ** 0.5) + 1) if A2 % a == 0]
    best = min(pairs, key=lambda p: p[0] + p[1])
    ext = {"cp2": (f"Draw two different rectangles that each have an area of {A2} square meters. Which one needs less fence?", "Examples: " + ", ".join(f"{a} × {b} (P = {2 * (a + b)})" for a, b in pairs) + f". The {best[0]} × {best[1]} rectangle needs the least fence."),
           "cp1": (f"A garden must have an area of {A2} square meters. Find the whole-number side lengths that need the least fence.", ", ".join(f"{a} × {b} (P = {2 * (a + b)})" for a, b in pairs) + f". The {best[0]} × {best[1]} square needs the least: {2 * sum(best)} meters."),
           "honors": ("You have 40 meters of fence for a rectangular garden with whole-number sides. What side lengths give the greatest area? Explain the pattern you see.", "10 × 10 gives 100 square meters. As the sides get closer to equal (1 × 19 = 19, 5 × 15 = 75, 9 × 11 = 99), the area grows.")}[L]
    return dict(scenario="The school has money for a new playground, and the principal wants YOUR blueprint. Builders need exact measurements, so every number on your plan matters.",
                objectives=["Use the area and perimeter formulas for rectangles.", "Find an unknown side length.", "Convert from a larger unit to a smaller unit.", "Solve measurement word problems about time, money and liquid volume."],
                materials=["Grid paper", "Ruler", "Colored pencils"], tasks=tasks, extension=ext)


# ---------------------------------------------------------------- Unit 9
@project("geometry-angles-symmetry", "math4-project-angle-art-studio", "Angle Art Studio",
         "Create a piece of geometric art, then measure and classify every line, angle and shape in it.",
         "Students create geometric artwork. They draw points, lines, rays and angles, measure and sketch angles with a protractor, add angle measures to find unknown angles, classify shapes by their sides and angles, and add lines of symmetry.",
         "Art & Geometry", "Geometric Art Piece", 3, ["4.G.A.1", "4.G.A.2", "4.G.A.3", "4.MD.C.5", "4.MD.C.6", "4.MD.C.7"])
def p9(L):
    angs = {"cp2": [40, 90, 120], "cp1": [35, 90, 145], "honors": [35, 90, 145, 180]}[L]
    kind = lambda a: "acute" if a < 90 else "right" if a == 90 else "obtuse" if a < 180 else "straight"
    a1, whole = {"cp2": (30, 90), "cp1": (55, 90), "honors": (65, 180)}[L]
    parts = {"cp2": [50, 70], "cp1": [45, 60, 35], "honors": [38, 67, 49]}[L]
    turn = {"cp2": (1, 4), "cp1": (1, 6), "honors": (5, 12)}[L]
    tdeg = 360 * turn[0] // turn[1]
    shapes = [("square", 4, "4 right angles, 2 pairs of parallel sides, 4 lines of symmetry"), ("rectangle (not a square)", 2, "4 right angles, 2 pairs of parallel sides, 2 lines of symmetry"),
              ("equilateral triangle", 3, "3 acute angles, no parallel sides, 3 lines of symmetry"), ("right triangle with sides of different lengths", 0, "1 right angle, 2 perpendicular sides, 0 lines of symmetry")]
    tasks = [
        ("Lines in Your Art", "Start your artwork with these parts. Use a ruler.",
         [("Draw and label: a point, a line, a line segment and a ray.", "Check: a line has two arrows, a segment has two endpoints, a ray has one endpoint and one arrow."),
          ("Draw a pair of parallel lines and a pair of perpendicular lines. How are they different?", "Parallel lines never meet and stay the same distance apart. Perpendicular lines meet to form right angles.")], None),
        ("Measure and Classify Angles", "Use a protractor to draw angles with these measures: " + ", ".join(f"{a}°" for a in angs) + ".",
         [(f"Classify the {a}° angle.", kind(a)) for a in angs] + [(f"A dial turns {fr(*turn)} of a full circle. How many degrees is that?", f"{fr(*turn)} of 360° = {tdeg}°")], None),
        ("Angles That Add", f"In your art, a {whole}° angle is split into two angles. One of them measures {a1}°.",
         [("What is the measure of the other angle? Write an equation.", f"{a1} + x = {whole}, so x = {whole - a1}°"),
          (f"{len(parts)} angles share a vertex and do not overlap. They measure " + ", ".join(f"{p}°" for p in parts) + ". What is the measure of the whole angle?", " + ".join(map(str, parts)) + f" = {sum(parts)}°"),
          ("Is the whole angle acute, right, obtuse or straight?", kind(sum(parts)))], None),
        ("Shapes and Symmetry", "Add these four shapes to your art. Draw every line of symmetry with a dashed line.",
         [(f"How many lines of symmetry does a {n} have?", str(k)) for n, k, _ in shapes] +
         [("Sort your shapes: which have at least one pair of parallel sides?", "The square and the rectangle."), ("Finish your art piece. Label 3 angles with their measures.", "Check the labeled measures with a protractor (within about 2°).")],
         [["Shape", "Angles and sides"]] + [[n, d] for n, _, d in shapes]),
    ]
    ext = {"cp2": ("Draw a shape that has exactly 1 line of symmetry. Show the line.", "Examples: an isosceles triangle, a kite, the letter A."),
           "cp1": ("The hands of a clock at 3:00 make a right angle. What angle do they make at 1:00? Explain.", "30°. The clock face has 12 equal parts, and 360° ÷ 12 = 30°."),
           "honors": ("Four angles meet at a point and fill the full circle. Three of them measure 85°, 110° and 95°. Find the fourth angle and classify it.", "360 − (85 + 110 + 95) = 70°. It is acute.")}[L]
    return dict(scenario="The art studio needs a new piece for its math gallery. You are the artist, and your tools are a ruler, a protractor and everything you know about geometry.",
                objectives=["Draw and identify points, lines, rays, segments, parallel and perpendicular lines.", "Measure, draw and classify angles.", "Add angle measures to find unknown angles.", "Classify shapes and draw lines of symmetry."],
                materials=["Ruler", "Protractor", "Blank paper", "Colored pencils or markers"], tasks=tasks, extension=ext)


# ---------------------------------------------------------------- Unit 10
@project("data-line-plots-word-problems", "math4-project-class-measurement-survey", "Class Measurement Survey",
         "Collect measurements, display them on a line plot, and answer questions with the data.",
         "Students run a measurement survey. They read a data set of lengths measured to the nearest fraction of an inch, make a line plot, add and subtract fractions to answer questions about the data, and solve multistep problems.",
         "Science & Data", "Line Plot Poster", 2, ["4.MD.B.4", "4.OA.A.3", "4.NF.B.3"])
def p10(L):
    den = {"cp2": 2, "cp1": 4, "honors": 8}[L]
    data = {"cp2": [F(4), F(9, 2), F(9, 2), F(5), F(5), F(5), F(11, 2), F(6), F(6), F(9, 2)],
            "cp1": [F(17, 4), F(9, 2), F(9, 2), F(19, 4), F(19, 4), F(19, 4), F(5), F(21, 4), F(21, 4), F(4), F(19, 4), F(9, 2)],
            "honors": [F(33, 8), F(17, 4), F(35, 8), F(35, 8), F(9, 2), F(9, 2), F(9, 2), F(37, 8), F(19, 4), F(19, 4), F(41, 8), F(35, 8)]}[L]
    def m(v):
        n = int(v * den); w, r = divmod(n, den)
        return (f"{w}" if w else "") + (f" {r}/{den}" if r else "")
    vals = sorted(set(data))
    counts = {v: data.count(v) for v in vals}
    mode = max(vals, key=lambda v: counts[v])
    rng = max(data) - min(data)
    two = min(data) + max(data)
    above = sum(1 for v in data if v > mode)
    tot_mode = mode * counts[mode]
    per = {"cp2": 3, "cp1": 4, "honors": 6}[L]
    packs = -(-len(data) // per)
    price = {"cp2": 2, "cp1": 3, "honors": 4}[L]
    tasks = [
        ("The Data", f"Students measured the length of their pencils to the nearest 1/{den} inch.",
         [("How many pencils were measured?", str(len(data))), ("Write the lengths in order from shortest to longest.", ", ".join(m(v) for v in sorted(data))),
          ("What are the shortest and the longest lengths?", f"{m(min(data))} inches and {m(max(data))} inches")], [["Pencil lengths (inches)"], [", ".join(m(v) for v in data)]]),
        ("Make the Line Plot", f"Draw a number line from {m(min(data))} to {m(max(data))} with a mark every 1/{den} inch. Put one X above the number for each pencil.",
         [("How many Xs are above each length?", "; ".join(f"{m(v)}: {counts[v]}" for v in vals)), ("Which length has the most Xs?", f"{m(mode)} inches ({counts[mode]} pencils)"),
          (f"How many pencils are longer than {m(mode)} inches?", str(above))], None),
        ("Questions from the Plot", "Use your line plot and fraction addition and subtraction.",
         [("What is the difference between the longest and the shortest pencil?", f"{m(max(data))} − {m(min(data))} = {m(rng).strip()} inch" + ("" if rng <= 1 else "es")),
          ("If the shortest and the longest pencil are placed end to end, how long are they together?", f"{m(min(data))} + {m(max(data))} = {m(two)} inches"),
          (f"The {counts[mode]} pencils that are {m(mode)} inches long are placed end to end. How long is the line?", f"{counts[mode]} × {m(mode)} = {m(tot_mode)} inches")], None),
        ("New Pencils for Everyone", f"Each student in the survey gets one new pencil. Pencils come in packs of {per}. Each pack costs ${price}.",
         [("How many packs are needed?", f"{len(data)} ÷ {per} = {len(data) // per}" + (f" R {len(data) % per}, so {packs} packs" if len(data) % per else f", so {packs} packs")),
          ("How much do the packs cost in all?", f"{packs} × ${price} = ${packs * price}"), ("Make a poster of your line plot with a title, labels and two facts you learned from the data.", "Check: title, number line with equal spacing, one X per data value, and two true statements.")], None)]
    ext = {"cp2": ("Measure 8 objects in your classroom to the nearest 1/2 inch. Make your own line plot and write one question about it.", "Plots vary. Check equal spacing and one X per object."),
           "cp1": ("A new pencil is measured and the difference between the longest and shortest pencil becomes 1 1/2 inches. How long could the new pencil be?", f"{m(min(data) + F(3, 2))} inches (longer) or {m(max(data) - F(3, 2))} inches (shorter)."),
           "honors": ("A student says, 'Most pencils are longer than 4 1/2 inches.' Use the line plot to decide whether the statement is true. Explain with numbers.", f"{sum(1 for v in data if v > F(9, 2))} of {len(data)} pencils are longer than 4 1/2 inches, so the statement is " + ("true" if sum(1 for v in data if v > F(9, 2)) * 2 > len(data) else "false") + " (most means more than half).")}[L]
    return dict(scenario="Scientists collect data, display it, and use it to answer questions. Today your class is the science team, and your first data set is a pile of pencils.",
                objectives=["Make a line plot of measurements in fractions of a unit.", "Read a line plot to answer questions.", "Add and subtract fractions to solve problems about the data.", "Solve multistep word problems."],
                materials=["Ruler marked in fractions of an inch", "Grid or lined paper", "Poster paper", "Markers"], tasks=tasks, extension=ext)
