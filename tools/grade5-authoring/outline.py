"""Grade 5 (math5) course outline: the single source of truth for units, skills and standards.
Skill order here == course-catalog.js order == skill IDs (<unit>-skill-NN). Do not reorder after publication."""

COURSE_ID = "math5"
COURSE_NAME = "5th Grade Math"
PREFIX = "m5"

# Massachusetts 2017 Mathematics Curriculum Framework, Grade 5 (identical codes to Common Core Grade 5).
STANDARDS = {
    "5.OA.A.1": "Use parentheses, brackets, or braces in numerical expressions, and evaluate expressions with these symbols.",
    "5.OA.A.2": "Write simple expressions that record calculations with numbers, and interpret numerical expressions without evaluating them.",
    "5.OA.B.3": "Generate two numerical patterns using two given rules; identify relationships between corresponding terms; form and graph ordered pairs.",
    "5.NBT.A.1": "Recognize that in a multi-digit number, a digit in one place represents 10 times as much as it represents in the place to its right and 1/10 of what it represents in the place to its left.",
    "5.NBT.A.2": "Explain patterns in the number of zeros of the product when multiplying a number by powers of 10, and patterns in the placement of the decimal point; use whole-number exponents to denote powers of 10.",
    "5.NBT.A.3.a": "Read and write decimals to thousandths using base-ten numerals, number names, and expanded form.",
    "5.NBT.A.3.b": "Compare two decimals to thousandths based on meanings of the digits in each place, using >, =, and < symbols.",
    "5.NBT.A.4": "Use place value understanding to round decimals to any place.",
    "5.NBT.B.5": "Fluently multiply multi-digit whole numbers using the standard algorithm.",
    "5.NBT.B.6": "Find whole-number quotients of whole numbers with up to four-digit dividends and two-digit divisors, using strategies based on place value, properties of operations, and the relationship between multiplication and division.",
    "5.NBT.B.7": "Add, subtract, multiply, and divide decimals to hundredths, using concrete models or drawings and strategies based on place value.",
    "5.NF.A.1": "Add and subtract fractions with unlike denominators (including mixed numbers) by replacing given fractions with equivalent fractions.",
    "5.NF.A.2": "Solve word problems involving addition and subtraction of fractions referring to the same whole; use benchmark fractions and number sense to estimate and assess reasonableness.",
    "5.NF.B.3": "Interpret a fraction as division of the numerator by the denominator; solve word problems involving division of whole numbers leading to answers in the form of fractions or mixed numbers.",
    "5.NF.B.4.a": "Interpret the product (a/b) × q as a parts of a partition of q into b equal parts; equivalently, as the result of a sequence of operations a × q ÷ b.",
    "5.NF.B.4.b": "Find the area of a rectangle with fractional side lengths by tiling it with unit squares of the appropriate unit fraction side lengths, and show that the area is the same as would be found by multiplying the side lengths.",
    "5.NF.B.5.a": "Interpret multiplication as scaling: compare the size of a product to the size of one factor on the basis of the size of the other factor, without performing the indicated multiplication.",
    "5.NF.B.5.b": "Explain why multiplying by a fraction greater than 1 results in a product greater than the given number, and by a fraction less than 1 in a product smaller than the given number; relate to equivalence a/b = (n × a)/(n × b).",
    "5.NF.B.6": "Solve real-world problems involving multiplication of fractions and mixed numbers.",
    "5.NF.B.7.a": "Interpret division of a unit fraction by a non-zero whole number, and compute such quotients.",
    "5.NF.B.7.b": "Interpret division of a whole number by a unit fraction, and compute such quotients.",
    "5.NF.B.7.c": "Solve real-world problems involving division of unit fractions by non-zero whole numbers and division of whole numbers by unit fractions.",
    "5.MD.A.1": "Convert among different-sized standard measurement units within a given measurement system, and use these conversions in solving multi-step, real-world problems.",
    "5.MD.B.2": "Make a line plot (dot plot) to display a data set of measurements in fractions of a unit; use operations on fractions to solve problems involving information presented in line plots.",
    "5.MD.C.3.a": "A cube with side length 1 unit, called a unit cube, is said to have one cubic unit of volume, and can be used to measure volume.",
    "5.MD.C.3.b": "A solid figure which can be packed without gaps or overlaps using n unit cubes is said to have a volume of n cubic units.",
    "5.MD.C.4": "Measure volumes by counting unit cubes, using cubic cm, cubic in., cubic ft., and non-standard units.",
    "5.MD.C.5.a": "Find the volume of a right rectangular prism with whole-number edge lengths by packing it with unit cubes, and show that the volume is the same as multiplying the edge lengths or multiplying the height by the area of the base.",
    "5.MD.C.5.b": "Apply the formulas V = l × w × h and V = B × h for rectangular prisms to find volumes in real-world and mathematical problems.",
    "5.MD.C.5.c": "Recognize volume as additive; find volumes of solid figures composed of two non-overlapping right rectangular prisms.",
    "5.G.A.1": "Use a pair of perpendicular number lines (axes) to define a coordinate system; locate a point using an ordered pair of numbers (its coordinates).",
    "5.G.A.2": "Represent real-world and mathematical problems by graphing points in the first quadrant of the coordinate plane, and interpret coordinate values of points in the context of the situation.",
    "5.G.B.3": "Understand that attributes belonging to a category of two-dimensional figures also belong to all subcategories of that category.",
    "5.G.B.4": "Classify two-dimensional figures in a hierarchy based on properties.",
}

