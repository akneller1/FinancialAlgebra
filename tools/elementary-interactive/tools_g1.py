"""Grade 1 Interactive Math tools (math1-*)."""
from reg import tool

G = 1

# ------------------------------------------------------------------ Ten-Frame Builder
tool(G, "ten-frame-builder", ["add-subtract-10", "add-subtract-20", "word-problems-20"], "Ten-Frame Builder",
     "Fill two ten-frames with red and yellow counters to add, take away and make ten. The number sentence changes as you build.",
     "Use + and − to put red and yellow counters in the ten-frames. Use Take away to cross some out.",
     ["Addition within 20", "Subtraction within 20", "Making ten"], "1.OA.A.1, 1.OA.C.5, 1.OA.C.6",
     """<div class="tl-model" id="tfModel"></div><div class="tl-big" id="tfEq" aria-live="polite"></div>
<div class="tl-controls" id="tfCtl"></div><div class="tl-out" id="tfOut"></div>""",
     r"""
var st;
function reset() { st = { a: 6, b: 3, take: 0 }; draw(); }
function draw() {
  var n = st.a + st.b, s = '', f, i;
  for (f = 0; f < 2; f++) {
    var x0 = 20 + f * 370;
    s += '<rect x="' + x0 + '" y="20" width="350" height="140" rx="8" fill="#fff" stroke="#22408a" stroke-width="5"/>';
    for (i = 0; i < 10; i++) {
      var cx = x0 + 35 + (i % 5) * 70, cy = 55 + Math.floor(i / 5) * 70, k = f * 10 + i;
      s += '<rect x="' + (cx - 35) + '" y="' + (cy - 35) + '" width="70" height="70" fill="none" stroke="#22408a" stroke-width="2.5"/>';
      if (k < n) {
        var red = k < st.a, gone = k >= n - st.take;
        s += '<circle cx="' + cx + '" cy="' + cy + '" r="26" fill="' + (red ? '#e5484d' : '#ffd34d') + '" stroke="' + (red ? '#8c1d22' : '#b7791f') + '" stroke-width="3"' + (gone ? ' opacity=".35"' : '') + '/>';
        if (gone) s += '<path d="M' + (cx - 22) + ' ' + (cy - 22) + ' L' + (cx + 22) + ' ' + (cy + 22) + ' M' + (cx + 22) + ' ' + (cy - 22) + ' L' + (cx - 22) + ' ' + (cy + 22) + '" stroke="#1d2a3a" stroke-width="6" stroke-linecap="round"/>';
      }
    }
  }
  $('tfModel').innerHTML = K.svg(760, 180, s, st.a + ' red and ' + st.b + ' yellow counters' + (st.take ? ', ' + st.take + ' crossed out' : ''));
  $('tfCtl').innerHTML = K.step('a', 'Red counters', [1], st.a) + K.step('b', 'Yellow counters', [1], st.b) + K.step('take', 'Take away', [1], st.take);
  $('tfEq').textContent = st.take ? n + ' − ' + st.take + ' = ' + (n - st.take) : st.a + ' + ' + st.b + ' = ' + n;
  var msg;
  if (st.take) msg = 'Start with <b>' + n + '</b>. Cross out <b>' + st.take + '</b>. <b>' + (n - st.take) + '</b> are left.';
  else if (n < 10) msg = '<b>' + n + '</b> and <b>' + (10 - n) + '</b> more make 10. Count the empty boxes in the first frame!';
  else if (n === 10) msg = 'The first ten-frame is full. <b>' + st.a + ' + ' + st.b + ' = 10</b>.';
  else msg = 'One full ten-frame and <b>' + (n - 10) + '</b> more: <b>10 + ' + (n - 10) + ' = ' + n + '</b>.' + (st.a < 10 && st.b > 0 ? ' (' + (10 - st.a) + ' yellow counters filled the first frame.)' : '');
  $('tfOut').innerHTML = msg;
  T.update({ a: st.a, b: st.b, take: st.take, n: n });
}
var CH = [
  { text: 'Show 6 + 4. Are there any empty boxes in the first frame?', test: function (s) { return s.a === 6 && s.b === 4 && !s.take; } },
  { text: 'Find another way to make 10 with red and yellow (not 6 + 4).', test: function (s) { return s.n === 10 && s.a > 0 && s.b > 0 && s.a !== 6 && !s.take; } },
  { text: 'Show 9 + 5. Write it as 10 + something.', test: function (s) { return s.a === 9 && s.b === 5 && !s.take; } },
  { text: 'Make 13 with 10 red counters and some yellow ones.', test: function (s) { return s.a === 10 && s.n === 13; } },
  { text: 'Show 12 − 4: make 12, then take away 4.', test: function (s) { return s.n === 12 && s.take === 4; } },
  { text: 'Make 16. How many more than 10 is it?', test: function (s) { return s.n === 16 && !s.take; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
T.steppers($('tfCtl'), function (k, d) {
  if (k === 'take') st.take = K.clamp(st.take + d, 0, st.a + st.b);
  else { var v = st[k] + d; if (v < 0 || st.a + st.b + d > 20) return; st[k] = v; st.take = Math.min(st.take, st.a + st.b); }
  draw();
});
reset();
""",
     [("Show 7 + 3. How many empty boxes are in the first ten-frame?", "0 — it is full. 7 + 3 = 10"),
      ("Show 9 + 4. Write it as 10 + __.", "10 + 3 = 13"),
      ("Show 8 + 5. How many yellow counters fill the first frame? How many are in the second frame?", "2 fill the first frame; 3 are in the second. 8 + 5 = 13"),
      ("Show 5 + 6, then 6 + 5. Are the totals the same?", "Yes. Both are 11."),
      ("Make 14. Take away 6. How many are left?", "8 (14 − 6 = 8)"),
      ("Write two different ways to make 10 with red and yellow counters.", "Any two pairs that make 10, for example 4 + 6 and 7 + 3"),
      ("Reflect: How does a ten-frame help you add 8 + 6?", "Move 2 of the 6 to fill the frame: 10 + 4 = 14.")],
     ["A ten-frame holds exactly 10. Count the empty boxes to find how many more make 10.",
      "To add 9 + 5, fill the first frame first: 9 + 1 = 10, then 4 more makes 14.",
      "Changing the order (6 + 3 or 3 + 6) does not change how many counters there are.",
      "Taking away crosses out counters; the ones left over are the answer."],
     ["Start with partners of 10: keep red + yellow = 10 and ask students to find every pair.",
      "For make-ten facts (8 + 5, 9 + 4), ask: How many yellow counters will fill the first frame? How many are left over?",
      "Use Take away for take-from stories: “There were 12 birds. 4 flew away.” Students build 12 and cross out 4."])

