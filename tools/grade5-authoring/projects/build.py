"""Builds every Grade 5 project in the site's existing project format (artifacts/<folder>/):
  <slug>-cp2|cp1|honors.pdf/.docx/.pptx, <slug>-teacher-guide.pdf/.docx, hero.png, index.html, and thumbs/<folder>.jpg.
Also writes projects-registry.json (entries for worksheet-generator/menu/printables-projects.js).
Usage: python3 tools/math5/projects/build.py <scratch-dir>   then   node tools/math5/print/print.cjs <scratch-dir>/jobs.json
"""
import html, json, os, re, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from pptx import Presentation
from pptx.util import Inches as PI, Pt as PP
from pptx.dml.color import RGBColor as PRGB
sys.path.insert(0, os.path.dirname(__file__))
import projects as PR

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
TMP = sys.argv[1] if len(sys.argv) > 1 else "/tmp/g5proj"
os.makedirs(TMP, exist_ok=True)
FIGS = "file://" + os.path.join(ROOT, "worksheet-generator", "grade5", "g5-figs.js")
RUBRIC = [("Math accuracy", "All answers correct", "Most answers correct", "Some answers correct", "Few answers correct"),
          ("Shows work", "Clear work for every step", "Work for most steps", "Some work shown", "Little work shown"),
          ("Explains thinking", "Clear, complete explanations", "Mostly clear explanations", "Some explanation", "Little explanation"),
          ("Final product", "Complete, neat and creative", "Complete and neat", "Partly complete", "Not complete")]
CSS = """@page{size:letter;margin:0}*{box-sizing:border-box}body{margin:0;font-family:'DejaVu Sans',Verdana,sans-serif;color:#1E293B}
.pg{width:8.5in;min-height:11in;padding:.45in .55in .6in;page-break-after:always;position:relative;background:#FFFDF7}.pg:last-child{page-break-after:auto}
.ban{background:linear-gradient(90deg,#2563EB,#7C3AED);color:#fff;border-radius:18px;padding:.14in .22in;display:flex;gap:.16in;align-items:center}.ban h1{margin:0;font-size:22pt}.ban p{margin:.03in 0 0;font-size:10.5pt}
.ban .ic{flex:0 0 1.05in;background:#fff;border-radius:12px;padding:3px}.lv{margin-left:auto;background:#FACC15;color:#1E293B;border-radius:999px;padding:3px 11px;font-weight:700;font-size:9.5pt;white-space:nowrap}
.meta{display:flex;gap:.3in;margin:.12in 0;font-size:10.5pt}.meta span{flex:1;border-bottom:1.5px solid #94A3B8;padding-bottom:2px}
.box{border:2.5px solid var(--c,#7C3AED);border-radius:14px;padding:.1in .16in;margin:.1in 0;background:#fff;break-inside:avoid}.box h2{margin:0 0 .05in;font-size:13.5pt;color:var(--c,#7C3AED)}
.q{margin:.07in 0 .02in;font-size:11pt}.q b{color:#2563EB}.ln{border-bottom:1.3px solid #CBD5E1;height:.32in}.ans{color:#047857;font-weight:700;font-size:10.5pt;margin:.02in 0 .07in .25in}
table.t{border-collapse:collapse;width:100%;margin:.06in 0;font-size:10.5pt}table.t td{border:1.4px solid #94A3B8;padding:5px 7px;height:.3in}table.t tr:first-child td{background:#EEF2FF;font-weight:700;color:#4C1D95}
ul{margin:.03in 0;padding-left:.22in}li{margin:2px 0;font-size:10.8pt}.ft{position:absolute;bottom:.25in;left:0;right:0;text-align:center;font-size:8.5pt;color:#64748B}
.rub td{font-size:9pt;vertical-align:top}.key{background:#DCFCE7;color:#065F46;border-radius:999px;padding:2px 10px;font-weight:700;font-size:9pt}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:.85em;line-height:1;margin:0 1px}.fr span:first-child{border-bottom:1.2px solid currentColor;padding:0 2px}"""


def fx(s):
    s = html.escape(str(s))
    s = re.sub(r"(\d+) (\d+)/(\d+)", r'\1<span class="fr"><span>\2</span><span>\3</span></span>', s)
    return re.sub(r"(?<![\d>])(\d+)/(\d+)(?!\d)", r'<span class="fr"><span>\1</span><span>\2</span></span>', s)


