"""Grade 2 Interactive Math tools (math2-*)."""
from reg import tool

G = 2

# ------------------------------------------------------------------ Place-Value Blocks to 1,000
tool(G, "place-value-blocks", ["place-value-1000", "count-compare-1000", "add-subtract-1000"], "Place-Value Blocks to 1,000",
     "Build three-digit numbers with hundreds flats, tens rods and ones cubes. Bundle and break apart blocks, and see standard, expanded and word form.",
     "Use + and − to add blocks. Bundle 10 ones into a ten or 10 tens into a hundred, or break a block apart.",
     ["Hundreds, tens and ones", "Expanded form", "Regrouping"], "2.NBT.A.1, 2.NBT.A.3, 2.NBT.B.7",
     """<div class="tl-model" id="pvModel"></div><div class="tl-big" id="pvNum" aria-live="polite"></div>
<div class="tl-controls" id="pvCtl"></div>
<div class="tl-controls" style="margin-top:.6rem"><button type="button" class="tl-btn" id="pvB1">Bundle 10 ones → 1 ten</button><button type="button" class="tl-btn" id="pvB2">Bundle 10 tens → 1 hundred</button><button type="button" class="tl-btn" id="pvK2">Break 1 hundred → 10 tens</button><button type="button" class="tl-btn" id="pvK1">Break 1 ten → 10 ones</button></div>
<div class="tl-out" id="pvOut"></div>""",
     r"""
var st;
function reset() { st = { h: 1, t: 2, o: 5, bundT: 0, ways: {}, msg: '' }; draw(); }
function val() { return 100 * st.h + 10 * st.t + st.o; }
function draw() {
  var s = '', i, k, n = val();
  for (i = 0; i < st.h; i++) {
    var x = 10 + (i % 5) * 96, y = 10 + Math.floor(i / 5) * 100;
    s += '<rect x="' + x + '" y="' + y + '" width="88" height="88" fill="#fbbf24" stroke="#92400e" stroke-width="2"/>';
    for (k = 1; k < 10; k++) s += '<line x1="' + (x + k * 8.8) + '" y1="' + y + '" x2="' + (x + k * 8.8) + '" y2="' + (y + 88) + '" stroke="#92400e" stroke-width=".8"/><line x1="' + x + '" y1="' + (y + k * 8.8) + '" x2="' + (x + 88) + '" y2="' + (y + k * 8.8) + '" stroke="#92400e" stroke-width=".8"/>';
  }
  for (i = 0; i < st.t; i++) { var rx = 500 + (i % 15) * 13, ry = 10 + Math.floor(i / 15) * 100; s += '<rect x="' + rx + '" y="' + ry + '" width="9" height="88" fill="#34d399" stroke="#065f46" stroke-width="1.5"/>'; }
  for (i = 0; i < st.o; i++) s += '<rect x="' + (710 + (i % 5) * 19) + '" y="' + (10 + Math.floor(i / 5) * 19) + '" width="14" height="14" fill="#60a5fa" stroke="#1e3a8a" stroke-width="1.5"/>';
  var H = 40 + Math.max(100, Math.ceil(st.h / 5) * 100, Math.ceil(st.t / 15) * 100, Math.ceil(st.o / 5) * 19 + 10);
  [['Hundreds', 245, st.h], ['Tens', 595, st.t], ['Ones', 755, st.o]].forEach(function (p) { s += K.txt(p[1], H - 12, p[0] + ': ' + p[2], { size: 19 }); });
  $('pvModel').innerHTML = K.svg(820, H, s, st.h + ' hundreds, ' + st.t + ' tens and ' + st.o + ' ones');
  $('pvNum').textContent = n === 1000 ? '1,000' : n;
  $('pvCtl').innerHTML = K.step('h', 'Hundreds', [1], st.h) + K.step('t', 'Tens', [1], st.t) + K.step('o', 'Ones', [1], st.o);
  var dh = Math.floor(n / 100), dt = Math.floor(n / 10) % 10, d1 = n % 10;
  var exp = n === 1000 ? '1,000' : [dh * 100, dt * 10, d1].filter(function (v) { return v; }).join(' + ') || '0';
  var out = '<b>Blocks:</b> ' + st.h + ' hundred' + (st.h === 1 ? '' : 's') + ', ' + st.t + ' ten' + (st.t === 1 ? '' : 's') + ', ' + st.o + ' one' + (st.o === 1 ? '' : 's') + '<br><b>Expanded form:</b> ' + exp + '<br><b>Word form:</b> ' + K.words(n);
  if (st.o >= 10 || st.t >= 10) out += '<br>You have 10 or more ' + (st.o >= 10 ? 'ones' : 'tens') + '. You can bundle them!';
  if (st.msg) out += '<br>' + st.msg;
  $('pvOut').innerHTML = out; st.msg = '';
  ['B1', 'B2', 'K2', 'K1'].forEach(function (b, i) { $('pv' + b).disabled = [st.o < 10, st.t < 10, st.h < 1 || st.t > 20, st.t < 1 || st.o > 20][i]; });
  var key = st.h + ',' + st.t + ',' + st.o; (st.ways[n] = st.ways[n] || {})[key] = 1;
  T.update({ n: n, h: st.h, t: st.t, o: st.o, bundT: st.bundT, ways: st.ways });
}
var CH = [
  { text: 'Build 347 with hundreds, tens and ones.', test: function (s) { return s.h === 3 && s.t === 4 && s.o === 7; } },
  { text: 'Build 405. Which place has no blocks?', test: function (s) { return s.h === 4 && s.t === 0 && s.o === 5; } },
  { text: 'Show 160 using only tens.', test: function (s) { return s.h === 0 && s.t === 16 && s.o === 0; } },
  { text: 'Get 10 tens, then bundle them into a hundred.', test: function (s) { return s.bundT > 0; } },
  { text: 'Build 1,000. How many hundreds is that?', test: function (s) { return s.n === 1000; } },
  { text: 'Show 512 in two different ways.', test: function (s) { return s.ways[512] && Object.keys(s.ways[512]).length >= 2; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
T.steppers($('pvCtl'), function (k, d) {
  var v = st[k] + d, max = { h: 10, t: 30, o: 30 }[k];
  if (v < 0 || v > max) return;
  if (val() + d * { h: 100, t: 10, o: 1 }[k] > 1000) { st.msg = 'This tool builds numbers up to 1,000.'; return draw(); }
  st[k] = v; draw();
});
$('pvB1').onclick = function () { st.o -= 10; st.t++; draw(); };
$('pvB2').onclick = function () { st.t -= 10; st.h++; st.bundT++; draw(); };
$('pvK2').onclick = function () { st.h--; st.t += 10; draw(); };
$('pvK1').onclick = function () { st.t--; st.o += 10; draw(); };
reset();
""",
     [("Build 628. Write it in expanded form.", "600 + 20 + 8"),
      ("How many tens are in 340? (Hint: show it with only tens.)", "34 tens"),
      ("Build 9 hundreds, 0 tens and 6 ones. What number is it?", "906"),
      ("Build 715. Write it in word form.", "seven hundred fifteen"),
      ("How many hundreds make 1,000?", "10 hundreds"),
      ("Compare 482 and 428. Write >, = or <.", "482 > 428, because 8 tens is more than 2 tens"),
      ("Reflect: Why do we write a 0 in 405?", "There are no tens. The 0 holds the tens place so the 4 still means 4 hundreds.")],
     ["Each place is worth 10 of the place to its right: 10 ones = 1 ten, 10 tens = 1 hundred.",
      "Bundling or breaking blocks changes how the number looks, not how much it is.",
      "A 0 holds a place when there are none of that block: 405 has no tens.",
      "Expanded form shows the value of each digit: 347 = 300 + 40 + 7."],
     ["Ask for two ways to build the same number (512 = 5 hundreds 1 ten 2 ones = 4 hundreds 11 tens 2 ones).",
      "Use Break to prepare for subtraction with regrouping: “I need more tens, so I break a hundred.”",
      "Compare numbers by building both and comparing hundreds first, then tens, then ones."])

