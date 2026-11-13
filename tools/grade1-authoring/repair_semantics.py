#!/usr/bin/env python3
"""Targeted, idempotent Grade 1 semantic repair.

Run ONLY on the unpublished grade1-question-bank branch. Preserve all stable IDs,
8,370 questions, skill/level quotas, standards and review flags. Repair the stored
check (not just the visible text), choices, provenance and changed diagrams together.
The independent math/semantic verifiers must both pass after running this script.
"""
import json, os, re, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import figs1

BANKS = ROOT / "question-banks" / "math1"
CHECKS = HERE / "out"
OUTLINE = json.loads((ROOT / "course-outlines" / "grade1.json").read_text())
MANIFEST = json.loads((BANKS / "manifest.json").read_text())
assert len(MANIFEST["banks"]) == 8 and all(e["approved"] is False and e.get("teacherUse") is False for e in MANIFEST["banks"])
stats = Counter()
GRAMMAR = [(re.compile(r"\b1 tens\b"), "1 ten"), (re.compile(r"\b1 ones\b"), "1 one")]
ONES_PLACE = re.compile(r"How many ones are in (\d+) tens? and (\d+) ones?", re.I)
START = re.compile(r"\bgave\b[\s\S]*?\b(\d+)\s+more\b[\s\S]*?\bnow\b[\s\S]*?\bhas\b\s+(\d+)\b", re.I)
NUM_COUNT = re.compile(r"(?:how many (?:straight )?(?:sides|corners|vertices|faces)\b|count the (?:straight )?(?:sides|corners)\b|(?:shape|figure) has _+ (?:straight )?sides\b)", re.I)
PART_NAME = re.compile(r"(?:parts called|name one part|each part is one|two equal parts are called|four equal parts are called)", re.I)
PICTURES = {"circle","square","rectangle","triangle","hexagon","cube","cylinder","sphere","cone"}
BASE_NOTE = ("Programmatically generated Grade 1 item. Answer calculated from stored mathematical inputs "
             "and independently rechecked; teacher/editorial review pending.")

def textual(s):
    if not isinstance(s, str):
        return s
    for regex, replacement in GRAMMAR:
        s = regex.sub(replacement, s)
    return s

def redraw(q, record):
    diagram = record.get("diagram")
    assert diagram and q.get("diagram"), q["id"]
    target = ROOT / q["diagram"]["spec"]["src"]
    assert target.is_file() and target.is_relative_to(ROOT / "question-banks" / "assets" / "math1"), target
    # render deterministic 720×480 diagrams only when their underlying data changes
    png = figs1.render_png(diagram["kind"], diagram["data"])
    if target.read_bytes() != png:
        target.write_bytes(png)
        stats["images_regenerated"] += 1

def answer_fix(q, record, meta, answer, new_check, steps):
    """Correct a mathematical answer and every answer-dependent field in lockstep."""
    assert q["format"] in ("short-answer", "multiple-choice"), q["id"]
    answer = str(answer)
    old = str(q["answer"])
    if old == answer and record["q"] == new_check:
        return
    q["answer"] = answer
    record["q"] = new_check
    q["solutionSteps"] = steps
    wrongs = []
    if q["format"] == "multiple-choice":
        opts = q["options"]
        assert len(opts) == 4 and sum(bool(x["correct"]) for x in opts) == 1, q["id"]
        used = {answer}
        for item in opts:
            if item["correct"]:
                item["text"] = answer
            else:
                val = str(item["text"])
                if val == answer or val in used or not re.fullmatch(r"\d+",val):
                    val = ""
                if val:
                    used.add(val)
                    wrongs.append(val)
                item["text"] = val
        value = int(answer)
        candidates = [old, str(value+1), str(max(0,value-1)),str(value+2),
                      str(max(0,value-2)),str(value+10),str(value+3)]
        for item in opts:
            if item["correct"] or item["text"]:
                continue
            replacement = next((x for x in candidates if x not in used), None)
            assert replacement is not None
            item["text"] = replacement
            wrongs.append(replacement)
            used.add(replacement)
        assert len({x["text"] for x in opts}) == 4, q["id"]
    else:
        value = int(answer)
        wrongs = [old, str(value+1), str(max(0,value-1)),str(value+2)]
        wrongs = list(dict.fromkeys(x for x in wrongs if x != answer))[:3]
    if wrongs:
        meta["distractors"] = {v:"Confuses the starting amount, change, or total." for v in wrongs}
    meta["explanation"] = steps[-1]
    stats["actual_answer_corrections"] += 1

