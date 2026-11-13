"""Grade 4 Interactive Math tools: writes artifacts/math4-<slug>/index.html and interactive/manifest.json.
Usage: python3 tools/grade4-authoring/interactive/tools.py
Each tool is one page: a live picture and its controls in ONE workspace card (so zoom, Fit and Present scale them
together), Try-this challenges that tick themselves off, a closed "What should I notice?" panel, teacher notes, Reset.
All math uses whole numbers and exact fractions. No network calls."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("G4_ROOT", os.path.abspath(os.path.join(HERE, "..", "..", "..")))
V = "grade4-20261112"
PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · 4th Grade Math | Mr. K's Classroom</title><meta name="description" content="{desc}">
<link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../../worksheet-generator/elementary/el-tools.css?v={v}">
</head><body class="tl">
<main class="tl-main"><section class="tl-card" id="workspace"><h1>{title}</h1><p class="tl-sub">{intro}</p>
{body}
</section>
<aside class="tl-aside"><section class="tl-card" id="challenges"></section><section class="tl-card" id="notice"></section></aside></main>
<script src="../../worksheet-generator/elementary/el-tool-shell.js?v={v}"></script>
<script>
(function () {{
'use strict';
var T = window.TOOL, $ = T.$;
{script}
}})();
</script></body></html>
"""
TOOLS = []


def tool(slug, units, title, desc, intro, topics, standards, body, script):
    TOOLS.append(dict(slug="math4-" + slug, units=units, title=title, description=desc, intro=intro, topics=topics, standards=standards, body=body, script=script))


def step(key, label, bid):
    return (f'<div class="tl-field"><span class="lab">{label}</span><div class="tl-step"><button type="button" data-k="{key}" data-s="-1" aria-label="{label} down">−</button>'
            f'<b id="{bid}"></b><button type="button" data-k="{key}" data-s="1" aria-label="{label} up">+</button></div></div>')


def slider(sid, label, lo, hi, val, stp=1):
    return f'<div class="tl-field"><label for="{sid}">{label}: <b id="{sid}V"></b></label><input type="range" id="{sid}" min="{lo}" max="{hi}" step="{stp}" value="{val}"></div>'


INIT = """T.init({{ course: 'math4', courseName: '4th Grade Math', unit: '{unit}', title: '{title}', standards: '{standards}',
  teacher: {teacher}, notice: {notice}, challenges: CH, reset: function () {{ reset(); draw(); }} }});"""

# ------------------------------------------------------------------ 1 Place-Value Blocks
tool("place-value-blocks", ["place-value-number-sense", "multi-digit-addition-subtraction"], "Place-Value Blocks",
     "Build numbers to 9,999 with thousands cubes, hundreds flats, tens rods and ones. See standard, expanded and word form, and regroup 10 of one place into 1 of the next.",
     "Use + and − to add or take away blocks. When a place has 10 blocks, press Regroup to trade them.", ["Place value", "Base-ten blocks", "Regrouping"], "4.NBT.A.1, 4.NBT.A.2",
     '<div class="tl-model" id="pvModel" aria-live="polite"></div><div class="tl-big" id="pvNum"></div>'
     '<div class="tl-controls" id="pvCtl">' + step("3", "Thousands", "pv3") + step("2", "Hundreds", "pv2") + step("1", "Tens", "pv1") + step("0", "Ones", "pv0") +
     '<button type="button" class="tl-btn" id="pvRe">Regroup</button><button type="button" class="tl-btn" id="pvTen">× 10</button></div>'
     '<div class="tl-out" id="pvOut"></div>',
     r"""var st, NAMES = ['ones', 'tens', 'hundreds', 'thousands'];
function reset() { st = { d: [6, 4, 3, 1], regrouped: 0, times10: 0 }; }
function value() { return st.d[0] + 10 * st.d[1] + 100 * st.d[2] + 1000 * st.d[3]; }
var ONES = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'], TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
function words(n) { if (n < 20) return ONES[n]; if (n < 100) return TENS[Math.floor(n / 10)] + (n % 10 ? '-' + ONES[n % 10] : ''); if (n < 1000) return ONES[Math.floor(n / 100)] + ' hundred' + (n % 100 ? ' ' + words(n % 100) : ''); return words(Math.floor(n / 1000)) + ' thousand' + (n % 1000 ? ', ' + words(n % 1000) : ''); }
function blocks() {
  var s = '<svg viewBox="0 0 760 250" role="img" aria-label="Base-ten blocks: ' + st.d[3] + ' thousands, ' + st.d[2] + ' hundreds, ' + st.d[1] + ' tens, ' + st.d[0] + ' ones">', i, x;
  var col = [['#f472b6', '#9d174d'], ['#fbbf24', '#92400e'], ['#34d399', '#065f46'], ['#60a5fa', '#1e3a8a']];
  for (i = 0; i < Math.min(st.d[3], 12); i++) { x = 14 + (i % 6) * 34; var y = 30 + Math.floor(i / 6) * 96; s += '<rect x="' + x + '" y="' + (y + 12) + '" width="56" height="56" fill="' + col[3][0] + '" stroke="' + col[3][1] + '" stroke-width="2"/><path d="M' + x + ' ' + (y + 12) + ' l12 -12 h56 l-12 12z M' + (x + 56) + ' ' + (y + 12) + ' l12 -12 v56 l-12 12z" fill="#3b82f6" stroke="' + col[3][1] + '" stroke-width="2"/>'; }
  for (i = 0; i < Math.min(st.d[2], 12); i++) { x = 250 + (i % 6) * 26; s += '<rect x="' + x + '" y="' + (30 + Math.floor(i / 6) * 100 + (i % 6) * 5) + '" width="60" height="60" fill="' + col[2][0] + '" stroke="' + col[2][1] + '" stroke-width="2" opacity=".93"/>'; }
  for (i = 0; i < Math.min(st.d[1], 14); i++) s += '<rect x="' + (470 + i * 13) + '" y="30" width="9" height="90" fill="' + col[1][0] + '" stroke="' + col[1][1] + '" stroke-width="1.5"/>';
  for (i = 0; i < Math.min(st.d[0], 14); i++) s += '<rect x="' + (660 + (i % 5) * 16) + '" y="' + (30 + Math.floor(i / 5) * 16) + '" width="11" height="11" fill="' + col[0][0] + '" stroke="' + col[0][1] + '" stroke-width="1.5"/>';
  ['Thousands', 'Hundreds', 'Tens', 'Ones'].forEach(function (t, k) { s += '<text x="' + [100, 330, 550, 695][k] + '" y="236" text-anchor="middle" font-size="19" font-weight="800" fill="#1d2a3a">' + t + ': ' + st.d[3 - k] + '</text>'; });
  return s + '</svg>';
}
function draw() {
  var n = value();
  $('pvModel').innerHTML = blocks(); $('pvNum').textContent = T.comma(n);
  [0, 1, 2, 3].forEach(function (k) { $('pv' + k).textContent = st.d[k]; });
  var exp = [3, 2, 1, 0].filter(function (k) { return st.d[k]; }).map(function (k) { return T.comma(st.d[k] * Math.pow(10, k)); }).join(' + ') || '0';
  var can = st.d.slice(0, 3).some(function (v) { return v >= 10; });
  $('pvRe').disabled = !can;
  $('pvOut').innerHTML = '<b>Expanded form:</b> ' + exp + '<br><b>Word form:</b> ' + words(n) + (can ? '<br><b>Regroup!</b> A place has 10 or more blocks. Trade 10 of them for 1 of the next place.' : '');
  T.update({ n: n, d: st.d, regrouped: st.regrouped, times10: st.times10 });
}
var CH = [{ text: 'Build 2,405. Which place has no blocks?', test: function (s) { return s.n === 2405 && s.d[1] === 0; } },
  { text: 'Make 10 or more ones, then press Regroup.', test: function (s) { return s.regrouped > 0; } },
  { text: 'Build 360, then press × 10. What happens to each digit?', test: function (s) { return s.times10 > 0 && s.n === 3600; } },
  { text: 'Build the greatest number you can with 3 blocks.', test: function (s) { return s.n === 3000; } }];
reset();
INIT
T.steppers($('pvCtl'), function (k, dlt) { k = +k; st.d[k] = Math.max(0, Math.min(k === 3 ? 9 : 14, st.d[k] + dlt)); draw(); });
$('pvRe').onclick = function () { for (var k = 0; k < 3; k++) if (st.d[k] >= 10 && st.d[k + 1] < (k === 2 ? 9 : 14)) { st.d[k] -= 10; st.d[k + 1]++; st.regrouped++; break; } draw(); };
$('pvTen').onclick = function () { var n = value() * 10; if (n > 9999) { $('pvOut').innerHTML = '<b>Too big:</b> this tool shows numbers up to 9,999.'; return; } st.d = [n % 10, Math.floor(n / 10) % 10, Math.floor(n / 100) % 10, Math.floor(n / 1000)]; st.times10++; draw(); };
draw();""")