# ------------------------------------------------------------------ Number Line Jumps
tool(G, "number-line-jumps", ["add-subtract-100", "add-subtract-1000", "length-number-line", "count-compare-1000"], "Number Line Jumps",
     "Jump forward and back on an open number line by ones, tens and hundreds. Every trip becomes an addition or subtraction equation.",
     "Set a start number. Then jump with the + and − buttons. The number line grows to show your whole trip.",
     ["Adding on a number line", "Subtracting on a number line", "Counting by 10s and 100s"], "2.MD.B.6, 2.NBT.B.5, 2.NBT.B.7, 2.NBT.B.8",
     """<div class="tl-model" id="nlModel"></div><div class="tl-big" id="nlEq" aria-live="polite"></div>
<div class="tl-controls" id="nlCtl"></div>
<div class="tl-controls" id="nlJump" style="margin-top:.6rem;align-items:center"><span class="lab" style="font-weight:800">Jump:</span>
<button type="button" class="tl-btn" data-j="-100">−100</button><button type="button" class="tl-btn" data-j="-10">−10</button><button type="button" class="tl-btn" data-j="-1">−1</button>
<button type="button" class="tl-btn" data-j="1">+1</button><button type="button" class="tl-btn" data-j="10">+10</button><button type="button" class="tl-btn" data-j="100">+100</button><button type="button" class="tl-btn" id="nlClear">Clear jumps</button></div>
<div class="tl-out" id="nlOut"></div>""",
     r"""
var st;
function reset() { st = { start: 20, jumps: [], msg: '' }; draw(); }
function pos() { return st.start + st.jumps.reduce(function (a, b) { return a + b; }, 0); }
function draw() {
  var pts = [st.start], p = st.start;
  st.jumps.forEach(function (j) { p += j; pts.push(p); });
  var lo = Math.min.apply(null, pts), hi = Math.max.apply(null, pts);
  if (hi - lo < 10) { lo -= 5; hi += 5; }
  var span = hi - lo;
  var tick = [1, 2, 5, 10, 20, 50, 100].filter(function (t) { return span / t <= 24; })[0] || 100;
  lo = Math.max(0, Math.floor((lo - span * 0.08) / tick) * tick); hi = Math.ceil((hi + span * 0.08) / tick) * tick; if (hi - lo < tick * 4) hi = lo + tick * 4;
  var W = 800, X0 = 30, X1 = 770, sc = function (v) { return X0 + (v - lo) / (hi - lo) * (X1 - X0); }, Y = 150, s = '';
  s += '<line x1="' + (X0 - 14) + '" y1="' + Y + '" x2="' + (X1 + 14) + '" y2="' + Y + '" stroke="#1d2a3a" stroke-width="3"/>';
  for (var v = lo; v <= hi; v += tick) s += '<line x1="' + sc(v) + '" y1="' + (Y - 8) + '" x2="' + sc(v) + '" y2="' + (Y + 8) + '" stroke="#1d2a3a" stroke-width="2"/>' + K.txt(sc(v), Y + 30, v, { size: 14, w: 700, fill: '#55657a' });
  // group consecutive jumps of the same size into one arc each so long trips stay readable
  var groups = [], i;
  st.jumps.forEach(function (j) { var g = groups[groups.length - 1]; if (g && g.j === j && g.n < 9) g.n++; else groups.push({ j: j, n: 1 }); });
  p = st.start;
  groups.forEach(function (g) {
    for (i = 0; i < g.n; i++) {
      var a = sc(p), b = sc(p + g.j), up = g.j > 0, h = Math.min(70, 18 + Math.abs(b - a) * 0.45);
      s += '<path d="M' + a + ' ' + Y + ' Q' + ((a + b) / 2) + ' ' + (up ? Y - h * 2 : Y + h * 2) + ' ' + b + ' ' + Y + '" fill="none" stroke="' + (up ? '#1fa565' : '#f08c1a') + '" stroke-width="3.5"/>';
      if (Math.abs(b - a) > 26 || g.n === 1) s += K.txt((a + b) / 2, up ? Y - h - 6 : Y + h + 22, (up ? '+' : '−') + Math.abs(g.j), { size: 15, fill: up ? '#0d6b3c' : '#b45309' });
      p += g.j;
    }
  });
  s += '<circle cx="' + sc(st.start) + '" cy="' + Y + '" r="9" fill="#1f78c8"/>' + K.txt(sc(st.start), 26, 'start ' + st.start, { size: 15, fill: '#1f78c8' });
  s += '<circle cx="' + sc(pos()) + '" cy="' + Y + '" r="9" fill="#d63c7a"/>';
  $('nlModel').innerHTML = K.svg(W, 260, s, 'Number line from ' + lo + ' to ' + hi + '. Start ' + st.start + ', now at ' + pos());
  $('nlCtl').innerHTML = K.step('start', 'Start number', [1, 10, 100], st.start);
  var tot = pos() - st.start;
  $('nlEq').textContent = st.jumps.length ? st.start + (tot >= 0 ? ' + ' : ' − ') + Math.abs(tot) + ' = ' + pos() : 'Start: ' + st.start;
  var count = {}; st.jumps.forEach(function (j) { count[j] = (count[j] || 0) + 1; });
  var out = st.jumps.length ? '<b>Your jumps:</b> ' + Object.keys(count).sort(function (a, b) { return Math.abs(b) - Math.abs(a); }).map(function (j) { return count[j] + ' jump' + (count[j] > 1 ? 's' : '') + ' of ' + (j > 0 ? '+' : '−') + Math.abs(j); }).join(', ') + '. You moved <b>' + Math.abs(tot) + '</b> ' + (tot >= 0 ? 'forward' : 'back') + ' and landed on <b>' + pos() + '</b>.' : 'Press a jump button to start your trip.';
  if (st.msg) out += '<br>' + st.msg;
  $('nlOut').innerHTML = out; st.msg = '';
  T.update({ start: st.start, pos: pos(), jumps: st.jumps.slice() });
}
var CH = [
  { text: 'Start at 47. Jump to 72. How far did you go?', test: function (s) { return s.start === 47 && s.pos === 72; } },
  { text: 'Show 63 − 28 by jumping back from 63.', test: function (s) { return s.start === 63 && s.pos === 35; } },
  { text: 'Count up from 38 to 100. How far is it?', test: function (s) { return s.start === 38 && s.pos === 100; } },
  { text: 'Start at 250 and jump +100 three times.', test: function (s) { return s.start === 250 && s.pos === 550 && s.jumps.filter(function (j) { return j === 100; }).length >= 3; } },
  { text: 'Show 300 − 1. What number comes just before 300?', test: function (s) { return s.start === 300 && s.pos === 299; } },
  { text: 'Land exactly on 1,000.', test: function (s) { return s.pos === 1000; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
T.steppers($('nlCtl'), function (k, d) { st.start = K.clamp(st.start + d, 0, 1000); st.jumps = []; draw(); });
$('nlJump').addEventListener('click', function (e) { var b = e.target.closest('[data-j]'); if (!b) return; var j = +b.dataset.j, v = pos() + j; if (v < 0 || v > 1000) { st.msg = 'This number line goes from 0 to 1,000.'; return draw(); } if (st.jumps.length >= 60) { st.msg = 'That is a lot of jumps! Press Clear jumps to start a new trip.'; return draw(); } st.jumps.push(j); draw(); });
$('nlClear').onclick = function () { st.jumps = []; draw(); };
reset();
""",
     [("Start at 56. Jump +10 three times. Where do you land? Write the equation.", "86. 56 + 30 = 86"),
      ("Start at 74. Jump −10 four times. Where do you land?", "34 (74 − 40 = 34)"),
      ("Show 45 + 27 with jumps. Which jumps did you use? What is the sum?", "For example +10, +10, +1 seven times (or +10, +10, +7). The sum is 72."),
      ("Show 92 − 18 by jumping back. What is the difference?", "74"),
      ("Count up from 68 to 100. How far is it?", "32 (for example +2 to 70, then +10 three times)"),
      ("Start at 450 and jump +100 three times. Where do you land?", "750"),
      ("Reflect: Why is it faster to jump by tens than by ones?", "One jump of 10 does the work of ten jumps of 1.")],
     ["Jumping forward adds; jumping back subtracts.",
      "Counting up from the smaller number to the bigger one finds the difference.",
      "Jumps of 10 and 100 are fast: 3 jumps of +100 add 300.",
      "Landing on a ten (like 70) first makes the next jumps easy."],
     ["Ask for two different jump plans for the same problem and compare which is faster.",
      "For length problems, treat the number line as a ruler: a ribbon 45 cm long plus 27 cm more.",
      "The equation shows the total distance, so students can check a plan with many small jumps."])