# ------------------------------------------------------------------ Tens and Ones Builder
tool(G, "tens-ones-builder", ["tens-ones", "count-120", "compare-numbers"], "Tens and Ones Builder",
     "Build numbers to 120 with ten-rods and ones cubes, bundle 10 ones into a ten, break a ten apart, and compare two numbers with >, = and <.",
     "Add tens and ones with + and −. When you have 10 ones, bundle them into a ten. Turn on Compare to build a second number.",
     ["Tens and ones", "Numbers to 120", "Comparing numbers"], "1.NBT.A.1, 1.NBT.B.2, 1.NBT.B.3",
     """<div class="tl-model" id="toModel"></div><div class="tl-big" id="toNum" aria-live="polite"></div>
<div class="tl-controls" id="toCtl"></div>
<div class="tl-controls" style="margin-top:.6rem"><button type="button" class="tl-btn" id="toBundle">Bundle 10 ones → 1 ten</button><button type="button" class="tl-btn" id="toBreak">Break 1 ten → 10 ones</button><button type="button" class="tl-btn" id="toCmp" aria-pressed="false">Compare</button></div>
<div id="toCmpBox" hidden><div class="tl-model" id="toModelB"></div><div class="tl-controls" id="toCtlB"></div>
<div class="tl-controls" style="margin-top:.6rem;justify-content:center" role="group" aria-label="Choose a sign"><span class="tl-big" id="toA"></span><button type="button" class="tl-btn" data-sym="&gt;">&gt;</button><button type="button" class="tl-btn" data-sym="=">=</button><button type="button" class="tl-btn" data-sym="&lt;">&lt;</button><span class="tl-big" id="toB"></span></div></div>
<div class="tl-out" id="toOut"></div>""",
     r"""
var st;
function reset() { st = { t: 2, o: 3, tb: 3, ob: 2, cmp: false, pick: null, bundles: 0, msg: '' }; $('toCmpBox').hidden = true; draw(); }
function blocks(t, o, label) {
  var s = '', i, r;
  for (i = 0; i < t; i++) { var x = 14 + i * 30; s += '<rect x="' + x + '" y="12" width="22" height="200" fill="#34d399" stroke="#065f46" stroke-width="2"/>'; for (r = 1; r < 10; r++) s += '<line x1="' + x + '" y1="' + (12 + r * 20) + '" x2="' + (x + 22) + '" y2="' + (12 + r * 20) + '" stroke="#065f46" stroke-width="1.2"/>'; }
  var ox = Math.max(14 + t * 30 + 26, 200);
  for (i = 0; i < o; i++) s += '<rect x="' + (ox + (i % 5) * 26) + '' + '" y="' + (12 + Math.floor(i / 5) * 26) + '" width="20" height="20" fill="#60a5fa" stroke="#1e3a8a" stroke-width="2"/>';
  var w = Math.max(ox + 5 * 26 + 10, 380);
  return K.svg(w, 222, s, label);
}
function draw() {
  var n = 10 * st.t + st.o, nb = 10 * st.tb + st.ob;
  $('toModel').innerHTML = blocks(st.t, st.o, st.t + ' ten rods and ' + st.o + ' ones cubes');
  $('toNum').textContent = n;
  $('toCtl').innerHTML = K.step('t', 'Tens (rods)', [1], st.t) + K.step('o', 'Ones (cubes)', [1], st.o);
  $('toBundle').disabled = st.o < 10; $('toBreak').disabled = st.t < 1;
  var out = '<b>' + st.t + '</b> ten' + (st.t === 1 ? '' : 's') + ' and <b>' + st.o + '</b> one' + (st.o === 1 ? '' : 's') + ' = <b>' + n + '</b>';
  if (st.o >= 10) out += '<br>You have <b>' + st.o + ' ones</b>. 10 ones can be bundled into 1 ten!';
  else if (st.t >= 10) out += '<br>' + st.t + ' tens = ' + (st.t * 10) + '. Ten tens make one hundred.';
  var ok = false;
  if (st.cmp) {
    $('toModelB').innerHTML = blocks(st.tb, st.ob, 'Second number: ' + st.tb + ' tens and ' + st.ob + ' ones');
    $('toCtlB').innerHTML = K.step('tb', 'Second number: tens', [1], st.tb) + K.step('ob', 'Second number: ones', [1], st.ob);
    $('toA').textContent = n; $('toB').textContent = nb;
    var right = n > nb ? '>' : n < nb ? '<' : '=';
    Array.prototype.forEach.call(document.querySelectorAll('[data-sym]'), function (b) { b.setAttribute('aria-pressed', b.dataset.sym === st.pick); });
    if (st.pick) {
      ok = st.pick === right;
      var why = st.t !== st.tb ? 'Compare the tens first: ' + st.t + ' tens ' + (st.t > st.tb ? 'is more than' : 'is less than') + ' ' + st.tb + ' tens.' : st.o !== st.ob ? 'The tens are the same, so compare the ones: ' + st.o + ' ' + (st.o > st.ob ? '>' : '<') + ' ' + st.ob + '.' : 'Same tens and same ones.';
      out += '<br>' + (ok ? '<span class="el-ok">Yes! ' + n + ' ' + right + ' ' + nb + '.</span> ' : '<span class="el-no">Not yet. Try again.</span> ') + (ok ? why : '');
    } else out += '<br>Which sign makes it true? Tap &gt;, = or &lt;.';
  }
  if (st.msg) out += '<br>' + st.msg;
  $('toOut').innerHTML = out; st.msg = '';
  T.update({ t: st.t, o: st.o, n: n, nb: nb, tb: st.tb, ob: st.ob, cmp: st.cmp, ok: ok, bundles: st.bundles });
}
var CH = [
  { text: 'Build 34 with 3 tens and 4 ones.', test: function (s) { return s.t === 3 && s.o === 4; } },
  { text: 'Build 14 with ones only, then press Bundle. What do you have now?', test: function (s) { return s.bundles > 0 && s.t === 1 && s.o === 4; } },
  { text: 'Break a ten to show 25 as 1 ten and 15 ones.', test: function (s) { return s.t === 1 && s.o === 15; } },
  { text: 'Build 100. How many tens is that?', test: function (s) { return s.n === 100; } },
  { text: 'Build 120, the biggest number here.', test: function (s) { return s.n === 120; } },
  { text: 'Turn on Compare. Build two numbers with the same tens and choose the right sign.', test: function (s) { return s.cmp && s.ok && s.t === s.tb && s.o !== s.ob; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
function change(k, d) {
  var nx = Object.assign({}, st); nx[k] = st[k] + d;
  if (nx[k] < 0) return;
  if (k === 'o' && nx.o > 20) return;
  if (k === 'ob' && nx.ob > 9) { st.msg = 'Use a ten rod instead of 10 ones.'; return draw(); }
  if (10 * nx.t + nx.o > 120 || 10 * nx.tb + nx.ob > 120) { st.msg = 'This tool counts to 120.'; return draw(); }
  st[k] = nx[k]; st.pick = null; draw();
}
T.steppers($('toCtl'), change); T.steppers($('toCtlB'), change);
$('toBundle').onclick = function () { if (st.o >= 10) { st.o -= 10; st.t++; st.bundles++; st.pick = null; draw(); } };
$('toBreak').onclick = function () { if (st.t >= 1 && st.o <= 10) { st.t--; st.o += 10; st.pick = null; draw(); } else if (st.o > 10) { st.msg = 'Bundle some ones first.'; draw(); } };
$('toCmp').onclick = function () { st.cmp = !st.cmp; st.pick = null; this.setAttribute('aria-pressed', st.cmp); $('toCmpBox').hidden = !st.cmp; draw(); };
Array.prototype.forEach.call(document.querySelectorAll('[data-sym]'), function (b) { b.onclick = function () { st.pick = b.dataset.sym; draw(); }; });
reset();
""",
     [("Build 46. How many tens and how many ones?", "4 tens and 6 ones"),
      ("Build 17 using only ones. Then bundle. What do you have now?", "1 ten and 7 ones"),
      ("Show 32 as 2 tens and some ones. How many ones do you need?", "12 ones"),
      ("Build 7 tens. What number is it?", "70"),
      ("How many tens make 100?", "10 tens"),
      ("Compare 58 and 85. Write >, = or <.", "58 < 85, because 5 tens is less than 8 tens"),
      ("Reflect: Why is 1 ten the same as 10 ones?", "A ten rod is 10 ones put together, so it is worth 10.")],
     ["Ten ones can be bundled into one ten. A ten can be broken into ten ones. The number stays the same.",
      "In a two-digit number, the first digit tells how many tens and the second tells how many ones.",
      "To compare, look at the tens first. If the tens are the same, compare the ones.",
      "10 tens is 100. 12 tens is 120."],
     ["Ask students to build the same number two ways (34 as 3 tens 4 ones and as 2 tens 14 ones) and explain why both are 34.",
      "For teen numbers, build 10 ones, bundle them, and say “one ten and ___ ones.”",
      "In Compare, ask students to say the comparison in words: “58 is less than 85.”"])

