"""Grade 2 projects: one per unit plus two cumulative projects. Every answer is computed here, so the student packets,
the teacher solutions and the rubric can never disagree.

The three versions differ in SUPPORT and REASONING, not only in numbers:
  cp2 Remedial  – smaller numbers, a hint for each question, sentence frames, fewer free choices.
  cp1 Standard  – the full task set at grade level; students choose their own strategies.
  honors Advanced – the same context with an open design challenge, error analysis and a written justification (no hints).
Each level returns: scenario, objectives, materials, tasks [(title, intro, [(question, answer, hint)], table)], extension (q, a).
Materials are inexpensive classroom supplies; no accounts, paid products or student personal data are needed."""

LV = ["cp2", "cp1", "honors"]
LNAME = {"cp2": "Remedial", "cp1": "Standard", "honors": "Advanced"}
P = {}


def project(key, units, folder, slug, title, tagline, description, theme, product, days, standards, targets, prereqs, materials, timing, notes, cumulative=False):
    def deco(fn):
        P[key] = dict(key=key, units=units, unit=units[0], folder=folder, slug=slug, title=title, tagline=tagline, description=description, theme=theme, product=product,
                      days=days, standards=standards, targets=targets, prereqs=prereqs, materials=materials, timing=timing, notes=notes, cumulative=cumulative, build=fn)
        return fn
    return deco


def T(L, *rows):
    """rows of (question, answer, hint); hints appear only in the Remedial packet."""
    return [(q, a, h if L == "cp2" else None) for q, a, h in rows]


def pick3(L, a, b, c):
    return {"cp2": a, "cp1": b, "honors": c}[L]


def pl(n, one, many=None):
    return f"{n} {one}" if n == 1 else f"{n} {many or one + 's'}"


def coins_value(q=0, d=0, n=0, p=0):
    return 25 * q + 10 * d + 5 * n + p


def fewest_words(c):
    out = []
    for v, one, many in ((25, "quarter", "quarters"), (10, "dime", "dimes"), (5, "nickel", "nickels"), (1, "penny", "pennies")):
        k, c = divmod(c, v)
        if k:
            out.append(f"{k} {one if k == 1 else many}")
    return ", ".join(out)


# =================================================================== Unit 1
@project("add-subtract-20", ["add-subtract-20"], "math2-project-snack-stand", "snack-stand", "Snack Stand Facts",
         "Run a class snack stand and use fact strategies to count every snack.",
         "Students run a pretend snack stand. They add and subtract snack counts within 20 with make-a-ten and doubles, find missing numbers, and build a fact family menu board.",
         "Food & Shopping", "Fact Family Menu Board", 2, ["2.OA.B.2"],
         ["I can add within 20 using make a ten and doubles.", "I can subtract within 20 by thinking addition.", "I can write a fact family and find a missing number."],
         ["Count to 20 and add within 10 (Grade 1)"],
         ["Two-color counters or cubes (20 per pair)", "Ten-frame mats (printable support page)", "Pencils and crayons", "Paper for the menu board"],
         ["Day 1 (40 min): count snacks with ten frames; Parts 1–2.", "Day 2 (40 min): missing numbers and the fact family menu board (Parts 3–4)."],
         ["Have students show make-a-ten on two ten frames before writing equations.", "Ask “What fact do you already know that helps?” for every problem.",
          "Advanced students design a menu where every price pair makes a ten and explain their choices."])
def p01(L):
    a, b = pick3(L, (8, 5), (9, 7), (8, 9))
    w, part = pick3(L, (13, 6), (16, 9), (17, 8))
    tasks = [("Counting Snacks", f"The stand has {a} apples and {b} bananas.",
              T(L, ("How many pieces of fruit are there?", f"{a + b}", f"Make a ten: {a} + {10 - a} = 10, then add the rest."),
                (f"Show how you made a ten. {a} + {b} = 10 + ___", f"{a + b - 10}", f"Break {b} into {10 - a} and {b - (10 - a)}.")),
              [["Snack", "How many"], ["apples", str(a)], ["bananas", str(b)], ["total", ""]]),
             ("Selling Snacks", f"There were {w} granola bars. The stand sold {part}.",
              T(L, ("How many granola bars are left?", f"{w - part}", f"Think: {part} + ___ = {w}."),
                ("Write the addition fact you used to check.", f"{part} + {w - part} = {w}", "The parts add up to the whole.")), None),
             ("Missing Numbers", "Find the number that makes each equation true.",
              T(L, ("7 + ___ = 15", "8", "Count up from 7 to 15."), ("___ − 6 = 9", "15", "Think 9 + 6."), ("6 + 6 = 5 + ___", "7", "Both sides must equal 12.")), None)]
    if L == "honors":
        tasks.append(("Menu Challenge", "Every snack costs a whole number of tickets from 1 to 9. A combo is two snacks.",
                      T(L, ("Find three different combos that cost exactly 10 tickets.", "Answers vary, e.g. 1 + 9, 2 + 8, 3 + 7, 4 + 6.", None),
                        ("A combo costs 17 tickets. One snack costs 9. Kai says the other costs 6. Is he right? Explain.", "No. 9 + 8 = 17, so the other snack costs 8 tickets.", None),
                        ("Write the fact family for 9, 8 and 17.", "9 + 8 = 17, 8 + 9 = 17, 17 − 9 = 8, 17 − 8 = 9", None)), None))
    else:
        tasks.append(("Fact Family Menu Board", "Pick three snacks and make a fact family for each pair of numbers on your menu board.",
                      T(L, ("Write one fact family with a sum from 11 to 18.", "Answers vary; all four facts must use the same three numbers.", "Frame: __ + __ = __, __ + __ = __, __ − __ = __, __ − __ = __")), None))
    return dict(scenario="Our class is running a snack stand! Count the snacks, keep track of sales, and make a menu board of fact families.",
                objectives=["Add within 20 with strategies", "Subtract within 20 by thinking addition", "Write fact families"],
                materials=["Pencil", "Counters", "Ten-frame mats"], tasks=tasks,
                extension=("The stand gets 9 more apples and 9 more bananas. How many new pieces of fruit? Use a double.", "18 (9 + 9)"))


# =================================================================== Unit 2
@project("odd-even-arrays", ["odd-even-arrays"], "math2-project-classroom-seating", "classroom-seating", "Classroom Seating Plan",
         "Pair up partners and set the desks in neat arrays.",
         "Students plan seats for a class event. They decide whether groups can be made into partners (odd or even), write even numbers as doubles, and arrange chairs in arrays with up to 5 rows and 5 columns.",
         "School & Community", "Seating Plan", 2, ["2.OA.C.3", "2.OA.C.4", "2.G.A.2"],
         ["I can tell if a group up to 20 is odd or even by making pairs.", "I can write an even number as two equal addends.", "I can find the total in an array and write a repeated-addition equation."],
         ["Count by 2s and 5s", "Add within 20"],
         ["Counters or cubes (25 per pair)", "Grid paper (printable support page)", "Crayons"],
         ["Day 1 (40 min): partners and doubles (Parts 1–2).", "Day 2 (40 min): chair arrays and the seating plan (Parts 3–4)."],
         ["Let students line up counters in two rows to check for a partner.", "Say “rows go across” and point while counting rows.",
          "Advanced students find every array (up to 5 by 5) for a given number of chairs and explain which numbers have no array other than one row."])
