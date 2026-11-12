"""Grade 5 reference content: vocabulary, concept flashcards, visual flashcards and cheat-sheet sides, one entry per unit.
Every numeric example carries a check that build_content.py evaluates before writing anything.
Fractions are written a/b (mixed numbers 'w a/b'); build_content.py turns them into stacked fractions where needed."""

V = {}      # unit -> [(term, definition, example)]
CARDS = {}  # unit -> [(front, back, kind)]  kinds: concept, symbol, rule, mental, misconception, representation
VIS = {}    # unit -> [(front, figure kind, figure data, back)]
SHEET = {}  # unit -> dict(focus, morefocus, sides=[side, side])  side: big, vocab, how, fig, remember, watch, tryit

# ---------------------------------------------------------------- Unit 1
u = "place-value-number-sense"
V[u] = [("place value", "The value a digit has because of where it is in a number.", "In 3.47, the 4 is worth 0.4"),
        ("digit", "One of the symbols 0 to 9 used to write numbers.", "7,204 has four digits"),
        ("decimal", "A number with a decimal point that shows parts of a whole.", "2.35"),
        ("tenths", "The first place to the right of the decimal point, worth 1/10 of a whole.", "0.6 = 6 tenths"),
        ("hundredths", "The second place to the right of the decimal point, worth 1/100 of a whole.", "0.08 = 8 hundredths"),
        ("thousandths", "The third place to the right of the decimal point, worth 1/1000 of a whole.", "0.005 = 5 thousandths"),
        ("exponent", "A small raised number that tells how many times to use the base as a factor.", "10³ = 10 × 10 × 10"),
        ("power of 10", "A number like 10, 100, 1,000 made by multiplying 10s.", "10⁴ = 10,000"),
        ("expanded form", "A number written as the sum of the values of its digits.", "4.36 = 4 + 0.3 + 0.06"),
        ("word form", "A number written in words.", "2.7 = two and seven tenths"),
        ("standard form", "A number written with digits.", "forty-one and six hundredths = 41.06"),
        ("round", "Change a number to a nearby number that is easier to use.", "3.86 rounds to 3.9")]
CARDS[u] = [("A digit moves one place to the LEFT. What happens to its value?", "It becomes 10 times as much.", "rule"),
            ("A digit moves one place to the RIGHT. What happens to its value?", "It becomes 1/10 as much.", "rule"),
            ("What does 10³ mean?", "10 × 10 × 10 = 1,000", "symbol"),
            ("Multiply 4.5 × 100 in your head.", "450 (each digit moves 2 places left)", "mental"),
            ("Divide 72 ÷ 1,000 in your head.", "0.072", "mental"),
            ("Which is greater, 0.5 or 0.45?", "0.5, because 5 tenths is more than 4 tenths.", "misconception"),
            ("Is 0.30 equal to 0.3?", "Yes. 3 tenths = 30 hundredths. A zero at the end does not change the value.", "concept"),
            ("What do the symbols < and > mean?", "< means “is less than.” > means “is greater than.” The open side faces the greater number.", "symbol"),
            ("Round 6.45 to the nearest tenth.", "6.5 (the hundredths digit is 5, so round up)", "rule"),
            ("Why is 0.7 not the same as 0.07?", "0.7 is 7 tenths; 0.07 is 7 hundredths, which is 10 times smaller.", "misconception")]
VIS[u] = [("What number do the blocks show? A flat is 1 whole.", "base_ten", {"flats": 1, "rods": 4, "units": 6, "key": "flat = 1, rod = 0.1, cube = 0.01"}, "1.46"),
          ("What decimal is shaded?", "hundred_grid", {"shaded": 35}, "0.35 (35 hundredths)"),
          ("What is the value of the highlighted digit?", "place_chart", {"places": ["ones", "tenths", "hundredths", "thousandths"], "digits": {"ones": 2, "tenths": 0, "hundredths": 8, "thousandths": 4}, "highlight": "hundredths"}, "0.08")]
SHEET[u] = dict(focus="place value patterns, powers of ten, and reading decimals", morefocus="comparing, ordering and rounding decimals",
    sides=[dict(big="Each place is worth 10 times the place to its right. Moving left multiplies by 10; moving right divides by 10.",
                vocab=["place value", "tenths", "hundredths", "exponent"],
                how=dict(text="Multiply by a power of 10 by moving digits.", example="3.27 × 10²", steps=[["10² = 100:", "move each digit 2 places left"], ["Result:", "327"]], answer="327", check="3.27*100==327"),
                fig=("place_chart", {"places": ["tens", "ones", "tenths", "hundredths", "thousandths"], "digits": {"tens": 4, "ones": 5, "tenths": 2, "hundredths": 0, "thousandths": 6}, "highlight": "tenths"}, "45.206: the 2 is in the tenths place, so it is worth 0.2."),
                remember=["10¹ = 10, 10² = 100, 10³ = 1,000", "Read “and” for the decimal point: 5.04 is five and four hundredths."],
                watch=[["0.4 vs 0.04", "0.4 is 10 times as much as 0.04"], ["“and” means the decimal point", "two and three tenths is 2.3, not 2,003"]],
                tryit=[["Write 6 × 10 + 4 × 1 + 7 × 1/100 in standard form.", "64.07", "6*10+4+7/100==64.07"], ["0.56 × 1,000 = ?", "560", "0.56*1000==560"]]),
           dict(big="Compare decimals place by place from the left. Round by looking at the digit to the right of the rounding place.",
                vocab=["round", "standard form", "expanded form", "word form"],
                how=dict(text="Compare 2.48 and 2.5.", example="Line up the decimal points.", steps=[["Ones:", "2 = 2"], ["Tenths:", "4 < 5"]], answer="2.48 < 2.5", check="2.48<2.5"),
                fig=("number_line", {"lo": "3.4", "hi": "3.5", "den": 100, "label_every": 10, "fmt": "dec", "points": [{"x": "347/100", "label": "3.47"}]}, "3.47 is closer to 3.5 than to 3.4, so it rounds to 3.5."),
                remember=["5 or more: round up. Less than 5: keep the digit.", "Extra zeros at the end of a decimal do not change its value: 0.6 = 0.60."],
                watch=[["More digits is not always bigger", "0.9 > 0.125"], ["Round, do not just chop", "4.68 rounds to 4.7, not 4.6"]],
                tryit=[["Order from least to greatest: 0.62, 0.6, 0.065", "0.065, 0.6, 0.62", "0.065<0.6&&0.6<0.62"], ["Round 7.349 to the nearest hundredth.", "7.35", "Math.round(7.349*100)/100==7.35"]])])

# ---------------------------------------------------------------- Unit 2
u = "multi-digit-multiplication-division"
V[u] = [("factor", "A number that is multiplied.", "In 24 × 6 = 144, 24 and 6 are factors"),
        ("product", "The answer to a multiplication problem.", "144 is the product of 24 × 6"),
        ("partial products", "The smaller products you add to find a whole product.", "23 × 4 = 80 + 12"),
        ("standard algorithm", "The step-by-step written method for multiplying or dividing.", "Multiply by ones, then tens, then add"),
        ("dividend", "The number being divided.", "In 84 ÷ 4, the dividend is 84"),
        ("divisor", "The number you divide by.", "In 84 ÷ 4, the divisor is 4"),
        ("quotient", "The answer to a division problem.", "84 ÷ 4 = 21"),
        ("remainder", "The amount left over after dividing.", "17 ÷ 5 = 3 R 2"),
        ("estimate", "A close answer found with rounded or compatible numbers.", "398 × 21 ≈ 400 × 20 = 8,000"),
        ("compatible numbers", "Numbers that are easy to work with mentally.", "2,738 ÷ 9 ≈ 2,700 ÷ 9 = 300"),
        ("area model", "A rectangle split into parts to show multiplication or division.", "a 30 + 4 by 20 + 5 rectangle")]
