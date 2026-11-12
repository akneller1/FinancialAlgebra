/*
  MR. K'S CLASSROOM: LIBRARY CONTENT

  To add an activity:
    1. Put its HTML file in a new folder under artifacts/, for example artifacts/my-activity/index.html
    2. Optional: add a preview image at thumbs/my-activity.jpg (about 720 x 450 pixels).
    3. Add an entry to the right unit's "artifacts" list below.

  Activity fields
    title        Name shown on the card.
    path         Where the activity's HTML file lives.
    thumb        Preview image (optional; a colored placeholder shows without one).
    description  One or two sentences about what students do.
    type         "Game", "Practice", "Exploration", and so on. Becomes a filter.
    level        Optional, for example ["CP"] or ["CP", "Honors"]. Becomes a filter.
    topics       Optional list of skills. Searchable and shown on the card.
    added        Date as "YYYY-MM-DD". Activities show a "New" tag for 30 days.

  Course colors: "blue", "orange", "green", or "purple". Units show in the order listed.
  A unit with no activities shows as "Coming soon".
*/
window.LIBRARY = {
  "title": "Mr. K's Classroom",
  "tagline": "Interactive math games, generators and printables for Algebra 1, Geometry, and Algebra 2. Choose a unit and open an activity on any device.",
  "footer": "Activities run in any modern browser. Saved activities are kept in this browser only.",
  "newDays": 30,
  "courses": [
{
  "id": "discrete",
  "name": "Discrete Math",
  "color": "green",
  "art": "network",
  "planned": true,
  "blurb": "Logic, proofs, counting, graphs, voting, and optimization.",
  "curriculumSource": "https://www.stjohns.k12.fl.us/year-at-a-glance/wp-content/uploads/sites/101/2025/08/Discrete-Math-Honors-Year-at-a-Glance-25-26.pdf",
  "units": [
    {
      "id": "speaking-mathematically",
      "name": "Speaking Mathematically",
      "quarter": 1,
      "artifacts": []
    },
    {
      "id": "compound-statements-logic",
      "name": "The Logic of Compound Statements",
      "quarter": 1,
      "artifacts": []
    },
    {
      "id": "number-theory-proof",
      "name": "Elementary Number Theory and Methods of Proof",
      "quarter": 1,
      "artifacts": []
    },
    {
      "id": "sequences-induction-recursion",
      "name": "Sequences, Mathematical Induction, and Recursion",
      "quarter": 2,
      "artifacts": []
    },
    {
      "id": "set-theory",
      "name": "Set Theory",
      "quarter": 2,
      "artifacts": []
    },
    {
      "id": "properties-relations",
      "name": "Properties of Relations",
      "quarter": 3,
      "artifacts": []
    },
    {
      "id": "counting-probability",
      "name": "Counting and Probability",
      "quarter": 3,
      "artifacts": []
    },
    {
      "id": "graphs-trees",
      "name": "Theory of Graphs and Trees",
      "quarter": 3,
      "artifacts": []
    },
    {
      "id": "election-theory",
      "name": "Election Theory",
      "quarter": 4,
      "artifacts": []
    },
    {
      "id": "linear-programming",
      "name": "Linear Programming",
      "quarter": 4,
      "artifacts": []
    }
  ]
},
{
  "id": "statistics",
  "name": "Statistics",
  "color": "blue",
  "art": "distribution",
  "planned": false,
  "blurb": "Explore data, design studies, model chance, and draw conclusions with statistical inference.",
  "curriculumSource": "https://resources.finalsite.net/images/v1623872059/parkhillk12mous/cskhg83dim7bbtbfbqej/StatisticsCourseSummary--BoardApprovedMarch302017.pdf",
  "units": [
    {
      "id": "exploring-data",
      "name": "Exploring Data",
      "weeks": 4,
      "artifacts": []
    },
    {
      "id": "sampling-experimentation",
      "name": "Sampling and Experimentation",
      "weeks": 2,
      "artifacts": []
    },
    {
      "id": "anticipating-patterns",
      "name": "Anticipating Patterns",
      "weeks": 5,
      "artifacts": []
    },
    {
      "id": "statistical-inference",
      "name": "Statistical Inference",
      "weeks": 7,
      "artifacts": []
    }
  ]
},
{
  "id": "calculus",
  "name": "Calculus",
  "color": "orange",
  "art": "tangent",
  "planned": true,
  "blurb": "Limits, derivatives, integrals, and their applications. AP Calculus AB scope.",
  "units": [
    {
      "id": "precalculus-review",
      "name": "Precalculus Review",
      "artifacts": []
    },
    {
      "id": "limits-continuity",
      "name": "Limits and Continuity",
      "artifacts": []
    },
    {
      "id": "derivatives",
      "name": "Derivatives",
      "artifacts": []
    },
    {
      "id": "applications-derivatives",
      "name": "Applications of Derivatives",
      "artifacts": []
    },
    {
      "id": "antiderivatives-definite-integrals",
      "name": "Antiderivatives and Definite Integrals",
      "artifacts": []
    },
    {
      "id": "fundamental-theorem-calculus",
      "name": "The Fundamental Theorem of Calculus",
      "artifacts": []
    },
    {
      "id": "applications-integrals",
      "name": "Applications of Integrals",
      "artifacts": []
    },
    {
      "id": "differential-equations",
      "name": "Differential Equations",
      "artifacts": []
    },
    {
      "id": "ap-review",
      "name": "AP Calculus Review",
      "artifacts": []
    }
  ]
},
{
  "id": "precalculus",
  "name": "Precalculus",
  "color": "purple",
  "art": "wave",
  "planned": true,
  "blurb": "Functions, trigonometry, conics, matrices, vectors, and probability.",
  "units": [
    {
      "id": "equations-inequalities",
      "name": "Equations and Inequalities",
      "artifacts": []
    },
    {
      "id": "functions",
      "name": "Functions",
      "artifacts": []
    },
    {
      "id": "conics",
      "name": "Conics",
      "artifacts": []
    },
    {
      "id": "trigonometric-functions",
      "name": "Trigonometric Functions",
      "artifacts": []
    },
    {
      "id": "general-triangle-trigonometry",
      "name": "Trigonometry of General Triangles",
      "artifacts": []
    },
    {
      "id": "matrices",
      "name": "Matrices",
      "artifacts": []
    },
    {
      "id": "vectors",
      "name": "Vectors",
      "artifacts": []
    },
    {
      "id": "probability",
      "name": "Probability",
      "artifacts": []
    }
  ]
},
    {
      "id": "algebra",
      "name": "Algebra 1",
      "color": "blue",
      "art": "curve",
      "blurb": "Equations, inequalities, functions, and polynomials.",
      "units": [
        {
          "id": "foundations-algebra",
          "name": "Foundations of Algebra",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-foundations",
              "thumb": "thumbs/practice-test.svg",
              "description": "Measure Foundations of Algebra readiness with a mixed-topic test, diagnostic skill report, and fresh targeted reassessment.",
              "type": "Study Guide",
              "topics": [
                "Foundations of Algebra",
                "Test readiness",
                "Self-assessment"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-foundations",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-foundations",
              "thumb": "thumbs/worksheet-generator-foundations.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-foundations",
              "thumb": "thumbs/menu-assessment-generator-foundations.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=maze",
              "thumb": "thumbs/maze-generator-foundations.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=color",
              "thumb": "thumbs/color-generator-foundations.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-foundations.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=error",
              "thumb": "thumbs/error-generator-foundations.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=partner",
              "thumb": "thumbs/partner-generator-foundations.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=who",
              "thumb": "thumbs/who-generator-foundations.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=stations",
              "thumb": "thumbs/stations-generator-foundations.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Foundations of Algebra Flashcards",
              "path": "artifacts/foundations-algebra-flashcards/index.html",
              "thumb": "thumbs/foundations-algebra-flashcards.jpg",
              "description": "A fresh deck of foundations of algebra flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Combining like terms",
                "Distributive property",
                "Evaluating expressions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Foundations of Algebra Showdown",
              "path": "artifacts/foundations-algebra-showdown/index.html",
              "thumb": "thumbs/foundations-algebra-showdown.jpg",
              "description": "A game board for foundations of algebra review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Combining like terms",
                "Distributive property",
                "Evaluating expressions",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Foundations of Algebra Connect Four",
              "path": "artifacts/foundations-algebra-connect-four/index.html",
              "thumb": "thumbs/foundations-algebra-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice foundations of algebra problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Combining like terms",
                "Distributive property",
                "Evaluating expressions",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Foundations of Algebra Tic-Tac-Toe",
              "path": "artifacts/foundations-algebra-tic-tac-toe/index.html",
              "thumb": "thumbs/foundations-algebra-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice foundations of algebra problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Combining like terms",
                "Distributive property",
                "Evaluating expressions",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Foundations of Algebra: Picture Reveal",
              "path": "artifacts/foundations-algebra-picture-reveal/index.html",
              "thumb": "thumbs/foundations-algebra-picture-reveal.jpg",
              "description": "Solve 10 foundations of algebra problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Combining like terms",
                "Distributive property",
                "Evaluating expressions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "The Midnight Library Mystery",
              "path": "artifacts/foundations-algebra-midnight-library-mystery/index.html",
              "thumb": "thumbs/foundations-algebra-midnight-library-mystery.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Order of operations",
                "Evaluating expressions",
                "Combining like terms",
                "Distributive property",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Night at the Number Museum",
              "path": "artifacts/foundations-algebra-escape-room/index.html",
              "thumb": "thumbs/foundations-algebra-escape-room.jpg",
              "description": "Story-driven escape room for teams: five galleries with a cipher, hidden clues, property plaques, a step-ordering lock and dials, a 10-minute timer, hints that cost time, and a final password. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Order of operations",
                "Evaluating expressions",
                "Combining like terms",
                "Distributive property",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Foundations of Algebra Cheat Sheet",
              "path": "artifacts/foundations-algebra-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/foundations-algebra-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: variables, order of operations, real numbers, properties and simplifying. Back: like terms, the distributive property, words to algebra and integers. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            }
          ]
        },
        {
          "id": "expressions-equations",
          "name": "Solving Linear Equations",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-expressions-equations",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-expressions-equations",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-expressions-equations",
              "thumb": "thumbs/worksheet-generator-expressions-equations.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-expressions-equations",
              "thumb": "thumbs/menu-assessment-generator.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=maze",
              "thumb": "thumbs/maze-generator-expressions-equations.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=color",
              "thumb": "thumbs/color-generator-expressions-equations.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-expressions-equations.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=error",
              "thumb": "thumbs/error-generator-expressions-equations.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=partner",
              "thumb": "thumbs/partner-generator-expressions-equations.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=who",
              "thumb": "thumbs/who-generator-expressions-equations.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=stations",
              "thumb": "thumbs/stations-generator-expressions-equations.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "The Golden Whisk Caper",
              "path": "artifacts/expressions-equations-golden-whisk-caper/index.html",
              "thumb": "thumbs/expressions-equations-golden-whisk-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Solving equations",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "The Great Rigged Bake-Off",
              "path": "artifacts/expressions-equations-escape-room/index.html",
              "thumb": "thumbs/expressions-equations-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Combining like terms",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Solving Linear Equations Cheat Sheet",
              "path": "artifacts/expressions-equations-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/expressions-equations-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: solving one-step, two-step and multi-step equations, and checking solutions. Back: writing equations from words, proportions, percents and literal equations. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Solving Equations Flashcards",
              "path": "artifacts/solving-equations-flashcards/index.html",
              "thumb": "thumbs/solving-equations-flashcards.jpg",
              "description": "A fresh deck of solving equations flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Multi-step equations",
                "Variables on both sides",
                "Proportions",
                "Literal equations",
                "Equations from word problems"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Solving Equations Showdown",
              "path": "artifacts/solving-equations-showdown/index.html",
              "thumb": "thumbs/solving-equations-showdown.jpg",
              "description": "A game board for solving equations review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Multi-step equations",
                "Variables on both sides",
                "Proportions",
                "Literal equations",
                "Equations from word problems",
                "Team game"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Solving Equations Connect Four",
              "path": "artifacts/solving-equations-connect-four/index.html",
              "thumb": "thumbs/solving-equations-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice solving equations problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Multi-step equations",
                "Variables on both sides",
                "Proportions",
                "Literal equations",
                "Equations from word problems",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Solving Equations Tic-Tac-Toe",
              "path": "artifacts/solving-equations-tic-tac-toe/index.html",
              "thumb": "thumbs/solving-equations-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice solving equations problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Multi-step equations",
                "Variables on both sides",
                "Proportions",
                "Literal equations",
                "Equations from word problems",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Solving Equations: Picture Reveal",
              "path": "artifacts/solving-equations-picture-reveal/index.html",
              "thumb": "thumbs/solving-equations-picture-reveal.jpg",
              "description": "Solve 10 solving equations problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Multi-step equations",
                "Variables on both sides",
                "Proportions",
                "Literal equations",
                "Equations from word problems"
              ],
              "added": "2026-10-25"
            }
          ]
        },
        {
          "id": "inequalities",
          "name": "Linear Inequalities",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-inequalities",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-inequalities",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Linear Inequalities",
                "Unit 3"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-inequalities",
              "thumb": "thumbs/worksheet-generator-inequalities.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Inequalities"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-inequalities",
              "thumb": "thumbs/menu-assessment-generator-inequalities.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Inequalities"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=maze",
              "thumb": "thumbs/maze-generator-inequalities.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=color",
              "thumb": "thumbs/color-generator-inequalities.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-inequalities.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=error",
              "thumb": "thumbs/error-generator-inequalities.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=partner",
              "thumb": "thumbs/partner-generator-inequalities.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=who",
              "thumb": "thumbs/who-generator-inequalities.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=stations",
              "thumb": "thumbs/stations-generator-inequalities.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "The Golden Parabola Heist",
              "path": "artifacts/inequalities-golden-parabola-heist/index.html",
              "thumb": "thumbs/inequalities-golden-parabola-heist.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Inequalities",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Code Red: Station Nimbus",
              "path": "artifacts/inequalities-escape-room/index.html",
              "thumb": "thumbs/inequalities-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Compound inequalities",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Linear Inequalities Cheat Sheet",
              "path": "artifacts/inequalities-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/inequalities-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: writing, solving and graphing inequalities. Back: compound inequalities, absolute value and inequalities in context. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Linear Inequalities",
                "Unit 3"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Linear Inequalities Flashcards",
              "path": "artifacts/linear-inequalities-flashcards/index.html",
              "thumb": "thumbs/linear-inequalities-flashcards.jpg",
              "description": "A fresh deck of linear inequalities flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Solving inequalities",
                "Compound inequalities",
                "Absolute value inequalities",
                "Inequalities from word problems"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Linear Inequalities Showdown",
              "path": "artifacts/linear-inequalities-showdown/index.html",
              "thumb": "thumbs/linear-inequalities-showdown.jpg",
              "description": "A game board for linear inequalities review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Solving inequalities",
                "Compound inequalities",
                "Absolute value inequalities",
                "Inequalities from word problems",
                "Team game"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Linear Inequalities Connect Four",
              "path": "artifacts/linear-inequalities-connect-four/index.html",
              "thumb": "thumbs/linear-inequalities-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice linear inequalities problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Solving inequalities",
                "Compound inequalities",
                "Absolute value inequalities",
                "Inequalities from word problems",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Linear Inequalities Tic-Tac-Toe",
              "path": "artifacts/linear-inequalities-tic-tac-toe/index.html",
              "thumb": "thumbs/linear-inequalities-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice linear inequalities problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Solving inequalities",
                "Compound inequalities",
                "Absolute value inequalities",
                "Inequalities from word problems",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Linear Inequalities: Picture Reveal",
              "path": "artifacts/linear-inequalities-picture-reveal/index.html",
              "thumb": "thumbs/linear-inequalities-picture-reveal.jpg",
              "description": "Solve 10 linear inequalities problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Solving inequalities",
                "Compound inequalities",
                "Absolute value inequalities",
                "Inequalities from word problems"
              ],
              "added": "2026-10-25"
            }
          ]
        },
        {
          "id": "relations-functions",
          "name": "Relations and Functions",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-relations-functions",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-relations-functions",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Relations and Functions",
                "Unit 4"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-relations-functions",
              "thumb": "thumbs/worksheet-generator-relations-functions.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-relations-functions",
              "thumb": "thumbs/menu-assessment-generator-relations-functions.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=maze",
              "thumb": "thumbs/maze-generator-relations-functions.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=color",
              "thumb": "thumbs/color-generator-relations-functions.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-relations-functions.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=error",
              "thumb": "thumbs/error-generator-relations-functions.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=partner",
              "thumb": "thumbs/partner-generator-relations-functions.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=who",
              "thumb": "thumbs/who-generator-relations-functions.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=stations",
              "thumb": "thumbs/stations-generator-relations-functions.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Relations and Functions Flashcards",
              "path": "artifacts/relations-functions-flashcards/index.html",
              "thumb": "thumbs/relations-functions-flashcards.jpg",
              "description": "A fresh deck of relations and functions flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Relations and Functions Showdown",
              "path": "artifacts/relations-functions-showdown/index.html",
              "thumb": "thumbs/relations-functions-showdown.jpg",
              "description": "A game board for relations and functions review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Relations and Functions Connect Four",
              "path": "artifacts/relations-functions-connect-four/index.html",
              "thumb": "thumbs/relations-functions-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice relations and functions problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Relations and Functions Tic-Tac-Toe",
              "path": "artifacts/relations-functions-tic-tac-toe/index.html",
              "thumb": "thumbs/relations-functions-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice relations and functions problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Relations and Functions: Picture Reveal",
              "path": "artifacts/relations-functions-picture-reveal/index.html",
              "thumb": "thumbs/relations-functions-picture-reveal.jpg",
              "description": "Solve 10 relations and functions problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Function Machine Factory",
              "path": "artifacts/relations-functions-function-machine-factory/index.html",
              "thumb": "thumbs/function-machine-factory.jpg",
              "description": "Build function machines by arranging operation gears to match input-output tables, then work backward to find missing inputs. Ten levels progress from one-step rules to two-step machines.",
              "type": "Game",
              "bankFormat": "topic-games",
              "unitSpecific": true,
              "topics": [
                "Input-output tables",
                "Function rules",
                "Evaluating functions",
                "Inverse operations"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "The Arcade Token Heist",
              "path": "artifacts/relations-functions-arcade-token-heist/index.html",
              "thumb": "thumbs/relations-functions-arcade-token-heist.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Escape the Function Factory",
              "path": "artifacts/relations-functions-escape-room/index.html",
              "thumb": "thumbs/relations-functions-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with a function machine, a cipher with a hidden shift, a function-or-not sorting belt, a step-ordering lock and dials, a 10-minute timer, hints that cost time, and a final password. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Relations and Functions Cheat Sheet",
              "path": "artifacts/relations-functions-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/relations-functions-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: relations, functions, domain and range, and function notation. Back: rate of change, linear vs. nonlinear, sequences and reading graphs. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Relations and Functions",
                "Unit 4"
              ],
              "added": "2026-10-25"
            }
          ]
        },
        {
          "id": "linear-equations-slope",
          "name": "Linear Functions and Graphing",
          "artifacts": [
            {
              "title": "Linear Functions and Graphing Matching Game",
              "path": "worksheet-generator/match-game.html#unit=algebra1-linear-equations-slope",
              "thumb": "thumbs/matching-game-linear-equations-slope.svg",
              "description": "Interactive card sort: drag each graph, equation, table and description into the set it belongs to. Zoom in on any card (read coordinates on the big graph), check your sets, and get hints. CP2/CP1/Honors; uses the same verified cards as the printable Matching Card Sort.",
              "type": "Game",
              "topics": [
                "Matching game",
                "Linear Functions and Graphing",
                "Unit 5"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-linear-equations-slope",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-linear-equations-slope",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Linear Functions and Graphing",
                "Unit 5"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-linear-equations-slope",
              "thumb": "thumbs/worksheet-generator-linear-equations-slope.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Linear functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-linear-equations-slope",
              "thumb": "thumbs/menu-assessment-generator-linear-equations-slope.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Linear functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=maze",
              "thumb": "thumbs/maze-generator-linear-equations-slope.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=color",
              "thumb": "thumbs/color-generator-linear-equations-slope.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-linear-equations-slope.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=error",
              "thumb": "thumbs/error-generator-linear-equations-slope.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=partner",
              "thumb": "thumbs/partner-generator-linear-equations-slope.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=who",
              "thumb": "thumbs/who-generator-linear-equations-slope.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=stations",
              "thumb": "thumbs/stations-generator-linear-equations-slope.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Slope Links Mini Golf",
              "path": "artifacts/slope-links-mini-golf/index.html",
              "thumb": "thumbs/slope-links-mini-golf.jpg",
              "description": "Enter a slope, pick a direction and a club, and hit. The ball follows a line through its starting point, and you only see where it went after the shot. Six holes with walls, sand, and water.",
              "type": "Game",
              "bankFormat": "topic-games",
              "unitSpecific": true,
              "topics": [
                "Slope",
                "Rise over run",
                "Coordinate plane"
              ],
              "added": "2026-10-16"
            },
            {
              "title": "The Summit Sabotage",
              "path": "artifacts/linear-equations-slope-summit-sabotage/index.html",
              "thumb": "thumbs/linear-equations-slope-summit-sabotage.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Slope-intercept form",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Avalanche Patrol: Race to the Lodge",
              "path": "artifacts/linear-equations-slope-escape-room/index.html",
              "thumb": "thumbs/linear-equations-slope-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Slope from points, tables, and graphs",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Linear Functions and Graphing Cheat Sheet",
              "path": "artifacts/linear-equations-slope-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/linear-equations-slope-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: slope, rate of change, slope-intercept form and graphing lines. Back: writing equations of lines, intercepts, parallel and perpendicular lines. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Linear Functions and Graphing",
                "Unit 5"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Linear Functions Flashcards",
              "path": "artifacts/linear-functions-flashcards/index.html",
              "thumb": "thumbs/linear-functions-flashcards.jpg",
              "description": "A fresh deck of linear functions flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Slope",
                "Linear equations",
                "Parallel and perpendicular lines",
                "Linear models"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Linear Functions Showdown",
              "path": "artifacts/linear-functions-showdown/index.html",
              "thumb": "thumbs/linear-functions-showdown.jpg",
              "description": "A game board for linear functions review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Slope",
                "Linear equations",
                "Parallel and perpendicular lines",
                "Linear models",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Linear Functions Connect Four",
              "path": "artifacts/linear-functions-connect-four/index.html",
              "thumb": "thumbs/linear-functions-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice linear functions problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Slope",
                "Linear equations",
                "Parallel and perpendicular lines",
                "Linear models",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Linear Functions Tic-Tac-Toe",
              "path": "artifacts/linear-functions-tic-tac-toe/index.html",
              "thumb": "thumbs/linear-functions-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice linear functions problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Slope",
                "Linear equations",
                "Parallel and perpendicular lines",
                "Linear models",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Linear Functions: Picture Reveal",
              "path": "artifacts/linear-functions-picture-reveal/index.html",
              "thumb": "thumbs/linear-functions-picture-reveal.jpg",
              "description": "Solve 10 linear functions problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Slope",
                "Linear equations",
                "Parallel and perpendicular lines",
                "Linear models"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "systems-of-equations",
          "name": "Systems of Equations and Inequalities",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-systems-of-equations",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-systems-of-equations",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Systems of Equations and Inequalities",
                "Unit 6"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-systems-of-equations",
              "thumb": "thumbs/worksheet-generator-systems-of-equations.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Systems of equations"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-systems-of-equations",
              "thumb": "thumbs/menu-assessment-generator-systems-of-equations.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Systems of equations"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=maze",
              "thumb": "thumbs/maze-generator-systems-of-equations.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=color",
              "thumb": "thumbs/color-generator-systems-of-equations.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-systems-of-equations.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=error",
              "thumb": "thumbs/error-generator-systems-of-equations.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=partner",
              "thumb": "thumbs/partner-generator-systems-of-equations.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=who",
              "thumb": "thumbs/who-generator-systems-of-equations.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=stations",
              "thumb": "thumbs/stations-generator-systems-of-equations.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "The Space Station Swindle",
              "path": "artifacts/systems-of-equations-space-station-swindle/index.html",
              "thumb": "thumbs/systems-of-equations-space-station-swindle.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Solving systems",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Locked In: Night at the Museum",
              "path": "artifacts/systems-of-equations-escape-room/index.html",
              "thumb": "thumbs/systems-of-equations-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Checking and graphing solutions",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Systems of Equations Cheat Sheet",
              "path": "artifacts/systems-of-equations-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/systems-of-equations-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: solving systems by graphing, substitution and elimination. Back: special systems, choosing a method and word problems. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Systems of Equations",
                "Unit 6"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Zombie Fence",
              "path": "artifacts/zombie-fence/index.html",
              "thumb": "thumbs/zombie-fence.jpg",
              "description": "Build fences from inequalities in slope-intercept form. Keep every survivor in the safe zone and every zombie out, using solid and dashed lines and, on later nights, two inequalities at once.",
              "type": "Game",
              "bankFormat": "topic-games",
              "unitSpecific": true,
              "topics": [
                "Graphing inequalities",
                "Slope-intercept form",
                "Systems of inequalities"
              ],
              "added": "2026-10-16"
            },
            {
              "title": "Aquarium After Hours",
              "path": "artifacts/graphing-inequalities-aquarium-after-hours/index.html",
              "thumb": "thumbs/graphing-inequalities-aquarium-after-hours.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Graphing linear inequalities",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Treasure Island: The Feasible Region",
              "path": "artifacts/graphing-inequalities-escape-room/index.html",
              "thumb": "thumbs/graphing-inequalities-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Solid and dashed boundary lines",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Systems of Inequalities Cheat Sheet",
              "path": "artifacts/graphing-inequalities-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/graphing-inequalities-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: graphing linear inequalities in two variables. Back: systems of inequalities and feasible regions. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Graphing Linear Inequalities",
                "Unit 6"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Systems of Equations Flashcards",
              "path": "artifacts/systems-flashcards/index.html",
              "thumb": "thumbs/systems-flashcards.jpg",
              "description": "A fresh deck of systems of equations flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Systems of equations",
                "Substitution",
                "Elimination",
                "Systems of inequalities"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Systems of Equations Showdown",
              "path": "artifacts/systems-showdown/index.html",
              "thumb": "thumbs/systems-showdown.jpg",
              "description": "A game board for systems of equations review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Systems of equations",
                "Substitution",
                "Elimination",
                "Systems of inequalities",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Systems of Equations Connect Four",
              "path": "artifacts/systems-connect-four/index.html",
              "thumb": "thumbs/systems-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice systems of equations problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Systems of equations",
                "Substitution",
                "Elimination",
                "Systems of inequalities",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Systems of Equations Tic-Tac-Toe",
              "path": "artifacts/systems-tic-tac-toe/index.html",
              "thumb": "thumbs/systems-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice systems of equations problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Systems of equations",
                "Substitution",
                "Elimination",
                "Systems of inequalities",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Systems of Equations: Picture Reveal",
              "path": "artifacts/systems-picture-reveal/index.html",
              "thumb": "thumbs/systems-picture-reveal.jpg",
              "description": "Solve 10 systems of equations problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Systems of equations",
                "Substitution",
                "Elimination",
                "Systems of inequalities"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "exponents-exponential-functions",
          "name": "Exponents and Scientific Notation",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-exponents-scientific-notation",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-exponents-scientific-notation",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Exponents and Scientific Notation",
                "Unit 7"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-exponents-scientific-notation",
              "thumb": "thumbs/worksheet-generator-exponents-scientific-notation.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-exponents-scientific-notation",
              "thumb": "thumbs/menu-assessment-generator-exponents-scientific-notation.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=maze",
              "thumb": "thumbs/maze-generator-exponents-scientific-notation.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=color",
              "thumb": "thumbs/color-generator-exponents-scientific-notation.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-exponents-scientific-notation.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=error",
              "thumb": "thumbs/error-generator-exponents-scientific-notation.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=partner",
              "thumb": "thumbs/partner-generator-exponents-scientific-notation.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=who",
              "thumb": "thumbs/who-generator-exponents-scientific-notation.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=stations",
              "thumb": "thumbs/stations-generator-exponents-scientific-notation.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Exponents Flashcards",
              "path": "artifacts/exponents-flashcards/index.html",
              "thumb": "thumbs/exponents-flashcards.jpg",
              "description": "A fresh deck of exponents flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Exponent rules",
                "Negative exponents",
                "Scientific notation"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponents Showdown",
              "path": "artifacts/exponents-showdown/index.html",
              "thumb": "thumbs/exponents-showdown.jpg",
              "description": "A game board for exponents review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Negative exponents",
                "Scientific notation",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponents Connect Four",
              "path": "artifacts/exponents-connect-four/index.html",
              "thumb": "thumbs/exponents-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice exponents problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Negative exponents",
                "Scientific notation",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponents Tic-Tac-Toe",
              "path": "artifacts/exponents-tic-tac-toe/index.html",
              "thumb": "thumbs/exponents-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice exponents problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Negative exponents",
                "Scientific notation",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponents: Picture Reveal",
              "path": "artifacts/exponents-picture-reveal/index.html",
              "thumb": "thumbs/exponents-picture-reveal.jpg",
              "description": "Solve 10 exponents problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Negative exponents",
                "Scientific notation"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "The Planetarium Power Outage",
              "path": "artifacts/exponents-scientific-notation-planetarium-power-outage/index.html",
              "thumb": "thumbs/exponents-scientific-notation-planetarium-power-outage.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Zero and negative exponents",
                "Scientific notation",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Escape the Rocket Lab",
              "path": "artifacts/exponents-scientific-notation-escape-room/index.html",
              "thumb": "thumbs/exponents-scientific-notation-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with fuel gauges, a cipher with a hidden shift, a true-or-false airlock, a step-ordering lock and dials, a 10-minute timer, hints that cost time, and a final password. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Zero and negative exponents",
                "Scientific notation",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Exponents and Scientific Notation Cheat Sheet",
              "path": "artifacts/exponents-scientific-notation-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/exponents-scientific-notation-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: exponent rules, zero and negative exponents, and evaluating powers. Back: scientific notation and operations with it. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Exponents and Scientific Notation",
                "Unit 7"
              ],
              "added": "2026-10-25"
            }
          ]
        },
        {
          "id": "exponential-functions",
          "name": "Exponential Functions",
          "artifacts": [
            {
              "title": "Outbreak Simulator",
              "path": "artifacts/exponential-functions-outbreak-simulator/index.html",
              "thumb": "thumbs/exponential-functions-outbreak-simulator.jpg",
              "description": "Use exponential growth and decay models to project cases, find initial amounts and growth factors, and solve for time across ten simulation levels.",
              "type": "Game",
              "bankFormat": "topic-games",
              "unitSpecific": true,
              "topics": [
                "Exponential growth",
                "Exponential decay",
                "Initial value and growth factor",
                "Solving exponential models"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "Exponential Functions Matching Game",
              "path": "worksheet-generator/match-game.html#unit=algebra1-exponential-functions",
              "thumb": "thumbs/matching-game-exponential-functions.svg",
              "description": "Interactive card sort: drag each graph, equation, table and description into the set it belongs to. Zoom in on any card (read coordinates on the big graph), check your sets, and get hints. CP2/CP1/Honors; uses the same verified cards as the printable Matching Card Sort.",
              "type": "Game",
              "topics": [
                "Matching game",
                "Exponential Functions",
                "Unit 8"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-exponential-functions",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-exponential-functions",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Exponential Functions",
                "Unit 8"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-exponential-functions",
              "thumb": "thumbs/worksheet-generator-exponential-functions.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Exponential functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-exponential-functions",
              "thumb": "thumbs/menu-assessment-generator-exponential-functions.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Exponential functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=maze",
              "thumb": "thumbs/maze-generator-exponential-functions.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=color",
              "thumb": "thumbs/color-generator-exponential-functions.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-exponential-functions.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=error",
              "thumb": "thumbs/error-generator-exponential-functions.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=partner",
              "thumb": "thumbs/partner-generator-exponential-functions.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=who",
              "thumb": "thumbs/who-generator-exponential-functions.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=stations",
              "thumb": "thumbs/stations-generator-exponential-functions.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "The Great Pumpkin Snatch",
              "path": "artifacts/exponents-exponential-functions-great-pumpkin-snatch/index.html",
              "thumb": "thumbs/exponents-exponential-functions-great-pumpkin-snatch.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Detective game",
                "Typed answers",
                "Units 7–8"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Dr. Petri’s Growth Lab",
              "path": "artifacts/exponents-exponential-functions-escape-room/index.html",
              "thumb": "thumbs/exponents-exponential-functions-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Escape room",
                "Teamwork",
                "Units 7–8"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Exponential Functions Cheat Sheet",
              "path": "artifacts/exponents-exponential-functions-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/exponents-exponential-functions-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: exponential functions, growth and decay. Back: writing models, compound interest, geometric sequences and solving equations. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Exponential Functions",
                "Unit 8"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Exponential Functions Flashcards",
              "path": "artifacts/exponential-functions-flashcards/index.html",
              "thumb": "thumbs/exponential-functions-flashcards.jpg",
              "description": "A fresh deck of exponential functions flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Exponential growth and decay",
                "Exponential equations",
                "Geometric sequences",
                "Linear vs. exponential"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponential Functions Showdown",
              "path": "artifacts/exponential-functions-showdown/index.html",
              "thumb": "thumbs/exponential-functions-showdown.jpg",
              "description": "A game board for exponential functions review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Exponential growth and decay",
                "Exponential equations",
                "Geometric sequences",
                "Linear vs. exponential",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponential Functions Connect Four",
              "path": "artifacts/exponential-functions-connect-four/index.html",
              "thumb": "thumbs/exponential-functions-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice exponential functions problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Exponential growth and decay",
                "Exponential equations",
                "Geometric sequences",
                "Linear vs. exponential",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponential Functions Tic-Tac-Toe",
              "path": "artifacts/exponential-functions-tic-tac-toe/index.html",
              "thumb": "thumbs/exponential-functions-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice exponential functions problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Exponential growth and decay",
                "Exponential equations",
                "Geometric sequences",
                "Linear vs. exponential",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponential Functions: Picture Reveal",
              "path": "artifacts/exponential-functions-picture-reveal/index.html",
              "thumb": "thumbs/exponential-functions-picture-reveal.jpg",
              "description": "Solve 10 exponential functions problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Exponential growth and decay",
                "Exponential equations",
                "Geometric sequences",
                "Linear vs. exponential"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "polynomials-factoring",
          "name": "Polynomials",
          "artifacts": [
            {
              "title": "Polynomial Garden Planner",
              "path": "artifacts/polynomials-garden-planner/index.html",
              "thumb": "thumbs/polynomials-garden-planner.jpg",
              "description": "Arrange algebra tiles to multiply polynomials, find missing factors from area models, and calculate garden perimeters across ten levels.",
              "type": "Game",
              "bankFormat": "topic-games",
              "unitSpecific": true,
              "topics": [
                "Multiplying polynomials",
                "Factoring polynomials",
                "Area models",
                "Polynomial perimeter"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-polynomials",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-polynomials",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Polynomials",
                "Unit 9"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-polynomials",
              "thumb": "thumbs/worksheet-generator-polynomials.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Polynomials"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-polynomials",
              "thumb": "thumbs/menu-assessment-generator-polynomials.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Polynomials"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=maze",
              "thumb": "thumbs/maze-generator-polynomials.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=color",
              "thumb": "thumbs/color-generator-polynomials.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-polynomials.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=error",
              "thumb": "thumbs/error-generator-polynomials.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=partner",
              "thumb": "thumbs/partner-generator-polynomials.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=who",
              "thumb": "thumbs/who-generator-polynomials.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=stations",
              "thumb": "thumbs/stations-generator-polynomials.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Polynomials Flashcards",
              "path": "artifacts/polynomials-flashcards/index.html",
              "thumb": "thumbs/polynomials-flashcards.jpg",
              "description": "A fresh deck of polynomials flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Polynomials Showdown",
              "path": "artifacts/polynomials-showdown/index.html",
              "thumb": "thumbs/polynomials-showdown.jpg",
              "description": "A game board for polynomials review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Polynomials Connect Four",
              "path": "artifacts/polynomials-connect-four/index.html",
              "thumb": "thumbs/polynomials-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice polynomials problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Polynomials Tic-Tac-Toe",
              "path": "artifacts/polynomials-tic-tac-toe/index.html",
              "thumb": "thumbs/polynomials-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice polynomials problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Polynomials: Picture Reveal",
              "path": "artifacts/polynomials-picture-reveal/index.html",
              "thumb": "thumbs/polynomials-picture-reveal.jpg",
              "description": "Solve 10 polynomials problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "The Toy Factory Takedown",
              "path": "artifacts/polynomials-toy-factory-takedown/index.html",
              "thumb": "thumbs/polynomials-toy-factory-takedown.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Classifying polynomials",
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Escape the Toy Workshop",
              "path": "artifacts/polynomials-escape-room/index.html",
              "thumb": "thumbs/polynomials-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with a block machine, a cipher with a hidden shift, monomial-binomial-trinomial sorting bins, a step-ordering lock and dials, a 10-minute timer, hints that cost time, and a final password. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Classifying polynomials",
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Polynomials Cheat Sheet",
              "path": "artifacts/polynomials-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/polynomials-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: vocabulary, classifying, adding and subtracting polynomials. Back: multiplying, special products and dividing by a monomial. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Polynomials",
                "Unit 9"
              ],
              "added": "2026-10-25"
            }
          ]
        },
        {
          "id": "factoring-zero-product",
          "name": "Factoring and Zero Product Property",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-factoring-zero-product",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-factoring-zero-product",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Factoring and Zero Product Property",
                "Unit 10"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-factoring-zero-product",
              "thumb": "thumbs/worksheet-generator-factoring-zero-product.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Factoring"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-factoring-zero-product",
              "thumb": "thumbs/menu-assessment-generator-factoring-zero-product.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Factoring"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=maze",
              "thumb": "thumbs/maze-generator-factoring-zero-product.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=color",
              "thumb": "thumbs/color-generator-factoring-zero-product.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-factoring-zero-product.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=error",
              "thumb": "thumbs/error-generator-factoring-zero-product.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=partner",
              "thumb": "thumbs/partner-generator-factoring-zero-product.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=who",
              "thumb": "thumbs/who-generator-factoring-zero-product.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=stations",
              "thumb": "thumbs/stations-generator-factoring-zero-product.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "The Castle Crown Caper",
              "path": "artifacts/polynomials-factoring-castle-crown-caper/index.html",
              "thumb": "thumbs/polynomials-factoring-castle-crown-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Factoring",
                "Detective game",
                "Typed answers",
                "Units 9–10"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "The Wizard’s Spell Library",
              "path": "artifacts/polynomials-factoring-escape-room/index.html",
              "thumb": "thumbs/polynomials-factoring-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Adding, subtracting and multiplying polynomials",
                "Escape room",
                "Teamwork",
                "Units 9–10"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Factoring and Zero Product Cheat Sheet",
              "path": "artifacts/polynomials-factoring-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/polynomials-factoring-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: factoring GCF, trinomials, special patterns and grouping. Back: factoring completely and solving quadratics with the Zero Product Property. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Factoring and Zero Product",
                "Unit 10"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Factoring Flashcards",
              "path": "artifacts/factoring-zero-product-flashcards/index.html",
              "thumb": "thumbs/factoring-zero-product-flashcards.jpg",
              "description": "A fresh deck of factoring flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "GCF and grouping",
                "Factoring trinomials",
                "Special products",
                "Zero product property"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Factoring Showdown",
              "path": "artifacts/factoring-zero-product-showdown/index.html",
              "thumb": "thumbs/factoring-zero-product-showdown.jpg",
              "description": "A game board for factoring review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "GCF and grouping",
                "Factoring trinomials",
                "Special products",
                "Zero product property",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Factoring Connect Four",
              "path": "artifacts/factoring-zero-product-connect-four/index.html",
              "thumb": "thumbs/factoring-zero-product-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice factoring problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "GCF and grouping",
                "Factoring trinomials",
                "Special products",
                "Zero product property",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Factoring Tic-Tac-Toe",
              "path": "artifacts/factoring-zero-product-tic-tac-toe/index.html",
              "thumb": "thumbs/factoring-zero-product-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice factoring problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "GCF and grouping",
                "Factoring trinomials",
                "Special products",
                "Zero product property",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Factoring: Picture Reveal",
              "path": "artifacts/factoring-zero-product-picture-reveal/index.html",
              "thumb": "thumbs/factoring-zero-product-picture-reveal.jpg",
              "description": "Solve 10 factoring problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "GCF and grouping",
                "Factoring trinomials",
                "Special products",
                "Zero product property"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "quadratics",
          "name": "Quadratic Functions and Equations",
          "artifacts": [
            {
              "title": "Quadratic Functions and Equations Matching Game",
              "path": "worksheet-generator/match-game.html#unit=algebra1-quadratics",
              "thumb": "thumbs/matching-game-quadratics.svg",
              "description": "Interactive card sort: drag each graph, equation, table and description into the set it belongs to. Zoom in on any card (read coordinates on the big graph), check your sets, and get hints. CP2/CP1/Honors; uses the same verified cards as the printable Matching Card Sort.",
              "type": "Game",
              "topics": [
                "Matching game",
                "Quadratic Functions and Equations",
                "Unit 11"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-quadratics",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-quadratics",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Quadratic Functions and Equations",
                "Unit 11"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-quadratics",
              "thumb": "thumbs/worksheet-generator-quadratics.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Quadratics"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-quadratics",
              "thumb": "thumbs/menu-assessment-generator-quadratics.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Quadratics"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=maze",
              "thumb": "thumbs/maze-generator-quadratics.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=color",
              "thumb": "thumbs/color-generator-quadratics.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-quadratics.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=error",
              "thumb": "thumbs/error-generator-quadratics.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=partner",
              "thumb": "thumbs/partner-generator-quadratics.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=who",
              "thumb": "thumbs/who-generator-quadratics.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=stations",
              "thumb": "thumbs/stations-generator-quadratics.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "The Cannonball Circus Caper",
              "path": "artifacts/quadratics-cannonball-circus-caper/index.html",
              "thumb": "thumbs/quadratics-cannonball-circus-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Solving quadratics",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Thunder Bolt: Launch Gone Wrong",
              "path": "artifacts/quadratics-escape-room/index.html",
              "thumb": "thumbs/quadratics-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Solving quadratic equations",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Quadratic Functions Cheat Sheet",
              "path": "artifacts/quadratics-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/quadratics-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: graphing quadratic functions and their key features. Back: solving quadratic equations: factoring, square roots, completing the square and the formula. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Quadratic Functions",
                "Unit 11"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Quadratics Flashcards",
              "path": "artifacts/quadratic-practice-flashcards/index.html",
              "thumb": "thumbs/quadratic-practice-flashcards.jpg",
              "description": "A fresh deck of quadratics flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Parabolas",
                "Quadratic formula",
                "Completing the square",
                "Projectile motion"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Quadratics Showdown",
              "path": "artifacts/quadratic-practice-showdown/index.html",
              "thumb": "thumbs/quadratic-practice-showdown.jpg",
              "description": "A game board for quadratics review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Parabolas",
                "Quadratic formula",
                "Completing the square",
                "Projectile motion",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Quadratics Connect Four",
              "path": "artifacts/quadratic-practice-connect-four/index.html",
              "thumb": "thumbs/quadratic-practice-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice quadratics problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Parabolas",
                "Quadratic formula",
                "Completing the square",
                "Projectile motion",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Quadratics Tic-Tac-Toe",
              "path": "artifacts/quadratic-practice-tic-tac-toe/index.html",
              "thumb": "thumbs/quadratic-practice-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice quadratics problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Parabolas",
                "Quadratic formula",
                "Completing the square",
                "Projectile motion",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Quadratics: Picture Reveal",
              "path": "artifacts/quadratic-practice-picture-reveal/index.html",
              "thumb": "thumbs/quadratic-practice-picture-reveal.jpg",
              "description": "Solve 10 quadratics problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Parabolas",
                "Quadratic formula",
                "Completing the square",
                "Projectile motion"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "statistics-data-modeling",
          "name": "Statistics and Data Modeling",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-statistics-data-modeling",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-statistics-data-modeling",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Statistics and Data Modeling",
                "Unit 12"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-statistics-data-modeling",
              "thumb": "thumbs/worksheet-generator-statistics-data-modeling.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Statistics"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-statistics-data-modeling",
              "thumb": "thumbs/menu-assessment-generator-statistics-data-modeling.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Statistics"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-statistics-data-modeling&kind=maze",
              "thumb": "thumbs/maze-generator-statistics-data-modeling.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Statistics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-statistics-data-modeling&kind=color",
              "thumb": "thumbs/color-generator-statistics-data-modeling.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Statistics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-statistics-data-modeling&kind=error",
              "thumb": "thumbs/error-generator-statistics-data-modeling.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Statistics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-statistics-data-modeling&kind=partner",
              "thumb": "thumbs/partner-generator-statistics-data-modeling.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Statistics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-statistics-data-modeling&kind=who",
              "thumb": "thumbs/who-generator-statistics-data-modeling.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Statistics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-statistics-data-modeling&kind=stations",
              "thumb": "thumbs/stations-generator-statistics-data-modeling.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Statistics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Statistics Flashcards",
              "path": "artifacts/statistics-data-modeling-flashcards/index.html",
              "thumb": "thumbs/statistics-data-modeling-flashcards.jpg",
              "description": "A fresh deck of statistics flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Measures of center and spread",
                "Box plots",
                "Two-way tables",
                "Scatter plots and lines of fit"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Statistics Showdown",
              "path": "artifacts/statistics-data-modeling-showdown/index.html",
              "thumb": "thumbs/statistics-data-modeling-showdown.jpg",
              "description": "A game board for statistics review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Measures of center and spread",
                "Box plots",
                "Two-way tables",
                "Scatter plots and lines of fit",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Statistics Connect Four",
              "path": "artifacts/statistics-data-modeling-connect-four/index.html",
              "thumb": "thumbs/statistics-data-modeling-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice statistics problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Measures of center and spread",
                "Box plots",
                "Two-way tables",
                "Scatter plots and lines of fit",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Statistics Tic-Tac-Toe",
              "path": "artifacts/statistics-data-modeling-tic-tac-toe/index.html",
              "thumb": "thumbs/statistics-data-modeling-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice statistics problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Measures of center and spread",
                "Box plots",
                "Two-way tables",
                "Scatter plots and lines of fit",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Statistics: Picture Reveal",
              "path": "artifacts/statistics-data-modeling-picture-reveal/index.html",
              "thumb": "thumbs/statistics-data-modeling-picture-reveal.jpg",
              "description": "Solve 10 statistics problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Measures of center and spread",
                "Box plots",
                "Two-way tables",
                "Scatter plots and lines of fit"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "The Stadium Scoreboard Scandal",
              "path": "artifacts/statistics-data-modeling-stadium-scoreboard-scandal/index.html",
              "thumb": "thumbs/statistics-data-modeling-stadium-scoreboard-scandal.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Measures of center and spread",
                "Box plots and outliers",
                "Two-way tables",
                "Lines of fit and residuals",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Escape the Stats Lab",
              "path": "artifacts/statistics-data-modeling-escape-room/index.html",
              "thumb": "thumbs/statistics-data-modeling-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with a data wall, a cipher with a hidden shift, a correlation sorting room, a step-ordering lock and dials, a 10-minute timer, hints that cost time, and a final password. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Measures of center and spread",
                "Box plots and outliers",
                "Two-way tables",
                "Lines of fit and residuals",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Statistics and Data Modeling Cheat Sheet",
              "path": "artifacts/statistics-data-modeling-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/statistics-data-modeling-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: center, spread, box plots and outliers. Back: two-way tables, scatter plots, lines of fit and residuals. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Statistics and Data Modeling",
                "Unit 12"
              ],
              "added": "2026-10-25"
            }
          ]
        }
      ]
    },
    {
      "id": "algebra2",
      "name": "Algebra 2",
      "color": "purple",
      "art": "curve",
      "blurb": "Functions, polynomials, logarithms, and beyond.",
      "units": [
        {
          "id": "functions-transformations",
          "name": "Functions & Transformations",
          "artifacts": [
            {
              "title": "Functions & Transformations Matching Game",
              "path": "worksheet-generator/match-game.html#unit=algebra2-functions-transformations",
              "thumb": "thumbs/matching-game-algebra2-functions-transformations.svg",
              "description": "Interactive card sort: drag each graph, equation, table and description into the set it belongs to. Zoom in on any card (read coordinates on the big graph), check your sets, and get hints. CP2/CP1/Honors; uses the same verified cards as the printable Matching Card Sort.",
              "type": "Game",
              "topics": [
                "Matching game",
                "Functions & Transformations",
                "Algebra 2"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "The Function Bistro: Assessment Menu",
              "path": "artifacts/functions-transformations-assessment-menu/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-assessment-menu.jpg",
              "description": "Choice-based test: students order 4 Appetizers, 4 Entrées and 2 Chef’s Specials worth 5, 10 and 20 points, covering all four skill groups, with printed grids for graphing dishes. 100 points total. Includes a teacher guide, rubrics and answer key with computed graphs.",
              "type": "Printable",
              "topics": [
                "Function notation",
                "Transformations",
                "Composition and inverses",
                "Choice menu"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Color By Number",
              "path": "artifacts/functions-transformations-color-by-number/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-color-by-number.jpg",
              "description": "Printable 2-page color-by-number: solve 10 problems on function notation, domain, transformations, piecewise functions, composition and inverses, match each answer to the color code, then color the lighthouse on the island. Page 1 is the picture, page 2 is the work space.",
              "type": "Printable",
              "topics": [
                "Function notation",
                "Transformations",
                "Composition & inverses",
                "Color by number"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Cheat Sheet",
              "path": "artifacts/functions-transformations-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: function notation, domain and range, parent functions and transformations. Back: operations, composition, piecewise functions and inverses. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Functions & Transformations",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Functions Four",
              "path": "artifacts/functions-transformations-connect-four/index.html",
              "thumb": "thumbs/functions-transformations-connect-four.jpg",
              "description": "Connect Four for two teams. Evaluate functions, find domain and range, match equations to graphs, transform parent functions, compose and invert, and model with piecewise functions. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Function notation, domain and range",
                "Parent functions and transformations",
                "Piecewise functions and composition",
                "Inverse functions"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Error Analysis",
              "path": "artifacts/functions-transformations-error-analysis/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-error-analysis.jpg",
              "description": "Find the mistake in 10 worked solutions on function notation, domain, horizontal shifts, reflections, stretches, composition order, inverses and piecewise graphs. Five items include computed correct-versus-student graphs. Explain the error and show the correct work.",
              "type": "Printable",
              "topics": [
                "Transformations",
                "Function notation",
                "Composition",
                "Inverse functions"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Picture Reveal",
              "path": "artifacts/functions-transformations-picture-reveal/index.html",
              "thumb": "thumbs/functions-transformations-picture-reveal.jpg",
              "description": "Evaluate functions, find domains, read transformed and piecewise graphs, compose and invert functions to uncover a hidden lighthouse scene. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Transformations",
                "Domain",
                "Composition",
                "Piecewise graphs"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Mirror Maze Mayhem",
              "path": "artifacts/functions-transformations-escape-room/index.html",
              "thumb": "thumbs/functions-transformations-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with a cipher, graph-reading locks, a combination-safe dial puzzle, a logic order lock, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Transformations of graphs",
                "Composition and inverse functions",
                "Domain and range",
                "Escape room"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Flashcards",
              "path": "artifacts/functions-transformations-flashcards/index.html",
              "thumb": "thumbs/functions-transformations-flashcards.jpg",
              "description": "25 flashcards with worked solutions and computed graphs for function notation, domain and range, parent functions and symmetry, transformations of graphs, piecewise functions, composition, and inverse functions. Mark cards you need to practice and review them again. Filter by skill and by level (Easy, Medium or Hard).",
              "type": "Practice",
              "topics": [
                "Function notation and domain",
                "Parent functions and transformations",
                "Piecewise functions and composition",
                "Inverse functions"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Showdown",
              "path": "artifacts/functions-transformations-jeopardy/index.html",
              "thumb": "thumbs/functions-transformations-jeopardy.jpg",
              "description": "A game board for Functions & Transformations. Evaluate functions and find domains, describe and write transformations from graphs, then finish with piecewise functions, composites, and inverses.",
              "type": "Game",
              "topics": [
                "Function notation and domain",
                "Transformations of graphs",
                "Piecewise functions and composition",
                "Inverse functions"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Maze",
              "path": "artifacts/functions-transformations-maze/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-maze.jpg",
              "description": "Printable 4-page worksheet: evaluate functions, find domain and range, apply transformations, compose and invert functions to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Function notation, domain and range",
                "Transformations of graphs",
                "Composition and inverse functions",
                "Piecewise and transformed equations"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Stations",
              "path": "artifacts/algebra2-functions-transformations-stations/worksheet.pdf",
              "thumb": "thumbs/algebra2-functions-transformations-stations.svg",
              "description": "Printable Algebra 2 station work for Functions & Transformations. Students rotate through four problem sets to practice and review unit skills, with a teacher answer key.",
              "type": "Printable",
              "topics": [
                "Stations",
                "Station work",
                "Functions & Transformations"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Tarsia Puzzle",
              "path": "artifacts/functions-transformations-tarsia/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-tarsia.jpg",
              "description": "Printable tarsia puzzle: cut out 24 triangles and match 30 problems to their answers to rebuild a hexagon. Covers function notation, piecewise functions, composition, inverse functions, domain and range, and transformations of parent graphs. Includes a show-your-work page and a teacher key with the solved hexagon.",
              "type": "Printable",
              "topics": [
                "Composition and inverses",
                "Domain and range",
                "Transformations of graphs",
                "Tarsia puzzle"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Vanishing Violin Caper",
              "path": "artifacts/functions-transformations-vanishing-violin-caper/index.html",
              "thumb": "thumbs/functions-transformations-vanishing-violin-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers, with buttons for exponents, absolute value, intervals and function composition.",
              "type": "Game",
              "topics": [
                "Functions & transformations",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Tic-Tac-Toe",
              "path": "artifacts/functions-transformations-tic-tac-toe/index.html",
              "thumb": "thumbs/functions-transformations-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice problem to claim a square. A wrong answer lets the other team steal. Optional timer.",
              "type": "Game",
              "topics": [
                "Functions & transformations",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Vanishing Violin Caper (Printable)",
              "path": "artifacts/functions-transformations-whodunnit/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-whodunnit.jpg",
              "description": "Printable whodunnit: 10 clue cards to post around the room, each a multiple-choice problem where every answer leads to a clue. Includes a story and case board, a show-your-work page, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Functions & transformations",
                "Whodunnit",
                "Multiple choice",
                "Self-checking"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Partner Check 1: Function Operations & Evaluation",
              "path": "artifacts/algebra2-functions-transformations-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-functions-transformations-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Function Operations & Evaluation"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Transformations of Functions",
              "path": "artifacts/algebra2-functions-transformations-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-functions-transformations-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Transformations of Functions"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "linear-functions-systems",
          "name": "Linear Functions & Systems",
          "artifacts": [
            {
              "title": "Linear Functions & Systems Matching Game",
              "path": "worksheet-generator/match-game.html#unit=algebra2-linear-functions-systems",
              "thumb": "thumbs/matching-game-algebra2-linear-functions-systems.svg",
              "description": "Interactive card sort: drag each graph, equation, table and description into the set it belongs to. Zoom in on any card (read coordinates on the big graph), check your sets, and get hints. CP2/CP1/Honors; uses the same verified cards as the printable Matching Card Sort.",
              "type": "Game",
              "topics": [
                "Matching game",
                "Linear Functions & Systems",
                "Algebra 2"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "The Line Cook Bistro: Assessment Menu",
              "path": "artifacts/linear-functions-systems-assessment-menu/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-assessment-menu.jpg",
              "description": "Choice-based test: students order 4 Appetizers, 4 Entrées and 2 Chef’s Specials worth 5, 10 and 20 points, covering all four skill groups, with printed coordinate grids for graphing dishes. 100 points total. Includes a teacher guide, rubrics and answer key with graphs computed from the equations.",
              "type": "Printable",
              "topics": [
                "Linear equations",
                "Systems of equations",
                "Linear programming",
                "Choice menu"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Color By Number",
              "path": "artifacts/linear-functions-systems-color-by-number/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-color-by-number.jpg",
              "description": "Printable 2-page color-by-number: solve 10 problems on slope, parallel and perpendicular lines, residuals, linear modeling, systems, linear programming and three-variable systems, match each answer to the color code, then color the hot air balloons over the patchwork farms. Page 1 is the picture, page 2 is the work space.",
              "type": "Printable",
              "topics": [
                "Linear modeling",
                "Systems of equations",
                "Linear programming",
                "Color by number"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Cheat Sheet",
              "path": "artifacts/linear-functions-systems-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: slope, forms of a line, parallel and perpendicular lines, and linear models. Back: inequalities, systems, linear programming and three variables. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Linear Functions & Systems",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Crossroads Four",
              "path": "artifacts/linear-functions-systems-connect-four/index.html",
              "thumb": "thumbs/linear-functions-systems-connect-four.jpg",
              "description": "Connect Four for two teams. Find slopes and equations of lines, read graphs and shaded regions, solve systems, fit lines to data, and find the best corner in linear programming. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Slope and equations of lines",
                "Linear inequalities and graphs",
                "Systems of equations and inequalities",
                "Linear programming and best-fit lines"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Error Analysis",
              "path": "artifacts/linear-functions-systems-error-analysis/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-error-analysis.jpg",
              "description": "Find the mistake in 10 worked solutions on point-slope form, perpendicular slopes, linear models, systems, dashed versus solid boundaries, shading, best-fit lines, linear programming and three-variable systems. Seven items include computed student-versus-correct graphs. Explain the error and show the correct work.",
              "type": "Printable",
              "topics": [
                "Linear equations",
                "Systems",
                "Inequalities",
                "Linear programming"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Picture Reveal",
              "path": "artifacts/linear-functions-systems-picture-reveal/index.html",
              "thumb": "thumbs/linear-functions-systems-picture-reveal.jpg",
              "description": "Find rates of change, write and graph linear equations and inequalities, solve systems, read residuals, optimize with linear programming and solve three-variable systems to uncover a hidden alpine gondola scene. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Linear equations",
                "Systems",
                "Linear programming",
                "Residuals"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Blizzard at Summit Lodge",
              "path": "artifacts/linear-functions-systems-escape-room/index.html",
              "thumb": "thumbs/linear-functions-systems-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with a cipher, a scatter-plot trend line, a feasible-region check, a combination-vault dial puzzle (3 by 3 system), a linear programming order lock, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Linear functions",
                "Systems of equations and inequalities",
                "Linear programming",
                "Escape room"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Flashcards",
              "path": "artifacts/linear-functions-systems-flashcards/index.html",
              "thumb": "thumbs/linear-functions-systems-flashcards.jpg",
              "description": "25 flashcards with worked solutions and computed graphs for slope and rate of change, writing linear equations, lines of best fit and residuals, linear and absolute value inequalities, systems of two and three equations, and linear programming. Mark cards you need to practice and review them again. Filter by skill and by level (Easy, Medium or Hard).",
              "type": "Practice",
              "topics": [
                "Slope and writing linear equations",
                "Linear modeling and best fit",
                "Systems of equations and inequalities",
                "Linear programming"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Showdown",
              "path": "artifacts/linear-functions-systems-jeopardy/index.html",
              "thumb": "thumbs/linear-functions-systems-jeopardy.jpg",
              "description": "A game board for Linear Functions & Systems. Write equations and model with lines of best fit, solve systems and inequalities (including graphs of shaded regions), then finish with linear programming and three-variable systems.",
              "type": "Game",
              "topics": [
                "Lines and linear models",
                "Systems and inequalities",
                "Linear programming",
                "Three-variable systems"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Maze",
              "path": "artifacts/linear-functions-systems-maze/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-maze.jpg",
              "description": "Printable 4-page worksheet: write linear equations, use parallel and perpendicular slopes, solve systems of two and three equations, fit a regression line, and optimize with linear programming to find the right door through a maze, recording each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Writing and graphing linear equations",
                "Parallel and perpendicular lines",
                "Systems of equations and inequalities",
                "Linear modeling and linear programming"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Stations",
              "path": "artifacts/algebra2-linear-functions-systems-stations/worksheet.pdf",
              "thumb": "thumbs/algebra2-linear-functions-systems-stations.svg",
              "description": "Printable Algebra 2 station work for Linear Functions & Systems. Students rotate through four problem sets to practice and review unit skills, with a teacher answer key.",
              "type": "Printable",
              "topics": [
                "Stations",
                "Station work",
                "Linear Functions & Systems"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Tarsia Puzzle",
              "path": "artifacts/linear-functions-systems-tarsia/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-tarsia.jpg",
              "description": "Printable tarsia puzzle: cut out 24 triangles and match 30 problems to their answers to rebuild a hexagon. Covers writing equations of lines, parallel and perpendicular lines, linear models and lines of best fit, systems of equations and inequalities, linear programming, and three-variable systems. Includes a show-your-work page (with two graphs) and a teacher key with the solved hexagon.",
              "type": "Printable",
              "topics": [
                "Writing linear equations",
                "Systems of equations",
                "Linear programming",
                "Tarsia puzzle"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Amber Fossil Fiasco",
              "path": "artifacts/linear-functions-systems-amber-fossil-fiasco/index.html",
              "thumb": "thumbs/linear-functions-systems-amber-fossil-fiasco.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type equations of lines in any form, ordered pairs and triples, and inequalities.",
              "type": "Game",
              "topics": [
                "Linear functions & systems",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Tic-Tac-Toe",
              "path": "artifacts/linear-functions-systems-tic-tac-toe/index.html",
              "thumb": "thumbs/linear-functions-systems-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice problem to claim a square. A wrong answer lets the other team steal. Optional timer.",
              "type": "Game",
              "topics": [
                "Linear functions & systems",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Amber Fossil Fiasco (Printable)",
              "path": "artifacts/linear-functions-systems-whodunnit/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-whodunnit.jpg",
              "description": "Printable whodunnit: 10 clue cards to post around the room, each a multiple-choice problem where every answer leads to a clue. Includes a story and case board, a show-your-work page, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Linear functions & systems",
                "Whodunnit",
                "Multiple choice",
                "Self-checking"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Partner Check 1: Linear Equations & Graphs",
              "path": "artifacts/algebra2-linear-functions-systems-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-linear-functions-systems-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Linear Equations & Graphs"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Systems of Equations & Inequalities",
              "path": "artifacts/algebra2-linear-functions-systems-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-linear-functions-systems-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Systems of Equations & Inequalities"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "quadratic-functions-complex-numbers",
          "name": "Quadratic Functions & Complex Numbers",
          "artifacts": [
            {
              "title": "Quadratic Functions & Complex Numbers Matching Game",
              "path": "worksheet-generator/match-game.html#unit=algebra2-quadratic-functions-complex-numbers",
              "thumb": "thumbs/matching-game-algebra2-quadratic-functions-complex-numbers.svg",
              "description": "Interactive card sort: drag each graph, equation, table and description into the set it belongs to. Zoom in on any card (read coordinates on the big graph), check your sets, and get hints. CP2/CP1/Honors; uses the same verified cards as the printable Matching Card Sort.",
              "type": "Game",
              "topics": [
                "Matching game",
                "Quadratic Functions & Complex Numbers",
                "Algebra 2"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "The Rising Soufflé Bistro: Assessment Menu",
              "path": "artifacts/quadratic-functions-complex-numbers-assessment-menu/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-assessment-menu.jpg",
              "description": "Choice-based test: students order 4 Appetizers, 4 Entrées and 2 Chef’s Specials worth 5, 10 and 20 points, covering all four skill groups, with printed coordinate grids for graphing dishes. 100 points total. Includes a teacher guide, rubrics and answer key with graphs computed from the equations.",
              "type": "Printable",
              "topics": [
                "Quadratic functions",
                "Complex numbers",
                "Quadratic formula",
                "Choice menu"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Color By Number",
              "path": "artifacts/quadratic-functions-complex-numbers-color-by-number/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-color-by-number.jpg",
              "description": "Printable 2-page color-by-number: solve 10 problems on vertex form, factoring, completing the square, the discriminant, the quadratic formula, complex number multiplication and division, a projectile model and a quadratic inequality, match each answer to the color code, then color the windmill among the tulip fields. Page 1 is the picture, page 2 is the work space.",
              "type": "Printable",
              "topics": [
                "Quadratic functions",
                "Complex numbers",
                "Quadratic formula & discriminant",
                "Color by number"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratics & Complex Numbers Cheat Sheet",
              "path": "artifacts/quadratic-functions-complex-numbers-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: parabola forms, completing the square, the quadratic formula and the discriminant. Back: complex numbers, quadratic inequalities, linear-quadratic systems and modeling. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Quadratics & Complex Numbers",
                "Unit 3"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Parabola Four",
              "path": "artifacts/quadratic-functions-complex-numbers-connect-four/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-connect-four.jpg",
              "description": "Connect Four for two teams. Match parabola graphs to equations, read vertices and shaded regions, solve quadratics, use the discriminant, and simplify complex numbers. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Parabolas: vertex form, graphs, transformations",
                "Solving quadratics and the discriminant",
                "Imaginary and complex numbers",
                "Quadratic models and inequalities"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Error Analysis",
              "path": "artifacts/quadratic-functions-complex-numbers-error-analysis/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-error-analysis.jpg",
              "description": "Find the mistake in 10 worked solutions on vertex form, completing the square, square roots, the quadratic formula, the discriminant, powers of i, dividing complex numbers and quadratic inequalities. Seven items include computed student-versus-correct graphs. Explain the error and show the correct work.",
              "type": "Printable",
              "topics": [
                "Quadratics",
                "Complex numbers",
                "Discriminant",
                "Quadratic inequalities"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Picture Reveal",
              "path": "artifacts/quadratic-functions-complex-numbers-picture-reveal/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-picture-reveal.jpg",
              "description": "Solve by square roots, write a parabola from its graph, optimize area, find when a projectile lands, use the discriminant, multiply and divide complex numbers and solve quadratic inequalities and systems to uncover a hidden skate park scene. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Quadratics",
                "Complex numbers",
                "Quadratic modeling",
                "Inequalities"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Lockdown at Fountain Park",
              "path": "artifacts/quadratic-functions-complex-numbers-escape-room/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with a cipher, a parabola graph to write in vertex form, a graphs-and-discriminants true/false panel, a valve-vault dial puzzle (discriminant, vertex, powers of i), a complex-solutions order lock, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Quadratic functions",
                "Discriminant and vertex form",
                "Complex numbers",
                "Escape room"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Flashcards",
              "path": "artifacts/quadratic-functions-complex-numbers-flashcards/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-flashcards.jpg",
              "description": "25 flashcards with worked solutions and computed parabola graphs for vertex form, graphing and converting between forms, solving by factoring, square roots, completing the square and the quadratic formula, imaginary and complex numbers (conjugates and division), the discriminant, quadratic modeling, and quadratic inequalities and systems. Mark cards you need to practice and review them again. Filter by skill and by level (Easy, Medium or Hard).",
              "type": "Practice",
              "topics": [
                "Vertex form and graphing parabolas",
                "Solving quadratics",
                "Complex numbers",
                "Quadratic modeling and inequalities"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Showdown",
              "path": "artifacts/quadratic-functions-complex-numbers-jeopardy/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-jeopardy.jpg",
              "description": "A game board for Quadratic Functions & Complex Numbers. Write and model with parabolas, simplify, divide and solve with complex numbers, then finish with the discriminant, quadratic inequalities and line-parabola systems, many with computed graphs.",
              "type": "Game",
              "topics": [
                "Parabolas and models",
                "Complex numbers and equations",
                "Discriminant and inequalities",
                "Systems with a parabola"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Maze",
              "path": "artifacts/quadratic-functions-complex-numbers-maze/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-maze.jpg",
              "description": "Printable 4-page worksheet: find vertices, complete the square, use the quadratic formula, simplify powers of i, multiply and divide complex numbers, solve for complex roots, and model with quadratics to find the right door through a maze, recording each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Vertex form and graphing parabolas",
                "Solving quadratics: completing the square and the quadratic formula",
                "Complex numbers and complex roots",
                "Quadratic modeling and inequalities"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Stations",
              "path": "artifacts/algebra2-quadratic-functions-complex-numbers-stations/worksheet.pdf",
              "thumb": "thumbs/algebra2-quadratic-functions-complex-numbers-stations.svg",
              "description": "Printable Algebra 2 station work for Quadratic Functions & Complex Numbers. Students rotate through four problem sets covering parabolas and forms, solving quadratics and the discriminant, complex numbers, and quadratic models, inequalities and systems, with a one-page teacher answer key.",
              "type": "Printable",
              "topics": [
                "Stations",
                "Station work",
                "Quadratic Functions & Complex Numbers"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Tarsia Puzzle",
              "path": "artifacts/quadratic-functions-complex-numbers-tarsia/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-tarsia.jpg",
              "description": "Printable tarsia puzzle: cut out 24 triangles and match 30 problems to their answers to rebuild a hexagon. Covers vertex and standard form, solving quadratics four ways, the discriminant, complex number arithmetic and complex roots, quadratic models, and quadratic inequalities. Includes a show-your-work page (with one graph) and a teacher key with the solved hexagon.",
              "type": "Printable",
              "topics": [
                "Parabolas and quadratic forms",
                "Quadratic formula and discriminant",
                "Complex numbers",
                "Tarsia puzzle"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Backlot Blackout",
              "path": "artifacts/quadratic-functions-complex-numbers-backlot-blackout/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-backlot-blackout.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type vertex-form equations, vertex pairs, exact roots with ±, complex numbers in a + bi form, lists of points and interval answers.",
              "type": "Game",
              "topics": [
                "Quadratic functions & complex numbers",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Tic-Tac-Toe",
              "path": "artifacts/quadratic-functions-complex-numbers-tic-tac-toe/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice problem to claim a square. A wrong answer lets the other team steal. Optional timer.",
              "type": "Game",
              "topics": [
                "Quadratic functions & complex numbers",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Backlot Blackout (Printable)",
              "path": "artifacts/quadratic-functions-complex-numbers-whodunnit/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-whodunnit.jpg",
              "description": "Printable whodunnit: 10 clue cards to post around the room, each a multiple-choice problem where every answer leads to a clue. Includes a story and case board, a show-your-work page, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Quadratic functions & complex numbers",
                "Whodunnit",
                "Multiple choice",
                "Self-checking"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Partner Check 1: Solving Quadratic Equations",
              "path": "artifacts/algebra2-quadratic-functions-complex-numbers-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-quadratic-functions-complex-numbers-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Solving Quadratic Equations"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Complex Numbers & Parabolas",
              "path": "artifacts/algebra2-quadratic-functions-complex-numbers-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-quadratic-functions-complex-numbers-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Complex Numbers & Parabolas"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "polynomial-functions",
          "name": "Polynomial Functions",
          "artifacts": [
            {
              "title": "Polynomial Functions Matching Game",
              "path": "worksheet-generator/match-game.html#unit=algebra2-polynomial-functions",
              "thumb": "thumbs/matching-game-algebra2-polynomial-functions.svg",
              "description": "Interactive card sort: drag each graph, equation, table and description into the set it belongs to. Zoom in on any card (read coordinates on the big graph), check your sets, and get hints. CP2/CP1/Honors; uses the same verified cards as the printable Matching Card Sort.",
              "type": "Game",
              "topics": [
                "Matching game",
                "Polynomial Functions",
                "Algebra 2"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "Partner Check 1: Polynomial Operations & Graphs",
              "path": "artifacts/algebra2-polynomial-functions-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-polynomial-functions-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Polynomial Operations & Graphs"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Zeros, Factoring & Inequalities",
              "path": "artifacts/algebra2-polynomial-functions-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-polynomial-functions-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Zeros, Factoring & Inequalities"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Polynomial Functions Cheat Sheet",
              "path": "artifacts/polynomial-functions-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/polynomial-functions-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: polynomial operations, factoring patterns, synthetic division and the remainder and factor theorems. Back: zeros and multiplicity, end behavior, graphing, the Fundamental Theorem of Algebra, the Rational Root Theorem and an open-box application. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Polynomial Functions",
                "Unit 4"
              ],
              "added": "2026-10-31"
            }
          ]
        },
        {
          "id": "radicals-rational-exponents",
          "name": "Radicals & Rational Exponents",
          "artifacts": [
            {
              "title": "Radicals & Rational Exponents Matching Game",
              "path": "worksheet-generator/match-game.html#unit=algebra2-radicals-rational-exponents",
              "thumb": "thumbs/matching-game-algebra2-radicals-rational-exponents.svg",
              "description": "Interactive card sort: drag each graph, equation, table and description into the set it belongs to. Zoom in on any card (read coordinates on the big graph), check your sets, and get hints. CP2/CP1/Honors; uses the same verified cards as the printable Matching Card Sort.",
              "type": "Game",
              "topics": [
                "Matching game",
                "Radicals & Rational Exponents",
                "Algebra 2"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "Partner Check 1: Simplifying Radicals & Exponents",
              "path": "artifacts/algebra2-radicals-rational-exponents-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-radicals-rational-exponents-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Simplifying Radicals & Exponents"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Radical Equations & Functions",
              "path": "artifacts/algebra2-radicals-rational-exponents-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-radicals-rational-exponents-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Radical Equations & Functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Radicals & Rational Exponents Cheat Sheet",
              "path": "artifacts/radicals-rational-exponents-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/radicals-rational-exponents-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: simplifying radicals, radical operations, rational exponents and exponent rules. Back: radical and rational-exponent equations, extraneous solutions, and square-root and cube-root graphs and transformations. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Radicals & Rational Exponents",
                "Unit 5"
              ],
              "added": "2026-10-31"
            }
          ]
        },
        {
          "id": "exponential-logarithmic-functions",
          "name": "Exponential & Logarithmic Functions",
          "artifacts": [
            {
              "title": "Exponential & Logarithmic Functions Matching Game",
              "path": "worksheet-generator/match-game.html#unit=algebra2-exponential-logarithmic-functions",
              "thumb": "thumbs/matching-game-algebra2-exponential-logarithmic-functions.svg",
              "description": "Interactive card sort: drag each graph, equation, table and description into the set it belongs to. Zoom in on any card (read coordinates on the big graph), check your sets, and get hints. CP2/CP1/Honors; uses the same verified cards as the printable Matching Card Sort.",
              "type": "Game",
              "topics": [
                "Matching game",
                "Exponential & Logarithmic Functions",
                "Algebra 2"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "The Time Capsule Switcheroo",
              "path": "artifacts/exponential-logarithmic-functions-time-capsule-switcheroo/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-time-capsule-switcheroo.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers, with symbol buttons for exponents, logs and ln.",
              "type": "Game",
              "topics": [
                "Exponential & log equations",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Logarithmic Functions Tic-Tac-Toe",
              "path": "artifacts/exponential-logarithmic-functions-tic-tac-toe/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice problem to claim a square. A wrong answer lets the other team steal. Optional timer.",
              "type": "Game",
              "topics": [
                "Exponential & log equations",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Time Capsule Switcheroo (Printable)",
              "path": "artifacts/exponential-logarithmic-functions-whodunnit/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-whodunnit.jpg",
              "description": "Printable whodunnit: 10 clue cards to post around the room, each a multiple-choice problem where every answer leads to a clue. Includes a story and case board, a show-your-work page, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Exponential & log equations",
                "Whodunnit",
                "Multiple choice",
                "Self-checking"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exp & Log Functions Tarsia Puzzle",
              "path": "artifacts/exponential-logarithmic-functions-tarsia/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-tarsia.jpg",
              "description": "Printable tarsia puzzle: cut out 24 triangles and match 30 problems to their answers to rebuild a hexagon. Covers exponential and log form, evaluating logs, log properties, exponential and log equations, and modeling. Includes a show-your-work page and a teacher key with the solved hexagon.",
              "type": "Printable",
              "topics": [
                "Log and exponential form",
                "Log properties",
                "Solving exp and log equations",
                "Tarsia puzzle"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Logarithm Bistro: Assessment Menu",
              "path": "artifacts/exponential-logarithmic-functions-assessment-menu/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-assessment-menu.jpg",
              "description": "Choice-based test: students order 4 Appetizers, 4 Entrées and 2 Chef’s Specials worth 5, 10 and 20 points, covering all four skill groups. 100 points total. Includes a teacher guide, rubrics and answer key.",
              "type": "Printable",
              "topics": [
                "Exponential functions",
                "Logarithms",
                "Assessment",
                "Choice menu"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Pressure Drop: Escape the Deep",
              "path": "artifacts/exponential-logarithmic-functions-escape-room/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Exponential decay and half-life",
                "Evaluating and solving logarithms",
                "Extraneous solutions",
                "Escape room"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Logarithmic Functions Color By Number",
              "path": "artifacts/exponential-logarithmic-functions-color-by-number/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-color-by-number.jpg",
              "description": "Printable 2-page color-by-number: solve 10 problems, match each answer to the color code, then color the nautilus shell on the sea floor. Page 1 is the picture, page 2 is the work space.",
              "type": "Printable",
              "topics": [
                "Exponential equations",
                "Logarithms",
                "Color by number",
                "Self-checking"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Logarithmic Functions Error Analysis",
              "path": "artifacts/exponential-logarithmic-functions-error-analysis/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-error-analysis.jpg",
              "description": "Find the mistake in 10 worked solutions on logarithm properties, change of base, exponential and log equations, extraneous solutions and compound interest. Explain the error and show the correct work.",
              "type": "Printable",
              "topics": [
                "Log properties",
                "Change of base",
                "Extraneous solutions",
                "Compound interest"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Logarithmic Functions Picture Reveal",
              "path": "artifacts/exponential-logarithmic-functions-picture-reveal/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-picture-reveal.jpg",
              "description": "Convert and evaluate logs, expand and condense, solve exponential and log equations, and model growth and half-life to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Log properties",
                "Change of base",
                "Log equations",
                "Growth and half-life"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Logs Four",
              "path": "artifacts/exponential-logarithmic-functions-connect-four/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-connect-four.jpg",
              "description": "Connect Four for two teams. Convert between exponential and log form, evaluate and expand logs, solve exponential and log equations, and model growth, decay, and compound interest. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Exponential and log form",
                "Properties of logs and change of base",
                "Solving exponential and log equations",
                "Compound interest and half-life"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exp & Log Functions Flashcards",
              "path": "artifacts/exponential-logarithmic-functions-flashcards/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-flashcards.jpg",
              "description": "25 flashcards with worked solutions for exponential growth and decay, graphs and asymptotes, compound and continuous interest, logarithm form and domain, log properties and change of base, solving exponential and log equations (with extraneous solutions), and half-life, growth, and pH models. Mark cards you need to practice and review them again. Filter by skill and by level (Easy, Medium or Hard).",
              "type": "Practice",
              "topics": [
                "Exponential functions and graphs",
                "Compound interest and e",
                "Logarithm properties",
                "Solving exponential and log equations"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exp & Log Functions Showdown",
              "path": "artifacts/exponential-logarithmic-functions-jeopardy/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-jeopardy.jpg",
              "description": "A game board for Exponential & Logarithmic Functions. Work with exponential models and compound interest, then log form, domain, expanding and condensing, and finish with exponential and log equations and half-life problems.",
              "type": "Game",
              "topics": [
                "Exponential functions and interest",
                "Logarithm definition and properties",
                "Solving exponential and log equations",
                "Half-life and growth models"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Logarithmic Functions Maze",
              "path": "artifacts/exponential-logarithmic-functions-maze/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-maze.jpg",
              "description": "Printable 4-page worksheet: evaluate logarithms, solve exponential and logarithmic equations and model growth and decay to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Evaluating and expanding logarithms",
                "Solving exponential and log equations",
                "Extraneous solutions",
                "Compound interest and decay models"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Logarithmic Functions Stations",
              "path": "artifacts/algebra2-exponential-logarithmic-functions-stations/worksheet.pdf",
              "thumb": "thumbs/algebra2-exponential-logarithmic-functions-stations.svg",
              "description": "Printable Algebra 2 station work for Exponential & Logarithmic Functions. Students rotate through four problem sets to practice and review unit skills, with a teacher answer key.",
              "type": "Printable",
              "topics": [
                "Stations",
                "Station work",
                "Exponential & Logarithmic Functions"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Log Functions Cheat Sheet",
              "path": "artifacts/exponential-logarithmic-functions-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: exponential functions, the number e and the logarithm. Back: log properties, solving equations and modeling. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Exponential & Log Functions",
                "Unit 6"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check 1: Exponential & Log Basics",
              "path": "artifacts/algebra2-exponential-logarithmic-functions-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-exponential-logarithmic-functions-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Exponential & Log Basics"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Exp & Log Equations and Graphs",
              "path": "artifacts/algebra2-exponential-logarithmic-functions-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-exponential-logarithmic-functions-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Exp & Log Equations and Graphs"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "rational-functions",
          "name": "Rational Functions",
          "artifacts": [
            {
              "title": "Rational Functions Matching Game",
              "path": "worksheet-generator/match-game.html#unit=algebra2-rational-functions",
              "thumb": "thumbs/matching-game-algebra2-rational-functions.svg",
              "description": "Interactive card sort: drag each graph, equation, table and description into the set it belongs to. Zoom in on any card (read coordinates on the big graph), check your sets, and get hints. CP2/CP1/Honors; uses the same verified cards as the printable Matching Card Sort.",
              "type": "Game",
              "topics": [
                "Matching game",
                "Rational Functions",
                "Algebra 2"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "Partner Check 1: Rational Expressions & Equations",
              "path": "artifacts/algebra2-rational-functions-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-rational-functions-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Rational Expressions & Equations"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Graphs of Rational Functions",
              "path": "artifacts/algebra2-rational-functions-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-rational-functions-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Graphs of Rational Functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Rational Functions Cheat Sheet",
              "path": "artifacts/rational-functions-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/rational-functions-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: simplifying, multiplying, dividing, adding and subtracting rational expressions, and solving rational equations. Back: asymptotes and holes, graphing, transformations of 1/x, variation and work problems. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Rational Functions",
                "Unit 7"
              ],
              "added": "2026-10-31"
            }
          ]
        },
        {
          "id": "sequences-series",
          "name": "Sequences & Series",
          "artifacts": [
            {
              "title": "Sequences & Series Matching Game",
              "path": "worksheet-generator/match-game.html#unit=algebra2-sequences-series",
              "thumb": "thumbs/matching-game-algebra2-sequences-series.svg",
              "description": "Interactive card sort: drag each graph, equation, table and description into the set it belongs to. Zoom in on any card (read coordinates on the big graph), check your sets, and get hints. CP2/CP1/Honors; uses the same verified cards as the printable Matching Card Sort.",
              "type": "Game",
              "topics": [
                "Matching game",
                "Sequences & Series",
                "Algebra 2"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "Partner Check 1: Arithmetic & Geometric Sequences",
              "path": "artifacts/algebra2-sequences-series-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-sequences-series-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Arithmetic & Geometric Sequences"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Series, Binomials & Applications",
              "path": "artifacts/algebra2-sequences-series-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-sequences-series-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Series, Binomials & Applications"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Sequences & Series Cheat Sheet",
              "path": "artifacts/sequences-series-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/sequences-series-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: arithmetic and geometric sequences, recursive and explicit formulas. Back: arithmetic and geometric series, sigma notation, infinite geometric series and applications. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Sequences & Series",
                "Unit 8"
              ],
              "added": "2026-10-31"
            }
          ]
        },
        {
          "id": "conic-sections",
          "name": "Conic Sections",
          "artifacts": [
            {
              "title": "Partner Check 1: Circles & Parabolas",
              "path": "artifacts/algebra2-conic-sections-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-conic-sections-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Circles & Parabolas"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Ellipses & Hyperbolas",
              "path": "artifacts/algebra2-conic-sections-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-conic-sections-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Ellipses & Hyperbolas"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Conic Sections Cheat Sheet",
              "path": "artifacts/conic-sections-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/conic-sections-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: circles, parabolas, ellipses and hyperbolas in standard form. Back: identifying conics, converting to standard form, focus and directrix, vertical orientation and applications. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Conic Sections",
                "Unit 9"
              ],
              "added": "2026-10-31"
            }
          ]
        },
        {
          "id": "trigonometric-functions",
          "name": "Trigonometric Functions",
          "artifacts": [
            {
              "title": "Partner Check 1: Radians, Unit Circle & Right-Triangle Trig",
              "path": "artifacts/algebra2-trigonometric-functions-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-trigonometric-functions-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Radians, Unit Circle & Right-Triangle Trig"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Graphs of Trig Functions & Trig Equations",
              "path": "artifacts/algebra2-trigonometric-functions-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-trigonometric-functions-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Graphs of Trig Functions & Trig Equations"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Trigonometric Functions Cheat Sheet",
              "path": "artifacts/trigonometric-functions-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/trigonometric-functions-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: radians, the unit circle, reference angles and trig values of any angle. Back: sine and cosine graphs, amplitude, period and phase shift, identities, trig equations, inverse trig and modeling. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Trigonometric Functions",
                "Unit 10"
              ],
              "added": "2026-10-31"
            }
          ]
        },
        {
          "id": "probability-statistics",
          "name": "Probability & Statistics",
          "artifacts": [
            {
              "title": "Partner Check 1: Counting & Probability",
              "path": "artifacts/algebra2-probability-statistics-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-probability-statistics-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Counting & Probability"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Statistics & Normal Distributions",
              "path": "artifacts/algebra2-probability-statistics-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-probability-statistics-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Statistics & Normal Distributions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Probability & Statistics Cheat Sheet",
              "path": "artifacts/probability-statistics-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/probability-statistics-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: counting, permutations, combinations, independent and dependent events, and conditional probability. Back: probability distributions, expected value, normal distributions, z-scores and sampling. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Probability & Statistics",
                "Unit 11"
              ],
              "added": "2026-10-31"
            }
          ]
        }
      ],
      "comingSoon": false
    },
    {
      "id": "geometry",
      "name": "Geometry",
      "color": "orange",
      "art": "triangle",
      "blurb": "Reasoning, shapes, measurement, and transformations.",
      "units": [
        {
          "id": "foundations-geometry",
          "name": "Foundations of Geometry",
          "artifacts": [
            {
              "title": "Shipwreck Salvage",
              "path": "artifacts/geometry-shipwreck-salvage/index.html",
              "thumb": "thumbs/geometry-shipwreck-salvage.jpg",
              "description": "Navigate a coordinate grid to locate shipwrecks, find distances with the Pythagorean Theorem, and calculate midpoints across ten salvage missions.",
              "type": "Game",
              "bankFormat": "topic-games",
              "unitSpecific": true,
              "topics": [
                "Coordinate plane",
                "Distance formula",
                "Pythagorean Theorem",
                "Midpoint"
              ],
              "added": "2026-10-31"
            },
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-basics-reasoning",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Basics & Reasoning readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-27"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-basics-reasoning",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Basics & Reasoning: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-27"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-basics-reasoning",
              "thumb": "thumbs/geometry-worksheet-generator-basics-reasoning.svg",
              "description": "Differentiated Basics & Reasoning worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-27"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-basics-reasoning",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Basics & Reasoning quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-27"
            },
            {
              "title": "Reasoning Four",
              "path": "artifacts/basics-reasoning-connect-four/index.html",
              "description": "Connect Four for two teams on Basics & Reasoning. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Segments, midpoints and distance",
                "Angle addition and bisectors",
                "Converse, inverse, contrapositive",
                "Reasoning and proof properties",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/basics-reasoning-connect-four.jpg"
            },
            {
              "title": "Basics & Reasoning Flashcards",
              "path": "artifacts/basics-reasoning-flashcards/index.html",
              "thumb": "thumbs/basics-reasoning-flashcards.jpg",
              "description": "25 flashcards with worked solutions for points, lines and planes, segment and angle addition, midpoints and distance, conditional statements, inductive and deductive reasoning, and the properties used in proofs. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Segments, midpoints and distance",
                "Angle addition and bisectors",
                "Converse, inverse, contrapositive",
                "Reasoning and proof properties"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Basics & Reasoning Picture Reveal",
              "path": "artifacts/basics-reasoning-picture-reveal/index.html",
              "description": "Ten typed problems on Basics & Reasoning. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Segments, midpoints and distance",
                "Angle addition and bisectors",
                "Converse, inverse, contrapositive",
                "Reasoning and proof properties"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/basics-reasoning-picture-reveal.jpg"
            },
            {
              "title": "Reasoning Showdown",
              "path": "artifacts/basics-reasoning-showdown/index.html",
              "description": "A game board for Basics & Reasoning: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Segments, midpoints and distance",
                "Angle addition and bisectors",
                "Converse, inverse, contrapositive",
                "Reasoning and proof properties",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/basics-reasoning-showdown.jpg"
            },
            {
              "title": "The Pirate Cove Puzzle",
              "path": "artifacts/basics-reasoning-pirate-cove-puzzle/index.html",
              "thumb": "thumbs/basics-reasoning-pirate-cove-puzzle.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Segments and angles",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Basics & Reasoning Tic-Tac-Toe",
              "path": "artifacts/basics-reasoning-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Basics & Reasoning. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Segments, midpoints and distance",
                "Angle addition and bisectors",
                "Converse, inverse, contrapositive",
                "Reasoning and proof properties",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/basics-reasoning-tic-tac-toe.jpg"
            },
            {
              "title": "Temple of Logic: Jungle Escape",
              "path": "artifacts/basics-reasoning-escape-room/index.html",
              "thumb": "thumbs/basics-reasoning-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Segment addition and midpoints",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Basics & Reasoning Cheat Sheet",
              "path": "artifacts/geometry-basics-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-basics-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Basics & Reasoning. Front: points, lines, planes, segments, rays and angles. Back: segment and angle addition, midpoints, distance and angle pairs. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Basics & Reasoning",
                "Unit 1"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-basics-reasoning&kind=color",
              "thumb": "thumbs/geometry-color-generator-basics-reasoning.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Basics & Reasoning"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-basics-reasoning&kind=error",
              "thumb": "thumbs/geometry-error-generator-basics-reasoning.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Basics & Reasoning"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-basics-reasoning&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-basics-reasoning.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Basics & Reasoning"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-basics-reasoning&kind=who",
              "thumb": "thumbs/geometry-who-generator-basics-reasoning.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Basics & Reasoning"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-basics-reasoning&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-basics-reasoning.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Basics & Reasoning"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "angles-parallel-lines",
          "name": "Angles and Parallel Lines",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-angles-parallel-lines",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Angles & Parallel Lines readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-27"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-angles-parallel-lines",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Angles & Parallel Lines: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-27"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-angles-parallel-lines",
              "thumb": "thumbs/geometry-worksheet-generator-angles-parallel-lines.svg",
              "description": "Differentiated Angles & Parallel Lines worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-27"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-angles-parallel-lines",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Angles & Parallel Lines quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-27"
            },
            {
              "title": "Angles Four",
              "path": "artifacts/angles-parallel-lines-connect-four/index.html",
              "description": "Connect Four for two teams on Angles & Parallel Lines. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Proving lines parallel",
                "Triangle and exterior angles",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/angles-parallel-lines-connect-four.jpg"
            },
            {
              "title": "Angles & Parallel Lines Flashcards",
              "path": "artifacts/angles-parallel-lines-flashcards/index.html",
              "thumb": "thumbs/angles-parallel-lines-flashcards.jpg",
              "description": "25 flashcards with worked solutions for complementary, supplementary and vertical angles, angles made by a transversal, solving for x, proving lines parallel, and triangle angle sums. Figures are drawn to scale. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Proving lines parallel",
                "Triangle and exterior angles"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Angles & Parallel Lines Picture Reveal",
              "path": "artifacts/angles-parallel-lines-picture-reveal/index.html",
              "description": "Ten typed problems on Angles & Parallel Lines. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Proving lines parallel",
                "Triangle and exterior angles"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/angles-parallel-lines-picture-reveal.jpg"
            },
            {
              "title": "Angles Showdown",
              "path": "artifacts/angles-parallel-lines-showdown/index.html",
              "description": "A game board for Angles & Parallel Lines: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Proving lines parallel",
                "Triangle and exterior angles",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/angles-parallel-lines-showdown.jpg"
            },
            {
              "title": "The Midnight Express Mystery",
              "path": "artifacts/angles-parallel-lines-midnight-express-mystery/index.html",
              "thumb": "thumbs/angles-parallel-lines-midnight-express-mystery.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Parallel lines and triangles",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Angles & Parallel Lines Tic-Tac-Toe",
              "path": "artifacts/angles-parallel-lines-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Angles & Parallel Lines. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Proving lines parallel",
                "Triangle and exterior angles",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/angles-parallel-lines-tic-tac-toe.jpg"
            },
            {
              "title": "Crossing Tracks: Rail Yard Escape",
              "path": "artifacts/angles-parallel-lines-escape-room/index.html",
              "thumb": "thumbs/angles-parallel-lines-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Angles & Parallel Lines Cheat Sheet",
              "path": "artifacts/geometry-angles-parallel-lines-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-angles-parallel-lines-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Angles & Parallel Lines. Front: angle pairs and parallel lines cut by a transversal. Back: proving lines parallel, triangle angle sums and angle chasing. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Angles & Parallel Lines",
                "Unit 2"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-angles-parallel-lines&kind=color",
              "thumb": "thumbs/geometry-color-generator-angles-parallel-lines.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Angles & Parallel Lines"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-angles-parallel-lines&kind=error",
              "thumb": "thumbs/geometry-error-generator-angles-parallel-lines.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Angles & Parallel Lines"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-angles-parallel-lines&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-angles-parallel-lines.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Angles & Parallel Lines"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-angles-parallel-lines&kind=who",
              "thumb": "thumbs/geometry-who-generator-angles-parallel-lines.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Angles & Parallel Lines"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-angles-parallel-lines&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-angles-parallel-lines.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Angles & Parallel Lines"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "triangle-congruence",
          "name": "Triangle Congruence",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-triangles-congruence",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Triangles & Congruence readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-triangles-congruence",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Triangles & Congruence: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-triangles-congruence",
              "thumb": "thumbs/geometry-worksheet-generator-triangles-congruence.svg",
              "description": "Differentiated Triangles & Congruence worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-triangles-congruence",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Triangles & Congruence quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Triangle Congruence Proofs",
              "path": "artifacts/geometry-congruence-proofs/index.html",
              "thumb": "thumbs/geometry-congruence-proofs.jpg",
              "description": "Twelve two-column proofs on accurate generated diagrams that build from drag-and-drop statements, to reasons, to both, to written proofs and CPCTC. Every row is checked instantly; New set makes a fresh set, and teachers can print the worksheet and key.",
              "type": "Practice",
              "topics": [
                "SSS",
                "SAS",
                "ASA",
                "AAS",
                "HL",
                "CPCTC",
                "Two-column proofs"
              ],
              "added": "2026-11-01"
            },
            {
              "title": "Triangles & Congruence Flashcards",
              "path": "artifacts/triangles-congruence-flashcards/index.html",
              "description": "Generated congruence flashcards (matching parts, SSS, SAS, ASA, AAS, HL and proofs) with Easy, Medium, and Hard settings, skill selection, and practice tracking.",
              "type": "Practice",
              "added": "2026-10-28",
              "thumb": "thumbs/triangles-congruence-flashcards.jpg"
            },
            {
              "title": "Congruence Four",
              "path": "artifacts/triangles-congruence-connect-four/index.html",
              "description": "Connect Four for two teams on Triangles & Congruence. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "classifying triangles, angle sums, isosceles triangles and side–angle relationships",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/triangles-congruence-connect-four.jpg"
            },
            {
              "title": "Triangles & Congruence Picture Reveal",
              "path": "artifacts/triangles-congruence-picture-reveal/index.html",
              "description": "Ten typed problems on Triangles & Congruence. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "classifying triangles, angle sums, isosceles triangles and side–angle relationships"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/triangles-congruence-picture-reveal.jpg"
            },
            {
              "title": "Triangles Showdown",
              "path": "artifacts/triangles-congruence-showdown/index.html",
              "description": "A game board for Triangles & Congruence: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "classifying triangles, angle sums, isosceles triangles and side–angle relationships",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/triangles-congruence-showdown.jpg"
            },
            {
              "title": "The Pyramid Puzzle",
              "path": "artifacts/triangles-congruence-pyramid-puzzle/index.html",
              "thumb": "thumbs/triangles-congruence-pyramid-puzzle.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Congruence rules",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Triangles & Congruence Tic-Tac-Toe",
              "path": "artifacts/triangles-congruence-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Triangles & Congruence. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "classifying triangles, angle sums, isosceles triangles and side–angle relationships",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/triangles-congruence-tic-tac-toe.jpg"
            },
            {
              "title": "Lockdown at the Robot Factory",
              "path": "artifacts/triangles-congruence-escape-room/index.html",
              "thumb": "thumbs/triangles-congruence-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Triangle inequality and angle sums",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Triangles & Congruence Cheat Sheet",
              "path": "artifacts/geometry-triangles-congruence-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-triangles-congruence-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Triangles & Congruence. Front: classifying triangles, angle sums, isosceles triangles and side–angle relationships. Back: congruence shortcuts, CPCTC and two-column proofs. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Triangles & Congruence",
                "Unit 3"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangles-congruence&kind=color",
              "thumb": "thumbs/geometry-color-generator-triangles-congruence.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangles & Congruence"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangles-congruence&kind=error",
              "thumb": "thumbs/geometry-error-generator-triangles-congruence.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangles & Congruence"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangles-congruence&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-triangles-congruence.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangles & Congruence"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangles-congruence&kind=who",
              "thumb": "thumbs/geometry-who-generator-triangles-congruence.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangles & Congruence"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangles-congruence&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-triangles-congruence.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangles & Congruence"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "triangle-relationships",
          "name": "Triangle Relationships",
          "artifacts": [
            {
              "title": "Starlight Observatory: Locked Under the Stars",
              "path": "artifacts/triangle-relationships-escape-room/index.html",
              "thumb": "thumbs/triangle-relationships-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key (code 205).",
              "type": "Game",
              "topics": [
                "Triangle relationships",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "The Harbor Museum Compass Caper",
              "path": "artifacts/triangle-relationships-harbor-museum-caper/index.html",
              "thumb": "thumbs/triangle-relationships-harbor-museum-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Triangle relationships",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-triangle-relationships",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Triangle Relationships readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-27"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-triangle-relationships",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Triangle Relationships: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-27"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-triangle-relationships",
              "thumb": "thumbs/geometry-worksheet-generator-triangle-relationships.svg",
              "description": "Differentiated Triangle Relationships worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-27"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-triangle-relationships",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Triangle Relationships quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-27"
            },
            {
              "title": "Triangle Relationships Flashcards",
              "path": "artifacts/triangle-relationships-flashcards/index.html",
              "description": "Generated triangle angle-sum, exterior-angle, and isosceles-angle flashcards with Easy, Medium, and Hard settings, skill selection, and practice tracking.",
              "type": "Practice",
              "added": "2026-10-18",
              "thumb": "thumbs/triangle-relationships-flashcards.jpg"
            },
            {
              "title": "Triangle Relationships Showdown",
              "path": "artifacts/triangle-relationships-showdown/index.html",
              "description": "A game board for Triangle Relationships: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "angle facts, inequalities and special segments in triangles",
                "Team game"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/triangle-relationships-showdown.jpg"
            },
            {
              "title": "Triangle Relationships Four",
              "path": "artifacts/triangle-relationships-connect-four/index.html",
              "description": "Connect Four for two teams on Triangle Relationships. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "angle facts, inequalities and special segments in triangles",
                "Team game"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/triangle-relationships-connect-four.jpg"
            },
            {
              "title": "Triangle Relationships Tic-Tac-Toe",
              "path": "artifacts/triangle-relationships-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Triangle Relationships. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "angle facts, inequalities and special segments in triangles",
                "Team game"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/triangle-relationships-tic-tac-toe.jpg"
            },
            {
              "title": "Triangle Relationships Picture Reveal",
              "path": "artifacts/triangle-relationships-picture-reveal/index.html",
              "description": "Ten typed problems on Triangle Relationships. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "angle facts, inequalities and special segments in triangles"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/triangle-relationships-picture-reveal.jpg"
            },
            {
              "title": "Triangle Relationships Cheat Sheet",
              "path": "artifacts/geometry-triangle-relationships-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-triangle-relationships-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Triangle Relationships. Front: angle facts, inequalities and special segments in triangles. Back: midsegments, medians, bisectors, altitudes and points of concurrency. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Triangle Relationships",
                "Unit 4"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangle-relationships&kind=color",
              "thumb": "thumbs/geometry-color-generator-triangle-relationships.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangle Relationships"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangle-relationships&kind=error",
              "thumb": "thumbs/geometry-error-generator-triangle-relationships.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangle Relationships"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangle-relationships&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-triangle-relationships.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangle Relationships"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangle-relationships&kind=who",
              "thumb": "thumbs/geometry-who-generator-triangle-relationships.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangle Relationships"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangle-relationships&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-triangle-relationships.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangle Relationships"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "similarity",
          "name": "Similarity",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-similarity",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Similarity readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-similarity",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Similarity: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-similarity",
              "thumb": "thumbs/geometry-worksheet-generator-similarity.svg",
              "description": "Differentiated Similarity worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-similarity",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Similarity quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Similarity Four",
              "path": "artifacts/similarity-connect-four/index.html",
              "description": "Connect Four for two teams on Similarity. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Scale factor and proportions",
                "AA, SAS~ and SSS~",
                "Triangle proportionality theorem",
                "Perimeter, area and indirect measurement",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/similarity-connect-four.jpg"
            },
            {
              "title": "Similarity Flashcards",
              "path": "artifacts/similarity-flashcards/index.html",
              "thumb": "thumbs/similarity-flashcards.jpg",
              "description": "25 flashcards with worked solutions on similar figures and scale factor, AA, SAS and SSS similarity, similar triangles inside triangles, the Triangle Proportionality Theorem, perimeter and area ratios, and indirect measurement. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Scale factor and proportions",
                "AA, SAS~ and SSS~",
                "Triangle proportionality theorem",
                "Perimeter, area and indirect measurement"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Similarity Picture Reveal",
              "path": "artifacts/similarity-picture-reveal/index.html",
              "description": "Ten typed problems on Similarity. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Scale factor and proportions",
                "AA, SAS~ and SSS~",
                "Triangle proportionality theorem",
                "Perimeter, area and indirect measurement"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/similarity-picture-reveal.jpg"
            },
            {
              "title": "Similarity Showdown",
              "path": "artifacts/similarity-showdown/index.html",
              "description": "A game board for Similarity: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Scale factor and proportions",
                "AA, SAS~ and SSS~",
                "Triangle proportionality theorem",
                "Perimeter, area and indirect measurement",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/similarity-showdown.jpg"
            },
            {
              "title": "The Toy Workshop Theft",
              "path": "artifacts/similarity-toy-workshop-theft/index.html",
              "thumb": "thumbs/similarity-toy-workshop-theft.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Similar figures",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Similarity Tic-Tac-Toe",
              "path": "artifacts/similarity-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Similarity. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Scale factor and proportions",
                "AA, SAS~ and SSS~",
                "Triangle proportionality theorem",
                "Perimeter, area and indirect measurement",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/similarity-tic-tac-toe.jpg"
            },
            {
              "title": "The Shrink-Ray Workshop",
              "path": "artifacts/similarity-escape-room/index.html",
              "thumb": "thumbs/similarity-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Ratios and proportions",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Similarity Cheat Sheet",
              "path": "artifacts/geometry-similarity-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-similarity-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Similarity. Front: scale factors, similar figures and proportions. Back: similarity criteria, dilations, area and indirect measurement. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Similarity",
                "Unit 5"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-similarity&kind=color",
              "thumb": "thumbs/geometry-color-generator-similarity.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Similarity"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-similarity&kind=error",
              "thumb": "thumbs/geometry-error-generator-similarity.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Similarity"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-similarity&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-similarity.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Similarity"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-similarity&kind=who",
              "thumb": "thumbs/geometry-who-generator-similarity.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Similarity"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-similarity&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-similarity.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Similarity"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "right-triangles-trigonometry",
          "name": "Right Triangles and Trigonometry",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-right-triangles-trigonometry",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Right Triangles & Trigonometry readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-right-triangles-trigonometry",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Right Triangles & Trigonometry: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-right-triangles-trigonometry",
              "thumb": "thumbs/geometry-worksheet-generator-right-triangles-trigonometry.svg",
              "description": "Differentiated Right Triangles & Trigonometry worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-right-triangles-trigonometry",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Right Triangles & Trigonometry quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Trig Four",
              "path": "artifacts/right-triangles-trigonometry-connect-four/index.html",
              "description": "Connect Four for two teams on Right Triangles & Trigonometry. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Elevation and depression",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/right-triangles-trigonometry-connect-four.jpg"
            },
            {
              "title": "Right Triangles & Trigonometry Flashcards",
              "path": "artifacts/right-triangles-trigonometry-flashcards/index.html",
              "thumb": "thumbs/right-triangles-trigonometry-flashcards.jpg",
              "description": "25 flashcards with worked solutions on the Pythagorean Theorem and its converse, Pythagorean triples, special right triangles, sine, cosine and tangent, finding sides and angles, and angles of elevation and depression. Decimal answers are rounded to one decimal place.",
              "type": "Practice",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Elevation and depression"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Right Triangles & Trigonometry Picture Reveal",
              "path": "artifacts/right-triangles-trigonometry-picture-reveal/index.html",
              "description": "Ten typed problems on Right Triangles & Trigonometry. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Elevation and depression"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/right-triangles-trigonometry-picture-reveal.jpg"
            },
            {
              "title": "Right Triangles Showdown",
              "path": "artifacts/right-triangles-trigonometry-showdown/index.html",
              "description": "A game board for Right Triangles & Trigonometry: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Elevation and depression",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/right-triangles-trigonometry-showdown.jpg"
            },
            {
              "title": "The Lighthouse Lantern Mystery",
              "path": "artifacts/right-triangles-trigonometry-lighthouse-lantern-mystery/index.html",
              "thumb": "thumbs/right-triangles-trigonometry-lighthouse-lantern-mystery.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Right triangle trig",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Right Triangles & Trig Tic-Tac-Toe",
              "path": "artifacts/right-triangles-trigonometry-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Right Triangles & Trigonometry. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Elevation and depression",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/right-triangles-trigonometry-tic-tac-toe.jpg"
            },
            {
              "title": "Rotor Rescue: Summit Mission",
              "path": "artifacts/right-triangles-trigonometry-escape-room/index.html",
              "thumb": "thumbs/right-triangles-trigonometry-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Right Triangles & Trigonometry Cheat Sheet",
              "path": "artifacts/geometry-right-triangles-trigonometry-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-right-triangles-trigonometry-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Right Triangles & Trigonometry. Front: the Pythagorean Theorem, special right triangles and trig ratios. Back: finding sides and angles with SOH-CAH-TOA, elevation and depression. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Right Triangles & Trigonometry",
                "Unit 6"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-right-triangles-trigonometry&kind=color",
              "thumb": "thumbs/geometry-color-generator-right-triangles-trigonometry.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Right Triangles & Trigonometry"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-right-triangles-trigonometry&kind=error",
              "thumb": "thumbs/geometry-error-generator-right-triangles-trigonometry.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Right Triangles & Trigonometry"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-right-triangles-trigonometry&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-right-triangles-trigonometry.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Right Triangles & Trigonometry"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-right-triangles-trigonometry&kind=who",
              "thumb": "thumbs/geometry-who-generator-right-triangles-trigonometry.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Right Triangles & Trigonometry"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-right-triangles-trigonometry&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-right-triangles-trigonometry.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Right Triangles & Trigonometry"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "quadrilaterals-polygons",
          "name": "Quadrilaterals and Polygons",
          "artifacts": [
            {
              "title": "Lockdown at the Tile Factory",
              "path": "artifacts/quadrilaterals-polygons-escape-room/index.html",
              "thumb": "thumbs/quadrilaterals-polygons-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key (code 205).",
              "type": "Game",
              "topics": [
                "Quadrilaterals and polygons",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "The Mosaic Gallery Heist",
              "path": "artifacts/quadrilaterals-polygons-mosaic-gallery-heist/index.html",
              "thumb": "thumbs/quadrilaterals-polygons-mosaic-gallery-heist.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Quadrilaterals and polygons",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-quadrilaterals-polygons",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Quadrilaterals & Polygons readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-quadrilaterals-polygons",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Quadrilaterals & Polygons: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-quadrilaterals-polygons",
              "thumb": "thumbs/geometry-worksheet-generator-quadrilaterals-polygons.svg",
              "description": "Differentiated Quadrilaterals & Polygons worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-quadrilaterals-polygons",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Quadrilaterals & Polygons quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Quadrilaterals & Polygons Flashcards",
              "path": "artifacts/quadrilaterals-polygons-flashcards/index.html",
              "description": "Generated polygon-angle and parallelogram flashcards with Easy, Medium, and Hard difficulty, skill selection, and practice tracking.",
              "type": "Practice",
              "added": "2026-10-27",
              "thumb": "thumbs/quadrilaterals-polygons-flashcards.jpg"
            },
            {
              "title": "Quadrilaterals & Polygons Showdown",
              "path": "artifacts/quadrilaterals-polygons-showdown/index.html",
              "description": "A game board for Quadrilaterals & Polygons: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "polygon angle sums and the properties of quadrilaterals",
                "Team game"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/quadrilaterals-polygons-showdown.jpg"
            },
            {
              "title": "Quadrilaterals & Polygons Four",
              "path": "artifacts/quadrilaterals-polygons-connect-four/index.html",
              "description": "Connect Four for two teams on Quadrilaterals & Polygons. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "polygon angle sums and the properties of quadrilaterals",
                "Team game"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/quadrilaterals-polygons-connect-four.jpg"
            },
            {
              "title": "Quadrilaterals & Polygons Tic-Tac-Toe",
              "path": "artifacts/quadrilaterals-polygons-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Quadrilaterals & Polygons. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "polygon angle sums and the properties of quadrilaterals",
                "Team game"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/quadrilaterals-polygons-tic-tac-toe.jpg"
            },
            {
              "title": "Quadrilaterals & Polygons Picture Reveal",
              "path": "artifacts/quadrilaterals-polygons-picture-reveal/index.html",
              "description": "Ten typed problems on Quadrilaterals & Polygons. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "polygon angle sums and the properties of quadrilaterals"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/quadrilaterals-polygons-picture-reveal.jpg"
            },
            {
              "title": "Quadrilaterals & Polygons Cheat Sheet",
              "path": "artifacts/geometry-quadrilaterals-polygons-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-quadrilaterals-polygons-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Quadrilaterals & Polygons. Front: polygon angle sums and the properties of quadrilaterals. Back: parallelograms, rectangles, rhombuses, trapezoids, kites and coordinate proofs. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Quadrilaterals & Polygons",
                "Unit 7"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-quadrilaterals-polygons&kind=color",
              "thumb": "thumbs/geometry-color-generator-quadrilaterals-polygons.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadrilaterals & Polygons"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-quadrilaterals-polygons&kind=error",
              "thumb": "thumbs/geometry-error-generator-quadrilaterals-polygons.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadrilaterals & Polygons"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-quadrilaterals-polygons&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-quadrilaterals-polygons.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadrilaterals & Polygons"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-quadrilaterals-polygons&kind=who",
              "thumb": "thumbs/geometry-who-generator-quadrilaterals-polygons.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadrilaterals & Polygons"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-quadrilaterals-polygons&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-quadrilaterals-polygons.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadrilaterals & Polygons"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "transformations",
          "name": "Transformations",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-transformations",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Transformations readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-transformations",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Transformations: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-transformations",
              "thumb": "thumbs/geometry-worksheet-generator-transformations.svg",
              "description": "Differentiated Transformations worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-transformations",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Transformations quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Transformations Four",
              "path": "artifacts/coordinate-geometry-transformations-connect-four/index.html",
              "description": "Connect Four for two teams on Transformations. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Classifying figures from coordinates",
                "Translations, reflections, rotations and dilations",
                "Compositions and congruence",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/coordinate-geometry-transformations-connect-four.jpg"
            },
            {
              "title": "Coordinate Geometry & Transformations Flashcards",
              "path": "artifacts/coordinate-geometry-transformations-flashcards/index.html",
              "thumb": "thumbs/coordinate-geometry-transformations-flashcards.jpg",
              "description": "25 flashcards with worked solutions for distance, midpoint and slope, classifying figures on the coordinate plane, translations, reflections, rotations, dilations and compositions. Graphs are drawn to scale. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Distance, midpoint and slope",
                "Classifying figures from coordinates",
                "Translations, reflections, rotations and dilations",
                "Compositions and congruence"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Coordinate Geometry & Transformations Picture Reveal",
              "path": "artifacts/coordinate-geometry-transformations-picture-reveal/index.html",
              "description": "Ten typed problems on Transformations. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Classifying figures from coordinates",
                "Translations, reflections, rotations and dilations",
                "Compositions and congruence"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/coordinate-geometry-transformations-picture-reveal.jpg"
            },
            {
              "title": "Coordinate Showdown",
              "path": "artifacts/coordinate-geometry-transformations-showdown/index.html",
              "description": "A game board for Transformations: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Classifying figures from coordinates",
                "Translations, reflections, rotations and dilations",
                "Compositions and congruence",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/coordinate-geometry-transformations-showdown.jpg"
            },
            {
              "title": "The Treasure Map Mystery",
              "path": "artifacts/coordinate-geometry-transformations-treasure-map-mystery/index.html",
              "thumb": "thumbs/coordinate-geometry-transformations-treasure-map-mystery.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Transformations",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Transformations Tic-Tac-Toe",
              "path": "artifacts/coordinate-geometry-transformations-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Transformations. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Classifying figures from coordinates",
                "Translations, reflections, rotations and dilations",
                "Compositions and congruence",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/coordinate-geometry-transformations-tic-tac-toe.jpg"
            },
            {
              "title": "Glitch World: Trapped in the Game",
              "path": "artifacts/coordinate-geometry-transformations-escape-room/index.html",
              "thumb": "thumbs/coordinate-geometry-transformations-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Transformations Cheat Sheet",
              "path": "artifacts/geometry-coordinate-transformations-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-coordinate-transformations-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Transformations. Front: distance, midpoint, slope and translations. Back: reflections, rotations, dilations and sequences of transformations. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Transformations",
                "Unit 8"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-transformations&kind=color",
              "thumb": "thumbs/geometry-color-generator-transformations.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Transformations"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-transformations&kind=error",
              "thumb": "thumbs/geometry-error-generator-transformations.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Transformations"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-transformations&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-transformations.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Transformations"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-transformations&kind=who",
              "thumb": "thumbs/geometry-who-generator-transformations.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Transformations"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-transformations&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-transformations.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Transformations"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "circles",
          "name": "Circles",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-circles",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Circles readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-circles",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Circles: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-circles",
              "thumb": "thumbs/geometry-worksheet-generator-circles.svg",
              "description": "Differentiated Circles worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-circles",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Circles quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Circles Four",
              "path": "artifacts/circles-connect-four/index.html",
              "description": "Connect Four for two teams on Circles. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/circles-connect-four.jpg"
            },
            {
              "title": "Circles Flashcards",
              "path": "artifacts/circles-flashcards/index.html",
              "thumb": "thumbs/circles-flashcards.jpg",
              "description": "25 flashcards with worked solutions for parts of a circle, circumference and area, arcs and sectors, central and inscribed angles, tangents and chords, and equations of circles. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Circles Picture Reveal",
              "path": "artifacts/circles-picture-reveal/index.html",
              "description": "Ten typed problems on Circles. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/circles-picture-reveal.jpg"
            },
            {
              "title": "Circles Showdown",
              "path": "artifacts/circles-showdown/index.html",
              "description": "A game board for Circles: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/circles-showdown.jpg"
            },
            {
              "title": "The Carnival Caper",
              "path": "artifacts/circles-carnival-caper/index.html",
              "thumb": "thumbs/circles-carnival-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Circle measures",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Circles Tic-Tac-Toe",
              "path": "artifacts/circles-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Circles. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/circles-tic-tac-toe.jpg"
            },
            {
              "title": "Carnival After Dark: Locked In the Midway",
              "path": "artifacts/circles-escape-room/index.html",
              "thumb": "thumbs/circles-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Circles Cheat Sheet",
              "path": "artifacts/geometry-circles-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-circles-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Circles. Front: parts of a circle, circumference, area, arcs and sectors. Back: inscribed angles, chords, tangents and angles inside and outside a circle. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Circles",
                "Unit 9"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-circles&kind=color",
              "thumb": "thumbs/geometry-color-generator-circles.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Circles"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-circles&kind=error",
              "thumb": "thumbs/geometry-error-generator-circles.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Circles"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-circles&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-circles.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Circles"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-circles&kind=who",
              "thumb": "thumbs/geometry-who-generator-circles.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Circles"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-circles&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-circles.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Circles"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "area-surface-area-volume",
          "name": "Area, Surface Area and Volume",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-area-surface-area-volume",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Area, Surface Area & Volume readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-area-surface-area-volume",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Area, Surface Area & Volume: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-area-surface-area-volume",
              "thumb": "thumbs/geometry-worksheet-generator-area-surface-area-volume.svg",
              "description": "Differentiated Area, Surface Area & Volume worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-area-surface-area-volume",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Area, Surface Area & Volume quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Volume Four",
              "path": "artifacts/area-surface-area-volume-connect-four/index.html",
              "description": "Connect Four for two teams on Area, Surface Area & Volume. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Volume and surface area of solids",
                "Unit conversions and scale factors",
                "Real-world volume problems",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/area-surface-area-volume-connect-four.jpg"
            },
            {
              "title": "Area, Surface Area & Volume Flashcards",
              "path": "artifacts/area-surface-area-volume-flashcards/index.html",
              "thumb": "thumbs/area-surface-area-volume-flashcards.jpg",
              "description": "25 flashcards with worked solutions for area of polygons and composite figures, volume and surface area of prisms, cylinders, pyramids, cones and spheres, unit conversions, scale factors and real-world problems. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Area of polygons and composite figures",
                "Volume and surface area of solids",
                "Unit conversions and scale factors",
                "Real-world volume problems"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Area, Surface Area & Volume Picture Reveal",
              "path": "artifacts/area-surface-area-volume-picture-reveal/index.html",
              "description": "Ten typed problems on Area, Surface Area & Volume. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Volume and surface area of solids",
                "Unit conversions and scale factors",
                "Real-world volume problems"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/area-surface-area-volume-picture-reveal.jpg"
            },
            {
              "title": "Measurement Showdown",
              "path": "artifacts/area-surface-area-volume-showdown/index.html",
              "description": "A game board for Area, Surface Area & Volume: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Volume and surface area of solids",
                "Unit conversions and scale factors",
                "Real-world volume problems",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/area-surface-area-volume-showdown.jpg"
            },
            {
              "title": "The Candy Factory Caper",
              "path": "artifacts/area-surface-area-volume-candy-factory-caper/index.html",
              "thumb": "thumbs/area-surface-area-volume-candy-factory-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Area, surface area, volume",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Area, Surface Area & Volume Tic-Tac-Toe",
              "path": "artifacts/area-surface-area-volume-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Area, Surface Area & Volume. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Volume and surface area of solids",
                "Unit conversions and scale factors",
                "Real-world volume problems",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/area-surface-area-volume-tic-tac-toe.jpg"
            },
            {
              "title": "The Pharaoh’s Pyramid: Sealed Inside",
              "path": "artifacts/area-surface-area-volume-escape-room/index.html",
              "thumb": "thumbs/area-surface-area-volume-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Area, Surface Area & Volume Cheat Sheet",
              "path": "artifacts/geometry-area-surface-area-volume-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-area-surface-area-volume-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Area, Surface Area & Volume. Front: area formulas, composite figures and units. Back: surface area and volume of prisms, cylinders, pyramids, cones and spheres. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Area, Surface Area & Volume",
                "Unit 10"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-area-surface-area-volume&kind=color",
              "thumb": "thumbs/geometry-color-generator-area-surface-area-volume.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Area, Surface Area & Volume"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-area-surface-area-volume&kind=error",
              "thumb": "thumbs/geometry-error-generator-area-surface-area-volume.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Area, Surface Area & Volume"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-area-surface-area-volume&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-area-surface-area-volume.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Area, Surface Area & Volume"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-area-surface-area-volume&kind=who",
              "thumb": "thumbs/geometry-who-generator-area-surface-area-volume.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Area, Surface Area & Volume"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-area-surface-area-volume&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-area-surface-area-volume.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Area, Surface Area & Volume"
              ],
              "added": "2026-10-28"
            }
          ]
        }
      ],
      "comingSoon": false
    }
    ,  {
      "id": "prealgebra",
      "name": "Pre-Algebra (8th)",
      "color": "teal",
      "art": "curve",
      "blurb": "Grade 8 mathematics: real numbers, equations, functions, data, transformations, and geometry.",
      "units": [
          {
              "id": "real-numbers-exponents",
              "name": "Real Numbers and Exponents",
              "artifacts": [
                {
                  "title": "Real Numbers and Exponents Cheat Sheet",
                  "path": "artifacts/prealgebra-real-numbers-exponents-cheat-sheet/worksheet.pdf",
                  "thumb": "thumbs/prealgebra-real-numbers-exponents-cheat-sheet.jpg",
                  "description": "Two-page printable cheat sheet for Real Numbers and Exponents. Front: rational and irrational numbers, square and cube roots. Back: negative exponents, exponent rules and scientific notation. Key vocabulary, worked examples with every answer checked, and common mistakes.",
                  "type": "Printable",
                  "topics": [
                    "Cheat sheet",
                    "Reference",
                    "Real Numbers and Exponents",
                    "Unit 1"
                  ],
                  "added": "2026-11-01"
                }
              ]
          },
          {
              "id": "equations-expressions",
              "name": "Equations and Expressions",
              "artifacts": [
                {
                  "title": "Equations and Expressions Cheat Sheet",
                  "path": "artifacts/prealgebra-equations-expressions-cheat-sheet/worksheet.pdf",
                  "thumb": "thumbs/prealgebra-equations-expressions-cheat-sheet.jpg",
                  "description": "Two-page printable cheat sheet for Equations and Expressions. Front: expressions with exponents and roots, writing linear equations. Back: variables on both sides, the distributive property and the number of solutions. Key vocabulary, worked examples with every answer checked, and common mistakes.",
                  "type": "Printable",
                  "topics": [
                    "Cheat sheet",
                    "Reference",
                    "Equations and Expressions",
                    "Unit 2"
                  ],
                  "added": "2026-11-01"
                }
              ]
          },
          {
              "id": "linear-functional-relationships",
              "name": "Linear and Functional Relationships",
              "artifacts": [
                {
                  "title": "Linear and Functional Relationships Cheat Sheet",
                  "path": "artifacts/prealgebra-linear-functional-relationships-cheat-sheet/worksheet.pdf",
                  "thumb": "thumbs/prealgebra-linear-functional-relationships-cheat-sheet.jpg",
                  "description": "Two-page printable cheat sheet for Linear and Functional Relationships. Front: functions, function rules, tables and graphs. Back: linear vs. nonlinear, rate of change, intervals and graphs in context. Key vocabulary, worked examples with every answer checked, and common mistakes.",
                  "type": "Printable",
                  "topics": [
                    "Cheat sheet",
                    "Reference",
                    "Linear and Functional Relationships",
                    "Unit 3"
                  ],
                  "added": "2026-11-01"
                }
              ]
          },
          {
              "id": "systems-linear-equations",
              "name": "Systems of Linear Equations",
              "artifacts": [
                {
                  "title": "Systems of Linear Equations Cheat Sheet",
                  "path": "artifacts/prealgebra-systems-linear-equations-cheat-sheet/worksheet.pdf",
                  "thumb": "thumbs/prealgebra-systems-linear-equations-cheat-sheet.jpg",
                  "description": "Two-page printable cheat sheet for Systems of Linear Equations. Front: slope-intercept form and solving systems by graphing. Back: substitution, elimination, inspection and word problems. Key vocabulary, worked examples with every answer checked, and common mistakes.",
                  "type": "Printable",
                  "topics": [
                    "Cheat sheet",
                    "Reference",
                    "Systems of Linear Equations",
                    "Unit 4"
                  ],
                  "added": "2026-11-01"
                }
              ]
          },
          {
              "id": "patterns-bivariate-data",
              "name": "Patterns and Bivariate Data",
              "artifacts": [
                {
                  "title": "Patterns and Bivariate Data Cheat Sheet",
                  "path": "artifacts/prealgebra-patterns-bivariate-data-cheat-sheet/worksheet.pdf",
                  "thumb": "thumbs/prealgebra-patterns-bivariate-data-cheat-sheet.jpg",
                  "description": "Two-page printable cheat sheet for Patterns and Bivariate Data. Front: scatter plots, association and lines of best fit. Back: two-way tables, relative frequencies and making predictions. Key vocabulary, worked examples with every answer checked, and common mistakes.",
                  "type": "Printable",
                  "topics": [
                    "Cheat sheet",
                    "Reference",
                    "Patterns and Bivariate Data",
                    "Unit 5"
                  ],
                  "added": "2026-11-01"
                }
              ]
          },
          {
              "id": "congruence-similarity",
              "name": "Congruence and Similarity",
              "artifacts": [
                {
                  "title": "Congruence and Similarity Cheat Sheet",
                  "path": "artifacts/prealgebra-congruence-similarity-cheat-sheet/worksheet.pdf",
                  "thumb": "thumbs/prealgebra-congruence-similarity-cheat-sheet.jpg",
                  "description": "Two-page printable cheat sheet for Congruence and Similarity. Front: translations, reflections, rotations and dilations on the coordinate plane. Back: congruence and similarity through transformations, triangle angles and parallel lines. Key vocabulary, worked examples with every answer checked, and common mistakes.",
                  "type": "Printable",
                  "topics": [
                    "Cheat sheet",
                    "Reference",
                    "Congruence and Similarity",
                    "Unit 6"
                  ],
                  "added": "2026-11-01"
                }
              ]
          },
          {
              "id": "geometry-applications",
              "name": "Geometry",
              "artifacts": [
                {
                  "title": "Geometry Cheat Sheet",
                  "path": "artifacts/prealgebra-geometry-applications-cheat-sheet/worksheet.pdf",
                  "thumb": "thumbs/prealgebra-geometry-applications-cheat-sheet.jpg",
                  "description": "Two-page printable cheat sheet for Geometry. Front: the Pythagorean theorem and its converse in 2-D, 3-D and on the coordinate plane. Back: volume of cylinders, cones, spheres and composite solids. Key vocabulary, worked examples with every answer checked, and common mistakes.",
                  "type": "Printable",
                  "topics": [
                    "Cheat sheet",
                    "Reference",
                    "Geometry",
                    "Unit 7"
                  ],
                  "added": "2026-11-01"
                }
              ]
          }
      ],
      "comingSoon": false
  },
{
  "id": "prealgebra7",
  "name": "Pre-Algebra (7th)",
  "color": "green",
  "art": "curve",
  "blurb": "Expressions, integers, fractions, proportions, functions, geometry, statistics, and polynomials.",
  "units": [
    {
      "id": "algebraic-expressions-integers",
      "name": "Algebraic Expressions and Integers",
      "artifacts": []
    },
    {
      "id": "one-step-equations-inequalities",
      "name": "Solving One-Step Equations and Inequalities",
      "artifacts": []
    },
    {
      "id": "decimals-equations",
      "name": "Decimals and Equations",
      "artifacts": []
    },
    {
      "id": "factors-fractions-exponents",
      "name": "Factors, Fractions, and Exponents",
      "artifacts": []
    },
    {
      "id": "operations-fractions",
      "name": "Operations with Fractions",
      "artifacts": []
    },
    {
      "id": "ratios-proportions-percentages",
      "name": "Ratios, Proportions, and Percentages",
      "artifacts": []
    },
    {
      "id": "solving-equations-inequalities",
      "name": "Solving Equations and Inequalities",
      "artifacts": []
    },
    {
      "id": "linear-functions-graphing",
      "name": "Linear Functions and Graphing",
      "artifacts": []
    },
    {
      "id": "spatial-thinking",
      "name": "Spatial Thinking",
      "artifacts": []
    },
    {
      "id": "area-volume",
      "name": "Area and Volume",
      "artifacts": []
    },
    {
      "id": "right-triangles-algebra",
      "name": "Right Triangles in Algebra",
      "artifacts": []
    },
    {
      "id": "data-analysis-probability",
      "name": "Data Analysis and Probability",
      "artifacts": []
    },
    {
      "id": "nonlinear-functions-polynomials",
      "name": "Nonlinear Functions and Polynomials",
      "artifacts": []
    }
  ],
  "comingSoon": false
},
{
  "id": "math5",
  "name": "5th Grade Math",
  "color": "sunshine",
  "art": "fifth",
  "blurb": "Place value, multi-digit operations, decimals, expressions, fractions, measurement, volume, coordinate planes, shapes, and data.",
  "units": [
    {
      "id": "place-value-number-sense",
      "name": "Place Value and Number Sense",
      "artifacts": []
    },
    {
      "id": "multi-digit-multiplication-division",
      "name": "Multi-Digit Multiplication and Division",
      "artifacts": []
    },
    {
      "id": "decimal-operations",
      "name": "Decimal Operations",
      "artifacts": []
    },
    {
      "id": "numerical-expressions-patterns",
      "name": "Numerical Expressions and Patterns",
      "artifacts": []
    },
    {
      "id": "fraction-addition-subtraction",
      "name": "Fraction Concepts and Operations",
      "artifacts": []
    },
    {
      "id": "fraction-multiplication-division",
      "name": "Multiplying and Dividing Fractions",
      "artifacts": []
    },
    {
      "id": "measurement-conversions",
      "name": "Measurement and Conversions",
      "artifacts": []
    },
    {
      "id": "volume-three-dimensional-figures",
      "name": "Volume and Three-Dimensional Figures",
      "artifacts": []
    },
    {
      "id": "coordinate-plane-graphing",
      "name": "Coordinate Planes and Graphing",
      "artifacts": []
    },
    {
      "id": "classifying-two-dimensional-figures",
      "name": "Geometry and Classifying Shapes",
      "artifacts": []
    },
    {
      "id": "data-line-plots-problem-solving",
      "name": "Data, Line Plots, and Problem Solving",
      "artifacts": []
    }
  ],
  "comingSoon": false
},
{
  "id": "math6",
  "name": "6th Grade Math",
  "color": "coral",
  "art": "curve",
  "blurb": "Ratios, fractions, rational numbers, expressions, equations, inequalities, geometry, and data.",
  "units": [
    {
      "id": "ratios-rates-percent-proportions",
      "name": "Ratios, Rate, Percent and Proportions",
      "artifacts": []
    },
    {
      "id": "fractions-decimals-operations",
      "name": "Operations of Fractions and Decimals",
      "artifacts": []
    },
    {
      "id": "rational-numbers",
      "name": "Rational Numbers",
      "artifacts": []
    },
    {
      "id": "expressions-equations",
      "name": "Expressions and Equations",
      "artifacts": []
    },
    {
      "id": "inequalities",
      "name": "Inequalities",
      "artifacts": []
    },
    {
      "id": "geometry",
      "name": "Geometry",
      "artifacts": []
    },
    {
      "id": "data-displays",
      "name": "Data Displays",
      "artifacts": []
    }
  ],
  "comingSoon": false
}
  ]
};

/* Bank-backed resources supplement retained original activities and PDFs. */
(function(G){
 var course=G.LIBRARY.courses.find(function(c){return c.id==='algebra2'});if(!course)return;
 course.units.forEach(function(u){
  [['flashcards','Flashcards','flashcards'],['connect-four','Connect 4','connect-four'],['tic-tac-toe','Tic-Tac-Toe','tic-tac-toe'],['picture-reveal','Picture Reveal','picture-reveal'],['showdown','Showdown','showdown'],['detective','Detective','detective-games'],['escape-room','Escape Room','escape-rooms']].forEach(function(g){
   u.artifacts.push({title:u.name+' '+g[1]+' — Skill Practice',path:'worksheet-generator/algebra2-game.html?unit='+u.id+'&game='+g[0],bankFormat:g[2],type:g[0]==='flashcards'?'Study Guide':'Game',thumb:'thumbs/foundations-algebra-'+(g[0]==='flashcards'?'flashcards':['detective','escape-room'].includes(g[0])?'showdown':g[0])+'.jpg',description:'Practice selected skills with the shared Algebra 2 question bank and difficulty settings.'});
  });
  u.artifacts.push({title:'Assessment Readiness Check',path:'worksheet-generator/algebra2-practice.html?unit='+u.id,bankFormat:'interactive-practice-test',type:'Study Guide',thumb:'thumbs/practice-test.svg',description:'Interactive practice with feedback, worked solutions, and skill review.'});
 });
})(window);

/* Grade 8 authored banks use the established course players and native generators. */
(function(G){
 const course=G.LIBRARY.courses.find(c=>c.id==='prealgebra');if(!course)return;
 course.units.forEach(u=>{
  [['showdown','Showdown','showdown'],['connect-four','Connect 4','connect-four'],['tic-tac-toe','Tic-Tac-Toe','tic-tac-toe'],['escape-room','Escape Room','escape-rooms'],['detective','Detective','detective-games'],['picture-reveal','Picture Reveal','picture-reveal'],['flashcards','Flashcards','flashcards']].forEach(([game,title,format])=>{
   u.artifacts.push({title:u.name+' '+title,path:'worksheet-generator/'+(['escape-room','detective'].includes(game)?'course-activity':'course-game')+'.html?course=prealgebra&unit='+u.id+'&game='+game,bankFormat:format,type:game==='flashcards'?'Study Guide':'Game',thumb:'thumbs/previews/prealgebra/'+u.id+'-'+game+'.png',description:'Choose Grade 8 skills and Remedial, Standard, or Advanced questions.'});
  });
  u.artifacts.push({title:'Vocabulary Activities and Crosswords',path:'worksheet-generator/printables.html#unit=prealgebra-'+u.id+'&kind=vocabulary',type:'Printable',thumb:'thumbs/vocabulary-prealgebra.svg',description:'Matching, fill-in-the-blank, examples, and crosswords using vocabulary from the existing unit cheat sheet.'});
  if(u.id==='linear-functional-relationships')u.artifacts.push({title:'Matching Card Sort',path:'worksheet-generator/printables.html#unit=prealgebra-'+u.id+'&kind=match',type:'Printable',thumb:'thumbs/matching-game-linear-equations-slope.svg',description:'Match linear-function graphs, equations, tables, and descriptions. Print cards or play online.'});
  [['error','Error Analysis','error-generator-foundations.svg'],['tarsia','Tarsia Puzzle','tarsia-generator-foundations.svg']].forEach(([kind,title,thumb])=>{
   u.artifacts.push({title:title+' Generator',path:'worksheet-generator/printables.html#unit=prealgebra-'+u.id+'&kind='+kind,type:'Printable',thumb:'thumbs/'+thumb,description:kind==='error'?'Find, explain, and correct mistakes using authored Pre-Algebra questions. Includes teacher solutions.':'Match problems and answers to assemble a triangle puzzle. Includes work pages and a solved teacher key.',topics:['Printable generator',u.name]});
  });
  u.artifacts.push({title:'Assessment Readiness Check',path:'worksheet-generator/practice-test.html#unit=prealgebra-'+u.id,bankFormat:'interactive-practice-test',type:'Study Guide',thumb:'thumbs/practice-test.svg',description:'Practice Grade 8 skills, review worked solutions, and target skills for reassessment.'});
 });
})(window);

/* Grade 7 and Grade 6 authored banks use the same course players and native generators as Grade 8. */
(function(G){
 [['prealgebra7','Grade 7'],['math6','Grade 6']].forEach(([courseId,label])=>{
  const course=G.LIBRARY.courses.find(c=>c.id===courseId);if(!course)return;
  course.units.forEach(u=>{
   [['showdown','Showdown','showdown'],['connect-four','Connect 4','connect-four'],['tic-tac-toe','Tic-Tac-Toe','tic-tac-toe'],['escape-room','Escape Room','escape-rooms'],['detective','Detective','detective-games'],['picture-reveal','Picture Reveal','picture-reveal'],['flashcards','Flashcards','flashcards']].forEach(([game,title,format])=>{
    u.artifacts.push({title:u.name+' '+title,path:'worksheet-generator/'+(['escape-room','detective'].includes(game)?'course-activity':'course-game')+'.html?course='+courseId+'&unit='+u.id+'&game='+game,bankFormat:format,type:game==='flashcards'?'Study Guide':'Game',thumb:'thumbs/foundations-algebra-'+(game==='flashcards'?'flashcards':['detective','escape-room'].includes(game)?'showdown':game)+'.jpg',description:'Choose '+label+' skills and Remedial, Standard, or Advanced questions from the approved bank.',level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-04'});
   });
   u.artifacts.push({title:'Vocabulary Activities and Crosswords',path:'worksheet-generator/printables.html#unit='+courseId+'-'+u.id+'&kind=vocabulary',type:'Printable',thumb:'thumbs/vocabulary-prealgebra.svg',description:'Matching, fill-in-the-blank, examples, and crosswords using the unit vocabulary.',level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-04'});
   [['error','Error Analysis','error-generator-foundations.svg'],['tarsia','Tarsia Puzzle','tarsia-generator-foundations.svg']].forEach(([kind,title,thumb])=>{
    u.artifacts.push({title:title+' Generator',path:'worksheet-generator/printables.html#unit='+courseId+'-'+u.id+'&kind='+kind,type:'Printable',thumb:'thumbs/'+thumb,description:kind==='error'?'Find, explain, and correct mistakes using authored '+label+' questions. Includes teacher solutions.':'Match problems and answers to assemble a triangle puzzle. Includes work pages and a solved teacher key.',level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-04'});
   });
   u.artifacts.push({title:'Assessment Readiness Check',path:'worksheet-generator/practice-test.html#unit='+courseId+'-'+u.id,bankFormat:'interactive-practice-test',type:'Study Guide',thumb:'thumbs/practice-test.svg',description:'Practice '+label+' skills, review worked solutions, and target skills for reassessment.',level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-04'});
  });
 });
})(window);

/* Grade 6/7/8 printable activity links: all existing bank-driven generators, no new runtime.
   Grade 8 (prealgebra) joined 2026-11-07: its units already build these formats in the printable generator. */
(function(G){
 [['prealgebra','Grade 8','2026-11-07'],['prealgebra7','Grade 7'],['math6','Grade 6']].forEach(function(pair){
  var c=G.LIBRARY.courses.find(function(item){return item.id===pair[0]});if(!c)return;
  c.units.forEach(function(u){
   [
    ['maze','Maze','maze-generator-foundations.svg','Follow a route of correctly answered questions through a mathematical maze.'],
    ['color','Color by Number','geometry-color-generator-basics-reasoning.svg','Solve problems to reveal a color-coded picture.'],
    ['partner','Partner Check','partner-generator-foundations.svg','Solve and compare matched-answer problems in pairs.'],
    ['stations','Station Work','stations-generator-foundations.svg','Rotate through independent stations with mixed problem types.'],
    ['who','Whodunnit','foundations-algebra-whodunnit.jpg','Solve clues and narrow down the mystery.']
   ].forEach(function(a){
    var url='worksheet-generator/printables.html#unit='+c.id+'-'+u.id+'&kind='+a[0];
    if(u.artifacts.some(function(x){return x.path===url}))return;
    u.artifacts.push({title:a[1]+' Generator',path:url,bankFormat:'printable-generator',type:'Printable',
      thumb:'thumbs/'+a[2],description:a[3]+' Uses '+pair[1]+' questions and a teacher key.',
      level:['CP2','CP1','Honors'],topics:[u.name],added:pair[2]||'2026-11-04'});
   });
  });
 });
})(window);

/* Precalculus and Calculus use the shared approved-bank activities. */
/* Grade 7 and Grade 6 authored banks use the same course players and native generators as Grade 8. */
(function(G){
 [['precalculus','Precalculus'],['calculus','Calculus'],['statistics','Statistics']].forEach(([courseId,label])=>{
  const course=G.LIBRARY.courses.find(c=>c.id===courseId);if(!course)return;
  course.units.forEach(u=>{
   [['showdown','Showdown','showdown'],['connect-four','Connect 4','connect-four'],['tic-tac-toe','Tic-Tac-Toe','tic-tac-toe'],['escape-room','Escape Room','escape-rooms'],['detective','Detective','detective-games'],['picture-reveal','Picture Reveal','picture-reveal'],['flashcards','Flashcards','flashcards']].forEach(([game,title,format])=>{
    u.artifacts.push({title:u.name+' '+title,path:'worksheet-generator/'+(['escape-room','detective'].includes(game)?'course-activity':'course-game')+'.html?course='+courseId+'&unit='+u.id+'&game='+game,bankFormat:format,type:game==='flashcards'?'Study Guide':'Game',thumb:'thumbs/foundations-algebra-'+(game==='flashcards'?'flashcards':['detective','escape-room'].includes(game)?'showdown':game)+'.jpg',description:'Choose '+label+' skills and CP2, CP1, or Honors questions from the approved bank.',level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-04'});
   });
   u.artifacts.push({title:'Vocabulary Activities and Crosswords',path:'worksheet-generator/printables.html#unit='+courseId+'-'+u.id+'&kind=vocabulary',type:'Printable',thumb:'thumbs/vocabulary-prealgebra.svg',description:'Matching, fill-in-the-blank, examples, and crosswords using the unit vocabulary.',level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-04'});
   [['error','Error Analysis','error-generator-foundations.svg'],['tarsia','Tarsia Puzzle','tarsia-generator-foundations.svg']].forEach(([kind,title,thumb])=>{
    u.artifacts.push({title:title+' Generator',path:'worksheet-generator/printables.html#unit='+courseId+'-'+u.id+'&kind='+kind,type:'Printable',thumb:'thumbs/'+thumb,description:kind==='error'?'Find, explain, and correct mistakes using authored '+label+' questions. Includes teacher solutions.':'Match problems and answers to assemble a triangle puzzle. Includes work pages and a solved teacher key.',level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-04'});
   });
   u.artifacts.push({title:'Assessment Readiness Check',path:'worksheet-generator/practice-test.html#unit='+courseId+'-'+u.id,bankFormat:'interactive-practice-test',type:'Study Guide',thumb:'thumbs/practice-test.svg',description:'Practice '+label+' skills, review worked solutions, and target skills for reassessment.',level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-04'});
  });
 });
})(window);

/* Grade 6/7 printable activity links: all existing bank-driven generators, no new runtime. */
(function(G){
 [['precalculus','Precalculus'],['calculus','Calculus'],['statistics','Statistics']].forEach(function(pair){
  var c=G.LIBRARY.courses.find(function(item){return item.id===pair[0]});if(!c)return;
  c.units.forEach(function(u){
   [
    ['maze','Maze','maze-generator-foundations.svg','Follow a route of correctly answered questions through a mathematical maze.'],
    ['color','Color by Number','geometry-color-generator-basics-reasoning.svg','Solve problems to reveal a color-coded picture.'],
    ['partner','Partner Check','partner-generator-foundations.svg','Solve and compare matched-answer problems in pairs.'],
    ['stations','Station Work','stations-generator-foundations.svg','Rotate through independent stations with mixed problem types.'],
    ['who','Whodunnit','foundations-algebra-whodunnit.jpg','Solve clues and narrow down the mystery.']
   ].forEach(function(a){
    var url='worksheet-generator/printables.html#unit='+c.id+'-'+u.id+'&kind='+a[0];
    if(u.artifacts.some(function(x){return x.path===url}))return;
    u.artifacts.push({title:a[1]+' Generator',path:url,bankFormat:'printable-generator',type:'Printable',
      thumb:'thumbs/'+a[2],description:a[3]+' Uses '+pair[1]+' questions and a teacher key.',
      level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-04'});
   });
  });
 });
})(window);

(function(G){ G.LIBRARY.courses.filter(c=>["precalculus","calculus"].includes(c.id)).forEach(c=>{c.planned=false;}); })(window);

/* 5th Grade Math (2026-11-11): Grade 5 game collection, flashcards, Understanding Checks, elementary cheat sheets,
   vocabulary and printable generators from the approved bank, Interactive Math and unit projects (built by tools/grade5-authoring/). */
(function(G){
 var c=G.LIBRARY.courses.find(function(x){return x.id==='math5';});if(!c)return;
 var R={"place-value-number-sense":[{"title":"Math Quest: Place Value and Number Sense","path":"worksheet-generator/grade5-games.html?game=math-quest&unit=place-value-number-sense","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-quest.svg","description":"Unlock six lands on an adventure map by answering correctly. Play alone or as a class. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense","Grade 5 game"],"added":"2026-11-11"},{"title":"Treasure Trail: Place Value and Number Sense","path":"worksheet-generator/grade5-games.html?game=treasure-trail&unit=place-value-number-sense","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-treasure.svg","description":"Follow the treasure map stone by stone and collect gems. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense","Grade 5 game"],"added":"2026-11-11"},{"title":"Space Explorer: Place Value and Number Sense","path":"worksheet-generator/grade5-games.html?game=space-explorer&unit=place-value-number-sense","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-space.svg","description":"Earn fuel cells to fly from planet to planet. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Builders: Place Value and Number Sense","path":"worksheet-generator/grade5-games.html?game=math-builders&unit=place-value-number-sense","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-builders.svg","description":"Earn a building for your town with every correct answer. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense","Grade 5 game"],"added":"2026-11-11"},{"title":"Picture Reveal: Place Value and Number Sense","path":"worksheet-generator/grade5-games.html?game=picture-reveal&unit=place-value-number-sense","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-reveal.svg","description":"Uncover tiles to reveal a hidden picture. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Race: Place Value and Number Sense","path":"worksheet-generator/grade5-games.html?game=math-race&unit=place-value-number-sense","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-race.svg","description":"Two to four teams race; a correct answer moves the team car one space. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Soccer: Place Value and Number Sense","path":"worksheet-generator/grade5-games.html?game=math-soccer&unit=place-value-number-sense","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-soccer.svg","description":"Two teams kick the ball toward the goal with correct answers. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense","Grade 5 game"],"added":"2026-11-11"},{"title":"Connect 4: Place Value and Number Sense","path":"worksheet-generator/grade5-games.html?game=connect-four&unit=place-value-number-sense","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-connect4.svg","description":"Two teams answer to earn discs. Four in a row wins. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense","Grade 5 game"],"added":"2026-11-11"},{"title":"Puzzle Masters: Place Value and Number Sense","path":"worksheet-generator/grade5-games.html?game=puzzle-masters&unit=place-value-number-sense","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-puzzle.svg","description":"Flip cards and match each problem to its answer, alone or with a partner. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense","Grade 5 game"],"added":"2026-11-11"},{"title":"Flashcards: Place Value and Number Sense","path":"worksheet-generator/grade5-flashcards.html?unit=place-value-number-sense","bankFormat":"flashcards","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-flashcards.svg","description":"Colorful flashcards for vocabulary, symbols, big ideas, pictures, rules, mental math and common mistakes.","topics":["Place Value and Number Sense"],"added":"2026-11-11"},{"title":"Understanding Check","path":"worksheet-generator/grade5-understanding-check.html?unit=place-value-number-sense","bankFormat":"interactive-practice-test","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-understanding-check.svg","description":"A friendly check of learning: one question at a time or all on one page, hints, worked solutions, review of missed questions and a teacher summary.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense"],"added":"2026-11-11"},{"title":"Understanding Check (Printable Version)","path":"worksheet-generator/practice-test.html#unit=math5-place-value-number-sense","bankFormat":"interactive-practice-test","type":"Study Guide","thumb":"thumbs/practice-test.svg","description":"Build a printable Understanding Check from the Grade 5 bank, with an answer key and a targeted follow-up.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense"],"added":"2026-11-11"},{"title":"Place Value and Number Sense Cheat Sheet","path":"artifacts/math5-place-value-number-sense-cheat-sheet/worksheet.pdf","thumb":"thumbs/math5-place-value-number-sense-cheat-sheet.jpg","type":"Printable","description":"Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It! for Place Value and Number Sense.","topics":["Cheat sheet","Reference","Place Value and Number Sense","Unit 1"],"added":"2026-11-11"},{"title":"Vocabulary Activities and Crosswords","path":"worksheet-generator/printables.html#unit=math5-place-value-number-sense&kind=vocabulary","type":"Printable","thumb":"thumbs/vocabulary-prealgebra.svg","description":"Matching, fill-in-the-blank, examples, and crosswords using the Grade 5 unit vocabulary.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense"],"added":"2026-11-11"},{"title":"Error Analysis Generator","path":"worksheet-generator/printables.html#unit=math5-place-value-number-sense&kind=error","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/error-generator-foundations.svg","description":"Find, explain, and correct mistakes. Includes teacher solutions. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense"],"added":"2026-11-11"},{"title":"Tarsia Puzzle Generator","path":"worksheet-generator/printables.html#unit=math5-place-value-number-sense&kind=tarsia","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/tarsia-generator-foundations.svg","description":"Match problems and answers to assemble a triangle puzzle. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense"],"added":"2026-11-11"},{"title":"Maze Generator","path":"worksheet-generator/printables.html#unit=math5-place-value-number-sense&kind=maze","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/maze-generator-foundations.svg","description":"Follow a route of correctly answered questions through a maze. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense"],"added":"2026-11-11"},{"title":"Color by Number Generator","path":"worksheet-generator/printables.html#unit=math5-place-value-number-sense&kind=color","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/geometry-color-generator-basics-reasoning.svg","description":"Solve problems to reveal a color-coded picture. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense"],"added":"2026-11-11"},{"title":"Partner Check Generator","path":"worksheet-generator/printables.html#unit=math5-place-value-number-sense&kind=partner","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/partner-generator-foundations.svg","description":"Solve and compare matched-answer problems in pairs. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense"],"added":"2026-11-11"},{"title":"Station Work Generator","path":"worksheet-generator/printables.html#unit=math5-place-value-number-sense&kind=stations","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/stations-generator-foundations.svg","description":"Rotate through stations with mixed problem types. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense"],"added":"2026-11-11"},{"title":"Whodunnit Generator","path":"worksheet-generator/printables.html#unit=math5-place-value-number-sense&kind=who","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/foundations-algebra-whodunnit.jpg","description":"Solve clues and narrow down the mystery. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense"],"added":"2026-11-11"},{"title":"Decimal Place-Value Builder","path":"artifacts/math5-place-value-builder/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/math5-place-value-builder.jpg","description":"Build numbers digit by digit in a place-value chart, multiply and divide by 10, and see expanded form, word form and base-ten blocks change.","topics":["Place value","Decimals","Powers of 10"],"worksheet":"artifacts/math5-place-value-builder/worksheet.pdf","answerKey":"artifacts/math5-place-value-builder/teacher-key.pdf","added":"2026-11-11"},{"title":"Project: Sports Stats Showdown","path":"artifacts/math5-project-sports-stats-showdown/index.html","bankFormat":"projects","keepPath":true,"type":"Project","thumb":"thumbs/math5-project-sports-stats-showdown.jpg","description":"Students become the Field Day statisticians. They read and write decimal race times and jump distances, compare and order them to award medals, round results for the scoreboard, and use powers of 10 to scale ticket and snack sales.","level":["Remedial","Standard","Advanced"],"topics":["Place Value and Number Sense","Project","Sports & Field Day"],"added":"2026-11-11"}],"multi-digit-multiplication-division":[{"title":"Math Quest: Multi-Digit Multiplication and Division","path":"worksheet-generator/grade5-games.html?game=math-quest&unit=multi-digit-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-quest.svg","description":"Unlock six lands on an adventure map by answering correctly. Play alone or as a class. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division","Grade 5 game"],"added":"2026-11-11"},{"title":"Treasure Trail: Multi-Digit Multiplication and Division","path":"worksheet-generator/grade5-games.html?game=treasure-trail&unit=multi-digit-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-treasure.svg","description":"Follow the treasure map stone by stone and collect gems. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division","Grade 5 game"],"added":"2026-11-11"},{"title":"Space Explorer: Multi-Digit Multiplication and Division","path":"worksheet-generator/grade5-games.html?game=space-explorer&unit=multi-digit-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-space.svg","description":"Earn fuel cells to fly from planet to planet. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Builders: Multi-Digit Multiplication and Division","path":"worksheet-generator/grade5-games.html?game=math-builders&unit=multi-digit-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-builders.svg","description":"Earn a building for your town with every correct answer. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division","Grade 5 game"],"added":"2026-11-11"},{"title":"Picture Reveal: Multi-Digit Multiplication and Division","path":"worksheet-generator/grade5-games.html?game=picture-reveal&unit=multi-digit-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-reveal.svg","description":"Uncover tiles to reveal a hidden picture. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Race: Multi-Digit Multiplication and Division","path":"worksheet-generator/grade5-games.html?game=math-race&unit=multi-digit-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-race.svg","description":"Two to four teams race; a correct answer moves the team car one space. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Soccer: Multi-Digit Multiplication and Division","path":"worksheet-generator/grade5-games.html?game=math-soccer&unit=multi-digit-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-soccer.svg","description":"Two teams kick the ball toward the goal with correct answers. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division","Grade 5 game"],"added":"2026-11-11"},{"title":"Connect 4: Multi-Digit Multiplication and Division","path":"worksheet-generator/grade5-games.html?game=connect-four&unit=multi-digit-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-connect4.svg","description":"Two teams answer to earn discs. Four in a row wins. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division","Grade 5 game"],"added":"2026-11-11"},{"title":"Puzzle Masters: Multi-Digit Multiplication and Division","path":"worksheet-generator/grade5-games.html?game=puzzle-masters&unit=multi-digit-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-puzzle.svg","description":"Flip cards and match each problem to its answer, alone or with a partner. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division","Grade 5 game"],"added":"2026-11-11"},{"title":"Flashcards: Multi-Digit Multiplication and Division","path":"worksheet-generator/grade5-flashcards.html?unit=multi-digit-multiplication-division","bankFormat":"flashcards","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-flashcards.svg","description":"Colorful flashcards for vocabulary, symbols, big ideas, pictures, rules, mental math and common mistakes.","topics":["Multi-Digit Multiplication and Division"],"added":"2026-11-11"},{"title":"Understanding Check","path":"worksheet-generator/grade5-understanding-check.html?unit=multi-digit-multiplication-division","bankFormat":"interactive-practice-test","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-understanding-check.svg","description":"A friendly check of learning: one question at a time or all on one page, hints, worked solutions, review of missed questions and a teacher summary.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division"],"added":"2026-11-11"},{"title":"Understanding Check (Printable Version)","path":"worksheet-generator/practice-test.html#unit=math5-multi-digit-multiplication-division","bankFormat":"interactive-practice-test","type":"Study Guide","thumb":"thumbs/practice-test.svg","description":"Build a printable Understanding Check from the Grade 5 bank, with an answer key and a targeted follow-up.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division"],"added":"2026-11-11"},{"title":"Multi-Digit Multiplication and Division Cheat Sheet","path":"artifacts/math5-multi-digit-multiplication-division-cheat-sheet/worksheet.pdf","thumb":"thumbs/math5-multi-digit-multiplication-division-cheat-sheet.jpg","type":"Printable","description":"Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It! for Multi-Digit Multiplication and Division.","topics":["Cheat sheet","Reference","Multi-Digit Multiplication and Division","Unit 2"],"added":"2026-11-11"},{"title":"Vocabulary Activities and Crosswords","path":"worksheet-generator/printables.html#unit=math5-multi-digit-multiplication-division&kind=vocabulary","type":"Printable","thumb":"thumbs/vocabulary-prealgebra.svg","description":"Matching, fill-in-the-blank, examples, and crosswords using the Grade 5 unit vocabulary.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division"],"added":"2026-11-11"},{"title":"Error Analysis Generator","path":"worksheet-generator/printables.html#unit=math5-multi-digit-multiplication-division&kind=error","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/error-generator-foundations.svg","description":"Find, explain, and correct mistakes. Includes teacher solutions. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division"],"added":"2026-11-11"},{"title":"Tarsia Puzzle Generator","path":"worksheet-generator/printables.html#unit=math5-multi-digit-multiplication-division&kind=tarsia","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/tarsia-generator-foundations.svg","description":"Match problems and answers to assemble a triangle puzzle. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division"],"added":"2026-11-11"},{"title":"Maze Generator","path":"worksheet-generator/printables.html#unit=math5-multi-digit-multiplication-division&kind=maze","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/maze-generator-foundations.svg","description":"Follow a route of correctly answered questions through a maze. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division"],"added":"2026-11-11"},{"title":"Color by Number Generator","path":"worksheet-generator/printables.html#unit=math5-multi-digit-multiplication-division&kind=color","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/geometry-color-generator-basics-reasoning.svg","description":"Solve problems to reveal a color-coded picture. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division"],"added":"2026-11-11"},{"title":"Partner Check Generator","path":"worksheet-generator/printables.html#unit=math5-multi-digit-multiplication-division&kind=partner","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/partner-generator-foundations.svg","description":"Solve and compare matched-answer problems in pairs. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division"],"added":"2026-11-11"},{"title":"Station Work Generator","path":"worksheet-generator/printables.html#unit=math5-multi-digit-multiplication-division&kind=stations","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/stations-generator-foundations.svg","description":"Rotate through stations with mixed problem types. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division"],"added":"2026-11-11"},{"title":"Whodunnit Generator","path":"worksheet-generator/printables.html#unit=math5-multi-digit-multiplication-division&kind=who","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/foundations-algebra-whodunnit.jpg","description":"Solve clues and narrow down the mystery. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division"],"added":"2026-11-11"},{"title":"Area Model Explorer","path":"artifacts/math5-area-model-explorer/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/math5-area-model-explorer.jpg","description":"Split rectangles into partial products to multiply two-digit numbers, then switch to fractions and multiply parts of a whole.","topics":["Area model","Partial products","Multiplying fractions"],"worksheet":"artifacts/math5-area-model-explorer/worksheet.pdf","answerKey":"artifacts/math5-area-model-explorer/teacher-key.pdf","added":"2026-11-11"},{"title":"Project: School Carnival Planner","path":"artifacts/math5-project-school-carnival-planner/index.html","bankFormat":"projects","keepPath":true,"type":"Project","thumb":"thumbs/math5-project-school-carnival-planner.jpg","description":"Students plan a school carnival. They multiply to find ticket and prize totals, divide to share supplies and arrange buses and tables, interpret remainders, and estimate to check that the plan makes sense.","level":["Remedial","Standard","Advanced"],"topics":["Multi-Digit Multiplication and Division","Project","Events & Planning"],"added":"2026-11-11"}],"decimal-operations":[{"title":"Math Quest: Decimal Operations","path":"worksheet-generator/grade5-games.html?game=math-quest&unit=decimal-operations","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-quest.svg","description":"Unlock six lands on an adventure map by answering correctly. Play alone or as a class. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Treasure Trail: Decimal Operations","path":"worksheet-generator/grade5-games.html?game=treasure-trail&unit=decimal-operations","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-treasure.svg","description":"Follow the treasure map stone by stone and collect gems. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Space Explorer: Decimal Operations","path":"worksheet-generator/grade5-games.html?game=space-explorer&unit=decimal-operations","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-space.svg","description":"Earn fuel cells to fly from planet to planet. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Builders: Decimal Operations","path":"worksheet-generator/grade5-games.html?game=math-builders&unit=decimal-operations","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-builders.svg","description":"Earn a building for your town with every correct answer. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Picture Reveal: Decimal Operations","path":"worksheet-generator/grade5-games.html?game=picture-reveal&unit=decimal-operations","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-reveal.svg","description":"Uncover tiles to reveal a hidden picture. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Race: Decimal Operations","path":"worksheet-generator/grade5-games.html?game=math-race&unit=decimal-operations","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-race.svg","description":"Two to four teams race; a correct answer moves the team car one space. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Soccer: Decimal Operations","path":"worksheet-generator/grade5-games.html?game=math-soccer&unit=decimal-operations","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-soccer.svg","description":"Two teams kick the ball toward the goal with correct answers. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Connect 4: Decimal Operations","path":"worksheet-generator/grade5-games.html?game=connect-four&unit=decimal-operations","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-connect4.svg","description":"Two teams answer to earn discs. Four in a row wins. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Puzzle Masters: Decimal Operations","path":"worksheet-generator/grade5-games.html?game=puzzle-masters&unit=decimal-operations","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-puzzle.svg","description":"Flip cards and match each problem to its answer, alone or with a partner. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Flashcards: Decimal Operations","path":"worksheet-generator/grade5-flashcards.html?unit=decimal-operations","bankFormat":"flashcards","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-flashcards.svg","description":"Colorful flashcards for vocabulary, symbols, big ideas, pictures, rules, mental math and common mistakes.","topics":["Decimal Operations"],"added":"2026-11-11"},{"title":"Understanding Check","path":"worksheet-generator/grade5-understanding-check.html?unit=decimal-operations","bankFormat":"interactive-practice-test","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-understanding-check.svg","description":"A friendly check of learning: one question at a time or all on one page, hints, worked solutions, review of missed questions and a teacher summary.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations"],"added":"2026-11-11"},{"title":"Understanding Check (Printable Version)","path":"worksheet-generator/practice-test.html#unit=math5-decimal-operations","bankFormat":"interactive-practice-test","type":"Study Guide","thumb":"thumbs/practice-test.svg","description":"Build a printable Understanding Check from the Grade 5 bank, with an answer key and a targeted follow-up.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations"],"added":"2026-11-11"},{"title":"Decimal Operations Cheat Sheet","path":"artifacts/math5-decimal-operations-cheat-sheet/worksheet.pdf","thumb":"thumbs/math5-decimal-operations-cheat-sheet.jpg","type":"Printable","description":"Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It! for Decimal Operations.","topics":["Cheat sheet","Reference","Decimal Operations","Unit 3"],"added":"2026-11-11"},{"title":"Vocabulary Activities and Crosswords","path":"worksheet-generator/printables.html#unit=math5-decimal-operations&kind=vocabulary","type":"Printable","thumb":"thumbs/vocabulary-prealgebra.svg","description":"Matching, fill-in-the-blank, examples, and crosswords using the Grade 5 unit vocabulary.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations"],"added":"2026-11-11"},{"title":"Error Analysis Generator","path":"worksheet-generator/printables.html#unit=math5-decimal-operations&kind=error","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/error-generator-foundations.svg","description":"Find, explain, and correct mistakes. Includes teacher solutions. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations"],"added":"2026-11-11"},{"title":"Tarsia Puzzle Generator","path":"worksheet-generator/printables.html#unit=math5-decimal-operations&kind=tarsia","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/tarsia-generator-foundations.svg","description":"Match problems and answers to assemble a triangle puzzle. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations"],"added":"2026-11-11"},{"title":"Maze Generator","path":"worksheet-generator/printables.html#unit=math5-decimal-operations&kind=maze","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/maze-generator-foundations.svg","description":"Follow a route of correctly answered questions through a maze. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations"],"added":"2026-11-11"},{"title":"Color by Number Generator","path":"worksheet-generator/printables.html#unit=math5-decimal-operations&kind=color","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/geometry-color-generator-basics-reasoning.svg","description":"Solve problems to reveal a color-coded picture. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations"],"added":"2026-11-11"},{"title":"Partner Check Generator","path":"worksheet-generator/printables.html#unit=math5-decimal-operations&kind=partner","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/partner-generator-foundations.svg","description":"Solve and compare matched-answer problems in pairs. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations"],"added":"2026-11-11"},{"title":"Station Work Generator","path":"worksheet-generator/printables.html#unit=math5-decimal-operations&kind=stations","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/stations-generator-foundations.svg","description":"Rotate through stations with mixed problem types. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations"],"added":"2026-11-11"},{"title":"Whodunnit Generator","path":"worksheet-generator/printables.html#unit=math5-decimal-operations&kind=who","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/foundations-algebra-whodunnit.jpg","description":"Solve clues and narrow down the mystery. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations"],"added":"2026-11-11"},{"title":"Project: Class Party Budget","path":"artifacts/math5-project-class-party-budget/index.html","bankFormat":"projects","keepPath":true,"type":"Project","thumb":"thumbs/math5-project-class-party-budget.jpg","description":"Students plan an end-of-year class party. They add the costs of decorations and food, multiply decimal prices by quantities, divide to find the cost per student and the better buy, and subtract to stay within the budget.","level":["Remedial","Standard","Advanced"],"topics":["Decimal Operations","Project","Money & Shopping"],"added":"2026-11-11"},{"title":"Decimal Place-Value Builder","path":"artifacts/math5-place-value-builder/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/math5-place-value-builder.jpg","description":"Build numbers digit by digit in a place-value chart, multiply and divide by 10, and see expanded form, word form and base-ten blocks change.","topics":["Place value","Decimals","Powers of 10"],"worksheet":"artifacts/math5-place-value-builder/worksheet.pdf","answerKey":"artifacts/math5-place-value-builder/teacher-key.pdf","added":"2026-11-11"}],"numerical-expressions-patterns":[{"title":"Math Quest: Numerical Expressions and Patterns","path":"worksheet-generator/grade5-games.html?game=math-quest&unit=numerical-expressions-patterns","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-quest.svg","description":"Unlock six lands on an adventure map by answering correctly. Play alone or as a class. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns","Grade 5 game"],"added":"2026-11-11"},{"title":"Treasure Trail: Numerical Expressions and Patterns","path":"worksheet-generator/grade5-games.html?game=treasure-trail&unit=numerical-expressions-patterns","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-treasure.svg","description":"Follow the treasure map stone by stone and collect gems. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns","Grade 5 game"],"added":"2026-11-11"},{"title":"Space Explorer: Numerical Expressions and Patterns","path":"worksheet-generator/grade5-games.html?game=space-explorer&unit=numerical-expressions-patterns","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-space.svg","description":"Earn fuel cells to fly from planet to planet. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Builders: Numerical Expressions and Patterns","path":"worksheet-generator/grade5-games.html?game=math-builders&unit=numerical-expressions-patterns","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-builders.svg","description":"Earn a building for your town with every correct answer. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns","Grade 5 game"],"added":"2026-11-11"},{"title":"Picture Reveal: Numerical Expressions and Patterns","path":"worksheet-generator/grade5-games.html?game=picture-reveal&unit=numerical-expressions-patterns","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-reveal.svg","description":"Uncover tiles to reveal a hidden picture. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Race: Numerical Expressions and Patterns","path":"worksheet-generator/grade5-games.html?game=math-race&unit=numerical-expressions-patterns","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-race.svg","description":"Two to four teams race; a correct answer moves the team car one space. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Soccer: Numerical Expressions and Patterns","path":"worksheet-generator/grade5-games.html?game=math-soccer&unit=numerical-expressions-patterns","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-soccer.svg","description":"Two teams kick the ball toward the goal with correct answers. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns","Grade 5 game"],"added":"2026-11-11"},{"title":"Connect 4: Numerical Expressions and Patterns","path":"worksheet-generator/grade5-games.html?game=connect-four&unit=numerical-expressions-patterns","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-connect4.svg","description":"Two teams answer to earn discs. Four in a row wins. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns","Grade 5 game"],"added":"2026-11-11"},{"title":"Puzzle Masters: Numerical Expressions and Patterns","path":"worksheet-generator/grade5-games.html?game=puzzle-masters&unit=numerical-expressions-patterns","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-puzzle.svg","description":"Flip cards and match each problem to its answer, alone or with a partner. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns","Grade 5 game"],"added":"2026-11-11"},{"title":"Flashcards: Numerical Expressions and Patterns","path":"worksheet-generator/grade5-flashcards.html?unit=numerical-expressions-patterns","bankFormat":"flashcards","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-flashcards.svg","description":"Colorful flashcards for vocabulary, symbols, big ideas, pictures, rules, mental math and common mistakes.","topics":["Numerical Expressions and Patterns"],"added":"2026-11-11"},{"title":"Understanding Check","path":"worksheet-generator/grade5-understanding-check.html?unit=numerical-expressions-patterns","bankFormat":"interactive-practice-test","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-understanding-check.svg","description":"A friendly check of learning: one question at a time or all on one page, hints, worked solutions, review of missed questions and a teacher summary.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns"],"added":"2026-11-11"},{"title":"Understanding Check (Printable Version)","path":"worksheet-generator/practice-test.html#unit=math5-numerical-expressions-patterns","bankFormat":"interactive-practice-test","type":"Study Guide","thumb":"thumbs/practice-test.svg","description":"Build a printable Understanding Check from the Grade 5 bank, with an answer key and a targeted follow-up.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns"],"added":"2026-11-11"},{"title":"Numerical Expressions and Patterns Cheat Sheet","path":"artifacts/math5-numerical-expressions-patterns-cheat-sheet/worksheet.pdf","thumb":"thumbs/math5-numerical-expressions-patterns-cheat-sheet.jpg","type":"Printable","description":"Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It! for Numerical Expressions and Patterns.","topics":["Cheat sheet","Reference","Numerical Expressions and Patterns","Unit 4"],"added":"2026-11-11"},{"title":"Vocabulary Activities and Crosswords","path":"worksheet-generator/printables.html#unit=math5-numerical-expressions-patterns&kind=vocabulary","type":"Printable","thumb":"thumbs/vocabulary-prealgebra.svg","description":"Matching, fill-in-the-blank, examples, and crosswords using the Grade 5 unit vocabulary.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns"],"added":"2026-11-11"},{"title":"Error Analysis Generator","path":"worksheet-generator/printables.html#unit=math5-numerical-expressions-patterns&kind=error","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/error-generator-foundations.svg","description":"Find, explain, and correct mistakes. Includes teacher solutions. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns"],"added":"2026-11-11"},{"title":"Tarsia Puzzle Generator","path":"worksheet-generator/printables.html#unit=math5-numerical-expressions-patterns&kind=tarsia","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/tarsia-generator-foundations.svg","description":"Match problems and answers to assemble a triangle puzzle. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns"],"added":"2026-11-11"},{"title":"Maze Generator","path":"worksheet-generator/printables.html#unit=math5-numerical-expressions-patterns&kind=maze","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/maze-generator-foundations.svg","description":"Follow a route of correctly answered questions through a maze. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns"],"added":"2026-11-11"},{"title":"Color by Number Generator","path":"worksheet-generator/printables.html#unit=math5-numerical-expressions-patterns&kind=color","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/geometry-color-generator-basics-reasoning.svg","description":"Solve problems to reveal a color-coded picture. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns"],"added":"2026-11-11"},{"title":"Partner Check Generator","path":"worksheet-generator/printables.html#unit=math5-numerical-expressions-patterns&kind=partner","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/partner-generator-foundations.svg","description":"Solve and compare matched-answer problems in pairs. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns"],"added":"2026-11-11"},{"title":"Station Work Generator","path":"worksheet-generator/printables.html#unit=math5-numerical-expressions-patterns&kind=stations","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/stations-generator-foundations.svg","description":"Rotate through stations with mixed problem types. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns"],"added":"2026-11-11"},{"title":"Whodunnit Generator","path":"worksheet-generator/printables.html#unit=math5-numerical-expressions-patterns&kind=who","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/foundations-algebra-whodunnit.jpg","description":"Solve clues and narrow down the mystery. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns"],"added":"2026-11-11"},{"title":"Expression Builder","path":"artifacts/math5-expression-builder/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/math5-expression-builder.jpg","description":"Type or tap to build numerical expressions with parentheses, brackets and braces, then watch them evaluated one step at a time.","topics":["Order of operations","Grouping symbols","Expressions"],"worksheet":"artifacts/math5-expression-builder/worksheet.pdf","answerKey":"artifacts/math5-expression-builder/teacher-key.pdf","added":"2026-11-11"},{"title":"Project: Theme Park Points","path":"artifacts/math5-project-theme-park-points/index.html","bankFormat":"projects","keepPath":true,"type":"Project","thumb":"thumbs/math5-project-theme-park-points.jpg","description":"Students plan a theme park day. They write and evaluate expressions with grouping symbols for ride points and costs, interpret expressions without calculating, generate two numerical patterns for two savings plans, and graph the ordered pairs to compare them.","level":["Remedial","Standard","Advanced"],"topics":["Numerical Expressions and Patterns","Project","Travel & Fun"],"added":"2026-11-11"}],"fraction-addition-subtraction":[{"title":"Math Quest: Fraction Concepts and Operations","path":"worksheet-generator/grade5-games.html?game=math-quest&unit=fraction-addition-subtraction","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-quest.svg","description":"Unlock six lands on an adventure map by answering correctly. Play alone or as a class. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Treasure Trail: Fraction Concepts and Operations","path":"worksheet-generator/grade5-games.html?game=treasure-trail&unit=fraction-addition-subtraction","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-treasure.svg","description":"Follow the treasure map stone by stone and collect gems. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Space Explorer: Fraction Concepts and Operations","path":"worksheet-generator/grade5-games.html?game=space-explorer&unit=fraction-addition-subtraction","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-space.svg","description":"Earn fuel cells to fly from planet to planet. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Builders: Fraction Concepts and Operations","path":"worksheet-generator/grade5-games.html?game=math-builders&unit=fraction-addition-subtraction","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-builders.svg","description":"Earn a building for your town with every correct answer. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Picture Reveal: Fraction Concepts and Operations","path":"worksheet-generator/grade5-games.html?game=picture-reveal&unit=fraction-addition-subtraction","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-reveal.svg","description":"Uncover tiles to reveal a hidden picture. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Race: Fraction Concepts and Operations","path":"worksheet-generator/grade5-games.html?game=math-race&unit=fraction-addition-subtraction","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-race.svg","description":"Two to four teams race; a correct answer moves the team car one space. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Soccer: Fraction Concepts and Operations","path":"worksheet-generator/grade5-games.html?game=math-soccer&unit=fraction-addition-subtraction","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-soccer.svg","description":"Two teams kick the ball toward the goal with correct answers. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Connect 4: Fraction Concepts and Operations","path":"worksheet-generator/grade5-games.html?game=connect-four&unit=fraction-addition-subtraction","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-connect4.svg","description":"Two teams answer to earn discs. Four in a row wins. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Puzzle Masters: Fraction Concepts and Operations","path":"worksheet-generator/grade5-games.html?game=puzzle-masters&unit=fraction-addition-subtraction","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-puzzle.svg","description":"Flip cards and match each problem to its answer, alone or with a partner. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Fraction Frenzy: Fraction Concepts and Operations","path":"worksheet-generator/grade5-games.html?game=fraction-frenzy&unit=fraction-addition-subtraction","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-frenzy.svg","description":"Match fraction models to fractions, including equivalent fractions and simplest form. Fraction models are drawn exactly from the chosen numbers.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations","Grade 5 game"],"added":"2026-11-11"},{"title":"Flashcards: Fraction Concepts and Operations","path":"worksheet-generator/grade5-flashcards.html?unit=fraction-addition-subtraction","bankFormat":"flashcards","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-flashcards.svg","description":"Colorful flashcards for vocabulary, symbols, big ideas, pictures, rules, mental math and common mistakes.","topics":["Fraction Concepts and Operations"],"added":"2026-11-11"},{"title":"Understanding Check","path":"worksheet-generator/grade5-understanding-check.html?unit=fraction-addition-subtraction","bankFormat":"interactive-practice-test","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-understanding-check.svg","description":"A friendly check of learning: one question at a time or all on one page, hints, worked solutions, review of missed questions and a teacher summary.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations"],"added":"2026-11-11"},{"title":"Understanding Check (Printable Version)","path":"worksheet-generator/practice-test.html#unit=math5-fraction-addition-subtraction","bankFormat":"interactive-practice-test","type":"Study Guide","thumb":"thumbs/practice-test.svg","description":"Build a printable Understanding Check from the Grade 5 bank, with an answer key and a targeted follow-up.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations"],"added":"2026-11-11"},{"title":"Fraction Concepts and Operations Cheat Sheet","path":"artifacts/math5-fraction-addition-subtraction-cheat-sheet/worksheet.pdf","thumb":"thumbs/math5-fraction-addition-subtraction-cheat-sheet.jpg","type":"Printable","description":"Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It! for Fraction Concepts and Operations.","topics":["Cheat sheet","Reference","Fraction Concepts and Operations","Unit 5"],"added":"2026-11-11"},{"title":"Vocabulary Activities and Crosswords","path":"worksheet-generator/printables.html#unit=math5-fraction-addition-subtraction&kind=vocabulary","type":"Printable","thumb":"thumbs/vocabulary-prealgebra.svg","description":"Matching, fill-in-the-blank, examples, and crosswords using the Grade 5 unit vocabulary.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations"],"added":"2026-11-11"},{"title":"Error Analysis Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-addition-subtraction&kind=error","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/error-generator-foundations.svg","description":"Find, explain, and correct mistakes. Includes teacher solutions. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations"],"added":"2026-11-11"},{"title":"Tarsia Puzzle Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-addition-subtraction&kind=tarsia","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/tarsia-generator-foundations.svg","description":"Match problems and answers to assemble a triangle puzzle. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations"],"added":"2026-11-11"},{"title":"Maze Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-addition-subtraction&kind=maze","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/maze-generator-foundations.svg","description":"Follow a route of correctly answered questions through a maze. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations"],"added":"2026-11-11"},{"title":"Color by Number Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-addition-subtraction&kind=color","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/geometry-color-generator-basics-reasoning.svg","description":"Solve problems to reveal a color-coded picture. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations"],"added":"2026-11-11"},{"title":"Partner Check Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-addition-subtraction&kind=partner","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/partner-generator-foundations.svg","description":"Solve and compare matched-answer problems in pairs. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations"],"added":"2026-11-11"},{"title":"Station Work Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-addition-subtraction&kind=stations","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/stations-generator-foundations.svg","description":"Rotate through stations with mixed problem types. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations"],"added":"2026-11-11"},{"title":"Whodunnit Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-addition-subtraction&kind=who","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/foundations-algebra-whodunnit.jpg","description":"Solve clues and narrow down the mystery. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations"],"added":"2026-11-11"},{"title":"Fraction Explorer","path":"artifacts/math5-fraction-explorer/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/math5-fraction-explorer.jpg","description":"Build two fractions with fraction bars, find equivalent fractions and a common denominator, and compare, add or subtract them.","topics":["Fractions","Equivalent fractions","Common denominators"],"worksheet":"artifacts/math5-fraction-explorer/worksheet.pdf","answerKey":"artifacts/math5-fraction-explorer/teacher-key.pdf","added":"2026-11-11"},{"title":"Project: School Garden Plan","path":"artifacts/math5-project-school-garden-plan/index.html","bankFormat":"projects","keepPath":true,"type":"Project","thumb":"thumbs/math5-project-school-garden-plan.jpg","description":"Students design a school garden. They split a garden into fractional sections with unlike denominators, check that the sections make one whole, add and subtract mixed numbers for fence and path lengths, and use benchmark fractions to check that answers are reasonable.","level":["Remedial","Standard","Advanced"],"topics":["Fraction Concepts and Operations","Project","Nature & Gardening"],"added":"2026-11-11"}],"fraction-multiplication-division":[{"title":"Math Quest: Multiplying and Dividing Fractions","path":"worksheet-generator/grade5-games.html?game=math-quest&unit=fraction-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-quest.svg","description":"Unlock six lands on an adventure map by answering correctly. Play alone or as a class. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions","Grade 5 game"],"added":"2026-11-11"},{"title":"Treasure Trail: Multiplying and Dividing Fractions","path":"worksheet-generator/grade5-games.html?game=treasure-trail&unit=fraction-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-treasure.svg","description":"Follow the treasure map stone by stone and collect gems. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions","Grade 5 game"],"added":"2026-11-11"},{"title":"Space Explorer: Multiplying and Dividing Fractions","path":"worksheet-generator/grade5-games.html?game=space-explorer&unit=fraction-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-space.svg","description":"Earn fuel cells to fly from planet to planet. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Builders: Multiplying and Dividing Fractions","path":"worksheet-generator/grade5-games.html?game=math-builders&unit=fraction-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-builders.svg","description":"Earn a building for your town with every correct answer. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions","Grade 5 game"],"added":"2026-11-11"},{"title":"Picture Reveal: Multiplying and Dividing Fractions","path":"worksheet-generator/grade5-games.html?game=picture-reveal&unit=fraction-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-reveal.svg","description":"Uncover tiles to reveal a hidden picture. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Race: Multiplying and Dividing Fractions","path":"worksheet-generator/grade5-games.html?game=math-race&unit=fraction-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-race.svg","description":"Two to four teams race; a correct answer moves the team car one space. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Soccer: Multiplying and Dividing Fractions","path":"worksheet-generator/grade5-games.html?game=math-soccer&unit=fraction-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-soccer.svg","description":"Two teams kick the ball toward the goal with correct answers. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions","Grade 5 game"],"added":"2026-11-11"},{"title":"Connect 4: Multiplying and Dividing Fractions","path":"worksheet-generator/grade5-games.html?game=connect-four&unit=fraction-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-connect4.svg","description":"Two teams answer to earn discs. Four in a row wins. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions","Grade 5 game"],"added":"2026-11-11"},{"title":"Puzzle Masters: Multiplying and Dividing Fractions","path":"worksheet-generator/grade5-games.html?game=puzzle-masters&unit=fraction-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-puzzle.svg","description":"Flip cards and match each problem to its answer, alone or with a partner. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions","Grade 5 game"],"added":"2026-11-11"},{"title":"Fraction Frenzy: Multiplying and Dividing Fractions","path":"worksheet-generator/grade5-games.html?game=fraction-frenzy&unit=fraction-multiplication-division","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-frenzy.svg","description":"Match fraction models to fractions, including equivalent fractions and simplest form. Fraction models are drawn exactly from the chosen numbers.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions","Grade 5 game"],"added":"2026-11-11"},{"title":"Flashcards: Multiplying and Dividing Fractions","path":"worksheet-generator/grade5-flashcards.html?unit=fraction-multiplication-division","bankFormat":"flashcards","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-flashcards.svg","description":"Colorful flashcards for vocabulary, symbols, big ideas, pictures, rules, mental math and common mistakes.","topics":["Multiplying and Dividing Fractions"],"added":"2026-11-11"},{"title":"Understanding Check","path":"worksheet-generator/grade5-understanding-check.html?unit=fraction-multiplication-division","bankFormat":"interactive-practice-test","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-understanding-check.svg","description":"A friendly check of learning: one question at a time or all on one page, hints, worked solutions, review of missed questions and a teacher summary.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions"],"added":"2026-11-11"},{"title":"Understanding Check (Printable Version)","path":"worksheet-generator/practice-test.html#unit=math5-fraction-multiplication-division","bankFormat":"interactive-practice-test","type":"Study Guide","thumb":"thumbs/practice-test.svg","description":"Build a printable Understanding Check from the Grade 5 bank, with an answer key and a targeted follow-up.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions"],"added":"2026-11-11"},{"title":"Multiplying and Dividing Fractions Cheat Sheet","path":"artifacts/math5-fraction-multiplication-division-cheat-sheet/worksheet.pdf","thumb":"thumbs/math5-fraction-multiplication-division-cheat-sheet.jpg","type":"Printable","description":"Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It! for Multiplying and Dividing Fractions.","topics":["Cheat sheet","Reference","Multiplying and Dividing Fractions","Unit 6"],"added":"2026-11-11"},{"title":"Vocabulary Activities and Crosswords","path":"worksheet-generator/printables.html#unit=math5-fraction-multiplication-division&kind=vocabulary","type":"Printable","thumb":"thumbs/vocabulary-prealgebra.svg","description":"Matching, fill-in-the-blank, examples, and crosswords using the Grade 5 unit vocabulary.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions"],"added":"2026-11-11"},{"title":"Error Analysis Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-multiplication-division&kind=error","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/error-generator-foundations.svg","description":"Find, explain, and correct mistakes. Includes teacher solutions. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions"],"added":"2026-11-11"},{"title":"Tarsia Puzzle Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-multiplication-division&kind=tarsia","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/tarsia-generator-foundations.svg","description":"Match problems and answers to assemble a triangle puzzle. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions"],"added":"2026-11-11"},{"title":"Maze Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-multiplication-division&kind=maze","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/maze-generator-foundations.svg","description":"Follow a route of correctly answered questions through a maze. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions"],"added":"2026-11-11"},{"title":"Color by Number Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-multiplication-division&kind=color","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/geometry-color-generator-basics-reasoning.svg","description":"Solve problems to reveal a color-coded picture. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions"],"added":"2026-11-11"},{"title":"Partner Check Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-multiplication-division&kind=partner","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/partner-generator-foundations.svg","description":"Solve and compare matched-answer problems in pairs. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions"],"added":"2026-11-11"},{"title":"Station Work Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-multiplication-division&kind=stations","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/stations-generator-foundations.svg","description":"Rotate through stations with mixed problem types. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions"],"added":"2026-11-11"},{"title":"Whodunnit Generator","path":"worksheet-generator/printables.html#unit=math5-fraction-multiplication-division&kind=who","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/foundations-algebra-whodunnit.jpg","description":"Solve clues and narrow down the mystery. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions"],"added":"2026-11-11"},{"title":"Project: Recipe Remix","path":"artifacts/math5-project-recipe-remix/index.html","bankFormat":"projects","keepPath":true,"type":"Project","thumb":"thumbs/math5-project-recipe-remix.jpg","description":"Students run a cooking club. They scale a recipe by whole numbers, fractions and mixed numbers, explain scaling, interpret fractions as division when sharing, and divide whole numbers by unit fractions to find servings.","level":["Remedial","Standard","Advanced"],"topics":["Multiplying and Dividing Fractions","Project","Food & Cooking"],"added":"2026-11-11"},{"title":"Area Model Explorer","path":"artifacts/math5-area-model-explorer/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/math5-area-model-explorer.jpg","description":"Split rectangles into partial products to multiply two-digit numbers, then switch to fractions and multiply parts of a whole.","topics":["Area model","Partial products","Multiplying fractions"],"worksheet":"artifacts/math5-area-model-explorer/worksheet.pdf","answerKey":"artifacts/math5-area-model-explorer/teacher-key.pdf","added":"2026-11-11"},{"title":"Fraction Explorer","path":"artifacts/math5-fraction-explorer/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/math5-fraction-explorer.jpg","description":"Build two fractions with fraction bars, find equivalent fractions and a common denominator, and compare, add or subtract them.","topics":["Fractions","Equivalent fractions","Common denominators"],"worksheet":"artifacts/math5-fraction-explorer/worksheet.pdf","answerKey":"artifacts/math5-fraction-explorer/teacher-key.pdf","added":"2026-11-11"}],"measurement-conversions":[{"title":"Math Quest: Measurement and Conversions","path":"worksheet-generator/grade5-games.html?game=math-quest&unit=measurement-conversions","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-quest.svg","description":"Unlock six lands on an adventure map by answering correctly. Play alone or as a class. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions","Grade 5 game"],"added":"2026-11-11"},{"title":"Treasure Trail: Measurement and Conversions","path":"worksheet-generator/grade5-games.html?game=treasure-trail&unit=measurement-conversions","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-treasure.svg","description":"Follow the treasure map stone by stone and collect gems. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions","Grade 5 game"],"added":"2026-11-11"},{"title":"Space Explorer: Measurement and Conversions","path":"worksheet-generator/grade5-games.html?game=space-explorer&unit=measurement-conversions","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-space.svg","description":"Earn fuel cells to fly from planet to planet. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Builders: Measurement and Conversions","path":"worksheet-generator/grade5-games.html?game=math-builders&unit=measurement-conversions","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-builders.svg","description":"Earn a building for your town with every correct answer. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions","Grade 5 game"],"added":"2026-11-11"},{"title":"Picture Reveal: Measurement and Conversions","path":"worksheet-generator/grade5-games.html?game=picture-reveal&unit=measurement-conversions","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-reveal.svg","description":"Uncover tiles to reveal a hidden picture. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Race: Measurement and Conversions","path":"worksheet-generator/grade5-games.html?game=math-race&unit=measurement-conversions","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-race.svg","description":"Two to four teams race; a correct answer moves the team car one space. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Soccer: Measurement and Conversions","path":"worksheet-generator/grade5-games.html?game=math-soccer&unit=measurement-conversions","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-soccer.svg","description":"Two teams kick the ball toward the goal with correct answers. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions","Grade 5 game"],"added":"2026-11-11"},{"title":"Connect 4: Measurement and Conversions","path":"worksheet-generator/grade5-games.html?game=connect-four&unit=measurement-conversions","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-connect4.svg","description":"Two teams answer to earn discs. Four in a row wins. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions","Grade 5 game"],"added":"2026-11-11"},{"title":"Puzzle Masters: Measurement and Conversions","path":"worksheet-generator/grade5-games.html?game=puzzle-masters&unit=measurement-conversions","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-puzzle.svg","description":"Flip cards and match each problem to its answer, alone or with a partner. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions","Grade 5 game"],"added":"2026-11-11"},{"title":"Flashcards: Measurement and Conversions","path":"worksheet-generator/grade5-flashcards.html?unit=measurement-conversions","bankFormat":"flashcards","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-flashcards.svg","description":"Colorful flashcards for vocabulary, symbols, big ideas, pictures, rules, mental math and common mistakes.","topics":["Measurement and Conversions"],"added":"2026-11-11"},{"title":"Understanding Check","path":"worksheet-generator/grade5-understanding-check.html?unit=measurement-conversions","bankFormat":"interactive-practice-test","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-understanding-check.svg","description":"A friendly check of learning: one question at a time or all on one page, hints, worked solutions, review of missed questions and a teacher summary.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions"],"added":"2026-11-11"},{"title":"Understanding Check (Printable Version)","path":"worksheet-generator/practice-test.html#unit=math5-measurement-conversions","bankFormat":"interactive-practice-test","type":"Study Guide","thumb":"thumbs/practice-test.svg","description":"Build a printable Understanding Check from the Grade 5 bank, with an answer key and a targeted follow-up.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions"],"added":"2026-11-11"},{"title":"Measurement and Conversions Cheat Sheet","path":"artifacts/math5-measurement-conversions-cheat-sheet/worksheet.pdf","thumb":"thumbs/math5-measurement-conversions-cheat-sheet.jpg","type":"Printable","description":"Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It! for Measurement and Conversions.","topics":["Cheat sheet","Reference","Measurement and Conversions","Unit 7"],"added":"2026-11-11"},{"title":"Vocabulary Activities and Crosswords","path":"worksheet-generator/printables.html#unit=math5-measurement-conversions&kind=vocabulary","type":"Printable","thumb":"thumbs/vocabulary-prealgebra.svg","description":"Matching, fill-in-the-blank, examples, and crosswords using the Grade 5 unit vocabulary.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions"],"added":"2026-11-11"},{"title":"Error Analysis Generator","path":"worksheet-generator/printables.html#unit=math5-measurement-conversions&kind=error","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/error-generator-foundations.svg","description":"Find, explain, and correct mistakes. Includes teacher solutions. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions"],"added":"2026-11-11"},{"title":"Tarsia Puzzle Generator","path":"worksheet-generator/printables.html#unit=math5-measurement-conversions&kind=tarsia","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/tarsia-generator-foundations.svg","description":"Match problems and answers to assemble a triangle puzzle. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions"],"added":"2026-11-11"},{"title":"Maze Generator","path":"worksheet-generator/printables.html#unit=math5-measurement-conversions&kind=maze","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/maze-generator-foundations.svg","description":"Follow a route of correctly answered questions through a maze. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions"],"added":"2026-11-11"},{"title":"Color by Number Generator","path":"worksheet-generator/printables.html#unit=math5-measurement-conversions&kind=color","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/geometry-color-generator-basics-reasoning.svg","description":"Solve problems to reveal a color-coded picture. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions"],"added":"2026-11-11"},{"title":"Partner Check Generator","path":"worksheet-generator/printables.html#unit=math5-measurement-conversions&kind=partner","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/partner-generator-foundations.svg","description":"Solve and compare matched-answer problems in pairs. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions"],"added":"2026-11-11"},{"title":"Station Work Generator","path":"worksheet-generator/printables.html#unit=math5-measurement-conversions&kind=stations","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/stations-generator-foundations.svg","description":"Rotate through stations with mixed problem types. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions"],"added":"2026-11-11"},{"title":"Whodunnit Generator","path":"worksheet-generator/printables.html#unit=math5-measurement-conversions&kind=who","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/foundations-algebra-whodunnit.jpg","description":"Solve clues and narrow down the mystery. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions"],"added":"2026-11-11"},{"title":"Measurement Converter","path":"artifacts/math5-measurement-converter/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/math5-measurement-converter.jpg","description":"Convert customary and metric measurements, see the conversion fact as a picture, and decide when to multiply or divide.","topics":["Measurement","Unit conversion","Customary and metric units"],"worksheet":"artifacts/math5-measurement-converter/worksheet.pdf","answerKey":"artifacts/math5-measurement-converter/teacher-key.pdf","added":"2026-11-11"},{"title":"Project: Field Trip Packing List","path":"artifacts/math5-project-field-trip-packing/index.html","bankFormat":"projects","keepPath":true,"type":"Project","thumb":"thumbs/math5-project-field-trip-packing.jpg","description":"Students pack for a nature field trip. They convert gallons of water to cups, feet of rope to inches, pounds to ounces for backpack weight, and metric distances, solving multi-step problems with regrouping.","level":["Remedial","Standard","Advanced"],"topics":["Measurement and Conversions","Project","Outdoors & Science"],"added":"2026-11-11"}],"volume-three-dimensional-figures":[{"title":"Math Quest: Volume and Three-Dimensional Figures","path":"worksheet-generator/grade5-games.html?game=math-quest&unit=volume-three-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-quest.svg","description":"Unlock six lands on an adventure map by answering correctly. Play alone or as a class. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures","Grade 5 game"],"added":"2026-11-11"},{"title":"Treasure Trail: Volume and Three-Dimensional Figures","path":"worksheet-generator/grade5-games.html?game=treasure-trail&unit=volume-three-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-treasure.svg","description":"Follow the treasure map stone by stone and collect gems. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures","Grade 5 game"],"added":"2026-11-11"},{"title":"Space Explorer: Volume and Three-Dimensional Figures","path":"worksheet-generator/grade5-games.html?game=space-explorer&unit=volume-three-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-space.svg","description":"Earn fuel cells to fly from planet to planet. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Builders: Volume and Three-Dimensional Figures","path":"worksheet-generator/grade5-games.html?game=math-builders&unit=volume-three-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-builders.svg","description":"Earn a building for your town with every correct answer. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures","Grade 5 game"],"added":"2026-11-11"},{"title":"Picture Reveal: Volume and Three-Dimensional Figures","path":"worksheet-generator/grade5-games.html?game=picture-reveal&unit=volume-three-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-reveal.svg","description":"Uncover tiles to reveal a hidden picture. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Race: Volume and Three-Dimensional Figures","path":"worksheet-generator/grade5-games.html?game=math-race&unit=volume-three-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-race.svg","description":"Two to four teams race; a correct answer moves the team car one space. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Soccer: Volume and Three-Dimensional Figures","path":"worksheet-generator/grade5-games.html?game=math-soccer&unit=volume-three-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-soccer.svg","description":"Two teams kick the ball toward the goal with correct answers. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures","Grade 5 game"],"added":"2026-11-11"},{"title":"Connect 4: Volume and Three-Dimensional Figures","path":"worksheet-generator/grade5-games.html?game=connect-four&unit=volume-three-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-connect4.svg","description":"Two teams answer to earn discs. Four in a row wins. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures","Grade 5 game"],"added":"2026-11-11"},{"title":"Puzzle Masters: Volume and Three-Dimensional Figures","path":"worksheet-generator/grade5-games.html?game=puzzle-masters&unit=volume-three-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-puzzle.svg","description":"Flip cards and match each problem to its answer, alone or with a partner. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures","Grade 5 game"],"added":"2026-11-11"},{"title":"Flashcards: Volume and Three-Dimensional Figures","path":"worksheet-generator/grade5-flashcards.html?unit=volume-three-dimensional-figures","bankFormat":"flashcards","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-flashcards.svg","description":"Colorful flashcards for vocabulary, symbols, big ideas, pictures, rules, mental math and common mistakes.","topics":["Volume and Three-Dimensional Figures"],"added":"2026-11-11"},{"title":"Understanding Check","path":"worksheet-generator/grade5-understanding-check.html?unit=volume-three-dimensional-figures","bankFormat":"interactive-practice-test","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-understanding-check.svg","description":"A friendly check of learning: one question at a time or all on one page, hints, worked solutions, review of missed questions and a teacher summary.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures"],"added":"2026-11-11"},{"title":"Understanding Check (Printable Version)","path":"worksheet-generator/practice-test.html#unit=math5-volume-three-dimensional-figures","bankFormat":"interactive-practice-test","type":"Study Guide","thumb":"thumbs/practice-test.svg","description":"Build a printable Understanding Check from the Grade 5 bank, with an answer key and a targeted follow-up.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures"],"added":"2026-11-11"},{"title":"Volume and Three-Dimensional Figures Cheat Sheet","path":"artifacts/math5-volume-three-dimensional-figures-cheat-sheet/worksheet.pdf","thumb":"thumbs/math5-volume-three-dimensional-figures-cheat-sheet.jpg","type":"Printable","description":"Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It! for Volume and Three-Dimensional Figures.","topics":["Cheat sheet","Reference","Volume and Three-Dimensional Figures","Unit 8"],"added":"2026-11-11"},{"title":"Vocabulary Activities and Crosswords","path":"worksheet-generator/printables.html#unit=math5-volume-three-dimensional-figures&kind=vocabulary","type":"Printable","thumb":"thumbs/vocabulary-prealgebra.svg","description":"Matching, fill-in-the-blank, examples, and crosswords using the Grade 5 unit vocabulary.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures"],"added":"2026-11-11"},{"title":"Error Analysis Generator","path":"worksheet-generator/printables.html#unit=math5-volume-three-dimensional-figures&kind=error","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/error-generator-foundations.svg","description":"Find, explain, and correct mistakes. Includes teacher solutions. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures"],"added":"2026-11-11"},{"title":"Tarsia Puzzle Generator","path":"worksheet-generator/printables.html#unit=math5-volume-three-dimensional-figures&kind=tarsia","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/tarsia-generator-foundations.svg","description":"Match problems and answers to assemble a triangle puzzle. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures"],"added":"2026-11-11"},{"title":"Maze Generator","path":"worksheet-generator/printables.html#unit=math5-volume-three-dimensional-figures&kind=maze","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/maze-generator-foundations.svg","description":"Follow a route of correctly answered questions through a maze. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures"],"added":"2026-11-11"},{"title":"Color by Number Generator","path":"worksheet-generator/printables.html#unit=math5-volume-three-dimensional-figures&kind=color","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/geometry-color-generator-basics-reasoning.svg","description":"Solve problems to reveal a color-coded picture. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures"],"added":"2026-11-11"},{"title":"Partner Check Generator","path":"worksheet-generator/printables.html#unit=math5-volume-three-dimensional-figures&kind=partner","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/partner-generator-foundations.svg","description":"Solve and compare matched-answer problems in pairs. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures"],"added":"2026-11-11"},{"title":"Station Work Generator","path":"worksheet-generator/printables.html#unit=math5-volume-three-dimensional-figures&kind=stations","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/stations-generator-foundations.svg","description":"Rotate through stations with mixed problem types. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures"],"added":"2026-11-11"},{"title":"Whodunnit Generator","path":"worksheet-generator/printables.html#unit=math5-volume-three-dimensional-figures&kind=who","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/foundations-algebra-whodunnit.jpg","description":"Solve clues and narrow down the mystery. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures"],"added":"2026-11-11"},{"title":"Volume Builder","path":"artifacts/math5-volume-builder/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/math5-volume-builder.jpg","description":"Stack unit cubes into rectangular prisms, see layers and base area, and connect counting cubes to V = l × w × h and composite figures.","topics":["Volume","Unit cubes","Composite figures"],"worksheet":"artifacts/math5-volume-builder/worksheet.pdf","answerKey":"artifacts/math5-volume-builder/teacher-key.pdf","added":"2026-11-11"},{"title":"Project: Miniature City Builder","path":"artifacts/math5-project-miniature-city-builder/index.html","bankFormat":"projects","keepPath":true,"type":"Project","thumb":"thumbs/math5-project-miniature-city-builder.jpg","description":"Students design a miniature city. They build rectangular-prism buildings from unit cubes, find volumes with V = l × w × h and V = B × h, find volumes of L-shaped (composite) buildings, and plan how many boxes fit in a delivery truck.","level":["Remedial","Standard","Advanced"],"topics":["Volume and Three-Dimensional Figures","Project","Design & Engineering"],"added":"2026-11-11"}],"coordinate-plane-graphing":[{"title":"Math Quest: Coordinate Planes and Graphing","path":"worksheet-generator/grade5-games.html?game=math-quest&unit=coordinate-plane-graphing","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-quest.svg","description":"Unlock six lands on an adventure map by answering correctly. Play alone or as a class. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing","Grade 5 game"],"added":"2026-11-11"},{"title":"Treasure Trail: Coordinate Planes and Graphing","path":"worksheet-generator/grade5-games.html?game=treasure-trail&unit=coordinate-plane-graphing","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-treasure.svg","description":"Follow the treasure map stone by stone and collect gems. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing","Grade 5 game"],"added":"2026-11-11"},{"title":"Space Explorer: Coordinate Planes and Graphing","path":"worksheet-generator/grade5-games.html?game=space-explorer&unit=coordinate-plane-graphing","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-space.svg","description":"Earn fuel cells to fly from planet to planet. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Builders: Coordinate Planes and Graphing","path":"worksheet-generator/grade5-games.html?game=math-builders&unit=coordinate-plane-graphing","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-builders.svg","description":"Earn a building for your town with every correct answer. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing","Grade 5 game"],"added":"2026-11-11"},{"title":"Picture Reveal: Coordinate Planes and Graphing","path":"worksheet-generator/grade5-games.html?game=picture-reveal&unit=coordinate-plane-graphing","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-reveal.svg","description":"Uncover tiles to reveal a hidden picture. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Race: Coordinate Planes and Graphing","path":"worksheet-generator/grade5-games.html?game=math-race&unit=coordinate-plane-graphing","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-race.svg","description":"Two to four teams race; a correct answer moves the team car one space. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Soccer: Coordinate Planes and Graphing","path":"worksheet-generator/grade5-games.html?game=math-soccer&unit=coordinate-plane-graphing","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-soccer.svg","description":"Two teams kick the ball toward the goal with correct answers. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing","Grade 5 game"],"added":"2026-11-11"},{"title":"Connect 4: Coordinate Planes and Graphing","path":"worksheet-generator/grade5-games.html?game=connect-four&unit=coordinate-plane-graphing","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-connect4.svg","description":"Two teams answer to earn discs. Four in a row wins. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing","Grade 5 game"],"added":"2026-11-11"},{"title":"Puzzle Masters: Coordinate Planes and Graphing","path":"worksheet-generator/grade5-games.html?game=puzzle-masters&unit=coordinate-plane-graphing","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-puzzle.svg","description":"Flip cards and match each problem to its answer, alone or with a partner. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing","Grade 5 game"],"added":"2026-11-11"},{"title":"Flashcards: Coordinate Planes and Graphing","path":"worksheet-generator/grade5-flashcards.html?unit=coordinate-plane-graphing","bankFormat":"flashcards","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-flashcards.svg","description":"Colorful flashcards for vocabulary, symbols, big ideas, pictures, rules, mental math and common mistakes.","topics":["Coordinate Planes and Graphing"],"added":"2026-11-11"},{"title":"Understanding Check","path":"worksheet-generator/grade5-understanding-check.html?unit=coordinate-plane-graphing","bankFormat":"interactive-practice-test","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-understanding-check.svg","description":"A friendly check of learning: one question at a time or all on one page, hints, worked solutions, review of missed questions and a teacher summary.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing"],"added":"2026-11-11"},{"title":"Understanding Check (Printable Version)","path":"worksheet-generator/practice-test.html#unit=math5-coordinate-plane-graphing","bankFormat":"interactive-practice-test","type":"Study Guide","thumb":"thumbs/practice-test.svg","description":"Build a printable Understanding Check from the Grade 5 bank, with an answer key and a targeted follow-up.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing"],"added":"2026-11-11"},{"title":"Coordinate Planes and Graphing Cheat Sheet","path":"artifacts/math5-coordinate-plane-graphing-cheat-sheet/worksheet.pdf","thumb":"thumbs/math5-coordinate-plane-graphing-cheat-sheet.jpg","type":"Printable","description":"Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It! for Coordinate Planes and Graphing.","topics":["Cheat sheet","Reference","Coordinate Planes and Graphing","Unit 9"],"added":"2026-11-11"},{"title":"Vocabulary Activities and Crosswords","path":"worksheet-generator/printables.html#unit=math5-coordinate-plane-graphing&kind=vocabulary","type":"Printable","thumb":"thumbs/vocabulary-prealgebra.svg","description":"Matching, fill-in-the-blank, examples, and crosswords using the Grade 5 unit vocabulary.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing"],"added":"2026-11-11"},{"title":"Error Analysis Generator","path":"worksheet-generator/printables.html#unit=math5-coordinate-plane-graphing&kind=error","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/error-generator-foundations.svg","description":"Find, explain, and correct mistakes. Includes teacher solutions. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing"],"added":"2026-11-11"},{"title":"Tarsia Puzzle Generator","path":"worksheet-generator/printables.html#unit=math5-coordinate-plane-graphing&kind=tarsia","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/tarsia-generator-foundations.svg","description":"Match problems and answers to assemble a triangle puzzle. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing"],"added":"2026-11-11"},{"title":"Maze Generator","path":"worksheet-generator/printables.html#unit=math5-coordinate-plane-graphing&kind=maze","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/maze-generator-foundations.svg","description":"Follow a route of correctly answered questions through a maze. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing"],"added":"2026-11-11"},{"title":"Color by Number Generator","path":"worksheet-generator/printables.html#unit=math5-coordinate-plane-graphing&kind=color","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/geometry-color-generator-basics-reasoning.svg","description":"Solve problems to reveal a color-coded picture. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing"],"added":"2026-11-11"},{"title":"Partner Check Generator","path":"worksheet-generator/printables.html#unit=math5-coordinate-plane-graphing&kind=partner","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/partner-generator-foundations.svg","description":"Solve and compare matched-answer problems in pairs. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing"],"added":"2026-11-11"},{"title":"Station Work Generator","path":"worksheet-generator/printables.html#unit=math5-coordinate-plane-graphing&kind=stations","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/stations-generator-foundations.svg","description":"Rotate through stations with mixed problem types. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing"],"added":"2026-11-11"},{"title":"Whodunnit Generator","path":"worksheet-generator/printables.html#unit=math5-coordinate-plane-graphing&kind=who","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/foundations-algebra-whodunnit.jpg","description":"Solve clues and narrow down the mystery. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing"],"added":"2026-11-11"},{"title":"Coordinate Plane Explorer","path":"artifacts/math5-coordinate-explorer/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/math5-coordinate-explorer.jpg","description":"Plot points in the first quadrant by clicking or typing, connect them into shapes, measure distances along grid lines, and graph two-rule patterns.","topics":["Coordinate plane","Ordered pairs","Patterns"],"worksheet":"artifacts/math5-coordinate-explorer/worksheet.pdf","answerKey":"artifacts/math5-coordinate-explorer/teacher-key.pdf","added":"2026-11-11"},{"title":"Project: Playground Designer","path":"artifacts/math5-project-playground-designer/index.html","bankFormat":"projects","keepPath":true,"type":"Project","thumb":"thumbs/math5-project-playground-designer.jpg","description":"Students design a playground on a coordinate grid. They plot equipment at ordered pairs, find distances along grid lines, find the fourth corner and perimeter of rectangular areas, and interpret a graph of visitors over time.","level":["Remedial","Standard","Advanced"],"topics":["Coordinate Planes and Graphing","Project","Design & Community"],"added":"2026-11-11"}],"classifying-two-dimensional-figures":[{"title":"Math Quest: Geometry and Classifying Shapes","path":"worksheet-generator/grade5-games.html?game=math-quest&unit=classifying-two-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-quest.svg","description":"Unlock six lands on an adventure map by answering correctly. Play alone or as a class. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes","Grade 5 game"],"added":"2026-11-11"},{"title":"Treasure Trail: Geometry and Classifying Shapes","path":"worksheet-generator/grade5-games.html?game=treasure-trail&unit=classifying-two-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-treasure.svg","description":"Follow the treasure map stone by stone and collect gems. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes","Grade 5 game"],"added":"2026-11-11"},{"title":"Space Explorer: Geometry and Classifying Shapes","path":"worksheet-generator/grade5-games.html?game=space-explorer&unit=classifying-two-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-space.svg","description":"Earn fuel cells to fly from planet to planet. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Builders: Geometry and Classifying Shapes","path":"worksheet-generator/grade5-games.html?game=math-builders&unit=classifying-two-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-builders.svg","description":"Earn a building for your town with every correct answer. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes","Grade 5 game"],"added":"2026-11-11"},{"title":"Picture Reveal: Geometry and Classifying Shapes","path":"worksheet-generator/grade5-games.html?game=picture-reveal&unit=classifying-two-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-reveal.svg","description":"Uncover tiles to reveal a hidden picture. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Race: Geometry and Classifying Shapes","path":"worksheet-generator/grade5-games.html?game=math-race&unit=classifying-two-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-race.svg","description":"Two to four teams race; a correct answer moves the team car one space. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Soccer: Geometry and Classifying Shapes","path":"worksheet-generator/grade5-games.html?game=math-soccer&unit=classifying-two-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-soccer.svg","description":"Two teams kick the ball toward the goal with correct answers. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes","Grade 5 game"],"added":"2026-11-11"},{"title":"Connect 4: Geometry and Classifying Shapes","path":"worksheet-generator/grade5-games.html?game=connect-four&unit=classifying-two-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-connect4.svg","description":"Two teams answer to earn discs. Four in a row wins. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes","Grade 5 game"],"added":"2026-11-11"},{"title":"Puzzle Masters: Geometry and Classifying Shapes","path":"worksheet-generator/grade5-games.html?game=puzzle-masters&unit=classifying-two-dimensional-figures","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-puzzle.svg","description":"Flip cards and match each problem to its answer, alone or with a partner. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes","Grade 5 game"],"added":"2026-11-11"},{"title":"Flashcards: Geometry and Classifying Shapes","path":"worksheet-generator/grade5-flashcards.html?unit=classifying-two-dimensional-figures","bankFormat":"flashcards","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-flashcards.svg","description":"Colorful flashcards for vocabulary, symbols, big ideas, pictures, rules, mental math and common mistakes.","topics":["Geometry and Classifying Shapes"],"added":"2026-11-11"},{"title":"Understanding Check","path":"worksheet-generator/grade5-understanding-check.html?unit=classifying-two-dimensional-figures","bankFormat":"interactive-practice-test","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-understanding-check.svg","description":"A friendly check of learning: one question at a time or all on one page, hints, worked solutions, review of missed questions and a teacher summary.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes"],"added":"2026-11-11"},{"title":"Understanding Check (Printable Version)","path":"worksheet-generator/practice-test.html#unit=math5-classifying-two-dimensional-figures","bankFormat":"interactive-practice-test","type":"Study Guide","thumb":"thumbs/practice-test.svg","description":"Build a printable Understanding Check from the Grade 5 bank, with an answer key and a targeted follow-up.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes"],"added":"2026-11-11"},{"title":"Geometry and Classifying Shapes Cheat Sheet","path":"artifacts/math5-classifying-two-dimensional-figures-cheat-sheet/worksheet.pdf","thumb":"thumbs/math5-classifying-two-dimensional-figures-cheat-sheet.jpg","type":"Printable","description":"Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It! for Geometry and Classifying Shapes.","topics":["Cheat sheet","Reference","Geometry and Classifying Shapes","Unit 10"],"added":"2026-11-11"},{"title":"Vocabulary Activities and Crosswords","path":"worksheet-generator/printables.html#unit=math5-classifying-two-dimensional-figures&kind=vocabulary","type":"Printable","thumb":"thumbs/vocabulary-prealgebra.svg","description":"Matching, fill-in-the-blank, examples, and crosswords using the Grade 5 unit vocabulary.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes"],"added":"2026-11-11"},{"title":"Error Analysis Generator","path":"worksheet-generator/printables.html#unit=math5-classifying-two-dimensional-figures&kind=error","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/error-generator-foundations.svg","description":"Find, explain, and correct mistakes. Includes teacher solutions. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes"],"added":"2026-11-11"},{"title":"Tarsia Puzzle Generator","path":"worksheet-generator/printables.html#unit=math5-classifying-two-dimensional-figures&kind=tarsia","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/tarsia-generator-foundations.svg","description":"Match problems and answers to assemble a triangle puzzle. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes"],"added":"2026-11-11"},{"title":"Maze Generator","path":"worksheet-generator/printables.html#unit=math5-classifying-two-dimensional-figures&kind=maze","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/maze-generator-foundations.svg","description":"Follow a route of correctly answered questions through a maze. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes"],"added":"2026-11-11"},{"title":"Color by Number Generator","path":"worksheet-generator/printables.html#unit=math5-classifying-two-dimensional-figures&kind=color","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/geometry-color-generator-basics-reasoning.svg","description":"Solve problems to reveal a color-coded picture. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes"],"added":"2026-11-11"},{"title":"Partner Check Generator","path":"worksheet-generator/printables.html#unit=math5-classifying-two-dimensional-figures&kind=partner","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/partner-generator-foundations.svg","description":"Solve and compare matched-answer problems in pairs. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes"],"added":"2026-11-11"},{"title":"Station Work Generator","path":"worksheet-generator/printables.html#unit=math5-classifying-two-dimensional-figures&kind=stations","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/stations-generator-foundations.svg","description":"Rotate through stations with mixed problem types. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes"],"added":"2026-11-11"},{"title":"Whodunnit Generator","path":"worksheet-generator/printables.html#unit=math5-classifying-two-dimensional-figures&kind=who","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/foundations-algebra-whodunnit.jpg","description":"Solve clues and narrow down the mystery. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes"],"added":"2026-11-11"},{"title":"Project: Shape Mosaic Designer","path":"artifacts/math5-project-shape-mosaic-designer/index.html","bankFormat":"projects","keepPath":true,"type":"Project","thumb":"thumbs/math5-project-shape-mosaic-designer.jpg","description":"Students design a mosaic for the school entrance. They classify triangles by sides and angles, classify quadrilaterals by their properties, use the shape hierarchy to explain how shapes are related, and describe regular polygons.","level":["Remedial","Standard","Advanced"],"topics":["Geometry and Classifying Shapes","Project","Art & Design"],"added":"2026-11-11"}],"data-line-plots-problem-solving":[{"title":"Math Quest: Data, Line Plots, and Problem Solving","path":"worksheet-generator/grade5-games.html?game=math-quest&unit=data-line-plots-problem-solving","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-quest.svg","description":"Unlock six lands on an adventure map by answering correctly. Play alone or as a class. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving","Grade 5 game"],"added":"2026-11-11"},{"title":"Treasure Trail: Data, Line Plots, and Problem Solving","path":"worksheet-generator/grade5-games.html?game=treasure-trail&unit=data-line-plots-problem-solving","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-treasure.svg","description":"Follow the treasure map stone by stone and collect gems. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving","Grade 5 game"],"added":"2026-11-11"},{"title":"Space Explorer: Data, Line Plots, and Problem Solving","path":"worksheet-generator/grade5-games.html?game=space-explorer&unit=data-line-plots-problem-solving","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-space.svg","description":"Earn fuel cells to fly from planet to planet. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Builders: Data, Line Plots, and Problem Solving","path":"worksheet-generator/grade5-games.html?game=math-builders&unit=data-line-plots-problem-solving","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-builders.svg","description":"Earn a building for your town with every correct answer. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving","Grade 5 game"],"added":"2026-11-11"},{"title":"Picture Reveal: Data, Line Plots, and Problem Solving","path":"worksheet-generator/grade5-games.html?game=picture-reveal&unit=data-line-plots-problem-solving","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-reveal.svg","description":"Uncover tiles to reveal a hidden picture. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Race: Data, Line Plots, and Problem Solving","path":"worksheet-generator/grade5-games.html?game=math-race&unit=data-line-plots-problem-solving","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-race.svg","description":"Two to four teams race; a correct answer moves the team car one space. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving","Grade 5 game"],"added":"2026-11-11"},{"title":"Math Soccer: Data, Line Plots, and Problem Solving","path":"worksheet-generator/grade5-games.html?game=math-soccer&unit=data-line-plots-problem-solving","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-soccer.svg","description":"Two teams kick the ball toward the goal with correct answers. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving","Grade 5 game"],"added":"2026-11-11"},{"title":"Connect 4: Data, Line Plots, and Problem Solving","path":"worksheet-generator/grade5-games.html?game=connect-four&unit=data-line-plots-problem-solving","bankFormat":"topic-games","keepPath":true,"gameMode":"Team Games","type":"Game","thumb":"thumbs/math5-game-connect4.svg","description":"Two teams answer to earn discs. Four in a row wins. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving","Grade 5 game"],"added":"2026-11-11"},{"title":"Puzzle Masters: Data, Line Plots, and Problem Solving","path":"worksheet-generator/grade5-games.html?game=puzzle-masters&unit=data-line-plots-problem-solving","bankFormat":"topic-games","keepPath":true,"gameMode":"Individual Review","type":"Game","thumb":"thumbs/math5-game-puzzle.svg","description":"Flip cards and match each problem to its answer, alone or with a partner. Remedial, Standard and Advanced questions from the Grade 5 bank.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving","Grade 5 game"],"added":"2026-11-11"},{"title":"Flashcards: Data, Line Plots, and Problem Solving","path":"worksheet-generator/grade5-flashcards.html?unit=data-line-plots-problem-solving","bankFormat":"flashcards","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-flashcards.svg","description":"Colorful flashcards for vocabulary, symbols, big ideas, pictures, rules, mental math and common mistakes.","topics":["Data, Line Plots, and Problem Solving"],"added":"2026-11-11"},{"title":"Understanding Check","path":"worksheet-generator/grade5-understanding-check.html?unit=data-line-plots-problem-solving","bankFormat":"interactive-practice-test","keepPath":true,"type":"Study Guide","thumb":"thumbs/math5-understanding-check.svg","description":"A friendly check of learning: one question at a time or all on one page, hints, worked solutions, review of missed questions and a teacher summary.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving"],"added":"2026-11-11"},{"title":"Understanding Check (Printable Version)","path":"worksheet-generator/practice-test.html#unit=math5-data-line-plots-problem-solving","bankFormat":"interactive-practice-test","type":"Study Guide","thumb":"thumbs/practice-test.svg","description":"Build a printable Understanding Check from the Grade 5 bank, with an answer key and a targeted follow-up.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving"],"added":"2026-11-11"},{"title":"Data, Line Plots, and Problem Solving Cheat Sheet","path":"artifacts/math5-data-line-plots-problem-solving-cheat-sheet/worksheet.pdf","thumb":"thumbs/math5-data-line-plots-problem-solving-cheat-sheet.jpg","type":"Printable","description":"Two-page colorful cheat sheet: Big Idea, vocabulary, How It Works, visual models, Remember This, Watch Out! and Try It! for Data, Line Plots, and Problem Solving.","topics":["Cheat sheet","Reference","Data, Line Plots, and Problem Solving","Unit 11"],"added":"2026-11-11"},{"title":"Vocabulary Activities and Crosswords","path":"worksheet-generator/printables.html#unit=math5-data-line-plots-problem-solving&kind=vocabulary","type":"Printable","thumb":"thumbs/vocabulary-prealgebra.svg","description":"Matching, fill-in-the-blank, examples, and crosswords using the Grade 5 unit vocabulary.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving"],"added":"2026-11-11"},{"title":"Error Analysis Generator","path":"worksheet-generator/printables.html#unit=math5-data-line-plots-problem-solving&kind=error","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/error-generator-foundations.svg","description":"Find, explain, and correct mistakes. Includes teacher solutions. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving"],"added":"2026-11-11"},{"title":"Tarsia Puzzle Generator","path":"worksheet-generator/printables.html#unit=math5-data-line-plots-problem-solving&kind=tarsia","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/tarsia-generator-foundations.svg","description":"Match problems and answers to assemble a triangle puzzle. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving"],"added":"2026-11-11"},{"title":"Maze Generator","path":"worksheet-generator/printables.html#unit=math5-data-line-plots-problem-solving&kind=maze","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/maze-generator-foundations.svg","description":"Follow a route of correctly answered questions through a maze. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving"],"added":"2026-11-11"},{"title":"Color by Number Generator","path":"worksheet-generator/printables.html#unit=math5-data-line-plots-problem-solving&kind=color","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/geometry-color-generator-basics-reasoning.svg","description":"Solve problems to reveal a color-coded picture. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving"],"added":"2026-11-11"},{"title":"Partner Check Generator","path":"worksheet-generator/printables.html#unit=math5-data-line-plots-problem-solving&kind=partner","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/partner-generator-foundations.svg","description":"Solve and compare matched-answer problems in pairs. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving"],"added":"2026-11-11"},{"title":"Station Work Generator","path":"worksheet-generator/printables.html#unit=math5-data-line-plots-problem-solving&kind=stations","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/stations-generator-foundations.svg","description":"Rotate through stations with mixed problem types. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving"],"added":"2026-11-11"},{"title":"Whodunnit Generator","path":"worksheet-generator/printables.html#unit=math5-data-line-plots-problem-solving&kind=who","bankFormat":"printable-generator","type":"Printable","thumb":"thumbs/foundations-algebra-whodunnit.jpg","description":"Solve clues and narrow down the mystery. Uses Grade 5 questions and a teacher key.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving"],"added":"2026-11-11"},{"title":"Project: Plant Growth Investigation","path":"artifacts/math5-project-plant-growth-investigation/index.html","bankFormat":"projects","keepPath":true,"type":"Project","thumb":"thumbs/math5-project-plant-growth-investigation.jpg","description":"Students run a plant-growth investigation. They organize fraction measurements of seedlings in a line plot, find totals and differences, find an equal (fair) share of water, and solve a multi-step problem with the data.","level":["Remedial","Standard","Advanced"],"topics":["Data, Line Plots, and Problem Solving","Project","Science & Data"],"added":"2026-11-11"}]};
 c.units.forEach(function(u){(R[u.id]||[]).forEach(function(a){if(!u.artifacts.some(function(x){return x.path===a.path;}))u.artifacts.push(a);});});
 c.planned=false;
})(window);