# ------------------------------------------------------------------ Arrays and Odd/Even
tool(G, "array-builder", ["odd-even-arrays"], "Arrays and Odd or Even",
     "Build arrays up to 5 rows and 5 columns and write the total as repeated addition. Pair up counters to see whether a number is odd or even.",
     "Set the rows and columns of the array. Below, choose a number and see whether every counter has a partner.",
     ["Arrays", "Repeated addition", "Odd and even"], "2.OA.C.3, 2.OA.C.4",
     """<div class="tl-model" id="arModel"></div><div class="tl-controls" id="arCtl"></div><div class="tl-out" id="arOut"></div>
<h2 style="margin-top:.9rem">Odd or even?</h2><div class="tl-model" id="oeModel"></div><div class="tl-controls" id="oeCtl"></div><div class="tl-out" id="oeOut"></div>""",
     r"""
var st;
function reset() { st = { r: 2, c: 3, n: 9, seen: {} }; draw(); }
function draw() {
  var s = '', i, j, N = st.r * st.c;
  for (i = 0; i < st.r; i++) { s += '<rect x="20" y="' + (12 + i * 60) + '" width="' + (st.c * 60 + 10) + '" height="52" rx="12" fill="' + (i % 2 ? '#eef7ff' : '#f2fbf5') + '"/>'; for (j = 0; j < st.c; j++) s += '<circle cx="' + (55 + j * 60) + '" cy="' + (38 + i * 60) + '" r="21" fill="#e5484d" stroke="#8c1d22" stroke-width="3"/>'; }
  $('arModel').innerHTML = K.svg(Math.max(360, st.c * 60 + 40), st.r * 60 + 20, s, st.r + ' rows of ' + st.c);
  $('arCtl').innerHTML = K.step('r', 'Rows', [1], st.r) + K.step('c', 'Columns', [1], st.c);
  var rows = [], cols = []; for (i = 0; i < st.r; i++) rows.push(st.c); for (i = 0; i < st.c; i++) cols.push(st.r);
  $('arOut').innerHTML = '<b>' + st.r + '</b> row' + (st.r > 1 ? 's' : '') + ' of <b>' + st.c + '</b> = <b>' + N + '</b> in all.<br>Add the rows: ' + rows.join(' + ') + ' = ' + N + '<br>Add the columns: ' + cols.join(' + ') + ' = ' + N;
  st.seen[st.r + 'x' + st.c] = 1;
  var o = '', k = Math.floor(st.n / 2), odd = st.n % 2;
  for (i = 0; i < k; i++) { o += '<rect x="' + (14 + i * 44) + '" y="8" width="36" height="84" rx="12" fill="#f2fbf5" stroke="#9fd8b8" stroke-width="2"/><circle cx="' + (32 + i * 44) + '" cy="30" r="14" fill="#1f78c8"/><circle cx="' + (32 + i * 44) + '" cy="70" r="14" fill="#1f78c8"/>'; }
  if (odd) o += '<circle cx="' + (32 + k * 44) + '" cy="30" r="14" fill="#f08c1a" stroke="#1d2a3a" stroke-width="2.5" stroke-dasharray="4 3"/>' + K.txt(32 + k * 44, 76, 'no partner', { size: 11, fill: '#b45309' });
  $('oeModel').innerHTML = K.svg(Math.max(460, (k + 1) * 44 + 40), 100, o, st.n + ' counters in pairs');
  $('oeCtl').innerHTML = K.step('n', 'How many counters', [1], st.n);
  $('oeOut').innerHTML = odd ? '<b>' + st.n + ' is odd.</b> One counter has no partner: ' + st.n + ' = ' + k + ' + ' + k + ' + 1.' : '<b>' + st.n + ' is even.</b> Every counter has a partner: ' + st.n + ' = ' + k + ' + ' + k + '.';
  T.update({ r: st.r, c: st.c, total: N, n: st.n, seen: Object.assign({}, st.seen) });
}
var CH = [
  { text: 'Make 3 rows of 4.', test: function (s) { return s.r === 3 && s.c === 4; } },
  { text: 'Make 4 rows of 3. Is the total the same as 3 rows of 4?', test: function (s) { return s.seen['3x4'] && s.seen['4x3']; } },
  { text: 'Make an array with 10 in all.', test: function (s) { return s.total === 10; } },
  { text: 'Show 7 counters. Is 7 odd or even?', test: function (s) { return s.n === 7; } },
  { text: 'Show 14 as a double: 14 = ? + ?', test: function (s) { return s.n === 14; } },
  { text: 'Make an array with 5 columns and 20 in all.', test: function (s) { return s.c === 5 && s.total === 20; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
function step(k, d) { st[k] = K.clamp(st[k] + d, 1, k === 'n' ? 20 : 5); draw(); }
T.steppers($('arCtl'), step); T.steppers($('oeCtl'), step);
reset();
""",
     [("Make 2 rows of 5. Write an addition equation for the total.", "5 + 5 = 10"),
      ("Make 4 rows of 3. Write the total as repeated addition.", "3 + 3 + 3 + 3 = 12"),
      ("How many in all are in 5 rows of 5?", "25"),
      ("Is 13 odd or even? Write it as a double plus 1.", "Odd. 13 = 6 + 6 + 1"),
      ("Is 18 odd or even? Write it as a double.", "Even. 18 = 9 + 9"),
      ("Find two different arrays with 12 in all (5 rows or fewer, 5 columns or fewer).", "3 rows of 4 and 4 rows of 3"),
      ("Reflect: How can you tell if a number is even by pairing counters?", "If every counter has a partner, the number is even.")],
     ["An array has equal rows. Adding the rows or the columns gives the same total.",
      "3 rows of 4 and 4 rows of 3 have the same total.",
      "Even numbers can be split into two equal groups (a double). Odd numbers have one left over.",
      "Even numbers end in 0, 2, 4, 6 or 8."],
     ["Ask students to say each array two ways: “3 rows of 4” and “4 columns of 3.”",
      "Connect to real arrays: egg cartons, windows, chairs in rows.",
      "For odd and even, ask: Can two friends share these equally?"])