# ------------------------------------------------------------------ Balance Scale
tool(G, "balance-scale", ["equal-sign", "add-subtract-20"], "Equal Sign Balance",
     "Put cubes on both sides of a balance. When both sides are worth the same, the scale is level and the equation is true.",
     "Use + and − to put cubes on each side. The heavier side goes down. Make the scale level to make a true equation.",
     ["The equal sign", "True and false equations", "Missing numbers"], "1.OA.D.7, 1.OA.D.8",
     """<div class="tl-model" id="bsModel"></div><div class="tl-big" id="bsEq" aria-live="polite"></div>
<div class="tl-controls" id="bsCtl"></div><div class="tl-out" id="bsOut"></div>""",
     r"""
var st;
function reset() { st = { a: 3, b: 4, c: 5, d: 1 }; draw(); }
function cubes(x, y, n, col, stroke) { var s = ''; for (var i = 0; i < n; i++) s += '<rect x="' + (x + (i % 5) * 21) + '" y="' + (y - 21 - Math.floor(i / 5) * 21) + '" width="19" height="19" rx="3" fill="' + col + '" stroke="' + stroke + '" stroke-width="2"/>'; return s; }
function draw() {
  var L = st.a + st.b, R = st.c + st.d, ang = K.clamp((R - L) * 5, -16, 16), rad = ang * Math.PI / 180, s = '';
  var cx = 380, cy = 110, half = 225;
  var lx = cx - half * Math.cos(rad), ly = cy - half * Math.sin(rad), rx = cx + half * Math.cos(rad), ry = cy + half * Math.sin(rad);
  s += '<path d="M' + (cx - 50) + ' 330 L' + cx + ' ' + (cy + 8) + ' L' + (cx + 50) + ' 330 Z" fill="#8a4fd6" stroke="#4c1d95" stroke-width="3"/>';
  s += '<line x1="' + lx + '" y1="' + ly + '" x2="' + rx + '" y2="' + ry + '" stroke="#4c1d95" stroke-width="12" stroke-linecap="round"/><circle cx="' + cx + '" cy="' + cy + '" r="10" fill="#ffd34d" stroke="#4c1d95" stroke-width="3"/>';
  [[lx, ly, st.a, st.b, 'Left'], [rx, ry, st.c, st.d, 'Right']].forEach(function (p) {
    var px = p[0], py = p[1] + 100;
    s += '<line x1="' + p[0] + '" y1="' + p[1] + '" x2="' + (px - 108) + '" y2="' + py + '" stroke="#55657a" stroke-width="2"/><line x1="' + p[0] + '" y1="' + p[1] + '" x2="' + (px + 108) + '" y2="' + py + '" stroke="#55657a" stroke-width="2"/>';
    s += '<path d="M' + (px - 118) + ' ' + py + ' h236 l-18 20 h-200 z" fill="#cfe8da" stroke="#0d6b3c" stroke-width="3"/>';
    s += cubes(px - 110, py, p[2], '#e5484d', '#8c1d22') + cubes(px + 6, py, p[3], '#1f78c8', '#123f73');
  });
  $('bsModel').innerHTML = K.svg(760, 340, s, 'Balance: left side ' + L + ' cubes, right side ' + R + ' cubes');
  $('bsCtl').innerHTML = K.step('a', 'Left: red', [1], st.a) + K.step('b', 'Left: blue', [1], st.b) + K.step('c', 'Right: red', [1], st.c) + K.step('d', 'Right: blue', [1], st.d);
  function side(x, y) { return y ? x + ' + ' + y : String(x); }
  var eq = L === R;
  $('bsEq').innerHTML = side(st.a, st.b) + (eq ? ' = ' : ' <span style="color:#b42318">?</span> ') + side(st.c, st.d);
  $('bsOut').innerHTML = eq ? '<span class="el-ok">True!</span> Both sides are worth <b>' + L + '</b>, so the scale is level. The equal sign means <b>the same amount as</b>.' :
    '<span class="el-no">Not equal.</span> The left side is <b>' + L + '</b> and the right side is <b>' + R + '</b>. The <b>' + (L > R ? 'left' : 'right') + '</b> side is heavier, so it goes down. Writing “=” here would be false.';
  T.update({ a: st.a, b: st.b, c: st.c, d: st.d, L: L, R: R });
}
var CH = [
  { text: 'Make 4 + 3 balance with 5 + ?', test: function (s) { return s.a === 4 && s.b === 3 && s.c === 5 && s.d === 2; } },
  { text: 'Make both sides 10, using different numbers on each side.', test: function (s) { return s.L === 10 && s.R === 10 && s.a && s.b && s.c && s.d && Math.min(s.a, s.b) !== Math.min(s.c, s.d); } },
  { text: 'Show 7 = 7 with just one number on each side.', test: function (s) { return s.L === 7 && s.R === 7 && (!s.a || !s.b) && (!s.c || !s.d); } },
  { text: 'Show 6 + 2 = 2 + 6.', test: function (s) { return s.a === 6 && s.b === 2 && s.c === 2 && s.d === 6; } },
  { text: 'Make the right side go down. Is the equation true or false?', test: function (s) { return s.R > s.L; } },
  { text: 'Find the missing number: 9 + ? = 10 + 4.', test: function (s) { return s.a === 9 && s.b === 5 && s.c === 10 && s.d === 4; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
T.steppers($('bsCtl'), function (k, d) { st[k] = K.clamp(st[k] + d, 0, 10); draw(); });
reset();
""",
     [("Put 5 + 3 on the left. Put 6 on the right. What must you add to the right side to balance?", "2 (5 + 3 = 6 + 2)"),
      ("Is 8 = 5 + 3 true or false?", "True. Both sides are 8."),
      ("Is 6 + 1 = 6 + 2 true or false? Which side goes down?", "False. The right side (8) goes down because 8 is more than 7."),
      ("Find the missing number: 9 + 4 = __ + 3", "10"),
      ("Find the missing number: 7 + __ = 10 + 2", "5"),
      ("Write two different ways to balance 10 on both sides.", "Any two, for example 4 + 6 = 7 + 3"),
      ("Reflect: What does the equal sign mean?", "Both sides are worth the same amount.")],
     ["The equal sign means “is the same amount as.” It does not mean “the answer comes next.”",
      "When both sides are worth the same, the scale is level and the equation is true.",
      "The heavier side goes down. An equation with sides that are not the same is false.",
      "6 + 2 and 2 + 6 balance: changing the order does not change the total."],
     ["Read equations both ways: 7 = 4 + 3 is as true as 4 + 3 = 7.",
      "For a missing number, ask: How many is the full side worth? How many does the other side already have?",
      "Display false equations (6 + 1 = 6 + 2) and ask students to fix them in two different ways."])