# ------------------------------------------------------------------ 2 Arrays and Area Models
tool("array-area-models", ["multiplication-strategies", "factors-multiples-patterns"], "Arrays and Area Models",
     "Build a multiplication array, split it into tens and ones, and see the partial products add up to the whole product.",
     "Choose the number of rows and columns. Move the split line to break the array into two easier parts.", ["Multiplication", "Arrays", "Area model", "Distributive property"], "4.NBT.B.5, 4.OA.B.4",
     '<div class="tl-model" id="amModel"></div><div class="tl-controls">' + slider("amR", "Rows", 1, 12, 4) + slider("amC", "Columns", 1, 30, 12) + slider("amS", "Split after column", 0, 30, 10) +
     '<button type="button" class="tl-btn" id="amMode" aria-pressed="false">Show as area model</button></div><div class="tl-out" id="amOut"></div>',
     r"""var st;
function reset() { st = { r: 4, c: 12, s: 10, area: false, splits: {} }; $('amR').value = 4; $('amC').value = 12; $('amS').max = 30; $('amS').value = 10; }
function draw() {
  st.r = +$('amR').value; st.c = +$('amC').value; $('amS').max = st.c; st.s = Math.min(+$('amS').value, st.c); $('amS').value = st.s;
  $('amRV').textContent = st.r; $('amCV').textContent = st.c; $('amSV').textContent = st.s ? st.s : 'no split';
  var u = Math.min(22, 700 / st.c, 250 / st.r), W = st.c * u + 70, H = st.r * u + 60, x0 = 44, y0 = 34, s = '<svg viewBox="0 0 ' + W.toFixed(0) + ' ' + H.toFixed(0) + '" role="img" aria-label="' + st.r + ' by ' + st.c + ' array">';
  var a = st.s && st.s < st.c ? st.s : 0;
  if (st.area) {
    s += '<rect x="' + x0 + '" y="' + y0 + '" width="' + ((a || st.c) * u) + '" height="' + (st.r * u) + '" fill="#7fb6f0" stroke="#1e3a8a" stroke-width="3"/>';
    if (a) s += '<rect x="' + (x0 + a * u) + '" y="' + y0 + '" width="' + ((st.c - a) * u) + '" height="' + (st.r * u) + '" fill="#ffc27a" stroke="#1e3a8a" stroke-width="3"/>';
    s += '<text x="' + (x0 + (a || st.c) * u / 2) + '" y="' + (y0 + st.r * u / 2 + 7) + '" text-anchor="middle" font-size="20" font-weight="800">' + st.r * (a || st.c) + '</text>';
    if (a) s += '<text x="' + (x0 + a * u + (st.c - a) * u / 2) + '" y="' + (y0 + st.r * u / 2 + 7) + '" text-anchor="middle" font-size="20" font-weight="800">' + st.r * (st.c - a) + '</text>';
  } else {
    for (var i = 0; i < st.r; i++) for (var j = 0; j < st.c; j++) s += '<circle cx="' + (x0 + j * u + u / 2).toFixed(1) + '" cy="' + (y0 + i * u + u / 2).toFixed(1) + '" r="' + (u * 0.36).toFixed(1) + '" fill="' + (a && j >= a ? '#f08c1a' : '#2f7fd8') + '"/>';
    if (a) s += '<line x1="' + (x0 + a * u) + '" y1="' + (y0 - 8) + '" x2="' + (x0 + a * u) + '" y2="' + (y0 + st.r * u + 8) + '" stroke="#1d2a3a" stroke-width="3" stroke-dasharray="7 6"/>';
  }
  s += '<text x="' + (x0 - 12) + '" y="' + (y0 + st.r * u / 2 + 7) + '" text-anchor="end" font-size="20" font-weight="800">' + st.r + '</text>';
  s += '<text x="' + (x0 + (a || st.c) * u / 2) + '" y="' + (y0 - 12) + '" text-anchor="middle" font-size="20" font-weight="800">' + (a || st.c) + '</text>';
  if (a) s += '<text x="' + (x0 + a * u + (st.c - a) * u / 2) + '" y="' + (y0 - 12) + '" text-anchor="middle" font-size="20" font-weight="800">' + (st.c - a) + '</text>';
  $('amModel').innerHTML = s + '</svg>';
  var p = st.r * st.c;
  $('amOut').innerHTML = a ? '<b>' + st.r + ' × ' + st.c + '</b> = (' + st.r + ' × ' + a + ') + (' + st.r + ' × ' + (st.c - a) + ') = ' + st.r * a + ' + ' + st.r * (st.c - a) + ' = <b>' + p + '</b>' : '<b>' + st.r + ' × ' + st.c + ' = ' + p + '</b>. ' + st.r + ' and ' + st.c + ' are a factor pair of ' + p + '.';
  if (a) st.splits[st.r + 'x' + st.c + '@' + a] = 1;
  T.update({ r: st.r, c: st.c, a: a, area: st.area, p: p });
}
var CH = [{ text: 'Build 6 × 14 and split it into 6 × 10 and 6 × 4.', test: function (s) { return s.r === 6 && s.c === 14 && s.a === 10; } },
  { text: 'Show 7 × 23 as an area model split at 20.', test: function (s) { return s.r === 7 && s.c === 23 && s.a === 20 && s.area; } },
  { text: 'Find an array with 24 dots that is not 4 × 6.', test: function (s) { return s.p === 24 && !(s.r === 4 && s.c === 6) && !(s.r === 6 && s.c === 4); } },
  { text: 'Make a square array. What is special about its two factors?', test: function (s) { return s.r === s.c && s.r > 1; } }];
reset();
INIT
['amR', 'amC', 'amS'].forEach(function (id) { $(id).oninput = draw; });
$('amMode').onclick = function () { st.area = !st.area; this.setAttribute('aria-pressed', st.area); this.textContent = st.area ? 'Show as dots' : 'Show as area model'; draw(); };
draw();""")

