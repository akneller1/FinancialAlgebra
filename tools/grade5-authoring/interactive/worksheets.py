"""Explore & Reflect worksheets and teacher keys (2 pages each) for the Grade 5 tools, plus thumbnail jobs.
Usage: python3 tools/math5/interactive/worksheets.py && node tools/math5/print/print.cjs /tmp/…/jobs.json"""
import json, os, sys, html
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
M = json.load(open(os.path.join(os.path.dirname(__file__), "manifest.json")))
TMP = sys.argv[1] if len(sys.argv) > 1 else "/tmp/g5print"
os.makedirs(TMP, exist_ok=True)
CSS = """@page{size:letter;margin:0}*{box-sizing:border-box}body{margin:0;font-family:'DejaVu Sans',Verdana,sans-serif;color:#1E293B}
.pg{width:8.5in;height:11in;padding:.45in .55in;page-break-after:always;position:relative;background:#FFFDF7}.pg:last-child{page-break-after:auto}
.ban{background:linear-gradient(90deg,#2563EB,#7C3AED);color:#fff;border-radius:16px;padding:.12in .2in}.ban h1{margin:0;font-size:20pt}.ban p{margin:.03in 0 0;font-size:10pt}
.meta{display:flex;gap:.3in;margin:.12in 0;font-size:10.5pt}.meta span{flex:1;border-bottom:1.5px solid #94A3B8;padding-bottom:2px}
.box{border:2.5px solid #7C3AED;border-radius:14px;padding:.1in .15in;margin:.1in 0;background:#fff}.box h2{margin:0 0 .05in;font-size:13pt;color:#7C3AED}
.q{margin:.08in 0 .02in;font-size:11.2pt}.q b{color:#2563EB}.ln{border-bottom:1.3px solid #CBD5E1;height:.33in}.ans{color:#047857;font-weight:700;font-size:11pt;margin:.02in 0 .08in .25in}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:.85em;line-height:1;margin:0 1px}.fr span:first-child{border-bottom:1.2px solid currentColor;padding:0 2px}
.ft{position:absolute;bottom:.25in;left:0;right:0;text-align:center;font-size:8.5pt;color:#64748B}.key{background:#DCFCE7;color:#065F46;border-radius:999px;padding:2px 10px;font-weight:700;font-size:9pt;float:right}"""


import re
def fx(s):
    """Escape, then show a/b and w a/b as stacked fractions."""
    s = html.escape(s)
    s = re.sub(r"(\d+) (\d+)/(\d+)", r'\1<span class="fr"><span>\2</span><span>\3</span></span>', s)
    return re.sub(r"(?<![\d>])(\d+)/(\d+)(?!\d)", r'<span class="fr"><span>\1</span><span>\2</span></span>', s)


def page(t, body, key=False):
    return (f'<div class="pg"><div class="ban">{"<span class=key>TEACHER KEY</span>" if key else ""}<h1>{html.escape(t["title"])}</h1><p>5th Grade Math · Interactive Math · Explore &amp; Reflect</p></div>'
            + ('' if key else '<div class="meta"><span>Name:</span><span>Date:</span><span>Class:</span></div>') + body +
            f'<div class="ft">Use with the {html.escape(t["title"])} at mrksclassroom.com · Mr. K’s Classroom</div></div>')


jobs = []
for t in M["tools"]:
    qs = t["worksheet"]
    first, second = qs[:5], qs[5:]
    def block(items, key, start):
        return "".join(f'<div class="q"><b>{start + i + 1}.</b> {fx(q)}</div>' + (f'<div class="ans">{fx(a)}</div>' if key else '<div class="ln"></div><div class="ln"></div>') for i, (q, a) in enumerate(items))
    for key in (False, True):
        p1 = page(t, f'<div class="box"><h2>Get started</h2><div style="font-size:10.5pt">{html.escape(t["description"])} Open the tool and use it to answer each question.</div></div><div class="box"><h2>Explore</h2>{block(first, key, 0)}</div>', key)
        p2 = page(t, f'<div class="box"><h2>Explore more</h2>{block(second[:-1], key, len(first))}</div><div class="box" style="border-color:#059669"><h2 style="color:#059669">Reflect</h2>{block(second[-1:], key, len(qs) - 1)}' +
                  ('' if key else '<div class="ln"></div><div class="ln"></div>') + '</div>' + ('<div class="box" style="border-color:#EA7A12"><h2 style="color:#EA7A12">Teacher notes</h2><div style="font-size:10.5pt">Accept equivalent forms (for example 1/2 = 2/4 = 0.5) and any correct example where several answers are possible. Have students explain using the tool’s picture.</div></div>' if key else ''), key)
        f = os.path.join(TMP, f'{t["slug"]}-{"key" if key else "ws"}.html')
        open(f, "w", encoding="utf-8").write(f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{p1}{p2}</body></html>")
        jobs.append({"html": f, "pdf": os.path.join(ROOT, "artifacts", t["slug"], "teacher-key.pdf" if key else "worksheet.pdf")})
    jobs.append({"url": f"http://localhost:8765/artifacts/{t['slug']}/index.html", "jpg": os.path.join(ROOT, "thumbs", t["slug"] + ".jpg"), "w": 1200, "h": 750, "wait": 500})
json.dump(jobs, open(os.path.join(TMP, "jobs.json"), "w"))
print(len(jobs), "jobs →", os.path.join(TMP, "jobs.json"))
