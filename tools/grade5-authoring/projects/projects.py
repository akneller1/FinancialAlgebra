"""Grade 5 real-world projects: one per unit, three levels each (cp2 Remedial, cp1 Standard, honors Advanced).
Every answer is computed here with exact arithmetic (Fractions / integer cents), so the teacher guide and the
student pages can never disagree. build.py turns these into PDF, Word and PowerPoint files.
Each level returns: scenario, objectives, skills, materials, tasks [(title, intro, [(question, answer)], table)], extension (q, a)."""
from fractions import Fraction as F
import math

LV = ["cp2", "cp1", "honors"]
LNAME = {"cp2": "Remedial", "cp1": "Standard", "honors": "Advanced"}


def mx(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    w, r = divmod(x.numerator, x.denominator)
    return (f"{w} " if w else "") + f"{r}/{x.denominator}"


def money(c):
    """c in cents (int)."""
    return f"${c // 100:,}.{c % 100:02d}"


def dec(x, places=None):
    x = F(x)
    s = f"{float(x):.{places}f}" if places is not None else (f"{float(x):.3f}".rstrip("0").rstrip("."))
    return s


P = {}


def project(unit, folder, slug, title, tagline, description, theme, product, days, standards):
    def deco(fn):
        P[unit] = dict(unit=unit, folder=folder, slug=slug, title=title, tagline=tagline, description=description, theme=theme, product=product, days=days, standards=standards, build=fn)
        return fn
    return deco


# ---------------------------------------------------------------- Unit 1
@project("place-value-number-sense", "math5-project-sports-stats-showdown", "sports-stats-showdown", "Sports Stats Showdown",
         "Be the official statistician for Field Day: read, compare, order and round decimal results.",
         "Students become the Field Day statisticians. They read and write decimal race times and jump distances, compare and order them to award medals, round results for the scoreboard, and use powers of 10 to scale ticket and snack sales.",
         "Sports & Field Day", "Field Day Results Board", 2, ["5.NBT.A.1", "5.NBT.A.2", "5.NBT.A.3", "5.NBT.A.4"])
def p1(L):
    times = {"cp2": ["14.6", "13.9", "14.2", "15.1"], "cp1": ["13.58", "13.85", "13.5", "14.06"], "honors": ["13.508", "13.58", "13.085", "13.805"]}[L]
    names = ["Ava", "Ben", "Carmen", "Dev"]
    vals = [F(t) for t in times]
    order = [n for _, n in sorted(zip(vals, names))]
    jumps = {"cp2": "3.47", "cp1": "4.385", "honors": "4.385"}[L]
    jv = F(jumps)
    r_tenth = math.floor(jv * 10 + F(1, 2)) / F(10)
    r_hund = math.floor(jv * 100 + F(1, 2)) / F(100)
    tickets = {"cp2": (4, 10), "cp1": (3.75, 100), "honors": (2.45, 1000)}[L]
    tv = F(str(tickets[0])) * tickets[1]
    exp = {"cp2": 2, "cp1": 3, "honors": 4}[L]
    tasks = [
        ("Race Times", "The 50-meter dash times (in seconds) are: " + ", ".join(f"{n} {t}" for n, t in zip(names, times)) + ". The fastest time is the least number.",
         [("Write the times in order from fastest to slowest (by name).", ", ".join(order)), ("Who wins the gold medal?", order[0]),
          (f"Write {times[0]} in word form.", None), (f"Write {times[0]} in expanded form.", None)], [["Runner", "Time (s)"]] + [[n, t] for n, t in zip(names, times)]),
        ("Long Jump Scoreboard", f"The winning long jump was {jumps} meters. The scoreboard can only show some digits.",
         [(f"Round {jumps} m to the nearest tenth.", dec(r_tenth, 1) + " m"), (f"Round {jumps} m to the nearest hundredth.", dec(r_hund, 2) + " m"),
          (f"What is the value of the digit 8 in {jumps}?" if "8" in jumps else f"What is the value of the digit 4 in {jumps}?", ("0.08" if jumps == "4.385" else "0.4") if "8" in jumps or True else "")], None),
        ("Powers of 10 at the Snack Stand", f"One bag of popcorn costs ${dec(F(str(tickets[0])), 2)}.",
         [(f"How much do {tickets[1]:,} bags cost?", money(int(tv * 100))), (f"Write {tickets[1]:,} as a power of 10.", f"10{'²' if tickets[1] == 100 else '³' if tickets[1] == 1000 else '¹'}"),
          (f"A banner is 10{chr(0x00B2) if exp == 2 else chr(0x00B3) if exp == 3 else chr(0x2074)} centimeters long. How many centimeters is that?", f"{10 ** exp:,} cm")], None),
        ("Results Board", "Design a results board for Field Day. Show the medal winners for the dash and the jump, with times and distances written in standard form and in word form.",
         [("Include at least 4 decimals, each written two ways.", "Answers vary; check that standard and word forms match.")], None)]
    # fill word/expanded forms
    from_words = {"14.6": ("fourteen and six tenths", "1 × 10 + 4 × 1 + 6 × 1/10"), "13.58": ("thirteen and fifty-eight hundredths", "1 × 10 + 3 × 1 + 5 × 1/10 + 8 × 1/100"),
                  "13.508": ("thirteen and five hundred eight thousandths", "1 × 10 + 3 × 1 + 5 × 1/10 + 8 × 1/1000")}
    w, e = from_words[times[0]]
    tasks[0][2][2] = (tasks[0][2][2][0], w)
    tasks[0][2][3] = (tasks[0][2][3][0], e)
    if jumps == "3.47":
        tasks[1][2][2] = ("What is the value of the digit 4 in 3.47?", "0.4")
    return dict(scenario="Our school is holding Field Day, and you are the official statistician! Every result is a decimal, and the medals depend on reading them correctly.",
                objectives=["Read and write decimals in standard, word and expanded form", "Compare and order decimals to thousandths", "Round decimals to a given place", "Use powers of 10 and exponents"],
                materials=["Pencil", "Colored pencils or markers", "Poster paper (optional)"], tasks=tasks,
                extension=("Two runners' times differ by only 0.01 second. Write two possible times between 13.5 and 13.6 seconds that are 0.01 apart and explain who wins.", "Example: 13.54 and 13.55; the runner with 13.54 wins because it is less."))


# ---------------------------------------------------------------- Unit 2
@project("multi-digit-multiplication-division", "math5-project-school-carnival-planner", "school-carnival-planner", "School Carnival Planner",
         "Plan the school carnival: tickets, prizes, tables and buses, all with multi-digit math.",
         "Students plan a school carnival. They multiply to find ticket and prize totals, divide to share supplies and arrange buses and tables, interpret remainders, and estimate to check that the plan makes sense.",
         "Events & Planning", "Carnival Plan", 2, ["5.NBT.B.5", "5.NBT.B.6"])
def p2(L):
    kids = {"cp2": 168, "cp1": 1248, "honors": 2735}[L]
    per_bus = {"cp2": 24, "cp1": 52, "honors": 48}[L]
    q, r = divmod(kids, per_bus)
    buses = q + (1 if r else 0)
    tix = {"cp2": (36, 12), "cp1": (248, 35), "honors": (1265, 48)}[L]
    prizes = {"cp2": (144, 12), "cp1": (2340, 18), "honors": (4836, 26)}[L]
    pq, pr = divmod(*prizes)
    est = (round(tix[0], -1 if tix[0] < 100 else -2), round(tix[1], -1))
    tasks = [
        ("Getting Everyone There", f"{kids:,} students are coming. Each bus holds {per_bus} students.",
         [("How many buses are needed?", f"{buses} buses"), ("Write the division and explain the remainder.", f"{kids:,} ÷ {per_bus} = {q} R{r}" + (f"; the {r} extra students need one more bus." if r else "; no extra bus is needed."))], None),
        ("Ticket Sales", f"The class sells {tix[0]:,} ticket books. Each book has {tix[1]} tickets.",
         [("Estimate the total number of tickets.", f"about {est[0] * est[1]:,}"), ("Find the exact total.", f"{tix[0] * tix[1]:,} tickets"), ("Is your answer reasonable? Explain.", "Yes, it is close to the estimate.")], None),
        ("Prize Bags", f"There are {prizes[0]:,} small prizes to put into bags of {prizes[1]}.",
         [("How many full prize bags can be made?", f"{pq} bags"), ("How many prizes are left over?", f"{pr} prizes")], None),
        ("Carnival Plan", "Make a one-page plan that shows your buses, tickets and prize bags with the math for each.", [("Show an area model or partial products for one multiplication.", "Answers vary.")], None)]
    return dict(scenario="The whole school is going to the spring carnival, and your class is in charge of planning. You need to make sure there are enough buses, tickets and prizes!",
                objectives=["Multiply multi-digit whole numbers", "Divide by two-digit divisors", "Interpret remainders in context", "Estimate to check reasonableness"],
                materials=["Pencil", "Grid paper for area models (optional)"], tasks=tasks,
                extension=("Buses cost $185 each for the day. What is the total bus cost? If the cost is shared by all students, about how much is that per student?", f"${buses * 185:,}; about ${round(buses * 185 / kids, 2):.2f} per student"))


# ---------------------------------------------------------------- Unit 3
@project("decimal-operations", "math5-project-class-party-budget", "class-party-budget", "Class Party Budget",
         "Plan an end-of-year class party without going over budget.",
         "Students plan an end-of-year class party. They add the costs of decorations and food, multiply decimal prices by quantities, divide to find the cost per student and the better buy, and subtract to stay within the budget.",
         "Money & Shopping", "Party Shopping List", 2, ["5.NBT.B.7"])
def p3(L):
    budget = {"cp2": 5000, "cp1": 7500, "honors": 12000}[L]
    items = {"cp2": [("Balloons", 450, 2), ("Juice box pack", 625, 3), ("Paper plates", 389, 1), ("Snack mix", 799, 2)],
             "cp1": [("Balloons", 475, 3), ("Juice box pack", 649, 4), ("Paper plates", 389, 2), ("Pizza", 1150, 3)],
             "honors": [("Balloons", 475, 4), ("Juice box pack", 649, 5), ("Paper plates", 389, 3), ("Pizza", 1275, 5)]}[L]
    lines = [(n, c, q, c * q) for n, c, q in items]
    total = sum(x[3] for x in lines)
    students = {"cp2": 20, "cp1": 25, "honors": 28}[L]
    left = budget - total
    per = F(total, 100 * students)
    a_ct, a_price = (6, 450) if L != "honors" else (8, 576)
    b_ct, b_price = (10, 690) if L != "honors" else (12, 828)
    ua, ub = F(a_price, a_ct * 100), F(b_price, b_ct * 100)
    tasks = [
        ("Shopping List", f"Your budget is {money(budget)}. Find the cost of each item and the total.",
         [(f"Cost of {q} × {n} at {money(c)} each", money(t)) for n, c, q, t in lines] + [("Total cost", money(total))], [["Item", "Price", "Quantity", "Cost"]] + [[n, money(c), str(q), ""] for n, c, q, t in lines]),
        ("Stay on Budget", "", [("How much money is left (or how much over budget)?", (money(left) + " left") if left >= 0 else (money(-left) + " over"))], None),
        ("Cost per Student", f"There are {students} students.", [("What is the cost per student? Round to the nearest cent.", money(int(per * 100 + F(1, 2))))], None),
        ("Better Buy", f"Pack A: {a_ct} cookies for {money(a_price)}. Pack B: {b_ct} cookies for {money(b_price)}.",
         [("Find the price of one cookie in each pack.", f"A: ${dec(ua, 2) if (ua * 100).denominator == 1 else dec(ua)}; B: ${dec(ub, 2) if (ub * 100).denominator == 1 else dec(ub)}"), ("Which pack is the better buy?", "Pack A" if ua < ub else "Pack B")], None)]
    return dict(scenario="It's the end of the school year and your class is throwing a party! You are the party planner with a set budget.",
                objectives=["Add and subtract decimals to hundredths", "Multiply decimals by whole numbers", "Divide decimals", "Make budget decisions"],
                materials=["Pencil", "Calculator for checking only (optional)"], tasks=tasks,
                extension=("Choose one item to change so the party stays under budget and costs as close to the budget as possible. Show your new total.", "Answers vary; check the new total is at most the budget."))


# ---------------------------------------------------------------- Unit 4
@project("numerical-expressions-patterns", "math5-project-theme-park-points", "theme-park-points", "Theme Park Points",
         "Use expressions and patterns to plan the best day at a theme park.",
         "Students plan a theme park day. They write and evaluate expressions with grouping symbols for ride points and costs, interpret expressions without calculating, generate two numerical patterns for two savings plans, and graph the ordered pairs to compare them.",
         "Travel & Fun", "Theme Park Day Plan", 2, ["5.OA.A.1", "5.OA.A.2", "5.OA.B.3"])
def p4(L):
    a, b, c = {"cp2": (3, 5, 2), "cp1": (4, 6, 3), "honors": (6, 8, 5)}[L]
    e1 = f"{c} × ({a} + {b})"
    v1 = c * (a + b)
    e2 = f"[{a} × {b} + {c}] × 2" if L != "cp2" else f"{a} × {b} + {c}"
    v2 = (a * b + c) * 2 if L != "cp2" else a * b + c
    s1, s2 = {"cp2": (2, 4), "cp1": (3, 6), "honors": (4, 12)}[L]
    weeks = 5
    A = [s1 * i for i in range(weeks + 1)]
    B = [s2 * i for i in range(weeks + 1)]
    ratio = s2 // s1
    tasks = [
        ("Ride Points", f"The Roller Coaster earns {a} points and the Water Slide earns {b} points. You ride both, {c} times each.",
         [("Write an expression for your total points.", e1), ("Evaluate it.", str(v1))], None),
        ("Bonus Points", f"Evaluate the bonus expression: {e2}", [("Value:", str(v2))], None),
        ("Without Calculating", f"How does {c} × (1,248 + 367) compare with 1,248 + 367?", [("Answer:", f"It is {c} times as large.")], None),
        ("Two Savings Plans", f"Plan A: start at $0 and save ${s1} each week. Plan B: start at $0 and save ${s2} each week.",
         [("List the first 6 terms of each plan.", "A: " + ", ".join(map(str, A)) + "; B: " + ", ".join(map(str, B))), ("Write the ordered pairs (Plan A, Plan B).", ", ".join(f"({x}, {y})" for x, y in zip(A, B))),
          ("How does each Plan B amount compare with Plan A?", f"Each Plan B amount is {ratio} times the Plan A amount.")], [["Week", "Plan A ($)", "Plan B ($)"]] + [[str(i), "", ""] for i in range(weeks + 1)]),
        ("Graph It", "Graph the ordered pairs on a coordinate grid. Label the axes Plan A and Plan B.", [("What do you notice about the points?", "They line up in a straight path from (0, 0).")], None)]
    return dict(scenario="Your class won a trip to Pi Peaks Theme Park! You need to plan your rides and save money for the trip.",
                objectives=["Write and evaluate expressions with grouping symbols", "Interpret expressions without calculating", "Generate two numerical patterns and compare terms", "Graph ordered pairs from patterns"],
                materials=["Pencil", "Coordinate grid paper", "Colored pencils"], tasks=tasks,
                extension=("Plan C starts at $10 and saves $" + str(s1) + " each week. After how many weeks does Plan B have more than Plan C?", f"Week {next(i for i in range(1, 50) if s2 * i > 10 + s1 * i)}"))


# ---------------------------------------------------------------- Unit 5
@project("fraction-addition-subtraction", "math5-project-school-garden-plan", "school-garden-plan", "School Garden Plan",
         "Design a school garden where every fraction adds up.",
         "Students design a school garden. They split a garden into fractional sections with unlike denominators, check that the sections make one whole, add and subtract mixed numbers for fence and path lengths, and use benchmark fractions to check that answers are reasonable.",
         "Nature & Gardening", "Garden Design Map", 2, ["5.NF.A.1", "5.NF.A.2"])
def p5(L):
    parts = {"cp2": [F(1, 2), F(1, 4), F(1, 8)], "cp1": [F(1, 3), F(1, 4), F(1, 6)], "honors": [F(2, 5), F(1, 4), F(1, 6)]}[L]
    names = ["Tomatoes", "Beans", "Flowers"]
    used = sum(parts)
    rest = 1 - used
    f1, f2 = {"cp2": (F(9, 2), F(13, 4)), "cp1": (F(17, 3), F(19, 4)), "honors": (F(38, 5), F(37, 6))}[L]
    path_total, cut = {"cp2": (F(6), F(9, 4)), "cp1": (F(25, 2), F(23, 6)), "honors": (F(47, 4), F(55, 12))}[L]
    tasks = [
        ("Garden Sections", "The garden is one whole. " + ", ".join(f"{n}: {mx(p)}" for n, p in zip(names, parts)) + ".",
         [("What fraction of the garden is planted?", mx(used)), ("What fraction is left for a bench area?", mx(rest)), ("Use a benchmark to check: is the planted part more or less than 1/2?", "more" if used > F(1, 2) else "less")], None),
        ("Fence Lengths", f"The garden needs two fence pieces: {mx(f1)} yards and {mx(f2)} yards.", [("How many yards of fence in all?", mx(f1 + f2) + " yards"), ("How much longer is the first piece?", mx(abs(f1 - f2)) + " yards")], None),
        ("Stepping-Stone Path", f"You have {mx(path_total)} feet of stepping stones. You use {mx(cut)} feet for the first path.", [("How many feet are left?", mx(path_total - cut) + " feet")], None),
        ("Garden Map", "Draw your garden as a rectangle cut into sections. Label each section with its fraction and plant.", [("Do all your sections add to 1 whole?", "Answers vary; sections must add to 1.")], None)]
    return dict(scenario="Our school is building a new garden, and your team gets to design it! Every section of the garden is a fraction of the whole.",
                objectives=["Add and subtract fractions with unlike denominators", "Add and subtract mixed numbers", "Use benchmark fractions to estimate and check"],
                materials=["Pencil", "Colored pencils", "Grid paper"], tasks=tasks,
                extension=("Change two section sizes so the planted part is exactly 5/6 of the garden. Show the math.", "Answers vary; the three sections must add to 5/6."))


# ---------------------------------------------------------------- Unit 6
@project("fraction-multiplication-division", "math5-project-recipe-remix", "recipe-remix", "Recipe Remix",
         "Scale a recipe up and down and share it fairly using fraction multiplication and division.",
         "Students run a cooking club. They scale a recipe by whole numbers, fractions and mixed numbers, explain scaling, interpret fractions as division when sharing, and divide whole numbers by unit fractions to find servings.",
         "Food & Cooking", "Recipe Card Set", 2, ["5.NF.B.3", "5.NF.B.4", "5.NF.B.5", "5.NF.B.6", "5.NF.B.7"])
def p6(L):
    rec = {"cp2": [("flour", F(2), "cups"), ("sugar", F(1, 2), "cup"), ("milk", F(3, 4), "cup")], "cp1": [("flour", F(9, 4), "cups"), ("sugar", F(2, 3), "cup"), ("milk", F(3, 4), "cup")],
           "honors": [("flour", F(9, 4), "cups"), ("sugar", F(2, 3), "cup"), ("milk", F(5, 4), "cups")]}[L]
    k = {"cp2": F(3), "cp1": F(3, 2), "honors": F(5, 2)}[L]
    half = F(1, 2)
    share_n, share_d = {"cp2": (3, 4), "cp1": (5, 4), "honors": (7, 3)}[L]
    whole, unit = {"cp2": (3, 4), "cp1": (4, 3), "honors": (6, 8)}[L]
    tasks = [
        ("Make More", f"Multiply each ingredient by {mx(k)}.", [(f"{n}: {mx(q)} × {mx(k)}", mx(q * k) + " " + ("cups" if q * k > 1 else "cup")) for n, q, u in rec], [["Ingredient", "Original", "× " + mx(k)]] + [[n, mx(q) + " " + u, ""] for n, q, u in rec]),
        ("Make Less", "Make half of the recipe.", [(f"{n}: {mx(q)} × 1/2", mx(q * half) + " " + ("cups" if q * half > 1 else "cup")) for n, q, u in rec[:2]] + [("Is half a recipe more or less than the original? Why?", "Less, because multiplying by 1/2 (less than 1) makes each amount smaller.")], None),
        ("Fair Shares", f"{share_n} pans of cornbread are shared equally by {share_d} friends.", [("How much does each friend get?", mx(F(share_n, share_d)) + " pan" + ("s" if share_n > share_d else "")), ("Between which two whole numbers is that?", f"{share_n // share_d} and {share_n // share_d + 1}")], None),
        ("Servings", f"You have {whole} cups of trail mix. Each serving is 1/{unit} cup.", [("How many servings can you make?", f"{whole * unit} servings"), ("Check with multiplication.", f"{whole * unit} × 1/{unit} = {whole}")], None)]
    return dict(scenario="Welcome to the Cooking Club! Today you will change a recipe to feed different numbers of people and share food fairly.",
                objectives=["Multiply fractions and mixed numbers", "Explain multiplication as scaling", "Interpret fractions as division", "Divide whole numbers by unit fractions"],
                materials=["Pencil", "Recipe card template", "Measuring cups (optional)"], tasks=tasks,
                extension=("Write your own recipe with 4 ingredients and scale it by 2 1/2. Show each product.", "Answers vary; check each product."))


# ---------------------------------------------------------------- Unit 7
@project("measurement-conversions", "math5-project-field-trip-packing", "field-trip-packing", "Field Trip Packing List",
         "Pack for an outdoor field trip by converting units of length, weight and capacity.",
         "Students pack for a nature field trip. They convert gallons of water to cups, feet of rope to inches, pounds to ounces for backpack weight, and metric distances, solving multi-step problems with regrouping.",
         "Outdoors & Science", "Packing Plan", 2, ["5.MD.A.1"])
def p7(L):
    gal = {"cp2": 2, "cp1": 3, "honors": 5}[L]
    students = {"cp2": 16, "cp1": 22, "honors": 30}[L]
    cups = gal * 16
    rope_ft, piece_in = {"cp2": (6, 8), "cp1": (15, 9), "honors": (25, 14)}[L]
    pieces, left = divmod(rope_ft * 12, piece_in)
    items = {"cp2": [(3, 4), (1, 8)], "cp1": [(4, 10), (2, 9), (1, 7)], "honors": [(5, 12), (3, 9), (2, 14)]}[L]
    oz = sum(lb * 16 + o for lb, o in items)
    km = {"cp2": F(2), "cp1": F(5, 2), "honors": F(37, 10)}[L]
    tasks = [
        ("Water Station", f"The class brings {gal} gallons of water. 1 gallon = 16 cups.", [("How many cups of water is that?", f"{cups} cups"), (f"Is that enough for {students} students to get 2 cups each?", "Yes" if cups >= 2 * students else f"No, they need {2 * students - cups} more cups")], None),
        ("Rope for the Tent", f"You have {rope_ft} feet of rope and cut it into {piece_in}-inch pieces.", [("How many inches of rope is that?", f"{rope_ft * 12} inches"), ("How many full pieces?", f"{pieces} pieces"), ("How many inches are left over?", f"{left} inches")], None),
        ("Backpack Weight", "The backpack holds: " + ", ".join(f"{lb} lb {o} oz" for lb, o in items) + ".", [("What is the total weight in pounds and ounces?", f"{oz // 16} lb {oz % 16} oz"), ("What is the total in ounces?", f"{oz} oz")], None),
        ("Trail Distance", f"The nature trail is {dec(km)} kilometers long.", [("How many meters is that?", f"{int(km * 1000):,} m")], None)]
    return dict(scenario="Your class is going on an all-day nature field trip! You are in charge of packing water, rope and supplies, and everything has to be measured.",
                objectives=["Convert customary units of length, weight and capacity", "Convert metric units", "Solve multi-step measurement problems"],
                materials=["Pencil", "Conversion chart", "Ruler (optional)"], tasks=tasks,
                extension=("The packing rule says a backpack can weigh at most 10 lb (160 oz). Is this backpack under the limit? By how many ounces is it under or over?",
                           (f"Under the limit by {160 - oz} oz" if oz < 160 else f"Over the limit by {oz - 160} oz" if oz > 160 else "Exactly at the limit")))


# ---------------------------------------------------------------- Unit 8
@project("volume-three-dimensional-figures", "math5-project-miniature-city-builder", "miniature-city-builder", "Miniature City Builder",
         "Design a miniature city of buildings and find the volume of every one.",
         "Students design a miniature city. They build rectangular-prism buildings from unit cubes, find volumes with V = l × w × h and V = B × h, find volumes of L-shaped (composite) buildings, and plan how many boxes fit in a delivery truck.",
         "Design & Engineering", "City Blueprint", 3, ["5.MD.C.3", "5.MD.C.4", "5.MD.C.5"])
def p8(L):
    bld = {"cp2": [("House", 3, 2, 2), ("Shop", 4, 3, 2), ("Library", 5, 3, 3)], "cp1": [("House", 4, 3, 3), ("Shop", 6, 4, 3), ("Library", 7, 5, 4)], "honors": [("House", 5, 4, 3), ("Shop", 8, 5, 4), ("Library", 9, 6, 5)]}[L]
    B, h = {"cp2": (12, 4), "cp1": (24, 6), "honors": (45, 8)}[L]
    a, b = {"cp2": ((4, 2, 3), (2, 2, 5)), "cp1": ((6, 3, 4), (3, 3, 8)), "honors": ((8, 4, 5), (4, 4, 10))}[L]
    va, vb = a[0] * a[1] * a[2], b[0] * b[1] * b[2]
    truck, box = {"cp2": ((6, 4, 4), (2, 2, 2)), "cp1": ((10, 6, 6), (2, 3, 2)), "honors": ((12, 8, 6), (3, 2, 2))}[L]
    nbox = (truck[0] // box[0]) * (truck[1] // box[1]) * (truck[2] // box[2])
    tasks = [
        ("Buildings", "Find the volume of each building in cubic units.", [(f"{n}: {l} × {w} × {hh}", f"{l * w * hh} cubic units") for n, l, w, hh in bld], [["Building", "l", "w", "h", "Volume"]] + [[n, str(l), str(w), str(hh), ""] for n, l, w, hh in bld]),
        ("Tower", f"The tower's base has an area of {B} square units and it is {h} units tall.", [("Use V = B × h to find its volume.", f"{B * h} cubic units")], None),
        ("L-Shaped Mall", f"The mall is two prisms: {a[0]} × {a[1]} × {a[2]} and {b[0]} × {b[1]} × {b[2]}.", [("Find the volume of each part.", f"{va} and {vb} cubic units"), ("Find the total volume.", f"{va + vb} cubic units")], None),
        ("Delivery Truck", f"A truck is {truck[0]} × {truck[1]} × {truck[2]} units. Boxes are {box[0]} × {box[1]} × {box[2]} units, packed the same direction.", [("How many boxes fit?", f"{nbox} boxes")], None),
        ("Your Blueprint", "Design one more building of your own with a volume between 50 and 100 cubic units.", [("Give its dimensions and volume.", "Answers vary.")], None)]
    return dict(scenario="The town council wants a model of a new miniature city! You are the architect. Every building is a rectangular prism, and the council needs to know its volume.",
                objectives=["Find volume by counting unit cubes", "Use V = l × w × h and V = B × h", "Find volumes of composite figures", "Solve real-world volume problems"],
                materials=["Pencil", "Unit cubes or grid paper", "Boxes or paper for models (optional)"], tasks=tasks,
                extension=("Design two different buildings with exactly the same volume, 72 cubic units. Give the dimensions of each.", "Examples: 6 × 4 × 3 and 9 × 4 × 2"))


# ---------------------------------------------------------------- Unit 9
@project("coordinate-plane-graphing", "math5-project-playground-designer", "playground-designer", "Playground Designer",
         "Place playground equipment on a coordinate grid and measure paths and fences.",
         "Students design a playground on a coordinate grid. They plot equipment at ordered pairs, find distances along grid lines, find the fourth corner and perimeter of rectangular areas, and interpret a graph of visitors over time.",
         "Design & Community", "Playground Map", 2, ["5.G.A.1", "5.G.A.2"])
def p9(L):
    pts = {"cp2": {"Swings": (2, 3), "Slide": (6, 3), "Sandbox": (6, 7)}, "cp1": {"Swings": (2, 4), "Slide": (9, 4), "Sandbox": (9, 10)}, "honors": {"Swings": (3, 2), "Slide": (11, 2), "Sandbox": (11, 9)}}[L]
    s, sl, sb = pts["Swings"], pts["Slide"], pts["Sandbox"]
    fourth = (s[0], sb[1])
    w_, h_ = sl[0] - s[0], sb[1] - sl[1]
    per_visit = {"cp2": 3, "cp1": 5, "honors": 7}[L]
    tasks = [
        ("Plot the Equipment", ", ".join(f"{k} at ({x}, {y})" for k, (x, y) in pts.items()) + ".", [("Plot and label each point. How far is the Swings from the Slide?", f"{w_} units"), ("How far is the Slide from the Sandbox?", f"{h_} units")], None),
        ("Fence the Play Area", "The Swings, Slide and Sandbox are three corners of a rectangle.", [("Where is the fourth corner?", f"({fourth[0]}, {fourth[1]})"), ("What is the perimeter of the fence?", f"{2 * (w_ + h_)} units"), ("What is the area inside?", f"{w_ * h_} square units")], None),
        ("Visitors", f"Each hour, {per_visit} more families visit. Make ordered pairs (hours, families) for 0 to 4 hours.", [("List the ordered pairs.", ", ".join(f"({i}, {per_visit * i})" for i in range(5))), ("What does the point (3, " + str(3 * per_visit) + ") mean?", f"After 3 hours, {3 * per_visit} families have visited.")], None),
        ("Your Design", "Add two more pieces of equipment to your map. Give their coordinates and the distance between them along a grid line.", [("Coordinates and distance:", "Answers vary.")], None)]
    return dict(scenario="The town is building a new playground, and you are the designer! Everything must be placed on the town's coordinate grid.",
                objectives=["Plot and read ordered pairs in the first quadrant", "Find distances along grid lines", "Solve problems with figures on the grid", "Interpret coordinates in context"],
                materials=["Pencil", "Coordinate grid paper", "Colored pencils"], tasks=tasks,
                extension=("A water fountain should be exactly halfway between the Swings and the Slide. Where should it go?", f"({(s[0] + sl[0]) / 2:g}, {s[1]})"))


# ---------------------------------------------------------------- Unit 10
@project("classifying-two-dimensional-figures", "math5-project-shape-mosaic-designer", "shape-mosaic-designer", "Shape Mosaic Designer",
         "Create a mosaic and prove what every shape in it is.",
         "Students design a mosaic for the school entrance. They classify triangles by sides and angles, classify quadrilaterals by their properties, use the shape hierarchy to explain how shapes are related, and describe regular polygons.",
         "Art & Design", "Mosaic with Shape Key", 2, ["5.G.B.3", "5.G.B.4"])
def p10(L):
    tri = [("Triangle A", "all three sides 5 cm; angles 60°, 60°, 60°", "equilateral acute"), ("Triangle B", "exactly two sides equal; angles 70°, 70°, 40°", "isosceles acute"),
           ("Triangle C", "no sides equal; angles 90°, 40°, 50°", "scalene right"), ("Triangle D", "exactly two sides equal; angles 30°, 30°, 120°", "isosceles obtuse")]
    if L == "cp2":
        tri = tri[:3]
    quads = [("Tile 1", "4 equal sides, 4 right angles", "square"), ("Tile 2", "2 pairs of parallel sides, 4 right angles, sides 6 and 3", "rectangle"), ("Tile 3", "4 equal sides, no right angles", "rhombus"), ("Tile 4", "exactly 1 pair of parallel sides", "trapezoid")]
    tasks = [
        ("Triangle Tiles", "Classify each triangle by its sides AND its angles.", [(f"{n}: {d}", ans) for n, d, ans in tri], None),
        ("Four-Sided Tiles", "Give the most specific name for each tile.", [(f"{n}: {d}", ans) for n, d, ans in quads], None),
        ("Family Tree", "Use the shape hierarchy.", [("Is every square a rectangle? Explain.", "Yes. A square has 4 right angles and 2 pairs of parallel sides."), ("Is every rectangle a square? Explain.", "No. A rectangle's sides do not all have to be equal.")] + ([("Name every category a square belongs to.", "square, rectangle, rhombus, parallelogram, trapezoid (inclusive), quadrilateral, polygon")] if L != "cp2" else []), None),
        ("Mosaic Design", "Design a mosaic using at least 6 different shapes. Make a key that names each shape and one property.", [("Shape key:", "Answers vary; names must match properties.")], None)]
    return dict(scenario="The art teacher needs a mosaic for the school entrance, and your team is the design studio! Every tile must be named correctly.",
                objectives=["Classify triangles by sides and angles", "Classify quadrilaterals by properties", "Explain the shape hierarchy", "Identify regular polygons"],
                materials=["Pencil", "Ruler", "Colored paper or pencils"], tasks=tasks,
                extension=("A regular hexagon has a perimeter of 42 cm. How long is each side? Is a regular hexagon's angle acute or obtuse?", "7 cm; obtuse (120°)"))


# ---------------------------------------------------------------- Unit 11
@project("data-line-plots-problem-solving", "math5-project-plant-growth-investigation", "plant-growth-investigation", "Plant Growth Investigation",
         "Measure seedlings, make a line plot, and answer questions about the data.",
         "Students run a plant-growth investigation. They organize fraction measurements of seedlings in a line plot, find totals and differences, find an equal (fair) share of water, and solve a multi-step problem with the data.",
         "Science & Data", "Investigation Report", 2, ["5.MD.B.2", "5.NF.A.2", "5.NF.B.6"])
def p11(L):
    data = {"cp2": ["1/2", "1", "1/2", "1 1/2", "1", "1/2", "1"], "cp1": ["1 1/4", "1 1/2", "1 1/4", "2", "1 3/4", "1 1/4", "1 1/2", "1 3/4"],
            "honors": ["1 3/8", "1 1/2", "1 3/8", "2 1/8", "1 3/4", "1 3/8", "1 5/8", "1 3/4", "2 1/8", "1 1/2"]}[L]
    def P(s):
        return F(int(s.split()[0])) + F(s.split()[1]) if " " in s else F(s)
    vals = [P(s) for s in data]
    cnt = {}
    for v in vals:
        cnt[v] = cnt.get(v, 0) + 1
    mode = max(cnt, key=lambda k: cnt[k])
    tot = sum(vals)
    water = {"cp2": ["1/2", "1/4", "3/4", "1/2"], "cp1": ["3/4", "1/2", "1/4", "1/2", "1"], "honors": ["3/4", "5/8", "1/4", "1/2", "7/8", "1"]}[L]
    wv = [F(w) for w in water]
    share = sum(wv) / len(wv)
    tasks = [
        ("Make a Line Plot", "Seedling heights (inches): " + ", ".join(data) + ".", [("Which height appears most often?", mx(mode) + " in."), ("How many seedlings were measured?", str(len(vals)))], [["Height (in.)", "Number of seedlings"]] + [[mx(k), ""] for k in sorted(cnt)]),
        ("Compare Heights", "", [("What is the difference between the tallest and shortest seedling?", mx(max(vals) - min(vals)) + " in."), ("What is the total of all the heights?", mx(tot) + " in.")], None),
        ("Fair Share of Water", "Water in each cup (liters): " + ", ".join(water) + ".", [("What is the total amount of water?", mx(sum(wv)) + " L"), ("If the water is shared equally among the cups, how much is in each cup?", mx(share) + " L")], None),
        ("Report", "Write a short report: what did you find out about the seedlings? Use at least two numbers from your line plot.", [("Report:", "Answers vary.")], None)]
    return dict(scenario="Your class is a team of plant scientists! You planted seedlings and measured them. Now it's time to organize and understand the data.",
                objectives=["Make a line plot with fraction measurements", "Use fraction operations to answer questions about data", "Find an equal share", "Communicate findings"],
                materials=["Pencil", "Ruler marked in 1/8 inches", "Grid or line plot template"], tasks=tasks,
                extension=("If every seedling grows another 1/4 inch, what is the new total height of all the seedlings?", mx(tot + F(len(vals), 4)) + " in."))