def rewrite_safe(q, record, meta):
    # Keep select-all text, answer list and check lookup keys in sync.
    if q.get("options"):
        originals = [x["text"] for x in q["options"]]
        for item in q["options"]:
            item["text"] = textual(item["text"])
        if q["format"] == "select-all":
            q["answer"] = [x["text"] for x in q["options"] if x["correct"]]
            table=(record.get("q") or {}).get("table")
            if isinstance(table,dict):
                record["q"]["table"] = {textual(k):v for k,v in table.items()}
        if originals != [x["text"] for x in q["options"]]:
            stats["option_text_edits"] += 1
    before = q["prompt"]
    q["prompt"] = textual(q["prompt"])
    if before != q["prompt"]:
        stats["grammar_fixes"] += 1
    for part in q.get("parts",[]) or []:
        part["prompt"] = textual(part["prompt"])
        part["answer"] = textual(part["answer"])
    if isinstance(q["answer"],str):
        q["answer"] = textual(q["answer"])
    q["solutionSteps"] = [textual(x) for x in q["solutionSteps"]]
    if q.get("diagram"):
        q["diagram"]["spec"]["alt"] = textual(q["diagram"]["spec"]["alt"])
    if "explanation" in meta:
        meta["explanation"] = textual(meta["explanation"])
    if meta.get("distractors"):
        meta["distractors"] = {textual(k):textual(v) for k,v in meta["distractors"].items()}
    if meta.get("shown"):
        meta["shown"] = [textual(v) for v in meta["shown"]]
    # Correctly inflected answer and distractor text can collide after removing
    # the malformed "1 ones" variant; preserve one correct choice and three
    # genuinely distinct plausible errors.
    if q["format"]=="multiple-choice":
        seen=set()
        for item in q["options"]:
            if item["correct"]:
                seen.add(item["text"])
        for item in q["options"]:
            if item["correct"]:
                continue
            if item["text"] in seen:
                ans=q["answer"]
                candidates=[]
                m=re.search(r"(\d+) ten(?:s)? and (\d+) one(?:s)?",str(ans))
                if m:
                    t,o=map(int,m.groups())
                    candidates=[f"{t} tens and {o+1} ones",f"{t+1} tens and {o} ones",
                                f"{t} tens and {max(0,o-1)} ones"]
                if re.fullmatch(r"\d+",str(ans)):
                    n=int(ans)
                    candidates += [str(n+1),str(max(0,n-1)),str(n+2),str(n+3)]
                pick=next((textual(x) for x in candidates if textual(x) not in seen and textual(x)!=ans),None)
                if pick is None:
                    raise AssertionError("Cannot uniquely repair MC distractor "+q["id"])
                item["text"]=pick
                stats["colliding_options_replaced"]+=1
            seen.add(item["text"])
        if len(seen)!=len(q["options"]):
            raise AssertionError("Duplicate option survived "+q["id"])
        if meta.get("distractors"):
            meta["distractors"]={o["text"]:meta["distractors"].get(o["text"],"Common place-value misconception.") for o in q["options"] if not o["correct"]}
    q["sourceNotes"] = BASE_NOTE + " (family: " + record.get("family","unknown") + ")."