def icon_div(unit):
    return f'<div class="ic" data-unit="{unit}"></div>'


SCRIPT = f'<script src="{FIGS}"></script><script>document.querySelectorAll(".ic").forEach(function(d){{d.innerHTML=G5FIGS.unitIcon(d.dataset.unit)}})</script>'


def doc(body):
    return f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{body}{SCRIPT}</body></html>"


def banner(p, sub, lv):
    return f'<div class="ban">{icon_div(p["unit"])}<div><h1>{html.escape(p["title"])}</h1><p>{html.escape(sub)}</p></div><span class="lv">{html.escape(lv)}</span></div>'


def table_html(rows):
    return '<table class="t">' + "".join("<tr>" + "".join(f"<td>{fx(c)}</td>" for c in r) + "</tr>" for r in rows) + "</table>"


def rubric_html():
    return '<table class="t rub"><tr><td>Category</td><td>4 Excellent</td><td>3 Good</td><td>2 Developing</td><td>1 Beginning</td></tr>' + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in RUBRIC) + "</table>"


def student_html(p, L, d):
    lv = f"Grade 5 · {PR.LNAME[L]}"
    first = (banner(p, "5th Grade Math Project · " + p["theme"], lv) + '<div class="meta"><span>Name:</span><span>Date:</span><span>Class:</span></div>' +
             f'<div class="box" style="--c:#2563EB"><h2>The Challenge</h2><div style="font-size:11.2pt">{fx(d["scenario"])}</div><div style="margin-top:.05in;font-size:10.5pt"><b>You will make:</b> {html.escape(p["product"])}</div></div>' +
             '<div class="box" style="--c:#059669"><h2>What you will learn</h2><ul>' + "".join(f"<li>{fx(o)}</li>" for o in d["objectives"]) + "</ul></div>" +
             '<div class="box" style="--c:#EA7A12"><h2>Materials</h2><ul>' + "".join(f"<li>{html.escape(m)}</li>" for m in d["materials"]) + '</ul></div>' +
             '<div class="box" style="--c:#DB2777"><h2>How to do it</h2><ol style="margin:.02in 0;padding-left:.25in;font-size:10.8pt">' + "".join(f"<li>Part {i + 1}: {html.escape(t[0])}</li>" for i, t in enumerate(d["tasks"])) + "<li>Check your work and share your " + html.escape(p["product"].lower()) + ".</li></ol></div>")
    parts, n = [], 0
    for i, (title, intro, qs, table) in enumerate(d["tasks"]):
        b = f'<div class="box"><h2>Part {i + 1}: {html.escape(title)}</h2>' + (f'<div style="font-size:10.8pt">{fx(intro)}</div>' if intro else "") + (table_html(table) if table else "")
        for q, a in qs:
            n += 1
            b += f'<div class="q"><b>{n}.</b> {fx(q)}</div><div class="ln"></div><div class="ln"></div>'
        parts.append(b + "</div>")
    ext = f'<div class="box" style="--c:#7C3AED"><h2>⭐ Extension Challenge</h2><div class="q">{fx(d["extension"][0])}</div><div class="ln"></div><div class="ln"></div></div>'
    rub = '<div class="box" style="--c:#0D9488"><h2>How your project will be scored</h2>' + rubric_html() + "</div>"
    pages = [first] + chunk(parts + [ext, rub], 2)
    ft = f'<div class="ft">{html.escape(p["title"])} · {PR.LNAME[L]} · Mr. K’s Classroom</div>'
    return doc("".join(f'<div class="pg">{pg}{ft}</div>' for pg in pages))


def chunk(blocks, per):
    out, cur = [], []
    for b in blocks:
        cur.append(b)
        if len(cur) == per:
            out.append("".join(cur)); cur = []
    if cur:
        out.append("".join(cur))
    return out


