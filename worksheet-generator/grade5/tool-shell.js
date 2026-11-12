/* Shared shell for Grade 5 Interactive Math tools (artifacts/math5-[tool]/index.html).
 * Header with zoom (A−/A+), Student/Teacher view, Fit, Present (projector) and Reset; a "Try this" challenge list that ticks off
 * as students meet each goal; and a closed "What should I notice?" panel. No network, no tracking. */
(function (G) {
  'use strict';
  var zoom = 1;
  function $(id) { return G.document.getElementById(id); }
  function setZoom(z) { zoom = Math.max(0.7, Math.min(2.2, z)); G.document.documentElement.style.fontSize = (17 * zoom) + 'px'; $('tsZoom').textContent = Math.round(zoom * 100) + '%'; }
  function init(o) {
    var top = G.document.createElement('header'); top.className = 'g5-top';
    top.innerHTML = '<a href="../../index.html#math5">← 5th Grade Math</a><span class="g5-title">' + o.title + '</span><div class="g5-tools" role="toolbar" aria-label="Display controls">' +
      '<button type="button" id="tsOut" aria-label="Zoom out">A−</button><button type="button" id="tsZoom" aria-label="Reset zoom">100%</button><button type="button" id="tsIn" aria-label="Zoom in">A+</button>' +
      '<button type="button" id="tsMode" aria-pressed="false" title="Switch between the student view and the teacher view">Teacher view</button><button type="button" id="tsFit">Fit</button><button type="button" id="tsPresent" aria-pressed="false">Present</button><button type="button" id="tsReset">Reset</button></div>';
    G.document.body.insertBefore(top, G.document.body.firstChild);
    $('tsOut').onclick = function () { setZoom(zoom - 0.1); }; $('tsIn').onclick = function () { setZoom(zoom + 0.1); }; $('tsZoom').onclick = function () { setZoom(1); };
    $('tsFit').onclick = function () { var m = G.document.querySelector('main.g5'); setZoom(1); setZoom(Math.max(0.7, Math.min(1.8, G.innerHeight / (m.scrollHeight + top.offsetHeight + 16)))); };
    $('tsPresent').onclick = function () { var on = G.document.body.classList.toggle('present'); this.setAttribute('aria-pressed', on); };
    $('tsReset').onclick = function () { if (o.reset) o.reset(); };
    if (new URLSearchParams(G.location.search).get('present') === '1') $('tsPresent').click();
    /* Student view (default): the tool, challenges and the closed "notice" panel. Teacher view adds teaching notes,
       opens the "notice" panel and links the printable worksheet and teacher key. Nothing is saved. */
    var tn = G.document.createElement('section'); tn.id = 'tsTeacher'; tn.className = 'g5-card ts-teacher'; tn.hidden = true;
    tn.innerHTML = '<h2>Teacher notes</h2>' + (o.teacher ? '<ul>' + o.teacher.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul>' : '') +
      (o.challenges ? '<p><b>Challenges students work toward:</b> ' + o.challenges.map(function (c) { return c.text; }).join(' · ') + '</p>' : '') +
      '<p><a href="worksheet.pdf" target="_blank" rel="noopener">Printable student worksheet (PDF)</a> · <a href="teacher-key.pdf" target="_blank" rel="noopener">Teacher key (PDF)</a></p>';
    var mainEl = G.document.querySelector('main') || G.document.body; mainEl.insertBefore(tn, mainEl.firstChild);
    function setMode(teacher) {
      G.document.body.classList.toggle('teacher', teacher); tn.hidden = !teacher;
      $('tsMode').setAttribute('aria-pressed', teacher); $('tsMode').textContent = teacher ? 'Student view' : 'Teacher view';
      var d = G.document.querySelector('#notice details'); if (d) d.open = teacher;
    }
    $('tsMode').onclick = function () { setMode(!G.document.body.classList.contains('teacher')); };
    if (new URLSearchParams(G.location.search).get('mode') === 'teacher') setTimeout(function () { setMode(true); }, 0);
    var ch = $('challenges');
    if (ch && o.challenges) ch.innerHTML = '<h2>Try this</h2><ol class="ts-ch">' + o.challenges.map(function (c, i) { return '<li id="ch' + i + '"><span class="box" aria-hidden="true">☐</span> ' + c.text + '</li>'; }).join('') + '</ol>';
    var nt = $('notice');
    if (nt && o.notice) nt.innerHTML = '<details><summary>What should I notice?</summary><ul>' + o.notice.map(function (n) { return '<li>' + n + '</li>'; }).join('') + '</ul></details>';
  }
  /* Call after every change with the current state; ticks challenges whose test(state) is true. */
  function update(o, st) {
    (o.challenges || []).forEach(function (c, i) { var li = $('ch' + i); if (li && !li.classList.contains('done') && c.test(st)) { li.classList.add('done'); li.querySelector('.box').textContent = '☑'; } });
  }
  function frac(n, d) { return '<span class="fr"><span class="fn">' + n + '</span><span class="fd">' + d + '</span></span>'; }
  function gcd(a, b) { return b ? gcd(b, a % b) : Math.abs(a); }
  function mixed(n, d) { var g = gcd(n, d); n /= g; d /= g; if (d === 1) return String(n); var w = Math.floor(n / d), r = n % d; return (w ? w + ' ' : '') + frac(r, d); }
  G.TOOL = { init: init, update: update, frac: frac, gcd: gcd, mixed: mixed, $: $ };
})(window);