# ------------------------------------------------------------------ 3 Division: Groups and Arrays
tool("division-groups", ["division-remainders"], "Division: Groups and Arrays",
     "Share counters into equal groups or arrange them in rows. See the quotient, the remainder and the multiplication check.",
     "Choose how many counters and how many groups. Watch what is left over.", ["Division", "Equal groups", "Remainders"], "4.NBT.B.6, 4.OA.A.3",
     '<div class="tl-model" id="dvModel"></div><div class="tl-controls">' + slider("dvN", "Counters (dividend)", 1, 60, 17) + slider("dvD", "Groups (divisor)", 1, 10, 3) +
     '<button type="button" class="tl-btn" id="dvMode" aria-pressed="false">Show as rows</button></div><div class="tl-out" id="dvOut"></div>',
     r"""var st;
function reset() { st = { n: 17, d: 3, rows: false }; $('dvN').value = 17; $('dvD').value = 3; }
function draw() {
  st.n = +$('dvN').value; st.d = +$('dvD').value; $('dvNV').textContent = st.n; $('dvDV').textContent = st.d;
  var q = Math.floor(st.n / st.d), r = st.n % st.d, s, i, j;
  if (st.rows) {
    var u = Math.min(26, 640 / Math.max(q + r, 6)), W = Math.max(q + (r ? 1 : 0), 6) * u + 150;
    s = '<svg viewBox="0 0 ' + W.toFixed(0) + ' ' + (st.d * u + 50) + '" role="img" aria-label="' + st.d + ' rows of ' + q + ' with ' + r + ' left over">';
    for (i = 0; i < st.d; i++) for (j = 0; j < q; j++) s += '<circle cx="' + (30 + j * u + u / 2) + '" cy="' + (20 + i * u + u / 2) + '" r="' + u * 0.36 + '" fill="#8a4fd6"/>';
    for (i = 0; i < r; i++) s += '<circle cx="' + (30 + q * u + 50 + u / 2) + '" cy="' + (20 + i * u + u / 2) + '" r="' + u * 0.36 + '" fill="#f08c1a"/>';
    if (r) s += '<text x="' + (30 + q * u + 50 + u / 2) + '" y="' + (st.d * u + 42) + '" text-anchor="middle" font-size="16" font-weight="800" fill="#b4590b">left over</text>';
  } else {
    var per = Math.min(5, Math.max(1, Math.ceil(Math.sqrt(Math.max(q, 1))))), gw = Math.max(1, per) * 22 + 20, gh = Math.ceil(Math.max(q, 1) / per) * 22 + 20, cols = Math.min(st.d, 5), rowsN = Math.ceil(st.d / cols);
    s = '<svg viewBox="0 0 ' + (cols * (gw + 14) + 120) + ' ' + (rowsN * (gh + 14) + 30) + '" role="img" aria-label="' + st.d + ' groups of ' + q + ' with ' + r + ' left over">';
    for (i = 0; i < st.d; i++) { var gx = 10 + (i % cols) * (gw + 14), gy = 10 + Math.floor(i / cols) * (gh + 14); s += '<rect x="' + gx + '" y="' + gy + '" width="' + gw + '" height="' + gh + '" rx="12" fill="#fff" stroke="#8a4fd6" stroke-width="3"/>'; for (j = 0; j < q; j++) s += '<circle cx="' + (gx + 21 + (j % per) * 22) + '" cy="' + (gy + 21 + Math.floor(j / per) * 22) + '" r="8" fill="#8a4fd6"/>'; }
    for (i = 0; i < r; i++) s += '<circle cx="' + (cols * (gw + 14) + 30 + (i % 3) * 24) + '" cy="' + (30 + Math.floor(i / 3) * 24) + '" r="9" fill="#f08c1a"/>';
    if (r) s += '<text x="' + (cols * (gw + 14) + 54) + '" y="' + (30 + Math.ceil(r / 3) * 24 + 14) + '" text-anchor="middle" font-size="15" font-weight="800" fill="#b4590b">left over</text>';
  }
  $('dvModel').innerHTML = s + '</svg>';
  $('dvOut').innerHTML = '<b>' + st.n + ' ÷ ' + st.d + ' = ' + q + (r ? ' R ' + r : '') + '</b> &nbsp; Check: ' + st.d + ' × ' + q + (r ? ' + ' + r : '') + ' = ' + st.n + (r ? '<br>The remainder ' + r + ' is less than the divisor ' + st.d + '.' : '<br>No remainder: ' + st.d + ' is a factor of ' + st.n + '.');
  T.update({ n: st.n, d: st.d, q: q, r: r, rows: st.rows });
}
var CH = [{ text: 'Share 23 counters into 4 groups. What is left over?', test: function (s) { return s.n === 23 && s.d === 4; } },
  { text: 'Find a number of counters that leaves a remainder of 0 when divided by 6.', test: function (s) { return s.d === 6 && s.r === 0 && s.n >= 6; } },
  { text: 'Make the largest remainder you can when dividing by 5.', test: function (s) { return s.d === 5 && s.r === 4; } },
  { text: 'Show 36 ÷ 9 as rows. How is it like an array?', test: function (s) { return s.n === 36 && s.d === 9 && s.rows; } }];
reset();
INIT
$('dvN').oninput = draw; $('dvD').oninput = draw;
$('dvMode').onclick = function () { st.rows = !st.rows; this.setAttribute('aria-pressed', st.rows); this.textContent = st.rows ? 'Show as groups' : 'Show as rows'; draw(); };
draw();""")

# ------------------------------------------------------------------ 4 Equivalent Fraction Models
tool("equivalent-fractions", ["fractions-equivalent-fractions"], "Equivalent Fraction Models",
     "Shade a fraction bar, then cut every part into smaller equal parts. The amount stays the same while the numerator and denominator are multiplied by the same number.",
     "Set a fraction. Then choose how many pieces to cut each part into.", ["Fractions", "Equivalent fractions", "Simplest form"], "4.NF.A.1, 4.NF.A.2",
     '<div class="tl-model" id="efModel"></div><div class="tl-controls" id="efCtl">' + step("n", "Numerator", "efN") + step("d", "Denominator", "efD") + step("k", "Cut each part into", "efK") + '</div><div class="tl-out" id="efOut"></div>',
     r"""var st;
function reset() { st = { n: 2, d: 3, k: 2 }; }
function bar(y, n, d, fill, label) {
  var w = 640 / d, s = '';
  for (var i = 0; i < d; i++) s += '<rect x="' + (20 + i * w).toFixed(1) + '" y="' + y + '" width="' + w.toFixed(1) + '" height="64" fill="' + (i < n ? fill : '#fff') + '" stroke="#1d2a3a" stroke-width="2.5"/>';
  return s + '<text x="700" y="' + (y + 26) + '" text-anchor="middle" font-size="24" font-weight="800">' + n + '</text><line x1="680" y1="' + (y + 33) + '" x2="720" y2="' + (y + 33) + '" stroke="#1d2a3a" stroke-width="3"/><text x="700" y="' + (y + 58) + '" text-anchor="middle" font-size="24" font-weight="800">' + d + '</text>';
}
function draw() {
  var N = st.n * st.k, Dn = st.d * st.k, g = T.gcd(st.n, st.d);
  $('efN').textContent = st.n; $('efD').textContent = st.d; $('efK').textContent = st.k;
  $('efModel').innerHTML = '<svg viewBox="0 0 740 190" role="img" aria-label="Two fraction bars: ' + st.n + ' of ' + st.d + ' and ' + N + ' of ' + Dn + '">' + bar(14, st.n, st.d, '#f5a3c4') + bar(108, N, Dn, '#c3a6f0') +
    '<line x1="' + (20 + 640 * st.n / st.d) + '" y1="6" x2="' + (20 + 640 * st.n / st.d) + '" y2="182" stroke="#d63c7a" stroke-width="3" stroke-dasharray="7 6"/></svg>';
  $('efOut').innerHTML = T.frac(st.n, st.d) + ' = ' + T.frac(st.n + ' × ' + st.k, st.d + ' × ' + st.k) + ' = <b>' + T.frac(N, Dn) + '</b> &nbsp; The shading ends at the same place on both bars.' +
    (g > 1 ? '<br>Simplest form of ' + T.frac(st.n, st.d) + ' is ' + T.frac(st.n / g, st.d / g) + '.' : '<br>' + T.frac(st.n, st.d) + ' is in simplest form.') +
    '<br>Compared with ' + T.frac(1, 2) + ': ' + T.frac(st.n, st.d) + ' is <b>' + (2 * st.n > st.d ? 'greater than' : 2 * st.n < st.d ? 'less than' : 'equal to') + '</b> ' + T.frac(1, 2) + '.';
  T.update({ n: st.n, d: st.d, k: st.k, N: N, D: Dn });
}
var CH = [{ text: 'Show that 2/3 is equal to 8/12.', test: function (s) { return s.n === 2 && s.d === 3 && s.k === 4; } },
  { text: 'Make a fraction equal to 1/2 that has a denominator of 10.', test: function (s) { return s.N * 2 === s.D && s.D === 10; } },
  { text: 'Build 6/8. What is its simplest form?', test: function (s) { return s.n === 6 && s.d === 8; } },
  { text: 'Find three different names for 3/4.', test: (function () { var seen = {}; return function (s) { if (s.n * 4 === s.d * 3) seen[s.N + '/' + s.D] = 1; return Object.keys(seen).length >= 3; }; })() }];
CH.forEach(function (c) { c.text = c.text.replace(/(\d+)\/(\d+)/g, function (m, a, b) { return T.frac(a, b); }); });
reset();
INIT
T.steppers($('efCtl'), function (k, dlt) {
  if (k === 'n') st.n = Math.max(0, Math.min(st.d, st.n + dlt));
  if (k === 'd') { st.d = Math.max(1, Math.min(12, st.d + dlt)); st.n = Math.min(st.n, st.d); }
  if (k === 'k') st.k = Math.max(1, Math.min(6, st.k + dlt));
  draw();
});
draw();""")

