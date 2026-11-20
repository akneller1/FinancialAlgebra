"""Grade 5 audit (2026-11-19): year-end and planning materials.

#9  math5-practice-test-{a,b}/exam.html and key.html: two cumulative practice tests in the MCAS style. Each has two sessions
    of 20 questions: 12 multiple choice, 3 select all that apply, 4 short answer and a four-part constructed response.
    Session 1 covers Operations and Algebraic Thinking and Number and Operations in Base Ten; Session 2 covers Number and
    Operations: Fractions, Measurement and Data, and Geometry. The selected-response and short-answer items are Standard and
    Advanced core bank items (answers re-derived by verify.py), spread over the skills, and no item is in both tests. The
    constructed-response tasks are written here and their answers are recomputed by check_cr() below.
    math5-reference-sheet/index.html: the conversions and formulas Grade 5 students use, written for this site.
#15 math5-pacing-guide/index.html: a 180-day pacing guide that finishes the course before the spring MCAS window.
#16 lab worksheets for math5-decimal-grid-lab/ and math5-scaling-lab/ (worksheet.html, teacher-key.html).
print_yearend.cjs turns the HTML into PDFs and card thumbnails. Deterministic. Usage (repository root):
    python3 tools/grade5-authoring/yearend.py && node tools/grade5-authoring/print_yearend.cjs"""
import html, json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUTLINE = json.load(open(os.path.join(HERE, 'outline.json'), encoding='utf-8'))
UNITS = [u['id'] for u in OUTLINE['units']]
SESSIONS = [(('OA', 'NBT'), 'Session 1 · Operations and Algebraic Thinking; Number and Operations in Base Ten'),
            (('NF', 'MD', 'G'), 'Session 2 · Fractions; Measurement and Data; Geometry')]
PER_SESSION = {'multiple-choice': 12, 'select-all': 3, 'short-answer': 4}
DOMAIN = {'OA': 'Operations and Algebraic Thinking', 'NBT': 'Number and Operations in Base Ten', 'NF': 'Number and Operations: Fractions',
          'MD': 'Measurement and Data', 'G': 'Geometry'}

# Constructed response, written for these tests: 1 point per part. check_cr() recomputes every answer.
CR = {
 'a': [dict(domain='NBT', title='Art supplies', stem='A school orders 24 boxes of markers. Each box holds 36 markers and costs $2.35.',
            parts=[('How many markers are in the order?', '864 markers'),
                   ('The markers are sorted into bins of 18. How many bins are filled?', '48 bins'),
                   ('What is the cost of the 24 boxes?', '$56.40'),
                   ('The school pays with $60. How much change does it get?', '$3.60')]),
       dict(domain='NF', title='Garden bed', stem='A garden bed is a rectangle 3 1/2 feet long and 2 1/4 feet wide. A raised planter next to it is a rectangular prism 6 feet long, 3 feet wide and 2 feet tall.',
            parts=[('What is the area of the garden bed?', '7 7/8 square feet'),
                   ('How many feet of edging go all the way around the garden bed?', '11 1/2 feet'),
                   ('What is the volume of the planter?', '36 cubic feet'),
                   ('Soil comes in bags of 2 cubic feet. How many bags fill the planter?', '18 bags')])],
 'b': [dict(domain='NBT', title='Field trip', stem='138 students and 12 adults go on a field trip. Each bus holds 44 people and costs $187.50.',
            parts=[('How many people go on the trip?', '150 people'),
                   ('How many buses are needed?', '4 buses'),
                   ('What do the buses cost in all?', '$750.00'),
                   ('The cost is shared equally by all the people. How much does each person pay?', '$5.00')]),
       dict(domain='MD', title='Rain gauge', stem='The rainfall each day for 8 days, in inches: 1/4, 1/2, 3/4, 1/2, 1, 3/4, 1/2, 3/4.',
            parts=[('Make a line plot of the data. On how many days was the rainfall 3/4 inch?', '3 days'),
                   ('What was the total rainfall for the 8 days?', '5 inches'),
                   ('What is the difference between the most and the least rainfall in one day?', '3/4 inch'),
                   ('If the total rainfall were shared equally among the 8 days, how much would fall each day?', '5/8 inch')])]}


