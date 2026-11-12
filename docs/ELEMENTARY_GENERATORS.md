# Elementary generator standard

Use the existing Algebra 1 engines for all four teacher generators: worksheet.html,
menu-assessment.html, lesson-planner.html and printables.html. Do not build a reduced
parallel generator for a new grade. Keep elementary class levels Remedial / Standard /
Advanced, exact bank levels and age-appropriate content. Never add student-link controls
to teacher generators; offer student sharing only for individual games and study guides.

The course repository retains its approved banks, teaching notes and assets. The release
assembler adapts these to the main question-bank manifest and authoritative skill catalog.
Grade 5 demonstrates this in scripts/integrate-approved-courses.mjs. Future grades need
an explicit approved release adapter and teaching-note records before publication; adding
a scope alone must not expose an unfinished grade.

Every worksheet/test supports ordered named parts with counts, response formats,
section skills, difficulty, point rules where relevant, parallel versions, question review,
pinning/replacement/manual edits, undo, print layout, saved copies and JSON round trips.
Diagram parts select actual diagram questions. Lesson plans reuse the plan/notes editor,
combined lessons, section order/counts, agenda timing, guided/completed notes and PowerPoint
export. Activities reuse the shared printable controls, variants and teacher keys.

Finite elementary banks may reuse a question across different versions, but never within
one version. A shortage must be visible, and must not change levels or invent questions.