CARDS[u] = [("What is a placeholder zero?", "When you multiply by the tens digit, write a 0 in the ones place first, because you are multiplying by tens.", "rule"),
            ("How can you check 1,256 ÷ 4 = 314?", "Multiply: 314 × 4 = 1,256.", "rule"),
            ("Estimate 612 × 39.", "600 × 40 = 24,000", "mental"),
            ("40 × 30 = ?", "1,200 (4 × 3 = 12, then two zeros)", "mental"),
            ("6,400 ÷ 80 = ?", "80 (64 ÷ 8 = 8, one zero left)", "mental"),
            ("When do you round a quotient UP in a word problem?", "When everyone or everything needs a place, like the number of buses needed.", "concept"),
            ("Can the remainder be bigger than the divisor?", "No. If it is, the quotient digit was too small.", "misconception"),
            ("What does 47 R 3 mean?", "47 equal groups, with 3 left over.", "symbol"),
            ("Why multiply 34 × 26 as 34 × 6 plus 34 × 20?", "26 = 20 + 6, so you multiply by each part and add (distributive property).", "concept")]
VIS[u] = [("What is the product shown by this area model?", "area_model", {"rows": ["20", "3"], "cols": ["40", "5"], "cells": [["800", "100"], ["120", "15"]]}, "45 × 23 = 800 + 100 + 120 + 15 = 1,035"),
          ("The area model shows 936 ÷ 4. What is the quotient?", "area_model", {"rows": ["4"], "cols": ["200", "30", "4"], "cells": [["800", "120", "16"]]}, "200 + 30 + 4 = 234"),
          ("What multiplication does this array show?", "array", {"rows": 4, "cols": 9}, "4 × 9 = 36")]
SHEET[u] = dict(focus="multiplying multi-digit numbers and estimating", morefocus="dividing with one- and two-digit divisors and using remainders",
    sides=[dict(big="Break a big multiplication into smaller parts, multiply each part, and add the partial products.",
                vocab=["factor", "product", "partial products", "estimate"],
                how=dict(text="Multiply 46 × 23 with partial products.", example="46 × 23", steps=[["46 × 3 =", "138"], ["46 × 20 =", "920"], ["Add:", "138 + 920"]], answer="1,058", check="46*23==1058"),
                fig=("area_model", {"rows": ["20", "3"], "cols": ["40", "6"], "cells": [["800", "120"], ["120", "18"]]}, "Area model for 46 × 23: 800 + 120 + 120 + 18 = 1,058."),
                remember=["Estimate first so you can tell if your answer makes sense.", "Line up places when you add partial products."],
                watch=[["Forgetting the placeholder zero", "46 × 20 is 920, not 92"], ["Adding instead of multiplying the parts", "use × for every part"]],
                tryit=[["327 × 14 = ?", "4,578", "327*14==4578"], ["Estimate 489 × 31.", "500 × 30 = 15,000", "500*30==15000"]]),
           dict(big="Division makes equal groups. Use place value: divide, multiply, subtract, bring down. Then decide what the remainder means.",
                vocab=["dividend", "divisor", "quotient", "remainder"],
                how=dict(text="Divide 1,476 ÷ 12.", example="1,476 ÷ 12", steps=[["14 ÷ 12 → 1 (hundred):", "1,476 − 1,200 = 276"], ["27 ÷ 12 → 2 (tens):", "276 − 240 = 36"], ["36 ÷ 12 →", "3 (ones)"]], answer="123", check="1476/12==123"),
                fig=("area_model", {"rows": ["12"], "cols": ["100", "20", "3"], "cells": [["1,200", "240", "36"]]}, "Area model for 1,476 ÷ 12: the lengths 100 + 20 + 3 make the quotient 123."),
                remember=["Check: quotient × divisor + remainder = dividend.", "Remainders: round up, drop it, or use it as the answer, depending on the question."],
                watch=[["Remainder too big", "the remainder must be less than the divisor"], ["Skipping a zero in the quotient", "816 ÷ 8 = 102, not 12"]],
                tryit=[["2,345 ÷ 7 = ?", "335", "2345/7==335"], ["150 students, buses hold 42. How many buses?", "4 buses (3 R 24, round up)", "Math.ceil(150/42)==4"]])])

# ---------------------------------------------------------------- Unit 3
u = "decimal-operations"
V[u] = [("decimal point", "The dot that separates the whole-number part from the parts of a whole.", "In 12.5, the point is between 2 and 5"),
        ("sum", "The answer to an addition problem.", "1.2 + 0.5 = 1.7"),
        ("difference", "The answer to a subtraction problem.", "3.4 − 1.1 = 2.3"),
        ("regroup", "Trade 10 of one place for 1 of the next place (or the reverse).", "10 hundredths = 1 tenth"),
        ("decimal places", "The number of digits to the right of the decimal point.", "4.375 has 3 decimal places"),
        ("estimate", "A close answer found by rounding.", "3.9 × 5.1 ≈ 4 × 5 = 20"),
        ("unit price", "The cost of one item or one unit.", "$6.00 for 4 → $1.50 each"),
        ("hundredths grid", "A 10 by 10 square that shows one whole split into 100 equal parts.", "35 squares shaded = 0.35")]
CARDS[u] = [("How do you line up numbers to add 4.5 + 2.37?", "Line up the decimal points. Write 4.50 so both have the same places.", "rule"),
            ("Where does the decimal point go in 0.3 × 0.2?", "0.06. One place + one place = two decimal places.", "rule"),
            ("Multiplying by a decimal less than 1 makes the product…", "smaller than the other factor.", "concept"),
            ("Dividing by a decimal less than 1 makes the quotient…", "bigger than the dividend.", "concept"),
            ("How do you divide 4.8 ÷ 0.6?", "Multiply both by 10: 48 ÷ 6 = 8.", "rule"),
            ("0.5 × 8 in your head", "4 (half of 8)", "mental"),
            ("1.2 + 0.8 in your head", "2", "mental"),
            ("Ava says 3.2 + 1.45 = 1.77. What went wrong?", "She lined up the last digits. Line up the decimal points: 3.20 + 1.45 = 4.65.", "misconception"),
            ("How do you write money amounts?", "Use two decimal places: $4.50, not $4.5.", "symbol")]
VIS[u] = [("The model shows 0.4 × 0.7. What is the product?", "area_grid", {"rows": 10, "cols": 10, "sh_rows": 4, "sh_cols": 7, "mode": "overlap"}, "28 hundredths = 0.28"),
          ("What sum does the model show? (Each large square is 1 whole.)", "hundred_grid", {"shaded": 128, "grids": 2}, "1.28"),
          ("The tape shows 7.2 split into 4 equal parts. What is one part?", "tape", {"parts": 4, "shaded": 1, "total_label": "7.2"}, "7.2 ÷ 4 = 1.8")]
