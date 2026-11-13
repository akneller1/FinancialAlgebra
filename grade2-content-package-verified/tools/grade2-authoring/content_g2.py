"""Grade 2 reference content: vocabulary, concept flashcards, visual flashcards, cheat-sheet sides.
Every numeric example carries a check that build_content.py evaluates (Node) before anything is written.
Same structure as tools/grade3-authoring/content_g3.py so the shared cheat-sheet and flashcard builders read it unchanged."""

V = {}      # unit -> [(term, definition, example)]
CARDS = {}  # unit -> [(front, back, kind)]
VIS = {}    # unit -> [(front, figure kind, figure data, back)]
SHEET = {}  # unit -> dict(focus, morefocus, sides=[side, side])

# ---------------------------------------------------------------- Unit 1
u = "add-subtract-20"
V[u] = [("sum", "The answer when you add.", "8 + 5 = 13, so 13 is the sum"),
        ("difference", "The answer when you subtract.", "13 − 5 = 8, so 8 is the difference"),
        ("addend", "A number that is added.", "In 8 + 5, the addends are 8 and 5"),
        ("make a ten", "Break apart a number to make 10 first.", "8 + 5 = 8 + 2 + 3 = 10 + 3"),
        ("doubles", "Adding a number to itself.", "6 + 6 = 12"),
        ("doubles plus one", "A double and 1 more.", "6 + 7 = 6 + 6 + 1 = 13"),
        ("fact family", "Facts that use the same three numbers.", "8 + 5 = 13, 5 + 8 = 13, 13 − 5 = 8, 13 − 8 = 5"),
        ("equal sign", "Means “is the same as.”", "9 + 4 = 10 + 3"),
        ("think addition", "Use an addition fact to subtract.", "14 − 6: 6 + 8 = 14, so 8")]
CARDS[u] = [("What is 9 + 6? Make a ten.", "9 + 1 = 10, then 10 + 5 = 15.", "strategy"),
            ("What is 7 + 8? Use a double.", "7 + 7 = 14, so 7 + 8 = 15.", "strategy"),
            ("What is 15 − 7? Think addition.", "7 + 8 = 15, so 15 − 7 = 8.", "strategy"),
            ("Go back through ten: 13 − 5", "13 − 3 = 10, then 10 − 2 = 8.", "strategy"),
            ("Write the fact family for 6, 9, 15.", "6 + 9 = 15, 9 + 6 = 15, 15 − 6 = 9, 15 − 9 = 6", "concept"),
            ("Is 8 + 4 = 12 + 1 true?", "No. 8 + 4 = 12, but 12 + 1 = 13.", "misconception"),
            ("Missing number: 7 + ___ = 16", "9, because 7 + 9 = 16.", "example"),
            ("Is 6 − 14 the same as 14 − 6?", "No. In subtraction, start with the whole: 14 − 6 = 8.", "misconception")]
VIS[u] = [("How many dots in all?", "groups", {"counts": [8, 6]}, "8 + 6 = 14 (make a ten: 8 + 2 + 4)"),
          ("Where does the jump land?", "jline", {"lo": 0, "hi": 20, "step": 1, "label_every": 5, "jumps": [[15, 7, "−8"]], "points": [{"v": 7, "label": "?"}]}, "15 − 8 = 7"),
          ("Find the missing part.", "bars", {"rows": [{"parts": [[17, "17"]]}, {"parts": [[9, "9"], [8, "?"]]}]}, "17 − 9 = 8, because 9 + 8 = 17")]
SHEET[u] = dict(focus="adding within 20 with make-a-ten and doubles", morefocus="subtracting by thinking addition, fact families and missing numbers",
    sides=[dict(big="Use what you know to add fast. Make a ten, or use a double you already know.",
                vocab=["sum", "addend", "make a ten", "doubles plus one"],
                how=dict(text="Add 8 + 7 by making a ten.", example="8 + 7", steps=[["Break 7 into", "2 and 5"], ["8 + 2 =", "10"], ["10 + 5 =", "15"]], answer="15", check="8+7==15&&8+2==10&&10+5==15"),
                fig=("groups", {"counts": [9, 4]}, "9 + 4: move 1 dot to make 10. Then 10 + 3 = 13."),
                remember=["Count on from the bigger number.", "Doubles: 5 + 5 = 10, 6 + 6 = 12, 7 + 7 = 14, 8 + 8 = 16, 9 + 9 = 18."],
                watch=[["Counting the start number", "8 + 3: say 9, 10, 11 (not 8, 9, 10)"], ["Forgetting the second part", "after making ten, add what is left"]],
                tryit=[["9 + 5", "14", "9+5==14"], ["6 + 7", "13", "6+7==13"]]),
           dict(big="Addition and subtraction are related. Use an addition fact to subtract, and use the equal sign to mean “is the same as.”",
                vocab=["difference", "fact family", "think addition", "equal sign"],
                how=dict(text="Find 16 − 9 by thinking addition.", example="9 + ? = 16", steps=[["Think:", "9 + 7 = 16"], ["So", "16 − 9 = 7"]], answer="7", check="16-9==7&&9+7==16"),
                fig=("bars", {"rows": [{"parts": [[16, "16"]]}, {"parts": [[9, "9"], [7, "?"]]}]}, "The whole is 16. One part is 9. The other part is 7."),
                remember=["The whole goes first in a subtraction fact.", "Check: the parts add up to the whole."],
                watch=[["7 + ___ = 15 → 22", "the equal sign is not “write the answer”. 7 + 8 = 15."], ["15 − 7 → 12", "do not subtract the ones digits: 15 − 7 = 8"]],
                tryit=[["14 − 6", "8", "14-6==8"], ["5 + ___ = 13", "8", "5+8==13"]])])

# ---------------------------------------------------------------- Unit 2
u = "odd-even-arrays"
V[u] = [("even", "A number of objects that can be put in pairs with none left over.", "14 is even: 7 pairs"),
        ("odd", "A number of objects that has one left over when you make pairs.", "13 is odd: 6 pairs and 1 left"),
        ("pair", "A group of 2.", "a pair of socks"),
        ("equal addends", "Addends that are the same number.", "16 = 8 + 8"),
        ("array", "Objects in equal rows and equal columns.", "3 rows of 4 dots"),
        ("row", "A line of objects that goes across.", "an array with 3 rows"),
        ("column", "A line of objects that goes up and down.", "an array with 4 columns"),
        ("repeated addition", "Adding the same number again and again.", "4 + 4 + 4 = 12")]
CARDS[u] = [("Is 17 odd or even?", "Odd. 17 makes 8 pairs with 1 left over.", "concept"),
            ("Even numbers end in which digits?", "0, 2, 4, 6, or 8.", "fact"),
            ("Write 18 as two equal addends.", "9 + 9 = 18", "example"),
            ("Can 11 be two equal addends?", "No. 11 is odd: 5 + 5 = 10 and 6 + 6 = 12.", "misconception"),
            ("3 rows of 5 dots: write an equation.", "5 + 5 + 5 = 15", "example"),
            ("3 rows of 5: is the total 3 + 5?", "No. Add 5 three times: 5 + 5 + 5 = 15.", "misconception"),
            ("Count by 2s to 20.", "2, 4, 6, 8, 10, 12, 14, 16, 18, 20", "strategy"),
            ("Add an array by rows or by columns?", "Either way gives the same total.", "rule")]
