#!/usr/bin/env python3
"""Surgically repair Grade 1 addition-width/regrouping mismatches.

Only replaces items *provably* inconsistent with the four Grade 1 Adding
Within 100 skill objectives. Keeps IDs, levels, formats, all review flags,
the 93-skill outline, and all unrelated questions untouched.
"""
import json, re, sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sys.path.insert(0,str(HERE))
from outline import UNITS, skill_records
from g1lib import Reject, rng
from build1 import Builder
from families import add_two_digit_items
import figs1

UNIT="adding-within-100"
BANK=ROOT/"question-banks"/"math1"/(UNIT+".json")
META=ROOT/"question-banks"/"math1"/"meta"/(UNIT+".meta.json")
CHECK=HERE/"out"/(UNIT+".checks.json")
manifest=json.loads((ROOT/"question-banks"/"math1"/"manifest.json").read_text())
assert all(e["approved"] is False and e.get("teacherUse") is False for e in manifest["banks"])
data=json.loads(BANK.read_text());meta=json.loads(META.read_text());checks=json.loads(CHECK.read_text())
unit=next(u for u in UNITS if u["id"]==UNIT)
recs={r["id"]:r for r in skill_records(unit)}
SCOPES=Counter()
scope_key=lambda q:(q["skillId"],q["level"])
def identity(q):
    normal=lambda x:re.sub(r"\s+"," ",str(x).strip().lower())
    return (normal(q["prompt"]),tuple(sorted(normal(o["text"]) for o in q.get("options",[]))),
            normal((q.get("diagram") or {}).get("spec",{}).get("alt","")))
def broken(q):
    if q["format"] not in ("multiple-choice","short-answer"):
        return False
    idx=int(q["skillId"].split("-skill-")[-1])
    if idx not in (1,2,4,7):return False
    ck=(checks[q["id"]].get("q") or {})
    if ck.get("fn")!="add":return False
    a,b=int(ck["a"]),int(ck["b"])
    carry=(a%10)+(b%10)>=10
    if idx==1:return not ((10<=max(a,b)<=99) and 1<=min(a,b)<=9 and not carry)
    if idx==2:return not (a>=10 and b>=10 and not carry)
    if idx==4:return not ((10<=max(a,b)<=99) and 1<=min(a,b)<=9 and carry)
    return not (a>=10 and b>=10 and carry)
targets=[q for q in data["questions"] if broken(q)]
assert len(targets)>100 and len(targets)<230, "Unexpected old wrong-addend count; review before continuing"
targetIds={q["id"] for q in targets}
for q in data["questions"]:
    if q["id"] not in targetIds:
        SCOPES[(scope_key(q),identity(q))]+=1
b=Builder(None,unit)
newImages={}
stats=Counter()
for old in targets:
    rec=recs[old["skillId"]]
    idx=rec["index"]
    L=["cp2","cp1","honors"].index(old["level"])
    generator=add_two_digit_items(compose=idx in (4,7),second_digits=1 if idx in (1,4) else 2)
    chosen=None
    for attempt in range(1,1401):
        r=rng("grade1-aligned-addends",old["id"],attempt)
        try:
            p=generator(r,L)
        except Reject:
            continue
        # Preserve which questions are usable in text-only skill-filtered games.
        if not old.get("diagram"):p.diagram=None
        if old["format"]=="multiple-choice" and len(p.wrong)<3:continue
        cq,cm,cc=b.emit(rec,L,0,p,old["format"],"aligned_add_two_digit_items",r,
                        pos=(attempt%4),qid=old["id"])
        if old["format"]=="multiple-choice" and (not cq["options"] or len(cq["options"])!=4):
            continue
        key=(scope_key(cq),identity(cq))
        if SCOPES[key]:continue
        ck=cc["q"]
        a,b0=int(ck["a"]),int(ck["b"])
        assert a+b0==int(cq["answer"])
        assert (a%10)+(b0%10)>=10 if idx in (4,7) else (a%10)+(b0%10)<10
        assert (min(a,b0)<10) == (idx in (1,4))
        chosen=(cq,cm,cc)
        SCOPES[key]+=1
        if cq.get("diagram"):
            img=cc["diagram"]
            newImages[cq["diagram"]["spec"]["src"]]=(img["kind"],img["data"])
        break
    if not chosen:
        raise RuntimeError("Unable to replace "+old["id"]+" with aligned unique question")
    q,m,c=chosen
    old.clear()
    old.update(q)
    meta[q["id"]]=m
    checks[q["id"]]=c
    stats["replaced"]+=1
    stats["skill"+str(idx)]+=1
    if q.get("diagram"):stats["diagramsUpdated"]+=1
for rel,(kind,params) in newImages.items():
    file=ROOT/rel
    assert file.parent.is_dir()
    file.write_bytes(figs1.render_png(kind,params))
assert len(data["questions"])==8370-7560 and len(meta)==len(data["questions"]) and len(checks)==len(data["questions"])
BANK.write_text(json.dumps(data,ensure_ascii=False,indent=1)+"\n")
META.write_text(json.dumps(meta,ensure_ascii=False,indent=0)+"\n")
CHECK.write_text(json.dumps(checks,ensure_ascii=False,indent=0)+"\n")
assert all(e["approved"] is False and e.get("teacherUse") is False for e in json.loads((ROOT/"question-banks"/"math1"/"manifest.json").read_text())["banks"])
print("Grade 1 aligned-addend repair:",dict(stats))
