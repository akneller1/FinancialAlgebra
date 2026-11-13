/* Elementary Understanding Check: a friendly, low-pressure check of learning built from the course's approved bank.
   One question at a time or all on one page; feedback right away or at the end; hints; worked solutions;
   review of missed questions; retry missed or try a new set; a student link that opens the same settings; a printable
   results page (print it or save it as a PDF) for the teacher. Nothing is saved or sent anywhere. */
(function (G) {
  'use strict';
  var K = G.MKEL, el = K.el, D = G.document, P = K.P;
  var GROUPS = { conceptual: 'Ideas', explain: 'Reasoning', 'true-false': 'Reasoning', 'compare-strategies': 'Reasoning', 'error-analysis': 'Reasoning',
    visual: 'Pictures and models', procedural: 'Solving', numerical: 'Solving', 'fill-blank': 'Solving', ordering: 'Solving', matching: 'Solving',
    'word-problem': 'Word problems', 'real-world': 'Word problems', 'multi-step': 'Multi-step' };
  var st = { info: null, all: [], pool: [], set: [], answers: [], responses: [], opts: null, skills: [], round: 1 };
  var main;

  function pickSet(n, exclude) {
    /* balance: rotate through skills, and within a skill through question-type groups */
    var by = {};
    st.pool.forEach(function (p) { if (exclude && exclude[p.id]) return; var g = GROUPS[p.meta.questionType] || 'Solving'; ((by[p.skillId] = by[p.skillId] || {})[g] = (by[p.skillId][g] || [])).push(p); });
    Object.keys(by).forEach(function (s) { Object.keys(by[s]).forEach(function (g) { by[s][g] = K.shuffle(by[s][g]); }); });
    var out = [], skills = K.shuffle(Object.keys(by)), gi = {}, guard = 0;
    while (out.length < n && guard++ < 500) {
      var any = false;
      skills.forEach(function (s) {
        if (out.length >= n) return;
        var gs = Object.keys(by[s]).filter(function (g) { return by[s][g].length; });
        if (!gs.length) return;
        any = true;
        gi[s] = (gi[s] || 0) + 1;
        var g = gs[gi[s] % gs.length];
        out.push(by[s][g].pop());
      });
      if (!any) break;
    }
    return K.shuffle(out);
  }

  function start(o) {
    st.opts = o;
    st.pool = st.all.filter(function (q) { return q.level === o.level && st.skills.indexOf(q.skillId) >= 0; }).map(K.prepare);
    st.set = pickSet(o.extra.count());
    st.answers = []; st.responses = []; st.round = 1;
    if (!st.set.length) { K.errorBox(main, 'No questions match these settings.'); return; }
    if (o.extra.view() === 'page') fullPage(); else oneAtATime(0);
  }

  function progress(host, i) {
    var bar = el('div', host, 'el-hud');
    el('span', bar, 'el-chip', 'Question ' + (i + 1) + ' of ' + st.set.length);
    var track = el('div', bar); track.style.cssText = 'flex:1;min-width:8rem;height:.8rem;background:#e6efff;border-radius:999px;overflow:hidden';
    track.setAttribute('role', 'progressbar'); track.setAttribute('aria-valuemin', 0); track.setAttribute('aria-valuemax', st.set.length); track.setAttribute('aria-valuenow', i);
    var fill = el('div', track); fill.style.cssText = 'height:100%;width:' + (100 * i / st.set.length) + '%;background:linear-gradient(90deg,#2f7fd8,#1aa37a)';
  }

  /* quiet answer box used for "feedback at the end" and the full-page view */
  function quiet(host, p, idx) {
    var box = el('div', host, 'el-q'); box.style.marginBottom = '1rem';
    el('div', box, 'el-q-label', 'Question ' + (idx + 1));
    K.math(el('div', box, 'el-prompt'), p.prompt);
    if (p.img) { var im = el('img', box, 'el-fig'); im.src = p.img.src; im.alt = p.img.alt; im.loading = 'lazy'; }
    var get;
    if (p.kind === 'mc' || p.kind === 'sel') {
      var list = el('div', box, 'el-choices');
      var name = 'q' + idx;
      var inputs = p.options.map(function (o, i) {
        var lab = el('label', list, 'el-choice'); var r = el('input', lab); r.type = p.kind === 'sel' ? 'checkbox' : 'radio'; r.name = name; r.value = i;
        el('span', lab, 'el-letter', 'ABCDEF'.charAt(i)); K.math(el('span', lab, 'el-ct'), o.text);
        r.onchange = function () { Array.prototype.forEach.call(list.children, function (c) { c.classList.toggle('on', c.querySelector('input').checked); }); };
        return r;
      });
      get = function () {
        if (p.kind === 'sel') return { done: inputs.some(function (r) { return r.checked; }), ok: p.options.every(function (o, i) { return o.correct === inputs[i].checked; }), text: p.options.filter(function (o, i) { return inputs[i].checked; }).map(function (o) { return o.text; }).join('; ') };
        var c = inputs.filter(function (r) { return r.checked; })[0];
        return { done: !!c, ok: !!c && p.options[+c.value].correct, text: c ? p.options[+c.value].text : '' };
      };
    } else if (p.kind === 'parts') {
      var ins = p.parts.map(function (pt, i) { var row = el('label', box, 'el-part'); el('span', row, 'el-letter', 'abcd'.charAt(i)); K.math(el('span', row, 'el-pt'), pt.prompt); var x = el('input', row, 'el-input'); x.setAttribute('aria-label', 'Part ' + 'abcd'.charAt(i)); return x; });
      get = function () { return { done: ins.some(function (x) { return x.value.trim(); }), ok: ins.every(function (x, i) { return K.matches(x.value, p.parts[i].answer); }), text: ins.map(function (x, i) { return '(' + 'abcd'.charAt(i) + ') ' + x.value.trim(); }).join('; ') }; };
    } else {
      var inp = el('input', box, 'el-input'); inp.setAttribute('aria-label', 'Answer to question ' + (idx + 1)); inp.placeholder = 'Type your answer'; inp.autocomplete = 'off';
      get = function () { return { done: !!inp.value.trim(), ok: K.matches(inp.value, p.answer), text: inp.value.trim() }; };
    }
    return { box: box, get: get };
  }

  function reveal(box, p, ok) {
    var fb = el('div', box, 'el-feedback ' + (ok ? 'good' : 'try'), ok ? K.pick(K.PRAISE) : 'Not yet — here is a way to think about it.');
    if (!ok) K.math(el('div', fb, 'el-key'), 'Answer: ' + (Array.isArray(p.answer) ? p.answer.join('; ') : p.answer));
    var d = el('details', box, 'el-steps'); el('summary', d, null, 'See the worked solution');
    var ol = el('ol', d); p.steps.forEach(function (t) { K.math(el('li', ol), t); });
    if (!ok && p.meta.misconception) { var m = el('p', box, 'el-hint'); m.textContent = 'Watch out: a common mistake is when someone ' + p.meta.misconception.replace(/\.$/, '') + '.'; }
  }

  function oneAtATime(i) {
    main.innerHTML = '';
    if (i >= st.set.length) { finish(); return; }
    progress(main, i);
    var p = st.set[i], host = el('div', main);
    if (st.opts.extra.feedback() === 'now') {
      K.card(host, p, { label: 'Question ' + (i + 1), tries: 2, teacher: false,
        onAnswer: function (ok, tries, text) { st.answers[i] = ok; st.responses[i] = text || ''; }, onNext: function () { oneAtATime(i + 1); }, nextLabel: i + 1 < st.set.length ? 'Next question →' : 'See my results' });
    } else {
      var q = quiet(host, p, i);
      var nav = el('div', main, 'el-q-tools');
      var next = el('button', nav, 'el-btn primary', i + 1 < st.set.length ? 'Save and continue →' : 'Finish');
      next.onclick = function () { var r = q.get(); st.answers[i] = r.ok; st.responses[i] = r.text || ''; oneAtATime(i + 1); };
      if (p.steps.length > 1) { var hb = el('button', nav, 'el-btn ghost', '💡 Hint'); hb.onclick = function () { hb.disabled = true; K.math(el('div', q.box, 'el-hint'), 'Hint: ' + p.steps[0]); }; }
    }
  }

  function fullPage() {
    main.innerHTML = '';
    var head = el('section', main, 'el-panel');
    el('h2', head, null, 'Understanding Check');
    el('p', head, 'el-intro', 'Answer as many as you can. Use the hint buttons if you get stuck. Press “Check my work” at the bottom when you are ready.');
    var qs = st.set.map(function (p, i) {
      var q = quiet(main, p, i);
      if (p.steps.length > 1) { var hb = el('button', q.box, 'el-btn ghost sm', '💡 Hint'); hb.style.marginTop = '.5rem'; hb.onclick = function () { hb.disabled = true; K.math(el('div', q.box, 'el-hint'), 'Hint: ' + p.steps[0]); }; }
      return q;
    });
    var go = el('button', main, 'el-btn primary big', 'Check my work ✓');
    go.onclick = function () {
      go.disabled = true;
      qs.forEach(function (q, i) { var r = q.get(); st.answers[i] = r.ok; st.responses[i] = r.text || ''; reveal(q.box, st.set[i], r.ok); });
      var b = el('div', main); summaryPanel(b);
      b.scrollIntoView({ behavior: 'smooth' });
    };
  }

  function finish() {
    main.innerHTML = '';
    if (st.opts.extra.feedback() === 'end') {
      var rev = el('section', main, 'el-panel'); el('h2', rev, null, 'Let’s look at your answers');
      st.set.forEach(function (p, i) {
        var box = el('div', rev, 'el-q'); box.style.margin = '.8rem 0';
        el('div', box, 'el-q-label', 'Question ' + (i + 1)); K.math(el('div', box, 'el-prompt'), p.prompt);
        if (p.img) { var im = el('img', box, 'el-fig'); im.src = p.img.src; im.alt = p.img.alt; }
        reveal(box, p, !!st.answers[i]);
      });
    }
    summaryPanel(main);
  }

  function summaryPanel(host) {
    var right = st.answers.filter(Boolean).length, n = st.set.length;
    var box = el('section', host, 'el-panel el-celebrate');
    el('div', box, 'big', right === n ? '🌟' : right >= n * 0.7 ? '🎉' : '💪');
    el('h2', box, null, right === n ? 'You got every one — amazing!' : right >= n * 0.7 ? 'Great thinking!' : 'Nice effort! Every mistake helps you learn.');
    el('p', box, null, 'You answered ' + right + ' of ' + n + ' correctly.' + (right < n ? ' Look over the worked solutions, then try the missed ones again.' : ''));
    var tools = el('div', box, 'el-q-tools'); tools.style.justifyContent = 'center';
    var missed = st.set.filter(function (_, i) { return !st.answers[i]; });
    if (missed.length) {
      var rb = el('button', tools, 'el-btn primary', 'Retry missed questions (' + missed.length + ')');
      rb.onclick = function () { st.set = K.shuffle(missed); st.answers = []; st.responses = []; st.round++; if (st.opts.extra.view() === 'page') fullPage(); else oneAtATime(0); };
    }
    var nb = el('button', tools, 'el-btn', 'Try a new set');
    nb.onclick = function () { var used = {}; st.set.forEach(function (p) { used[p.id] = 1; }); st.set = pickSet(st.opts.extra.count(), used); if (!st.set.length) st.set = pickSet(st.opts.extra.count()); st.answers = []; st.responses = []; st.round = 1; if (st.opts.extra.view() === 'page') fullPage(); else oneAtATime(0); };
    var rp = el('button', tools, 'el-btn', '🖨 Print or save my results (PDF)');
    rp.onclick = function () { resultsPage(); };
    if (P.get('student') !== '1') {
      var det = el('details', box, 'el-summary'); det.style.textAlign = 'left'; el('summary', det, null, 'Teacher view: results by skill (shown here only, never saved)');
      var t = el('table', det), h = el('tr', t); ['Skill', 'Correct', 'Questions'].forEach(function (x) { el('th', h, null, x); });
      var rows = [];
      st.info.skills.forEach(function (s) {
        var ids = st.set.map(function (p, i) { return p.skillId === s.id ? i : -1; }).filter(function (i) { return i >= 0; });
        if (!ids.length) return;
        var c = ids.filter(function (i) { return st.answers[i]; }).length;
        var r = el('tr', t); el('td', r, null, s.name); el('td', r, null, c); el('td', r, null, ids.length);
        rows.push(s.name + ': ' + c + '/' + ids.length);
      });
      var cp = el('button', det, 'el-btn ghost sm', 'Copy summary'); cp.style.marginTop = '.5rem';
      cp.onclick = function () { var txt = 'Understanding Check · ' + st.info.unit.name + ' · ' + K.levelName(st.opts.level) + '\n' + rows.join('\n'); if (G.navigator.clipboard) G.navigator.clipboard.writeText(txt).then(function () { cp.textContent = 'Copied!'; }); };
      var pr = el('button', det, 'el-btn ghost sm', 'Print'); pr.style.marginLeft = '.5rem'; pr.onclick = function () { G.print(); };
    }
  }

  /* A printable record of this attempt for the teacher: name (typed on the page by the student, never stored), date, settings, score,
     and for every question the student's answer, whether it was correct, and the correct answer. The browser's Print
     dialog can save it as a PDF. */
  function resultsPage() {
    var old = D.getElementById('el-results'); if (old) old.remove();
    var right = st.answers.filter(Boolean).length, n = st.set.length;
    var r = el('section', D.body, 'el-results'); r.id = 'el-results';
    el('h1', r, null, 'Understanding Check Results');
    var meta = el('table', r, 'el-results-meta');
    [['Name', null], ['Date', new Date().toLocaleDateString()], ['Course', (st.info.course && st.info.course.name) || K.CFG.label],
     ['Unit', 'Unit ' + st.info.number + ': ' + st.info.unit.name], ['Level', K.levelName(st.opts.level)], ['Score', right + ' out of ' + n + (st.round > 1 ? ' (retry of missed questions, round ' + st.round + ')' : '')]]
      .forEach(function (x) {
        var tr = el('tr', meta); el('th', tr, null, x[0]); var td = el('td', tr, null, x[1]);
        if (x[1] === null) { var ni = el('input', td, 'el-results-name'); ni.type = 'text'; ni.maxLength = 60; ni.placeholder = 'Type your name here'; ni.setAttribute('aria-label', 'Your name (printed only, never saved)'); ni.autocomplete = 'off'; }
      });
    var t = el('table', r, 'el-results-table'), h = el('tr', t);
    ['#', 'Question', 'My answer', 'Result', 'Correct answer'].forEach(function (x) { el('th', h, null, x); });
    st.set.forEach(function (p, i) {
      var tr = el('tr', t); el('td', tr, null, String(i + 1));
      var q = el('td', tr); K.math(el('div', q), p.prompt); if (p.img) { var im = el('img', q); im.src = p.img.src; im.alt = p.img.alt; }
      K.math(el('td', tr), st.responses[i] || '(no answer)');
      el('td', tr, st.answers[i] ? 'ok' : 'no', st.answers[i] ? '✓ Correct' : '✗ Not yet');
      K.math(el('td', tr), Array.isArray(p.answer) ? p.answer.join('; ') : String(p.answer));
    });
    var bySkill = el('table', r, 'el-results-table'), h2 = el('tr', bySkill); ['Skill', 'Correct', 'Questions'].forEach(function (x) { el('th', h2, null, x); });
    st.info.skills.forEach(function (s) {
      var ids = st.set.map(function (p, i) { return p.skillId === s.id ? i : -1; }).filter(function (i) { return i >= 0; });
      if (!ids.length) return;
      var tr = el('tr', bySkill); el('td', tr, null, s.name); el('td', tr, null, String(ids.filter(function (i) { return st.answers[i]; }).length)); el('td', tr, null, String(ids.length));
    });
    el('p', r, 'el-results-note', 'Mr. K’s Classroom · This page was made on this device. Nothing was saved or sent.');
    var bar = el('div', r, 'el-results-bar');
    var pb = el('button', bar, 'el-btn primary', '🖨 Print or save as PDF'); pb.onclick = function () { G.print(); };
    var cb = el('button', bar, 'el-btn', 'Close'); cb.onclick = function () { r.remove(); D.body.classList.remove('el-results-open'); };
    D.body.classList.add('el-results-open');
    r.scrollIntoView();
    var first = r.querySelector('.el-results-name'); if (first) try { first.focus({ preventScroll: true }); } catch (e) {}
  }

  function boot() {
    main = D.getElementById('app');
    var unitId = P.get('unit'), info = K.unitInfo(unitId);
    if (!info.unit) { K.errorBox(main, 'Choose a ' + K.CFG.label + ' unit from Mr. K’s Classroom.'); return; }
    st.info = info;
    D.title = 'Understanding Check · ' + info.unit.name + ' · ' + K.CFG.label;
    K.chrome('✅ Understanding Check', K.CFG.label + ' · Unit ' + info.number + ': ' + info.unit.name);
    var loading = el('div', main, 'el-panel', 'Loading questions…');
    K.load(unitId).then(function (qs) {
      loading.remove(); st.all = qs;
      K.chooseSkills(info, function (ids) {
        st.skills = ids;
        K.setupPanel(main, { heading: '✅ Understanding Check', intro: 'This is a chance to show what you know — not a test. Take your time, use hints, and learn from every question.', startLabel: 'Start ▶',
          extra: function (p) {
            function pills(legend, name, items, dflt) {
              var fs = el('fieldset', p, 'el-pills'); el('legend', fs, null, legend);
              items.forEach(function (it) { var lab = el('label', fs, 'el-pill'); var r = el('input', lab); r.type = 'radio'; r.name = name; r.value = it[0]; r.checked = it[0] === dflt; el('span', lab, null, it[1]); });
              return function () { return (p.querySelector('input[name=' + name + ']:checked') || {}).value || dflt; };
            }
            var count = pills('How many questions?', 'elcount', [['8', '8'], ['12', '12'], ['16', '16'], ['20', '20']], P.get('count') || '12');
            var view = pills('Show questions', 'elview', [['one', 'One at a time'], ['page', 'All on one page']], P.get('view') || 'one');
            var fb = pills('Feedback', 'elfb', [['now', 'Right away'], ['end', 'At the end']], P.get('feedback') || 'now');
            return { count: function () { return +count(); }, view: view, feedback: fb };
          },
          skills: ids, linkParams: function () { var g = function (n, d) { return (main.querySelector('input[name=' + n + ']:checked') || {}).value || d; }; return { count: g('elcount', '12'), view: g('elview', 'one'), feedback: g('elfb', 'now') }; },
          start: start });
      });
    }).catch(function (e) { K.errorBox(main, e.message); });
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
})(window);
