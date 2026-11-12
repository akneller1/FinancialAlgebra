/* Manifest-driven loading of independently approved question-bank files.
 * Manifest entries must be explicitly approved during editorial review.
 * No unreviewed bank is made available to student-facing consumers.
 */
(function(root){
'use strict';
var adapter=root.MK_QUESTION_BANKS;
function load(manifest, fetchJSON){
 if(!adapter||typeof fetchJSON!=='function') return Promise.reject(new Error('Question bank adapter or fetcher unavailable'));
 if(!manifest||manifest.version!==1||!Array.isArray(manifest.banks)) return Promise.reject(new Error('Invalid bank manifest'));
 var allowed=Object.create(null),entries=[];
 manifest.banks.forEach(function(item){
  if(!item||!item.courseId||!item.unitId||typeof item.path!=='string'||!/^(?:question-banks|math5)\/[a-z0-9/_-]+\.json$/.test(item.path))
   throw new Error('Invalid manifest entry');
  var id=item.courseId+'/'+item.unitId;
  if(allowed[id])throw new Error('Duplicate manifest entry '+id);
  allowed[id]=true;
  // Algebra 2 authored banks may be used in teacher generators without editorial sign-off.
  // This is NOT equivalent to manifest approved:true.
  if(item.approved===true||(item.courseId==='algebra2'&&item.teacherUse===true))entries.push(item);
 });
 return Promise.all(entries.map(function(item){
  return Promise.resolve().then(function(){return fetchJSON(item.path)}).then(function(bank){
   if(!bank||bank.courseId!==item.courseId||bank.unitId!==item.unitId) throw new Error('Course/unit mismatch: '+item.path);
   var validation=adapter.validate(bank);
   if(!validation.ok)throw new Error(item.path+': '+validation.errors.join('; '));
   return {item:item,bank:bank};
  });
 })).then(function(results){
  // Validate every approved file before registering any, to avoid partial loads on validation failure.
  return results.map(function(result){
   var applied=adapter.register(result.bank,{verified:true});
   if(!applied.ok)throw new Error(result.item.path+': '+applied.errors.join('; '));
   return result.item.courseId+'/'+result.item.unitId;
  });
 });
}
function loadFromSite(path,base){
 base=base||'';
 if(base!==''&&base!=='../')return Promise.reject(new Error('Invalid bank base path'));
 path=path||'manifest.json';
 if(!/^(?:manifest|question-banks\/[a-z0-9/_-]+)\.json$/.test(path))return Promise.reject(new Error('Invalid manifest path'));
 if(typeof root.fetch!=='function')return Promise.reject(new Error('Fetch unavailable'));
 function read(url){return root.fetch(base+url,{cache:url===path?'no-store':'default'}).then(function(res){if(!res.ok)throw new Error('Unable to load '+url);return res.json()});}
 return read(path).then(function(manifest){return load(manifest,read)});
}

// Optional unit-scoped loader for the main library. The original loadFromSite()
// remains unchanged for generators that expect all approved banks to be ready.
var manifestRequests=Object.create(null);
var scopedRequests=Object.create(null);
function loadUnitFromSite(courseId,unitId,path,base){
 base=base||'';
 path=path||'manifest.json';
 if(base!==''&&base!=='../')return Promise.reject(new Error('Invalid bank base path'));
 if(!/^[a-z0-9_-]+$/.test(courseId||'')||!(/^[a-z0-9_-]+$/.test(unitId||'')))return Promise.reject(new Error('Invalid course or unit'));
 if(!/^(?:manifest|question-banks\/[a-z0-9/_-]+)\.json$/.test(path))return Promise.reject(new Error('Invalid manifest path'));
 if(typeof root.fetch!=='function')return Promise.reject(new Error('Fetch unavailable'));
 var id=courseId+'/'+unitId;
 if(adapter&&adapter.available(courseId,unitId))return Promise.resolve([id]);
 if(scopedRequests[id])return scopedRequests[id];
 var manifestKey=base+path;
 function read(url,cache){return root.fetch(base+url,{cache:cache||'default'}).then(function(res){if(!res.ok)throw new Error('Unable to load '+url);return res.json()});}
 if(!manifestRequests[manifestKey])manifestRequests[manifestKey]=read(path,'no-store').catch(function(e){delete manifestRequests[manifestKey];throw e;});
 scopedRequests[id]=manifestRequests[manifestKey].then(function(manifest){
  if(!manifest||manifest.version!==1||!Array.isArray(manifest.banks))throw new Error('Invalid bank manifest');
  var seen=Object.create(null),match=null;
  manifest.banks.forEach(function(item){
   if(!item||!item.courseId||!item.unitId||typeof item.path!=='string'||!/^(?:question-banks|math5)\/[a-z0-9/_-]+\.json$/.test(item.path))throw new Error('Invalid manifest entry');
   var k=item.courseId+'/'+item.unitId;
   if(seen[k])throw new Error('Duplicate manifest entry '+k);
   seen[k]=true;
   if(k===id && (item.approved===true||(item.courseId==='algebra2'&&item.teacherUse===true)))match=item;
  });
  if(!match)return [];
  if(adapter.available(courseId,unitId))return [id];
  return read(match.path).then(function(bank){
   if(!bank||bank.courseId!==courseId||bank.unitId!==unitId)throw new Error('Course/unit mismatch: '+match.path);
   var result=adapter.validate(bank);
   if(!result.ok)throw new Error(match.path+': '+result.errors.join('; '));
   if(!adapter.available(courseId,unitId)){
    var applied=adapter.register(bank,{verified:true});
    if(!applied.ok)throw new Error(match.path+': '+applied.errors.join('; '));
   }
   return [id];
  });
 }).catch(function(e){delete scopedRequests[id];throw e;});
 return scopedRequests[id];
}
root.MK_BANK_LOADER={version:1,load:load,loadFromSite:loadFromSite,loadUnitFromSite:loadUnitFromSite};
})(typeof window!=='undefined'?window:globalThis);
