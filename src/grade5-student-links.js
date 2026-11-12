/* Build shareable Grade 5 student destinations without exposing teacher guide
   links in the course UI. Public static files remain public; student=1 is a
   display mode, not an authentication/permission boundary. */
(function (G) {
  'use strict';
  var levels = { cp2: 'Remedial', cp1: 'Standard', honors: 'Advanced' };
  function hasLevel(resource) {
    return resource.type === 'Game' || resource.type === 'Project' || resource.type === 'Printable' ||
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
    if (resource.type === 'Game' || resource.type === 'Printable' ||
       (resource.type === 'Study Guide' && resource.title !== 'Cheat Sheet') ||
        resource.type === 'Interactive') {
      url.searchParams.set('student','1');
      if (resource.type !== 'Printable') url.searchParams.delete('mode'); // preserve generator type
      url.searchParams.delete('present');
      if (hasLevel(resource)) url.searchParams.set('level',level);
    }
    return url.href;
  }
  function chooseSkills(resource, level, base) {
    var path = resource && resource.path || '';
    var filterable = (resource.type === 'Game' && !/[?&]game=fraction-frenzy(?:&|$)/.test(path)) ||
      (resource.type === 'Study Guide' && resource.title === 'Understanding Check') ||
      resource.type === 'Printable';
    if (!filterable) return false;
    var unit = new URL(path, base || G.location.href).searchParams.get('unit');
    var records = G.MK_COURSE_CATALOG && G.MK_COURSE_CATALOG.getSkillRecords('math5',unit);
    if (!records || !records.length) { G.alert('Skills for this unit are unavailable.'); return true; }
    var d = G.document, dialog = d.createElement('dialog');
    dialog.setAttribute('aria-label','Choose skills and generate student link');
    dialog.style.cssText='width:min(620px,94vw);max-height:90vh;overflow:auto;box-sizing:border-box;padding:22px;border:2px solid #3456d1;border-radius:14px;color:#17233b;background:#fff';
    var h=d.createElement('h2');h.textContent='Choose skills for this activity';dialog.appendChild(h);
    var p=d.createElement('p');p.textContent=resource.title+' · Select the skills students should practice.';dialog.appendChild(p);
    var controls=d.createElement('div');dialog.appendChild(controls);
    var fieldset=d.createElement('fieldset'),legend=d.createElement('legend');legend.textContent='Unit skills';fieldset.appendChild(legend);
    var checks=records.map(function(skill){var label=d.createElement('label'),check=d.createElement('input');check.type='checkbox';check.value=skill.id;check.checked=true;label.style.cssText='display:flex;gap:10px;padding:8px';label.append(check,d.createTextNode(skill.name));fieldset.appendChild(label);return check;});
    dialog.appendChild(fieldset);
    var status=d.createElement('p');status.setAttribute('role','status');dialog.appendChild(status);
    var results=d.createElement('div');dialog.appendChild(results);
    function btn(name,parent,fn){var b=d.createElement('button');b.type='button';b.textContent=name;b.className='btn';b.style.margin='6px';b.onclick=fn;parent.appendChild(b);return b;}
    var submit=btn('Generate student link',dialog,function(){
      var ids=checks.filter(function(c){return c.checked;}).map(function(c){return c.value;});if(!ids.length)return;
      var url=new URL(destination(resource,level,base));url.searchParams.set('skills',JSON.stringify(ids));
      results.replaceChildren();var note=d.createElement('p');note.textContent=ids.length+' of '+records.length+' skills selected.';results.appendChild(note);
      var input=d.createElement('input');input.readOnly=true;input.value=url.href;input.setAttribute('aria-label','Student link');input.style.cssText='width:100%;box-sizing:border-box;padding:9px';results.appendChild(input);
      btn('Copy student link',results,function(){if(G.navigator.clipboard&&G.navigator.clipboard.writeText)G.navigator.clipboard.writeText(url.href).then(function(){status.textContent='Student link copied!';},function(){input.select();});else input.select();});input.focus();input.select();
    });
    function update(){var n=checks.filter(function(c){return c.checked;}).length;status.textContent=n+' of '+records.length+' skills selected';submit.disabled=!n;}
    btn('Select All',controls,function(){checks.forEach(function(c){c.checked=true;});update();});
    btn('Clear All',controls,function(){checks.forEach(function(c){c.checked=false;});update();});
    checks.forEach(function(c){c.onchange=update;});
    btn('Cancel',dialog,function(){dialog.close();});dialog.onclose=function(){dialog.remove();};d.body.appendChild(dialog);update();dialog.showModal();return true;
  }
  G.MK_GRADE5_STUDENT_LINKS = {
    levels: levels, hasLevel: hasLevel, destination: destination, chooseSkills: chooseSkills
  };
})(typeof window!=='undefined'?window:globalThis);
