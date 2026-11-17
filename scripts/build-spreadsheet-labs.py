"""Build the three Financial Algebra spreadsheet-lab templates (2026-11-17).

Writes financial/spreadsheet-labs/<lab>.xlsx from the steps in financial/spreadsheet-labs/labs.json (the lab page reads the same file). Each workbook has an Instructions sheet with numbered steps and a
working sheet with sample numbers and live formulas, so it opens ready to use in Excel or Google Sheets
(File > Import > Upload). Run: python3 scripts/build-spreadsheet-labs.py
tests/spreadsheet-labs.test.mjs checks the formulas; scripts/check-spreadsheet-labs.sh recalculates them in
LibreOffice and compares the results with the lab pages' "check your sheet" values.
"""
import json
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUT = os.path.join(os.path.dirname(__file__), '..', 'financial', 'spreadsheet-labs')
os.makedirs(OUT, exist_ok=True)
LABS = {l['slug']: l for l in json.load(open(os.path.join(OUT, 'labs.json')))['labs']}
BOLD = Font(bold=True)
HEAD = PatternFill('solid', fgColor='E6E8F7')
INPUT = PatternFill('solid', fgColor='FFF6D6')
THIN = Border(bottom=Side(style='thin', color='B0B3CC'))
MONEY = '"$"#,##0.00'
PCT = '0.0%'


def instructions(wb, title, steps, note):
    ws = wb.active
    ws.title = 'Instructions'
    ws['A1'] = title
    ws['A1'].font = Font(bold=True, size=14)
    ws['A2'] = 'Mr. K\'s Classroom · Financial Algebra · Fictional numbers for classroom use.'
    ws['A4'] = 'Steps'
    ws['A4'].font = BOLD
    for i, s in enumerate(steps):
        ws.cell(row=5 + i, column=1, value=f'{i + 1}. {s}').alignment = Alignment(wrap_text=True, vertical='top')
    ws.cell(row=6 + len(steps), column=1, value=note).font = Font(italic=True)
    ws.column_dimensions['A'].width = 110
    return ws


