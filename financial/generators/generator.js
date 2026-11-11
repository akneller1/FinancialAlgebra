/* Financial Algebra generators: Lesson Plan, Worksheet, Assessment, Practice Test.
 * Reads extended banks from ../banks/<unit>.json. No network beyond same-origin fetch; no AI. */
(function (G) {
  'use strict';
  var R = G.FA_RENDER, $ = function (s, r) { return (r || document).querySelector(s); };
  var params = new URLSearchParams(location.search);
  var state = { unit: params.get('unit') || 'budgeting', mode: params.get('mode') || 'worksheet', bank: null, index: null };
  var MODES = { lesson: 'Lesson Plan', worksheet: 'Worksheet', assessment: 'Assessment', practice: 'Practice Test' };
  var FORMATS = {
    'case-study': { label: 'Case Study', blurb: 'Warm-up items on one skill, then a multi-part case with data, calculations, and a written recommendation.' },
    compare: { label: 'Compare Two Options', blurb: 'Side-by-side alternatives, total-cost math, and a justified choice.' },
    document: { label: 'Financial Document Analysis', blurb: 'Fictional statements, stubs, and offers to read and interpret.' },
    analysis: { label: 'Budget & Data Analysis', blurb: 'Tables of income, expenses, or costs to total, compare, and interpret.' },
    decision: { label: 'Financial Decision Challenge', blurb: 'Open-ended decisions and claims that require evidence and reasoning.' },
    vocabulary: { label: 'Vocabulary & Concept Review', blurb: 'Terms, definitions, examples, and common misconceptions.' },
    math: { label: 'Mathematical Applications', blurb: 'Focused calculation practice that supports the decisions.' },
    mixed: { label: 'Mixed Review', blurb: 'A balanced blend of every question type.' }
  };
  function rng(seed) { var a = 0; String(seed).split('').forEach(function (c) { a = Math.imul(a ^ c.charCodeAt(0), 2654435761) >>> 0; }); return function () { a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function shuffle(a, r) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(r() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  var isOpen = function (q) { return q.format === 'open-response'; };
  var hasData = function (q) { return !!(q.scenario && (q.scenario.table || q.scenario.document)); };
  var FILTERS = {
    'case-study': null, compare: function (q) { return q.type === 'comparison'; }, document: function (q) { return q.type === 'document' || !!(q.scenario && q.scenario.document); },
    analysis: function (q) { return hasData(q) && q.type !== 'vocabulary'; }, decision: function (q) { return isOpen(q) || q.type === 'claim' || q.type === 'reasoning'; },
    vocabulary: function (q) { return q.type === 'vocabulary' || q.type === 'concept'; }, math: function (q) { return q.type === 'calculation' || (q.numeric && q.type !== 'document'); }, mixed: function () { return true; }
  };
  /* Pick n items across selected skills with family diversity (never two from the same family in a row when avoidable). */
  function pick(pool, n, r, complexity) {
    var weight = function (q) { var o = isOpen(q); return complexity === 'foundational' ? (o ? 0.3 : 1) : complexity === 'challenge' ? (o || hasData(q) ? 1 : 0.45) : 1; };
    var byFam = {}; shuffle(pool, r).forEach(function (q) { if (r() <= weight(q)) (byFam[q.family] = byFam[q.family] || []).push(q); });
    var fams = shuffle(Object.keys(byFam), r), out = [];
    while (out.length < n && fams.some(function (f) { return byFam[f].length; })) fams.forEach(function (f) { if (out.length < n && byFam[f].length) out.push(byFam[f].pop()); });
    return out;
  }
  function skillsChosen() { return Array.prototype.map.call(document.querySelectorAll('input[name=skill]:checked'), function (c) { return c.value; }); }
  function val(id) { var e = $('#' + id); return e ? e.value : null; }
  function sheet(title, sub, body, teacher) {
    return '<section class="fa-sheet' + (teacher ? ' fa-pagebreak' : '') + '"><header class="fa-sheet-head"><div><div class="fa-pill">Financial Algebra · ' + R.esc(state.bank.unitName) + (teacher ? ' · TEACHER KEY' : '') + '</div><h2>' + R.esc(title) + '</h2><div>' + R.esc(sub) + '</div></div>' +
      (teacher ? '' : '<div class="fa-name">Name ____________________<br>Date ______  Period ____</div>') + '</header>' + body + '<p class="fa-doc-kind" style="margin-top:14px">All people, companies, and numbers are fictional. Rates, taxes, and returns are illustrative assumptions, not guarantees.</p></section>';
  }
  /* ---------------- Worksheet ---------------- */
  function caseStudy(pool, n, r) {
    var anchors = shuffle(pool.filter(function (q) { return isOpen(q) && hasData(q); }), r), out = [];
    var anchor = anchors[0] || shuffle(pool.filter(isOpen), r)[0], second = n >= 8 ? anchors.filter(function (q) { return q !== anchor && q.skillId !== (anchor || {}).skillId; })[0] : null;
    var rel = pick(pool.filter(function (q) { return q !== anchor && !isOpen(q) && (!anchor || q.skillId === anchor.skillId); }), n - (anchor ? 1 : 0), r);
    if (rel.length < n - 1) rel = rel.concat(pick(pool.filter(function (q) { return q !== anchor && !isOpen(q) && rel.indexOf(q) < 0; }), n - 1 - rel.length, r));
    out = rel.slice(0, n - (anchor ? 1 : 0) - (second ? 1 : 0)).concat(anchor ? [anchor] : [], second ? [second] : []);
    return out;
  }
  function worksheet() {
    var fmt = val('wsFormat'), n = +val('count'), cx = val('complexity'), space = +val('space'), seed = val('version') + fmt + n + cx + skillsChosen().join();
    var r = rng(seed), pool = state.bank.questions.filter(function (q) { return skillsChosen().indexOf(q.skillId) >= 0; });
    var items = fmt === 'case-study' ? caseStudy(pool, n, r) : pick(pool.filter(FILTERS[fmt]), n, r, cx);
    if (fmt !== 'case-study') items.sort(function (a, b) { return (isOpen(a) ? 1 : 0) - (isOpen(b) ? 1 : 0); });
    if (!items.length) return '<p class="fa-note">No items match this format for the selected skills. Choose more skills or another format.</p>';
    var intro = '<p class="fa-note">' + R.esc(FORMATS[fmt].blurb) + (items.some(isOpen) ? ' Written responses are scored with the rubric on the key; any well-supported recommendation can earn full credit.' : '') + '</p>';
    var body = function (t) { return items.map(function (q, i) { return R.question(q, { n: i + 1, teacher: t, space: space }); }).join(''); };
    var title = FORMATS[fmt].label + ' — Version ' + val('version');
    return sheet(title, items.length + ' questions', intro + body(false)) + sheet(title, 'Answer key with worked solutions', body(true), true);
  }
  /* ---------------- Assessment ---------------- */
  var BUCKETS = [
    ['vocab', 'Vocabulary & concepts', function (q) { return (q.type === 'vocabulary' || q.type === 'concept') && !isOpen(q); }, 20],
    ['math', 'Mathematical applications', function (q) { return q.type === 'calculation' && !isOpen(q); }, 20],
    ['scenario', 'Financial scenario analysis', function (q) { return !isOpen(q) && (q.type === 'scenario' || q.type === 'document' || q.type === 'claim' || (q.type === 'comparison' && !isOpen(q))); }, 30],
    ['justify', 'Comparison & written justification', isOpen, 30]
  ];
  function points(q) { return isOpen(q) ? 8 : q.format === 'short-answer' || q.format === 'select-all' ? 2 : 1; }
  function assessment() {
    var r = rng(val('version') + 'A' + skillsChosen().join() + val('total')), target = +val('total'), pool = state.bank.questions.filter(function (q) { return skillsChosen().indexOf(q.skillId) >= 0; });
    var parts = [], used = {}, guide = [];
    BUCKETS.forEach(function (b) {
      var pctB = +val('w-' + b[0]) / 100, goal = Math.round(target * pctB), got = 0, sel = [];
      var cand = pick(pool.filter(function (q) { return b[2](q) && !used[q.id]; }), 60, r);
      for (var i = 0; i < cand.length && got < goal; i++) { var p = points(cand[i]); if (got + p <= goal + (b[0] === 'justify' ? 4 : 0)) { sel.push(cand[i]); used[cand[i].id] = 1; got += p; } }
      parts.push({ label: b[1], items: sel, pts: got }); guide.push([b[1], (pctB * 100).toFixed(0) + '%', got]);
    });
    var tot = parts.reduce(function (s, p) { return s + p.pts; }, 0), k = 0;
    var body = function (t) { k = 0; return parts.filter(function (p) { return p.items.length; }).map(function (p, i) { return '<h3 class="fa-section-h">Part ' + 'ABCD'[i] + ': ' + R.esc(p.label) + ' (' + p.pts + ' pts)</h3>' + p.items.map(function (q) { return R.question(q, { n: ++k, teacher: t, points: points(q), space: 1.2, showType: true }); }).join(''); }).join(''); };
    var scoring = '<h3 class="fa-section-h">Scoring guide</h3>' + R.table({ headers: ['Component', 'Target', 'Points'], rows: guide.map(function (g) { return [g[0], g[1], String(g[2])]; }).concat([['Total', '100%', String(tot)]]) }) +
      '<p>Multiple choice = 1 pt; short answer and select-all = 2 pts (1 pt for correct setup with a computation error); extended responses = 8 pts using the 4-criterion rubric (each criterion 0–2). Written responses are hand-scored: accept any defensible recommendation supported by accurate evidence.</p>';
    return sheet('Unit Assessment — Form ' + val('version'), tot + ' points', body(false)) + sheet('Unit Assessment — Form ' + val('version'), 'Answer key, worked solutions, and rubrics', scoring + body(true), true);
  }
  /* ---------------- Lesson plan ---------------- */
  function lesson() {
    var sid = val('lessonSkill'), idx = +sid.slice(-2), L = (state.bank.lessons || []).find(function (l) { return l.skill === idx; });
    if (!L) return '<p class="fa-note">Lesson content for this skill is not available yet.</p>';
    var r = rng(val('version') + sid), qs = state.bank.questions.filter(function (q) { return q.skillId === sid; });
    var vocab = state.bank.vocab.filter(function (v) { return L.vocab.indexOf(v.term) >= 0; });
    var docQ = shuffle(qs.filter(function (q) { return q.scenario && q.scenario.document; }), r)[0] || shuffle(state.bank.questions.filter(function (q) { return q.scenario && q.scenario.document; }), r)[0];
    var guided = shuffle(qs.filter(isOpen), r)[0], practice = pick(qs.filter(function (q) { return !isOpen(q) && q !== docQ; }), 5, r), exit = pick(qs.filter(function (q) { return q.format === 'multiple-choice' && practice.indexOf(q) < 0; }), 2, r);
    var teacher = val('lessonView') === 'teacher', ed = ' contenteditable="true" spellcheck="true"';
    var sec = function (h, inner) { return '<h3 class="fa-section-h">' + h + '</h3><div' + ed + '>' + inner + '</div>'; };
    var ul = function (a) { return '<ul>' + a.map(function (x) { return '<li>' + R.rich(x) + '</li>'; }).join('') + '</ul>'; };
    var h = '';
    h += sec('Learning objectives', '<p>Students will be able to:</p>' + ul(L.objectives));
    h += sec('Key vocabulary', '<dl>' + vocab.map(function (v) { return '<dt><strong>' + R.esc(v.term) + '</strong></dt><dd>' + (teacher ? R.rich(v.def) + (v.example ? '<br><em>Example:</em> ' + R.rich(v.example) : '') : R.lines(1)) + '</dd>'; }).join('') + '</dl>');
    h += sec('Do Now / Hook (5 min)', '<p>' + R.rich(L.hook) + '</p>' + (teacher ? '' : R.lines(3)));
    h += sec('Notes (15 min)', L.notes.map(function (n) { return '<p><strong>' + R.esc(n.h) + '.</strong> ' + (teacher ? R.rich(n.body) : R.rich(n.body.split('. ')[0]) + '. ' + R.lines(2)) + '</p>'; }).join(''));
    h += sec('Worked examples (10 min)', L.examples.map(function (e, i) { return '<div class="fa-panel flat"><p><strong>Example ' + (i + 1) + '.</strong> ' + R.rich(e.problem) + '</p>' + (teacher ? '<ol>' + e.steps.map(function (s) { return '<li>' + R.rich(s) + '</li>'; }).join('') + '</ol><div class="fa-key"><strong>Answer:</strong> ' + R.rich(e.answer) + '</div>' : R.lines(4)) + '</div>'; }).join(''));
    if (docQ) h += sec('Read the document (5 min)', R.question(docQ, { teacher: teacher, showType: false }));
    if (guided) h += sec('Guided scenario analysis (10 min)', R.question(guided, { teacher: teacher, showType: false }));
    h += sec('Independent practice', practice.map(function (q, i) { return R.question(q, { n: i + 1, teacher: teacher }); }).join(''));
    h += sec('Discussion questions', ul(L.discussion));
    h += sec('Exit ticket (5 min)', exit.map(function (q, i) { return R.question(q, { n: i + 1, teacher: teacher }); }).join(''));
    h += sec('Reflection', ul(L.reflection) + (teacher ? '' : R.lines(3)));
    if (teacher) {
      h += sec('Common misconceptions & responses', '<table class="fa-table"><thead><tr><th>Misconception</th><th>Teacher move</th></tr></thead><tbody>' + L.misconceptions.map(function (m) { return '<tr><td>' + R.rich(m[0]) + '</td><td>' + R.rich(m[1]) + '</td></tr>'; }).join('') + '</tbody></table>');
      h += sec('Differentiation & scaffolding', '<p><strong>Support:</strong></p>' + ul(L.differentiation.support) + '<p><strong>Extend:</strong></p>' + ul(L.differentiation.extend));
      h += sec('Extension activity', '<p>' + R.rich(L.extension) + '</p>');
      h += sec('Real-world connection', '<p>' + R.rich(L.realWorld) + '</p>');
      h += sec('Facilitation notes', ul(['Ask: “What would change your answer?” after every calculation.', 'Cold-call for the assumption behind each number (rate, time, rounding).', 'Accept different recommendations when the evidence supports them; push for the tradeoff.']));
    }
    return sheet(L.title, (teacher ? 'Teacher lesson plan' : 'Student guided notes') + ' · about ' + L.minutes + ' minutes · ' + (state.bank.skills.find(function (s) { return s.id === sid; }) || {}).name, '<p class="fa-noprint fa-note">Every section below is editable — click to type before printing.</p>' + h);
  }
  /* ---------------- Practice test (interactive) ---------------- */
  function practice() {
    var r = rng(Date.now()), pool = state.bank.questions.filter(function (q) { return skillsChosen().indexOf(q.skillId) >= 0 && !isOpen(q) && (q.format !== 'short-answer' || q.numeric); });
    var items = pick(pool, +val('count'), r), score = 0, done = 0;
    var host = document.createElement('div');
    host.innerHTML = '<div class="fa-panel"><h2>Practice Test — ' + R.esc(state.bank.unitName) + '</h2><p>Answer each question, then check it. Worked solutions appear after you check.</p><p role="status" id="ptScore">Score: 0 of ' + items.length + '</p></div>' +
      items.map(function (q, i) {
        var input = q.format === 'multiple-choice' ? q.options.map(function (o, j) { return '<label class="fa-opt"><input type="radio" name="pt' + i + '" value="' + j + '"> ' + R.rich(o.text) + '</label>'; }).join('<br>') :
          q.format === 'select-all' ? q.options.map(function (o, j) { return '<label class="fa-opt"><input type="checkbox" name="pt' + i + '" value="' + j + '"> ' + R.rich(o.text) + '</label>'; }).join('<br>') :
            '<label class="fa-field">Your answer<input name="pt' + i + '" inputmode="decimal" autocomplete="off"></label>';
        var stripped = Object.assign({}, q, { options: null });
        return '<div class="fa-panel flat" data-i="' + i + '">' + R.question(stripped, { n: i + 1 }).replace(/<div class="fa-lines"[\s\S]*?<\/div><\/div>/, '') + input + '<p><button class="fa-btn primary" data-check="' + i + '">Check</button></p><div class="fa-fb" aria-live="polite"></div></div>';
      }).join('');
    host.addEventListener('click', function (e) {
      var i = e.target.getAttribute('data-check'); if (i == null) return;
      var q = items[+i], box = host.querySelector('[data-i="' + i + '"]'), ok;
      if (q.format === 'multiple-choice') { var c = box.querySelector('input:checked'); if (!c) return; ok = q.options[+c.value].correct; }
      else if (q.format === 'select-all') { var chosen = Array.prototype.map.call(box.querySelectorAll('input:checked'), function (x) { return +x.value; }); ok = q.options.every(function (o, j) { return o.correct === (chosen.indexOf(j) >= 0); }); }
      else ok = R.checkNumeric(q, box.querySelector('input').value);
      e.target.disabled = true; done++; if (ok) score++;
      box.querySelector('.fa-fb').innerHTML = '<div class="' + (ok ? 'fa-key' : 'fa-mis') + '"><strong>' + (ok ? 'Correct.' : 'Not quite.') + '</strong> Answer: ' + R.rich(Array.isArray(q.answer) ? q.answer.join('; ') : q.answer) + '</div><ol>' + q.solutionSteps.map(function (s) { return '<li>' + R.rich(s) + '</li>'; }).join('') + '</ol>';
      $('#ptScore').textContent = 'Score: ' + score + ' of ' + items.length + (done === items.length ? ' — finished (' + Math.round(score / items.length * 100) + '%)' : '');
    });
    return host;
  }
  /* ---------------- UI ---------------- */
  function controls() {
    var b = state.bank, m = state.mode;
    var skills = '<fieldset class="fa-field"><legend>Skills</legend><div class="fa-checks">' + b.skills.map(function (s) { return '<label><input type="checkbox" name="skill" value="' + s.id + '" checked> ' + R.esc(s.name) + '</label>'; }).join('') + '</div></fieldset>';
    var version = '<label class="fa-field">Version<select id="version">' + 'ABCDEF'.split('').map(function (v) { return '<option>' + v + '</option>'; }).join('') + '</select></label>';
    var h = '<div class="fa-tabs fa-noprint" role="tablist">' + Object.keys(MODES).map(function (k) { return '<button class="fa-btn" role="tab" aria-selected="' + (k === m) + '" data-mode="' + k + '">' + MODES[k] + '</button>'; }).join('') + '</div>';
    if (m === 'worksheet') h += skills + '<div class="fa-grid"><label class="fa-field">Format<select id="wsFormat">' + Object.keys(FORMATS).map(function (k) { return '<option value="' + k + '">' + FORMATS[k].label + '</option>'; }).join('') + '</select></label><label class="fa-field">Questions<select id="count"><option>4</option><option selected>6</option><option>8</option><option>10</option><option>12</option></select></label><label class="fa-field">Complexity<select id="complexity"><option value="foundational">Foundational</option><option value="standard" selected>Standard</option><option value="challenge">Challenge</option></select></label><label class="fa-field">Writing space<select id="space"><option value="0.7">Compact</option><option value="1" selected>Standard</option><option value="1.6">Extra</option></select></label>' + version + '</div>';
    if (m === 'assessment') h += skills + '<div class="fa-grid"><label class="fa-field">Target points<select id="total"><option>40</option><option selected>50</option><option>60</option><option>80</option></select></label>' + BUCKETS.map(function (bk) { return '<label class="fa-field">' + bk[1] + ' (%)<input id="w-' + bk[0] + '" type="number" min="0" max="100" step="5" value="' + bk[3] + '"></label>'; }).join('') + version + '</div>';
    if (m === 'lesson') h += '<div class="fa-grid"><label class="fa-field">Lesson (skill)<select id="lessonSkill">' + b.skills.map(function (s) { return '<option value="' + s.id + '">' + R.esc(s.name) + '</option>'; }).join('') + '</select></label><label class="fa-field">Version<select id="lessonView"><option value="teacher">Teacher plan</option><option value="student">Student guided notes</option></select></label>' + version + '</div>';
    if (m === 'practice') h += skills + '<div class="fa-grid"><label class="fa-field">Questions<select id="count"><option>8</option><option selected>12</option><option>16</option><option>20</option></select></label></div>';
    h += '<p class="fa-noprint" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px"><button class="fa-btn primary" id="go">' + (m === 'practice' ? 'Start practice test' : 'Generate') + '</button>' + (m === 'practice' ? '' : '<button class="fa-btn" id="print" onclick="window.print()">Print / Save PDF</button>') + '</p>';
    return h;
  }
  function render() {
    $('#controls').innerHTML = controls();
    $('#title').textContent = 'Financial Algebra ' + MODES[state.mode] + ' — ' + state.bank.unitName;
    document.title = MODES[state.mode] + ' · ' + state.bank.unitName + ' | Financial Algebra';
    $('#controls').addEventListener('click', function (e) { var md = e.target.getAttribute('data-mode'); if (md) { state.mode = md; history.replaceState(null, '', '?unit=' + state.unit + '&mode=' + md); render(); } });
    $('#go').onclick = generate; generate();
  }
  function generate() {
    var out = $('#output');
    if (state.mode !== 'lesson' && !skillsChosen().length) { out.innerHTML = '<p class="fa-note">Select at least one skill.</p>'; return; }
    if (state.mode === 'practice') { out.replaceChildren(practice()); return; }
    out.innerHTML = { worksheet: worksheet, assessment: assessment, lesson: lesson }[state.mode]();
  }
  function unitPicker(index) {
    var sel = $('#unit'); sel.innerHTML = index.units.map(function (u) { return '<option value="' + u.unitId + '"' + (u.unitId === state.unit ? ' selected' : '') + '>' + R.esc(u.name) + '</option>'; }).join('');
    sel.onchange = function () { location.search = '?unit=' + sel.value + '&mode=' + state.mode; };
  }
  G.FA_GENERATOR = { pick: pick, FILTERS: FILTERS, FORMATS: FORMATS, BUCKETS: BUCKETS, points: points };
  if (typeof document === 'undefined' || !document.getElementById('output')) return;
  fetch('../banks/index.json').then(function (r) { return r.json(); }).then(function (index) {
    if (!index.units.some(function (u) { return u.unitId === state.unit; })) state.unit = index.units[0].unitId;
    unitPicker(index);
    return fetch('../banks/' + state.unit + '.json').then(function (r) { return r.json(); });
  }).then(function (bank) { state.bank = bank; render(); })
    .catch(function (e) { $('#output').innerHTML = '<p class="fa-note">Unable to load the question bank (' + R.esc(e.message) + '). Open this page from the website rather than the file system.</p>'; });
})(typeof window !== 'undefined' ? window : globalThis);
