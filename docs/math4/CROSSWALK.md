# 4th Grade Math: crosswalk from the Math Expressions outline to the ten course units

The development repository held a 12-unit outline taken from the 15-page *Math Expressions Grade 4 – Scope and
Sequence*. The course built here follows the ten Common Core topic units in the project brief, so
`course-outlines/grade4.json` now describes those ten units (the file the preview assembler reads), and the original
outline is kept unchanged as `course-outlines/grade4-math-expressions.json` (its tests still run against it).

Course ID: `math4`. Skill IDs: `<unit-id>-skill-NN`, numbered in the order of `tools/grade4-authoring/outline.py`.
The ten unit IDs are new; none of the twelve outline unit IDs is reused, so nothing that pointed at the old outline
is silently redirected.

## Where each Math Expressions unit went

| Math Expressions unit (outline) | Course unit(s) that teach it |
|---|---|
| 1. Solve Multiplication and Division Word Problems | 3 Multiplication Strategies (comparisons, facts) · 4 Division and Remainders (facts) · 5 Factors, Multiples, and Number Patterns (factors, multiples, prime and composite) · 10 Data and Multi-Step Word Problems (one- and two-step problems, equations) |
| 2. Quadrilaterals | 9 Geometry, Angles, and Symmetry (lines, classification, symmetry) · 8 Measurement (area and perimeter of rectangles) |
| 3. Place Value and Multi-Digit Addition & Subtraction | 1 Place Value and Number Sense · 2 Multi-Digit Addition and Subtraction |
| 4. Angles & Polygons | 9 Geometry, Angles, and Symmetry |
| 5. Multi-Digit Multiplication | 3 Multiplication Strategies and Multi-Digit Multiplication |
| 6. The Metric Measurement System | 8 Measurement and Unit Conversions |
| 7. Multi-Digit Division | 4 Division and Remainders · 8 Measurement (elapsed time) |
| 8. Patterns, Functions, and Graphs | 5 Factors, Multiples, and Number Patterns (rules, input-output tables, shape patterns) |
| 9. Fractions | 6 Fractions and Equivalent Fractions · 7 Fraction Operations and Decimals |
| 10. Three-Dimensional Figures | 8 Measurement (rectangle area and perimeter). See "Not carried over". |
| 11. Decimal Numbers | 7 Fraction Operations and Decimals (tenths and hundredths, comparing decimals) · 8 Measurement (money problems) |
| 12. The U.S. Customary System | 8 Measurement and Unit Conversions |

## Outline objectives that are not Grade 4 Common Core and were not carried over

These appear in the Math Expressions outline but belong to other grades in the Common Core (and the 2017
Massachusetts framework). They are left out so that Grade 5 content is not presented as a Grade 4 requirement.
If your school's pacing guide still teaches them in Grade 4, they would need their own skills.

| Outline objective | Common Core placement |
|---|---|
| Identify and classify cubes, spheres, prisms and pyramids (unit 10) | Grades 1–2 and 6 (volume in Grade 5) |
| Mean, median, mode and range (unit 7) | Grade 6 |
| Probability and experimental probability (unit 9) | Grade 7 |
| Plot ordered pairs on a grid (unit 8) | Grade 5 |
| Multiply and divide decimals by whole numbers (unit 7); add and subtract decimals in general (unit 11) | Grade 5. Grade 4 keeps decimals as fractions with denominators 10 and 100 and money to the cent. |
| Fractions as division (unit 9) | Grade 5 |
| Rotational symmetry, congruent and similar figures (units 2 and 4) | Grade 8. Line symmetry is kept. |
| Bar graphs and pictographs (units 1, 3, 9) | Grade 3. Grade 4 data work is line plots with fractions. |
| Temperature (units 6 and 12) | Not a Common Core measurement standard |

## Outline limits that were kept

- Whole numbers through six digits (one million as the top of the place-value chart).
- Multiplication: up to four digits by one digit, and two digits by two digits. Division: up to four-digit dividends
  with one-digit divisors.
- Factors and multiples within 100. Prime and composite within 100 (the outline says 1–50; the standard says 1–100;
  Remedial items stay at 30 or less).
- Fractions with denominators 2, 3, 4, 5, 6, 8, 10, 12 and 100. Decimals to hundredths.
- Line plots to halves, fourths and eighths.
- Elapsed time: Remedial items stay under one hour (so within two adjacent hours, as the outline says); Standard and
  Advanced items run up to about three hours.
- The two lessons the outline excludes (3.2 and 8.5) are textbook lessons; no course material depends on them.