SHEET[u] = dict(focus="adding, subtracting and multiplying decimals", morefocus="dividing decimals and solving money problems",
    sides=[dict(big="Add and subtract decimals by lining up the decimal points. Multiply as whole numbers, then count decimal places.",
                vocab=["decimal point", "regroup", "decimal places", "estimate"],
                how=dict(text="Multiply 2.4 × 1.5.", example="2.4 × 1.5", steps=[["24 × 15 =", "360"], ["1 + 1 decimal places:", "3.60"]], answer="3.6", check="Math.abs(2.4*1.5-3.6)<1e-9"),
                fig=("area_grid", {"rows": 10, "cols": 10, "sh_rows": 3, "sh_cols": 6, "mode": "overlap"}, "0.3 × 0.6 = 0.18: the overlap is 18 of 100 small squares."),
                remember=["Write zeros to fill empty places: 6.4 − 2.35 → 6.40 − 2.35.", "Estimate to place the decimal point: 4 × 2.9 ≈ 12."],
                watch=[["Lining up the last digits", "line up the decimal points instead"], ["Counting decimal places", "0.2 × 0.4 = 0.08, not 0.8"]],
                tryit=[["7.3 − 2.65 = ?", "4.65", "Math.abs(7.3-2.65-4.65)<1e-9"], ["6 × 1.25 = ?", "7.5", "6*1.25==7.5"]]),
           dict(big="To divide by a whole number, place the decimal point above the one in the dividend. To divide by a decimal, make the divisor a whole number first.",
                vocab=["sum", "difference", "unit price", "hundredths grid"],
                how=dict(text="Divide 3.6 ÷ 0.4.", example="3.6 ÷ 0.4", steps=[["Multiply both by 10:", "36 ÷ 4"], ["Divide:", "9"]], answer="9", check="Math.abs(3.6/0.4-9)<1e-9"),
                fig=("tape", {"parts": 3, "shaded": 1, "total_label": "$7.50", "note": "3 friends share $7.50"}, "$7.50 ÷ 3 = $2.50 for each friend."),
                remember=["Check division with multiplication: 9 × 0.4 = 3.6.", "Money answers have two decimal places."],
                watch=[["Moving only one decimal point", "move the point in BOTH numbers"], ["Better buy", "compare the price of ONE item, not the totals"]],
                tryit=[["9.6 ÷ 3 = ?", "3.2", "Math.abs(9.6/3-3.2)<1e-9"], ["You buy 2 pens at $1.35. Change from $5?", "$2.30", "Math.abs(5-2*1.35-2.3)<1e-9"]])])

# ---------------------------------------------------------------- Unit 4
u = "numerical-expressions-patterns"
V[u] = [("numerical expression", "Numbers and operation signs with no equals sign.", "4 × (3 + 5)"),
        ("evaluate", "Find the value of an expression.", "4 × (3 + 5) = 32"),
        ("parentheses ( )", "Grouping symbols that show what to do first.", "(2 + 3) × 4 = 20"),
        ("brackets [ ]", "Grouping symbols used around parentheses.", "2 × [5 + (1 + 1)]"),
        ("braces { }", "Grouping symbols used around brackets.", "{3 × [2 + (4 − 1)]}"),
        ("order of operations", "The rules for which step to do first: grouping, then × and ÷, then + and −.", "3 + 4 × 2 = 11"),
        ("pattern", "Numbers that follow a rule.", "3, 6, 9, 12, …"),
        ("rule", "Tells how to get the next term.", "Add 3"),
        ("term", "One number in a pattern.", "In 2, 4, 6, the 3rd term is 6"),
        ("ordered pair", "Two numbers (x, y) that name a point on a graph.", "(2, 6)")]
CARDS[u] = [("What do you do first in 18 − [2 × (3 + 1)]?", "3 + 1 (innermost grouping symbols)", "rule"),
            ("Write “add 6 and 4, then multiply by 3.”", "3 × (6 + 4)", "representation"),
            ("Without computing: how does 5 × (127 + 38) compare to 127 + 38?", "It is 5 times as large.", "concept"),
            ("Is 3 + 4 × 2 equal to 14?", "No. Multiply first: 3 + 8 = 11.", "misconception"),
            ("Pattern A adds 2, Pattern B adds 6 (both start at 0). How are they related?", "Each B term is 3 times the A term.", "concept"),
            ("Next term: 5, 10, 20, 40, …", "80 (rule: multiply by 2)", "mental"),
            ("12 + 8 × 0 = ?", "12", "mental"),
            ("What is the difference between ( ), [ ], and { }?", "They all group. Work from the inside out: ( ), then [ ], then { }.", "symbol")]
VIS[u] = [("What is the rule for each pattern? How do the terms compare?", "two_tables", {"rows": [["Pattern A", ["0", "4", "8", "12"]], ["Pattern B", ["0", "8", "16", "24"]]]}, "A adds 4, B adds 8. Each B term is 2 times the A term."),
          ("What point comes next if the pairs are graphed?", "coord", {"xmax": 6, "ymax": 12, "step": 2, "points": [{"x": 0, "y": 0}, {"x": 1, "y": 3}, {"x": 2, "y": 6}, {"x": 3, "y": 9}]}, "(4, 12): y is 3 times x.")]
SHEET[u] = dict(focus="grouping symbols and writing and interpreting expressions", morefocus="number patterns and relationships between two patterns",
    sides=[dict(big="Grouping symbols tell you what to do first. Work from the inside out: ( ), then [ ], then { }. Then × and ÷, then + and −.",
                vocab=["numerical expression", "evaluate", "parentheses ( )", "order of operations"],
                how=dict(text="Evaluate 2 × [12 − (3 + 5)].", example="2 × [12 − (3 + 5)]", steps=[["Parentheses:", "3 + 5 = 8"], ["Brackets:", "12 − 8 = 4"], ["Multiply:", "2 × 4"]], answer="8", check="2*(12-(3+5))==8"),
                figtext=["“Multiply 6 by 4, then add 3” → (6 × 4) + 3", "“Add 6 and 4, then multiply by 3” → 3 × (6 + 4)", "4 × (93 + 18) is 4 times as large as 93 + 18"],
                remember=["You can compare expressions without calculating.", "Words like “sum,” “difference,” “product,” and “quotient” name operations."],
                watch=[["Working left to right", "3 + 4 × 2 = 11, not 14"], ["Forgetting parentheses", "“add, then multiply” needs ( )"]],
                tryit=[["(15 − 3) ÷ 4 + 2 = ?", "5", "(15-3)/4+2==5"], ["Write “subtract 2 from 9, then multiply by 5.”", "5 × (9 − 2)", "5*(9-2)==35"]]),
           dict(big="A pattern follows a rule. Two patterns can be compared term by term and graphed as ordered pairs.",
                vocab=["pattern", "rule", "term", "ordered pair"],
                how=dict(text="Pattern A: start 0, add 3. Pattern B: start 0, add 6.", example="Compare the terms.", steps=[["A:", "0, 3, 6, 9"], ["B:", "0, 6, 12, 18"]], answer="Each B term is 2 times the A term", check="[3,6,9].every((a,i)=>[6,12,18][i]==2*a)"),
                fig=("coord", {"xmax": 10, "ymax": 20, "step": 2, "points": [{"x": 0, "y": 0}, {"x": 3, "y": 6}, {"x": 6, "y": 12}, {"x": 9, "y": 18}]}, "Graphing (A, B): (0, 0), (3, 6), (6, 12), (9, 18) — the points line up."),
                remember=["The first number of the pair comes from Pattern A, the second from Pattern B.", "Check the rule on more than one term."],
                watch=[["Mixing up the order", "(3, 6) is not (6, 3)"], ["“More” vs “times”", "6 is 3 more than 3, but 2 times 3"]],
                tryit=[["Start at 1, multiply by 3. What is the 5th term?", "81", "1*3**4==81"], ["A: add 5, B: add 15 (start 0). Pair for term 3?", "(10, 30)", "2*5==10&&2*15==30"]])])