def teacher_html(p, levels):
    head = banner(p, "Teacher Guide & Answer Keys", "Grade 5 · All levels")
    over = (f'<div class="box" style="--c:#2563EB"><h2>Overview</h2><div style="font-size:11pt">{fx(p["description"])}</div><div style="margin-top:.05in;font-size:10.5pt"><b>Time:</b> {p["days"]} class periods · <b>Product:</b> {html.escape(p["product"])} · <b>Standards:</b> {", ".join(p["standards"])}</div></div>' +
            '<div class="box" style="--c:#059669"><h2>Suggested pacing</h2><ul><li>Day 1: Introduce the challenge, read the scenario together, and work Parts 1–2 in pairs.</li><li>Day 2: Finish the remaining parts and create the final product.</li>' + ('<li>Day 3: Share products in a gallery walk and reflect.</li>' if p["days"] >= 3 else '<li>Wrap-up: Share products and reflect on strategies.</li>') + '</ul></div>' +
            '<div class="box" style="--c:#EA7A12"><h2>Levels</h2><ul><li><b>Remedial:</b> smaller numbers, fewer steps, more structure.</li><li><b>Standard:</b> grade-level numbers and the full set of tasks.</li><li><b>Advanced:</b> harder numbers, extra reasoning and multi-step questions.</li></ul>All three levels practice the same learning goals, so the class can share and compare work.</div>' +
            '<div class="box" style="--c:#0D9488"><h2>Rubric</h2>' + rubric_html() + '</div>')
    pages = [head + over]
    for L in PR.LV:
        d = levels[L]
        b, n = f'<div class="box"><h2>Answer key · {PR.LNAME[L]} <span class="key">KEY</span></h2>', 0
        for i, (title, intro, qs, table) in enumerate(d["tasks"]):
            b += f'<div style="font-weight:700;color:#4C1D95;margin-top:.06in">Part {i + 1}: {html.escape(title)}</div>'
            for q, a in qs:
                n += 1
                b += f'<div class="q"><b>{n}.</b> {fx(q)}</div><div class="ans">{fx(a)}</div>'
        b += f'<div style="font-weight:700;color:#4C1D95;margin-top:.06in">Extension</div><div class="ans">{fx(d["extension"][1])}</div></div>'
        pages.append(head + b)
    pages.append(head + '<div class="box" style="--c:#DB2777"><h2>Worked teacher example (Standard, Part 1)</h2>' +
                 "".join(f'<div class="q">{fx(q)}</div><div class="ans">{fx(a)}</div>' for q, a in levels["cp1"]["tasks"][0][2]) +
                 '<div style="font-size:10.5pt;margin-top:.06in">Model the first part aloud: read the situation, name the operation, estimate, solve, and check. Then let partners try Part 2.</div></div>' +
                 '<div class="box" style="--c:#7C3AED"><h2>Look for</h2><ul><li>Students use correct notation and units in every answer.</li><li>Students explain why an answer is reasonable (estimates, benchmarks, pictures).</li><li>Final products show the math clearly, not just the answers.</li></ul></div>')
    ft = f'<div class="ft">{html.escape(p["title"])} · Teacher Guide · Mr. K’s Classroom</div>'
    return doc("".join(f'<div class="pg">{pg}{ft}</div>' for pg in pages))


def write_docx(path, p, L, d, teacher=False, levels=None):
    D = Document()
    st = D.styles["Normal"]; st.font.name = "Verdana"; st.font.size = Pt(11)
    D.add_heading(p["title"] + (" — Teacher Guide" if teacher else f" — {PR.LNAME[L]}"), 0)
    if not teacher:
        D.add_paragraph("Name: ____________________   Date: __________   Class: ________")
        D.add_heading("The Challenge", 1); D.add_paragraph(d["scenario"])
        D.add_heading("What you will learn", 1)
        for o in d["objectives"]:
            D.add_paragraph(o, style="List Bullet")
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
            for q, a in qs:
                n += 1
                D.add_paragraph(f"{n}. {q}"); D.add_paragraph("_" * 70)
        D.add_heading("Extension Challenge", 1); D.add_paragraph(d["extension"][0]); D.add_paragraph("_" * 70)
    else:
        D.add_paragraph(p["description"]); D.add_paragraph(f"Time: {p['days']} class periods. Standards: {', '.join(p['standards'])}.")
        for LL in PR.LV:
            dd = levels[LL]; D.add_heading(f"Answer key — {PR.LNAME[LL]}", 1); n = 0
            for i, (title, intro, qs, table) in enumerate(dd["tasks"]):
                D.add_paragraph(f"Part {i + 1}: {title}").runs[0].bold = True
                for q, a in qs:
                    n += 1
                    D.add_paragraph(f"{n}. {q}  →  {a}")
            D.add_paragraph(f"Extension → {dd['extension'][1]}")
    D.add_heading("Rubric", 1)
    t = D.add_table(rows=len(RUBRIC) + 1, cols=5); t.style = "Table Grid"
    for c, h in enumerate(["Category", "4 Excellent", "3 Good", "2 Developing", "1 Beginning"]):
        t.cell(0, c).text = h
    for r, row in enumerate(RUBRIC):
        for c, cell in enumerate(row):
            t.cell(r + 1, c).text = cell
    D.save(path)


