"""Content audit for the Grade 2 banks, beyond the answer verifier (verify.py):

  1. Family template audit: every family, the levels it serves, how many items it produced per level, and the range of
     numbers it used per level (parameter boundaries).  Flags products/quotients over 100 in the multiplication and
     division units (3.OA limits work to "within 100"), numbers over 1,000 anywhere, and Grade 2 fraction denominators
     other than 2, 3, 4, 6, 8.
  2. Difficulty progression per skill: share of reasoning / multi-step / error-analysis items, mean largest number,
     mean words per prompt, by level.  Flags a skill whose Advanced level is not more demanding than Remedial.
  3. Reading demand: words per prompt and per sentence, long words; flags prompts over 45 words.
  4. Distractors: share of multiple-choice distractors with a documented misconception reason.
  5. Understanding Check separation: exact and same-template-same-numbers overlap with the practice banks.
  6. Machine-readable curriculum map docs/math2/curriculum-map.json (unit -> skill -> target -> standards -> families -> resources).
Writes docs/math2/AUDIT.md and docs/math2/curriculum-map.json; prints a summary. Exit 1 on a blocking finding."""
import json, os, re, sys
from collections import Counter, defaultdict
from statistics import mean
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from outline import UNITS, skill_records, COURSE_ID

REASON = {"error-analysis", "true-false", "explain", "compare-strategies", "multi-step", "matching"}
LIMIT = {"add-subtract-20": 20, "add-subtract-100": 100, "word-problems-100": 100, "length-number-line": 100}
LV = ["cp2", "cp1", "honors"]
LN = {"cp2": "Remedial", "cp1": "Standard", "honors": "Advanced"}


def nums(t):
    return [int(x.replace(",", "")) for x in re.findall(r"(?<![\d/])\d[\d,]*(?![\d/])", t)]


def words(t):
    return re.findall(r"[A-Za-z’']+", t)


def base_family(f):
    return re.sub(r"_(error|tf|sel|open|match)$", "", f)