VIS[u] = [("Odd or even?", "counters", {"n": 13, "layout": "pairs"}, "Odd: one counter has no partner."),
          ("How many dots? Write an equation.", "array3", {"rows": 4, "cols": 5}, "5 + 5 + 5 + 5 = 20"),
          ("Write the even number as two equal addends.", "counters", {"n": 12, "layout": "pairs"}, "6 + 6 = 12")]
SHEET[u] = dict(focus="odd and even numbers and doubles", morefocus="arrays with up to 5 rows and 5 columns and repeated addition",
    sides=[dict(big="Make pairs. If every object has a partner, the number is even. If one is left over, the number is odd.",
                vocab=["even", "odd", "pair", "equal addends"],
                how=dict(text="Is 14 odd or even? Write it as two equal addends if you can.", example="14 counters", steps=[["Make pairs:", "7 pairs, none left"], ["Equal addends:", "7 + 7 = 14"]], answer="Even, 14 = 7 + 7", check="7+7==14&&14%2==0"),
                fig=("counters", {"n": 11, "layout": "pairs"}, "11 counters: 5 pairs and 1 left over, so 11 is odd."),
                remember=["Look at the ones digit: 0, 2, 4, 6, 8 means even.", "Every even number is a double."],
                watch=[["Looking at the tens digit", "12 is even even though the tens digit, 1, is odd"], ["Unequal addends", "14 = 10 + 4 is true, but the addends are not equal"]],
                tryit=[["Is 19 odd or even?", "odd", "19%2==1"], ["16 = ___ + ___ (equal addends)", "8 + 8", "8+8==16"]]),
           dict(big="An array has equal rows. Add the number in a row once for every row to find the total.",
                vocab=["array", "row", "column", "repeated addition"],
                how=dict(text="Find the total in 4 rows of 3.", example="4 rows of 3", steps=[["Each row:", "3"], ["Add 4 times:", "3 + 3 + 3 + 3"], ["Total:", "12"]], answer="12", check="3+3+3+3==12"),
                fig=("array3", {"rows": 3, "cols": 5}, "3 rows of 5: 5 + 5 + 5 = 15. By columns: 3 + 3 + 3 + 3 + 3 = 15."),
                remember=["Rows go across. Columns go up and down.", "Arrays in Grade 2 have up to 5 rows and 5 columns."],
                watch=[["Adding rows and columns", "3 rows of 4 is not 3 + 4 = 7"], ["Missing a row", "point to each row as you add"]],
                tryit=[["5 rows of 2", "10", "2+2+2+2+2==10"], ["2 rows of 5", "10", "5+5==10"]])])

# ---------------------------------------------------------------- Unit 3
u = "place-value-1000"
V[u] = [("digit", "One of the symbols 0 to 9 used to write numbers.", "425 has the digits 4, 2, and 5"),
        ("place value", "The value of a digit because of its place.", "In 425, the 4 is worth 400"),
        ("hundred", "Ten tens, or 100.", "10 tens = 1 hundred"),
        ("tens", "Groups of ten.", "6 tens = 60"),
        ("ones", "Single units.", "425 has 5 ones"),
        ("expanded form", "A number written as the sum of the values of its digits.", "425 = 400 + 20 + 5"),
        ("standard form", "A number written with digits.", "four hundred twenty-five is 425"),
        ("number name", "A number written in words.", "425 is four hundred twenty-five"),
        ("base-ten blocks", "Flats, rods, and cubes that show hundreds, tens, and ones.", "4 flats, 2 rods, 5 cubes is 425")]
CARDS[u] = [("How many tens make 100?", "10 tens.", "fact"),
            ("What is the value of the 7 in 372?", "70 (7 tens).", "concept"),
            ("Write 706 in expanded form.", "700 + 6", "example"),
            ("How many tens are in 140?", "14 tens (1 hundred and 4 tens).", "concept"),
            ("Is 5 hundreds written as 5?", "No. 5 hundreds is 500. The zeros show 0 tens and 0 ones.", "misconception"),
            ("Write “three hundred eight” in digits.", "308 (not 3008).", "misconception"),
            ("4 hundreds, 13 tens, 2 ones is what number?", "532, because 13 tens = 1 hundred and 3 tens.", "example"),
            ("What does the zero in 507 mean?", "There are 0 tens.", "concept")]
VIS[u] = [("What number do the blocks show?", "blocks", {"h": 3, "t": 4, "o": 6}, "3 hundreds, 4 tens, 6 ones = 346"),
          ("What number is in the chart?", "pv_chart", {"hundreds": 6, "tens": 0, "ones": 9}, "609"),
          ("How many tens? What number?", "blocks", {"t": 12}, "12 tens = 1 hundred and 2 tens = 120")]
SHEET[u] = dict(focus="hundreds as ten tens and the value of each digit", morefocus="reading and writing numbers three ways",
    sides=[dict(big="A hundred is ten tens. In a three-digit number, the digits tell how many hundreds, tens, and ones.",
                vocab=["hundred", "tens", "ones", "place value"],
                how=dict(text="What is the value of each digit in 538?", example="538", steps=[["5 hundreds:", "500"], ["3 tens:", "30"], ["8 ones:", "8"]], answer="500 + 30 + 8", check="500+30+8==538"),
                fig=("blocks", {"h": 2, "t": 3, "o": 4}, "2 flats, 3 rods, 4 cubes: 200 + 30 + 4 = 234."),
                remember=["10 ones = 1 ten. 10 tens = 1 hundred.", "100, 200, … 900 are 1 to 9 hundreds with 0 tens and 0 ones."],
                watch=[["The digit or its value?", "the 4 in 249 is worth 40, not 4"], ["Skipping the zero", "706 is 7 hundreds, 0 tens, 6 ones"]],
                tryit=[["Value of the 6 in 862", "60", "60==6*10"], ["How many tens in 300?", "30", "30*10==300"]]),
           dict(big="You can write the same number with digits, with words, and in expanded form.",
                vocab=["standard form", "number name", "expanded form", "digit"],
                how=dict(text="Write four hundred sixty-two three ways.", example="four hundred sixty-two", steps=[["Digits:", "462"], ["Expanded:", "400 + 60 + 2"], ["Words:", "four hundred sixty-two"]], answer="462", check="400+60+2==462"),
                figtext=["<b>Standard form:</b> 305", "<b>Number name:</b> three hundred five", "<b>Expanded form:</b> 300 + 5", "<b>Hundreds, tens, ones:</b> 3 hundreds, 0 tens, 5 ones"],
                remember=["Use a 0 to hold an empty place.", "Write a hyphen in two-digit names like forty-six."],
                watch=[["Writing what you hear", "three hundred eight is 308, not 3008"], ["Out-of-order parts", "6 + 400 + 20 is still 426"]],
                tryit=[["Write 790 in expanded form.", "700 + 90", "700+90==790"], ["Write 200 + 50 + 1 in digits.", "251", "200+50+1==251"]])])