# ------------------------------------------------------------------ Hundred Chart
tool(G, "hundred-chart", ["count-120", "add-subtract-100"], "Hundred Chart Hopper",
     "Hop on a chart from 1 to 120 by ones and tens. See 10 more and 10 less, and write each trip as an addition or subtraction.",
     "Tap a number to start there. Hop with +1, −1, +10 and −10 (or the arrow keys) and watch the number sentence.",
     ["Counting to 120", "10 more and 10 less", "Adding and subtracting tens"], "1.NBT.A.1, 1.NBT.C.4, 1.NBT.C.5, 1.NBT.C.6",
     """<div class="tl-model" id="hcModel"></div>
<div class="tl-controls" id="hcCtl"><button type="button" class="tl-btn" data-h="-10">−10 (up)</button><button type="button" class="tl-btn" data-h="-1">−1 (left)</button><span class="tl-big" id="hcNum" aria-live="polite"></span><button type="button" class="tl-btn" data-h="1">+1 (right)</button><button type="button" class="tl-btn" data-h="10">+10 (down)</button><button type="button" class="tl-btn" id="hcStart">Start here</button></div>
<div class="tl-out" id="hcOut"></div>""",
     r"""
var st;
function reset() { st = { n: 12, start: 12, jumps: [], visited: { 12: 1 }, msg: '' }; draw(); }
function draw() {
  var s = '', W = 64, H = 40;
  for (var v = 1; v <= 120; v++) {
    var r = Math.floor((v - 1) / 10), c = (v - 1) % 10, x = 4 + c * W, y = 4 + r * H;
    var fill = v === st.n ? '#f08c1a' : (v === st.n + 10 || v === st.n - 10) ? '#cde7ff' : st.visited[v] ? '#ffe8c7' : '#fff';
    s += '<g class="el-cell" data-v="' + v + '"><rect x="' + x + '" y="' + y + '" width="' + W + '" height="' + H + '" fill="' + fill + '" stroke="' + (v === st.start ? '#0d6b3c' : '#9fb7c9') + '" stroke-width="' + (v === st.start ? 4 : 1.2) + '"/>' +
      K.txt(x + W / 2, y + 27, v, { size: 19, w: v === st.n ? 900 : 700, fill: v === st.n ? '#fff' : '#1d2a3a' }) + '</g>';
  }
  $('hcModel').innerHTML = K.svg(648, 488, s, 'Number chart from 1 to 120. You are on ' + st.n + '.');
  $('hcNum').textContent = st.n;
  var sum = st.jumps.reduce(function (a, b) { return a + b; }, 0), out = '';
  if (st.jumps.length) out = '<b>Hops:</b> ' + st.start + ' ' + st.jumps.map(function (j) { return (j > 0 ? '+ ' : '− ') + Math.abs(j); }).join(' ') + ' → <b>' + st.n + '</b><br><b>Number sentence:</b> ' + st.start + (sum >= 0 ? ' + ' : ' − ') + Math.abs(sum) + ' = ' + st.n + '<br>';
  out += (st.n + 10 <= 120 ? '10 more than ' + st.n + ' is <b>' + (st.n + 10) + '</b>. ' : '') + (st.n - 10 >= 1 ? '10 less than ' + st.n + ' is <b>' + (st.n - 10) + '</b>.' : '');
  if (st.msg) out += '<br>' + st.msg;
  $('hcOut').innerHTML = out; st.msg = '';
  T.update({ n: st.n, start: st.start, jumps: st.jumps.slice() });
}
function hop(j) { var v = st.n + j; if (v < 1 || v > 120) { st.msg = 'That hop goes off the chart.'; return draw(); } st.n = v; st.jumps.push(j); st.visited[v] = 1; draw(); }
function startAt(v) { st.n = st.start = v; st.jumps = []; st.visited = {}; st.visited[v] = 1; draw(); }
var CH = [
  { text: 'Start on 23. Hop to 10 more.', test: function (s) { return s.start === 23 && s.n === 33; } },
  { text: 'Start on 50. Hop to 10 less.', test: function (s) { return s.start === 50 && s.n === 40; } },
  { text: 'Start on 7. Count by tens to 97.', test: function (s) { return s.start === 7 && s.n === 97 && s.jumps.every(function (j) { return j === 10; }); } },
  { text: 'Land on 120.', test: function (s) { return s.n === 120; } },
  { text: 'Show 45 + 30: start on 45 and hop.', test: function (s) { return s.start === 45 && s.n === 75; } },
  { text: 'Show 68 − 20: start on 68 and hop.', test: function (s) { return s.start === 68 && s.n === 48; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
$('hcCtl').addEventListener('click', function (e) { var b = e.target.closest('[data-h]'); if (b) hop(+b.dataset.h); });
$('hcStart').onclick = function () { startAt(st.n); };
$('hcModel').addEventListener('click', function (e) { var g = e.target.closest('.el-cell'); if (g) startAt(+g.dataset.v); });
window.addEventListener('keydown', function (e) { var m = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: 10, ArrowUp: -10 }[e.key]; if (m && !(e.target.closest && e.target.closest('input,select'))) { e.preventDefault(); hop(m); } });
reset();
""",
     [("Start on 36. Hop down one row. Where do you land?", "46 (10 more)"),
      ("What is 10 less than 81?", "71"),
      ("Start on 4 and hop +10 again and again. Write the numbers you land on.", "14, 24, 34, 44, 54, 64, 74, 84, 94, 104, 114"),
      ("Start on 52. Hop +10, +10, +1. Where do you land?", "73"),
      ("Use the chart: 67 − 30 = __", "37"),
      ("What number comes after 109?", "110"),
      ("Reflect: Why does moving down one row add 10?", "Each row has 10 numbers, so the number below is 10 more.")],
     ["Moving right adds 1. Moving down a row adds 10.",
      "Numbers in the same column have the same ones digit; only the tens change.",
      "Hopping +10 three times is the same as adding 30.",
      "After 99 comes 100, and the chart keeps going: 101, 102, … 120."],
     ["Cover a number with a sticky note on a printed chart and ask students to use the tool to check: What is 10 more? 10 less?",
      "Ask students to explain a trip in words: “I started on 45, hopped down 3 rows, and landed on 75.”",
      "The arrow keys hop too, which is handy on a projector."])

