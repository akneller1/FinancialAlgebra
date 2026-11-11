/* Financial Algebra shared HTML renderers (browser + Node). Attaches globalThis.FA_RENDER.
 * Division is displayed as a stacked fraction (numerator over denominator) — never with "/". */
(function (G) {
  'use strict';
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  var TOK = '(\\(?[−-]?\\$?[\\d,]*\\.?\\d+%?\\)?|\\([^()]{1,40}\\))';
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
      table(d.table) + (d.notes ? '<ul class="fa-doc-notes">' + d.notes.map(function (n) { return '<li>' + rich(n) + '</li>'; }).join('') + '</ul>' : '') + '</figure>';
  }
  function scenario(s) {
    if (!s) return '';
    return (s.title ? '<p class="fa-scn-title">' + rich(s.title) + '</p>' : '') + (s.text ? '<p>' + rich(s.text) + '</p>' : '') + table(s.table) + doc(s.document);
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
  var TYPE_LABEL = { vocabulary: 'Vocabulary', concept: 'Concept', scenario: 'Scenario', comparison: 'Compare options', document: 'Document analysis', calculation: 'Math application', reasoning: 'Reasoning', claim: 'Evaluate a claim' };
  /* Check a student's numeric answer deterministically. */
  function checkNumeric(q, input) {
    if (!q.numeric) return null;
    var v = parseFloat(String(input).replace(/[−–]/g, '-').replace(/[$,%\s]/g, ''));
    if (isNaN(v)) return false;
    return Math.abs(v - q.numeric.value) <= (q.numeric.tolerance || 0) + 1e-9;
  }
  G.FA_RENDER = { esc: esc, rich: rich, frac: frac, table: table, doc: doc, scenario: scenario, rubric: rubric, question: question, lines: lines, checkNumeric: checkNumeric, TYPE_LABEL: TYPE_LABEL };
})(typeof window !== 'undefined' ? window : globalThis);