def p02(L):
    groups = pick3(L, [10, 7], [14, 17], [19, 16])
    r, c = pick3(L, (3, 4), (4, 5), (5, 5))
    tasks = [("Partners", "Each group of children needs partners.",
              T(L, *[(f"A group has {n} children. Can everyone have a partner? Is {n} odd or even?", f"{'Yes, even' if n % 2 == 0 else 'No, odd'} ({n // 2} pairs{', 1 left over' if n % 2 else ''})", "Make pairs with counters.") for n in groups]), None),
             ("Doubles", "Write each even number as two equal addends.",
              T(L, *[(f"{n} = ___ + ___", f"{n // 2} + {n // 2}", "Split into two equal rows.") for n in [x for x in groups if x % 2 == 0] + [pick3(L, 8, 12, 18)]]), None),
             ("Chair Arrays", f"Chairs are set in {r} rows with {c} chairs in each row.",
              T(L, ("How many chairs are there?", f"{r * c} chairs", f"Add {c} for each row."),
                ("Write a repeated-addition equation for the rows.", " + ".join([str(c)] * r) + f" = {r * c}", "One addend for each row."),
                ("Write a repeated-addition equation for the columns.", " + ".join([str(r)] * c) + f" = {r * c}", "One addend for each column.")), None)]
    if L == "honors":
        tasks.append(("Array Challenge", "The class has 12 chairs. Rows can have up to 5 chairs and there can be up to 5 rows.",
                      T(L, ("List every array you can make with all 12 chairs.", "3 rows of 4 and 4 rows of 3 (2 rows of 6 and 6 rows of 2 do not fit)", None),
                        ("Is 12 odd or even? How does an array with 2 equal rows show this?", "Even: 2 equal rows of 6 means every chair has a partner.", None),
                        ("Mia says 13 chairs can make an array with 2 equal rows. Explain why not.", "13 is odd, so 2 equal rows leave 1 chair over (6 + 6 = 12).", None)), None))
    else:
        tasks.append(("Seating Plan", "Draw your seating plan as an array on grid paper.",
                      T(L, ("How many rows and how many chairs in each row? Write the equation.", "Answers vary; the equation must match the drawing.", "Frame: “I made __ rows of __, so __ + __ … = __.”")), None))
    return dict(scenario="Our class is hosting a reading party! Plan partners for games and set up the chairs in neat rows.",
                objectives=["Decide odd or even", "Write doubles", "Use arrays and repeated addition"],
                materials=["Pencil", "Counters", "Grid paper"], tasks=tasks,
                extension=("Two more rows of the same size are added. How many chairs now?", f"{(r + 2) * c} chairs"))


# =================================================================== Unit 3
@project("place-value-1000", ["place-value-1000"], "math2-project-bead-shop", "bead-shop", "Bead Shop Bundles",
         "Pack beads in bags of ten and boxes of a hundred, then fill orders.",
         "Students run a bead shop. Beads come in single beads, bags of 10 and boxes of 100. They pack orders, write order numbers with digits, words and expanded form, and explain place value.",
         "Crafts & Art", "Bead Order Cards", 2, ["2.NBT.A.1", "2.NBT.A.1.a", "2.NBT.A.1.b", "2.NBT.A.3"],
         ["I can explain that 100 is ten tens.", "I can tell how many hundreds, tens, and ones are in a number.", "I can write numbers with digits, words, and expanded form."],
         ["Count to 120 (Grade 1)", "Tens and ones to 100"],
         ["Base-ten blocks or paper base-ten cutouts (printable support page)", "Small cups or bags as “bags of 10”", "Index cards for order cards"],
         ["Day 1 (40 min): bags and boxes with base-ten blocks (Parts 1–2).", "Day 2 (40 min): writing orders three ways and the order cards (Parts 3–4)."],
         ["Use real bundles: 10 cubes in a cup, 10 cups make a box.", "Have students say the value of each digit aloud.",
          "Advanced students find different ways to pack the same number (e.g. 3 boxes and 14 bags) and explain why they are equal."])