# ---------------------------------------------------------------- Unit 4
u = "count-compare-1000"
V[u] = [("count on", "Say the numbers that come next.", "398, 399, 400, 401"),
        ("skip count", "Count by the same amount each time.", "by 5s: 35, 40, 45"),
        ("greater than", "More than. The symbol is >.", "512 > 498"),
        ("less than", "Fewer than. The symbol is <.", "389 < 398"),
        ("equal to", "The same amount. The symbol is =.", "400 = 400"),
        ("compare", "Decide which number is greater or less.", "compare the hundreds first"),
        ("10 more", "Add 1 to the tens digit.", "10 more than 365 is 375"),
        ("100 less", "Subtract 1 from the hundreds digit.", "100 less than 365 is 265")]
CARDS[u] = [("What comes after 499?", "500", "fact"),
            ("Count by 10s: 470, 480, 490, ___", "500", "example"),
            ("Count by 100s from 250.", "250, 350, 450, 550", "strategy"),
            ("Compare 489 and 512.", "489 < 512 because 4 hundreds < 5 hundreds.", "rule"),
            ("Is 389 greater than 401 because it has bigger digits?", "No. Compare hundreds first: 3 < 4, so 389 < 401.", "misconception"),
            ("10 more than 395?", "405", "example"),
            ("100 less than 604?", "504", "example"),
            ("How do you read 345 > 298?", "345 is greater than 298.", "concept")]
VIS[u] = [("What number goes in the box?", "chart", {"start": 381, "rows": 3, "hide": [397]}, "397 (10 more than 387)"),
          ("Where do you land?", "jline", {"lo": 220, "hi": 280, "step": 5, "label_every": 2, "jumps": [[230, 240, ""], [240, 250, ""], [250, 260, ""]], "points": [{"v": 260, "label": "?"}]}, "3 jumps of 10 from 230: 260"),
          ("Which is 10 more than the shaded number?", "chart", {"start": 541, "rows": 3, "shade": [556]}, "566")]
SHEET[u] = dict(focus="counting and skip counting within 1,000", morefocus="comparing three-digit numbers and adding or subtracting 10 and 100",
    sides=[dict(big="When you count past 9 ones, make a new ten. When you count past 9 tens, make a new hundred.",
                vocab=["count on", "skip count", "10 more", "100 less"],
                how=dict(text="Count by 10s from 470. Write the next 4 numbers.", example="470", steps=[["+10:", "480"], ["+10:", "490"], ["+10:", "500"], ["+10:", "510"]], answer="480, 490, 500, 510", check="470+40==510"),
                fig=("chart", {"start": 291, "rows": 3, "shade": [299, 300, 301]}, "299, 300, 301: count across the hundred."),
                remember=["By 5s: the ones digit goes 0, 5, 0, 5.", "By 10s: the tens digit changes. By 100s: the hundreds digit changes."],
                watch=[["After 109 comes 1010?", "No! After 109 comes 110."], ["395 + 10 = 3105?", "No! 395 + 10 = 405."]],
                tryit=[["Count by 5s: 85, 90, 95, ___", "100", "95+5==100"], ["10 less than 503", "493", "503-10==493"]]),
           dict(big="To compare, start with the biggest place. Only move to the next place when the digits are the same.",
                vocab=["compare", "greater than", "less than", "equal to"],
                how=dict(text="Compare 467 and 476.", example="467 ___ 476", steps=[["Hundreds:", "4 = 4"], ["Tens:", "6 < 7"], ["So", "467 < 476"]], answer="467 < 476", check="467<476"),
                figtext=["<b>&gt;</b> greater than: 720 &gt; 702", "<b>&lt;</b> less than: 199 &lt; 201", "<b>=</b> equal to: 500 = 5 hundreds"],
                remember=["The symbol opens toward the greater number.", "Hundreds first, then tens, then ones."],
                watch=[["Comparing ones first", "289 < 301 even though 9 > 1"], ["Bigger digits", "a 9 in the tens does not beat more hundreds"]],
                tryit=[["538 ___ 583", "<", "538<583"], ["100 more than 846", "946", "846+100==946"]])])

# ---------------------------------------------------------------- Unit 5
u = "add-subtract-100"
V[u] = [("regroup", "Trade 10 ones for 1 ten, or 1 ten for 10 ones.", "17 ones = 1 ten and 7 ones"),
        ("break apart", "Split a number into tens and ones.", "38 = 30 + 8"),
        ("open number line", "A number line with only the numbers you need.", "45 → 75 → 82 for 45 + 37"),
        ("count up", "Add on from the smaller number to the larger one to find a difference.", "38 to 40 to 70 to 72 is 34"),
        ("compensation", "Change one number to make it friendly, then fix the answer.", "48 + 25 = 50 + 23"),
        ("commutative property", "Adding in any order gives the same sum.", "36 + 47 = 47 + 36"),
        ("associative property", "Grouping addends in any way gives the same sum.", "(23 + 17) + 15 = 23 + (17 + 15)"),
        ("check", "Use the opposite operation to see if an answer is right.", "63 − 28 = 35, check: 35 + 28 = 63")]
CARDS[u] = [("47 + 35 by place value", "Tens: 40 + 30 = 70. Ones: 7 + 5 = 12. 70 + 12 = 82.", "strategy"),
            ("52 − 27: are there enough ones?", "No. Break apart a ten: 4 tens and 12 ones. 52 − 27 = 25.", "strategy"),
            ("52 − 27 = 35?", "No. 7 cannot come from 2 ones without breaking a ten. The answer is 25.", "misconception"),
            ("Check 81 − 46 = 35.", "35 + 46 = 81. It is correct.", "rule"),
            ("Add 23 + 17 + 15", "23 + 17 = 40, 40 + 15 = 55.", "strategy"),
            ("58 + 27 = 60 + ___", "25. Move 2 from 27 to 58.", "example"),
            ("Is 36 + 47 the same as 47 + 36?", "Yes. Order does not change the sum.", "concept"),
            ("Count up: 68 − 39", "39 + 1 = 40, + 20 = 60, + 8 = 68. 1 + 20 + 8 = 29.", "strategy")]
VIS[u] = [("What is the total? Trade if you can.", "blocks", {"t": 7, "o": 13}, "7 tens and 13 ones = 8 tens and 3 ones = 83"),
          ("Where does it land?", "jline", {"lo": 40, "hi": 80, "step": 1, "label_every": 10, "jumps": [[46, 76, "+30"], [76, 78, "+2"]], "points": [{"v": 78, "label": "?"}]}, "46 + 32 = 78"),
          ("Find the missing part.", "bars", {"rows": [{"parts": [[72, "72"]]}, {"parts": [[45, "45"], [27, "?"]]}]}, "72 − 45 = 27")]
