/* Mr. K's Classroom: shared helpers for the Interactive Math tools.
   Lab.layout() builds the page frame; Lab.graph() draws an SVG coordinate plane; Lab.slider(), Lab.chips(),
   Lab.tabs() make controls; Lab.challenges() is the "Try this" list that checks itself as students explore. */
(function (G) {
'use strict';
var SVGNS = 'http://www.w3.org/2000/svg';
function h(tag, attrs, parent, html) {
  var e = document.createElement(tag);
  if (attrs) Object.keys(attrs).forEach(function (k) { if (attrs[k] != null) e.setAttribute(k, attrs[k]); });
  if (html != null) e.innerHTML = html;
  if (parent) parent.appendChild(e);
  return e;
}
function s(tag, attrs, parent) {
  var e = document.createElementNS(SVGNS, tag);
  if (attrs) Object.keys(attrs).forEach(function (k) { if (attrs[k] != null) e.setAttribute(k, attrs[k]); });
  if (parent) parent.appendChild(e);
  return e;
}
function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

/* ---------- numbers ---------- */
function round(x, dp) { var p = Math.pow(10, dp == null ? 2 : dp); var r = Math.round(x * p) / p; return Object.is(r, -0) ? 0 : r; }
function num(x, dp) { if (!isFinite(x)) return x > 0 ? '∞' : x < 0 ? '−∞' : '—'; return String(round(x, dp)).replace('-', '−'); }
function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = b; b = a % b; a = t; } return a || 1; }
/* Closest fraction with a small denominator, or null if x isn't close to one. */
function toFrac(x, maxDen) {
  maxDen = maxDen || 12;
  for (var d = 1; d <= maxDen; d++) { var n = Math.round(x * d); if (Math.abs(n / d - x) < 1e-9) { var g = gcd(n, d); return [n / g, d / g]; } }
  return null;
}
/* Stacked fraction HTML (division is always shown stacked, never with a slash). */
function frac(n, d, opts) {
  if (typeof n === 'number' && typeof d === 'number') {
    if (d < 0) { n = -n; d = -d; }
    var g = gcd(n, d); n /= g; d /= g;
    if (d === 1) return num(n);
    var neg = n < 0;
    return (neg ? '−' : '') + '<span class="fr"><span class="fn">' + Math.abs(n) + '</span><span class="fd">' + d + '</span></span>';
  }
  return '<span class="fr"><span class="fn">' + n + '</span><span class="fd">' + d + '</span></span>';
}
/* A number as a stacked fraction when it is a simple fraction, otherwise a rounded decimal. */
function nice(x, maxDen, dp) {
  if (!isFinite(x)) return num(x);
  var f = toFrac(x, maxDen || 12);
  return f ? frac(f[0], f[1]) : num(x, dp);
}
/* Polynomial-style terms: [[coef, 'x²'], [coef, 'x'], [coef, '']] -> "3x² − x + 4". Zero terms are skipped. */
function terms(list, opts) {
  opts = opts || {};
  var out = '';
  list.forEach(function (t) {
    var c = t[0], v = t[1] || '';
    if (Math.abs(c) < 1e-12) return;
    var first = out === '';
    var sign = c < 0 ? (first ? '−' : ' − ') : (first ? '' : ' + ');
    var a = Math.abs(c), body;
    var cs = opts.frac === false ? num(a, opts.dp) : nice(a, 12, opts.dp);
    if (v && a === 1) body = '';
    else body = cs;
    out += sign + body + (v ? '<span class="v">' + v.charAt(0) + '</span>' + v.slice(1) : '');
  });
  return out || '0';
}
function V(name) { return '<span class="v">' + name + '</span>'; }
/* "(x − 3)" style binomial for a shift h: x - h. */
function shift(vname, hval) {
  if (Math.abs(hval) < 1e-12) return V(vname);
  return '(' + V(vname) + (hval > 0 ? ' − ' : ' + ') + nice(Math.abs(hval)) + ')';
}

