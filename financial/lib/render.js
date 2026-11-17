/* Financial Algebra shared HTML renderers (browser + Node). Attaches globalThis.FA_RENDER.
 * Division is displayed as a stacked fraction (numerator over denominator) — never with "/". */
(function (G) {
  'use strict';
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  var TOK = '(\\([^()]{1,40}\\)|[−-]?\\$?[\\d,]*\\.?\\d+%?)';   // a whole (group) first, so "÷ (1 + i)" is not cut at "(1"
  var DIV = new RegExp(TOK + ' ÷ ' + TOK, 'g');
  function frac(a, b) { return '<span class="fa-frac" role="math" aria-label="' + a + ' divided by ' + b + '"><span class="fa-num">' + a + '</span><span class="fa-den">' + b + '</span></span>'; }
  function rich(s) {
    var h = esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\[\[(.+?)\|\|(.+?)\]\]/g, function (_, a, b) { return frac(a.trim(), b.trim()); });
    for (var k = 0; k < 3; k++) h = h.replace(DIV, function (_, a, b) { return frac(a, b); });
    return h.replace(/\n/g, '<br>');
  }
  function table(t, cls) {
    if (!t) return '';
    return '<div class="fa-table-wrap"><table class="fa-table ' + (cls || '') + '">' + (t.caption ? '<caption>' + rich(t.caption) + '</caption>' : '') +
      '<thead><tr>' + t.headers.map(function (h) { return '<th scope="col">' + rich(h) + '</th>'; }).join('') + '</tr></thead><tbody>' +
      t.rows.map(function (r) { return '<tr>' + r.map(function (c, i) { return i ? '<td>' + rich(c) + '</td>' : '<th scope="row">' + rich(c) + '</th>'; }).join('') + '</tr>'; }).join('') + '</tbody></table></div>';
  }
  function doc(d) {
    if (!d) return '';
    return '<figure class="fa-doc fa-doc-' + esc(d.kind || 'generic') + '"><figcaption><span class="fa-doc-kind">' + esc((d.kind || 'document').replace(/-/g, ' ')) + ' · fictional</span><strong>' + esc(d.title) + '</strong></figcaption>' +
      (d.meta ? '<dl class="fa-doc-meta">' + d.meta.map(function (m) { return '<div><dt>' + esc(m[0]) + '</dt><dd>' + rich(m[1]) + '</dd></div>'; }).join('') + '</dl>' : '') +
      (d.boxes ? '<div class="fa-doc-boxes">' + d.boxes.map(function (b) { return '<div class="fa-doc-box' + (b[2] ? ' wide' : '') + '"><span>' + esc(b[0]) + '</span><b>' + rich(b[1]) + '</b></div>'; }).join('') + '</div>' : '') +
      table(d.table) + (d.notes ? '<ul class="fa-doc-notes">' + d.notes.map(function (n) { return '<li>' + rich(n) + '</li>'; }).join('') + '</ul>' : '') + '</figure>';
  }
  /* Graph of one or more functions (2026-11-17): g = {title, x:{label,min,max,step}, y:{label,min,max,step,money},
     series:[{name, pts:[[x,y],...]}], marks:[{x,y,label}], caption}. Inline SVG, so it prints and works offline; the
     series are told apart by line style as well as colour, and the aria-label lists every series and marked point. */
  var GCOL = ['#2f45c4', '#c4561a', '#178a52'], GDASH = ['', '7 5', '2 4'];
  function gnum(v, money) { var r = Math.round(v * 100) / 100, a = Math.abs(r), s = a >= 1000 ? Math.round(a).toLocaleString('en-US') : String(a); return (r < 0 ? '−' : '') + (money ? '$' : '') + s; }
  function graph(g) {
    if (!g) return '';
    var W = 560, H = 320, L = 86, R = 34, T = 16, B = 52, x = g.x, y = g.y;
    var px = function (v) { return L + (v - x.min) / (x.max - x.min) * (W - L - R); }, py = function (v) { return H - B - (v - y.min) / (y.max - y.min) * (H - T - B); };
    var h = '', v;
    for (v = x.min; v <= x.max + 1e-9; v += x.step) h += '<line x1="' + px(v) + '" x2="' + px(v) + '" y1="' + T + '" y2="' + (H - B) + '" class="fa-g-grid"/><text x="' + px(v) + '" y="' + (H - B + 16) + '" text-anchor="middle">' + gnum(v, x.money) + '</text>';
    for (v = y.min; v <= y.max + 1e-9; v += y.step) h += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + py(v) + '" y2="' + py(v) + '" class="fa-g-grid"/><text x="' + (L - 6) + '" y="' + (py(v) + 4) + '" text-anchor="end">' + gnum(v, y.money) + '</text>';
    h += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + py(Math.max(y.min, 0)) + '" y2="' + py(Math.max(y.min, 0)) + '" class="fa-g-axis"/><line x1="' + px(Math.max(x.min, 0)) + '" x2="' + px(Math.max(x.min, 0)) + '" y1="' + T + '" y2="' + (H - B) + '" class="fa-g-axis"/>';
    h += '<text x="' + ((L + W - R) / 2) + '" y="' + (H - 12) + '" text-anchor="middle" class="fa-g-lab">' + esc(x.label) + '</text><text transform="translate(14 ' + ((T + H - B) / 2) + ') rotate(-90)" text-anchor="middle" class="fa-g-lab">' + esc(y.label) + '</text>';
    (g.series || []).forEach(function (s, i) {
      h += '<polyline fill="none" stroke="' + GCOL[i % 3] + '" stroke-width="2.6" stroke-dasharray="' + GDASH[i % 3] + '" points="' + s.pts.map(function (p) { return px(p[0]).toFixed(1) + ',' + py(p[1]).toFixed(1); }).join(' ') + '"/>';
    });
    (g.marks || []).forEach(function (m) { h += '<circle cx="' + px(m.x) + '" cy="' + py(m.y) + '" r="4.5" class="fa-g-mark"/>' + (m.label ? '<text x="' + (px(m.x) + 7) + '" y="' + (py(m.y) - 7) + '" class="fa-g-mlab">' + esc(m.label) + '</text>' : ''); });
    var desc = (g.title || 'Graph') + '. ' + (g.series || []).map(function (s) { return s.name; }).join('; ') + '. ' + (g.marks || []).map(function (m) { return m.label || ('(' + m.x + ', ' + m.y + ')'); }).join('; ');
    var key = (g.series || []).length > 1 || (g.series[0] && g.series[0].name) ? '<ul class="fa-g-key">' + g.series.map(function (s, i) { return '<li><svg width="34" height="10" aria-hidden="true"><line x1="0" x2="34" y1="5" y2="5" stroke="' + GCOL[i % 3] + '" stroke-width="3" stroke-dasharray="' + GDASH[i % 3] + '"/></svg>' + rich(s.name) + '</li>'; }).join('') + '</ul>' : '';
    return '<figure class="fa-graph">' + (g.title ? '<figcaption>' + rich(g.title) + '</figcaption>' : '') + '<svg class="fa-g-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc(desc) + '">' + h + '</svg>' + key + (g.caption ? '<p class="fa-g-cap">' + rich(g.caption) + '</p>' : '') + '</figure>';
  }
  function scenario(s) {
    if (!s) return '';
    return (s.title ? '<p class="fa-scn-title">' + rich(s.title) + '</p>' : '') + (s.text ? '<p>' + rich(s.text) + '</p>' : '') + table(s.table) + doc(s.document) + graph(s.graph);
  }
  function rubric(r, scale) {
    if (!r) return '';
    scale = scale || 1;
    var tot = r.reduce(function (s, c) { return s + c.points; }, 0) * scale;
    return '<div class="fa-table-wrap"><table class="fa-table fa-rubric"><caption>Scoring rubric (' + tot + ' points). Accept any defensible conclusion supported by accurate evidence.</caption><thead><tr><th>Criterion</th><th>Full credit</th><th>Partial</th><th>Minimal</th></tr></thead><tbody>' +
      r.map(function (c) { return '<tr><th scope="row">' + esc(c.criterion) + ' (' + c.points * scale + ')</th><td>' + rich(c.full) + '</td><td>' + rich(c.partial || '') + '</td><td>' + rich(c.none || '') + '</td></tr>'; }).join('') + '</tbody></table></div>';
  }
  var LINES = { 'short-answer': 3, 'multiple-choice': 0, 'select-all': 0, 'open-response': 5 };
  function lines(n) { var h = ''; for (var i = 0; i < n; i++) h += '<div class="fa-line"></div>'; return n ? '<div class="fa-lines" aria-hidden="true">' + h + '</div>' : ''; }
  /* opts: {n, teacher, space (multiplier), showType} */
  function question(q, opts) {
    opts = opts || {};
    var sp = opts.space == null ? 1 : opts.space, t = opts.teacher;
    var h = '<article class="fa-q" data-format="' + q.format + '" data-type="' + q.type + '"><div class="fa-q-head">' + (opts.n ? '<span class="fa-q-num">' + opts.n + '</span>' : '') +
      (opts.showType !== false ? '<span class="fa-q-tag">' + esc(TYPE_LABEL[q.type] || q.type) + '</span>' : '') + (opts.points ? '<span class="fa-q-pts">' + opts.points + ' pt' + (opts.points > 1 ? 's' : '') + '</span>' : '') + '</div>';
    h += scenario(q.scenario) + '<div class="fa-q-prompt">' + rich(q.prompt) + '</div>';
    if (q.options) h += '<ol class="fa-opts" type="A">' + q.options.map(function (o) { return '<li' + (t && o.correct ? ' class="fa-correct"' : '') + '>' + (q.format === 'select-all' ? '<span class="fa-box" aria-hidden="true"></span>' : '') + rich(o.text) + '</li>'; }).join('') + '</ol>';
    if (q.parts) h += '<ol class="fa-parts" type="a">' + q.parts.map(function (p) { return '<li><div>' + rich(p.prompt) + '</div>' + (t ? '<div class="fa-key">' + rich(p.answer) + '</div>' : lines(Math.round(3 * sp))) + '</li>'; }).join('') + '</ol>';
    else if (!t) h += lines(Math.round((LINES[q.format] || 0) * sp));
    if (t) {
      h += '<div class="fa-key"><strong>Answer:</strong> ' + rich(Array.isArray(q.answer) ? q.answer.join('; ') : q.answer) + '</div>';
      h += '<details class="fa-sol" open><summary>Worked solution</summary><ol>' + q.solutionSteps.map(function (s) { return '<li>' + rich(s) + '</li>'; }).join('') + '</ol></details>';
      if (q.modelResponse) h += '<div class="fa-model"><strong>Model response:</strong> ' + rich(q.modelResponse) + '</div>';
      if (q.misconceptions && q.misconceptions.length) h += '<div class="fa-mis"><strong>Watch for:</strong> ' + q.misconceptions.map(rich).join(' ') + '</div>';
      if (q.rubric) h += rubric(q.rubric);
    }
    return h + '</article>';
  }
  var TYPE_LABEL = { vocabulary: 'Vocabulary', concept: 'Concept', scenario: 'Scenario', comparison: 'Compare options', document: 'Document analysis', calculation: 'Math application', modeling: 'Algebra modeling', reasoning: 'Reasoning', claim: 'Evaluate a claim' };
  /* Check a student's numeric answer deterministically. */
  function checkNumeric(q, input) {
    if (!q.numeric) return null;
    var v = parseFloat(String(input).replace(/[−–]/g, '-').replace(/[$,%\s]/g, ''));
    if (isNaN(v)) return false;
    return Math.abs(v - q.numeric.value) <= (q.numeric.tolerance || 0) + 1e-9;
  }
  G.FA_RENDER = { esc: esc, rich: rich, frac: frac, table: table, doc: doc, graph: graph, scenario: scenario, rubric: rubric, question: question, lines: lines, checkNumeric: checkNumeric, TYPE_LABEL: TYPE_LABEL };
})(typeof window !== 'undefined' ? window : globalThis);