# ------------------------------------------------------------------ Clock
tool(G, "clock-explorer", ["telling-time"], "Clock Explorer",
     "Move the hands of a clock by hours and half hours. See the digital time and the time in words, and notice where the hour hand points.",
     "Use + and − to move the clock forward or back an hour or a half hour.",
     ["Time to the hour", "Time to the half hour"], "1.MD.B.3",
     """<div id="ckTool"></div>""",
     r"""
var CH = [
  { text: 'Show 3:00 (3 o’clock).', test: function (s) { return s.h === 3 && s.m === 0; } },
  { text: 'Show half past 7.', test: function (s) { return s.h === 7 && s.m === 30; } },
  { text: 'Start at 2:00. Move forward 30 minutes two times. What time is it?', test: function (s) { return K.histHas(s.hist, ['2:00', '2:30', '3:00']); } },
  { text: 'Show 6:30. Where is the hour hand?', test: function (s) { return s.h === 6 && s.m === 30; } },
  { text: 'Show 12:00. Where do both hands point?', test: function (s) { return s.h === 12 && s.m === 0; } },
  { text: 'Start at 9:00 and go back 1 hour.', test: function (s) { return K.histHas(s.hist, ['9:00', '8:00']); } }];
K.clockTool(Object.assign({}, META, { steps: [60, 30], level: 1, start: [1, 0], challenges: CH }));
""",
     [("Show 4:00. Where does the minute hand point?", "To the 12"),
      ("Show 8:30. Where is the hour hand?", "Halfway between the 8 and the 9"),
      ("What time is it 1 hour after 5:30?", "6:30"),
      ("Write half past 11 as a digital time.", "11:30"),
      ("At 2:30, where does the minute hand point?", "To the 6"),
      ("What time is it a half hour after 12:00?", "12:30"),
      ("Reflect: Why is the hour hand between two numbers at half past?", "It moves slowly to the next hour; at half past it has gone halfway.")],
     ["The short hand shows the hour. The long hand shows the minutes.",
      "At o’clock times the minute hand points to the 12.",
      "At half past, the minute hand points to the 6 and the hour hand is halfway to the next number.",
      "Two half hours make one hour."],
     ["Pair each clock with a daily event (lunch at 11:30, recess at 10:00) and ask students to set it.",
      "Focus on the hour hand at half past: it is between two numbers, and we say the smaller one (except between 12 and 1).",
      "The arrow keys move the clock a half hour at a time."])

