/* Shared helpers for unit projects. */
export const RUBRIC = (s = {}) => [
  { category: 'Financial understanding', points: 20, levels: [s.fin || 'Uses vocabulary precisely and explains every financial concept involved, including assumptions.', 'Mostly accurate explanations with minor vocabulary gaps.', 'Partial understanding; some concepts misapplied.', 'Little evidence of understanding.'] },
  { category: 'Mathematical accuracy', points: 25, levels: [s.math || 'All calculations correct, labeled, and rounded appropriately; work is shown.', '1–2 minor errors that do not change conclusions.', 'Several errors or missing work.', 'Calculations largely missing or incorrect.'] },
  { category: 'Analysis & comparison', points: 20, levels: [s.analysis || 'Compares every option on the same basis and tests at least one changed assumption.', 'Compares options with small gaps.', 'Comparison superficial or uneven.', 'Little analysis.'] },
  { category: 'Justification', points: 15, levels: [s.just || 'Recommendation is supported by specific numbers and weighs non-financial factors and risks.', 'Mostly supported.', 'Mostly opinion.', 'No justification.'] },
  { category: 'Communication & presentation', points: 10, levels: ['Clear, organized, well-labeled tables, charts, and writing.', 'Minor clarity issues.', 'Hard to follow in places.', 'Disorganized.'] },
  { category: 'Completion', points: 10, levels: ['Every checklist item complete.', 'One item missing.', 'Two or three items missing.', 'Most items missing.'] }
];
export const RUBRIC_SLIDE = { title: 'How you will be scored (100 pts)', bullets: ['Financial understanding 20 · Math accuracy 25', 'Analysis & comparison 20 · Justification 15', 'Communication 10 · Completion 10', 'Any well-supported recommendation can earn full credit'] };
