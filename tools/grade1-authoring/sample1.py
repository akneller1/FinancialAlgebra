"""Print a random sample of items per skill/level: python3 sample1.py <unit-id> [k]"""
import json, random, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
u, k = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2
b = json.load(open(os.path.join(HERE, "..", "..", "question-banks", "math1", u + ".json")))
random.seed(7)
by = {}
for q in b["questions"]:
    by.setdefault((q["skillId"][-2:], q["level"]), []).append(q)
for key in sorted(by):
    for q in random.sample(by[key], min(k, len(by[key]))):
        o = " | ".join(x["text"] + ("*" if x["correct"] else "") for x in q.get("options", []))
        print(f"{key[0]} {key[1]:6} {q['format'][:5]} {q['prompt'][:150]!r} => {str(q['answer'])[:60]!r} {o[:140]}")