/* ---------- page frame ---------- */
function layout(o) {
  document.title = o.title + ' · Mr. K\'s Classroom';
  var root = document.getElementById('app') || h('main', { id: 'app' }, document.body);
  root.className = 'lab-page';
  var head = h('header', { class: 'lab-head' }, root);
  var t = h('div', null, head);
  h('p', { class: 'lab-eyebrow' }, t, esc(o.course + ' · ' + o.unit));
  h('h1', { class: 'lab-title' }, t, esc(o.title));
  if (o.intro) h('p', { class: 'lab-intro' }, t, o.intro);
  var grid = h('div', { class: 'lab-grid' }, root);
  var stage = h('section', { class: 'box stage', 'aria-label': 'Interactive display' }, grid);
  var panel = h('section', { class: 'box panel', 'aria-label': 'Controls' }, grid);
  var below = h('div', { style: 'display:grid;gap:16px' }, root);
  h('p', { class: 'note' }, below, '<span aria-hidden="true">✎</span><span><b>Worksheet:</b> keep your printed Explore &amp; Reflect worksheet next to you. Record what you see, then write the rule in your own words.</span>');
  return { root: root, stage: stage, panel: panel, below: below };
}

/* ---------- controls ---------- */
function slider(parent, o) {
  var id = 'sl-' + o.id;
  var wrap = h('div', { class: 'slider' }, parent);
  if (o.color) wrap.style.setProperty('--c', 'var(--' + o.color + ')');
  var top = h('div', { class: 'slider-top' }, wrap);
  h('label', { for: id }, top, o.label);
  var out = h('output', { for: id }, top);
  if (o.color) out.className = 'c-' + o.color;
  var row = h('div', { class: 'slider-row' }, wrap);
  var minus = h('button', { class: 'nudge', type: 'button', 'aria-label': 'Decrease ' + o.id }, row, '−');
  var input = h('input', { type: 'range', id: id, min: o.min, max: o.max, step: o.step || 1, value: o.value }, row);
  var plus = h('button', { class: 'nudge', type: 'button', 'aria-label': 'Increase ' + o.id }, row, '+');
  var fmt = o.format || function (v) { return nice(v); };
  function val() { return round(parseFloat(input.value), 6); }
  function show() { out.innerHTML = fmt(val()); }
  function fire() { show(); o.onInput && o.onInput(val()); }
  input.addEventListener('input', fire);
  function nudge(dir) { var st = parseFloat(o.step || 1); var v = round(val() + dir * st, 6); v = Math.max(o.min, Math.min(o.max, v)); input.value = v; fire(); }
  minus.addEventListener('click', function () { nudge(-1); });
  plus.addEventListener('click', function () { nudge(1); });
  show();
  return { el: wrap, input: input, get: val, set: function (v, silent) { input.value = v; show(); if (!silent && o.onInput) o.onInput(val()); } };
}
function chips(parent, o) {
  var wrap = h('div', { class: 'slider' }, parent);
  if (o.label) h('span', { style: 'font-weight:700' }, wrap, o.label);
  var row = h('div', { class: 'chips', role: 'group', 'aria-label': o.label || 'Options' }, wrap);
  var value = o.value, btns = [];
  o.options.forEach(function (opt) {
    var b = h('button', { class: 'chip', type: 'button', 'aria-pressed': String(opt.value === value) }, row, opt.label);
    b.addEventListener('click', function () { set(opt.value); });
    btns.push([opt.value, b]);
  });
  function set(v, silent) { value = v; btns.forEach(function (x) { x[1].setAttribute('aria-pressed', String(x[0] === v)); }); if (!silent && o.onChange) o.onChange(v); }
  return { el: wrap, get: function () { return value; }, set: set };
}
function tabs(parent, list, onChange) {
  var row = h('div', { class: 'tabs', role: 'tablist' }, parent);
  var cur = list[0].id, btns = {};
  list.forEach(function (t) {
    var b = h('button', { class: 'tab', role: 'tab', type: 'button', 'aria-selected': String(t.id === cur) }, row, esc(t.label));
    b.addEventListener('click', function () { set(t.id); });
    btns[t.id] = b;
  });
  function set(id) { cur = id; Object.keys(btns).forEach(function (k) { btns[k].setAttribute('aria-selected', String(k === id)); }); onChange && onChange(id); }
  return { get: function () { return cur; }, set: set };
}
function button(parent, label, onClick, ghost) {
  var b = h('button', { class: 'btn' + (ghost ? ' ghost' : ''), type: 'button' }, parent, label);
  b.addEventListener('click', onClick);
  return b;
}
function table(parent) {
  var wrap = h('div', { class: 'table-wrap' }, parent);
  var t = h('table', { class: 'lab-table' }, wrap);
  return { el: wrap, set: function (head, rows) {
    t.innerHTML = '<thead><tr>' + head.map(function (x) { return '<th scope="col">' + x + '</th>'; }).join('') + '</tr></thead><tbody>' +
      rows.map(function (r) { return '<tr>' + r.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody>';
  } };
}
/* "Try this" list. Each item {text, check}. Items stay checked once found. */
function challenges(parent, list, title) {
  var box = h('div', { class: 'challenges' }, parent);
  var head = h('div', { class: 'challenges-head' }, box);
  h('h2', null, head, title || 'Try this');
  var count = h('span', { 'aria-live': 'polite' }, head);
  var ol = h('ol', null, box);
  var items = list.map(function (c, i) {
    var li = h('li', null, ol, '<span class="mark" aria-hidden="true">' + (i + 1) + '</span><span>' + c.text + '</span>');
    return { c: c, li: li, done: false };
  });
  function update() {
    var n = 0;
    items.forEach(function (it, i) {
      var ok = false; try { ok = !!it.c.check(); } catch (e) { ok = false; }
      if (ok && !it.done) { it.done = true; it.li.classList.add('done', 'pop'); it.li.querySelector('.mark').textContent = '✓'; setTimeout(function () { it.li.classList.remove('pop'); }, 600); }
      if (it.done) n++;
    });
    count.textContent = n + ' of ' + items.length + ' found';
  }
  update();
  return { update: update };
}

/* ---------- coordinate plane ---------- */
function graph(parent, o) {
  o = o || {};
  var W = o.width || 640, H = o.height || 520, pad = 6;
  var svg = s('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': o.label || 'Coordinate plane' }, parent);
  var gGrid = s('g', null, svg), gShade = s('g', null, svg), gDyn = s('g', null, svg), gTop = s('g', null, svg);
  var v = { xmin: o.xmin == null ? -10 : o.xmin, xmax: o.xmax == null ? 10 : o.xmax, ymin: o.ymin == null ? -10 : o.ymin, ymax: o.ymax == null ? 10 : o.ymax };
  function X(x) { return pad + (x - v.xmin) / (v.xmax - v.xmin) * (W - 2 * pad); }
  function Y(y) { return H - pad - (y - v.ymin) / (v.ymax - v.ymin) * (H - 2 * pad); }
  function ix(px) { return v.xmin + (px - pad) / (W - 2 * pad) * (v.xmax - v.xmin); }
  function iy(py) { return v.ymin + (H - pad - py) / (H - 2 * pad) * (v.ymax - v.ymin); }
  function niceStep(span) { var raw = span / 10, p = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p; return (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10) * p; }
  function drawGrid() {
    gGrid.innerHTML = '';
    if (o.noGrid) return;
    var xs = o.xstep || niceStep(v.xmax - v.xmin), ys = o.ystep || niceStep(v.ymax - v.ymin);
    var xl = o.xlabelStep || xs, yl = o.ylabelStep || ys;
    for (var x = Math.ceil(v.xmin / xs) * xs; x <= v.xmax + 1e-9; x += xs) s('line', { x1: X(x), x2: X(x), y1: Y(v.ymin), y2: Y(v.ymax), class: 'g-grid' }, gGrid);
    for (var y = Math.ceil(v.ymin / ys) * ys; y <= v.ymax + 1e-9; y += ys) s('line', { y1: Y(y), y2: Y(y), x1: X(v.xmin), x2: X(v.xmax), class: 'g-grid' }, gGrid);
    var ax = Math.min(Math.max(0, v.ymin), v.ymax), ay = Math.min(Math.max(0, v.xmin), v.xmax);
    if (!o.noXAxis) s('line', { x1: X(v.xmin), x2: X(v.xmax), y1: Y(ax), y2: Y(ax), class: 'g-axis' }, gGrid);
    if (!o.noYAxis) s('line', { y1: Y(v.ymin), y2: Y(v.ymax), x1: X(ay), x2: X(ay), class: 'g-axis' }, gGrid);
    if (o.noLabels) return;
    var fx = o.xfmt || function (t) { return num(t, 4); }, fy = o.yfmt || function (t) { return num(t, 4); };
    if (o.xticks) {
      o.xticks.forEach(function (tk) {
        if (tk.x < v.xmin || tk.x > v.xmax || X(tk.x) < 14 || X(tk.x) > W - 14) return;
        var by = Math.min(H - 30, Y(ax) + 16);
        s('line', { x1: X(tk.x), x2: X(tk.x), y1: Y(ax) - 5, y2: Y(ax) + 5, class: 'g-axis' }, gGrid);
        if (!tk.den) { var t0 = s('text', { x: X(tk.x), y: by + 4, 'text-anchor': 'middle', class: 'g-tick' }, gGrid); t0.textContent = tk.num; return; }
        var t1 = s('text', { x: X(tk.x), y: by, 'text-anchor': 'middle', class: 'g-tick' }, gGrid); t1.textContent = tk.num;
        s('line', { x1: X(tk.x) - 9, x2: X(tk.x) + 9, y1: by + 4, y2: by + 4, stroke: 'var(--ink-soft)', 'stroke-width': 1.2 }, gGrid);
        var t2 = s('text', { x: X(tk.x), y: by + 17, 'text-anchor': 'middle', class: 'g-tick' }, gGrid); t2.textContent = tk.den;
      });
    } else for (x = Math.ceil(v.xmin / xl) * xl; x <= v.xmax + 1e-9; x += xl) {
      if (Math.abs(x) < 1e-9 && !o.noYAxis) continue;
      if (X(x) < 14 || X(x) > W - 14) continue;
      var t = s('text', { x: X(x), y: Math.min(H - 6, Y(ax) + 17), 'text-anchor': 'middle', class: 'g-tick' }, gGrid); t.textContent = fx(round(x, 6));
    }
    for (y = Math.ceil(v.ymin / yl) * yl; y <= v.ymax + 1e-9; y += yl) {
      if (Math.abs(y) < 1e-9 && !o.noXAxis) continue;
      if (Y(y) < 12 || Y(y) > H - 10) continue;
      var tx = Math.max(4, X(ay) - 6);
      t = s('text', { x: tx, y: Y(y) + 4, 'text-anchor': X(ay) - 6 < 20 ? 'start' : 'end', class: 'g-tick' }, gGrid); t.textContent = fy(round(y, 6));
    }
  }
  drawGrid();
  function col(c) { return c && c.indexOf('#') !== 0 && c.indexOf('var(') !== 0 && c !== 'none' ? 'var(--' + c + ')' : c; }
  var refocus = null;
  var api = {
    svg: svg, W: W, H: H, X: X, Y: Y, ix: ix, iy: iy, view: v, layer: gDyn, top: gTop, shadeLayer: gShade,
    setView: function (nv) { Object.assign(v, nv); drawGrid(); },
    clear: function () { var a = document.activeElement; refocus = a && svg.contains(a) ? a.getAttribute('aria-label') : null; gDyn.innerHTML = ''; gShade.innerHTML = ''; gTop.innerHTML = ''; },
    /* Plot y = f(x). Breaks the curve where it jumps (vertical asymptotes) or is undefined. */
    fn: function (f, p) {
      p = p || {};
      var a = p.from == null ? v.xmin : Math.max(v.xmin, p.from), b = p.to == null ? v.xmax : Math.min(v.xmax, p.to);
      var n = p.samples || 600, d = '', pen = false, prev = null, span = v.ymax - v.ymin;
      for (var i = 0; i <= n; i++) {
        var x = a + (b - a) * i / n, y;
        try { y = f(x); } catch (e) { y = NaN; }
        var ok = isFinite(y) && Math.abs(y - (v.ymin + v.ymax) / 2) < span * 20;
        if (ok && prev !== null && Math.abs(y - prev) > span * 1.5) pen = false;
        if (ok) { var py = Math.max(-H * 4, Math.min(H * 5, Y(y))); d += (pen ? 'L' : 'M') + X(x).toFixed(2) + ' ' + py.toFixed(2); pen = true; prev = y; }
        else { pen = false; prev = null; }
      }
      return s('path', { d: d, fill: 'none', stroke: col(p.color || 'blue'), 'stroke-width': p.width || 4, 'stroke-dasharray': p.dash || null, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', opacity: p.opacity || null }, p.layer || gDyn);
    },
    /* Parametric curve (x(t), y(t)). */
    param: function (fx, fy, t0, t1, p) {
      p = p || {}; var n = p.samples || 400, d = '';
      for (var i = 0; i <= n; i++) { var t = t0 + (t1 - t0) * i / n, x = fx(t), y = fy(t); if (!isFinite(x) || !isFinite(y)) continue; d += (d ? 'L' : 'M') + X(x).toFixed(2) + ' ' + Y(y).toFixed(2); }
      return s('path', { d: d, fill: p.fill ? col(p.fill) : 'none', 'fill-opacity': p.fillOpacity || null, stroke: col(p.color || 'blue'), 'stroke-width': p.width || 4, 'stroke-dasharray': p.dash || null, 'stroke-linejoin': 'round' }, p.layer || gDyn);
    },
    line: function (x1, y1, x2, y2, p) {
      p = p || {};
      return s('line', { x1: X(x1), y1: Y(y1), x2: X(x2), y2: Y(y2), stroke: col(p.color || 'ink'), 'stroke-width': p.width || 3, 'stroke-dasharray': p.dash || null, 'stroke-linecap': 'round', opacity: p.opacity || null }, p.layer || gDyn);
    },
    /* Infinite line through two points, clipped to the view. */
    fullLine: function (x1, y1, x2, y2, p) {
      if (Math.abs(x2 - x1) < 1e-12) return api.line(x1, v.ymin - 1, x1, v.ymax + 1, p);
      var m = (y2 - y1) / (x2 - x1);
      return api.line(v.xmin - 1, y1 + m * (v.xmin - 1 - x1), v.xmax + 1, y1 + m * (v.xmax + 1 - x1), p);
    },
    poly: function (pts, p) {
      p = p || {};
      return s('polygon', { points: pts.map(function (q) { return X(q[0]).toFixed(2) + ',' + Y(q[1]).toFixed(2); }).join(' '), fill: col(p.fill || 'blue'), 'fill-opacity': p.opacity == null ? 0.2 : p.opacity, stroke: p.stroke ? col(p.stroke) : 'none', 'stroke-width': p.width || 2 }, p.layer || gShade);
    },
    rect: function (x, y, w, hgt, p) { /* data units: (x,y) is the lower-left corner */
      p = p || {};
      return s('rect', { x: X(x), y: Y(y + hgt), width: Math.abs(X(x + w) - X(x)), height: Math.abs(Y(y) - Y(y + hgt)), fill: col(p.fill || 'blue'), 'fill-opacity': p.opacity == null ? 1 : p.opacity, stroke: p.stroke ? col(p.stroke) : 'none', 'stroke-width': p.width || 2, rx: p.rx || 0 }, p.layer || gDyn);
    },
    dot: function (x, y, p) {
      p = p || {};
      return s('circle', { cx: X(x), cy: Y(y), r: p.r || 7, fill: p.open ? 'var(--card)' : col(p.color || 'ink'), stroke: col(p.stroke || p.color || 'ink'), 'stroke-width': p.open ? 3 : (p.strokeWidth || 0) }, p.layer || gTop);
    },
    text: function (x, y, str, p) {
      p = p || {};
      var t = s('text', { x: X(x) + (p.dx || 0), y: Y(y) + (p.dy || 0), 'text-anchor': p.anchor || 'start', class: 'g-label', fill: p.color ? col(p.color) : null, 'font-size': p.size || null, 'font-weight': p.weight || null, 'paint-order': 'stroke', stroke: 'var(--card)', 'stroke-width': p.halo === false ? 0 : 5, 'stroke-linejoin': 'round' }, p.layer || gTop);
      t.textContent = str; return t;
    },
    /* Draggable handle. onDrag(x, y) receives data coordinates (already snapped if snap is set). */
    handle: function (x, y, p) {
      p = p || {};
      var c = s('circle', { cx: X(x), cy: Y(y), r: p.r || 11, fill: col(p.color || 'orange'), stroke: 'var(--ink)', 'stroke-width': 3, class: 'g-handle', tabindex: 0, role: 'slider', 'aria-label': p.label || 'Draggable point' }, gTop);
      var hit = s('circle', { cx: X(x), cy: Y(y), r: 26, fill: 'transparent', class: 'g-handle' }, gTop);
      function at(ev) {
        var pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
        var q = pt.matrixTransform(svg.getScreenCTM().inverse());
        var dx = ix(q.x), dy = iy(q.y);
        if (p.snap) { dx = Math.round(dx / p.snap) * p.snap; dy = Math.round(dy / p.snap) * p.snap; }
        dx = Math.max(v.xmin, Math.min(v.xmax, dx)); dy = Math.max(v.ymin, Math.min(v.ymax, dy));
        return [round(dx, 6), round(dy, 6)];
      }
      function start(ev) {
        ev.preventDefault();
        var move = function (e) { var q = at(e); p.onDrag && p.onDrag(q[0], q[1]); };
        var up = function () { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); p.onEnd && p.onEnd(); };
        window.addEventListener('pointermove', move); window.addEventListener('pointerup', up);
      }
      c.addEventListener('pointerdown', start); hit.addEventListener('pointerdown', start);
      if (refocus && refocus === (p.label || 'Draggable point')) { refocus = null; setTimeout(function () { c.focus(); }, 0); }
      c.addEventListener('keydown', function (e) {
        var st = p.snap || 0.5, k = { ArrowLeft: [-st, 0], ArrowRight: [st, 0], ArrowUp: [0, st], ArrowDown: [0, -st] }[e.key];
        if (!k) return; e.preventDefault(); p.onDrag && p.onDrag(round(x + k[0], 6), round(y + k[1], 6));
      });
      return c;
    }
  };
  return api;
}

/* Debounced animation-frame redraw. */
function scheduler(fn) { var q = false; return function () { if (q) return; q = true; requestAnimationFrame(function () { q = false; fn(); }); }; }

G.Lab = { h: h, s: s, esc: esc, round: round, num: num, gcd: gcd, toFrac: toFrac, frac: frac, nice: nice, terms: terms, V: V, shift: shift,
  layout: layout, slider: slider, chips: chips, tabs: tabs, button: button, table: table, challenges: challenges, graph: graph, scheduler: scheduler };
})(window);