# ---------------------------------------------------------------- Unit 5
u = "fraction-addition-subtraction"
V[u] = [("fraction", "A number that names equal parts of a whole.", "3/4"),
        ("numerator", "The top number; how many parts you have.", "In 3/4, the numerator is 3"),
        ("denominator", "The bottom number; how many equal parts make one whole.", "In 3/4, the denominator is 4"),
        ("equivalent fractions", "Fractions that name the same amount.", "1/2 = 2/4 = 3/6"),
        ("common denominator", "A denominator shared by two or more fractions.", "1/3 and 1/4 → 4/12 and 3/12"),
        ("least common denominator", "The smallest common denominator.", "LCD of 1/4 and 1/6 is 12"),
        ("simplest form", "A fraction whose numerator and denominator share no factor except 1.", "6/8 = 3/4"),
        ("mixed number", "A whole number and a fraction together.", "2 1/3"),
        ("improper fraction", "A fraction greater than or equal to 1, with numerator ≥ denominator.", "7/3"),
        ("benchmark fraction", "A friendly fraction used to estimate, such as 0, 1/2, or 1.", "5/8 is close to 1/2")]
CARDS[u] = [("What does the denominator tell us?", "How many equal parts make one whole.", "concept"),
            ("What does the numerator tell us?", "How many of those parts we have.", "concept"),
            ("Why can’t you add 1/2 + 1/3 by adding tops and bottoms?", "The parts are different sizes. Rename them with a common denominator: 3/6 + 2/6 = 5/6.", "misconception"),
            ("Rename 3/4 with denominator 12.", "9/12 (multiply top and bottom by 3)", "rule"),
            ("1/2 + 1/4 in your head", "3/4", "mental"),
            ("1 − 3/8 = ?", "5/8 (1 = 8/8)", "mental"),
            ("How do you regroup to subtract 3 1/4 − 1 3/4?", "Rename 3 1/4 as 2 5/4. Then 2 5/4 − 1 3/4 = 1 2/4 = 1 1/2.", "rule"),
            ("Is 2/5 + 1/2 more or less than 1?", "Less: 2/5 is less than 1/2, so the sum is less than 1/2 + 1/2.", "concept"),
            ("Show 3/4 using a picture.", "A bar or circle cut into 4 equal parts with 3 parts shaded.", "representation")]
VIS[u] = [("Show 3/4 using a picture.", "fraction_bars", {"bars": [{"parts": 4, "shaded": 3, "label": "3/4"}]}, "A model with 3 of 4 equal parts shaded."),
          ("Which fractions are equivalent?", "fraction_bars", {"bars": [{"parts": 3, "shaded": 2, "label": "2/3"}, {"parts": 6, "shaded": 4, "label": "4/6"}]}, "2/3 = 4/6: the same amount is shaded."),
          ("Use the model to add 1/2 + 1/3.", "fraction_bars", {"bars": [{"parts": 2, "shaded": 1, "label": "1/2"}, {"parts": 3, "shaded": 1, "label": "1/3"}, {"parts": 6, "shaded": 5, "label": "5/6"}]}, "3/6 + 2/6 = 5/6"),
          ("Is 7/8 closest to 0, 1/2, or 1?", "number_line", {"lo": "0", "hi": "1", "den": 8, "labels": "whole", "points": [{"x": "7/8", "label": "7/8"}]}, "1")]
SHEET[u] = dict(focus="equivalent fractions and adding or subtracting with unlike denominators", morefocus="mixed numbers, estimating with benchmarks, and word problems",
    sides=[dict(big="You can only add or subtract parts that are the same size. Rename the fractions with a common denominator first.",
                vocab=["numerator", "denominator", "equivalent fractions", "common denominator"],
                how=dict(text="Add 2/3 + 1/4.", example="2/3 + 1/4", steps=[["Common denominator 12:", "8/12 + 3/12"], ["Add the numerators:", "11/12"]], answer="11/12", check="Math.abs(2/3+1/4-11/12)<1e-12"),
                fig=("fraction_bars", {"bars": [{"parts": 3, "shaded": 2, "label": "2/3"}, {"parts": 12, "shaded": 8, "label": "8/12"}]}, "2/3 and 8/12 cover the same amount."),
                remember=["Multiply the numerator AND denominator by the same number.", "Keep the denominator when you add: 3/8 + 2/8 = 5/8."],
                watch=[["Adding the denominators", "1/2 + 1/3 is not 2/5"], ["Not simplifying", "6/8 → 3/4"]],
                tryit=[["5/6 − 1/4 = ?", "7/12", "Math.abs(5/6-1/4-7/12)<1e-12"], ["Rename 3/5 with denominator 20.", "12/20", "3/5==12/20"]]),
           dict(big="With mixed numbers, add or subtract the fractions and the whole numbers. Use benchmarks (0, 1/2, 1) to check if an answer makes sense.",
                vocab=["mixed number", "improper fraction", "simplest form", "benchmark fraction"],
                how=dict(text="Subtract 4 1/3 − 1 5/6.", example="4 1/3 − 1 5/6", steps=[["Common denominator:", "4 2/6 − 1 5/6"], ["Regroup a whole:", "3 8/6 − 1 5/6"], ["Subtract:", "2 3/6 = 2 1/2"]], answer="2 1/2", check="Math.abs((4+1/3)-(1+5/6)-2.5)<1e-12"),
                fig=("number_line", {"lo": "0", "hi": "1", "den": 8, "labels": "whole", "points": [{"x": "3/8", "label": "3/8"}, {"x": "7/8", "label": "7/8", "color": "#2f7fd8"}]}, "3/8 is close to 1/2 and 7/8 is close to 1, so 3/8 + 7/8 is about 1 1/2."),
                remember=["One whole = denominator over itself: 1 = 5/5.", "Estimate first: 2/5 + 1/2 must be less than 1."],
                watch=[["Not regrouping", "3 1/4 − 1 3/4 needs 2 5/4"], ["Unreasonable answers", "3/8 + 1/2 cannot be 4/10"]],
                tryit=[["2 3/4 + 1 1/2 = ?", "4 1/4", "Math.abs(2.75+1.5-4.25)<1e-12"], ["Estimate 7/8 + 5/12 with benchmarks.", "about 1 1/2", "true"]])])

# ---------------------------------------------------------------- Unit 6
u = "fraction-multiplication-division"
V[u] = [("fraction as division", "a/b means a ÷ b.", "3/4 = 3 ÷ 4"),
        ("product", "The answer to a multiplication problem.", "1/2 × 3/5 = 3/10"),
        ("scaling", "Resizing a number by multiplying by a factor.", "1/2 × 8 is half of 8"),
        ("unit fraction", "A fraction with a numerator of 1.", "1/5"),
        ("area", "The number of square units that cover a flat shape.", "1/2 ft × 1/3 ft = 1/6 square foot"),
        ("quotient", "The answer to a division problem.", "4 ÷ 1/2 = 8"),
        ("factor", "A number being multiplied.", "In 2/3 × 6, the factors are 2/3 and 6"),
        ("whole number", "A number like 0, 1, 2, 3, … with no fraction part.", "7")]