SHEET[u] = dict(focus="adding and subtracting two-digit numbers by place value", morefocus="adding up to four numbers and explaining strategies",
    sides=[dict(big="Add or subtract tens with tens and ones with ones. Make a ten when there are 10 or more ones. Break apart a ten when there are not enough ones.",
                vocab=["regroup", "break apart", "count up", "check"],
                how=dict(text="Subtract 63 − 28.", example="63 − 28", steps=[["Not enough ones:", "63 = 5 tens and 13 ones"], ["Ones:", "13 − 8 = 5"], ["Tens:", "5 − 2 = 3"]], answer="35", check="63-28==35&&35+28==63"),
                fig=("blocks", {"t": 6, "o": 3}, "63: trade 1 ten for 10 ones to get 5 tens and 13 ones."),
                remember=["Check subtraction by adding.", "Count up from the smaller number to subtract."],
                watch=[["47 + 35 = 712", "10 or more ones make a new ten: 82"], ["52 − 27 = 35", "do not subtract smaller from larger in each place"]],
                tryit=[["38 + 46", "84", "38+46==84"], ["70 − 24", "46", "70-24==46"]]),
           dict(big="Add three or four numbers in any order. Look for numbers that make a ten.",
                vocab=["commutative property", "associative property", "compensation", "open number line"],
                how=dict(text="Add 24 + 15 + 36.", example="24 + 15 + 36", steps=[["Friendly pair:", "24 + 36 = 60"], ["Add the rest:", "60 + 15 = 75"]], answer="75", check="24+15+36==75&&24+36==60"),
                fig=("jline", {"lo": 30, "hi": 70, "step": 1, "label_every": 10, "jumps": [[38, 40, "+2"], [40, 60, "+20"], [60, 65, "+5"]]}, "Count up from 38 to 65: 2 + 20 + 5 = 27, so 65 − 38 = 27."),
                remember=["Changing the order of addends does not change the sum.", "Explain using tens and ones."],
                watch=[["Losing an addend", "cross off each number as you add it"], ["Forgetting new tens", "ones can make 2 new tens: 9 + 8 + 7 = 24"]],
                tryit=[["16 + 22 + 14 + 30", "82", "16+22+14+30==82"], ["49 + 26 = 50 + ___", "25", "49+26==50+25"]])])

# ---------------------------------------------------------------- Unit 6
u = "word-problems-100"
V[u] = [("add to", "A story where more is joined to a group.", "Ana had 25 shells and found 12 more"),
        ("take from", "A story where some are taken away.", "There were 40 birds and 15 flew away"),
        ("put together", "A story with two parts that make a whole.", "18 red and 24 blue apples"),
        ("take apart", "A story where a whole is split into parts.", "60 children, 35 are girls, how many boys?"),
        ("compare", "A story about how many more or how many fewer.", "Ben has 12 more than Ana"),
        ("unknown", "The number you need to find. Use ? or a box.", "25 + ? = 40"),
        ("bar model", "Bars that show the parts and the whole.", "a bar for 40 split into 25 and ?"),
        ("two-step problem", "A problem that needs two steps to solve.", "add, then subtract")]
CARDS[u] = [("Ana had 28 stickers and got some more. Now she has 45. How many did she get?", "28 + ? = 45, so 17.", "example"),
            ("Some birds were on a tree. 14 flew away. 23 are left. How many at first?", "? − 14 = 23, so 37.", "example"),
            ("Does “more” always mean add?", "No. “Ben has 12 more than Ana; Ben has 50” means Ana has 50 − 12 = 38.", "misconception"),
            ("How do you find how many more?", "Subtract the smaller amount from the bigger amount.", "rule"),
            ("What goes in a bar model?", "The whole on top and the parts below.", "concept"),
            ("Two-step: 35 on the bus, 12 get on, 9 get off.", "35 + 12 = 47, 47 − 9 = 38.", "example"),
            ("Write an equation for: 64 apples, 29 are red, how many are green?", "29 + ? = 64 (or 64 − 29 = ?). ? = 35.", "strategy"),
            ("First step of a two-step problem?", "Find what you need to know first, then use it.", "strategy")]
VIS[u] = [("How many more laps did Mia swim?", "bars", {"rows": [{"label": "Mia", "parts": [[52, "52"]]}, {"label": "Leo", "parts": [[34, "34"], [18, "?"]]}]}, "52 − 34 = 18 more laps"),
          ("Find the missing part.", "bars", {"rows": [{"parts": [[61, "61"]]}, {"parts": [[26, "26"], [35, "?"]]}]}, "61 − 26 = 35"),
          ("Where does the jump land?", "jline", {"lo": 40, "hi": 70, "step": 1, "label_every": 10, "jumps": [[43, 61, "+18"]], "points": [{"v": 61, "label": "?"}]}, "43 + 18 = 61")]
SHEET[u] = dict(focus="add-to, take-from, put-together and take-apart stories", morefocus="compare stories and two-step problems",
    sides=[dict(big="Read the story and decide what is known and what is unknown. Draw a bar model, then write an equation with ? for the unknown.",
                vocab=["add to", "take from", "put together", "unknown"],
                how=dict(text="Mia had some beads. She bought 16 more. Now she has 43. How many did she have at first?", example="? + 16 = 43", steps=[["Unknown start:", "? + 16 = 43"], ["Think:", "43 − 16 = 27"]], answer="27 beads", check="27+16==43"),
                fig=("bars", {"rows": [{"parts": [[43, "43"]]}, {"parts": [[27, "?"], [16, "16"]]}]}, "The whole is 43. One part is 16. The start is 43 − 16 = 27."),
                remember=["Put the whole on top of the bar model.", "Check: does the answer make sense in the story?"],
                watch=[["Key words", "“gave” does not always mean subtract"], ["Adding the whole and a part", "if a part is unknown, subtract"]],
                tryit=[["55 cards. 28 are red. How many are blue?", "27 cards", "55-28==27"], ["Ted had 40¢. He spent some. Now he has 14¢. How much did he spend?", "26¢", "40-14==26"]]),
           dict(big="Compare stories ask how many more or how many fewer. Two-step stories need one answer to find the next.",
                vocab=["compare", "bar model", "two-step problem", "take apart"],
                how=dict(text="Leo has 34 stamps. Zoe has 18 more than Leo. How many do they have together?", example="two steps", steps=[["Zoe:", "34 + 18 = 52"], ["Together:", "34 + 52 = 86"]], answer="86 stamps", check="34+18==52&&34+52==86"),
                fig=("bars", {"rows": [{"label": "Leo", "parts": [[34, "34"]]}, {"label": "Zoe", "parts": [[34, "34"], [18, "18"]]}]}, "Zoe's bar is Leo's bar and 18 more."),
                remember=["How many more = bigger − smaller.", "Write one equation for each step."],
                watch=[["Doing only one step", "ask: did I answer the question?"], ["“Fewer” stories", "Ana has 9 fewer than Ben (50): Ana has 41"]],
                tryit=[["Ana read 62 pages. Ben read 45. How many more did Ana read?", "17 pages", "62-45==17"], ["30 on the bus, 14 get on, 8 get off.", "36", "30+14-8==36"]])])