# ------------------------------------------------------------------ Bar Models
tool(G, "bar-model", ["word-problems-100", "add-subtract-20", "add-subtract-100"], "Bar Model Builder",
     "Show word problems with tape diagrams: part-part-whole stories and compare stories. Hide the unknown, write the equation and check the answer.",
     "Choose a story type. Set the numbers, choose what is unknown, and use Show answer to check your thinking.",
     ["Word problems", "Part-part-whole", "Compare problems"], "2.OA.A.1, 2.NBT.B.5",
     """<div class="tl-controls el-view" role="group" aria-label="Story type"><button type="button" class="tl-btn" data-mode="ppw">Parts and whole</button><button type="button" class="tl-btn" data-mode="cmp">Compare</button></div>
<div class="tl-out" id="bmStory" style="margin:0 0 .6rem"></div><div class="tl-model" id="bmModel"></div><div class="tl-big" id="bmEq" aria-live="polite"></div>
<div class="tl-controls" id="bmCtl"></div><div class="tl-controls" id="bmUnk" style="margin-top:.6rem"></div><div class="tl-out" id="bmOut"></div>""",
     r"""
var st;
function reset() { st = { mode: 'ppw', a: 24, b: 13, unk: 'whole', shown: false, x: 45, y: 28 }; draw(); }
function seg(x, y, w, h, fill, label) { return '<rect x="' + x + '" y="' + y + '" width="' + Math.max(w, 2) + '" height="' + h + '" fill="' + fill + '" stroke="#1d2a3a" stroke-width="2.5"/>' + (w > 30 ? K.txt(x + w / 2, y + h / 2 + 8, label, { size: 22 }) : ''); }
function draw() {
  Array.prototype.forEach.call(document.querySelectorAll('[data-mode]'), function (b) { b.setAttribute('aria-pressed', b.dataset.mode === st.mode); });
  var s = '', W = 700, X = 40, eq, story, ans;
  if (st.mode === 'ppw') {
    var whole = st.a + st.b, u = whole ? W / Math.max(whole, 1) : 0, q = function (k, v) { return st.unk === k && !st.shown ? '?' : v; };
    s += '<path d="M' + X + ' 30 v-12 h' + W + ' v12" fill="none" stroke="#1d2a3a" stroke-width="2.5"/>' + K.txt(X + W / 2, 14, 'Whole: ' + q('whole', whole), { size: 20 });
    s += seg(X, 40, st.a * u, 70, '#bfe6d0', q('a', st.a)) + seg(X + st.a * u, 40, st.b * u, 70, '#cde7ff', q('b', st.b));
    $('bmModel').innerHTML = K.svg(780, 130, s, 'Bar model: parts ' + st.a + ' and ' + st.b + ', whole ' + whole);
    eq = st.unk === 'whole' ? st.a + ' + ' + st.b + ' = ?' : st.unk === 'a' ? '? + ' + st.b + ' = ' + whole : st.a + ' + ? = ' + whole;
    ans = st.unk === 'whole' ? whole : st.unk === 'a' ? st.a : st.b;
    story = st.unk === 'whole' ? 'Lena has <b>' + st.a + '</b> red beads and <b>' + st.b + '</b> blue beads. How many beads does she have in all?' :
      st.unk === 'a' ? 'Lena has some red beads and <b>' + st.b + '</b> blue beads. She has <b>' + whole + '</b> beads in all. How many red beads does she have?' :
        'Lena had <b>' + st.a + '</b> beads. Then she got some more. Now she has <b>' + whole + '</b>. How many beads did she get?';
    $('bmCtl').innerHTML = K.step('a', 'First part', [1, 10], st.a) + K.step('b', 'Second part', [1, 10], st.b);
    $('bmUnk').innerHTML = '<span class="lab" style="font-weight:800">Unknown:</span>' + [['a', 'First part'], ['b', 'Second part'], ['whole', 'Whole']].map(function (p) { return '<button type="button" class="tl-btn" data-unk="' + p[0] + '" aria-pressed="' + (st.unk === p[0]) + '">' + p[1] + '</button>'; }).join('') + '<button type="button" class="tl-btn" id="bmShow">' + (st.shown ? 'Hide answer' : 'Show answer') + '</button>';
  } else {
    var big = Math.max(st.x, st.y, 1), uu = W / big, diff = Math.abs(st.x - st.y);
    s += K.txt(X - 6, 72, 'Max', { a: 'end', size: 18 }) + seg(X + 10, 40, st.x * uu - 10, 54, '#bfe6d0', st.x);
    s += K.txt(X - 6, 152, 'Zoe', { a: 'end', size: 18 }) + seg(X + 10, 120, st.y * uu - 10, 54, '#cde7ff', st.y);
    if (diff) { var lo = Math.min(st.x, st.y) * uu, hi = big * uu, yy = st.x < st.y ? 40 : 120; s += '<rect x="' + (X + lo) + '" y="' + yy + '" width="' + (hi - lo) + '" height="54" fill="none" stroke="#d63c7a" stroke-width="3" stroke-dasharray="8 5"/>' + K.txt(X + (lo + hi) / 2, yy + 34, st.shown ? diff : '?', { size: 22, fill: '#d63c7a' }); }
    $('bmModel').innerHTML = K.svg(780, 190, s, 'Compare bars: Max ' + st.x + ', Zoe ' + st.y);
    var more = st.x >= st.y ? ['Max', 'Zoe'] : ['Zoe', 'Max'];
    story = 'Max read <b>' + st.x + '</b> pages. Zoe read <b>' + st.y + '</b> pages. ' + (diff ? 'How many more pages did ' + more[0] + ' read than ' + more[1] + '?' : 'Who read more?');
    eq = diff ? Math.max(st.x, st.y) + ' − ' + Math.min(st.x, st.y) + ' = ?' : st.x + ' = ' + st.y; ans = diff;
    $('bmCtl').innerHTML = K.step('x', 'Max’s pages', [1, 10], st.x) + K.step('y', 'Zoe’s pages', [1, 10], st.y);
    $('bmUnk').innerHTML = '<button type="button" class="tl-btn" id="bmShow">' + (st.shown ? 'Hide answer' : 'Show answer') + '</button>';
  }
  $('bmStory').innerHTML = story; $('bmEq').textContent = eq;
  $('bmOut').innerHTML = st.shown ? '<b>Answer:</b> ' + (st.mode === 'cmp' && !ans ? 'They read the same number of pages. The difference is 0.' : ans) + (st.mode === 'ppw' && st.unk !== 'whole' ? '. Check: ' + st.a + ' + ' + st.b + ' = ' + (st.a + st.b) + '.' : '') : 'Solve it, then press Show answer to check.';
  T.update({ mode: st.mode, a: st.a, b: st.b, unk: st.unk, shown: st.shown, x: st.x, y: st.y });
}
var CH = [
  { text: 'Show a whole of 35 with parts 20 and 15.', test: function (s) { return s.mode === 'ppw' && s.a === 20 && s.b === 15; } },
  { text: 'Hide the whole, solve the story, then press Show answer.', test: function (s) { return s.mode === 'ppw' && s.unk === 'whole' && s.shown; } },
  { text: 'Make a part the unknown. What equation fits the story?', test: function (s) { return s.mode === 'ppw' && s.unk !== 'whole'; } },
  { text: 'Compare 42 and 30. How many more?', test: function (s) { return s.mode === 'cmp' && Math.max(s.x, s.y) === 42 && Math.min(s.x, s.y) === 30; } },
  { text: 'In Compare, make the two bars the same length. What is the difference?', test: function (s) { return s.mode === 'cmp' && s.x === s.y; } },
  { text: 'Make a whole of 100 with two parts.', test: function (s) { return s.mode === 'ppw' && s.a + s.b === 100 && s.a > 0 && s.b > 0; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
T.steppers($('bmCtl'), function (k, d) { var v = st[k] + d; if (v < 0 || v > 100) return; if (st.mode === 'ppw' && (k === 'a' ? v + st.b : st.a + v) > 100) return; st[k] = v; st.shown = false; draw(); });
document.addEventListener('click', function (e) {
  var b = e.target.closest('[data-mode],[data-unk],#bmShow'); if (!b) return;
  if (b.dataset.mode) { st.mode = b.dataset.mode; st.shown = false; } else if (b.dataset.unk) { st.unk = b.dataset.unk; st.shown = false; } else st.shown = !st.shown;
  draw();
});
reset();
""",
     [("The parts are 26 and 18. What is the whole?", "44 (26 + 18 = 44)"),
      ("The whole is 50 and one part is 32. What is the other part?", "18 (32 + ? = 50, or 50 − 32 = 18)"),
      ("Max read 64 pages. Zoe read 39 pages. How many more pages did Max read?", "25 more (64 − 39 = 25)"),
      ("Sam had some marbles. He got 15 more. Now he has 40. How many did he have at first?", "25 (? + 15 = 40)"),
      ("Draw a bar model for 57 − 23 and solve it.", "Whole 57, one part 23, the other part is 34"),
      ("Find two parts that make a whole of 100.", "Any pair that adds to 100, for example 60 and 40"),
      ("Reflect: How does a bar model help you choose to add or subtract?", "If the whole is missing, add the parts. If a part is missing, subtract the known part from the whole.")],
     ["The two parts together make the whole.",
      "If the whole is unknown, add. If a part is unknown, subtract (or count up from the part you know).",
      "In a compare story, the difference is the extra piece on the longer bar.",
      "The same bar model can match an addition and a subtraction equation."],
     ["Read the story aloud first; students decide which box gets the question mark before touching the tool.",
      "Ask for both equations for a missing part: 24 + ? = 37 and 37 − 24 = ?",
      "In Compare, ask “how many more” and “how many fewer” about the same picture."])

