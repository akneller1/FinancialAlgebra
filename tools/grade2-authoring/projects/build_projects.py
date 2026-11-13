"""Builds every Grade 2 project in the site's existing project format (artifacts/<folder>/), adapted from the Grade 5 builder:
  <slug>-cp2|cp1|honors.pdf/.docx/.pptx   student packets (Remedial / Standard / Advanced)
  <slug>-teacher-guide.pdf/.docx           timing, materials, prerequisites, standards, differentiation, notes, rubric, complete solutions
  <slug>-supports.pdf                      printable supports: data cards / tables and grid paper
  hero.png, index.html                     landing page;   thumbs/<folder>.jpg and thumbs/<folder>.svg
Also writes projects-registry.json (entries keyed math2-<unit> for the Activity generator's project list).
Usage: python3 tools/grade2-authoring/projects/build_projects.py <scratch-dir>  then  node tools/grade2-authoring/print/print.cjs <scratch-dir>/jobs.json"""
import base64, html, json, os, re, subprocess, sys
from docx import Document
from docx.shared import Pt
from pptx import Presentation
from pptx.util import Inches as PI, Pt as PP
from pptx.dml.color import RGBColor as PRGB
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import projects2 as PR
import figs2

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TMP = sys.argv[1] if len(sys.argv) > 1 else "/tmp/g2proj"
os.makedirs(TMP, exist_ok=True)
HERO = {"add-subtract-20": ("groups", {"counts": [8, 5]}), "odd-even-arrays": ("array3", {"rows": 4, "cols": 5}),
        "place-value-1000": ("blocks", {"h": 2, "t": 4, "o": 5}), "count-compare-1000": ("chart", {"start": 291, "rows": 3, "shade": [300]}),
        "add-subtract-100": ("jline", {"lo": 30, "hi": 80, "step": 1, "label_every": 10, "jumps": [[37, 67, "+30"], [67, 75, "+8"]]}),
        "word-problems-100": ("bars", {"rows": [{"parts": [[48, "48"]]}, {"parts": [[29, "29"], [19, "?"]]}]}),
        "add-subtract-1000": ("blocks", {"h": 4, "t": 7, "o": 6}), "measuring-length": ("ruler2", {"length": 12, "unit": "inches", "objects": [{"start": 0, "end": 7, "label": "pencil"}]}),
        "length-number-line": ("jline", {"lo": 0, "hi": 50, "step": 1, "label_every": 10, "jumps": [[0, 24, "+24"], [24, 37, "+13"]]}),
        "time-money": ("clock", {"h": 10, "m": 25}), "graphs-data": ("bargraph1", {"title": "Favorite Fruit", "cats": ["apple", "banana", "grape", "pear"], "vals": [9, 6, 12, 4], "top": 12, "ylabel": "Votes"}),
        "shapes-equal-shares": ("partition", {"shape": "rect", "cuts": "grid", "rows": 3, "cols": 4, "shade": [0, 5, 10]}),
        "cumulative-carnival": ("array3", {"rows": 3, "cols": 5}), "cumulative-market-day": ("money", {"bills": [5, 1], "coins": ["quarter", "dime", "nickel"]})}