def p03(L):
    orders = pick3(L, [245, 130], [406, 382], [705, 590])
    tasks = [("Bags and Boxes", "A bag holds 10 beads. A box holds 10 bags.",
              T(L, ("How many beads are in one box?", "100 beads", "10 tens = 1 hundred."),
                (f"How many bags make {pick3(L, 300, 500, 800)} beads?", f"{pick3(L, 300, 500, 800) // 10} bags", "Each box is 10 bags.")), None),
             ("Packing Orders", "Pack each order with boxes, bags, and single beads.",
              T(L, *[(f"Order: {n} beads. How many boxes, bags, and single beads?", f"{pl(n // 100, 'box', 'boxes')}, {pl(n // 10 % 10, 'bag')}, {pl(n % 10, 'single bead')}", "Hundreds, tens, ones.") for n in orders]),
              [["Order", "Boxes (100)", "Bags (10)", "Single beads (1)"]] + [[str(n), "", "", ""] for n in orders]),
             ("Writing Orders", "Write each order three ways.",
              T(L, *[(f"Write {n} in expanded form.", " + ".join(str(x) for x in (n // 100 * 100, n // 10 % 10 * 10, n % 10) if x), "Write the value of each digit.") for n in orders]), None)]
    if L == "honors":
        tasks.append(("Packing Puzzle", "The shop is out of boxes, so it packs with bags and single beads only.",
                      T(L, (f"How many bags and single beads make {orders[0]}?", f"{orders[0] // 10} bags and {orders[0] % 10} single beads", None),
                        ("Leo packed 3 boxes and 14 bags. Ana packed 4 boxes and 4 bags. Who packed more beads? Explain.", "They packed the same: 300 + 140 = 440 and 400 + 40 = 440.", None),
                        ("Uma wrote seven hundred five as 7005. Explain the mistake.", "Seven hundred five is 7 hundreds, 0 tens, 5 ones: 705.", None)), None))
    else:
        tasks.append(("Order Cards", "Make an order card for a number of beads you choose from 100 to 999.",
                      T(L, ("Write the number in digits, in words, and in expanded form, and draw the boxes, bags and beads.", "Answers vary; all forms must show the same number.", "Frame: “__ boxes, __ bags, __ beads is __.”")), None))
    return dict(scenario="Welcome to the bead shop! Beads come one at a time, in bags of ten, and in boxes of one hundred. Fill the orders!",
                objectives=["Understand hundreds as ten tens", "Find hundreds, tens and ones", "Write numbers three ways"],
                materials=["Pencil", "Base-ten blocks", "Index cards"], tasks=tasks,
                extension=("An order is 9 boxes, 9 bags and 9 beads. One more bead is added. What is the new number?", "1,000 beads (999 + 1)"))


# =================================================================== Unit 4
@project("count-compare-1000", ["count-compare-1000"], "math2-project-library-shelves", "library-shelves", "Library Shelf Hunt",
         "Find books by number, count along the shelves and compare book numbers.",
         "Students help a librarian. Books have numbers from 100 to 999. They count on and skip count to find books, compare book numbers with >, = and <, and use 10 more, 10 less, 100 more and 100 less to move along the shelves.",
         "Books & Reading", "Shelf Map", 2, ["2.NBT.A.2", "2.NBT.A.4", "2.NBT.B.8"],
         ["I can count and skip count within 1,000.", "I can compare three-digit numbers with >, =, and <.", "I can find 10 or 100 more or less than a number."],
         ["Place value to 1,000 (Unit 3)"],
         ["Sticky notes for book numbers", "Number chart pages (printable support page)", "Pencils"],
         ["Day 1 (40 min): counting along the shelves (Parts 1–2).", "Day 2 (40 min): comparing and moving by 10s and 100s; shelf map (Parts 3–4)."],
         ["Post book-number sticky notes in a line on the wall for counting practice.", "Ask “Which place changed?” after every 10 or 100 move.",
          "Advanced students design a shelf rule and order mixed book numbers."])
def p04(L):
    s = pick3(L, 296, 597, 895)
    a, b = pick3(L, (345, 354), (628, 682), (509, 590))
    n = pick3(L, 450, 693, 805)
    tasks = [("Counting Along the Shelf", f"The books are in order starting at {s}.",
              T(L, ("Write the next five book numbers.", ", ".join(str(s + i) for i in range(1, 6)), "Count on by ones. Watch for a new hundred."),
                (f"Count by 10s from {s - 6}. Write the next four numbers.", ", ".join(str(s - 6 + 10 * i) for i in range(1, 5)), "Only the tens change, until you cross a hundred.")), None),
             ("Skip Counting Carts", "A cart holds 5 books, and a box holds 100 books.",
              T(L, ("Count by 5s: how many books on 7 carts?", "35 books", "5, 10, 15, …"),
                (f"Count by 100s from {pick3(L, 100, 200, 350)}: write four numbers.", ", ".join(str(pick3(L, 100, 200, 350) + 100 * i) for i in range(4)), "The hundreds digit goes up by 1.")), None),
             ("Comparing Book Numbers", "Compare with >, =, or <.",
              T(L, (f"{a} ___ {b}", "<" if a < b else ">", "Hundreds first, then tens."),
                (f"Put in order from least to greatest: {b}, {a}, {a - 100}", f"{a - 100}, {min(a, b)}, {max(a, b)}", "Compare the hundreds digits first.")), None),
             ("Moving Along", f"Start at book {n}.",
              T(L, ("What is 10 more?", str(n + 10), "Tens digit + 1."), ("What is 100 less?", str(n - 100), "Hundreds digit − 1."),
                ("What is 10 less?", str(n - 10), "Tens digit − 1.")), None)]
    if L == "honors":
        tasks.append(("Shelf Puzzle", "Explain your thinking.",
                      T(L, ("Ted says 389 > 401 because 8 and 9 are big digits. Is he right?", "No. Compare hundreds first: 3 < 4, so 389 < 401.", None),
                        ("What is the greatest digit that makes 6□4 < 654 true?", "4 (644 < 654, but 654 is not less than 654)", None)), None))
    return dict(scenario="The school librarian needs help! Every book has a number, and the shelves are out of order.",
                objectives=["Count and skip count", "Compare three-digit numbers", "Find 10 or 100 more or less"],
                materials=["Pencil", "Number chart", "Sticky notes"], tasks=tasks,
                extension=("Start at 995. Count on by ones to 1,000. What numbers do you say?", "996, 997, 998, 999, 1,000"))


# =================================================================== Unit 5
@project("add-subtract-100", ["add-subtract-100"], "math2-project-points-store", "points-store", "Class Points Store",
         "Shop the class points store and explain your adding and subtracting strategies.",
         "Students spend class reward points (not real money) at a pretend store. They add and subtract within 100 with place value, add up to four prices, check with the related operation, and explain strategies.",
         "Shopping & Stores", "Shopping Plan", 2, ["2.NBT.B.5", "2.NBT.B.6", "2.NBT.B.9"],
         ["I can add and subtract within 100 using place value.", "I can add up to four two-digit numbers.", "I can explain why my strategy works."],
         ["Tens and ones to 100", "Facts within 20 (Unit 1)"],
         ["Base-ten blocks", "Price cards (printable support page)", "Open number line strips", "Pencils"],
         ["Day 1 (40 min): shopping with two prices (Parts 1–2).", "Day 2 (40 min): four-item baskets, checking and explaining (Parts 3–4)."],
         ["Ask students to say what happened to the tens and ones.", "Use blocks to show trading 10 ones for 1 ten.",
          "Advanced students plan a basket that uses exactly their points and compare two strategies."])
def p05(L):
    have = pick3(L, 60, 85, 100)
    a, b = pick3(L, (23, 14), (37, 28), (48, 37))
    items = pick3(L, [12, 15, 21], [18, 26, 14, 32], [27, 19, 36, 15])
    tasks = [("Two Prizes", f"A sticker pack costs {a} points and a pencil costs {b} points.",
              T(L, ("How many points do both cost?", f"{a + b} points", "Add tens, then ones."),
                (f"You have {have} points. How many points are left after you buy both?", f"{have - a - b} points", f"{have} − {a + b}.")), None),
             ("Checking", f"Mia had {have} points and spent {a}. She says she has {have - a} left.",
              T(L, ("Check with addition. Is she right?", f"Yes: {have - a} + {a} = {have}", "Add the answer and the points spent.")), None),
             ("Basket of Prizes", "Add all the prices in the basket.",
              T(L, ("Prices: " + ", ".join(map(str, items)) + ". What is the total?", f"{sum(items)} points", "Look for numbers that make a ten.")),
              [["Prize", "Points"]] + [[f"Prize {i + 1}", str(v)] for i, v in enumerate(items)] + [["Total", ""]]),
             ("Explain a Strategy", f"Find {a + b + 10} − {b}.",
              T(L, ("Solve it and explain your strategy with tens and ones.", f"{a + 10}. For example: count up from {b} or break apart {b} into tens and ones.", "Frame: “I broke ___ into ___ and ___ because …”")), None)]
    if L == "honors":
        tasks.append(("Exact Points", f"You have exactly {have} points. Prizes cost 15, 22, 28, 35 and 40 points.",
                      T(L, (f"Find prizes that use all {have} points. Show your adding.", "Answers vary, e.g. 15 + 22 + 28 + 35 = 100.", None),
                        ("Ben says 47 + 36 = 713. Explain his mistake and find the correct sum.", "He wrote 13 ones in the ones place. 47 + 36 = 83.", None)), None))
    return dict(scenario="Our class earned reward points! Spend them at the class store and keep track of every point.",
                objectives=["Add and subtract within 100", "Add up to four numbers", "Explain strategies"],
                materials=["Pencil", "Base-ten blocks", "Price cards"], tasks=tasks,
                extension=("The store has a sale: every prize costs 10 points less. What does the basket cost now?", f"{sum(items) - 10 * len(items)} points"))


# =================================================================== Unit 6
@project("word-problems-100", ["word-problems-100"], "math2-project-zoo-stories", "zoo-stories", "Zoo Story Problems",
         "Write and solve zoo story problems with bar models and equations.",
         "Students visit a pretend zoo. They solve add-to, take-from, put-together, take-apart and compare stories with unknowns in every position, draw bar models, and write their own two-step story problem book.",
         "Animals & Nature", "Story Problem Book", 2, ["2.OA.A.1"],
         ["I can solve one- and two-step word problems within 100.", "I can draw a bar model for a story.", "I can write an equation with a ? for the unknown."],
         ["Add and subtract within 100 (Unit 5)"],
         ["Bar-model strips (printable support page)", "Folded paper for the book", "Crayons"],
         ["Day 1 (40 min): stories with the result or a part unknown (Parts 1–2).", "Day 2 (40 min): compare and two-step stories; the story book (Parts 3–4)."],
         ["Have students act out a story before drawing the bar model.", "Ask “What do we know? What do we need?” for every story.",
          "Advanced students write stories with the start unknown and trade them with a partner."])
def p06(L):
    a, b = pick3(L, (18, 12), (36, 27), (48, 35))
    s = a + b
    tasks = [("Add To and Take From", "Solve each story. Write an equation with ?.",
              T(L, (f"There were {a} ducks in the pond. {b} more came. How many ducks now?", f"{s} ducks ({a} + {b} = ?)", "Add-to story."),
                (f"The zoo had {s} maps. Visitors took {b}. How many maps are left?", f"{a} maps ({s} − {b} = ?)", "Take-from story."),
                (f"Some seals were on a rock. {b} jumped off. {a} seals are still there. How many were there at first?", f"{s} seals (? − {b} = {a})", "The start is unknown. Add the parts.")), None),
             ("Put Together and Take Apart", f"The zoo has {s} birds. {a} are parrots and the rest are owls.",
              T(L, ("How many owls are there?", f"{b} owls ({a} + ? = {s})", "Draw a bar for the whole and the parts.")), None),
             ("Compare", f"The penguins ate {s} fish. The seals ate {b} fewer fish than the penguins.",
              T(L, ("How many fish did the seals eat?", f"{a} fish ({s} − {b} = ?)", "Fewer: the seals ate less, so subtract."),
                ("How many more fish did the penguins eat than the seals?", f"{b} fish", "The difference is the extra part of the longer bar.")), None),
             ("Two Steps", f"A tram had {a} riders. {b} got on and {pick3(L, 7, 15, 22)} got off.",
              T(L, ("How many riders are on the tram now?", f"{s - pick3(L, 7, 15, 22)} riders", "First add, then subtract.")), None)]
    if L == "honors":
        tasks.append(("Story Check", "Find and fix the mistake.",
                      T(L, (f"Kai solved: “Ana has {s} stickers. She has {b} more than Ben. How many does Ben have?” Kai wrote {s} + {b} = {s + b}. Fix it.", f"Ben has fewer: {s} − {b} = {a} stickers.", None),
                        ("Write a two-step zoo story whose answer is 40. Show the equations.", "Answers vary; both steps must be correct and the answer must be 40.", None)), None))
    else:
        tasks.append(("My Story Book", "Write two zoo stories: one add-to and one compare. Draw a bar model for each.",
                      T(L, ("Write, draw, and solve your stories.", "Answers vary; each bar model must match its equation.", "Frame: “There were __ … Then … How many …?”")), None))
    return dict(scenario="Welcome to the zoo! The zookeepers need help counting animals, food and visitors.",
                objectives=["Solve one-step stories with unknowns anywhere", "Solve compare stories", "Solve two-step stories"],
                materials=["Pencil", "Bar-model strips", "Paper for the book"], tasks=tasks,
                extension=("The zoo had 64 visitors before lunch and 29 after lunch. How many more came before lunch?", "35 more visitors"))


def trade_note(a, b):
    ro = a % 10 + b % 10 >= 10
    rt = a // 10 % 10 + b // 10 % 10 + ro >= 10
    if not ro and not rt:
        return "No. No place had 10 or more."
    return "Yes: " + " and ".join(x for x, f in (("the ones made a new ten", ro), ("the tens made a new hundred", rt)) if f) + "."


# =================================================================== Unit 7
@project("add-subtract-1000", ["add-subtract-1000"], "math2-project-recycling-drive", "recycling-drive", "Recycling Drive Report",
         "Total the cans each class collects and report the results.",
         "Students run a school recycling drive. They add and subtract three-digit numbers with base-ten models and written methods, compose and decompose tens and hundreds, and write a report of the results.",
         "Earth & Environment", "Recycling Report", 2, ["2.NBT.B.7", "2.NBT.B.9"],
         ["I can add three-digit numbers, making new tens and hundreds.", "I can subtract three-digit numbers, breaking apart tens and hundreds.", "I can explain my method with place value."],
         ["Place value to 1,000 (Unit 3)", "Adding and subtracting within 100 (Unit 5)"],
         ["Base-ten blocks or paper cutouts", "Collection data card (printable support page)", "Poster paper"],
         ["Day 1 (40 min): totals with blocks and written methods (Parts 1–2).", "Day 2 (40 min): differences and the report (Parts 3–4)."],
         ["Model each trade with blocks before writing it.", "Check every subtraction by adding.",
          "Advanced students find which two classes together collected closest to a goal and justify it."])
def p07(L):
    cans = pick3(L, {"Room 1": 234, "Room 2": 152, "Room 3": 315}, {"Room 1": 368, "Room 2": 247, "Room 3": 185}, {"Room 1": 476, "Room 2": 358, "Room 3": 129})
    goal = pick3(L, 500, 800, 1000)
    r1, r2, r3 = cans.values()
    tasks = [("Class Totals", "Use the collection card.",
              T(L, ("How many cans did Room 1 and Room 2 collect together?", f"{r1 + r2} cans", "Add hundreds, tens, ones."),
                ("Did you need to make a new ten or hundred? Explain.", trade_note(r1, r2), "Look at each place total.")),
              [["Class", "Cans"]] + [[k, str(v)] for k, v in cans.items()]),
             ("Comparing Classes", "Find the differences.",
              T(L, ("How many more cans did Room 1 collect than Room 3?" if r1 > r3 else "How many more cans did Room 3 collect than Room 1?", f"{abs(r1 - r3)} cans", "Subtract and check by adding."),
                ("How many more cans did Room 1 collect than Room 2?", f"{r1 - r2} cans", "Break apart a ten or hundred if needed.")), None),
             ("The Goal", f"The school goal is {goal} cans.",
              T(L, ("How many cans did all three rooms collect?", f"{r1 + r2 + r3} cans", "Add two rooms first, then the third."),
                ("Did they reach the goal? How many more or extra cans?", (f"Yes, {r1 + r2 + r3 - goal} extra cans" if r1 + r2 + r3 >= goal else f"No, {goal - r1 - r2 - r3} more cans needed"), "Compare the total with the goal.")), None)]
    if L == "honors":
        tasks.append(("Report Check", "Check the report.",
                      T(L, (f"Leo wrote {r1} − {r2} = {sum(abs(x - y) * p for x, y, p in zip(map(int, str(r1)), map(int, str(r2)), (100, 10, 1)))}. Explain the mistake.", f"He subtracted the smaller digit from the larger digit in each place. {r1} − {r2} = {r1 - r2}.", None),
                        ("Which two rooms together came closest to 600 cans? Show your work.", f"{min([('Room 1 and Room 2', r1 + r2), ('Room 1 and Room 3', r1 + r3), ('Room 2 and Room 3', r2 + r3)], key=lambda x: abs(x[1] - 600))[0]}", None)), None))
    else:
        tasks.append(("Recycling Report", "Make a report poster with the totals and one difference.",
                      T(L, ("Show one sum and one difference with blocks or a written method.", "Answers vary; work must match the data card.", "Frame: “Room __ collected __ more cans than Room __.”")), None))
    return dict(scenario="Our school is collecting cans to recycle! Every class counts its cans. Help total the results and write the report.",
                objectives=["Add within 1,000", "Subtract within 1,000", "Explain with place value"],
                materials=["Pencil", "Base-ten blocks", "Data card"], tasks=tasks,
                extension=("Next week Room 2 collects 100 more cans than this week. How many is that?", f"{r2 + 100} cans"))


# =================================================================== Unit 8
@project("measuring-length", ["measuring-length"], "math2-project-measure-my-classroom", "measure-my-classroom", "Measure My Classroom",
         "Measure classroom objects with the right tools and show the data on a line plot.",
         "Students measure real classroom objects. They choose rulers, yardsticks, meter sticks or measuring tapes, measure in two units, estimate first, compare lengths, and make a line plot of pencil lengths.",
         "School & Community", "Measurement Line Plot Poster", 2, ["2.MD.A.1", "2.MD.A.2", "2.MD.A.3", "2.MD.A.4", "2.MD.D.9"],
         ["I can choose a tool and measure to the nearest whole unit.", "I can estimate and compare lengths.", "I can show measurements on a line plot."],
         ["Count and compare numbers within 100"],
         ["Rulers (inches and centimeters)", "Yardstick or meter stick", "Measuring tape (paper tape works)", "Pencils of different lengths", "Line plot frame (printable support page)"],
         ["Day 1 (40 min): estimate and measure objects in two units (Parts 1–2).", "Day 2 (40 min): compare lengths and make the line plot (Parts 3–4)."],
         ["Check that every student starts at 0 on the ruler.", "Record estimates before measuring so students can compare.",
          "Advanced students explain why the inch and centimeter measurements are different numbers."])
def p08(L):
    pencils = pick3(L, [5, 6, 6, 7, 7, 7, 8], [4, 5, 5, 6, 6, 6, 7, 7, 8, 8], [3, 4, 5, 5, 6, 6, 6, 6, 7, 7, 8, 9])
    from collections import Counter
    cnt = Counter(pencils)
    mode = max(cnt, key=cnt.get)
    tasks = [("Estimate, Then Measure", "Estimate first. Then measure to the nearest inch.",
              T(L, ("Which tool will you use for a book? For the classroom door? For around a globe?", "ruler; yardstick or meter stick; measuring tape", "Short: ruler. Medium: yardstick. Long or curved: measuring tape."),
                ("Measure a crayon. Start at 0. How long is it?", "Answers vary (about 3 inches)", "Line up the end with 0.")),
              [["Object", "Estimate", "Measure (inches)", "Measure (centimeters)"], ["crayon", "", "", ""], ["book", "", "", ""], ["desk", "", "", ""]]),
             ("Two Units", "Measure the same book in inches and in centimeters.",
              T(L, ("Which number is greater: the inches or the centimeters? Why?", "Centimeters, because a centimeter is shorter than an inch, so it takes more of them.", "Which unit is smaller?")), None),
             ("How Much Longer?", "The desk is " + str(pick3(L, 24, 30, 36)) + " inches long. The book is " + str(pick3(L, 10, 11, 9)) + " inches long.",
              T(L, ("How much longer is the desk than the book?", f"{pick3(L, 24, 30, 36) - pick3(L, 10, 11, 9)} inches", "Subtract the lengths.")), None),
             ("Line Plot", "The table shows pencil lengths in inches. Make a line plot.",
              T(L, ("Which length has the most pencils?", f"{mode} inches", "Find the tallest stack of X marks."),
                ("How much longer is the longest pencil than the shortest?", f"{max(pencils) - min(pencils)} inches", "Longest − shortest."),
                ("How many pencils were measured?", str(len(pencils)), "Each X is one pencil.")),
              [["Pencil", "Length (inches)"]] + [[str(i + 1), str(v)] for i, v in enumerate(pencils)])]
    if L == "honors":
        tasks.append(("Measure Check", "Explain your thinking.",
                      T(L, ("Uma measured a ribbon from the 2 mark to the 9 mark and said it is 9 inches. What is its real length?", "7 inches (9 − 2)", None),
                        ("A table is 2 meters long. About how many centimeters is that? Explain.", "200 centimeters, because 1 meter is 100 centimeters.", None)), None))
    return dict(scenario="How big is our classroom world? Measure, estimate and compare real things around the room!",
                objectives=["Choose tools and units", "Estimate and compare lengths", "Make a line plot"],
                materials=["Ruler", "Yardstick or meter stick", "Measuring tape", "Pencil"], tasks=tasks,
                extension=("Add your own pencil to the line plot. Does the most common length change?", "Answers vary."))


# =================================================================== Unit 9
@project("length-number-line", ["length-number-line"], "math2-project-paper-airplanes", "paper-airplanes", "Paper Airplane Contest",
         "Fly paper airplanes, record distances on a number line and solve length problems.",
         "Students hold a paper airplane contest. They record flight lengths in feet, show them as lengths from 0 on a number line, add and subtract flights with jumps, and solve length word problems.",
         "Science & Engineering", "Flight Record Number Line", 2, ["2.MD.B.5", "2.MD.B.6"],
         ["I can solve length problems by adding and subtracting.", "I can show numbers as lengths from 0 on a number line.", "I can show sums and differences as jumps on a number line."],
         ["Measuring length (Unit 8)", "Adding and subtracting within 100"],
         ["Scrap paper for airplanes", "Measuring tape or yardstick", "Masking tape number line (0 to 50 feet, optional)", "Number line strips (printable support page)"],
         ["Day 1 (40 min): fly, measure and record (Parts 1–2).", "Day 2 (40 min): jumps and length problems (Parts 3–4)."],
         ["If space is short, use the provided flight data instead of flying.", "Ask students to say where they start, which way they jump and how far.",
          "Advanced students find an unknown flight from a total and a difference."])
def p09(L):
    f = pick3(L, [12, 18, 9], [24, 37, 19], [38, 45, 27])
    tasks = [("Flight Record", "Here are three flights (in feet).",
              T(L, ("Which flight is longest? How long?", f"Flight {f.index(max(f)) + 1}, {max(f)} feet", "Compare the numbers."),
                ("Show the longest flight as a length from 0 on the number line. Where does it end?", f"At {max(f)}", "Start at 0.")),
              [["Flight", "Feet"]] + [[str(i + 1), str(v)] for i, v in enumerate(f)]),
             ("Jumps", "Use a number line.",
              T(L, (f"Start at {f[0]}. Jump forward {f[2]}. Where do you land?", str(f[0] + f[2]), "Forward means add."),
                (f"Start at {f[1]}. Jump back {f[2]}. Where do you land?", str(f[1] - f[2]), "Back means subtract.")), None),
             ("Length Problems", "Solve. Write the unit.",
              T(L, (f"How much farther did flight 2 go than flight 1?" if f[1] > f[0] else "How much farther did flight 1 go than flight 2?", f"{abs(f[1] - f[0])} feet", "Subtract the shorter from the longer."),
                (f"Flights 1 and 3 together went how far?", f"{f[0] + f[2]} feet", "Add the lengths.")), None)]
    if L == "honors":
        tasks.append(("Mystery Flight", "Use clues.",
                      T(L, (f"Flight 4 went 15 feet less than flight 2. Flight 5 went 8 feet more than flight 4. How far did flight 5 go?", f"{f[1] - 15 + 8} feet", None),
                        ("Zoe says a flight from 0 to 12 is 13 feet because she counted 13 tick marks. Explain the mistake.", "Count the spaces, not the ticks: from 0 to 12 is 12 feet.", None)), None))
    else:
        tasks.append(("My Flights", "Fly your airplane three times. Record the flights and show them on a number line.",
                      T(L, ("What is the difference between your longest and shortest flight?", "Answers vary; must be longest − shortest.", "Frame: “__ − __ = __ feet.”")), None))
    return dict(scenario="Ready for takeoff! Build paper airplanes, fly them, and use a number line to see how far they went.",
                objectives=["Solve length problems", "Use a number line", "Show sums and differences as jumps"],
                materials=["Paper", "Measuring tape", "Number line strips"], tasks=tasks,
                extension=("If every flight went 10 feet farther, what would the three flights be?", ", ".join(str(v + 10) for v in f) + " feet"))


# =================================================================== Unit 10
@project("time-money", ["time-money"], "math2-project-lemonade-stand", "lemonade-stand", "Lemonade Stand",
         "Plan the stand's schedule with AM and PM and handle pretend coins and bills.",
         "Students plan a pretend lemonade stand. They write a schedule with times to five minutes and AM or PM, count coins and bills, use ¢ and $ correctly, and solve money problems with change.",
         "Business & Money", "Stand Schedule and Price Sign", 2, ["2.MD.C.7", "2.MD.C.8"],
         ["I can tell and write time to five minutes with AM and PM.", "I can count coins and bills and use ¢ and $.", "I can solve money word problems."],
         ["Count by 5s and 10s", "Add and subtract within 100"],
         ["Paper clocks or a demonstration clock", "Play coins and bills (printable support page)", "Markers for the price sign"],
         ["Day 1 (40 min): the schedule (Parts 1–2).", "Day 2 (40 min): coins, bills and change; the price sign (Parts 3–4)."],
         ["Use play money only.", "Have students sort coins from greatest to least value before counting.",
          "Advanced students find two different ways to pay an amount and the fewest coins."])
def p10(L):
    open_ = pick3(L, (10, 0), (9, 30), (9, 45))
    run = pick3(L, 30, 45, 55)
    t = open_[0] * 60 + open_[1] + run
    close = f"{t // 60}:{t % 60:02d}"
    price = pick3(L, 35, 45, 65)
    paid = pick3(L, (1, 1, 1, 0), (2, 0, 0, 0), (2, 2, 1, 0))
    pv = coins_value(*paid)
    tasks = [("Stand Schedule", f"The stand opens at {open_[0]}:{open_[1]:02d} in the morning.",
              T(L, ("Write the opening time with AM or PM.", f"{open_[0]}:{open_[1]:02d} AM", "Morning is AM."),
                (f"The first rush lasts {run} minutes. What time does it end?", f"{close} AM" if t // 60 < 12 else f"{close} PM", "Count on by 5s."),
                ("The stand closes at 3:15 in the afternoon. Write it with AM or PM.", "3:15 PM", "Afternoon is PM.")), None),
             ("Clock Reading", "Draw the hands on a clock for each time.",
              T(L, ("Where does the minute hand point at 3:15?", "at the 3", "15 minutes is 3 jumps of 5."),
                ("Where does the minute hand point at 10:40?", "at the 8", "40 minutes is 8 jumps of 5.")), None),
             ("Counting Money", f"A cup of lemonade costs {price}¢.",
              T(L, ("A customer pays with " + ", ".join(pl(n, w, m) for n, w, m in zip(paid, ("quarter", "dime", "nickel", "penny"), ("quarters", "dimes", "nickels", "pennies")) if n) + ". How much is that?", f"{pv}¢", "Count quarters, then dimes, then nickels."),
                ("How much change does the customer get?", f"{pv - price}¢", f"{pv} − {price}.")), None),
             ("Bills", "At the end of the day the stand has these bills: $5, $1, $1, $1.",
              T(L, ("How many dollars is that?", "$8", "5 + 1 + 1 + 1."), ("Write 8 dollars and 40 cents.", "$8 and 40¢", "Dollars with $, cents with ¢.")), None)]
    if L == "honors":
        tasks.append(("Pay It Two Ways", f"Show {price}¢ two ways.",
                      T(L, (f"Show {price}¢ with the fewest coins.", fewest_words(price), None),
                        (f"Ella says 4 coins are always worth 4¢. Give an example that shows she is wrong.", "4 quarters are worth 100¢.", None)), None))
    else:
        tasks.append(("Price Sign", "Make a price sign for two drinks. Write each price with ¢.",
                      T(L, ("What do both drinks cost together?", "Answers vary; the sum must match the sign.", "Frame: “__¢ + __¢ = __¢.”")), None))
    return dict(scenario="Our class is opening a pretend lemonade stand! Plan the day and keep track of the play money.",
                objectives=["Tell time to five minutes with AM and PM", "Count coins and bills", "Solve money problems"],
                materials=["Pencil", "Paper clock", "Play money"], tasks=tasks,
                extension=("The stand sold 2 cups. How much money did it take in?", f"{2 * price}¢"))


# =================================================================== Unit 11
@project("graphs-data", ["graphs-data"], "math2-project-class-survey", "class-survey", "Class Survey Graphs",
         "Collect anonymous votes, make a picture graph and a bar graph, and answer questions.",
         "Students run an anonymous class survey (for example, a favorite fruit vote with tally marks). They make a picture graph and a single-unit bar graph with up to four categories and solve put-together, take-apart and compare problems.",
         "Data & Surveys", "Survey Graph Poster", 2, ["2.MD.D.10"],
         ["I can make a picture graph and a bar graph with a scale of 1.", "I can read a graph.", "I can solve problems with data from a graph."],
         ["Counting and comparing within 20"],
         ["Sticky notes for anonymous votes", "Tally chart and graph frames (printable support page)", "Crayons", "Poster paper"],
         ["Day 1 (40 min): collect votes and make a tally chart and picture graph (Parts 1–2).", "Day 2 (40 min): the bar graph and questions (Parts 3–4)."],
         ["Votes are anonymous; no names are recorded.", "Remind students that each picture stands for 1 and the scale starts at 0.",
          "Advanced students write three questions about their graph and answer them."])
def p11(L):
    data = pick3(L, {"apple": 6, "banana": 4, "grape": 8}, {"apple": 9, "banana": 6, "grape": 12, "pear": 4}, {"apple": 14, "banana": 9, "grape": 17, "pear": 6})
    k = list(data)
    most = max(data, key=data.get)
    least = min(data, key=data.get)
    tasks = [("Tally Chart", "Here are the class votes for a favorite fruit (or use your own anonymous votes).",
              T(L, ("How many votes are there in all?", f"{sum(data.values())} votes", "Add every category.")),
              [["Fruit", "Votes"]] + [[c, str(v)] for c, v in data.items()]),
             ("Picture Graph", "Make a picture graph. Each picture stands for 1 vote.",
              T(L, (f"How many pictures go in the {k[0]} row?", str(data[k[0]]), "One picture for each vote."),
                ("Which fruit has the most votes?", most, "Find the longest row.")), None),
             ("Bar Graph", "Make a bar graph with a scale of 1.",
              T(L, (f"How tall is the bar for {k[1]}?", str(data[k[1]]), "Count up from 0."),
                ("What does the graph need besides bars?", "A title, labels, and a scale that counts by 1s", "Look at a graph in your book.")), None),
             ("Questions", "Use your graph.",
              T(L, (f"How many more votes for {most} than {least}?", f"{data[most] - data[least]} votes", "Subtract."),
                (f"How many votes for {k[0]} and {k[1]} together?", f"{data[k[0]] + data[k[1]]} votes", "Add.")), None)]
    if L == "honors":
        tasks.append(("Graph Check", "Explain your thinking.",
                      T(L, (f"Leo says {most} has {data[most] + 1} votes because he counted the line at 0. What is wrong?", f"Read the number at the top of the bar: {data[most]}. The line at 0 is not a vote.", None),
                        ("Write a two-step question about the graph and answer it.", "Answers vary; both steps must use graph data correctly.", None)), None))
    return dict(scenario="What is our class's favorite fruit? Collect anonymous votes, graph them, and report what you find.",
                objectives=["Make picture graphs and bar graphs", "Read graphs", "Solve problems with graph data"],
                materials=["Pencil", "Crayons", "Graph frames"], tasks=tasks,
                extension=("Three more votes for the fruit with the fewest votes come in. Does it still have the fewest?", "Answers depend on the data; compare the new total with the others."))


# =================================================================== Unit 12
@project("shapes-equal-shares", ["shapes-equal-shares"], "math2-project-paper-quilt", "paper-quilt", "Paper Quilt Square",
         "Design a paper quilt square with shapes, rows of squares and equal shares.",
         "Students design a class paper quilt. They name and draw shapes by sides and angles, partition a rectangle into rows and columns of same-size squares, and color halves, thirds and fourths, explaining that equal shares can look different.",
         "Art & Design", "Paper Quilt Square", 2, ["2.G.A.1", "2.G.A.2", "2.G.A.3"],
         ["I can name and draw shapes by their sides and angles.", "I can partition a rectangle into rows and columns of squares and count them.", "I can make halves, thirds and fourths."],
         ["Count within 100", "Arrays (Unit 2)"],
         ["Square paper or construction paper", "Rulers", "Crayons or colored pencils", "Dot paper and grid paper (printable support page)", "Scissors and glue"],
         ["Day 1 (40 min): shapes and the quilt grid (Parts 1–2).", "Day 2 (40 min): equal shares and the finished quilt square (Parts 3–4)."],
         ["Fold paper to check that shares are equal.", "Turn shapes to show the name does not change.",
          "Advanced students cut the same square into halves two different ways and prove the halves are equal."])
def p12(L):
    r, c = pick3(L, (2, 3), (3, 4), (4, 5))
    tasks = [("Shape Patches", "Draw each shape on dot paper.",
              T(L, ("Draw a shape with 5 sides. What is it called?", "pentagon", "Count the sides as you draw."),
                ("How many angles does a hexagon have?", "6 angles", "Angles = sides."),
                ("Draw a quadrilateral that is not a square or a rectangle.", "Answers vary; it must have 4 straight sides.", "4 sides, any lengths.")), None),
             ("Quilt Grid", f"Partition your quilt rectangle into {r} rows and {c} columns of same-size squares.",
              T(L, ("How many squares are there?", f"{r * c} squares", f"Add {c} for each row."),
                ("Write a repeated-addition equation.", " + ".join([str(c)] * r) + f" = {r * c}", "One addend for each row.")), None),
             ("Equal Shares", "Color some squares in halves, thirds and fourths.",
              T(L, ("Cut one square into 4 equal shares. What is each share called?", "one fourth", "4 equal shares are fourths."),
                ("How many thirds make a whole?", "3 thirds", "A whole is three thirds."),
                ("Which is bigger: one half or one fourth of the same square?", "one half", "Fewer shares means bigger shares.")), None)]
    if L == "honors":
        tasks.append(("Prove It", "Explain with drawings.",
                      T(L, ("Cut one square into halves with a straight line and another with a diagonal line. Are the halves the same size? Explain.", "Yes. Each is half of the same square, even though one is a rectangle and one is a triangle.", None),
                        ("Raj cut a rectangle into 3 parts that are not the same size and called them thirds. What is wrong?", "Thirds must be equal shares.", None)), None))
    else:
        tasks.append(("My Quilt Square", "Finish your quilt square with at least two shapes and one square cut into equal shares.",
                      T(L, ("Label each shape and each share.", "Answers vary; labels must match the drawing.", "Frame: “This is a __. It has __ sides.”")), None))
    return dict(scenario="Our class is making a paper quilt! Each student designs one square with shapes, rows of squares and equal shares.",
                objectives=["Name and draw shapes", "Partition rectangles into squares", "Make halves, thirds and fourths"],
                materials=["Square paper", "Ruler", "Crayons", "Dot paper"], tasks=tasks,
                extension=("The class quilt has 4 rows of 5 quilt squares. How many squares in all?", "20 squares (5 + 5 + 5 + 5)"))


# =================================================================== Cumulative 1 (Units 1–6)
@project("cumulative-carnival", ["add-subtract-20", "odd-even-arrays", "place-value-1000", "count-compare-1000", "add-subtract-100", "word-problems-100"],
         "math2-project-school-carnival", "school-carnival", "School Carnival",
         "Run carnival booths with tickets, prizes and team lines (Units 1–6).",
         "A cumulative project for Units 1–6. Students plan a school carnival: ticket facts within 20, teams in pairs and arrays, prize counts in hundreds, tens and ones, comparing ticket totals, adding and subtracting within 100, and two-step booth stories.",
         "Events & Planning", "Carnival Plan", 3, ["2.OA.A.1", "2.OA.B.2", "2.OA.C.3", "2.OA.C.4", "2.NBT.A.1", "2.NBT.A.3", "2.NBT.A.4", "2.NBT.B.5", "2.NBT.B.8"],
         ["I can add and subtract within 20 and within 100.", "I can use place value to write and compare numbers.", "I can solve one- and two-step word problems."],
         ["Units 1–6 of 2nd Grade Math"],
         ["Booth cards and ticket sheet (printable support page)", "Counters or base-ten blocks", "Poster paper", "Pencils"],
         ["Day 1 (40 min): tickets and teams (Parts 1–2).", "Day 2 (40 min): prizes and comparing (Parts 3–4).", "Day 3 (40 min): booth stories and the carnival plan (Part 5); presentations."],
         ["Use this after Unit 6 as a review; each part names the unit it reviews.", "Groups of 3–4 work well; rotate the recorder role.",
          "Advanced students decide how to split prizes between booths and justify the plan."], cumulative=True)
def pc1(L):
    t1, t2 = pick3(L, (7, 6), (9, 8), (8, 9))
    kids = pick3(L, 12, 15, 19)
    r, c = pick3(L, (3, 4), (4, 5), (5, 4))
    prizes = pick3(L, 236, 405, 618)
    a, b = pick3(L, (34, 25), (48, 37), (67, 29))
    tasks = [("Tickets (Unit 1)", f"Ana has {t1} tickets and Ben has {t2}.",
              T(L, ("How many tickets do they have together?", str(t1 + t2), "Make a ten or use a double."),
                (f"A game costs 15 tickets. How many more tickets do they need?" if t1 + t2 < 15 else f"A game costs 15 tickets. How many tickets are left after one game?", str(abs(15 - t1 - t2)), "Think addition.")), None),
             ("Teams and Lines (Unit 2)", f"{kids} children want to play the partner game. Chairs for the show are in {r} rows of {c}.",
              T(L, (f"Is {kids} odd or even? Can everyone have a partner?", f"{'even, yes' if kids % 2 == 0 else 'odd, no (one is left over)'}", "Make pairs."),
                ("How many chairs are there?", f"{r * c} chairs", " + ".join([str(c)] * r) + ".")), None),
             ("Prizes (Unit 3)", f"The carnival has {prizes} prizes.",
              T(L, (f"How many hundreds, tens and ones are in {prizes}?", f"{pl(prizes // 100, 'hundred')}, {pl(prizes // 10 % 10, 'ten')}, {pl(prizes % 10, 'one')}", "Look at each digit."),
                (f"Write {prizes} in expanded form.", " + ".join(str(x) for x in (prizes // 100 * 100, prizes // 10 % 10 * 10, prizes % 10) if x), "Value of each digit.")), None),
             ("Comparing (Unit 4)", f"Booth A gave out {prizes - 100} prizes and booth B gave out {prizes - 10}.",
              T(L, ("Which booth gave out more? Write it with > or <.", f"{prizes - 10} > {prizes - 100}", "Compare hundreds first."),
                (f"What is 10 more than {prizes - 10}?", str(prizes), "Tens digit + 1.")), None),
             ("Booth Stories (Units 5–6)", f"The ring toss had {a} players in the morning and {b} in the afternoon.",
              T(L, ("How many players in all?", f"{a + b} players", "Add tens and ones."),
                ("How many more players came in the morning?", f"{a - b} players", "Subtract."),
                (f"Then 12 more players came at night. How many players for the whole day?", f"{a + b + 12} players", "Two steps: add, then add again.")), None)]
    if L == "honors":
        tasks.append(("Prize Plan", f"Split {prizes} prizes between two booths so booth A gets 100 more than booth B.",
                      T(L, ("How many prizes does each booth get? Show your thinking.", f"Booth A: {(prizes + 100) // 2}, booth B: {(prizes - 100) // 2}" if prizes % 2 == 0 else "It cannot be split exactly; answers explain why one prize is left over.", None),)
                      , None))
    return dict(scenario="The school carnival is coming! Your team plans tickets, teams, prizes and booth reports.",
                objectives=["Facts within 20", "Odd, even and arrays", "Place value and comparing", "Add, subtract and solve stories within 100"],
                materials=["Pencil", "Counters", "Booth cards", "Poster paper"], tasks=tasks,
                extension=("If each of 4 booths gives out 25 prizes, how many prizes are given out? Use repeated addition.", "100 prizes (25 + 25 + 25 + 25)"))


# =================================================================== Cumulative 2 (Units 7–12)
@project("cumulative-market-day", ["add-subtract-1000", "measuring-length", "length-number-line", "time-money", "graphs-data", "shapes-equal-shares"],
         "math2-project-market-day", "market-day", "Neighborhood Market Day",
         "Plan a pretend market with measuring, time, money, graphs and shapes (Units 7–12).",
         "A cumulative project for Units 7–12. Students plan a pretend neighborhood market: visitor totals within 1,000, measuring booth tables, a number-line map of the street, a schedule with AM and PM, play-money sales, a graph of favorite booths and booth signs cut into equal shares.",
         "Community & Markets", "Market Day Plan", 3, ["2.NBT.B.7", "2.MD.A.1", "2.MD.A.4", "2.MD.B.5", "2.MD.B.6", "2.MD.C.7", "2.MD.C.8", "2.MD.D.10", "2.G.A.1", "2.G.A.3"],
         ["I can add and subtract within 1,000.", "I can measure, tell time and count money.", "I can make a graph and use shapes and equal shares."],
         ["Units 7–12 of 2nd Grade Math"],
         ["Rulers and a measuring tape", "Play coins and bills (printable support page)", "Paper clocks", "Graph frames", "Construction paper for signs"],
         ["Day 1 (40 min): visitors and measuring (Parts 1–2).", "Day 2 (40 min): street map, schedule and money (Parts 3–4).", "Day 3 (40 min): graph, signs and the market plan (Parts 5–6)."],
         ["Use this after Unit 12 as a review; each part names the unit it reviews.", "Each group member is responsible for one part of the final plan.",
          "Advanced students design the street layout under length limits and explain it."], cumulative=True)
def pc2(L):
    v1, v2 = pick3(L, (245, 132), (378, 264), (486, 357))
    tbl = pick3(L, (36, 24), (48, 30), (60, 42))
    pos = pick3(L, (10, 35), (15, 60), (25, 85))
    st = pick3(L, (9, 0), (8, 30), (8, 45))
    dur = pick3(L, 30, 45, 50)
    tm_ = st[0] * 60 + st[1] + dur
    price, paid = pick3(L, (40, 50), (65, 100), (85, 100))
    votes = pick3(L, {"bakery": 7, "plants": 5, "toys": 9}, {"bakery": 11, "plants": 8, "toys": 14, "books": 6}, {"bakery": 16, "plants": 12, "toys": 19, "books": 9})
    tasks = [("Visitors (Unit 7)", f"Saturday had {v1} visitors and Sunday had {v2}.",
              T(L, ("How many visitors in all?", f"{v1 + v2} visitors", "Add hundreds, tens, ones."),
                ("How many more came on Saturday?", f"{v1 - v2} visitors", "Subtract and check by adding.")), None),
             ("Booth Tables (Unit 8)", f"The bakery table is {tbl[0]} inches long. The plant table is {tbl[1]} inches long.",
              T(L, ("Which tool would you use to measure a table?", "a yardstick or a measuring tape", "Tables are longer than a ruler."),
                ("How much longer is the bakery table?", f"{tbl[0] - tbl[1]} inches", "Subtract.")), None),
             ("Street Map (Unit 9)", f"The bakery is at {pos[0]} feet and the toy booth is at {pos[1]} feet along the street.",
              T(L, ("How far apart are the booths?", f"{pos[1] - pos[0]} feet", "Jump from the smaller to the larger number."),
                (f"The plant booth is 20 feet past the bakery. Where is it?", f"{pos[0] + 20} feet", "Jump forward 20.")), None),
             ("Schedule and Money (Unit 10)", f"The market opens at {st[0]}:{st[1]:02d} in the morning. A cookie costs {price}¢.",
              T(L, ("Write the opening time with AM or PM.", f"{st[0]}:{st[1]:02d} AM", "Morning is AM."),
                (f"The music starts {dur} minutes after opening. What time is that?", f"{tm_ // 60}:{tm_ % 60:02d} AM", "Count on by 5s."),
                (f"A buyer pays {paid}¢ for a cookie. What is the change?", f"{paid - price}¢", "Subtract.")), None),
             ("Favorite Booth Graph (Unit 11)", "Make a bar graph of the votes (scale of 1).",
              T(L, ("Which booth got the most votes?", max(votes, key=votes.get), "Tallest bar."),
                ("How many votes in all?", f"{sum(votes.values())} votes", "Add every bar.")),
              [["Booth", "Votes"]] + [[k, str(v)] for k, v in votes.items()]),
             ("Booth Signs (Unit 12)", "Each sign is a rectangle.",
              T(L, ("Cut a sign into 3 equal shares. What is each share called?", "one third", "3 equal shares are thirds."),
                ("A sign shaped like a hexagon has how many sides?", "6 sides", "Hexagon: 6.")), None)]
    if L == "honors":
        tasks.append(("Street Design", "The street is 100 feet long. Booths need 15 feet each with 5 feet between booths.",
                      T(L, ("How many booths fit on the street? Show your thinking on a number line.", "5 booths (15 + 5 + 15 + 5 + 15 + 5 + 15 + 5 + 15 = 95 feet)", None),)
                      , None))
    return dict(scenario="Our neighborhood is having a pretend market day! Plan the visitors, booths, street, schedule, money, graph and signs.",
                objectives=["Add and subtract within 1,000", "Measure and use a number line", "Time and money", "Graphs, shapes and equal shares"],
                materials=["Pencil", "Ruler", "Play money", "Paper clock", "Graph frame"], tasks=tasks,
                extension=("Next year 100 more visitors come each day. How many visitors in all?", f"{v1 + v2 + 200} visitors"))
