/* Curated, narrowly scoped Massachusetts math standards crosswalk.
 * Aligned by specific lesson name, not by entire unit or activity.
 * Curriculum reference: 2017 Massachusetts Mathematics Curriculum Framework
 * https://www.doe.mass.edu/frameworks/math/2017-06.pdf
 * Standards Navigator: https://www.doe.mass.edu/frameworks/search/
 * These links identify a relevant standard; they do not certify each activity.
 */
(function(root){
 'use strict';
 var records=[
  {
    "courseId": "algebra",
    "unitId": "expressions-equations",
    "skill": "Solving Multi-Step Equations",
    "code": "AI.A-REI.B.3",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.A-REI.B.03"
  },
  {
    "courseId": "algebra",
    "unitId": "expressions-equations",
    "skill": "Equations with Variables on Both Sides",
    "code": "AI.A-REI.B.3",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.A-REI.B.03"
  },
  {
    "courseId": "algebra",
    "unitId": "expressions-equations",
    "skill": "Literal Equations and Formulas",
    "code": "AI.A-REI.B.3",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.A-REI.B.03"
  },
  {
    "courseId": "algebra",
    "unitId": "inequalities",
    "skill": "Solving One- and Two-Step Inequalities",
    "code": "AI.A-REI.B.3",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.A-REI.B.03"
  },
  {
    "courseId": "algebra",
    "unitId": "inequalities",
    "skill": "Absolute Value Equations and Inequalities",
    "code": "AI.A-REI.B.3.a",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.A-REI.B.03.a&a=1"
  },
  {
    "courseId": "algebra",
    "unitId": "relations-functions",
    "skill": "Identifying Functions",
    "code": "AI.F-IF.A.1",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.F-IF.A.01"
  },
  {
    "courseId": "algebra",
    "unitId": "relations-functions",
    "skill": "Domain and Range",
    "code": "AI.F-IF.A.1",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.F-IF.A.01"
  },
  {
    "courseId": "algebra",
    "unitId": "relations-functions",
    "skill": "Function Notation and Evaluating Functions",
    "code": "AI.F-IF.A.1",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.F-IF.A.01"
  },
  {
    "courseId": "algebra",
    "unitId": "systems-of-equations",
    "skill": "Solving Systems by Graphing",
    "code": "AI.A-REI.C.6",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.A-REI.C.06"
  },
  {
    "courseId": "algebra",
    "unitId": "systems-of-equations",
    "skill": "Solving Systems by Substitution",
    "code": "AI.A-REI.C.6",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.A-REI.C.06"
  },
  {
    "courseId": "algebra",
    "unitId": "systems-of-equations",
    "skill": "Solving Systems by Elimination (Add/Subtract)",
    "code": "AI.A-REI.C.6",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.A-REI.C.06"
  },
  {
    "courseId": "algebra",
    "unitId": "systems-of-equations",
    "skill": "Elimination with Multiplication",
    "code": "AI.A-REI.C.6",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.A-REI.C.06"
  },
  {
    "courseId": "algebra",
    "unitId": "systems-of-equations",
    "skill": "Graphing Linear Inequalities in Two Variables",
    "code": "AI.A-REI.D.12",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CIS_CODE=AI.A-REI.D.12"
  },
  {
    "courseId": "algebra",
    "unitId": "systems-of-equations",
    "skill": "Systems of Linear Inequalities",
    "code": "AI.A-REI.D.12",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CIS_CODE=AI.A-REI.D.12"
  },
  {
    "courseId": "algebra",
    "unitId": "exponential-functions",
    "skill": "Linear vs. Exponential Patterns",
    "code": "AI.F-LE.A.1",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CIS_CODE=AI.F-LE.A.1"
  },
  {
    "courseId": "algebra",
    "unitId": "quadratics",
    "skill": "Completing the Square",
    "code": "AI.A-REI.B.4.a",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.A-REI.B.04.a&a=1"
  },
  {
    "courseId": "algebra",
    "unitId": "quadratics",
    "skill": "The Quadratic Formula",
    "code": "AI.A-REI.B.4.b",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.A-REI.B.04.b"
  },
  {
    "courseId": "algebra",
    "unitId": "factoring-zero-product",
    "skill": "Solving Quadratic Equations by Factoring",
    "code": "AI.A-REI.B.4.b",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.AI.A-REI.B.04.b"
  },
  {
    "courseId": "geometry",
    "unitId": "angles-parallel-lines",
    "skill": "Vertical Angles and Linear Pairs",
    "code": "GEO.G-CO.C.9",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.GEO.G-CO.C.09"
  },
  {
    "courseId": "geometry",
    "unitId": "angles-parallel-lines",
    "skill": "Corresponding and Alternate Interior Angles",
    "code": "GEO.G-CO.C.9",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.GEO.G-CO.C.09"
  },
  {
    "courseId": "geometry",
    "unitId": "angles-parallel-lines",
    "skill": "Proving Lines Parallel",
    "code": "GEO.G-CO.C.9",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.GEO.G-CO.C.09"
  },
  {
    "courseId": "geometry",
    "unitId": "triangle-congruence",
    "skill": "Congruent Figures and Rigid Motions",
    "code": "GEO.G-CO.B.6",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.GEO.G-CO.B.06&a=1"
  },
  {
    "courseId": "geometry",
    "unitId": "triangle-congruence",
    "skill": "SSS and SAS Triangle Congruence",
    "code": "GEO.G-CO.B.8",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.GEO.G-CO.B.08"
  },
  {
    "courseId": "geometry",
    "unitId": "triangle-congruence",
    "skill": "Corresponding Parts of Triangles",
    "code": "GEO.G-CO.B.7",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.GEO.G-CO.B.07&a=1"
  },
  {
    "courseId": "geometry",
    "unitId": "similarity",
    "skill": "AA Triangle Similarity",
    "code": "GEO.G-SRT.A.3",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CIS_CODE=GEO.G-SRT.A.3"
  },
  {
    "courseId": "geometry",
    "unitId": "similarity",
    "skill": "Scale Factors and Dilations",
    "code": "GEO.G-SRT.A.1",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CIS_CODE=GEO.G-SRT.A.1"
  },
  {
    "courseId": "geometry",
    "unitId": "similarity",
    "skill": "SAS and SSS Triangle Similarity",
    "code": "GEO.G-SRT.B.5",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.GEO.G-SRT.B.05"
  },
  {
    "courseId": "geometry",
    "unitId": "right-triangles-trigonometry",
    "skill": "Sine, Cosine, and Tangent Ratios",
    "code": "GEO.G-SRT.C.6",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CIS_CODE=GEO.G-SRT.C.6"
  },
  {
    "courseId": "geometry",
    "unitId": "right-triangles-trigonometry",
    "skill": "Right-Triangle Word Problems",
    "code": "GEO.G-SRT.C.8",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.GEO.G-SRT.C.08&a=1"
  },
  {
    "courseId": "geometry",
    "unitId": "transformations",
    "skill": "Rigid Motions and Congruence",
    "code": "GEO.G-CO.B.6",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.GEO.G-CO.B.06&a=1"
  },
  {
    "courseId": "geometry",
    "unitId": "circles",
    "skill": "Arc Length and Sector Area",
    "code": "GEO.G-C.B.5",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.GEO.G-C.B.05&a=1"
  },
  {
    "courseId": "geometry",
    "unitId": "circles",
    "skill": "Equations of Circles on the Coordinate Plane",
    "code": "GEO.G-GPE.A.1",
    "url": "https://www.doe.mass.edu/frameworks/search/Map.aspx?ST_CODE=Mathematics.GEO.G-GPE.A.01"
  }
];
 function forSkill(courseId,unitId,skill){
  return records.filter(function(r){return r.courseId===courseId&&r.unitId===unitId&&r.skill===skill;}).slice();
 }
 root.MK_MA_STANDARDS={version:1,framework:'Massachusetts 2017',records:records,forSkill:forSkill};
})(typeof window!=='undefined'?window:globalThis);
