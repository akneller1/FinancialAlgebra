"""Grade 1 reference content: vocabulary, concept flashcards, visual flashcards, cheat-sheet sides.
Same structure as tools/grade2-authoring/content_g2.py so build_content.py and the shared cheat-sheet builder read it unchanged.
Every cheat-sheet example and Try It! carries a JS check; every 'a + b = c' / 'a − b = c' in any card is re-checked by build_content.py."""

V = {}      # unit -> [(term, definition, example)]
CARDS = {}  # unit -> [(front, back, kind)]
VIS = {}    # unit -> [(front, figure kind, figure data, back)]
SHEET = {}  # unit -> dict(focus, morefocus, sides=[side, side])

# ---------------------------------------------------------------- Unit 1
u = "count-120"
V[u] = [("count", "Say numbers in order, one for each object.", "1, 2, 3, 4, 5"),
        ("count on", "Start at a number and keep counting up.", "Start at 8: 9, 10, 11"),
        ("count back", "Start at a number and count down.", "Start at 8: 7, 6, 5"),
        ("number", "Tells how many.", "There are 12 apples"),
        ("digit", "One of the symbols 0 to 9 used to write numbers.", "47 has the digits 4 and 7"),
        ("numeral", "A number written with digits.", "twenty-three is written 23"),
        ("120 chart", "A chart of the numbers 1 to 120 in rows of ten.", "Below 45 is 55"),
        ("one more", "The next number when you count.", "One more than 39 is 40")]
CARDS[u] = [("What comes after 39?", "40. The ones go back to 0 and the tens go up by 1.", "concept"),
            ("What comes after 109?", "110, not 200.", "misconception"),
            ("Count on 3 from 98.", "99, 100, 101.", "example"),
            ("Write one hundred four.", "104, not 1004.", "misconception"),
            ("Write seventy-two.", "72", "example"),
            ("What comes just before 60?", "59", "example"),
            ("6 + 2 by counting on", "Start at 6. Say 7, 8. So 6 + 2 = 8.", "strategy"),
            ("9 − 3 by counting back", "Start at 9. Say 8, 7, 6. So 9 − 3 = 6.", "strategy")]
VIS[u] = [("How many counters?", "tenframe", {"frames": 2, "a": 16}, "16: one full ten frame and 6 more"),
          ("What number is hidden?", "chart", {"start": 101, "per_row": 10, "rows": 2, "hide": [114]}, "114"),
          ("Start at 7. Count on 3.", "jline", {"lo": 0, "hi": 15, "jumps": [[7, 10, "+3"]], "points": [{"v": 7, "label": "Start"}]}, "7 + 3 = 10")]
SHEET[u] = dict(focus="counting objects and counting on to 120", morefocus="reading and writing numbers and counting on or back to add and subtract",
    sides=[dict(big="Count each object one time. You can start counting at any number and count on to 120.",
                vocab=["count", "count on", "120 chart", "one more"],
                how=dict(text="Count on from 97. Say the next 4 numbers.", example="97, …", steps=[["After 97:", "98, 99"], ["Then:", "100, 101"]], answer="98, 99, 100, 101", check="97+4==101"),
                fig=("chart", {"start": 91, "per_row": 10, "rows": 3, "hide": [110]}, "After 109 comes 110. After 119 comes 120."),
                remember=["Touch each object as you count it.", "When the ones digit is 9, the next number has 0 ones and one more ten."],
                watch=[["…48, 49, 40", "after 49 comes 50"], ["…109, 200", "after 109 comes 110"]],
                tryit=[["What comes after 79?", "80", "79+1==80"], ["Count on 3 from 117.", "118, 119, 120", "117+3==120"]]),
           dict(big="Read and write numbers with digits. Count on to add and count back to subtract.",
                vocab=["digit", "numeral", "count back", "number"],
                how=dict(text="Find 12 − 3 by counting back.", example="12 − 3", steps=[["Start at", "12"], ["Count back 3:", "11, 10, 9"]], answer="9", check="12-3==9"),
                fig=("jline", {"lo": 0, "hi": 15, "jumps": [[12, 9, "−3"]], "points": [{"v": 12, "label": "Start"}]}, "Start at 12 and jump back 3. You land on 9."),
                remember=["Say the start number, then count only the jumps.", "Write the tens digit first: forty-six is 46."],
                watch=[["5 + 3: 5, 6, 7", "do not count the start. Say 6, 7, 8."], ["one hundred four → 1004", "it is 104"]],
                tryit=[["Write sixty-one.", "61", "60+1==61"], ["Count on: 8 + 3", "11", "8+3==11"]])])

# ---------------------------------------------------------------- Unit 2
u = "add-subtract-10"
V[u] = [("add", "Put groups together to find how many in all.", "3 + 2 = 5"),
        ("subtract", "Take away or find how many are left.", "5 − 2 = 3"),
        ("sum", "The answer when you add.", "In 4 + 3 = 7, the sum is 7"),
        ("difference", "The answer when you subtract.", "In 7 − 3 = 4, the difference is 4"),
        ("ten frame", "A box with 10 spaces in 2 rows of 5.", "8 counters leave 2 spaces empty"),
        ("make ten", "Find two numbers that add to 10.", "6 + 4 = 10"),
        ("part", "One of the groups that make a whole.", "3 and 5 are parts of 8"),
        ("whole", "All of the parts together.", "8 is the whole for 3 and 5")]
CARDS[u] = [("4 + 3", "7", "fact"), ("9 − 4", "5", "fact"),
            ("Which number goes with 7 to make 10?", "3, because 7 + 3 = 10.", "example"),
            ("Pairs that make 10", "1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5", "fact"),
            ("8 is 5 and ___", "3, because 5 + 3 = 8.", "example"),
            ("6 + 0", "6. Adding 0 does not change a number.", "concept"),
            ("Is 3 − 7 the same as 7 − 3?", "No. Start with the whole: 7 − 3 = 4.", "misconception"),
            ("To find 9 − 6, think…", "6 + 3 = 9, so 9 − 6 = 3.", "strategy")]
