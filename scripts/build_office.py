"""Builds editable Word packets/guides and PowerPoint slides for every project in dist/office-jobs.json.
Run after scripts/build-print.mjs.  python3 scripts/build_office.py"""
import json, re, sys
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.table import WD_TABLE_ALIGNMENT
from pptx import Presentation
from pptx.util import Inches as PI, Pt as PP
from pptx.dml.color import RGBColor as PR
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parents[1]
PURPLE, INK, TINT = RGBColor(0x5a, 0x2f, 0xd6), RGBColor(0x14, 0x17, 0x3a), 'EBE3FF'
clean = lambda s: re.sub(r'\[\[(.+?)\|\|(.+?)\]\]', lambda m: m.group(1).strip() + ' ÷ ' + m.group(2).strip(), re.sub(r'\*\*(.+?)\*\*', r'\1', str(s)))

def shade(cell, hexcolor):
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement('w:shd')
    sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hexcolor); tcPr.append(sh)

def new_doc():
    d = Document(); s = d.styles['Normal']; s.font.name = 'Calibri'; s.font.size = Pt(11)
    for sec in d.sections: sec.left_margin = sec.right_margin = Inches(0.75); sec.top_margin = sec.bottom_margin = Inches(0.7)
    return d

def h(d, text, lvl=1):
    p = d.add_heading(clean(text), level=lvl)
    for r in p.runs: r.font.color.rgb = PURPLE if lvl > 1 else INK
    return p

def table(d, headers, rows, widths=None):
    t = d.add_table(rows=1, cols=len(headers)); t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, x in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = clean(x); shade(c, TINT)
        for r in c.paragraphs[0].runs: r.bold = True
    for row in rows:
        cells = t.add_row().cells
        for i, x in enumerate(row): cells[i].text = clean(x)
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                for r in p.runs: r.font.size = Pt(9.5)
    d.add_paragraph()
    return t

def bullets(d, items, style='List Bullet'):
    for x in items: d.add_paragraph(clean(x), style=style)

def lines(d, n):
    for _ in range(n): d.add_paragraph('_' * 86)

def rubric(d, rub):
    table(d, ['Category (points)', 'Exemplary', 'Proficient', 'Developing', 'Beginning'], [[f"{r['category']} ({r['points']})", *r['levels']] for r in rub])
    d.add_paragraph(f"Total: {sum(r['points'] for r in rub)} points. Alternative recommendations earn full credit when supported by accurate evidence.")

def documents(d, p):
    for doc in p['documents']:
        h(d, doc['title'], 3); table(d, doc['table']['headers'], doc['table']['rows'])
        if doc.get('note'): d.add_paragraph(clean(doc['note'])).runs[0].italic = True

def student(p):
    d = new_doc(); h(d, p['title'], 0); d.add_paragraph(clean(p['tagline'])).runs[0].italic = True
    d.add_paragraph(f"Financial Algebra · Unit {p['unitNum']}: {p['unitName']} · {p['days']} · {p['grouping']}")
    d.add_paragraph('Name(s) ______________________________   Period ____   Due ________')
    h(d, 'Introduction', 2); d.add_paragraph(clean(p['intro'])); d.add_paragraph(clean(p['scenario'])).runs[0].bold = True
    h(d, 'Learning goals', 2); bullets(d, p['goals'])
    h(d, 'Supporting documents and data', 2); documents(d, p)
    d.add_page_break(); h(d, 'Tasks', 2)
    for i, t in enumerate(p['tasks']):
        h(d, f"Task {i+1}: {t['title']}", 3); bullets(d, t['steps'], 'List Number')
        d.add_paragraph('Deliverable: ' + clean(t['deliverable'])).runs[0].bold = True; lines(d, 6)
    h(d, 'Reflection', 2)
    for i, q in enumerate(p['reflection']): d.add_paragraph(f"{i+1}. {clean(q)}"); lines(d, 3)
    h(d, 'Submission checklist', 2); bullets(d, ['☐ ' + c for c in p['checklist']], 'Normal')
    d.add_page_break(); h(d, 'Scoring rubric', 2); rubric(d, p['rubric'])
    d.add_paragraph('All people, businesses, places, and numbers in this project are fictional. Rates and costs are illustrative assumptions.').runs[0].italic = True
    return d

