"""Content audit for the Grade 1 (math1) banks: counts, Grade 1 scope limits, reading load, level progression,
distractor reasons, duplicates, repetition, game eligibility and asset references. Writes out/audit.json and prints a summary.
Usage: python3 audit1.py"""
import glob, json, math, os, re, statistics as st, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from outline import UNITS, COURSE_ID, STANDARDS, skill_records

LIMIT = {"count-120": 120, "add-subtract-10": 10, "add-subtract-20": 20, "equal-sign": 20, "word-problems-20": 20, "tens-ones": 99,
         "compare-numbers": 99, "add-subtract-100": 109, "measuring-length": 20, "telling-time": 12, "data": 60, "shapes-equal-shares": 20}
LV = ["cp2", "cp1", "honors"]


def nums(t):
    return [int(x) for x in re.findall(r"(?<![:\d])\d+(?![:\d])", t)]


def words(t):
    return len(re.findall(r"[A-Za-z']+|\d+", t))


def main():
    blocking, notes = [], []
    rep = {"units": {}, "skills": {}}
    allq, meta_all = [], {}
    for u in UNITS:
        b = json.load(open(os.path.join(ROOT, "question-banks", COURSE_ID, u["id"] + ".json"), encoding="utf-8"))
        m = json.load(open(os.path.join(ROOT, "question-banks", COURSE_ID, "meta", u["id"] + ".meta.json"), encoding="utf-8"))
        meta_all.update(m)
        for q in b["questions"]:
            q["_unit"] = u["id"]
            allq.append(q)
    by = defaultdict(list)
    for q in allq:
        by[(q["skillId"], q["level"])].append(q)
    # scope, notation, reading load
    over = []
    for q in allq:
        text = q["prompt"] + " " + (q["answer"] if isinstance(q["answer"], str) else " ".join(q["answer"])) + " " + " ".join(p["prompt"] for p in q.get("parts", []))
        text = re.sub(r"(answered|Answer shown): .*", "", text)
        mx = max(nums(text) + [0])
        if mx > LIMIT[q["_unit"]]:
            over.append((q["id"], mx))
        for o in q.get("options", []):
            if not o["correct"] and max(nums(o["text"]) + [0]) > 10 * LIMIT[q["_unit"]] + 10:
                notes.append(f"{q['id']}: far-off distractor {o['text']}")
        if re.search(r"×|÷|\d/\d", text + " ".join(q["solutionSteps"])):
            blocking.append(f"{q['id']}: beyond Grade 1 notation")
    for i, mx in over:
        blocking.append(f"{i}: number {mx} is outside the unit's Grade 1 range")
    wc = [words(q["prompt"].split("\n")[1] if q["prompt"].startswith(tuple(n + " solved" for n in [])) else q["prompt"]) for q in allq]
    long_ = [q["id"] for q in allq if words(q["prompt"]) > 45 and "solved this problem" not in q["prompt"]]
    # progression per skill: mean of the largest number in prompt+answer, and share of reasoning/multistep items
    prog_flags = []
    for u in UNITS:
        for rec in skill_records(u):
            row = {}
            for lv in LV:
                qs = by[(rec["id"], lv)]
                mags = [max(nums(q["prompt"] + " " + str(q["answer"])) + [0]) for q in qs]
                reason = sum(1 for q in qs if meta_all[q["id"]]["questionType"] in ("reasoning", "explain", "multi-step", "error-analysis", "compare-strategies", "true-false", "matching")) / len(qs)
                row[lv] = {"n": len(qs), "formats": dict(Counter(q["format"] for q in qs)), "meanMaxNumber": round(st.mean(mags), 1),
                           "reasoningShare": round(reason, 2), "meanWords": round(st.mean(words(q["prompt"]) for q in qs), 1),
                           "diagrams": sum(1 for q in qs if q.get("diagram"))}
            rep["skills"][rec["id"]] = row
            a, c = row["cp2"], row["honors"]
            if not (c["meanMaxNumber"] > a["meanMaxNumber"] or c["reasoningShare"] > a["reasoningShare"] + 0.05):
                prog_flags.append(rec["id"])
    # distractor reasons
    dtot = dres = 0
    for q in allq:
        d = meta_all[q["id"]].get("distractors", {})
        dtot += len(d)
        dres += sum(1 for v in d.values() if v)
    # duplicates and repetition
    ex = Counter(" ".join(q["prompt"].lower().split()) + "|" + q.get("diagram", {}).get("spec", {}).get("alt", "") + "|" + "|".join(sorted(o["text"] for o in q.get("options", [])))
                 + "|" + "|".join(p["prompt"] for p in q.get("parts", [])) for q in allq)
    exact = sum(v - 1 for v in ex.values() if v > 1)
    tmpl = Counter((q["skillId"], q["level"], re.sub(r"\d+", "#", q["prompt"].lower())) for q in allq)
    heavy = sum(1 for v in tmpl.values() if v > 6)
    near = Counter((re.sub(r"\d+", "#", q["prompt"].lower()), str(sorted(nums(q["prompt"]))), str(q["answer"]), q.get("diagram", {}).get("spec", {}).get("alt", ""),
                    "|".join(sorted(o["text"] for o in q.get("options", []))), "|".join(p["prompt"] for p in q.get("parts", []))) for q in allq)
    cross = sum(v - 1 for v in near.values() if v > 1)
    # MC quality
    mc_bad = []
    for q in allq:
        if q["format"] == "multiple-choice":
            ts = [o["text"] for o in q["options"]]
            if len(ts) != 4 or len(set(t.strip().lower() for t in ts)) != 4 or sum(o["correct"] for o in q["options"]) != 1:
                mc_bad.append(q["id"])
            pos = [i for i, o in enumerate(q["options"]) if o["correct"]]
    pos = Counter([i for q in allq if q["format"] == "multiple-choice" for i, o in enumerate(q["options"]) if o["correct"]])
    # assets
    missing, unused = [], []
    srcs = {q["diagram"]["spec"]["src"] for q in allq if q.get("diagram")}
    for f in glob.glob(os.path.join(ROOT, "question-banks", COURSE_ID, "checks", "*.json")):
        srcs |= {q["diagram"]["spec"]["src"] for q in json.load(open(f, encoding="utf-8"))["questions"] if q.get("diagram")}
    for s in srcs:
        if not os.path.exists(os.path.join(ROOT, s)):
            missing.append(s)
    on_disk = {os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "question-banks", "assets", COURSE_ID, "*", "*.png"))}
    unused = sorted(on_disk - srcs)
    games = Counter()
    for q in allq:
        g = meta_all[q["id"]].get("game", {})
        games["textMC"] += g.get("textMC", False)
        games["numeric"] += g.get("numeric", False)
    # explanations end with the answer; unit in the answer matches the noun the prompt asks about
    step_miss, unit_miss = [], []
    for q in allq:
        if q["format"] in ("short-answer", "multiple-choice") and isinstance(q["answer"], str):
            a_ = q["answer"]
            core = re.sub(r"\s+", " ", a_.lower()).rstrip(".")
            last = " ".join(q["solutionSteps"][-2:]).lower()
            nn = nums(a_)
            if nn and not all(str(x) in last for x in nn) and core not in last:
                step_miss.append(q["id"])
            m_ = re.search(r"how many ([a-z]+(?: [a-z]+)?)", q["prompt"].split("\n")[-2 if "solved this problem" in q["prompt"] else 0].lower())
            mu = re.fullmatch(r"\d+ ([a-z ]+)", a_.lower())
            if m_ and mu:
                asked, unit = m_.group(1), mu.group(1)
                stem = lambda w: re.sub(r"(es|s)$", "", w.split()[-1])
                if stem(unit) not in asked and stem(unit) not in q["prompt"].lower():
                    unit_miss.append(q["id"])
    rep["stepAnswerMismatch"] = step_miss
    rep["unitMismatch"] = unit_miss
    covered = {s for q in allq for s in q["standards"]}
    rep["summary"] = {"questions": len(allq), "units": len(UNITS), "skills": sum(len(u["skills"]) for u in UNITS),
                      "standardsCovered": f"{len(covered & set(STANDARDS))}/{len(STANDARDS)}", "formats": dict(Counter(q["format"] for q in allq)),
                      "levels": dict(Counter(q["level"] for q in allq)), "withDiagram": sum(1 for q in allq if q.get("diagram")),
                      "questionTypes": dict(Counter(meta_all[q["id"]]["questionType"] for q in allq).most_common()),
                      "promptsOver45Words": len(long_), "maxPromptWords": max(words(q["prompt"]) for q in allq if "solved this problem" not in q["prompt"]),
                      "meanPromptWords": {lv: round(st.mean(words(q["prompt"]) for q in allq if q["level"] == lv), 1) for lv in LV},
                      "distractorReasonCoverage": round(dres / max(dtot, 1), 3), "exactDuplicates": exact, "sameNumbersSameTemplateAcrossBank": cross,
                      "templatesOver6InASkillLevel": heavy, "mcProblems": len(mc_bad), "mcCorrectPosition": dict(sorted(pos.items())),
                      "assetsReferenced": len(srcs), "assetsMissing": len(missing), "assetsUnused": len(unused),
                      "gameEligible": dict(games), "explanationWithoutAnswer": len(step_miss), "answerUnitNotInPrompt": len(unit_miss), "outOfRange": len(over), "progressionFlags": prog_flags}
    rep["notes"] = notes
    rep["summary"]["farOffDistractors"] = len(notes)
    rep["blocking"] = blocking + [f"missing asset {m}" for m in missing] + [f"bad MC {i}" for i in mc_bad]
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    json.dump(rep, open(os.path.join(HERE, "out", "audit.json"), "w"), indent=1)
    print(json.dumps(rep["summary"], indent=1))
    print("BLOCKING", len(rep["blocking"]))
    for x in rep["blocking"][:30]:
        print("  ", x)
    return 1 if rep["blocking"] else 0


if __name__ == "__main__":
    sys.exit(main())