VIS[u] = [("How many in all?", "tenframe", {"frames": 1, "a": 5, "b": 3}, "5 + 3 = 8"),
          ("How many are left?", "crossrow", {"n": 9, "x": 4}, "9 − 4 = 5"),
          ("How many more make 10?", "tenframe", {"frames": 1, "a": 6}, "6 + 4 = 10, so 4 more")]
SHEET[u] = dict(focus="adding and subtracting within 10", morefocus="making ten and number partners",
    sides=[dict(big="Adding puts parts together. Subtracting takes some away. Know these facts quickly.",
                vocab=["add", "subtract", "sum", "difference"],
                how=dict(text="Find 6 + 3 by counting on.", example="6 + 3", steps=[["Start at", "6"], ["Count on 3:", "7, 8, 9"]], answer="9", check="6+3==9"),
                fig=("tenframe", {"frames": 1, "a": 7, "x": 2}, "7 counters, 2 crossed out: 7 − 2 = 5."),
                remember=["Start with the bigger number and count on.", "Adding 0 keeps the number the same."],
                watch=[["Counting the start number", "6 + 3: say 7, 8, 9"], ["Taking the big from the small", "8 − 5, not 5 − 8"]],
                tryit=[["5 + 4", "9", "5+4==9"], ["10 − 3", "7", "10-3==7"]]),
           dict(big="A ten frame shows how close a number is to 10. Two parts make a whole.",
                vocab=["ten frame", "make ten", "part", "whole"],
                how=dict(text="What goes with 7 to make 10?", example="7 + ___ = 10", steps=[["Fill the frame:", "8, 9, 10"], ["That is", "3 more"]], answer="3", check="7+3==10"),
                fig=("tenframe", {"frames": 1, "a": 4, "b": 6}, "4 red and 6 yellow make 10."),
                remember=["1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5 all make 10.", "To subtract, think: what part is missing?"],
                watch=[["7 + ___ = 10 → 17", "the blank is the missing part: 3"], ["Counting the counters, not the spaces", "count the empty boxes"]],
                tryit=[["2 + ___ = 10", "8", "2+8==10"], ["9 is 4 and ___", "5", "4+5==9"]])])

# ---------------------------------------------------------------- Unit 3
u = "add-subtract-20"
V[u] = [("addend", "A number that is added.", "In 8 + 5, the addends are 8 and 5"),
        ("doubles", "Adding a number to itself.", "6 + 6 = 12"),
        ("near doubles", "A double plus or minus 1.", "6 + 7 = 6 + 6 + 1 = 13"),
        ("make a ten", "Break a number apart to fill a ten first.", "8 + 5 = 8 + 2 + 3 = 13"),
        ("teen number", "A number from 11 to 19.", "15 is 10 and 5"),
        ("any order", "Addends can switch places. The sum stays the same.", "3 + 9 = 9 + 3"),
        ("fact family", "Facts that use the same three numbers.", "6 + 8 = 14, 8 + 6 = 14, 14 − 6 = 8, 14 − 8 = 6"),
        ("related facts", "An addition fact and a subtraction fact that go together.", "9 + 4 = 13 and 13 − 4 = 9")]
CARDS[u] = [("9 + 6: make a ten", "9 + 1 = 10, 10 + 5 = 15.", "strategy"),
            ("7 + 8: use a double", "7 + 7 = 14, so 7 + 8 = 15.", "strategy"),
            ("15 − 7: think addition", "7 + 8 = 15, so 15 − 7 = 8.", "strategy"),
            ("13 − 5: go back to 10", "13 − 3 = 10, 10 − 2 = 8.", "strategy"),
            ("4 + 7 + 6: find a ten", "4 + 6 = 10, 10 + 7 = 17.", "strategy"),
            ("Is 3 + 8 the same as 8 + 3?", "Yes. Both are 11.", "concept"),
            ("Is 14 − 6 = 12?", "No. 14 − 6 = 8. Do not take 4 from 6.", "misconception"),
            ("Fact family for 5, 9, 14", "5 + 9 = 14, 9 + 5 = 14, 14 − 5 = 9, 14 − 9 = 5", "concept")]
VIS[u] = [("How many in all?", "tenframe", {"frames": 2, "a": 9, "b": 5}, "9 + 5 = 14 (9 + 1 = 10, then 4 more)"),
          ("Where do you land?", "jline", {"lo": 0, "hi": 20, "jumps": [[15, 7, "−8"]], "points": [{"v": 15, "label": "Start"}]}, "15 − 8 = 7"),
          ("Find the missing part.", "bars", {"rows": [{"parts": [[16, "16"]]}, {"parts": [[9, "9"], [7, "?"]]}]}, "9 + 7 = 16, so the part is 7")]
SHEET[u] = dict(focus="adding within 20 with make-a-ten, doubles and three addends", morefocus="subtracting within 20 and related facts",
    sides=[dict(big="Use a strategy to add fast: make a ten, use a double, or add in any order.",
                vocab=["make a ten", "doubles", "near doubles", "any order"],
                how=dict(text="Add 8 + 5 by making a ten.", example="8 + 5", steps=[["Break 5 into", "2 and 3"], ["8 + 2 =", "10"], ["10 + 3 =", "13"]], answer="13", check="8+5==13&&8+2==10&&10+3==13"),
                fig=("tenframe", {"frames": 2, "a": 8, "b": 5}, "Fill the first ten frame, then count the rest: 10 + 3 = 13."),
                remember=["Doubles: 6 + 6 = 12, 7 + 7 = 14, 8 + 8 = 16, 9 + 9 = 18.", "With three numbers, add two that make 10 first."],
                watch=[["Forgetting the rest", "after making 10, add what is left"], ["Leaving out an addend", "add all three numbers"]],
                tryit=[["9 + 7", "16", "9+7==16"], ["3 + 5 + 7", "15", "3+5+7==15"]]),
           dict(big="Subtraction undoes addition. Use an addition fact you know to subtract.",
                vocab=["fact family", "related facts", "teen number", "addend"],
                how=dict(text="Find 14 − 6 by thinking addition.", example="6 + ? = 14", steps=[["Think:", "6 + 8 = 14"], ["So", "14 − 6 = 8"]], answer="8", check="14-6==8&&6+8==14"),
                fig=("bars", {"rows": [{"parts": [[14, "14"]]}, {"parts": [[6, "6"], [8, "?"]]}]}, "The whole is 14. One part is 6. The other part is 8."),
                remember=["In subtraction, the whole comes first.", "Go back to 10: 13 − 5 = 13 − 3 − 2 = 8."],
                watch=[["14 − 6 → 12", "do not take 4 from 6. 14 − 6 = 8."], ["6 − 14", "write the whole first: 14 − 6"]],
                tryit=[["16 − 9", "7", "16-9==7"], ["12 − 5", "7", "12-5==7"]])])