CARDS[u] = [("What does 3/4 mean as division?", "3 ÷ 4", "symbol"),
            ("How do you multiply 2/3 × 4/5?", "Multiply numerators and denominators: 8/15.", "rule"),
            ("What is 2/3 of 12?", "8 (12 ÷ 3 = 4, then 4 × 2)", "mental"),
            ("Is 3/4 × 20 more or less than 20? Why?", "Less, because 3/4 is less than 1.", "concept"),
            ("Is 5/4 × 20 more or less than 20? Why?", "More, because 5/4 is greater than 1.", "concept"),
            ("4 ÷ 1/3 = ?", "12 (there are 3 thirds in each whole)", "mental"),
            ("1/3 ÷ 4 = ?", "1/12 (split one third into 4 parts)", "mental"),
            ("Does multiplying always make a number bigger?", "No. Multiplying by a number less than 1 makes it smaller.", "misconception"),
            ("Why is 2/3 × 4/4 equal to 2/3?", "4/4 = 1, and multiplying by 1 keeps the value the same.", "concept")]
VIS[u] = [("The model shows 2/3 × 3/4. What is the product?", "area_grid", {"rows": 3, "cols": 4, "sh_rows": 2, "sh_cols": 3, "mode": "overlap", "left": "2/3", "top": "3/4"}, "6/12 = 1/2"),
          ("How many 1/4s fit in 2?", "number_line", {"lo": "0", "hi": "2", "den": 4, "labels": "all", "jumps": [[f"{i}/4", f"{i + 1}/4"] for i in range(8)]}, "8, so 2 ÷ 1/4 = 8"),
          ("3 pies are shared by 4 people. How much does each get?", "fraction_circle", {"parts": 4, "shaded": 3, "circles": 3, "per_circle": 1}, "3/4 of a pie")]
SHEET[u] = dict(focus="fractions as division and multiplying fractions", morefocus="area, scaling, and dividing with unit fractions",
    sides=[dict(big="A fraction is a division: a/b = a ÷ b. To multiply fractions, multiply the numerators and multiply the denominators.",
                vocab=["fraction as division", "product", "factor", "whole number"],
                how=dict(text="Multiply 3/4 × 2/5.", example="3/4 × 2/5", steps=[["Numerators:", "3 × 2 = 6"], ["Denominators:", "4 × 5 = 20"], ["Simplify:", "6/20 = 3/10"]], answer="3/10", check="Math.abs(3/4*2/5-3/10)<1e-12"),
                fig=("area_grid", {"rows": 4, "cols": 5, "sh_rows": 3, "sh_cols": 2, "mode": "overlap", "left": "3/4", "top": "2/5"}, "The overlap is 6 of 20 parts: 3/4 × 2/5 = 6/20 = 3/10."),
                remember=["“Of” means multiply: 2/3 of 9 = 6.", "5 ÷ 8 = 5/8, and 17 ÷ 5 = 3 2/5."],
                watch=[["Cross-multiplying", "multiply straight across"], ["Adding denominators", "1/2 × 1/3 = 1/6, not 1/5"]],
                tryit=[["2/3 × 15 = ?", "10", "2/3*15==10"], ["4 friends share 7 pizzas. How much each?", "1 3/4 pizzas", "7/4==1.75"]]),
           dict(big="Multiplying by a fraction less than 1 shrinks a number; greater than 1 grows it. Dividing by a unit fraction asks how many pieces fit.",
                vocab=["scaling", "unit fraction", "area", "quotient"],
                how=dict(text="Divide 3 ÷ 1/4.", example="How many fourths are in 3?", steps=[["Each whole has 4 fourths:", "3 × 4"]], answer="12", check="3/(1/4)==12"),
                fig=("fraction_bars", {"bars": [{"parts": 3, "shaded": 1, "label": "1/3"}, {"parts": 6, "shaded": 1, "label": "1/6"}]}, "1/3 ÷ 2 = 1/6: one third split into 2 equal parts."),
                remember=["Area of a rectangle = length × width, even with fractions.", "Check: 12 × 1/4 = 3 and 1/6 × 2 = 1/3."],
                watch=[["Dividing makes smaller?", "6 ÷ 1/2 = 12 is bigger than 6"], ["Mixed numbers", "write them as fractions before multiplying"]],
                tryit=[["1/2 × 3/4 square foot rectangle area?", "3/8 square foot", "1/2*3/4==3/8"], ["1/5 ÷ 3 = ?", "1/15", "Math.abs((1/5)/3-1/15)<1e-12"]])])

# ---------------------------------------------------------------- Unit 7
u = "measurement-conversions"
V[u] = [("convert", "Change a measurement to a different unit.", "3 feet = 36 inches"),
        ("customary units", "Units used in the United States: inches, feet, yards, miles, ounces, pounds, cups, quarts, gallons.", "1 foot = 12 inches"),
        ("metric units", "Units based on powers of 10: millimeters, meters, grams, liters.", "1 meter = 100 centimeters"),
        ("length", "How long something is.", "a pencil is 18 centimeters long"),
        ("weight / mass", "How heavy something is.", "a puppy weighs 12 pounds"),
        ("capacity", "How much a container holds.", "a jug holds 1 gallon"),
        ("kilo-", "A prefix meaning 1,000.", "1 kilometer = 1,000 meters"),
        ("centi-", "A prefix meaning 1/100.", "1 centimeter = 0.01 meter"),
        ("milli-", "A prefix meaning 1/1000.", "1 milliliter = 0.001 liter")]
CARDS[u] = [("1 foot = ? inches", "12 inches", "rule"), ("1 yard = ? feet", "3 feet", "rule"), ("1 mile = ? feet", "5,280 feet", "rule"),
            ("1 pound = ? ounces", "16 ounces", "rule"), ("1 gallon = ? quarts", "4 quarts", "rule"), ("1 quart = ? cups", "4 cups (and 1 pint = 2 cups)", "rule"),
            ("1 kilogram = ? grams", "1,000 grams", "rule"), ("1 meter = ? centimeters", "100 centimeters", "rule"),
            ("Big unit to small unit: multiply or divide?", "Multiply — you need MORE of the small units.", "concept"),
            ("5 centimeters = ? meters", "0.05 meter (divide by 100)", "mental"),
            ("Kai says 48 inches = 576 feet. What went wrong?", "He multiplied. Inches to feet means divide: 48 ÷ 12 = 4 feet.", "misconception")]
VIS[u] = [("How long is the crayon?", "ruler", {"length": 6, "den": 8, "end": "3 5/8", "object": "crayon"}, "3 5/8 inches"),
          ("Complete the table: feet → inches", "table", {"header": ["Feet", "Inches"], "rows": [["1", "12"], ["2", "24"], ["3", "36"], ["5", "60"]]}, "Multiply feet by 12.")]
