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
  G.MK_GRADE5_STUDENT_LINKS = {
    levels: levels, hasLevel: hasLevel, destination: destination
  };
})(typeof window!=='undefined'?window:globalThis);
