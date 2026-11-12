/* Grade 5 (math5) shared runtime: bank loading, question normalization, answer checking, the question card,
   friendly feedback, zoom and presentation controls. Used by the Grade 5 games, Understanding Checks and flashcards.
   No network calls except the site's own question-bank files; no accounts; nothing is stored about students. */
(function (G) {
  'use strict';
  var D = G.document;
  var P = new URLSearchParams(G.location.search);
  var COURSE = 'math5';
  var LEVELS = [['cp2', 'Remedial'], ['cp1', 'Standard'], ['honors', 'Advanced']];
  var PRAISE = ['Great thinking!', 'You got it!', 'Nice work!', 'Super job!', 'Way to go!', 'That’s right!', 'Excellent reasoning!', 'You nailed it!'];
  var NUDGE = ['Almost! Let’s try another strategy.', 'Not quite yet. Check each step.', 'Good try! Look at the hint.', 'Keep going — you can do this!', 'Check your place values.', 'Try using a picture to help.'];

  function el(tag, parent, cls, text) {
    var e = D.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function math(node, text) {
    node.innerHTML = G.MK_MATH_DISPLAY ? G.MK_MATH_DISPLAY.html(String(text == null ? '' : text)) : esc(text);
    return node;
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  /* ---------- exact numbers for answer checking ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a || 1; }
  function frac(n, d) { if (d < 0) { n = -n; d = -d; } var g = gcd(n, d); return [n / g, d / g]; }
  function parseNum(s) {
    s = String(s).replace(/[‑−]/g, '-').replace(/,(?=\d{3})/g, '').trim();
    var m = /^\$?\s*(-?\d+)\s+(\d+)\s*\/\s*(\d+)/.exec(s);
    if (m) return frac(+m[1] * +m[3] + +m[2], +m[3]);
    m = /^\$?\s*(-?\d+)\s*\/\s*(\d+)/.exec(s);
    if (m) return +m[2] ? frac(+m[1], +m[2]) : null;
    m = /^\$?\s*(-?\d*)\.(\d+)/.exec(s);
    if (m) { var d = Math.pow(10, m[2].length); return frac((m[1] === '' || m[1] === '-' ? 0 : +m[1]) * d + (m[1].charAt(0) === '-' ? -1 : 1) * +m[2], d); }
    m = /^\$?\s*(-?\d+)/.exec(s);
    if (m) return [+m[1], 1];
    return null;
  }
  function restAfterNumber(s) {
    return String(s).replace(/[‑]/g, '-').replace(/^\s*\$?\s*-?[\d,]*(\.\d+)?(\s+\d+\s*\/\s*\d+|\s*\/\s*\d+)?/, '').trim();
  }
  function norm(s) {
    return String(s == null ? '' : s).replace(/[‑−]/g, '-').replace(/[’]/g, "'").toLowerCase().replace(/,(?=\d{3})/g, '')
      .replace(/\s+/g, ' ').replace(/^(the|a|an|point|shape|triangle|box|garden|pack|mix) /, '').replace(/[.!]+$/, '').trim();
  }
  function unitWord(u) { return norm(u).replace(/feet/g, 'foot').replace(/(ch|sh|x|bus)es\b/g, '$1').replace(/s\b/g, ''); }
  /* Is a typed answer equivalent to the key? Numbers compare by exact value; units may be left off. */
  function matches(typed, key) {
    var t = String(typed || '').trim(), k = String(key || '').trim();
    if (!t) return false;
    if (norm(t) === norm(k)) return true;
    // ordered pairs, remainders and lists compare piece by piece
    var pair = /^\(?\s*([^,()]+?)\s*,\s*([^,()]+?)\s*\)?$/;
    if (/^\(.+,.+\)$/.test(k)) { var a = pair.exec(t), b = pair.exec(k); return !!(a && b && matches(a[1], b[1]) && matches(a[2], b[2])); }
    var rk = /^([\d,]+)\s*R\s*(\d+)$/i.exec(k);
    if (rk) { var rt = /^([\d,]+)\s*r\s*(\d+)$/i.exec(t.replace(/\s+/g, ' ')); return !!(rt && +rt[1].replace(/,/g, '') === +rk[1].replace(/,/g, '') && +rt[2] === +rk[2]); }
    if (k.indexOf(',') > 0 && /\d, /.test(k)) {
      var ks = k.split(/,\s*/), ts = t.split(/\s*,\s*|\s+(?=\d+(?:\.\d+)?(?:,|$))/);
      ts = t.split(/\s*,\s*/);
      return ks.length === ts.length && ks.every(function (x, i) { return matches(ts[i], x); });
    }
    var cmp = /^\s*$/;
    var nk = parseNum(k), nt = parseNum(t);
    if (nk && nt && nk[0] === nt[0] && nk[1] === nt[1]) {
      var uk = restAfterNumber(k), ut = restAfterNumber(t);
      // compound measures such as "5 feet 3 inches" must match completely
      if (/\d/.test(uk)) return norm(t).replace(/\s/g, '') === norm(k).replace(/\s/g, '') || compound(t, k);
      return !ut || unitWord(ut) === unitWord(uk) || unitWord('square ' + ut) === unitWord(uk) || unitWord('cubic ' + ut) === unitWord(uk);
    }
    if (/^[<>=]$/.test(k)) return t.replace(/\s/g, '') === k;
    return false;
  }
  function compound(t, k) {
    var re = /^([\d,]+)\s+([a-z ]+?)\s+([\d,]+)\s+([a-z ]+)$/i, a = re.exec(norm(t)), b = re.exec(norm(k));
    return !!(a && b && +a[1] === +b[1] && +a[3] === +b[3] && unitWord(a[2]) === unitWord(b[2]) && unitWord(a[4]) === unitWord(b[4]));
  }

  /* ---------- banks ---------- */
  var META = {};
  function load(unitId) {
    if (!G.MK_BANK_LOADER) return Promise.reject(new Error('Question bank loader missing'));
    return G.MK_BANK_LOADER.loadUnitFromSite(COURSE, unitId, null, '../').then(function (ids) {
      if (!ids.length) throw new Error('This unit’s questions are not published yet.');
      return G.fetch('../math5/meta/' + unitId + '.meta.json').then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; });
    }).then(function (meta) { META = meta || {}; return G.MK_QUESTION_BANKS.select({ courseId: COURSE, unitId: unitId }); });
  }
  function unitInfo(unitId) {
    var c = (G.LIBRARY && G.LIBRARY.courses || []).filter(function (x) { return x.id === COURSE; })[0];
    var u = c && c.units.filter(function (x) { return x.id === unitId; })[0];
    var idx = c ? c.units.indexOf(u) + 1 : 0;
    return { course: c, unit: u, number: idx, skills: G.MK_COURSE_CATALOG.getSkillRecords(COURSE, unitId) };
  }
  /* A question ready for play. mc: choices are verified; typed answers are checked with matches(). */
  function prepare(q) {
    var out = { id: q.id, skillId: q.skillId, level: q.level, prompt: q.prompt, steps: q.solutionSteps || [], answer: q.answer, img: null, meta: META[q.id] || {} };
    if (q.diagram && q.diagram.type === 'image') out.img = { src: '../' + q.diagram.spec.src, alt: q.diagram.spec.alt };
    if (q.format === 'multiple-choice') { out.kind = 'mc'; out.options = q.options.map(function (o) { return { text: o.text, correct: o.correct }; }); }
    else if (q.format === 'select-all') { out.kind = 'sel'; out.options = q.options.map(function (o) { return { text: o.text, correct: o.correct }; }); }
    else if (q.format === 'open-response') { out.kind = 'parts'; out.parts = q.parts; }
    else { out.kind = 'sa'; }
    return out;
  }
  /* Multiple-choice version of any single-answer item. Distractors come only from the verified distractor list
     (each one re-checked as wrong by tools/grade5-authoring/verify.py), never invented here. */
  function asChoice(p) {
    if (p.kind === 'mc') return p;
    if (p.kind !== 'sa') return null;
    var ds = Object.keys(p.meta.distractors || {}).filter(function (d) { return !matches(d, p.answer); });
    if (ds.length < 2) return null;
    var opts = shuffle(ds).slice(0, 3).map(function (t) { return { text: t, correct: false }; });
    opts.push({ text: p.answer, correct: true });
    var c = Object.assign({}, p);
    c.kind = 'mc'; c.options = shuffle(opts);
    return c;
  }

  /* ---------- the question card ---------- */
  function card(host, p, opts) {
    opts = opts || {};
    host.innerHTML = '';
    var box = el('div', host, 'g5-q');
    if (opts.label) el('div', box, 'g5-q-label', opts.label);
    math(el('div', box, 'g5-prompt'), p.prompt);
    if (p.img) { var im = el('img', box, 'g5-fig'); im.src = p.img.src; im.alt = p.img.alt; im.loading = 'lazy'; }
    var area = el('div', box, 'g5-answer');
    var fb = el('div', box, 'g5-feedback'); fb.setAttribute('role', 'status'); fb.setAttribute('aria-live', 'polite');
    var tools = el('div', box, 'g5-q-tools');
    var tries = 0, done = false;
    function finish(ok) {
      if (done) return; done = true;
      if (opts.onAnswer) opts.onAnswer(ok, tries);
    }
    function explain() {
      var s = el('details', box, 'g5-steps'); s.open = !!opts.openSteps;
      el('summary', s, null, 'See the worked solution');
      var ol = el('ol', s);
      p.steps.forEach(function (t) { math(el('li', ol), t); });
    }
    function feedback(ok, last) {
      fb.className = 'g5-feedback ' + (ok ? 'good' : 'try');
      fb.textContent = ok ? pick(PRAISE) : (last ? 'Good effort! Here is how to solve it.' : pick(NUDGE));
      if (ok || last) {
        if (!ok && opts.showAnswer !== false) { var a = el('div', fb, 'g5-key'); math(a, 'Answer: ' + (Array.isArray(p.answer) ? p.answer.join('; ') : p.answer)); }
        explain();
        if (opts.onNext) { var nb = el('button', tools, 'g5-btn primary', opts.nextLabel || 'Next →'); nb.onclick = opts.onNext; setTimeout(function () { nb.focus(); }, 30); }
      }
    }
    var maxTries = opts.tries || 2;
    if (p.kind === 'mc' || p.kind === 'sel') {
      var list = el('div', area, 'g5-choices' + (p.options.length > 3 && p.options.every(function (o) { return o.text.length < 28; }) ? ' grid' : ''));
      var picked = [];
      p.options.forEach(function (o, i) {
        var b = el('button', list, 'g5-choice');
        b.type = 'button'; b.dataset.i = i;
        el('span', b, 'g5-letter', 'ABCDEF'.charAt(i));
        math(el('span', b, 'g5-ct'), o.text);
        b.onclick = function () {
          if (done) return;
          if (p.kind === 'sel') { b.classList.toggle('on'); return; }
          tries++;
          var ok = o.correct;
          b.classList.add(ok ? 'right' : 'wrong'); b.disabled = !ok || true;
          var last = ok || tries >= maxTries;
          feedback(ok, last);
          if (last) { Array.prototype.forEach.call(list.children, function (c, j) { c.disabled = true; if (p.options[j].correct && opts.showAnswer !== false) c.classList.add('right'); }); finish(ok); }
        };
      });
      if (p.kind === 'sel') {
        el('p', area, 'g5-hint-text', 'Select all that apply, then press Check.');
        var cb = el('button', area, 'g5-btn primary', 'Check');
        cb.onclick = function () {
          if (done) return; tries++;
          var ok = p.options.every(function (o, j) { return o.correct === list.children[j].classList.contains('on'); });
          var last = ok || tries >= maxTries;
          feedback(ok, last);
          if (last) { cb.disabled = true; Array.prototype.forEach.call(list.children, function (c, j) { c.disabled = true; if (p.options[j].correct) c.classList.add('right'); else if (c.classList.contains('on')) c.classList.add('wrong'); }); finish(ok); }
        };
      }
    } else if (p.kind === 'parts') {
      var inputs = p.parts.map(function (pt, i) {
        var row = el('label', area, 'g5-part');
        el('span', row, 'g5-letter', 'abcd'.charAt(i));
        math(el('span', row, 'g5-pt'), pt.prompt);
        var inp = el('input', row, 'g5-input'); inp.autocomplete = 'off'; inp.setAttribute('aria-label', 'Answer for part ' + 'abcd'.charAt(i));
        return inp;
      });
      var pb = el('button', area, 'g5-btn primary', 'Check');
      pb.onclick = function () {
        if (done) return; tries++;
        var all = true;
        inputs.forEach(function (inp, i) { var ok = matches(inp.value, p.parts[i].answer); inp.classList.toggle('right', ok); inp.classList.toggle('wrong', !ok); all = all && ok; });
        var last = all || tries >= maxTries;
        feedback(all, last);
        if (last) { pb.disabled = true; finish(all); }
      };
    } else {
      var row2 = el('div', area, 'g5-typed');
      var input = el('input', row2, 'g5-input'); input.autocomplete = 'off'; input.setAttribute('aria-label', 'Your answer');
      input.placeholder = 'Type your answer';
      var go = el('button', row2, 'g5-btn primary', 'Check');
      el('p', area, 'g5-hint-text', 'Fractions: 3/4 · Mixed numbers: 2 1/2 · Remainders: 12 R 3 · Ordered pairs: (3, 5)');
      var submit = function () {
        if (done || !input.value.trim()) return;
        tries++;
        var ok = matches(input.value, p.answer);
        input.classList.toggle('right', ok); input.classList.toggle('wrong', !ok);
        var last = ok || tries >= maxTries;
        feedback(ok, last);
        if (last) { input.disabled = true; go.disabled = true; finish(ok); }
      };
      go.onclick = submit;
      input.onkeydown = function (e) { if (e.key === 'Enter') submit(); };
      setTimeout(function () { try { input.focus({ preventScroll: true }); } catch (e) {} }, 30);
    }
    if (opts.hints !== false && p.steps.length > 1) {
      var hb = el('button', tools, 'g5-btn ghost', '💡 Hint');
      hb.onclick = function () { hb.disabled = true; var h = el('div', box, 'g5-hint'); math(h, 'Hint: ' + p.steps[0]); };
    }
    if (opts.teacher) {
      var rb = el('button', tools, 'g5-btn ghost', 'Show answer');
      rb.onclick = function () { rb.disabled = true; var a = el('div', box, 'g5-key'); math(a, 'Answer: ' + (Array.isArray(p.answer) ? p.answer.join('; ') : p.answer)); };
    }
    return box;
  }

  /* ---------- page chrome: header, zoom, presentation ---------- */
  function chrome(title, sub) {
    var student = P.get('student') === '1';
    var head = el('header', D.body.firstChild ? null : D.body, 'g5-top');
    D.body.insertBefore(head, D.body.firstChild);
    if (!student) { var home = el('a', head, 'g5-home', '← Mr. K’s Classroom'); home.href = '../grade5.html#math5' + (P.get('unit') ? '.' + P.get('unit') : ''); }
    var t = el('div', head, 'g5-title'); el('strong', t, null, title); if (sub) el('span', t, null, sub);
    var z = el('div', head, 'g5-zoom'); z.setAttribute('role', 'group'); z.setAttribute('aria-label', 'Display size');
    var level = 1;
    try { level = +G.localStorage.getItem('g5-zoom') || 1; } catch (e) {}
    function apply() { D.documentElement.style.setProperty('--g5-zoom', level); try { G.localStorage.setItem('g5-zoom', level); } catch (e) {} }
    [['A−', -0.1, 'Smaller'], ['A+', 0.1, 'Larger'], ['Fit', 0, 'Reset size']].forEach(function (b) {
      var btn = el('button', z, 'g5-btn ghost sm', b[0]); btn.title = b[2]; btn.setAttribute('aria-label', b[2]);
      btn.onclick = function () { level = b[1] ? Math.max(0.7, Math.min(1.8, +(level + b[1]).toFixed(2))) : 1; apply(); };
    });
    var pres = el('button', z, 'g5-btn ghost sm', '⛶'); pres.title = 'Presentation mode (full screen)'; pres.setAttribute('aria-label', 'Presentation mode');
    pres.onclick = function () { D.body.classList.toggle('g5-present'); if (D.fullscreenElement) D.exitFullscreen(); else if (D.documentElement.requestFullscreen) D.documentElement.requestFullscreen().catch(function () {}); };
    apply();
    return head;
  }
  function levelName(l) { return (LEVELS.filter(function (x) { return x[0] === l; })[0] || [l, l])[1]; }
  function setupPanel(host, cfg) {
    /* level + mode chooser (skills are chosen by the site's shared teacher dialog first) */
    host.innerHTML = '';
    var p = el('section', host, 'g5-panel g5-setup');
    el('h2', p, null, cfg.heading || 'Get ready!');
    if (cfg.intro) el('p', p, 'g5-intro', cfg.intro);
    var fs1 = el('fieldset', p, 'g5-pills'); el('legend', fs1, null, 'Level');
    var lv = P.get('level') || 'cp1';
    LEVELS.forEach(function (l) {
      var lab = el('label', fs1, 'g5-pill'); var r = el('input', lab); r.type = 'radio'; r.name = 'g5level'; r.value = l[0]; r.checked = l[0] === lv; el('span', lab, null, l[1]);
    });
    var modeVal = cfg.modes ? cfg.modes[0][0] : null;
    if (cfg.modes && cfg.modes.length > 1) {
      var fs2 = el('fieldset', p, 'g5-pills'); el('legend', fs2, null, 'Play');
      cfg.modes.forEach(function (m, i) { var lab = el('label', fs2, 'g5-pill'); var r = el('input', lab); r.type = 'radio'; r.name = 'g5mode'; r.value = m[0]; r.checked = !i; el('span', lab, null, m[1]); });
    }
    var extra = cfg.extra ? cfg.extra(p) : null;
    var go = el('button', p, 'g5-btn primary big', cfg.startLabel || 'Start ▶');
    go.onclick = function () {
      var l = (p.querySelector('input[name=g5level]:checked') || {}).value || 'cp1';
      var m = (p.querySelector('input[name=g5mode]:checked') || {}).value || modeVal;
      cfg.start({ level: l, mode: m, extra: extra });
    };
    if (P.get('student') === '1' && P.get('level')) { setTimeout(function () { go.click(); }, 0); }
    return p;
  }
  function chooseSkills(info, start) {
    var skills = info.skills.map(function (s) { return { id: s.id, name: s.name }; });
    if (G.TeacherSkills && G.TeacherSkills.choose) G.TeacherSkills.choose(skills, start);
    else start(skills.map(function (s) { return s.id; }));
  }
  function errorBox(host, msg) { host.innerHTML = ''; var p = el('div', host, 'g5-panel'); el('h2', p, null, 'Oops!'); el('p', p, null, msg); }

  G.G5 = { P: P, COURSE: COURSE, LEVELS: LEVELS, PRAISE: PRAISE, NUDGE: NUDGE, el: el, math: math, esc: esc, pick: pick, shuffle: shuffle,
    parseNum: parseNum, matches: matches, load: load, unitInfo: unitInfo, prepare: prepare, asChoice: asChoice, card: card,
    chrome: chrome, setupPanel: setupPanel, chooseSkills: chooseSkills, levelName: levelName, errorBox: errorBox };
})(window);
