/* Standards shown on teacher copies (lesson planner, worksheet / assessment / printable answer keys).

   MKSTD.split(text|array)      → normalized codes ("A.SSE.A.1a" → "A-SSE.A.1a", "7.NS.A.2.D" → "7.NS.A.2d")
   MKSTD.describe(code)         → a short plain-language summary of the standard ('' if unknown)
   MKSTD.forSkill(set, skill)   → codes a generator skill addresses (standards-map.js, built by
                                  scripts/build_standards_map.cjs from the planner lessons and the question banks)
   MKSTD.forProblem(p, set)     → codes for one generated problem (its bank question's own tags first)
   MKSTD.summaryHtml(rows)      → the "Standards addressed" table for a teacher key
   MKSTD.chipsHtml(codes)       → small code chips for a key row

   Summaries paraphrase the Common Core State Standards for Mathematics (CCSS-M). Calculus and Statistics
   banks are tagged with AP framework codes, which are shown with their big idea / topic area. */
(function (G) {
  'use strict';
  var STD = {};

  /* ---------- normalizing ---------- */
  function norm(c) {
    c = String(c || '').replace(/[‐-–]/g, function (x) { return x === '–' ? '–' : '-'; }).replace(/\s+/g, ' ').trim();
    if (!c) return '';
    if (/^AP/.test(c)) return c;
    var m = /^(?:HS)?([NAFGS])[.\-]([A-Z]{1,4})(\.|$)(.*)$/.exec(c);
    if (m) c = m[1] + '-' + m[2] + (m[4] ? '.' + m[4] : '');
    c = c.replace(/^([0-9]\.[A-Z]+\.[A-Z]\.[0-9]+)\.([A-Da-d])$/, function (x, a, l) { return a + l.toLowerCase(); })
         .replace(/^([NAFGS]-[A-Z]+\.[A-Z]\.[0-9]+)\.([A-Da-d])$/, function (x, a, l) { return a + l.toLowerCase(); });
    return c;
  }
  STD.norm = norm;
  STD.split = function (v) {
    var list = Array.isArray(v) ? v : String(v || '').split(/[,;]\s*/);
    var out = [];
    list.forEach(function (x) { var c = norm(x); if (c && out.indexOf(c) < 0) out.push(c); });
    return out;
  };
  STD.isPractice = function (c) { return /^(SMP|MP)\b/.test(c); };
  /* Content standards only (the Standards for Mathematical Practice apply to every lesson). */
  STD.content = function (list) { return (list || []).filter(function (c) { return !STD.isPractice(c); }); };

  /* ---------- summaries ---------- */
  var D = {
    /* Mathematical practices */
    'SMP 1–8': 'Standards for Mathematical Practice 1–8 (make sense of problems, reason, argue, model, use tools, precision, structure, regularity).',
    'MP.1': 'Make sense of problems and persevere in solving them.',
    'MP.2': 'Reason abstractly and quantitatively.',
    'MP.3': 'Construct viable arguments and critique the reasoning of others.',
    'MP.4': 'Model with mathematics.',
    'MP.5': 'Use appropriate tools strategically.',
    'MP.6': 'Attend to precision.',
    'MP.7': 'Look for and make use of structure.',
    'MP.8': 'Look for and express regularity in repeated reasoning.',

    /* Grade 4–5 */
    '4.G.A.1': 'Draw and identify points, lines, segments, rays, angles, and perpendicular and parallel lines.',
    '4.G.A.3': 'Recognize and draw lines of symmetry in two-dimensional figures.',
    '4.NF.A.1': 'Explain why fractions are equivalent and generate equivalent fractions.',
    '4.OA.B.4': 'Find factor pairs and multiples; decide whether a whole number is prime or composite.',
    '5.G.B.3': 'Understand that attributes of a category of two-dimensional figures belong to its subcategories.',
    '5.MD.A.1': 'Convert among different-sized standard measurement units within one system.',
    '5.NBT.A.1': 'Understand place value: a digit is 10 times what it represents one place to its right.',
    '5.NBT.A.3': 'Read, write and compare decimals to thousandths.',
    '5.NBT.A.4': 'Use place value to round decimals to any place.',
    '5.NF.A.1': 'Add and subtract fractions with unlike denominators.',
    '5.OA.A.1': 'Use parentheses, brackets or braces in numerical expressions and evaluate them.',
    '5.OA.B.3': 'Generate two numerical patterns from rules and compare corresponding terms.',
    '5.G.A.1': 'Use a pair of perpendicular number lines (axes) to define a coordinate system; locate a point using an ordered pair of numbers (its coordinates).',
    '5.G.A.2': 'Represent real-world and mathematical problems by graphing points in the first quadrant of the coordinate plane, and interpret coordinate values of points in the context of the situation.',
    '5.G.B.4': 'Classify two-dimensional figures in a hierarchy based on properties.',
    '5.MD.B.2': 'Make a line plot (dot plot) to display a data set of measurements in fractions of a unit; use operations on fractions to solve problems involving information presented in line plots.',
    '5.MD.C.3a': 'A unit cube has one cubic unit of volume and can be used to measure volume.',
    '5.MD.C.3b': 'A solid packed with n unit cubes without gaps or overlaps has a volume of n cubic units.',
    '5.MD.C.4': 'Measure volumes by counting unit cubes, using cubic cm, cubic in., cubic ft., and non-standard units.',
    '5.MD.C.5a': 'Find the volume of a rectangular prism by packing it with unit cubes; relate to multiplying edge lengths.',
    '5.MD.C.5b': 'Apply V = l × w × h and V = B × h to find volumes of rectangular prisms.',
    '5.MD.C.5c': 'Recognize volume as additive; find volumes of figures made of two rectangular prisms.',
    '5.NBT.A.2': 'Explain patterns in the number of zeros of the product when multiplying a number by powers of 10, and patterns in the placement of the decimal point; use whole-number exponents to denote powers of 10.',
    '5.NBT.A.3.a': 'Read and write decimals to thousandths using base-ten numerals, number names, and expanded form.',
    '5.NBT.A.3.b': 'Compare two decimals to thousandths based on meanings of the digits in each place, using >, =, and < symbols.',
    '5.NBT.B.5': 'Fluently multiply multi-digit whole numbers using the standard algorithm.',
    '5.NBT.B.6': 'Find whole-number quotients of whole numbers with up to four-digit dividends and two-digit divisors, using strategies based on place value, properties of operations, and the relationship between multiplication and division.',
    '5.NBT.B.7': 'Add, subtract, multiply, and divide decimals to hundredths, using concrete models or drawings and strategies based on place value.',
    '5.NF.A.2': 'Solve word problems involving addition and subtraction of fractions referring to the same whole; use benchmark fractions and number sense to estimate and assess reasonableness.',
    '5.NF.B.3': 'Interpret a fraction as division of the numerator by the denominator; solve word problems involving division of whole numbers leading to answers in the form of fractions or mixed numbers.',
    '5.NF.B.4a': 'Interpret (a/b) × q as a parts of q split into b equal parts.',
    '5.NF.B.4b': 'Find the area of a rectangle with fractional side lengths by tiling and by multiplying.',
    '5.NF.B.5a': 'Compare the size of a product to one factor based on the size of the other factor.',
    '5.NF.B.5b': 'Explain why multiplying by a fraction greater or less than 1 makes a product greater or smaller.',
    '5.NF.B.6': 'Solve real-world problems involving multiplication of fractions and mixed numbers.',
    '5.NF.B.7a': 'Divide a unit fraction by a whole number.',
    '5.NF.B.7b': 'Divide a whole number by a unit fraction.',
    '5.NF.B.7c': 'Solve word problems dividing unit fractions by whole numbers and whole numbers by unit fractions.',
    '5.OA.A.2': 'Write simple expressions that record calculations with numbers, and interpret numerical expressions without evaluating them.',

    /* Grade 6 */
    '6.EE': 'Expressions and Equations (grade 6).',
    '6.EE.A.1': 'Write and evaluate numerical expressions with whole-number exponents.',
    '6.EE.A.2': 'Write, read and evaluate expressions in which letters stand for numbers.',
    '6.EE.A.2a': 'Write expressions that record operations with numbers and letters.',
    '6.EE.A.2b': 'Identify parts of an expression (sum, term, product, factor, quotient, coefficient).',
    '6.EE.A.2c': 'Evaluate expressions at specific values of their variables, using order of operations.',
    '6.EE.A.3': 'Apply the properties of operations to generate equivalent expressions.',
    '6.EE.A.4': 'Identify when two expressions are equivalent.',
    '6.EE.B.5': 'Understand solving an equation or inequality as finding the values that make it true.',
    '6.EE.B.6': 'Use variables to represent numbers and write expressions for real-world problems.',
    '6.EE.B.7': 'Write and solve one-step equations x + p = q and px = q.',
    '6.EE.B.8': 'Write inequalities x > c or x < c and graph their solutions on a number line.',
    '6.EE.C.9': 'Use variables for two quantities that change together; relate tables, graphs and equations.',
    '6.G.A.1': 'Find the area of triangles, special quadrilaterals and polygons by composing or decomposing.',
    '6.G.A.2': 'Find the volume of a right rectangular prism with fractional edge lengths.',
    '6.G.A.3': 'Draw polygons in the coordinate plane; find side lengths from coordinates.',
    '6.G.A.4': 'Use nets to represent three-dimensional figures and find surface area.',
    '6.NS.A.1': 'Interpret and compute quotients of fractions.',
    '6.NS.B.2': 'Fluently divide multi-digit numbers using the standard algorithm.',
    '6.NS.B.3': 'Fluently add, subtract, multiply and divide multi-digit decimals.',
    '6.NS.B.4': 'Find the greatest common factor and least common multiple; use the distributive property.',
    '6.NS.C.5': 'Use positive and negative numbers to represent quantities in real-world contexts.',
    '6.NS.C.6': 'Understand rational numbers as points on the number line and coordinate plane.',
    '6.NS.C.6a': 'Recognize opposite signs as opposite sides of 0; the opposite of the opposite is the number.',
    '6.NS.C.6b': 'Understand signs of ordered pairs as quadrants; reflections across the axes.',
    '6.NS.C.6c': 'Find and position integers and other rational numbers on a number line and coordinate plane.',
    '6.NS.C.7': 'Understand ordering and absolute value of rational numbers.',
    '6.NS.C.7a': 'Interpret statements of inequality as relative position on a number line.',
    '6.NS.C.7b': 'Write, interpret and explain statements of order for rational numbers in context.',
    '6.NS.C.7c': 'Understand absolute value as distance from 0.',
    '6.NS.C.7d': 'Distinguish comparisons of absolute value from statements about order.',
    '6.NS.C.8': 'Solve problems by graphing points in all four quadrants; distance with a shared coordinate.',
    '6.RP.A.1': 'Understand ratios and use ratio language to describe a relationship between two quantities.',
    '6.RP.A.2': 'Understand unit rates associated with ratios.',
    '6.RP.A.3': 'Use ratio and rate reasoning to solve real-world problems.',
    '6.RP.A.3a': 'Make tables of equivalent ratios; plot pairs on the coordinate plane; compare ratios.',
    '6.RP.A.3b': 'Solve unit rate problems, including unit pricing and constant speed.',
    '6.RP.A.3c': 'Find a percent of a quantity as a rate per 100; find the whole from a part and percent.',
    '6.RP.A.3d': 'Use ratio reasoning to convert measurement units.',
    '6.SP.A.1': 'Recognize a statistical question, one that anticipates variability in the data.',
    '6.SP.A.2': 'Understand that a data distribution has a center, a spread and an overall shape.',
    '6.SP.A.3': 'A measure of center summarizes the data with one number; a measure of variation describes spread.',
    '6.SP.B.4': 'Display numerical data in dot plots, histograms and box plots.',
    '6.SP.B.5': 'Summarize numerical data sets in relation to their context.',
    '6.SP.B.5a': 'Report the number of observations.',
    '6.SP.B.5c': 'Give measures of center (median, mean) and variability (IQR, MAD) and describe patterns.',
    '6.SP.B.5d': 'Relate the choice of measures of center and variability to the shape of the data.',

    /* Grade 7 */
    '7.EE': 'Expressions and Equations (grade 7).',
    '7.EE.A.1': 'Add, subtract, factor and expand linear expressions with rational coefficients.',
    '7.EE.A.2': 'Rewrite an expression in different forms to show how quantities are related.',
    '7.EE.B.3': 'Solve multi-step problems with positive and negative rational numbers in any form.',
    '7.EE.B.4': 'Use variables to construct simple equations and inequalities to solve problems.',
    '7.EE.B.4a': 'Solve equations px + q = r and p(x + q) = r fluently.',
    '7.EE.B.4b': 'Solve inequalities px + q > r or px + q < r and graph the solution set.',
    '7.G.A.1': 'Solve problems involving scale drawings, including computing actual lengths and areas.',
    '7.G.A.2': 'Draw geometric shapes with given conditions; decide when conditions give a unique triangle.',
    '7.G.A.3': 'Describe the two-dimensional cross sections of three-dimensional figures.',
    '7.G.B.4': 'Know and use the formulas for the area and circumference of a circle.',
    '7.G.B.5': 'Use supplementary, complementary, vertical and adjacent angles to find unknown angles.',
    '7.G.B.6': 'Solve problems involving area, volume and surface area of two- and three-dimensional objects.',
    '7.NS': 'The Number System (grade 7): operations with rational numbers.',
    '7.NS.A.1': 'Add and subtract rational numbers; represent addition and subtraction on a number line.',
    '7.NS.A.1-3': 'Add, subtract, multiply and divide rational numbers, including real-world problems.',
    '7.NS.A.1b': 'Understand p + q as the number |q| from p; additive inverses sum to 0.',
    '7.NS.A.1c': 'Understand subtraction as adding the additive inverse: p − q = p + (−q).',
    '7.NS.A.1d': 'Apply properties of operations to add and subtract rational numbers.',
    '7.NS.A.2': 'Multiply and divide rational numbers.',
    '7.NS.A.2a': 'Understand the rules for multiplying signed numbers from the properties of operations.',
    '7.NS.A.2b': 'Understand that integers can be divided (nonzero divisor) and quotients are rational.',
    '7.NS.A.2d': 'Convert a rational number to a decimal; it terminates or eventually repeats.',
    '7.NS.A.3': 'Solve real-world problems with the four operations on rational numbers.',
    '7.RP': 'Ratios and Proportional Relationships (grade 7).',
    '7.RP.A.1': 'Compute unit rates with ratios of fractions.',
    '7.RP.A.2': 'Recognize and represent proportional relationships between quantities.',
    '7.RP.A.2a': 'Decide whether two quantities are proportional (tables, graphs through the origin).',
    '7.RP.A.2b': 'Identify the constant of proportionality in tables, graphs, equations and diagrams.',
    '7.RP.A.2c': 'Represent proportional relationships by equations, such as t = pn.',
    '7.RP.A.3': 'Use proportional relationships to solve multistep ratio and percent problems.',
    '7.SP.A.1': 'Understand that random samples support valid inferences about a population.',
    '7.SP.A.2': 'Use data from a random sample to draw inferences; gauge variation across samples.',
    '7.SP.B.3': 'Informally compare two data distributions with similar variability.',
    '7.SP.C.5': 'Probability is a number from 0 to 1 that expresses the likelihood of an event.',
    '7.SP.C.6': 'Approximate a probability by collecting data and observing long-run relative frequency.',
    '7.SP.C.7a': 'Develop a uniform probability model and use it to find probabilities.',
    '7.SP.C.7b': 'Develop a probability model (may not be uniform) from observed frequencies.',
    '7.SP.C.8a': 'The probability of a compound event is the fraction of outcomes in its sample space.',
    '7.SP.C.8b': 'Represent sample spaces for compound events with lists, tables and tree diagrams.',

    /* Grade 8 */
    '8.EE': 'Expressions and Equations (grade 8).',
    '8.EE.A.1': 'Know and apply the properties of integer exponents.',
    '8.EE.A.2': 'Use square and cube root symbols; evaluate square roots of perfect squares and cube roots of perfect cubes.',
    '8.EE.A.3': 'Use numbers in the form a × 10ⁿ to estimate very large or very small quantities.',
    '8.EE.A.4': 'Perform operations with numbers in scientific notation.',
    '8.EE.B.5': 'Graph proportional relationships; interpret the unit rate as the slope.',
    '8.EE.B.6': 'Use similar triangles to explain slope; derive y = mx and y = mx + b.',
    '8.EE.C.7': 'Solve linear equations in one variable.',
    '8.EE.C.7a': 'Give examples of linear equations with one solution, infinitely many or no solutions.',
    '8.EE.C.7b': 'Solve linear equations with rational coefficients, including distributing and combining like terms.',
    '8.EE.C.8': 'Analyze and solve pairs of simultaneous linear equations.',
    '8.EE.C.8a': 'Solutions of a system correspond to points where the graphs intersect.',
    '8.EE.C.8b': 'Solve systems of two linear equations algebraically and estimate by graphing.',
    '8.EE.C.8c': 'Solve real-world problems leading to two linear equations in two variables.',
    '8.F.A.1': 'A function assigns each input exactly one output; its graph is the set of ordered pairs.',
    '8.F.A.2': 'Compare properties of two functions represented in different ways.',
    '8.F.A.3': 'Interpret y = mx + b as a linear function; give examples of nonlinear functions.',
    '8.F.B.4': 'Construct a function to model a linear relationship; find and interpret rate of change and initial value.',
    '8.F.B.5': 'Describe a functional relationship qualitatively by analyzing a graph.',
    '8.G.A.1': 'Verify the properties of rotations, reflections and translations.',
    '8.G.A.2': 'Understand congruence through a sequence of rotations, reflections and translations.',
    '8.G.A.3': 'Describe the effect of dilations, translations, rotations and reflections using coordinates.',
    '8.G.A.4': 'Understand similarity through rigid motions and dilations.',
    '8.G.A.5': 'Use informal arguments about angle sums, exterior angles, transversals and angle-angle similarity.',
    '8.G.B.6': 'Explain a proof of the Pythagorean Theorem and its converse.',
    '8.G.B.7': 'Apply the Pythagorean Theorem to find unknown side lengths in two and three dimensions.',
    '8.G.B.8': 'Apply the Pythagorean Theorem to find the distance between two points in a coordinate system.',
    '8.G.C.9': 'Know and use the volume formulas for cones, cylinders and spheres.',
    '8.NS.A.1': 'Know that irrational numbers are not rational; every number has a decimal expansion.',
    '8.NS.A.2': 'Use rational approximations of irrational numbers to compare and estimate them.',
    '8.SP.A.1': 'Construct and interpret scatter plots; describe clustering, outliers and association.',
    '8.SP.A.2': 'Informally fit a straight line to a scatter plot and judge its fit.',
    '8.SP.A.3': 'Use a linear model to solve problems; interpret slope and intercept.',
    '8.SP.A.4': 'Show patterns of association in categorical data with two-way tables.',

    /* High school · Number and Quantity */
    'N-RN.A.1': 'Explain how rational exponents extend the properties of integer exponents.',
    'N-RN.A.2': 'Rewrite expressions with radicals and rational exponents using the properties of exponents.',
    'N-RN.B.3': 'Explain why sums and products of rational and irrational numbers are rational or irrational.',
    'N-Q.A.1': 'Use units to understand problems and guide multi-step solutions; choose scales and units.',
    'N-Q.A.2': 'Define appropriate quantities for descriptive modeling.',
    'N-Q.A.3': 'Choose a level of accuracy appropriate to the limits of measurement.',
    'N-CN.A.1': 'Know that i² = −1 and every complex number has the form a + bi.',
    'N-CN.A.2': 'Add, subtract and multiply complex numbers.',
    'N-CN.B.4': 'Represent complex numbers in rectangular and polar form on the complex plane.',
    'N-CN.B.6': 'Find distance and midpoint in the complex plane.',
    'N-CN.C.7': 'Solve quadratic equations with real coefficients that have complex solutions.',
    'N-CN.C.8': 'Extend polynomial identities to the complex numbers.',
    'N-CN.C.9': 'Know the Fundamental Theorem of Algebra.',
    'N-VM.A.1': 'Recognize vectors as having magnitude and direction; use vector notation.',
    'N-VM.A.2': 'Find a vector’s components by subtracting initial point coordinates from terminal point coordinates.',
    'N-VM.A.3': 'Solve problems involving velocity and other quantities represented by vectors.',
    'N-VM.B.4': 'Add and subtract vectors.',
    'N-VM.B.4b': 'Find the magnitude and direction of the sum of two vectors.',
    'N-VM.B.5': 'Multiply a vector by a scalar.',
    'N-VM.C.6': 'Use matrices to represent and manipulate data.',
    'N-VM.C.7': 'Multiply matrices by scalars.',
    'N-VM.C.8': 'Add, subtract and multiply matrices of appropriate dimensions.',
    'N-VM.C.10': 'Understand the zero and identity matrices; a square matrix has an inverse iff its determinant is nonzero.',
    'N-VM.C.11': 'Multiply a vector by a matrix to produce a new vector.',
    'N-VM.C.12': 'Work with 2 × 2 matrices as transformations of the plane; interpret the determinant as area.',

    /* High school · Algebra */
    'A-SSE.A.1': 'Interpret expressions that represent a quantity in terms of its context.',
    'A-SSE.A.1a': 'Interpret parts of an expression, such as terms, factors and coefficients.',
    'A-SSE.A.1b': 'Interpret complicated expressions by viewing one or more of their parts as a single entity.',
    'A-SSE.A.2': 'Use the structure of an expression to identify ways to rewrite it.',
    'A-SSE.B.3a': 'Factor a quadratic expression to reveal the zeros of the function it defines.',
    'A-SSE.B.3b': 'Complete the square in a quadratic expression to reveal its maximum or minimum.',
    'A-SSE.B.3c': 'Use the properties of exponents to transform expressions for exponential functions.',
    'A-SSE.B.4': 'Derive and use the formula for the sum of a finite geometric series.',
    'A-APR.A.1': 'Add, subtract and multiply polynomials; polynomials are closed under these operations.',
    'A-APR.B.2': 'Know and apply the Remainder Theorem.',
    'A-APR.B.3': 'Identify zeros of polynomials when suitable factorizations are available; sketch the graph.',
    'A-APR.C.4': 'Prove polynomial identities and use them to describe numerical relationships.',
    'A-APR.D.6': 'Rewrite simple rational expressions in different forms (long division).',
    'A-APR.D.7': 'Add, subtract, multiply and divide rational expressions.',
    'A-CED.A.1': 'Create equations and inequalities in one variable and use them to solve problems.',
    'A-CED.A.2': 'Create equations in two or more variables; graph them on coordinate axes with labels and scales.',
    'A-CED.A.3': 'Represent constraints by equations or inequalities and interpret solutions as viable or not.',
    'A-CED.A.4': 'Rearrange formulas to highlight a quantity of interest.',
    'A-REI.A.1': 'Explain each step in solving an equation and justify the solution method.',
    'A-REI.A.2': 'Solve rational and radical equations in one variable; identify extraneous solutions.',
    'A-REI.B.3': 'Solve linear equations and inequalities in one variable, including literal coefficients.',
    'A-REI.B.4a': 'Use completing the square to transform a quadratic equation; derive the quadratic formula.',
    'A-REI.B.4b': 'Solve quadratic equations by inspection, square roots, completing the square, the quadratic formula and factoring.',
    'A-REI.C.5': 'Prove that replacing one equation by a sum with a multiple of the other keeps the same solutions.',
    'A-REI.C.6': 'Solve systems of linear equations exactly and approximately, focusing on pairs of equations.',
    'A-REI.C.7': 'Solve a simple system of a linear equation and a quadratic equation in two variables algebraically and graphically.',
    'A-REI.C.8': 'Represent a system of linear equations as a single matrix equation.',
    'A-REI.C.9': 'Find the inverse of a matrix and use it to solve a system of linear equations.',
    'A-REI.D.11': 'Explain why the x-coordinates of intersection points solve f(x) = g(x); find solutions approximately.',
    'A-REI.D.12': 'Graph the solutions to a linear inequality as a half-plane, and to a system as the intersection.',

    /* High school · Functions */
    'F-IF.A.1': 'Understand a function as assigning each input exactly one output; use f(x) notation.',
    'F-IF.A.2': 'Use function notation, evaluate functions and interpret statements in context.',
    'F-IF.A.3': 'Recognize that sequences are functions whose domain is a subset of the integers.',
    'F-IF.B.4': 'Interpret key features of graphs and tables (intercepts, intervals of increase, maxima, symmetry, end behavior).',
    'F-IF.B.5': 'Relate the domain of a function to its graph and to the quantitative relationship it describes.',
    'F-IF.B.6': 'Calculate and interpret the average rate of change of a function over an interval.',
    'F-IF.C.7': 'Graph functions expressed symbolically and show key features of the graph.',
    'F-IF.C.7a': 'Graph linear and quadratic functions and show intercepts, maxima and minima.',
    'F-IF.C.7b': 'Graph square root, cube root, piecewise and absolute value functions.',
    'F-IF.C.7c': 'Graph polynomial functions, identifying zeros and showing end behavior.',
    'F-IF.C.7d': 'Graph rational functions, identifying zeros and asymptotes.',
    'F-IF.C.7e': 'Graph exponential, logarithmic and trigonometric functions, showing intercepts, end behavior, period and amplitude.',
    'F-IF.C.8a': 'Factor and complete the square in a quadratic to show zeros, extreme values and symmetry.',
    'F-IF.C.8b': 'Use the properties of exponents to interpret exponential expressions as growth or decay.',
    'F-IF.C.9': 'Compare properties of two functions each represented in a different way.',
    'F-BF.A.1': 'Write a function that describes a relationship between two quantities.',
    'F-BF.A.1a': 'Determine an explicit expression, a recursive process or steps for calculation from a context.',
    'F-BF.A.1b': 'Combine standard function types using arithmetic operations.',
    'F-BF.A.1c': 'Compose functions.',
    'F-BF.A.2': 'Write arithmetic and geometric sequences recursively and explicitly; translate between forms.',
    'F-BF.B.3': 'Identify the effect on a graph of replacing f(x) by f(x) + k, k·f(x), f(kx) and f(x + k).',
    'F-BF.B.4a': 'Solve f(x) = c for a simple function and write an expression for the inverse.',
    'F-BF.B.4c': 'Read values of an inverse function from a graph or a table.',
    'F-BF.B.5': 'Use the inverse relationship between exponents and logarithms to solve problems.',
    'F-LE.A.1': 'Distinguish between situations modeled by linear functions and by exponential functions.',
    'F-LE.A.1a': 'Prove linear functions grow by equal differences and exponential functions by equal factors.',
    'F-LE.A.1c': 'Recognize situations where a quantity grows or decays by a constant percent rate per unit interval.',
    'F-LE.A.2': 'Construct linear and exponential functions, including arithmetic and geometric sequences, from a graph, description or table.',
    'F-LE.A.3': 'Observe that a quantity increasing exponentially eventually exceeds one increasing linearly or polynomially.',
    'F-LE.A.4': 'Express the solution to an exponential model as a logarithm and evaluate it.',
    'F-LE.B.5': 'Interpret the parameters in a linear or exponential function in terms of a context.',
    'F-TF.A.1': 'Understand radian measure of an angle as the length of the arc on the unit circle it subtends.',
    'F-TF.A.2': 'Explain how the unit circle extends trigonometric functions to all real numbers.',
    'F-TF.A.3': 'Use special triangles to find sine, cosine and tangent of π/3, π/4 and π/6 and related angles.',
    'F-TF.B.5': 'Choose trigonometric functions to model periodic phenomena with given amplitude, frequency and midline.',
    'F-TF.B.6': 'Restrict a trigonometric function’s domain so its inverse can be constructed.',
    'F-TF.B.7': 'Use inverse functions to solve trigonometric equations in modeling contexts.',
    'F-TF.C.8': 'Prove sin²θ + cos²θ = 1 and use it to find trigonometric values.',
    'F-TF.C.9': 'Prove and use the addition and subtraction formulas for sine, cosine and tangent.',

    /* High school · Geometry */
    'G-CO': 'Congruence: transformations, congruence, theorems and constructions.',
    'G-CO.A.1': 'Know precise definitions of angle, circle, perpendicular and parallel lines, and line segment.',
    'G-CO.A.2': 'Represent transformations in the plane; compare rigid motions with other transformations.',
    'G-CO.A.3': 'Describe the rotations and reflections that carry a polygon onto itself.',
    'G-CO.A.4': 'Develop definitions of rotations, reflections and translations.',
    'G-CO.A.5': 'Draw the image of a figure under a transformation; specify a sequence that maps one figure onto another.',
    'G-CO.B.6': 'Use rigid motions to transform figures and to decide whether two figures are congruent.',
    'G-CO.B.7': 'Show two triangles are congruent iff corresponding sides and angles are congruent.',
    'G-CO.B.8': 'Explain how the ASA, SAS and SSS criteria follow from rigid motions.',
    'G-CO.C.9': 'Prove theorems about lines and angles (vertical angles, transversals, perpendicular bisectors).',
    'G-CO.C.10': 'Prove theorems about triangles (angle sum, base angles, midsegments, medians).',
    'G-CO.C.11': 'Prove theorems about parallelograms.',
    'G-CO.D.12': 'Make formal geometric constructions with a variety of tools and methods.',
    'G-CO.D.13': 'Construct an equilateral triangle, a square, and a regular hexagon inscribed in a circle.',
    'G-SRT': 'Similarity, right triangles and trigonometry.',
    'G-SRT.A.1': 'Verify the properties of dilations given by a center and a scale factor.',
    'G-SRT.A.2': 'Use similarity transformations to decide whether two figures are similar.',
    'G-SRT.A.3': 'Establish the AA criterion for triangle similarity.',
    'G-SRT.B.4': 'Prove theorems about triangles (a line parallel to one side divides the others proportionally; Pythagorean Theorem).',
    'G-SRT.B.5': 'Use congruence and similarity criteria to solve problems and prove relationships in figures.',
    'G-SRT.C.6': 'Understand that side ratios in right triangles define the trigonometric ratios.',
    'G-SRT.C.7': 'Explain and use the relationship between the sine and cosine of complementary angles.',
    'G-SRT.C.8': 'Use trigonometric ratios and the Pythagorean Theorem to solve right triangles.',
    'G-SRT.D.9': 'Derive the formula A = ½ab·sin C for the area of a triangle.',
    'G-SRT.D.10': 'Prove the Laws of Sines and Cosines and use them to solve problems.',
    'G-SRT.D.11': 'Use the Laws of Sines and Cosines to find unknown measures in any triangle.',
    'G-C': 'Circles: theorems, arcs, sectors and equations.',
    'G-C.A.1': 'Prove that all circles are similar.',
    'G-C.A.2': 'Identify and describe relationships among inscribed angles, radii, chords and tangents.',
    'G-C.A.3': 'Construct inscribed and circumscribed circles; prove properties of angles of an inscribed quadrilateral.',
    'G-C.B.5': 'Derive arc length and sector area; define radian measure as a constant of proportionality.',
    'G-GPE': 'Expressing geometric properties with equations (coordinate geometry).',
    'G-GPE.A.1': 'Derive the equation of a circle; complete the square to find its center and radius.',
    'G-GPE.A.2': 'Derive the equation of a parabola given a focus and directrix.',
    'G-GPE.A.3': 'Derive the equations of ellipses and hyperbolas given the foci.',
    'G-GPE.B.4': 'Use coordinates to prove simple geometric theorems algebraically.',
    'G-GPE.B.5': 'Prove the slope criteria for parallel and perpendicular lines and use them to solve problems.',
    'G-GPE.B.6': 'Find the point on a segment that partitions it in a given ratio.',
    'G-GPE.B.7': 'Use coordinates to compute perimeters of polygons and areas of triangles and rectangles.',
    'G-GMD': 'Geometric measurement and dimension.',
    'G-GMD.A.1': 'Give informal arguments for the circumference, area and volume formulas of circles, cylinders, pyramids and cones.',
    'G-GMD.A.3': 'Use volume formulas for cylinders, pyramids, cones and spheres to solve problems.',
    'G-GMD.B.4': 'Identify cross sections of three-dimensional objects and solids of rotation.',
    'G-MG.A.1': 'Use geometric shapes, their measures and their properties to describe objects.',
    'G-MG.A.2': 'Apply concepts of density based on area and volume in modeling situations.',
    'G-MG.A.3': 'Apply geometric methods to solve design problems.',

    /* High school · Statistics and Probability */
    'S-ID.A.1': 'Represent data with plots on the real number line (dot plots, histograms and box plots).',
    'S-ID.A.2': 'Use statistics appropriate to the shape of the data to compare center and spread of data sets.',
    'S-ID.A.3': 'Interpret differences in shape, center and spread, accounting for possible outliers.',
    'S-ID.A.4': 'Use the mean and standard deviation to fit data to a normal distribution and estimate percentages.',
    'S-ID.B.5': 'Summarize categorical data for two categories in two-way frequency tables; interpret relative frequencies.',
    'S-ID.B.6': 'Represent data for two quantitative variables on a scatter plot and describe how they are related.',
    'S-ID.B.6a': 'Fit a function to the data and use it to solve problems in context.',
    'S-ID.B.6b': 'Informally assess the fit of a function by plotting and analyzing residuals.',
    'S-ID.B.6c': 'Fit a linear function for a scatter plot that suggests a linear association.',
    'S-ID.C.7': 'Interpret the slope and the intercept of a linear model in the context of the data.',
    'S-ID.C.8': 'Compute (using technology) and interpret the correlation coefficient of a linear fit.',
    'S-ID.C.9': 'Distinguish between correlation and causation.',
    'S-IC.A.1': 'Understand statistics as a process for making inferences about a population from a random sample.',
    'S-IC.B.3': 'Recognize the purposes of and differences among sample surveys, experiments and observational studies.',
    'S-IC.B.4': 'Use data from a sample survey to estimate a population mean or proportion; develop a margin of error.',
    'S-CP.A.1': 'Describe events as subsets of a sample space using unions, intersections and complements.',
    'S-CP.A.2': 'Understand that A and B are independent if P(A and B) = P(A)·P(B).',
    'S-CP.A.3': 'Understand conditional probability P(A | B) as P(A and B) / P(B).',
    'S-CP.A.4': 'Construct and interpret two-way frequency tables; use them to decide independence and find conditional probabilities.',
    'S-CP.B.6': 'Find the conditional probability of A given B as the fraction of B’s outcomes that also belong to A.',
    'S-CP.B.7': 'Apply the Addition Rule, P(A or B) = P(A) + P(B) − P(A and B).',
    'S-CP.B.8': 'Apply the general Multiplication Rule in a uniform probability model.',
    'S-CP.B.9': 'Use permutations and combinations to compute probabilities of compound events.',
    'S-MD.A.1': 'Define a random variable for a quantity of interest and graph its probability distribution.',
    'S-MD.A.2': 'Calculate the expected value of a random variable; interpret it as the mean of the distribution.',
    'S-MD.A.3': 'Develop a probability distribution from theoretical probabilities and find the expected value.',
    'S-MD.B.5': 'Weigh the possible outcomes of a decision by assigning probabilities and finding expected values.',
    'S-MD.B.7': 'Analyze decisions and strategies using probability concepts.'
  };
  /* AP framework codes (Calculus, Statistics banks): summarize by big idea / topic outline area. */
  var AP_CALC = { LIM: 'AP Calculus · Big Idea: Limits', CHA: 'AP Calculus · Big Idea: Change', FUN: 'AP Calculus · Big Idea: Analysis of Functions' };
  var AP_STATS = { I: 'AP Statistics · Exploring Data', II: 'AP Statistics · Sampling and Experimentation', III: 'AP Statistics · Anticipating Patterns (probability and simulation)', IV: 'AP Statistics · Statistical Inference' };
  STD.describe = function (code) {
    var c = norm(code);
    if (D[c]) return D[c];
    var m = /^AP ([A-Z]{3})-/.exec(c); if (m && AP_CALC[m[1]]) return AP_CALC[m[1]];
    m = /^APSTATS\.(IV|III|II|I)(?![IV])/.exec(c); if (m) return AP_STATS[m[1]];
    m = /^(.*\.[0-9]+)[a-d]$/.exec(c); if (m && D[m[1]]) return D[m[1]];   // a sub-standard falls back to its parent
    return '';
  };
  STD.framework = function (code) {
    var c = norm(code);
    if (/^APSTATS/.test(c)) return 'AP Statistics';
    if (/^AP /.test(c)) return 'AP Calculus';
    if (STD.isPractice(c)) return 'CCSS Practice';
    return 'Common Core';
  };
  STD.isCommonCore = function (code) { return STD.framework(code) === 'Common Core'; };

  /* ---------- lookups ---------- */
  STD.forSkill = function (set, skill) {
    var m = G.MKSTD_SKILLS && G.MKSTD_SKILLS[set];
    return (m && m[skill]) ? m[skill].slice() : [];
  };
  /* An approved bank question keeps its own tags (exact); a generated problem uses its skill's standards. */
  STD.forProblem = function (p, set) {
    if (!p || p.failed) return [];
    var own = p.standards ? STD.split(p.standards) : [];
    if (!own.length && G.MKMENU && typeof G.MKMENU.sourceStandards === 'function') own = STD.split(G.MKMENU.sourceStandards(p));
    if (STD.content(own).length) return STD.content(own);
    var bySkill = STD.forSkill(set, p.skill);
    return bySkill.length ? bySkill : own;
  };
  function cmp(a, b) { return a.localeCompare(b, 'en', { numeric: true }); }
  function domainOrder(c) {
    var i = ['N-', 'A-', 'F-', 'G-', 'S-'].indexOf(c.slice(0, 2));
    if (/^[0-9]/.test(c)) return c.charAt(0);   // grade-level codes first, by grade
    return i >= 0 ? 'H' + i : 'Z';
  }
  STD.sort = function (list) { return list.slice().sort(function (a, b) { var x = domainOrder(a), y = domainOrder(b); return x < y ? -1 : x > y ? 1 : cmp(a, b); }); };

  /* rows: [{ label: '1' | 'A3', codes: [...] }] → [{ code, text, labels: [...] }] in standard order */
  STD.collect = function (rows) {
    var by = {}, order = [];
    (rows || []).forEach(function (r) {
      (r.codes || []).forEach(function (c) {
        if (!by[c]) { by[c] = []; order.push(c); }
        if (r.label != null && by[c].indexOf(String(r.label)) < 0) by[c].push(String(r.label));
      });
    });
    return STD.sort(order).map(function (c) { return { code: c, text: STD.describe(c), labels: by[c] }; });
  };

  /* ---------- HTML ---------- */
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (ch) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]; }); }
  function ranges(labels) {   // "1, 2, 3, 5" → "1–3, 5" when the labels are plain numbers
    if (!labels.length || !labels.every(function (l) { return /^[0-9]+$/.test(l); })) return labels.join(', ');
    var n = labels.map(Number).sort(function (a, b) { return a - b; }), out = [], s = n[0], p = n[0];
    for (var i = 1; i <= n.length; i++) {
      if (i < n.length && n[i] === p + 1) { p = n[i]; continue; }
      out.push(s === p ? String(s) : s + '–' + p);
      if (i < n.length) { s = p = n[i]; }
    }
    return out.join(', ');
  }
  STD.frameworkTitle = function (list) {
    var f = {}; list.forEach(function (r) { f[STD.framework(r.code || r)] = 1; });
    delete f['CCSS Practice'];
    var k = Object.keys(f);
    if (!k.length || (k.length === 1 && k[0] === 'Common Core')) return 'Common Core standards addressed';
    if (k.indexOf('Common Core') < 0) return k.join(' / ') + ' framework codes addressed';
    return 'Standards addressed';
  };
  /* opts: { title, labelHead ('Questions'), note, compact } */
  STD.summaryHtml = function (rows, opts) {
    opts = opts || {};
    var list = Array.isArray(rows) && rows.length && rows[0] && rows[0].code ? rows : STD.collect(rows);
    if (!list.length) return '';
    var showLabels = list.some(function (r) { return r.labels && r.labels.length; });
    return '<div class="mk-std"><h3>' + esc(opts.title || STD.frameworkTitle(list)) + '</h3>' +
      '<table class="mk-std-tbl"><thead><tr><th>Standard</th><th>What students do</th>' + (showLabels ? '<th>' + esc(opts.labelHead || 'Questions') + '</th>' : '') + '</tr></thead><tbody>' +
      list.map(function (r) {
        return '<tr><td class="mk-std-code"><b>' + esc(r.code) + '</b></td><td>' + esc(r.text || '') + '</td>' + (showLabels ? '<td class="mk-std-q">' + esc(ranges(r.labels || [])) + '</td>' : '') + '</tr>';
      }).join('') + '</tbody></table>' +
      (opts.note ? '<p class="mk-std-note">' + esc(opts.note) + '</p>' : '') + '</div>';
  };
  STD.chipsHtml = function (codes) {
    codes = codes || [];
    if (!codes.length) return '';
    return '<div class="mk-std-chips">' + codes.map(function (c) { return '<span class="mk-std-chip" title="' + esc(STD.describe(c)) + '">' + esc(c) + '</span>'; }).join('') + '</div>';
  };
  /* "A-SSE.A.1a, N-RN.B.3" with each summary, for one lesson (planner). */
  STD.listHtml = function (codes) {
    var list = STD.split(codes);
    if (!list.length) return '';
    return '<ul class="mk-std-list">' + list.map(function (c) {
      var t = STD.describe(c);
      return '<li><b>' + esc(c) + '</b>' + (t ? ' — ' + esc(t) : '') + '</li>';
    }).join('') + '</ul>';
  };
  /* Styles live here so every page that loads this file gets them (print-safe, small). */
  STD.CSS = '.mk-std{margin:10px 0 12px;border:1px solid #c9d6e6;border-radius:8px;padding:8px 10px;background:#f7fafd;break-inside:avoid}' +
    '.mk-std h3{margin:0 0 6px;font-size:12pt;color:#1d3557}' +
    '.mk-std-tbl{width:100%;border-collapse:collapse;font-size:9.5pt}' +
    '.mk-std-tbl th,.mk-std-tbl td{border:1px solid #d6dfeb;padding:3px 6px;text-align:left;vertical-align:top}' +
    '.mk-std-tbl th{background:#e8eff8;font-weight:700}' +
    '.mk-std-code{white-space:nowrap}.mk-std-q{white-space:nowrap;width:1%}' +
    '.mk-std-note{margin:5px 0 0;font-size:8.5pt;color:#55657a}' +
    '.mk-std-chips{margin-top:3px;display:flex;flex-wrap:wrap;gap:2px}' +
    '.mk-std-chip{display:inline-block;font-size:7pt;line-height:1.3;padding:0 4px;border:1px solid #9fb6d3;border-radius:6px;color:#1d3557;background:#eef4fb;white-space:nowrap}' +
    '.mk-std-list{margin:0;padding-left:1.1em}.mk-std-list li{margin:1px 0}' +
    '@media print{.mk-std{background:#fff}.mk-std-tbl th{background:#eee}.mk-std-chip{background:#fff}}';
  STD.injectCss = function (doc) {
    doc = doc || G.document;
    if (!doc || !doc.head || doc.getElementById('mk-std-css')) return;
    var s = doc.createElement('style'); s.id = 'mk-std-css'; s.textContent = STD.CSS; doc.head.appendChild(s);
  };
  if (G.document) { if (G.document.head) STD.injectCss(G.document); else G.document.addEventListener('DOMContentLoaded', function () { STD.injectCss(G.document); }); }

  G.MKSTD = STD;
  if (typeof module !== 'undefined' && module.exports) module.exports = STD;
})(typeof window !== 'undefined' ? window : globalThis);