# ------------------------------------------------------------------ 5 Fraction Number Line
tool("fraction-number-line", ["fractions-equivalent-fractions", "fraction-operations-decimals"], "Fraction Number Line",
     "Jump along a number line by equal fractions. See a fraction as a multiple of a unit fraction, as a mixed number, and as a product.",
     "Choose the size of each jump and how many jumps to take, starting at 0.", ["Fractions", "Number line", "Multiplying a fraction by a whole number", "Mixed numbers"], "4.NF.B.3, 4.NF.B.4",
     '<div class="tl-model" id="nlModel"></div><div class="tl-controls" id="nlCtl"><div class="tl-field"><label for="nlD">Denominator</label><select id="nlD"><option>2</option><option>3</option><option selected>4</option><option>5</option><option>6</option><option>8</option><option>10</option><option>12</option></select></div>' +
     step("a", "Numerator of each jump", "nlA") + step("j", "Number of jumps", "nlJ") + '</div><div class="tl-out" id="nlOut"></div>',
     r"""var st;
function reset() { st = { d: 4, a: 3, j: 2 }; $('nlD').value = 4; }
function draw() {
  st.d = +$('nlD').value; st.a = Math.min(st.a, st.d * 2);
  var tot = st.a * st.j, hi = Math.max(2, Math.ceil(tot / st.d) + (tot % st.d === 0 ? 0 : 0)), W = 760, x0 = 40, sc = (W - 80) / hi, y = 150, s, i;
  $('nlA').textContent = st.a; $('nlJ').textContent = st.j;
  s = '<svg viewBox="0 0 ' + W + ' 210" role="img" aria-label="Number line from 0 to ' + hi + ' with ' + st.j + ' jumps of ' + st.a + ' over ' + st.d + '"><line x1="' + (x0 - 14) + '" y1="' + y + '" x2="' + (W - 26) + '" y2="' + y + '" stroke="#1d2a3a" stroke-width="3.5"/>';
  for (i = 0; i <= hi * st.d; i++) { var big = i % st.d === 0, x = x0 + i * sc / st.d; s += '<line x1="' + x.toFixed(1) + '" y1="' + (y - (big ? 15 : 8)) + '" x2="' + x.toFixed(1) + '" y2="' + (y + (big ? 15 : 8)) + '" stroke="#1d2a3a" stroke-width="' + (big ? 3.5 : 1.8) + '"/>'; if (big) s += '<text x="' + x.toFixed(1) + '" y="' + (y + 44) + '" text-anchor="middle" font-size="24" font-weight="800">' + i / st.d + '</text>'; }
  for (i = 0; i < st.j; i++) { var a = x0 + i * st.a * sc / st.d, b = x0 + (i + 1) * st.a * sc / st.d; s += '<path d="M' + a.toFixed(1) + ' ' + (y - 6) + ' Q' + ((a + b) / 2).toFixed(1) + ' ' + (y - 96) + ' ' + b.toFixed(1) + ' ' + (y - 6) + '" fill="none" stroke="#f08c1a" stroke-width="4"/>'; }
  s += '<circle cx="' + (x0 + tot * sc / st.d).toFixed(1) + '" cy="' + y + '" r="10" fill="#d63c7a" stroke="#fff" stroke-width="2.5"/>';
  $('nlModel').innerHTML = s + '</svg>';
  $('nlOut').innerHTML = '<b>' + st.j + ' × ' + T.frac(st.a, st.d) + ' = ' + T.frac(tot, st.d) + '</b>' + (tot >= st.d ? ' = <b>' + T.mixed(tot, st.d) + '</b>' : '') +
    '<br>' + T.frac(tot, st.d) + ' is ' + tot + ' copies of ' + T.frac(1, st.d) + ': ' + tot + ' × ' + T.frac(1, st.d) + '.' + (st.j > 1 && st.j <= 5 ? '<br>As addition: ' + new Array(st.j).fill(T.frac(st.a, st.d)).join(' + ') + ' = ' + T.frac(tot, st.d) : '');
  T.update({ d: st.d, a: st.a, j: st.j, tot: tot });
}
var CH = [{ text: 'Show 3 × 2/5. Where do you land?', test: function (s) { return s.d === 5 && s.a === 2 && s.j === 3; } },
  { text: 'Land exactly on 2 using jumps of 1/4.', test: function (s) { return s.d === 4 && s.a === 1 && s.tot === 8; } },
  { text: 'Land on 1 1/2 in two different ways.', test: (function () { var seen = {}; return function (s) { if (s.tot * 2 === s.d * 3) seen[s.d + ':' + s.a + ':' + s.j] = 1; return Object.keys(seen).length >= 2; }; })() },
  { text: 'Make a product that is between 2 and 3.', test: function (s) { return s.tot > 2 * s.d && s.tot < 3 * s.d; } }];
CH.forEach(function (c) { c.text = c.text.replace(/(\d+) (\d+)\/(\d+)/g, function (m, w, a, b) { return w + ' ' + T.frac(a, b); }).replace(/(^|[^>\d])(\d+)\/(\d+)/g, function (m, p, a, b) { return p + T.frac(a, b); }); });
reset();
INIT
T.steppers($('nlCtl'), function (k, dlt) { if (k === 'a') st.a = Math.max(1, Math.min(st.d * 2, st.a + dlt)); if (k === 'j') st.j = Math.max(0, Math.min(12, st.j + dlt)); if (st.a * st.j > st.d * 6) st.j = Math.floor(st.d * 6 / st.a); draw(); });
$('nlD').onchange = draw;
draw();""")