# ------------------------------------------------------------------ Clock (five minutes, a.m./p.m.)
tool(G, "clock-explorer", ["time-money"], "Clock to Five Minutes",
     "Move a clock by hours and five minutes, count by fives around the face, and choose a.m. or p.m. The digital time and the time in words update as you go.",
     "Use + and − to move the clock. Turn the minute labels on or off, and pick a.m. or p.m.",
     ["Time to five minutes", "a.m. and p.m."], "2.MD.C.7",
     """<div id="ckTool"></div>""",
     r"""
function has(h, list) { return K.histHas(h, list.map(function (x) { return x + 'am'; })) || K.histHas(h, list.map(function (x) { return x + 'pm'; })); }
var CH = [
  { text: 'Show 3:15 (quarter past 3).', test: function (s) { return s.h === 3 && s.m === 15; } },
  { text: 'Show 7:45. Say it two ways.', test: function (s) { return s.h === 7 && s.m === 45; } },
  { text: 'Show 8:05. Which number does the minute hand point to?', test: function (s) { return s.h === 8 && s.m === 5; } },
  { text: 'Show 6:00 p.m., a time for dinner.', test: function (s) { return s.h === 6 && s.m === 0 && s.pm; } },
  { text: 'Show noon: 12:00 p.m.', test: function (s) { return s.h === 12 && s.m === 0 && s.pm; } },
  { text: 'Count by fives from 2:00 to 2:30.', test: function (s) { return has(s.hist, ['2:00', '2:05', '2:10', '2:15', '2:20', '2:25', '2:30']); } }];
K.clockTool(Object.assign({}, META, { steps: [60, 5], ampm: true, fives: true, level: 2, start: [1, 0], challenges: CH }));
""",
     [("Show 4:35. Which number does the minute hand point to?", "The 7"),
      ("Show 9:50. How many minutes until 10:00?", "10 minutes"),
      ("Write quarter past 6 as a digital time.", "6:15"),
      ("What time is it 25 minutes after 3:00?", "3:25"),
      ("Do you eat breakfast at 7:30 a.m. or 7:30 p.m.?", "7:30 a.m."),
      ("Write half past 11 at night with a.m. or p.m.", "11:30 p.m."),
      ("Reflect: Why do we count by fives around the clock?", "Each number on the clock is 5 more minutes, because there are 5 minutes between numbers.")],
     ["Each number on the clock face is 5 more minutes: count by fives from the 12.",
      "Quarter past means 15 minutes after the hour; quarter to means 15 minutes before the next hour.",
      "a.m. is from midnight to noon; p.m. is from noon to midnight.",
      "The hour hand moves a little as the minutes go by."],
     ["Start with minute labels on, then hide them and count by fives together.",
      "Name daily events and ask for a.m. or p.m. (lunch 12:15 p.m., wake up 6:45 a.m.).",
      "Arrow keys move the clock five minutes at a time."])

