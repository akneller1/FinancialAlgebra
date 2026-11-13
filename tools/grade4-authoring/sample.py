"""Print a readable sample of a built bank: python3 sample.py <unit-id> [level] [n-per-skill]"""
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
u = sys.argv[1]
lv = sys.argv[2] if len(sys.argv) > 2 else None
n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
b = json.load(open(os.path.join(HERE, "..", "..", "question-banks", "math4", u + ".json")))
c = json.load(open(os.path.join(HERE, "out", u + ".checks.json")))
seen = {}
for q in b["questions"]:
    if lv and q["level"] != lv:
        continue
    k = (q["skillId"], c[q["id"]]["family"])
    if k in seen:
        continue
    seen[k] = 1
    if sum(1 for x in seen if x[0] == q["skillId"]) > n:
        continue
    opts = " | ".join(("*" if o["correct"] else "") + o["text"] for o in q.get("options", []))
    parts = " | ".join(p["prompt"] + " => " + p["answer"] for p in q.get("parts", []))[:300]
    print(f"[{q['id']} {c[q['id']]['family']}] {q['prompt']!r}\n    ANS: {q['answer']}  {('OPTS: ' + opts) if opts else ''} {parts}")
