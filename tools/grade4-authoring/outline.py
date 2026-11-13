"""Grade 4 (math4) course outline: the single source of truth for units, skills and standards.
Skill order here == course-catalog.js order == skill IDs (<unit>-skill-NN). Do not reorder after publication."""
import json, os

COURSE_ID = "math4"
COURSE_NAME = "4th Grade Math"
PREFIX = "m4"
BLURB = "Place value, multi-digit operations, factors and patterns, fractions and decimals, measurement, geometry, and data."

# Common Core State Standards for Mathematics, Grade 4. The 2017 Massachusetts Curriculum Framework uses the same
# codes and adds 4.OA.A.3.a (multiplication and division facts through 12 x 12).
STANDARDS = {
    "4.OA.A.1": "Interpret a multiplication equation as a comparison (35 = 5 × 7 means 35 is 5 times as many as 7), and represent verbal statements of multiplicative comparisons as multiplication equations.",
    "4.OA.A.2": "Multiply or divide to solve word problems involving multiplicative comparison, distinguishing multiplicative comparison from additive comparison.",
    "4.OA.A.3": "Solve multistep word problems posed with whole numbers and having whole-number answers using the four operations, including problems in which remainders must be interpreted; represent them with equations with a letter for the unknown; assess reasonableness using mental computation and estimation, including rounding.",
    "4.OA.A.3.a": "(Massachusetts) Know multiplication facts and related division facts through 12 × 12.",
    "4.OA.B.4": "Find all factor pairs for a whole number in the range 1–100; recognize that a whole number is a multiple of each of its factors; determine whether a whole number is a multiple of a given one-digit number; determine whether a whole number in the range 1–100 is prime or composite.",
    "4.OA.C.5": "Generate a number or shape pattern that follows a given rule; identify apparent features of the pattern that were not explicit in the rule itself.",
    "4.NBT.A.1": "Recognize that in a multi-digit whole number, a digit in one place represents ten times what it represents in the place to its right.",
    "4.NBT.A.2": "Read and write multi-digit whole numbers using base-ten numerals, number names, and expanded form; compare two multi-digit numbers using >, =, and < symbols.",
    "4.NBT.A.3": "Use place value understanding to round multi-digit whole numbers to any place.",
    "4.NBT.B.4": "Fluently add and subtract multi-digit whole numbers using the standard algorithm.",
    "4.NBT.B.5": "Multiply a whole number of up to four digits by a one-digit whole number, and multiply two two-digit numbers, using strategies based on place value and the properties of operations; illustrate and explain with equations, rectangular arrays, and/or area models.",
    "4.NBT.B.6": "Find whole-number quotients and remainders with up to four-digit dividends and one-digit divisors, using strategies based on place value, the properties of operations, and/or the relationship between multiplication and division; illustrate and explain with equations, rectangular arrays, and/or area models.",
    "4.NF.A.1": "Explain why a fraction a/b is equivalent to a fraction (n × a)/(n × b) by using visual fraction models; use this principle to recognize and generate equivalent fractions.",
    "4.NF.A.2": "Compare two fractions with different numerators and different denominators by creating common denominators or numerators, or by comparing to a benchmark fraction such as 1/2; record the results with >, =, or <.",
    "4.NF.B.3.a": "Understand addition and subtraction of fractions as joining and separating parts referring to the same whole.",
    "4.NF.B.3.b": "Decompose a fraction into a sum of fractions with the same denominator in more than one way, recording each decomposition by an equation.",
    "4.NF.B.3.c": "Add and subtract mixed numbers with like denominators.",
    "4.NF.B.3.d": "Solve word problems involving addition and subtraction of fractions referring to the same whole and having like denominators.",
    "4.NF.B.4.a": "Understand a fraction a/b as a multiple of 1/b.",
    "4.NF.B.4.b": "Understand a multiple of a/b as a multiple of 1/b, and use this understanding to multiply a fraction by a whole number.",
    "4.NF.B.4.c": "Solve word problems involving multiplication of a fraction by a whole number.",
    "4.NF.C.5": "Express a fraction with denominator 10 as an equivalent fraction with denominator 100, and use this technique to add two fractions with respective denominators 10 and 100.",
    "4.NF.C.6": "Use decimal notation for fractions with denominators 10 or 100.",
    "4.NF.C.7": "Compare two decimals to hundredths by reasoning about their size; record the results with >, =, or <.",
    "4.MD.A.1": "Know relative sizes of measurement units within one system of units (km, m, cm; kg, g; lb, oz; l, ml; hr, min, sec); express measurements in a larger unit in terms of a smaller unit; record measurement equivalents in a two-column table.",
    "4.MD.A.2": "Use the four operations to solve word problems involving distances, intervals of time, liquid volumes, masses of objects, and money, including problems involving simple fractions or decimals; represent measurement quantities using diagrams such as number line diagrams.",
    "4.MD.A.3": "Apply the area and perimeter formulas for rectangles in real-world and mathematical problems.",
    "4.MD.B.4": "Make a line plot to display a data set of measurements in fractions of a unit (1/2, 1/4, 1/8); solve problems involving addition and subtraction of fractions by using information presented in line plots.",
    "4.MD.C.5.a": "An angle is measured with reference to a circle with its center at the common endpoint of the rays; an angle that turns through 1/360 of a circle is called a one-degree angle.",
    "4.MD.C.5.b": "An angle that turns through n one-degree angles is said to have an angle measure of n degrees.",
    "4.MD.C.6": "Measure angles in whole-number degrees using a protractor; sketch angles of specified measure.",
    "4.MD.C.7": "Recognize angle measure as additive; solve addition and subtraction problems to find unknown angles on a diagram in real-world and mathematical problems.",
    "4.G.A.1": "Draw points, lines, line segments, rays, angles (right, acute, obtuse), and perpendicular and parallel lines; identify these in two-dimensional figures.",
    "4.G.A.2": "Classify two-dimensional figures based on the presence or absence of parallel or perpendicular lines, or the presence or absence of angles of a specified size; recognize right triangles as a category.",
    "4.G.A.3": "Recognize a line of symmetry for a two-dimensional figure as a line across the figure such that the figure can be folded along the line into matching parts; identify line-symmetric figures and draw lines of symmetry.",
}

