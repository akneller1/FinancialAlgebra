/* Shared drawing helpers and three reusable engines for elementary Interactive Math tools (Grades 1–3).
 * Load after el-tool-shell.js. Tools stay self-contained pages; this file only removes repetition.
 *   ELK.step(key, label, steps)     stepper markup: −10 −1 [value] +1 +10 (works with TOOL.steppers)
 *   ELK.words(n)                    number names to 1,000
 *   ELK.clockSvg(h, m, opt)         analog clock face
 *   ELK.timeWords(h, m, level)      "half past 3", "quarter to 5", "25 minutes after 4"
 *   ELK.clockTool(cfg)              Grade 1/2 clock explorer
 *   ELK.graphTool(cfg)              tally chart, picture graph and bar graph builder (scaled for Grade 3)
 *   ELK.sharesTool(cfg)             equal shares: halves, thirds, fourths; optional rows × columns grid
 * Everything is drawn as inline SVG sized in viewBox units, so the shell's zoom, Fit and Present scale it with the page.
 * No network calls; nothing is stored. */
(function (G) {
  'use strict';
  var T = G.TOOL, D = G.document, K = {};
  K.esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  K.svg = function (w, h, inner, label) { return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + w + ' ' + h + '" role="img" aria-label="' + K.esc(label || '') + '">' + inner + '</svg>'; };
  K.txt = function (x, y, s, o) { o = o || {}; return '<text x="' + x + '" y="' + y + '" text-anchor="' + (o.a || 'middle') + '" font-size="' + (o.size || 18) + '" font-weight="' + (o.w || 800) + '" fill="' + (o.fill || '#1d2a3a') + '"' + (o.extra || '') + '>' + s + '</text>'; };
  /* steps: list of positive step sizes, e.g. [1, 10]. Buttons are − biggest … − smallest [value] + smallest … + biggest. */
  K.step = function (key, label, steps, val) {
    steps = steps || [1];
    var dn = steps.slice().reverse().map(function (s) { return '<button type="button" data-k="' + key + '" data-s="-' + s + '" aria-label="' + label + ' minus ' + s + '">−' + (steps.length > 1 ? s : '') + '</button>'; }).join('');
    var up = steps.map(function (s) { return '<button type="button" data-k="' + key + '" data-s="' + s + '" aria-label="' + label + ' plus ' + s + '">+' + (steps.length > 1 ? s : '') + '</button>'; }).join('');
    return '<div class="tl-field"><span class="lab">' + label + '</span><div class="tl-step' + (steps.length > 1 ? ' tl-step-wide' : '') + '">' + dn + '<b id="v-' + key + '" aria-live="polite">' + (val == null ? '' : val) + '</b>' + up + '</div></div>';
  };
  K.clamp = function (v, lo, hi) { return Math.max(lo, Math.min(hi, v)); };
  var ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split(' '),
    TENS = ',,twenty,thirty,forty,fifty,sixty,seventy,eighty,ninety'.split(',');
  K.words = function (n) {
    if (n < 20) return ONES[n];
    if (n < 100) return TENS[Math.floor(n / 10)] + (n % 10 ? '-' + ONES[n % 10] : '');
    if (n < 1000) return ONES[Math.floor(n / 100)] + ' hundred' + (n % 100 ? ' ' + K.words(n % 100) : '');
    return 'one thousand';
  };
  K.pad = function (m) { return (m < 10 ? '0' : '') + m; };

  /* ---------------------------------------------------------------- clock */
  K.clockSvg = function (h, m, opt) {
    opt = opt || {};
    var c = 160, r = 140, s = '<circle cx="160" cy="160" r="150" fill="' + (opt.face || '#fff') + '" stroke="#22408a" stroke-width="8"/>', i, a;
    for (i = 0; i < 60; i++) { a = i * Math.PI / 30; var big = i % 5 === 0, r1 = big ? 122 : 131; s += '<line x1="' + (c + r1 * Math.sin(a)).toFixed(1) + '" y1="' + (c - r1 * Math.cos(a)).toFixed(1) + '" x2="' + (c + r * Math.sin(a)).toFixed(1) + '" y2="' + (c - r * Math.cos(a)).toFixed(1) + '" stroke="#1d2a3a" stroke-width="' + (big ? 4 : 1.6) + '"/>'; }
    for (i = 1; i <= 12; i++) { a = i * Math.PI / 6; s += K.txt((c + 100 * Math.sin(a)).toFixed(1), (c - 100 * Math.cos(a) + 11).toFixed(1), i, { size: 32, w: 900 }); }
    if (opt.fives) for (i = 0; i < 12; i++) { a = i * Math.PI / 6; s += K.txt((c + 166 * Math.sin(a)).toFixed(1), (c - 166 * Math.cos(a) + 6).toFixed(1), K.pad(i * 5), { size: 15, fill: '#1f78c8' }); }
    var ha = ((h % 12) + m / 60) * Math.PI / 6, ma = m * Math.PI / 30;
    s += '<line x1="160" y1="160" x2="' + (c + 72 * Math.sin(ha)).toFixed(1) + '" y2="' + (c - 72 * Math.cos(ha)).toFixed(1) + '" stroke="#d63c7a" stroke-width="13" stroke-linecap="round"/>';
    s += '<line x1="160" y1="160" x2="' + (c + 118 * Math.sin(ma)).toFixed(1) + '" y2="' + (c - 118 * Math.cos(ma)).toFixed(1) + '" stroke="#1f78c8" stroke-width="7" stroke-linecap="round"/>';
    s += '<circle cx="160" cy="160" r="10" fill="#1d2a3a"/>';
    var pad = opt.fives ? 26 : 0;
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="' + (-pad) + ' ' + (-pad) + ' ' + (320 + 2 * pad) + ' ' + (320 + 2 * pad) + '" role="img" aria-label="Clock showing ' + h + ':' + K.pad(m) + '. The short pink hand is the hour hand and the long blue hand is the minute hand.">' + s + '</svg>';
  };
  K.timeWords = function (h, m, level) {
    var nx = h % 12 + 1;
    if (m === 0) return h + ' o’clock';
    if (m === 30) return 'half past ' + h;
    if (level === 1) return m + ' minutes after ' + h;
    if (m === 15) return 'quarter past ' + h;
    if (m === 45) return 'quarter to ' + nx;
    if (m < 30) return m + ' minute' + (m === 1 ? '' : 's') + ' after ' + h;
    return (60 - m) + ' minute' + (60 - m === 1 ? '' : 's') + ' before ' + nx;
  };
  /* cfg: { course, courseName, unit, title, standards, steps:[minutes…], ampm, fives, level, start:[h,m], challenges(fn → list), notice, teacher } */
  K.clockTool = function (cfg) {
    var st;
    function reset() { st = { h: cfg.start[0], m: cfg.start[1], pm: false, hist: [], minLabels: !!cfg.fives }; log(); draw(); }
    function key() { return st.h + ':' + K.pad(st.m) + (cfg.ampm ? (st.pm ? 'pm' : 'am') : ''); }
    function log() { st.hist.push(key()); if (st.hist.length > 40) st.hist.shift(); }
    function move(min) {
      var t = ((st.h % 12) * 60 + st.m + min) % 720; if (t < 0) t += 720;
      var before = st.h % 12 * 60 + st.m;
      if (cfg.ampm && ((min > 0 && t < before) || (min < 0 && t > before))) st.pm = !st.pm;   // crossed 12
      st.h = Math.floor(t / 60) || 12; st.m = t % 60; log(); draw();
    }
    var ws = T.$('ckTool');
    ws.innerHTML = '<div class="el-clock-row"><div class="tl-model el-clock" id="ckFace"></div><div class="el-clock-side"><div class="el-digital" id="ckDig" aria-live="polite"></div><div class="tl-out" id="ckOut"></div></div></div>' +
      '<div class="tl-controls" id="ckCtl">' + cfg.steps.map(function (s) { var lab = s >= 60 ? (s / 60) + ' hour' : s + ' minutes'; return '<div class="tl-field"><span class="lab">' + lab + '</span><div class="tl-step"><button type="button" data-k="t" data-s="-' + s + '" aria-label="Back ' + lab + '">−</button><button type="button" data-k="t" data-s="' + s + '" aria-label="Forward ' + lab + '">+</button></div></div>'; }).join('') +
      (cfg.ampm ? '<div class="tl-field"><span class="lab">Morning or afternoon</span><div class="tl-step"><button type="button" class="tl-btn" id="ckAm" aria-pressed="true">a.m.</button><button type="button" class="tl-btn" id="ckPm" aria-pressed="false">p.m.</button></div></div>' : '') +
      (cfg.fives ? '<div class="tl-field"><span class="lab">Helpers</span><button type="button" class="tl-btn" id="ckFives" aria-pressed="true">Minute labels</button></div>' : '') + '</div>';
    function draw() {
      T.$('ckFace').innerHTML = K.clockSvg(st.h, st.m, { fives: st.minLabels, face: cfg.ampm ? (st.pm && st.h !== 12 && st.h >= 6 ? '#eef2ff' : '#fffef5') : '#fff' });
      T.$('ckDig').innerHTML = st.h + ':' + K.pad(st.m) + (cfg.ampm ? ' <small>' + (st.pm ? 'p.m.' : 'a.m.') + '</small>' : '');
      var hourNote = st.m === 0 ? 'The hour hand points right at the <b>' + st.h + '</b>.' : 'The hour hand is between the <b>' + st.h + '</b> and the <b>' + (st.h % 12 + 1) + '</b>.';
      var minNote = st.m === 0 ? 'The minute hand points to the <b>12</b>.' : 'The minute hand points ' + (st.m % 5 === 0 ? 'to the <b>' + (st.m / 5) + '</b>' : 'between the <b>' + (Math.floor(st.m / 5) || 12) + '</b> and the <b>' + (Math.floor(st.m / 5) + 1) + '</b>') + ' — that is <b>' + st.m + '</b> minutes after the hour.';
      var day = cfg.ampm ? '<br>' + (st.pm ? (st.h === 12 ? 'Noon to midnight: afternoon (12 p.m. is noon).' : st.h >= 6 && st.h !== 12 ? 'Evening or night (p.m.).' : 'Afternoon (p.m.).') : (st.h === 12 ? 'Midnight to noon: 12 a.m. is midnight.' : st.h < 6 ? 'Night or very early morning (a.m.).' : 'Morning (a.m.).')) : '';
      T.$('ckOut').innerHTML = '<b>In words:</b> ' + K.timeWords(st.h, st.m, cfg.level) + '<br>' + hourNote + '<br>' + minNote + day;
      if (cfg.ampm) { T.$('ckAm').setAttribute('aria-pressed', !st.pm); T.$('ckPm').setAttribute('aria-pressed', st.pm); }
      T.update({ h: st.h, m: st.m, pm: st.pm, hist: st.hist.slice() });
    }
    T.init({ course: cfg.course, courseName: cfg.courseName, unit: cfg.unit, title: cfg.title, standards: cfg.standards, teacher: cfg.teacher, notice: cfg.notice, challenges: cfg.challenges, reset: reset, printables: true });
    T.steppers(T.$('ckCtl'), function (k, d) { move(d); });
    if (cfg.ampm) { T.$('ckAm').onclick = function () { st.pm = false; log(); draw(); }; T.$('ckPm').onclick = function () { st.pm = true; log(); draw(); }; }
    if (cfg.fives) T.$('ckFives').onclick = function () { st.minLabels = !st.minLabels; this.setAttribute('aria-pressed', st.minLabels); draw(); };
    G.addEventListener('keydown', function (e) { if (e.target.closest && e.target.closest('input,select,textarea')) return; var s = cfg.steps[cfg.steps.length - 1]; if (e.key === 'ArrowRight') { move(s); e.preventDefault(); } if (e.key === 'ArrowLeft') { move(-s); e.preventDefault(); } });
    reset();
    return { seq: function (hist, list) { var j = hist.join('|'); return j.indexOf(list.join('|')) >= 0; } };
  };
  K.histHas = function (hist, list) { return ('|' + hist.join('|') + '|').indexOf('|' + list.join('|') + '|') >= 0; };

  /* ---------------------------------------------------------------- graphs */
  /* A single picture symbol for every category (a smiley face), drawn whole or cut to a fraction for scaled keys. */
  function face(x, y, s, part) {
    var id = 'cl' + Math.random().toString(36).slice(2, 8), g = '';
    if (part < 1) g += '<clipPath id="' + id + '"><rect x="' + x + '" y="' + y + '" width="' + (s * part) + '" height="' + s + '"/></clipPath>';
    g += '<g' + (part < 1 ? ' clip-path="url(#' + id + ')"' : '') + '><circle cx="' + (x + s / 2) + '" cy="' + (y + s / 2) + '" r="' + (s / 2 - 1.5) + '" fill="#ffd34d" stroke="#b7791f" stroke-width="2"/>' +
      '<circle cx="' + (x + s * 0.36) + '" cy="' + (y + s * 0.4) + '" r="' + (s * 0.06) + '" fill="#1d2a3a"/><circle cx="' + (x + s * 0.64) + '" cy="' + (y + s * 0.4) + '" r="' + (s * 0.06) + '" fill="#1d2a3a"/>' +
      '<path d="M' + (x + s * 0.3) + ' ' + (y + s * 0.6) + ' Q' + (x + s / 2) + ' ' + (y + s * 0.8) + ' ' + (x + s * 0.7) + ' ' + (y + s * 0.6) + '" stroke="#1d2a3a" stroke-width="2.4" fill="none" stroke-linecap="round"/></g>';
    if (part < 1) g += '<circle cx="' + (x + s / 2) + '" cy="' + (y + s / 2) + '" r="' + (s / 2 - 1.5) + '" fill="none" stroke="#b7791f" stroke-width="1.4" stroke-dasharray="3 3"/>';
    return g;
  }
  function tally(x, y, n) {
    var s = '', g, k, gx = x;
    for (g = 0; g < Math.ceil(n / 5); g++) {
      var c = Math.min(5, n - g * 5);
      for (k = 0; k < Math.min(4, c); k++) s += '<line x1="' + (gx + k * 9) + '" y1="' + y + '" x2="' + (gx + k * 9) + '" y2="' + (y + 30) + '" stroke="#1d2a3a" stroke-width="3.2" stroke-linecap="round"/>';
      if (c === 5) s += '<line x1="' + (gx - 5) + '" y1="' + (y + 25) + '" x2="' + (gx + 32) + '" y2="' + (y + 5) + '" stroke="#d63c7a" stroke-width="3.2" stroke-linecap="round"/>';
      gx += 50;
    }
    return s;
  }
  /* cfg: { cats:[names], colors, counts:[…], max, steps:[1] or [1,5], views:['tally','pic','bar'], keys:[1,2,5,10], scales:[1,2,5,10], title, question } */
  K.graphTool = function (cfg) {
    var st, n = cfg.cats.length, COL = cfg.colors || ['#e5484d', '#f08c1a', '#1fa565', '#1f78c8', '#8a4fd6'];
    function reset() { st = { c: cfg.counts.slice(), view: cfg.views[0], key: cfg.key0 || cfg.keys[0], scale: cfg.scale0 || cfg.scales[0], seen: {} }; st.seen[st.view] = 1; draw(); }
    var ws = T.$('grTool');
    ws.innerHTML = '<div class="tl-controls el-view" role="group" aria-label="Choose a display">' + cfg.views.map(function (v) { return '<button type="button" class="tl-btn" data-view="' + v + '">' + { tally: 'Tally chart', pic: 'Picture graph', bar: 'Bar graph', table: 'Table' }[v] + '</button>'; }).join('') +
      (cfg.keys.length > 1 ? '<div class="tl-field el-inline"><label for="grKey">Picture key: each face =</label><select id="grKey">' + cfg.keys.map(function (k) { return '<option value="' + k + '">' + k + '</option>'; }).join('') + '</select></div>' : '') +
      (cfg.scales.length > 1 ? '<div class="tl-field el-inline"><label for="grScale">Bar scale: count by</label><select id="grScale">' + cfg.scales.map(function (k) { return '<option value="' + k + '">' + k + 's</option>'; }).join('') + '</select></div>' : '') + '</div>' +
      '<div class="tl-model" id="grModel"></div><div class="tl-controls" id="grCtl">' + cfg.cats.map(function (c, i) { return K.step(i, c, cfg.steps); }).join('') + '</div><div class="tl-out" id="grOut" aria-live="polite"></div>';
    function chart() {
      var W = 760, rowH = 62, top = 46, H = top + n * rowH + (st.view === 'bar' ? 70 : 30), s = K.txt(W / 2, 28, cfg.title, { size: 22 }), i;
      var maxC = cfg.max, left = 150;
      if (st.view === 'bar') {
        var sc = st.scale, axisMax = Math.ceil(maxC / sc) * sc, unit = (W - left - 40) / axisMax;
        for (var v = 0; v <= axisMax; v += sc) { var x = left + v * unit; s += '<line x1="' + x + '" y1="' + top + '" x2="' + x + '" y2="' + (top + n * rowH) + '" stroke="#cfe8da" stroke-width="2"/>' + K.txt(x, top + n * rowH + 26, v, { size: 16, w: 700 }); }
        s += K.txt(left + (W - left - 40) / 2, top + n * rowH + 56, 'Number of votes', { size: 16, w: 700, fill: '#55657a' });
        for (i = 0; i < n; i++) {
          var y = top + i * rowH + 12;
          s += K.txt(left - 12, y + 27, cfg.cats[i], { a: 'end', size: 19 }) + '<rect x="' + left + '" y="' + y + '" width="' + (st.c[i] * unit) + '" height="38" rx="4" fill="' + COL[i] + '" stroke="#1d2a3a" stroke-width="1.5"/>';
          if (st.c[i] % sc) s += '<line x1="' + (left + st.c[i] * unit) + '" y1="' + (y - 4) + '" x2="' + (left + st.c[i] * unit) + '" y2="' + (y + 42) + '" stroke="#1d2a3a" stroke-width="2" stroke-dasharray="4 3"/>';
        }
        s += '<line x1="' + left + '" y1="' + top + '" x2="' + left + '" y2="' + (top + n * rowH) + '" stroke="#1d2a3a" stroke-width="3"/>';
      } else {
        for (i = 0; i < n; i++) {
          var yy = top + i * rowH;
          s += '<rect x="10" y="' + yy + '" width="' + (W - 20) + '" height="' + rowH + '" fill="' + (i % 2 ? '#f7fbf8' : '#fff') + '" stroke="#cfe8da"/>' + K.txt(left - 12, yy + 39, cfg.cats[i], { a: 'end', size: 19 });
          if (st.view === 'tally') s += tally(left + 14, yy + 16, st.c[i]);
          if (st.view === 'table') s += K.txt(left + 60, yy + 40, st.c[i], { size: 26 });
          if (st.view === 'pic') {
            var k = st.key, full = Math.floor(st.c[i] / k), rem = st.c[i] % k, sz = Math.min(44, (W - left - 40) / Math.max(10, Math.ceil(Math.max.apply(null, st.c) / k)) - 4);
            for (var j = 0; j < full; j++) s += face(left + 10 + j * (sz + 4), yy + (rowH - sz) / 2, sz, 1);
            if (rem) s += face(left + 10 + full * (sz + 4), yy + (rowH - sz) / 2, sz, rem / k);
          }
        }
        s += '<line x1="' + left + '" y1="' + top + '" x2="' + left + '" y2="' + (top + n * rowH) + '" stroke="#1d2a3a" stroke-width="2"/>';
        if (st.view === 'pic') s += face(W - 250, top + n * rowH + 2, 26, 1) + K.txt(W - 216, top + n * rowH + 22, 'Key: each face = ' + st.key + ' vote' + (st.key > 1 ? 's' : ''), { a: 'start', size: 17 });
      }
      return K.svg(W, H, s, cfg.title + ': ' + cfg.cats.map(function (c, i) { return c + ' ' + st.c[i]; }).join(', '));
    }
    function draw() {
      T.$('grModel').innerHTML = chart();
      cfg.cats.forEach(function (c, i) { T.$('v-' + i).textContent = st.c[i]; });
      Array.prototype.forEach.call(ws.querySelectorAll('[data-view]'), function (b) { b.setAttribute('aria-pressed', b.dataset.view === st.view); });
      if (T.$('grKey')) T.$('grKey').value = st.key; if (T.$('grScale')) T.$('grScale').value = st.scale;
      var tot = st.c.reduce(function (a, b) { return a + b; }, 0), mx = Math.max.apply(null, st.c), mn = Math.min.apply(null, st.c);
      var most = cfg.cats.filter(function (c, i) { return st.c[i] === mx; }), few = cfg.cats.filter(function (c, i) { return st.c[i] === mn; });
      var note = '';
      if (st.view === 'pic' && st.key > 1) { var odd = cfg.cats.filter(function (c, i) { return st.c[i] % st.key; }); if (odd.length) note = '<br><b>Part of a face:</b> ' + odd.join(', ') + (odd.length > 1 ? ' do' : ' does') + ' not fill a whole face. A part of a face stands for less than ' + st.key + ' votes.'; }
      T.$('grOut').innerHTML = '<b>Total votes:</b> ' + tot + ' · <b>Most:</b> ' + most.join(' and ') + ' (' + mx + ') · <b>Fewest:</b> ' + few.join(' and ') + ' (' + mn + ')<br><b>' + most[0] + '</b> has <b>' + (mx - mn) + '</b> more vote' + (mx - mn === 1 ? '' : 's') + ' than <b>' + few[few.length - 1] + '</b>.' + note;
      T.update({ c: st.c.slice(), view: st.view, key: st.key, scale: st.scale, seen: Object.assign({}, st.seen), total: tot, max: mx, min: mn, cats: cfg.cats });
    }
    T.init({ course: cfg.course, courseName: cfg.courseName, unit: cfg.unit, title: cfg.toolTitle, standards: cfg.standards, teacher: cfg.teacher, notice: cfg.notice, challenges: cfg.challenges, reset: reset, printables: true });
    T.steppers(T.$('grCtl'), function (k, d) { st.c[+k] = K.clamp(st.c[+k] + d, 0, cfg.max); draw(); });
    Array.prototype.forEach.call(ws.querySelectorAll('[data-view]'), function (b) { b.onclick = function () { st.view = b.dataset.view; st.seen[st.view] = 1; draw(); }; });
    if (T.$('grKey')) T.$('grKey').onchange = function () { st.key = +this.value; draw(); };
    if (T.$('grScale')) T.$('grScale').onchange = function () { st.scale = +this.value; draw(); };
    reset();
  };

  /* ---------------------------------------------------------------- equal shares */
  var UNEQUAL = { 2: [0.68, 0.32], 3: [0.5, 0.3, 0.2], 4: [0.4, 0.1, 0.35, 0.15] };
  function sharePaths(shape, parts, equal) {
    var P = [], i, cx = 190, cy = 160, r = 140;
    var w = equal ? null : UNEQUAL[parts];
    if (shape === 'circle') {
      var a0 = -Math.PI / 2;
      for (i = 0; i < parts; i++) {
        var fr = equal ? 1 / parts : w[i], a1 = a0 + fr * 2 * Math.PI;
        P.push(parts === 1 ? 'M' + (cx - r) + ' ' + cy + ' a' + r + ' ' + r + ' 0 1 0 ' + 2 * r + ' 0 a' + r + ' ' + r + ' 0 1 0 ' + (-2 * r) + ' 0z' :
          'M' + cx + ' ' + cy + ' L' + (cx + r * Math.cos(a0)).toFixed(2) + ' ' + (cy + r * Math.sin(a0)).toFixed(2) + ' A' + r + ' ' + r + ' 0 ' + (fr > 0.5 ? 1 : 0) + ' 1 ' + (cx + r * Math.cos(a1)).toFixed(2) + ' ' + (cy + r * Math.sin(a1)).toFixed(2) + 'Z');
        a0 = a1;
      }
      return P;
    }
    var W = shape === 'square' ? 280 : 360, H = 280, x0 = 190 - W / 2, y0 = 20;
    if (shape === 'square' && parts === 4 && equal) { [[0, 0], [1, 0], [0, 1], [1, 1]].forEach(function (q) { P.push('M' + (x0 + q[0] * W / 2) + ' ' + (y0 + q[1] * H / 2) + ' h' + W / 2 + ' v' + H / 2 + ' h' + (-W / 2) + 'z'); }); return P; }
    var x = x0;
    for (i = 0; i < parts; i++) { var ww = (equal ? 1 / parts : w[i]) * W; P.push('M' + x.toFixed(2) + ' ' + y0 + ' h' + ww.toFixed(2) + ' v' + H + ' h' + (-ww).toFixed(2) + 'z'); x += ww; }
    return P;
  }
  var NAMEP = { 1: ['whole', 'whole'], 2: ['half', 'halves'], 3: ['third', 'thirds'], 4: ['fourth', 'fourths'] };
  /* cfg: { parts:[2,4] or [2,3,4], grid:bool, shapes:[…] } */
  K.sharesTool = function (cfg) {
    var st;
    function reset() { st = { mode: 'shares', shape: 'circle', parts: 2, equal: true, shade: [], rows: 2, cols: 3, seen: {}, grids: {} }; mark(); draw(); }
    function mark() { st.seen[st.shape + st.parts + (st.equal ? 'e' : 'u')] = 1; if (st.mode === 'grid') st.grids[st.rows + 'x' + st.cols] = 1; }
    var ws = T.$('shTool');
    ws.innerHTML = (cfg.grid ? '<div class="tl-controls el-view" role="group" aria-label="Choose an activity"><button type="button" class="tl-btn" data-mode="shares">Equal shares</button><button type="button" class="tl-btn" data-mode="grid">Rows and columns of squares</button></div>' : '') +
      '<div class="tl-model" id="shModel"></div><div class="tl-controls" id="shCtl"></div><div class="tl-out" id="shOut" aria-live="polite"></div>';
    function controls() {
      var c = T.$('shCtl');
      if (st.mode === 'grid') { c.innerHTML = K.step('rows', 'Rows', [1], st.rows) + K.step('cols', 'Columns', [1], st.cols); return; }
      c.innerHTML = '<div class="tl-field"><span class="lab">Shape</span><div class="tl-step">' + cfg.shapes.map(function (s) { return '<button type="button" class="tl-btn" data-shape="' + s + '" aria-pressed="' + (st.shape === s) + '">' + s.charAt(0).toUpperCase() + s.slice(1) + '</button>'; }).join('') + '</div></div>' +
        '<div class="tl-field"><span class="lab">Split into</span><div class="tl-step">' + cfg.parts.map(function (p) { return '<button type="button" class="tl-btn" data-parts="' + p + '" aria-pressed="' + (st.parts === p) + '">' + p + ' parts</button>'; }).join('') + '</div></div>' +
        '<div class="tl-field"><span class="lab">Cut</span><div class="tl-step"><button type="button" class="tl-btn" data-eq="1" aria-pressed="' + st.equal + '">Equal parts</button><button type="button" class="tl-btn" data-eq="0" aria-pressed="' + !st.equal + '">Not equal parts</button></div></div>' +
        '<div class="tl-field"><span class="lab">Color</span><div class="tl-step"><button type="button" class="tl-btn" id="shAll">Color all</button><button type="button" class="tl-btn" id="shNone">Clear</button></div></div>';
    }
    function draw() {
      if (cfg.grid) Array.prototype.forEach.call(ws.querySelectorAll('[data-mode]'), function (b) { b.setAttribute('aria-pressed', b.dataset.mode === st.mode); });
      controls();
      var out = T.$('shOut'), s = '';
      if (st.mode === 'grid') {
        var cell = Math.min(300 / st.rows, 360 / st.cols), x0 = 190 - cell * st.cols / 2, y0 = 170 - cell * st.rows / 2;
        for (var r = 0; r < st.rows; r++) for (var c = 0; c < st.cols; c++) s += '<rect x="' + (x0 + c * cell) + '" y="' + (y0 + r * cell) + '" width="' + cell + '" height="' + cell + '" fill="' + ((r + c) % 2 ? '#bfe6d0' : '#e3f6ea') + '" stroke="#0d6b3c" stroke-width="2.5"/>';
        T.$('shModel').innerHTML = K.svg(380, 340, s, st.rows + ' rows and ' + st.cols + ' columns of squares');
        var add = []; for (var k = 0; k < st.rows; k++) add.push(st.cols);
        out.innerHTML = '<b>' + st.rows + '</b> row' + (st.rows > 1 ? 's' : '') + ' of <b>' + st.cols + '</b> square' + (st.cols > 1 ? 's' : '') + ' = <b>' + st.rows * st.cols + '</b> same-size squares.<br>Count by rows: ' + add.join(' + ') + ' = ' + st.rows * st.cols;
      } else {
        var P = sharePaths(st.shape, st.parts, st.equal);
        P.forEach(function (d, i) { s += '<path d="' + d + '" class="el-part" data-i="' + i + '" tabindex="0" role="button" aria-pressed="' + !!st.shade[i] + '" aria-label="Part ' + (i + 1) + (st.shade[i] ? ', colored' : '') + '" fill="' + (st.shade[i] ? '#f08c1a' : '#fff') + '" stroke="#1d2a3a" stroke-width="4" stroke-linejoin="round"/>'; });
        T.$('shModel').innerHTML = K.svg(380, 320, s, st.shape + ' cut into ' + st.parts + (st.equal ? ' equal' : ' unequal') + ' parts');
        var nShade = st.shade.filter(Boolean).length, nm = NAMEP[st.parts];
        if (st.equal) out.innerHTML = 'The ' + st.shape + ' is cut into <b>' + st.parts + ' equal shares</b>: ' + nm[1] + '. Each share is <b>one ' + nm[0] + '</b>.<br>' +
          (nShade === 0 ? 'Tap a share to color it.' : nShade === st.parts ? 'All ' + st.parts + ' ' + nm[1] + ' are colored: that is <b>one whole</b>.' : 'Colored: <b>' + (nShade === 1 ? 'one ' + nm[0] : K.words(nShade) + ' ' + nm[1]) + '</b>' + (cfg.fracs ? ' = ' + T.frac(nShade, st.parts) : '') + ' of the ' + st.shape + '.');
        else out.innerHTML = 'These <b>' + st.parts + ' parts are not the same size</b>, so they are <b>not</b> ' + nm[1] + '. Equal shares must all be the same size.' + (nShade ? '<br>A colored part here is not one ' + nm[0] + '.' : '');
      }
      T.update({ mode: st.mode, shape: st.shape, parts: st.parts, equal: st.equal, shaded: st.shade.filter(Boolean).length, rows: st.rows, cols: st.cols, seen: Object.assign({}, st.seen), grids: Object.assign({}, st.grids) });
    }
    T.init({ course: cfg.course, courseName: cfg.courseName, unit: cfg.unit, title: cfg.toolTitle, standards: cfg.standards, teacher: cfg.teacher, notice: cfg.notice, challenges: cfg.challenges, reset: reset, printables: true });
    function toggle(i) { st.shade[i] = !st.shade[i]; draw(); var p = ws.querySelector('.el-part[data-i="' + i + '"]'); if (p) p.focus(); }
    ws.addEventListener('click', function (e) {
      var t = e.target.closest('[data-shape],[data-parts],[data-eq],[data-mode],#shAll,#shNone,.el-part'); if (!t) return;
      if (t.dataset.mode) { st.mode = t.dataset.mode; }
      else if (t.dataset.shape) { st.shape = t.dataset.shape; st.shade = []; }
      else if (t.dataset.parts) { st.parts = +t.dataset.parts; st.shade = []; }
      else if (t.dataset.eq) { st.equal = t.dataset.eq === '1'; st.shade = []; }
      else if (t.id === 'shAll') { st.shade = []; for (var i = 0; i < st.parts; i++) st.shade[i] = true; }
      else if (t.id === 'shNone') st.shade = [];
      else if (t.classList.contains('el-part')) return toggle(+t.dataset.i);
      mark(); draw();
    });
    ws.addEventListener('keydown', function (e) { var t = e.target; if (t.classList && t.classList.contains('el-part') && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); toggle(+t.dataset.i); } });
    T.steppers(T.$('shCtl'), function (k, d) { st[k] = K.clamp(st[k] + d, 1, 6); mark(); draw(); });
    reset();
  };
  G.ELK = K;
})(window);
