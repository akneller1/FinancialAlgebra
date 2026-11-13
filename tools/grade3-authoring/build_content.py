"""Build Grade 3 reference content from content_g3.py (adapted from the Grade 5 builder).

Writes:
  worksheet-generator/grade3/flashcards/<unit>.json          concept, vocabulary and visual flashcards (SVG drawn by figs.py)
  tools/grade3-authoring/patches/vocabulary-math3.js        MATH3 vocabulary block (MKVOCAB_BANKS keys math3-<unit>); the release adapter appends it
  worksheet-generator/grade3/worked-examples.json           one worked example per skill + misconception notes (from the verified bank)
  tools/grade3-authoring/staging/teaching-notes.json         native lesson-planner notes (MKPLAN_TEACH.grade3), objectives.json
  scripts/cheat-sheets/content/math3-<unit>.cjs              cheat-sheet content for scripts/cheat-sheets/build.cjs (theme: elementary)
Every example/try-it check is evaluated with Node before anything is written."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from outline import UNITS, COURSE_NAME, skill_records
import figs3 as figs
from content_g3 import V, CARDS, VIS, SHEET


def checks():
    exprs = []
    for u, s in SHEET.items():
        for i, side in enumerate(s["sides"]):
            exprs.append((f"{u} side {i + 1} how", side["how"]["check"]))
            for t in side["tryit"]:
                exprs.append((f"{u} side {i + 1} try: {t[0]}", t[2]))
    js = "const out=[];" + "".join(f"try{{if(!({e}))out.push({json.dumps(w)})}}catch(x){{out.push({json.dumps(w)}+' '+x.message)}};" for w, e in exprs) + "console.log(JSON.stringify(out));"
    bad = json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout)
    if bad:
        print("CHECK FAILED:\n  " + "\n  ".join(bad))
        sys.exit(1)
    return len(exprs)


def tex_fracs(s):
    """'2 1/3' -> ⟨2\\frac{1}{3}⟩ and '3/4' -> ⟨\\frac{3}{4}⟩ for the cheat sheets (KaTeX)."""
    s = re.sub(r"(?<![\d/⟨{])(\d+) (\d+)/(\d+)(?![\d/])", lambda m: f"⟨{m.group(1)}\\frac{{{m.group(2)}}}{{{m.group(3)}}}⟩", s)
    s = re.sub(r"(?<![\d/⟨{\w])(\d+)/(\d+)(?![\d/])", lambda m: f"⟨\\frac{{{m.group(1)}}}{{{m.group(2)}}}⟩", s)
    return s


ICON = {  # small inline icons for section headers (drawn, no emoji fonts needed)
    "big": '<svg width="14" height="14" viewBox="0 0 24 24" style="vertical-align:-2px;margin-right:4px"><circle cx="12" cy="10" r="7" fill="#fff"/><rect x="9" y="17" width="6" height="4" rx="1" fill="#fff"/></svg>',
    "vocab": '<svg width="14" height="14" viewBox="0 0 24 24" style="vertical-align:-2px;margin-right:4px"><rect x="3" y="4" width="18" height="16" rx="2" fill="#fff"/><path d="M12 4v16" stroke="currentColor" stroke-width="2"/></svg>',
    "how": '<svg width="14" height="14" viewBox="0 0 24 24" style="vertical-align:-2px;margin-right:4px"><circle cx="12" cy="12" r="9" fill="#fff"/><path d="M8 12l3 3 5-6" stroke="currentColor" stroke-width="2.5" fill="none"/></svg>',
    "fig": '<svg width="14" height="14" viewBox="0 0 24 24" style="vertical-align:-2px;margin-right:4px"><rect x="3" y="3" width="8" height="8" fill="#fff"/><rect x="13" y="3" width="8" height="8" fill="#fff" opacity=".7"/><rect x="3" y="13" width="8" height="8" fill="#fff" opacity=".7"/><rect x="13" y="13" width="8" height="8" fill="#fff"/></svg>',
    "remember": '<svg width="14" height="14" viewBox="0 0 24 24" style="vertical-align:-2px;margin-right:4px"><path d="M12 2l3 6.5 7 1-5 4.8 1.2 7L12 18l-6.2 3.3L7 14.3 2 9.5l7-1z" fill="#fff"/></svg>',
    "try": '<svg width="14" height="14" viewBox="0 0 24 24" style="vertical-align:-2px;margin-right:4px"><path d="M4 20l4-1L19 8l-3-3L5 16z" fill="#fff"/></svg>',
}


def vrow(unit, term):
    for t, d, e in V[unit]:
        if t == term:
            return [t, tex_fracs(d), tex_fracs(e)]
    raise KeyError((unit, term))


def side_sections(unit, side, k):
    cols = [["orange", "blue", "green", "purple", "pink", "teal"], ["teal", "purple", "orange", "blue", "green", "pink"]][k]
    out = [dict(title=ICON["big"] + "Big Idea", kind="html", color=cols[0],
                html=f'<div style="font-size:13pt;line-height:1.5;padding-top:.04in">{tex_fracs(side["big"])}</div>'),
           dict(title=ICON["vocab"] + "Important Vocabulary", kind="vocab", color=cols[1], rows=[vrow(unit, t) for t in side["vocab"]])]
    h = side["how"]
    out.append(dict(title=ICON["how"] + "How It Works", kind="example", color=cols[2], text=tex_fracs(h["text"]), example=tex_fracs(h["example"]),
                    steps=[[tex_fracs(a), tex_fracs(b)] for a, b in h["steps"]], answer=tex_fracs(h["answer"])))
    if side.get("fig"):
        kind, data, caption = side["fig"]
        svg = figs.render(kind, data)
        svg = re.sub(r'width="(\d+)" height="(\d+)"', lambda m: f'width="100%" style="max-height:1.9in" preserveAspectRatio="xMidYMid meet"', svg, count=1)
        out.append(dict(title=ICON["fig"] + "Visual Model", kind="figure", color=cols[3], svg=svg, text=tex_fracs(caption)))
    else:
        out.append(dict(title=ICON["fig"] + "Visual Model", kind="html", color=cols[3],
                        html='<div style="display:grid;gap:4px;padding-top:.04in">' + "".join(f'<div style="background:#fff;border:1.5px solid var(--c);border-radius:8px;padding:3px 7px">{tex_fracs(x)}</div>' for x in side["figtext"]) + "</div>"))
    out.append(dict(title=ICON["remember"] + "Remember This · Watch Out!", kind="html", color=cols[4],
                    html='<div class="ok">★ Remember this</div><ul>' + "".join(f"<li>{tex_fracs(x)}</li>" for x in side["remember"]) + "</ul>"
                         '<div class="no">⚠ Watch out!</div><ul>' + "".join(f"<li><b>{tex_fracs(a)}:</b> {tex_fracs(b)}</li>" for a, b in side["watch"]) + "</ul>"))
    out.append(dict(title=ICON["try"] + "Try It!", kind="html", color=cols[5],
                    html="<ol style=\"margin:.04in 0;padding-left:.2in\">" + "".join(f"<li style=\"margin-bottom:.05in\">{tex_fracs(q)}<div style=\"margin-top:2px;font-size:8pt;color:#555\">Answer: <span style=\"display:inline-block;transform:rotate(180deg)\">{tex_fracs(a)}</span></div></li>" for q, a, _ in side["tryit"]) + "</ol>"
                         '<div style="font-size:7.5pt;color:#666">Answers are printed upside down. Turn the page to check!</div>'))
    return out


def cheat_sheets():
    d = os.path.join(ROOT, "scripts", "cheat-sheets", "content")
    for i, u in enumerate(UNITS, 1):
        s = SHEET[u["id"]]
        C = dict(name=f"math3-{u['id']}", course=COURSE_NAME, unitNo=i, unitName=u["name"], theme="elementary", focus=s["focus"], morefocus=s["morefocus"],
                 front=side_sections(u["id"], s["sides"][0], 0), back=side_sections(u["id"], s["sides"][1], 1))
        C["checks"] = [{"true": s["sides"][k]["how"]["check"]} for k in (0, 1)] + [{"true": t[2]} for k in (0, 1) for t in s["sides"][k]["tryit"]]
        with open(os.path.join(d, f"math3-{u['id']}.cjs"), "w", encoding="utf-8") as f:
            f.write(f"/* 3rd Grade Math Unit {i} cheat sheet ({u['name']}). Generated by tools/grade3-authoring/build_content.py from content_g3.py. */\n")
            f.write("module.exports = " + json.dumps(C, ensure_ascii=False, indent=1) + ";\n")


def flashcards():
    d = os.path.join(ROOT, "worksheet-generator", "grade3", "flashcards")
    os.makedirs(d, exist_ok=True)
    total = 0
    for i, u in enumerate(UNITS, 1):
        cards = []
        for t, df, ex in V[u["id"]]:
            cards.append({"front": t[0].upper() + t[1:], "back": df, "example": ex, "kind": "vocabulary"})
        for f_, b, k in CARDS[u["id"]]:
            cards.append({"front": f_, "back": b, "kind": k})
        for f_, kind, data, b in VIS[u["id"]]:
            cards.append({"front": f_, "back": b, "kind": "visual", "svg": figs.render(kind, data)})
        for c in cards:
            for k in ("front", "back", "example"):
                if k in c:
                    c[k] = re.sub(r"(?<=[A-Za-z0-9])-(?=[A-Za-z])|(?<=[A-Za-z])-(?=[A-Za-z0-9])", "‑", c[k])
        total += len(cards)
        json.dump({"unit": u["id"], "unitName": u["name"], "number": i, "cards": cards}, open(os.path.join(d, u["id"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    return total


def vocabulary():
    rows = {}
    for u in UNITS:
        items = []
        for t, d, e in V[u["id"]]:
            d, e = d.replace("; ", ", "), e.replace("; ", ", ")
            assert "|" not in t + d + e and ";" not in t + d + e, (t, d, e)
            items.append(f"{t}|{d}|{e}")
        rows["math3-" + u["id"]] = ";".join(items)
    block = ("/* MATH3-VOCAB-START: 3rd Grade Math vocabulary, generated by tools/grade3-authoring/build_content.py. */\n"
             "Object.assign(window.MKVOCAB_BANKS,{\n" + ",\n".join(f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}" for k, v in rows.items()) + "\n});\n/* MATH3-VOCAB-END */\n")
    os.makedirs(os.path.join(HERE, "patches"), exist_ok=True)
    open(os.path.join(HERE, "patches", "vocabulary-math3.js"), "w", encoding="utf-8").write(block)
    return sum(len(V[u["id"]]) for u in UNITS)


def worked_examples():
    """One worked example per skill (Remedial and Standard), chosen from the verified practice bank, plus misconception notes."""
    from collections import Counter
    out = {}
    for u in UNITS:
        bank = json.load(open(os.path.join(ROOT, "question-banks", "math3", u["id"] + ".json"), encoding="utf-8"))["questions"]
        meta = json.load(open(os.path.join(ROOT, "question-banks", "math3", "meta", u["id"] + ".meta.json"), encoding="utf-8"))
        for rec in skill_records(u):
            ex = {}
            for lv in ("cp2", "cp1"):
                qs = [q for q in bank if q["skillId"] == rec["id"] and q["level"] == lv and q["format"] in ("short-answer", "multiple-choice") and meta[q["id"]]["questionType"] not in ("error-analysis", "true-false") and len(q["solutionSteps"]) >= 2]
                qs.sort(key=lambda q: (q["format"] != "short-answer", 0 if q.get("diagram") else 1, meta[q["id"]]["questionType"] not in ("word-problem", "visual"), q["id"]))
                q = qs[0]
                ex[{"cp2": "remedial", "cp1": "standard"}[lv]] = {"questionId": q["id"], "prompt": q["prompt"], "diagram": q.get("diagram"), "steps": q["solutionSteps"], "answer": q["answer"]}
            reasons = Counter(r for q in bank if q["skillId"] == rec["id"] for r in meta[q["id"]].get("distractors", {}).values())
            out[rec["id"]] = {"unit": u["id"], "skill": rec["name"], "standards": rec["standards"], "target": rec["target"], "workedExamples": ex,
                              "misconception": rec["misconception"], "howToAddress": rec["fix"], "commonErrors": [r for r, _ in reasons.most_common(4)]}
    d = os.path.join(ROOT, "worksheet-generator", "grade3")
    json.dump({"course": "math3", "skills": out}, open(os.path.join(d, "worked-examples.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return len(out)


def teaching_notes():
    """Native lesson-planner notes (MKPLAN_TEACH.grade3), same record shape as Grade 4 (tools/grade4-authoring/staging)."""
    notes, objectives = {}, {}
    for u in UNITS:
        sides, voc_all = SHEET[u["id"]]["sides"], V[u["id"]]
        recs = skill_records(u)
        objectives[u["id"]] = []
        for i, rec in enumerate(recs):
            side = sides[0] if i < (len(recs) + 1) // 2 else sides[1]
            terms = set(side["vocab"])
            voc = [[t, d] for t, d, _ in voc_all if t in terms]
            obj = rec["target"][len("I can "):] if rec["target"].startswith("I can ") else rec["target"]
            objectives[u["id"]].append(obj)
            watch = [f"{a}: {b}." for a, b in side["watch"]] + [f"Common error: {rec['misconception']} {rec['fix']}"]
            how = side["how"]
            steps = list(side["remember"]) + [f"Example: {how['text']} Answer: {how['answer']}"]
            notes[rec["id"]] = {"obj": obj, "idea": side["big"], "voc": voc, "watch": " ".join(watch),
                                "cards": [{"h": rec["name"], "big": side["big"], "steps": steps, "figs": []},
                                          {"h": "Watch out", "big": "Explain your thinking and check your answer.", "steps": watch, "figs": []}]}
    d = os.path.join(HERE, "staging")
    os.makedirs(d, exist_ok=True)
    json.dump(notes, open(os.path.join(d, "teaching-notes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    json.dump(objectives, open(os.path.join(d, "objectives.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return len(notes)


if __name__ == "__main__":
    n = checks()
    print(f"{n} content checks passed")
    print(f"{flashcards()} flashcards written")
    print(f"{vocabulary()} vocabulary terms written")
    cheat_sheets()
    print("11 cheat-sheet content files written")
    print(f"{worked_examples()} worked-example records written")
    print(f"{teaching_notes()} teaching-note records written")