# ------------------------------------------------------------------ Length
tool(G, "length-measurer", ["measuring-length"], "Measure with Cubes",
     "Line up cubes end to end to measure a crayon, marker, pencil and ribbon. See why gaps and overlaps give wrong measurements, then compare the lengths.",
     "Pick an object. Add cubes one at a time from the left end until you reach the other end. Then count.",
     ["Measuring length", "Comparing lengths"], "1.MD.A.1, 1.MD.A.2",
     """<div class="tl-controls" id="lmPick" role="group" aria-label="Choose an object"></div>
<div class="tl-model" id="lmModel"></div>
<div class="tl-controls"><button type="button" class="tl-btn" id="lmAdd">+ Add a cube</button><button type="button" class="tl-btn" id="lmSub">− Take one off</button>
<div class="tl-field el-inline"><span class="lab">How to line up</span><button type="button" class="tl-btn" data-mode="ok">End to end</button><button type="button" class="tl-btn" data-mode="gaps">With gaps</button><button type="button" class="tl-btn" data-mode="overlap">Overlapping</button></div></div>
<div class="tl-out" id="lmOut" aria-live="polite"></div>""",
     r"""
var OBJ = [['crayon', 4, '#e5484d'], ['marker', 6, '#1f78c8'], ['pencil', 7, '#ffd34d'], ['ribbon', 11, '#8a4fd6']], STEP = { ok: 1, gaps: 1.5, overlap: 0.65 }, U = 56;
var st;
function reset() { st = { obj: 2, k: 0, mode: 'ok', measured: {}, tried: {} }; draw(); }
function len() { return OBJ[st.obj][1]; }
function end(k) { return k ? STEP[st.mode] * (k - 1) + 1 : 0; }
function draw() {
  var o = OBJ[st.obj], L = o[1], s = '', i;
  $('lmPick').innerHTML = OBJ.map(function (b, i) { return '<button type="button" class="tl-btn" data-o="' + i + '" aria-pressed="' + (i === st.obj) + '">' + b[0][0].toUpperCase() + b[0].slice(1) + '</button>'; }).join('');
  Array.prototype.forEach.call(document.querySelectorAll('[data-mode]'), function (b) { b.setAttribute('aria-pressed', b.dataset.mode === st.mode); });
  var x0 = 20;
  if (o[0] === 'pencil') s += '<rect x="' + x0 + '" y="40" width="' + (L * U - 40) + '" height="44" fill="' + o[2] + '" stroke="#1d2a3a" stroke-width="3"/><path d="M' + (x0 + L * U - 40) + ' 40 l40 22 l-40 22z" fill="#f6d7a7" stroke="#1d2a3a" stroke-width="3"/>';
  else if (o[0] === 'ribbon') s += '<path d="M' + x0 + ' 44 h' + L * U + ' l-14 18 l14 18 h-' + L * U + ' l14 -18z" fill="' + o[2] + '" stroke="#1d2a3a" stroke-width="3"/>';
  else s += '<rect x="' + x0 + '" y="40" width="' + L * U + '" height="44" rx="14" fill="' + o[2] + '" stroke="#1d2a3a" stroke-width="3"/>';
  s += '<line x1="' + x0 + '" y1="20" x2="' + x0 + '" y2="190" stroke="#0d6b3c" stroke-width="3" stroke-dasharray="6 5"/><line x1="' + (x0 + L * U) + '" y1="20" x2="' + (x0 + L * U) + '" y2="190" stroke="#0d6b3c" stroke-width="3" stroke-dasharray="6 5"/>';
  for (i = 0; i < st.k; i++) { var x = x0 + STEP[st.mode] * i * U, y = st.mode === 'overlap' ? 108 + (i % 2) * 8 : 110; s += '<rect x="' + x + '" y="' + y + '" width="' + U + '" height="' + U + '" rx="5" fill="' + (i % 2 ? '#60a5fa' : '#34d399') + '" stroke="#1d2a3a" stroke-width="2.5" opacity=".92"/>' + K.txt(x + U / 2, y + 37, i + 1, { size: 20 }); }
  $('lmModel').innerHTML = K.svg(Math.max(12, L + 1.5) * U + 40, 200, s, 'A ' + o[0] + ' with ' + st.k + ' cubes below it');
  var e = end(st.k), msg;
  if (!st.k) msg = 'Start the first cube at the left end of the ' + o[0] + '.';
  else if (st.mode === 'ok') {
    if (st.k < L) msg = '<b>' + st.k + '</b> cube' + (st.k > 1 ? 's' : '') + ' so far. The ' + o[0] + ' is longer — keep going.';
    else if (st.k === L) { msg = '<span class="el-ok">The ' + o[0] + ' is ' + L + ' cubes long.</span> No gaps and no overlaps.'; st.measured[o[0]] = L; }
    else msg = 'Too many: the cubes go past the end of the ' + o[0] + '. Take one off.';
  } else {
    if (e < L) msg = '<b>' + st.k + '</b> cubes so far. Keep going to the end.';
    else { msg = '<span class="el-no">' + st.k + ' cubes reach the end, but this is not a correct measurement.</span> ' + (st.mode === 'gaps' ? 'Gaps leave parts of the ' + o[0] + ' that no cube covers, so the count is <b>too small</b>.' : 'Overlapping cubes cover some parts twice, so the count is <b>too big</b>.'); st.tried[st.mode] = 1; }
  }
  var names = Object.keys(st.measured).sort(function (a, b) { return st.measured[a] - st.measured[b]; });
  if (names.length > 1) msg += '<br><b>Shortest to longest:</b> ' + names.map(function (n) { return n + ' (' + st.measured[n] + ')'; }).join(', ');
  $('lmOut').innerHTML = msg;
  $('lmSub').disabled = !st.k; $('lmAdd').disabled = end(st.k) > L + 1;
  T.update({ obj: o[0], k: st.k, mode: st.mode, measured: Object.assign({}, st.measured), tried: Object.assign({}, st.tried) });
}
var CH = [
  { text: 'Measure the pencil with no gaps or overlaps.', test: function (s) { return s.measured.pencil; } },
  { text: 'Measure the crayon. Which is longer, the crayon or the pencil?', test: function (s) { return s.measured.pencil && s.measured.crayon; } },
  { text: 'Line up the cubes with gaps. Is the count too big or too small?', test: function (s) { return s.tried.gaps; } },
  { text: 'Now try overlapping cubes. What happens to the count?', test: function (s) { return s.tried.overlap; } },
  { text: 'Measure the ribbon and the marker. How many cubes longer is the ribbon?', test: function (s) { return s.measured.ribbon && s.measured.marker; } },
  { text: 'Measure all four things and put them in order.', test: function (s) { return Object.keys(s.measured).length === 4; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
$('lmPick').addEventListener('click', function (e) { var b = e.target.closest('[data-o]'); if (b) { st.obj = +b.dataset.o; st.k = 0; draw(); } });
document.addEventListener('click', function (e) { var b = e.target.closest('[data-mode]'); if (b) { st.mode = b.dataset.mode; st.k = 0; draw(); } });
$('lmAdd').onclick = function () { st.k++; draw(); };
$('lmSub').onclick = function () { st.k = Math.max(0, st.k - 1); draw(); };
reset();
""",
     [("How many cubes long is the pencil?", "7 cubes"),
      ("How many cubes long is the crayon?", "4 cubes"),
      ("How many cubes longer is the pencil than the crayon?", "3 cubes"),
      ("Put the crayon, marker, pencil and ribbon in order from shortest to longest.", "crayon (4), marker (6), pencil (7), ribbon (11)"),
      ("Measure the pencil with gaps. How many cubes reach the end? Is that the real length?", "5 cubes. No — gaps make the count too small; it is really 7."),
      ("Measure the pencil with overlapping cubes. How many cubes? Is that right?", "11 cubes. No — overlaps make the count too big."),
      ("Reflect: Why must the cubes touch with no gaps and no overlaps?", "So every part of the length is counted exactly once.")],
     ["Start measuring at one end and stop at the other end.",
      "Units must touch end to end: gaps make the count too small and overlaps make it too big.",
      "A longer object needs more cubes.",
      "Measuring with the same unit lets us compare and order lengths."],
     ["Model a gap and an overlap on the projector, then ask students to predict whether the count will be too big or too small before pressing +.",
      "Connect to real cubes: students measure a classroom pencil and compare with the tool.",
      "Ask comparison questions: How many cubes longer is the ribbon than the marker? (5)"])

