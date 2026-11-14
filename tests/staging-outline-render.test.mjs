import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {mountOutline} from '../src/outline-template.js';
for(const grade of [1,2])test('Grade '+grade+' current outline renders every unit',()=>{
 const course=JSON.parse(fs.readFileSync(new URL('../course-outlines/grade'+grade+'.json',import.meta.url)));
 const nodes=new Map(),listeners={};
 function node(id){if(!nodes.has(id))nodes.set(id,{innerHTML:'',value:'',style:{},addEventListener(){},focus(){}});return nodes.get(id);}
 const previous={document:globalThis.document,window:globalThis.window,location:globalThis.location};
 globalThis.document={getElementById:node};globalThis.location={hash:''};globalThis.window={addEventListener(type,fn){listeners[type]=fn;},scrollTo(){}};
 try{
  mountOutline(course,{page:'grade'+grade+'.html'});
  assert.match(node('main').innerHTML,/12 units/);
  for(const unit of course.units){
   location.hash='#'+course.id+'.'+unit.id;listeners.hashchange();
   const html=node('main').innerHTML;
   assert(html.includes(unit.name));assert(!html.includes('undefined'));
   assert(html.includes('grade'+grade+'-flashcards.html?'));
   assert(html.includes('grade'+grade+'-games.html?'));
   assert(!/coming soon/i.test(html));
  }
 }finally{Object.assign(globalThis,previous);}
});
