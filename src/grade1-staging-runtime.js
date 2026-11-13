/* Emitted only by the explicit branch-only Grade 1 staging build.
   Banks are registered UNVERIFIED. No source or production manifest is promoted. */
(function(G){
 'use strict';
 var A=G.MK_QUESTION_BANKS,L=G.MK_BANK_LOADER;
 if(!A||!L||!G.document.currentScript)throw Error('Grade 1 staging dependencies missing');
 var base=new URL('.',G.document.currentScript.src),requests={},manifest;
 var C=G.MK_COURSE_CATALOG,records=C.getSkillRecords;
 C.getSkillRecords=function(c,u){
  var found=records.call(C,c,u);
  return scoped(c)&&!found.length?records.call(C,c==='math1'?'grade1':'math1',u):found;
 };
 var originalAvailable=A.available,originalSelect=A.select,all=L.loadFromSite,one=L.loadUnitFromSite;
 function scoped(c){return c==='grade1'||c==='math1';}
 function read(url){return G.fetch(new URL(url,base)).then(function(r){if(!r.ok)throw Error('Staging resource unavailable: '+url);return r.json();});}
 function entries(){return manifest||(manifest=Promise.all([read('manifest.json'),read('content-index.json')]).then(function(results){
  var m=results[0];G.MK_GRADE1_STAGING.content=results[1];
  if(m.staging!==true||m.banks.length!==8||Object.keys(results[1]).length!==8370||m.banks.some(function(b){return b.approved!==false||b.courseId!=='math1';}))throw Error('Invalid unapproved Grade 1 staging manifest');return m.banks;
 }));}
 function ensure(id){
  if(!requests[id])requests[id]=entries().then(function(es){var e=es.find(function(b){return b.unitId===id;});if(!e)throw Error('Unknown Grade 1 staging unit');return read(e.path);}).then(function(bank){
   if(bank.courseId!=='math1'||bank.unitId!==id)throw Error('Grade 1 staging bank mismatch');
   var adapted=JSON.parse(JSON.stringify(bank));adapted.courseId='grade1';
   [bank,adapted].forEach(function(b){if(originalAvailable(b.courseId,id,{includeUnverified:true}))return;var result=A.register(b,{verified:false});if(!result.ok)throw Error(result.errors.join('; '));});
   return id;
  });
  return requests[id];
 }
 A.available=function(c,u,o){return originalAvailable(c,u,scoped(c)?{includeUnverified:true}:o);};
 A.select=function(o){return originalSelect(scoped(o&&o.courseId)?Object.assign({},o,{includeUnverified:true}):o);};
 L.loadUnitFromSite=function(c,u){return scoped(c)?ensure(u).then(function(){return [c+'/'+u];}):one.apply(L,arguments);};
 L.loadFromSite=function(){var args=arguments;return Promise.all([all.apply(L,args),entries().then(function(es){return Promise.all(es.map(function(e){return ensure(e.unitId);}));})]).then(function(results){return results[0].concat(results[1].map(function(u){return 'grade1/'+u;}));});};
 G.MK_GRADE1_STAGING={ready:function(){return entries().then(function(es){return Promise.all(es.map(function(e){return ensure(e.unitId);}));});},originalAvailable:originalAvailable};
 function notice(){var p=G.document.createElement('p');p.id='grade1-staging-notice';p.textContent='Grade 1 development preview';p.style.cssText='padding:10px 20px;margin:8px auto;max-width:1200px;background:#fff4d6;color:#302a20;border-radius:8px';G.document.body.prepend(p);}
 if(G.document.readyState==='loading')G.document.addEventListener('DOMContentLoaded',notice);else notice();
})(window);