def check_cr():
    """Every constructed-response answer recomputed from its stem."""
    a1 = CR['a'][0]['parts']; assert a1[0][1] == f'{24 * 36} markers' and a1[1][1] == f'{24 * 36 // 18} bins' and 24 * 36 % 18 == 0
    assert a1[2][1] == f'${float(24 * F("2.35")):.2f}' and F(60) - 24 * F('2.35') == F('3.60')
    a2 = CR['a'][1]['parts']; L, W = F(7, 2), F(9, 4)
    assert L * W == F(63, 8) and 2 * (L + W) == F(23, 2) and 6 * 3 * 2 == 36 and 36 // 2 == 18
    b1 = CR['b'][0]['parts']; n = 138 + 12; buses = -(-n // 44)
    assert n == 150 and buses == 4 and buses * F('187.50') == 750 and F(750) / n == 5
    vals = [F(1, 4), F(1, 2), F(3, 4), F(1, 2), F(1), F(3, 4), F(1, 2), F(3, 4)]
    assert vals.count(F(3, 4)) == 3 and sum(vals) == 5 and max(vals) - min(vals) == F(3, 4) and sum(vals) / 8 == F(5, 8)


CSS = '''
@page { size: letter; margin: 0.5in 0.55in; }
* { box-sizing: border-box; }
body { font-family: "Atkinson Hyperlegible", Inter, "DejaVu Sans", Arial, sans-serif; color: #14173a; font-size: 10.5pt; line-height: 1.4; margin: 0; }
h1 { font-size: 22pt; margin: 0 0 4px; } h3 { font-size: 12pt; margin: 8px 0 4px; } h2 { font-size: 14pt; margin: 0 0 6px; border-bottom: 2.5px solid #14173a; padding-bottom: 3px; }
.eyebrow { font-size: 9pt; letter-spacing: .12em; text-transform: uppercase; color: #15803d; font-weight: 700; }
.name { display: flex; gap: 14px; margin: 10px 0 14px; } .name span { flex: 1; border-bottom: 1.5px solid #14173a; padding-bottom: 2px; } .name span:first-child { flex: 2.2; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 12px; } th, td { border: 1.5px solid #14173a; padding: 4px 7px; text-align: left; vertical-align: top; } th { background: #dcfce7; }
.box { background: #ecfdf3; border-radius: 8px; padding: 8px 12px; margin: 8px 0; }
.section { break-before: page; }
ol.mc { padding-left: 24px; margin: 0; } ol.mc > li { break-inside: avoid; margin-bottom: 14px; }
.q { white-space: pre-wrap; }
.choices { display: grid; grid-template-columns: 1fr 1fr; gap: 3px 18px; margin-top: 4px; }
.choices div { break-inside: avoid; } .choices b { margin-right: 6px; }
.sel div { margin: 2px 0; } .sel span.bx { display: inline-block; width: 11px; height: 11px; border: 1.5px solid #14173a; margin-right: 7px; vertical-align: -1px; }
.blank { display: inline-block; min-width: 1.8in; border-bottom: 1.5px solid #14173a; height: 18px; margin-top: 4px; }
.tag { font-size: 8pt; color: #4a4f78; margin-left: 6px; font-weight: 700; letter-spacing: .04em; }
img.dg { max-width: 330px; max-height: 190px; display: block; margin: 5px 0; }
.cr { break-inside: avoid; margin: 0 0 12px; } .part { break-inside: avoid; margin: 8px 0 0; } .work { height: 1.05in; border-bottom: 1px dashed #9aa0c8; }
.ans { color: #c8102e; font-weight: 700; } .steps { margin: 3px 0 0 18px; padding: 0; color: #2b2f55; } .steps li { margin-bottom: 2px; }
.foot { font-size: 8.5pt; color: #4a4f78; margin-top: 10px; }
.fr { display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; font-size: .9em; line-height: 1.05; margin: 0 2px; }
.fr span:first-child { border-bottom: 1.2px solid currentColor; padding: 0 2px; }
.ref h3 { margin: 8px 0 3px; border-bottom: 1.5px solid #9aa0c8; } .ref table { margin: 3px 0 6px; } .ref td, .ref th { font-size: 9.6pt; padding: 3px 6px; } .ref td:first-child { width: 36%; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 0 18px; }
.pace td, .pace th { font-size: 9.2pt; padding: 3px 6px; } .pace tr.rev td { background: #fef9c3; } .pace tr.mcas td { background: #fee2e2; font-weight: 700; }
.grid10 { display: inline-grid; grid-template-columns: repeat(10, 15px); border: 2px solid #14173a; margin: 4px 12px 4px 0; } .grid10 i { width: 15px; height: 15px; border: .5px solid #9aa0c8; }
.sq { display: inline-block; width: 150px; height: 150px; border: 2px solid #14173a; margin: 4px 12px 4px 0; }
'''


def esc(s):
    return html.escape(str(s), quote=False)


def frac(n, d):
    return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'


def math(s):
    """Escape, then show a/b and mixed numbers as stacked fractions."""
    s = esc(s)
    s = re.sub(r'(?<![\w/.])(\d+) (\d+)/(\d+)(?![\w/])', lambda m: m.group(1) + frac(m.group(2), m.group(3)), s)
    return re.sub(r'(?<![\w/.])(\d+)/(\d+)(?![\w/])', lambda m: frac(m.group(1), m.group(2)), s)


def page(title, body, eyebrow='5th Grade Math'):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(title)} · Mr. K’s Classroom</title><style>{CSS}</style></head><body><div class="eyebrow">{esc(eyebrow)}</div>{body}</body></html>')