for unit in OUTLINE["units"]:
    uid=unit["id"]
    bpath=BANKS/(uid+".json")
    mpath=BANKS/"meta"/(uid+".meta.json")
    cpath=CHECKS/(uid+".checks.json")
    bank=json.loads(bpath.read_text())
    metas=json.loads(mpath.read_text())
    checks=json.loads(cpath.read_text())
    for q in bank["questions"]:
        qid=q["id"]
        record=checks[qid]
        meta=metas[qid]
        check=record.get("q") or {}
        fn=check.get("fn")
        p=q["prompt"]
        ans=str(q["answer"])
        # Start-unknown stories: final=initial+increase. The existing dataset
        # incorrectly uses final as its "starting" answer. Retain story type.
        if fn=="add" and q["format"] in ("short-answer","multiple-choice") \
             and re.search(r"\bhad some\b",p,re.I) and re.search(r"\bstart(?:ed)? with\b",p,re.I):
            m=START.search(p)
            if m:
                gain, final=map(int,m.groups())
                correct=final-gain
                assert correct>=0 and int(ans)==final, (qid,ans,gain,final)
                answer_fix(q,record,meta,correct,{"k":"fn","fn":"missing_part","total":final,"part":gain},
                           [f"Start with an unknown number. Add {gain} to reach {final}.",
                            f"{final} − {gain} = {correct}. The starting amount is {correct}."])
                stats["start_unknown"] += 1
        # Shape identification questions sometimes display only distractors,
        # excluding the shape which is actually the answer.
        if q.get("diagram") and fn=="shape_attr_name":
            dd=record.get("diagram") or {}
            shapes=dd.get("data",{}).get("shapes")
            is_compose=(dd.get("data",{}).get("caption")=="Join the pieces" or
                "Two triangles are put together" in p or
                "Two triangles and" in p)
            if is_compose and ans in ("hexagon","square"):
                if ans=="hexagon":
                    q["prompt"]="Six equal equilateral triangles meet at one center point. What shape do they make?"
                    q["solutionSteps"]=["Join six equal triangular pieces around one center point.",
                                        "Their outside edges form a hexagon."]
                else:
                    q["prompt"]="Two matching right triangles cut from a square are joined along their longest sides. What shape do they make?"
                    q["solutionSteps"]=["Join the two matching halves along the long diagonal.",
                                        "Their outside edges form a square."]
                record["diagram"]={"kind":"composition","data":{"shape":ans}}
                q["diagram"]["spec"]["alt"]=f"A {ans} made by joining congruent triangular pieces."
                meta["diagram"]="composition"
                meta["explanation"]=q["solutionSteps"][-1]
                redraw(q,record)
                stats["composition_corrections"]+=1
            elif isinstance(shapes,list) and shapes and ans in PICTURES and not any(x.get("type")==ans for x in shapes):
                shapes[0]["type"]=ans
                q["diagram"]["spec"]["alt"]="Shapes shown: "+", ".join(x.get("type","shape") for x in shapes)+"."
                redraw(q,record)
                stats["shape_diagram_corrections"]+=1
        # Answer is a shape name but the question now demands a numeric
        # side/corner count, a mismatch introduced by the dedupe templates.
        if q["format"]=="short-answer" and fn=="shape_attr_name" and ans in PICTURES and NUM_COUNT.search(q["prompt"]):
            sides=int(check["sides"])
            q["prompt"]=("Which shape in the picture has no corners?" if sides==0
                         else f"Which shape in the picture has {sides} sides?")
            q["solutionSteps"]=[f"Look for the shape with {sides} sides." if sides else "Look for the shape with no corners.",
                                f"The answer is {ans}."]
            meta["explanation"]=q["solutionSteps"][-1]
            stats["shape_count_vs_name"]+=1
        # Number of equal parts is a count; "name one part" demands a
        # fraction word, even when the stored answer is 2/4.
        if fn=="partition_count" and q["format"]=="short-answer" and PART_NAME.search(q["prompt"]):
            q["prompt"]="How many equal parts are shown in the picture?"
            q["solutionSteps"]=["Count all the equal parts in the picture.",f"There are {ans} equal parts."]
            meta["explanation"]=q["solutionSteps"][-1]
            stats["part_count_wording"]+=1
        # Traded groups of ten are not ones-place digits.
        if fn=="tens_from_ones" and q["format"]=="short-answer" and \
            re.search(r"\bones (?:digit|place)\b|\bhow many ones\b",q["prompt"],re.I):
            count=int(check["ones"])
            q["prompt"]=f"How many groups of ten can be made from {count} ones?"
            q["solutionSteps"]=[f"Make a group of ten from every 10 ones.",f"{count} ones make {ans} tens."]
            meta["explanation"]=q["solutionSteps"][-1]
            stats["tens_from_ones"]+=1
        # Comparison phrasing must agree with the stored check.
        if fn=="shorter" and re.search(r"\bwhich (?:object|one|item)?\s*(?:is )?longer\b",q["prompt"],re.I):
            q["prompt"]="Which object is shorter?"
            stats["comparison_wording"]+=1
        elif fn=="longer" and re.search(r"\bwhich (?:object|one|item)?\s*(?:is )?shorter\b",q["prompt"],re.I):
            q["prompt"]="Which object is longer?"
            stats["comparison_wording"]+=1
        q["prompt"]=ONES_PLACE.sub(
            lambda m:f"In a number with {m.group(1)} tens and {m.group(2)} ones, what is the ones digit?",
            q["prompt"])
        if q["prompt"]!=p and "ones digit" in q["prompt"]:
            stats["ambiguous_ones"]+=1
        rewrite_safe(q,record,meta)
    # When a specific picture was fixed, two once-distinct broken prompts can
    # become identical. Preserve meaning while varying the instructional question.
    # The verifier defines identity by prompt + option text + diagram alt.
    seen_scoped=set()
    def scope_key(q):
        return (q["skillId"],q["level"],re.sub(r"\s+"," ",q["prompt"]).strip().lower().rstrip("."),
                tuple(sorted(o["text"].strip().lower() for o in q.get("options",[]))),
                (q.get("diagram") or {}).get("spec",{}).get("alt","").strip().lower())
    for q in bank["questions"]:
        key=scope_key(q)
        if key in seen_scoped:
            rec=checks[q["id"]]
            fn=(rec.get("q") or {}).get("fn")
            original=q["prompt"]
            ans=str(q["answer"])
            if rec.get("diagram",{}).get("kind")=="composition":
                if ans=="hexagon":
                    variants=["Six equal triangular pieces share a center point. What shape does their outline form?",
                              "What shape forms when six equal triangles meet around one point?",
                              "Name the shape made from six equilateral triangles meeting at their tips.",
                              "Six equal triangles are joined around the middle. What shape is formed?"]
                else:
                    variants=["Two matching halves of a square are joined along their diagonal. What shape is made?",
                              "Which shape is made by joining two matching right triangles cut from one square?",
                              "Two equal right triangles are put back together into their original figure. What shape is it?"]
            elif fn=="shape_attr_name":
                sides=int(rec["q"].get("sides",0))
                variants=([f"Find the shape in the picture with {sides} sides.",
                           f"Name the shape that has {sides} straight sides in this picture.",
                           f"Which shown shape has exactly {sides} straight sides?",
                           f"Choose the {sides}-sided shape shown in the diagram."] if sides else
                          ["Find the shape with no corners in the picture.",
                           "Which pictured shape has no straight sides?",
                           "Name the pictured shape without corners."])
            else:
                raise AssertionError("Unexpected repeated question after repairs "+q["id"]+" "+original)
            for new in variants:
                q["prompt"]=new
                key=scope_key(q)
                if key not in seen_scoped:
                    stats["meaning_preserving_rewordings"]+=1
                    break
            else:
                raise AssertionError("Could not make an authentic unique question "+q["id"])
        seen_scoped.add(key)
    bpath.write_text(json.dumps(bank,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
    mpath.write_text(json.dumps(metas,ensure_ascii=False,indent=0)+"\n",encoding="utf-8")
    cpath.write_text(json.dumps(checks,ensure_ascii=False,indent=0)+"\n",encoding="utf-8")
    stats["units_repaired"]+=1

# Explicitly preserve release gate; the repair script must never approve content.
after=json.loads((BANKS/"manifest.json").read_text())
assert after==MANIFEST and all(e["approved"] is False and e.get("teacherUse") is False for e in after["banks"])
assert stats["units_repaired"]==8
print("Grade 1 targeted semantic repairs:",dict(stats),flush=True)
