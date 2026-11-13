"""Grade 3 projects: one per unit plus two cumulative projects. Every answer is computed here with exact arithmetic,
so the student packets, the teacher solutions and the rubric can never disagree.

The three versions differ in SUPPORT and REASONING, not only in numbers:
  cp2 Remedial  – a worked model for each part, hints, partly filled tables, sentence frames, fewer free choices.
  cp1 Standard  – the full task set at grade level, students choose their own strategies.
  honors Advanced – the same context with open design constraints, missing information to find, error analysis and a
                    written justification (no hints).
Each level returns: scenario, objectives, materials, tasks [(title, intro, [(question, answer, hint)], table)], extension (q, a)."""
from fractions import Fraction as F

LV = ["cp2", "cp1", "honors"]
LNAME = {"cp2": "Remedial", "cp1": "Standard", "honors": "Advanced"}
P = {}


def mx(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    w, r = divmod(x.numerator, x.denominator)
    return (f"{w} " if w else "") + f"{r}/{x.denominator}"


def project(key, units, folder, slug, title, tagline, description, theme, product, days, standards, targets, prereqs, materials, timing, notes, cumulative=False):
    def deco(fn):
        P[key] = dict(key=key, units=units, unit=units[0], folder=folder, slug=slug, title=title, tagline=tagline, description=description, theme=theme, product=product,
                      days=days, standards=standards, targets=targets, prereqs=prereqs, materials=materials, timing=timing, notes=notes, cumulative=cumulative, build=fn)
        return fn
    return deco


def T(L, *rows):
    """rows of (question, answer, hint); hints appear only in the Remedial packet."""
    return [(q, a, h if L == "cp2" else None) for q, a, h in rows]


# =================================================================== Unit 1
@project("multiplication-meaning", ["multiplication-meaning"], "math3-project-school-store-shelves", "school-store-shelves", "School Store Shelves",
         "Stock the school store with equal groups and arrays, then write a shelf plan.",
         "Students stock a school store. They model packs of supplies as equal groups, arrange items in arrays, write multiplication equations and solve store word problems.",
         "Shopping & Stores", "Store Shelf Plan", 2, ["3.OA.A.1", "3.OA.A.3", "3.OA.C.7"],
         ["I can write a multiplication expression for equal groups and tell what each factor means.", "I can describe an array and find the total by multiplying.",
          "I can solve equal-group and array word problems with a drawing and an equation."],
         ["Count objects and skip count by 2s, 5s and 10s (Grade 2)", "Add equal addends (repeated addition)"],
         ["Pencils, crayons and markers", "Counters or cubes (about 40 per pair)", "Grid paper (printable support page)", "Chart paper for the shelf plan"],
         ["Day 1 (45 min): read the challenge together; model packs with counters; Parts 1–2.", "Day 2 (45 min): arrays and store problems (Parts 3–4); build and share the shelf plan."],
         ["Let students build each pack with counters before they write the equation.", "Ask “How many groups? How many in each group?” for every item.",
          "Advanced students design their own shelf with a fixed number of items; check every array they claim."])
def pr1(L):
    packs = {"cp2": (4, 5), "cp1": (6, 8), "honors": (7, 9)}[L]
    rows = {"cp2": (3, 5), "cp1": (4, 7), "honors": (6, 8)}[L]
    g, n = packs
    r, c = rows
    tasks = [("Pencil Packs", f"The store gets {g} packs of pencils. Each pack has {n} pencils.",
              T(L, (f"Draw {g} equal groups. How many pencils are in each group?", str(n), "Each pack is one group."),
                (f"Write a multiplication expression for the pencils.", f"{g} × {n}", "Number of groups × number in each group."),
                ("How many pencils are there in all?", f"{g * n} pencils", f"Skip count by {n}s {g} times.")),
              [["Packs (groups)", "Pencils in each pack", "Total"], [str(g), str(n), "" if L != "cp2" else ""]]),
             ("Eraser Display", f"Erasers are set out in an array with {r} rows and {c} erasers in each row.",
              T(L, ("How many erasers are in each row?", str(c), "Count across one row."),
                ("Write an equation for the array.", f"{r} × {c} = {r * c}", "Rows × number in each row."),
                (f"The display turns so it has {c} rows. How many in each row now?", str(r), "Turning an array switches rows and columns.")), None),
             ("Store Problems", "Use a drawing or an equation for each problem.",
              T(L, ("Markers come in boxes of 10. The store orders 6 boxes. How many markers?", "60 markers", "Skip count by 10s."),
                ("Each notebook costs 5 dollars. How much do 7 notebooks cost?" if L != "honors" else "Notebooks cost 5 dollars each. What is the cost of 7 notebooks and 3 folders that cost 2 dollars each?",
                 "35 dollars" if L != "honors" else "41 dollars", "7 groups of 5.")), None)]
    if L == "honors":
        tasks.append(("Design Challenge", "The store has 36 glue sticks. Design shelf arrays that use ALL 36 with no extras.",
                      T(L, ("List every array (rows × number in each row) that uses exactly 36 glue sticks.", "1 × 36, 2 × 18, 3 × 12, 4 × 9, 6 × 6, 9 × 4, 12 × 3, 18 × 2, 36 × 1", None),
                        ("A shelf holds at most 6 rows and 9 in each row. Which arrays fit?", "4 × 9 and 6 × 6", None),
                        ("Kai says 5 × 7 works because 5 + 7 is close to 36. Explain the mistake.", "5 × 7 = 35, not 36, and adding the factors does not give the total.", None)), None))
    else:
        tasks.append(("Shelf Plan", "Make a shelf plan with three items. Show each item as equal groups or an array with an equation.",
                      T(L, ("Item 1, item 2 and item 3 with equations.", "Answers vary; each equation must match its picture.", "Use the sentence frame: “There are __ groups of __, so __ × __ = __.”")), None))
    return dict(scenario="You are the manager of the school store! New supplies arrived, and every item comes in equal packs or goes on the shelf in neat arrays.",
                objectives=["Write multiplication expressions for equal groups", "Use arrays to multiply", "Solve store word problems"],
                materials=["Pencil", "Counters or cubes", "Grid paper"], tasks=tasks,
                extension=("The store sells stickers in sheets of 4 rows of 5. A class buys 3 sheets. How many stickers?", "60 stickers (3 × 20)"))


# =================================================================== Unit 2
@project("division-meaning", ["division-meaning"], "math3-project-field-day-teams", "field-day-teams", "Field Day Teams",
         "Split the class into fair teams and share the equipment equally.",
         "Students plan Field Day. They share equipment equally (how many in each group), make teams of a given size (how many groups), write division equations and check with multiplication.",
         "Sports & Field Day", "Field Day Team Plan", 2, ["3.OA.A.2", "3.OA.A.3", "3.OA.B.6"],
         ["I can share a total equally and tell how many are in each group.", "I can make groups of a given size and tell how many groups there are.",
          "I can solve a division fact by finding the missing factor."],
         ["Multiplication facts and equal groups (Unit 1)", "Skip counting"],
         ["Counters (about 40 per pair)", "Paper plates or cups as groups", "Pencils", "Poster paper"],
         ["Day 1 (45 min): act out sharing and grouping with counters; Parts 1–2.", "Day 2 (45 min): Parts 3–4 and the team plan poster; gallery walk."],
         ["Act out both meanings with the same numbers so students see the answer means different things.", "Require a label on every answer (6 balls each, 6 teams).",
          "Advanced students handle a total that cannot be shared equally and must decide what to change."])
def pr2(L):
    kids = {"cp2": 20, "cp1": 24, "honors": 28}[L]
    team = {"cp2": 5, "cp1": 6, "honors": 7}[L]
    balls = {"cp2": 12, "cp1": 32, "honors": 48}[L]
    stations = {"cp2": 4, "cp1": 8, "honors": 6}[L]
    tasks = [("Making Teams", f"There are {kids} students. Each team needs {team} players.",
              T(L, ("How many teams can be made?", f"{kids // team} teams", f"Make groups of {team}. Count the groups."),
                ("Write a division equation.", f"{kids} ÷ {team} = {kids // team}", "Total ÷ number in each team."),
                ("Write the multiplication fact that checks it.", f"{kids // team} × {team} = {kids}", "Teams × players on each team.")), None),
             ("Sharing Equipment", f"{balls} balls are shared equally among {stations} stations.",
              T(L, ("How many balls go to each station?", f"{balls // stations} balls", f"Deal the balls one at a time to {stations} stations."),
                ("Is this sharing or grouping? Explain.", "Sharing: the number of groups (stations) is known.", "Sharing means you know how many groups.")), None),
             ("Fact Families", "Use multiplication to divide.",
              T(L, (f"Use {kids // team} × {team} = {kids} to find {kids} ÷ {kids // team}.", f"{team}", "The same three numbers."),
                ("Find 42 ÷ 7. Write the related multiplication fact.", "6, because 6 × 7 = 42", "7 × ? = 42.")), None)]
    if L == "honors":
        tasks.append(("Fair Teams?", "Two more students join, so there are " + str(kids + 2) + " students.",
                      T(L, (f"Can teams of {team} still be made with no one left out? Explain.", f"No. {kids + 2} is not a multiple of {team} ({kids // team} teams use {kids}).", None),
                        (f"Find a team size from 3 to 10 that works for {kids + 2} students. How many teams?", "Answers vary: e.g. teams of " +
                         ", ".join(f"{d} ({(kids + 2) // d} teams)" for d in range(3, 11) if (kids + 2) % d == 0), None)), None))
    else:
        tasks.append(("Team Plan", "Make a poster that shows the teams and the equipment for each station.",
                      T(L, ("Show your teams with a picture and an equation.", "Answers vary; picture and equation must match.", "Frame: “__ students in teams of __ makes __ teams.”")), None))
    return dict(scenario="Field Day is coming! The coach needs fair teams and the same equipment at every station.",
                objectives=["Divide by sharing equally", "Divide by making equal groups", "Use multiplication facts to divide"],
                materials=["Pencil", "Counters", "Paper plates or cups"], tasks=tasks,
                extension=("The coach has 45 cones and 35 flags for 5 stations. How many cones and flags does each station get?", "9 cones and 7 flags (45 ÷ 5 = 9, 35 ÷ 5 = 7)"))


# =================================================================== Unit 3
@project("properties-fact-strategies", ["properties-fact-strategies"], "math3-project-bakery-boxes", "bakery-boxes", "Bakery Boxes",
         "Fill bakery orders using properties and fact strategies to multiply quickly.",
         "Students run a bakery. They pack muffins in trays and boxes, turn arrays (commutative), regroup trays and boxes (associative), break hard facts into easier ones (distributive) and explain their strategies.",
         "Food & Cooking", "Bakery Order Sheet", 2, ["3.OA.B.5", "3.OA.C.7"],
         ["I can use the commutative and associative properties to multiply.", "I can break a factor into parts, multiply each part and add.", "I can find any fact to 10 × 10 with a strategy."],
         ["Arrays and equal groups (Unit 1)", "Facts for 2, 5 and 10"],
         ["Grid paper or square tiles", "Colored pencils", "Order sheet (printable support page)"],
         ["Day 1 (45 min): trays as arrays; turn and split arrays (Parts 1–2).", "Day 2 (45 min): boxes of trays (Part 3) and the order sheet with explained strategies."],
         ["Split arrays with a colored line so the two parts are visible.", "Ask students to name the known fact they start from.",
          "Advanced students compare two strategies for the same order and judge which is easier and why."])
def pr3(L):
    a, b = {"cp2": (4, 6), "cp1": (7, 6), "honors": (8, 7)}[L]
    p = 5
    boxes, trays, per = {"cp2": (2, 3, 5), "cp1": (3, 2, 5), "honors": (4, 3, 5)}[L]
    tasks = [("Muffin Trays", f"One tray holds {a} rows of {b} muffins.",
              T(L, ("How many muffins are on one tray?", f"{a * b} muffins", f"{a} × {b}."),
                (f"Turn the tray. Write the other multiplication equation.", f"{b} × {a} = {a * b}", "Rows become columns.")), None),
             ("Break It Apart", f"Split the tray after the 5th column to make {a} × {b} easier.",
              T(L, (f"Write the two smaller facts.", f"{a} × 5 = {a * 5} and {a} × {b - 5} = {a * (b - 5)}", f"{b} = 5 + {b - 5}."),
                ("Add the parts. What is the total?", f"{a * b}", "Add the two products.")), None),
             ("Boxes of Trays", f"A box holds {trays} trays, and each tray has {per} cupcakes. An order is for {boxes} boxes.",
              T(L, ("How many cupcakes are in one box?", f"{trays * per} cupcakes", f"{trays} × {per}."),
                ("How many cupcakes are in the whole order?", f"{boxes * trays * per} cupcakes", f"({boxes} × {trays}) × {per} or {boxes} × ({trays} × {per})."),
                ("Which grouping did you use, and why was it easy?", "Answers vary, e.g. " + f"{trays} × {per} = {trays * per} first, then × {boxes}.", "Look for a 10.")), None)]
    if L == "honors":
        tasks.append(("Compare Strategies", "Two bakers found 9 × 8 in different ways.",
                      T(L, ("Ana: (10 × 8) − 8. Ben: (5 × 8) + (4 × 8). Find each result.", "Both get 72: 80 − 8 = 72; 40 + 32 = 72.", None),
                        ("Which strategy uses fewer steps? Explain.", "Ana’s: one known fact and one subtraction.", None),
                        ("Cora wrote 9 × 8 = (9 × 5) + 3. What is wrong?", "She did not multiply the 3 by 9; it should be (9 × 5) + (9 × 3) = 72.", None)), None))
    else:
        tasks.append(("Order Sheet", "Fill in the order sheet for 3 orders. Show one strategy for each product.",
                      T(L, ("Orders and strategies.", "Answers vary; check each product and strategy.", "Use a fact you know: × 2 is double, × 5 is half of × 10.")), None))
    return dict(scenario="Welcome to the Third Grade Bakery! Orders are pouring in, and the fastest bakers use smart multiplication strategies.",
                objectives=["Use the commutative property", "Use the associative property", "Break apart a fact with the distributive property"],
                materials=["Pencil", "Grid paper", "Colored pencils"], tasks=tasks,
                extension=("A pan has 6 rows of 9 rolls. Show two different ways to break apart 6 × 9.", "Examples: (6 × 5) + (6 × 4) = 54; (5 × 9) + (1 × 9) = 54."))


# =================================================================== Unit 4
@project("addition-subtraction-1000", ["addition-subtraction-1000"], "math3-project-read-a-thon", "read-a-thon", "Read‑a‑Thon Report",
         "Total the pages read, compare classes and report rounded results.",
         "Students run the school Read-a-Thon. They add and subtract page counts within 1,000, round totals to the nearest 10 and 100 for a news report, and use estimates to check answers.",
         "Reading & Libraries", "Read‑a‑Thon News Report", 2, ["3.NBT.A.1", "3.NBT.A.2", "3.OA.D.8"],
         ["I can round whole numbers to the nearest 10 and 100.", "I can add and subtract within 1,000 with place value strategies.", "I can estimate to check whether an answer is reasonable."],
         ["Place value of hundreds, tens and ones (Grade 2)", "Adding and subtracting within 100"],
         ["Base‑ten blocks (optional)", "Place-value chart (printable support page)", "Pencils"],
         ["Day 1 (45 min): totals and differences (Parts 1–2) with base‑ten blocks available.", "Day 2 (45 min): rounding and estimates (Part 3) and the news report."],
         ["Insist on an estimate before every exact calculation.", "Use a place-value chart for regrouping; check subtraction by adding.",
          "Advanced students find a missing weekly total and judge a classmate’s rounded report."])
def pr4(L):
    weeks = {"cp2": [124, 213, 152], "cp1": [236, 318, 287], "honors": [348, 276, 0]}[L]
    goal = {"cp2": 600, "cp1": 950, "honors": 1000}[L]
    if L == "honors":
        total_known = 891
        weeks[2] = total_known - weeks[0] - weeks[1]
    tot = sum(weeks)
    other = {"cp2": 412, "cp1": 685, "honors": 734}[L]
    def r10(n): return (n + 5) // 10 * 10
    def r100(n): return (n + 50) // 100 * 100
    rows = [["Week", "Pages read"]] + [[f"Week {i + 1}", str(w) if not (L == "honors" and i == 2) else "?"] for i, w in enumerate(weeks)]
    tasks = [("Weekly Pages", "Room 12 recorded the pages it read." + (" The three-week total was 891 pages." if L == "honors" else ""),
              T(L, ("How many pages did Room 12 read in Weeks 1 and 2 together?", f"{weeks[0] + weeks[1]} pages", "Add hundreds, tens, then ones. Regroup if needed."),
                ("How many pages in all three weeks?" if L != "honors" else "How many pages were read in Week 3?",
                 f"{tot} pages" if L != "honors" else f"{weeks[2]} pages", "Add the third week to your answer above." if L == "cp2" else None)), rows),
             ("Beat the Goal?", f"The class goal was {goal} pages.",
              T(L, ("How many more pages are needed to reach the goal (or how many over the goal)?" if tot < goal else "How many pages over the goal did the class read?",
                    f"{abs(goal - tot)} pages", "Subtract the smaller number from the larger number."),
                (f"Room 14 read {other} pages. How many more pages did Room 12 read than Room 14?", f"{tot - other} pages", "Subtract and check by adding.")), None),
             ("News Report Numbers", "A newspaper uses rounded numbers.",
              T(L, ("Round Room 12’s total to the nearest 10.", f"{r10(tot)}", "Look at the ones digit."),
                ("Round Room 12’s total to the nearest 100.", f"{r100(tot)}", "Look at the tens digit."),
                ("Estimate the total for both rooms by rounding to the nearest 100. Is your exact sum reasonable?", f"{r100(tot)} + {r100(other)} = {r100(tot) + r100(other)}; exact {tot + other} is close, so it is reasonable.", "Round each, then add.")), None)]
    if L == "honors":
        tasks.append(("Check the Reporter", "A reporter wrote: “Room 12 read about 800 pages, 300 more than Room 14.”",
                      T(L, ("Is “about 800” correct to the nearest 100? Explain.", f"No. {tot} rounds to {r100(tot)}.", None),
                        ("Is “300 more” reasonable? Use exact numbers and estimates.", f"Exact: {tot} − {other} = {tot - other}, about {r100(tot - other)}; so 300 is not reasonable.", None)), None))
    else:
        tasks.append(("Write the Report", "Write 3 sentences for the school news with one exact number, one rounded number and one comparison.",
                      T(L, ("Your report.", "Answers vary; numbers must match the work above.", "Frame: “Room 12 read ___ pages. That is about ___. That is ___ more than Room 14.”")), None))
    return dict(scenario="The school Read‑a‑Thon is over. You are the reporter who adds up the pages and writes the news!",
                objectives=["Add and subtract within 1,000", "Round to the nearest 10 and 100", "Check answers with estimates"],
                materials=["Pencil", "Place-value chart", "Base‑ten blocks (optional)"], tasks=tasks,
                extension=("Room 16 read 1,000 pages minus 368 pages. How many is that? Round it to the nearest 100.", "632 pages; about 600"))


# =================================================================== Unit 5
@project("patterns-unknowns-two-step", ["patterns-unknowns-two-step"], "math3-project-class-celebration", "class-celebration", "Class Celebration Planner",
         "Plan a class party with two-step problems, unknowns and multiples of 10.",
         "Students plan a class celebration. They buy supplies in packs, find unknown numbers, multiply by multiples of 10, write equations with a letter for two-step problems and check that the plan is reasonable.",
         "Events & Planning", "Celebration Plan", 2, ["3.OA.A.4", "3.OA.D.8", "3.NBT.A.3", "3.OA.D.9"],
         ["I can find an unknown number in a multiplication or division equation.", "I can multiply a one-digit number by a multiple of 10.",
          "I can write and solve an equation with a letter for a two-step problem and check that the answer is reasonable."],
         ["Multiplication and division facts (Units 1–3)", "Adding and subtracting within 1,000 (Unit 4)"],
         ["Pencils", "Planning sheet (printable support page)", "Play money (optional)"],
         ["Day 1 (45 min): supply packs and unknowns (Parts 1–2).", "Day 2 (45 min): budget two-step problems and the celebration plan (Parts 3–4)."],
         ["Have students underline the question and name what the letter stands for before writing an equation.", "Require an estimate for every money answer.",
          "Advanced students meet a budget with choices and justify their plan."])
def pr5(L):
    kids = {"cp2": 20, "cp1": 24, "honors": 27}[L]
    cups_pack = {"cp2": 10, "cp1": 8, "honors": 6}[L]
    packs = -(-kids // cups_pack)
    price = {"cp2": 3, "cp1": 4, "honors": 6}[L]
    budget = {"cp2": 50, "cp1": 90, "honors": 150}[L]
    pizza_cost = {"cp2": 20, "cp1": 30, "honors": 40}[L]
    pizzas = {"cp2": 2, "cp1": 2, "honors": 2}[L]
    left = budget - pizzas * pizza_cost - packs * price
    tasks = [("Supply Packs", f"There are {kids} students. Cups come in packs of {cups_pack}.",
              T(L, (f"How many packs are needed so every student gets a cup? (Write ? × {cups_pack} ≥ {kids}.)", f"{packs} packs", f"Skip count by {cups_pack}s until you reach {kids} or more."),
                (f"How many cups will be left over?", f"{packs * cups_pack - kids} cups", f"{packs} × {cups_pack} − {kids}.")), None),
             ("Mystery Numbers", "Find each unknown.",
              T(L, ("6 × n = 48", "n = 8", "Think 48 ÷ 6."), ("n ÷ 4 = 7", "n = 28", "Think 4 × 7."), (f"{kids * 2} = 2 × n", f"n = {kids}", "Half of the total."))
              , None),
             ("Tens Shopping", "Balloons come in bags of 20, 30 or 40.",
              T(L, ("What is 4 × 30?", "120", "4 × 3 tens = 12 tens."), ("What is 6 × 40?", "240", "6 × 4 tens."), ("How many balloons are in 3 bags of 20 and 2 bags of 30?", "120 balloons", "Find each product, then add.")), None),
             ("Budget", f"The class has {budget} dollars. Pizza costs {pizza_cost} dollars each and cup packs cost {price} dollars each.",
              T(L, (f"Write an equation for the money left after {pizzas} pizzas and {packs} cup packs. Use m for the money left.",
                    f"m = {budget} − ({pizzas} × {pizza_cost}) − ({packs} × {price})", "Two costs are taken away from the budget."),
                    ("Solve for m.", f"m = {left} dollars", "Multiply first, then subtract."),
                    ("Is your answer reasonable? Explain with an estimate.", "Answers vary, e.g. " + f"{budget} − {pizzas * pizza_cost} − about {(packs * price + 5) // 10 * 10} ≈ {budget - pizzas * pizza_cost - (packs * price + 5) // 10 * 10}.", "Round each cost to the nearest 10.")), None)]
    if L == "honors":
        tasks.append(("Design Challenge", f"Spend the leftover {left} dollars on games that cost 7 dollars and prizes that cost 4 dollars.",
                      T(L, ("Find a combination that spends as much as possible without going over. Show the equation.", "Answers vary; e.g. " + best_combo(left), None),
                        ("Explain why your plan is the best one.", "Answers vary; must compare at least two plans.", None)), None))
    return dict(scenario="Our class earned a celebration! You are on the planning team with a budget to manage.",
                objectives=["Find unknown numbers", "Multiply by multiples of 10", "Write and solve two-step equations", "Check that answers are reasonable"],
                materials=["Pencil", "Planning sheet"], tasks=tasks,
                extension=("Products in the 5s column end in 0 or 5. Explain why using 5 × n = 10 × n − 5 × n or half of 10 × n.", "5 × n is half of 10 × n; 10 × n ends in 0, and half of it ends in 0 or 5."))


def best_combo(m):
    best = max(((g, p) for g in range(m // 7 + 1) for p in range(m // 4 + 1) if 7 * g + 4 * p <= m), key=lambda x: (7 * x[0] + 4 * x[1], x[0]))
    return f"{best[0]} games and {best[1]} prizes: 7 × {best[0]} + 4 × {best[1]} = {7 * best[0] + 4 * best[1]} dollars"


# =================================================================== Unit 6
@project("understanding-fractions", ["understanding-fractions"], "math3-project-garden-plots", "garden-plots", "Garden Plot Fractions",
         "Split garden beds into equal parts and mark a fraction trail.",
         "Students plan a class garden. They split beds into equal parts, name unit fractions and fractions built from unit fractions, and place trail markers on a fraction number line.",
         "Gardens & Nature", "Garden Map", 2, ["3.NF.A.1", "3.NF.A.2.a", "3.NF.A.2.b", "3.G.A.2"],
         ["I can name a unit fraction for one of b equal parts.", "I can explain a/b as a copies of 1/b.", "I can place fractions on a number line, including fractions greater than 1."],
         ["Partition shapes into halves, thirds and fourths (Grade 2)", "Equal parts"],
         ["Grid paper and rulers", "Colored pencils", "Fraction strips (printable support page)", "String or a paper strip for the trail"],
         ["Day 1 (45 min): beds and equal parts (Parts 1–2).", "Day 2 (45 min): the fraction trail on a number line (Part 3) and the garden map."],
         ["Check every partition for EQUAL parts before naming fractions.", "On number lines, have students count jumps aloud from 0.",
          "Advanced students design a bed with a required fraction for each plant and defend that the parts are equal."])
def pr6(L):
    bed = {"cp2": 4, "cp1": 6, "honors": 8}[L]
    car, bea = {"cp2": (1, 2), "cp1": (2, 3), "honors": (3, 2)}[L]
    den = {"cp2": 4, "cp1": 4, "honors": 3}[L]
    stop = {"cp2": 3, "cp1": 5, "honors": 7}[L]
    tasks = [("Garden Beds", f"Bed A is a rectangle split into {bed} equal parts.",
              T(L, ("What fraction of the bed is one part?", f"1/{bed}", f"{bed} equal parts: each is 1/{bed}."),
                (f"Carrots fill {car} {'part' if car == 1 else 'parts'}. What fraction of the bed is carrots?", f"{car}/{bed}", "Count the carrot parts. The denominator stays the same."),
                (f"Beans fill {bea} parts. What fraction of the bed is beans?", f"{bea}/{bed}", "Beans are copies of the unit fraction."),
                ("What fraction of the bed is still empty?", f"{bed - car - bea}/{bed}", "Total parts minus carrot and bean parts.")),
              [["Plant", "Parts", "Fraction"], ["Carrots", str(car), f"{car}/{bed}" if L == "cp2" else ""], ["Beans", str(bea), ""], ["Empty", "", ""]]),
             ("Equal or Not?", "Mia split Bed B into 4 parts: two big and two small.",
              T(L, ("Can each part be called 1/4 of the bed? Explain.", "No. The parts are not equal, so they are not fourths.", "Fourths must be 4 EQUAL parts.")), None),
             ("Fraction Trail", f"The garden path from the gate (0) to the fountain (1) is marked in {DEN(den)}." + (" It keeps going to the shed at 2." if L != "cp2" else ""),
              T(L, ("Where is the first marker? Write a fraction.", f"1/{den}", "Count one jump from 0."),
                (f"A bird bath is {stop} jumps from the gate. What fraction is that?", f"{stop}/{den}", f"Count {stop} jumps of 1/{den}."),
                ("Is the bird bath before or after the fountain at 1? How do you know?", "After" if stop > den else "Before", f"1 = {den}/{den}.")), None)]
    if L == "honors":
        tasks.append(("Design Challenge", "Design Bed C (a rectangle on grid paper) for 4 plants.",
                      T(L, ("Use eighths. Tomatoes 3/8, peppers 2/8, herbs 2/8 and flowers the rest. What fraction is flowers?", "1/8", None),
                        ("Draw it so all parts have equal area even if they are different shapes. Explain how you know.", "Answers vary; each eighth must have the same number of grid squares.", None)), None))
    return dict(scenario="Our class is planting a garden! The beds must be split into equal parts, and the path needs fraction markers.",
                objectives=["Name unit fractions", "Build fractions from unit fractions", "Place fractions on a number line"],
                materials=["Pencil", "Grid paper", "Colored pencils"], tasks=tasks,
                extension=("The path goes from 0 to 2 in fourths. Name every marker past 1.", "5/4, 6/4, 7/4, 8/4"))


def DEN(d):
    return {2: "halves", 3: "thirds", 4: "fourths", 6: "sixths", 8: "eighths"}[d]


# =================================================================== Unit 7
@project("equivalent-comparing-fractions", ["equivalent-comparing-fractions"], "math3-project-ribbon-shop", "ribbon-shop", "The Ribbon Shop",
         "Cut, match and compare ribbon orders using equivalent fractions.",
         "Students run a ribbon shop where every ribbon is 1 yard long. They match equivalent orders on fraction strips, write whole numbers as fractions, and compare orders with the same numerator or the same denominator.",
         "Shopping & Crafts", "Ribbon Order Chart", 2, ["3.NF.A.3.a", "3.NF.A.3.b", "3.NF.A.3.c", "3.NF.A.3.d"],
         ["I can show and explain equivalent fractions with models.", "I can write whole numbers as fractions.", "I can compare fractions with the same numerator or the same denominator and justify my answer."],
         ["Unit fractions and number lines (Unit 6)"],
         ["Fraction strips (printable support page) or paper strips", "Scissors and tape", "Colored pencils"],
         ["Day 1 (45 min): matching equivalent orders with strips (Parts 1–2).", "Day 2 (45 min): comparing orders (Part 3) and the order chart."],
         ["All strips must be the same length (the same whole).", "For every comparison, ask students to name the piece size.",
          "Advanced students judge customers’ claims and build an equivalence chart."])
def pr7(L):
    pairs = {"cp2": [("1/2", "2/4"), ("1/4", "2/8")], "cp1": [("1/2", "4/8"), ("2/3", "4/6"), ("3/4", "6/8")], "honors": [("2/3", "4/6"), ("3/4", "6/8"), ("3/2", "6/4")]}[L]
    sd = {"cp2": ("3/8", "5/8"), "cp1": ("5/6", "2/6"), "honors": ("7/8", "5/8")}[L]
    sn = {"cp2": ("1/3", "1/6"), "cp1": ("2/4", "2/8"), "honors": ("3/6", "3/4")}[L]
    def cmpsym(a, b): return ">" if F(a) > F(b) else "<" if F(a) < F(b) else "="
    tasks = [("Matching Orders", "Two customers get the same amount of ribbon when their fractions are equivalent.",
              T(L, *[(f"Order {a} yard. Which order in {DEN(F(b).denominator if False else int(b.split('/')[1]))} is the same length?", f"{b} yard", f"Line up the {a} strip with the strip cut in {DEN(int(b.split('/')[1]))}.") for a, b in pairs]), None),
             ("Whole Yards", "Some customers buy whole yards.",
              T(L, ("Write 2 yards as a fraction with denominator 1.", "2/1", "2 wholes, each with 1 part."),
                ("Write 1 yard in fourths.", "4/4", "All 4 fourths make 1 whole."),
                ("Write 3 yards in halves.", "6/2", "Each yard has 2 halves: 3 × 2.")), None),
             ("Who Gets More?", "Compare the orders. Write >, < or = and explain.",
              T(L, (f"{sd[0]} yard ___ {sd[1]} yard", cmpsym(*sd), "Same denominator: compare the numerators."),
                (f"{sn[0]} yard ___ {sn[1]} yard", cmpsym(*sn), "Same numerator: the bigger pieces win.")), None)]
    if L == "honors":
        tasks.append(("Customer Claims", "Decide if each claim is true. Explain with a model.",
                      T(L, ("“1/8 yard is more than 1/4 yard because 8 > 4.”", "False. Eighths are smaller pieces; 1/8 < 1/4.", None),
                        ("“1/2 of my small ribbon roll is the same as 1/2 of the big roll.”", "False. The wholes are different sizes.", None),
                        ("“4/4 = 8/8 = 1 yard.”", "True. All the parts of one whole make 1.", None)), None))
    else:
        tasks.append(("Order Chart", "Make a chart of 4 orders: two equivalent pairs and one comparison.",
                      T(L, ("Your chart.", "Answers vary; check the models.", "Use strips of the same length for every order.")), None))
    return dict(scenario="Welcome to the Ribbon Shop! Every roll is 1 yard long, and customers order ribbon in fractions of a yard.",
                objectives=["Find equivalent fractions", "Write whole numbers as fractions", "Compare fractions"],
                materials=["Pencil", "Fraction strips", "Scissors and tape"], tasks=tasks,
                extension=("Find three fractions equal to 1/2 using halves, fourths, sixths or eighths.", "2/4, 3/6, 4/8"))


# =================================================================== Unit 8
@project("time-volume-mass", ["time-volume-mass"], "math3-project-science-museum-day", "science-museum-day", "Science Museum Day",
         "Build a field-trip schedule and run a water-and-mass lab.",
         "Students plan a day at a science museum. They read clocks, build a schedule with elapsed time, and at the lab station measure and solve problems with liters, grams and kilograms.",
         "Science & Field Trips", "Museum Day Schedule and Lab Sheet", 2, ["3.MD.A.1", "3.MD.A.2"],
         ["I can tell and write time to the nearest minute.", "I can find elapsed time, start times and end times in minutes.", "I can measure and solve one-step problems with liters, grams and kilograms."],
         ["Telling time to 5 minutes (Grade 2)", "Adding and subtracting within 100"],
         ["Demonstration clock or paper clocks", "Containers marked in liters (or the printable beaker page)", "Balance scale and gram weights (optional)", "Pencils"],
         ["Day 1 (45 min): clocks and the schedule (Parts 1–2) with open number lines.", "Day 2 (45 min): the water and mass lab (Part 3) and the final schedule."],
         ["Model elapsed time on an open number line: jump to the next hour first.", "Have students read the scale value of one mark before reading any measurement.",
          "Advanced students fit activities into a fixed time block and fix a schedule with an error."])
def pr8(L):
    start = {"cp2": (9, 10), "cp1": (9, 15), "honors": (9, 5)}[L]
    acts = {"cp2": [("Dinosaur Hall", 30), ("Space Show", 20)], "cp1": [("Dinosaur Hall", 35), ("Space Show", 25), ("Lunch", 40)], "honors": [("Dinosaur Hall", 45), ("Space Show", 35), ("Lunch", 40)]}[L]
    def add(h, m, k):
        t = h * 60 + m + k
        return (t // 60 - 1) % 12 + 1, t % 60
    def tm(h, m): return f"{h}:{m:02d}"
    rows, cur = [["Activity", "Start", "Minutes", "End"]], start
    for nm, d in acts:
        end = add(*cur, d)
        rows.append([nm, tm(*cur), str(d), tm(*end) if L == "cp2" and nm == acts[0][0] else ""])
        cur = end
    final = cur
    total = sum(d for _, d in acts)
    tasks = [("Clock Check", "The bus arrives at the museum. The clock shows " + tm(*start) + ".",
              T(L, ("Where is the hour hand? Where is the minute hand?", f"Hour hand just past the {start[0]}; minute hand on the {start[1] // 5}.", "The minute hand counts by 5s."),
                ("How many minutes until 10:00?", f"{60 - start[1]} minutes", "60 minutes in an hour.")), None),
             ("Build the Schedule", "Fill in the end time of each activity. Each one starts when the one before it ends.",
              T(L, ("What time does the last activity end?", tm(*final), "Add the minutes on a number line."),
                ("How many minutes do all the activities take?", f"{total} minutes", "Add the minutes column.")), rows),
             ("Water and Mass Lab", "At the lab, you measure water and weigh rocks.",
              T(L, ("A tank holds 18 liters. You pour in 3 buckets of 4 liters. How many more liters fill the tank?" if L != "cp2" else "You pour 3 buckets of 4 liters into a tank. How many liters is that?",
                    "6 liters" if L != "cp2" else "12 liters", "3 × 4 first."),
                ("A rock is 350 grams. A crystal is 125 grams. How many more grams is the rock?", "225 grams", "Subtract the masses."),
                ("Would you measure a backpack in grams or kilograms?", "kilograms", "Heavy things: kilograms.")), None)]
    if L == "honors":
        tasks.append(("Fix the Schedule", "The bus leaves at 12:30.",
                      T(L, (f"The last activity ends at {tm(*final)}. How many minutes are left before the bus leaves?", f"{minutes_between(final, (12, 30))} minutes", None),
                        ("Add a 25-minute Robot Lab. Does it fit? Explain.", (f"Yes. {minutes_between(final, (12, 30))} minutes are left, and 25 < {minutes_between(final, (12, 30))}." if minutes_between(final, (12, 30)) >= 25 else f"No. Only {minutes_between(final, (12, 30))} minutes are left."), None)), None))
    return dict(scenario="Our class is going to the science museum! You are in charge of the schedule and the lab station.",
                objectives=["Tell time to the minute", "Find elapsed time", "Measure liquid volume and mass"],
                materials=["Pencil", "Paper clock", "Beaker page"], tasks=tasks,
                extension=("A movie at the museum starts at 1:45 and lasts 50 minutes. When does it end?", "2:35"))


def minutes_between(a, b):
    def m(t):
        h = t[0] % 12
        return (h + 12 if h < 7 else h) * 60 + t[1]
    return m(b) - m(a)


# =================================================================== Unit 9
@project("graphs-measurement-data", ["graphs-measurement-data"], "math3-project-class-survey-report", "class-survey-report", "Class Survey and Data Report",
         "Run a class survey, draw scaled graphs and measure pencils for a line plot.",
         "Students run an anonymous class survey (no names), show the results in a scaled picture graph and a scaled bar graph, answer how-many-more questions, and measure pencils to the nearest quarter inch for a line plot.",
         "Data & Surveys", "Data Report Poster", 3, ["3.MD.B.3", "3.MD.B.4"],
         ["I can draw a scaled picture graph and bar graph from data.", "I can solve one- and two-step how-many-more and how-many-less problems with a graph.",
          "I can measure to the nearest quarter inch and make a line plot."],
         ["Tally charts and simple graphs (Grade 2)", "Multiplication by 2, 5 and 10"],
         ["Rulers marked in quarter inches", "Pencils of different lengths (about 10 per group)", "Grid paper", "Sample data card (printable support page) for classes that skip the survey"],
         ["Day 1 (45 min): collect votes with tallies (no names) and make the picture graph.", "Day 2 (45 min): bar graph and how-many-more questions.",
          "Day 3 (45 min): measure pencils, make the line plot, and finish the poster."],
         ["Use only anonymous tally votes; never record student names or personal information.", "If time is short, use the sample data card.",
          "Advanced students choose and defend their own scales."])
def pr9(L):
    data = {"Pizza": 12, "Tacos": 8, "Pasta": 6, "Salad": 4} if L != "honors" else {"Pizza": 14, "Tacos": 9, "Pasta": 6, "Salad": 3}
    key = 2
    lengths = ["3", "3 1/2", "4", "3 1/2", "4 1/2", "3 1/2", "4"] if L == "cp2" else ["3 1/4", "3 1/2", "4", "3 1/2", "4 3/4", "3 1/4", "4", "3 1/2"]
    from collections import Counter
    cnt = Counter(F(x.split(" ")[0]) + (F(x.split(" ")[1]) if " " in x else 0) for x in lengths)
    most = max(cnt, key=cnt.get)
    rows = [["Lunch", "Votes"]] + [[k, str(v)] for k, v in data.items()]
    tasks = [("Survey Data", "Use your class votes or the sample data in the table." if L != "honors" else "Use the sample data in the table (or your own class votes).",
              T(L, (f"In a picture graph, each ★ = {key} votes. How many ★ for Pizza?", f"{mx(F(data['Pizza'], key))} stars", f"{data['Pizza']} ÷ {key}."),
                (f"How many ★ for Tacos?", f"{mx(F(data['Tacos'], key))} stars", "Use half a star for 1 vote." if data['Tacos'] % 2 else f"{data['Tacos']} ÷ {key}.")), rows),
             ("Bar Graph", "Make a bar graph with a scale that counts by 2s.",
              T(L, ("How many more votes for Pizza than for Salad?", f"{data['Pizza'] - data['Salad']} votes", "Subtract the bars."),
                ("How many more votes for Pizza than for Tacos and Salad together?" if data['Pizza'] > data['Tacos'] + data['Salad'] else "How many fewer votes for Pizza than for Tacos and Salad together?",
                 f"{abs(data['Pizza'] - data['Tacos'] - data['Salad'])} votes", "Add Tacos and Salad first.")), None),
             ("Pencil Line Plot", "Measure pencils to the nearest " + ("half" if L == "cp2" else "quarter") + " inch. Sample lengths: " + ", ".join(lengths) + " inches.",
              T(L, ("Which length appears most often?", f"{mx(most)} inches", "Count each length."),
                    ("How many pencils are longer than 3 1/2 inches?", f"{sum(v for k, v in cnt.items() if k > F(7, 2))} pencils", "Count the X marks to the right of 3 1/2."),
                    ("How should the line plot scale be marked?", "in half inches" if L == "cp2" else "in quarter inches", "The scale needs a mark for every value.")), None)]
    if L == "honors":
        tasks.append(("Choose the Scale", "A bigger school voted: Pizza 140, Tacos 95, Pasta 60, Salad 35.",
                      T(L, ("Choose a key for a picture graph so every number uses whole or half symbols. Explain.", "Key of 10 (half symbol = 5) works: 14, 9 1/2, 6, 3 1/2 symbols.", None),
                        ("How many more votes for Pizza than Pasta and Salad together?", "45 votes", None)), None))
    return dict(scenario="You are the class data team! Collect lunch votes (no names), make graphs, and measure pencils for a line plot.",
                objectives=["Make scaled picture and bar graphs", "Answer how-many-more questions", "Measure to the nearest quarter inch", "Make a line plot"],
                materials=["Pencil", "Ruler", "Grid paper"], tasks=tasks,
                extension=("Make a second bar graph of the same data with a scale that counts by 4s. Which bars end between grid lines?",
                           ", ".join(k for k, v in data.items() if v % 4) + " (not multiples of 4)"))


# =================================================================== Unit 10
@project("area", ["area"], "math3-project-reading-nook", "reading-nook", "Design a Reading Nook",
         "Plan a cozy reading nook with rugs, mats and an L‑shaped corner, using area.",
         "Students design a classroom reading nook on grid paper. They count square units, multiply side lengths, split rectangles with the distributive property and find the area of an L‑shaped corner.",
         "Design & Building", "Reading Nook Floor Plan", 2, ["3.MD.C.5.a", "3.MD.C.5.b", "3.MD.C.6", "3.MD.C.7.a", "3.MD.C.7.b", "3.MD.C.7.c", "3.MD.C.7.d"],
         ["I can find area by counting unit squares and name it in square units.", "I can find the area of a rectangle by multiplying side lengths.",
          "I can find the area of a rectilinear figure by splitting it into rectangles."],
         ["Arrays and multiplication facts (Units 1–3)"],
         ["Grid paper (1 square = 1 square foot, printable support page)", "Square tiles (optional)", "Colored pencils", "Rulers"],
         ["Day 1 (45 min): rugs and mats by tiling and multiplying (Parts 1–2).", "Day 2 (45 min): the L‑shaped corner and the final floor plan (Parts 3–4)."],
         ["Check that every area answer uses square units.", "Have students shade each rectangle in a different color before adding areas.",
          "Advanced students meet area and space limits and compare two designs."])
def pr10(L):
    rug = {"cp2": (4, 3), "cp1": (6, 4), "honors": (8, 6)}[L]
    mat = {"cp2": (6, 2, 4), "cp1": (7, 5, 3), "honors": (9, 7, 5)}[L]   # h, a, b
    W, H, a, h1 = {"cp2": (6, 5, 3, 2), "cp1": (9, 7, 4, 3), "honors": (12, 9, 5, 4)}[L]
    larea = W * h1 + a * (H - h1)
    tasks = [("The Rug", f"The rug is {rug[0]} feet long and {rug[1]} feet wide. Each grid square is 1 square foot.",
              T(L, ("Draw the rug on grid paper. How many square feet does it cover?", f"{rug[0] * rug[1]} square feet", f"{rug[1]} rows of {rug[0]} squares."),
                ("Write a multiplication equation for its area.", f"{rug[0]} × {rug[1]} = {rug[0] * rug[1]}", "Length × width.")), None),
             ("Break Apart the Mat", f"A floor mat is {mat[0]} feet by {mat[1] + mat[2]} feet. Split the long side into {mat[1]} and {mat[2]}.",
              T(L, ("Find the area of each part.", f"{mat[0]} × {mat[1]} = {mat[0] * mat[1]} and {mat[0]} × {mat[2]} = {mat[0] * mat[2]}", "Each part is a rectangle."),
                ("Add to find the area of the whole mat.", f"{mat[0] * (mat[1] + mat[2])} square feet", "Add the two areas.")), None),
             ("The L‑Shaped Corner", f"The corner is {W} feet across the bottom and {H} feet up the left side. The bottom part is {h1} feet tall, and the top part is {a} feet wide.",
              T(L, ("Split the corner into two rectangles. Write the area of each.", f"{W} × {h1} = {W * h1} and {a} × {H - h1} = {a * (H - h1)}", f"The top part is {H} − {h1} = {H - h1} feet tall."),
                ("What is the area of the whole corner?", f"{larea} square feet", "Add the two areas.")), None)]
    if L == "honors":
        tasks.append(("Design Challenge", f"The nook can use at most {larea} square feet. You want one rug plus two pillow mats that are 2 by 3 feet.",
                      T(L, (f"Give rug side lengths so everything fits in {larea} square feet. Show the area total.", f"Answers vary; the rug area must be at most {larea - 12} square feet, e.g. " + rug_example(larea - 12) + ".", None),
                        ("Jaden says the corner is " + f"{W} × {H} = {W * H}" + " square feet. Explain his mistake.", "He used the whole rectangle around the L and counted the missing corner.", None)), None))
    else:
        tasks.append(("Floor Plan", "Draw your nook with the rug and the mat in the L‑shaped corner. Label each area.",
                      T(L, ("Your plan with labels.", "Answers vary; labels must match the drawing.", "Use one color for each rectangle.")), None))
    return dict(scenario="Our class is building a cozy reading nook! You are the designer, and every rug and mat must fit.",
                objectives=["Count unit squares", "Multiply to find area", "Split rectangles to find area"],
                materials=["Pencil", "Grid paper", "Colored pencils"], tasks=tasks,
                extension=("Find two different rugs that each cover 24 square feet.", "Examples: 4 by 6, 3 by 8, 2 by 12"))


def rug_example(limit):
    a, b = max(((x, y) for x in range(2, 10) for y in range(x, 12) if x * y <= limit), key=lambda t: (t[0] * t[1], t[0]))
    return f"{b} by {a} = {a * b} square feet"


# =================================================================== Unit 11
@project("perimeter-shapes", ["perimeter-shapes"], "math3-project-playground-design", "playground-design", "Playground Designer",
         "Fence the play areas, compare perimeter and area, and use quadrilaterals in the design.",
         "Students design a playground. They find perimeters and missing side lengths for fences, compare rectangles with the same perimeter and different areas, sort quadrilateral play pads and split a garden into equal areas.",
         "Design & Building", "Playground Blueprint", 2, ["3.MD.D.8", "3.G.A.1", "3.G.A.2"],
         ["I can find perimeter and unknown side lengths.", "I can show rectangles with the same perimeter and different areas.",
          "I can classify quadrilaterals and split a shape into equal areas."],
         ["Area of rectangles (Unit 10)", "Adding within 100"],
         ["Grid paper", "Rulers", "Colored pencils", "Shape cards (printable support page)"],
         ["Day 1 (45 min): fences and same-perimeter sandboxes (Parts 1–2).", "Day 2 (45 min): shapes and the garden (Parts 3–4) and the blueprint."],
         ["Distinguish perimeter (around) and area (inside) every time.", "Use the attribute checklist for each quadrilateral.",
          "Advanced students find the greatest area for a fixed fence and explain the pattern."])
def pr11(L):
    w, h = {"cp2": (8, 5), "cp1": (14, 9), "honors": (18, 12)}[L]
    P = {"cp2": 12, "cp1": 16, "honors": 20}[L]
    rects = [(x, P // 2 - x) for x in range(1, P // 4 + 1)]
    best = max(rects, key=lambda t: t[0] * t[1])
    sides = {"cp2": [6, 4, 6, 4], "cp1": [12, 9, 7, 10], "honors": [15, 11, 9, 13]}[L]
    Pk = sum(sides)
    tasks = [("Fence the Field", f"The grass field is a rectangle {w} meters long and {h} meters wide.",
              T(L, ("How many meters of fence go all the way around?", f"{2 * (w + h)} meters", f"{w} + {h} + {w} + {h}."),
                (f"The fence around the climbing area is {Pk} meters. Three sides are {sides[0]}, {sides[1]} and {sides[2]} meters. How long is the fourth side?", f"{sides[3]} meters", "Add the three sides, then subtract from the perimeter.")), None),
             ("Sandbox Choices", f"You have {P} meters of border for a rectangular sandbox (whole-number sides).",
              T(L, ("List the rectangles you can make and the area of each.", "; ".join(f"{a} by {b}: area {a * b}" for a, b in rects), f"Length + width = {P // 2}."),
                ("Which sandbox has the most space to play?", f"{best[0]} by {best[1]} (area {best[0] * best[1]} square meters)", "Compare the areas.")),
              [["Length", "Width", "Perimeter", "Area"]] + [[str(b), str(a), str(P), str(a * b) if L == "cp2" and i == 0 else ""] for i, (a, b) in enumerate(rects)]),
             ("Play Pads", "The play pads are shapes: a square, a rectangle, a rhombus and a trapezoid.",
              T(L, ("Which pads are quadrilaterals?", "All four.", "Count the sides."),
                ("Which pad is both a rectangle and a rhombus?", "The square.", "4 right angles AND 4 equal sides."),
                ("Draw a quadrilateral that is not a rectangle, rhombus or square.", "Answers vary, e.g. a trapezoid or a kite.", "Change the angles or side lengths.")), None),
             ("Garden Corner", "A square garden is split into 4 parts with equal area for 4 classes.",
              T(L, ("What fraction of the garden does each class get?", "1/4", "4 equal parts."),
                ("Show two different ways to split it.", "Answers vary, e.g. 4 strips or 4 triangles from the diagonals.", "Equal area does not need the same shape.")), None)]
    if L == "honors":
        tasks.append(("Pattern Hunt", "Look at your sandbox table.",
                      T(L, ("What happens to the area as the rectangle gets closer to a square?", "The area gets larger.", None),
                        ("Use the pattern to predict the largest area for 24 meters of border.", "6 by 6: 36 square meters", None)), None))
    return dict(scenario="The school is building a new playground, and you are the designer! Fences, sandboxes, play pads and a garden all need careful math.",
                objectives=["Find perimeter and missing sides", "Compare perimeter and area", "Classify quadrilaterals", "Split shapes into equal areas"],
                materials=["Pencil", "Grid paper", "Ruler"], tasks=tasks,
                extension=("Find two rectangles with an area of 12 square meters and different perimeters.", "Examples: 3 by 4 (perimeter 14) and 2 by 6 (perimeter 16)"))


# =================================================================== Cumulative 1 (Units 1–5)
@project("cumulative-fun-fair", ["multiplication-meaning", "division-meaning", "properties-fact-strategies", "addition-subtraction-1000", "patterns-unknowns-two-step"],
         "math3-project-school-fun-fair", "school-fun-fair", "School Fun Fair",
         "Run game booths, share prizes and balance the fair budget (Units 1–5).",
         "A cumulative project for Units 1–5. Students plan a school fun fair: tickets sold in equal groups, prizes shared equally among booths, fact strategies for prices, totals within 1,000 with rounding, and two-step budget problems with equations.",
         "Events & Planning", "Fun Fair Plan", 3, ["3.OA.A.1", "3.OA.A.2", "3.OA.A.3", "3.OA.A.4", "3.OA.B.5", "3.OA.C.7", "3.OA.D.8", "3.NBT.A.1", "3.NBT.A.2", "3.NBT.A.3"],
         ["I can multiply and divide within 100 to solve equal-group problems.", "I can add and subtract within 1,000 and round to estimate.",
          "I can write and solve two-step equations and check that the answer is reasonable."],
         ["Units 1–5 of 3rd Grade Math"],
         ["Pencils", "Booth cards and ticket sheet (printable support page)", "Play money (optional)", "Poster paper"],
         ["Day 1 (45 min): tickets and prizes (Parts 1–2).", "Day 2 (45 min): sales totals and rounding (Part 3).", "Day 3 (45 min): the budget and the final plan (Part 4); presentations."],
         ["Use this after Unit 5 as a review; each part names the unit it reviews.", "Groups of 3–4 work well; rotate the recorder role.",
          "Advanced students decide how many prizes to buy within a budget and defend their choice."], cumulative=True)
def prc1(L):
    booths = {"cp2": 4, "cp1": 6, "honors": 8}[L]
    tix = {"cp2": 5, "cp1": 8, "honors": 9}[L]
    kids = {"cp2": 9, "cp1": 7, "honors": 9}[L]
    prizes = {"cp2": 24, "cp1": 48, "honors": 72}[L]
    sales = {"cp2": [215, 168], "cp1": [348, 279], "honors": [486, 397]}[L]
    def r100(n): return (n + 50) // 100 * 100
    tasks = [("Tickets (Unit 1)", f"Each child buys a strip of {tix} tickets. {kids} children buy strips at the first table.",
              T(L, ("How many tickets were sold at the first table?", f"{tix * kids} tickets", f"{kids} groups of {tix}."),
                (f"Use a strategy to check {kids} × {tix}.", f"Example: ({kids} × 5) + ({kids} × {tix - 5}) = {kids * tix}" if tix > 5 else f"Example: skip count by 5s {kids} times = {kids * tix}", "Break apart or skip count.")), None),
             ("Prizes (Units 2–3)", f"{prizes} prizes are shared equally among {booths} booths.",
              T(L, ("How many prizes does each booth get?", f"{prizes // booths} prizes", f"{prizes} ÷ {booths}: think {booths} × ? = {prizes}."),
                ("Write the fact family.", f"{booths} × {prizes // booths} = {prizes}, {prizes // booths} × {booths} = {prizes}, {prizes} ÷ {booths} = {prizes // booths}, {prizes} ÷ {prizes // booths} = {booths}", "Four facts with the same three numbers.")), None),
             ("Sales (Unit 4)", f"Morning sales were {sales[0]} tickets and afternoon sales were {sales[1]} tickets.",
              T(L, ("How many tickets were sold in all?", f"{sum(sales)} tickets", "Add and regroup."),
                ("How many more tickets were sold in the morning?", f"{sales[0] - sales[1]} tickets", "Subtract and check by adding."),
                ("Round each number to the nearest 100 and estimate the total. Is your exact total reasonable?", f"{r100(sales[0])} + {r100(sales[1])} = {r100(sales[0]) + r100(sales[1])}; yes, {sum(sales)} is close.", "Round, then add.")), None),
             ("Budget (Unit 5)", "Each booth needs 3 bags of 20 balloons, and a bag costs 4 dollars.",
              T(L, (f"Write an equation with b for the balloons needed for all {booths} booths.", f"b = {booths} × (3 × 20)", "Find one booth first."),
                ("Solve for b.", f"b = {booths * 60} balloons", "3 × 20 = 60."),
                (f"How much do all the bags cost?", f"{booths * 3 * 4} dollars", f"{booths} × 3 bags × 4 dollars.")), None)]
    if L == "honors":
        tasks.append(("Prize Plan", "The fair has 300 dollars for prizes. Small prizes cost 3 dollars and big prizes cost 9 dollars.",
                      T(L, (f"Each booth needs the same number of big prizes and 6 small prizes. How many big prizes can each of the {booths} booths get?",
                            f"{(300 - booths * 6 * 3) // (booths * 9)} big prizes each ({booths} × 6 × 3 = {booths * 18} dollars for small prizes, leaving {300 - booths * 18}; {booths} × 9 × {(300 - booths * 6 * 3) // (booths * 9)} = {booths * 9 * ((300 - booths * 6 * 3) // (booths * 9))})", None),
                        ("Explain how you know your answer stays within the budget.", "Answers vary; must show the total cost is at most 300 dollars.", None)), None))
    return dict(scenario="The school is holding a fun fair! Your team plans tickets, prizes, sales and the balloon budget.",
                objectives=["Multiply and divide", "Use properties and strategies", "Add, subtract and round", "Solve two-step problems"],
                materials=["Pencil", "Booth cards", "Poster paper"], tasks=tasks,
                extension=("If 30 more tickets are sold in the evening, what is the new total? Round it to the nearest 10.", f"{sum(sales) + 30} tickets; about {(sum(sales) + 35) // 10 * 10}"))


# =================================================================== Cumulative 2 (Units 6–11)
@project("cumulative-community-garden", ["understanding-fractions", "equivalent-comparing-fractions", "time-volume-mass", "graphs-measurement-data", "area", "perimeter-shapes"],
         "math3-project-community-garden-festival", "community-garden-festival", "Community Garden Festival",
         "Design garden beds, schedule watering, graph the harvest and fence the plots (Units 6–11).",
         "A cumulative project for Units 6–11. Students design a community garden: beds split into fractions, equivalent and compared plantings, a watering schedule with liters and elapsed time, a harvest graph and line plot, and bed areas and fence perimeters.",
         "Gardens & Nature", "Garden Festival Plan", 3, ["3.NF.A.1", "3.NF.A.3.b", "3.NF.A.3.d", "3.MD.A.1", "3.MD.A.2", "3.MD.B.3", "3.MD.B.4", "3.MD.C.7.b", "3.MD.C.7.d", "3.MD.D.8", "3.G.A.2"],
         ["I can name, compare and find equivalent fractions of a garden bed.", "I can solve time, liquid volume and mass problems.",
          "I can graph data and find area and perimeter of garden plots."],
         ["Units 6–11 of 3rd Grade Math"],
         ["Grid paper", "Rulers marked in quarter inches", "Colored pencils", "Harvest data card and bed templates (printable support page)"],
         ["Day 1 (45 min): beds and fractions (Parts 1–2).", "Day 2 (45 min): watering schedule and harvest graph (Parts 3–4).", "Day 3 (45 min): area and fences (Part 5) and the festival plan."],
         ["Use this after Unit 11 as a review; each part names the unit it reviews.", "Groups of 3–4; each student is responsible for one part of the final plan.",
          "Advanced students design the bed layout under area and perimeter limits and justify it."], cumulative=True)
def prc2(L):
    w, h = {"cp2": (4, 2), "cp1": (6, 4), "honors": (8, 6)}[L]
    tom = {"cp2": 1, "cp1": 3, "honors": 3}[L]
    water = {"cp2": (3, 4), "cp1": (6, 5), "honors": (8, 7)}[L]
    start = {"cp2": (8, 15), "cp1": (8, 40), "honors": (8, 45)}[L]
    mins = {"cp2": 30, "cp1": 35, "honors": 50}[L]
    def add(hh, m, k):
        t = hh * 60 + m + k
        return f"{(t // 60 - 1) % 12 + 1}:{t % 60:02d}"
    harvest = {"Beans": 30, "Carrots": 45, "Squash": 20, "Peppers": 35}
    tasks = [("Fraction Beds (Unit 6)", "Bed A is split into 8 equal parts.",
              T(L, (f"Tomatoes fill {tom} parts. What fraction is tomatoes?", f"{tom}/8", "Count the tomato parts out of 8."),
                ("Where is 3/8 on a number line from 0 to 1 marked in eighths?", "3 jumps of 1/8 from 0", "Count jumps, not tick marks.")), None),
             ("Equal and Compare (Unit 7)", "Bed B is split into 4 equal parts. Bed C is the same size as Bed A.",
              T(L, ("Herbs fill 2/4 of Bed B. How many eighths of Bed A is the same amount?", "4/8", "Split each fourth into 2 parts."),
                ("Compare 3/8 and 3/4 of the same size bed. Which is more?", "3/4 > 3/8", "Same numerator: bigger pieces win.")), None),
             ("Watering Day (Unit 8)", f"Watering starts at {start[0]}:{start[1]:02d} and takes {mins} minutes. The garden uses {water[0]} cans of {water[1]} liters.",
              T(L, ("What time does watering end?", add(*start, mins), "Jump to the next hour, then the rest."),
                ("How many liters of water are used?", f"{water[0] * water[1]} liters", f"{water[0]} × {water[1]}.")), None),
             ("Harvest Graph (Unit 9)", "The harvest (in pounds) is shown in the table. Make a bar graph with a scale of 5.",
              T(L, ("How many more pounds of carrots than squash?", "25 pounds", "Subtract."),
                ("How many fewer pounds of beans than carrots and squash together?", "35 pounds", "Add carrots and squash first.")),
              [["Crop", "Pounds"]] + [[k, str(v)] for k, v in harvest.items()]),
             ("Plots and Fences (Units 10–11)", f"Each bed is a rectangle {w} feet by {h} feet.",
              T(L, ("What is the area of one bed?", f"{w * h} square feet", "Length × width."),
                ("How many feet of fence go around one bed?", f"{2 * (w + h)} feet", "Add all four sides."),
                ("Two beds are placed side by side along their long sides to make one big rectangle. What is its area?", f"{2 * w * h} square feet", "Add the two areas.")), None)]
    if L == "honors":
        tasks.append(("Design Challenge", "Design an L‑shaped herb garden with area 30 square feet using two rectangles.",
                      T(L, ("Give side lengths for both rectangles and show the total area.", "Answers vary; e.g. 5 × 4 + 2 × 5 = 30.", None),
                        ("Find the perimeter of your L shape.", "Answers vary; must add every outside side.", None)), None))
    return dict(scenario="Our town is holding a garden festival! Your team plans the beds, the watering, the harvest report and the fences.",
                objectives=["Use fractions of a garden bed", "Solve time and liquid volume problems", "Graph harvest data", "Find area and perimeter"],
                materials=["Pencil", "Grid paper", "Ruler"], tasks=tasks,
                extension=("A 1‑yard ribbon is cut into fourths for prize ribbons. How many prize ribbons from 3 yards?", "12 prize ribbons"))