/* Discrete Math (2026-11-09): approved question banks in every shared game, generator and study guide, plus partner checks,
   unit cheat sheets and Interactive Math (built by the discrete-math and interactive-math-discrete tools). Must stay above the
   Math Millionaire block, which only adds games to courses that are no longer planned. */
(function(G){
 var c=G.LIBRARY.courses.find(function(x){return x.id==='discrete';});if(!c)return;
 var P=[{"unit":"speaking-mathematically","a":{"title":"Partner Check 1: Speaking Mathematically","path":"artifacts/discrete-speaking-mathematically-partner-check-1/worksheet.pdf","thumb":"thumbs/discrete-speaking-mathematically-partner-check-1.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Speaking Mathematically"],"added":"2026-11-09"}},{"unit":"speaking-mathematically","a":{"title":"Partner Check 2: Speaking Mathematically","path":"artifacts/discrete-speaking-mathematically-partner-check-2/worksheet.pdf","thumb":"thumbs/discrete-speaking-mathematically-partner-check-2.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Speaking Mathematically"],"added":"2026-11-09"}},{"unit":"compound-statements-logic","a":{"title":"Partner Check 1: The Logic of Compound Statements","path":"artifacts/discrete-compound-statements-logic-partner-check-1/worksheet.pdf","thumb":"thumbs/discrete-compound-statements-logic-partner-check-1.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","The Logic of Compound Statements"],"added":"2026-11-09"}},{"unit":"compound-statements-logic","a":{"title":"Partner Check 2: The Logic of Compound Statements","path":"artifacts/discrete-compound-statements-logic-partner-check-2/worksheet.pdf","thumb":"thumbs/discrete-compound-statements-logic-partner-check-2.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","The Logic of Compound Statements"],"added":"2026-11-09"}},{"unit":"number-theory-proof","a":{"title":"Partner Check 1: Elementary Number Theory and Methods of Proof","path":"artifacts/discrete-number-theory-proof-partner-check-1/worksheet.pdf","thumb":"thumbs/discrete-number-theory-proof-partner-check-1.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Elementary Number Theory and Methods of Proof"],"added":"2026-11-09"}},{"unit":"number-theory-proof","a":{"title":"Partner Check 2: Elementary Number Theory and Methods of Proof","path":"artifacts/discrete-number-theory-proof-partner-check-2/worksheet.pdf","thumb":"thumbs/discrete-number-theory-proof-partner-check-2.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Elementary Number Theory and Methods of Proof"],"added":"2026-11-09"}},{"unit":"sequences-induction-recursion","a":{"title":"Partner Check 1: Sequences, Mathematical Induction, and Recursion","path":"artifacts/discrete-sequences-induction-recursion-partner-check-1/worksheet.pdf","thumb":"thumbs/discrete-sequences-induction-recursion-partner-check-1.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Sequences, Mathematical Induction, and Recursion"],"added":"2026-11-09"}},{"unit":"sequences-induction-recursion","a":{"title":"Partner Check 2: Sequences, Mathematical Induction, and Recursion","path":"artifacts/discrete-sequences-induction-recursion-partner-check-2/worksheet.pdf","thumb":"thumbs/discrete-sequences-induction-recursion-partner-check-2.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Sequences, Mathematical Induction, and Recursion"],"added":"2026-11-09"}},{"unit":"set-theory","a":{"title":"Partner Check 1: Set Theory","path":"artifacts/discrete-set-theory-partner-check-1/worksheet.pdf","thumb":"thumbs/discrete-set-theory-partner-check-1.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Set Theory"],"added":"2026-11-09"}},{"unit":"set-theory","a":{"title":"Partner Check 2: Set Theory","path":"artifacts/discrete-set-theory-partner-check-2/worksheet.pdf","thumb":"thumbs/discrete-set-theory-partner-check-2.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Set Theory"],"added":"2026-11-09"}},{"unit":"properties-relations","a":{"title":"Partner Check 1: Properties of Relations","path":"artifacts/discrete-properties-relations-partner-check-1/worksheet.pdf","thumb":"thumbs/discrete-properties-relations-partner-check-1.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Properties of Relations"],"added":"2026-11-09"}},{"unit":"properties-relations","a":{"title":"Partner Check 2: Properties of Relations","path":"artifacts/discrete-properties-relations-partner-check-2/worksheet.pdf","thumb":"thumbs/discrete-properties-relations-partner-check-2.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Properties of Relations"],"added":"2026-11-09"}},{"unit":"counting-probability","a":{"title":"Partner Check 1: Counting and Probability","path":"artifacts/discrete-counting-probability-partner-check-1/worksheet.pdf","thumb":"thumbs/discrete-counting-probability-partner-check-1.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Counting and Probability"],"added":"2026-11-09"}},{"unit":"counting-probability","a":{"title":"Partner Check 2: Counting and Probability","path":"artifacts/discrete-counting-probability-partner-check-2/worksheet.pdf","thumb":"thumbs/discrete-counting-probability-partner-check-2.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Counting and Probability"],"added":"2026-11-09"}},{"unit":"graphs-trees","a":{"title":"Partner Check 1: Theory of Graphs and Trees","path":"artifacts/discrete-graphs-trees-partner-check-1/worksheet.pdf","thumb":"thumbs/discrete-graphs-trees-partner-check-1.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Theory of Graphs and Trees"],"added":"2026-11-09"}},{"unit":"graphs-trees","a":{"title":"Partner Check 2: Theory of Graphs and Trees","path":"artifacts/discrete-graphs-trees-partner-check-2/worksheet.pdf","thumb":"thumbs/discrete-graphs-trees-partner-check-2.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Theory of Graphs and Trees"],"added":"2026-11-09"}},{"unit":"election-theory","a":{"title":"Partner Check 1: Election Theory","path":"artifacts/discrete-election-theory-partner-check-1/worksheet.pdf","thumb":"thumbs/discrete-election-theory-partner-check-1.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Election Theory"],"added":"2026-11-09"}},{"unit":"election-theory","a":{"title":"Partner Check 2: Election Theory","path":"artifacts/discrete-election-theory-partner-check-2/worksheet.pdf","thumb":"thumbs/discrete-election-theory-partner-check-2.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Election Theory"],"added":"2026-11-09"}},{"unit":"linear-programming","a":{"title":"Partner Check 1: Linear Programming","path":"artifacts/discrete-linear-programming-partner-check-1/worksheet.pdf","thumb":"thumbs/discrete-linear-programming-partner-check-1.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Linear Programming"],"added":"2026-11-09"}},{"unit":"linear-programming","a":{"title":"Partner Check 2: Linear Programming","path":"artifacts/discrete-linear-programming-partner-check-2/worksheet.pdf","thumb":"thumbs/discrete-linear-programming-partner-check-2.jpg","description":"Discrete Math partner check: Partner A and Partner B solve different problems with matching answers. Six student pages (CP2, CP1 and Honors, A and B versions); teacher answer key included.","type":"Printable","level":["CP2","CP1","Honors"],"topics":["Partner Check","Linear Programming"],"added":"2026-11-09"}}];
 var S={"speaking-mathematically":{"title":"Speaking Mathematically Cheat Sheet","path":"artifacts/discrete-speaking-mathematically-cheat-sheet/worksheet.pdf","thumb":"thumbs/discrete-speaking-mathematically-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: statements, variables, universal and existential statements, conditional statements. Back: set notation, subsets, Cartesian products, ordered pairs and strings. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Speaking Mathematically","Unit 1"],"added":"2026-11-09"},"compound-statements-logic":{"title":"The Logic of Compound Statements Cheat Sheet","path":"artifacts/discrete-compound-statements-logic-cheat-sheet/worksheet.pdf","thumb":"thumbs/discrete-compound-statements-logic-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: connectives, truth tables, logical equivalence, conditionals and their negations. Back: converse, inverse and contrapositive; valid arguments, rules of inference and fallacies. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","The Logic of Compound Statements","Unit 2"],"added":"2026-11-09"},"number-theory-proof":{"title":"Elementary Number Theory and Methods of Proof Cheat Sheet","path":"artifacts/discrete-number-theory-proof-cheat-sheet/worksheet.pdf","thumb":"thumbs/discrete-number-theory-proof-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: definitions, counterexamples, direct proof, existential and universal statements, rational numbers. Back: divisibility, the quotient-remainder theorem, proof by contradiction and contraposition, choosing a strategy. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Elementary Number Theory and Methods of Proof","Unit 3"],"added":"2026-11-09"},"sequences-induction-recursion":{"title":"Sequences, Mathematical Induction, and Recursion Cheat Sheet","path":"artifacts/discrete-sequences-induction-recursion-cheat-sheet/worksheet.pdf","thumb":"thumbs/discrete-sequences-induction-recursion-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: explicit and recursive sequences, arithmetic and geometric patterns, factorials, binomial coefficients, Fibonacci. Back: iteration, the principle of mathematical induction, writing inductive proofs, patterns and tessellations. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Sequences, Mathematical Induction, and Recursion","Unit 4"],"added":"2026-11-09"},"set-theory":{"title":"Set Theory Cheat Sheet","path":"artifacts/discrete-set-theory-cheat-sheet/worksheet.pdf","thumb":"thumbs/discrete-set-theory-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: set equality, the empty set, union, intersection, difference, complements and Venn diagrams. Back: power sets, element-argument proofs, set identities and disproving set statements. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Set Theory","Unit 5"],"added":"2026-11-09"},"properties-relations":{"title":"Properties of Relations Cheat Sheet","path":"artifacts/discrete-properties-relations-cheat-sheet/worksheet.pdf","thumb":"thumbs/discrete-properties-relations-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: relations and inverses, directed graphs, reflexive, symmetric and transitive properties. Back: relations on infinite sets, partitions, equivalence relations and equivalence classes. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Properties of Relations","Unit 6"],"added":"2026-11-09"},"counting-probability":{"title":"Counting and Probability Cheat Sheet","path":"artifacts/discrete-counting-probability-cheat-sheet/worksheet.pdf","thumb":"thumbs/discrete-counting-probability-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: sample spaces, events, lists and arrays, possibility trees, addition and multiplication rules. Back: permutations and combinations, equally likely probability and counting with probability. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Counting and Probability","Unit 7"],"added":"2026-11-09"},"graphs-trees":{"title":"Theory of Graphs and Trees Cheat Sheet","path":"artifacts/discrete-graphs-trees-cheat-sheet/worksheet.pdf","thumb":"thumbs/discrete-graphs-trees-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: vertices, edges, loops, degrees, directed graphs, constructing graphs and graph coloring. Back: walks, trails, paths, circuits, Euler and Hamiltonian circuits, trees and spanning trees. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Theory of Graphs and Trees","Unit 8"],"added":"2026-11-09"},"election-theory":{"title":"Election Theory Cheat Sheet","path":"artifacts/discrete-election-theory-cheat-sheet/worksheet.pdf","thumb":"thumbs/discrete-election-theory-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: preference schedules and four named voting methods, fairness criteria. Back: weighted voting, coalitions and power, fair division and apportionment. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Election Theory","Unit 9"],"added":"2026-11-09"},"linear-programming":{"title":"Linear Programming Cheat Sheet","path":"artifacts/discrete-linear-programming-cheat-sheet/worksheet.pdf","thumb":"thumbs/discrete-linear-programming-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: writing constraints, graphing systems of inequalities, feasible regions and objective functions. Back: corner points, maximizing and minimizing, special cases and interpreting solutions. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Linear Programming","Unit 10"],"added":"2026-11-09"}};
 var T=[{"unit":"compound-statements-logic","a":{"title":"Truth Table Lab","path":"artifacts/discrete-truth-table-lab/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/discrete-truth-table-lab.jpg","description":"Type statements with ~, ∧, ∨, ⊕, → and ↔ and see a full truth table with every intermediate column. Compare two statements for logical equivalence, make the converse, inverse, contrapositive and negation of a conditional, and test argument forms using critical rows.","topics":["Truth tables","Logical equivalence","Conditional statements","Valid and invalid arguments"],"worksheet":"artifacts/discrete-truth-table-lab/worksheet.pdf","answerKey":"artifacts/discrete-truth-table-lab/teacher-key.pdf","added":"2026-11-09"}},{"unit":"number-theory-proof","a":{"title":"Euclidean Algorithm Explorer","path":"artifacts/discrete-euclid-explorer/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/discrete-euclid-explorer.jpg","description":"See the Euclidean algorithm as square tiling of an a × b rectangle, step through a = bq + r, back-substitute to write gcd(a, b) as a linear combination, compare prime factorizations, and explore the quotient-remainder theorem for negative numbers.","topics":["Greatest common divisor","Euclidean algorithm","Quotient-remainder theorem","Prime factorization"],"worksheet":"artifacts/discrete-euclid-explorer/worksheet.pdf","answerKey":"artifacts/discrete-euclid-explorer/teacher-key.pdf","added":"2026-11-09"}},{"unit":"sequences-induction-recursion","a":{"title":"Recursion & Closed Form Explorer","path":"artifacts/discrete-recursion-explorer/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/discrete-recursion-explorer.jpg","description":"Set first-order (aₙ = c·aₙ₋₁ + d) or second-order (aₙ = c·aₙ₋₁ + d·aₙ₋₂) recurrences with any initial terms. See the terms, partial sums and a graph, recognize arithmetic and geometric sequences, and check a closed-form guess against the first 15 terms before proving it by induction.","topics":["Recurrence relations","Arithmetic and geometric sequences","Closed formulas","Mathematical induction"],"worksheet":"artifacts/discrete-recursion-explorer/worksheet.pdf","answerKey":"artifacts/discrete-recursion-explorer/teacher-key.pdf","added":"2026-11-09"}},{"unit":"set-theory","a":{"title":"Venn Diagram & Membership Table Explorer","path":"artifacts/discrete-venn-explorer/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/discrete-venn-explorer.jpg","description":"Two- or three-set Venn diagrams inside a stated universe U = {1, …, 20}. Shade any set expression, compare two expressions region by region (a membership table), click or tab through regions to shade your own answer, and list the actual elements of the result.","topics":["Set operations","Venn diagrams","Set identities","Membership tables"],"worksheet":"artifacts/discrete-venn-explorer/worksheet.pdf","answerKey":"artifacts/discrete-venn-explorer/teacher-key.pdf","added":"2026-11-09"}},{"unit":"properties-relations","a":{"title":"Relation Property Explorer","path":"artifacts/discrete-relation-explorer/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/discrete-relation-explorer.jpg","description":"Toggle ordered pairs on a set of 3 to 6 elements using the relation matrix or the directed graph. See which properties hold with a witness for each failure, form reflexive, symmetric and transitive closures and the inverse, and see the equivalence classes whenever the relation is an equivalence relation.","topics":["Reflexive, symmetric, transitive","Directed graphs of relations","Equivalence relations and classes","Closures"],"worksheet":"artifacts/discrete-relation-explorer/worksheet.pdf","answerKey":"artifacts/discrete-relation-explorer/teacher-key.pdf","added":"2026-11-09"}},{"unit":"counting-probability","a":{"title":"Counting Outcomes Explorer","path":"artifacts/discrete-counting-explorer/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/discrete-counting-explorer.jpg","description":"List every outcome for selections of r items from n letters under all four counting models (ordered or not, with or without repetition). Group permutations into combinations to see why P(n, r) = C(n, r) · r!, and compute equally likely probabilities for events like “contains A”.","topics":["Multiplication rule","Permutations","Combinations","Equally likely probability"],"worksheet":"artifacts/discrete-counting-explorer/worksheet.pdf","answerKey":"artifacts/discrete-counting-explorer/teacher-key.pdf","added":"2026-11-09"}},{"unit":"graphs-trees","a":{"title":"Graph Explorer: Euler, Hamilton & Trees","path":"artifacts/discrete-graph-lab/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/discrete-graph-lab.jpg","description":"Add vertices, edges, loops and parallel edges by pointer or keyboard. See the degree sum, components, Euler circuit or trail (with a route), whether a Hamiltonian cycle exists (by exhaustive search on up to 10 vertices), whether the graph is a tree or bipartite, its chromatic number with a coloring, and a step-by-step minimum spanning tree.","topics":["Degree and the handshake theorem","Euler and Hamiltonian circuits","Trees and spanning trees","Graph coloring"],"worksheet":"artifacts/discrete-graph-lab/worksheet.pdf","answerKey":"artifacts/discrete-graph-lab/teacher-key.pdf","added":"2026-11-09"}},{"unit":"election-theory","a":{"title":"Voting, Power & Apportionment Explorer","path":"artifacts/discrete-voting-explorer/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/discrete-voting-explorer.jpg","description":"Ranked ballots: plurality, Borda count, plurality with elimination and pairwise comparisons side by side, with majority and Condorcet checks and stated tie rules. Weighted voting: winning coalitions, critical players, Banzhaf and Shapley–Shubik indices, dictators, veto power and dummies. Apportionment: quotas, modified divisors, the quota rule and the Alabama paradox.","topics":["Voting methods","Fairness criteria","Weighted voting and power","Apportionment"],"worksheet":"artifacts/discrete-voting-explorer/worksheet.pdf","answerKey":"artifacts/discrete-voting-explorer/teacher-key.pdf","added":"2026-11-09"}},{"unit":"linear-programming","a":{"title":"Feasible Region Optimizer","path":"artifacts/algebra2-feasible-region-optimizer/index.html","bankFormat":"interactive-math","type":"Interactive","thumb":"thumbs/algebra2-feasible-region-optimizer.jpg","description":"Explore a linear programming problem: see the feasible region, slide the objective line, and discover why the maximum and minimum occur at vertices.","topics":["Linear programming","Feasible region","Optimization"],"worksheet":"artifacts/algebra2-feasible-region-optimizer/worksheet.pdf","answerKey":"artifacts/algebra2-feasible-region-optimizer/teacher-key.pdf","added":"2026-11-09"}}];
 var add=function(u,a){if(u&&!u.artifacts.some(function(x){return x.path===a.path;}))u.artifacts.push(a);};
 var unit=function(id){return c.units.find(function(u){return u.id===id;});};
 c.units.forEach(function(u){
  [['showdown','Showdown','showdown'],['connect-four','Connect 4','connect-four'],['tic-tac-toe','Tic-Tac-Toe','tic-tac-toe'],['escape-room','Escape Room','escape-rooms'],['detective','Detective','detective-games'],['picture-reveal','Picture Reveal','picture-reveal'],['flashcards','Flashcards','flashcards']].forEach(function(g){
   add(u,{title:u.name+' '+g[1],path:'worksheet-generator/'+(['escape-room','detective'].indexOf(g[0])>=0?'course-activity':'course-game')+'.html?course=discrete&unit='+u.id+'&game='+g[0],bankFormat:g[2],type:g[0]==='flashcards'?'Study Guide':'Game',thumb:'thumbs/foundations-algebra-'+(g[0]==='flashcards'?'flashcards':['detective','escape-room'].indexOf(g[0])>=0?'showdown':g[0])+'.jpg',description:'Choose Discrete Math skills and CP2, CP1, or Honors questions from the approved bank.',level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-09'});
  });
  add(u,{title:'Vocabulary Activities and Crosswords',path:'worksheet-generator/printables.html#unit=discrete-'+u.id+'&kind=vocabulary',type:'Printable',thumb:'thumbs/vocabulary-prealgebra.svg',description:'Matching, fill-in-the-blank, examples, and crosswords using the unit vocabulary.',level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-09'});
  [['error','Error Analysis','error-generator-foundations.svg','Find, explain, and correct mistakes using authored Discrete Math questions. Includes teacher solutions.'],['tarsia','Tarsia Puzzle','tarsia-generator-foundations.svg','Match problems and answers to assemble a triangle puzzle. Includes work pages and a solved teacher key.'],
   ['maze','Maze','maze-generator-foundations.svg','Follow a route of correctly answered questions through a mathematical maze. Uses Discrete Math questions and a teacher key.'],['color','Color by Number','geometry-color-generator-basics-reasoning.svg','Solve problems to reveal a color-coded picture. Uses Discrete Math questions and a teacher key.'],
   ['partner','Partner Check','partner-generator-foundations.svg','Solve and compare matched-answer problems in pairs. Uses Discrete Math questions and a teacher key.'],['stations','Station Work','stations-generator-foundations.svg','Rotate through independent stations with mixed problem types. Uses Discrete Math questions and a teacher key.'],
   ['who','Whodunnit','foundations-algebra-whodunnit.jpg','Solve clues and narrow down the mystery. Uses Discrete Math questions and a teacher key.']].forEach(function(k){
   add(u,{title:k[1]+' Generator',path:'worksheet-generator/printables.html#unit=discrete-'+u.id+'&kind='+k[0],bankFormat:'printable-generator',type:'Printable',thumb:'thumbs/'+k[2],description:k[3],level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-09'});
  });
  add(u,{title:'Assessment Readiness Check',path:'worksheet-generator/practice-test.html#unit=discrete-'+u.id,bankFormat:'interactive-practice-test',type:'Study Guide',thumb:'thumbs/practice-test.svg',description:'Practice Discrete Math skills, review worked solutions, and target skills for reassessment.',level:['CP2','CP1','Honors'],topics:[u.name],added:'2026-11-09'});
  if(S[u.id])add(u,S[u.id]);
 });
 P.forEach(function(it){add(unit(it.unit),it.a);});
 T.forEach(function(it){add(unit(it.unit),it.a);});
 c.planned=false;
})(window);


/* Unit cheat sheets for 6th Grade, Pre-Algebra (7th), Precalculus, Calculus and Statistics (built by scripts/cheat-sheets). */
(function(G){
 var S={"statistics":{"exploring-data":{"title":"Exploring Data Cheat Sheet","path":"artifacts/statistics-exploring-data-cheat-sheet/worksheet.pdf","thumb":"thumbs/statistics-exploring-data-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: displays, shape, center, spread, box plots, outliers, normal models and z-scores. Back: two-way tables, scatterplots, correlation, least-squares regression and residuals. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Exploring Data","Unit 1"],"added":"2026-11-07"},"sampling-experimentation":{"title":"Sampling and Experimentation Cheat Sheet","path":"artifacts/statistics-sampling-experimentation-cheat-sheet/worksheet.pdf","thumb":"thumbs/statistics-sampling-experimentation-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: populations and samples, random sampling methods and sources of bias. Back: observational studies, experiments, experimental designs and the scope of inference. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Sampling and Experimentation","Unit 2"],"added":"2026-11-07"},"anticipating-patterns":{"title":"Anticipating Patterns Cheat Sheet","path":"artifacts/statistics-anticipating-patterns-cheat-sheet/worksheet.pdf","thumb":"thumbs/statistics-anticipating-patterns-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: probability rules, conditional probability, independence and simulation. Back: random variables, binomial and geometric models, and sampling distributions. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Anticipating Patterns","Unit 3"],"added":"2026-11-07"},"statistical-inference":{"title":"Statistical Inference Cheat Sheet","path":"artifacts/statistics-statistical-inference-cheat-sheet/worksheet.pdf","thumb":"thumbs/statistics-statistical-inference-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: confidence intervals for a proportion and a mean, conditions and interpretation. Back: significance tests, p-values, Type I and II errors, power and two-sample procedures. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Statistical Inference","Unit 4"],"added":"2026-11-07"}},"calculus":{"antiderivatives-definite-integrals":{"title":"Antiderivatives and Definite Integrals Cheat Sheet","path":"artifacts/calculus-antiderivatives-definite-integrals-cheat-sheet/worksheet.pdf","thumb":"thumbs/calculus-antiderivatives-definite-integrals-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: antiderivatives, indefinite integrals and u-substitution. Back: Riemann sums, definite integrals and their properties. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Antiderivatives and Definite Integrals","Unit 5"],"added":"2026-11-05"},"ap-review":{"title":"AP Review Cheat Sheet","path":"artifacts/calculus-ap-review-cheat-sheet/worksheet.pdf","thumb":"thumbs/calculus-ap-review-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: limits, derivatives and their applications. Back: integrals, FTC and free-response tips. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","AP Review","Unit 9"],"added":"2026-11-05"},"applications-derivatives":{"title":"Applications of Derivatives Cheat Sheet","path":"artifacts/calculus-applications-derivatives-cheat-sheet/worksheet.pdf","thumb":"thumbs/calculus-applications-derivatives-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: related rates, motion and linearization. Back: extrema, the MVT, curve sketching and optimization. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Applications of Derivatives","Unit 4"],"added":"2026-11-05"},"applications-integrals":{"title":"Applications of Integrals Cheat Sheet","path":"artifacts/calculus-applications-integrals-cheat-sheet/worksheet.pdf","thumb":"thumbs/calculus-applications-integrals-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: area between curves. Back: volumes by discs, washers and cross sections. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Applications of Integrals","Unit 7"],"added":"2026-11-05"},"derivatives":{"title":"Derivatives Cheat Sheet","path":"artifacts/calculus-derivatives-cheat-sheet/worksheet.pdf","thumb":"thumbs/calculus-derivatives-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: the definition of the derivative and basic rules. Back: product, quotient and chain rules, implicit and higher derivatives. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Derivatives","Unit 3"],"added":"2026-11-05"},"differential-equations":{"title":"Differential Equations Cheat Sheet","path":"artifacts/calculus-differential-equations-cheat-sheet/worksheet.pdf","thumb":"thumbs/calculus-differential-equations-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: slope fields and verifying solutions. Back: separation of variables and exponential growth and decay. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Differential Equations","Unit 8"],"added":"2026-11-05"},"fundamental-theorem-calculus":{"title":"The Fundamental Theorem of Calculus Cheat Sheet","path":"artifacts/calculus-fundamental-theorem-calculus-cheat-sheet/worksheet.pdf","thumb":"thumbs/calculus-fundamental-theorem-calculus-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: FTC part 1 and part 2. Back: average value, accumulation functions and net change. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","The Fundamental Theorem of Calculus","Unit 6"],"added":"2026-11-05"},"limits-continuity":{"title":"Limits and Continuity Cheat Sheet","path":"artifacts/calculus-limits-continuity-cheat-sheet/worksheet.pdf","thumb":"thumbs/calculus-limits-continuity-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: limit notation, evaluating limits algebraically and graphically. Back: one-sided and infinite limits, continuity and the IVT. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Limits and Continuity","Unit 2"],"added":"2026-11-05"},"precalculus-review":{"title":"Precalculus Review Cheat Sheet","path":"artifacts/calculus-precalculus-review-cheat-sheet/worksheet.pdf","thumb":"thumbs/calculus-precalculus-review-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: functions, domain, graphs and transformations. Back: exponentials, logarithms and trigonometry you will need. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Precalculus Review","Unit 1"],"added":"2026-11-05"}},"math6":{"data-displays":{"title":"Data Displays Cheat Sheet","path":"artifacts/math6-data-displays-cheat-sheet/worksheet.pdf","thumb":"thumbs/math6-data-displays-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: statistical questions, dot plots, histograms and box plots. Back: mean, median, range, IQR, MAD and the shape of a distribution. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Data Displays","Unit 7"],"added":"2026-11-05"},"expressions-equations":{"title":"Expressions and Equations Cheat Sheet","path":"artifacts/math6-expressions-equations-cheat-sheet/worksheet.pdf","thumb":"thumbs/math6-expressions-equations-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: exponents, the order of operations and algebraic expressions. Back: equivalent expressions, one-step equations and variables. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Expressions and Equations","Unit 4"],"added":"2026-11-05"},"fractions-decimals-operations":{"title":"Operations of Fractions and Decimals Cheat Sheet","path":"artifacts/math6-fractions-decimals-operations-cheat-sheet/worksheet.pdf","thumb":"thumbs/math6-fractions-decimals-operations-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: dividing fractions and mixed numbers. Back: multi-digit decimals, GCF, LCM and the distributive property. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Operations of Fractions and Decimals","Unit 2"],"added":"2026-11-05"},"geometry":{"title":"Geometry Cheat Sheet","path":"artifacts/math6-geometry-cheat-sheet/worksheet.pdf","thumb":"thumbs/math6-geometry-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: area of quadrilaterals, triangles and composite polygons. Back: volume, polygons on the coordinate plane, nets and surface area. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Geometry","Unit 6"],"added":"2026-11-05"},"inequalities":{"title":"Inequalities Cheat Sheet","path":"artifacts/math6-inequalities-cheat-sheet/worksheet.pdf","thumb":"thumbs/math6-inequalities-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: inequality symbols, solutions and graphs. Back: solving one-step inequalities and applications. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Inequalities","Unit 5"],"added":"2026-11-05"},"rational-numbers":{"title":"Rational Numbers Cheat Sheet","path":"artifacts/math6-rational-numbers-cheat-sheet/worksheet.pdf","thumb":"thumbs/math6-rational-numbers-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: positive and negative numbers, the number line, comparing and ordering. Back: absolute value and the coordinate plane. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Rational Numbers","Unit 3"],"added":"2026-11-05"},"ratios-rates-percent-proportions":{"title":"Ratios, Rate, Percent and Proportions Cheat Sheet","path":"artifacts/math6-ratios-rates-percent-proportions-cheat-sheet/worksheet.pdf","thumb":"thumbs/math6-ratios-rates-percent-proportions-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: ratios, unit rates, equivalent ratios and tables. Back: proportions, percents and unit conversions. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Ratios, Rate, Percent and Proportions","Unit 1"],"added":"2026-11-05"}},"prealgebra7":{"algebraic-expressions-integers":{"title":"Algebraic Expressions and Integers Cheat Sheet","path":"artifacts/prealgebra7-algebraic-expressions-integers-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-algebraic-expressions-integers-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: place value, variables, expressions and the order of operations. Back: integer operations, estimation, patterns and the coordinate plane. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Algebraic Expressions and Integers","Unit 1"],"added":"2026-11-05"},"area-volume":{"title":"Area and Volume Cheat Sheet","path":"artifacts/prealgebra7-area-volume-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-area-volume-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: area of parallelograms, triangles, trapezoids and circles. Back: space figures, surface area and volume. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Area and Volume","Unit 10"],"added":"2026-11-05"},"data-analysis-probability":{"title":"Data Analysis and Probability Cheat Sheet","path":"artifacts/prealgebra7-data-analysis-probability-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-data-analysis-probability-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: frequency tables, histograms, box plots and stem-and-leaf plots. Back: probability, independent and dependent events, counting and sampling. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Data Analysis and Probability","Unit 12"],"added":"2026-11-05"},"decimals-equations":{"title":"Decimals and Equations Cheat Sheet","path":"artifacts/prealgebra7-decimals-equations-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-decimals-equations-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: rounding, estimating and measures of center. Back: formulas, decimal equations and the metric system. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Decimals and Equations","Unit 3"],"added":"2026-11-05"},"factors-fractions-exponents":{"title":"Factors, Fractions, and Exponents Cheat Sheet","path":"artifacts/prealgebra7-factors-fractions-exponents-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-factors-fractions-exponents-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: divisibility, prime factorization, GCF and simplifying fractions. Back: rational and irrational numbers, exponent rules, scientific notation and cube roots. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Factors, Fractions, and Exponents","Unit 4"],"added":"2026-11-05"},"linear-functions-graphing":{"title":"Linear Functions and Graphing Cheat Sheet","path":"artifacts/prealgebra7-linear-functions-graphing-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-linear-functions-graphing-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: relations, functions, two-variable equations, slope and intercepts. Back: writing rules, scatter plots, systems and graphing inequalities. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Linear Functions and Graphing","Unit 8"],"added":"2026-11-05"},"nonlinear-functions-polynomials":{"title":"Nonlinear Functions and Polynomials Cheat Sheet","path":"artifacts/prealgebra7-nonlinear-functions-polynomials-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-nonlinear-functions-polynomials-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: sequences, nonlinear graphs and exponential growth and decay. Back: adding, subtracting and multiplying polynomials. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Nonlinear Functions and Polynomials","Unit 13"],"added":"2026-11-05"},"one-step-equations-inequalities":{"title":"Solving One-Step Equations and Inequalities Cheat Sheet","path":"artifacts/prealgebra7-one-step-equations-inequalities-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-one-step-equations-inequalities-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: number properties, the distributive property and simplifying. Back: one-step equations and inequalities and their graphs. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Solving One-Step Equations and Inequalities","Unit 2"],"added":"2026-11-05"},"operations-fractions":{"title":"Operations with Fractions Cheat Sheet","path":"artifacts/prealgebra7-operations-fractions-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-operations-fractions-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: comparing rational numbers, fractions and decimals, the four operations. Back: customary units, fraction equations and powers of quotients. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Operations with Fractions","Unit 5"],"added":"2026-11-05"},"ratios-proportions-percentages":{"title":"Ratios, Proportions, and Percentages Cheat Sheet","path":"artifacts/prealgebra7-ratios-proportions-percentages-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-ratios-proportions-percentages-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: ratios, unit rates, proportions, scale drawings and probability. Back: percents, percent of change, markup, discount and tables. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Ratios, Proportions, and Percentages","Unit 6"],"added":"2026-11-05"},"right-triangles-algebra":{"title":"Right Triangles in Algebra Cheat Sheet","path":"artifacts/prealgebra7-right-triangles-algebra-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-right-triangles-algebra-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: square roots, the Pythagorean theorem, distance and midpoint. Back: proportions, special right triangles and trigonometric ratios. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Right Triangles in Algebra","Unit 11"],"added":"2026-11-05"},"solving-equations-inequalities":{"title":"Solving Equations and Inequalities Cheat Sheet","path":"artifacts/prealgebra7-solving-equations-inequalities-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-solving-equations-inequalities-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: two-step and multi-step equations, fractions and decimals. Back: variables on both sides, two-step inequalities, formulas and interest. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Solving Equations and Inequalities","Unit 7"],"added":"2026-11-05"},"spatial-thinking":{"title":"Spatial Thinking Cheat Sheet","path":"artifacts/prealgebra7-spatial-thinking-cheat-sheet/worksheet.pdf","thumb":"thumbs/prealgebra7-spatial-thinking-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: points, lines, planes, angle pairs, parallel lines and polygons. Back: congruence, circles, constructions, translations, symmetry and rotations. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Spatial Thinking","Unit 9"],"added":"2026-11-05"}},"precalculus":{"conics":{"title":"Conics Cheat Sheet","path":"artifacts/precalculus-conics-cheat-sheet/worksheet.pdf","thumb":"thumbs/precalculus-conics-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: parabolas and circles. Back: ellipses, hyperbolas and identifying conics. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Conics","Unit 3"],"added":"2026-11-05"},"equations-inequalities":{"title":"Equations and Inequalities Cheat Sheet","path":"artifacts/precalculus-equations-inequalities-cheat-sheet/worksheet.pdf","thumb":"thumbs/precalculus-equations-inequalities-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: linear, absolute value and quadratic equations. Back: polynomial, rational and radical equations and inequalities. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Equations and Inequalities","Unit 1"],"added":"2026-11-05"},"functions":{"title":"Functions Cheat Sheet","path":"artifacts/precalculus-functions-cheat-sheet/worksheet.pdf","thumb":"thumbs/precalculus-functions-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: domain, range, graphs and transformations. Back: combinations, inverses, polynomial, rational, exponential and logarithmic functions. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Functions","Unit 2"],"added":"2026-11-05"},"general-triangle-trigonometry":{"title":"Trigonometry of General Triangles Cheat Sheet","path":"artifacts/precalculus-general-triangle-trigonometry-cheat-sheet/worksheet.pdf","thumb":"thumbs/precalculus-general-triangle-trigonometry-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: right-triangle trig and the Law of Sines. Back: the Law of Cosines, the ambiguous case and triangle area. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Trigonometry of General Triangles","Unit 5"],"added":"2026-11-05"},"matrices":{"title":"Matrices Cheat Sheet","path":"artifacts/precalculus-matrices-cheat-sheet/worksheet.pdf","thumb":"thumbs/precalculus-matrices-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: matrix operations and multiplication. Back: determinants, inverses and solving systems. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Matrices","Unit 6"],"added":"2026-11-05"},"probability":{"title":"Probability Cheat Sheet","path":"artifacts/precalculus-probability-cheat-sheet/worksheet.pdf","thumb":"thumbs/precalculus-probability-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: counting, permutations, combinations and basic probability. Back: conditional probability, independence, the binomial theorem and expected value. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Probability","Unit 8"],"added":"2026-11-05"},"trigonometric-functions":{"title":"Trigonometric Functions Cheat Sheet","path":"artifacts/precalculus-trigonometric-functions-cheat-sheet/worksheet.pdf","thumb":"thumbs/precalculus-trigonometric-functions-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: angles, radians, the unit circle and graphs. Back: inverse trig functions, identities and trig equations. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Trigonometric Functions","Unit 4"],"added":"2026-11-05"},"vectors":{"title":"Vectors Cheat Sheet","path":"artifacts/precalculus-vectors-cheat-sheet/worksheet.pdf","thumb":"thumbs/precalculus-vectors-cheat-sheet.jpg","description":"Two-page printable cheat sheet. Front: vector components, magnitude, direction and operations. Back: dot product, angles between vectors, projections and applications. Key vocabulary, worked examples with every answer checked, and common mistakes.","type":"Printable","topics":["Cheat sheet","Reference","Vectors","Unit 7"],"added":"2026-11-05"}}};
 G.LIBRARY.courses.forEach(function(c){var m=S[c.id];if(!m)return;c.units.forEach(function(u){var a=m[u.id];if(!a||u.artifacts.some(function(x){return x.path===a.path}))return;u.artifacts.push(a);});});
})(window);