def style_header(ws, row, cols):
    for c in range(1, cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = BOLD
        cell.fill = HEAD
        cell.border = THIN


# ---------- Lab 1: Monthly budget ----------
wb = Workbook()
instructions(wb, LABS['budget']['title'], LABS['budget']['steps'], LABS['budget']['check'])
ws = wb.create_sheet('Budget')
ws['A1'] = 'Monthly budget'
ws['A1'].font = Font(bold=True, size=13)
ws['A3'], ws['B3'] = 'Income', 'Monthly'
style_header(ws, 3, 2)
for r, (name, v) in enumerate([('Net pay', 2800), ('Other income', 150)], start=4):
    ws.cell(row=r, column=1, value=name)
    c = ws.cell(row=r, column=2, value=v)
    c.fill, c.number_format = INPUT, MONEY
ws['A6'], ws['B6'] = 'Total income', '=SUM(B4:B5)'
ws['A6'].font = BOLD
ws['B6'].number_format = MONEY
for i, h in enumerate(['Expense', 'Monthly', 'Type', 'Share of income'], start=1):
    ws.cell(row=8, column=i, value=h)
style_header(ws, 8, 4)
expenses = [('Rent', 1100, 'Fixed'), ('Utilities', 120, 'Variable'), ('Phone', 55, 'Fixed'), ('Car insurance', 130, 'Fixed'),
            ('Groceries', 380, 'Variable'), ('Gas', 140, 'Variable'), ('Student loan', 210, 'Fixed'), ('Streaming', 25, 'Fixed'),
            ('Fun', 240, 'Variable'), ('Savings transfer', 300, 'Fixed')]
types = DataValidation(type='list', formula1='"Fixed,Variable"', allow_blank=True)
ws.add_data_validation(types)
for r, (name, v, t) in enumerate(expenses, start=9):
    ws.cell(row=r, column=1, value=name)
    c = ws.cell(row=r, column=2, value=v)
    c.fill, c.number_format = INPUT, MONEY
    tc = ws.cell(row=r, column=3, value=t)
    tc.fill = INPUT
    types.add(tc)
    d = ws.cell(row=r, column=4, value=f'=B{r}/$B$6')
    d.number_format = PCT
ws['A19'], ws['B19'], ws['D19'] = 'Total expenses', '=SUM(B9:B18)', '=B19/$B$6'
ws['A19'].font = BOLD
ws['B19'].number_format, ws['D19'].number_format = MONEY, PCT
ws['A21'], ws['B21'] = 'Net cash flow', '=B6-B19'
ws['A21'].font = BOLD
ws['B21'].number_format = MONEY
from openpyxl.formatting.rule import CellIsRule
ws.conditional_formatting.add('B21', CellIsRule(operator='lessThan', formula=['0'], font=Font(color='C00000', bold=True)))
ws['A23'], ws['B23'] = 'Fixed expenses', '=SUMIF(C9:C18,"Fixed",B9:B18)'
ws['A24'], ws['B24'] = 'Variable expenses', '=SUMIF(C9:C18,"Variable",B9:B18)'
ws['B23'].number_format = ws['B24'].number_format = MONEY
ws.column_dimensions['A'].width = 22
for col in 'BCD':
    ws.column_dimensions[col].width = 16
wb.save(os.path.join(OUT, 'budget.xlsx'))

# ---------- Lab 2: Amortization table ----------
wb = Workbook()
instructions(wb, LABS['amortization']['title'], LABS['amortization']['steps'], LABS['amortization']['check'])
ws = wb.create_sheet('Loan')
for r, (k, v, fmt) in enumerate([('Loan amount', 18000, MONEY), ('APR', 0.069, '0.00%'), ('Months', 60, '0')], start=1):
    ws.cell(row=r, column=1, value=k).font = BOLD
    c = ws.cell(row=r, column=2, value=v)
    c.fill, c.number_format = INPUT, fmt
ws['A4'], ws['B4'] = 'Monthly payment', '=ROUND(PMT(B2/12,B3,-B1),2)'
ws['A5'], ws['B5'] = 'Total interest', '=SUM(C9:C80)'
ws['A6'], ws['B6'] = 'Total paid', '=SUM(B9:B80)'
for a in ('A4', 'A5', 'A6'):
    ws[a].font = BOLD
for a in ('B4', 'B5', 'B6'):
    ws[a].number_format = MONEY
for i, h in enumerate(['Payment #', 'Payment', 'Interest', 'Principal', 'Balance'], start=1):
    ws.cell(row=7, column=i, value=h)
style_header(ws, 7, 5)
ws['A8'], ws['E8'] = 0, '=B1'
ws['E8'].number_format = MONEY
for n in range(1, 73):
    r = 8 + n
    ws.cell(row=r, column=1, value=f'=IF({n}>$B$3,"",{n})')
    ws.cell(row=r, column=3, value=f'=IF(A{r}="","",ROUND(E{r - 1}*$B$2/12,2))')
    ws.cell(row=r, column=2, value=f'=IF(A{r}="","",IF(A{r}=$B$3,E{r - 1}+C{r},$B$4))')
    ws.cell(row=r, column=4, value=f'=IF(A{r}="","",B{r}-C{r})')
    ws.cell(row=r, column=5, value=f'=IF(A{r}="","",E{r - 1}-D{r})')
    for c in range(2, 6):
        ws.cell(row=r, column=c).number_format = MONEY
ws.column_dimensions['A'].width = 18
for col in 'BCDE':
    ws.column_dimensions[col].width = 14
ws.freeze_panes = 'A8'
wb.save(os.path.join(OUT, 'amortization.xlsx'))

# ---------- Lab 3: PMT and FV ----------
wb = Workbook()
instructions(wb, LABS['pmt-fv']['title'], LABS['pmt-fv']['steps'], LABS['pmt-fv']['check'])
ws = wb.create_sheet('Calculator')
blocks = [
    (2, 'Block 1: Loan payment (PMT)', [('Amount borrowed', 24000, MONEY), ('APR', 0.065, '0.00%'), ('Months', 60, '0')], ('Monthly payment', '=PMT(B4/12,B5,-B3)')),
    (8, 'Block 2: Savings growth (FV)', [('Monthly deposit', 100, MONEY), ('APR', 0.05, '0.00%'), ('Months', 120, '0')], ('Future value', '=FV(B10/12,B11,-B9)')),
    (14, 'Block 3: Saving for a goal (PMT with FV)', [('Goal', 12000, MONEY), ('APR', 0.04, '0.00%'), ('Months', 36, '0')], ('Monthly deposit needed', '=PMT(B16/12,B17,0,-B15)')),
]
for top, title, inputs, (label, f) in blocks:
    ws.cell(row=top, column=1, value=title).font = Font(bold=True, size=12)
    for i, (k, v, fmt) in enumerate(inputs, start=1):
        ws.cell(row=top + i, column=1, value=k)
        c = ws.cell(row=top + i, column=2, value=v)
        c.fill, c.number_format = INPUT, fmt
    ws.cell(row=top + 4, column=1, value=label).font = BOLD
    ws.cell(row=top + 4, column=2, value=f).number_format = MONEY
ws['A19'], ws['B19'] = 'Check: FV of that deposit', '=FV(B16/12,B17,-B18)'
ws['B19'].number_format = MONEY
ws.column_dimensions['A'].width = 34
ws.column_dimensions['B'].width = 16
wb.save(os.path.join(OUT, 'pmt-fv.xlsx'))
print('wrote budget.xlsx, amortization.xlsx, pmt-fv.xlsx')