# ------------------------------------------------------------------ Graphs
tool(G, "graph-builder", ["data"], "Tally and Picture Graph Builder",
     "Collect votes for favorite fruits, show them with tally marks, a table or a picture graph, and answer how many in all, how many more and how many fewer.",
     "Use + and − to add votes. Switch between the tally chart, the table and the picture graph.",
     ["Tally marks", "Picture graphs", "Comparing data"], "1.MD.C.4",
     """<div id="grTool"></div>""",
     r"""
var CH = [
  { text: 'Give Apples 5 votes. What do 5 tally marks look like?', test: function (s) { return s.c[0] === 5 && s.view === 'tally'; } },
  { text: 'Make Bananas 2 more than Grapes.', test: function (s) { return s.c[1] === s.c[2] + 2; } },
  { text: 'Make 12 votes in all.', test: function (s) { return s.total === 12; } },
  { text: 'Make two fruits tie.', test: function (s) { return s.c[0] === s.c[1] || s.c[1] === s.c[2] || s.c[0] === s.c[2]; } },
  { text: 'Look at the picture graph.', test: function (s) { return s.seen.pic; } },
  { text: 'Make Grapes the favorite fruit.', test: function (s) { return s.c[2] > s.c[0] && s.c[2] > s.c[1]; } }];
K.graphTool(Object.assign({}, META, { toolTitle: META.title, title: 'Our Favorite Fruit', cats: ['Apples', 'Bananas', 'Grapes'], counts: [4, 6, 3], max: 10, steps: [1], views: ['tally', 'table', 'pic'], keys: [1], scales: [1], challenges: CH }));
""",
     [("How many votes are there in all? (Apples 4, Bananas 6, Grapes 3)", "13"),
      ("How many more votes do Bananas have than Grapes?", "3 more"),
      ("Which fruit has the most votes?", "Bananas"),
      ("Add 2 votes to Apples. How many do Apples have now? Which fruits tie?", "6. Apples and Bananas tie."),
      ("Draw the tally marks for 7.", "One bundle of 5 (4 lines crossed by 1) and 2 more lines"),
      ("How many fewer votes do Grapes have than Bananas?", "3 fewer"),
      ("Reflect: Why do we cross the fifth tally mark?", "It makes bundles of 5, so we can count by fives.")],
     ["Each tally mark, each row in the table and each face stands for one vote.",
      "Tally marks are grouped in fives so they are quick to count.",
      "To find how many more, compare the two counts: 6 is 3 more than 3.",
      "The total is all the votes added together."],
     ["Collect a real class vote and enter it with the class watching.",
      "Ask the three kinds of questions the standard names: how many in all, how many in each category, and how many more or fewer.",
      "Switch views without changing the votes and ask: Did anything change? (No — the same data, a different display.)"])

