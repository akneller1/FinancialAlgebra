/* Grade 5 Understanding Check: a friendly, low-pressure check of learning built from the approved Grade 5 bank.
   One question at a time or all on one page; feedback right away or at the end; hints; worked solutions;
   review of missed questions; retry missed or try a new set. Teacher summary is shown on screen only (nothing is saved). */
(function (G) {
  'use strict';
  var g5 = G.G5, el = g5.el, D = G.document, P = g5.P;
  var GROUPS = { conceptual: 'Ideas', explain: 'Reasoning', 'true-false': 'Reasoning', 'compare-strategies': 'Reasoning', 'error-analysis': 'Reasoning',
    visual: 'Pictures and models', procedural: 'Solving', numerical: 'Solving', 'fill-blank': 'Solving', ordering: 'Solving', matching: 'Solving',
    'word-problem': 'Word problems', 'real-world': 'Word problems', 'multi-step': 'Multi-step' };
  var st = { info: null, all: [], pool: [], set: [], answers: [], opts: null, skills: [] };
  var main;

  function pickSet(n, exclude) {
    /* balance: rotate through skills, and within a skill through question-type groups */
    var by = {};
    st.pool.forEach(function (p) { if (exclude && exclude[p.id]) return; var g = GROUPS[p.meta.questionType] || 'Solving'; ((by[p.skillId] = by[p.skillId] || {})[g] = (by[p.skillId][g] || [])).push(p); });
    Object.keys(by).forEach(function (s) { Object.keys(by[s]).forEach(function (g) { by[s][g] = g5.shuffle(by[s][g]); }); });
    var out = [], skills = g5.shuffle(Object.keys(by)), gi = {}, guard = 0;
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
    return g5.shuffle(out);
  }

  function start(o) {
    st.opts = o;
    st.pool = st.all.filter(function (q) { return q.level === o.level && st.skills.indexOf(q.skillId) >= 0; }).map(g5.prepare);
    st.set = pickSet(o.extra.count());
    st.answers = [];
    if (!st.set.length) { g5.errorBox(main, 'No questions match these settings.'); return; }
    if (o.extra.view() === 'page') fullPage(); else oneAtATime(0);
  }

  function progress(host, i) {
    var bar = el('div', host, 'g5-hud');
    el('span', bar, 'g5-chip', 'Question ' + (i + 1) + ' of ' + st.set.length);
    var track = el('div', bar); track.style.cssText = 'flex:1;min-width:8rem;height:.8rem;background:#e6efff;border-radius:999px;overflow:hidden';
    track.setAttribute('role', 'progressbar'); track.setAttribute('aria-valuemin', 0); track.setAttribute('aria-valuemax', st.set.length); track.setAttribute('aria-valuenow', i);
    var fill = el('div', track); fill.style.cssText = 'height:100%;width:' + (100 * i / st.set.length) + '%;background:linear-gradient(90deg,#2f7fd8,#1aa37a)';
  }

  /* quiet answer box used for "feedback at the end" and the full-page view */
  function quiet(host, p, idx) {
    var box = el('div', host, 'g5-q'); box.style.marginBottom = '1rem';
    el('div', box, 'g5-q-label', 'Question ' + (idx + 1));
    g5.math(el('div', box, 'g5-prompt'), p.prompt);
    if (p.img) { var im = el('img', box, 'g5-fig'); im.src = p.img.src; im.alt = p.img.alt; im.loading = 'lazy'; }
    var get;
    if (p.kind === 'mc' || p.kind === 'sel') {
      var list = el('div', box, 'g5-choices');
      var name = 'q' + idx;
      var inputs = p.options.map(function (o, i) {
        var lab = el('label', list, 'g5-choice'); var r = el('input', lab); r.type = p.kind === 'sel' ? 'checkbox' : 'radio'; r.name = name; r.value = i;
        el('span', lab, 'g5-letter', 'ABCDEF'.charAt(i)); g5.math(el('span', lab, 'g5-ct'), o.text);
        r.onchange = function () { Array.prototype.forEach.call(list.children, function (c) { c.classList.toggle('on', c.querySelector('input').checked); }); };
        return r;
      });
      get = function () {
        if (p.kind === 'sel') return { done: inputs.some(function (r) { return r.checked; }), ok: p.options.every(function (o, i) { return o.correct === inputs[i].checked; }) };
        var c = inputs.filter(function (r) { return r.checked; })[0];
        return { done: !!c, ok: !!c && p.options[+c.value].correct };
      };
    } else if (p.kind === 'parts') {
      var ins = p.parts.map(function (pt, i) { var row = el('label', box, 'g5-part'); el('span', row, 'g5-letter', 'abcd'.charAt(i)); g5.math(el('span', row, 'g5-pt'), pt.prompt); var x = el('input', row, 'g5-input'); x.setAttribute('aria-label', 'Part ' + 'abcd'.charAt(i)); return x; });
      get = function () { return { done: ins.some(function (x) { return x.value.trim(); }), ok: ins.every(function (x, i) { return g5.matches(x.value, p.parts[i].answer); }) }; };
    } else {
      var inp = el('input', box, 'g5-input'); inp.setAttribute('aria-label', 'Answer to question ' + (idx + 1)); inp.placeholder = 'Type your answer'; inp.autocomplete = 'off';
      get = function () { return { done: !!inp.value.trim(), ok: g5.matches(inp.value, p.answer) }; };
    }
    return { box: box, get: get };
  }

  function reveal(box, p, ok) {
    var fb = el('div', box, 'g5-feedback ' + (ok ? 'good' : 'try'), ok ? g5.pick(g5.PRAISE) : 'Not yet — here is a way to think about it.');
    if (!ok) g5.math(el('div', fb, 'g5-key'), 'Answer: ' + (Array.isArray(p.answer) ? p.answer.join('; ') : p.answer));
    var d = el('details', box, 'g5-steps'); el('summary', d, null, 'See the worked solution');
    var ol = el('ol', d); p.steps.forEach(function (t) { g5.math(el('li', ol), t); });
    if (!ok && p.meta.misconception) { var m = el('p', box, 'g5-hint'); m.textContent = 'Watch out: a common mistake is when someone ' + p.meta.misconception.replace(/\.$/, '') + '.'; }
  }

  function oneAtATime(i) {
    main.innerHTML = '';
    if (i >= st.set.length) { finish(); return; }
    progress(main, i);
    var p = st.set[i], host = el('div', main);
    if (st.opts.extra.feedback() === 'now') {
      g5.card(host, p, { label: 'Question ' + (i + 1), tries: 2, teacher: false,
        onAnswer: function (ok) { st.answers[i] = ok; }, onNext: function () { oneAtATime(i + 1); }, nextLabel: i + 1 < st.set.length ? 'Next question →' : 'See my results' });
    } else {
      var q = quiet(host, p, i);
      var nav = el('div', main, 'g5-q-tools');
      var next = el('button', nav, 'g5-btn primary', i + 1 < st.set.length ? 'Save and continue →' : 'Finish');
      next.onclick = function () { var r = q.get(); st.answers[i] = r.ok; oneAtATime(i + 1); };
      if (p.steps.length > 1) { var hb = el('button', nav, 'g5-btn ghost', '💡 Hint'); hb.onclick = function () { hb.disabled = true; g5.math(el('div', q.box, 'g5-hint'), 'Hint: ' + p.steps[0]); }; }
    }
  }

  function fullPage() {
    main.innerHTML = '';
    var head = el('section', main, 'g5-panel');
    el('h2', head, null, 'Understanding Check');
    el('p', head, 'g5-intro', 'Answer as many as you can. Use the hint buttons if you get stuck. Press “Check my work” at the bottom when you are ready.');
    var qs = st.set.map(function (p, i) {
      var q = quiet(main, p, i);
      if (p.steps.length > 1) { var hb = el('button', q.box, 'g5-btn ghost sm', '💡 Hint'); hb.style.marginTop = '.5rem'; hb.onclick = function () { hb.disabled = true; g5.math(el('div', q.box, 'g5-hint'), 'Hint: ' + p.steps[0]); }; }
      return q;
    });
    var go = el('button', main, 'g5-btn primary big', 'Check my work ✓');
    go.onclick = function () {
      go.disabled = true;
      qs.forEach(function (q, i) { var r = q.get(); st.answers[i] = r.ok; reveal(q.box, st.set[i], r.ok); });
      var b = el('div', main); summaryPanel(b);
      b.scrollIntoView({ behavior: 'smooth' });
    };
  }

  function finish() {
    main.innerHTML = '';
    if (st.opts.extra.feedback() === 'end') {
      var rev = el('section', main, 'g5-panel'); el('h2', rev, null, 'Let’s look at your answers');
      st.set.forEach(function (p, i) {
        var box = el('div', rev, 'g5-q'); box.style.margin = '.8rem 0';
        el('div', box, 'g5-q-label', 'Question ' + (i + 1)); g5.math(el('div', box, 'g5-prompt'), p.prompt);
        if (p.img) { var im = el('img', box, 'g5-fig'); im.src = p.img.src; im.alt = p.img.alt; }
        reveal(box, p, !!st.answers[i]);
      });
    }
    summaryPanel(main);
  }

  function summaryPanel(host) {
    var right = st.answers.filter(Boolean).length, n = st.set.length;
    var box = el('section', host, 'g5-panel g5-celebrate');
    el('div', box, 'big', right === n ? '🌟' : right >= n * 0.7 ? '🎉' : '💪');
    el('h2', box, null, right === n ? 'You got every one — amazing!' : right >= n * 0.7 ? 'Great thinking!' : 'Nice effort! Every mistake helps you learn.');
    el('p', box, null, 'You answered ' + right + ' of ' + n + ' correctly.' + (right < n ? ' Look over the worked solutions, then try the missed ones again.' : ''));
    var tools = el('div', box, 'g5-q-tools'); tools.style.justifyContent = 'center';
    var missed = st.set.filter(function (_, i) { return !st.answers[i]; });
    if (missed.length) {
      var rb = el('button', tools, 'g5-btn primary', 'Retry missed questions (' + missed.length + ')');
      rb.onclick = function () { st.set = g5.shuffle(missed); st.answers = []; if (st.opts.extra.view() === 'page') fullPage(); else oneAtATime(0); };
    }
    var nb = el('button', tools, 'g5-btn', 'Try a new set');
    nb.onclick = function () { var used = {}; st.set.forEach(function (p) { used[p.id] = 1; }); st.set = pickSet(st.opts.extra.count(), used); if (!st.set.length) st.set = pickSet(st.opts.extra.count()); st.answers = []; if (st.opts.extra.view() === 'page') fullPage(); else oneAtATime(0); };
    if (P.get('student') !== '1') {
      var det = el('details', box, 'g5-summary'); det.style.textAlign = 'left'; el('summary', det, null, 'Teacher view: results by skill (shown here only, never saved)');
      var t = el('table', det), h = el('tr', t); ['Skill', 'Correct', 'Questions'].forEach(function (x) { el('th', h, null, x); });
      var rows = [];
      st.info.skills.forEach(function (s) {
        var ids = st.set.map(function (p, i) { return p.skillId === s.id ? i : -1; }).filter(function (i) { return i >= 0; });
        if (!ids.length) return;
        var c = ids.filter(function (i) { return st.answers[i]; }).length;
        var r = el('tr', t); el('td', r, null, s.name); el('td', r, null, c); el('td', r, null, ids.length);
        rows.push(s.name + ': ' + c + '/' + ids.length);
      });
      var cp = el('button', det, 'g5-btn ghost sm', 'Copy summary'); cp.style.marginTop = '.5rem';
      cp.onclick = function () { var txt = 'Understanding Check · ' + st.info.unit.name + ' · ' + g5.levelName(st.opts.level) + '\n' + rows.join('\n'); if (G.navigator.clipboard) G.navigator.clipboard.writeText(txt).then(function () { cp.textContent = 'Copied!'; }); };
      var pr = el('button', det, 'g5-btn ghost sm', 'Print'); pr.style.marginLeft = '.5rem'; pr.onclick = function () { G.print(); };
    }
  }

  function boot() {
    main = D.getElementById('app');
    var unitId = P.get('unit'), info = g5.unitInfo(unitId);
    if (!info.unit) { g5.errorBox(main, 'Choose a ' + g5.COURSE_NAME + ' unit from Mr. K’s Classroom.'); return; }
    st.info = info;
    D.title = 'Understanding Check · ' + info.unit.name + ' · ' + g5.COURSE_NAME;
    g5.chrome('✅ Understanding Check', g5.COURSE_NAME + ' · Unit ' + info.number + ': ' + info.unit.name);
    var loading = el('div', main, 'g5-panel', 'Loading questions…');
    g5.load(unitId).then(function (qs) {
      loading.remove(); st.all = qs;
      g5.chooseSkills(info, function (ids) {
        st.skills = ids;
        g5.setupPanel(main, { heading: '✅ Understanding Check', intro: 'This is a chance to show what you know — not a test. Take your time, use hints, and learn from every question.', startLabel: 'Start ▶',
          extra: function (p) {
            function pills(legend, name, items, dflt) {
              var fs = el('fieldset', p, 'g5-pills'); el('legend', fs, null, legend);
              items.forEach(function (it) { var lab = el('label', fs, 'g5-pill'); var r = el('input', lab); r.type = 'radio'; r.name = name; r.value = it[0]; r.checked = it[0] === dflt; el('span', lab, null, it[1]); });
              return function () { return (p.querySelector('input[name=' + name + ']:checked') || {}).value || dflt; };
            }
            var count = pills('How many questions?', 'g5count', [['8', '8'], ['12', '12'], ['16', '16'], ['20', '20']], P.get('count') || '12');
            var view = pills('Show questions', 'g5view', [['one', 'One at a time'], ['page', 'All on one page']], P.get('view') || 'one');
            var fb = pills('Feedback', 'g5fb', [['now', 'Right away'], ['end', 'At the end']], P.get('feedback') || 'now');
            return { count: function () { return +count(); }, view: view, feedback: fb };
          },
          start: start });
      });
    }).catch(function (e) { g5.errorBox(main, e.message); });
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
})(window);