# ---------------------------------------------------------------- Unit 7
u = "add-subtract-1000"
V[u] = [("hundreds place", "The place that tells how many hundreds.", "In 527, the 5 is in the hundreds place"),
        ("compose", "Put together 10 ones to make a ten, or 10 tens to make a hundred.", "12 tens = 1 hundred and 2 tens"),
        ("decompose", "Break a ten into 10 ones, or a hundred into 10 tens.", "400 = 3 hundreds and 10 tens"),
        ("written method", "Writing each place in a column and adding or subtracting place by place.", "234 + 152 in columns"),
        ("place-value chart", "A chart with hundreds, tens, and ones columns.", "3 hundreds, 4 tens, 6 ones in three columns"),
        ("across zeros", "Subtracting from a number with zeros, like 500 or 403.", "500 − 123: trade a hundred, then a ten")]
CARDS[u] = [("Add 345 + 278", "Hundreds 500, tens 110, ones 13. 500 + 110 + 13 = 623.", "strategy"),
            ("What does a new hundred mean?", "10 tens are traded for 1 hundred.", "concept"),
            ("Subtract 500 − 123", "500 = 4 hundreds, 9 tens, 10 ones. 500 − 123 = 377.", "strategy"),
            ("Is 432 − 158 = 386?", "No. That subtracts smaller from larger in each place. 432 − 158 = 274.", "misconception"),
            ("Check 600 − 245 = 355", "355 + 245 = 600. Correct.", "rule"),
            ("Count up: 703 − 488", "488 + 12 = 500, + 200 = 700, + 3 = 703. 12 + 200 + 3 = 215.", "strategy"),
            ("In 456 + 287, which places need a trade?", "Ones (6 + 7 = 13) and tens (5 + 8 + 1 = 14).", "concept")]
VIS[u] = [("What is the sum? Trade if you can.", "blocks", {"h": 5, "t": 11, "o": 7}, "5 hundreds, 11 tens, 7 ones = 617"),
          ("Take away 135. How many are left?", "blocks", {"h": 3, "t": 5, "o": 8}, "358 − 135 = 223"),
          ("What number is shown?", "pv_chart", {"hundreds": 8, "tens": 0, "ones": 4}, "804")]
SHEET[u] = dict(focus="adding three-digit numbers with models and new tens and hundreds", morefocus="subtracting three-digit numbers, including across zeros",
    sides=[dict(big="Add hundreds and hundreds, tens and tens, ones and ones. When a place has 10 or more, trade for one of the next place.",
                vocab=["hundreds place", "compose", "written method", "place-value chart"],
                how=dict(text="Add 368 + 254.", example="368 + 254", steps=[["Hundreds:", "300 + 200 = 500"], ["Tens:", "60 + 50 = 110"], ["Ones:", "8 + 4 = 12"], ["Total:", "500 + 110 + 12 = 622"]], answer="622", check="368+254==622&&500+110+12==622"),
                fig=("blocks", {"h": 5, "t": 11, "o": 12}, "5 hundreds, 11 tens, 12 ones: trade to get 6 hundreds, 2 tens, 2 ones = 622."),
                remember=["Line up the places.", "A small 1 above a column shows a trade."],
                watch=[["Writing 12 in the ones place", "write 2 and trade the ten"], ["Forgetting the traded hundred", "add it to the hundreds column"]],
                tryit=[["247 + 135", "382", "247+135==382"], ["486 + 357", "843", "486+357==843"]]),
           dict(big="Subtract place by place. If a place does not have enough, break apart a ten or a hundred.",
                vocab=["decompose", "across zeros", "written method", "hundreds place"],
                how=dict(text="Subtract 403 − 158.", example="403 − 158", steps=[["Trade:", "403 = 3 hundreds, 9 tens, 13 ones"], ["Ones:", "13 − 8 = 5"], ["Tens:", "9 − 5 = 4"], ["Hundreds:", "3 − 1 = 2"]], answer="245", check="403-158==245"),
                fig=("blocks", {"h": 4, "t": 0, "o": 3}, "403 has 0 tens: break apart a hundred into 10 tens first."),
                remember=["Check by adding the answer and the number taken away.", "You can also count up from the smaller number."],
                watch=[["Smaller from larger", "in 432 − 158 you cannot do 8 − 2"], ["Across zeros", "500 → 4 hundreds, 9 tens, 10 ones"]],
                tryit=[["725 − 413", "312", "725-413==312"], ["600 − 274", "326", "600-274==326"]])])

# ---------------------------------------------------------------- Unit 8
u = "measuring-length"
V[u] = [("length", "How long something is from end to end.", "the pencil's length is 7 inches"),
        ("inch", "A small customary unit of length, about the length of a paper clip.", "a crayon is about 3 inches"),
        ("foot", "12 inches. A ruler is 1 foot long.", "a book is about 1 foot"),
        ("yard", "3 feet. A yardstick is 1 yard long.", "a baseball bat is about 1 yard long"),
        ("centimeter", "A small metric unit, about the width of a fingertip.", "an eraser is about 5 centimeters"),
        ("meter", "100 centimeters. A meter stick is 1 meter long.", "a door is about 2 meters tall"),
        ("estimate", "A careful guess.", "the desk is about 3 feet long"),
        ("line plot", "A number line with an X for each measurement.", "an X above 6 for each 6-inch pencil"),
        ("measuring tape", "A long tool that bends, used for long or curved lengths.", "measure around a pumpkin")]
CARDS[u] = [("Where do you start measuring on a ruler?", "At 0, with the end of the object lined up.", "rule"),
            ("An object goes from 2 to 9 on a ruler. How long is it?", "9 − 2 = 7 units.", "example"),
            ("Which tool for a classroom's length?", "A measuring tape (or meter stick moved many times).", "concept"),
            ("Why is a desk 3 feet but 36 inches?", "Inches are smaller, so it takes more of them.", "concept"),
            ("Best estimate for a door?", "About 2 meters (not 2 centimeters).", "example"),
            ("15 inches vs 15 centimeters: which is longer?", "15 inches, because an inch is longer than a centimeter.", "misconception"),
            ("How much longer is 12 cm than 8 cm?", "12 − 8 = 4 cm.", "example"),
            ("On a line plot, what does each X mean?", "One object that was measured.", "concept")]