# ---------------------------------------------------------------- Unit 4
u = "equal-sign"
V[u] = [("equal sign", "Means “is the same as.”", "4 + 2 = 6"),
        ("equation", "A number sentence with an equal sign.", "8 = 5 + 3"),
        ("true", "Both sides of the equal sign are the same amount.", "7 = 7 is true"),
        ("false", "The two sides are not the same amount.", "5 + 2 = 8 is false"),
        ("unknown", "A missing number in an equation.", "4 + ___ = 9"),
        ("both sides", "The amounts to the left and right of the equal sign.", "6 + 4 = 5 + 5: both sides are 10")]
CARDS[u] = [("Is 7 = 3 + 4 true?", "Yes. 3 + 4 is 7, so both sides are 7.", "concept"),
            ("Is 9 = 9 true?", "Yes. Both sides are 9.", "misconception"),
            ("Is 5 + 4 = 10 true or false?", "False. 5 + 4 is 9.", "example"),
            ("6 + 4 = 5 + ___", "5. Both sides must be 10.", "example"),
            ("8 + ___ = 11", "3, because 8 + 3 = 11.", "example"),
            ("___ − 4 = 6", "10, because 10 − 4 = 6.", "example"),
            ("Kim writes 7 + ___ = 15 → 22. Right?", "No. The blank is 8, because 7 + 8 = 15.", "misconception"),
            ("Does = mean “the answer is”?", "No. It means “is the same as.”", "concept")]
VIS[u] = [("Are the bars the same length?", "bars", {"rows": [{"parts": [[6, "6"], [4, "4"]]}, {"parts": [[5, "5"], [5, "5"]]}]}, "Yes. 6 + 4 = 5 + 5 is true."),
          ("What is the missing part?", "bars", {"rows": [{"parts": [[12, "12"]]}, {"parts": [[8, "8"], [4, "?"]]}]}, "8 + 4 = 12"),
          ("How many more make 10?", "tenframe", {"frames": 1, "a": 7}, "7 + 3 = 10")]
SHEET[u] = dict(focus="the equal sign and true or false equations", morefocus="finding unknown numbers and balancing both sides",
    sides=[dict(big="The equal sign means “is the same as.” An equation is true when both sides are the same amount.",
                vocab=["equal sign", "equation", "true", "false"],
                how=dict(text="Is 8 = 3 + 5 true?", example="8 = 3 + 5", steps=[["Left side:", "8"], ["Right side: 3 + 5 =", "8"]], answer="true", check="8==3+5"),
                fig=("bars", {"rows": [{"parts": [[7, "7"], [2, "2"]]}, {"parts": [[6, "6"], [3, "3"]]}]}, "7 + 2 = 6 + 3. Both bars are 9 long."),
                remember=["The answer can be on either side: 9 = 4 + 5.", "Find the amount on each side, then compare."],
                watch=[["8 = 3 + 5 is backward", "it is true"], ["5 + 2 = 7 + 1", "false: 7 is not 8"]],
                tryit=[["Is 10 = 6 + 4 true?", "true", "10==6+4"], ["Is 3 + 3 = 5 true?", "false", "3+3!=5"]]),
           dict(big="To find an unknown, ask: what number makes both sides the same?",
                vocab=["unknown", "both sides", "equation", "equal sign"],
                how=dict(text="Find the blank: 6 + 4 = 7 + ___", example="6 + 4 = 7 + ___", steps=[["Left side:", "10"], ["7 + 3 =", "10"]], answer="3", check="6+4==7+3"),
                fig=("bars", {"rows": [{"parts": [[6, "6"], [4, "4"]]}, {"parts": [[7, "7"], [3, "?"]]}]}, "Both bars must be 10 long, so the blank is 3."),
                remember=["Put your number in the blank and check.", "Subtraction blanks: 9 − ___ = 5 means 9 − 4 = 5."],
                watch=[["6 + 4 = 7 + 10", "the blank is not the total of the left side"], ["8 + ___ = 11 → 19", "do not add all the numbers"]],
                tryit=[["9 + ___ = 14", "5", "9+5==14"], ["5 + 5 = 8 + ___", "2", "5+5==8+2"]])])

# ---------------------------------------------------------------- Unit 5
u = "word-problems-20"
V[u] = [("add to", "A story where more join a group.", "5 birds, 3 more come"),
        ("take from", "A story where some leave a group.", "9 apples, 4 are eaten"),
        ("put together", "A story with two parts that make a total.", "4 red and 6 blue beads"),
        ("take apart", "A story where a total is split into parts.", "10 cups, 7 are red, the rest blue"),
        ("compare", "Find how many more or fewer.", "8 is 3 more than 5"),
        ("total", "How many in all.", "4 + 6 = 10 in all"),
        ("bar model", "A drawing of bars that shows the parts and the whole.", "a bar for 12 split into 5 and 7")]
CARDS[u] = [("Sam has 7 shells and finds 5 more. How many?", "7 + 5 = 12 shells.", "example"),
            ("12 birds, 4 fly away. How many are left?", "12 − 4 = 8 birds.", "example"),
            ("Mia has 9. Leo has 6. How many more does Mia have?", "9 − 6 = 3 more.", "example"),
            ("Ann had some. She got 4 more. Now she has 11. How many at the start?", "11 − 4 = 7.", "strategy"),
            ("3 red, 5 blue, 6 green. How many in all?", "3 + 5 + 6 = 14.", "example"),
            ("Does “more” always mean add?", "No. “How many more” compares, so subtract.", "misconception"),
            ("10 cups: 6 are red, the rest are blue.", "10 − 6 = 4 blue cups.", "example"),
            ("How do I check my answer?", "Put it back into the story and see if it fits.", "strategy")]
