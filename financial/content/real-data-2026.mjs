/* Real federal figures for tax year 2026, used by the dated "2026" question families (2026-11-16).
 * Sources: IRS Rev. Proc. 2025-32 (brackets, standard deduction); SSA notice for 2026 (Federal Register,
 * 3 Nov 2025) for the Social Security wage base. Update once a year: change these numbers, `year` and `asOf`,
 * then rebuild with node scripts/build-banks.mjs. tests/fa-applied.test.mjs fails if asOf is more than
 * 15 months old, so stale figures are caught. */
export const TAX_2026 = {
  year: 2026,
  asOf: 'November 2026',
  asOfDate: '2026-11-16',
  source: 'IRS Rev. Proc. 2025-32',
  standardDeduction: { single: 16100, marriedJoint: 32200, headOfHousehold: 24150 },
  bracketsSingle: [
    { rate: 0.10, upTo: 12400 }, { rate: 0.12, upTo: 50400 }, { rate: 0.22, upTo: 105700 }, { rate: 0.24, upTo: 201775 },
    { rate: 0.32, upTo: 256225 }, { rate: 0.35, upTo: 640600 }, { rate: 0.37, upTo: Infinity }
  ],
  socialSecurityWageBase: 184500,
  socialSecurityRate: 0.062,
  medicareRate: 0.0145
};