VIS[u] = [("How long is the pencil?", "ruler2", {"length": 12, "unit": "inches", "objects": [{"start": 0, "end": 7, "label": "pencil"}]}, "7 inches"),
          ("How long is the key?", "ruler2", {"length": 15, "unit": "centimeters", "objects": [{"start": 3, "end": 10, "label": "key"}]}, "10 − 3 = 7 centimeters"),
          ("How many pencils are 6 inches?", "lineplot", {"lo": "4", "hi": "9", "den": 1, "values": ["4", "5", "5", "6", "6", "6", "7", "8"], "title": "Pencil Lengths", "unit": "Length (inches)"}, "3 pencils")]
SHEET[u] = dict(focus="measuring with rulers and choosing tools and units", morefocus="estimating, comparing lengths and line plots",
    sides=[dict(big="Line up one end with 0 and count the units the object covers. Use small units for short things and big units for long things.",
                vocab=["length", "inch", "centimeter", "measuring tape"],
                how=dict(text="A crayon starts at the 2 mark and ends at the 8 mark. How long is it?", example="2 to 8", steps=[["Count the spaces:", "8 − 2"], ["Length:", "6 units"]], answer="6 units", check="8-2==6"),
                fig=("ruler2", {"length": 12, "unit": "inches", "objects": [{"start": 0, "end": 5, "label": "eraser"}]}, "The eraser starts at 0 and ends at 5: 5 inches."),
                remember=["Ruler: 12 inches. Yardstick: 3 feet. Meter stick: 100 centimeters.", "Smaller units give bigger numbers."],
                watch=[["Starting at 1", "start at 0, or subtract the start mark"], ["Counting tick marks", "count the spaces between them"]],
                tryit=[["2 feet is how many inches?", "24 inches", "12+12==24"], ["Best unit for a car: inches or feet?", "feet", "1==1"]]),
           dict(big="Use benchmarks to estimate. To compare lengths, find the difference in the same unit.",
                vocab=["estimate", "foot", "meter", "line plot"],
                how=dict(text="The blue ribbon is 23 cm. The red ribbon is 15 cm. How much longer is the blue ribbon?", example="23 − 15", steps=[["Same unit:", "centimeters"], ["Subtract:", "23 − 15 = 8"]], answer="8 centimeters", check="23-15==8"),
                fig=("lineplot", {"lo": "3", "hi": "8", "den": 1, "values": ["3", "4", "4", "5", "5", "5", "7"], "title": "Leaf Lengths", "unit": "Length (centimeters)"}, "Each X is one leaf. Three leaves are 5 cm long."),
                remember=["Paper clip ≈ 1 inch. Fingertip ≈ 1 cm. Long step ≈ 1 meter.", "Line plot: one X for each measurement."],
                watch=[["Different units", "you cannot compare 5 inches and 5 cm by the numbers"], ["Adding to compare", "how much longer means subtract"]],
                tryit=[["A pencil is 7 paper clips long. About how many inches?", "about 7 inches", "7==7"], ["18 in. and 11 in.: how much longer?", "7 inches", "18-11==7"]])])

# ---------------------------------------------------------------- Unit 9
u = "length-number-line"
V[u] = [("number line", "A line with equally spaced points for numbers, like a ruler.", "0, 1, 2, 3 …"),
        ("unit", "The length from one number to the next on a number line.", "from 4 to 5 is 1 unit"),
        ("jump", "A move along a number line.", "a jump of +10 from 35 lands on 45"),
        ("distance", "How far apart two points are.", "from 20 to 35 is 15"),
        ("same units", "Lengths measured with the same unit so they can be added or subtracted.", "12 cm + 9 cm = 21 cm"),
        ("cut off", "Take a length away.", "a 50 cm ribbon with 18 cm cut off is 32 cm")]
CARDS[u] = [("A bar from 0 to 9: how long?", "9 units (count spaces, not ticks).", "concept"),
            ("Show 35 + 20 on a number line.", "Start at 35, jump forward 20, land on 55.", "strategy"),
            ("Show 62 − 8 on a number line.", "Start at 62, jump back 8, land on 54.", "strategy"),
            ("Jump from 27 to 41: how long?", "41 − 27 = 14.", "example"),
            ("A board was cut by 15 ft and is now 48 ft. How long at first?", "48 + 15 = 63 feet.", "example"),
            ("Can you add 12 inches and 12 cm to get 24?", "No. Use the same unit.", "misconception"),
            ("Ticks are labeled 0, 5, 10. The point is 2 ticks after 10. What number?", "20, because each tick is 5.", "concept")]
VIS[u] = [("What number is at the point?", "jline", {"lo": 0, "hi": 100, "step": 5, "label_every": 2, "points": [{"v": 35, "label": "?"}]}, "35"),
          ("Where does it land?", "jline", {"lo": 20, "hi": 60, "step": 1, "label_every": 10, "jumps": [[28, 48, "+20"], [48, 53, "+5"]], "points": [{"v": 53, "label": "?"}]}, "28 + 25 = 53"),
          ("How long are the sticks together?", "ruler2", {"length": 12, "unit": "inches", "objects": [{"start": 0, "end": 5, "label": "stick 1"}, {"start": 5, "end": 9, "label": "stick 2"}]}, "5 + 4 = 9 inches")]
SHEET[u] = dict(focus="length word problems", morefocus="whole numbers, sums and differences on a number line",
    sides=[dict(big="Add lengths that are joined. Subtract when a length is cut off or when you compare. Keep the same unit.",
                vocab=["same units", "cut off", "distance", "unit"],
                how=dict(text="A rope is 64 feet long. 27 feet are cut off. How long is it now?", example="64 − 27", steps=[["Cut off means subtract:", "64 − 27"], ["Answer:", "37"]], answer="37 feet", check="64-27==37"),
                fig=("ruler2", {"length": 12, "unit": "inches", "objects": [{"start": 0, "end": 7, "label": "7 in."}, {"start": 7, "end": 11, "label": "4 in."}]}, "7 inches + 4 inches = 11 inches."),
                remember=["Write the unit with the answer.", "Draw a ruler or bar to see the lengths."],
                watch=[["Mixed units", "change nothing; only add the same unit"], ["Start unknown", "cut off 15, now 48: add to find the start"]],
                tryit=[["32 cm and 45 cm joined", "77 centimeters", "32+45==77"], ["A 90 m path has 38 m done. How much is left?", "52 meters", "90-38==52"]]),
           dict(big="A number line is like a ruler. Numbers are lengths from 0. Adding jumps right and subtracting jumps left.",
                vocab=["number line", "jump", "unit", "distance"],
                how=dict(text="Show 46 + 27 on a number line.", example="46 + 27", steps=[["Jump +20:", "46 → 66"], ["Jump +7:", "66 → 73"]], answer="73", check="46+27==73"),
                fig=("jline", {"lo": 40, "hi": 80, "step": 1, "label_every": 10, "jumps": [[46, 66, "+20"], [66, 73, "+7"]], "points": [{"v": 73, "label": "73"}]}, "46 + 20 = 66, 66 + 7 = 73."),
                remember=["Count the spaces between ticks, not the ticks.", "Find how much each tick is worth first."],
                watch=[["Wrong direction", "subtracting jumps to the left"], ["Reading the jump size", "the answer is where you land"]],
                tryit=[["Start at 70, jump back 25", "45", "70-25==45"], ["From 38 to 61: how far?", "23", "61-38==23"]])])

