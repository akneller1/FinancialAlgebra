/* Massachusetts 2017 framework-strand navigation, one record per course unit.
 * A strand is a broad topic area, NOT an individual content standard.
 * This mapping must never be used to claim that a question or activity is standards-aligned.
 * Framework source: https://www.doe.mass.edu/frameworks/math/2017-06.pdf
 * "related" means cross-grade/course topical overlap, "prerequisite" means background
 * for a course beyond the 2017 model framework, "no-direct" means no defensible match.
 */
(function(root){
 'use strict';
 var records=[
  {
    "courseId": "math5",
    "unitId": "place-value-number-sense",
    "strand": "5.NBT",
    "relationship": "grade-level"
  },
  {
    "courseId": "math5",
    "unitId": "multi-digit-multiplication-division",
    "strand": "5.NBT",
    "relationship": "grade-level"
  },
  {
    "courseId": "math5",
    "unitId": "decimal-operations",
    "strand": "5.NBT",
    "relationship": "grade-level"
  },
  {
    "courseId": "math5",
    "unitId": "numerical-expressions-patterns",
    "strand": "5.OA",
    "relationship": "grade-level"
  },
  {
    "courseId": "math5",
    "unitId": "fraction-addition-subtraction",
    "strand": "5.NF",
    "relationship": "grade-level"
  },
  {
    "courseId": "math5",
    "unitId": "fraction-multiplication-division",
    "strand": "5.NF",
    "relationship": "grade-level"
  },
  {
    "courseId": "math5",
    "unitId": "measurement-conversions",
    "strand": "5.MD",
    "relationship": "grade-level"
  },
  {
    "courseId": "math5",
    "unitId": "volume-three-dimensional-figures",
    "strand": "5.MD",
    "relationship": "grade-level"
  },
  {
    "courseId": "math5",
    "unitId": "coordinate-plane-graphing",
    "strand": "5.G",
    "relationship": "grade-level"
  },
  {
    "courseId": "math5",
    "unitId": "classifying-two-dimensional-figures",
    "strand": "5.G",
    "relationship": "grade-level"
  },
  {
    "courseId": "math5",
    "unitId": "data-line-plots-problem-solving",
    "strand": "5.MD",
    "relationship": "grade-level"
  },
  {
    "courseId": "math6",
    "unitId": "ratios-rates-percent-proportions",
    "strand": "6.RP",
    "relationship": "grade-level"
  },
  {
    "courseId": "math6",
    "unitId": "fractions-decimals-operations",
    "strand": "6.NS",
    "relationship": "grade-level"
  },
  {
    "courseId": "math6",
    "unitId": "rational-numbers",
    "strand": "6.NS",
    "relationship": "grade-level"
  },
  {
    "courseId": "math6",
    "unitId": "expressions-equations",
    "strand": "6.EE",
    "relationship": "grade-level"
  },
  {
    "courseId": "math6",
    "unitId": "inequalities",
    "strand": "6.EE",
    "relationship": "grade-level"
  },
  {
    "courseId": "math6",
    "unitId": "geometry",
    "strand": "6.G",
    "relationship": "grade-level"
  },
  {
    "courseId": "math6",
    "unitId": "data-displays",
    "strand": "6.SP",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "algebraic-expressions-integers",
    "strand": "7.NS",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "one-step-equations-inequalities",
    "strand": "7.EE",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "decimals-equations",
    "strand": "7.EE",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "factors-fractions-exponents",
    "strand": "7.NS",
    "relationship": "related"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "operations-fractions",
    "strand": "7.NS",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "ratios-proportions-percentages",
    "strand": "7.RP",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "solving-equations-inequalities",
    "strand": "7.EE",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "linear-functions-graphing",
    "strand": "8.F",
    "relationship": "related"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "spatial-thinking",
    "strand": "7.G",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "area-volume",
    "strand": "7.G",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "right-triangles-algebra",
    "strand": "8.G",
    "relationship": "related"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "data-analysis-probability",
    "strand": "7.SP",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra7",
    "unitId": "nonlinear-functions-polynomials",
    "strand": "8.F",
    "relationship": "related"
  },
  {
    "courseId": "prealgebra",
    "unitId": "real-numbers-exponents",
    "strand": "8.NS",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra",
    "unitId": "equations-expressions",
    "strand": "8.EE",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra",
    "unitId": "linear-functional-relationships",
    "strand": "8.F",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra",
    "unitId": "systems-linear-equations",
    "strand": "8.EE",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra",
    "unitId": "patterns-bivariate-data",
    "strand": "8.SP",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra",
    "unitId": "congruence-similarity",
    "strand": "8.G",
    "relationship": "grade-level"
  },
  {
    "courseId": "prealgebra",
    "unitId": "geometry-applications",
    "strand": "8.G",
    "relationship": "grade-level"
  },
  {
    "courseId": "algebra",
    "unitId": "foundations-algebra",
    "strand": "AI.A-SSE",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra",
    "unitId": "expressions-equations",
    "strand": "AI.A-REI",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra",
    "unitId": "inequalities",
    "strand": "AI.A-REI",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra",
    "unitId": "relations-functions",
    "strand": "AI.F-IF",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra",
    "unitId": "linear-equations-slope",
    "strand": "AI.F-IF",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra",
    "unitId": "systems-of-equations",
    "strand": "AI.A-REI",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra",
    "unitId": "exponents-exponential-functions",
    "strand": "AI.N-RN",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra",
    "unitId": "exponential-functions",
    "strand": "AI.F-LE",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra",
    "unitId": "polynomials-factoring",
    "strand": "AI.A-APR",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra",
    "unitId": "factoring-zero-product",
    "strand": "AI.A-SSE",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra",
    "unitId": "quadratics",
    "strand": "AI.F-IF",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra",
    "unitId": "statistics-data-modeling",
    "strand": "AI.S-ID",
    "relationship": "course-strand"
  },
  {
    "courseId": "geometry",
    "unitId": "foundations-geometry",
    "strand": "GEO.G-CO",
    "relationship": "course-strand"
  },
  {
    "courseId": "geometry",
    "unitId": "angles-parallel-lines",
    "strand": "GEO.G-CO",
    "relationship": "course-strand"
  },
  {
    "courseId": "geometry",
    "unitId": "triangle-congruence",
    "strand": "GEO.G-CO",
    "relationship": "course-strand"
  },
  {
    "courseId": "geometry",
    "unitId": "triangle-relationships",
    "strand": "GEO.G-CO",
    "relationship": "course-strand"
  },
  {
    "courseId": "geometry",
    "unitId": "similarity",
    "strand": "GEO.G-SRT",
    "relationship": "course-strand"
  },
  {
    "courseId": "geometry",
    "unitId": "right-triangles-trigonometry",
    "strand": "GEO.G-SRT",
    "relationship": "course-strand"
  },
  {
    "courseId": "geometry",
    "unitId": "quadrilaterals-polygons",
    "strand": "GEO.G-CO",
    "relationship": "course-strand"
  },
  {
    "courseId": "geometry",
    "unitId": "transformations",
    "strand": "GEO.G-CO",
    "relationship": "course-strand"
  },
  {
    "courseId": "geometry",
    "unitId": "circles",
    "strand": "GEO.G-C",
    "relationship": "course-strand"
  },
  {
    "courseId": "geometry",
    "unitId": "area-surface-area-volume",
    "strand": "GEO.G-GMD",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra2",
    "unitId": "functions-transformations",
    "strand": "AII.F-BF",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra2",
    "unitId": "linear-functions-systems",
    "strand": "AII.A-CED",
    "relationship": "related"
  },
  {
    "courseId": "algebra2",
    "unitId": "quadratic-functions-complex-numbers",
    "strand": "AII.N-CN",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra2",
    "unitId": "polynomial-functions",
    "strand": "AII.A-APR",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra2",
    "unitId": "radicals-rational-exponents",
    "strand": "AII.A-REI",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra2",
    "unitId": "exponential-logarithmic-functions",
    "strand": "AII.F-LE",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra2",
    "unitId": "rational-functions",
    "strand": "AII.A-APR",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra2",
    "unitId": "sequences-series",
    "strand": "AII.A-SSE",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra2",
    "unitId": "conic-sections",
    "strand": "PC.G-GPE",
    "relationship": "related"
  },
  {
    "courseId": "algebra2",
    "unitId": "trigonometric-functions",
    "strand": "AII.F-TF",
    "relationship": "course-strand"
  },
  {
    "courseId": "algebra2",
    "unitId": "probability-statistics",
    "strand": "AII.S-CP",
    "relationship": "course-strand"
  },
  {
    "courseId": "precalculus",
    "unitId": "equations-inequalities",
    "strand": "PC.A-REI",
    "relationship": "course-strand"
  },
  {
    "courseId": "precalculus",
    "unitId": "functions",
    "strand": "PC.F-BF",
    "relationship": "course-strand"
  },
  {
    "courseId": "precalculus",
    "unitId": "conics",
    "strand": "PC.G-GPE",
    "relationship": "course-strand"
  },
  {
    "courseId": "precalculus",
    "unitId": "trigonometric-functions",
    "strand": "PC.F-TF",
    "relationship": "course-strand"
  },
  {
    "courseId": "precalculus",
    "unitId": "general-triangle-trigonometry",
    "strand": "PC.G-SRT",
    "relationship": "course-strand"
  },
  {
    "courseId": "precalculus",
    "unitId": "matrices",
    "strand": "PC.N-VM",
    "relationship": "course-strand"
  },
  {
    "courseId": "precalculus",
    "unitId": "vectors",
    "strand": "PC.N-VM",
    "relationship": "course-strand"
  },
  {
    "courseId": "precalculus",
    "unitId": "probability",
    "strand": "AII.S-CP",
    "relationship": "related"
  },
  {
    "courseId": "calculus",
    "unitId": "precalculus-review",
    "strand": "PC.F-BF",
    "relationship": "prerequisite"
  },
  {
    "courseId": "calculus",
    "unitId": "limits-continuity",
    "strand": "PC.F-IF",
    "relationship": "prerequisite"
  },
  {
    "courseId": "calculus",
    "unitId": "derivatives",
    "strand": "PC.F-IF",
    "relationship": "prerequisite"
  },
  {
    "courseId": "calculus",
    "unitId": "applications-derivatives",
    "strand": "PC.F-IF",
    "relationship": "prerequisite"
  },
  {
    "courseId": "calculus",
    "unitId": "antiderivatives-definite-integrals",
    "strand": null,
    "relationship": "no-direct"
  },
  {
    "courseId": "calculus",
    "unitId": "fundamental-theorem-calculus",
    "strand": null,
    "relationship": "no-direct"
  },
  {
    "courseId": "calculus",
    "unitId": "applications-integrals",
    "strand": null,
    "relationship": "no-direct"
  },
  {
    "courseId": "calculus",
    "unitId": "differential-equations",
    "strand": null,
    "relationship": "no-direct"
  },
  {
    "courseId": "calculus",
    "unitId": "ap-review",
    "strand": null,
    "relationship": "no-direct"
  },
  {
    "courseId": "statistics",
    "unitId": "exploring-data",
    "strand": "AII.S-ID",
    "relationship": "related"
  },
  {
    "courseId": "statistics",
    "unitId": "sampling-experimentation",
    "strand": "AII.S-IC",
    "relationship": "related"
  },
  {
    "courseId": "statistics",
    "unitId": "anticipating-patterns",
    "strand": "AII.S-CP",
    "relationship": "related"
  },
  {
    "courseId": "statistics",
    "unitId": "statistical-inference",
    "strand": "AII.S-IC",
    "relationship": "related"
  },
  {
    "courseId": "discrete",
    "unitId": "speaking-mathematically",
    "strand": null,
    "relationship": "no-direct"
  },
  {
    "courseId": "discrete",
    "unitId": "compound-statements-logic",
    "strand": null,
    "relationship": "no-direct"
  },
  {
    "courseId": "discrete",
    "unitId": "number-theory-proof",
    "strand": null,
    "relationship": "no-direct"
  },
  {
    "courseId": "discrete",
    "unitId": "sequences-induction-recursion",
    "strand": "PC.A-APR",
    "relationship": "related"
  },
  {
    "courseId": "discrete",
    "unitId": "set-theory",
    "strand": null,
    "relationship": "no-direct"
  },
  {
    "courseId": "discrete",
    "unitId": "properties-relations",
    "strand": null,
    "relationship": "no-direct"
  },
  {
    "courseId": "discrete",
    "unitId": "counting-probability",
    "strand": "AII.S-CP",
    "relationship": "related"
  },
  {
    "courseId": "discrete",
    "unitId": "graphs-trees",
    "strand": null,
    "relationship": "no-direct"
  },
  {
    "courseId": "discrete",
    "unitId": "election-theory",
    "strand": null,
    "relationship": "no-direct"
  },
  {
    "courseId": "discrete",
    "unitId": "linear-programming",
    "strand": "AI.A-CED",
    "relationship": "related"
  }
];
 function forUnit(courseId,unitId){
  return records.filter(function(r){return r.courseId===courseId&&r.unitId===unitId;})[0]||null;
 }
 root.MK_MA_FRAMEWORK_STRANDS={version:1,framework:'Massachusetts Mathematics Framework 2017',source:'https://www.doe.mass.edu/frameworks/math/2017-06.pdf',records:records,forUnit:forUnit};
})(typeof window!=='undefined'?window:globalThis);