def write_pptx(path, p, L, d):
    prs = Presentation(); prs.slide_width, prs.slide_height = PI(13.333), PI(7.5)
    def slide(title, lines, color="2563EB"):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        bar = s.shapes.add_shape(1, 0, 0, prs.slide_width, PI(1.2)); bar.fill.solid(); bar.fill.fore_color.rgb = PRGB.from_string(color); bar.line.fill.background()
        tb = bar.text_frame; tb.text = title; tb.paragraphs[0].runs[0].font.size = PP(36); tb.paragraphs[0].runs[0].font.bold = True; tb.paragraphs[0].runs[0].font.color.rgb = PRGB(255, 255, 255)
        box = s.shapes.add_textbox(PI(0.6), PI(1.5), PI(12.1), PI(5.6)); tf = box.text_frame; tf.word_wrap = True
        for i, ln in enumerate(lines):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); para.text = ln; para.font.size = PP(24); para.space_after = PP(10)
    slide(p["title"], [p["tagline"], f"5th Grade Math · {PR.LNAME[L]}", "You will make: " + p["product"]], "7C3AED")
    slide("The Challenge", [d["scenario"]])
    slide("What you will learn", ["• " + o for o in d["objectives"]], "059669")
    n = 0
    for i, (title, intro, qs, table) in enumerate(d["tasks"]):
        lines = ([intro] if intro else [])
        for q, a in qs:
            n += 1; lines.append(f"{n}. {q}")
        slide(f"Part {i + 1}: {title}", lines, ["2563EB", "EA7A12", "DB2777", "0D9488", "7C3AED"][i % 5])
    slide("⭐ Extension Challenge", [d["extension"][0]], "7C3AED")
    slide("How you will be scored", [f"{r[0]}: 4 = {r[1]}" for r in RUBRIC], "0D9488")
    prs.save(path)