UNITS = [
    dict(id="place-value-number-sense", name="Place Value and Number Sense", abbr="pv", icon="blocks", color="#2f7fd8", strand="4.NBT",
         blurb="Place value to one million: reading, writing, comparing and rounding multi-digit whole numbers.",
         skills=[("Place Value to One Million", ["4.NBT.A.1"]),
                 ("Reading and Writing Multi-Digit Numbers", ["4.NBT.A.2"]),
                 ("Comparing and Ordering Whole Numbers", ["4.NBT.A.2"]),
                 ("Rounding Whole Numbers", ["4.NBT.A.3"])]),
    dict(id="multi-digit-addition-subtraction", name="Multi-Digit Addition and Subtraction", abbr="as", icon="plusminus", color="#1aa37a", strand="4.NBT",
         blurb="Add and subtract multi-digit numbers with the standard algorithm, estimate, and solve word problems.",
         skills=[("Adding Multi-Digit Whole Numbers", ["4.NBT.B.4"]),
                 ("Subtracting Multi-Digit Whole Numbers", ["4.NBT.B.4"]),
                 ("Subtracting Across Zeros", ["4.NBT.B.4"]),
                 ("Estimating Sums and Differences", ["4.NBT.A.3", "4.OA.A.3"]),
                 ("Addition and Subtraction Word Problems", ["4.NBT.B.4", "4.OA.A.3"])]),
    dict(id="multiplication-strategies", name="Multiplication Strategies and Multi-Digit Multiplication", abbr="ms", icon="array", color="#e2563b", strand="4.NBT",
         blurb="Multiplicative comparison, multiples of ten, area models, partial products and two-digit multiplication.",
         skills=[("Multiplicative Comparisons", ["4.OA.A.1", "4.OA.A.2"]),
                 ("Multiplying by Multiples of 10, 100, and 1,000", ["4.NBT.B.5", "4.OA.A.3.a"]),
                 ("Multiplying by One-Digit Numbers", ["4.NBT.B.5"]),
                 ("Multiplying Two-Digit Numbers", ["4.NBT.B.5"]),
                 ("Estimating Products and Multiplication Word Problems", ["4.NBT.B.5", "4.OA.A.3"])]),
    dict(id="division-remainders", name="Division and Remainders", abbr="dv", icon="groups", color="#8a4fd6", strand="4.NBT",
         blurb="Division facts and patterns, area models and partial quotients, remainders and what they mean.",
         skills=[("Division Facts and Patterns", ["4.NBT.B.6", "4.OA.A.3.a"]),
                 ("Dividing with Models and Partial Quotients", ["4.NBT.B.6"]),
                 ("Dividing by One-Digit Divisors", ["4.NBT.B.6"]),
                 ("Division with Remainders", ["4.NBT.B.6"]),
                 ("Interpreting Remainders in Word Problems", ["4.OA.A.3", "4.OA.A.2"])]),
    dict(id="factors-multiples-patterns", name="Factors, Multiples, and Number Patterns", abbr="fm", icon="pattern", color="#0f97b5", strand="4.OA",
         blurb="Factor pairs, multiples, prime and composite numbers, and number and shape patterns.",
         skills=[("Factors and Factor Pairs", ["4.OA.B.4"]),
                 ("Multiples", ["4.OA.B.4"]),
                 ("Prime and Composite Numbers", ["4.OA.B.4"]),
                 ("Number Patterns and Rules", ["4.OA.C.5"]),
                 ("Shape Patterns and Pattern Features", ["4.OA.C.5"])]),
    dict(id="fractions-equivalent-fractions", name="Fractions and Equivalent Fractions", abbr="fe", icon="fraction", color="#d63c7a", strand="4.NF",
         blurb="Equivalent fractions with models and multiplication, simplest form, and comparing and ordering fractions.",
         skills=[("Understanding Equivalent Fractions", ["4.NF.A.1"]),
                 ("Generating Equivalent Fractions", ["4.NF.A.1"]),
                 ("Comparing Fractions with Common Denominators or Numerators", ["4.NF.A.2"]),
                 ("Comparing Fractions with Benchmarks", ["4.NF.A.2"]),
                 ("Ordering Fractions", ["4.NF.A.2"])]),
    dict(id="fraction-operations-decimals", name="Fraction Operations and Decimals", abbr="fd", icon="decimal", color="#f08c1a", strand="4.NF",
         blurb="Add and subtract fractions and mixed numbers with like denominators, multiply fractions by whole numbers, and use decimals to hundredths.",
         skills=[("Decomposing Fractions", ["4.NF.B.3.a", "4.NF.B.3.b"]),
                 ("Adding and Subtracting Fractions with Like Denominators", ["4.NF.B.3.a", "4.NF.B.3.d"]),
                 ("Adding and Subtracting Mixed Numbers", ["4.NF.B.3.c", "4.NF.B.3.d"]),
                 ("Multiplying a Fraction by a Whole Number", ["4.NF.B.4.a", "4.NF.B.4.b", "4.NF.B.4.c"]),
                 ("Tenths and Hundredths as Fractions and Decimals", ["4.NF.C.5", "4.NF.C.6"]),
                 ("Comparing Decimals", ["4.NF.C.7"])]),
    dict(id="measurement-unit-conversions", name="Measurement and Unit Conversions", abbr="mc", icon="ruler", color="#5a62d8", strand="4.MD",
         blurb="Customary and metric units, conversion tables, elapsed time, money, and area and perimeter of rectangles.",
         skills=[("Customary Units and Conversions", ["4.MD.A.1"]),
                 ("Metric Units and Conversions", ["4.MD.A.1"]),
                 ("Time and Elapsed Time", ["4.MD.A.1", "4.MD.A.2"]),
                 ("Measurement and Money Word Problems", ["4.MD.A.2"]),
                 ("Area and Perimeter of Rectangles", ["4.MD.A.3"])]),
    dict(id="geometry-angles-symmetry", name="Geometry, Angles, and Symmetry", abbr="ga", icon="angle", color="#c2410c", strand="4.G",
         blurb="Lines, rays and angles, measuring angles, adding angle measures, classifying shapes, and lines of symmetry.",
         skills=[("Points, Lines, Rays, and Angles", ["4.G.A.1"]),
                 ("Measuring Angles", ["4.MD.C.5.a", "4.MD.C.5.b", "4.MD.C.6"]),
                 ("Adding and Subtracting Angle Measures", ["4.MD.C.7"]),
                 ("Classifying Triangles and Quadrilaterals", ["4.G.A.2"]),
                 ("Lines of Symmetry", ["4.G.A.3"])]),
    dict(id="data-line-plots-word-problems", name="Data, Line Plots, and Multi-Step Word Problems", abbr="dp", icon="lineplot", color="#16803c", strand="4.MD",
         blurb="Make and read line plots with fractions, solve problems with data, and solve multi-step word problems.",
         skills=[("Reading and Making Line Plots", ["4.MD.B.4"]),
                 ("Solving Problems with Line Plots", ["4.MD.B.4"]),
                 ("Multi-Step Word Problems", ["4.OA.A.3"]),
                 ("Equations and Reasonable Answers", ["4.OA.A.3"])]),
]


def skill_records(unit):
    return [dict(id=f"{unit['id']}-skill-{i:02d}", index=i, name=n, standards=s) for i, (n, s) in enumerate(unit["skills"], 1)]


def all_skills():
    for u in UNITS:
        for r in skill_records(u):
            yield u, r


if __name__ == "__main__":
    covered = {s for _, r in all_skills() for s in r["standards"]}
    print(len(UNITS), "units", sum(len(u["skills"]) for u in UNITS), "skills", f"{len(covered)}/{len(STANDARDS)} standards")
    print("uncovered:", sorted(set(STANDARDS) - covered))
    out = dict(id=COURSE_ID, name=COURSE_NAME, prefix=PREFIX, blurb=BLURB, standards=STANDARDS,
               units=[dict(u, skills=[[n, s] for n, s in u["skills"]]) for u in UNITS])
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "outline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
