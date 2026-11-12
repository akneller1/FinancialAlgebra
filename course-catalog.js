/* Shared course skill catalog. Content only: no question generation or diagrams.
   Keep course IDs and unit IDs consistent with data.js. */
(function(root){
  'use strict';
  var skills = {
  "discrete": {
  "speaking-mathematically": [
    "Variables and Mathematical Statements",
    "Universal and Existential Statements",
    "Conditional Statements",
    "Set-Roster and Set-Builder Notation",
    "Subsets and Set Membership",
    "Cartesian Products and Ordered Pairs",
    "Strings and Mathematical Notation"
  ],
  "compound-statements-logic": [
    "Negation, Conjunction, and Disjunction",
    "Truth Tables and Truth Values",
    "Logical Equivalence",
    "Conditional Statements and Equivalent Forms",
    "Negating Conditional Statements",
    "Converse, Inverse, and Contrapositive",
    "Rules of Inference and Valid Arguments",
    "Fallacies and Contradictions"
  ],
  "number-theory-proof": [
    "Definitions, Conjectures, and Counterexamples",
    "Direct Proof",
    "Proving Existential and Universal Statements",
    "Properties of Integers and Rational Numbers",
    "Divisibility and Number-Theory Arguments",
    "Proof by Contradiction",
    "Proof by Contraposition",
    "Choosing a Proof Strategy"
  ],
  "sequences-induction-recursion": [
    "Sequences and Explicit Formulas",
    "Arithmetic and Geometric Patterns",
    "Factorials and Binomial Coefficient Notation",
    "Fibonacci Sequences",
    "Recursively Defined Sequences",
    "Iteration and Recursive Computation",
    "The Principle of Mathematical Induction",
    "Writing Inductive Proofs",
    "Patterns and Tessellations"
  ],
  "set-theory": [
    "Set Equality and the Empty Set",
    "Union, Intersection, and Difference",
    "Complements and Set Operations",
    "Venn Diagrams",
    "Power Sets",
    "Proving Subset Relations",
    "Proving Set Equality and Set Identities",
    "Disproving Set Statements"
  ],
  "properties-relations": [
    "Relations and Their Inverses",
    "Directed Graphs of Relations",
    "Reflexive, Symmetric, and Transitive Properties",
    "Relations on Finite and Infinite Sets",
    "Partitions and Induced Relations",
    "Equivalence Relations",
    "Equivalence Classes"
  ],
  "counting-probability": [
    "Sample Spaces and Events",
    "Lists, Sublists, and One-Dimensional Arrays",
    "Possibility Trees",
    "The Addition Counting Rule",
    "The Multiplication Counting Rule",
    "Counting Outcomes Systematically",
    "Probability with Equally Likely Outcomes",
    "Applying Counting Rules to Probability"
  ],
  "graphs-trees": [
    "Vertices, Edges, Endpoints, and Loops",
    "Directed and Undirected Graphs",
    "Constructing Graphs from Given Characteristics",
    "Graph Coloring",
    "Trails and Paths",
    "Circuits",
    "Constructing and Characterizing Trees"
  ],
  "election-theory": [
    "Voting Terminology and Preference Data",
    "Comparing Voting Methods",
    "Analyzing Election Results",
    "Weighted Voting Systems and Quotas",
    "Coalitions and Voting Power",
    "Fair-Division Methods",
    "Apportionment Methods",
    "Comparing Fairness and Outcomes"
  ],
  "linear-programming": [
    "Writing Constraints from Real-World Situations",
    "Graphing Systems of Linear Inequalities",
    "Feasible Regions",
    "Objective Functions",
    "Vertices and Candidate Solutions",
    "Maximizing and Minimizing in Two Variables",
    "Interpreting Optimal Solutions in Context"
  ]
},
  "statistics": {
  "exploring-data": [
    "Exploring Data: Variables, Dot Plots, Stem Plots, and Histograms",
    "Describing Shape, Center, Spread, and Outliers",
    "Mean, Median, Range, Interquartile Range, and Standard Deviation",
    "Quartiles, Percentiles, Box Plots, and Comparing Distributions",
    "Modeling Distributions: Density Curves, Normal Models, and z-Scores",
    "Categorical Data: Two-Way Tables and Conditional Relative Frequencies",
    "Describing Relationships: Scatterplots and Correlation",
    "Least-Squares Regression, Predictions, and Coefficient of Determination",
    "Residuals, Influential Points, and Limits of Linear Models"
  ],
  "sampling-experimentation": [
    "Sampling: Populations, Samples, Censuses, and Surveys",
    "Simple Random, Stratified, and Cluster Sampling",
    "Undercoverage, Nonresponse, and Response Bias",
    "Observational Studies and Experiments",
    "Experimenting: Treatments, Controls, Random Assignment, and Replication",
    "Confounding, Placebos, and Blinding",
    "Completely Randomized, Randomized Block, and Matched Pairs Designs",
    "Generalizing Results and Distinguishing Association from Causation"
  ],
  "anticipating-patterns": [
    "Probability: Long-Run Relative Frequency and the Law of Large Numbers",
    "Addition and Multiplication Rules",
    "Conditional Probability and Independent Events",
    "Simulating Random Behavior",
    "Random Variables: Discrete Probability Distributions",
    "Expected Value, Standard Deviation, and Linear Transformations",
    "Binomial and Geometric Distributions",
    "Combining Independent Random Variables",
    "Sampling Distributions of Proportions and Means",
    "Bias, Variability, Sample Size, and the Central Limit Theorem"
  ],
  "statistical-inference": [
    "Confidence Intervals: Point Estimates, Standard Error, and Margin of Error",
    "Interpreting Confidence Levels and Checking Inference Conditions",
    "One-Proportion z-Intervals and Sample Size",
    "One-Mean t-Intervals and Degrees of Freedom",
    "Significance Tests: Null and Alternative Hypotheses",
    "Test Statistics, p-Values, and Conclusions in Context",
    "One-Proportion z-Tests and One-Mean t-Tests",
    "Type I and Type II Errors and Statistical Power",
    "Comparing Two Populations: Intervals and Tests for Two Proportions",
    "Independent Two-Sample and Paired t-Procedures",
    "Extension: Confidence Intervals for a Regression Slope"
  ]
},
  "calculus": {
  "precalculus-review": [
    "Factoring and Simplifying Expressions",
    "Exponential Functions",
    "Logarithmic Functions",
    "Unit Circle and Exact Trigonometric Values",
    "Graphical, Numerical, and Algebraic Representations"
  ],
  "limits-continuity": [
    "Limit Notation and Interpretation",
    "Estimating Limits from Graphs and Tables",
    "Evaluating Limits Algebraically",
    "One-Sided and Two-Sided Limits",
    "Using Limits to Describe Function Behavior",
    "Continuity on an Interval",
    "Points and Types of Discontinuity",
    "Applying Theorems Requiring Continuity"
  ],
  "derivatives": [
    "The Derivative as a Limit of Difference Quotients",
    "Estimating Derivatives from Graphs and Tables",
    "Calculating Derivatives",
    "Higher-Order Derivatives",
    "Differentiability and Continuity",
    "Tangent Lines and Their Slopes",
    "Connecting a Function and Its Derivative"
  ],
  "applications-derivatives": [
    "Interpreting Derivatives in Context",
    "Analyzing Function Behavior with Derivatives",
    "Increasing and Decreasing Intervals",
    "Relative and Absolute Extrema",
    "Concavity and Inflection Points",
    "Related Rates",
    "Optimization",
    "Rectilinear Motion: Position, Velocity, and Acceleration",
    "Rates of Change in Applied Contexts",
    "The Mean Value Theorem",
    "Midterm Review"
  ],
  "antiderivatives-definite-integrals": [
    "Antidifferentiation as the Inverse of Differentiation",
    "Antiderivatives of Basic Functions",
    "Definite Integrals as Limits of Riemann Sums",
    "Converting Riemann Sums to Integral Notation",
    "Approximating Definite Integrals",
    "Evaluating Integrals Using Geometry",
    "Properties of Definite Integrals"
  ],
  "fundamental-theorem-calculus": [
    "Connecting Differentiation and Integration",
    "Accumulation Functions",
    "Analyzing Functions Defined by Integrals",
    "Differentiating Functions Defined by Integrals",
    "Evaluating Definite Integrals with Antiderivatives"
  ],
  "applications-integrals": [
    "Interpreting Definite Integrals in Context",
    "Accumulation and Net Change",
    "Average Value of a Function",
    "Motion and Displacement",
    "Total Distance Traveled",
    "Area Between Curves",
    "Volumes of Solids",
    "Integral Models in Applied Contexts"
  ],
  "differential-equations": [
    "Functions Defined by Their Rates of Change",
    "Verifying Solutions to Differential Equations",
    "Estimating Solutions to Differential Equations",
    "Separating Variables",
    "Solving Separable Differential Equations",
    "Initial Conditions and Particular Solutions"
  ],
  "ap-review": [
    "Limits and Continuity Review",
    "Derivatives and Their Applications Review",
    "Integrals and the Fundamental Theorem Review",
    "Differential Equations Review",
    "Connecting Graphs, Tables, Formulas, and Verbal Descriptions",
    "Justifying Solutions with Definitions and Theorems",
    "Calculus Notation and Written Explanations"
  ]
},
  "precalculus": {
  "equations-inequalities": [
    "Writing Linear Equations",
    "Parallel and Perpendicular Lines",
    "Solving Equations Graphically",
    "Applications of Equations",
    "Linear, Compound, and Polynomial Inequalities",
    "Interval Notation",
    "Graphing Linear Inequalities",
    "Systems of Equations in Two Variables",
    "Systems of Equations in Three Variables",
    "Systems of Linear Inequalities",
    "Linear Programming"
  ],
  "functions": [
    "Linear Graphs, Slope, Intercepts, and Zeros",
    "Function Operations and Composition",
    "Function Iteration",
    "Twelve Basic Functions and Domains",
    "Piecewise, Step, and Absolute Value Functions",
    "Parent Functions and Graph Transformations",
    "Families of Related Graphs",
    "Nonlinear and Absolute Value Inequalities",
    "Inverse Functions and Relations",
    "Direct, Inverse, and Joint Variation",
    "Quadratic Equations and Quadratic Form",
    "Rational Functions and Asymptotes",
    "Remainder and Factor Theorems",
    "Locating Polynomial Zeros",
    "Exponential and Logistic Functions",
    "The Number e and Natural Exponential Functions",
    "Logarithmic Functions and Graphs"
  ],
  "conics": [
    "Circles and Their Equations",
    "Parabolas: Focus, Directrix, and Standard Form",
    "Ellipses: Graphs, Vertices, and Foci",
    "Writing Equations of Ellipses",
    "Hyperbolas: Graphs and Key Features",
    "Writing Equations of Hyperbolas"
  ],
  "trigonometric-functions": [
    "Unit Circle and Circular Functions",
    "Exact Trigonometric Values",
    "Angles and Radian Measure",
    "Arc Length and Sector Area",
    "Right Triangle Applications",
    "Amplitude and Period",
    "Sine Functions and Graphs",
    "Cosine Functions and Graphs",
    "Solving Trigonometric Equations",
    "Inverse Trigonometric Functions and Graphs",
    "Principal Values and Technology"
  ],
  "general-triangle-trigonometry": [
    "Triangle Area and the Law of Sines",
    "Solving Triangles with the Law of Sines",
    "The Ambiguous Case: Zero, One, or Two Triangles",
    "The Law of Cosines",
    "Triangle Area from Three Sides",
    "Deriving the Laws of Sines and Cosines",
    "Sum and Difference Identities",
    "Rotations with Identities and Matrices"
  ],
  "matrices": [
    "Matrix Notation and Organizing Data",
    "Adding and Subtracting Matrices",
    "Scalar and Matrix Multiplication",
    "Augmented Matrices and Row Reduction",
    "Reduced Row Echelon Form with Technology",
    "Networks and Matrix Models",
    "Identity and Inverse Matrices",
    "Determinants of 2 by 2 and 3 by 3 Matrices",
    "Geometric Transformations with Matrices",
    "Modeling Motion with Matrices",
    "Solving Systems with Matrix Equations"
  ],
  "vectors": [
    "Complex Number Operations and Quadratic Zeros",
    "Distance, Midpoints, and Modulus in the Complex Plane",
    "Geometric Vectors",
    "Algebraic Vectors and Components",
    "Vector Magnitude and Direction",
    "Vector Applications in Geometry and Modeling",
    "Vector Transformations Using Matrices",
    "Dot Products and Projections",
    "Polar and Rectangular Coordinates"
  ],
  "probability": [
    "Probability, Odds, and Distributions",
    "Independent and Dependent Events",
    "Permutations and Combinations",
    "Compound Event Probabilities",
    "Probability Models and Decision Making",
    "Data Types and Statistical Displays",
    "Shapes of Distributions",
    "Normal Distributions",
    "Binomial Probabilities"
  ]
},
  "algebra": {
    "foundations-algebra": [
      "Variables, Expressions, and Verbal Phrases",
      "Order of Operations and Evaluating Expressions",
      "The Real Number System",
      "Operations with Real Numbers",
      "Properties of Real Numbers",
      "Distributive Property and Combining Like Terms",
      "Interpreting Expressions in Context"
    ],
    "expressions-equations": [
      "Solving One-Step Equations",
      "Solving Two-Step Equations",
      "Solving Multi-Step Equations",
      "Equations with Variables on Both Sides",
      "Special Solutions: No Solution and Infinitely Many",
      "Writing and Solving Equations from Context",
      "Ratios, Proportions, and Percent Equations",
      "Literal Equations and Formulas",
      "Units and Dimensional Analysis"
    ],
    "inequalities": [
      "Writing and Graphing Inequalities",
      "Solving One- and Two-Step Inequalities",
      "Multi-Step Inequalities",
      "Compound Inequalities",
      "Absolute Value Equations and Inequalities",
      "Inequalities in Context"
    ],
    "relations-functions": [
      "Representing Relations",
      "Domain and Range",
      "Identifying Functions",
      "Function Notation and Evaluating Functions",
      "Key Features of Function Graphs",
      "Sketching Graphs from Verbal Descriptions",
      "Discrete vs. Continuous Functions and Domain in Context",
      "Arithmetic Sequences as Functions"
    ],
    "linear-equations-slope": [
      "Rate of Change and Slope",
      "Slope from Graphs, Tables, and Two Points",
      "Slope-Intercept Form",
      "Graphing Lines in Slope-Intercept Form",
      "Standard Form and Intercepts",
      "Point-Slope Form",
      "Writing Linear Equations from Graphs, Tables, and Points",
      "Parallel and Perpendicular Lines",
      "Transformations of Linear Functions",
      "Linear Models in Context",
      "Comparing Linear Functions in Different Representations"
    ],
    "systems-of-equations": [
      "Solving Systems by Graphing",
      "Solving Systems by Substitution",
      "Solving Systems by Elimination (Add/Subtract)",
      "Elimination with Multiplication",
      "Special Systems: No Solution and Infinitely Many",
      "Choosing a Method and Writing Systems from Context",
      "Systems Applications",
      "Graphing Linear Inequalities in Two Variables",
      "Systems of Linear Inequalities",
      "Modeling with Constraints"
    ],
    "exponents-exponential-functions": [
      "Product and Power Rules",
      "Quotient Rule, Zero and Negative Exponents",
      "Simplifying with Multiple Exponent Rules",
      "Rational Exponents and Radicals",
      "Scientific Notation",
      "Operations with Scientific Notation in Context"
    ],
    "exponential-functions": [
      "Linear vs. Exponential Patterns",
      "Exponential Functions: Graphs and Key Features",
      "Exponential Growth",
      "Exponential Decay",
      "Writing Exponential Functions",
      "Compound Interest and Percent Rate of Change",
      "Geometric Sequences",
      "Comparing Linear and Exponential Models",
      "Solving Exponential Equations"
    ],
    "polynomials-factoring": [
      "Classifying Polynomials",
      "Adding and Subtracting Polynomials",
      "Multiplying a Monomial by a Polynomial",
      "Multiplying Binomials",
      "Multiplying Polynomials and Special Products",
      "Polynomials in Context and Closure"
    ],
    "factoring-zero-product": [
      "Factoring the Greatest Common Factor",
      "Factoring by Grouping",
      "Factoring x² + bx + c",
      "Factoring ax² + bx + c",
      "Special Factoring Patterns",
      "Factoring Completely",
      "The Zero Product Property",
      "Solving Quadratic Equations by Factoring",
      "Factoring Applications"
    ],
    "quadratics": [
      "Key Features of Quadratic Graphs",
      "Graphing Quadratics in Standard Form",
      "Vertex Form and Transformations",
      "Factored Form and Connecting Forms",
      "Solving Quadratics by Graphing",
      "Solving by Square Roots",
      "Completing the Square",
      "The Quadratic Formula",
      "The Discriminant",
      "Choosing a Solution Method",
      "Quadratic Models: Projectiles and Area",
      "Comparing Linear, Exponential, and Quadratic Models"
    ],
    "statistics-data-modeling": [
      "Mean, Median, and Mode",
      "Dot Plots, Histograms, and Box Plots",
      "Comparing Distributions: Shape and Outliers",
      "Two-Way Frequency Tables",
      "Scatter Plots and Association",
      "Lines of Fit",
      "Correlation Coefficient and Causation",
      "Residuals and Regression with Technology"
    ]
  },
  "geometry": {
    "foundations-geometry": [
      "Points, Lines, Planes, and Space",
      "Segments, Rays, and Geometric Notation",
      "Measuring and Adding Segments",
      "Midpoints and Segment Bisectors",
      "Angles and Angle Classification",
      "Angle Addition and Angle Bisectors",
      "Distance and Midpoint on the Coordinate Plane",
      "Geometric Reasoning and Basic Constructions"
    ],
    "angles-parallel-lines": [
      "Complementary and Supplementary Angles",
      "Vertical Angles and Linear Pairs",
      "Parallel and Perpendicular Lines",
      "Transversals and Angle Pairs",
      "Corresponding and Alternate Interior Angles",
      "Alternate Exterior and Same-Side Interior Angles",
      "Solving Algebraic Angle Relationships",
      "Proving Lines Parallel",
      "Slopes of Parallel and Perpendicular Lines"
    ],
    "triangle-congruence": [
      "Classifying Triangles",
      "Triangle Angle Sum and Exterior Angles",
      "Corresponding Parts of Triangles",
      "Congruent Figures and Rigid Motions",
      "SSS and SAS Triangle Congruence",
      "ASA and AAS Triangle Congruence",
      "Hypotenuse–Leg (HL) Congruence",
      "CPCTC",
      "Writing Triangle Congruence Proofs"
    ],
    "triangle-relationships": [
      "Isosceles and Equilateral Triangle Properties",
      "Triangle Inequality Theorem",
      "Ordering Sides and Angles",
      "Perpendicular and Angle Bisectors",
      "Medians, Altitudes, and Triangle Centers",
      "Midsegments of Triangles",
      "Indirect Proof and Triangle Inequalities",
      "Algebraic Applications of Triangle Relationships"
    ],
    "similarity": [
      "Ratios, Rates, and Proportions",
      "Similar Polygons and Corresponding Parts",
      "Scale Factors and Dilations",
      "AA Triangle Similarity",
      "SAS and SSS Triangle Similarity",
      "Finding Missing Side Lengths",
      "Triangle Proportionality and Side-Splitter Theorems",
      "Indirect Measurement and Scale Drawings",
      "Similarity in Right Triangles"
    ],
    "right-triangles-trigonometry": [
      "Pythagorean Theorem",
      "Converse of the Pythagorean Theorem",
      "Special Right Triangles: 45–45–90",
      "Special Right Triangles: 30–60–90",
      "Geometric Mean and Right-Triangle Altitudes",
      "Sine, Cosine, and Tangent Ratios",
      "Finding Missing Sides with Trigonometry",
      "Finding Missing Angles with Inverse Trigonometry",
      "Angles of Elevation and Depression",
      "Right-Triangle Word Problems"
    ],
    "quadrilaterals-polygons": [
      "Interior and Exterior Angles of Polygons",
      "Properties of Parallelograms",
      "Proving a Quadrilateral Is a Parallelogram",
      "Rectangles and Their Properties",
      "Rhombi and Squares",
      "Trapezoids and Midsegments",
      "Kites and Special Quadrilaterals",
      "Classifying Quadrilaterals",
      "Quadrilaterals on the Coordinate Plane"
    ],
    "transformations": [
      "Translations on the Coordinate Plane",
      "Reflections over Axes and Lines",
      "Rotations about the Origin",
      "Compositions of Transformations",
      "Rigid Motions and Congruence",
      "Dilations and Scale Factor",
      "Similarity Transformations",
      "Symmetry and Invariant Properties",
      "Coordinate Proofs Using Transformations"
    ],
    "circles": [
      "Parts of a Circle: Radius, Diameter, Chord, and Arc",
      "Central Angles and Arc Measures",
      "Inscribed Angles and Intercepted Arcs",
      "Angles Formed by Chords, Secants, and Tangents",
      "Tangents and Radius Properties",
      "Chord Lengths and Distances from the Center",
      "Arc Length and Sector Area",
      "Segment Relationships in Circles",
      "Equations of Circles on the Coordinate Plane"
    ],
    "area-surface-area-volume": [
      "Perimeter and Area of Polygons",
      "Area of Triangles, Trapezoids, and Regular Polygons",
      "Area of Composite Figures",
      "Circumference and Area of Circles",
      "Arc Length and Sector Area Applications",
      "Nets and Surface Area of Prisms and Pyramids",
      "Volume of Prisms, Cylinders, Pyramids, and Cones",
      "Surface Area and Volume of Spheres",
      "Composite Solids",
      "Effects of Scale Factor on Area and Volume"
    ]
  },
  "algebra2": {
    "functions-transformations": [
      "Function notation and evaluation",
      "Domain and range",
      "Operations and composition of functions",
      "Inverse functions",
      "Parent functions and graph transformations",
      "Piecewise functions",
      "Even and odd functions",
      "Modeling with functions"
    ],
    "linear-functions-systems": [
      "Linear equations in multiple forms",
      "Slope and rate of change",
      "Writing linear models",
      "Systems by graphing and substitution",
      "Systems by elimination",
      "Linear inequalities and systems",
      "Linear programming and applications"
    ],
    "quadratic-functions-complex-numbers": [
      "Graphing quadratic functions",
      "Vertex and intercept forms",
      "Factoring quadratic expressions",
      "Solving by square roots and completing the square",
      "Quadratic formula and discriminant",
      "Complex numbers and arithmetic",
      "Quadratic equations with complex solutions",
      "Quadratic modeling applications"
    ],
    "polynomial-functions": [
      "Polynomial operations",
      "Special products and factoring",
      "Long division and synthetic division",
      "Remainder and factor theorems",
      "Zeros and multiplicities",
      "Graphing polynomial functions",
      "Fundamental theorem of algebra",
      "Polynomial equations and applications"
    ],
    "radicals-rational-exponents": [
      "Simplifying radicals",
      "Operations with radical expressions",
      "Rational exponents",
      "Converting between radicals and exponents",
      "Solving radical equations",
      "Extraneous solutions",
      "Graphing square-root and cube-root functions",
      "Radical function transformations"
    ],
    "exponential-logarithmic-functions": [
      "Exponential growth and decay",
      "Graphing exponential functions",
      "Inverse relationship of exponentials and logarithms",
      "Logarithm properties",
      "Evaluating logarithms",
      "Solving exponential equations",
      "Solving logarithmic equations",
      "Compound interest and real-world models"
    ],
    "rational-functions": [
      "Simplifying rational expressions",
      "Multiplying and dividing rational expressions",
      "Adding and subtracting rational expressions",
      "Solving rational equations",
      "Excluded values and extraneous solutions",
      "Vertical and horizontal asymptotes",
      "Graphing rational functions",
      "Rational variation and modeling"
    ],
    "sequences-series": [
      "Arithmetic sequences",
      "Geometric sequences",
      "Recursive and explicit formulas",
      "Arithmetic series and sums",
      "Geometric series and sums",
      "Sigma notation",
      "Finite and infinite geometric series",
      "Applications of sequences"
    ],
    "conic-sections": [
      "Circles in standard form",
      "Parabolas and focus-directrix form",
      "Ellipses and their equations",
      "Hyperbolas and their equations",
      "Graphing conic sections",
      "Converting equations to standard form",
      "Identifying conics from equations"
    ],
    "trigonometric-functions": [
      "Angles in degrees and radians",
      "Unit circle coordinates",
      "Sine, cosine, and tangent",
      "Graphs of sine and cosine",
      "Amplitude, period, and phase shift",
      "Trigonometric identities",
      "Solving trigonometric equations",
      "Inverse trigonometric functions",
      "Trigonometric modeling"
    ],
    "probability-statistics": [
      "Counting principles and permutations",
      "Combinations",
      "Independent and dependent events",
      "Conditional probability",
      "Probability distributions",
      "Expected value",
      "Normal distributions and z-scores",
      "Sampling, inference, and statistical models"
    ]
  },
  "prealgebra": {
    "real-numbers-exponents": [
      "Rational numbers",
      "Operations with rational numbers",
      "Converting fractions and decimals",
      "Identifying irrational numbers",
      "Properties of irrational numbers",
      "Comparing and ordering irrational numbers",
      "Evaluating and approximating square and cube roots",
      "Negative exponents",
      "Operations with negative exponents",
      "Scientific notation",
      "Operations with numbers in scientific notation"
    ],
    "equations-expressions": [
      "Expressions with radical exponents",
      "Expressions with integer exponents",
      "Creating linear equations",
      "Solving equations with variables on both sides",
      "Solving equations using the distributive property",
      "Solving equations by combining like terms",
      "One, infinitely many, or no solutions",
      "Solving exponent equations"
    ],
    "linear-functional-relationships": [
      "Introduction to functions and writing function rules",
      "Graphing functions",
      "Distinguishing linear and nonlinear functions",
      "Exploring linear functions",
      "Equations of linear functions",
      "Graphs of linear functions",
      "Tables of linear functions",
      "Increasing, decreasing, maximum, and minimum",
      "Interpreting rates of change",
      "Interpreting functions in context",
      "Sketching piecewise functions"
    ],
    "systems-linear-equations": [
      "Graphing in slope-intercept form",
      "Solving systems by graphing",
      "Solving systems by substitution",
      "Solving systems by elimination",
      "Solving systems by inspection",
      "Applications of systems of linear equations"
    ],
    "patterns-bivariate-data": [
      "Constructing scatter plots",
      "Analyzing scatter plots",
      "Linear and nonlinear association",
      "Lines of best fit",
      "Constructing two-way tables",
      "Interpreting two-way tables"
    ],
    "congruence-similarity": [
      "Identifying transformations",
      "Rotations and their properties",
      "Reflections and their properties",
      "Translations and their properties",
      "Dilations and their properties",
      "Sequences of transformations: congruence and similarity",
      "Sum of the angles in a triangle",
      "Similar triangles",
      "Parallel lines cut by a transversal"
    ],
    "geometry-applications": [
      "Pythagorean theorem and its converse",
      "Two-dimensional applications of the Pythagorean theorem",
      "Three-dimensional applications of the Pythagorean theorem",
      "Distance between points using the Pythagorean theorem",
      "Volume of cylinders, cones, and spheres",
      "Solving for a missing dimension",
      "Volume of composite solids"
    ]
  },
  "prealgebra7": {
    "algebraic-expressions-integers": [
      "Place Value",
      "Variables and Expressions",
      "The Order of Operations",
      "Writing and Evaluating Expressions",
      "Integers and Absolute Value",
      "Adding Integers",
      "Subtracting Integers",
      "Problem Solving: Rounding and Estimating",
      "Inductive Reasoning",
      "Patterns",
      "Multiplying and Dividing Integers",
      "The Coordinate Plane"
    ],
    "one-step-equations-inequalities": [
      "Properties of Numbers",
      "The Distributive Property",
      "Simplifying Variable Expressions",
      "Variables and Equations",
      "Solving Equations by Adding or Subtracting",
      "Solving Equations by Multiplying or Dividing",
      "Guess, Check, and Revise",
      "Inequalities and Their Graphs",
      "Solving One-Step Inequalities by Adding or Subtracting",
      "Solving One-Step Inequalities by Multiplying or Dividing"
    ],
    "decimals-equations": [
      "Rounding and Estimating",
      "Estimating Decimal Products and Quotients",
      "Mean, Median, and Mode",
      "Using Formulas",
      "Solving Equations by Adding or Subtracting Decimals",
      "Solving Equations by Multiplying or Dividing Decimals",
      "Using the Metric System"
    ],
    "factors-fractions-exponents": [
      "Divisibility and Factors",
      "Exponents",
      "Prime Factorization and Greatest Common Factor",
      "Simplifying Fractions",
      "Rational Numbers",
      "Irrational Numbers",
      "Exponents and Multiplication",
      "Exponents and Division",
      "Scientific Notation",
      "Cube Roots"
    ],
    "operations-fractions": [
      "Comparing and Ordering Rational Numbers",
      "Fractions and Decimals",
      "Adding and Subtracting Fractions",
      "Multiplying and Dividing Fractions",
      "Using Customary Units of Measurement",
      "Solving Equations by Adding or Subtracting Fractions",
      "Solving Equations by Multiplying Fractions",
      "Powers of Products and Quotients"
    ],
    "ratios-proportions-percentages": [
      "Ratios and Unit Rates",
      "Proportions",
      "Similar Figures and Scale Drawings",
      "Probability",
      "Fractions, Decimals, and Percentages",
      "Proportions and Percentages",
      "Percentages and Equations",
      "Percent of Change",
      "Markup and Discount",
      "Tables"
    ],
    "solving-equations-inequalities": [
      "Solving Two-Step Equations",
      "Solving Multi-Step Equations",
      "Multi-Step Equations with Fractions and Decimals",
      "Write an Equation",
      "Solving Equations with Variables on Both Sides",
      "Solving Two-Step Inequalities",
      "Transforming Formulas",
      "Simple and Compound Interest"
    ],
    "linear-functions-graphing": [
      "Relations and Functions",
      "Equations with Two Variables",
      "Slope and y-intercept",
      "Writing Rules for Linear Functions",
      "Scatter Plots",
      "Solving Systems of Linear Equations by Graphing",
      "Solving Systems of Linear Equations by Substitution",
      "Graphing Linear Inequalities"
    ],
    "spatial-thinking": [
      "Introduction to Geometry: Points, Lines, and Planes",
      "Angle Relationships and Parallel Lines",
      "Classifying Polygons",
      "Draw a Diagram",
      "Congruence",
      "Circles",
      "Constructions",
      "Translations",
      "Symmetry and Rotations",
      "Rotations"
    ],
    "area-volume": [
      "Area of Parallelograms",
      "Area of Triangles and Trapezoids",
      "Area of Circles",
      "Space Figures",
      "Surface Area of Prisms and Cylinders",
      "Surface Area of Pyramids, Cones, and Spheres",
      "Volumes of Prisms and Cylinders",
      "Volume of Pyramids, Cones, and Spheres"
    ],
    "right-triangles-algebra": [
      "Square Roots and Irrational Numbers",
      "The Pythagorean Theorem",
      "Distance and Midpoint Formulas",
      "Write a Proportion",
      "Special Right Triangles",
      "Sine, Cosine, and Tangent Ratios",
      "Angles of Elevation and Depression"
    ],
    "data-analysis-probability": [
      "Frequency Tables, Line Plots, and Histograms",
      "Box-and-Whisker Plots",
      "Stem and Leaf Plots",
      "Counting Outcomes and Theoretical Probability",
      "Independent and Dependent Events",
      "Permutations and Combinations",
      "Experimental Probability",
      "Random Samples and Surveys"
    ],
    "nonlinear-functions-polynomials": [
      "Patterns and Sequences",
      "Graphing Nonlinear Functions",
      "Exponential Growth and Decay",
      "Polynomials",
      "Adding and Subtracting Polynomials",
      "Multiplying a Polynomial by a Monomial",
      "Multiplying Binomials",
      "Using Multiple Strategies"
    ]
  },
  "math5": {
    "place-value-number-sense": [
      "Place Value Patterns",
      "Powers of Ten and Exponents",
      "Reading and Writing Decimals",
      "Comparing and Ordering Decimals",
      "Rounding Decimals"
    ],
    "multi-digit-multiplication-division": [
      "Multiplying Multi-Digit Whole Numbers",
      "Estimating Products and Quotients",
      "Dividing by One-Digit Divisors",
      "Dividing by Two-Digit Divisors",
      "Interpreting Remainders in Word Problems"
    ],
    "decimal-operations": [
      "Adding and Subtracting Decimals",
      "Multiplying Decimals by Whole Numbers",
      "Multiplying Decimals by Decimals",
      "Dividing Decimals by Whole Numbers",
      "Dividing by Decimals",
      "Decimal Word Problems and Money"
    ],
    "numerical-expressions-patterns": [
      "Order of Operations with Grouping Symbols",
      "Writing Numerical Expressions",
      "Interpreting Expressions Without Evaluating",
      "Generating Numerical Patterns",
      "Relationships Between Two Patterns"
    ],
    "fraction-addition-subtraction": [
      "Equivalent Fractions and Common Denominators",
      "Adding Fractions with Unlike Denominators",
      "Subtracting Fractions with Unlike Denominators",
      "Adding and Subtracting Mixed Numbers",
      "Estimating with Benchmark Fractions",
      "Fraction Word Problems"
    ],
    "fraction-multiplication-division": [
      "Fractions as Division",
      "Multiplying a Fraction by a Whole Number",
      "Multiplying Fractions by Fractions",
      "Area with Fractional Side Lengths",
      "Multiplication as Scaling",
      "Dividing Unit Fractions and Whole Numbers",
      "Fraction Multiplication and Division Word Problems"
    ],
    "measurement-conversions": [
      "Customary Length Conversions",
      "Customary Weight and Capacity Conversions",
      "Metric Conversions",
      "Multi-Step Measurement Problems"
    ],
    "volume-three-dimensional-figures": [
      "Understanding Volume and Unit Cubes",
      "Counting Cubes to Find Volume",
      "Volume Formulas",
      "Volume of Composite Figures",
      "Volume Word Problems"
    ],
    "coordinate-plane-graphing": [
      "The Coordinate System",
      "Plotting and Reading Points",
      "Real-World Problems on the Coordinate Plane",
      "Graphing Patterns and Relationships"
    ],
    "classifying-two-dimensional-figures": [
      "Polygons and Their Attributes",
      "Classifying Triangles",
      "Classifying Quadrilaterals",
      "Shape Hierarchies"
    ],
    "data-line-plots-problem-solving": [
      "Reading Line Plots with Fractions",
      "Making Line Plots",
      "Solving Problems with Line Plot Data",
      "Multi-Step Problem Solving"
    ]
  },
  "math6": {
    "ratios-rates-percent-proportions": [
      "Ratios",
      "Unit Rate",
      "Equivalent Ratios and Tables",
      "Comparing Ratios",
      "Proportions",
      "Percent and Rates per 100",
      "A Fraction as a Percent",
      "Ratio and Measurement Units"
    ],
    "fractions-decimals-operations": [
      "Dividing Fractions",
      "Dividing Whole Numbers and Fractions",
      "Dividing Mixed Numbers and Fractions",
      "Dividing Multi-Digit Numbers",
      "Adding and Subtracting Multi-Digit Decimals",
      "Multiplying and Dividing Multi-Digit Decimals",
      "Least Common Multiple and Greatest Common Factor",
      "The Distributive Property and Products of Decimals"
    ],
    "rational-numbers": [
      "Positive and Negative Numbers",
      "Positive and Negative Numbers on the Number Line",
      "Comparing and Ordering Rational Numbers",
      "Writing and Interpreting Inequality Statements",
      "Absolute Value of Rational Numbers",
      "Absolute Value and Ordering Numbers",
      "Rational Numbers and the Coordinate Plane",
      "Ordered Pairs on the Coordinate Plane",
      "Distance on the Coordinate Plane"
    ],
    "expressions-equations": [
      "Writing and Evaluating Numerical Expressions with Exponents",
      "Writing and Evaluating Algebraic Expressions",
      "The Order of Operations",
      "Equivalent Expressions",
      "Solutions of Equations",
      "Solving One-Variable Equations",
      "Dependent and Independent Variables"
    ],
    "inequalities": [
      "Inequalities",
      "Solving One-Variable Inequalities",
      "Solutions of Inequalities",
      "Solutions of Inequalities on the Number Line",
      "Applications of Inequalities"
    ],
    "geometry": [
      "Area of Special Quadrilaterals",
      "Area of Right Triangles",
      "Area of All Triangles",
      "Area of Polygons Through Composition and Decomposition",
      "Volume of Right Rectangular Prisms",
      "Polygons on the Coordinate Plane",
      "Perimeter and Area of Polygons on the Coordinate Plane",
      "Nets and Surface Area"
    ],
    "data-displays": [
      "Statistical Questions",
      "Displaying Data on Dot Plots, Histograms, and Box Plots",
      "Mean and Median",
      "Range and Interquartile Range",
      "Mean Absolute Deviation",
      "Comparing Data Displays",
      "Shape of Data Distributions",
      "Describing Distributions"
    ]
  }
};
  function get(courseId,unitId){
    return (skills[courseId] && skills[courseId][unitId] || []).slice();
  }
  function getSkillRecords(courseId,unitId){
    return get(courseId,unitId).map(function(name,i){
      return {id:unitId+'-skill-'+String(i+1).padStart(2,'0'),name:name,index:i+1};
    });
  }
  function listCourses(library){
    return (library && library.courses || []).map(function(course){
      return {id:course.id,name:course.name,units:course.units.map(function(unit){
        return {id:unit.id,name:unit.name,skills:getSkillRecords(course.id,unit.id),resources:(unit.artifacts||[]).map(function(a){return {title:a.title,path:a.path};})};
      })};
    });
  }
  root.MK_COURSE_CATALOG = {skills:skills,getSkills:get,getSkillRecords:getSkillRecords,listCourses:listCourses,version:1};
})(typeof window !== 'undefined' ? window : globalThis);
