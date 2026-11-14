/* Shared shell for elementary Interactive Math tools (artifacts/<course>-<tool>/index.html).
 * Header: back link, zoom (A−, %, A+), Fit, Present, Teacher view, Reset. A "Try this" list ticks off as students meet each
 * goal, and "What should I notice?" stays closed until opened (Teacher view opens it and shows teaching notes).
 * Zoom changes the root font size, and every tool is sized in rem, so the picture and its controls always scale
 * together. Fit measures the whole workspace (picture + controls) and picks the largest zoom that shows all of it.
 * No network calls, no tracking, nothing stored except the display zoom. */
(function (G) {
  'use strict';
  var D = G.document, zoom = 1, BASE = 17, opts = null;
  function $(id) { return D.getElementById(id); }
  function setZoom(z) { zoom = Math.max(0.6, Math.min(2.6, +z.toFixed(2))); D.documentElement.style.fontSize = (BASE * zoom) + 'px'; var b = $('tsZoom'); if (b) b.textContent = Math.round(zoom * 100) + '%'; }
  /* Largest zoom at which header + workspace fit in the window (height and width). Recomputed a few times because
     text wraps differently at each size. */
  function fit() {
    var ws = $('workspace'), top = D.querySelector('.tl-top');
    if (!ws) return;
    setZoom(1);
    for (var k = 0; k < 4; k++) {
      var availH = G.innerHeight - top.offsetHeight - 0.9 * BASE * zoom * 2, h = ws.offsetHeight;
      var availW = G.innerWidth - 0.9 * BASE * zoom * 2, w = ws.scrollWidth;
      var z = zoom * Math.min(availH / h, w > availW ? availW / w : 99);
      if (Math.abs(z - zoom) < 0.02) break;
      setZoom(z);
    }
    /* safety: never leave any part of the workspace outside the window */
    for (var n = 0; n < 40 && zoom > 0.6; n++) { var r = ws.getBoundingClientRect(); if (r.bottom <= G.innerHeight - 2 && D.documentElement.scrollWidth <= G.innerWidth + 1) break; setZoom(zoom - 0.02); }
    G.scrollTo(0, 0);
  }
  function homeUrl(course) {
    try {
      var r = D.referrer ? new URL(D.referrer) : null;
      if (r && r.origin === G.location.origin && /\/(?:[\w-]+\.html)?$/.test(r.pathname) && r.pathname.indexOf('/artifacts/') < 0 && r.pathname.indexOf('/worksheet-generator/') < 0) { try { G.sessionStorage.setItem('el-home-' + course, r.origin + r.pathname); } catch (e) {} return r.origin + r.pathname; }
      var s = G.sessionStorage.getItem('el-home-' + course); if (s) return s;
    } catch (e) {}
    return '../../index.html';
  }
  function init(o) {
    opts = o;
    D.body.classList.add('tl');
    var P = new URLSearchParams(G.location.search), student = P.get('student') === '1';
    var top = D.createElement('header'); top.className = 'tl-top';
    top.innerHTML = (student ? '' : '<a id="tsHome" href="#">← ' + o.courseName + '</a>') + '<span class="tl-title">' + o.title + '</span><div class="tl-bar" role="toolbar" aria-label="Display controls">' +
      '<button type="button" id="tsOut" aria-label="Smaller">A−</button><button type="button" id="tsZoom" aria-label="Reset size to 100%">100%</button><button type="button" id="tsIn" aria-label="Larger">A+</button>' +
      '<button type="button" id="tsFit" title="Make the whole activity fit this screen">Fit</button><button type="button" id="tsPresent" aria-pressed="false" title="Presentation mode for a projector or smartboard">Present</button>' +
      (student ? '' : '<button type="button" id="tsMode" aria-pressed="false" title="Show or hide the teacher notes">Teacher view</button>') + '<button type="button" id="tsReset">Reset</button></div>';
    D.body.insertBefore(top, D.body.firstChild);
    if ($('tsHome')) $('tsHome').href = homeUrl(o.course) + '#' + o.course + (o.unit ? '.' + o.unit : '');
    $('tsOut').onclick = function () { setZoom(zoom - 0.1); }; $('tsIn').onclick = function () { setZoom(zoom + 0.1); }; $('tsZoom').onclick = function () { setZoom(1); };
    $('tsFit').onclick = fit;
    $('tsPresent').onclick = function () {
      var on = D.body.classList.toggle('present'); this.setAttribute('aria-pressed', on);
      if (on && D.documentElement.requestFullscreen) D.documentElement.requestFullscreen().then(function () { setTimeout(fit, 150); }, function () { fit(); });
      else { if (!on && D.fullscreenElement && D.exitFullscreen) D.exitFullscreen(); if (on) fit(); else setZoom(1); }
    };
    $('tsReset').onclick = function () { if (o.reset) o.reset(); (o.challenges || []).forEach(function (c, i) { var li = $('ch' + i); if (li) { li.classList.remove('done'); li.querySelector('.box').textContent = '☐'; } }); };
    var mainEl = D.querySelector('main');
    var tn = D.createElement('section'); tn.id = 'tsTeacher'; tn.className = 'tl-card tl-teacher'; tn.hidden = true;
    tn.innerHTML = '<h2>Teacher notes</h2>' + (o.teacher ? '<ul>' + o.teacher.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul>' : '') +
      (o.standards ? '<p><b>Standards:</b> ' + o.standards + '</p>' : '') +
      (o.challenges ? '<p><b>Challenges students work toward:</b> ' + o.challenges.map(function (c) { return c.text; }).join(' · ') + '</p>' : '') +
      /* Grade 5 parity: tools that ship an Explore & Reflect worksheet and teacher key link them here (teacher view only). */
      (o.printables ? '<p><a href="worksheet.pdf" target="_blank" rel="noopener">Printable student worksheet (PDF)</a> · <a href="teacher-key.pdf" target="_blank" rel="noopener">Teacher key (PDF)</a></p>' : '') + '<p>Use <b>Present</b> on a projector or smartboard, and <b>Fit</b> to make the picture and its controls fill the screen together.</p>';
    mainEl.appendChild(tn);
    function setMode(t) { D.body.classList.toggle('teacher', t); tn.hidden = !t; var b = $('tsMode'); if (b) { b.setAttribute('aria-pressed', t); b.textContent = t ? 'Student view' : 'Teacher view'; } var d = D.querySelector('#notice details'); if (d) d.open = t; }
    if ($('tsMode')) $('tsMode').onclick = function () { setMode(!D.body.classList.contains('teacher')); };
    if (P.get('mode') === 'teacher' && !student) setTimeout(function () { setMode(true); }, 0);
    var ch = $('challenges');
    if (ch && o.challenges) ch.innerHTML = '<h2>Try this</h2><ol class="tl-ch">' + o.challenges.map(function (c, i) { return '<li id="ch' + i + '"><span class="box" aria-hidden="true">☐</span> ' + c.text + '</li>'; }).join('') + '</ol>';
    var nt = $('notice');
    if (nt && o.notice) nt.innerHTML = '<details><summary>What should I notice?</summary><ul>' + o.notice.map(function (n) { return '<li>' + n + '</li>'; }).join('') + '</ul></details>';
    try { var z = +G.localStorage.getItem('el-tool-zoom'); if (z) setZoom(z); } catch (e) {}
    G.addEventListener('beforeunload', function () { try { G.localStorage.setItem('el-tool-zoom', zoom); } catch (e) {} });
    if (P.get('present') === '1') { D.body.classList.add('present'); $('tsPresent').setAttribute('aria-pressed', true); setTimeout(fit, 60); }
  }
  /* Call after every change with the current state; ticks challenges whose test(state) is true. */
  function update(st) {
    ((opts && opts.challenges) || []).forEach(function (c, i) { var li = $('ch' + i), ok = false; try { ok = c.test(st); } catch (e) {} if (li && ok && !li.classList.contains('done')) { li.classList.add('done'); li.querySelector('.box').textContent = '☑'; } });
  }
  function frac(n, d) { return '<span class="fr"><span class="fn">' + n + '</span><span class="fd">' + d + '</span></span>'; }
  function gcd(a, b) { return b ? gcd(b, a % b) : Math.abs(a); }
  function mixed(n, d) { if (n % d === 0) return String(n / d); var w = Math.floor(n / d), r = n % d; return (w ? w + ' ' : '') + frac(r, d); }
  function comma(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  /* +/− stepper buttons: <button data-k="key" data-s="1">. onStep(key, delta) */
  function steppers(root, onStep) { root.addEventListener('click', function (e) { var b = e.target.closest('button[data-k]'); if (b) onStep(b.dataset.k, +b.dataset.s); }); }
  G.TOOL = { init: init, update: update, fit: fit, setZoom: setZoom, zoom: function () { return zoom; }, frac: frac, gcd: gcd, mixed: mixed, comma: comma, steppers: steppers, $: $ };
})(window);
