/* Financial Decision Lab engine — a reusable 7-step guided decision activity.
 * Scenario configs live in scenarios.js (window.FA_LABS). Math comes from FA_MATH. No network, no AI.
 * Student responses are kept only in this browser (localStorage, best-effort) and in the printable summary. */
(function (G) {
  'use strict';
  var R = G.FA_RENDER, M = G.FA_MATH, LABS = G.FA_LABS || {};
  var STEPS = ['Situation', 'Options', 'Initial decision', 'Investigation', 'Change the variables', 'Final recommendation', 'Reflection'];
  var COLORS = ['#7448ff', '#0c7a55', '#d9480f', '#1c7ed6'];
  var p = new URLSearchParams(location.search), labId = p.get('lab'), lab = LABS[labId];
  var teacher = p.get('teacher') === '1';
  var app = document.getElementById('app');
  var store = { get: function (k) { try { return JSON.parse(localStorage.getItem('fa-lab:' + labId + ':' + k)); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem('fa-lab:' + labId + ':' + k, JSON.stringify(v)); } catch (e) { } } };
  function fmt(v, f) {
    if (v == null || isNaN(v)) return '—';
    if (v === Infinity) return 'Never';
    switch (f) {
      case 'money': return (v < 0 ? '−$' : '$') + Math.abs(Math.round(v)).toLocaleString('en-US');
      case 'cents': return (v < 0 ? '−$' : '$') + Math.abs(v).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      case 'pct': return (Math.round(v * 1000) / 10) + '%';
      case 'pct2': return (Math.round(v * 10000) / 100) + '%';
      case 'months': return Math.round(v) + ' mo';
      case 'years': return (Math.round(v * 10) / 10) + ' yr';
      default: return (Math.round(v * 100) / 100).toLocaleString('en-US');
    }
  }
  if (!lab) {
    app.innerHTML = '<h1>Financial Decision Labs</h1><p>Choose a lab. Add <code>&amp;teacher=1</code> to the address for teacher view.</p><div class="fa-grid">' +
      Object.keys(LABS).map(function (k) { var L = LABS[k]; return '<a class="fa-panel" style="text-decoration:none;color:inherit" href="?lab=' + k + '"><span class="fa-pill">Unit ' + L.unitNum + '</span><h2>' + R.esc(L.title) + '</h2><p>' + R.esc(L.subtitle) + '</p></a>'; }).join('') + '</div>';
    return;
  }
  var vars = {}; lab.vars.forEach(function (v) { vars[v.id] = v.value; });
  var defaults = Object.assign({}, vars);
  var locked = store.get('locked') || false;
  var step = Math.min(store.get('step') || 0, STEPS.length - 1);
  var resp = store.get('resp') || {};
  function save() { store.set('resp', resp); store.set('step', step); }

  /* ---------- pieces ---------- */
  function optionName(id) { return (lab.options.find(function (o) { return o.id === id; }) || {}).name || id; }
  function resultsTable(v) {
    var out = lab.compute(v);
    return '<div class="fa-table-wrap"><table class="fa-table"><caption>' + R.esc(out.caption || 'Comparison under current assumptions') + '</caption><thead><tr><th>Measure</th>' + lab.options.map(function (o) { return '<th>' + R.esc(o.name) + '</th>'; }).join('') + '</tr></thead><tbody>' +
      out.rows.map(function (row) {
        var vals = lab.options.map(function (o) { return row.values[o.id]; }), finite = vals.filter(function (x) { return typeof x === 'number' && isFinite(x); });
        var best = row.better ? (row.better === 'low' ? Math.min.apply(null, finite) : Math.max.apply(null, finite)) : null;
        return '<tr><th scope="row">' + R.esc(row.label) + '</th>' + vals.map(function (x) { return '<td' + (best != null && x === best ? ' style="font-weight:700;color:var(--fa-good)"' : '') + '>' + (typeof x === 'string' ? R.esc(x) : fmt(x, row.fmt)) + (best != null && x === best ? ' ★' : '') + '</td>'; }).join('') + '</tr>';
      }).join('') + '</tbody></table></div>' + (out.note ? '<p class="fa-doc-kind">' + R.esc(out.note) + '</p>' : '') + (out.series ? chart(out.series) : '');
  }
  function chart(s) {
    var W = 640, H = 260, L = 64, B = 34, T = 14, Rr = 12, keys = Object.keys(s.lines), all = [];
    keys.forEach(function (k) { s.lines[k].forEach(function (y) { if (isFinite(y)) all.push(y); }); });
    var ymin = Math.min(0, Math.min.apply(null, all)), ymax = Math.max.apply(null, all) || 1, n = s.x.length;
    var X = function (i) { return L + (W - L - Rr) * (n === 1 ? 0 : i / (n - 1)); }, Y = function (y) { return T + (H - T - B) * (1 - (y - ymin) / (ymax - ymin || 1)); };
    var g = '';
    for (var t = 0; t <= 4; t++) { var yv = ymin + (ymax - ymin) * t / 4; g += '<line x1="' + L + '" x2="' + (W - Rr) + '" y1="' + Y(yv) + '" y2="' + Y(yv) + '" stroke="#cfd3ea"/><text x="' + (L - 6) + '" y="' + (Y(yv) + 4) + '" text-anchor="end" font-size="11">' + fmt(yv, s.fmt || 'money') + '</text>'; }
    var stepX = Math.max(1, Math.ceil(n / 8));
    s.x.forEach(function (x, i) { if (i % stepX === 0 || i === n - 1) g += '<text x="' + X(i) + '" y="' + (H - B + 16) + '" text-anchor="middle" font-size="11">' + R.esc(x) + '</text>'; });
    keys.forEach(function (k, j) { var pts = s.lines[k].map(function (y, i) { return isFinite(y) ? X(i) + ',' + Y(y) : null; }).filter(Boolean).join(' '); g += '<polyline fill="none" stroke="' + COLORS[j % 4] + '" stroke-width="3" ' + (j % 2 ? 'stroke-dasharray="7 4"' : '') + ' points="' + pts + '"/>'; });
    var legend = keys.map(function (k, j) { return '<span style="display:inline-flex;align-items:center;gap:6px;margin-right:14px"><svg width="26" height="8" aria-hidden="true"><line x1="0" x2="26" y1="4" y2="4" stroke="' + COLORS[j % 4] + '" stroke-width="3" ' + (j % 2 ? 'stroke-dasharray="7 4"' : '') + '/></svg>' + R.esc(optionName(k)) + '</span>'; }).join('');
    var desc = keys.map(function (k) { var a = s.lines[k]; return optionName(k) + ' ends at ' + fmt(a[a.length - 1], s.fmt || 'money'); }).join('; ');
    return '<figure class="fa-chart"><figcaption><strong>' + R.esc(s.title) + '</strong> <span class="fa-doc-kind">(' + R.esc(s.xLabel || '') + ')</span></figcaption><svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + R.esc(s.title + '. ' + desc) + '" style="width:100%;max-width:680px;height:auto;background:#fff;border-radius:8px">' + g + '</svg><div style="font-size:.9rem">' + legend + '</div></figure>';
  }
  function varControls() {
    return '<div class="fa-grid">' + lab.vars.map(function (v) {
      if (v.type === 'toggle') return '<label class="fa-field" style="flex-direction:row;align-items:center;gap:8px"><input type="checkbox" data-var="' + v.id + '"' + (vars[v.id] ? ' checked' : '') + (locked && !teacher ? ' disabled' : '') + '> ' + R.esc(v.label) + '</label>';
      return '<label class="fa-field">' + R.esc(v.label) + ' <output id="o-' + v.id + '">' + fmt(vars[v.id], v.fmt) + '</output><input type="range" data-var="' + v.id + '" min="' + v.min + '" max="' + v.max + '" step="' + v.step + '" value="' + vars[v.id] + '"' + (locked && !teacher ? ' disabled' : '') + '></label>';
    }).join('') + '</div>';
  }
  function choice(name) {
    return '<fieldset class="fa-field"><legend>Choose an option</legend>' + lab.options.map(function (o) { return '<label style="font-weight:400"><input type="radio" name="' + name + '" value="' + o.id + '"' + (resp[name] === o.id ? ' checked' : '') + '> ' + R.esc(o.name) + '</label>'; }).join('') + '</fieldset>';
  }
  function area(key, label) { return '<label class="fa-field">' + R.esc(label) + '<textarea data-resp="' + key + '">' + R.esc(resp[key] || '') + '</textarea></label>'; }
  function qBlock(list, prefix, useVars) {
    return list.map(function (q, i) {
      var key = prefix + i, v = useVars ? vars : defaults, ans = q.answer(v);
      return '<div class="fa-panel flat"><p><strong>' + (i + 1) + '.</strong> ' + R.rich(typeof q.prompt === 'function' ? q.prompt(v) : q.prompt) + '</p>' +
        (q.answer ? '<label class="fa-field">Your answer' + (q.fmt === 'pct' ? ' (%)' : '') + '<input data-resp="' + key + '" inputmode="decimal" value="' + R.esc(resp[key] || '') + '"></label><p><button class="fa-btn" data-check="' + key + '" data-list="' + prefix + '" data-i="' + i + '">Check</button> <span class="fa-fb" id="fb-' + key + '" aria-live="polite"></span></p>' : '') +
        (teacher ? '<div class="fa-key"><strong>Answer:</strong> ' + fmt(ans, q.fmt) + (q.solution ? '<br>' + R.rich(q.solution(v)) : '') + '</div>' : '') + '</div>';
    }).join('');
  }
  function stepBody() {
    switch (step) {
      case 0: return '<div class="fa-panel"><p class="fa-pill">' + R.esc(lab.person.name) + '</p><p>' + R.rich(lab.situation) + '</p>' + R.table({ headers: ['Fact', 'Detail'], rows: lab.person.facts }) + '<p><strong>Goal:</strong> ' + R.rich(lab.goal) + '</p></div>' + '<details class="fa-panel flat"><summary><strong>Learning objectives</strong></summary><ul>' + lab.objectives.map(function (o) { return '<li>' + R.rich(o) + '</li>'; }).join('') + '</ul></details>';
      case 1: return '<div class="fa-grid">' + lab.options.map(function (o, j) { return '<div class="fa-panel" style="border-top:8px solid ' + COLORS[j] + '"><h3>' + R.esc(o.name) + '</h3><p>' + R.rich(o.tagline) + '</p>' + R.table({ headers: ['Detail', ''], rows: o.details }) + '</div>'; }).join('') + '</div>' + (lab.assumptions ? '<p class="fa-note"><strong>Assumptions:</strong> ' + R.rich(lab.assumptions) + '</p>' : '');
      case 2: return '<div class="fa-panel"><p>Before doing any math, which option would you choose? This is a prediction — you can change your mind later.</p>' + choice('initial') + area('initialWhy', 'Why? What feels most important right now?') + '</div>';
      case 3: return '<div class="fa-panel"><p>Use the details from Step 2 (default assumptions). Calculate, then check.</p>' + qBlock(lab.questions, 'q', false) + '</div><div class="fa-panel"><h3>Comparison at default assumptions</h3>' + resultsTable(defaults) + '</div>';
      case 4: return '<div class="fa-panel"><p>Move the sliders to test different assumptions. The table and chart update immediately.</p>' + varControls() + '<p><button class="fa-btn" id="resetVars">Reset to defaults</button></p><div id="live">' + resultsTable(vars) + '</div></div><div class="fa-panel"><h3>Challenges</h3>' + qBlock(lab.challenges, 'c', false) + area('sensitivity', 'Which assumption changed the result the most? Describe what happened.') + '</div>';
      case 5: return '<div class="fa-panel">' + choice('final') + area('finalWhy', 'Justify your recommendation using at least two numbers from your investigation and one non-financial factor.') +
        '<p><strong>A strong recommendation…</strong></p><ul>' + ['states the choice clearly', 'cites specific calculated costs or values', 'names the key assumption it depends on', 'weighs a tradeoff that is not just about money', 'explains what would change the decision'].map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul>' + (teacher ? R.rubric(lab.rubric || defaultRubric()) : '') + '</div>';
      case 6: return '<div class="fa-panel">' + lab.reflection.map(function (q, i) { return area('ref' + i, q); }).join('') + '<p><button class="fa-btn primary" id="summary">Create printable summary</button></p></div>';
    }
  }
  function defaultRubric() {
    return [{ criterion: 'Financial accuracy', points: 4, full: 'Investigation answers correct; values labeled.', partial: 'Minor errors.', none: 'Major errors.' }, { criterion: 'Evidence', points: 4, full: 'Cites at least two calculated values.', partial: 'One value.', none: 'None.' }, { criterion: 'Tradeoffs & assumptions', points: 4, full: 'Weighs money and non-money factors; names the key assumption.', partial: 'Lists factors without weighing.', none: 'Opinion only.' }, { criterion: 'Reflection', points: 4, full: 'Explains whether thinking changed and what information is still needed.', partial: 'Brief.', none: 'Missing.' }];
  }
  function teacherPanel() {
    if (!teacher) return '';
    var T = lab.teacher;
    return '<aside class="fa-panel" style="border-color:var(--fa-accent)"><h2>Teacher view</h2><p><strong>Skills:</strong> ' + lab.skills.join(', ') + ' · <strong>Time:</strong> ' + R.esc(T.time) + '</p><ul>' + T.notes.map(function (n) { return '<li>' + R.rich(n) + '</li>'; }).join('') + '</ul><p><strong>Common misconceptions:</strong></p><ul>' + T.misconceptions.map(function (n) { return '<li>' + R.rich(n) + '</li>'; }).join('') + '</ul><div class="fa-model"><strong>Model recommendation:</strong> ' + R.rich(T.model) + '</div>' +
      '<p class="fa-noprint"><label><input type="checkbox" id="lockVars"' + (locked ? ' checked' : '') + '> Lock sliders for students on this device</label> · <a href="?lab=' + labId + '">Open student view</a></p></aside>';
  }
  function render() {
    document.title = lab.title + ' | Financial Decision Lab';
    app.innerHTML = '<p class="fa-noprint"><a href="?">All labs</a> · <a href="../../index.html#financial-algebra.' + lab.unit + '">Unit page</a>' + (teacher ? '' : ' · <a href="?lab=' + labId + '&teacher=1">Teacher view</a>') + '</p>' +
      '<header><span class="fa-pill">Unit ' + lab.unitNum + ' · Financial Decision Lab</span><h1>' + R.esc(lab.title) + '</h1><p>' + R.esc(lab.subtitle) + '</p></header>' + teacherPanel() +
      '<nav aria-label="Lab steps" class="fa-tabs fa-noprint">' + STEPS.map(function (s, i) { return '<button class="fa-btn" data-step="' + i + '" aria-current="' + (i === step ? 'step' : 'false') + '" aria-selected="' + (i === step) + '">' + (i + 1) + '. ' + s + '</button>'; }).join('') + '</nav>' +
      '<h2>Step ' + (step + 1) + ': ' + STEPS[step] + '</h2>' + stepBody() +
      '<p class="fa-noprint" style="display:flex;gap:8px;justify-content:space-between"><button class="fa-btn" data-step="' + (step - 1) + '"' + (step ? '' : ' disabled') + '>← Back</button><button class="fa-btn primary" data-step="' + (step + 1) + '"' + (step < STEPS.length - 1 ? '' : ' disabled') + '>Next →</button></p><div id="printSummary"></div>';
  }
  function summary() {
    var rows = [['Initial choice', optionName(resp.initial || '—')], ['Initial reasoning', resp.initialWhy || ''], ['Final choice', optionName(resp.final || '—')], ['Justification', resp.finalWhy || ''], ['Sensitivity', resp.sensitivity || '']].concat(lab.reflection.map(function (q, i) { return [q, resp['ref' + i] || '']; }));
    document.getElementById('printSummary').innerHTML = '<section class="fa-sheet"><header class="fa-sheet-head"><div><div class="fa-pill">Decision Lab summary</div><h2>' + R.esc(lab.title) + '</h2></div><div class="fa-name">Name ____________________</div></header>' + R.table({ headers: ['Prompt', 'Response'], rows: rows }) + '<h3 class="fa-section-h">Comparison at default assumptions</h3>' + resultsTable(defaults) + '</section>';
    window.print();
  }
  app.addEventListener('click', function (e) {
    var t = e.target, s = t.getAttribute('data-step');
    if (s != null && !t.disabled) { step = +s; save(); render(); window.scrollTo(0, 0); return; }
    if (t.id === 'resetVars') { vars = Object.assign({}, defaults); render(); return; }
    if (t.id === 'summary') { summary(); return; }
    var key = t.getAttribute('data-check');
    if (key) {
      var list = t.getAttribute('data-list') === 'q' ? lab.questions : lab.challenges, q = list[+t.getAttribute('data-i')], target = q.answer(defaults);
      var raw = parseFloat(String(resp[key] || '').replace(/[−–]/g, '-').replace(/[$,%\s]/g, '')), val = q.fmt === 'pct' ? raw / 100 : raw;
      var tol = q.tol != null ? q.tol : (q.fmt === 'pct' ? 0.0005 : 0.5), ok = Math.abs(val - target) <= tol;
      document.getElementById('fb-' + key).innerHTML = isNaN(raw) ? 'Enter a number.' : ok ? '<span style="color:var(--fa-good);font-weight:700">✓ Correct</span>' : '<span style="color:var(--fa-bad);font-weight:700">Not yet.</span> ' + (q.hint ? R.rich(q.hint) : 'Recheck your setup.');
    }
  });
  app.addEventListener('input', function (e) {
    var t = e.target, k = t.getAttribute('data-resp');
    if (k) { resp[k] = t.value; save(); return; }
    var v = t.getAttribute('data-var');
    if (v) { var def = lab.vars.find(function (x) { return x.id === v; }); vars[v] = def.type === 'toggle' ? t.checked : +t.value; var o = document.getElementById('o-' + v); if (o) o.textContent = fmt(vars[v], def.fmt); document.getElementById('live').innerHTML = resultsTable(vars); }
  });
  app.addEventListener('change', function (e) {
    var t = e.target;
    if (t.type === 'radio') { resp[t.name] = t.value; save(); }
    if (t.id === 'lockVars') { locked = t.checked; store.set('locked', locked); }
    if (t.getAttribute('data-var') && t.type === 'checkbox') { vars[t.getAttribute('data-var')] = t.checked; document.getElementById('live').innerHTML = resultsTable(vars); }
  });
  G.FA_LAB_ENGINE = { fmt: fmt };
  render();
})(window);
