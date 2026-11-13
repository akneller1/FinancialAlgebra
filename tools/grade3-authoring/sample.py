"""Print sample questions for review: python3 sample.py <unit-id> [n per skill/level] [skill-number]"""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
u = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 2; only = sys.argv[3] if len(sys.argv) > 3 else None
qs = json.load(open(os.path.join(ROOT, "question-banks", "math3", u + ".json")))["questions"]
by = {}
for q in qs:
    by.setdefault((q["skillId"], q["level"]), []).append(q)
r = random.Random(7)
for (s, lv), L in sorted(by.items(), key=lambda x: (x[0][0], ["cp2", "cp1", "honors"].index(x[0][1]))):
    if only and not s.endswith(only):
        continue
    for q in r.sample(L, min(n, len(L))):
        print(f"[{q['id']} {q['format']}] {q['prompt']}")
        if q.get("diagram"): print("   DIAGRAM:", q["diagram"]["spec"]["alt"])
        for o in q.get("options", []): print("   ", "*" if o["correct"] else "-", o["text"])
        for p in q.get("parts", []): print("    part:", p["prompt"], "->", p["answer"])
        print("   ANSWER:", q["answer"], "| STEPS:", " ".join(q["solutionSteps"])[:200])