# ------------------------------------------------------------------ Money
tool(G, "money-counter", ["time-money"], "Coin and Bill Counter",
     "Add pennies, nickels, dimes, quarters and dollar bills. Count on from the biggest value, and find different ways to make the same amount.",
     "Use + and − to add coins and bills. The tool counts them from the biggest value to the smallest.",
     ["Counting coins", "Dollars and cents", "Money word problems"], "2.MD.C.8",
     """<div class="tl-model" id="mnModel"></div><div class="tl-big" id="mnTot" aria-live="polite"></div>
<div class="tl-controls" id="mnCtl"></div><div class="tl-out" id="mnOut"></div>""",
     r"""
var C = [['b5', 'Five-dollar bills', 500], ['b1', 'One-dollar bills', 100], ['q', 'Quarters', 25], ['d', 'Dimes', 10], ['n', 'Nickels', 5], ['p', 'Pennies', 1]];
var st;
function reset() { st = { b5: 0, b1: 0, q: 1, d: 1, n: 0, p: 3, ways: {} }; draw(); }
function fmt(c) { return c >= 100 ? '$' + Math.floor(c / 100) + '.' + K.pad(c % 100) : c + '¢'; }
function coin(x, y, k) {
  var r = { q: 30, d: 21, n: 26, p: 24 }[k], col = k === 'p' ? ['#d9895b', '#8a4a24'] : ['#d6dde6', '#5b6b7d'], lab = { q: '25¢', d: '10¢', n: '5¢', p: '1¢' }[k];
  return '<circle cx="' + x + '" cy="' + y + '" r="' + r + '" fill="' + col[0] + '" stroke="' + col[1] + '" stroke-width="3"/>' + K.txt(x, y + 6, lab, { size: r > 24 ? 16 : 13, fill: '#1d2a3a' });
}
function draw() {
  var s = '', x = 14, y, i, total = 0, coins = 0, run = [], t = 0;
  C.forEach(function (c) { total += st[c[0]] * c[2]; if (c[0][0] !== 'b') coins += st[c[0]]; for (i = 0; i < st[c[0]]; i++) { t += c[2]; run.push(fmt(t)); } });
  y = 14;
  ['b5', 'b1'].forEach(function (k) { for (i = 0; i < st[k]; i++) { s += '<rect x="' + x + '" y="' + y + '" width="120" height="56" rx="6" fill="#bfe6c4" stroke="#2f6b3a" stroke-width="3"/>' + K.txt(x + 60, y + 37, k === 'b5' ? '$5' : '$1', { size: 26, fill: '#1f4d2b' }); x += 128; if (x > 640) { x = 14; y += 64; } } });
  x = 14; y += (st.b5 + st.b1 ? 104 : 40);
  ['q', 'd', 'n', 'p'].forEach(function (k) { for (i = 0; i < st[k]; i++) { s += coin(x + 32, y, k); x += 70; if (x > 700) { x = 14; y += 72; } } });
  $('mnModel').innerHTML = K.svg(780, Math.max(120, y + 50), s, 'Money: ' + fmt(total));
  $('mnTot').textContent = fmt(total);
  $('mnCtl').innerHTML = C.map(function (c) { return K.step(c[0], c[1], [1], st[c[0]]); }).join('');
  $('mnOut').innerHTML = total ? '<b>Count on, biggest first:</b> ' + run.join(', ') + '<br>Total: <b>' + fmt(total) + '</b>' + (total >= 100 ? ' (' + total + ' cents)' : '') + ' with ' + coins + ' coin' + (coins === 1 ? '' : 's') + (st.b1 + st.b5 ? ' and ' + (st.b1 + st.b5) + ' bill' + (st.b1 + st.b5 > 1 ? 's' : '') : '') + '.' : 'Add some coins or bills.';
  var key = C.map(function (c) { return st[c[0]]; }).join(','); (st.ways[total] = st.ways[total] || {})[key] = 1;
  T.update({ total: total, coins: coins, q: st.q, d: st.d, n: st.n, p: st.p, b1: st.b1, b5: st.b5, ways: st.ways });
}
var CH = [
  { text: 'Make 25¢ without using a quarter.', test: function (s) { return s.total === 25 && s.q === 0; } },
  { text: 'Make $1.00 with only quarters.', test: function (s) { return s.q === 4 && s.total === 100; } },
  { text: 'Make 47¢.', test: function (s) { return s.total === 47; } },
  { text: 'Make 47¢ with the fewest coins you can.', test: function (s) { return s.total === 47 && s.coins === 5 && !s.b1 && !s.b5; } },
  { text: 'Make $3.50 using bills and coins.', test: function (s) { return s.total === 350 && (s.b1 + s.b5) > 0 && s.coins > 0; } },
  { text: 'Make the same amount in two different ways.', test: function (s) { return Object.keys(s.ways).some(function (t) { return +t > 0 && Object.keys(s.ways[t]).length >= 2; }); } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
T.steppers($('mnCtl'), function (k, d) { st[k] = K.clamp(st[k] + d, 0, 9); draw(); });
reset();
""",
     [("How much are 2 quarters, 1 dime and 3 pennies?", "63¢"),
      ("How much are 3 dimes and 4 nickels?", "50¢"),
      ("How many nickels make a quarter?", "5 nickels"),
      ("How much are one $1 bill and 2 quarters?", "$1.50"),
      ("Make 47¢ with the fewest coins. Which coins did you use?", "1 quarter, 2 dimes and 2 pennies (5 coins)"),
      ("Ana has 80¢. She buys a pencil for 65¢. How much money is left?", "15¢"),
      ("Reflect: Why is it easier to count the coins worth the most first?", "Big jumps first, then small ones: 25, 35, 45, 46, 47 is quicker than counting pennies first.")],
     ["Count the coins worth the most first, then count on.",
      "A penny is 1¢, a nickel 5¢, a dime 10¢ and a quarter 25¢. 100¢ is $1.00.",
      "The same amount can be made with different coins.",
      "The biggest coin is not always the one worth the most: a dime is smaller than a nickel but worth more."],
     ["Ask students to count aloud along the running total shown in the tool.",
      "Pose making-change stories: “You have $1.00 and spend 65¢.”",
      "Use “fewest coins” to build number sense with 25s and 10s."])

