/* Shared curriculum discovery for generator unit selectors.
   Exposes NEW grade-level courses without manufacturing question banks.
   A unit becomes selectable only after its MKMENU skill set is actually registered. */
(function (G) {
  'use strict';
  var ns = G.MKMENU, library = G.LIBRARY, catalog = G.MK_COURSE_CATALOG;
  if (!ns || !Array.isArray(ns.CATALOG) || !library || !catalog) return;
  var courseIds = ['math5', 'math6', 'prealgebra7', 'prealgebra', 'algebra2', 'precalculus', 'calculus', 'statistics', 'discrete'];
  var seen = Object.create(null);
  ns.CATALOG.forEach(function (group) { group.units.forEach(function (u) { seen[u[0]] = true; }); });
  var insertAt = 0;
  courseIds.forEach(function (id) {
    var course = library.courses.filter(function (c) { return c.id === id; })[0];
    if (!course) return;
    var existingGroup = ns.CATALOG.filter(function (g) { return g.course === course.name; })[0];
    if (id === 'algebra2' && existingGroup) {   // every Algebra 2 unit, in course order, labelled like the other courses
      existingGroup.units = course.units.map(function (unit, i) { seen['algebra2-' + unit.id] = true; return ['algebra2-' + unit.id, 'Unit ' + (i + 1) + ' · ' + unit.name]; });
      return;
    }
    var units = course.units.map(function (unit, i) {
      var bankId = (id === 'algebra2' ? 'algebra2-' : id + '-') + unit.id;
      return [bankId, 'Unit ' + (i + 1) + ' · ' + unit.name];
    }).filter(function (u) { return !seen[u[0]]; });
    if (units.length) {
      if (existingGroup) existingGroup.units = existingGroup.units.concat(units);
      else ns.CATALOG.splice(insertAt++, 0, { course: course.name, units: units });
      units.forEach(function (u) { seen[u[0]] = true; });
    }
  });
  ns.courseBridge = { version: 1, registeredCourses: courseIds.slice() };
})(typeof window !== 'undefined' ? window : globalThis);