# ------------------------------------------------------------------------------------------------- reference sheet
def reference_html(standalone=True):
    body = f'''<div class="ref"><h2>Grade 5 Mathematics Reference Sheet</h2>
<div class="cols"><div>
<h3>Customary length</h3><table>
<tr><td>1 foot (ft)</td><td>= 12 inches (in.)</td></tr><tr><td>1 yard (yd)</td><td>= 3 feet = 36 inches</td></tr><tr><td>1 mile (mi)</td><td>= 5,280 feet</td></tr></table>
<h3>Customary capacity</h3><table>
<tr><td>1 cup (c)</td><td>= 8 fluid ounces (fl oz)</td></tr><tr><td>1 pint (pt)</td><td>= 2 cups</td></tr><tr><td>1 quart (qt)</td><td>= 2 pints</td></tr><tr><td>1 gallon (gal)</td><td>= 4 quarts</td></tr></table>
<h3>Customary weight</h3><table>
<tr><td>1 pound (lb)</td><td>= 16 ounces (oz)</td></tr><tr><td>1 ton (T)</td><td>= 2,000 pounds</td></tr></table>
<h3>Time</h3><table><tr><td>1 hour (h)</td><td>= 60 minutes (min)</td></tr><tr><td>1 minute</td><td>= 60 seconds (s)</td></tr></table>
</div><div>
<h3>Metric</h3><table>
<tr><td>1 kilometer (km)</td><td>= 1,000 meters (m)</td></tr><tr><td>1 meter</td><td>= 100 centimeters (cm) = 1,000 millimeters (mm)</td></tr>
<tr><td>1 liter (L)</td><td>= 1,000 milliliters (mL)</td></tr><tr><td>1 kilogram (kg)</td><td>= 1,000 grams (g)</td></tr></table>
<h3>Volume of a rectangular prism</h3><table>
<tr><td>V = l × w × h</td><td>length × width × height</td></tr><tr><td>V = B × h</td><td>B is the area of the base</td></tr><tr><td>Unit</td><td>cubic units (cubic cm, cubic in., …)</td></tr></table>
<h3>Area and perimeter of a rectangle</h3><table>
<tr><td>A = l × w</td><td>square units</td></tr><tr><td>P = 2 × l + 2 × w</td><td>units of length</td></tr></table>
<h3>Powers of ten</h3><table>
<tr><td>10<sup>1</sup> = 10 · 10<sup>2</sup> = 100 · 10<sup>3</sup> = 1,000</td><td>× 10<sup>n</sup>: digits move n places left<br>÷ 10<sup>n</sup>: digits move n places right</td></tr></table>
<h3>Order of operations</h3><table><tr><td>Grouping symbols</td><td>( ) first, then [ ], then {{ }}; then × and ÷ left to right; then + and − left to right</td></tr></table>
</div></div>
<p class="foot">Written for Mr. K’s Classroom to collect the conversions and formulas used in Grade 5. It is not the official MCAS reference sheet; check the Massachusetts DESE site for the sheet students receive on the test.</p></div>'''
    if not standalone:
        return body
    return page('Grade 5 Reference Sheet', '<h1>Grade 5 Reference Sheet</h1><p>Conversions, the volume formula, powers of ten and the order of operations on one page. Keep it with your notes and use it on the practice tests.</p>' + body,
                '5th Grade Math · Reference')