/* Math Millionaire: one whole-class game show per unit. Each game draws 15 fresh multiple-choice questions
   from the unit's verified question bank, easiest first (worksheet-generator/millionaire.html). */
(function(G){
 G.LIBRARY.courses.forEach(function(c){
  if(c.planned)return;
  c.units.forEach(function(u){
   var path='worksheet-generator/millionaire.html?course='+c.id+'&unit='+u.id;
   if(u.artifacts.some(function(a){return a.path===path;}))return;
   u.artifacts.push({title:u.name+' Millionaire',path:path,bankFormat:'millionaire',type:'Game',
    description:'A whole-class game show: 15 multiple-choice questions climb from warm-up to challenge on a prize ladder. Groups take turns in the hot seat with 50:50, Ask the Class and Hint lifelines. Fresh questions every game.',
    topics:[u.name,'Whole-class game'],added:'2026-11-05'});
  });
 });
})(window);

/* Interactive Math: hands-on tools with printable Explore & Reflect worksheets and teacher keys.
   Built from tools/interactive-math-20261105 (build.py, build_worksheets.py, print_pdfs.cjs). */
(function(G){
 var ITEMS=[{"course": "algebra","unit": "foundations-algebra","a": {"title": "Algebra Tiles Lab","path": "artifacts/foundations-algebra-algebra-tiles-lab/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/foundations-algebra-algebra-tiles-lab.jpg","description": "Model expressions with x-tiles and unit tiles, combine like terms, cancel zero pairs, and see the distributive property as an area.","topics": ["Combining like terms","Zero pairs","Distributive property"],"worksheet": "artifacts/foundations-algebra-algebra-tiles-lab/worksheet.pdf","answerKey": "artifacts/foundations-algebra-algebra-tiles-lab/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra","unit": "expressions-equations","a": {"title": "Equation Balance Scale","path": "artifacts/expressions-equations-balance-scale/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/expressions-equations-balance-scale.jpg","description": "Solve equations on a balance scale: apply operations to one or both sides, see why both sides must change together, and meet equations with no solution or infinitely many.","topics": ["Inverse operations","Solving equations","No solution / infinitely many"],"worksheet": "artifacts/expressions-equations-balance-scale/worksheet.pdf","answerKey": "artifacts/expressions-equations-balance-scale/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra","unit": "inequalities","a": {"title": "Inequality Number Line","path": "artifacts/inequalities-inequality-number-line/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/inequalities-inequality-number-line.jpg","description": "Graph inequalities with open and closed circles, test points, and discover why multiplying or dividing by a negative flips the inequality symbol.","topics": ["Graphing inequalities","Test points","Flipping the symbol"],"worksheet": "artifacts/inequalities-inequality-number-line/worksheet.pdf","answerKey": "artifacts/inequalities-inequality-number-line/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra","unit": "relations-functions","a": {"title": "Function Detector","path": "artifacts/relations-functions-function-detector/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/relations-functions-function-detector.jpg","description": "Use the vertical line test on graphs and plotted points, link each graph to a mapping diagram, and read domain and range.","topics": ["Vertical line test","Mapping diagrams","Domain and range"],"worksheet": "artifacts/relations-functions-function-detector/worksheet.pdf","answerKey": "artifacts/relations-functions-function-detector/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra","unit": "linear-equations-slope","a": {"title": "Slope-Intercept Explorer","path": "artifacts/linear-equations-slope-slope-intercept-explorer/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/linear-equations-slope-slope-intercept-explorer.jpg","description": "Use sliders or drag points to change m and b in y = mx + b. See the slope triangle, the table and parallel or perpendicular lines update live.","topics": ["Slope","y-intercept","Parallel and perpendicular lines"],"worksheet": "artifacts/linear-equations-slope-slope-intercept-explorer/worksheet.pdf","answerKey": "artifacts/linear-equations-slope-slope-intercept-explorer/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra","unit": "systems-of-equations","a": {"title": "Systems Explorer","path": "artifacts/systems-of-equations-systems-explorer/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/systems-of-equations-systems-explorer.jpg","description": "Adjust two lines and watch their intersection. Find systems with one, no or infinitely many solutions, then switch on inequality shading.","topics": ["Solving by graphing","Number of solutions","Systems of inequalities"],"worksheet": "artifacts/systems-of-equations-systems-explorer/worksheet.pdf","answerKey": "artifacts/systems-of-equations-systems-explorer/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra","unit": "exponents-exponential-functions","a": {"title": "Exponent Rules Unpacker","path": "artifacts/exponents-exponential-functions-exponent-rules-unpacker/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/exponents-exponential-functions-exponent-rules-unpacker.jpg","description": "Expand powers into repeated factors to see why the product, quotient and power rules work, and follow a pattern to zero and negative exponents.","topics": ["Product rule","Quotient rule","Zero and negative exponents"],"worksheet": "artifacts/exponents-exponential-functions-exponent-rules-unpacker/worksheet.pdf","answerKey": "artifacts/exponents-exponential-functions-exponent-rules-unpacker/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra","unit": "exponential-functions","a": {"title": "Linear vs. Exponential Race","path": "artifacts/exponential-functions-linear-vs-exponential/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/exponential-functions-linear-vs-exponential.jpg","description": "Compare y = a·bˣ with a linear function in a graph and a table. See constant differences versus constant ratios, growth versus decay, and the asymptote.","topics": ["Growth and decay","Constant ratio","Initial value"],"worksheet": "artifacts/exponential-functions-linear-vs-exponential/worksheet.pdf","answerKey": "artifacts/exponential-functions-linear-vs-exponential/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra","unit": "polynomials-factoring","a": {"title": "Area Model Multiplier","path": "artifacts/polynomials-factoring-area-model-multiplier/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/polynomials-factoring-area-model-multiplier.jpg","description": "Build (ax + b)(cx + d) as a rectangle of tiles to see each partial product, where the middle term comes from, and why (x + 3)² is not x² + 9.","topics": ["Multiplying binomials","Area model","Special products"],"worksheet": "artifacts/polynomials-factoring-area-model-multiplier/worksheet.pdf","answerKey": "artifacts/polynomials-factoring-area-model-multiplier/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra","unit": "factoring-zero-product","a": {"title": "Factor Rectangle Builder","path": "artifacts/factoring-zero-product-factor-rectangle-builder/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/factoring-zero-product-factor-rectangle-builder.jpg","description": "Arrange x², x and unit tiles into a rectangle to factor a trinomial, then connect the factors to the zeros and x-intercepts of the parabola.","topics": ["Factoring trinomials","Zero product property","x-intercepts"],"worksheet": "artifacts/factoring-zero-product-factor-rectangle-builder/worksheet.pdf","answerKey": "artifacts/factoring-zero-product-factor-rectangle-builder/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra","unit": "quadratics","a": {"title": "Parabola Explorer","path": "artifacts/quadratics-parabola-explorer/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/quadratics-parabola-explorer.jpg","description": "Use vertex-form sliders for a, h and k, then standard form with the vertex, axis of symmetry, discriminant and number of x-intercepts.","topics": ["Vertex form","Transformations","Discriminant"],"worksheet": "artifacts/quadratics-parabola-explorer/worksheet.pdf","answerKey": "artifacts/quadratics-parabola-explorer/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra","unit": "statistics-data-modeling","a": {"title": "Line of Best Fit Lab","path": "artifacts/statistics-data-modeling-line-of-best-fit-lab/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/statistics-data-modeling-line-of-best-fit-lab.jpg","description": "Drag data points, fit a line by eye, compare it with the least-squares line, and see how residuals, outliers and r change.","topics": ["Scatter plots","Correlation coefficient","Residuals and outliers"],"worksheet": "artifacts/statistics-data-modeling-line-of-best-fit-lab/worksheet.pdf","answerKey": "artifacts/statistics-data-modeling-line-of-best-fit-lab/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra2","unit": "functions-transformations","a": {"title": "Transformation Lab","path": "artifacts/algebra2-transformation-lab/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/algebra2-transformation-lab.jpg","description": "Transform six parent functions with a, b, h and k sliders and a ghost parent graph, and discover that the rules work the same way for every function.","topics": ["Parent functions","Shifts and stretches","Reflections"],"worksheet": "artifacts/algebra2-transformation-lab/worksheet.pdf","answerKey": "artifacts/algebra2-transformation-lab/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra2","unit": "linear-functions-systems","a": {"title": "Feasible Region Optimizer","path": "artifacts/algebra2-feasible-region-optimizer/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/algebra2-feasible-region-optimizer.jpg","description": "Explore a linear programming problem: see the feasible region, slide the objective line, and discover why the maximum and minimum occur at vertices.","topics": ["Linear programming","Feasible region","Optimization"],"worksheet": "artifacts/algebra2-feasible-region-optimizer/worksheet.pdf","answerKey": "artifacts/algebra2-feasible-region-optimizer/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra2","unit": "quadratic-functions-complex-numbers","a": {"title": "Discriminant & Roots Explorer","path": "artifacts/algebra2-discriminant-roots-explorer/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/algebra2-discriminant-roots-explorer.jpg","description": "Change a, b and c, watch the discriminant, and follow the roots from the x-axis onto the complex plane as conjugate pairs.","topics": ["Discriminant","Complex roots","Conjugate pairs"],"worksheet": "artifacts/algebra2-discriminant-roots-explorer/worksheet.pdf","answerKey": "artifacts/algebra2-discriminant-roots-explorer/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra2","unit": "polynomial-functions","a": {"title": "Zeros & Multiplicity Builder","path": "artifacts/algebra2-zeros-multiplicity-builder/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/algebra2-zeros-multiplicity-builder.jpg","description": "Choose zeros, multiplicities and the leading coefficient to build a polynomial, and discover end behavior and how multiplicity shapes the graph at each zero.","topics": ["Zeros and multiplicity","End behavior","Degree"],"worksheet": "artifacts/algebra2-zeros-multiplicity-builder/worksheet.pdf","answerKey": "artifacts/algebra2-zeros-multiplicity-builder/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra2","unit": "exponential-logarithmic-functions","a": {"title": "Exponential & Log Mirror","path": "artifacts/algebra2-exponential-log-mirror/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/algebra2-exponential-log-mirror.jpg","description": "See bˣ and log_b x as reflections across y = x with a base slider and matching points, then compound interest more often to discover e.","topics": ["Inverse functions","Logarithms","The number e"],"worksheet": "artifacts/algebra2-exponential-log-mirror/worksheet.pdf","answerKey": "artifacts/algebra2-exponential-log-mirror/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra2","unit": "rational-functions","a": {"title": "Asymptote & Hole Explorer","path": "artifacts/algebra2-asymptote-hole-explorer/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/algebra2-asymptote-hole-explorer.jpg","description": "Choose factors for the numerator and denominator to see holes, vertical asymptotes, horizontal asymptotes and x-intercepts appear on the graph.","topics": ["Vertical asymptotes","Holes","Horizontal asymptotes"],"worksheet": "artifacts/algebra2-asymptote-hole-explorer/worksheet.pdf","answerKey": "artifacts/algebra2-asymptote-hole-explorer/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra2","unit": "sequences-series","a": {"title": "Sequence Builder","path": "artifacts/algebra2-sequence-builder/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/algebra2-sequence-builder.jpg","description": "Build arithmetic and geometric sequences with sliders, graph the terms and the running sum, and see when a geometric series converges.","topics": ["Arithmetic sequences","Geometric sequences","Series and convergence"],"worksheet": "artifacts/algebra2-sequence-builder/worksheet.pdf","answerKey": "artifacts/algebra2-sequence-builder/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra2","unit": "conic-sections","a": {"title": "Conic Explorer","path": "artifacts/algebra2-conic-explorer/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/algebra2-conic-explorer.jpg","description": "Explore circles, ellipses, hyperbolas and parabolas from their standard-form equations, with centers, foci, vertices and the directrix drawn live.","topics": ["Circles and ellipses","Hyperbolas","Foci and directrix"],"worksheet": "artifacts/algebra2-conic-explorer/worksheet.pdf","answerKey": "artifacts/algebra2-conic-explorer/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra2","unit": "trigonometric-functions","a": {"title": "Unit Circle to Sine Wave","path": "artifacts/algebra2-unit-circle-sine-wave/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/algebra2-unit-circle-sine-wave.jpg","description": "Drag an angle around the unit circle to trace sine and cosine, read exact values, then change amplitude, period and shifts on the wave.","topics": ["Unit circle","Sine and cosine graphs","Amplitude and period"],"worksheet": "artifacts/algebra2-unit-circle-sine-wave/worksheet.pdf","answerKey": "artifacts/algebra2-unit-circle-sine-wave/teacher-key.pdf","added": "2026-11-05"}},{"course": "algebra2","unit": "probability-statistics","a": {"title": "Probability Simulation Lab","path": "artifacts/algebra2-probability-simulation-lab/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/algebra2-probability-simulation-lab.jpg","description": "Simulate coins and dice to compare experimental and theoretical probability, then use mean and standard deviation sliders to explore the empirical rule.","topics": ["Experimental probability","Law of large numbers","Normal distribution"],"worksheet": "artifacts/algebra2-probability-simulation-lab/worksheet.pdf","answerKey": "artifacts/algebra2-probability-simulation-lab/teacher-key.pdf","added": "2026-11-05"}},{"course": "precalculus","unit": "trigonometric-functions","a": {"title": "Unit Circle to Sine Wave","path": "artifacts/algebra2-unit-circle-sine-wave/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/algebra2-unit-circle-sine-wave.jpg","description": "Drag an angle around the unit circle to trace sine and cosine, read exact values, then change amplitude, period and shifts on the wave.","topics": ["Unit circle","Sine and cosine graphs","Amplitude and period"],"worksheet": "artifacts/algebra2-unit-circle-sine-wave/worksheet.pdf","answerKey": "artifacts/algebra2-unit-circle-sine-wave/teacher-key.pdf","added": "2026-11-05"}},{"course": "calculus","unit": "precalculus-review","a": {"title": "Unit Circle to Sine Wave","path": "artifacts/algebra2-unit-circle-sine-wave/index.html","bankFormat": "interactive-math","type": "Interactive","thumb": "thumbs/algebra2-unit-circle-sine-wave.jpg","description": "Drag an angle around the unit circle to trace sine and cosine, read exact values, then change amplitude, period and shifts on the wave.","topics": ["Unit circle","Sine and cosine graphs","Amplitude and period"],"worksheet": "artifacts/algebra2-unit-circle-sine-wave/worksheet.pdf","answerKey": "artifacts/algebra2-unit-circle-sine-wave/teacher-key.pdf","added": "2026-11-05"}}];
 ITEMS.forEach(function(it){
  var c=G.LIBRARY.courses.find(function(x){return x.id===it.course;});if(!c)return;
  var u=c.units.find(function(x){return x.id===it.unit;});if(!u||u.artifacts.some(function(a){return a.path===it.a.path;}))return;
  u.artifacts.push(it.a);
 });
})(window);

/* Interactive Math for Geometry: one hands-on tool per unit, with printable Explore & Reflect worksheets and teacher keys. */
(function(G){
 var ITEMS=[{"course": "geometry", "unit": "foundations-geometry", "a": {"title": "Distance & Midpoint Explorer", "path": "artifacts/geometry-distance-midpoint-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/geometry-distance-midpoint-explorer.jpg", "description": "Drag two points to see the distance formula built from a right triangle and the midpoint as an average, then check segment addition with a point on the segment.", "topics": ["Distance formula", "Midpoint formula", "Segment addition"], "worksheet": "artifacts/geometry-distance-midpoint-explorer/worksheet.pdf", "answerKey": "artifacts/geometry-distance-midpoint-explorer/teacher-key.pdf", "added": "2026-11-05"}}, {"course": "geometry", "unit": "angles-parallel-lines", "a": {"title": "Parallel Lines & Transversal", "path": "artifacts/geometry-parallel-lines-transversal/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/geometry-parallel-lines-transversal.jpg", "description": "Turn a transversal across two parallel lines, highlight corresponding, alternate and same-side angle pairs, and see what happens when the lines aren't parallel.", "topics": ["Corresponding angles", "Alternate interior angles", "Same-side interior angles"], "worksheet": "artifacts/geometry-parallel-lines-transversal/worksheet.pdf", "answerKey": "artifacts/geometry-parallel-lines-transversal/teacher-key.pdf", "added": "2026-11-05"}}, {"course": "geometry", "unit": "triangle-congruence", "a": {"title": "Triangle Congruence Builder", "path": "artifacts/geometry-triangle-congruence-builder/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/geometry-triangle-congruence-builder.jpg", "description": "Set three parts of a triangle with SSS, SAS, ASA, AAS, SSA or AAA and see whether they make exactly one triangle, two, none or many.", "topics": ["SSS, SAS, ASA, AAS", "Why SSA and AAA fail", "Triangle construction"], "worksheet": "artifacts/geometry-triangle-congruence-builder/worksheet.pdf", "answerKey": "artifacts/geometry-triangle-congruence-builder/teacher-key.pdf", "added": "2026-11-05"}}, {"course": "geometry", "unit": "triangle-relationships", "a": {"title": "Triangle Explorer", "path": "artifacts/geometry-triangle-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/geometry-triangle-explorer.jpg", "description": "Drag a triangle's vertices to explore the angle sum, exterior angles, the side and angle order, and the four triangle centers, then test the triangle inequality.", "topics": ["Angle sum and exterior angles", "Triangle centers", "Triangle inequality"], "worksheet": "artifacts/geometry-triangle-explorer/worksheet.pdf", "answerKey": "artifacts/geometry-triangle-explorer/teacher-key.pdf", "added": "2026-11-05"}}, {"course": "geometry", "unit": "similarity", "a": {"title": "Dilation & Similarity Lab", "path": "artifacts/geometry-dilation-similarity-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/geometry-dilation-similarity-lab.jpg", "description": "Dilate a triangle with a movable center and scale factor, and compare side ratios, angles, perimeter and area of similar triangles.", "topics": ["Dilations", "Scale factor", "Perimeter and area ratios"], "worksheet": "artifacts/geometry-dilation-similarity-lab/worksheet.pdf", "answerKey": "artifacts/geometry-dilation-similarity-lab/teacher-key.pdf", "added": "2026-11-05"}}, {"course": "geometry", "unit": "right-triangles-trigonometry", "a": {"title": "Trig Ratio Explorer", "path": "artifacts/geometry-trig-ratio-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/geometry-trig-ratio-explorer.jpg", "description": "Change the angle and size of a right triangle to see that sine, cosine and tangent depend only on the angle, then explore the special right triangles.", "topics": ["Sine, cosine and tangent", "Special right triangles", "Pythagorean theorem"], "worksheet": "artifacts/geometry-trig-ratio-explorer/worksheet.pdf", "answerKey": "artifacts/geometry-trig-ratio-explorer/teacher-key.pdf", "added": "2026-11-05"}}, {"course": "geometry", "unit": "quadrilaterals-polygons", "a": {"title": "Polygon & Quadrilateral Explorer", "path": "artifacts/geometry-polygon-angle-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/geometry-polygon-angle-explorer.jpg", "description": "Find polygon angle sums by splitting into triangles, then drag a quadrilateral's vertices and classify it from its sides, angles and diagonals.", "topics": ["Polygon angle sums", "Exterior angles", "Classifying quadrilaterals"], "worksheet": "artifacts/geometry-polygon-angle-explorer/worksheet.pdf", "answerKey": "artifacts/geometry-polygon-angle-explorer/teacher-key.pdf", "added": "2026-11-05"}}, {"course": "geometry", "unit": "transformations", "a": {"title": "Transformation Studio", "path": "artifacts/geometry-transformation-studio/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/geometry-transformation-studio.jpg", "description": "Apply translations, reflections, rotations and dilations to a triangle, read the coordinate rule, and see which transformations keep size and orientation.", "topics": ["Coordinate rules", "Rigid motions", "Dilations"], "worksheet": "artifacts/geometry-transformation-studio/worksheet.pdf", "answerKey": "artifacts/geometry-transformation-studio/teacher-key.pdf", "added": "2026-11-05"}}, {"course": "geometry", "unit": "circles", "a": {"title": "Circle Angle Explorer", "path": "artifacts/geometry-circle-angle-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/geometry-circle-angle-explorer.jpg", "description": "Drag points on a circle to compare central and inscribed angles with their arcs, then find arc length and sector area as fractions of the circle.", "topics": ["Inscribed angles", "Central angles and arcs", "Arc length and sector area"], "worksheet": "artifacts/geometry-circle-angle-explorer/worksheet.pdf", "answerKey": "artifacts/geometry-circle-angle-explorer/teacher-key.pdf", "added": "2026-11-05"}}, {"course": "geometry", "unit": "area-surface-area-volume", "a": {"title": "Solids Volume Lab", "path": "artifacts/geometry-solids-volume-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/geometry-solids-volume-lab.jpg", "description": "Change the dimensions of five solids to see their volume and surface area formulas at work, compare cones with cylinders, and scale solids by k.", "topics": ["Volume", "Surface area", "Scale factor and volume"], "worksheet": "artifacts/geometry-solids-volume-lab/worksheet.pdf", "answerKey": "artifacts/geometry-solids-volume-lab/teacher-key.pdf", "added": "2026-11-05"}}];
 ITEMS.forEach(function(it){
  var c=G.LIBRARY.courses.find(function(x){return x.id===it.course;});if(!c)return;
  var u=c.units.find(function(x){return x.id===it.unit;});if(!u||u.artifacts.some(function(a){return a.path===it.a.path;}))return;
  u.artifacts.push(it.a);
 });
})(window);

/* Interactive Math 2026-11-07: 14 tools for 6th Grade, Pre-Algebra (7th and 8th), Precalculus and Calculus, plus existing tools
   listed in other courses where they fit. Built from tools/interactive-math-20261107 (build.py, build_worksheets.py, print_pdfs.cjs).
   Same pattern as the blocks above: an entry is skipped if its unit is missing or already lists that path. */
(function(G){
 var ITEMS=[{"course": "math6", "unit": "ratios-rates-percent-proportions", "a": {"title": "Double Number Line Ratio Explorer", "path": "artifacts/math6-ratio-double-number-line/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/math6-ratio-double-number-line.jpg", "description": "Slide a marker along a double number line linked to a ratio table and a graph. Find both unit rates, test pairs for equivalence, and see why adding the same amount to both parts changes the ratio.", "topics": ["Equivalent ratios", "Unit rate", "Double number lines"], "worksheet": "artifacts/math6-ratio-double-number-line/worksheet.pdf", "answerKey": "artifacts/math6-ratio-double-number-line/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "math6", "unit": "fractions-decimals-operations", "a": {"title": "Fraction Division: How Many Groups?", "path": "artifacts/math6-fraction-division-groups/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/math6-fraction-division-groups.jpg", "description": "Model a ÷ b as “how many groups of b fit in a?” with bars cut into equal pieces. See full and partial groups, why dividing by a fraction less than 1 gives a bigger answer, and where “multiply by the reciprocal” comes from.", "topics": ["Dividing fractions", "Measurement division", "Reciprocals"], "worksheet": "artifacts/math6-fraction-division-groups/worksheet.pdf", "answerKey": "artifacts/math6-fraction-division-groups/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "math6", "unit": "geometry", "a": {"title": "Parallelogram & Triangle Area Lab", "path": "artifacts/math6-area-shear-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/math6-area-shear-lab.jpg", "description": "Drag the top of a parallelogram or triangle to lean it, cut and slide it into a rectangle, and copy a triangle into a parallelogram to see why area depends on base and height, not on slanted sides.", "topics": ["Area of parallelograms", "Area of triangles", "Base and height"], "worksheet": "artifacts/math6-area-shear-lab/worksheet.pdf", "answerKey": "artifacts/math6-area-shear-lab/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "math6", "unit": "data-displays", "a": {"title": "Dot Plot Balance: Mean, Median & Spread", "path": "artifacts/math6-balance-point-dot-plot/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/math6-balance-point-dot-plot.jpg", "description": "Drag data values on a dot plot and watch the mean balance point, the median, the range, IQR and MAD respond. See how outliers pull the mean and why distances on each side of the mean balance.", "topics": ["Mean and median", "Mean absolute deviation", "Outliers"], "worksheet": "artifacts/math6-balance-point-dot-plot/worksheet.pdf", "answerKey": "artifacts/math6-balance-point-dot-plot/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "prealgebra7", "unit": "linear-functions-graphing", "a": {"title": "Proportional Relationship Explorer", "path": "artifacts/prealgebra7-proportional-relationships/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/prealgebra7-proportional-relationships.jpg", "description": "Link a price context, a table, a graph and an equation. Find the constant of proportionality, see why y = kx passes through (0, 0), and discover why a straight line with a starting fee is not proportional.", "topics": ["Constant of proportionality", "y = kx", "Proportional vs. non-proportional"], "worksheet": "artifacts/prealgebra7-proportional-relationships/worksheet.pdf", "answerKey": "artifacts/prealgebra7-proportional-relationships/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "prealgebra7", "unit": "ratios-proportions-percentages", "a": {"title": "Percent Change Bar Model", "path": "artifacts/prealgebra7-percent-change-bar/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/prealgebra7-percent-change-bar.jpg", "description": "Model markups, discounts, tax and two changes in a row with percent bars on one dollar scale. See why +20% then −20% does not return to the start and why percent changes multiply instead of add.", "topics": ["Percent of change", "Markup and discount", "Successive percent changes"], "worksheet": "artifacts/prealgebra7-percent-change-bar/worksheet.pdf", "answerKey": "artifacts/prealgebra7-percent-change-bar/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "prealgebra7", "unit": "data-analysis-probability", "a": {"title": "Spinner Probability Lab", "path": "artifacts/prealgebra7-spinner-probability-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/prealgebra7-spinner-probability-lab.jpg", "description": "Build a spinner from equal parts, find theoretical probabilities, and compare them with experimental results as the number of spins grows. Use expected counts and see that the spinner has no memory.", "topics": ["Theoretical probability", "Experimental probability", "Expected value"], "worksheet": "artifacts/prealgebra7-spinner-probability-lab/worksheet.pdf", "answerKey": "artifacts/prealgebra7-spinner-probability-lab/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "prealgebra", "unit": "geometry-applications", "a": {"title": "Pythagorean Squares Explorer", "path": "artifacts/prealgebra-pythagorean-squares/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/prealgebra-pythagorean-squares.jpg", "description": "Drag a triangle on a grid with a square on each side. Compare a² + b² with c² for right, acute and obtuse triangles, use the converse, and find the area of a tilted square without measuring its side.", "topics": ["Pythagorean theorem", "Converse of the Pythagorean theorem", "Square roots"], "worksheet": "artifacts/prealgebra-pythagorean-squares/worksheet.pdf", "answerKey": "artifacts/prealgebra-pythagorean-squares/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "prealgebra7", "unit": "right-triangles-algebra", "a": {"title": "Pythagorean Squares Explorer", "path": "artifacts/prealgebra-pythagorean-squares/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/prealgebra-pythagorean-squares.jpg", "description": "Drag a triangle on a grid with a square on each side. Compare a² + b² with c² for right, acute and obtuse triangles, use the converse, and find the area of a tilted square without measuring its side.", "topics": ["Pythagorean theorem", "Converse of the Pythagorean theorem", "Square roots"], "worksheet": "artifacts/prealgebra-pythagorean-squares/worksheet.pdf", "answerKey": "artifacts/prealgebra-pythagorean-squares/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "prealgebra", "unit": "real-numbers-exponents", "a": {"title": "Square Roots on the Number Line", "path": "artifacts/prealgebra-square-roots-number-line/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/prealgebra-square-roots-number-line.jpg", "description": "Link a square’s area to its side length, trap √A between neighbors by squaring, zoom to tenths, hundredths and thousandths, and test your own estimates. Compare perfect squares with irrational square roots.", "topics": ["Square roots", "Estimating irrational numbers", "Rational vs. irrational"], "worksheet": "artifacts/prealgebra-square-roots-number-line/worksheet.pdf", "answerKey": "artifacts/prealgebra-square-roots-number-line/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "precalculus", "unit": "vectors", "a": {"title": "Vector Explorer", "path": "artifacts/precalculus-vector-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/precalculus-vector-explorer.jpg", "description": "Drag two vectors to see component-wise addition, tip-to-tail and parallelogram sums, u − v as u + (−v), and scalar multiples, with live components, magnitudes and direction angles.", "topics": ["Vector components", "Magnitude and direction", "Vector addition and scalar multiples"], "worksheet": "artifacts/precalculus-vector-explorer/worksheet.pdf", "answerKey": "artifacts/precalculus-vector-explorer/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "calculus", "unit": "limits-continuity", "a": {"title": "Limit Explorer", "path": "artifacts/calculus-limit-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/calculus-limit-explorer.jpg", "description": "Approach a point from both sides with tables and graphs for a hole, a moved point, a jump, a vertical asymptote, an oscillation and a continuous function. Set f(a) separately to see that the limit does not depend on it.", "topics": ["One-sided limits", "Limit vs. function value", "Types of discontinuity"], "worksheet": "artifacts/calculus-limit-explorer/worksheet.pdf", "answerKey": "artifacts/calculus-limit-explorer/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "calculus", "unit": "derivatives", "a": {"title": "Secant to Tangent", "path": "artifacts/calculus-secant-to-tangent/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/calculus-secant-to-tangent.jpg", "description": "Shrink h from both sides to watch secant slopes approach the tangent slope, see why |x| has no derivative at 0, and trace the tangent slopes into the graph of the derivative.", "topics": ["Difference quotient", "Tangent line slope", "Graph of the derivative"], "worksheet": "artifacts/calculus-secant-to-tangent/worksheet.pdf", "answerKey": "artifacts/calculus-secant-to-tangent/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "calculus", "unit": "antiderivatives-definite-integrals", "a": {"title": "Riemann Sum Lab", "path": "artifacts/calculus-riemann-sum-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/calculus-riemann-sum-lab.jpg", "description": "Build left, right, midpoint and trapezoid sums with up to 100 subintervals, compare them with the exact definite integral, and see how areas below the axis make the integral signed area rather than total area.", "topics": ["Riemann sums", "Definite integral as a limit", "Signed vs. total area"], "worksheet": "artifacts/calculus-riemann-sum-lab/worksheet.pdf", "answerKey": "artifacts/calculus-riemann-sum-lab/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "calculus", "unit": "fundamental-theorem-calculus", "a": {"title": "Accumulation Function Explorer", "path": "artifacts/calculus-accumulation-ftc/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/calculus-accumulation-ftc.jpg", "description": "Drag the upper limit of an accumulation function and watch A(x) = ∫ f(t) dt build up from signed area. See that the slope of A equals f(x), where A has maximums and minimums, and what changing the lower limit does.", "topics": ["Accumulation functions", "Fundamental Theorem of Calculus", "Signed area"], "worksheet": "artifacts/calculus-accumulation-ftc/worksheet.pdf", "answerKey": "artifacts/calculus-accumulation-ftc/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "prealgebra", "unit": "linear-functional-relationships", "a": {"title": "Slope-Intercept Explorer", "path": "artifacts/linear-equations-slope-slope-intercept-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/linear-equations-slope-slope-intercept-explorer.jpg", "description": "Use sliders or drag points to change m and b in y = mx + b. See the slope triangle, the table and parallel or perpendicular lines update live.", "topics": ["Slope", "y-intercept", "Parallel and perpendicular lines"], "worksheet": "artifacts/linear-equations-slope-slope-intercept-explorer/worksheet.pdf", "answerKey": "artifacts/linear-equations-slope-slope-intercept-explorer/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "prealgebra", "unit": "systems-linear-equations", "a": {"title": "Systems Explorer", "path": "artifacts/systems-of-equations-systems-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/systems-of-equations-systems-explorer.jpg", "description": "Adjust two lines and watch their intersection. Find systems with one, no or infinitely many solutions, then switch on inequality shading.", "topics": ["Solving by graphing", "Number of solutions", "Systems of inequalities"], "worksheet": "artifacts/systems-of-equations-systems-explorer/worksheet.pdf", "answerKey": "artifacts/systems-of-equations-systems-explorer/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "prealgebra", "unit": "congruence-similarity", "a": {"title": "Transformation Studio", "path": "artifacts/geometry-transformation-studio/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/geometry-transformation-studio.jpg", "description": "Apply translations, reflections, rotations and dilations to a triangle, read the coordinate rule, and see which transformations keep size and orientation.", "topics": ["Coordinate rules", "Rigid motions", "Dilations"], "worksheet": "artifacts/geometry-transformation-studio/worksheet.pdf", "answerKey": "artifacts/geometry-transformation-studio/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "precalculus", "unit": "functions", "a": {"title": "Transformation Lab", "path": "artifacts/algebra2-transformation-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/algebra2-transformation-lab.jpg", "description": "Transform six parent functions with a, b, h and k sliders and a ghost parent graph, and discover that the rules work the same way for every function.", "topics": ["Parent functions", "Shifts and stretches", "Reflections"], "worksheet": "artifacts/algebra2-transformation-lab/worksheet.pdf", "answerKey": "artifacts/algebra2-transformation-lab/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "precalculus", "unit": "functions", "a": {"title": "Asymptote & Hole Explorer", "path": "artifacts/algebra2-asymptote-hole-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/algebra2-asymptote-hole-explorer.jpg", "description": "Choose factors for the numerator and denominator to see holes, vertical asymptotes, horizontal asymptotes and x-intercepts appear on the graph.", "topics": ["Vertical asymptotes", "Holes", "Horizontal asymptotes"], "worksheet": "artifacts/algebra2-asymptote-hole-explorer/worksheet.pdf", "answerKey": "artifacts/algebra2-asymptote-hole-explorer/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "precalculus", "unit": "equations-inequalities", "a": {"title": "Feasible Region Optimizer", "path": "artifacts/algebra2-feasible-region-optimizer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/algebra2-feasible-region-optimizer.jpg", "description": "Explore a linear programming problem: see the feasible region, slide the objective line, and discover why the maximum and minimum occur at vertices.", "topics": ["Linear programming", "Feasible region", "Optimization"], "worksheet": "artifacts/algebra2-feasible-region-optimizer/worksheet.pdf", "answerKey": "artifacts/algebra2-feasible-region-optimizer/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "precalculus", "unit": "conics", "a": {"title": "Conic Explorer", "path": "artifacts/algebra2-conic-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/algebra2-conic-explorer.jpg", "description": "Explore circles, ellipses, hyperbolas and parabolas from their standard-form equations, with centers, foci, vertices and the directrix drawn live.", "topics": ["Circles and ellipses", "Hyperbolas", "Foci and directrix"], "worksheet": "artifacts/algebra2-conic-explorer/worksheet.pdf", "answerKey": "artifacts/algebra2-conic-explorer/teacher-key.pdf", "added": "2026-11-07"}}, {"course": "precalculus", "unit": "probability", "a": {"title": "Probability Simulation Lab", "path": "artifacts/algebra2-probability-simulation-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/algebra2-probability-simulation-lab.jpg", "description": "Simulate coins and dice to compare experimental and theoretical probability, then use mean and standard deviation sliders to explore the empirical rule.", "topics": ["Experimental probability", "Law of large numbers", "Normal distribution"], "worksheet": "artifacts/algebra2-probability-simulation-lab/worksheet.pdf", "answerKey": "artifacts/algebra2-probability-simulation-lab/teacher-key.pdf", "added": "2026-11-07"}}];
 ITEMS.forEach(function(it){
  var c=G.LIBRARY.courses.find(function(x){return x.id===it.course;});if(!c)return;
  var u=c.units.find(function(x){return x.id===it.unit;});if(!u||u.artifacts.some(function(a){return a.path===it.a.path;}))return;
  u.artifacts.push(it.a);
 });
})(window);

/* Interactive Math Statistics 2026-11-08: 7 tools for the Statistics course plus the Algebra 2 Probability Simulation Lab.
   Built from tools/interactive-math-statistics. Same pattern as the Interactive Math blocks above: an entry is skipped
   if its unit is missing or already lists that path. The active course lists these alongside its bank-driven resources. */
(function(G){
 var ITEMS=[{"course": "statistics", "unit": "anticipating-patterns", "a": {"title": "Sampling Distribution Lab", "path": "artifacts/statistics-sampling-distribution-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/statistics-sampling-distribution-lab.jpg", "description": "Draw samples from skewed, uniform, bimodal or normal populations (or a proportion) and build the sampling distribution of x̄ or p̂. See unbiasedness, how spread shrinks with √n, the Central Limit Theorem and the Large Counts condition.", "topics": ["Sampling distributions", "Central Limit Theorem", "Standard deviation of x̄ and p̂"], "worksheet": "artifacts/statistics-sampling-distribution-lab/worksheet.pdf", "answerKey": "artifacts/statistics-sampling-distribution-lab/teacher-key.pdf", "added": "2026-11-08"}}, {"course": "statistics", "unit": "statistical-inference", "a": {"title": "Confidence Interval Lab", "path": "artifacts/statistics-confidence-interval-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/statistics-confidence-interval-lab.jpg", "description": "Build hundreds of one-proportion z-intervals or one-mean t-intervals from repeated samples. Watch the capture rate, see how confidence level and sample size change the margin of error, and test what happens when conditions fail or z* replaces t*.", "topics": ["Confidence intervals", "Margin of error", "Conditions for inference"], "worksheet": "artifacts/statistics-confidence-interval-lab/worksheet.pdf", "answerKey": "artifacts/statistics-confidence-interval-lab/teacher-key.pdf", "added": "2026-11-08"}}, {"course": "statistics", "unit": "statistical-inference", "a": {"title": "Significance Test & Power Explorer", "path": "artifacts/statistics-significance-power-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/statistics-significance-power-explorer.jpg", "description": "Set H₀, Hₐ, α, n and the sample result for a one-proportion z test and watch the p-value appear as a tail area under the null model. Then compare the null and true models to see Type I error, Type II error and power, and what raises power.", "topics": ["p-values", "Type I and Type II errors", "Power"], "worksheet": "artifacts/statistics-significance-power-explorer/worksheet.pdf", "answerKey": "artifacts/statistics-significance-power-explorer/teacher-key.pdf", "added": "2026-11-08"}}, {"course": "statistics", "unit": "sampling-experimentation", "a": {"title": "Sampling Methods Lab", "path": "artifacts/statistics-sampling-methods-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/statistics-sampling-methods-lab.jpg", "description": "Take simple random, stratified, cluster, systematic and convenience samples from a 160-student population and repeat them hundreds of times. Separate bias (center) from variability (spread), see why a bigger convenience sample is still biased, and why stratifying helps.", "topics": ["Sampling methods", "Bias and variability", "Stratified and cluster sampling"], "worksheet": "artifacts/statistics-sampling-methods-lab/worksheet.pdf", "answerKey": "artifacts/statistics-sampling-methods-lab/teacher-key.pdf", "added": "2026-11-08"}}, {"course": "statistics", "unit": "sampling-experimentation", "a": {"title": "Random Assignment Lab", "path": "artifacts/statistics-random-assignment-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/statistics-random-assignment-lab.jpg", "description": "Compare random assignment, randomized matched pairs and letting students choose. See confounding create a fake effect, see random assignment balance GPA on average (but not every time), see pairing reduce variability, and find a p-value by re-randomizing the group labels.", "topics": ["Random assignment and confounding", "Matched pairs and blocking", "Randomization tests"], "worksheet": "artifacts/statistics-random-assignment-lab/worksheet.pdf", "answerKey": "artifacts/statistics-random-assignment-lab/teacher-key.pdf", "added": "2026-11-08"}}, {"course": "statistics", "unit": "anticipating-patterns", "a": {"title": "Conditional Probability: Screening Tests", "path": "artifacts/statistics-conditional-probability-explorer/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/statistics-conditional-probability-explorer.jpg", "description": "Link a tree diagram, a two-way table and a “who tests positive” bar to see why P(condition | positive) differs from P(positive | condition), how strongly it depends on the base rate and on specificity, and what independence looks like.", "topics": ["Conditional probability", "Two-way tables and tree diagrams", "Independence"], "worksheet": "artifacts/statistics-conditional-probability-explorer/worksheet.pdf", "answerKey": "artifacts/statistics-conditional-probability-explorer/teacher-key.pdf", "added": "2026-11-08"}}, {"course": "statistics", "unit": "exploring-data", "a": {"title": "Residuals & Influence Lab", "path": "artifacts/statistics-regression-influence-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/statistics-regression-influence-lab.jpg", "description": "Fit a least-squares line with a linked residual plot. See why a high r does not prove a line is the right model, separate outliers, high-leverage points and influential points with a movable extra point, and check what changing units does to the slope, r and r².", "topics": ["Least-squares regression", "Residual plots", "Outliers, leverage and influence"], "worksheet": "artifacts/statistics-regression-influence-lab/worksheet.pdf", "answerKey": "artifacts/statistics-regression-influence-lab/teacher-key.pdf", "added": "2026-11-08"}}, {"course": "statistics", "unit": "anticipating-patterns", "a": {"title": "Probability Simulation Lab", "path": "artifacts/algebra2-probability-simulation-lab/index.html", "bankFormat": "interactive-math", "type": "Interactive", "thumb": "thumbs/algebra2-probability-simulation-lab.jpg", "description": "Simulate coins and dice to compare experimental and theoretical probability, then use mean and standard deviation sliders to explore the empirical rule.", "topics": ["Experimental probability", "Law of large numbers", "Normal distribution"], "worksheet": "artifacts/algebra2-probability-simulation-lab/worksheet.pdf", "answerKey": "artifacts/algebra2-probability-simulation-lab/teacher-key.pdf", "added": "2026-11-08"}}];
 ITEMS.forEach(function(it){
  var c=G.LIBRARY.courses.find(function(x){return x.id===it.course;});if(!c)return;
  var u=c.units.find(function(x){return x.id===it.unit;});if(!u||u.artifacts.some(function(a){return a.path===it.a.path;}))return;
  u.artifacts.push(it.a);
 });
})(window);