VIS[u] = [("8 big, 5 small. How many in all?", "bars", {"rows": [{"parts": [[13, "?"]]}, {"parts": [[8, "8"], [5, "5"]]}]}, "8 + 5 = 13"),
          ("How many more does Ana have?", "bars", {"rows": [{"label": "Ana", "parts": [[11, "11"]]}, {"label": "Ben", "parts": [[7, "7"]]}]}, "11 − 7 = 4 more"),
          ("6 cookies, 2 eaten. How many left?", "crossrow", {"n": 6, "x": 2}, "6 − 2 = 4")]
SHEET[u] = dict(focus="add to, take from, put together and take apart stories", morefocus="compare stories, unknown starts and three addends",
    sides=[dict(big="Act out the story. Did a group get bigger, get smaller, or is it two parts of a total?",
                vocab=["add to", "take from", "put together", "take apart"],
                how=dict(text="There are 15 cups. 9 are red. The rest are blue. How many are blue?", example="9 + ___ = 15", steps=[["Whole:", "15"], ["15 − 9 =", "6"]], answer="6 blue cups", check="15-9==6"),
                fig=("bars", {"rows": [{"parts": [[15, "15"]]}, {"parts": [[9, "9"], [6, "?"]]}]}, "The whole is 15. One part is 9. The other part is 6."),
                remember=["Write an equation with a blank for the unknown.", "Answer with a number and a word: 6 cups."],
                watch=[["Adding every number you see", "think about what happens first"], ["Giving the part you were told", "find the missing part"]],
                tryit=[["7 ducks, 6 more come. How many?", "13", "7+6==13"], ["14 pens, 5 lost. How many left?", "9", "14-5==9"]]),
           dict(big="Compare stories ask how many more or fewer. Some stories hide the start or the change.",
                vocab=["compare", "total", "bar model", "add to"],
                how=dict(text="Liz has 12 stickers. Max has 8. How many more does Liz have?", example="8 + ___ = 12", steps=[["Line up 12 and 8", ""], ["12 − 8 =", "4"]], answer="4 more", check="12-8==4"),
                fig=("bars", {"rows": [{"label": "Liz", "parts": [[12, "12"]]}, {"label": "Max", "parts": [[8, "8"]]}]}, "The extra part of Liz's bar is 4."),
                remember=["“How many more” and “how many fewer” mean compare.", "Three numbers: add them all, look for a ten."],
                watch=[["Adding because you see “more”", "how many more means find the difference"], ["Unknown start", "had some, got 4, now 11: 11 − 4 = 7"]],
                tryit=[["Ted has 5. Ana has 4 more than Ted. Ana has?", "9", "5+4==9"], ["2 + 8 + 5", "15", "2+8+5==15"]])])

# ---------------------------------------------------------------- Unit 6
u = "tens-ones"
V[u] = [("ten", "A group of 10 ones.", "10 cubes snapped in a tower"),
        ("ones", "Single objects that are not in a ten.", "In 34, there are 4 ones"),
        ("tens place", "The left digit of a two-digit number.", "In 52, the 5 means 5 tens"),
        ("ones place", "The right digit of a two-digit number.", "In 52, the 2 means 2 ones"),
        ("teen number", "1 ten and some ones.", "17 is 1 ten and 7 ones"),
        ("base-ten blocks", "Rods show tens and cubes show ones.", "3 rods and 2 cubes show 32"),
        ("bundle", "Ten objects tied together to make one ten.", "a bundle of 10 straws")]
CARDS[u] = [("How many ones make 1 ten?", "10", "fact"),
            ("16 = 1 ten and ___ ones", "6", "example"),
            ("What number is 4 tens and 7 ones?", "47", "example"),
            ("How many tens are in 80?", "8 tens and 0 ones.", "fact"),
            ("Is 47 the same as 74?", "No. 47 is 4 tens and 7 ones. 74 is 7 tens and 4 ones.", "misconception"),
            ("Count by tens from 30.", "30, 40, 50, 60, 70", "example"),
            ("2 tens and 13 ones is…", "33, because 13 ones is 1 ten and 3 ones.", "concept"),
            ("Is sixteen written 61?", "No. Sixteen is 16: 1 ten and 6 ones.", "misconception")]
VIS[u] = [("What number do the blocks show?", "blocks", {"t": 3, "o": 6}, "3 tens and 6 ones = 36"),
          ("What teen number is shown?", "tenframe", {"frames": 2, "a": 14}, "1 ten and 4 ones = 14"),
          ("How many cubes?", "blocks", {"t": 6, "o": 0}, "6 tens = 60")]
SHEET[u] = dict(focus="ten as a bundle of ten ones and teen numbers", morefocus="counting by tens and tens and ones in two-digit numbers",
    sides=[dict(big="Ten ones make one ten. A teen number is one ten and some ones.",
                vocab=["ten", "ones", "bundle", "teen number"],
                how=dict(text="Show 17 as tens and ones.", example="17", steps=[["Fill a ten:", "1 ten"], ["Left over:", "7 ones"]], answer="1 ten and 7 ones", check="10+7==17"),
                fig=("tenframe", {"frames": 2, "a": 17}, "One full ten frame and 7 more: 17."),
                remember=["11 to 19 all have 1 ten.", "A ten rod is worth 10, not 1."],
                watch=[["Sixteen → 61", "write the ten first: 16"], ["Counting a rod as 1", "each rod is 10"]],
                tryit=[["1 ten and 9 ones", "19", "10+9==19"], ["How many ones in 2 tens?", "20", "2*10==20"]]),
           dict(big="In a two-digit number, the left digit tells the tens and the right digit tells the ones.",
                vocab=["tens place", "ones place", "base-ten blocks", "ten"],
                how=dict(text="How many tens and ones are in 58?", example="58", steps=[["Tens digit:", "5 tens = 50"], ["Ones digit:", "8 ones"]], answer="5 tens and 8 ones", check="50+8==58"),
                fig=("blocks", {"t": 4, "o": 3}, "4 rods and 3 cubes: 43."),
                remember=["Count by tens: 10, 20, 30, 40, 50, 60, 70, 80, 90.", "50 is 5 tens and 0 ones."],
                watch=[["47 → 7 tens and 4 ones", "read the tens digit first"], ["Trading", "12 ones is 1 ten and 2 ones"]],
                tryit=[["6 tens and 2 ones", "62", "60+2==62"], ["How many tens in 90?", "9", "90/10==9"]])])