# ------------------------------------------------------------------ 6 Decimal Grids
tool("decimal-grids", ["fraction-operations-decimals"], "Decimal Grids",
     "Shade tenths and hundredths on a 10 by 10 grid. Read the amount as a fraction, as tenths plus hundredths, as a decimal and in words, and compare two decimals.",
     "Tap a column to shade a whole tenth, or use the buttons to add one hundredth at a time. Then compare with the second grid.", ["Decimals", "Tenths and hundredths", "Comparing decimals"], "4.NF.C.5, 4.NF.C.6, 4.NF.C.7",
     '<div class="tl-model" id="dgModel"></div><div class="tl-controls" id="dgCtl">' + step("a", "Grid A hundredths", "dgA") + step("at", "Grid A tenths", "dgAT") + step("b", "Grid B hundredths", "dgB") + step("bt", "Grid B tenths", "dgBT") + '</div><div class="tl-out" id="dgOut"></div>',
     r"""var st;
function reset() { st = { a: 25, b: 60 }; }
var W1 = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'], W10 = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
function w(n) { return n < 20 ? W1[n] : W10[Math.floor(n / 10)] + (n % 10 ? '-' + W1[n % 10] : ''); }
function dec(n) { return n === 100 ? '1.00' : '0.' + (n < 10 ? '0' : '') + n; }
function name(n) { return n === 100 ? 'one whole' : n === 0 ? 'zero' : n % 10 === 0 ? w(n / 10) + ' tenth' + (n === 10 ? '' : 's') + ', or ' + w(n) + ' hundredths' : w(n) + ' hundredth' + (n === 1 ? '' : 's'); }
function grid(x0, n, fill, id) {
  var s = '', u = 26;
  for (var i = 0; i < 100; i++) { var c = Math.floor(i / 10), r = i % 10; s += '<rect data-g="' + id + '" data-c="' + c + '" x="' + (x0 + c * u) + '" y="' + (16 + r * u) + '" width="' + u + '" height="' + u + '" fill="' + (i < n ? fill : '#fff') + '" stroke="#52627a" stroke-width="1"/>'; }
  return s + '<rect x="' + x0 + '" y="16" width="260" height="260" fill="none" stroke="#1d2a3a" stroke-width="3"/><text x="' + (x0 + 130) + '" y="306" text-anchor="middle" font-size="24" font-weight="800">' + (id === 'a' ? 'A' : 'B') + ': ' + dec(n) + '</text>';
}
function draw() {
  $('dgA').textContent = st.a; $('dgB').textContent = st.b; $('dgAT').textContent = Math.floor(st.a / 10); $('dgBT').textContent = Math.floor(st.b / 10);
  var cmp = st.a > st.b ? '>' : st.a < st.b ? '<' : '=';
  $('dgModel').innerHTML = '<svg viewBox="0 0 700 316" role="img" aria-label="Grid A has ' + st.a + ' of 100 squares shaded. Grid B has ' + st.b + ' of 100 squares shaded.">' + grid(30, st.a, '#ffc27a', 'a') +
    '<text x="350" y="160" text-anchor="middle" font-size="54" font-weight="900" fill="#d63c7a">' + cmp + '</text>' + grid(410, st.b, '#86d4e4', 'b') + '</svg>';
  var t = Math.floor(st.a / 10), h = st.a % 10;
  $('dgOut').innerHTML = '<b>Grid A:</b> ' + T.frac(st.a, 100) + (st.a < 100 ? ' = ' + T.frac(t, 10) + ' + ' + T.frac(h, 100) : '') + ' = <b>' + dec(st.a) + '</b>' + (h === 0 && st.a < 100 && st.a > 0 ? ' = <b>0.' + t + '</b>' : '') + ' (' + name(st.a) + ')' +
    '<br><b>Compare:</b> ' + dec(st.a) + ' ' + cmp + ' ' + dec(st.b) + ' because ' + st.a + ' hundredths is ' + (cmp === '>' ? 'more than' : cmp === '<' ? 'less than' : 'the same as') + ' ' + st.b + ' hundredths.';
  T.update({ a: st.a, b: st.b });
}
var CH = [{ text: 'Shade 0.4 on Grid A and 0.35 on Grid B. Which is greater?', test: function (s) { return s.a === 40 && s.b === 35; } },
  { text: 'Show that 0.7 and 0.70 are the same amount.', test: function (s) { return s.a === 70 && s.b === 70; } },
  { text: 'Shade 3 tenths and 4 hundredths on Grid A.', test: function (s) { return s.a === 34; } },
  { text: 'Make Grid B greater than 0.5 but less than 0.6.', test: function (s) { return s.b > 50 && s.b < 60; } }];
reset();
INIT
T.steppers($('dgCtl'), function (k, dlt) { var key = k.charAt(0), amt = k.length > 1 ? 10 * dlt : dlt; st[key] = Math.max(0, Math.min(100, st[key] + amt)); draw(); });
$('dgModel').addEventListener('click', function (e) { var r = e.target.closest('rect[data-g]'); if (!r) return; var g = r.dataset.g, c = +r.dataset.c + 1; st[g] = st[g] === c * 10 ? (c - 1) * 10 : c * 10; draw(); });
draw();""")

