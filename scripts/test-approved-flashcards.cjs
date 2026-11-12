#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'worksheet-generator/approved-flashcards.html'),'utf8');
const js=fs.readFileSync(path.join(root,'worksheet-generator/approved-flashcards.js'),'utf8');
new vm.Script(js);
for(const id of ['afStatus','afApp','afLevel','afSkill','afCard','afPrev','afNext','afFlip','afNeed','afGot','afShuffle','afMissed','afReset'])assert.ok(html.includes('id="'+id+'"'),'Missing '+id);
assert.ok(html.indexOf('question-bank-adapter.js')<html.indexOf('approved-flashcards.js'),'Question adapter must load first');
assert.ok(html.includes('question-bank-loader.js'),'Approved manifest loader required');
assert.ok(js.includes('banks.available(courseId,unitId)'),'Approval gating must be enforced');
assert.ok(js.includes("formats:['short-answer','multiple-choice']"),'Flashcards must filter compatible questions');
assert.ok(js.includes('function imagePath(q)') && js.includes('diagram(q,card)'), 'Safe diagram renderer required');
assert.ok(js.includes('question-banks') && js.includes('assets') && js.includes('imagePath(q)'), 'Only local diagram assets may be used');
assert.ok(js.includes("if(!figure.isConnected)return"),'Stale diagram errors must not affect subsequent cards');
assert.ok(js.includes("el('afNeed').disabled=true") && js.includes("el('afGot').disabled=true"),'Missing diagram must disable self-rating');
assert.ok(js.includes("if(S.flipped){\\n  text('p',q.prompt,card)".replace('\\n','\n')),'Answer side must preserve the question and diagram');
assert.ok(!js.includes('innerHTML'),'Question content must render as text rather than injected HTML');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'question-banks/manifest.json'),'utf8'));
assert.equal(manifest.version,1);
assert.ok(Array.isArray(manifest.banks));
for(const item of manifest.banks){
 assert.ok(item.approved===true||(item.courseId==='algebra2'&&item.teacherUse===true),'Manifest entries must be explicitly approved or enabled for Algebra 2 teacher use');
 assert.equal(item.path,'question-banks/'+item.courseId+'/'+item.unitId+'.json');
 assert.ok(fs.existsSync(path.join(root,item.path)),'Approved bank file missing: '+item.path);
}
assert.ok(html.includes("['math5','math6','prealgebra7','prealgebra']"),'Middle-school course detection required');
for(const label of ['Remedial','Standard','Advanced'])assert.ok(html.includes("text='"+label+"'"),'Missing middle-school label '+label);
console.log('PASS approved flashcard player structure, gating and content rendering safeguards');
