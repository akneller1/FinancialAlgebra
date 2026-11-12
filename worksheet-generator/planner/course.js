/* Daily Lesson Planner course selector.
   The same planner UI and exports serve Algebra 1, Geometry, and Algebra 2. */
(function (G) {
  'use strict';
  var h = {};
  try { (G.location && G.location.hash || '').replace(/^#/, '').split('&').forEach(function (kv) { var p = kv.split('='); if (p[0]) h[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || ''); }); } catch (e) { /* no location */ }
  var mid = ['prealgebra', 'prealgebra7', 'math6', 'math5'].filter(function (c) { return (h.course === c || new RegExp('^' + c + '-').test(h.unit || '')) && G['MKPLAN_SCOPE_' + c.toUpperCase()]; })[0];
  var hs = mid ? null : ['precalculus', 'calculus', 'statistics', 'discrete'].filter(function (c) { return (h.course === c || new RegExp('^' + c + '-').test(h.unit || '')) && G['MKPLAN_SCOPE_' + c.toUpperCase()]; })[0];
  var pa8 = !!mid;
  var a2 = (h.course === 'algebra2' || /^algebra2-/.test(h.unit || '')) && G.MKPLAN_SCOPE_ALGEBRA2 && G.MKPLAN_SKILLS_ALGEBRA2;
  var geo = !a2 && (h.course === 'geometry' || /^geometry-/.test(h.unit || '')) && G.MKPLAN_SCOPE_GEOMETRY && G.MKPLAN_SKILLS_GEOMETRY;
  G.MKPLAN_COURSE = pa8 ? mid : hs ? hs : a2 ? 'algebra2' : geo ? 'geometry' : 'algebra1';
  if (hs) { G.MKPLAN_SCOPE = G['MKPLAN_SCOPE_' + hs.toUpperCase()]; G.MKPLAN_SKILLS = G['MKPLAN_SKILLS_' + hs.toUpperCase()]; return; }   // high-school courses keep the CP2 / CP1 / Honors labels
  if (pa8) { G.MKPLAN_SCOPE = G['MKPLAN_SCOPE_' + mid.toUpperCase()]; G.MKPLAN_SKILLS = G['MKPLAN_SKILLS_' + mid.toUpperCase()]; Object.keys(G.MKMENU.LEVELS).forEach(function(k){var name={cp2:'Remedial',cp1:'Standard',honors:'Advanced'}[k];G.MKMENU.LEVELS[k].name=name;G.MKMENU.LEVELS[k].long=name;}); }
  else if (a2) { G.MKPLAN_SCOPE = G.MKPLAN_SCOPE_ALGEBRA2; G.MKPLAN_SKILLS = G.MKPLAN_SKILLS_ALGEBRA2; }
  else if (geo) { G.MKPLAN_SCOPE = G.MKPLAN_SCOPE_GEOMETRY; G.MKPLAN_SKILLS = G.MKPLAN_SKILLS_GEOMETRY; }
})(typeof window !== 'undefined' ? window : globalThis);