# ------------------------------------------------------------------------------------------------- practice tests
def load():
    banks = {}
    for u in UNITS:
        banks[u] = json.load(open(os.path.join(ROOT, 'math5', u + '.json'), encoding='utf-8'))['questions']
    names = {}
    for u in OUTLINE['units']:
        for i, s in enumerate(u['skills'], 1):
            names[f'{u["id"]}-skill-{i:02d}'] = s[0]
    return banks, names


def domain(q):
    return q['standards'][0].split('.')[1]


def usable(q):
    if re.search(r'-g\d{2}$', q['id']) or q['level'] not in ('cp1', 'honors'):
        return False
    if q['format'] == 'multiple-choice':
        return len(q['options']) == 4 and sum(o['correct'] for o in q['options']) == 1 and len(q['prompt']) >= 30 and not q['prompt'].startswith('Is this answer correct')
    if q['format'] == 'select-all':
        return 4 <= len(q['options']) <= 6 and 1 <= sum(o['correct'] for o in q['options']) < len(q['options'])
    if q['format'] == 'short-answer':
        return len(str(q['answer'])) <= 18 and len(q['prompt']) >= 25 and not q.get('diagram')
    return False


def pick(banks):
    rng = random.Random('grade5-mcas-practice')
    pool_all = [q for u in UNITS for q in banks[u]]
    used = {'a': {}, 'b': {}}
    for doms, _ in SESSIONS:
        for fmt, n in PER_SESSION.items():
            by = {}
            for q in sorted((q for q in pool_all if q['format'] == fmt and domain(q) in doms and usable(q)), key=lambda q: q['id']):
                by.setdefault(q['skillId'], []).append(q)
            for v in by.values():
                rng.shuffle(v)
            skills = sorted(by); rng.shuffle(skills)
            for ex in ('a', 'b'):
                got, i = [], 0
                seen = {q['skillId'] for qs in used[ex].values() for q in qs}
                while len(got) < n:
                    sk = skills[i % len(skills)]; i += 1
                    if by[sk] and (sk not in seen or i > len(skills)):
                        got.append(by[sk].pop()); seen.add(sk)
                    if i > 50 * len(skills):
                        raise SystemExit(f'not enough {fmt} items for {doms}')
                used[ex].setdefault(doms, []).extend(got)
    return used


def key_text(q):
    if q['format'] == 'multiple-choice':
        return '(' + 'ABCD'[[o['correct'] for o in q['options']].index(True)] + ') ' + str(q['answer'])
    if q['format'] == 'select-all':
        return '; '.join(o['text'] for o in q['options'] if o['correct'])
    return str(q['answer'])


def item_html(q, n, key):
    d = (q.get('diagram') or {}).get('spec') or {}
    im = f'<img class="dg" src="../{esc(d["src"])}" alt="{esc(d.get("alt", ""))}">' if d.get('src') else ''
    kind = {'multiple-choice': 'Multiple choice', 'select-all': 'Select all that apply', 'short-answer': 'Short answer'}[q['format']]
    out = f'<li value="{n}"><div class="q">{math(q["prompt"])}<span class="tag">{kind.upper()}</span></div>{im}'
    if q['format'] == 'multiple-choice':
        out += '<div class="choices">' + ''.join(f'<div><b>({"ABCD"[i]})</b>{math(o["text"])}</div>' for i, o in enumerate(q['options'])) + '</div>'
    elif q['format'] == 'select-all':
        out += '<div class="sel">' + ''.join(f'<div><span class="bx"></span>{math(o["text"])}</div>' for o in q['options']) + '</div>'
    elif not key:
        out += '<div>Answer: <span class="blank"></span></div>'
    if key:
        out += f'<div class="ans">Answer: {math(key_text(q))}</div><ol class="steps">' + ''.join(f'<li>{math(s)}</li>' for s in q.get('solutionSteps', [])) + '</ol>'
    return out + '</li>'


def cr_html(c, n, key):
    out = f'<li value="{n}" class="cr"><div class="q"><b>{esc(c["title"])}.</b> {math(c["stem"])}<span class="tag">CONSTRUCTED RESPONSE · 4 POINTS</span></div>'
    for i, (p, a) in enumerate(c['parts']):
        out += f'<div class="part"><div class="q"><b>({"abcd"[i]})</b> {math(p)}</div>' + (f'<div class="ans">{math(a)}</div>' if key else '<div class="work"></div>') + '</div>'
    if key:
        out += '<div class="foot">Scoring: 1 point for each part with a correct answer and supporting work; give the point for a correct method that carries forward an earlier wrong answer.</div>'
    return out + '</li>'