def landing(p):
    lv = "".join(f'<div class="card"><h2 style="background:{c}">{PR.LNAME[L]}</h2><p>{desc}</p><div class="btns"><a class="btn" href="{p["slug"]}-{L}.pdf">PDF</a><a class="btn ghost" href="{p["slug"]}-{L}.docx" download>Word</a><a class="btn ghost" href="{p["slug"]}-{L}.pptx" download>PowerPoint</a></div></div>'
                 for L, c, desc in [("cp2", "#059669", "Friendlier numbers and more structure."), ("cp1", "#2563EB", "Grade-level numbers and the full project."), ("honors", "#7C3AED", "Harder numbers and extra reasoning.")])
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(p['title'])} · 5th Grade Math Project</title><meta name="description" content="{html.escape(p['description'])}">
<style>body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:#FFFDF7;color:#1d2433}}.wrap{{max-width:980px;margin:0 auto;padding:24px 18px 48px}}
.hero{{display:grid;grid-template-columns:1.1fr 1fr;gap:22px;align-items:center;background:linear-gradient(90deg,#2563EB,#7C3AED);color:#fff;border-radius:16px;padding:22px;border-bottom:6px solid #FACC15}}
.hero img{{width:100%;border-radius:10px;display:block;background:#fff}}.kicker{{font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;color:#E0E7FF;font-weight:700}}h1{{margin:.25em 0 .2em;font-size:2rem}}.tag{{color:#EEF2FF;font-size:1.05rem;margin:0}}
.meta{{margin-top:12px;display:flex;gap:8px;flex-wrap:wrap}}.pill{{background:rgba(255,255,255,.18);padding:4px 10px;border-radius:999px;font-size:.85rem}}p.desc{{font-size:1.02rem;line-height:1.5;margin:20px 2px}}
.levels{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.card{{background:#fff;border-radius:14px;box-shadow:0 1px 4px rgba(0,0,0,.08);overflow:hidden;display:flex;flex-direction:column}}.card h2{{margin:0;color:#fff;font-size:1.25rem;padding:12px 16px}}.card p{{margin:12px 16px;font-size:.92rem;line-height:1.4;flex:1}}
.btns{{display:flex;flex-direction:column;gap:8px;padding:0 16px 16px}}.btn{{display:block;text-align:center;text-decoration:none;border-radius:9px;padding:9px 10px;font-weight:700;background:#7C3AED;color:#fff}}.btn.ghost{{background:#fff;color:#7C3AED;border:2px solid #7C3AED}}
.teacher{{margin-top:18px;background:#fff;border-radius:14px;padding:16px;box-shadow:0 1px 4px rgba(0,0,0,.08)}}@media(max-width:760px){{.hero,.levels{{grid-template-columns:1fr}}}}a.back{{color:#2563EB;font-weight:700}}</style></head><body><div class="wrap">
<p><a class="back" href="../../index.html#c/math5">← 5th Grade Math</a></p><div class="hero"><div><div class="kicker">5th Grade Math Project · {html.escape(p['theme'])}</div><h1>{html.escape(p['title'])}</h1><p class="tag">{html.escape(p['tagline'])}</p>
<div class="meta"><span class="pill">{p['days']} class periods</span><span class="pill">Product: {html.escape(p['product'])}</span><span class="pill">{', '.join(p['standards'])}</span></div></div><img src="hero.png" alt="{html.escape(p['title'])} illustration"></div>
<p class="desc">{html.escape(p['description'])}</p><div class="levels">{lv}</div>
<div class="teacher"><b>Teacher guide &amp; answer keys:</b> <a href="{p['slug']}-teacher-guide.pdf">PDF</a> · <a href="{p['slug']}-teacher-guide.docx" download>Word</a>. Includes pacing, a worked example, answer keys for all three levels and a rubric.</div></div></body></html>"""


def hero_html(p):
    return doc(f'<div style="width:800px;height:500px;background:linear-gradient(135deg,#EEF2FF,#FEF3C7);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;font-family:DejaVu Sans">'
               f'<div class="ic" data-unit="{p["unit"]}" style="width:330px;background:#fff;border-radius:24px;padding:10px;box-shadow:0 6px 0 #C7D2FE"></div><div style="font-size:42px;font-weight:800;color:#4C1D95">{html.escape(p["title"])}</div>'
               f'<div style="font-size:20px;color:#1E3A8A">{html.escape(p["theme"])} · 5th Grade Math</div></div>').replace(".pg{", ".x{")


def main():
    jobs, registry = [], {}
    for unit, p in PR.P.items():
        folder = os.path.join(ROOT, "artifacts", p["folder"]); os.makedirs(folder, exist_ok=True)
        levels = {L: p["build"](L) for L in PR.LV}
        for L in PR.LV:
            f = os.path.join(TMP, f"{p['slug']}-{L}.html"); open(f, "w", encoding="utf-8").write(student_html(p, L, levels[L]))
            jobs.append({"html": f, "pdf": os.path.join(folder, f"{p['slug']}-{L}.pdf")})
            write_docx(os.path.join(folder, f"{p['slug']}-{L}.docx"), p, L, levels[L])
            write_pptx(os.path.join(folder, f"{p['slug']}-{L}.pptx"), p, L, levels[L])
        f = os.path.join(TMP, f"{p['slug']}-teacher.html"); open(f, "w", encoding="utf-8").write(teacher_html(p, levels))
        jobs.append({"html": f, "pdf": os.path.join(folder, f"{p['slug']}-teacher-guide.pdf")})
        write_docx(os.path.join(folder, f"{p['slug']}-teacher-guide.docx"), p, "cp1", levels["cp1"], teacher=True, levels=levels)
        h = os.path.join(TMP, f"{p['slug']}-hero.html"); open(h, "w", encoding="utf-8").write(hero_html(p))
        jobs.append({"url": "file://" + h, "png": os.path.join(folder, "hero.png"), "w": 800, "h": 500, "outW": 800})
        jobs.append({"url": "file://" + h, "jpg": os.path.join(ROOT, "thumbs", p["folder"] + ".jpg"), "w": 800, "h": 500, "outW": 720})
        open(os.path.join(folder, "index.html"), "w", encoding="utf-8").write(landing(p))
        registry["math5-" + unit] = [{k: p[k] for k in ("folder", "slug", "title", "tagline", "description", "theme", "product")}]
    json.dump(jobs, open(os.path.join(TMP, "jobs.json"), "w"))
    json.dump(registry, open(os.path.join(os.path.dirname(__file__), "projects-registry.json"), "w"), indent=2, ensure_ascii=False)
    print(len(PR.P), "projects;", len(jobs), "print jobs →", os.path.join(TMP, "jobs.json"))


if __name__ == "__main__":
    main()