UNITS = [
    dict(id="place-value-number-sense", name="Place Value and Number Sense", abbr="pv", icon="blocks", color="#2f7fd8",
         blurb="Place value patterns, powers of ten, and reading, comparing and rounding decimals.",
         skills=[("Place Value Patterns", ["5.NBT.A.1"]),
                 ("Powers of Ten and Exponents", ["5.NBT.A.2"]),
                 ("Reading and Writing Decimals", ["5.NBT.A.3.a"]),
                 ("Comparing and Ordering Decimals", ["5.NBT.A.3.b"]),
                 ("Rounding Decimals", ["5.NBT.A.4"])]),
    dict(id="multi-digit-multiplication-division", name="Multi-Digit Multiplication and Division", abbr="md", icon="array", color="#e2563b",
         blurb="Multiply with the standard algorithm, estimate, and divide with area models and partial quotients.",
         skills=[("Multiplying Multi-Digit Whole Numbers", ["5.NBT.B.5"]),
                 ("Estimating Products and Quotients", ["5.NBT.B.5", "5.NBT.B.6"]),
                 ("Dividing by One-Digit Divisors", ["5.NBT.B.6"]),
                 ("Dividing by Two-Digit Divisors", ["5.NBT.B.6"]),
                 ("Interpreting Remainders in Word Problems", ["5.NBT.B.6"])]),
    dict(id="decimal-operations", name="Decimal Operations", abbr="do", icon="decimal", color="#1aa37a",
         blurb="Add, subtract, multiply and divide decimals to hundredths with models and place value.",
         skills=[("Adding and Subtracting Decimals", ["5.NBT.B.7"]),
                 ("Multiplying Decimals by Whole Numbers", ["5.NBT.B.7"]),
                 ("Multiplying Decimals by Decimals", ["5.NBT.B.7"]),
                 ("Dividing Decimals by Whole Numbers", ["5.NBT.B.7"]),
                 ("Dividing by Decimals", ["5.NBT.B.7"]),
                 ("Decimal Word Problems and Money", ["5.NBT.B.7"])]),
    dict(id="numerical-expressions-patterns", name="Numerical Expressions and Patterns", abbr="ep", icon="brackets", color="#8a4fd6",
         blurb="Grouping symbols, writing and interpreting expressions, and comparing two number patterns.",
         skills=[("Order of Operations with Grouping Symbols", ["5.OA.A.1"]),
                 ("Writing Numerical Expressions", ["5.OA.A.2"]),
                 ("Interpreting Expressions Without Evaluating", ["5.OA.A.2"]),
                 ("Generating Numerical Patterns", ["5.OA.B.3"]),
                 ("Relationships Between Two Patterns", ["5.OA.B.3"])]),
    dict(id="fraction-addition-subtraction", name="Fraction Concepts and Operations", abbr="fa", icon="fraction-circle", color="#f08c1a",
         blurb="Equivalent fractions, adding and subtracting unlike denominators and mixed numbers, and estimating.",
         skills=[("Equivalent Fractions and Common Denominators", ["5.NF.A.1"]),
                 ("Adding Fractions with Unlike Denominators", ["5.NF.A.1"]),
                 ("Subtracting Fractions with Unlike Denominators", ["5.NF.A.1"]),
                 ("Adding and Subtracting Mixed Numbers", ["5.NF.A.1"]),
                 ("Estimating with Benchmark Fractions", ["5.NF.A.2"]),
                 ("Fraction Word Problems", ["5.NF.A.2"])]),
    dict(id="fraction-multiplication-division", name="Multiplying and Dividing Fractions", abbr="fm", icon="fraction-bar", color="#d63c7a",
         blurb="Fractions as division, multiplying fractions, scaling, area, and dividing with unit fractions.",
         skills=[("Fractions as Division", ["5.NF.B.3"]),
                 ("Multiplying a Fraction by a Whole Number", ["5.NF.B.4.a"]),
                 ("Multiplying Fractions by Fractions", ["5.NF.B.4.a", "5.NF.B.6"]),
                 ("Area with Fractional Side Lengths", ["5.NF.B.4.b"]),
                 ("Multiplication as Scaling", ["5.NF.B.5.a", "5.NF.B.5.b"]),
                 ("Dividing Unit Fractions and Whole Numbers", ["5.NF.B.7.a", "5.NF.B.7.b"]),
                 ("Fraction Multiplication and Division Word Problems", ["5.NF.B.6", "5.NF.B.7.c"])]),
    dict(id="measurement-conversions", name="Measurement and Conversions", abbr="mc", icon="ruler", color="#0f97b5",
         blurb="Convert customary and metric units and solve multi-step measurement problems.",
         skills=[("Customary Length Conversions", ["5.MD.A.1"]),
                 ("Customary Weight and Capacity Conversions", ["5.MD.A.1"]),
                 ("Metric Conversions", ["5.MD.A.1", "5.NBT.A.2"]),
                 ("Multi-Step Measurement Problems", ["5.MD.A.1"])]),
    dict(id="volume-three-dimensional-figures", name="Volume and Three-Dimensional Figures", abbr="vo", icon="cubes", color="#5a62d8",
         blurb="Unit cubes, counting cubes, V = l × w × h and V = B × h, and composite figures.",
         skills=[("Understanding Volume and Unit Cubes", ["5.MD.C.3.a", "5.MD.C.3.b"]),
                 ("Counting Cubes to Find Volume", ["5.MD.C.4"]),
                 ("Volume Formulas", ["5.MD.C.5.a", "5.MD.C.5.b"]),
                 ("Volume of Composite Figures", ["5.MD.C.5.c"]),
                 ("Volume Word Problems", ["5.MD.C.5.b"])]),
    dict(id="coordinate-plane-graphing", name="Coordinate Planes and Graphing", abbr="cp", icon="grid", color="#2a9d4b",
         blurb="Axes, origin and ordered pairs; plotting points; real-world graphs; graphing patterns.",
         skills=[("The Coordinate System", ["5.G.A.1"]),
                 ("Plotting and Reading Points", ["5.G.A.1"]),
                 ("Real-World Problems on the Coordinate Plane", ["5.G.A.2"]),
                 ("Graphing Patterns and Relationships", ["5.OA.B.3", "5.G.A.2"])]),
    dict(id="classifying-two-dimensional-figures", name="Geometry and Classifying Shapes", abbr="cs", icon="shapes", color="#c9481f",
         blurb="Polygon attributes, triangles, quadrilaterals, and shape hierarchies.",
         skills=[("Polygons and Their Attributes", ["5.G.B.3"]),
                 ("Classifying Triangles", ["5.G.B.3", "5.G.B.4"]),
                 ("Classifying Quadrilaterals", ["5.G.B.4"]),
                 ("Shape Hierarchies", ["5.G.B.3", "5.G.B.4"])]),
    dict(id="data-line-plots-problem-solving", name="Data, Line Plots, and Problem Solving", abbr="dl", icon="lineplot", color="#b8860b",
         blurb="Read and make line plots with fractions, solve problems with the data, and mixed problem solving.",
         skills=[("Reading Line Plots with Fractions", ["5.MD.B.2"]),
                 ("Making Line Plots", ["5.MD.B.2"]),
                 ("Solving Problems with Line Plot Data", ["5.MD.B.2", "5.NF.A.2", "5.NF.B.6"]),
                 ("Multi-Step Problem Solving", ["5.NBT.B.7", "5.NF.A.2", "5.MD.A.1"])]),
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