# ---------------------------------------------------------------- Unit 7
u = "compare-numbers"
V[u] = [("greater than", "More than. The symbol is >.", "52 > 25"),
        ("less than", "Fewer than. The symbol is <.", "25 < 52"),
        ("equal to", "The same amount. The symbol is =.", "40 = 4 tens"),
        ("compare", "Decide which number is greater, less, or if they are equal.", "Compare 38 and 41"),
        ("greatest", "The largest of three or more numbers.", "In 12, 31, 27, the greatest is 31"),
        ("least", "The smallest of three or more numbers.", "In 12, 31, 27, the least is 12")]
CARDS[u] = [("Which is greater: 61 or 59?", "61. It has more tens.", "example"),
            ("Which is less: 34 or 38?", "34. Same tens, fewer ones.", "example"),
            ("Is 29 > 41 because 9 > 1?", "No. Compare tens first: 41 is greater.", "misconception"),
            ("How do you read 45 < 54?", "45 is less than 54.", "concept"),
            ("Which way does the symbol point?", "The open side faces the greater number.", "strategy"),
            ("Order 72, 27, 57 from least to greatest.", "27, 57, 72", "example"),
            ("4? > 46. Which digits work?", "7, 8, or 9.", "example"),
            ("Is 6 tens and 0 ones = 60?", "Yes. 60 = 60.", "concept")]
VIS[u] = [("Which number is greater?", "table", {"header": ["Number", "Tens", "Ones"], "rows": [["A", 3, 8], ["B", 4, 1]]}, "B (41) has more tens than A (38)."),
          ("Compare to 52: blocks ___ 52", "blocks", {"t": 2, "o": 5}, "25 < 52"),
          ("Which comes later on the chart: 67 or 76?", "chart", {"start": 61, "per_row": 10, "rows": 2, "shade": [67, 76]}, "76 comes later, so 76 > 67")]
SHEET[u] = dict(focus="comparing two-digit numbers by tens and ones", morefocus="using >, = and < and reasoning about comparisons",
    sides=[dict(big="To compare, look at the tens first. If the tens are the same, compare the ones.",
                vocab=["compare", "greater than", "less than", "greatest"],
                how=dict(text="Which is greater, 46 or 64?", example="46 and 64", steps=[["Tens:", "4 and 6"], ["6 tens is more", ""]], answer="64", check="64>46"),
                fig=("table", {"header": ["Number", "Tens", "Ones"], "rows": [["46", 4, 6], ["64", 6, 4]]}, "64 has more tens, so 64 is greater."),
                remember=["More tens means a greater number.", "Same tens? The number with more ones is greater."],
                watch=[["29 > 41 because 9 > 1", "compare tens first"], ["Swapped digits are different", "35 and 53 are not equal"]],
                tryit=[["Greater: 73 or 37?", "73", "73>37"], ["Less: 58 or 52?", "52", "52<58"]]),
           dict(big="Write a comparison with >, <, or =. The open side of the symbol faces the greater number.",
                vocab=["greater than", "less than", "equal to", "least"],
                how=dict(text="Write >, <, or =: 38 ___ 41", example="38 ___ 41", steps=[["Tens:", "3 < 4"], ["So", "38 < 41"]], answer="<", check="38<41"),
                fig=None, figtext=["<b>&gt;</b> greater than: 52 &gt; 25", "<b>&lt;</b> less than: 25 &lt; 52", "<b>=</b> equal to: 30 = 3 tens"],
                remember=["Read from left to right: 38 < 41 is “38 is less than 41.”", "Check on a number line: greater numbers are to the right."],
                watch=[["Pointing the symbol the wrong way", "the open side faces the greater number"], ["Using = for close numbers", "= only when exactly the same"]],
                tryit=[["67 ___ 76", "<", "67<76"], ["90 ___ 9 tens", "=", "90==9*10"]])])

# ---------------------------------------------------------------- Unit 8
u = "add-subtract-100"
V[u] = [("10 more", "The number with one more ten.", "10 more than 34 is 44"),
        ("10 less", "The number with one less ten.", "10 less than 34 is 24"),
        ("decade number", "A number with 0 ones: 10, 20, 30 …", "70 is a decade number"),
        ("new ten", "10 ones put together to make 1 ten.", "8 ones + 5 ones = 1 ten and 3 ones"),
        ("hundred chart", "A chart of 1 to 100 in rows of 10.", "Below 23 is 33"),
        ("place value", "The value of a digit by its place.", "In 46, the 4 is worth 40")]
CARDS[u] = [("10 more than 57", "67. Only the tens digit changes.", "fact"),
            ("10 less than 81", "71", "fact"),
            ("40 + 30", "70. 4 tens + 3 tens = 7 tens.", "example"),
            ("80 − 50", "30. 8 tens − 5 tens = 3 tens.", "example"),
            ("32 + 5", "37. Add ones to ones.", "example"),
            ("Is 32 + 5 = 82?", "No. Add 5 to the ones: 37.", "misconception"),
            ("38 + 5: make a new ten", "38 + 2 = 40, 40 + 3 = 43.", "strategy"),
            ("24 + 35", "Tens 20 + 30 = 50. Ones 4 + 5 = 9. Total 59.", "strategy")]
VIS[u] = [("What is 10 more?", "blocks", {"t": 2, "o": 7}, "27 + 10 = 37"),
          ("What number is below 45?", "chart", {"start": 41, "per_row": 10, "rows": 2, "hide": [55]}, "55 (10 more than 45)"),
          ("Add 6 ones. What is the sum?", "blocks", {"t": 4, "o": 8}, "48 + 6 = 54 (8 + 6 = 14 makes a new ten)")]