CSS = """@page{size:letter;margin:0}*{box-sizing:border-box}body{margin:0;font-family:'DejaVu Sans',Verdana,sans-serif;color:#1E293B}
.pg{width:8.5in;height:11in;padding:.45in .55in .6in;page-break-after:always;position:relative;background:#FFFDF7;overflow:hidden}.pg:last-child{page-break-after:auto}
.ban{background:linear-gradient(90deg,#0f97b5,#1aa37a 60%,#f0a020);color:#fff;border-radius:18px;padding:.14in .22in;display:flex;gap:.16in;align-items:center}.ban h1{margin:0;font-size:22pt}.ban p{margin:.03in 0 0;font-size:10.5pt}
.ban .ic{flex:0 0 1.15in;background:#fff;border-radius:12px;padding:3px}.ban .ic img{width:100%;display:block}.lv{margin-left:auto;background:#FACC15;color:#1E293B;border-radius:999px;padding:3px 11px;font-weight:700;font-size:9.5pt;white-space:nowrap}
.meta{display:flex;gap:.3in;margin:.12in 0;font-size:10.5pt}.meta span{flex:1;border-bottom:1.5px solid #94A3B8;padding-bottom:2px}
.box{border:2.5px solid var(--c,#0f97b5);border-radius:14px;padding:.1in .16in;margin:.1in 0;background:#fff;break-inside:avoid}.box h2{margin:0 0 .05in;font-size:13.5pt;color:var(--c,#0b5f6b)}
.q{margin:.07in 0 .02in;font-size:11.5pt}.q b{color:#0f8f9e}.ln{border-bottom:1.3px solid #CBD5E1;height:.34in}.ans{color:#047857;font-weight:700;font-size:10.5pt;margin:.02in 0 .07in .25in}
.hint{font-size:10pt;color:#7c4a03;background:#FEF3C7;border-radius:8px;padding:2px 8px;margin:.02in 0 .03in .25in;display:inline-block}
table.t{border-collapse:collapse;width:100%;margin:.06in 0;font-size:11pt}table.t td{border:1.4px solid #94A3B8;padding:5px 7px;height:.32in}table.t tr:first-child td{background:#E0F6F8;font-weight:700;color:#0b5f6b}
ul,ol{margin:.03in 0;padding-left:.22in}li{margin:2px 0;font-size:10.8pt}.ft{position:absolute;bottom:.25in;left:0;right:0;text-align:center;font-size:8.5pt;color:#64748B}
.rub td{font-size:9pt;vertical-align:top}.key{background:#DCFCE7;color:#065F46;border-radius:999px;padding:2px 10px;font-weight:700;font-size:9pt}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:.85em;line-height:1;margin:0 1px}.fr span:first-child{border-bottom:1.2px solid currentColor;padding:0 2px}
.grid{width:100%;height:7.4in;background-image:linear-gradient(#94A3B8 1px,transparent 1px),linear-gradient(90deg,#94A3B8 1px,transparent 1px);background-size:.5in .5in;border:1.5px solid #64748B}"""


def fx(s):
    s = html.escape(str(s))
    s = re.sub(r"(?<![\d/])(\d+) (\d+)/(\d+)(?![\d/])", r'\1<span class="fr"><span>\2</span><span>\3</span></span>', s)
    return re.sub(r"(?<![\d>/])(\d+)/(\d+)(?![\d/])", r'<span class="fr"><span>\1</span><span>\2</span></span>', s)


def hero_png(p):
    kind, data = HERO[p["key"]]
    svg = figs2.render(kind, data)
    png = subprocess.run(["rsvg-convert", "-z", "1.4"], input=svg.encode(), capture_output=True, check=True).stdout
    return "data:image/png;base64," + base64.b64encode(png).decode()


def doc(body):
    return f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{body}</body></html>"


def banner(p, sub, lv, art):
    return f'<div class="ban"><div class="ic"><img src="{art}" alt=""></div><div><h1>{html.escape(p["title"])}</h1><p>{html.escape(sub)}</p></div><span class="lv">{html.escape(lv)}</span></div>'


def table_html(rows):
    return '<table class="t">' + "".join("<tr>" + "".join(f"<td>{fx(c)}</td>" for c in r) + "</tr>" for r in rows) + "</table>"


def rubric(p):
    rows = [(t, "Correct and complete; explains how", "Mostly correct", "Partly correct", "Not yet") for t in p["targets"]]
    rows += [("I can explain my thinking with pictures, numbers and words.", "Clear for every part", "Clear for most parts", "Some explanation", "Little explanation"),
             (f"My {p['product'].lower()} is complete and matches my math.", "Complete, neat, accurate", "Complete", "Partly complete", "Not complete")]
    return rows


def rubric_html(p):
    return ('<table class="t rub"><tr><td>Learning target</td><td>4 Exceeds</td><td>3 Meets</td><td>2 Approaching</td><td>1 Beginning</td></tr>' +
            "".join("<tr>" + "".join(f"<td>{fx(c)}</td>" for c in r) + "</tr>" for r in rubric(p)) + "</table>")


def chunk(blocks, per_page_units=8.0):
    """Greedy pagination by estimated height (inches) so parts are not split and pages do not overflow."""
    out, cur, h = [], [], 0.0
    for b, bh in blocks:
        if cur and h + bh > per_page_units:
            out.append("".join(cur)); cur, h = [], 0.0
        cur.append(b); h += bh
    if cur:
        out.append("".join(cur))
    return out


