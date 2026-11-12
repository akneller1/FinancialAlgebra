/* Grade 5 figure library (Mr. K's Classroom). Pure functions that return SVG strings.
 * Runs in the browser (window.G5FIGS) and in Node (require), so flashcards, games, interactive tools,
 * cheat sheets and thumbnails all draw from the same code. No dependencies, no network.
 * Every figure is drawn from the numbers passed in, so a picture always matches its question. */
(function (root) {
  'use strict';
  var C = { blue: '#3B82F6', orange: '#F59E0B', green: '#10B981', pink: '#EC4899', purple: '#8B5CF6', red: '#EF4444', teal: '#14B8A6', yellow: '#FACC15', ink: '#1E293B', soft: '#E2E8F0', paper: '#FFFFFF' };
  var CYCLE = [C.blue, C.orange, C.green, C.pink, C.purple, C.teal];
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function svg(w, h, body, title) {
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + w + ' ' + h + '" role="img"' + (title ? ' aria-label="' + esc(title) + '"' : ' aria-hidden="true"') +
      ' style="font-family:Atkinson Hyperlegible,DejaVu Sans,Verdana,sans-serif">' + (title ? '<title>' + esc(title) + '</title>' : '') + body + '</svg>';
  }
  function rect(x, y, w, h, fill, stroke, sw, rx) { return '<rect x="' + r1(x) + '" y="' + r1(y) + '" width="' + r1(w) + '" height="' + r1(h) + '" fill="' + fill + '" stroke="' + (stroke || 'none') + '" stroke-width="' + (sw || 0) + '"' + (rx ? ' rx="' + rx + '"' : '') + '/>'; }
  function line(x1, y1, x2, y2, stroke, sw, extra) { return '<line x1="' + r1(x1) + '" y1="' + r1(y1) + '" x2="' + r1(x2) + '" y2="' + r1(y2) + '" stroke="' + stroke + '" stroke-width="' + sw + '"' + (extra || '') + '/>'; }
  function text(x, y, s, size, fill, anchor, weight) { return '<text x="' + r1(x) + '" y="' + r1(y) + '" font-size="' + size + '" fill="' + (fill || C.ink) + '" text-anchor="' + (anchor || 'middle') + '" font-weight="' + (weight || 700) + '" dominant-baseline="middle">' + esc(s) + '</text>'; }
  function r1(v) { return Math.round(v * 10) / 10; }
  /* Stacked fraction (or mixed number "2 1/4") as SVG text, centered at x, y. */
  function frac(x, y, s, size, fill) {
    s = String(s); size = size || 16; fill = fill || C.ink;
    var m = /^(\d+) (\d+)\/(\d+)$/.exec(s), f = /^(\d+)\/(\d+)$/.exec(s);
    if (m) { var w = String(m[1]).length * size * 0.62; return text(x - size * 0.5, y, m[1], size * 1.1, fill) + frac(x + w * 0.45 + 2, y, m[2] + '/' + m[3], size, fill); }
    if (!f) return text(x, y, s, size, fill);
    var wd = Math.max(f[1].length, f[2].length) * size * 0.62 + 4;
    return text(x, y - size * 0.55, f[1], size, fill) + line(x - wd / 2, y, x + wd / 2, y, fill, Math.max(1.4, size / 11)) + text(x, y + size * 0.62, f[2], size, fill);
  }
  function shade(hex, k) {
    var h = hex.replace('#', ''), n = [0, 2, 4].map(function (i) { return Math.min(255, Math.round(parseInt(h.substr(i, 2), 16) * k)); });
    return '#' + n.map(function (v) { return ('0' + v.toString(16)).slice(-2); }).join('');
  }

  /* Fraction bars: rows [{d, n, color, label}] — each row is one whole cut into d equal parts, n shaded. */
  function fbars(rows, opt) {
    opt = opt || {}; var W = opt.width || 420, labelW = rows.some(function (r) { return r.label; }) ? 70 : 0, rowH = opt.rowH || 34, gap = 12;
    var H = rows.length * (rowH + gap) + 6, body = '';
    rows.forEach(function (r, i) {
      var y = 3 + i * (rowH + gap), pw = (W - labelW - 6) / r.d;
      for (var j = 0; j < r.d; j++) body += rect(3 + j * pw, y, pw, rowH, j < r.n ? (r.color || CYCLE[i % 6]) : C.paper, C.ink, 2);
      if (r.label) body += frac(W - labelW / 2, y + rowH / 2, r.label, 15);
    });
    return svg(W, H, body, opt.title || rows.map(function (r) { return r.n + ' of ' + r.d + ' equal parts shaded'; }).join('; '));
  }
  /* Fraction circles: [{d, n, color}] */
  function fcircles(list, opt) {
    opt = opt || {}; var R = 46, W = list.length * (2 * R + 20), H = 2 * R + 12, body = '';
    list.forEach(function (c, i) {
      var cx = 10 + R + i * (2 * R + 20), cy = R + 6;
      if (c.d === 1) { body += '<circle cx="' + cx + '" cy="' + cy + '" r="' + R + '" fill="' + (c.n ? (c.color || CYCLE[i % 6]) : C.paper) + '" stroke="' + C.ink + '" stroke-width="2"/>'; return; }
      for (var j = 0; j < c.d; j++) {
        var a0 = -Math.PI / 2 + j * 2 * Math.PI / c.d, a1 = a0 + 2 * Math.PI / c.d;
        var x0 = cx + R * Math.cos(a0), y0 = cy + R * Math.sin(a0), x1 = cx + R * Math.cos(a1), y1 = cy + R * Math.sin(a1);
        body += '<path d="M' + cx + ' ' + cy + ' L' + r1(x0) + ' ' + r1(y0) + ' A' + R + ' ' + R + ' 0 ' + (c.d === 2 ? 0 : 0) + ' 1 ' + r1(x1) + ' ' + r1(y1) + ' Z" fill="' + (j < c.n ? (c.color || CYCLE[i % 6]) : C.paper) + '" stroke="' + C.ink + '" stroke-width="2"/>';
      }
    });
    return svg(W, H, body, opt.title || list.map(function (c) { return c.n + ' of ' + c.d + ' equal slices shaded'; }).join('; '));
  }
  var PLACES = { 3: 'Thousands', 2: 'Hundreds', 1: 'Tens', 0: 'Ones', '-1': 'Tenths', '-2': 'Hundredths', '-3': 'Thousandths' };
  var PCOL = { 3: C.purple, 2: C.blue, 1: C.teal, 0: C.green, '-1': C.orange, '-2': C.pink, '-3': C.red };
  /* Place-value chart for a decimal string such as "347.392". highlight: place exponent to color. */
  function pvchart(numStr, opt) {
    opt = opt || {}; var s = String(numStr).replace(/,/g, ''), parts = s.split('.'), w = parts[0], f = parts[1] || '';
    var digits = {}; for (var i = 0; i < w.length; i++) digits[w.length - 1 - i] = w[i]; for (var k = 0; k < f.length; k++) digits[-(k + 1)] = f[k];
    var hi = Math.max(0, w.length - 1), lo = f.length ? -f.length : 0; if (opt.lo !== undefined) lo = Math.min(lo, opt.lo);
    var places = []; for (var e = hi; e >= lo; e--) places.push(e);
    var cw = 74, W = places.length * cw + (lo < 0 ? 16 : 0) + 4, body = '';
    places.forEach(function (e, j) {
      var x = 2 + j * cw + (e < 0 ? 16 : 0);
      body += rect(x, 2, cw - 4, 30, PCOL[e], null, 0, 6) + text(x + (cw - 4) / 2, 17, PLACES[e], PLACES[e].length > 10 ? 8.6 : PLACES[e].length > 8 ? 9.6 : 11.5, '#fff');
      body += rect(x, 36, cw - 4, 46, opt.highlight === e ? C.yellow : C.paper, C.ink, 2, 6) + text(x + (cw - 4) / 2, 59, opt.blank === e ? '?' : (digits[e] || '0'), 26, C.ink);
      if (e === 0 && lo < 0) body += '<circle cx="' + (x + cw + 4) + '" cy="74" r="4" fill="' + C.ink + '"/>';
    });
    return svg(W, 86, body, opt.title || 'Place-value chart for ' + numStr);
  }
  /* Hundred grid(s): n hundredths shaded in total. */
  function grid100(n, opt) {
    opt = opt || {}; var wholes = Math.max(1, Math.ceil(n / 100)), s = 13, W = wholes * (10 * s + 16), body = '', left = n;
    for (var g = 0; g < wholes; g++) {
      var ox = 4 + g * (10 * s + 16);
      for (var k = 0; k < 100; k++) { var a = k % 10, b = Math.floor(k / 10); body += rect(ox + a * s, 4 + b * s, s, s, k < left ? (opt.color || C.green) : C.paper, '#94A3B8', 0.8); }
      body += rect(ox, 4, 10 * s, 10 * s, 'none', C.ink, 2); left -= 100;
    }
    return svg(W, 10 * s + 8, body, opt.title || n + ' hundredths shaded');
  }
  /* Base-ten blocks; decimal=true means flat 1, rod 0.1, cube 0.01. */
  function blocks(flats, rods, units, opt) {
    opt = opt || {}; var s = 9, x = 4, body = '';
    for (var f = 0; f < flats; f++) { for (var i = 0; i < 100; i++) body += rect(x + (i % 10) * s, 4 + Math.floor(i / 10) * s, s, s, C.blue, '#fff', 0.6); body += rect(x, 4, 10 * s, 10 * s, 'none', C.ink, 1.6); x += 10 * s + 10; }
    for (var r = 0; r < rods; r++) { for (var j = 0; j < 10; j++) body += rect(x, 4 + j * s, s, s, C.orange, '#fff', 0.6); body += rect(x, 4, s, 10 * s, 'none', C.ink, 1.4); x += s + 6; }
    x += 4; for (var u = 0; u < units; u++) body += rect(x + (u % 3) * (s + 4), 4 + 10 * s - s - Math.floor(u / 3) * (s + 4), s, s, C.green, C.ink, 1.2);
    x += 3 * (s + 4);
    return svg(Math.max(x, 60) + 4, 10 * s + 8, body, opt.title || (flats + ' flats, ' + rods + ' rods and ' + units + ' small cubes'));
  }
  /* Area model: top = column labels, side = row labels, cells = 2-D array of strings. */
  function area(top, side, cells, opt) {
    opt = opt || {}; var W = 360, H = side.length > 1 ? 190 : 120, L = 46, T = 26, body = '';
    var tv = top.map(function (t) { var v = parseFloat(String(t).replace(/,/g, '')); return isFinite(v) ? v : 1; }), sv = side.map(function (t) { var v = parseFloat(String(t).replace(/,/g, '')); return isFinite(v) ? v : 1; });
    var tw = tv.map(function (v) { return Math.max(60, v / tv.reduce(function (a, b) { return a + b; }, 0) * (W - L - 4)); }), k = (W - L - 4) / tw.reduce(function (a, b) { return a + b; }, 0); tw = tw.map(function (w) { return w * k; });
    var sh = sv.map(function (v) { return Math.max(46, v / sv.reduce(function (a, b) { return a + b; }, 0) * (H - T - 4)); }), k2 = (H - T - 4) / sh.reduce(function (a, b) { return a + b; }, 0); sh = sh.map(function (h) { return h * k2; });
    var y = T;
    side.forEach(function (sl, i) {
      var x = L;
      top.forEach(function (tl, j) {
        body += rect(x, y, tw[j], sh[i], CYCLE[(i + j) % 6] + '44', C.ink, 2);
        if (cells && cells[i] && cells[i][j] != null) body += text(x + tw[j] / 2, y + sh[i] / 2, cells[i][j], 15, C.ink);
        if (i === 0) body += text(x + tw[j] / 2, 12, tl, 15, C.blue);
        x += tw[j];
      });
      body += text(L - 8, y + sh[i] / 2, sl, 15, C.red, 'end');
      y += sh[i];
    });
    return svg(W, H, body, opt.title || 'Area model');
  }
  /* Rectangular prism built from unit cubes (oblique view). */
  function cubes(l, w, h, opt) {
    opt = opt || {}; var col = opt.color || C.blue, s = 26, kx = 0.45 * 0.866 * s, ky = 0.45 * 0.5 * s;
    var W = l * s + w * kx + 8, H = h * s + w * ky + 8, body = '';
    function P(x, y, z) { return [4 + x * s + y * kx, H - 4 - (z * s + y * ky)]; }
    function poly(pts, fill) { return '<polygon points="' + pts.map(function (p) { return r1(p[0]) + ',' + r1(p[1]); }).join(' ') + '" fill="' + fill + '" stroke="' + C.ink + '" stroke-width="1.1"/>'; }
    for (var y = w - 1; y >= 0; y--) for (var z = 0; z < h; z++) for (var x = 0; x < l; x++) {
      body += poly([P(x, y, z), P(x + 1, y, z), P(x + 1, y, z + 1), P(x, y, z + 1)], col);
      body += poly([P(x, y, z + 1), P(x + 1, y, z + 1), P(x + 1, y + 1, z + 1), P(x, y + 1, z + 1)], shade(col, 1.25));
      body += poly([P(x + 1, y, z), P(x + 1, y + 1, z), P(x + 1, y + 1, z + 1), P(x + 1, y, z + 1)], shade(col, 0.78));
    }
    return svg(W, H, body, opt.title || ('Prism of unit cubes ' + l + ' long, ' + w + ' wide, ' + h + ' tall'));
  }
  /* Solid box with labelled edges. */
  function box(l, w, h, opt) {
    opt = opt || {}; var col = opt.color || C.teal, u = opt.unit ? ' ' + opt.unit : '', sc = opt.scale || Math.min(28, 210 / Math.max(l + w * 0.39, h + w * 0.23)), kx = 0.45 * 0.866 * sc, ky = 0.45 * 0.5 * sc;
    var W = l * sc + w * kx + 110, H = h * sc + w * ky + 50, ox = 50, oy = H - 30;
    function P(x, y, z) { return [ox + x * sc + y * kx, oy - (z * sc + y * ky)]; }
    function poly(pts, fill) { return '<polygon points="' + pts.map(function (p) { return r1(p[0]) + ',' + r1(p[1]); }).join(' ') + '" fill="' + fill + '" stroke="' + C.ink + '" stroke-width="2"/>'; }
    var body = poly([P(0, 0, 0), P(l, 0, 0), P(l, 0, h), P(0, 0, h)], col) + poly([P(0, 0, h), P(l, 0, h), P(l, w, h), P(0, w, h)], shade(col, 1.25)) + poly([P(l, 0, 0), P(l, w, 0), P(l, w, h), P(l, 0, h)], shade(col, 0.78));
    var a = P(l / 2, 0, 0), b = P(l, w / 2, 0), c = P(0, 0, h / 2);
    body += text(a[0], a[1] + 16, opt.labels ? opt.labels[0] : l + u, 15) + text(b[0] + 8, b[1] + 6, opt.labels ? opt.labels[1] : w + u, 15, C.ink, 'start') + text(c[0] - 8, c[1], opt.labels ? opt.labels[2] : h + u, 15, C.ink, 'end');
    return svg(W, H, body, opt.title || ('Rectangular prism ' + l + ' by ' + w + ' by ' + h + u));
  }
  /* First-quadrant coordinate grid. points: [[x, y, label, color]], segs: [[x1,y1,x2,y2,color]], poly: [[x,y],...] */
  function q1(opt) {
    opt = opt || {}; var mx = opt.max || 10, my = opt.maxY || mx, s = opt.cell || Math.min(30, 300 / Math.max(mx, my)), L = 30, B = 26, W = L + mx * s + 20, H = my * s + B + 16, body = '';
    function X(v) { return L + v * s; } function Y(v) { return H - B - v * s; }
    for (var i = 0; i <= mx; i++) body += line(X(i), Y(0), X(i), Y(my), '#CBD5E1', 1) + (i % (opt.every || 1) === 0 ? text(X(i), Y(0) + 13, i, 11, C.ink, 'middle', 400) : '');
    for (var j = 0; j <= my; j++) body += line(X(0), Y(j), X(mx), Y(j), '#CBD5E1', 1) + (j % (opt.every || 1) === 0 && j ? text(X(0) - 8, Y(j), j, 11, C.ink, 'end', 400) : '');
    body += line(X(0), Y(0), X(mx) + 10, Y(0), C.ink, 2.2) + line(X(0), Y(0), X(0), Y(my) - 10, C.ink, 2.2);
    body += text(X(mx) + 12, Y(0) - 10, opt.xlabel || 'x', 13, C.ink) + text(X(0) + 12, Y(my) - 10, opt.ylabel || 'y', 13, C.ink);
    if (opt.poly) body += '<polygon points="' + opt.poly.map(function (p) { return X(p[0]) + ',' + Y(p[1]); }).join(' ') + '" fill="' + C.teal + '33" stroke="' + C.teal + '" stroke-width="2.6"/>';
    (opt.segs || []).forEach(function (g) { body += line(X(g[0]), Y(g[1]), X(g[2]), Y(g[3]), g[4] || C.orange, 3); });
    (opt.points || []).forEach(function (p, k) { var col = p[3] || CYCLE[k % 6]; body += '<circle cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '" r="6" fill="' + col + '" stroke="#fff" stroke-width="1.5"/>' + (p[2] ? text(X(p[0]) + 12, Y(p[1]) - 10, p[2], 14, col) : ''); });
    return svg(W, H, body, opt.title || 'Coordinate grid');
  }
  /* Number line from lo to hi (numbers) with n equal parts; labels: array of label strings at given tick indexes {i: 'text'}. */
  function numline(n, labels, points, opt) {
    opt = opt || {}; var W = opt.width || 420, L = 24, R = W - 24, y = 44, body = line(L - 12, y, R + 12, y, C.ink, 2.2) + '<polygon points="' + (R + 16) + ',' + y + ' ' + (R + 6) + ',' + (y - 6) + ' ' + (R + 6) + ',' + (y + 6) + '" fill="' + C.ink + '"/><polygon points="' + (L - 16) + ',' + y + ' ' + (L - 6) + ',' + (y - 6) + ' ' + (L - 6) + ',' + (y + 6) + '" fill="' + C.ink + '"/>';
    for (var i = 0; i <= n; i++) { var x = L + (R - L) * i / n; body += line(x, y - 8, x, y + 8, C.ink, 1.8); if (labels && labels[i] !== undefined) body += frac(x, y + 26, labels[i], 13); }
    (points || []).forEach(function (p, k) { var x = L + (R - L) * p[0] / n; body += '<circle cx="' + r1(x) + '" cy="' + y + '" r="7" fill="' + (p[2] || C.red) + '"/>' + (p[1] ? text(x, y - 20, p[1], 15, p[2] || C.red) : ''); });
    return svg(W, 84, body, opt.title || 'Number line');
  }
  /* Line plot: values are strings like "1 1/4", positions from lo with step; ticks labels given. */
  function lineplot(ticks, counts, opt) {
    opt = opt || {}; var n = ticks.length, top = Math.max.apply(null, counts.concat([1])), W = Math.max(300, n * 64), L = 30, R = W - 30, base = 40 + top * 22, H = base + 56, body = line(L - 10, base, R + 10, base, C.ink, 2.2);
    ticks.forEach(function (t, i) { var x = L + (R - L) * i / (n - 1); body += line(x, base - 6, x, base + 6, C.ink, 1.8) + frac(x, base + 24, t, 13); for (var k = 0; k < counts[i]; k++) body += text(x, base - 16 - k * 22, '✕', 18, C.blue); });
    if (opt.xlabel) body += text(W / 2, H - 6, opt.xlabel, 12, C.ink, 'middle', 700);
    return svg(W, H, body, opt.title || 'Line plot');
  }
  /* Ruler (inches) with a bar of given length in 1/denom inch. */
  function ruler(lengthNum, denom, maxIn, opt) {
    opt = opt || {}; var s = 70, W = maxIn * s + 40, body = rect(10, 10, lengthNum / denom * s, 18, opt.color || C.orange, C.ink, 1.6, 3) + rect(6, 36, maxIn * s + 8, 34, '#FEF3C7', C.ink, 1.4, 4);
    for (var k = 0; k <= maxIn * denom; k++) { var x = 10 + k * s / denom, ht = k % denom === 0 ? 16 : (denom % 2 === 0 && k % (denom / 2) === 0 ? 11 : 7); body += line(x, 36, x, 36 + ht, C.ink, 1.3); if (k % denom === 0) body += text(x, 62, k / denom, 11, C.ink, 'middle', 400); }
    return svg(W, 76, body, opt.title || 'Ruler');
  }
  /* Named shapes with tick marks, right-angle marks and parallel arrows. */
  var SHAPES = {
    square: { pts: [[20, 120], [120, 120], [120, 20], [20, 20]], ticks: [1, 1, 1, 1], right: [0, 1, 2, 3], par: [1, 2, 1, 2] },
    rectangle: { pts: [[10, 110], [170, 110], [170, 30], [10, 30]], ticks: [1, 2, 1, 2], right: [0, 1, 2, 3], par: [1, 2, 1, 2] },
    rhombus: { pts: [[10, 110], [110, 110], [160, 30], [60, 30]], ticks: [1, 1, 1, 1], right: [], par: [1, 2, 1, 2] },
    parallelogram: { pts: [[10, 110], [140, 110], [175, 35], [45, 35]], ticks: [1, 2, 1, 2], right: [], par: [1, 2, 1, 2] },
    trapezoid: { pts: [[10, 110], [175, 110], [135, 35], [50, 35]], ticks: [0, 0, 0, 0], right: [], par: [1, 0, 1, 0] },
    kite: { pts: [[90, 10], [140, 55], [90, 125], [40, 55]], ticks: [1, 2, 2, 1], right: [], par: [0, 0, 0, 0] },
    equilateral: { pts: [[20, 120], [140, 120], [80, 16]], ticks: [1, 1, 1], right: [], par: [] },
    isosceles: { pts: [[30, 120], [130, 120], [80, 14]], ticks: [0, 1, 1], right: [], par: [] },
    scalene: { pts: [[10, 120], [160, 120], [55, 30]], ticks: [1, 2, 3], right: [], par: [] },
    right: { pts: [[20, 120], [140, 120], [20, 30]], ticks: [0, 0, 0], right: [0], par: [] },
    obtuse: { pts: [[10, 120], [110, 120], [165, 50]], ticks: [0, 0, 0], right: [], par: [] },
    pentagon: 5, hexagon: 6, octagon: 8
  };
  function shape(kind, opt) {
    opt = opt || {}; var def = SHAPES[kind], col = opt.color || C.purple;
    if (typeof def === 'number') { var n = def, pts = []; for (var i = 0; i < n; i++) pts.push([90 + 60 * Math.cos(-Math.PI / 2 + 2 * Math.PI * i / n), 72 + 60 * Math.sin(-Math.PI / 2 + 2 * Math.PI * i / n)]); def = { pts: pts, ticks: pts.map(function () { return 1; }), right: [], par: [] }; }
    var P = def.pts, n2 = P.length, body = '<polygon points="' + P.map(function (p) { return p.join(','); }).join(' ') + '" fill="' + col + '33" stroke="' + col + '" stroke-width="3.2" stroke-linejoin="round"/>';
    for (var k = 0; k < n2; k++) {
      var a = P[k], b = P[(k + 1) % n2], mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1], L = Math.sqrt(dx * dx + dy * dy), ux = dx / L, uy = dy / L, nx = -uy, ny = ux;
      for (var t = 0; t < (def.ticks[k] || 0); t++) { var off = (t - (def.ticks[k] - 1) / 2) * 6, px = mx + ux * off, py = my + uy * off; body += line(px - nx * 7, py - ny * 7, px + nx * 7, py + ny * 7, C.ink, 2); }
      for (var q = 0; q < (def.par[k] || 0); q++) { var o2 = 16 + q * 8, qx = mx + ux * o2, qy = my + uy * o2; body += '<polyline points="' + r1(qx - ux * 7 + nx * 6) + ',' + r1(qy - uy * 7 + ny * 6) + ' ' + r1(qx) + ',' + r1(qy) + ' ' + r1(qx - ux * 7 - nx * 6) + ',' + r1(qy - uy * 7 - ny * 6) + '" fill="none" stroke="' + C.red + '" stroke-width="2"/>'; }
    }
    (def.right || []).forEach(function (i) {
      var b = P[i], a = P[(i - 1 + n2) % n2], c = P[(i + 1) % n2], s = 12;
      function u(p) { var dx = p[0] - b[0], dy = p[1] - b[1], L = Math.sqrt(dx * dx + dy * dy); return [dx / L * s, dy / L * s]; }
      var ua = u(a), uc = u(c); body += '<polyline points="' + r1(b[0] + ua[0]) + ',' + r1(b[1] + ua[1]) + ' ' + r1(b[0] + ua[0] + uc[0]) + ',' + r1(b[1] + ua[1] + uc[1]) + ' ' + r1(b[0] + uc[0]) + ',' + r1(b[1] + uc[1]) + '" fill="none" stroke="' + C.ink + '" stroke-width="1.8"/>';
    });
    return svg(185, 140, body, opt.title || kind);
  }
  /* Array of dots. */
  function dots(rows, cols, opt) {
    opt = opt || {}; var s = 20, body = '';
    for (var i = 0; i < rows; i++) for (var j = 0; j < cols; j++) body += '<circle cx="' + (12 + j * s) + '" cy="' + (12 + i * s) + '" r="7" fill="' + (opt.color || C.pink) + '"/>';
    return svg(cols * s + 4, rows * s + 4, body, opt.title || rows + ' rows of ' + cols);
  }
  /* Unit icons used for thumbnails, unit cards and headers. */
  function unitIcon(unitId, opt) {
    opt = opt || {}; var b = '';
    var bg = { 'place-value-number-sense': C.blue, 'multi-digit-multiplication-division': C.orange, 'decimal-operations': C.green, 'numerical-expressions-patterns': C.purple,
      'fraction-addition-subtraction': C.pink, 'fraction-multiplication-division': C.red, 'measurement-conversions': C.teal, 'volume-three-dimensional-figures': C.blue,
      'coordinate-plane-graphing': C.green, 'classifying-two-dimensional-figures': C.purple, 'data-line-plots-problem-solving': C.orange }[unitId] || C.blue;
    b += rect(0, 0, 160, 120, bg + '22', null, 0, 18);
    function g(inner, tx, ty, sc) { return '<g transform="translate(' + tx + ',' + ty + ') scale(' + sc + ')">' + inner + '</g>'; }
    function strip(s) { return s.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '').replace(/<title>.*?<\/title>/, ''); }
    switch (unitId) {
      case 'place-value-number-sense': b += g(strip(blocks(1, 3, 4)), 16, 24, 0.78); break;
      case 'multi-digit-multiplication-division': b += g(strip(area(['20', '4'], ['10', '3'], [['200', '40'], ['60', '12']])), 8, 12, 0.4) + text(118, 100, '×  ÷', 22, C.orange); break;
      case 'decimal-operations': b += g(strip(grid100(37)), 30, 14, 0.66) + text(80, 108, '0.37', 16, C.green); break;
      case 'numerical-expressions-patterns': b += text(80, 50, '{ [ ( ) ] }', 26, C.purple) + text(80, 88, '2, 4, 6, 8…', 18, C.ink); break;
      case 'fraction-addition-subtraction': b += g(strip(fcircles([{ d: 4, n: 3, color: C.pink }])), 32, 14, 0.9); break;
      case 'fraction-multiplication-division': b += g(strip(fbars([{ d: 3, n: 2, color: C.red }, { d: 6, n: 4, color: C.orange }], { width: 240 })), 20, 30, 0.5) + text(80, 100, '× ÷', 20, C.red); break;
      case 'measurement-conversions': b += g(strip(ruler(10, 4, 3)), 14, 40, 0.55) + text(80, 30, '12 in = 1 ft', 14, C.teal); break;
      case 'volume-three-dimensional-figures': b += g(strip(cubes(3, 2, 2, { color: C.blue })), 40, 16, 0.95); break;
      case 'coordinate-plane-graphing': b += g(strip(q1({ max: 5, cell: 18, points: [[2, 3, '', C.green], [4, 1, '', C.orange]] })), 22, 2, 0.95); break;
      case 'classifying-two-dimensional-figures': b += g(strip(shape('equilateral', { color: C.purple })), 6, 30, 0.45) + g(strip(shape('square', { color: C.orange })), 58, 40, 0.42) + g(strip(shape('hexagon', { color: C.green })), 100, 26, 0.42); break;
      case 'data-line-plots-problem-solving': b += g(strip(lineplot(['0', '1/2', '1'], [2, 3, 1])), 14, 6, 0.52); break;
    }
    return svg(160, 120, b, opt.title || 'Unit icon');
  }
  var API = { C: C, CYCLE: CYCLE, svg: svg, frac: frac, fbars: fbars, fcircles: fcircles, pvchart: pvchart, grid100: grid100, blocks: blocks, area: area, cubes: cubes, box: box, q1: q1,
    numline: numline, lineplot: lineplot, ruler: ruler, shape: shape, dots: dots, unitIcon: unitIcon, SHAPES: SHAPES };
  if (typeof module !== 'undefined' && module.exports) module.exports = API; else root.G5FIGS = API;
})(typeof window !== 'undefined' ? window : globalThis);