SHEET[u] = dict(focus="10 more, 10 less and adding or subtracting tens", morefocus="adding a one-digit or two-digit number and making a new ten",
    sides=[dict(big="Adding or taking away tens only changes the tens digit. The ones stay the same.",
                vocab=["10 more", "10 less", "decade number", "hundred chart"],
                how=dict(text="Find 53 + 20.", example="53 + 20", steps=[["Tens:", "5 + 2 = 7 tens"], ["Ones stay:", "3"]], answer="73", check="53+20==73"),
                fig=("chart", {"start": 31, "per_row": 10, "rows": 3, "shade": [36, 46, 56]}, "Down one row is 10 more: 36, 46, 56."),
                remember=["10 more: the tens digit goes up 1.", "50 − 20: 5 tens − 2 tens = 3 tens = 30."],
                watch=[["34 + 10 → 35", "change the tens, not the ones"], ["50 − 20 → 3", "3 tens is 30"]],
                tryit=[["10 less than 62", "52", "62-10==52"], ["70 − 40", "30", "70-40==30"]]),
           dict(big="Add tens to tens and ones to ones. When the ones make 10 or more, make a new ten.",
                vocab=["new ten", "place value", "10 more", "decade number"],
                how=dict(text="Find 47 + 6.", example="47 + 6", steps=[["47 + 3 =", "50"], ["50 + 3 =", "53"]], answer="53", check="47+6==53&&47+3==50"),
                fig=("blocks", {"t": 2, "o": 9}, "29 + 4: 9 ones + 4 ones = 13 ones = 1 ten and 3 ones. 29 + 4 = 33."),
                remember=["Fill the next ten first: 38 + 5 = 40 + 3.", "24 + 35: 20 + 30 = 50, 4 + 5 = 9, so 59."],
                watch=[["32 + 5 → 82", "add 5 to the ones"], ["38 + 5 → 313", "13 ones is 1 ten and 3 ones: 43"]],
                tryit=[["26 + 3", "29", "26+3==29"], ["58 + 7", "65", "58+7==65"]])])

# ---------------------------------------------------------------- Unit 9
u = "measuring-length"
V[u] = [("length", "How long something is.", "The pencil is 6 cubes long"),
        ("longer", "Has more length.", "A bus is longer than a car"),
        ("shorter", "Has less length.", "A crayon is shorter than a pencil"),
        ("longest", "Has the most length of three or more.", "rope, ribbon, string: the rope is longest"),
        ("shortest", "Has the least length of three or more.", "the crayon is shortest"),
        ("length unit", "A same-size object used to measure.", "cubes or paper clips"),
        ("end to end", "Units touch with no gaps and no overlaps.", "cubes lined up in a row")]
CARDS[u] = [("Before comparing two lengths…", "Line up the ends at the same starting line.", "strategy"),
            ("Rope is longer than the desk. Desk is longer than the box. Rope or box?", "The rope is longer.", "concept"),
            ("A pencil is 7 cubes long. What does that mean?", "7 same-size cubes fit end to end along it.", "concept"),
            ("Gaps between units?", "The count is too small. Units must touch.", "misconception"),
            ("Overlapping units?", "The count is too big. Units must not overlap.", "misconception"),
            ("Big and small cubes mixed?", "Not fair. Use units that are all the same size.", "misconception"),
            ("Pencil 8 cubes, crayon 5 cubes. How much longer?", "8 − 5 = 3 cubes longer.", "example"),
            ("Paper clips or craft sticks: which takes more?", "Paper clips. Smaller units need more.", "concept")]
VIS[u] = [("Which is longest?", "lengths", {"items": [{"label": "Pencil", "len": 6}, {"label": "Crayon", "len": 4, "color": "orange"}, {"label": "Rope", "len": 9, "color": "green"}]}, "The rope is longest."),
          ("How long is the ribbon?", "measure", {"len": 5, "units": [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1]], "unit": "cube", "label": "Ribbon"}, "5 cubes"),
          ("Measured the right way?", "measure", {"len": 6, "units": [[0, 1], [1, 1], [2.4, 1], [3.4, 1], [4.4, 1]], "unit": "cube", "label": "Stick"}, "No. There is a gap.")]
SHEET[u] = dict(focus="comparing and ordering lengths, directly and with a third object", morefocus="measuring with same-size length units, end to end",
    sides=[dict(big="Line up the ends to compare. If you cannot move things, compare each to a third object.",
                vocab=["length", "longer", "shorter", "longest"],
                how=dict(text="The bed is longer than the rope. The rope is longer than the desk. Which is longer, the bed or the desk?", example="bed > rope > desk", steps=[["Order:", "bed, rope, desk"]], answer="the bed", check="3>2&&2>1"),
                fig=("lengths", {"items": [{"label": "Rope", "len": 8}, {"label": "Ribbon", "len": 5, "color": "orange"}, {"label": "String", "len": 3, "color": "green"}]}, "Shortest to longest: string, ribbon, rope."),
                remember=["Start all objects at the same line.", "Order three: find the shortest, then the next, then the longest."],
                watch=[["Ends not lined up", "an object can look longer when it is not"], ["Mixing up longer and shorter", "say both: A is longer, B is shorter"]],
                tryit=[["Ann's worm is longer than Ben's. Ben's is longer than Cal's. Longest?", "Ann's", "3>2&&2>1"], ["Pen 7, crayon 4 cubes. How much longer?", "3 cubes", "7-4==3"]]),
           dict(big="Length is the number of same-size units that fit end to end with no gaps or overlaps.",
                vocab=["length unit", "end to end", "length", "shortest"],
                how=dict(text="How long is the pencil?", example="cubes under the pencil", steps=[["Start at one end", ""], ["Count the cubes:", "6"]], answer="6 cubes", check="1+1+1+1+1+1==6"),
                fig=("measure", {"len": 6, "units": [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]], "unit": "cube", "label": "Pencil"}, "6 cubes, end to end: the pencil is 6 cubes long."),
                remember=["Every unit must be the same size.", "Smaller units: more of them. Bigger units: fewer."],
                watch=[["Gaps", "make the count too small"], ["Overlaps", "make the count too big"]],
                tryit=[["9 paper clips end to end. How long?", "9 paper clips", "9==9"], ["Gaps: counted 5. Real length?", "more than 5", "6>5"]])])

