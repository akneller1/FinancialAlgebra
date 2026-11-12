/* Build shareable Grade 5 student destinations without exposing teacher guide
   links in the course UI. Public static files remain public; student=1 is a
   display mode, not an authentication/permission boundary. */
(function (G) {
  'use strict';
  var levels = { cp2: 'Remedial', cp1: 'Standard', honors: 'Advanced' };
  function hasLevel(resource) {
    return resource.type === 'Game' || resource.type === 'Project' ||
      (resource.type === 'Study Guide' && resource.title === 'Understanding Check');
  }
  function destination(resource, level, base) {
    if (!resource || typeof resource.path !== 'string') throw new Error('Missing activity');
    level = Object.prototype.hasOwnProperty.call(levels,level) ? level : 'cp1';
    var path = resource.path;
    if (resource.type === 'Project') {
      var match = /^math5-project-([a-z0-9-]+)\/index\.html$/.exec(path);
      if (!match) throw new Error('Unknown project location');
      path = 'math5-project-' + match[1] + '/' + match[1] + '-' + level + '.pdf';
    }
    var url = new URL(path,base||G.location.href);
    if (resource.type === 'Game' ||
       (resource.type === 'Study Guide' && resource.title !== 'Cheat Sheet') ||
        resource.type === 'Interactive') {
      url.searchParams.set('student','1');
      url.searchParams.delete('mode'); // student share never starts in teacher mode
      url.searchParams.delete('present');
      if (hasLevel(resource)) url.searchParams.set('level',level);
    }
    return url.href;
  }
  function chooseSkills(resource,level,base) {
    var path=resource.path||'';
    var filterable=(resource.type==='Game' && !/[?&]game=fraction-frenzy(?:&|$)/.test(path)) ||
      (resource.type==='Study Guide' && resource.title==='Understanding Check');
    if(!filterable)return false;
    var unit=new URL(path,base||G.location.href).searchParams.get('unit');
    var records=G.MK_COURSE_CATALOG && G.MK_COURSE_CATALOG.getSkillRecords('math5',unit);
    if(!records||!records.length){G.alert('Skills for this unit are unavailable.');return true;}
    var d=G.document,dialog=d.createElement('dialog');
    dialog.style.cssText='width:min(620px,94vw);max-height:90vh;overflow:auto;box-sizing:border-box;padding:22px;border:2px solid #3456d1;border-radius:14px;color:#17233b;background:#fff';
    dialog.setAttribute('aria-label','Choose skills and generate student link');
    var title=d.createElement('h2');title.textContent='Choose skills for this activity';dialog.appendChild(title);
    var p=d.createElement('p');p.textContent=resource.title+' · Select the skills students should practice.';dialog.appendChild(p);
    var bar=d.createElement('div');dialog.appendChild(bar);
    var list=d.createElement('fieldset'),legend=d.createElement('legend');legend.textContent='Unit skills';list.appendChild(legend);
    var checks=records.map(function(skill){var label=d.createElement('label'),check=d.createElement('input');check.type='checkbox';check.value=skill.id;check.checked=true;label.style.cssText='display:flex;gap:10px;padding:8px';label.append(check,d.createTextNode(skill.name));list.appendChild(label);return check;});
    dialog.appendChild(list);
    var status=d.createElement('p');status.setAttribute('role','status');dialog.appendChild(status);
    var results=d.createElement('div');dialog.appendChild(results);
    function addButton(name,parent,fn){var btn=d.createElement('button');btn.type='button';btn.textContent=name;btn.className='btn';btn.style.margin='6px';btn.onclick=fn;parent.appendChild(btn);return btn;}
    var generate=addButton('Generate student link',dialog,function(){
      var ids=checks.filter(function(c){return c.checked;}).map(function(c){return c.value;});if(!ids.length)return;
      var url=new URL(destination(resource,level,base));url.searchParams.set('skills',JSON.stringify(ids));
      results.replaceChildren();
      var note=d.createElement('p');note.textContent=ids.length+' of '+records.length+' skills selected.';results.appendChild(note);
      var field=d.createElement('input');field.readOnly=true;field.value=url.href;field.setAttribute('aria-label','Student link');field.style.cssText='width:100%;box-sizing:border-box;padding:9px';results.appendChild(field);
      addButton('Copy student link',results,function(){if(G.navigator.clipboard&&G.navigator.clipboard.writeText)G.navigator.clipboard.writeText(url.href).then(function(){status.textContent='Student link copied!';},function(){field.select();});else field.select();});
      field.focus();field.select();
    });
    function update(){var n=checks.filter(function(c){return c.checked;}).length;status.textContent=n+' of '+records.length+' skills selected';generate.disabled=!n;}
    addButton('Select All',bar,function(){checks.forEach(function(c){c.checked=true;});update();});
    addButton('Clear All',bar,function(){checks.forEach(function(c){c.checked=false;});update();});
    checks.forEach(function(c){c.onchange=update;});
    addButton('Cancel',dialog,function(){dialog.close();});
    dialog.onclose=function(){dialog.remove();};d.body.appendChild(dialog);update();dialog.showModal();return true;
  }
  G.MK_GRADE5_STUDENT_LINKS = {
    levels: levels, hasLevel: hasLevel, destination: destination, chooseSkills: chooseSkills
  };
})(typeof window!=='undefined'?window:globalThis);