# ---------------------------------------------------------------- Unit 10
u = "time-money"
V[u] = [("hour hand", "The short hand. It shows the hour.", "between 3 and 4 means after 3:00"),
        ("minute hand", "The long hand. Each number is 5 minutes.", "on the 4 means 20 minutes"),
        ("AM", "Times from midnight to noon (a.m.).", "7:30 AM is in the morning"),
        ("PM", "Times from noon to midnight (p.m.).", "6:00 PM is in the evening"),
        ("quarter past", "15 minutes after the hour.", "quarter past 2 is 2:15"),
        ("half past", "30 minutes after the hour.", "half past 9 is 9:30"),
        ("penny", "A coin worth 1 cent.", "1¢"),
        ("nickel", "A coin worth 5 cents.", "5¢"),
        ("dime", "A coin worth 10 cents.", "10¢"),
        ("quarter", "A coin worth 25 cents.", "25¢"),
        ("dollar", "100 cents. Write it with $.", "$1 = 100¢"),
        ("cent sign", "The symbol ¢ written after an amount of cents.", "45¢")]
CARDS[u] = [("Minute hand on the 7?", "35 minutes (count by 5s).", "concept"),
            ("Hour hand just past 4, minute hand on 9?", "4:45", "example"),
            ("Is lunch at noon AM or PM?", "PM. Noon starts PM.", "misconception"),
            ("Value of 2 quarters, 1 dime, 3 pennies?", "25 + 25 + 10 + 3 = 63¢", "example"),
            ("Is a nickel worth more than a dime?", "No. A dime (10¢) is worth more, even though it is smaller.", "misconception"),
            ("Fewest coins for 40¢?", "1 quarter, 1 dime, 1 nickel.", "strategy"),
            ("How do you write 6 dollars?", "$6", "fact"),
            ("You have 75¢. How much more for $1?", "100 − 75 = 25¢", "example")]
VIS[u] = [("What time is it?", "clock", {"h": 8, "m": 25}, "8:25"),
          ("How much money?", "money", {"coins": ["quarter", "dime", "dime", "nickel", "penny"], "show_value": True}, "25 + 10 + 10 + 5 + 1 = 51¢"),
          ("How much money?", "money", {"bills": [5, 1, 1], "coins": ["quarter", "dime"]}, "$7 and 35¢")]
SHEET[u] = dict(focus="telling time to five minutes with AM and PM", morefocus="counting coins and bills and solving money problems",
    sides=[dict(big="The short hand shows the hour. The long hand shows the minutes: count by 5s for each number.",
                vocab=["hour hand", "minute hand", "AM", "PM"],
                how=dict(text="Read the clock: the hour hand is just past 3, and the minute hand is on 8.", example="3 and 8", steps=[["Hour:", "3"], ["Minutes:", "count by 5s 8 times: 5, 10 … 40"]], answer="3:40", check="5+5+5+5+5+5+5+5==40"),
                fig=("clock", {"h": 10, "m": 50}, "The minute hand is on 10 (50 minutes). The hour hand is almost at 11: 10:50."),
                remember=["AM: midnight to noon. PM: noon to midnight.", "Quarter past = :15. Half past = :30."],
                watch=[["Minute hand on 4 is 4 minutes?", "No: 20 minutes"], ["Hour hand almost at the next number", "it is still the earlier hour"]],
                tryit=[["Minute hand on 11", "55 minutes", "5+5+5+5+5+5+5+5+5+5+5==55"], ["Breakfast at 7:15: AM or PM?", "AM", "7<12"]]),
           dict(big="Count coins from greatest to least value. Write cents with ¢ and dollars with $.",
                vocab=["quarter", "dime", "nickel", "penny", "dollar", "cent sign"],
                how=dict(text="Find the value of 1 quarter, 2 dimes, 1 nickel, and 3 pennies.", example="25, 10, 10, 5, 1, 1, 1", steps=[["Skip count:", "25, 35, 45, 50, 51, 52, 53"]], answer="53¢", check="25+10+10+5+3==53"),
                fig=("money", {"coins": ["quarter", "quarter", "dime", "nickel", "penny"], "show_value": True}, "25 + 25 + 10 + 5 + 1 = 66¢"),
                remember=["$1 = 100¢.", "Change = money you have − price."],
                watch=[["Counting coins, not values", "4 coins can be 4¢ or 100¢"], ["$35¢", "use only one symbol: 35¢"]],
                tryit=[["3 dimes and 4 nickels", "50¢", "30+20==50"], ["You have 90¢ and spend 45¢", "45¢", "90-45==45"]])])

# ---------------------------------------------------------------- Unit 11
u = "graphs-data"
V[u] = [("data", "Information you collect, like votes or counts.", "votes for favorite fruit"),
        ("tally chart", "A chart that uses tally marks to count.", "a bundle of 5 marks"),
        ("picture graph", "A graph that uses pictures to show data.", "each star stands for 1 vote"),
        ("bar graph", "A graph that uses bars to show data.", "a bar up to 7 means 7"),
        ("scale", "The numbers along a bar graph.", "0, 1, 2, 3 … (counting by 1s)"),
        ("key", "Tells what each picture stands for.", "★ = 1 vote"),
        ("category", "A group in the data.", "dog, cat, fish, bird"),
        ("title", "The name of a graph that tells what it shows.", "Favorite Fruit")]
CARDS[u] = [("How do you read a bar?", "Look across from the top of the bar to the scale.", "rule"),
            ("Each picture stands for 1. A row has 8 pictures.", "8", "fact"),
            ("Apple 9, pear 4. How many more apples?", "9 − 4 = 5.", "example"),
            ("Tally: four marks with a slash", "5", "fact"),
            ("Which has the most?", "The longest row or the tallest bar.", "concept"),
            ("Is the bar height the number of grid lines you count from 1?", "No. Read the number where the bar ends; 0 is the start.", "misconception"),
            ("What does every graph need?", "A title, labels, and a scale or key.", "concept")]
VIS[u] = [("How many votes for grape?", "picgraph", {"title": "Favorite Fruit", "cats": ["apple", "banana", "grape"], "symbols": [6, 4, 8], "key": 1, "icon": "star", "unit": "vote"}, "8 votes"),
          ("How many more dogs than fish?", "bargraph1", {"title": "Pets in Our Class", "cats": ["dog", "cat", "fish"], "vals": [9, 6, 3], "top": 10, "ylabel": "Number of pets"}, "9 − 3 = 6 more"),
          ("How tall should the bar for pear be?", "tally", {"title": "Favorite Fruit", "cats": ["apple", "pear", "plum"], "counts": [7, 12, 4]}, "12")]