SHEET[u] = dict(focus="customary conversions for length, weight and capacity", morefocus="metric conversions and multi-step measurement problems",
    sides=[dict(big="To change a big unit to a small unit, multiply. To change a small unit to a big unit, divide.",
                vocab=["convert", "customary units", "weight / mass", "capacity"],
                how=dict(text="Convert 3 1/2 feet to inches.", example="3 1/2 feet = ? inches", steps=[["1 foot = 12 inches:", "3 1/2 × 12"]], answer="42 inches", check="3.5*12==42"),
                figtext=["Length: 1 foot = 12 inches · 1 yard = 3 feet · 1 mile = 5,280 feet", "Weight: 1 pound = 16 ounces · 1 ton = 2,000 pounds", "Capacity: 1 cup = 8 fluid ounces · 1 pint = 2 cups · 1 quart = 2 pints · 1 gallon = 4 quarts"],
                remember=["Write remainders as the smaller unit: 50 inches = 4 feet 2 inches.", "Check: does the number get bigger when the unit gets smaller?"],
                watch=[["Multiplying when you should divide", "inches → feet means ÷ 12"], ["Mixing units", "convert before you add"]],
                tryit=[["7 quarts = ? cups", "28 cups", "7*4==28"], ["70 ounces = ? pounds ? ounces", "4 pounds 6 ounces", "4*16+6==70"]]),
           dict(big="Metric units go up and down by powers of 10, so you move the decimal point.",
                vocab=["metric units", "kilo-", "centi-", "milli-"],
                how=dict(text="Convert 2,450 grams to kilograms.", example="2,450 grams = ? kilograms", steps=[["1 kilogram = 1,000 grams:", "2,450 ÷ 1,000"]], answer="2.45 kilograms", check="2450/1000==2.45"),
                figtext=["1 kilometer = 1,000 meters", "1 meter = 100 centimeters = 1,000 millimeters", "1 kilogram = 1,000 grams · 1 liter = 1,000 milliliters"],
                remember=["× 10, 100 or 1,000: move the point right. ÷: move it left.", "Solve multi-step problems one step at a time."],
                watch=[["Wrong power of 10", "centi- is 100, milli- is 1,000"], ["Dropping the unit", "always write the unit in your answer"]],
                tryit=[["3.2 liters = ? milliliters", "3,200 milliliters", "3.2*1000==3200"], ["6 pieces of 18-inch ribbon = ? feet", "9 feet", "6*18/12==9"]])])

# ---------------------------------------------------------------- Unit 8
u = "volume-three-dimensional-figures"
V[u] = [("volume-three-dimensional-figures", "The amount of space inside a solid figure.", "a box holds 24 cubic units"),
        ("unit cube", "A cube with edges 1 unit long; it has a volume of 1 cubic unit.", "a 1 cm cube"),
        ("cubic unit", "A unit for measuring volume.", "cubic centimeters, cubic inches"),
        ("rectangular prism", "A solid figure with 6 rectangular faces.", "a cereal box"),
        ("base", "A face of a prism; B is its area in V = B × h.", "B = 4 × 3 = 12 square units"),
        ("height", "The distance from the base to the top.", "h = 5 inches"),
        ("edge", "The line segment where two faces meet.", "a cube has 12 edges"),
        ("composite figure", "A solid made of two or more prisms.", "an L-shaped block")]
CARDS[u] = [("What is the formula for the volume of a rectangular prism?", "V = l × w × h, or V = B × h", "rule"),
            ("What is B in V = B × h?", "The area of the base (length × width).", "symbol"),
            ("Why is volume measured in cubic units?", "Volume counts cubes that fill the space in three directions.", "concept"),
            ("How do you find the volume of an L-shaped solid?", "Split it into two prisms, find each volume, and add.", "rule"),
            ("2 × 3 × 4 in your head", "24", "mental"),
            ("A cube has edges of 3 cm. What is its volume?", "27 cubic centimeters", "mental"),
            ("Does a box with gaps between cubes show the true volume?", "No. Cubes must fill the box with no gaps or overlaps.", "misconception"),
            ("Is volume the same as surface area?", "No. Volume fills the inside (cubic units); surface area covers the outside (square units).", "misconception")]
VIS[u] = [("What is the volume in cubic units?", "cubes", {"blocks": [{"l": 4, "w": 2, "h": 3}], "labels": True, "unit_word": "cubes"}, "4 × 2 × 3 = 24 cubic units"),
          ("Find the volume.", "prism", {"l": 6, "w": 3, "h": 4, "lt": "6 cm", "wt": "3 cm", "ht": "4 cm"}, "6 × 3 × 4 = 72 cubic centimeters"),
          ("Find the total volume.", "composite", {"a": {"l": 3, "w": 2, "h": 5, "lt": "3 ft", "wt": "2 ft", "ht": "5 ft"}, "b": {"l": 4, "w": 2, "h": 2, "lt": "4 ft", "ht": "2 ft"}}, "30 + 16 = 46 cubic feet")]
SHEET[u] = dict(focus="unit cubes and counting cubes to find volume", morefocus="volume formulas, composite figures and word problems",
    sides=[dict(big="Volume tells how many unit cubes fill a solid with no gaps or overlaps. Count one layer, then multiply by the number of layers.",
                vocab=["volume-three-dimensional-figures", "unit cube", "cubic unit", "rectangular prism"],
                how=dict(text="Find the volume of a box 5 cubes long, 3 wide, 2 tall.", example="Layers of cubes", steps=[["One layer:", "5 × 3 = 15 cubes"], ["2 layers:", "15 × 2"]], answer="30 cubic units", check="5*3*2==30"),
                fig=("cubes", {"blocks": [{"l": 5, "w": 3, "h": 2}], "labels": True, "unit_word": "cubes"}, "5 × 3 = 15 cubes in each layer; 2 layers make 30 cubes."),
                remember=["Volume units are cubic: cubic centimeters, cubic inches, cubic feet.", "The order of multiplying does not matter: (5 × 3) × 2 = 5 × (3 × 2)."],
                watch=[["Counting only the cubes you see", "include the hidden cubes"], ["Using square units", "volume uses CUBIC units"]],
                tryit=[["A box is 4 by 4 by 3 cubes. Volume?", "48 cubic units", "4*4*3==48"], ["12 cubes in a layer, 5 layers. Volume?", "60 cubic units", "12*5==60"]]),
           dict(big="Use V = l × w × h or V = B × h. Volume is additive: split a composite solid into prisms and add their volumes.",
                vocab=["base", "height", "edge", "composite figure"],
                how=dict(text="Find the volume of the L-shaped solid.", example="Two prisms: 4 × 3 × 6 and 5 × 3 × 2", steps=[["Prism 1:", "4 × 3 × 6 = 72"], ["Prism 2:", "5 × 3 × 2 = 30"], ["Add:", "72 + 30"]], answer="102 cubic feet", check="4*3*6+5*3*2==102"),
                fig=("composite", {"a": {"l": 4, "w": 3, "h": 6, "lt": "4 ft", "wt": "3 ft", "ht": "6 ft"}, "b": {"l": 5, "w": 3, "h": 2, "lt": "5 ft", "ht": "2 ft"}}, "Split the solid into two prisms that do not overlap."),
                remember=["Missing height? h = V ÷ (l × w).", "Doubling one edge doubles the volume."],
                watch=[["Treating it as one big box", "add the two prisms instead"], ["Adding the edges", "multiply length × width × height"]],
                tryit=[["B = 20 square inches, h = 6 inches. Volume?", "120 cubic inches", "20*6==120"], ["V = 96, l = 6, w = 4. Height?", "4", "96/(6*4)==4"]])])

