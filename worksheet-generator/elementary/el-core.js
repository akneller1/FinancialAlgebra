/* Elementary shared runtime (configured per course by window.MK_ELEMENTARY, see worksheet-generator/grade4/config.js):
   bank loading, question normalization, answer checking, the question card, friendly feedback, zoom and presentation
   controls. Used by the elementary games, Understanding Checks and flashcards. Course-neutral: nothing here names a grade.
   No network calls except the site's own question-bank files; no accounts; nothing is stored about students. */
(function (G) {
  'use strict';
  var D = G.document;
  var P = new URLSearchParams(G.location.search);
  var CFG = G.MK_ELEMENTARY || {};
  if (!CFG.course) throw new Error('MK_ELEMENTARY.course is not set (load the course config before el-core.js)');
  CFG.zoomKey = CFG.zoomKey || 'el-zoom-' + CFG.course;
  CFG.label = CFG.label || 'Grade ' + CFG.course.replace(/\D/g, '');
  var COURSE = CFG.course;
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
    if (/°$/.test(k)) { var dk = parseNum(k), dt = parseNum(t.replace(/\s*(°|degrees?)\s*$/i, '')); return !!(dk && dt && dk[0] === dt[0] && dk[1] === dt[1] && /^\s*\$?-?[\d,.]+\s*(°|degrees?)?\s*$/i.test(t)); }
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
    // An elementary course may supply a separate, verified Understanding Check bank.
    // Ordinary games, flashcards and generators continue using the practice bank.
    if (CFG.checkBankPath && /understanding-check\.html$/.test(G.location.pathname)) {
      if (!/^[a-z0-9-]+$/.test(unitId)) return Promise.reject(new Error('Invalid unit'));
      var base = CFG.checkBankPath.replace(/\/$/, '');
      var source = '../' + base + '/' + unitId;
      return Promise.all([
        G.fetch(source + '.json').then(function(r) { if (!r.ok) throw new Error('Understanding Check questions unavailable for this unit.'); return r.json(); }),
        G.fetch(base.replace(/^/, '../') + '/meta/' + unitId + '.meta.json').then(function(r) { return r.ok ? r.json() : {}; }).catch(function(){ return {}; })
      ]).then(function(parts) {
        var bank = parts[0];
        if (!bank || bank.unitId !== unitId || bank.courseId !== COURSE || !Array.isArray(bank.questions) || !bank.questions.length)
          throw new Error('Understanding Check bank is incomplete or mismatched.');
        META = parts[1] && parts[1].questions || {};
        return bank.questions;
      });
    }
    if (!G.MK_BANK_LOADER) return Promise.reject(new Error('Question bank loader missing'));
    return G.MK_BANK_LOADER.loadUnitFromSite(COURSE, unitId, null, '../').then(function (ids) {
      if (!ids.length) throw new Error('This unit’s questions are not published yet.');
      return G.fetch((CFG.metaPath || '../question-banks/' + COURSE + '/meta/') + unitId + '.meta.json').then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; });
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
     (each one re-checked as wrong by the course authoring verifier), never invented here. */
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
    var box = el('div', host, 'el-q');
    if (opts.label) el('div', box, 'el-q-label', opts.label);
    math(el('div', box, 'el-prompt'), p.prompt);
    if (p.img) { var im = el('img', box, 'el-fig'); im.src = p.img.src; im.alt = p.img.alt; im.loading = 'lazy'; }
    var area = el('div', box, 'el-answer');
    var fb = el('div', box, 'el-feedback'); fb.setAttribute('role', 'status'); fb.setAttribute('aria-live', 'polite');
    var tools = el('div', box, 'el-q-tools');
    var tries = 0, done = false;
    var response = '';
    function finish(ok) {
      if (done) return; done = true;
      if (opts.onAnswer) opts.onAnswer(ok, tries, response);
    }
    function explain() {
      var s = el('details', box, 'el-steps'); s.open = !!opts.openSteps;
      el('summary', s, null, 'See the worked solution');
      var ol = el('ol', s);
      p.steps.forEach(function (t) { math(el('li', ol), t); });
    }
    function feedback(ok, last) {
      fb.className = 'el-feedback ' + (ok ? 'good' : 'try');
      fb.textContent = ok ? pick(PRAISE) : (last ? 'Good effort! Here is how to solve it.' : pick(NUDGE));
      if (ok || last) {
        if (!ok && opts.showAnswer !== false) { var a = el('div', fb, 'el-key'); math(a, 'Answer: ' + (Array.isArray(p.answer) ? p.answer.join('; ') : p.answer)); }
        explain();
        if (opts.onNext) { var nb = el('button', tools, 'el-btn primary', opts.nextLabel || 'Next →'); nb.onclick = opts.onNext; setTimeout(function () { nb.focus(); }, 30); }
      }
    }
    var maxTries = opts.tries || 2;
    if (p.kind === 'mc' || p.kind === 'sel') {
      var list = el('div', area, 'el-choices' + (p.options.length > 3 && p.options.every(function (o) { return o.text.length < 28; }) ? ' grid' : ''));
      var picked = [];
      p.options.forEach(function (o, i) {
        var b = el('button', list, 'el-choice');
        b.type = 'button'; b.dataset.i = i;
        el('span', b, 'el-letter', 'ABCDEF'.charAt(i));
        math(el('span', b, 'el-ct'), o.text);
        b.onclick = function () {
          if (done) return;
          if (p.kind === 'sel') { b.classList.toggle('on'); return; }
          tries++; response = o.text;
          var ok = o.correct;
          b.classList.add(ok ? 'right' : 'wrong'); b.disabled = !ok || true;
          var last = ok || tries >= maxTries;
          feedback(ok, last);
          if (last) { Array.prototype.forEach.call(list.children, function (c, j) { c.disabled = true; if (p.options[j].correct && opts.showAnswer !== false) c.classList.add('right'); }); finish(ok); }
        };
      });
      if (p.kind === 'sel') {
        el('p', area, 'el-hint-text', 'Select all that apply, then press Check.');
        var cb = el('button', area, 'el-btn primary', 'Check');
        cb.onclick = function () {
          if (done) return; tries++;
          response = p.options.filter(function (o, j) { return list.children[j].classList.contains('on'); }).map(function (o) { return o.text; }).join('; ');
          var ok = p.options.every(function (o, j) { return o.correct === list.children[j].classList.contains('on'); });
          var last = ok || tries >= maxTries;
          feedback(ok, last);
          if (last) { cb.disabled = true; Array.prototype.forEach.call(list.children, function (c, j) { c.disabled = true; if (p.options[j].correct) c.classList.add('right'); else if (c.classList.contains('on')) c.classList.add('wrong'); }); finish(ok); }
        };
      }
    } else if (p.kind === 'parts') {
      var inputs = p.parts.map(function (pt, i) {
        var row = el('label', area, 'el-part');
        el('span', row, 'el-letter', 'abcd'.charAt(i));
        math(el('span', row, 'el-pt'), pt.prompt);
        var inp = el('input', row, 'el-input'); inp.autocomplete = 'off'; inp.setAttribute('aria-label', 'Answer for part ' + 'abcd'.charAt(i));
        return inp;
      });
      var pb = el('button', area, 'el-btn primary', 'Check');
      pb.onclick = function () {
        if (done) return; tries++;
        var all = true;
        response = inputs.map(function (inp, i) { return '(' + 'abcd'.charAt(i) + ') ' + inp.value.trim(); }).join('; ');
        inputs.forEach(function (inp, i) { var ok = matches(inp.value, p.parts[i].answer); inp.classList.toggle('right', ok); inp.classList.toggle('wrong', !ok); all = all && ok; });
        var last = all || tries >= maxTries;
        feedback(all, last);
        if (last) { pb.disabled = true; finish(all); }
      };
    } else {
      var row2 = el('div', area, 'el-typed');
      var input = el('input', row2, 'el-input'); input.autocomplete = 'off'; input.setAttribute('aria-label', 'Your answer');
      input.placeholder = 'Type your answer';
      var go = el('button', row2, 'el-btn primary', 'Check');
      el('p', area, 'el-hint-text', CFG.answerHint || 'Fractions: 3/4 · Mixed numbers: 2 1/2 · Remainders: 12 R 3 · Ordered pairs: (3, 5)');
      var submit = function () {
        if (done || !input.value.trim()) return;
        tries++; response = input.value.trim();
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
      var hb = el('button', tools, 'el-btn ghost', '💡 Hint');
      hb.onclick = function () { hb.disabled = true; var h = el('div', box, 'el-hint'); math(h, 'Hint: ' + p.steps[0]); };
    }
    if (opts.teacher) {
      var rb = el('button', tools, 'el-btn ghost', 'Show answer');
      rb.onclick = function () { rb.disabled = true; var a = el('div', box, 'el-key'); math(a, 'Answer: ' + (Array.isArray(p.answer) ? p.answer.join('; ') : p.answer)); };
    }
    return box;
  }

  /* The course page that opened this activity (the production home page or a staging course page); the default is the site home. */
  function homeUrl() {
    if (CFG.home) return CFG.home;
    try {
      var r = D.referrer ? new URL(D.referrer) : null;
      if (r && r.origin === G.location.origin && /\/(?:[\w-]+\.html)?$/.test(r.pathname) && r.pathname.indexOf('/worksheet-generator/') < 0 && r.pathname.indexOf('/artifacts/') < 0) {
        try { G.sessionStorage.setItem('el-home-' + COURSE, r.origin + r.pathname); } catch (e) {}
        return r.origin + r.pathname;
      }
      var saved = G.sessionStorage.getItem('el-home-' + COURSE);
      if (saved) return saved;
    } catch (e) {}
    // On the assembled site elementary players live one level deeper:
    // /grade2/worksheet-generator/grade2-games.html -> /index.html.
    // Preserve a project subpath (for example /FinancialAlgebra/) in staging.
    var m = G.location.pathname.match(/^(.*)\/grade[1-5]\/worksheet-generator\//);
    if (m) return m[1] + '/index.html';
    return '../index.html';
  }

  /* ---------- page chrome: header, zoom, presentation ---------- */
  function chrome(title, sub) {
    var student = P.get('student') === '1';
    var head = el('header', D.body.firstChild ? null : D.body, 'el-top');
    D.body.insertBefore(head, D.body.firstChild);
    if (!student) { var home = el('a', head, 'el-home', '← Mr. K’s Classroom'); home.href = homeUrl() + '#' + (/^math[1-5]$/.test(COURSE) ? 'grade' + COURSE.slice(4) : COURSE) + (P.get('unit') ? '.' + P.get('unit') : ''); }
    var t = el('div', head, 'el-title'); el('strong', t, null, title); if (sub) el('span', t, null, sub);
    var z = el('div', head, CFG.zoomKey); z.setAttribute('role', 'group'); z.setAttribute('aria-label', 'Display size');
    var level = 1;
    try { level = +G.localStorage.getItem(CFG.zoomKey) || 1; } catch (e) {}
    function apply() { D.documentElement.style.setProperty('--el-zoom', +(level * (D.body.classList.contains('el-present') ? 1.35 : 1)).toFixed(2)); try { G.localStorage.setItem(CFG.zoomKey, level); } catch (e) {} }
    [['A−', -0.1, 'Smaller'], ['A+', 0.1, 'Larger'], ['Fit', 0, 'Reset size']].forEach(function (b) {
      var btn = el('button', z, 'el-btn ghost sm', b[0]); btn.title = b[2]; btn.setAttribute('aria-label', b[2]);
      btn.onclick = function () { level = b[1] ? Math.max(0.7, Math.min(1.8, +(level + b[1]).toFixed(2))) : 1; apply(); };
    });
    var pres = el('button', z, 'el-btn ghost sm', '⛶'); pres.title = 'Presentation mode (full screen)'; pres.setAttribute('aria-label', 'Presentation mode');
    pres.onclick = function () { D.body.classList.toggle('el-present'); apply(); if (D.fullscreenElement) D.exitFullscreen(); else if (D.documentElement.requestFullscreen) D.documentElement.requestFullscreen().catch(function () {}); };
    apply();
    return head;
  }
  function levelName(l) { return (LEVELS.filter(function (x) { return x[0] === l; })[0] || [l, l])[1]; }
  function setupPanel(host, cfg) {
    /* level + mode chooser (skills are chosen by the site's shared teacher dialog first) */
    host.innerHTML = '';
    var p = el('section', host, 'el-panel el-setup');
    el('h2', p, null, cfg.heading || 'Get ready!');
    if (cfg.intro) el('p', p, 'el-intro', cfg.intro);
    var fs1 = el('fieldset', p, 'el-pills'); el('legend', fs1, null, 'Level');
    var lv = P.get('level') || 'cp1';
    LEVELS.forEach(function (l) {
      var lab = el('label', fs1, 'el-pill'); var r = el('input', lab); r.type = 'radio'; r.name = 'ellevel'; r.value = l[0]; r.checked = l[0] === lv; el('span', lab, null, l[1]);
    });
    var modeVal = cfg.modes ? cfg.modes[0][0] : null;
    if (cfg.modes && cfg.modes.length > 1) {
      var fs2 = el('fieldset', p, 'el-pills'); el('legend', fs2, null, 'Play');
      var want = P.get('mode'), hasWant = cfg.modes.some(function (m) { return m[0] === want; });
      cfg.modes.forEach(function (m, i) { var lab = el('label', fs2, 'el-pill'); var r = el('input', lab); r.type = 'radio'; r.name = 'elmode'; r.value = m[0]; r.checked = hasWant ? m[0] === want : !i; el('span', lab, null, m[1]); });
    }
    var extra = cfg.extra ? cfg.extra(p) : null;
    var go = el('button', p, 'el-btn primary big', cfg.startLabel || 'Start ▶');
    go.onclick = function () {
      var l = (p.querySelector('input[name=ellevel]:checked') || {}).value || 'cp1';
      var m = (p.querySelector('input[name=elmode]:checked') || {}).value || modeVal;
      cfg.start({ level: l, mode: m, extra: extra });
    };
    if (P.get('student') !== '1') studentLink(p, cfg);
    if (P.get('student') === '1' && P.get('level')) { setTimeout(function () { go.click(); }, 0); }
    return p;
  }
  /* Teacher: "Student link" builds a link that opens this activity already set up (unit, skills, level, mode and the
     activity's own settings). The link carries only these settings: no names, no accounts, nothing is stored. */
  function studentLink(p, cfg) {
    var row = el('div', p, 'el-share');
    var b = el('button', row, 'el-btn ghost', '🔗 Student link'); b.type = 'button';
    b.title = 'Make a link that opens this activity with these settings';
    var out = el('div', row, 'el-share-out'); out.hidden = true;
    b.onclick = function () {
      var q = new URLSearchParams(G.location.search);
      ['teacherShare', 'student', 'level', 'mode', 'skills'].forEach(function (k) { q.delete(k); });
      q.set('student', '1');
      q.set('level', (p.querySelector('input[name=ellevel]:checked') || {}).value || 'cp1');
      var m = p.querySelector('input[name=elmode]:checked'); if (m) q.set('mode', m.value);
      if (cfg.skills && cfg.skills.length) q.set('skills', JSON.stringify(cfg.skills));
      var extra = cfg.linkParams ? cfg.linkParams() : {};
      Object.keys(extra).forEach(function (k) { q.set(k, extra[k]); });
      var url = G.location.origin + G.location.pathname + '?' + q.toString();
      out.hidden = false; out.innerHTML = '';
      var inp = el('input', out, 'el-input el-share-url'); inp.readOnly = true; inp.value = url; inp.setAttribute('aria-label', 'Student link');
      var cp = el('button', out, 'el-btn sm', 'Copy'); cp.type = 'button';
      cp.onclick = function () { inp.select(); var done = function () { cp.textContent = 'Copied ✓'; }; if (G.navigator.clipboard && G.navigator.clipboard.writeText) G.navigator.clipboard.writeText(url).then(done, function () { try { D.execCommand('copy'); done(); } catch (e) {} }); else { try { D.execCommand('copy'); done(); } catch (e) {} } };
      el('p', out, 'el-hint-text', 'Students open the link and start right away with these skills and settings. No account or name is needed.');
      inp.focus(); inp.select();
    };
  }
  function chooseSkills(info, start) {
    var skills = info.skills.map(function (s) { return { id: s.id, name: s.name }; });
    if (G.TeacherSkills && G.TeacherSkills.choose) G.TeacherSkills.choose(skills, start);
    else start(skills.map(function (s) { return s.id; }));
  }
  function errorBox(host, msg) { host.innerHTML = ''; var p = el('div', host, 'el-panel'); el('h2', p, null, 'Oops!'); el('p', p, null, msg); }

  G.MKEL = { P: P, CFG: CFG, COURSE: COURSE, homeUrl: homeUrl, LEVELS: LEVELS, PRAISE: PRAISE, NUDGE: NUDGE, el: el, math: math, esc: esc, pick: pick, shuffle: shuffle,
    parseNum: parseNum, matches: matches, load: load, unitInfo: unitInfo, prepare: prepare, asChoice: asChoice, card: card,
    chrome: chrome, setupPanel: setupPanel, chooseSkills: chooseSkills, studentLink: studentLink, levelName: levelName, errorBox: errorBox };
})(window);
