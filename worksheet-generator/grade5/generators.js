/* Grade 5 generator controller: unit/skill selection, customization, paginated
   student handout and teacher key previews, printing, and question review. */
(function (G) {
  'use strict';
  var doc = G.document, C = G.G5_GENERATORS_CORE, R = G.G5_GENERATORS_RENDER;
  var Content = G.G5_GENERATOR_CONTENT || { units: {}, themes: {} };
  var P = new URLSearchParams(G.location.search);
  var MODES = { lesson: 'Lesson Plan', worksheet: 'Worksheet', assessment: 'Assessment', activity: 'Activity' };
  var $ = function (id) { return doc.getElementById(id); };
  var STUDENT = P.get('student') === '1';
  var state = { mode: 'lesson', unitId: '', unit: null, course: null, opts: null, plan: null, audience: 'student', zoom: 100, build: 0 };
  var editTimer;

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function readPrefs() {
    try { return JSON.parse(G.localStorage.getItem('g5-generator-options-v1') || '{}'); } catch (e) { return {}; }
  }
  function savePrefs() {
    try {
      G.localStorage.setItem('g5-generator-options-v1', JSON.stringify({
        level: state.opts.level, notes: state.opts.notes, worked: state.opts.worked, space: state.opts.space,
        theme: state.opts.theme, showName: state.opts.showName, showStandards: state.opts.showStandards,
        sections: state.opts.sections, duration: state.opts.duration
      }));
    } catch (e) {}
  }
  function field(id, label, control) { return '<div class="g5gen-field"><label for="' + id + '">' + label + '</label>' + control + '</div>'; }
  function select(id, choices, value) {
    return '<select id="' + id + '">' + choices.map(function (x) {
      var v = Array.isArray(x) ? x[0] : x, l = Array.isArray(x) ? x[1] : x;
      return '<option value="' + esc(v) + '"' + (String(v) === String(value) ? ' selected' : '') + '>' + esc(l) + '</option>';
    }).join('') + '</select>';
  }
  function numeric(id, value, min, max) { return '<input id="' + id + '" type="number" min="' + min + '" max="' + max + '" step="1" value="' + value + '">'; }
  function check(id, label, on) { return '<label class="g5gen-check"><input type="checkbox" id="' + id + '"' + (on ? ' checked' : '') + '><span>' + label + '</span></label>'; }
  function unitInfo(id) {
    var c = state.course, u = c.units.filter(function (x) { return x.id === id; })[0];
    return { unit: u, number: c.units.indexOf(u) + 1 };
  }
  function modeLabel() {
    if (state.mode !== 'activity') return MODES[state.mode];
    return 'Activity · ' + (C.ACTIVITIES[state.opts.activity] || C.ACTIVITIES.maze).name;
  }

  function renderControls() {
    var u = state.unit, o = state.opts, info = unitInfo(u.id);
    doc.title = modeLabel() + ' · ' + u.name + ' | Grade 5 Generators';
    var h = '<div class="g5gen-card"><h1>Grade 5 Generators</h1><p class="g5gen-hint">5th Grade Math · ' + info.number + ' of 11 units · approved question bank</p>' +
      '<div class="g5gen-tabs" aria-label="Generator type">' + Object.keys(MODES).map(function (k) {
        return '<button type="button" class="g5gen-tab" data-mode="' + k + '" aria-pressed="' + (state.mode === k) + '">' + MODES[k] + '</button>';
      }).join('') + '</div>' +
      field('unit', 'Unit', select('unit', state.course.units.map(function (x) { return [x.id, x.name]; }), u.id)) +
      field('level', 'Level', select('level', [['cp2', 'Remedial'], ['cp1', 'Standard'], ['honors', 'Advanced'], ['mixed', 'Mixed levels']], o.level)) +
      '<p class="g5gen-hint">Use with <a href="grade5-games.html?unit=' + encodeURIComponent(u.id) + '">games</a> · <a href="grade5-flashcards.html?unit=' + encodeURIComponent(u.id) + '">flashcards</a> · <a href="grade5-understanding-check.html?unit=' + encodeURIComponent(u.id) + '">Understanding Check</a> · <a href="../grade5.html#math5.' + encodeURIComponent(u.id) + '">unit page</a></p></div>';

    h += '<div class="g5gen-card"><h2><span class="g5gen-step">1</span> Choose skills</h2><p class="g5gen-hint">Every question comes from the approved Grade 5 bank for these skills.</p><div class="g5gen-skills">' +
      u.skills.map(function (s) { return '<label class="g5gen-check"><input type="checkbox" data-skill="' + esc(s.id) + '"' + (o.skills.indexOf(s.id) >= 0 ? ' checked' : '') + '><span>' + esc(s.name) + '</span></label>'; }).join('') +
      '</div><button class="g5gen-linkbtn" type="button" data-all-skills="1">Select all</button><button class="g5gen-linkbtn" type="button" data-all-skills="0">Clear</button></div>';

    h += '<div class="g5gen-card"><h2><span class="g5gen-step">2</span> Handout options</h2>';
    if (state.mode === 'lesson') {
      h += field('duration', 'Lesson length', select('duration', [[30, '30 minutes'], [45, '45 minutes'], [60, '60 minutes'], [90, '90 minutes']], o.duration)) +
        field('notesMode', 'Student notes', select('notesMode', [['completed', 'Completed notes'], ['guided', 'Guided notes — fill in the blanks'], ['blank', 'Blank note organizer']], o.notes)) +
        check('worked', 'Show worked example steps on the student copy', o.worked) +
        '<p class="g5gen-hint">Practice and exit-ticket answers stay on the teacher key.</p>';
    } else if (state.mode === 'activity') {
      h += field('activityKind', 'Activity type', select('activityKind', Object.keys(C.ACTIVITIES).map(function (k) { return [k, C.ACTIVITIES[k].icon + ' ' + C.ACTIVITIES[k].name]; }), o.activity)) +
        field('theme', 'Theme', select('theme', Object.keys(Content.themes || {}).map(function (k) { return [k, Content.themes[k].icon + ' ' + Content.themes[k].name]; }), o.theme)) +
        field('count', 'Problems', numeric('count', o.count, 6, 20)) +
        '<p class="g5gen-hint">' + esc((C.ACTIVITIES[o.activity] || C.ACTIVITIES.maze).blurb) + '</p>';
    } else {
      h += field('paperTitle', 'Handout title', '<input type="text" id="paperTitle" value="' + esc(o.title) + '" placeholder="Use the unit title">') +
        field('activityFormat', 'Content', select('activityFormat', Object.keys(C.FORMATS).map(function (k) { return [k, C.FORMATS[k]]; }), o.format)) +
        field('response', 'Question format', select('response', [['mixed', 'Mixed formats'], ['multiple-choice', 'Multiple choice'], ['short-answer', 'Short answer'], ['select-all', 'Select all'], ['open-response', 'Open response']], o.response)) +
        field('count', 'Questions', numeric('count', o.count, 1, 30));
      if (state.mode === 'assessment') {
        h += field('total', 'Total points', numeric('total', o.total, 10, 200)) + check('showPoints', 'Show point values', o.showPoints) +
          field('timeLimit', 'Time limit (minutes, optional)', '<input type="text" id="timeLimit" inputmode="numeric" value="' + esc(o.timeLimit) + '" placeholder="e.g. 40">');
      }
    }
    if (state.mode !== 'lesson') h += field('space', 'Work space', select('space', [['compact', 'Compact'], ['standard', 'Standard'], ['extra', 'Extra writing space']], o.space));
    h += check('showName', 'Include name / date line', o.showName) + check('showStandards', 'Show standards on the handout', o.showStandards) +
      field('version', 'Version', select('version', [['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D']], o.version)) +
      '<div class="g5gen-actions"><button type="button" class="g5gen-btn primary" id="generate">Generate ' + (state.mode === 'activity' ? 'activity' : state.mode === 'lesson' ? 'lesson plan' : state.mode) + '</button></div>' +
      '<p class="g5gen-hint">Version changes the question set. Options update the next handout when you press Generate.</p></div>';

    if (state.mode === 'lesson') {
      h += '<div class="g5gen-card"><h2><span class="g5gen-step">3</span> Include and arrange</h2><p class="g5gen-hint">Turn sections on or off, set problem counts, and change the order.</p>' +
        o.sections.map(function (s, i) {
          var meta = C.LESSON_SECTIONS.filter(function (x) { return x[0] === s.id; })[0] || [s.id, s.id];
          return '<div class="g5gen-section"><div class="g5gen-section-head"><label class="g5gen-check"><input type="checkbox" data-section="' + s.id + '"' + (s.on ? ' checked' : '') + '><span>' + esc(meta[1]) + '</span></label>' +
            '<button type="button" class="g5gen-btn sm ghost" data-move="' + i + '" data-dir="-1"' + (i === 0 ? ' disabled' : '') + ' aria-label="Move ' + esc(meta[1]) + ' up">↑</button>' +
            '<button type="button" class="g5gen-btn sm ghost" data-move="' + i + '" data-dir="1"' + (i === o.sections.length - 1 ? ' disabled' : '') + ' aria-label="Move ' + esc(meta[1]) + ' down">↓</button></div>' +
            (['warmup', 'teach', 'guided', 'practice', 'challenge', 'exit'].indexOf(s.id) >= 0 ? '<label class="g5gen-hint">Problems <input class="g5gen-section-count" type="number" min="0" max="20" data-section-count="' + s.id + '" value="' + s.count + '"></label>' : '') + '</div>';
        }).join('') + '</div>';
    }
    h += '<div class="g5gen-card g5gen-editor" id="questionEditor"><h2>Review questions</h2><p class="g5gen-hint">Generate a handout to review, replace or edit its questions.</p></div>';
    $('config').innerHTML = h;
    renderQuestionEditor();
  }

  function syncOptions() {
    var o = state.opts;
    function value(id, fallback) { return $(id) ? $(id).value : fallback; }
    o.skills = Array.prototype.map.call(doc.querySelectorAll('[data-skill]:checked'), function (e) { return e.dataset.skill; });
    o.level = value('level', o.level); o.duration = +value('duration', o.duration) || 60;
    o.notes = value('notesMode', o.notes); o.worked = $('worked') ? $('worked').checked : o.worked;
    o.title = value('paperTitle', o.title); o.format = value('activityFormat', o.format); o.response = value('response', o.response);
    o.count = C.clamp(value('count', o.count), 1, 30); o.total = C.clamp(value('total', o.total), 10, 200);
    o.space = value('space', o.space); o.showPoints = $('showPoints') ? $('showPoints').checked : o.showPoints;
    o.timeLimit = value('timeLimit', o.timeLimit); o.version = value('version', o.version);
    o.showName = $('showName') ? $('showName').checked : o.showName;
    o.showStandards = $('showStandards') ? $('showStandards').checked : o.showStandards;
    o.activity = value('activityKind', o.activity); o.theme = value('theme', o.theme);
    doc.querySelectorAll('[data-section]').forEach(function (e) { o.sections.find(function (s) { return s.id === e.dataset.section; }).on = e.checked; });
    doc.querySelectorAll('[data-section-count]').forEach(function (e) { o.sections.find(function (s) { return s.id === e.dataset.sectionCount; }).count = C.clamp(e.value, 0, 20); });
    if (state.mode === 'activity' && o.count < 6) o.count = 6;
    savePrefs();
  }

  function blocks() {
    if (!state.plan || state.plan.mode === 'activity') return [];
    return state.plan.sections.reduce(function (a, s) { return a.concat(s.blocks); }, []).filter(function (b) { return b.kind === 'question'; });
  }
  function renderQuestionEditor() {
    var host = $('questionEditor'); if (!host) return;
    var qs = blocks();
    if (!qs.length) { host.innerHTML = '<h2>Review questions</h2><p class="g5gen-hint">' + (state.plan && state.plan.mode === 'activity' ? 'Activity items are generated as a puzzle; regenerate with another version for a new set.' : 'Questions appear here after generation.') + '</p>'; return; }
    host.innerHTML = '<h2>Review questions</h2><p class="g5gen-hint">Edit a question if you change the numbers, also update its answer and worked solution.</p>' +
      qs.map(function (b, i) {
        var q = b.q;
        return '<details><summary>Question ' + (i + 1) + ' · ' + esc(C.plain(q.prompt).slice(0, 62)) + '</summary>' +
          '<label class="g5gen-label">Question wording<textarea data-edit="' + i + '">' + esc(q.prompt) + '</textarea></label>' +
          '<label class="g5gen-label">Answer<textarea data-answer="' + i + '">' + esc(C.answerText(q)) + '</textarea></label>' +
          '<label class="g5gen-label">Worked solution (one step per line)<textarea data-solution="' + i + '">' + esc((q.solutionSteps || []).join('\n')) + '</textarea></label>' +
          '<div class="g5gen-actions"><button class="g5gen-btn sm ghost" type="button" data-replace="' + i + '">New question</button>' +
          '<button class="g5gen-btn sm ghost" type="button" data-remove="' + i + '">Remove</button></div></details>';
      }).join('');
  }

  function previewTools() {
    var u = state.unit, teacher = state.audience === 'teacher';
    $('previewTools').innerHTML = '<div class="ptool g5gen-toolbar"><div><h2>' + esc(u.name) + '</h2><p class="g5gen-hint">' + esc(modeLabel()) + ' · Letter-size printable</p></div><span class="sp"></span>' +
      '<div class="g5gen-audience"><button type="button" class="g5gen-btn sm ghost" data-audience="student" aria-pressed="' + (!teacher) + '">Student handout</button>' +
      (STUDENT ? '' : '<button type="button" class="g5gen-btn sm ghost" data-audience="teacher" aria-pressed="' + teacher + '">Teacher key</button>') + '</div>' +
      '<label class="g5gen-zoom">Zoom ' + select('zoom', [[65, '65%'], [80, '80%'], [100, '100%'], [125, '125%']], state.zoom) + '</label>' +
      '<button class="g5gen-btn" type="button" data-print="student">Print student</button>' +
      (STUDENT ? '' : '<button class="g5gen-btn ghost" type="button" data-print="teacher">Print key</button>' +
      '<button class="g5gen-btn ghost sm" type="button" id="copyStudentLink">Copy student link</button>') + '</div>';
  }

  function makePages(teacher) {
    var html = R.render(state.plan, teacher);
    return G.MKPLAN.paginateStudent(html);
  }
  var previewTicket = 0, previewReady = Promise.resolve();
  function showPreview() {
    if (!state.plan) return;
    previewTools();
    var ticket = ++previewTicket, plan = state.plan;
    var out = $('output');
    function drawPreview() {
      if (ticket !== previewTicket || plan !== state.plan) return;
      out.replaceChildren();
      var pages = makePages(state.audience === 'teacher');
      pages.forEach(function (p) { out.appendChild(p); });
      out.style.zoom = state.zoom / 100;
      var oversize = pages.some(function (p) { return p.classList.contains('pl-page-oversize'); });
      var warnings = (state.plan.warnings || []).slice();
      if (oversize) warnings.push('One long item exceeds a single sheet. Reduce work space or remove that question before printing.');
      $('notice').className = 'g5gen-notice' + (warnings.length ? ' warn' : '');
      $('notice').textContent = warnings.concat(pages.length + ' Letter-size page' + (pages.length === 1 ? '' : 's') + ' · ' + (state.audience === 'teacher' ? 'Teacher key' : 'Student handout') + ' · Version ' + state.opts.version).join(' ');
      doc.body.classList.toggle('g5gen-teacher', state.audience === 'teacher');
    }
    drawPreview();
    renderQuestionEditor();
    /* Fonts and images can complete after the first synchronous layout.
       Reflow before printing so the page count and printed layout agree. */
    var images = Array.prototype.slice.call(out.querySelectorAll('img'));
    var imageReady = images.map(function (img) {
      if (typeof img.decode === 'function') return img.decode().catch(function () {});
      if (img.complete) return Promise.resolve();
      return new Promise(function (resolve) {
        img.addEventListener('load', resolve, {once:true});
        img.addEventListener('error', resolve, {once:true});
      });
    });
    previewReady = Promise.all([Promise.resolve(doc.fonts && doc.fonts.ready)].concat(imageReady))
      .then(function () {
        return new Promise(function (resolve) {
          if (typeof G.requestAnimationFrame === 'function') G.requestAnimationFrame(resolve);
          else resolve();
        });
      }).then(drawPreview);
  }

  function generate() {
    syncOptions();
    if (!state.opts.skills.length) { $('notice').className = 'g5gen-notice warn'; $('notice').textContent = 'Choose at least one skill.'; return; }
    if (state.mode === 'assessment' && state.opts.total < state.opts.count) {
      $('notice').className = 'g5gen-notice warn'; $('notice').textContent = 'Total points must be at least the number of questions. Increase the total or reduce the question count.'; return;
    }
    var seed = state.opts.version + '|' + state.unit.id + '|' + state.mode + '|' + (state.mode === 'activity' ? state.opts.activity : '') + '|' + state.build;
    if (state.mode === 'activity' && (state.opts.activity === 'error' || state.opts.activity === 'maze') &&
        state.unit.metaError && !state.unit.questions.some(function (q) {
          return q.options && q.options.some(function (choice) { return !choice.correct; });
        })) {
      $('notice').className = 'g5gen-notice warn';
      $('notice').textContent = 'Verified incorrect-answer data could not load. Reload the page and try again. ' + state.unit.metaError;
      return;
    }
    try { state.plan = C.build(state.unit, state.opts, state.mode, seed); }
    catch (e) { $('notice').className = 'g5gen-notice warn'; $('notice').textContent = e.message; return; }
    state.audience = 'student'; showPreview();
    G.history.replaceState(null, '', '?unit=' + encodeURIComponent(state.unit.id) + '&mode=' + state.mode +
      (state.mode === 'activity' ? '&kind=' + encodeURIComponent(state.opts.activity) : '') + '&level=' + encodeURIComponent(state.opts.level) +
      (STUDENT ? '&student=1' : '') + '&skills=' + encodeURIComponent(JSON.stringify(state.opts.skills)) + '&version=' + encodeURIComponent(state.opts.version));
  }

  function printHandout(which) {
    if (!state.plan) return;
    var plan = state.plan;
    Promise.resolve(previewReady).then(function () {
      if (plan !== state.plan) return;
      var root = $('printRoot'); root.replaceChildren();
      makePages(which === 'teacher').forEach(function (p) { root.appendChild(p); });
      state.printPrepared = true;
      G.print();
    });
  }

  function copyStudentLink() {
    var url = new URL(G.location.href);
    url.searchParams.set('student', '1'); url.searchParams.set('level', state.opts.level);
    url.searchParams.set('mode', state.mode);
    if (state.mode === 'activity') url.searchParams.set('kind', state.opts.activity);
    url.searchParams.set('skills', JSON.stringify(state.opts.skills));
    url.searchParams.set('version', state.opts.version);
    function manual() { if (G.prompt) G.prompt('Copy student link:', url.href); }
    if (G.navigator && G.navigator.clipboard && G.navigator.clipboard.writeText) {
      G.navigator.clipboard.writeText(url.href).then(function () { $('notice').textContent = 'Student link copied.'; }).catch(manual);
    } else manual();
  }

  function handleClick(e) {
    var t = e.target.closest('button'); if (!t) return;
    if (t.dataset.mode) {
      syncOptions();
      state.mode = MODES[t.dataset.mode] ? t.dataset.mode : 'lesson';
      state.plan = null;
      if (state.mode === 'activity' && !C.ACTIVITIES[state.opts.activity]) state.opts.activity = 'maze';
      renderControls(); generate(); return;
    }
    if (t.id === 'generate') { generate(); return; }
    if (t.dataset.allSkills !== undefined) { doc.querySelectorAll('[data-skill]').forEach(function (c) { c.checked = t.dataset.allSkills === '1'; }); return; }
    if (t.dataset.move !== undefined) {
      syncOptions();
      var i = +t.dataset.move, j = i + (+t.dataset.dir), a = state.opts.sections;
      if (j >= 0 && j < a.length) { var tmp = a[i]; a[i] = a[j]; a[j] = tmp; renderControls(); savePrefs(); }
      return;
    }
    if (t.dataset.audience) { state.audience = t.dataset.audience; showPreview(); return; }
    if (t.dataset.print) { printHandout(t.dataset.print); return; }
    if (t.id === 'copyStudentLink') { copyStudentLink(); return; }
    if (t.dataset.replace !== undefined) {
      var list = blocks(), block = list[+t.dataset.replace], used = {};
      list.forEach(function (b) { used[b.q.id] = true; });
      var pool = state.unit.questions.filter(function (q) { return state.opts.skills.indexOf(q.skillId) >= 0 && q.format === block.q.format && !used[q.id]; });
      var q = C.pickQuestions(pool, 1, 'replace' + Date.now())[0];
      if (q) { block.q = q; showPreview(); }
      else { $('notice').className = 'g5gen-notice warn'; $('notice').textContent = 'No other question matches this skill and format.'; }
      return;
    }
    if (t.dataset.remove !== undefined) {
      var target = blocks()[+t.dataset.remove];
      state.plan.sections.forEach(function (s) { s.blocks = s.blocks.filter(function (x) { return x !== target; }); });
      if (state.mode === 'assessment') {
        var qs = blocks(), pts = C.allocatePoints(qs.map(function (b) { return b.q; }), state.opts.total);
        qs.forEach(function (b, k) { b.points = pts[k]; });
      }
      showPreview(); return;
    }
  }

  function handleInput(e) {
    var t = e.target, list = blocks();
    if (t.dataset.edit !== undefined) list[+t.dataset.edit].q.prompt = t.value;
    else if (t.dataset.answer !== undefined) {
      var q = list[+t.dataset.answer].q;
      q.answer = q.format === 'select-all' ? t.value.split(';').map(function (s) { return s.trim(); }) : t.value;
      if (q.options && q.format === 'multiple-choice') { var correct = q.options.find(function (o) { return o.correct; }); if (correct) correct.text = t.value; }
    } else if (t.dataset.solution !== undefined) list[+t.dataset.solution].q.solutionSteps = t.value.split('\n').filter(Boolean);
    else return;
    clearTimeout(editTimer);
    editTimer = setTimeout(function () {
      var open = Array.prototype.map.call(doc.querySelectorAll('#questionEditor details'), function (d) { return d.open; });
      showPreview();
      doc.querySelectorAll('#questionEditor details').forEach(function (d, i) { d.open = open[i]; });
    }, 650);
  }

  function loadUnit(id) {
    $('notice').textContent = 'Loading unit…';
    var course = state.course, u = course.units.filter(function (x) { return x.id === id; })[0];
    if (!u) return showError(new Error('Unknown unit'));
    var pref = readPrefs();
    return G.MK_BANK_LOADER.loadUnitFromSite('math5', id, null, '../').then(function (ids) {
      if (!ids.length) throw new Error('This unit’s questions are not published yet.');
      // Error Analysis relies on vetted misconceptions stored separately from
      // the question bank. Do not silently erase them on a network/cache error.
      // The independent source URL is a fallback for older main-site builds.
      var metadataPath = '../math5/meta/' + encodeURIComponent(id) + '.meta.json';
      function readMetadata(url) {
        return G.fetch(url, { cache: 'no-store' }).then(function (response) {
          if (!response.ok) throw new Error('HTTP ' + response.status + ' for ' + url);
          return response.json();
        }).then(function (meta) {
          if (!meta || typeof meta !== 'object' || Array.isArray(meta) ||
              !Object.values(meta).some(function (record) { return record && record.distractors && Object.keys(record.distractors).length; }))
            throw new Error('No verified misconceptions in ' + url);
          return meta;
        });
      }
      return readMetadata(metadataPath).catch(function (primaryError) {
        return readMetadata('https://akneller1.github.io/FinancialAlgebra/math5/meta/' +
          encodeURIComponent(id) + '.meta.json').catch(function (fallbackError) {
          // Preserve ordinary generators even if both metadata sources fail.
          return { __loadError: primaryError.message + '; ' + fallbackError.message };
        });
      }).then(function (meta) {
        state.unitId = id;
        state.unit = {
          id: id, name: u.name, number: course.units.indexOf(u) + 1,
          skills: G.MK_COURSE_CATALOG.getSkillRecords('math5', id),
          questions: G.MK_QUESTION_BANKS.select({ courseId: 'math5', unitId: id }),
          meta: meta && !meta.__loadError ? meta : {},
          metaError: meta && meta.__loadError || '',
          content: Content.units[id] || {}
        };
        var overrides = {
          level: P.get('level') || pref.level || 'cp1', version: P.get('version') || undefined,
          notes: pref.notes, worked: pref.worked, space: pref.space, theme: pref.theme,
          showName: pref.showName, showStandards: pref.showStandards, sections: pref.sections,
          duration: pref.duration, activity: P.get('kind') || 'maze'
        };
        Object.keys(overrides).forEach(function (k) { if (overrides[k] === undefined) delete overrides[k]; });
        state.opts = C.options(overrides);
        var sharedSkills = null;
        try { sharedSkills = JSON.parse(P.get('skills') || 'null'); } catch (e) {}
        var availableSkills = state.unit.skills.map(function (s) { return s.id; });
        state.opts.skills = Array.isArray(sharedSkills) && sharedSkills.length
          ? sharedSkills.filter(function (id) { return availableSkills.indexOf(id) >= 0; })
          : availableSkills;
        state.plan = null;
        renderControls(); generate();
      });
    });
  }
  function showError(e) {
    $('notice').className = 'g5gen-notice warn';
    $('notice').textContent = 'Unable to load resources: ' + e.message;
  }

  doc.addEventListener('click', handleClick);
  doc.addEventListener('input', handleInput);
  doc.addEventListener('change', function (e) {
    if (e.target.id === 'unit') loadUnit(e.target.value).catch(showError);
    if (e.target.id === 'zoom') { state.zoom = +e.target.value; $('output').style.zoom = state.zoom / 100; }
    if (e.target.id === 'activityKind' || e.target.id === 'theme') { syncOptions(); generate(); }
  });
  G.addEventListener('beforeprint', function () {
    if (state.printPrepared || !state.plan) return;
    var root = $('printRoot'); root.replaceChildren();
    makePages(state.audience === 'teacher').forEach(function (p) { root.appendChild(p); });
  });
  G.addEventListener('afterprint', function () { state.printPrepared = false; });

  state.mode = MODES[P.get('mode')] ? P.get('mode') : 'lesson';
  var course = G.LIBRARY && G.LIBRARY.courses.filter(function (c) { return c.id === 'math5'; })[0];
  if (!course) { showError(new Error('The Grade 5 course catalog is unavailable.')); return; }
  state.course = course;
  var start = P.get('unit') || course.units[0].id;
  if (!course.units.some(function (u) { return u.id === start; })) start = course.units[0].id;
  loadUnit(start).catch(showError);
  G.G5_GENERATORS = { state: state, generate: generate, showPreview: showPreview, printHandout: printHandout };
})(window);
