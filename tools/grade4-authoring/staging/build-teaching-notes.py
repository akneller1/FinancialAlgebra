"""Lesson-planner teaching notes for the native Classroom planner, one record per skill (MKPLAN_TEACH.grade4).
Built from the cheat-sheet content (content_g4.py): the side of the sheet that covers the skill gives the big idea,
vocabulary, a worked example, reminders and common mistakes.   python3 staging/build-teaching-notes.py"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import content_g4 as c
O = json.load(open(os.path.join(os.path.dirname(HERE), 'outline.json'), encoding='utf-8'))
OBJ = json.load(open(os.path.join(HERE, 'objectives.json'), encoding='utf-8'))   # verb phrases: “Students will be able to …”
notes = {}
for u in O['units']:
    sides, V, n = c.SHEET[u['id']]['sides'], c.V[u['id']], len(u['skills'])
    for i, (name, _) in enumerate(u['skills']):
        side = sides[0] if i < (n + 1) // 2 else sides[1]      # the first side covers the first half of the unit
        terms = set(side.get('vocab', []))
        voc = [[t, d] for t, d, _ in V if t in terms] or [[t, d] for t, d, _ in V[:4]]
        watch = [f"{a}: {b}." for a, b in side.get('watch', [])]
        how = side.get('how', {})
        steps = list(side.get('remember', [])) + (['Example: ' + how['text'] + ' Answer: ' + str(how.get('answer', ''))] if how.get('text') else [])
        notes[f"{u['id']}-skill-{i + 1:02d}"] = {"obj": OBJ[u['id']][i], "idea": side['big'], "voc": voc, "watch": ' '.join(watch),
            "cards": [{"h": name, "big": side['big'], "steps": steps, "figs": []},
                      {"h": "Watch out", "big": "Explain your thinking and check your answer.", "steps": watch, "figs": []}]}
json.dump(notes, open(os.path.join(HERE, 'teaching-notes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(notes), 'skills')
