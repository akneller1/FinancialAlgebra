#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'../..');
const G={};
vm.runInNewContext(fs.readFileSync(path.join(root,'data.js'),'utf8'),{window:G});
vm.runInNewContext(fs.readFileSync(path.join(root,'course-catalog.js'),'utf8'),{window:G});
G.MKMENU={CATALOG:[{course:'Algebra 1',units:[['algebra1-foundations','Unit 1']]}],skillSets:{}};
const context={window:G};
const source=fs.readFileSync(path.join(__dirname,'course-catalog-bridge.js'),'utf8');
vm.runInNewContext(source,context);
assert.equal(G.MKMENU.CATALOG.length,10,'Four grade-level groups, Algebra 2, Precalculus, Calculus Statistics and Discrete Math should be added');
for(const id of ['math6','prealgebra7','prealgebra','algebra2','precalculus','calculus','statistics','discrete']){
 const course=G.LIBRARY.courses.find(c=>c.id===id);
 const group=G.MKMENU.CATALOG.find(g=>g.course===course.name);
 assert.ok(group,'Missing '+id);
 assert.equal(group.units.length,course.units.length,'Wrong unit count for '+id);
 group.units.forEach((unit,i)=>{
  assert.equal(unit[0],id+'-'+course.units[i].id);
  assert.ok(!G.MKMENU.skillSets[unit[0]],'Unsupported bank should not be enabled');
 });
}
vm.runInNewContext(source,context);
assert.equal(G.MKMENU.CATALOG.length,10,'Bridge must be idempotent');
assert.equal(G.MKMENU.CATALOG.at(-1).course,'Algebra 1','Existing algebra catalog preserved');
console.log('PASS: all 69 bank-driven units listed as unsupported without altering the existing course catalog');

