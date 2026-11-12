#!/usr/bin/env node
/* Dynamic route smoke test using the real catalog and application source.
 * This simulates DOM plumbing; it is NOT a substitute for graphical browser tests.
 */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),out=path.join(root,'_site');
const read=(name)=>fs.readFileSync(path.join(out,name),'utf8');
function node(id){
 return {id,innerHTML:'',textContent:'',value:'',hidden:false,style:{},
  appendChild(){},addEventListener(){},querySelector(){return null},
  querySelectorAll(){return []},focus(){},getAttribute(){return null},
  setAttribute(){},classList:{add(){},remove(){}}};
}
const elements=Object.create(null);
const get=id=>elements[id]||(elements[id]=node(id));
const document={
 title:'',referrer:'',getElementById:get,querySelector(){return get('site-bar')},
 querySelectorAll(){return []},createElement(){return node('created')},
 addEventListener(){},body:get('body'),documentElement:get('html')
};
const location={hash:'',href:'https://mrksclassroom.com/',origin:'https://mrksclassroom.com'};
const storage={getItem(){return null},setItem(){}};
const win={document,location,addEventListener(){},scrollTo(){}};
const ctx={window:win,document,location,localStorage:storage,sessionStorage:storage,
 navigator:{},history:{length:1},URL,URLSearchParams,setTimeout(){},console};
vm.createContext(ctx);
for(const f of ['data.js','course-catalog.js','unit-specific-arcade.js',
 'resource-standards.js','resource-eligibility.js','skill-crosswalk.js']){
 vm.runInContext(read(f),ctx,{filename:f,timeout:15000});
}
assert(win.LIBRARY&&Array.isArray(win.LIBRARY.courses),'Missing application course catalog');
const courses=win.LIBRARY.courses.map(c=>({id:c.id,name:c.name,units:c.units.map(u=>({id:u.id,name:u.name}))}));
assert.equal(courses.length,11,'Expected eleven courses');
const keys=courses.flatMap(c=>c.units.map(u=>[c.id,u.id,u.name]));
assert.equal(keys.length,102,'Expected 102 units');
const appSource=read('app.js');
let checked=0,views=0,broken=[];
function check(route,label){
 location.hash=route?'#'+route:'';
 try{
  vm.runInContext(appSource,ctx,{filename:'app.js',timeout:20000});
  const html=get('main').innerHTML||'';
  assert(html.includes('<h1'), 'Missing heading');
  if(label)assert(html.includes(label.slice(0,4)), 'Missing expected course/unit text: '+label);
  for(const m of html.matchAll(/href="([^"<>]+)"/g)){
   const href=m[1].replace(/&amp;/g,'&');
   if(/^(?:#|https?:|mailto:|tel:|data:)/i.test(href))continue;
   const pathname=href.split(/[?#]/)[0];
   if(!pathname)continue;
   const file=path.resolve(out,decodeURIComponent(pathname.replace(/^\//,'')));
   assert(file===out||file.startsWith(out+path.sep), 'Link escapes site: '+href);
   if(!fs.existsSync(file))broken.push({route:route||'home',url:href});
  }
  checked++;views++;
 }catch(error){broken.push({route:route||'home',error:error.message})}
}
check('','');
for(const c of courses)check(c.id,c.name);
for(const [courseId,unitId,name] of keys)check(courseId+'.'+unitId,name);
for(const t of ['activities','saved','activity.flashcards'])check(t,'');
const dedup=[...new Map(broken.map(x=>[JSON.stringify(x),x])).values()];
if(dedup.length){
 console.error('Dynamic routing failures:',JSON.stringify(dedup.slice(0,35),null,2));
 throw Error(dedup.length+' route errors or broken links');
}
assert.equal(checked,117,'Missing tested views');
console.log('PASS dynamic routing: '+courses.length+' courses, '+keys.length+' units, '+checked+' views, no broken rendered links');