# ------------------------------------------------------------------ 7 Angle Explorer
tool("angle-explorer", ["geometry-angles-symmetry"], "Angle Explorer",
     "Turn a ray around a point and read the angle on a protractor. See the angle type, the fraction of a full turn, and how two angles add.",
     "Drag the slider (or the end of the blue ray) to turn the ray. Add a second angle to see angle measures add up.", ["Angles", "Protractor", "Degrees", "Adding angle measures"], "4.MD.C.5, 4.MD.C.6, 4.MD.C.7, 4.G.A.1",
     '<div class="tl-model" id="agModel"></div><div class="tl-controls">' + slider("agA", "First angle", 0, 180, 65) + slider("agB", "Second angle (added on)", 0, 180, 0) +
     '<button type="button" class="tl-btn" id="agP" aria-pressed="true">Protractor</button></div><div class="tl-out" id="agOut"></div>',
     r"""var st;
function reset() { st = { a: 65, b: 0, pro: true, seen: {} }; $('agA').value = 65; $('agB').value = 0; }
function pt(cx, cy, r, d) { var t = d * Math.PI / 180; return [cx + r * Math.cos(t), cy - r * Math.sin(t)]; }
function type(a) { return a === 0 ? 'zero angle' : a < 90 ? 'acute' : a === 90 ? 'right' : a < 180 ? 'obtuse' : a === 180 ? 'straight' : 'more than a straight angle'; }
function gcd(a, b) { return b ? gcd(b, a % b) : a; }
function draw() {
  st.a = +$('agA').value; st.b = Math.min(+$('agB').value, 360 - st.a); $('agB').value = st.b; $('agAV').textContent = st.a + '°'; $('agBV').textContent = st.b + '°';
  var cx = 380, cy = st.a + st.b > 180 ? 250 : 330, R = 230, s = '<svg viewBox="0 0 760 ' + (st.a + st.b > 180 ? 500 : 370) + '" role="img" aria-label="Angle of ' + st.a + ' degrees' + (st.b ? ' plus ' + st.b + ' degrees' : '') + '" id="agSvg">', t, p, q;
  if (st.pro) {
    s += '<path d="M' + (cx - R - 20) + ' ' + cy + ' A' + (R + 20) + ' ' + (R + 20) + ' 0 0 1 ' + (cx + R + 20) + ' ' + cy + 'Z" fill="#eef6ff" stroke="#7a8aa0" stroke-width="2"/>';
    for (t = 0; t <= 180; t += 5) { p = pt(cx, cy, R + 20, t); q = pt(cx, cy, R + 20 - (t % 10 ? 9 : 16), t); s += '<line x1="' + p[0].toFixed(1) + '" y1="' + p[1].toFixed(1) + '" x2="' + q[0].toFixed(1) + '" y2="' + q[1].toFixed(1) + '" stroke="#52627a" stroke-width="' + (t % 10 ? 1 : 1.8) + '"/>'; if (t % 10 === 0) { q = pt(cx, cy, R - 14, t); s += '<text x="' + q[0].toFixed(1) + '" y="' + (q[1] + (t === 0 || t === 180 ? -6 : 5)).toFixed(1) + '" text-anchor="middle" font-size="14" font-weight="700" fill="#33435a">' + t + '</text>'; } }
  }
  function arc(a0, a1, r, col) { var p0 = pt(cx, cy, r, a0), p1 = pt(cx, cy, r, a1); return '<path d="M' + p0[0].toFixed(1) + ' ' + p0[1].toFixed(1) + ' A' + r + ' ' + r + ' 0 ' + (a1 - a0 > 180 ? 1 : 0) + ' 0 ' + p1[0].toFixed(1) + ' ' + p1[1].toFixed(1) + '" fill="none" stroke="' + col + '" stroke-width="5"/>'; }
  if (st.a === 90 && !st.b) s += '<path d="M' + (cx + 30) + ' ' + cy + ' v-30 h-30" fill="none" stroke="#d63c7a" stroke-width="4"/>'; else if (st.a) s += arc(0, st.a, 60, '#2f7fd8');
  if (st.b) s += arc(st.a, st.a + st.b, 84, '#f08c1a');
  function ray(d, col, id) { var e = pt(cx, cy, R + 44, d); return '<line x1="' + cx + '" y1="' + cy + '" x2="' + e[0].toFixed(1) + '" y2="' + e[1].toFixed(1) + '" stroke="' + col + '" stroke-width="6" stroke-linecap="round"/>' + (id ? '<circle id="' + id + '" cx="' + e[0].toFixed(1) + '" cy="' + e[1].toFixed(1) + '" r="15" fill="' + col + '" stroke="#fff" stroke-width="3" style="cursor:grab"/>' : ''); }
  s += ray(0, '#1d2a3a') + ray(st.a, '#2f7fd8', 'agH') + (st.b ? ray(st.a + st.b, '#f08c1a') : '') + '<circle cx="' + cx + '" cy="' + cy + '" r="7" fill="#1d2a3a"/>';
  $('agModel').innerHTML = s + '</svg>';
  var g = gcd(st.a, 360), tot = st.a + st.b;
  $('agOut').innerHTML = '<b>' + st.a + '°</b> is a' + (/^[ao]/.test(type(st.a)) ? 'n' : '') + ' <b>' + type(st.a) + '</b> angle' + (st.a ? '. It is ' + T.frac(st.a / g, 360 / g) + ' of a full turn (360°).' : '.') +
    (st.b ? '<br><b>Adding angles:</b> ' + st.a + '° + ' + st.b + '° = <b>' + tot + '°</b> (' + type(tot) + ').' : '') + (st.a < 90 && st.a > 0 && !st.b ? '<br>To make a right angle you need ' + (90 - st.a) + '° more.' : '');
  st.seen[type(st.a)] = 1;
  T.update({ a: st.a, b: st.b, tot: tot, seen: st.seen });
}
var CH = [{ text: 'Make a right angle. What fraction of a full turn is it?', test: function (s) { return s.a === 90; } },
  { text: 'Make an acute angle, a right angle and an obtuse angle.', test: function (s) { return s.seen.acute && s.seen.right && s.seen.obtuse; } },
  { text: 'Use two angles to make a straight angle (180°).', test: function (s) { return s.a > 0 && s.b > 0 && s.tot === 180; } },
  { text: 'A right angle is split into 35° and another angle. Show both.', test: function (s) { return s.tot === 90 && (s.a === 35 || s.b === 35); } }];
reset();
INIT
$('agA').oninput = draw; $('agB').oninput = draw;
$('agP').onclick = function () { st.pro = !st.pro; this.setAttribute('aria-pressed', st.pro); draw(); };
var dragging = false;
$('agModel').addEventListener('pointerdown', function (e) { if (e.target.id === 'agH') { dragging = true; e.preventDefault(); } });
window.addEventListener('pointerup', function () { dragging = false; });
window.addEventListener('pointermove', function (e) {
  if (!dragging) return; var svg = $('agSvg'), r = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal;
  var x = (e.clientX - r.left) * vb.width / r.width - 380, y = (st.a + st.b > 180 ? 250 : 330) - (e.clientY - r.top) * vb.height / r.height;
  var d = Math.round(Math.atan2(y, x) * 180 / Math.PI); if (d < 0) d = d < -90 ? 180 : 0; $('agA').value = Math.max(0, Math.min(180, d)); draw();
});
draw();""")

# ------------------------------------------------------------------ 8 Area and Perimeter Explorer
tool("area-perimeter", ["measurement-unit-conversions"], "Area and Perimeter Explorer",
     "Stretch a rectangle on a grid and watch its area and perimeter change. Find rectangles with the same area and different perimeters, or the same perimeter and different areas.",
     "Change the length and the width. Count the squares inside (area) and the units around the edge (perimeter).", ["Area", "Perimeter", "Rectangles", "Formulas"], "4.MD.A.3",
     '<div class="tl-model" id="apModel"></div><div class="tl-controls">' + slider("apW", "Length", 1, 20, 5) + slider("apH", "Width", 1, 12, 3) +
     '<button type="button" class="tl-btn" id="apPin">Remember this rectangle</button></div><div class="tl-out" id="apOut"></div>',
     r"""var st;
function reset() { st = { w: 5, h: 3, pin: null, sameA: false, sameP: false }; $('apW').value = 5; $('apH').value = 3; }
function draw() {
  st.w = +$('apW').value; st.h = +$('apH').value; $('apWV').textContent = st.w + ' units'; $('apHV').textContent = st.h + ' units';
  var u = 28, s = '<svg viewBox="0 0 660 390" role="img" aria-label="Rectangle ' + st.w + ' units long and ' + st.h + ' units wide"><rect x="40" y="20" width="560" height="336" fill="#f7fafc"/>', i;
  for (i = 0; i <= 20; i++) s += '<line x1="' + (40 + i * u) + '" y1="20" x2="' + (40 + i * u) + '" y2="356" stroke="#d6e1f0" stroke-width="1"/>';
  for (i = 0; i <= 12; i++) s += '<line x1="40" y1="' + (20 + i * u) + '" x2="600" y2="' + (20 + i * u) + '" stroke="#d6e1f0" stroke-width="1"/>';
  if (st.pin) s += '<rect x="40" y="20" width="' + st.pin.w * u + '" height="' + st.pin.h * u + '" fill="none" stroke="#d63c7a" stroke-width="3" stroke-dasharray="8 6"/>';
  s += '<rect x="40" y="20" width="' + st.w * u + '" height="' + st.h * u + '" fill="#8fdcbf" fill-opacity=".8" stroke="#0d6b3c" stroke-width="4"/>';
  for (i = 1; i < st.w; i++) s += '<line x1="' + (40 + i * u) + '" y1="20" x2="' + (40 + i * u) + '" y2="' + (20 + st.h * u) + '" stroke="#0d6b3c" stroke-width="1"/>';
  for (i = 1; i < st.h; i++) s += '<line x1="40" y1="' + (20 + i * u) + '" x2="' + (40 + st.w * u) + '" y2="' + (20 + i * u) + '" stroke="#0d6b3c" stroke-width="1"/>';
  s += '<text x="' + (40 + st.w * u / 2) + '" y="' + (20 + st.h * u + 24) + '" text-anchor="middle" font-size="19" font-weight="800">' + st.w + '</text><text x="26" y="' + (20 + st.h * u / 2 + 6) + '" text-anchor="middle" font-size="19" font-weight="800">' + st.h + '</text>';
  $('apModel').innerHTML = s + '</svg>';
  var A = st.w * st.h, P = 2 * (st.w + st.h), msg = '';
  if (st.pin) {
    var A0 = st.pin.w * st.pin.h, P0 = 2 * (st.pin.w + st.pin.h), diff = !(st.pin.w === st.w && st.pin.h === st.h) && !(st.pin.w === st.h && st.pin.h === st.w);
    msg = '<br><b>Remembered (dashed):</b> ' + st.pin.w + ' by ' + st.pin.h + ', area ' + A0 + ', perimeter ' + P0 + '.' + (diff && A0 === A ? ' <b>Same area, different perimeter!</b>' : '') + (diff && P0 === P ? ' <b>Same perimeter, different area!</b>' : '');
    if (diff && A0 === A && P0 !== P) st.sameA = true; if (diff && P0 === P && A0 !== A) st.sameP = true;
  }
  $('apOut').innerHTML = '<b>Area</b> = length × width = ' + st.w + ' × ' + st.h + ' = <b>' + A + ' square units</b><br><b>Perimeter</b> = 2 × ' + st.w + ' + 2 × ' + st.h + ' = ' + 2 * st.w + ' + ' + 2 * st.h + ' = <b>' + P + ' units</b>' + msg;
  T.update({ w: st.w, h: st.h, A: A, P: P, sameA: st.sameA, sameP: st.sameP });
}
var CH = [{ text: 'Make a rectangle with an area of 24 square units.', test: function (s) { return s.A === 24; } },
  { text: 'Remember a rectangle, then make a different one with the same area.', test: function (s) { return s.sameA; } },
  { text: 'Remember a rectangle, then make a different one with the same perimeter.', test: function (s) { return s.sameP; } },
  { text: 'Make a square with a perimeter of 20 units. What is its area?', test: function (s) { return s.w === 5 && s.h === 5; } }];
reset();
INIT
$('apW').oninput = draw; $('apH').oninput = draw;
$('apPin').onclick = function () { st.pin = { w: st.w, h: st.h }; draw(); };
draw();""")

