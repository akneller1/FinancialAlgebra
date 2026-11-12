/* Shared, read-only question bank adapter.
 * No grade-specific math, diagrams, or question generation lives here.
 * A bank is NOT student-ready unless explicitly marked verified after external review.
 */
(function (root) {
  'use strict';
  var catalog = root.MK_COURSE_CATALOG;
  var banks = Object.create(null);
  var FORMATS = ['short-answer', 'multiple-choice', 'select-all', 'open-response'];
  var LEVELS = ['cp2', 'cp1', 'honors'];
  function copy(value) { return JSON.parse(JSON.stringify(value)); }
  function key(courseId, unitId) { return courseId + '/' + unitId; }
  function validate(bank) {
    var errors = [], seen = Object.create(null);
    if (!bank || typeof bank !== 'object' || bank.schemaVersion !== 1) errors.push('Expected schema version 1.');
    if (!bank || !catalog || !catalog.getSkillRecords) return { ok: false, errors: errors.concat('Course catalog unavailable.') };
    var records = catalog.getSkillRecords(bank.courseId, bank.unitId);
    if (!records.length) errors.push('Unknown course or unit.');
    var skills = Object.create(null);
    records.forEach(function (s) { skills[s.id] = true; });
    if (!Array.isArray(bank.questions)) errors.push('questions must be an array.');
    (Array.isArray(bank.questions) ? bank.questions : []).forEach(function (q, i) {
      var where = 'questions[' + i + ']';
      if (!q || typeof q !== 'object') { errors.push(where + ' invalid'); return; }
      if (typeof q.id !== 'string' || !q.id.trim() || seen[q.id]) errors.push(where + ' missing/duplicate id');
      seen[q.id] = true;
      if (!skills[q.skillId]) errors.push(where + ' unknown skillId');
      if (LEVELS.indexOf(q.level) < 0) errors.push(where + ' invalid level');
      if (FORMATS.indexOf(q.format) < 0) errors.push(where + ' invalid format');
      if (typeof q.prompt !== 'string' || !q.prompt.trim()) errors.push(where + ' missing prompt');
      if (q.answer === undefined || q.answer === null) errors.push(where + ' missing answer');
      if (!Array.isArray(q.solutionSteps) || !q.solutionSteps.length) errors.push(where + ' missing worked steps');
      if (q.format === 'multiple-choice' || q.format === 'select-all') {
        var choices = Array.isArray(q.options) ? q.options : [];
        var n = choices.filter(function (o) { return o && o.correct === true; }).length;
        if (choices.length < 2 || (q.format === 'multiple-choice' && n !== 1) || (q.format === 'select-all' && n < 2)) errors.push(where + ' invalid choices');
      }
      if (q.format === 'open-response' && (!Array.isArray(q.parts) || q.parts.length < 4)) errors.push(where + ' needs four parts');
      if (q.diagram) {
        var d=q.diagram, spec=d.spec||{};
        if (d.type==='image') {
          if (typeof spec.src!=='string' || !spec.src.startsWith('question-banks/assets/') || !/^[a-zA-Z0-9_/-]+[.](png|jpg|jpeg|webp)$/.test(spec.src.slice('question-banks/assets/'.length)) || spec.src.includes('..') || typeof spec.alt!=='string' || !spec.alt.trim())
            errors.push(where+' invalid local image diagram');
        } else if (['svg','coordinate-plane','number-line','geometry-figure'].indexOf(d.type)<0)
          errors.push(where+' unsupported diagram type');
      }
    });
    return { ok: !errors.length, errors: errors };
  }
  function register(bank, opts) {
    var result = validate(bank);
    if (!result.ok) return result;
    var k = key(bank.courseId, bank.unitId);
    if (banks[k]) return { ok: false, errors: ['Bank already registered: ' + k] };
    banks[k] = { data: copy(bank), verified: !!(opts && opts.verified === true) };
    return { ok: true, errors: [], verified: banks[k].verified };
  }
  function available(courseId, unitId, opts) {
    var b = banks[key(courseId, unitId)];
    if (!b) return false;
    return !!(b.verified || (opts && opts.includeUnverified === true));
  }
  function select(options) {
    options = options || {};
    var b = banks[key(options.courseId, options.unitId)];
    if (!b || (!b.verified && options.includeUnverified !== true)) return [];
    var acceptedSkills = options.skillIds && options.skillIds.length ? options.skillIds : null;
    var acceptedFormats = options.formats && options.formats.length ? options.formats : null;
    var questions = b.data.questions.filter(function (q) {
      return (!options.level || q.level === options.level) &&
        (!acceptedSkills || acceptedSkills.indexOf(q.skillId) >= 0) &&
        (!acceptedFormats || acceptedFormats.indexOf(q.format) >= 0);
    });
    return copy(typeof options.limit === 'number' && options.limit >= 0 ? questions.slice(0, options.limit) : questions);
  }
  function coverage(courseId, unitId) {
    var skillRecords = catalog ? catalog.getSkillRecords(courseId, unitId) : [];
    var b = banks[key(courseId, unitId)];
    return skillRecords.map(function (skill) {
      var counts = { cp2: 0, cp1: 0, honors: 0 };
      if (b) b.data.questions.forEach(function (q) { if (q.skillId === skill.id && Object.prototype.hasOwnProperty.call(counts, q.level)) counts[q.level]++; });
      return { id: skill.id, name: skill.name, counts: counts, verified: !!(b && b.verified) };
    });
  }
  root.MK_QUESTION_BANKS = { version: 1, validate: validate, register: register, available: available, select: select, coverage: coverage };
})(typeof window !== 'undefined' ? window : globalThis);