def guide(p):
    T = p['teacher']; d = new_doc(); h(d, p['title'] + ' — Teacher Guide', 0)
    d.add_paragraph(f"Financial Algebra · Unit {p['unitNum']}: {p['unitName']} · {p['days']} · {p['grouping']}")
    h(d, 'Overview', 2); d.add_paragraph(clean(p['intro']))
    h(d, 'Skills covered', 2); bullets(d, p['skills'])
    h(d, 'Required materials', 2); bullets(d, T['materials'])
    h(d, 'Suggested pacing', 2); table(d, ['Session', 'Focus'], T['pacing'])
    h(d, 'Implementation guidance', 2); bullets(d, T['implementation'])
    h(d, 'Worked calculations', 2)
    for w in T['worked']: h(d, w['task'], 3); bullets(d, w['work'], 'List Number')
    h(d, 'Sample student responses', 2); bullets(d, T['samples'])
    h(d, 'Common misconceptions', 2); bullets(d, T['misconceptions'])
    h(d, 'Differentiation', 2); d.add_paragraph('Support').runs[0].bold = True; bullets(d, T['differentiation']['support'])
    d.add_paragraph('Extend').runs[0].bold = True; bullets(d, T['differentiation']['extend'])
    h(d, 'Extension opportunities', 2); bullets(d, T['extensions'])
    h(d, '100-point rubric', 2); rubric(d, p['rubric'])
    h(d, 'Student documents (reference)', 2); documents(d, p)
    return d

def slides(p):
    prs = Presentation(); prs.slide_width, prs.slide_height = PI(13.333), PI(7.5)
    blank = prs.slide_layouts[6]
    def add(title, bullets_, first=False):
        s = prs.slides.add_slide(blank)
        bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, PI(7.5 if first else 1.35)); bg.fill.solid(); bg.fill.fore_color.rgb = PR(0x74, 0x48, 0xff) if first else PR(0x14, 0x17, 0x3a); bg.line.fill.background()
        tb = s.shapes.add_textbox(PI(0.6), PI(2.3 if first else 0.25), PI(12), PI(1.2)); tf = tb.text_frame; tf.word_wrap = True
        r = tf.paragraphs[0].add_run(); r.text = clean(title); r.font.size = PP(54 if first else 34); r.font.bold = True; r.font.color.rgb = PR(255, 255, 255)
        box = s.shapes.add_textbox(PI(0.8), PI(3.7 if first else 1.75), PI(11.6), PI(5)); bf = box.text_frame; bf.word_wrap = True
        for i, b in enumerate(bullets_):
            para = bf.paragraphs[0] if i == 0 else bf.add_paragraph()
            run = para.add_run(); run.text = ('' if first else '•  ') + clean(b); run.font.size = PP(26 if first else 24)
            run.font.color.rgb = PR(255, 255, 255) if first else PR(0x14, 0x17, 0x3a); para.space_after = PP(12)
        if not first:
            ft = s.shapes.add_textbox(PI(0.6), PI(6.9), PI(12), PI(0.4)).text_frame.paragraphs[0].add_run()
            ft.text = f"Financial Algebra · Unit {p['unitNum']}: {p['unitName']} · {p['title']}"; ft.font.size = PP(12); ft.font.color.rgb = PR(0x6b, 0x6f, 0x96)
        s.notes_slide.notes_text_frame.text = 'Fictional scenario; values are illustrative assumptions.'
    for i, sl in enumerate(p['slides']): add(sl['title'], sl['bullets'], i == 0)
    return prs

def main():
    jobs = json.loads((ROOT / 'dist/office-jobs.json').read_text())
    for p in jobs:
        out = Path(p['dir']); f = p['slug']
        student(p).save(out / f'{f}-student.docx'); guide(p).save(out / f'{f}-teacher-guide.docx'); slides(p).save(out / f'{f}-slides.pptx')
        print('office files:', f)

if __name__ == '__main__': main()