# ------------------------------------------------------------------ Ruler and line plot
tool(G, "ruler-line-plot", ["measuring-length", "graphs-data"], "Ruler and Line Plot",
     "Measure pencils with an inch or centimeter ruler, including pencils that do not start at 0, and record each length on a line plot.",
     "Read the ruler, type the length and press Check. Correct inch measurements go on the line plot.",
     ["Measuring with a ruler", "Inches and centimeters", "Line plots"], "2.MD.A.1, 2.MD.D.9",
     """<div class="tl-controls" role="group" aria-label="Ruler settings"><span class="lab" style="font-weight:800">Ruler:</span><button type="button" class="tl-btn" data-u="in">Inches</button><button type="button" class="tl-btn" data-u="cm">Centimeters</button>
<span class="lab" style="font-weight:800;margin-left:.6rem">Pencil starts at:</span><button type="button" class="tl-btn" data-z="0">0</button><button type="button" class="tl-btn" data-z="1">Another mark</button></div>
<div class="tl-model" id="rlModel"></div>
<div class="tl-controls"><div class="tl-field el-inline"><label for="rlIn">The pencil is</label><input id="rlIn" type="number" min="0" max="20" inputmode="numeric"><span id="rlUnit"></span> long.</div><button type="button" class="tl-btn" id="rlCheck">Check</button><button type="button" class="tl-btn" id="rlNext">Next pencil</button></div>
<div class="tl-out" id="rlOut" aria-live="polite"></div><h2 style="margin-top:.8rem">Line plot: our pencils (inches)</h2><div class="tl-model" id="rlPlot"></div>""",
     r"""
var LIN = [5, 3, 7, 5, 6, 4, 7, 5, 8, 6, 3, 6, 4, 5], LCM = [12, 8, 15, 10, 6, 14, 9, 11, 13, 7], OFF = [2, 1, 3, 2, 1, 4];
var st;
function reset() { st = { u: 'in', z: 0, i: 0, plot: [], done: {}, msg: 'Read where the pencil ends. Remember to count the units, not the marks.', okIn: 0, okCm: 0, okOff: 0 }; $('rlIn').value = ''; draw(); }
function cur() { var L = st.u === 'in' ? LIN[st.i % LIN.length] : LCM[st.i % LCM.length], off = st.z ? OFF[st.i % OFF.length] : 0; return { L: L, off: off }; }
function draw() {
  Array.prototype.forEach.call(document.querySelectorAll('[data-u]'), function (b) { b.setAttribute('aria-pressed', b.dataset.u === st.u); });
  Array.prototype.forEach.call(document.querySelectorAll('[data-z]'), function (b) { b.setAttribute('aria-pressed', +b.dataset.z === st.z); });
  var c = cur(), max = st.u === 'in' ? 12 : 24, u = 740 / max, X = 30, s = '', i;
  s += '<rect x="' + X + '" y="80" width="' + max * u + '" height="70" fill="#fde68a" stroke="#92400e" stroke-width="2.5"/>';
  for (i = 0; i <= max; i++) { s += '<line x1="' + (X + i * u) + '" y1="80" x2="' + (X + i * u) + '" y2="' + (st.u === 'in' ? 118 : 108) + '" stroke="#1d2a3a" stroke-width="2.4"/>' + K.txt(X + i * u, 142, i, { size: st.u === 'in' ? 18 : 13 }); }
  var px = X + c.off * u, pw = c.L * u;
  s += '<rect x="' + px + '" y="28" width="' + (pw - 26) + '" height="34" fill="#ffd34d" stroke="#1d2a3a" stroke-width="2.5"/><rect x="' + px + '" y="28" width="14" height="34" fill="#f9a8d4" stroke="#1d2a3a" stroke-width="2.5"/><path d="M' + (px + pw - 26) + ' 28 l26 17 l-26 17z" fill="#f6d7a7" stroke="#1d2a3a" stroke-width="2.5"/>';
  s += '<line x1="' + px + '" y1="20" x2="' + px + '" y2="80" stroke="#0d6b3c" stroke-width="2" stroke-dasharray="5 4"/><line x1="' + (px + pw) + '" y1="20" x2="' + (px + pw) + '" y2="80" stroke="#0d6b3c" stroke-width="2" stroke-dasharray="5 4"/>';
  $('rlModel').innerHTML = K.svg(800, 160, s, 'A pencil above a ' + (st.u === 'in' ? 'inch' : 'centimeter') + ' ruler');
  $('rlUnit').textContent = st.u === 'in' ? 'inches' : 'centimeters';
  $('rlOut').innerHTML = 'Pencil ' + (st.i + 1) + '. ' + st.msg;
  var p = '', cnt = {}, Y = 150, sx = function (v) { return 30 + v * 70; };
  p += '<line x1="20" y1="' + Y + '" x2="760" y2="' + Y + '" stroke="#1d2a3a" stroke-width="3"/>';
  for (i = 0; i <= 10; i++) p += '<line x1="' + sx(i) + '" y1="' + (Y - 7) + '" x2="' + sx(i) + '" y2="' + (Y + 7) + '" stroke="#1d2a3a" stroke-width="2"/>' + K.txt(sx(i), Y + 28, i, { size: 16 });
  st.plot.forEach(function (v) { cnt[v] = (cnt[v] || 0) + 1; p += K.txt(sx(v), Y - 12 - (cnt[v] - 1) * 22, '×', { size: 28, fill: '#d63c7a' }); });
  p += K.txt(400, Y + 52, 'Length of pencil (inches)', { size: 15, w: 700, fill: '#55657a' });
  $('rlPlot').innerHTML = K.svg(780, 210, p, 'Line plot with ' + st.plot.length + ' pencil lengths');
  T.update({ plot: st.plot.slice(), okIn: st.okIn, okCm: st.okCm, okOff: st.okOff, u: st.u });
}
var CH = [
  { text: 'Measure a pencil in inches and check your answer.', test: function (s) { return s.okIn > 0; } },
  { text: 'Measure a pencil that does not start at 0.', test: function (s) { return s.okOff > 0; } },
  { text: 'Measure a pencil in centimeters.', test: function (s) { return s.okCm > 0; } },
  { text: 'Put 5 measurements on the line plot.', test: function (s) { return s.plot.length >= 5; } },
  { text: 'Find two pencils with the same length on the line plot.', test: function (s) { var c = {}; return s.plot.some(function (v) { c[v] = (c[v] || 0) + 1; return c[v] > 1; }); } },
  { text: 'Put 8 pencils on the line plot. How much longer is the longest than the shortest?', test: function (s) { return s.plot.length >= 8; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
function check() {
  var c = cur(), v = parseInt($('rlIn').value, 10);
  if (isNaN(v)) { st.msg = 'Type a number first.'; return draw(); }
  if (st.done[st.u + st.i]) { st.msg = 'You already measured this pencil. Press Next pencil.'; return draw(); }
  if (v === c.L) {
    st.done[st.u + st.i] = 1; if (st.u === 'in') { st.okIn++; st.plot.push(v); } else st.okCm++; if (c.off) st.okOff++;
    st.msg = '<span class="el-ok">Yes! ' + c.L + ' ' + (st.u === 'in' ? 'inches' : 'centimeters') + '.</span>' + (c.off ? ' It goes from ' + c.off + ' to ' + (c.off + c.L) + ', and ' + (c.off + c.L) + ' − ' + c.off + ' = ' + c.L + '.' : '') + (st.u === 'in' ? ' It is on the line plot.' : '') + ' Press Next pencil.';
  } else if (c.off && v === c.off + c.L) st.msg = '<span class="el-no">Not quite.</span> The pencil does not start at 0. Count the units from where it starts, or subtract.';
  else st.msg = '<span class="el-no">Not quite.</span> Count the spaces (units) between the start and the end of the pencil.';
  draw();
}
$('rlCheck').onclick = check;
$('rlIn').addEventListener('keydown', function (e) { if (e.key === 'Enter') check(); });
$('rlNext').onclick = function () { st.i++; st.msg = 'Read where the pencil ends.'; $('rlIn').value = ''; draw(); $('rlIn').focus(); };
document.addEventListener('click', function (e) { var b = e.target.closest('[data-u],[data-z]'); if (!b) return; if (b.dataset.u) st.u = b.dataset.u; else st.z = +b.dataset.z; st.msg = 'Read where the pencil ends.'; $('rlIn').value = ''; draw(); });
reset();
""",
     [("A pencil starts at 0 and ends at 6 on the inch ruler. How long is it?", "6 inches"),
      ("A pencil starts at 2 and ends at 9 on the inch ruler. How long is it?", "7 inches (9 − 2 = 7)"),
      ("Is a centimeter or an inch longer? Which unit gives a bigger number for the same pencil?", "An inch is longer. Centimeters give the bigger number."),
      ("A line plot has × marks at 3, 5, 5, 6 and 7 inches. How many pencils were measured?", "5 pencils"),
      ("On that line plot, which length is the most common?", "5 inches"),
      ("How much longer is the longest pencil (7 in) than the shortest (3 in)?", "4 inches"),
      ("Reflect: Why do you count spaces on a ruler and not the marks?", "Each space is one unit of length. Counting marks counts one too many.")],
     ["Line up one end of the object with 0, or subtract the start from the end.",
      "A length is the number of units (spaces) between the ends, not the number of marks.",
      "Centimeters are smaller than inches, so the same pencil is more centimeters than inches.",
      "On a line plot, each × is one measurement; stacked ×s show lengths that happened more than once."],
     ["Show a pencil that starts at 2 and ask why the end mark is not the length.",
      "After 8 measurements, ask questions about the line plot: most common length, longest minus shortest.",
      "Enter submits an answer; Next pencil gives a new length (the sequence is the same every time, so a class can work together)."])