SHEET[u] = dict(focus="reading picture graphs and bar graphs", morefocus="solving problems with graphs and making graphs from data",
    sides=[dict(big="In a picture graph each picture stands for 1. In a bar graph, read the number where the top of the bar lines up with the scale.",
                vocab=["picture graph", "bar graph", "scale", "key"],
                how=dict(text="Read the bar graph: the cat bar ends at 6.", example="cat bar", steps=[["Top of the bar:", "lines up with 6"], ["So:", "6 cats"]], answer="6 cats", check="6==6"),
                fig=("bargraph1", {"title": "Pets in Our Class", "cats": ["dog", "cat", "fish"], "vals": [8, 6, 3], "top": 10, "ylabel": "Number of pets"}, "Dog 8, cat 6, fish 3."),
                remember=["Start the scale at 0.", "Point to each picture as you count."],
                watch=[["Counting grid lines from 1", "read the number at the top of the bar"], ["Wrong row or bar", "read the label first"]],
                tryit=[["Dog and fish together", "11", "8+3==11"], ["How many more dogs than cats?", "2", "8-6==2"]]),
           dict(big="Use the graph to put together, take apart, or compare. Make a graph from a tally chart with a title, labels, and a scale of 1.",
                vocab=["tally chart", "data", "category", "title"],
                how=dict(text="Make a bar graph from the tally: apple 7, pear 12, plum 4.", example="tally chart", steps=[["Title and labels:", "Favorite Fruit"], ["Scale:", "0 to 12 by 1s"], ["Bars:", "7, 12, 4"]], answer="3 bars", check="7+12+4==23"),
                fig=("tally", {"title": "Favorite Fruit", "cats": ["apple", "pear", "plum"], "counts": [7, 12, 4]}, "Each bundle of tally marks is 5."),
                remember=["How many more: subtract.", "In all: add every category."],
                watch=[["Adding to compare", "how many more means subtract"], ["Missing title or labels", "check every part of the graph"]],
                tryit=[["How many votes in all: 7, 12, 4?", "23", "7+12+4==23"], ["How many more pear than plum?", "8", "12-4==8"]])])

# ---------------------------------------------------------------- Unit 12
u = "shapes-equal-shares"
V[u] = [("side", "A straight line that makes part of a shape.", "a triangle has 3 sides"),
        ("angle", "The corner made where two sides meet.", "a square has 4 angles"),
        ("vertex", "A corner point of a shape. More than one are vertices.", "a cube has 8 vertices"),
        ("triangle", "A closed shape with 3 sides and 3 angles.", "▲"),
        ("quadrilateral", "A closed shape with 4 sides and 4 angles.", "squares, rectangles, and other 4-sided shapes"),
        ("pentagon", "A closed shape with 5 sides and 5 angles.", "the outline of a house shape"),
        ("hexagon", "A closed shape with 6 sides and 6 angles.", "a honeycomb cell"),
        ("cube", "A solid with 6 equal square faces.", "a number cube"),
        ("face", "A flat surface of a solid.", "each face of a cube is a square"),
        ("equal shares", "Parts that are the same size.", "a sandwich cut into 2 equal shares"),
        ("halves", "2 equal shares of a whole.", "one half of a pizza"),
        ("thirds", "3 equal shares of a whole.", "one third of a cake"),
        ("fourths", "4 equal shares of a whole.", "one fourth of a square")]
CARDS[u] = [("How many sides does a pentagon have?", "5 sides and 5 angles.", "fact"),
            ("Is a tipped square still a quadrilateral?", "Yes. Turning a shape does not change its sides.", "misconception"),
            ("How many faces, edges, and vertices does a cube have?", "6 faces, 12 edges, 8 vertices.", "fact"),
            ("3 rows of 4 squares: how many squares?", "4 + 4 + 4 = 12.", "example"),
            ("How many fourths make a whole?", "4 fourths.", "fact"),
            ("Which is bigger: one half or one fourth of the same pizza?", "One half. More shares means smaller shares.", "misconception"),
            ("Can halves have different shapes?", "Yes. Triangle halves and rectangle halves of the same square are the same size.", "concept"),
            ("Cut into 3 parts: are they always thirds?", "Only if the parts are equal.", "misconception")]
VIS[u] = [("Name the shape.", "draw_shape", {"pts": [[0, 2], [2, 0], [5, 1], [4, 4], [1, 4]]}, "pentagon (5 sides)"),
          ("What part is shaded?", "partition", {"shape": "circle", "n": 3, "shade": [0]}, "one third"),
          ("How many squares?", "partition", {"shape": "rect", "cuts": "grid", "rows": 3, "cols": 4, "shade": []}, "3 rows of 4: 12 squares")]
SHEET[u] = dict(focus="naming and drawing shapes by sides and angles, and cubes", morefocus="partitioning rectangles into squares and halves, thirds and fourths",
    sides=[dict(big="Name a shape by counting its sides and angles, not by how it is turned. A cube is a solid with 6 equal square faces.",
                vocab=["side", "angle", "quadrilateral", "cube"],
                how=dict(text="Name a closed shape with 6 straight sides.", example="6 sides", steps=[["Count sides:", "6"], ["Count angles:", "6"]], answer="hexagon", check="6==6"),
                fig=("solids", {"items": [{"kind": "cube", "label": "cube"}, {"kind": "prism", "label": "not a cube"}, {"kind": "pyramid", "label": "pyramid"}]}, "A cube's faces are all the same square."),
                remember=["3 sides: triangle. 4: quadrilateral. 5: pentagon. 6: hexagon.", "Sides can be different lengths."],
                watch=[["A tipped square is a “diamond”", "it is still a quadrilateral"], ["Counting only the faces you see", "a cube has 6 faces"]],
                tryit=[["Sides on a triangle and a hexagon", "9", "3+6==9"], ["Faces on 2 cubes", "12", "6+6==12"]]),
           dict(big="Equal shares are the same size. Two equal shares are halves, three are thirds, four are fourths. A whole is two halves, three thirds, or four fourths.",
                vocab=["equal shares", "halves", "thirds", "fourths"],
                how=dict(text="A pizza is cut into fourths. Ana eats one fourth. How much is left?", example="4 fourths", steps=[["Whole:", "four fourths"], ["4 − 1 =", "3"]], answer="three fourths", check="4-1==3"),
                fig=("partition_pair", {"a": {"shape": "square", "cuts": "diag2", "shade": [0]}, "b": {"shape": "square", "cuts": "v", "widths": [1, 1], "shade": [0]}}, "Both shaded parts are one half of the same square."),
                remember=["More shares of the same whole means smaller shares.", "Rows and columns of same-size squares: count by rows."],
                watch=[["Unequal parts", "3 parts are thirds only if they are equal"], ["Fourths bigger than halves?", "no: one half is bigger"]],
                tryit=[["How many thirds make a whole?", "3", "3==3"], ["4 rows of 5 squares", "20", "5+5+5+5==20"]])])