def test_page(ex, items, names, key):
    title = f'Grade 5 Practice Test {ex.upper()}'
    P = [f'<h1>{title}{" — Teacher Key" if key else ""}</h1>']
    if not key:
        P.append('<div class="name"><span>Name</span><span>Date</span><span>Class</span></div>')
    P.append('<table><tr><th>Session</th><th>Questions</th><th>Tools</th><th>Points</th></tr>'
             f'<tr><td>{esc(SESSIONS[0][1][12:])}</td><td>20 (1–20): 12 multiple choice, 3 select all, 4 short answer, 1 constructed response</td><td>No calculator; reference sheet</td><td>23</td></tr>'
             f'<tr><td>{esc(SESSIONS[1][1][12:])}</td><td>20 (21–40): 12 multiple choice, 3 select all, 4 short answer, 1 constructed response</td><td>No calculator; reference sheet</td><td>23</td></tr></table>')
    P.append('<div class="box"><b>How to give it.</b> Give one session per class period (about 60 minutes each; untimed for students who need it). '
             'The question types are like the Grade 5 MCAS: multiple choice (one answer), select all that apply (every correct choice and no wrong ones), short answer, and a four-part constructed response. '
             'Calculators are not used on this practice test. Students may use the Grade 5 reference sheet at the end of this booklet. This is a practice test written for this site, not a released MCAS test.</div>')
    if key:
        P.append('<div class="box"><b>Scoring.</b> Multiple choice, select all and short answer: 1 point each (select all is all or nothing). Constructed response: 4 points, 1 per part. 46 points in all. Use the domain column to plan review.</div>')
        rows, n = '', 0
        for si, (doms, _) in enumerate(SESSIONS):
            for q in items[doms]:
                n += 1
                rows += f'<tr><td>{n}</td><td>{math(key_text(q))}</td><td>{esc(DOMAIN[domain(q)])}</td><td>{esc(names.get(q["skillId"], ""))}</td><td>{esc(", ".join(q["standards"]))}</td></tr>'
            n += 1
            c = CR[ex][si]
            rows += f'<tr><td>{n}</td><td>4-point constructed response</td><td>{esc(DOMAIN[c["domain"]])}</td><td>{esc(c["title"])}</td><td></td></tr>'
        P.append('<h2>Answer key</h2><table><tr><th>#</th><th>Key</th><th>Domain</th><th>Skill</th><th>Standards</th></tr>' + rows + '</table>')
    n = 0
    for si, (doms, head) in enumerate(SESSIONS):
        P.append(f'<div class="section"><h2>{esc(head)}</h2><ol class="mc">')
        for q in items[doms]:
            n += 1
            P.append(item_html(q, n, key))
        n += 1
        P.append(cr_html(CR[ex][si], n, key) + '</ol></div>')
    if not key:
        P.append('<div class="section">' + reference_html(False) + '</div>')
    P.append(f'<p class="foot">Mr. K’s Classroom · {title}{" · Teacher key" if key else ""}. Questions 1–19 and 21–39 come from the 5th Grade Math question banks, whose answers are re-derived by tools/grade5-authoring/verify.py.</p>')
    return page(title + (' · Teacher key' if key else ''), ''.join(P), '5th Grade Math · MCAS review')


# ------------------------------------------------------------------------------------------------- pacing guide
PACE = [  # unit index, days, months
    (0, 14, 'September'), (1, 18, 'late September – October'), (2, 18, 'October – November'), (3, 10, 'November'),
    (4, 18, 'December – early January'), (5, 20, 'January – February'), (6, 10, 'February'), (7, 12, 'March'),
    (8, 8, 'March'), (9, 8, 'late March – April'), (10, 10, 'April')]
REVIEW_DAYS, TEST_DAYS = 8, 4