# ------------------------------------------------------------------ 9 Symmetry and Shapes
tool("symmetry-shapes", ["geometry-angles-symmetry"], "Symmetry and Shapes",
     "Choose a shape and turn a fold line through its center. The tool flips one side over the line so you can see whether the two parts match, and lists the shape's sides and angles.",
     "Pick a shape. Turn the dashed fold line. The pink outline shows the shape flipped over the line: when it matches the shape exactly, you found a line of symmetry.", ["Line of symmetry", "Classifying shapes", "Parallel and perpendicular sides"], "4.G.A.2, 4.G.A.3",
     '<div class="tl-model" id="syModel"></div><div class="tl-controls"><div class="tl-field"><label for="syS">Shape</label><select id="syS"></select></div>' + slider("syA", "Fold line turn", 0, 175, 90, 5) +
     '<button type="button" class="tl-btn" id="syF" aria-pressed="true">Show the flip</button></div><div class="tl-out" id="syOut"></div>',
     r"""var SH = {
  'square': [[-1, -1], [1, -1], [1, 1], [-1, 1]], 'rectangle': [[-1.6, -0.9], [1.6, -0.9], [1.6, 0.9], [-1.6, 0.9]],
  'equilateral triangle': [[0, 1.3], [-1.126, -0.65], [1.126, -0.65]], 'isosceles triangle': [[0, 1.5], [-0.9, -1], [0.9, -1]], 'right triangle': [[-1.3, -0.9], [1.5, -0.9], [-1.3, 1.1]],
  'rhombus': [[0, 1.1], [-1.7, 0], [0, -1.1], [1.7, 0]], 'parallelogram': [[-1.7, -0.8], [0.9, -0.8], [1.7, 0.8], [-0.9, 0.8]], 'trapezoid': [[-1.6, -0.8], [1.6, -0.8], [0.8, 0.8], [-0.8, 0.8]],
  'kite': [[0, 1.0], [-1.0, 0.2], [0, -1.6], [1.0, 0.2]],
  'regular pentagon': [0, 1, 2, 3, 4].map(function (k) { return [1.4 * Math.sin(2 * Math.PI * k / 5), 1.4 * Math.cos(2 * Math.PI * k / 5)]; }),
  'regular hexagon': [0, 1, 2, 3, 4, 5].map(function (k) { return [1.4 * Math.cos(Math.PI * k / 3), 1.4 * Math.sin(Math.PI * k / 3)]; }),
  'arrow': [[-1.6, -0.4], [0.2, -0.4], [0.2, -1.1], [1.7, 0], [0.2, 1.1], [0.2, 0.4], [-1.6, 0.4]]
};
var st;
function reset() { st = { shape: 'rectangle', a: 90, flip: true, found: {} }; $('syS').value = 'rectangle'; $('syA').value = 90; }
function refl(p, deg) { var t = deg * Math.PI / 180, c = Math.cos(2 * t), s = Math.sin(2 * t); return [p[0] * c + p[1] * s, p[0] * s - p[1] * c]; }
function isAxis(P, deg) { return P.every(function (p) { var r = refl(p, deg); return P.some(function (q) { return Math.abs(q[0] - r[0]) < 0.01 && Math.abs(q[1] - r[1]) < 0.01; }); }); }
function axes(P) { var out = []; for (var d = 0; d < 180; d += 5) if (isAxis(P, d)) out.push(d); return out; }
function props(P) {
  var n = P.length, v = [], par = 0, right = 0, i, j;
  for (i = 0; i < n; i++) v.push([P[(i + 1) % n][0] - P[i][0], P[(i + 1) % n][1] - P[i][1]]);
  for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) if (Math.abs(v[i][0] * v[j][1] - v[i][1] * v[j][0]) < 1e-6) par++;
  for (i = 0; i < n; i++) { var a = v[(i + n - 1) % n], b = v[i]; if (Math.abs(a[0] * b[0] + a[1] * b[1]) < 1e-6) right++; }
  return { sides: n, par: par, right: right };
}
function draw() {
  st.shape = $('syS').value; st.a = +$('syA').value; $('syAV').textContent = st.a + '°';
  var P = SH[st.shape], cx = 380, cy = 190, sc = 105, X = function (p) { return (cx + p[0] * sc).toFixed(1) + ',' + (cy - p[1] * sc).toFixed(1); };
  var ok = isAxis(P, st.a), all = axes(P), t = st.a * Math.PI / 180, dx = Math.cos(t) * 330, dy = Math.sin(t) * 330;
  var s = '<svg viewBox="0 0 760 380" role="img" aria-label="' + st.shape + ' with a fold line turned ' + st.a + ' degrees. ' + (ok ? 'The two parts match.' : 'The two parts do not match.') + '">';
  s += '<polygon points="' + P.map(X).join(' ') + '" fill="#c3a6f0" stroke="#1d2a3a" stroke-width="4" stroke-linejoin="round"/>';
  if (st.flip) s += '<polygon points="' + P.map(function (p) { return X(refl(p, st.a)); }).join(' ') + '" fill="' + (ok ? 'none' : 'rgba(214,60,122,.12)') + '" stroke="#d63c7a" stroke-width="3" stroke-dasharray="' + (ok ? '0' : '9 7') + '" stroke-linejoin="round"/>';
  s += '<line x1="' + (cx - dx) + '" y1="' + (cy + dy) + '" x2="' + (cx + dx) + '" y2="' + (cy - dy) + '" stroke="' + (ok ? '#16865c' : '#52627a') + '" stroke-width="4" stroke-dasharray="12 8"/>';
  $('syModel').innerHTML = s + '</svg>';
  if (ok) st.found[st.shape + ':' + st.a] = 1;
  var mine = all.filter(function (d) { return st.found[st.shape + ':' + d]; }).length, pr = props(P);
  $('syOut').innerHTML = (ok ? '<b style="color:#16865c">Yes! This fold line is a line of symmetry.</b> The flipped shape lands exactly on the shape.' : '<b>Not a line of symmetry.</b> The flipped shape (pink) does not match.') +
    '<br>You have found <b>' + mine + '</b> line' + (mine === 1 ? '' : 's') + ' of symmetry for this ' + st.shape + '. Keep turning the line to look for more.' +
    '<br><b>Sides and angles:</b> ' + pr.sides + ' sides, ' + pr.par + ' pair' + (pr.par === 1 ? '' : 's') + ' of parallel sides, ' + pr.right + ' right angle' + (pr.right === 1 ? '' : 's') + '.';
  T.update({ shape: st.shape, a: st.a, ok: ok, found: st.found, mine: mine, total: all.length });
}
var CH = [{ text: 'Find both lines of symmetry of the rectangle.', test: function (s) { return s.found['rectangle:0'] && s.found['rectangle:90']; } },
  { text: 'Find all 4 lines of symmetry of the square.', test: function (s) { return [0, 45, 90, 135].every(function (d) { return s.found['square:' + d]; }); } },
  { text: 'Find a shape with no lines of symmetry. Check every turn.', test: (function () { var tried = {}; return function (s) { if (s.total === 0) { tried[s.shape + ':' + s.a] = 1; return Object.keys(tried).filter(function (k) { return k.indexOf(s.shape + ':') === 0; }).length >= 6; } return false; }; })() },
  { text: 'Find a shape with exactly 1 line of symmetry.', test: function (s) { return s.total === 1 && s.mine === 1; } }];
Object.keys(SH).forEach(function (k) { var o = document.createElement('option'); o.textContent = k; $('syS').appendChild(o); });
reset();
INIT
$('syS').onchange = draw; $('syA').oninput = draw;
$('syF').onclick = function () { st.flip = !st.flip; this.setAttribute('aria-pressed', st.flip); draw(); };
draw();""")

