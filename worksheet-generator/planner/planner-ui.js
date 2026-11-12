/* Daily Lesson Planner — page (DOM).

   Left: pick a day (by unit), class level, number of practice problems, new problems, print.
   Right: three views of the day —
     Plan            the teacher's plan with every problem, its answer and a "New problem" button
     Student handout one printable packet: Do Now · Notes · Practice · Exit ticket
     Teacher key     the plan page + every answer with worked steps
   URL: lesson-planner.html#day=<n>&level=<cp2|cp1|honors>&seed=<s>   or   #unit=<skill set id> (first day of that unit). */
(function (G) {
  'use strict';
  var doc = G.document, NS = G.MKMENU, WS = G.MKWS, P = G.MKPLAN, SC = G.MKPLAN_SCOPE;
  var COURSE = G.MKPLAN_COURSE || 'algebra1', GEO = COURSE === 'geometry', A2 = COURSE === 'algebra2', PA8 = ['prealgebra', 'prealgebra7', 'math6', 'math5', 'precalculus', 'calculus', 'statistics', 'discrete'].indexOf(COURSE) >= 0, CS = COURSE === 'algebra1' ? '' : '-'+COURSE;   // per-lesson saved data is kept separately for each course
  var KEY_LEVEL = 'mk-planner-level', KEY_THEME = 'mkws-theme', KEY_N = 'mk-planner-practice', KEY_NOTES = 'mk-planner-notes', KEY_MIN = 'mk-planner-minutes', KEY_NOTE_EDITS = 'mk-planner-note-edits', KEY_SECTIONS = 'mk-planner-sections-v1', KEY_SECTION_ORDER = 'mk-planner-section-order-v1', KEY_PROBLEM_LABELS = 'mk-planner-problem-labels-v1', KEY_COUNTS = 'mk-planner-section-counts-v1';
  KEY_NOTE_EDITS += CS; KEY_PROBLEM_LABELS += CS;
  function lsGet(k) { try { return G.localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { G.localStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  function $(s) { return doc.querySelector(s); }
  function esc(s) { return String(s === undefined || s === null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var ms = function (s) { return NS.mathSafe(s); };

  var ui = { day: 4, level: lsGet(KEY_LEVEL) || 'cp1', seed: 'A', practice: +(lsGet(KEY_N) || 10), view: 'plan', plan: null, notes: lsGet(KEY_NOTES) };
  /* Student notes: 'filled' = Completed notes, 'fill' = Guided notes. Until the teacher picks one (or with an older
     saved "as planned" choice) each lesson uses its scope notes style: Completed for "Pre-filled", otherwise Guided. */
  if (!/^(fill|filled)$/.test(ui.notes || '')) ui.notes = null;
  ui.selectedDays = [ui.day];
  function resetSelection() { ui.selectedDays = [ui.day]; }

  var sectionLabels = { donow:'Do Now', mixed:'Mixed Review', notes:'Notes', examples:'Examples', practice:'Practice', challenge:'Challenge Problems', summary:'Lesson Summary', exit:'Exit Ticket' };
  var sectionChoices = { donow:true, mixed:false, notes:true, examples:true, practice:true, challenge:false, summary:false, exit:true };
  try { var savedSections = JSON.parse(lsGet(KEY_SECTIONS) || '{}'); Object.keys(sectionChoices).forEach(function(k) { if (typeof savedSections[k] === 'boolean') sectionChoices[k] = savedSections[k]; }); } catch(e) {}
  var sectionOrder = (function() {
    var base = Object.keys(sectionChoices);
    try {
      var stored = JSON.parse(lsGet(KEY_SECTION_ORDER) || 'null');
      if (Array.isArray(stored)) {
        var valid = stored.filter(function(k, i) { return base.indexOf(k) >= 0 && stored.indexOf(k) === i; });
        var ordered = valid.concat(base.filter(function(k) { return valid.indexOf(k) < 0; }));
        if (valid.indexOf('challenge') < 0) { ordered.splice(ordered.indexOf('challenge'), 1); var afterPractice = ordered.indexOf('practice'); ordered.splice(afterPractice < 0 ? ordered.length : afterPractice + 1, 0, 'challenge'); }
        return ordered;
      }
    } catch(e) {}
    return base;
  })();
  var KEY_SEQUENCE = 'mk-planner-sequence-v1';
  var sectionSequence = (function() {
    try { var v = JSON.parse(lsGet(KEY_SEQUENCE) || 'null');
      if (Array.isArray(v) && v.length && v.length <= 30 && v.every(function(k) { return k in sectionChoices; })) return v;
    } catch(e) {}
    return sectionOrder.slice();
  })();
  var KEY_SECTION_CONFIG = 'mk-planner-occurrence-v1' + CS;
  var sectionConfigs = (function() { try { return JSON.parse(lsGet(KEY_SECTION_CONFIG) || '{}') || {}; } catch(e) { return {}; } })();
  function saveConfigs() { lsSet(KEY_SECTION_CONFIG, JSON.stringify(sectionConfigs)); }
  function configureSection(plan,s,index) {
    var cfg = sectionConfigs[index] || {};
    var day = (plan.selectedDays || []).map(function(n){return P.day(n);}).find(function(d){return d && d.lesson_id === cfg.lesson;});
    if (day) {
      s.lessonDay = day;
      s.title += ' — ' + day.title;
      if (s.id !== 'notes' && P.entriesFor) {
        var entries = P.entriesFor([day.lesson_id]);
        if (entries.length) s.groups.forEach(function(g) { g.items.forEach(function(p,i) {
          if (p.entry) { p.entry = entries[i % entries.length]; p.slot += '-topic-' + index; }
        }); });
      }
    }
    if (cfg.count != null && s.id !== 'notes' && s.id !== 'summary') {
      var all = []; s.groups.forEach(function(g){all=all.concat(g.items);});
      if (all.length) {
        var target = Math.max(0,Math.min(30,Math.round(+cfg.count)));
        var out = all.slice(0,target);
        while (out.length < target) {
          var p = all[out.length % all.length];
          out.push(Object.assign({},p,{slot:p.slot+'-copy-'+index+'-'+out.length}));
        }
        s.groups = [{name:'',items:out}];
      }
    }
  }
  function saveSequence() { lsSet(KEY_SEQUENCE, JSON.stringify(sectionSequence)); }
  function applySectionChoices(plan) {
    var original = {};
    plan.sections.forEach(function(s) { original[s.id] = s; });
    var occurrences = {};
    plan.sections = sectionSequence.map(function(id, seqIndex) {
      if (!sectionChoices[id] || !original[id]) return null;
      var n = occurrences[id] = (occurrences[id] || 0) + 1;
      var source = original[id];
      var s = Object.assign({}, source);
      s.occurrenceIndex = seqIndex;
      if (n > 1) s.title += ' (' + n + ')';
      s.groups = source.groups.map(function(g) {
        return Object.assign({}, g, {items:g.items.map(function(p) { return Object.assign({}, p); })});
      });
      return s;
    }).filter(Boolean);
    plan.sections.forEach(function(s) { configureSection(plan,s,s.occurrenceIndex); });
    plan.sections.forEach(function(s, si) {
      var cfg = sectionConfigs[s.occurrenceIndex] || {};
      var nth = s.title.match(/\((\d+)\)/);
      if (!nth && !cfg.lesson && cfg.count == null) return;
      s.groups.forEach(function(g,gi) { g.items.forEach(function(p,pi) {
        if (!p.entry) return;
        // Different slots and salts prevent repeated questions from cloning the originals.
        p.slot = p.slot + '-occ-' + s.occurrenceIndex + '-item-' + pi;
        P.regenerate(plan,si,gi,pi);
      }); });
    });
  }

  var problemCounts = (function() {
    try { var v = JSON.parse(lsGet(KEY_COUNTS) || '{}'); return v && typeof v === 'object' && !Array.isArray(v) ? v : {}; }
    catch(e) { return {}; }
  })();
  function totalProblems(section) {
    return section ? section.groups.reduce(function(n, g) { return n + g.items.length; }, 0) : null;
  }
  function problemCountInput(id) {
    if (['donow','mixed','examples','practice','challenge','exit'].indexOf(id) < 0) return '';
    var section = ui.plan && ui.plan.sections.find(function(s) { return s.id === id; });
    var count = Object.prototype.hasOwnProperty.call(problemCounts,id) ? problemCounts[id] : totalProblems(section);
    var unavailable = !section || (!totalProblems(section) && !Object.prototype.hasOwnProperty.call(problemCounts,id));
    if (count == null) count = 0;
    return '<label class="pl-hint" style="display:flex;align-items:center;gap:4px;margin:0">Problems <input type="number" data-problem-count="' + id +
      '" min="0" max="30" step="1" value="' + count + '"' + (unavailable ? ' disabled title="No generated problems for this lesson section"' : '') +
      ' aria-label="Number of problems in ' + esc(sectionLabels[id]) + '" style="width:68px;max-width:68px;padding:5px"></label>';
  }
  /* Minutes the teacher typed, remembered per day type (a Lesson-day timing applies to every Lesson day). */
  var minutesStore = (function () { try { return JSON.parse(lsGet(KEY_MIN) || '{}') || {}; } catch (e) { return {}; } })();
  function minutesFor(d) { return minutesStore[d.day_type] || null; }
  function saveMinutes(d, secId, v) {
    var m = minutesStore[d.day_type] = minutesStore[d.day_type] || {};
    if (v === null) delete m[secId]; else m[secId] = v;
    if (!Object.keys(m).length) delete minutesStore[d.day_type];
    lsSet(KEY_MIN, JSON.stringify(minutesStore));
  }
  var problemLabels = (function () { try { return JSON.parse(lsGet(KEY_PROBLEM_LABELS) || '{}') || {}; } catch(e) { return {}; } })();
  function labelKey(day, section, group, index) { return day + ':' + section + ':' + group + ':' + index; }
  function applyProblemLabels(plan) {
    plan.sections.forEach(function(s) { s.groups.forEach(function(g, gi) { g.items.forEach(function(p, pi) {
      p.teacherLabel = problemLabels[labelKey(plan.day.day, s.id + ':' + s.occurrenceIndex, gi, pi)] || '';
    }); }); });
  }
  function displayProblemLabel(p, fallback) { return fallback + (p.teacherLabel ? ' · ' + p.teacherLabel : ''); }
  function problemLabelPicker(plan, p, s, gi, pi) {
    var values = ['', 'I do', 'We do', 'You do'];
    return '<label class="pl-problem-label">Instructional label <select data-problem-label="' + esc(s.id) + '" data-occ-index="' + s.occurrenceIndex + '" data-group="' + gi + '" data-item="' + pi + '" aria-label="Label for ' + esc(s.title) + ' problem ' + p.num + '">' +
      values.map(function(v) { return '<option value="' + esc(v) + '"' + (p.teacherLabel === v ? ' selected' : '') + '>' + (v ? esc(v) : 'No label') + '</option>'; }).join('') +
      '</select></label>';
  }
  function filled(plan) { return plan.notesMode === 'filled'; }
  /* Notes the teacher edited, per lesson, kept in this browser (MKPLAN.noteEdits is read by define/keyIdea/vocab). */
  P.noteEdits = (function () { try { return JSON.parse(lsGet(KEY_NOTE_EDITS) || '{}') || {}; } catch (e) { return {}; } })();
  function saveNoteEdits() { lsSet(KEY_NOTE_EDITS, JSON.stringify(P.noteEdits)); }
  function editRecord(d) {   // the first edit copies the current notes so later edits change one field at a time
    if (!P.noteEdits[d.lesson_id]) { var n = P.lessonNotes(d); P.noteEdits[d.lesson_id] = { words: n.words.map(function (w) { return w.slice(); }), idea: n.idea, watch: n.watch, extra: n.extra }; }
    var r = P.noteEdits[d.lesson_id];
    if (!Array.isArray(r.cards)) r.cards = P.teachCards(d).map(function (c) { return { big: c.big, steps: c.steps.slice() }; });
    return r;
  }
  function notesEditor(plan, section) {
    var d = section.lessonDay || plan.day, n = P.lessonNotes(d);
    return '<details class="pl-noted-wrap"' + (ui.editorOpen ? ' open' : '') + '><summary>Edit these notes</summary><div class="pl-noted" data-note-day="' + d.day + '"><div class="pl-noted-hd"><b>Notes</b> <span class="pl-hint">Edit anything below. Your changes are saved in this browser and used on the handout, the key and the slides.</span>' +
      ' <button type="button" class="link" id="plNotesReset"' + (P.notesEdited(d) ? '' : ' hidden') + '>Reset to the original notes</button></div>' +
      '<label class="pl-nl">Key idea<textarea data-n="idea" rows="2">' + esc(n.idea) + '</textarea></label>' +
      P.teachCards(d).map(function (c, i) { return '<div class="pl-nl">Explanation: ' + esc(c.h.replace(/[⟨⟩]/g, '')) + '</div><textarea data-n="cb" data-i="' + i + '" rows="3" aria-label="Explanation for ' + esc(c.h) + '">' + esc(c.big) + '</textarea>' +
        '<label class="pl-nl">Steps <small>(one per line)</small><textarea data-n="cs" data-i="' + i + '" rows="' + Math.max(2, c.steps.length) + '">' + esc(c.steps.join('\n')) + '</textarea></label>'; }).join('') +
      '<p class="pl-hint">Put {{double braces}} around a word, number or step result to make it a blank on guided notes. ⟨…⟩ marks math.</p>' +
      '<div class="pl-nl">Vocabulary</div><table class="pl-ntbl"><thead><tr><th>Word</th><th>What it means / example</th><th></th></tr></thead><tbody>' +
      n.words.map(function (w, i) { return '<tr><td><input type="text" data-n="w" data-i="' + i + '" value="' + esc(w[0]) + '" aria-label="Word ' + (i + 1) + '"></td><td><textarea data-n="d" data-i="' + i + '" rows="2" aria-label="Meaning of ' + esc(w[0]) + '">' + esc(w[1]) + '</textarea></td><td><button type="button" class="btn ghost sm pl-delword" data-i="' + i + '" aria-label="Remove ' + esc(w[0]) + '">✕</button></td></tr>'; }).join('') +
      '</tbody></table><button type="button" class="btn ghost sm" id="plAddWord">+ Add a word</button>' +
      '<label class="pl-nl">Watch out (common mistake)<textarea data-n="watch" rows="2">' + esc(n.watch) + '</textarea></label>' +
      '<label class="pl-nl">My notes <small>(printed on the handout and the slides; leave blank for none)</small><textarea data-n="extra" rows="3" placeholder="Anything else students should write down: a rule, a diagram description, a reminder…">' + esc(n.extra) + '</textarea></label></div></details>';
  }
  if (!NS.LEVELS[ui.level]) ui.level = 'cp1';

  /* ---------- groups of days for the picker ---------- */
  function isSem(d) { return /^SEM-/.test(d.lesson_id); }
  function isFinal(d) { return /^END-/.test(d.lesson_id) || (!GEO && !d.unit && d.day >= 100); }
  function span(f) { var a = SC.days.filter(f); return a.length ? ' (days ' + a[0].day + '–' + a[a.length - 1].day + ')' : ''; }
  function dayGroups() {
    var launchDays = SC.days.filter(function (d) { return !d.unit && !isSem(d) && !isFinal(d); });
    var out = [{ key: 'launch', name: 'Course launch' + (launchDays.length ? ' (days ' + launchDays[0].day + '–' + launchDays[launchDays.length - 1].day + ')' : ''), days: [] }];
    SC.units.forEach(function (u) { out.push({ key: 'u' + u.unit, name: 'Unit ' + u.unit + ': ' + u.title + ' (days ' + u.start_day + '–' + u.end_day + ')', days: [] }); });
    out.push({ key: 'sem', name: 'Semester review & exam' + span(isSem), days: [] }, { key: 'final', name: 'Final review, exam' + (GEO ? '' : ' & project') + span(isFinal), days: [] });
    SC.days.forEach(function (d) {
      var k = groupKey(d);
      out.filter(function (g) { return g.key === k; })[0].days.push(d);
    });
    return out;
  }
  function groupKey(d) { return d.unit ? 'u' + d.unit : isSem(d) ? 'sem' : isFinal(d) ? 'final' : 'launch'; }
  var TYPE_CLS = { Lesson: 'lesson', Practice: 'practice', Quiz: 'quiz', Review: 'review', Assessment: 'test', Flex: 'flex', Launch: 'launch', Diagnostic: 'launch', 'Exam Review': 'review', Exam: 'test', Project: 'project' };

  /* ---------- hash ---------- */
  function readHash() {
    var h = {}; (location.hash || '').replace(/^#/, '').split('&').forEach(function (kv) { var p = kv.split('='); if (p[0]) h[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || ''); });
    // A link to another course (by #course= or by a #unit= from another course) needs a reload: the course's scope loads at start-up
    var target = h.course || (/^(algebra1|geometry|algebra2|prealgebra7|prealgebra|math6|math5|precalculus|calculus|statistics|discrete)-/.exec(h.unit || '') || [])[1];
    if (target && /^(algebra1|geometry|algebra2|prealgebra|prealgebra7|math6|math5|precalculus|calculus|statistics|discrete)$/.test(target) && target !== COURSE) { G.location.reload(); return; }
    if (h.unit) {
      var num = null; Object.keys(G.MKPLAN_SKILLS.UNIT_SET).forEach(function (n) { if (P.unitSetId(+n) === h.unit || String(n) === h.unit) num = +n; });
      var u = num && P.unitOf(num); if (u) ui.day = u.start_day;
    }
    if (h.day && P.day(+h.day)) ui.day = +h.day;
    if (h.level && NS.LEVELS[h.level]) ui.level = h.level;
    if (h.seed) ui.seed = h.seed.slice(0, 12);
    if (h.view && /^(plan|student|key)$/.test(h.view)) ui.view = h.view;
  }
  function writeHash() {
    var h = (COURSE === 'algebra1' ? '#day=' : '#course='+COURSE+'&day=') + ui.day + '&level=' + ui.level + (ui.seed !== 'A' ? '&seed=' + encodeURIComponent(ui.seed) : '') + (ui.view !== 'plan' ? '&view=' + ui.view : '');
    if (location.hash !== h) history.replaceState(null, '', h);
  }

  /* ---------- problem pieces ---------- */
  function promptHtml(p, inlineLabel) {
    if (p.failed) return '<div class="pl-missing">No ' + (A2 ? 'approved bank question' : 'verified problem') + ' for this slot (' + esc(p.reason || '') + '). Click “New problem” or write your own.</div>';
    var h = '<div class="pl-q">' + (inlineLabel ? '<b class="pl-qnum">' + esc(inlineLabel) + '</b> ' : '') + ms(p.prompt || '') + '</div>';
    if (p.work && p.work.length) h += '<ol class="mm-work-lines">' + p.work.map(function (w, i) { return '<li><span>Line ' + (i + 1) + ':</span> ' + ms('⟨' + w + '⟩') + '</li>'; }).join('') + '</ol>';
    if (p.fig) h += NS.figHtml(p.fig);
    if (p.fig && p.fig.proof) return h;   // the proof table under the diagram labels every blank
    if (p.authoredOptions && p.authoredOptions.length) h += '<ol class="pl-authored-options" style="list-style:none;padding-left:0">' + p.authoredOptions.map(function(o){return '<li>' + (p.authoredFormat === 'select-all' ? '☐ ' : '○ ') + ms(o.text) + '</li>';}).join('') + '</ol>';
    var parts = (p.parts || []).filter(function (pt) { return pt.prompt; });
    if (parts.length) h += '<div class="pl-parts">' + parts.map(function (pt) { return '<div><b>' + (pt.label ? '(' + esc(pt.label) + ')' : '') + '</b> ' + ms(pt.prompt) + '</div>'; }).join('') + '</div>';
    return h;
  }
  function answerHtml(p) {
    if (p.failed) return '';
    var parts = p.parts || [];
    return '<div class="pl-ans"><b>Answer:</b> ' + parts.map(function (pt) { return (parts.length > 1 && pt.label ? '<b>(' + esc(pt.label) + ')</b> ' : '') + ms(pt.answer || '') + (pt.answerFig ? NS.figHtml(pt.answerFig) : ''); }).join(' &nbsp; ') + '</div>';
  }
  function stepsHtml(p) {
    var st = (p.steps || []).filter(function (s) { return s.t || s.m; });
    if (!st.length) return '';
    return '<ol class="pl-steps">' + st.map(function (s) { return '<li>' + ms(s.t || '') + (s.m ? ' ' + ms('⟨' + s.m + '⟩') : '') + '</li>'; }).join('') + '</ol>';
  }
  function wide(p) { return !!(p.fig && p.fig.proof) || (p.parts || []).filter(function (x) { return x.prompt; }).length > 1 || (p.prompt || '').replace(/⟨[^⟩]*⟩/g, 'xxxxxxxx').length > 140 || (p.fig && /twoway/.test(p.fig.kind)); }
  function lessonTitle(id) { var l = P.lessonById(id); return l ? l.title : id; }
  function levelName() { return NS.LEVELS[ui.level].name; }
  function lines(n, label) { var h = '<div class="pl-lines">'; for (var i = 0; i < n; i++) h += '<div class="pl-line">' + (i === 0 && label ? '<span>' + esc(label) + '</span>' : '') + '</div>'; return h + '</div>'; }
  function frameHtml(f) { return esc(f || '').replace(/_{2,}/g, '<span class="pl-blank"></span>'); }

  /* ---------- the plan view (teacher, interactive) ---------- */
  function planInfo(plan) {
    var d = plan.day, T = P.template(d), u = d.unit ? P.unitOf(d.unit) : null;
    var meta = [['Standards', G.MKSTD && d.standards ? G.MKSTD.listHtml(d.standards) : esc(d.standards)], ['Content objective', esc(d.content_objective)], ['Language objective', esc(d.language_objective)]];
    if (d.sentence_frame) meta.push(['Sentence frame', '<i>' + frameHtml(d.sentence_frame) + '</i>']);
    if (d.key_vocabulary) meta.push(['Key vocabulary', P.vocab(d).map(function (v) { return '<span class="pl-chip">' + esc(v) + '</span>'; }).join(' ')]);
    if (P.watchOut(d)) meta.push(['Watch for', esc(P.watchOut(d))]);
    if (d.notes_style) meta.push(['Notes style', esc(d.notes_style)]);
    if (d.do_now_strategy) meta.push(['Do Now strategy', esc(d.do_now_strategy) + ((d.do_now_source_ids || []).length ? ' — from ' + d.do_now_source_ids.map(function (id) { return '<span class="pl-chip" title="' + esc(lessonTitle(id)) + '">' + esc(id) + '</span>'; }).join(' ') : '') + ((d.spiral_review_ids || []).length ? '; spiral ' + d.spiral_review_ids.map(function (id) { return '<span class="pl-chip" title="' + esc(lessonTitle(id)) + '">' + esc(id) + '</span>'; }).join(' ') : '')]);
    var changed = plan.sections.some(function (s) { return s.minutes !== s.defaultMinutes; });
    var agenda = '<table class="pl-agenda"><thead><tr><th>Part</th><th>Minutes</th><th>What happens</th></tr></thead><tbody>' + plan.sections.map(function (s, si) {
      return '<tr><td><b>' + esc(s.title) + '</b></td><td><input type="number" class="pl-mins" min="0" max="180" step="1" data-s="' + si + '" value="' + (s.minutes || 0) + '" aria-label="Minutes for ' + esc(s.title) + '"></td><td>' + esc(s.template || '') + '</td></tr>';
    }).join('') + '<tr class="pl-total"><td><b>Total</b></td><td><b id="plTotal">' + P.totalMinutes(plan) + '</b> min</td><td>' +
      '<span class="pl-hint">Times you change are kept for every ' + esc(d.day_type) + ' day.</span>' + ' <button type="button" class="link" id="plResetMin"' + (changed ? '' : ' hidden') + '>Reset to the planned times</button>' + '</td></tr></tbody></table>';
    var cov = plan.coverage.filter(function (c) { return c.cover !== 'full'; });
    var covHtml = cov.length ? '<div class="pl-cover"><b>Generator coverage</b>' + cov.map(function (c) { return '<div><span class="pl-chip ' + c.cover + '">' + esc(c.id) + ' · ' + (c.cover === 'none' ? 'not covered' : 'partly covered') + '</span> ' + esc(c.note) + '</div>'; }).join('') + '</div>' : '';
    var res = resourceLinks(plan);
    return '<div class="pl-info card">' +
      '<dl class="pl-meta">' + meta.map(function (m) { return '<dt>' + m[0] + '</dt><dd>' + m[1] + '</dd>'; }).join('') + '</dl>' + agenda + covHtml + res + '</div>';
  }
  function resourceLinks(plan) {
    var set = plan.unitSet, d = plan.day, links = [];
    if (set) {
      links.push(['Worksheet Generator', 'worksheet.html#unit=' + set], ['Assessment Generator', 'menu-assessment.html#unit=' + set]);
      if (/Practice|Review|Flex/.test(d.day_type)) links.push(['Maze', 'printables.html#unit=' + set + '&kind=maze'], ['Partner Check', 'printables.html#unit=' + set + '&kind=partner'], ['Stations', 'printables.html#unit=' + set + '&kind=stations']);
      if (/Quiz/.test(d.day_type)) links.splice(2, 0, ['Short quiz (versions A–C)', 'menu-assessment.html#unit=' + set]);
      if (COURSE === 'algebra1') links.push(['Unit page', '../index.html#algebra.' + unitPageId(d.unit)]);
      else {
        var lc = (G.LIBRARY && G.LIBRARY.courses || []).filter(function (c) { return c.id === COURSE; })[0], bare = set.replace(/^(geometry|algebra2|prealgebra)-/, '');
        var lu = lc && lc.units.filter(function (u) { return u.id === bare || (u.artifacts || []).some(function (a) { return /#unit=/.test(a.path || '') && (a.path.split('#unit=')[1] || '').split('&')[0] === set; }); })[0];
        if (lu) links.push(['Unit page', '../index.html#' + COURSE + '.' + lu.id]);
      }
    } else if (/Exam/.test(d.day_type)) {
      links.push(['Assessment Generator', 'menu-assessment.html']);
    }
    if (!links.length) return '';
    return '<div class="pl-res"><b>Unit resources</b> ' + links.map(function (l) { return '<a class="btn ghost sm" href="' + esc(l[1]) + '">' + esc(l[0]) + '</a>'; }).join(' ') + '</div>';
  }
  var UNIT_PAGE = { 1: 'foundations-algebra', 2: 'expressions-equations', 3: 'inequalities', 4: 'relations-functions', 5: 'linear-equations-slope', 6: 'systems-of-equations', 7: 'exponents-exponential-functions', 8: 'exponential-functions', 9: 'polynomials-factoring', 10: 'factoring-zero-product', 11: 'quadratics', 12: 'statistics-data-modeling' };
  function unitPageId(n) { return UNIT_PAGE[n] || ''; }

  function planView(plan) {
    var h = planInfo(plan);
    plan.sections.forEach(function (s, si) {
      h += '<section class="pl-sec card"><div class="pl-sechd"><h2>' + esc(s.title) + '</h2>' + '<span class="pl-min" data-min="' + si + '">' + (s.minutes ? s.minutes + ' min' : '') + '</span>' + '<span class="pl-tpl">' + esc(s.template || '') + '</span></div>';
      h += sectionTeacherExtras(plan, s);
      s.groups.forEach(function (g, gi) {
        if (g.name || g.note) h += '<h3 class="pl-grp">' + esc(g.name) + (g.note ? ' <small>' + esc(g.note) + '</small>' : '') + '</h3>';
        h += '<div class="pl-cards">' + g.items.map(function (p, ii) {
          return '<article class="pl-card' + (p.failed ? ' failed' : '') + '"><div class="pl-chd"><b>' + p.num + '.</b> <span class="pl-skill">' + esc(p.skillName) + ' · ' + esc(p.lesson) + (p.spiral ? ' · spiral' : '') + '</span>' +
            (p.failed ? '<span class="pl-badge bad">not verified</span>' : '<span class="pl-badge ok" title="Answer re-derived from the printed problem">✓ checked</span>') + '<span class="pl-diff" title="Difficulty within this set (c = generator difficulty 1–7)">' + (p.failed ? '' : P.difficultyName(plan, p) + ' · ') + 'c' + (p.c || '') + '</span></div>' +
            promptHtml(p) + (p.challengeQuestion ? '<p class="pl-prompt"><b>Go further:</b> ' + esc(p.challengeQuestion) + '</p>' : '') + answerHtml(p) + problemLabelPicker(plan, p, s, gi, ii) + '<button type="button" class="btn ghost sm pl-regen" data-s="' + si + '" data-g="' + gi + '" data-i="' + ii + '">New problem</button></article>';
        }).join('') + '</div>';
      });
      h += '</section>';
    });
    return h;
  }
  /* The completed / guided choice, shown in the sidebar and again at the top of the Notes preview. */
  function notesModeSwitch(plan, where) {
    var mode = filled(plan) ? 'filled' : 'fill';
    return '<div class="nt-switch" role="radiogroup" aria-label="Student notes"><span class="nt-switch-lab">Student sheet gets:</span>' + [['filled', 'Completed notes'], ['fill', 'Guided notes']].map(function (o) {
      return '<label class="nt-opt' + (mode === o[0] ? ' on' : '') + '"><input type="radio" name="plNotes' + (where === 'plan' ? 'Plan' : '') + '" value="' + o[0] + '"' + (mode === o[0] ? ' checked' : '') + '> ' + o[1] + '</label>';
    }).join('') + '<span class="pl-hint">Preview shows the teacher copy: <span class="nt-fill key">highlighted</span> parts are blanks on guided notes. The teacher key always has the completed notes.</span></div>';
  }
  function sectionTeacherExtras(plan, s) {
    var d = plan.day, out = '';
    if (s.prompt) out += '<p class="pl-prompt">Prompt: <i>' + esc(s.prompt) + '</i></p>';
    if (s.id === 'notes' && d.day_type === 'Lesson') {
      out += notesModeSwitch(plan, 'plan');
      var nd = s.lessonDay ? [s.lessonDay] : (plan.selectedDays || [d.day]).map(function (n) { return P.day(n); }).filter(Boolean);
      nd.forEach(function (x) {
        out += (nd.length > 1 ? '<h3 class="pl-grp">' + esc(x.title) + '</h3>' : '') + '<div class="nt-preview">' + teachNotesHtml(plan, x, 'key') + '</div>' +
          ((plan.worked && plan.worked[x.day] || []).length ? '<div class="pl-btns">' + plan.worked[x.day].map(function (p, k) { return '<button type="button" class="btn ghost sm" data-worked-day="' + x.day + '" data-worked-k="' + k + '">New worked example' + (plan.worked[x.day].length > 1 ? ' ' + (k + 1) : '') + '</button>'; }).join('') + '</div>' : '') +
          notesEditor(plan, Object.assign({}, s, { lessonDay: x }));
      });

      out += '<p class="pl-hint">Examples go from the level’s easiest to hardest: Example 1 I do, Example 2 we do' + (s.groups[0] && s.groups[0].items.length > 2 ? ', Example 3 you try' : '') + '.</p>';
    }
    if (s.frame) out += '<p class="pl-prompt">Summary frame: <i>' + frameHtml(s.frame) + '</i></p>';
    if (s.launch) out += '<p class="pl-prompt">' + esc(launchTask(d).teacher) + '</p>';
    if (s.project && s.id === 'practice') out += '<p class="pl-prompt">Checkpoints: ' + projectCheckpoints(d).map(esc).join(' · ') + '</p>';
    return out;
  }

  /* ---------- fixed text for non-problem parts ---------- */
  var launchTask = P.launchTask, routines = P.routines, projectCheckpoints = P.projectCheckpoints;

  /* Two problems per row; a row is a block that never splits across pages (grid items do not page-break reliably). */
  function rows(list) {
    var out = '', row = [];
    function flush() { if (row.length) { out += '<div class="pl-row">' + row.join('') + (row.length === 1 ? '<div class="pl-cell"></div>' : '') + '</div>'; row = []; } }
    list.forEach(function (x) { if (x.wide) { flush(); out += '<div class="pl-row one">' + x.html + '</div>'; } else { row.push(x.html); if (row.length === 2) flush(); } });
    flush();
    return out;
  }

  /* ---------- student handout (paper) ---------- */
  function studentProblem(p, label) {
    var space = p.failed ? 1 : Math.max(0.6, (p.space || [1, 1.3, 1.6])[1]);
    return '<div class="pl-p">' + (p.failed ? '<div class="pl-q"><b class="pl-qnum">' + esc(label || (p.num + '.')) + '</b> &nbsp;</div>' : promptHtml(p, label || (p.num + '.'))) + (p.challengeQuestion ? '<p class="pl-challenge"><b>Challenge:</b> ' + esc(p.challengeQuestion) + '</p><div class="pl-space" style="height:1.0in"></div>' : '<div class="pl-space" style="height:' + space.toFixed(2) + 'in"></div>') + '</div>';
  }
  function workedProblem(p, label) {
    return '<div class="pl-p pl-worked">' + promptHtml(p, label) + stepsHtml(p) + answerHtml(p) + '</div>';
  }
  function sheetHead(plan, kind) {
    var d = plan.day, u = d.unit ? 'Unit ' + d.unit + ': ' + d.unit_title : d.unit_title;
    return '<div class="pl-head"><div><div class="pl-title">' + esc(d.title) + '</div><div class="pl-sub">' + esc(SC.meta.course || 'Algebra 1') + ' · Day ' + d.day + ' · ' + esc(u) + (d.unit ? ' · day ' + esc(d.unit_day) : '') + ' · ' + esc(d.day_type) + '</div></div>' +
      (kind === 'key' ? '<span class="pl-tag key">Teacher key · ' + levelName() + '</span>' : '<span class="pl-tag">' + levelName() + '</span>') + '</div>' +
      (kind === 'key' ? '' : '<div class="pl-name"><span>Name <i></i></span><span>Date <i class="s"></i></span><span>Period <i class="s"></i></span></div>');
  }
  function studentSheet(plan) {
    var d = plan.day, h = sheetHead(plan, 'student');
    if (d.content_objective && !/Exam$|Assessment/.test(d.day_type)) h += '<div class="pl-ican"><b>Today:</b> ' + esc(P.iCan(d.content_objective)) + '</div>';
    plan.sections.forEach(function (s) {
      if (s.id === 'exit' || s.id === 'summary') return;
      h += '<div class="pl-sbox pl-s-' + s.id + '"><div class="pl-shd">' + esc(s.title) + (s.id === 'notes' && plan.day.day_type === 'Lesson' ? ' <small class="nt-mode">· ' + (filled(plan) ? 'Completed notes' : 'Guided notes — fill in the blanks as we go') + '</small>' : '') + (s.minutes ? '<span>' + s.minutes + ' min</span>' : '') + '</div>';
      h += studentSectionBody(plan, s);
      h += '</div>';
    });
    var ex = plan.sections.filter(function (s) { return s.id === 'exit'; })[0];
    if (ex) h += '<div class="pl-exit"><div class="pl-cut">✂ cut here</div><div class="pl-shd">' + esc(ex.title) + '<span>Name ______________________</span></div>' + studentSectionBody(plan, ex) + '</div>';
    var summary = plan.sections.filter(function(s) { return s.id === 'summary'; })[0];
    if (summary) h += '<div class="pl-sbox pl-s-summary"><div class="pl-shd">' + esc(summary.title) + '</div>' + studentSectionBody(plan, summary) + '</div>';
    return '<div class="pl-sheet">' + h + '</div>';
  }
  function studentSectionBody(plan, s) {
    var d = plan.day, h = '';
    if (s.prompt) h += '<p class="pl-sprompt">' + esc(s.prompt) + '</p>' + (s.id === 'challenge' ? '' : lines(3));
    if (s.id === 'notes') h += notesBody(plan, s);
    if (s.launch) { var lt = launchTask(d); h += '<p class="pl-sprompt"><b>' + esc(lt.title) + '.</b> ' + esc(lt.student) + '</p><div class="pl-space" style="height:3.2in"></div>'; }
    if (s.project && s.id === 'practice') h += '<table class="pl-tbl"><thead><tr><th>Checkpoint</th><th>Done?</th><th>Notes</th></tr></thead><tbody>' + projectCheckpoints(d).map(function (c) { return '<tr><td>' + esc(c) + '</td><td class="pl-chk">☐</td><td></td></tr>'; }).join('') + '</tbody></table><div class="pl-space" style="height:1.6in"></div>';
    if (s.quiz) h += '<p class="pl-dir">Show your work for every problem. Box your final answer.</p>';
    s.groups.forEach(function (g) {
      if (g.name && s.id !== 'notes') h += '<div class="pl-gh">' + esc(g.name) + (g.note ? ' <small>' + esc(g.note) + '</small>' : '') + '</div>';
      if (s.id === 'notes') return;   // notes are drawn inside notesBody
      h += rows(g.items.map(function (p, i) { return { wide: s.id === 'challenge' || wide(p), html: s.id === 'examples' && filled(plan) && i < g.items.length - 1 && !p.failed ? workedProblem(p, displayProblemLabel(p, 'Example ' + (i + 1))) : studentProblem(p, s.id === 'examples' ? displayProblemLabel(p, 'Example ' + (i + 1)) : undefined) }; }));
    });
    if (s.frame) h += '<p class="pl-frame"><b>Summary:</b> ' + frameHtml(s.frame) + '</p>';
    if (s.selfAssess) h += rateTable(s.selfAssess, 'How sure am I?');
    if (s.confidence) h += rateTable(s.confidence, 'Confidence (1 = not yet, 4 = I could teach it)');
    if (s.iCan) h += '<ul class="pl-checklist">' + s.iCan.map(function (id) { var l = P.lessonById(id); return '<li>☐ ' + esc(l ? P.iCan(l.content_objective) : id) + '</li>'; }).join('') + '</ul>';
    if (s.iCanUnits) h += rateTable(s.iCanUnits.map(function (g) { return 'Unit ' + g.unit + ': ' + g.title; }), 'How ready am I?', true);
    if (s.id === 'exit' && s.prompt === undefined && !s.groups.length && !s.frame && !s.confidence) h += lines(3);
    return h;
  }
  function rateTable(ids, head, raw) {
    return '<table class="pl-tbl pl-rate"><thead><tr><th>' + (raw ? 'Topic' : 'Lesson') + '</th><th colspan="4">' + esc(head) + '</th></tr></thead><tbody>' +
      ids.map(function (id) { return '<tr><td>' + esc(raw ? id : (id === 'LAUNCH-2' ? (SC.meta.diagnostic_label || 'Pre-algebra skills (expressions, equations, proportions)') : lessonTitle(id))) + '</td><td>1</td><td>2</td><td>3</td><td>4</td></tr>'; }).join('') + '</tbody></table>';
  }
  function notesBody(plan, s, singleDay) {
    if (!singleDay && !s.lessonDay && plan.selectedDays && plan.selectedDays.length > 1 && !s.reference && !s.routines && !s.project && !s.corrections) {
      return plan.selectedDays.map(function(n) {
        var d = P.day(n);
        return d ? '<div class="pl-gh">' + esc(d.title) + '</div>' + notesBody(plan, s, d) : '';
      }).join('');
    }
    var d = singleDay || s.lessonDay || plan.day, h = '', voc = P.vocab(d);
    if (s.routines) return '<table class="pl-tbl"><tbody>' + routines(d).map(function (r) { return '<tr><th>' + esc(r[0]) + '</th><td>' + esc(r[1]) + '</td></tr>'; }).join('') + '</tbody></table>';
    if (s.project) return '<table class="pl-tbl"><thead><tr><th>Model</th><th>Pattern in the data</th><th>Equation</th></tr></thead><tbody><tr><td>Linear</td><td>constant differences (same amount added)</td><td>⟨y = mx + b⟩</td></tr><tr><td>Exponential</td><td>constant ratios (same factor multiplied)</td><td>⟨y = a·b^x⟩</td></tr><tr><td>Quadratic</td><td>constant second differences; rises then falls (or falls then rises)</td><td>⟨y = ax^2 + bx + c⟩</td></tr></tbody></table>'.replace(/⟨[^⟩]*⟩/g, function (m) { return ms(m); }) + '<div class="pl-gh">Rubric: model choice · equation · graph · explanation · presentation (4 points each)</div>';
    if (s.corrections) return '<table class="pl-tbl pl-corr"><thead><tr><th>#</th><th>My error</th><th>Correct work</th></tr></thead><tbody>' + [1, 2, 3, 4].map(function () { return '<tr><td></td><td></td><td></td></tr>'; }).join('') + '</tbody></table>';
    if (s.reference) {
      var groups = s.byUnit ? P.byUnit(s.reference) : [{ ids: s.reference }];
      return groups.map(function (g) {
        return (g.unit ? '<div class="pl-gh">Unit ' + g.unit + ': ' + esc(g.title) + '</div>' : '') + '<table class="pl-tbl pl-ref"><thead><tr><th>Lesson</th><th>Key vocabulary</th><th>' + (s.myExample ? 'My example' : 'Key idea / example') + '</th></tr></thead><tbody>' +
          g.ids.map(function (id) { var l = P.lessonById(id); return '<tr><td><b>' + esc(l ? l.title : id) + '</b></td><td>' + esc(l ? l.key_vocabulary : '') + '</td><td>' + (filled(plan) && !s.myExample ? esc(P.keyIdea(id)) : '') + '</td></tr>'; }).join('') + '</tbody></table>';
      }).join('');
    }
    return teachNotesHtml(plan, d, filled(plan) ? 'completed' : 'guided');
  }

  /* ---------- teaching notes (Lesson days) ----------
     mode 'completed' | 'guided' (student sheet) or 'key' (teacher: completed, with the guided blanks highlighted). */
  function teachNotesHtml(plan, d, mode) {
    var h = '<div class="nt nt-' + mode + '">', idea = P.keyIdea(d.lesson_id), cards = P.teachCards(d), voc = P.vocab(d);
    if (idea) h += '<div class="nt-idea"><b>Big idea</b> ' + P.noteText(idea, mode) + '</div>';
    if (mode === 'guided' && /exploration/i.test(d.notes_style || '')) h += '<div class="pl-two"><div><div class="pl-gh">I notice…</div>' + lines(2) + '</div><div><div class="pl-gh">I wonder…</div>' + lines(2) + '</div></div>';
    cards.forEach(function (c) {
      var figs = (c.figs || []).map(function (f) { return P.diagram(f, mode); }).join('');
      h += '<div class="nt-card"><div class="nt-h">' + P.noteText(c.h, 'completed') + '</div><div class="nt-body' + (figs ? '' : ' nofig') + '"><div class="nt-text">' + (c.big ? '<p class="nt-big">' + P.noteText(c.big, mode) + '</p>' : '') +
        (c.steps.length ? '<ol class="nt-steps">' + c.steps.map(function (st) { return '<li>' + P.noteText(st, mode) + '</li>'; }).join('') + '</ol>' : '') + '</div>' +
        (figs ? '<div class="nt-figs">' + figs + '</div>' : '') + '</div></div>';
    });
    var worked = (plan.worked && plan.worked[d.day] || []).filter(function (p) { return !p.failed; });
    if (worked.length) h += '<div class="nt-wes">' + worked.map(function (p, k) { return workedNote(p, k, mode, worked.length); }).join('') + '</div>';
    if (voc.length) h += '<table class="pl-tbl pl-vocab nt-vocab' + (mode !== 'guided' ? ' filled' : '') + '"><thead><tr><th>Vocabulary</th><th>What it means / example</th></tr></thead><tbody>' + voc.map(function (v) { var def = P.define(v, d); return '<tr><td><b>' + esc(v) + '</b></td><td>' + (mode === 'guided' ? '' : mode === 'key' ? '<span class="nt-fill key">' + esc(def) + '</span>' : esc(def)) + '</td></tr>'; }).join('') + '</tbody></table>';
    if (P.watchOut(d)) h += '<p class="pl-watchout"><b>Watch out:</b> ' + P.noteText(P.watchOut(d), mode) + '</p>';
    if (P.myNotes(d)) h += '<div class="pl-mynotes">' + P.noteText(P.myNotes(d), mode).replace(/\n/g, '<br>') + '</div>';
    return h + '</div>';
  }
  function workedNote(p, k, mode, n) {
    var st = (p.steps || []).filter(function (x) { return x.t || x.m; }), h = '<div class="nt-we"><div class="nt-weh">Worked example' + (n > 1 ? ' ' + (k + 1) : '') + ' <small>' + esc(p.skillName || '') + '</small></div>' + promptHtml(p);
    if (st.length) h += '<ol class="nt-wsteps">' + st.map(function (x) {
      if (mode === 'completed') return '<li>' + ms(x.t || '') + (x.m ? ' ' + ms('⟨' + x.m + '⟩') : '') + '</li>';
      var g = P.guidedStep(x), norm = function (q) { return String(q || '').replace(/\s+/g, ''); };
      if (x.m && norm(p.prompt).indexOf(norm(x.m)) >= 0) g = { blank: '' };   // a line that only restates the problem stays printed
      if (!g.blank) return '<li>' + ms(x.t || '') + (x.m ? ' ' + ms('⟨' + x.m + '⟩') : '') + '</li>';
      var lead = ms(g.t) + (g.m ? ' ' + ms('⟨' + g.m + '⟩') : '');
      var blank = mode === 'guided' ? ' <span class="nt-blank" style="min-width:' + Math.max(3.5, Math.min(12, g.blank.replace(/\\[a-z]+|[{}^_ ]/g, '').length * 0.65 + 1.5)).toFixed(1) + 'em"></span>' : ' <span class="nt-fill key">' + (g.mathBlank ? ms('⟨' + g.blank + '⟩') : ms(g.blank)) + '</span>';
      return '<li>' + lead + blank + '</li>';
    }).join('') + '</ol>';
    var parts = p.parts || [];
    if (mode === 'guided') h += '<div class="nt-ans"><b>Answer:</b> <span class="nt-blank" style="min-width:9em"></span></div>';
    else h += '<div class="nt-ans' + (mode === 'key' ? ' key' : '') + '"><b>Answer:</b> ' + parts.map(function (pt) { return (parts.length > 1 && pt.label ? '<b>(' + esc(pt.label) + ')</b> ' : '') + ms(pt.answer || '') + (pt.answerFig ? NS.figHtml(pt.answerFig) : ''); }).join(' &nbsp; ') + '</div>';
    return h + '</div>';
  }
  P.teachNotesHtml = function (plan, d, mode) { return teachNotesHtml(plan, d, mode); };   // for tests

  /* ---------- teacher key (paper) ---------- */
  function keySheet(plan) {
    var d = plan.day, h = sheetHead(plan, 'key');
    var info = [['Standards', d.standards], ['Content objective', d.content_objective], ['Language objective', d.language_objective], ['Sentence frame', d.sentence_frame], ['Key vocabulary', d.key_vocabulary], ['Watch for', P.watchOut(d)], ['My notes', P.myNotes(d)], ['Notes style', d.notes_style], ['Do Now', d.do_now_strategy]].filter(function (r) { return r[1]; });
    if (P.keyIdea(d.lesson_id)) info.splice(4, 0, ['Key idea', P.keyIdea(d.lesson_id)]);
    if (G.MKSTD && d.standards) info = info.map(function (r) { return r[0] === 'Standards' ? ['Standards', r[1], G.MKSTD.listHtml(r[1])] : r; });
    var kv = P.vocab(d);
    if (kv.length && d.day_type === 'Lesson') info = info.map(function (r) { return r[0] === 'Key vocabulary' ? ['Key vocabulary', r[1], kv.map(function (v) { return '<b>' + esc(v) + '</b>: ' + esc(P.define(v, d)); }).join('<br>')] : r; });
    h += '<table class="pl-tbl pl-keyinfo"><tbody>' + info.map(function (r) { return '<tr><th>' + r[0] + '</th><td>' + (r[2] ? r[2] : r[0] === 'Sentence frame' ? frameHtml(r[1]) : esc(r[1])) + '</td></tr>'; }).join('') + '</tbody></table>';
    h += '<table class="pl-tbl pl-keyagenda"><thead><tr><th>Part</th><th>Min</th><th>What happens</th></tr></thead><tbody>' + plan.sections.map(function (s) { return '<tr><td><b>' + esc(s.title) + '</b></td><td>' + (s.minutes || '') + '</td><td>' + esc(s.template) + (s.prompt ? ' <i>Prompt: ' + esc(s.prompt) + '</i>' : '') + (s.launch ? ' ' + esc(launchTask(d).teacher) : '') + '</td></tr>'; }).join('') + '</tbody></table>';
    var cov = plan.coverage.filter(function (c) { return c.cover !== 'full'; });
    if (cov.length) h += '<div class="pl-keycov"><b>Add your own:</b> ' + cov.map(function (c) { return esc(c.note); }).join(' ') + '</div>';
    var noteSec = plan.sections.filter(function (s) { return s.id === 'notes'; })[0];
    if (noteSec && d.day_type === 'Lesson') {
      var nds = noteSec.lessonDay ? [noteSec.lessonDay] : (plan.selectedDays || [d.day]).map(function (n) { return P.day(n); }).filter(Boolean);
      h += '<div class="pl-sbox pl-s-notes"><div class="pl-shd">Notes — completed teacher copy <small class="nt-mode">· students have ' + (filled(plan) ? 'Completed notes' : 'Guided notes; highlighted parts are their blanks') + '</small></div>' +
        nds.map(function (x) { return (nds.length > 1 ? '<div class="pl-gh">' + esc(x.title) + '</div>' : '') + teachNotesHtml(plan, x, 'key'); }).join('') + '</div>';
    }
    plan.sections.forEach(function (s) {
      var all = []; s.groups.forEach(function (g) { g.items.forEach(function (p) { all.push([g, p]); }); });
      if (!all.length) return;
      h += '<div class="pl-shd">' + esc(s.title) + ' — answers</div>';
      s.groups.forEach(function (g) {
        if (!g.items.length) return;
        if (g.name && s.id !== 'notes') h += '<div class="pl-gh">' + esc(g.name) + '</div>';
        h += rows(g.items.map(function (p) { return { wide: wide(p) && !!p.fig && /plane|twoway/.test(p.fig.kind), html: '<div class="pl-kitem"><div class="pl-ph"><small>' + esc(p.skillName) + ' · ' + (p.failed ? '' : P.difficultyName(plan, p) + ' · ') + 'c' + (p.c || '') + '</small></div>' + promptHtml(p, s.id === 'notes' ? displayProblemLabel(p, 'Example ' + p.num) : displayProblemLabel(p, p.num + '.')) + answerHtml(p) + stepsHtml(p) + '</div>' }; }));
      });
    });
    return '<div class="pl-sheet pl-key">' + h + '</div>';
  }

  /* ---------- page ---------- */
  function picker() {
    var cur = P.day(ui.day), gk = groupKey(cur), groups = dayGroups();
    var crs = '<label class="pl-lab" for="plCourse">Course</label><select id="plCourse">' + [['math5', '5th Grade Math'], ['math6', '6th Grade Math'], ['prealgebra7', 'Pre-Algebra (7th)'], ['prealgebra', 'Pre-Algebra (8th)'], ['algebra1', 'Algebra 1'], ['geometry', 'Geometry'], ['algebra2', 'Algebra 2'], ['precalculus', 'Precalculus'], ['calculus', 'Calculus'], ['statistics', 'Statistics'], ['discrete', 'Discrete Math']].filter(function (o) { return o[0] !== 'geometry' || G.MKPLAN_SCOPE_GEOMETRY || GEO; }).map(function (o) { return '<option value="' + o[0] + '"' + (COURSE === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select>';
    var sel = crs + '<label class="pl-lab" for="plUnit">Unit</label><select id="plUnit">' + groups.map(function (g) { return '<option value="' + g.key + '"' + (g.key === gk ? ' selected' : '') + '>' + esc(g.name) + '</option>'; }).join('') + '</select>';
    var g = groups.filter(function (x) { return x.key === gk; })[0];
    var list = '<p class="pl-hint">Choose a primary day, then check additional lessons in this unit to combine their problem banks.</p>' + '<ol class="pl-days" aria-label="Days">' + g.days.map(function (d) {
      return '<li>' + (d.day_type === 'Lesson' ? '<label style="display:inline-flex;align-items:center;margin-right:7px" title="Include this lesson"><input type="checkbox" data-lesson-day="' + d.day + '"' + (ui.selectedDays.indexOf(d.day) >= 0 ? ' checked' : '') + ' aria-label="Include ' + esc(d.title) + '"></label>' : '') + '<button type="button" class="pl-daybtn' + (d.day === ui.day ? ' on' : '') + '" data-day="' + d.day + '"' + (d.day === ui.day ? ' aria-current="true"' : '') + '><span class="pl-dnum">' + d.day + '</span><span class="pl-type t-' + TYPE_CLS[d.day_type] + '">' + esc(d.day_type) + '</span><span class="pl-dtitle">' + esc(d.title) + '</span></button></li>';
    }).join('') + '</ol>';
    return sel + list;
  }
  function curNotes() { return ui.notes || (ui.plan ? ui.plan.notesMode : 'fill'); }
  function controls() {
    var lv = ['cp2', 'cp1', 'honors'].map(function (id) { var L = NS.LEVELS[id]; return '<label class="pl-lv' + (ui.level === id ? ' on' : '') + '"><input type="radio" name="plLevel" value="' + id + '"' + (ui.level === id ? ' checked' : '') + '> <span><b>' + L.name + '</b> <small>' + esc(L.long.split('·')[1] || '') + '</small></span></label>'; }).join('');
    return '<fieldset class="pl-levels"><legend class="pl-lab">Class level</legend>' + lv + '</fieldset>' +
      '<fieldset class="pl-levels"><legend class="pl-lab">Student notes</legend>' + [['filled', 'Completed notes', 'Explanations, diagram labels, steps and example answers printed'], ['fill', 'Guided notes', 'Key words, labels, step results and answers left blank; diagrams stay readable']].map(function (o) {
        return '<label class="pl-lv' + (curNotes() === o[0] ? ' on' : '') + '"><input type="radio" name="plNotes" value="' + o[0] + '"' + (curNotes() === o[0] ? ' checked' : '') + '> <span><b>' + o[1] + '</b> <small>' + o[2] + '</small></span></label>';
      }).join('') + '<p class="pl-hint">' + (ui.notes ? '' : 'Following this lesson’s planned notes style until you choose. ') + 'The teacher key always prints the completed notes.</p></fieldset>' +
      '<fieldset class="pl-levels pl-section-options"><legend class="pl-lab">Include in lesson</legend><p class="pl-hint">Unchecked sections are omitted from the lesson preview, handout, teacher key, and PowerPoint.</p>' +
      sectionSequence.map(function(k, i) { return '<div class="pl-section-choice" style="display:flex;align-items:center;gap:8px;margin:7px 0"><label style="flex:1;display:flex;gap:7px;align-items:center"><input type="checkbox" data-section-toggle="' + k + '"' + (sectionChoices[k] ? ' checked' : '') + '> ' + esc(sectionLabels[k]) + '</label>' + '<button type="button" class="btn ghost sm" data-move-section="' + i + '" data-direction="-1"' + (i === 0 ? ' disabled' : '') + ' aria-label="Move ' + esc(sectionLabels[k]) + ' up">↑</button><button type="button" class="btn ghost sm" data-move-section="' + i + '" data-direction="1"' + (i === sectionSequence.length - 1 ? ' disabled' : '') + ' aria-label="Move ' + esc(sectionLabels[k]) + ' down">↓</button><select data-occ-lesson="' + i + '" aria-label="Topic for this section"><option value="">All selected topics</option>' + ui.selectedDays.map(function(n){var d=P.day(n); return d && d.day_type==='Lesson' ? '<option value="' + esc(d.lesson_id) + '"' + ((sectionConfigs[i]||{}).lesson===d.lesson_id?' selected':'') + '>' + esc(d.title) + '</option>' : '';}).join('') + '</select>' + (['donow','mixed','examples','practice','challenge','exit'].indexOf(k) < 0 ? '' : '<label class="pl-hint">Problems <input type="number" min="0" max="30" style="width:62px" data-occ-count="' + i + '" placeholder="Auto" value="' + ((sectionConfigs[i]||{}).count == null ? '' : sectionConfigs[i].count) + '" aria-label="Problems in ' + esc(sectionLabels[k]) + ' occurrence ' + (i+1) + '"></label>') + '<button type="button" class="btn ghost sm" data-remove-repeat="' + i + '"' + (sectionSequence.filter(function(x){return x===k;}).length < 2 ? ' disabled' : '') + ' title="Remove repeated section">−</button></div>'; }).join('') + '<select id="plRepeatType" aria-label="Section to repeat">' + Object.keys(sectionLabels).map(function(k){return '<option value="' + k + '">' + esc(sectionLabels[k]) + '</option>';}).join('') + '</select> <button type="button" class="btn ghost sm" id="plRepeat">+ Repeat section</button><p class="pl-hint">Add a section again, then use arrows to arrange the sequence. All exports follow this order.</p></fieldset>' +
      '<div class="pl-btns"><button type="button" class="btn sec2" id="plNew">New problems</button></div>' +
      '<div class="pl-btns"><button type="button" class="btn" id="plPrintS">Print student handout</button><button type="button" class="btn ghost" id="plPrintK">Print teacher key</button></div>' +
      '<div class="pl-btns"><button type="button" class="btn ghost" id="plPptxStudent">Student PowerPoint</button><button type="button" class="btn ghost" id="plPptxTeacher">Teacher PowerPoint</button></div><p id="plPptxMsg" class="pl-hint" role="status" aria-live="polite"></p>' +
      '<p class="hint">' + ((A2 || PA8) ? 'Questions use approved course bank content; review the supplied answers and worked steps before printing.' : 'Every answer is re-derived from the printed problem by the same checker as the Worksheet and Assessment Generators.') + '</p>';
  }
  function render() {
    var d = P.day(ui.day);
    if (!ui.selectedDays.length || ui.selectedDays.some(function(n) { var x = P.day(n); return !x || x.unit !== d.unit; })) resetSelection();
    ui.plan = P.buildDay(ui.day, { level: ui.level, seed: ui.seed, practice: ui.practice, selectedDays: ui.selectedDays, notes: ui.notes, minutes: minutesFor(d), include: sectionChoices, counts: problemCounts });
    applySectionChoices(ui.plan);
    applyProblemLabels(ui.plan);
    $('#plPick').innerHTML = picker();
    $('#plCtl').innerHTML = controls();
    renderHead();
    renderView();
    var list = doc.querySelector('.pl-days'), on = doc.querySelector('.pl-daybtn.on');
    if (list && on) list.scrollTop = Math.max(0, on.getBoundingClientRect().top - list.getBoundingClientRect().top + list.scrollTop - list.clientHeight / 2 + on.offsetHeight / 2);
    writeHash();
    doc.title = 'Day ' + d.day + ': ' + d.title + ' · Daily Lesson Planner';
  }
  function renderHead() {
    var d = ui.plan.day, prev = P.day(ui.day - 1), next = P.day(ui.day + 1), sum = P.summary(ui.plan);
    $('#plHead').innerHTML = '<div class="pl-nav"><button type="button" class="btn ghost sm" id="plPrev"' + (prev ? '' : ' disabled') + '>← Day ' + (ui.day - 1) + '</button>' +
      '<div class="pl-htitle"><div class="pl-kicker">' + (A2 ? 'Unit ' + d.unit + ' · ' + esc(d.unit_title) + ' · ' + esc(d.unit_day) : 'Day ' + d.day + ' · Quarter ' + d.quarter + ' · Week ' + d.week + (d.unit ? ' · Unit ' + d.unit + ', day ' + esc(d.unit_day) : ' · ' + esc(d.unit_title))) + '</div><h1>' + esc(d.title) + ' <span class="pl-type t-' + TYPE_CLS[d.day_type] + '">' + esc(d.day_type) + '</span></h1>' +
      (ui.plan.selectedLessonTitles.length > 1 ? '<p class="pl-hint">Combined lessons: ' + ui.plan.selectedLessonTitles.map(esc).join(' · ') + '</p>' : '') +
      '<div class="pl-stat">' + sum.problems + ' problems' + (sum.failed ? ' · <b class="bad">' + sum.failed + ' need a new problem</b>' : sum.problems ? ((A2 || PA8) ? ' · approved bank questions' : ' · all answers checked') : '') + (d.day_type === 'Lesson' && ui.plan.sections.some(function (x) { return x.id === 'notes'; }) ? ' · <span class="nt-badge">' + (filled(ui.plan) ? 'Completed notes' : 'Guided notes') + '</span>' : '') + '</div></div>' +
      '<button type="button" class="btn ghost sm" id="plNext"' + (next ? '' : ' disabled') + '>Day ' + (ui.day + 1) + ' →</button></div>' +
      '<div class="pl-tabs" role="tablist">' + [['plan', 'Plan'], ['student', 'Student handout'], ['key', 'Teacher key']].map(function (t) { return '<button type="button" role="tab" class="tab" data-view="' + t[0] + '" aria-selected="' + (ui.view === t[0]) + '">' + t[1] + '</button>'; }).join('') + '</div>';
  }
  var previewRevision = 0;
  function renderView() {
    var v = $('#plView'), revision = ++previewRevision;
    v.className = 'pl-view v-' + ui.view;
    if (ui.view === 'student') {
      var html = studentSheet(ui.plan);
      v.innerHTML = '<div class="pl-paperwrap"><p class="pl-paging-status" role="status">Laying out printable pages…</p></div>';
      Promise.resolve(doc.fonts && doc.fonts.ready).then(function () {
        if (revision !== previewRevision || ui.view !== 'student') return;
        var pages = P.paginateStudent(html), wrap = v.querySelector('.pl-paperwrap');
        if (!wrap) return;
        wrap.replaceChildren();
        var count = doc.createElement('p');
        count.className = 'pl-paging-status';
        count.textContent = pages.length + ' letter-size page' + (pages.length === 1 ? '' : 's') + ' · preview matches the student print layout';
        wrap.appendChild(count);
        pages.forEach(function (page) { wrap.appendChild(page); });
      }).catch(function (err) {
        if (revision !== previewRevision) return;
        v.innerHTML = '<p class="pl-paging-status" role="alert">Page preview could not be laid out; printing will use browser pagination.</p><div class="pl-paperwrap">' + html + '</div>';
        if (G.console && G.console.error) G.console.error('Lesson handout pagination:', err);
      });
    } else {
      v.innerHTML = ui.view === 'plan' ? planView(ui.plan) : '<div class="pl-paperwrap">' + keySheet(ui.plan) + '</div>';
    }
    Array.prototype.forEach.call(doc.querySelectorAll('.pl-tabs .tab'), function (b) { b.setAttribute('aria-selected', String(b.getAttribute('data-view') === ui.view)); });
  }
  function doPrint(kind) {
    var root = $('#printRoot');
    function beginPrint() {
      root.replaceChildren();
      if (kind === 'student') {
        P.paginateStudent(studentSheet(ui.plan)).forEach(function (page) { root.appendChild(page); });
      } else root.innerHTML = keySheet(ui.plan);
      doc.body.classList.add('printing');
      setTimeout(function () { G.print(); }, 60);
    }
    Promise.resolve(doc.fonts && doc.fonts.ready).then(beginPrint, beginPrint);
  }
  G.addEventListener('afterprint', function () { doc.body.classList.remove('printing'); $('#printRoot').innerHTML = ''; });

  doc.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('button') : null; if (!t) return;
    if (t.classList.contains('pl-daybtn')) { ui.day = +t.getAttribute('data-day'); resetSelection(); render(); $('#plView').scrollIntoView ? G.scrollTo(0, 0) : 0; return; }
    if (t.hasAttribute('data-move-section')) {
      var from = +t.getAttribute('data-move-section'), to = from + +t.getAttribute('data-direction');
      if (from >= 0 && to >= 0 && to < sectionSequence.length) {
        sectionSequence.splice(to, 0, sectionSequence.splice(from, 1)[0]);
        var oldConfig = sectionConfigs[from];
        var nextConfigs = {};
        Object.keys(sectionConfigs).forEach(function(k) {
          var n = +k;
          if (n === from) return;
          if (from < to && n > from && n <= to) nextConfigs[n-1] = sectionConfigs[k];
          else if (to < from && n >= to && n < from) nextConfigs[n+1] = sectionConfigs[k];
          else nextConfigs[n] = sectionConfigs[k];
        });
        if (oldConfig) nextConfigs[to] = oldConfig;
        sectionConfigs = nextConfigs; saveConfigs(); saveSequence(); render();
      }
      return;
    }
    if (t.id === 'plRepeat') {
      var id = $('#plRepeatType').value;
      if (id in sectionChoices && sectionSequence.length < 30) {
        sectionChoices[id] = true; sectionSequence.push(id);
        lsSet(KEY_SECTIONS, JSON.stringify(sectionChoices));
        saveSequence(); render();
      }
      return;
    }
    if (t.hasAttribute('data-remove-repeat')) {
      var i = +t.getAttribute('data-remove-repeat'), k = sectionSequence[i];
      if (sectionSequence.filter(function(x){return x === k;}).length > 1) {
        sectionSequence.splice(i,1);
        var remaining = {};
        Object.keys(sectionConfigs).forEach(function(k) {
          var n = +k;
          if (n !== i) remaining[n > i ? n-1 : n] = sectionConfigs[k];
        });
        sectionConfigs = remaining; saveConfigs(); saveSequence(); render();
      }
      return;
    }
    if (t.id === 'plPrev') { ui.day--; resetSelection(); render(); return; }
    if (t.id === 'plNext') { ui.day++; resetSelection(); render(); return; }
    if (t.id === 'plNew') { ui.seed = Math.random().toString(36).slice(2, 7); render(); return; }
    if (t.id === 'plPrintS') { doPrint('student'); return; }
    if (t.id === 'plPrintK') { doPrint('key'); return; }
    if (t.id === 'plAddWord') { editRecord(noteDayFor(t)).words.push(['', '']); saveNoteEdits(); rerenderKeep(); var ins = doc.querySelectorAll('.pl-noted input[data-n="w"]'); if (ins.length) ins[ins.length - 1].focus(); return; }
    if (t.classList.contains('pl-delword')) { editRecord(noteDayFor(t)).words.splice(+t.getAttribute('data-i'), 1); saveNoteEdits(); rerenderKeep(); return; }
    if (t.id === 'plNotesReset') { delete P.noteEdits[noteDayFor(t).lesson_id]; saveNoteEdits(); rerenderKeep(); return; }
    if (t.id === 'plResetMin') { delete minutesStore[ui.plan.day.day_type]; lsSet(KEY_MIN, JSON.stringify(minutesStore)); P.applyMinutes(ui.plan, null); var y0 = G.scrollY; renderView(); G.scrollTo(0, y0); return; }
    if (t.id === 'plPptxStudent' || t.id === 'plPptxTeacher') {
      var audience = t.id === 'plPptxStudent' ? 'student' : 'teacher';
      var msg = $('#plPptxMsg'); t.disabled = true; msg.textContent = 'Building slides…';
      P.exportPptx(ui.plan, audience).then(function () { msg.textContent = 'Downloaded ' + P.deckFileName(ui.plan, audience) + '.'; }, function (err) { msg.textContent = 'Could not build the PowerPoint: ' + (err && err.message || err); }).then(function () { t.disabled = false; });
      return;
    }
    if (t.classList.contains('tab') && t.getAttribute('data-view')) { ui.view = t.getAttribute('data-view'); renderView(); writeHash(); return; }
    if (t.hasAttribute('data-worked-day')) { P.regenerateWorked(ui.plan, +t.getAttribute('data-worked-day'), +t.getAttribute('data-worked-k')); rerenderKeep(); return; }
    if (t.classList.contains('pl-regen')) {
      P.regenerate(ui.plan, +t.getAttribute('data-s'), +t.getAttribute('data-g'), +t.getAttribute('data-i'));
      var y = G.scrollY; renderView(); G.scrollTo(0, y); return;
    }
  });
  function noteDayFor(t) {
    var editor = t.closest && t.closest('.pl-noted');
    var day = editor && P.day(+editor.getAttribute('data-note-day'));
    return day || ui.plan.day;
  }
  var noteTimer = null;
  doc.addEventListener('input', function (e) {
    var t = e.target, k = t.getAttribute && t.getAttribute('data-n');
    if (!k || !ui.plan) return;
    var rec = editRecord(noteDayFor(t)), i = +t.getAttribute('data-i');
    if (k === 'idea' || k === 'watch' || k === 'extra') rec[k] = t.value;
    else if (k === 'cb' && rec.cards[i]) rec.cards[i].big = t.value;
    else if (k === 'cs' && rec.cards[i]) rec.cards[i].steps = t.value.split(/\n/);
    else if (k === 'w') rec.words[i][0] = t.value;
    else if (k === 'd') rec.words[i][1] = t.value;
    var reset = t.closest('.pl-noted').querySelector('#plNotesReset'); if (reset) reset.hidden = false;
    clearTimeout(noteTimer); noteTimer = setTimeout(saveNoteEdits, 300);
  });
  doc.addEventListener('toggle', function (e) { if (e.target && e.target.classList && e.target.classList.contains('pl-noted-wrap')) ui.editorOpen = e.target.open; }, true);
  function rerenderKeep() { var y = G.scrollY; renderView(); G.scrollTo(0, y); }
  doc.addEventListener('change', function (e) {
    var t = e.target;
    if (t.hasAttribute && (t.hasAttribute('data-occ-lesson') || t.hasAttribute('data-occ-count'))) {
      var idx = +(t.hasAttribute('data-occ-lesson') ? t.getAttribute('data-occ-lesson') : t.getAttribute('data-occ-count')), cfg = sectionConfigs[idx] || {};
      if (t.hasAttribute('data-occ-lesson')) cfg.lesson = t.value;
      else cfg.count = t.value === '' ? null : Math.max(0,Math.min(30,Math.round(+t.value)));
      sectionConfigs[idx] = cfg; saveConfigs(); render(); return;
    }
    if (t.hasAttribute && t.hasAttribute('data-problem-count')) {
      var sectionId = t.getAttribute('data-problem-count');
      if (['donow','mixed','examples','practice','challenge','exit'].indexOf(sectionId) < 0) return;
      var v = Math.max(0, Math.min(30, Math.round(Number(t.value))));
      if (!isFinite(v) || t.value.trim() === '') return;
      problemCounts[sectionId] = v;
      lsSet(KEY_COUNTS, JSON.stringify(problemCounts));
      render();
      return;
    }
    if (t.hasAttribute && t.hasAttribute('data-section-toggle')) {
      var k = t.getAttribute('data-section-toggle'); if (!(k in sectionChoices)) return;
      sectionChoices[k] = t.checked;
      lsSet(KEY_SECTIONS, JSON.stringify(sectionChoices));
      render(); return;
    }
    if (t.hasAttribute && t.hasAttribute('data-problem-label')) {
      var sectionId = t.getAttribute('data-problem-label'), gi = +t.getAttribute('data-group'), pi = +t.getAttribute('data-item');
      var sec = ui.plan.sections.find(function(s) { return s.id === sectionId && s.occurrenceIndex === +t.getAttribute('data-occ-index'); });
      if (sec && sec.groups[gi] && sec.groups[gi].items[pi]) {
        var value = ['I do','We do','You do'].indexOf(t.value) >= 0 ? t.value : '';
        sec.groups[gi].items[pi].teacherLabel = value;
        var key = labelKey(ui.plan.day.day, sectionId + ':' + sec.occurrenceIndex, gi, pi);
        if (value) problemLabels[key] = value; else delete problemLabels[key];
        lsSet(KEY_PROBLEM_LABELS, JSON.stringify(problemLabels));
      }
      return;
    }
    if (t.hasAttribute && t.hasAttribute('data-lesson-day')) {
      var dayNo = +t.getAttribute('data-lesson-day');
      if (t.checked) { if (ui.selectedDays.indexOf(dayNo) < 0) ui.selectedDays.push(dayNo); }
      else { ui.selectedDays = ui.selectedDays.filter(function(n) { return n !== dayNo; }); }
      ui.selectedDays.sort(function(a,b) { return a-b; });
      if (!ui.selectedDays.length) ui.selectedDays = [ui.day];
      if (ui.selectedDays.indexOf(ui.day) < 0) ui.day = ui.selectedDays[0];
      render(); return;
    }
    if (t.id === 'plCourse') { G.location.hash = '#course=' + t.value + '&day=1'; return; }
    if (t.id === 'plUnit') { var g = dayGroups().filter(function (x) { return x.key === t.value; })[0]; if (g && g.days.length) { ui.day = g.days[0].day; resetSelection(); render(); } return; }
    if (t.name === 'plLevel') { ui.level = t.value; lsSet(KEY_LEVEL, ui.level); render(); return; }
    if (t.name === 'plNotes' || t.name === 'plNotesPlan') {   // the notes setting changes only the printed notes, not the problems
      ui.notes = t.value === 'filled' ? 'filled' : 'fill'; lsSet(KEY_NOTES, ui.notes);
      ui.plan.notesMode = ui.notes; renderHead();
      $('#plCtl').innerHTML = controls(); var y1 = G.scrollY; renderView(); G.scrollTo(0, y1); return;
    }
    if (t.classList && t.classList.contains('pl-mins')) {   // a minute box: keeps the problems, updates every view
      var si = +t.getAttribute('data-s'), sec = ui.plan.sections[si], v = Math.max(0, Math.min(180, Math.round(+t.value || 0)));
      sec.minutes = v; t.value = v;
      saveMinutes(ui.plan.day, sec.id, v === sec.defaultMinutes ? null : v);
      var hd = doc.querySelector('.pl-min[data-min="' + si + '"]'); if (hd) hd.textContent = v ? v + ' min' : '';
      $('#plTotal').textContent = P.totalMinutes(ui.plan);
      $('#plResetMin').hidden = !ui.plan.sections.some(function (x) { return x.minutes !== x.defaultMinutes; });
      return;   // the handout, key and slides read the minutes when they are shown or built
    }
    if (t.id === 'plN') { ui.practice = Math.max(4, Math.min(20, +t.value || 10)); lsSet(KEY_N, ui.practice); render(); return; }
  });
  G.addEventListener('hashchange', function () { var m = /course=(\w+)/.exec(location.hash || ''); if (m && m[1] !== COURSE && /^(algebra1|geometry|algebra2|prealgebra|prealgebra7|math6|math5|precalculus|calculus|statistics|discrete)$/.test(m[1])) { G.location.reload(); return; } readHash(); resetSelection(); render(); });

  function applyTheme(t) { if (t) doc.documentElement.setAttribute('data-theme', t); else doc.documentElement.removeAttribute('data-theme'); }
  applyTheme(lsGet(KEY_THEME));
  $('#themeBtn').onclick = function () {
    var cur = doc.documentElement.getAttribute('data-theme') || (G.matchMedia && G.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var nx = cur === 'dark' ? 'light' : 'dark'; applyTheme(nx); lsSet(KEY_THEME, nx);
  };
  (function () { var cr = doc.querySelector('.crumb'); if (cr) cr.textContent = 'Daily Lesson Planner · ' + (SC.meta.course || 'Algebra 1'); doc.title = 'Daily Lesson Planner · ' + (SC.meta.course || 'Algebra 1') + ' · Mr. K\'s Classroom'; })();
  function startPlanner() { readHash(); resetSelection(); render(); P.ui = ui; }   // for tests
  if ((A2 || PA8) && G.MK_COURSE_BANKS_READY) G.MK_COURSE_BANKS_READY.then(startPlanner, startPlanner); else startPlanner();
})(window);