def pacing_html():
    units = OUTLINE['units']
    rows, day = '', 1
    for i, d, months in PACE:
        u = units[i]
        stds = sorted({s for sk in u['skills'] for s in sk[1]}, key=lambda s: [int(x) if x.isdigit() else x for x in re.split(r'[.]', s)])
        rows += (f'<tr><td>{i + 1}</td><td><b>{esc(u["name"])}</b><br><span class="foot">{esc("; ".join(sk[0] for sk in u["skills"]))}</span></td>'
                 f'<td>{d}</td><td>{day}–{day + d - 1}</td><td>{esc(months)}</td><td>{esc(", ".join(stds))}</td></tr>')
        day += d
    rows += (f'<tr class="rev"><td></td><td><b>MCAS review</b><br><span class="foot">Practice Test A (2 days) and B (2 days) with the reference sheet; reteach from the key’s domain column; Understanding Checks for weak skills.</span></td>'
             f'<td>{REVIEW_DAYS}</td><td>{day}–{day + REVIEW_DAYS - 1}</td><td>late April – May</td><td>all</td></tr>')
    day += REVIEW_DAYS
    rows += f'<tr class="mcas"><td></td><td>Grade 5 MCAS (mathematics sessions)</td><td>{TEST_DAYS}</td><td>{day}–{day + TEST_DAYS - 1}</td><td>spring window</td><td></td></tr>'
    day += TEST_DAYS
    rest = 180 - day + 1
    rows += (f'<tr><td></td><td><b>After the test</b><br><span class="foot">Unit projects (Playground Designer, Miniature City Builder, Plant Growth Investigation), the labs, and a look ahead to Grade 6 ratios and the coordinate plane in four quadrants.</span></td>'
             f'<td>{rest}</td><td>{day}–180</td><td>May – June</td><td></td></tr>')
    assert sum(d for _, d, _ in PACE) + REVIEW_DAYS + TEST_DAYS + rest == 180
    body = (f'<h1>Grade 5 Pacing Guide</h1><p>A 180-day plan that teaches all eleven units, then reviews before the spring MCAS. Days are class periods of about 60 minutes. '
            'The MCAS testing window changes each year: check the Massachusetts DESE schedule and your district calendar, and move the review block to end the week before your test dates.</p>'
            f'<table class="pace"><tr><th>Unit</th><th>Unit and skills</th><th>Days</th><th>Day</th><th>About when</th><th>Standards</th></tr>{rows}</table>'
            '<div class="box"><b>In each unit.</b> Day 1: the unit’s flashcards and cheat sheet. Most days: a lesson from the Lesson Plan Generator at the level that fits each group (Support, Standard or Advanced). '
            'Middle of the unit: the Understanding Check. Last two days: a review game and an assessment from the Assessment Generator. Projects can run alongside, or after the MCAS.</div>'
            '<div class="box"><b>If you fall behind.</b> Units 1–6 (number, operations and fractions) carry most of the Grade 5 MCAS points. Shorten Units 9–11 by a few days rather than rushing fractions, and keep the review block.</div>'
            '<p class="foot">Written for Mr. K’s Classroom. The day counts are a suggestion, not a requirement.</p>')
    return page('Grade 5 Pacing Guide', body, '5th Grade Math · Planning')


# ------------------------------------------------------------------------------------------------- lab worksheets
def grid10(shade_rows=0, shade_cols=0):
    cells = ''.join('<i style="background:%s"></i>' % ('#a78bfa' if r < shade_rows and c < shade_cols else '#fde68a' if r < shade_rows else '#bfdbfe' if c < shade_cols else '#fff')
                    for r in range(10) for c in range(10))
    return f'<span class="grid10">{cells}</span>'


