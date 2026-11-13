"""Fixed Understanding Check sets for Grade 3, kept separate from the practice banks.

For every unit, skill and level: 2 items (1 short answer + 1 multiple choice) drawn from the same skill-specific
families with a different random stream ("check"), never repeating a practice-bank prompt (exact or near duplicate).
Writes (same schema as the practice banks, so the existing players and printers can read them):
  question-banks/math3/checks/<unit>.json            schemaVersion 1, IDs m3c-<unit>-sNN-<level>-NNN
  question-banks/math3/checks/meta/<unit>.meta.json  question type, distractor reasons, skill feedback
  question-banks/assets/math3/<unit>/m3c-*.png       diagrams
  tools/grade3-authoring/out/checks/<unit>.checks.json  check data for verify.py (VERIFY_CHECKS=1)
Usage: python3 build_checks.py      (run after build.py)"""
import importlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "units"))
import build as B
from outline import UNITS, COURSE_ID, skill_records

B.QUOTA = {"sa": 1, "mc": 1, "err": 0, "tf": 0, "sel": 0, "open": 0}
B.PREFIX = "m3c"
_rng = B.rng
B.rng = lambda *parts: _rng("understanding-check", *parts)


def qkey(prompt, alt):
    """A question is the same question when its prompt and its diagram are the same (options and format may differ)."""
    return " ".join(prompt.lower().split()) + "||" + (alt or "").lower()


def pkey(p):
    # compare with the published (polished) text of the practice bank
    return qkey(B.fix_text(p.prompt), p.diagram.alt if p.diagram else "")


def nkey(p):
    k = pkey(p)
    return re.sub(r"\d+", "#", k) + "|" + ",".join(sorted(re.findall(r"\d+", k)))


B.pkey, B.nkey = pkey, nkey
SHORT = []


def main():
    for u in UNITS:   # practice questions are off limits: exact, and same template with the same numbers
        for q in json.load(open(os.path.join(B.ROOT, "question-banks", COURSE_ID, u["id"] + ".json"), encoding="utf-8"))["questions"]:
            k = qkey(q["prompt"], q.get("diagram", {}).get("spec", {}).get("alt", ""))
            B.SEEN[k] = q["id"]
            B.NEAR[re.sub(r"\d+", "#", k) + "|" + ",".join(sorted(re.findall(r"\d+", k))) + "|" + str(q["answer"])] += 1
    outdir = os.path.join(B.ROOT, "question-banks", COURSE_ID, "checks")
    os.makedirs(os.path.join(outdir, "meta"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "out", "checks"), exist_ok=True)
    total = 0
    for mname, u in zip(B.MODS, UNITS):
        mod = importlib.import_module(mname)
        b = B.Builder(mod, u)
        recs = skill_records(u)
        feedback = {}
        for rec in recs:
            spec = mod.SKILLS[rec["index"]]
            for L in range(3):
                try:
                    items = b.skill(rec, spec, L)
                except RuntimeError:
                    # very small families (e.g. Remedial facts with 2, 5 and 10): allow the same template with other numbers
                    # as practice, but never the same question (exact prompt and diagram stay blocked through SEEN)
                    saved = dict(B.NEAR)
                    B.NEAR.clear()
                    try:
                        items = b.skill(rec, spec, L)
                        print("   relaxed near-duplicate rule for", rec["id"], L)
                    except RuntimeError:
                        # the practice bank already uses every distinct item of this small family set: one check item, not two
                        q0 = dict(B.QUOTA)
                        B.QUOTA.update({"sa": 1, "mc": 0})
                        try:
                            items = b.skill(rec, spec, L)
                        except RuntimeError:
                            items = []
                        B.QUOTA.clear(); B.QUOTA.update(q0)
                        SHORT.append(f"{rec['id']} level {L}: {len(items)} check item(s)")
                        print("   short:", SHORT[-1])
                    B.NEAR.update(saved)
                for q, meta, chk in items:
                    b.questions.append(q)
                    b.meta[q["id"]] = meta
                    b.checks[q["id"]] = chk
            feedback[rec["id"]] = {"skill": rec["name"], "target": rec["target"], "standards": rec["standards"],
                                   "ifCorrect": f"You can do this: {rec['target'][2:] if rec['target'].startswith('I ') else rec['target']}",
                                   "ifMissed": f"Practice this skill again. Watch for this mistake: {rec['misconception']} Try this: {rec['fix']}"}
        bank = {"schemaVersion": 1, "courseId": COURSE_ID, "unitId": u["id"], "purpose": "understanding-check", "questions": b.questions}
        json.dump(bank, open(os.path.join(outdir, u["id"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump({"skillFeedback": feedback, "questions": b.meta}, open(os.path.join(outdir, "meta", u["id"] + ".meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        json.dump(b.checks, open(os.path.join(HERE, "out", "checks", u["id"] + ".checks.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        # draw only the new check diagrams (draw_all would clear the practice diagrams)
        import io, subprocess
        from PIL import Image
        for src, dg in b.diagrams:
            s = B.figs.render(dg.kind, dg.data)
            png = subprocess.run(["rsvg-convert", "-z", "1.25"], input=s.encode(), capture_output=True, check=True).stdout
            im = Image.open(io.BytesIO(png)).convert("RGB").quantize(colors=96, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
            im.save(os.path.join(B.ROOT, src), optimize=True)
        total += len(b.questions)
        print(u["id"], len(b.questions), "check items", len(b.diagrams), "diagrams")
    print(total, "Understanding Check items")
    json.dump({"short": SHORT}, open(os.path.join(HERE, "out", "checks", "_summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