# ------------------------------------------------------------------ Equal shares
tool(G, "equal-shares", ["shapes-equal-shares"], "Equal Shares",
     "Cut circles, rectangles and squares into halves and fourths, color the shares, and see why parts must be the same size.",
     "Choose a shape and how many parts. Tap a part to color it. Try Not equal parts to see shares that are not halves or fourths.",
     ["Halves", "Fourths", "Equal shares"], "1.G.A.3",
     """<div id="shTool"></div>""",
     r"""
var CH = [
  { text: 'Cut the circle into halves and color one half.', test: function (s) { return s.shape === 'circle' && s.parts === 2 && s.equal && s.shaded === 1; } },
  { text: 'Cut the rectangle into fourths and color one fourth.', test: function (s) { return s.shape === 'rectangle' && s.parts === 4 && s.equal && s.shaded === 1; } },
  { text: 'Find parts that are NOT equal shares.', test: function (s) { return !s.equal; } },
  { text: 'Color all four fourths. What do you have?', test: function (s) { return s.parts === 4 && s.equal && s.shaded === 4; } },
  { text: 'Look at halves and then fourths of the same shape. Which share is bigger?', test: function (s) { return ['circle', 'rectangle', 'square'].some(function (x) { return s.seen[x + '2e'] && s.seen[x + '4e']; }); } },
  { text: 'Color 2 fourths of the square. Is it the same amount as one half?', test: function (s) { return s.shape === 'square' && s.parts === 4 && s.equal && s.shaded === 2; } }];
K.sharesTool(Object.assign({}, META, { toolTitle: META.title, shapes: ['circle', 'rectangle', 'square'], parts: [2, 4], challenges: CH }));
""",
     [("Cut a circle into 2 equal shares. What is each share called?", "A half (one half)"),
      ("How many fourths make a whole rectangle?", "4 fourths"),
      ("Which is bigger: one half or one fourth of the same circle?", "One half"),
      ("A rectangle is cut into 2 parts that are not the same size. Are they halves?", "No. Halves must be equal shares."),
      ("Color 2 fourths of a square. How much of the square is colored?", "Two fourths, the same amount as one half"),
      ("How many halves make one whole?", "2 halves"),
      ("Reflect: Why does cutting into more equal shares make each share smaller?", "The same whole is split among more parts, so each part gets less.")],
     ["Equal shares are parts that are all the same size.",
      "2 equal shares are halves. 4 equal shares are fourths (also called quarters).",
      "All the shares together make one whole.",
      "The more equal shares you cut, the smaller each share is."],
     ["Use the Not equal parts button as a non-example: Are these halves? How do you know?",
      "Compare a half and a fourth of the same shape side by side; ask which you would rather have of a pizza.",
      "Students can tap shares or use Tab and Enter to color them."])