LABS = {
 'decimal-grid-lab': dict(title='Decimal Grid Lab', blurb='Use a hundredths grid to see why tenths times tenths makes hundredths, and why multiplying by a decimal less than 1 makes a smaller product.',
  tasks=[('Shade 0.3 of the grid by coloring 3 columns. How many hundredths is that?', '30 hundredths (0.30)'),
         ('Now color 0.4 of the rows. The part colored twice shows 0.4 × 0.3. How many small squares is it?', '12 squares'),
         ('Write the product 0.4 × 0.3 as a decimal.', '0.12'),
         ('Is 0.4 × 0.3 greater than or less than 0.3? Why?', 'Less: 0.4 of something is less than all of it.'),
         ('Use the grid to find 0.6 × 0.5.', '0.30 = 0.3'),
         ('Find 2 × 0.35 by shading 0.35 on two grids. What is the product?', '0.70 = 0.7'),
         ('Without the grid: which is greater, 0.8 × 0.9 or 0.9?', '0.9, because 0.8 × 0.9 is 0.8 of 0.9.'),
         ('Write a multiplication of two decimals whose product is 0.24.', 'Possible: 0.4 × 0.6, 0.3 × 0.8, 0.2 × 1.2')],
  fig=lambda: grid10(4, 3) + grid10()),
 'scaling-lab': dict(title='Scaling Lab', blurb='Use an area model to multiply fractions, then predict whether a product is greater or less than a factor before you compute.',
  tasks=[('Shade 2/3 of the square with vertical lines and 3/4 with horizontal lines. What fraction is shaded twice?', '6/12 = 1/2'),
         ('Write the multiplication the model shows.', '2/3 × 3/4 = 6/12 = 1/2'),
         ('Is 2/3 × 3/4 greater or less than 3/4? Explain with the model.', 'Less: it is only part (2/3) of the 3/4.'),
         ('Predict without computing: is 5 × 7/8 greater or less than 5?', 'Less, because 7/8 < 1.'),
         ('Predict: is 5 × 1 1/4 greater or less than 5?', 'Greater, because 1 1/4 > 1.'),
         ('Compute 5 × 7/8 and 5 × 1 1/4 to check.', '4 3/8 and 6 1/4'),
         ('A rectangle is 3/5 m by 2/3 m. What is its area?', '6/15 = 2/5 square meter'),
         ('Write a fraction you could multiply 12 by to get a product between 6 and 12.', 'Any fraction between 1/2 and 1, e.g. 3/4 (product 9).')],
  fig=lambda: '<span class="sq"></span><span class="sq"></span>')}


def check_labs():
    assert F(4, 10) * F(3, 10) == F(12, 100) and F(6, 10) * F(5, 10) == F(3, 10) and 2 * F(35, 100) == F(7, 10) and F(8, 10) * F(9, 10) < F(9, 10)
    assert F(2, 3) * F(3, 4) == F(1, 2) and 5 * F(7, 8) == F(35, 8) and 5 * F(5, 4) == F(25, 4) and F(3, 5) * F(2, 3) == F(2, 5) and 6 < 12 * F(3, 4) < 12


def lab_sheet(slug, key):
    L = LABS[slug]
    ol = ''.join(f'<li class="part"><div class="q">{math(t)}</div>' + (f'<div class="ans">{math(a)}</div>' if key else '<div class="work" style="height:.75in"></div>') + '</li>' for t, a in L['tasks'])
    body = (f'<h1>{esc(L["title"])}{" — Teacher Key" if key else ""}</h1>' + ('' if key else '<div class="name"><span>Name</span><span>Date</span><span>Class</span></div>') +
            f'<p>{esc(L["blurb"])} Use the interactive lab, or shade the models below.</p><div>{L["fig"]()}</div><ol>{ol}</ol>'
            '<p class="foot">Mr. K’s Classroom · 5th Grade Math lab.</p>')
    return page(L['title'] + (' · Teacher key' if key else ''), body, '5th Grade Math · Lab')


def main():
    check_cr(); check_labs()
    banks, names = load()
    used = pick(banks)
    ids = {ex: [q['id'] for doms, _ in SESSIONS for q in used[ex][doms]] for ex in used}
    assert not set(ids['a']) & set(ids['b']) and len(ids['a']) == len(ids['b']) == 38
    w = lambda rel, s: open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(s)
    for ex in ('a', 'b'):
        os.makedirs(os.path.join(ROOT, f'math5-practice-test-{ex}'), exist_ok=True)
        for key in (False, True):
            w(f'math5-practice-test-{ex}/{"key" if key else "exam"}.html', test_page(ex, used[ex], names, key))
    os.makedirs(os.path.join(ROOT, 'math5-reference-sheet'), exist_ok=True); w('math5-reference-sheet/index.html', reference_html(True))
    os.makedirs(os.path.join(ROOT, 'math5-pacing-guide'), exist_ok=True); w('math5-pacing-guide/index.html', pacing_html())
    for slug in LABS:
        os.makedirs(os.path.join(ROOT, 'math5-' + slug), exist_ok=True)
        w(f'math5-{slug}/worksheet.html', lab_sheet(slug, False)); w(f'math5-{slug}/teacher-key.html', lab_sheet(slug, True))
    json.dump({'tests': ids, 'cr': CR}, open(os.path.join(HERE, 'out', 'practice-tests.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('practice tests: 38 bank items + 2 constructed response each; reference sheet, pacing guide and 2 lab worksheets written')


if __name__ == '__main__':
    main()
