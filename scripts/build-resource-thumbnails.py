"""Build local, accessible resource previews for all Financial Algebra unit cards."""
from pathlib import Path
import json, html, textwrap, subprocess, tempfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'thumbs/financial-algebra';OUT.mkdir(parents=True,exist_ok=True)
manifest=json.loads((ROOT/'financial/resources.json').read_text())
ink='#14173a';purple='#7448ff';blue='#2563eb';green='#15803d'
def text(x,y,value,size=18,color=ink,bold=False):return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{html.escape(value)}</text>'
def rect(x,y,w,h,fill='white',stroke='#d4d8eb',rx=10):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def lines(value,x,y,width=53,size=18,maxlines=3):return ''.join(text(x,y+i*26,s,size) for i,s in enumerate(textwrap.wrap(value,width)[:maxlines]))
for u in manifest['units']:
 id=u['unitId'];bank=json.loads((ROOT/f'financial/banks/{id}.json').read_text());v=bank['vocab'][0]
 for kind,label in [('lesson','LESSON PLAN'),('worksheet','WORKSHEET'),('assessment','ASSESSMENT'),('practice','TEST REVIEW'),('flashcards','FLASHCARDS'),('lab','DECISION LAB'),('guide','TEACHER GUIDE')]:
  s=rect(0,0,720,450,'#f4f5fb',ink,0)+rect(25,24,670,63,'#ffd23f',ink,15)+text(45,65,label,27,ink,True)
  s+=text(37,119,f"UNIT {u['unitNum']} · {u['name']}",18,purple,True)
  if kind=='flashcards':
   s+=rect(133,161,475,225,'#e9e0ff',purple,17)+rect(109,145,475,225,'white',purple,17)
   s+=text(137,184,'KEY VOCABULARY',15,purple,True)+lines(v['term'],137,228,29,27,2)
   s+=text(137,307,'Think → Flip → Review',20,blue,True)+text(137,344,'Terms · formulas · financial principles',15)
  elif kind=='lab':
   for x,label2,c in [(40,'OPTION A',purple),(375,'OPTION B',blue)]:
    s+=rect(x,151,305,178,'white',c,12)+text(x+19,187,label2,22,c,True)
    for j,w in enumerate([235,170,205] if x==40 else [185,230,150]):s+=rect(x+19,209+j*31,w,14,'#e6efff',c,3)
   s+=text(40,374,'Compare cost · risk · flexibility',23,ink,True)+text(40,411,'Explain which choice fits your goals and why.',18)
  else:
   s+=rect(40,148,640,270,'white',purple,12)
   if kind=='practice':
    s+=text(61,185,'CHECK YOUR UNDERSTANDING',20,purple,True)+text(61,226,'Financial concepts + real-life decisions',20)
    for j,label2 in enumerate(['Answer the question','Check the explanation','Review the skill']):
     s+=f'<circle cx="78" cy="{271+j*45}" r="13" fill="#e6efff" stroke="{blue}" stroke-width="2"/>'+text(105,278+j*45,label2,19)
   elif kind=='guide':
    s+=text(61,185,'TEACHING SUPPORT',21,purple,True)
    for j,a in enumerate(['Discussion prompts','Model reasoning','Compare assumptions','Reflect on the decision']):s+=text(65,232+j*43,'✓ '+a,20)
   else:
    labels={'lesson':['Learning goals','Vocabulary & worked example','Practice & exit ticket'],'worksheet':['Explain a financial concept','Calculate and compare options','Show reasoning and check units'],'assessment':['Multiple choice','Short answer & scenarios','Worked teacher answer key']}[kind]
    for j,a in enumerate(labels):
     s+=text(61,188+j*76,f'{j+1}. '+a,21,purple,j==0)
     s+=f'<path d="M65 {214+j*76} H648" stroke="#d4d8eb" stroke-width="3"/>'
  (OUT/f'{id}-{kind}.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 450" role="img" aria-label="'+html.escape(label+' preview for '+u['name'],quote=True)+'">'+s+'</svg>')
 with tempfile.TemporaryDirectory() as d:
  subprocess.run(['pdftoppm','-scale-to','750','-png',str(ROOT/f'artifacts/financial-algebra-{id}-cheat-sheet/cheat-sheet.pdf'),d+'/page'],check=True,stderr=subprocess.DEVNULL)
  canvas=Image.new('RGB',(720,450),'#e6e8f1')
  for i in [1,2]:
   im=Image.open(f'{d}/page-{i}.png');im.thumbnail((340,430));canvas.paste(im,(10+(i-1)*355+(340-im.width)//2,10))
  canvas.save(OUT/f'{id}-cheat-sheet.jpg',quality=90)
print('Built 80 unit/resource previews, including actual front/back cheat-sheet thumbnails.')