def part_blocks(d, L, teacher=False):
    blocks, n = [], 0
    for i, (title, intro, qs, table) in enumerate(d["tasks"]):
        b = f'<div class="box"><h2>Part {i + 1}: {fx(title)}</h2>' + (f'<div style="font-size:11pt">{fx(intro)}</div>' if intro else "") + (table_html(table) if table else "")
        hgt = 0.75 + (0.35 * len(table) if table else 0) + 0.2 * (len(intro) // 90)
        for q, a, hint in qs:
            n += 1
            b += f'<div class="q"><b>{n}.</b> {fx(q)}</div>'
            if teacher:
                b += f'<div class="ans">{fx(a)}</div>'
                hgt += 0.55
            else:
                if hint:
                    b += f'<div class="hint">Hint: {fx(hint)}</div>'
                lines = 3 if ("Explain" in q or "Draw" in q or "List" in q or "Design" in q or "Your" in q or "Show" in q) else 2
                b += '<div class="ln"></div>' * lines
                hgt += 0.32 + 0.34 * lines + (0.3 if hint else 0) + 0.18 * (len(q) // 80)
        blocks.append((b + "</div>", hgt))
    return blocks


def student_html(p, L, d, art):
    lv = f"Grade 2 · {PR.LNAME[L]}"
    first = (banner(p, "2nd Grade Math Project · " + p["theme"], lv, art) + '<div class="meta"><span>Name:</span><span>Date:</span><span>Class:</span></div>' +
             f'<div class="box" style="--c:#0f97b5"><h2>The Challenge</h2><div style="font-size:11.5pt">{fx(d["scenario"])}</div><div style="margin-top:.05in;font-size:10.5pt"><b>You will make:</b> {html.escape(p["product"])}</div></div>' +
             '<div class="box" style="--c:#1aa37a"><h2>I can…</h2><ul>' + "".join(f"<li>{fx(t)}</li>" for t in p["targets"]) + "</ul></div>" +
             '<div class="box" style="--c:#EA7A12"><h2>Materials</h2><ul>' + "".join(f"<li>{html.escape(m)}</li>" for m in d["materials"]) + '</ul></div>' +
             '<div class="box" style="--c:#DB2777"><h2>Steps</h2><ol style="font-size:11pt">' + "".join(f"<li>Part {i + 1}: {html.escape(t[0])}</li>" for i, t in enumerate(d["tasks"])) +
             "<li>Check your work and share your " + html.escape(p["product"].lower()) + ".</li></ol>" +
             ('<div class="hint" style="margin-left:0">Look for the yellow Hint boxes. They show a first step.</div>' if L == "cp2" else "") + "</div>")
    blocks = part_blocks(d, L)
    blocks.append((f'<div class="box" style="--c:#7C3AED"><h2>Extension Challenge</h2><div class="q">{fx(d["extension"][0])}</div><div class="ln"></div><div class="ln"></div></div>', 1.4))
    blocks.append(('<div class="box" style="--c:#0D9488"><h2>How your project will be scored</h2>' + rubric_html(p) + "</div>", 0.9 + 0.55 * len(rubric(p))))
    pages = [first] + chunk(blocks, 8.6)
    ft = f'<div class="ft">{html.escape(p["title"])} · {PR.LNAME[L]} · Mr. K’s Classroom</div>'
    return doc("".join(f'<div class="pg">{pg}{ft}</div>' for pg in pages))


LEVEL_TEXT = {"cp2": "Remedial: hints for a first step, partly filled tables, sentence frames and fewer open choices; the same learning targets.",
              "cp1": "Standard: the full task set at grade level; students choose their strategies and models.",
              "honors": "Advanced: open design constraints, missing information, error analysis and a written justification; no hints."}


def teacher_html(p, levels, art):
    head = banner(p, "Teacher Guide · Solutions · Rubric", "Grade 2 · All levels", art)
    over = (f'<div class="box" style="--c:#0f97b5"><h2>Overview</h2><div style="font-size:11pt">{fx(p["description"])}</div>'
            f'<div style="margin-top:.05in;font-size:10.5pt"><b>Time:</b> {p["days"]} class periods · <b>Product:</b> {html.escape(p["product"])}</div>'
            f'<div style="font-size:10.5pt"><b>Standards:</b> {", ".join(p["standards"])}</div>'
            f'<div style="font-size:10.5pt"><b>Prerequisite skills:</b> {"; ".join(html.escape(x) for x in p["prereqs"])}</div></div>'
            '<div class="box" style="--c:#1aa37a"><h2>Learning targets</h2><ul>' + "".join(f"<li>{fx(t)}</li>" for t in p["targets"]) + "</ul></div>"
            '<div class="box" style="--c:#EA7A12"><h2>Timing and materials</h2><ul>' + "".join(f"<li>{html.escape(t)}</li>" for t in p["timing"]) + "</ul><b>Materials:</b> " +
            "; ".join(html.escape(m) for m in p["materials"]) + ". No accounts, paid products or student personal information are needed.</div>")
    pg2 = ('<div class="box" style="--c:#DB2777"><h2>The three versions</h2><ul>' + "".join(f"<li>{html.escape(LEVEL_TEXT[L])}</li>" for L in PR.LV) +
           "</ul>All versions use the same context and learning targets, so groups can share and compare work.</div>"
           '<div class="box" style="--c:#7C3AED"><h2>Implementation notes</h2><ul>' + "".join(f"<li>{html.escape(x)}</li>" for x in p["notes"]) +
           "<li>Before Part 1, read the challenge aloud and ask students to restate the goal.</li><li>Close with a gallery walk: each group explains one strategy.</li></ul></div>"
           '<div class="box" style="--c:#0D9488"><h2>Rubric</h2>' + rubric_html(p) + '</div>')
    pages = [head + over, head + pg2]
    for L in PR.LV:
        d = levels[L]
        blocks = [(f'<div class="box"><h2>Solutions · {PR.LNAME[L]} <span class="key">KEY</span></h2></div>', 0.6)] + part_blocks(d, L, teacher=True)
        blocks.append((f'<div class="box"><h2>Extension</h2><div class="q">{fx(d["extension"][0])}</div><div class="ans">{fx(d["extension"][1])}</div></div>', 1.2))
        pages += [head + x for x in chunk(blocks, 7.4)]
    ft = f'<div class="ft">{html.escape(p["title"])} · Teacher Guide · Mr. K’s Classroom</div>'
    return doc("".join(f'<div class="pg">{pg}{ft}</div>' for pg in pages))


def supports_html(p, levels, art):
    head = banner(p, "Printable supports", "Grade 2", art)
    tables = []
    for L in PR.LV:
        for title, intro, qs, table in levels[L]["tasks"]:
            if table:
                tables.append((f'<div class="box"><h2>{PR.LNAME[L]} · {fx(title)}</h2>{table_html(table)}</div>', len(table) + 2))
    if not tables:
        tables = [('<div class="box"><h2>Recording sheet</h2>' + table_html([["Part", "My work", "My answer"]] + [[str(i + 1), "", ""] for i in range(6)]) + "</div>", 9)]
    pages, cur, rows = [], "", 0
    for h, n in tables:          # about 24 table rows fit under the banner on one Letter page
        if cur and rows + n > 24:
            pages.append(cur); cur, rows = "", 0
        cur += h; rows += n
    pages.append(cur)
    grid = head + '<div class="box"><h2>Grid paper (each square = 1 unit)</h2><div class="grid"></div></div>'
    ft = f'<div class="ft">{html.escape(p["title"])} · Supports · Mr. K’s Classroom</div>'
    return doc("".join(f'<div class="pg">{head}{pg}{ft}</div>' for pg in pages) + f'<div class="pg">{grid}{ft}</div>')


def write_docx(path, p, L, d, teacher=False, levels=None):
    D = Document()
    st = D.styles["Normal"]; st.font.name = "Verdana"; st.font.size = Pt(11)
    D.add_heading(p["title"] + (" — Teacher Guide" if teacher else f" — {PR.LNAME[L]}"), 0)
    if not teacher:
        D.add_paragraph("Name: ____________________   Date: __________   Class: ________")
        D.add_heading("The Challenge", 1); D.add_paragraph(d["scenario"])
        D.add_heading("I can…", 1)
        for t in p["targets"]:
            D.add_paragraph(t, style="List Bullet")
        n = 0
        for i, (title, intro, qs, table) in enumerate(d["tasks"]):
            D.add_heading(f"Part {i + 1}: {title}", 1)
            if intro:
                D.add_paragraph(intro)
            if table:
                t = D.add_table(rows=len(table), cols=len(table[0])); t.style = "Table Grid"
                for r, row in enumerate(table):
                    for c, cell in enumerate(row):
                        t.cell(r, c).text = cell
            for q, a, hint in qs:
                n += 1
                D.add_paragraph(f"{n}. {q}")
                if hint:
                    D.add_paragraph(f"Hint: {hint}")
                D.add_paragraph("_" * 70); D.add_paragraph("_" * 70)
        D.add_heading("Extension Challenge", 1); D.add_paragraph(d["extension"][0]); D.add_paragraph("_" * 70)
    else:
        D.add_paragraph(p["description"])
        D.add_paragraph(f"Time: {p['days']} class periods. Standards: {', '.join(p['standards'])}. Prerequisites: {'; '.join(p['prereqs'])}.")
        D.add_heading("Timing", 1)
        for t in p["timing"]:
            D.add_paragraph(t, style="List Bullet")
        D.add_heading("Materials", 1); D.add_paragraph("; ".join(p["materials"]))
        D.add_heading("The three versions", 1)
        for LL in PR.LV:
            D.add_paragraph(LEVEL_TEXT[LL], style="List Bullet")
        D.add_heading("Implementation notes", 1)
        for x in p["notes"]:
            D.add_paragraph(x, style="List Bullet")
        for LL in PR.LV:
            dd = levels[LL]; D.add_heading(f"Solutions — {PR.LNAME[LL]}", 1); n = 0
            for i, (title, intro, qs, table) in enumerate(dd["tasks"]):
                D.add_paragraph(f"Part {i + 1}: {title}").runs[0].bold = True
                for q, a, hint in qs:
                    n += 1
                    D.add_paragraph(f"{n}. {q}  →  {a}")
            D.add_paragraph(f"Extension → {dd['extension'][1]}")
    D.add_heading("Rubric", 1)
    rows = rubric(p)
    t = D.add_table(rows=len(rows) + 1, cols=5); t.style = "Table Grid"
    for c, h in enumerate(["Learning target", "4 Exceeds", "3 Meets", "2 Approaching", "1 Beginning"]):
        t.cell(0, c).text = h
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            t.cell(r + 1, c).text = cell
    D.save(path)


def write_pptx(path, p, L, d):
    prs = Presentation(); prs.slide_width, prs.slide_height = PI(13.333), PI(7.5)

    def slide(title, lines, color="0F97B5"):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        bar = s.shapes.add_shape(1, 0, 0, prs.slide_width, PI(1.2)); bar.fill.solid(); bar.fill.fore_color.rgb = PRGB.from_string(color); bar.line.fill.background()
        tb = bar.text_frame; tb.text = title; tb.paragraphs[0].runs[0].font.size = PP(36); tb.paragraphs[0].runs[0].font.bold = True; tb.paragraphs[0].runs[0].font.color.rgb = PRGB(255, 255, 255)
        box = s.shapes.add_textbox(PI(0.6), PI(1.5), PI(12.1), PI(5.6)); tf = box.text_frame; tf.word_wrap = True
        for i, ln in enumerate(lines):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); para.text = ln; para.font.size = PP(24 if len(lines) < 7 else 20); para.space_after = PP(8)
    slide(p["title"], [p["tagline"], f"2nd Grade Math · {PR.LNAME[L]}", "You will make: " + p["product"]], "1AA37A")
    slide("The Challenge", [d["scenario"]])
    slide("I can…", ["• " + t for t in p["targets"]], "EA7A12")
    n = 0
    for i, (title, intro, qs, table) in enumerate(d["tasks"]):
        lines = ([intro] if intro else [])
        for q, a, hint in qs:
            n += 1; lines.append(f"{n}. {q}" + (f"  (Hint: {hint})" if hint else ""))
        slide(f"Part {i + 1}: {title}", lines, ["0F97B5", "EA7A12", "DB2777", "0D9488", "7C3AED"][i % 5])
    slide("Extension Challenge", [d["extension"][0]], "7C3AED")
    slide("How you will be scored", [f"{r[0]} (4 = {r[1]})" for r in rubric(p)], "0D9488")
    prs.save(path)


def landing(p, levels_desc):
    lv = "".join(f'<div class="card"><h2 style="background:{c}">{PR.LNAME[L]}</h2><p>{desc}</p><div class="btns"><a class="btn" href="{p["slug"]}-{L}.pdf">PDF</a><a class="btn ghost" href="{p["slug"]}-{L}.docx" download>Word</a><a class="btn ghost" href="{p["slug"]}-{L}.pptx" download>PowerPoint</a></div></div>'
                 for L, c, desc in [("cp2", "#1aa37a", "Hints, partly filled tables and sentence frames."), ("cp1", "#0f97b5", "The full project at grade level."), ("honors", "#7C3AED", "Open design, error analysis and justification.")])
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(p['title'])} · 2nd Grade Math Project</title><meta name="description" content="{html.escape(p['description'])}"><meta name="robots" content="noindex">
<style>body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:#FFFDF7;color:#1d2433}}.wrap{{max-width:980px;margin:0 auto;padding:24px 16px 48px}}
.hero{{display:grid;grid-template-columns:1.1fr 1fr;gap:22px;align-items:center;background:linear-gradient(90deg,#0f97b5,#1aa37a);color:#fff;border-radius:16px;padding:22px;border-bottom:6px solid #f0a020}}
.hero img{{width:100%;border-radius:10px;display:block;background:#fff}}.kicker{{font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;color:#e0f6f8;font-weight:700}}h1{{margin:.25em 0 .2em;font-size:2rem}}.tag{{color:#f1fbfb;font-size:1.05rem;margin:0}}
.meta{{margin-top:12px;display:flex;gap:8px;flex-wrap:wrap}}.pill{{background:rgba(255,255,255,.18);padding:4px 10px;border-radius:999px;font-size:.85rem}}p.desc{{font-size:1.02rem;line-height:1.5;margin:20px 2px}}
.levels{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.card{{background:#fff;border-radius:14px;box-shadow:0 1px 4px rgba(0,0,0,.08);overflow:hidden;display:flex;flex-direction:column}}.card h2{{margin:0;color:#fff;font-size:1.25rem;padding:12px 16px}}.card p{{margin:12px 16px;font-size:.92rem;line-height:1.4;flex:1}}
.btns{{display:flex;flex-direction:column;gap:8px;padding:0 16px 16px}}.btn{{display:block;text-align:center;text-decoration:none;border-radius:9px;padding:9px 10px;font-weight:700;background:#0f8f9e;color:#fff}}.btn.ghost{{background:#fff;color:#0f8f9e;border:2px solid #0f8f9e}}
.teacher{{margin-top:18px;background:#fff;border-radius:14px;padding:16px;box-shadow:0 1px 4px rgba(0,0,0,.08)}}@media(max-width:760px){{.hero,.levels{{grid-template-columns:1fr}}}}a.back{{color:#0f8f9e;font-weight:700}}</style></head><body><div class="wrap">
<p><a class="back" href="../../index.html#grade2">← 2nd Grade Math</a></p><div class="hero"><div><div class="kicker">2nd Grade Math Project · {html.escape(p['theme'])}</div><h1>{html.escape(p['title'])}</h1><p class="tag">{html.escape(p['tagline'])}</p>
<div class="meta"><span class="pill">{p['days']} class periods</span><span class="pill">Product: {html.escape(p['product'])}</span><span class="pill">{', '.join(p['standards'][:6])}{'…' if len(p['standards']) > 6 else ''}</span></div></div><img src="hero.png" alt="{html.escape(p['title'])} illustration"></div>
<p class="desc">{html.escape(p['description'])}</p><div class="levels">{lv}</div>
<div class="teacher"><b>Teacher guide, solutions and rubric:</b> <a href="{p['slug']}-teacher-guide.pdf">PDF</a> · <a href="{p['slug']}-teacher-guide.docx" download>Word</a>. <b>Printable supports:</b> <a href="{p['slug']}-supports.pdf">PDF</a>.</div></div></body></html>"""


def hero_html(p, art):
    return doc(f'<div style="width:800px;height:500px;background:linear-gradient(135deg,#E0F6F8,#FEF3C7);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;font-family:DejaVu Sans">'
               f'<div style="width:380px;background:#fff;border-radius:24px;padding:12px;box-shadow:0 6px 0 #9fdde3"><img src="{art}" style="width:100%;max-height:230px;object-fit:contain"></div>'
               f'<div style="font-size:40px;font-weight:800;color:#0b5f6b;text-align:center">{html.escape(p["title"])}</div>'
               f'<div style="font-size:20px;color:#7c4a03">{html.escape(p["theme"])} · 2nd Grade Math{" · Cumulative" if p["cumulative"] else ""}</div></div>').replace(".pg{", ".x{")


def main():
    jobs, registry = [], {}
    for key, p in PR.P.items():
        folder = os.path.join(ROOT, "artifacts", p["folder"]); os.makedirs(folder, exist_ok=True)
        art = hero_png(p)
        levels = {L: p["build"](L) for L in PR.LV}
        for L in PR.LV:
            f = os.path.join(TMP, f"{p['slug']}-{L}.html"); open(f, "w", encoding="utf-8").write(student_html(p, L, levels[L], art))
            jobs.append({"html": f, "pdf": os.path.join(folder, f"{p['slug']}-{L}.pdf")})
            write_docx(os.path.join(folder, f"{p['slug']}-{L}.docx"), p, L, levels[L])
            write_pptx(os.path.join(folder, f"{p['slug']}-{L}.pptx"), p, L, levels[L])
        f = os.path.join(TMP, f"{p['slug']}-teacher.html"); open(f, "w", encoding="utf-8").write(teacher_html(p, levels, art))
        jobs.append({"html": f, "pdf": os.path.join(folder, f"{p['slug']}-teacher-guide.pdf")})
        f = os.path.join(TMP, f"{p['slug']}-supports.html"); open(f, "w", encoding="utf-8").write(supports_html(p, levels, art))
        jobs.append({"html": f, "pdf": os.path.join(folder, f"{p['slug']}-supports.pdf")})
        write_docx(os.path.join(folder, f"{p['slug']}-teacher-guide.docx"), p, "cp1", levels["cp1"], teacher=True, levels=levels)
        h = os.path.join(TMP, f"{p['slug']}-hero.html"); open(h, "w", encoding="utf-8").write(hero_html(p, art))
        jobs.append({"url": "file://" + h, "png": os.path.join(folder, "hero.png"), "w": 800, "h": 500, "outW": 800})
        jobs.append({"url": "file://" + h, "jpg": os.path.join(ROOT, "thumbs", p["folder"] + ".jpg"), "w": 800, "h": 500, "outW": 720})
        open(os.path.join(folder, "index.html"), "w", encoding="utf-8").write(landing(p, None))
        reg_unit = p["units"][-1]
        registry.setdefault("math2-" + reg_unit, []).append({k: p[k] for k in ("folder", "slug", "title", "tagline", "description", "theme", "product")} |
                                                           {"units": p["units"], "standards": p["standards"], "cumulative": p["cumulative"]})
    json.dump(jobs, open(os.path.join(TMP, "jobs.json"), "w"))
    json.dump(registry, open(os.path.join(HERE, "projects-registry.json"), "w"), indent=2, ensure_ascii=False)
    print(len(PR.P), "projects;", len(jobs), "print jobs →", os.path.join(TMP, "jobs.json"))


def svg_thumbs():
    """thumbs/<folder>.svg (the unit-card thumbnail format the Grade 4 assembler links) wrapping the JPG thumbnail."""
    for key, p in PR.P.items():
        jpg = os.path.join(ROOT, "thumbs", p["folder"] + ".jpg")
        b64 = base64.b64encode(open(jpg, "rb").read()).decode()
        open(os.path.join(ROOT, "thumbs", p["folder"] + ".svg"), "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 720 450" role="img" aria-label="{html.escape(p["title"])}">'
            f'<image width="720" height="450" href="data:image/jpeg;base64,{b64}"/></svg>')


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "--svg-thumbs":
        svg_thumbs()
    else:
        main()