# ---------------------------------------------------------------- Unit 10
u = "telling-time"
V[u] = [("hour hand", "The short hand. It tells the hour.", "It points to 3 at 3 o'clock"),
        ("minute hand", "The long hand. It tells the minutes.", "It points to 12 at o'clock"),
        ("o'clock", "Time to the hour, with 0 minutes.", "7 o'clock is 7:00"),
        ("half past", "30 minutes after the hour.", "half past 4 is 4:30"),
        ("analog clock", "A clock with a face and hands.", "the classroom clock"),
        ("digital clock", "A clock that shows numbers only.", "9:30"),
        ("half hour", "30 minutes.", "from 2:00 to 2:30")]
CARDS[u] = [("At 6 o'clock, where is the minute hand?", "At the 12.", "fact"),
            ("At half past 6, where is the minute hand?", "At the 6.", "fact"),
            ("At half past 6, where is the hour hand?", "Between the 6 and the 7.", "misconception"),
            ("Write half past 9 like a digital clock.", "9:30", "example"),
            ("What does 11:00 mean?", "11 o'clock.", "example"),
            ("1 hour after 3:00", "4:00", "example"),
            ("Half an hour after 5:00", "5:30", "example"),
            ("The hour hand is past 8 but not at 9. The minute hand is at 6.", "Half past 8, or 8:30. Not 9:30.", "misconception")]
VIS[u] = [("What time is it?", "clock", {"h": 4, "m": 0}, "4 o'clock, 4:00"),
          ("What time is it?", "clock", {"h": 10, "m": 30}, "half past 10, 10:30"),
          ("Say it in words.", "digital", {"h": 2, "m": 30}, "half past 2")]
SHEET[u] = dict(focus="telling time to the hour on analog and digital clocks", morefocus="telling time to the half hour and matching clock times",
    sides=[dict(big="The short hand tells the hour. At o'clock, the long hand points to 12.",
                vocab=["hour hand", "minute hand", "o'clock", "analog clock"],
                how=dict(text="Read the clock: short hand at 8, long hand at 12.", example="8 and 12", steps=[["Hour:", "8"], ["Minutes:", "0"]], answer="8:00, 8 o'clock", check="8==8"),
                fig=("clock", {"h": 8, "m": 0}, "8 o'clock: the hour hand is at 8 and the minute hand is at 12."),
                remember=["Digital: hours, then a colon, then minutes: 8:00.", "1 hour later, the hour hand moves to the next number."],
                watch=[["Mixing up the hands", "short = hour, long = minutes"], ["12:15 for 3 o'clock", "read the short hand for the hour"]],
                tryit=[["Short hand at 5, long hand at 12", "5:00", "5==5"], ["1 hour after 11:00", "12:00", "11+1==12"]]),
           dict(big="Half past means 30 minutes after the hour. The long hand points to 6 and the short hand is halfway to the next hour.",
                vocab=["half past", "half hour", "digital clock", "hour hand"],
                how=dict(text="Read the clock: short hand between 3 and 4, long hand at 6.", example="between 3 and 4", steps=[["Hour: the number it passed", "3"], ["Minutes:", "30"]], answer="3:30, half past 3", check="3<4"),
                fig=("clock", {"h": 3, "m": 30}, "Half past 3: the hour hand is between 3 and 4."),
                remember=["Half past 7 is written 7:30.", "Half an hour after 7:00 is 7:30."],
                watch=[["Reading the next hour", "between 3 and 4 is still 3"], ["Writing 6:50 or 6:3", "half past 6 is 6:30"]],
                tryit=[["Half past 11 on a digital clock", "11:30", "11==11"], ["Half an hour after 2:00", "2:30", "0+30==30"]])])

# ---------------------------------------------------------------- Unit 11
u = "data"
V[u] = [("data", "Information you collect, like answers to a question.", "votes for a favorite fruit"),
        ("sort", "Put objects into groups that are alike.", "sort blocks by color"),
        ("category", "One group in a set of data.", "Apple, Banana, and Grape are categories"),
        ("tally mark", "A line that stands for 1. Five is four lines and a slash.", "a bundle of 5 and 2 more is 7"),
        ("tally chart", "A chart that uses tally marks to show data.", "Dogs: 6 tally marks"),
        ("picture graph", "A graph that uses pictures to show data.", "each star stands for 1"),
        ("table", "Rows and columns of data.", "Red 7, Blue 4, Green 9"),
        ("in all", "The total of all the categories.", "7 + 4 + 9 = 20 in all")]
CARDS[u] = [("How many is a bundle of tally marks?", "5", "fact"),
            ("2 bundles and 3 more marks", "5 + 5 + 3 = 13", "example"),
            ("Red 8, Blue 5. How many more red?", "8 − 5 = 3 more.", "example"),
            ("Red 8, Blue 5, Green 4. How many in all?", "8 + 5 + 4 = 17.", "example"),
            ("Which has the most?", "The category with the biggest number.", "concept"),
            ("Is each bundle of tallies worth 1?", "No. Each bundle is 5.", "misconception"),
            ("“How many more”: add or subtract?", "Subtract to compare the two numbers.", "misconception"),
            ("Sort 10 buttons: 6 big. How many small?", "10 − 6 = 4.", "example")]
VIS[u] = [("How many votes for Cat?", "tally", {"title": "Pets", "cats": ["Dog", "Cat", "Fish"], "counts": [6, 9, 3]}, "9 (one bundle of 5 and 4 more)"),
          ("Which has the fewest?", "picgraph", {"title": "Favorite Fruit", "cats": ["Apple", "Banana", "Grape"], "symbols": [5, 3, 7], "key": 1, "icon": "star", "unit": ""}, "Banana (3)"),
          ("How many in all?", "table", {"header": ["Color", "Number"], "rows": [["Red", 6], ["Blue", 4], ["Green", 5]]}, "6 + 4 + 5 = 15")]