# ---------------------------------------------------------------- Unit 9
u = "coordinate-plane-graphing"
V[u] = [("coordinate plane", "A grid made by two perpendicular number lines.", "used to locate points"),
        ("x-axis", "The horizontal number line on a coordinate plane.", "goes left to right"),
        ("y-axis", "The vertical number line on a coordinate plane.", "goes up and down"),
        ("origin", "The point (0, 0) where the axes meet.", "start here to plot"),
        ("ordered pair", "Two numbers (x, y) that tell where a point is.", "(4, 7)"),
        ("x-coordinate", "The first number: how far to move right.", "4 in (4, 7)"),
        ("y-coordinate", "The second number: how far to move up.", "7 in (4, 7)"),
        ("perpendicular", "Lines that meet to form right angles.", "the x-axis and y-axis")]
CARDS[u] = [("What does the first number in (5, 2) tell you?", "Move 5 units right (along the x-axis).", "symbol"),
            ("What does the second number in (5, 2) tell you?", "Move 2 units up (along the y-axis).", "symbol"),
            ("Are (3, 6) and (6, 3) the same point?", "No. Order matters: x comes first.", "misconception"),
            ("Where is (0, 5)?", "On the y-axis, 5 units up.", "concept"),
            ("Distance from (2, 3) to (2, 9)?", "6 units (9 − 3)", "mental"),
            ("A graph has x = hours, y = miles. What does (3, 120) mean?", "After 3 hours, 120 miles.", "concept"),
            ("Memory trick for plotting", "Walk before you climb: right first, then up.", "rule")]
VIS[u] = [("What are the coordinates of point A?", "coord", {"xmax": 8, "ymax": 8, "points": [{"x": 3, "y": 5, "label": "A"}]}, "(3, 5)"),
          ("Which point is at (6, 2)?", "coord", {"xmax": 8, "ymax": 8, "points": [{"x": 2, "y": 6, "label": "P"}, {"x": 6, "y": 2, "label": "Q"}]}, "Q (P is at (2, 6))")]
SHEET[u] = dict(focus="the coordinate system, plotting and reading points", morefocus="real-world graphs and graphing patterns",
    sides=[dict(big="An ordered pair (x, y) gives directions from the origin: move x units right, then y units up.",
                vocab=["origin", "x-axis", "y-axis", "ordered pair"],
                how=dict(text="Plot point B at (4, 6).", example="Start at (0, 0).", steps=[["Right:", "4 units"], ["Up:", "6 units"]], answer="B is at (4, 6)", check="true"),
                fig=("coord", {"xmax": 8, "ymax": 8, "points": [{"x": 4, "y": 6, "label": "B"}, {"x": 6, "y": 4, "label": "C"}]}, "B (4, 6) and C (6, 4) are different points."),
                remember=["The origin is (0, 0).", "Points on the x-axis have y = 0; points on the y-axis have x = 0."],
                watch=[["Swapping the numbers", "(4, 6) is not (6, 4)"], ["Counting boxes", "count grid LINES from 0"]],
                tryit=[["Start at (2, 3). Move 4 right and 1 up.", "(6, 4)", "2+4==6&&3+1==4"], ["Distance from (1, 5) to (7, 5)?", "6 units", "7-1==6"]]),
           dict(big="Graphs show how two quantities are related. Read the axis labels to know what each coordinate means.",
                vocab=["coordinate plane", "x-coordinate", "y-coordinate", "perpendicular"],
                how=dict(text="A plant grows 2 cm each week (start at 0).", example="Make ordered pairs (week, height).", steps=[["Pairs:", "(0, 0), (1, 2), (2, 4), (3, 6)"]], answer="After 3 weeks: 6 cm", check="3*2==6"),
                fig=("coord", {"xmax": 5, "ymax": 10, "points": [{"x": 0, "y": 0}, {"x": 1, "y": 2}, {"x": 2, "y": 4}, {"x": 3, "y": 6}, {"x": 4, "y": 8}], "path": [[0, 0], [4, 8]], "xlab": "Weeks", "ylab": "Height (cm)"}, "The points make a straight-line pattern."),
                remember=["x often shows time or the first pattern; y shows the amount.", "Use a pattern rule to predict the next point."],
                watch=[["Ignoring the scale", "some graphs count by 2s, 5s or 10s"], ["Reading the wrong axis", "x is across, y is up"]],
                tryit=[["(x, y) with y = 3 × x. Find y when x = 5.", "15", "3*5==15"], ["Walk (1, 1) → (5, 1) → (5, 4). Blocks?", "7 blocks", "4+3==7"]])])

# ---------------------------------------------------------------- Unit 10
u = "classifying-two-dimensional-figures"
V[u] = [("polygon", "A closed flat shape made of straight sides.", "triangle, pentagon"),
        ("parallel", "Always the same distance apart; never meet.", "opposite sides of a rectangle"),
        ("perpendicular", "Meeting to form a right angle.", "sides of a square"),
        ("right angle", "An angle of exactly 90°.", "the corner of a page"),
        ("acute / obtuse angle", "Acute: less than 90°. Obtuse: greater than 90°.", "45° is acute; 120° is obtuse"),
        ("equilateral / isosceles / scalene", "3 equal sides / exactly 2 equal sides / no equal sides.", "sides 5, 5, 8 → isosceles"),
        ("quadrilateral", "A polygon with 4 sides.", "square, trapezoid"),
        ("parallelogram", "A quadrilateral with 2 pairs of parallel sides.", "rectangles and rhombuses are parallelograms"),
        ("rhombus", "A parallelogram with 4 equal sides.", "a tilted square shape"),
        ("hierarchy", "An organized chart where each group belongs to the group above it.", "square → rectangle → parallelogram → quadrilateral")]
CARDS[u] = [("Is every square a rectangle?", "Yes. A square has 4 right angles, so it is a rectangle.", "concept"),
            ("Is every rectangle a square?", "No. A rectangle’s sides do not have to be equal.", "misconception"),
            ("What do tick marks on sides mean?", "Sides with the same number of tick marks are equal.", "symbol"),
            ("What do arrow marks on sides mean?", "Sides with matching arrows are parallel.", "symbol"),
            ("What does a small square in a corner mean?", "A right angle (90°).", "symbol"),
            ("A triangle has a 100° angle. What kind is it?", "Obtuse", "mental"),
            ("Which shapes are always parallelograms?", "Rectangles, rhombuses and squares.", "concept"),
            ("If all rectangles have 4 right angles and squares are rectangles, then…", "all squares have 4 right angles.", "rule")]
VIS[u] = [("Name this quadrilateral.", "shape", {"pts": [[0, 0], [5, 0], [8, 4], [3, 4]], "ticks": [[0, 1], [1, 1], [2, 1], [3, 1]], "arrows": [[0, 1], [2, 1], [1, 2], [3, 2]], "fill": "pink"}, "Rhombus: 4 equal sides, 2 pairs of parallel sides."),
          ("Classify the triangle by its sides.", "shape", {"pts": [[0, 0], [4, 0], [2, 5]], "ticks": [[1, 1], [2, 1]], "fill": "orange"}, "Isosceles (two equal sides)")]