# ------------------------------------------------------------------ Graphs
tool(G, "graph-builder", ["graphs-data"], "Picture and Bar Graph Builder",
     "Enter votes for favorite sports and see them as a picture graph, a bar graph and a table. Answer put-together, take-apart and compare questions.",
     "Use + and − to change the votes. Switch between the picture graph, the bar graph and the table.",
     ["Picture graphs", "Bar graphs", "Comparing data"], "2.MD.D.10",
     """<div id="grTool"></div>""",
     r"""
var CH = [
  { text: 'Make a bar graph where Soccer has 8 votes.', test: function (s) { return s.c[0] === 8 && s.view === 'bar'; } },
  { text: 'Make Basketball 3 more than Tennis.', test: function (s) { return s.c[1] === s.c[2] + 3; } },
  { text: 'Make 20 votes in all.', test: function (s) { return s.total === 20; } },
  { text: 'Look at the same data as a picture graph and as a bar graph.', test: function (s) { return s.seen.pic && s.seen.bar; } },
  { text: 'Make the difference between the most and fewest votes equal 6.', test: function (s) { return s.max - s.min === 6; } },
  { text: 'Make two sports tie for the fewest votes.', test: function (s) { return s.c.filter(function (v) { return v === s.min; }).length >= 2; } }];
K.graphTool(Object.assign({}, META, { toolTitle: META.title, title: 'Our Favorite Sport', cats: ['Soccer', 'Basketball', 'Tennis', 'Swimming'], counts: [7, 5, 4, 9], max: 20, steps: [1], views: ['pic', 'bar', 'table'], keys: [1], scales: [1], challenges: CH }));
""",
     [("How many votes are there in all? (Soccer 7, Basketball 5, Tennis 4, Swimming 9)", "25"),
      ("How many more votes does Swimming have than Tennis?", "5 more"),
      ("How many more votes does Soccer have than Basketball?", "2 more"),
      ("If 4 more students vote for Tennis, how many votes will Tennis have?", "8"),
      ("Which sport has the shortest bar?", "Tennis"),
      ("How many students voted for Soccer or Basketball?", "12"),
      ("Reflect: How are a picture graph and a bar graph alike?", "Both show the same counts. Each picture or each unit of a bar stands for 1 vote.")],
     ["Each picture or each unit of a bar stands for 1 vote.",
      "The longest bar shows the most votes; the shortest shows the fewest.",
      "To compare two categories, subtract: 9 − 4 = 5 more.",
      "The same data can be shown in different ways."],
     ["Collect class data first, then enter it together.",
      "Ask put-together (Soccer or Basketball), take-apart and compare questions.",
      "Have students make the graph on paper and check it against the tool."])

# ------------------------------------------------------------------ Equal shares + rows and columns
tool(G, "equal-shares", ["shapes-equal-shares"], "Equal Shares and Square Grids",
     "Cut circles and rectangles into halves, thirds and fourths, color the shares, and build rectangles from rows and columns of same-size squares.",
     "Choose a shape and the number of parts, then tap parts to color them. Switch to Rows and columns of squares to fill a rectangle.",
     ["Halves, thirds and fourths", "Equal shares", "Rows and columns of squares"], "2.G.A.2, 2.G.A.3",
     """<div id="shTool"></div>""",
     r"""
var CH = [
  { text: 'Cut a circle into thirds and color one third.', test: function (s) { return s.mode === 'shares' && s.shape === 'circle' && s.parts === 3 && s.equal && s.shaded === 1; } },
  { text: 'Color all three thirds. How many thirds make a whole?', test: function (s) { return s.mode === 'shares' && s.parts === 3 && s.equal && s.shaded === 3; } },
  { text: 'Find a rectangle cut into 3 parts that are NOT thirds.', test: function (s) { return s.mode === 'shares' && s.shape === 'rectangle' && s.parts === 3 && !s.equal; } },
  { text: 'Make a rectangle with 2 rows and 4 columns of squares.', test: function (s) { return s.mode === 'grid' && s.rows === 2 && s.cols === 4; } },
  { text: 'Make 12 squares in two different ways.', test: function (s) { return Object.keys(s.grids).filter(function (k) { var p = k.split('x'); return p[0] * p[1] === 12; }).length >= 2; } },
  { text: 'Color 2 fourths of a rectangle.', test: function (s) { return s.mode === 'shares' && s.shape === 'rectangle' && s.parts === 4 && s.equal && s.shaded === 2; } }];
K.sharesTool(Object.assign({}, META, { toolTitle: META.title, shapes: ['circle', 'rectangle', 'square'], parts: [2, 3, 4], grid: true, challenges: CH }));
""",
     [("Cut a circle into 3 equal shares. What is each share called?", "A third (one third)"),
      ("How many thirds make one whole?", "3 thirds"),
      ("Which is bigger: one third or one fourth of the same rectangle?", "One third"),
      ("A rectangle has 3 rows and 4 columns of squares. How many squares are there?", "12 squares"),
      ("Find another way to make a rectangle with 12 squares.", "For example 2 rows of 6 (or 4 rows of 3, or 6 rows of 2)"),
      ("Are equal shares of the same shape always the same shape? Explain.", "No. Halves of a square can be two rectangles or two triangles — they are the same size, not always the same shape."),
      ("Reflect: Why must the shares be the same size to be called thirds?", "Thirds are 3 equal shares. If the parts are different sizes, they are not thirds.")],
     ["Halves are 2 equal shares, thirds are 3 and fourths are 4.",
      "A whole is 2 halves, 3 thirds or 4 fourths.",
      "More equal shares means smaller shares.",
      "A rectangle can be filled with rows and columns of same-size squares; count them by rows."],
     ["Use Not equal parts as a non-example and ask students to explain why the parts are not thirds.",
      "In Rows and columns, ask students to predict the number of squares before they change the grid.",
      "Talk about “a whole” as 2 halves, 3 thirds or 4 fourths (2.G.A.3)."])