SHEET[u] = dict(focus="sorting and showing data with tally marks", morefocus="reading picture graphs and tables and answering questions",
    sides=[dict(big="Sort objects into groups, then show how many are in each group with tally marks, pictures, or numbers.",
                vocab=["data", "sort", "category", "tally mark"],
                how=dict(text="Read the tally: 2 bundles and 1 more mark.", example="bundles of 5", steps=[["Count by fives:", "5, 10"], ["Count on 1:", "11"]], answer="11", check="5+5+1==11"),
                fig=("tally", {"title": "Weather", "cats": ["Sunny", "Rainy", "Cloudy"], "counts": [11, 4, 7]}, "Sunny 11, Rainy 4, Cloudy 7."),
                remember=["Make a tally mark for each object.", "Every fifth mark crosses the four before it."],
                watch=[["Counting a bundle as 1", "a bundle is 5"], ["Counting an object twice", "cross it off as you tally"]],
                tryit=[["3 bundles and 2 marks", "17", "5+5+5+2==17"], ["Show 8 with tallies", "1 bundle and 3 marks", "5+3==8"]]),
           dict(big="Read each category carefully. Add to find how many in all. Subtract to compare two categories.",
                vocab=["picture graph", "table", "tally chart", "in all"],
                how=dict(text="Apple 5, Banana 3, Grape 7. How many more chose Grape than Banana?", example="7 and 3", steps=[["Grape:", "7"], ["7 − 3 =", "4"]], answer="4 more", check="7-3==4"),
                fig=("picgraph", {"title": "Favorite Fruit", "cats": ["Apple", "Banana", "Grape"], "symbols": [5, 3, 7], "key": 1, "icon": "star", "unit": ""}, "Each star stands for 1 vote."),
                remember=["In all: add all the categories.", "How many more or fewer: subtract."],
                watch=[["Reading the wrong row", "point to the label first"], ["Adding for “how many more”", "subtract to compare"]],
                tryit=[["How many in all? 5, 3, 7", "15", "5+3+7==15"], ["Apple 5, Banana 3. How many fewer bananas?", "2", "5-3==2"]])])

# ---------------------------------------------------------------- Unit 12
u = "shapes-equal-shares"
V[u] = [("side", "A straight line that is part of a shape.", "a triangle has 3 sides"),
        ("corner", "Where two sides meet. Also called a vertex.", "a square has 4 corners"),
        ("closed shape", "A shape with no gaps in its sides.", "a triangle is closed"),
        ("triangle", "A closed shape with 3 sides and 3 corners.", "a slice of pizza"),
        ("rectangle", "A closed shape with 4 sides and 4 square corners.", "a door"),
        ("square", "A rectangle with 4 equal sides.", "a sticky note"),
        ("trapezoid", "A 4-sided shape like the red pattern block.", "two make a hexagon"),
        ("hexagon", "A closed shape with 6 sides and 6 corners.", "the yellow pattern block"),
        ("cube", "A solid with 6 square faces.", "a number cube"),
        ("cylinder", "A solid with 2 circle faces and a curved side.", "a can"),
        ("cone", "A solid with 1 circle face and a point.", "an ice cream cone"),
        ("halves", "2 equal shares of a whole.", "half of a sandwich"),
        ("fourths", "4 equal shares of a whole. Also called quarters.", "a fourth of a pizza")]
CARDS[u] = [("How many sides does a triangle have?", "3 sides and 3 corners.", "fact"),
            ("A turned square: still a square?", "Yes. Turning does not change sides or corners.", "misconception"),
            ("A big red triangle and a small blue triangle?", "Both are triangles. Color and size do not matter.", "concept"),
            ("3 lines with a gap: a triangle?", "No. A triangle must be closed.", "misconception"),
            ("How many triangles make the yellow hexagon?", "6 triangles.", "fact"),
            ("Two half-circles make…", "a circle.", "fact"),
            ("Which is bigger: a half or a fourth of the same pizza?", "A half. More shares are smaller shares.", "misconception"),
            ("How many fourths make one whole?", "4 fourths.", "fact")]
VIS[u] = [("Name the shape.", "shapes1", {"items": [{"kind": "trapezoid", "color": "orange"}]}, "trapezoid"),
          ("How many triangles?", "compose", {"name": "hex_tri6"}, "6 triangles make a hexagon"),
          ("What part is shaded?", "partition", {"shape": "circle", "n": 4, "shade": [0]}, "one fourth (a quarter)")]
SHEET[u] = dict(focus="defining attributes, naming shapes and composing shapes", morefocus="halves and fourths, and more shares are smaller shares",
    sides=[dict(big="A shape's name comes from its sides and corners and whether it is closed, not from its color, size, or how it is turned.",
                vocab=["side", "corner", "closed shape", "hexagon"],
                how=dict(text="Name a closed shape with 4 sides and 4 square corners, with 2 long and 2 short sides.", example="4 sides", steps=[["Count sides:", "4"], ["Square corners:", "4"]], answer="rectangle", check="4==4"),
                fig=("compose", {"name": "hex_trap2"}, "2 trapezoids make a hexagon."),
                remember=["Triangle 3 sides, rectangle 4, hexagon 6.", "Solids: cube, rectangular prism, cylinder, cone."],
                watch=[["A turned square is a “diamond”", "it is still a square"], ["An open figure", "it must be closed to be a shape"]],
                tryit=[["Sides on 2 triangles", "6", "3+3==6"], ["Triangles in a hexagon", "6", "6==6"]]),
           dict(big="Equal shares are the same size. Two equal shares are halves. Four equal shares are fourths, or quarters.",
                vocab=["halves", "fourths", "cube", "cylinder"],
                how=dict(text="A pizza is cut into 4 equal shares. What is one share called?", example="4 equal shares", steps=[["4 equal shares:", "fourths"], ["One share:", "one fourth"]], answer="a fourth (a quarter)", check="4==4"),
                fig=("partition_pair", {"a": {"shape": "rect", "cuts": "v", "widths": [1, 1], "shade": [0]}, "b": {"shape": "rect", "cuts": "v", "widths": [1, 1, 1, 1], "shade": [0]}}, "Same rectangle: one half is bigger than one fourth."),
                remember=["2 halves or 4 fourths make one whole.", "More equal shares means smaller shares."],
                watch=[["Unequal parts", "they are not halves or fourths"], ["A fourth is bigger than a half?", "no: a half is bigger"]],
                tryit=[["How many halves make a whole?", "2", "2==2"], ["4 fourths, 1 eaten. How many left?", "3", "4-1==3"]])])