SHEET[u] = dict(focus="polygon attributes and classifying triangles", morefocus="classifying quadrilaterals and shape hierarchies",
    sides=[dict(big="Classify shapes by their attributes: number of sides, equal sides, parallel sides and kinds of angles.",
                vocab=["polygon", "parallel", "perpendicular", "equilateral / isosceles / scalene"],
                how=dict(text="Classify a triangle with sides 6, 6, 6.", example="All three sides equal.", steps=[["By sides:", "equilateral"], ["Each angle:", "60°, so acute"]], answer="acute equilateral", check="6==6"),
                fig=("shape_row", {"items": [{"pts": [[0, 0], [4, 0], [2, 3.46]], "label": "equilateral", "ticks": [[0, 1], [1, 1], [2, 1]]}, {"pts": [[0, 0], [4, 0], [2, 5]], "label": "isosceles", "ticks": [[1, 1], [2, 1]]}, {"pts": [[0, 0], [4, 0], [0, 3]], "label": "right", "right": [0]}]}, "Tick marks show equal sides; a small square shows a right angle."),
                remember=["Acute: all angles < 90°. Right: one 90° angle. Obtuse: one angle > 90°.", "Triangles get two names: one for angles, one for sides."],
                watch=[["Judging by looks", "use the marks and measurements"], ["Right AND obtuse?", "a triangle can have only one angle of 90° or more"]],
                tryit=[["Angles 30°, 60°, 90°. Classify by angles.", "right", "30+60+90==180"], ["Sides 3, 4, 5. Classify by sides.", "scalene", "3!=4&&4!=5"]]),
           dict(big="Shapes belong to families. Every attribute of a family belongs to all its members: a square is a rectangle, a rhombus, a parallelogram and a quadrilateral.",
                vocab=["quadrilateral", "parallelogram", "rhombus", "hierarchy"],
                how=dict(text="What names describe a square?", example="4 equal sides, 4 right angles, 2 pairs of parallel sides.", steps=[["Has 2 parallel pairs:", "parallelogram"], ["Has 4 right angles:", "rectangle"], ["Has 4 equal sides:", "rhombus"]], answer="square, rectangle, rhombus, parallelogram, quadrilateral", check="true"),
                figtext=["Quadrilateral (4 sides)", "→ Parallelogram (2 pairs of parallel sides)", "→ Rectangle (4 right angles)  and  Rhombus (4 equal sides)", "→ Square (both!)"],
                remember=["“All squares are rectangles” is true; “all rectangles are squares” is false.", "A trapezoid in these lessons has exactly one pair of parallel sides."],
                watch=[["Reversing the arrow", "every rhombus is a parallelogram, not the other way"], ["Most specific name", "a square is best named “square”"]],
                tryit=[["True or false: all rhombuses are squares.", "false", "true"], ["Name a shape that is a rectangle and a rhombus.", "square", "true"]])])

# ---------------------------------------------------------------- Unit 11
u = "data-line-plots-problem-solving"
V[u] = [("data", "Information collected, often numbers.", "lengths of 10 leaves"),
        ("line plot", "A number line with an X for each data value.", "X’s above 1/4, 1/2, 3/4"),
        ("frequency", "How many times a value appears.", "three X’s above 1/2"),
        ("scale", "The equal spacing marked on the number line.", "marks every 1/8 inch"),
        ("most common value", "The value with the most X’s (the mode).", "the tallest stack of X’s"),
        ("range", "The difference between the greatest and least values.", "1 1/4 − 1/4 = 1"),
        ("fair share", "The amount each would get if a total were shared equally.", "total ÷ number of items"),
        ("strategy", "A plan for solving a problem.", "draw a picture, work backward")]
CARDS[u] = [("What does each X on a line plot stand for?", "One data value (one measurement).", "concept"),
            ("How do you find the total from a line plot?", "Multiply each value by its number of X’s, then add.", "rule"),
            ("How do you find a fair share from a line plot?", "Find the total, then divide by the number of X’s.", "rule"),
            ("Three X’s are above 1/4. What is their total?", "3/4 (3 × 1/4)", "mental"),
            ("Range of 1/8, 3/8, 7/8?", "3/4 (7/8 − 1/8 = 6/8)", "mental"),
            ("Should a line plot skip values that have no data?", "No. Keep equal spacing and show every mark on the scale.", "misconception"),
            ("Steps for a multi-step problem", "Read, plan, solve one step at a time, check that the answer makes sense.", "rule")]
VIS[u] = [("How many ribbons are 3/4 yard long?", "lineplot", {"values": ["1/4", "1/2", "1/2", "3/4", "3/4", "3/4", "1"], "lo": "0", "hi": "1", "den": 4, "title": "Ribbon Lengths", "unit": "Length (yards)"}, "3 ribbons"),
          ("What is the total length of all the ribbons?", "lineplot", {"values": ["1/4", "1/2", "1/2", "3/4", "1"], "lo": "0", "hi": "1", "den": 4, "title": "Ribbon Lengths", "unit": "Length (yards)"}, "1/4 + 1/2 + 1/2 + 3/4 + 1 = 3 yards")]
SHEET[u] = dict(focus="reading and making line plots with fractions", morefocus="solving problems with line plot data and multi-step problems",
    sides=[dict(big="A line plot shows every measurement as an X above a number line. Stacks of X’s show how often each value happens.",
                vocab=["data", "line plot", "frequency", "scale"],
                how=dict(text="Make a line plot of 1/2, 1/4, 1/2, 3/4, 1/2.", example="Scale: 0 to 1 by fourths.", steps=[["Count:", "1/4 → 1, 1/2 → 3, 3/4 → 1"], ["Draw:", "one X per value"]], answer="3 X’s above 1/2", check="[0.5,0.25,0.5,0.75,0.5].filter(v=>v==0.5).length==3"),
                fig=("lineplot", {"values": ["1/4", "1/2", "1/2", "1/2", "3/4"], "lo": "0", "hi": "1", "den": 4, "title": "Plant Growth", "unit": "Inches"}, "The tallest stack is above 1/2."),
                remember=["Choose a scale that fits the smallest part (halves, fourths, eighths).", "Count your X’s: one for every data value."],
                watch=[["Uneven spacing", "every mark is the same distance apart"], ["Missing repeats", "two 1/2s need two X’s"]],
                tryit=[["Data: 1/8, 3/8, 3/8, 5/8. How many X’s above 3/8?", "2", "true"], ["Greatest minus least for that data?", "1/2", "5/8-1/8==1/2"]]),
           dict(big="Use fraction operations with line plot data: totals, differences, and fair shares. Solve multi-step problems one step at a time.",
                vocab=["most common value", "range", "fair share", "strategy"],
                how=dict(text="Beakers hold 1/4, 1/2, 1/2, 3/4 liter. Fair share?", example="Share the water equally.", steps=[["Total:", "1/4 + 1/2 + 1/2 + 3/4 = 2"], ["Share among 4:", "2 ÷ 4"]], answer="1/2 liter each", check="(0.25+0.5+0.5+0.75)/4==0.5"),
                fig=("lineplot", {"values": ["1/4", "1/2", "1/2", "3/4"], "lo": "0", "hi": "1", "den": 4, "title": "Water in Beakers", "unit": "Liters"}, "Total 2 liters shared by 4 beakers is 1/2 liter each."),
                remember=["Total = value × number of X’s, added up.", "Fair share = total ÷ number of data values."],
                watch=[["Adding values once", "count every X"], ["Skipping a step", "find the total BEFORE dividing"]],
                tryit=[["Total of 1/2, 1/2, 1/2, 1 (pounds)?", "2 1/2 pounds", "0.5*3+1==2.5"], ["Fair share of 3/4 and 1/4?", "1/2", "(0.75+0.25)/2==0.5"]])])