NOTES = {
    "math4-place-value-blocks": (["Ask students to predict the number before they read it, then build the same number with different blocks (for example 13 tens instead of 1 hundred 3 tens).", "Use × 10 to show that every digit moves one place to the left (4.NBT.A.1).", "Connect Regroup to the regrouping step in addition and subtraction."],
                                 ["A digit's value depends on its place: 4 tens is 40, 4 hundreds is 400.", "10 of any block can be traded for 1 of the next larger block.", "Multiplying by 10 moves every digit one place to the left."]),
    "math4-array-area-models": (["Start with dots for small numbers, then switch to the area model for larger ones.", "Have students choose their own split and compare: every split gives the same product.", "Link the two boxes to the partial products they write on paper."],
                                ["Splitting the array does not change the total number of dots.", "Splitting at a ten makes the multiplication easier.", "The numbers of rows and columns are a factor pair of the product."]),
    "math4-division-groups": (["Ask what the remainder would mean in a story: drop it, add one more group, or use it as the answer.", "Switch to rows to connect division with arrays and multiplication.", "Have students find all divisors of 24 that leave no remainder (its factors)."],
                              ["The remainder is always less than the divisor.", "divisor × quotient + remainder = dividend.", "When the remainder is 0, the divisor is a factor of the dividend."]),
    "math4-equivalent-fractions": (["Before cutting, ask: will the shaded amount change? Then cut and compare.", "Have students record each equation: 2/3 = (2 × 4)/(3 × 4) = 8/12.", "Use the dashed line to show the shading ends at the same place."],
                                   ["Cutting every part into the same number of pieces multiplies the numerator and the denominator by that number.", "The pieces get smaller but there are more of them, so the amount stays the same.", "A fraction is in simplest form when no number greater than 1 divides both parts."]),
    "math4-fraction-number-line": (["Use jumps of a unit fraction first (numerator 1) to show a/b as a copies of 1/b.", "Ask students to predict where the jumps will land before they press +.", "Connect repeated addition with multiplication of a fraction by a whole number."],
                                   ["A fraction a/b is a copies of the unit fraction 1/b.", "n × a/b = (n × a)/b: multiply the numerator, keep the denominator.", "When the numerator is greater than the denominator, the fraction is more than 1 and can be written as a mixed number."]),
    "math4-decimal-grids": (["Tap a whole column to show one tenth is ten hundredths.", "Compare 0.4 and 0.35 before revealing the symbol: many students expect 0.35 to be greater.", "Have students say each amount two ways: as tenths and hundredths, and as hundredths only."],
                            ["One tenth is the same as ten hundredths: 0.4 = 0.40.", "To compare decimals, think of both as hundredths.", "More digits does not mean a greater number."]),
    "math4-angle-explorer": (["Hide the protractor and have students estimate before they measure.", "Use the second angle to model unknown-angle problems: 35° + x = 90°.", "Link 90°, 180° and 360° to quarter, half and full turns."],
                             ["An angle is measured by how far one ray turns from the other, not by how long the rays are.", "Acute angles are less than 90°, right angles are exactly 90°, obtuse angles are between 90° and 180°.", "When two angles share a ray and do not overlap, their measures add."]),
    "math4-area-perimeter": (["Have students record rectangles with a perimeter of 20 in a table and look for the greatest area.", "Ask which measurement a fence needs and which a carpet needs.", "Use Remember to compare two rectangles side by side."],
                             ["Area counts the squares inside; perimeter counts the units around the edge.", "Rectangles with the same area can have different perimeters.", "Rectangles with the same perimeter can have different areas; the square has the greatest area."]),
    "math4-symmetry-shapes": (["Ask students to predict the number of lines of symmetry before they turn the line.", "Compare the rectangle and the parallelogram: why is the diagonal not a line of symmetry?", "Use the sides and angles line to sort shapes by parallel sides and right angles."],
                              ["A line of symmetry folds a shape into two parts that match exactly.", "Not every line through the middle is a line of symmetry.", "Regular shapes have as many lines of symmetry as they have sides."]),
}


def main():
    manifest = []
    for t in TOOLS:
        teacher, notice = NOTES[t["slug"]]
        init = INIT.format(unit=t["units"][0], title=t["title"].replace("'", "\\'"), standards=t["standards"], teacher=json.dumps(teacher, ensure_ascii=False), notice=json.dumps(notice, ensure_ascii=False))
        script = t["script"].replace("\nINIT\n", "\n" + init + "\n")
        assert "INIT" not in script.replace("T.init", ""), t["slug"]
        html = PAGE.format(title=t["title"], desc=t["description"], intro=t["intro"], body=t["body"], script=script, v=V)
        d = os.path.join(ROOT, "artifacts", t["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html)
        manifest.append({k: t[k] for k in ("slug", "units", "title", "description", "topics", "standards")})
    json.dump({"tools": manifest}, open(os.path.join(HERE, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(manifest), "interactive tools written")


if __name__ == "__main__":
    main()