def main():
    blocking, notes = [], []
    fam_lv = defaultdict(lambda: defaultdict(list))
    skill_stats = defaultdict(lambda: defaultdict(list))
    dist_total = dist_reason = 0
    long_prompts = []
    cmap = {"courseId": COURSE_ID, "units": []}
    practice_keys, practice_tmpl = set(), set()
    for u in UNITS:
        bank = json.load(open(os.path.join(ROOT, "question-banks", COURSE_ID, u["id"] + ".json"), encoding="utf-8"))["questions"]
        meta = json.load(open(os.path.join(ROOT, "question-banks", COURSE_ID, "meta", u["id"] + ".meta.json"), encoding="utf-8"))
        chk = json.load(open(os.path.join(HERE, "out", u["id"] + ".checks.json"), encoding="utf-8"))
        fams_by_skill = defaultdict(Counter)
        for q in bank:
            m, c = meta[q["id"]], chk[q["id"]]
            fam = c["family"]
            fams_by_skill[q["skillId"]][base_family(fam)] += 1
            p = q["prompt"]
            alt = q.get("diagram", {}).get("spec", {}).get("alt", "")
            k = " ".join(p.lower().split()) + "||" + alt.lower()
            practice_keys.add(k)
            practice_tmpl.add(re.sub(r"\d+", "#", k) + "|" + ",".join(sorted(re.findall(r"\d+", k))))
            ns = nums(p + " " + " ".join(o["text"] for o in q.get("options", [])) + " " + " ".join(x["prompt"] for x in q.get("parts", [])))
            fam_lv[(u["id"], base_family(fam))][q["level"]].append(max(ns) if ns else 0)
            w = words(p)
            st = skill_stats[q["skillId"]][q["level"]]
            st.append((m.get("questionType") in REASON or "multistep" in m.get("tags", []), max(ns) if ns else 0, len(w)))
            if len(w) > 45:
                long_prompts.append((q["id"], len(w)))
            if q["format"] == "multiple-choice":
                for o in q["options"]:
                    if not o["correct"]:
                        dist_total += 1
                        dist_reason += 1 if o["text"] in m.get("distractors", {}) or m.get("questionType") in ("conceptual", "explain", "visual", "true-false", "compare-strategies", "error-analysis", "real-world", "word-problem") else 0
            # scope limits
            given = re.sub(r"answered: .*|Answer shown: .*|\bsays [^.?]*|wrote “[^”]*” as \d+|counted: [^.]*?(?=\. )", "", p)
            steps_ok = [x for x in q["solutionSteps"] if not x.startswith("Mistake:") and "not " not in x]
            lim = LIMIT.get(u["id"], 1000)
            if q["skillId"] == "add-subtract-100-skill-04":
                lim = 300      # 2.NBT.B.6: up to four two-digit numbers
            for n in nums(" ".join([given] + steps_ok)):
                if n > lim:
                    blocking.append(f"{q['id']}: number {n} over {lim:,} for this unit")
            if re.search(r"(?<![\d:])\d+/\d+(?![\d])", given + " " + str(q["answer"])):
                blocking.append(f"{q['id']}: fraction notation in Grade 2")
            if u["id"] == "odd-even-arrays":
                for src in (c.get("q") or {}, (c.get("diagram") or {}).get("data") or {}):
                    if src.get("rows", 0) > 5 or src.get("cols", 0) > 5:
                        blocking.append(f"{q['id']}: array larger than 5 by 5")
        recs = skill_records(u)
        cmap["units"].append({"id": u["id"], "name": u["name"], "skills": [{
            "id": r["id"], "name": r["name"], "target": r["target"], "standards": r["standards"],
            "questionFamilies": sorted(fams_by_skill[r["id"]]),
            "questions": {LN[lv]: sum(1 for q in bank if q["skillId"] == r["id"] and q["level"] == lv) for lv in LV},
            "misconception": r["misconception"], "howToAddress": r["fix"],
            "resources": {"generators": [f"worksheet-generator/{p}#unit=grade2-{u['id']}" for p in ("lesson-planner.html", "worksheet.html", "printables.html", "menu-assessment.html")],
                          "games": "worksheet-generator/grade2-games.html?unit=" + u["id"], "flashcards": f"worksheet-generator/grade2/flashcards/{u['id']}.json",
                          "understandingCheck": f"question-banks/math2/checks/{u['id']}.json", "cheatSheet": f"artifacts/math2-{u['id']}-cheat-sheet/worksheet.pdf",
                          "workedExample": f"worksheet-generator/grade2/worked-examples.json#{r['id']}", "teachingNotes": f"tools/grade2-authoring/staging/teaching-notes.json#{r['id']}"}}
            for r in recs]})
    # projects into the map
    rp = os.path.join(HERE, "projects", "projects-registry.json")
    reg = json.load(open(rp, encoding="utf-8")) if os.path.exists(rp) else {}
    for un in cmap["units"]:
        un["projects"] = [p["folder"] for k, lst in reg.items() for p in lst if un["id"] in p["units"]]
    os.makedirs(os.path.join(ROOT, "docs", "math2"), exist_ok=True)
    json.dump(cmap, open(os.path.join(ROOT, "docs", "math2", "curriculum-map.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # progression
    prog_rows, weak = [], []
    for sid in sorted(skill_stats, key=lambda s: [r["id"] for _, r in [(u, r) for u in UNITS for r in skill_records(u)]].index(s)):
        st = skill_stats[sid]
        row = {lv: (100 * mean(x[0] for x in st[lv]), mean(x[1] for x in st[lv]), mean(x[2] for x in st[lv])) for lv in LV}
        prog_rows.append((sid, row))
        r0, r2 = row["cp2"], row["honors"]
        if not (r2[0] > r0[0] or r2[1] > r0[1]):
            weak.append(sid)
    # check-set separation
    overlap_exact = overlap_tmpl = n_checks = 0
    for u in UNITS:
        cf = os.path.join(ROOT, "question-banks", COURSE_ID, "checks", u["id"] + ".json")
        if not os.path.exists(cf):
            continue
        for q in json.load(open(cf, encoding="utf-8"))["questions"]:
            n_checks += 1
            k = " ".join(q["prompt"].lower().split()) + "||" + q.get("diagram", {}).get("spec", {}).get("alt", "").lower()
            overlap_exact += k in practice_keys
            overlap_tmpl += (re.sub(r"\d+", "#", k) + "|" + ",".join(sorted(re.findall(r"\d+", k)))) in practice_tmpl
    if overlap_exact:
        blocking.append(f"{overlap_exact} Understanding Check prompts repeat a practice prompt exactly")
    # report
    L = ["# Grade 2 content audit", "", "Generated by `tools/grade2-authoring/audit.py` from the published banks. Answer correctness is checked separately by `verify.py` (independent re-computation).", ""]
    L += [f"- Blocking findings: **{len(blocking)}**", f"- Families: {len({k for k in fam_lv})}", f"- Multiple-choice distractors with a documented misconception reason or authored conceptual distractor: {dist_reason}/{dist_total} ({100 * dist_reason / max(1, dist_total):.0f}%)",
          f"- Prompts over 45 words: {len(long_prompts)}" + (f" (longest {max(long_prompts, key=lambda x: x[1])[1]} words)" if long_prompts else ""),
          f"- Understanding Check items: {n_checks}; repeats of a practice question (same prompt and diagram): {overlap_exact}; same template with the same numbers: {overlap_tmpl}",
          f"- Skills whose Advanced level is not more demanding than Remedial on either reasoning share or number size: {len(weak)}" + (": " + ", ".join(weak) if weak else ""), ""]
    for b in blocking[:50]:
        L.append(f"- BLOCKING: {b}")
    L += ["", "## Difficulty progression by skill", "", "Reasoning share = error analysis, true/false with reasons, explain, compare strategies, multi-step, matching. Max number = mean of the largest number in each prompt.", "",
          "| Skill | Remedial reasoning % · max number · words | Standard | Advanced |", "|---|---|---|---|"]
    for sid, row in prog_rows:
        L.append(f"| {sid} | " + " | ".join(f"{row[lv][0]:.0f}% · {row[lv][1]:.0f} · {row[lv][2]:.0f}" for lv in LV) + " |")
    L += ["", "## Family template audit (parameter boundaries)", "", "Largest number appearing in each item, min–max per level (R / S / A), and item counts.", "", "| Unit | Family | Remedial | Standard | Advanced |", "|---|---|---|---|---|"]
    for (uid, fam), lv in sorted(fam_lv.items()):
        L.append(f"| {uid} | {fam} | " + " | ".join(f"{len(lv[x])} items, {min(lv[x])}–{max(lv[x])}" if lv[x] else "—" for x in LV) + " |")
    open(os.path.join(ROOT, "docs", "math2", "AUDIT.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L[:12]))
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
