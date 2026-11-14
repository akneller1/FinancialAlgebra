"""Grade 3 Interactive Math tools (math3-*)."""
from reg import tool

G = 3

# ------------------------------------------------------------------ Equal Groups (multiplication and division)
tool(G, "equal-groups", ["multiplication-meaning", "division-meaning", "patterns-unknowns-two-step"], "Equal Groups Explorer",
     "Make equal groups or arrays to multiply, then share or group counters to divide. See multiplication, repeated addition and division equations side by side.",
     "Choose Multiply or Divide. Set the numbers with + and −, and watch the groups and the equations change.",
     ["Equal groups", "Arrays", "Division as sharing and grouping"], "3.OA.A.1, 3.OA.A.2, 3.OA.A.3, 3.OA.B.6",
     """<div class="tl-controls el-view" role="group" aria-label="Multiply or divide"><button type="button" class="tl-btn" data-mode="mult">Multiply</button><button type="button" class="tl-btn" data-mode="div">Divide</button><span id="egSub" style="display:flex;gap:.4rem;margin-left:1rem"></span></div>
<div class="tl-model" id="egModel"></div><div class="tl-big" id="egEq" aria-live="polite"></div><div class="tl-controls" id="egCtl"></div><div class="tl-out" id="egOut"></div>""",
     r"""
var st;
function reset() { st = { mode: 'mult', g: 3, s: 5, view: 'groups', T: 12, d: 3, how: 'share', seen: {} }; draw(); }
function plates(list, left) {
  var x = 10, y = 10, rowH = 0, s = '', W = 760;
  list.forEach(function (n) {
    var cols = Math.max(1, Math.min(5, n)), rows = Math.max(1, Math.ceil(n / 5)), w = Math.max(64, cols * 22 + 22), h = rows * 22 + 22;
    if (x + w > W) { x = 10; y += rowH + 12; rowH = 0; }
    s += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="16" fill="#f2fbf5" stroke="#1fa565" stroke-width="2.5"/>';
    for (var i = 0; i < n; i++) s += '<circle cx="' + (x + 22 + (i % 5) * 22) + '" cy="' + (y + 22 + Math.floor(i / 5) * 22) + '" r="8.5" fill="#e5484d" stroke="#8c1d22" stroke-width="2"/>';
    x += w + 12; rowH = Math.max(rowH, h);
  });
  if (left) { if (x + 140 > W) { x = 10; y += rowH + 12; rowH = 44; } s += K.txt(x + 4, y + 18, 'left over:', { a: 'start', size: 15, fill: '#b45309' }); for (var j = 0; j < left; j++) s += '<circle cx="' + (x + 12 + (j % 5) * 22) + '" cy="' + (y + 38 + Math.floor(j / 5) * 22) + '" r="8.5" fill="#f08c1a" stroke="#1d2a3a" stroke-width="2" stroke-dasharray="3 2"/>'; rowH = Math.max(rowH, 44 + Math.ceil(left / 5) * 22); }
  return K.svg(W + 20, y + rowH + 12, s, list.length + ' groups' + (left ? ' and ' + left + ' left over' : ''));
}
function draw() {
  Array.prototype.forEach.call(document.querySelectorAll('[data-mode]'), function (b) { b.setAttribute('aria-pressed', b.dataset.mode === st.mode); });
  var out, eq, i;
  if (st.mode === 'mult') {
    var P = st.g * st.s, rep = []; for (i = 0; i < st.g; i++) rep.push(st.s);
    $('egSub').innerHTML = '<button type="button" class="tl-btn" data-view="groups" aria-pressed="' + (st.view === 'groups') + '">Groups</button><button type="button" class="tl-btn" data-view="array" aria-pressed="' + (st.view === 'array') + '">Array</button>';
    if (st.view === 'groups') { var L = []; for (i = 0; i < st.g; i++) L.push(st.s); $('egModel').innerHTML = plates(L, 0); }
    else { var s = ''; for (var r = 0; r < st.g; r++) for (var c = 0; c < st.s; c++) s += '<circle cx="' + (24 + c * 34) + '" cy="' + (22 + r * 34) + '" r="12" fill="#e5484d" stroke="#8c1d22" stroke-width="2"/>'; $('egModel').innerHTML = K.svg(Math.max(380, st.s * 34 + 20), st.g * 34 + 10, s, st.g + ' rows of ' + st.s); }
    $('egCtl').innerHTML = K.step('g', st.view === 'groups' ? 'Number of groups' : 'Rows', [1], st.g) + K.step('s', st.view === 'groups' ? 'In each group' : 'In each row', [1], st.s);
    eq = st.g + ' × ' + st.s + ' = ' + P;
    out = '<b>' + st.g + '</b> ' + (st.view === 'groups' ? 'group' + (st.g > 1 ? 's' : '') + ' of' : 'row' + (st.g > 1 ? 's' : '') + ' of') + ' <b>' + st.s + '</b> is <b>' + P + '</b> in all.<br>Repeated addition: ' + rep.join(' + ') + ' = ' + P;
    st.seen[st.g + 'x' + st.s] = 1;
  } else {
    var q = Math.floor(st.T / st.d), left = st.T % st.d, list = [];
    $('egSub').innerHTML = '<button type="button" class="tl-btn" data-how="share" aria-pressed="' + (st.how === 'share') + '">Share into groups</button><button type="button" class="tl-btn" data-how="group" aria-pressed="' + (st.how === 'group') + '">Make groups of</button>';
    if (st.how === 'share') { for (i = 0; i < st.d; i++) list.push(q); } else { for (i = 0; i < q; i++) list.push(st.d); }
    $('egModel').innerHTML = plates(list, left);
    $('egCtl').innerHTML = K.step('T', 'Total counters', [1, 5], st.T) + K.step('d', st.how === 'share' ? 'Number of groups' : 'Size of each group', [1], st.d);
    eq = left ? st.T + ' ÷ ' + st.d + ' is not a whole number' : st.T + ' ÷ ' + st.d + ' = ' + q;
    if (left) out = '<b>' + st.T + '</b> cannot be ' + (st.how === 'share' ? 'shared equally into ' + st.d + ' groups' : 'put into equal groups of ' + st.d) + ': <b>' + left + '</b> left over. Try a different total.';
    else out = (st.how === 'share' ? 'Share <b>' + st.T + '</b> into <b>' + st.d + '</b> equal groups: <b>' + q + '</b> in each group.' : 'Put <b>' + st.T + '</b> into groups of <b>' + st.d + '</b>: <b>' + q + '</b> groups.') + '<br>Check with multiplication: ' + (st.how === 'share' ? st.d + ' × ' + q : q + ' × ' + st.d) + ' = ' + st.T + '. The unknown factor is ' + q + '.';
  }
  $('egEq').textContent = eq; $('egOut').innerHTML = out;
  T.update({ mode: st.mode, g: st.g, s: st.s, view: st.view, T: st.T, d: st.d, how: st.how, left: st.T % st.d, seen: Object.assign({}, st.seen) });
}
var CH = [
  { text: 'Show 4 groups of 6. What is the product?', test: function (s) { return s.mode === 'mult' && s.g === 4 && s.s === 6; } },
  { text: 'Show 6 groups of 4. Is the product the same as 4 groups of 6?', test: function (s) { return s.seen['4x6'] && s.seen['6x4']; } },
  { text: 'Show 3 × 7 as an array.', test: function (s) { return s.mode === 'mult' && s.view === 'array' && s.g === 3 && s.s === 7; } },
  { text: 'Share 24 equally into 4 groups.', test: function (s) { return s.mode === 'div' && s.how === 'share' && s.T === 24 && s.d === 4; } },
  { text: 'Put 24 into groups of 4. How many groups?', test: function (s) { return s.mode === 'div' && s.how === 'group' && s.T === 24 && s.d === 4; } },
  { text: 'Find a number that cannot be shared equally into 5 groups.', test: function (s) { return s.mode === 'div' && s.how === 'share' && s.d === 5 && s.T > 0 && s.left > 0; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
T.steppers($('egCtl'), function (k, d) { st[k] = K.clamp(st[k] + d, k === 'T' ? 0 : 1, k === 'T' ? 60 : 10); draw(); });
document.addEventListener('click', function (e) { var b = e.target.closest('[data-mode],[data-view],[data-how]'); if (!b) return; if (b.dataset.mode) st.mode = b.dataset.mode; if (b.dataset.view) st.view = b.dataset.view; if (b.dataset.how) st.how = b.dataset.how; draw(); });
reset();
""",
     [("Show 5 groups of 3. Write a multiplication equation.", "5 × 3 = 15"),
      ("Write 7 × 4 as repeated addition and find the product.", "4 + 4 + 4 + 4 + 4 + 4 + 4 = 28"),
      ("How many counters are in an array with 3 rows of 8?", "24 (3 × 8 = 24)"),
      ("Share 18 equally into 3 groups. How many are in each group?", "6 (18 ÷ 3 = 6)"),
      ("Put 18 into groups of 3. How many groups?", "6 groups (18 ÷ 3 = 6)"),
      ("Find the unknown number: 4 × ? = 32", "8, because 4 groups of 8 is 32 (32 ÷ 4 = 8)"),
      ("Reflect: How are sharing and grouping different? How are they the same?", "Sharing knows the number of groups and finds the size; grouping knows the size and finds the number of groups. Both are division.")],
     ["Multiplication counts equal groups: 4 × 6 means 4 groups of 6.",
      "4 groups of 6 and 6 groups of 4 have the same product.",
      "Division can mean sharing into a number of groups or making groups of a size.",
      "Every division fact has a matching multiplication fact: 24 ÷ 4 = 6 because 4 × 6 = 24."],
     ["Ask students to tell a story for an equation before building it: “3 bags with 7 apples each.”",
      "Use the two division buttons with the same numbers to show that 24 ÷ 4 has two meanings and one answer.",
      "Totals that leave counters over set up the idea that some numbers cannot be shared equally."])

# ------------------------------------------------------------------ Break-Apart Arrays (distributive property)
tool(G, "break-apart-array", ["properties-fact-strategies", "area"], "Break-Apart Arrays",
     "Split an array of unit squares into two smaller arrays to find hard facts from easier ones. Rotate the array to see the commutative property.",
     "Set the rows and columns, then move the split line. Use Rotate to turn the array.",
     ["Distributive property", "Commutative property", "Area models"], "3.OA.B.5, 3.OA.C.7, 3.MD.C.7c",
     """<div class="tl-model" id="baModel"></div><div class="tl-big" id="baEq" aria-live="polite"></div>
<div class="tl-controls" id="baCtl"></div><div class="tl-controls" style="margin-top:.6rem"><button type="button" class="tl-btn" id="baRot">Rotate ↻</button></div><div class="tl-out" id="baOut"></div>""",
     r"""
var st;
function reset() { st = { r: 3, c: 5, k: 2, rots: 0 }; draw(); }
function draw() {
  var U = 40, s = '', i, j, X = 30, Y = 30;
  for (i = 0; i < st.r; i++) for (j = 0; j < st.c; j++) s += '<rect x="' + (X + j * U) + '" y="' + (Y + i * U) + '" width="' + U + '" height="' + U + '" fill="' + (j < st.k ? '#bfe6d0' : '#cde7ff') + '" stroke="#1d2a3a" stroke-width="1.6"/>';
  if (st.k > 0 && st.k < st.c) s += '<line x1="' + (X + st.k * U) + '" y1="' + (Y - 18) + '" x2="' + (X + st.k * U) + '" y2="' + (Y + st.r * U + 18) + '" stroke="#d63c7a" stroke-width="5" stroke-dasharray="10 6"/>';
  s += K.txt(X - 14, Y + st.r * U / 2 + 6, st.r, { size: 20 }) + (st.k ? K.txt(X + st.k * U / 2, Y - 8, st.k, { size: 20, fill: '#0d6b3c' }) : '') + (st.c - st.k ? K.txt(X + (st.k + st.c) * U / 2, Y - 8, st.c - st.k, { size: 20, fill: '#1f78c8' }) : '');
  $('baModel').innerHTML = K.svg(Math.max(460, st.c * U + 60), st.r * U + 60, s, st.r + ' by ' + st.c + ' array split after ' + st.k + ' columns');
  $('baCtl').innerHTML = K.step('r', 'Rows', [1], st.r) + K.step('c', 'Columns', [1], st.c) + K.step('k', 'Split after column', [1], st.k);
  var P = st.r * st.c, A = st.r * st.k, B = st.r * (st.c - st.k);
  $('baEq').textContent = st.r + ' × ' + st.c + ' = ' + P;
  $('baOut').innerHTML = st.k > 0 && st.k < st.c ? '<b>Break apart:</b> ' + st.r + ' × ' + st.c + ' = ' + st.r + ' × ' + st.k + ' + ' + st.r + ' × ' + (st.c - st.k) + ' = ' + A + ' + ' + B + ' = <b>' + P + '</b><br>As area: the ' + st.r + ' by ' + st.c + ' rectangle has an area of <b>' + P + ' square units</b>.' :
    'Move the split line to break the array into two smaller arrays.<br>As area: ' + st.r + ' rows of ' + st.c + ' unit squares = <b>' + P + ' square units</b>.';
  T.update({ r: st.r, c: st.c, k: st.k, rots: st.rots });
}
var CH = [
  { text: 'Make a 7 × 8 array (7 rows, 8 columns).', test: function (s) { return s.r === 7 && s.c === 8; } },
  { text: 'Break 7 × 8 into 7 × 5 + 7 × 3.', test: function (s) { return s.r === 7 && s.c === 8 && (s.k === 5 || s.k === 3); } },
  { text: 'Break 6 × 9 apart using a 5s fact.', test: function (s) { return s.r === 6 && s.c === 9 && (s.k === 5 || s.k === 4); } },
  { text: 'Make 4 × 6, then Rotate it to 6 × 4. Did the total change?', test: function (s) { return s.rots > 0 && s.r === 6 && s.c === 4; } },
  { text: 'Split an array into two equal parts.', test: function (s) { return s.k > 0 && s.k * 2 === s.c; } },
  { text: 'Break 8 × 7 into 8 × 2 + 8 × 5.', test: function (s) { return s.r === 8 && s.c === 7 && (s.k === 2 || s.k === 5); } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
T.steppers($('baCtl'), function (k, d) { if (k === 'k') st.k = K.clamp(st.k + d, 0, st.c); else { st[k] = K.clamp(st[k] + d, 1, 10); st.k = Math.min(st.k, st.c); } draw(); });
$('baRot').onclick = function () { var r = st.r; st.r = st.c; st.c = r; st.k = Math.min(st.k, st.c); st.rots++; draw(); };
reset();
""",
     [("Break 6 × 7 into 6 × 5 + 6 × 2. Find each part and the total.", "30 + 12 = 42"),
      ("Break 8 × 6 into two equal parts. Write the equation.", "8 × 3 + 8 × 3 = 24 + 24 = 48"),
      ("Use a 5s fact to find 4 × 9.", "4 × 5 + 4 × 4 = 20 + 16 = 36"),
      ("Rotate 7 × 4. What is 4 × 7?", "28 — the same as 7 × 4"),
      ("What is the area of a rectangle 3 units by 8 units?", "24 square units"),
      ("Fill in the blank: 9 × 6 = 9 × 5 + 9 × __", "1"),
      ("Reflect: Why does breaking an array apart give the same total?", "No squares are added or taken away — the two smaller arrays still cover the whole array.")],
     ["Breaking an array into two parts does not change the total: 7 × 8 = 7 × 5 + 7 × 3.",
      "Facts with 2, 5 and 10 are easy anchors for harder facts.",
      "Rotating an array swaps rows and columns but keeps the total: 4 × 6 = 6 × 4.",
      "An array of unit squares is a rectangle; its area is rows × columns."],
     ["Ask: Which split makes this fact easiest for you? There are several good answers.",
      "Connect to area (3.MD.C.7c): the same picture is a rectangle split into two rectangles.",
      "Record students’ splits on the board to show that different splits give the same product."])

# ------------------------------------------------------------------ Multiplication Table Patterns
tool(G, "multiplication-table", ["patterns-unknowns-two-step", "properties-fact-strategies", "multiplication-meaning"], "Multiplication Table Patterns",
     "Explore the 10 × 10 multiplication table. Highlight a row, shade even products, find every way to make a product, and solve missing-factor puzzles.",
     "Tap a cell (or use the arrow keys) to see its fact. Use the buttons to highlight patterns and to try a missing-factor puzzle.",
     ["Multiplication facts", "Patterns", "Unknown factors"], "3.OA.A.4, 3.OA.B.5, 3.OA.C.7, 3.OA.D.9",
     """<div class="tl-model" id="mtModel"></div>
<div class="tl-controls" id="mtCtl"></div>
<div class="tl-controls" style="margin-top:.6rem"><button type="button" class="tl-btn" id="mtEven" aria-pressed="false">Shade even products</button><button type="button" class="tl-btn" id="mtSq" aria-pressed="false">Show square numbers</button><button type="button" class="tl-btn" id="mtPz">Missing-factor puzzle</button></div>
<div class="tl-out" id="mtOut" aria-live="polite"></div>""",
     r"""
var PZ = [[0, 8, 56], [6, 0, 42], [0, 9, 63], [7, 0, 28], [0, 4, 36], [5, 0, 45]];
var st;
function reset() { st = { a: 0, b: 0, row: 0, even: false, sq: false, picked: {}, pz: -1, solved: 0, msg: '' }; draw(); }
function draw() {
  var W = 56, H = 42, s = '', i, j;
  for (i = 0; i <= 10; i++) for (j = 0; j <= 10; j++) {
    var x = 4 + j * W, y = 4 + i * H, head = !i || !j, p = i * j, v = head ? (i || j || '×') : p;
    var fill = head ? '#22408a' : '#fff';
    if (!head) {
      if (st.even && p % 2 === 0) fill = '#e3f6ea';
      if (st.row && (i === st.row || j === st.row)) fill = '#ffe8c7';
      if (st.sq && i === j) fill = '#efe3ff';
      if (st.picked[i + 'x' + j]) fill = '#cde7ff';
      if (i === st.a && j === st.b) fill = '#f08c1a';
    }
    s += '<g' + (head ? '' : ' class="el-cell" data-a="' + i + '" data-b="' + j + '"') + '><rect x="' + x + '" y="' + y + '" width="' + W + '" height="' + H + '" fill="' + fill + '" stroke="#9fb7c9" stroke-width="1.2"/>' +
      K.txt(x + W / 2, y + 28, v, { size: 18, w: head ? 900 : (i === st.a && j === st.b ? 900 : 700), fill: head ? '#fff' : (i === st.a && j === st.b ? '#fff' : '#1d2a3a') }) + '</g>';
  }
  $('mtModel').innerHTML = K.svg(624, 470, s, 'Multiplication table from 1 × 1 to 10 × 10' + (st.a ? '. Selected ' + st.a + ' × ' + st.b : ''));
  $('mtCtl').innerHTML = K.step('row', 'Highlight the row and column for', [1], st.row || 'none');
  $('mtEven').setAttribute('aria-pressed', st.even); $('mtSq').setAttribute('aria-pressed', st.sq);
  var out = '';
  if (st.pz >= 0) { var z = PZ[st.pz]; out += '<b>Puzzle:</b> ' + (z[0] || '?') + ' × ' + (z[1] || '?') + ' = ' + z[2] + '. Tap the cell that solves it.<br>'; }
  if (st.a) {
    var p = st.a * st.b, pairs = [];
    for (i = 1; i <= 10; i++) if (p % i === 0 && p / i <= 10) pairs.push(i + ' × ' + (p / i));
    out += '<b>' + st.a + ' × ' + st.b + ' = ' + p + '</b>. ' + (st.a !== st.b ? 'Also ' + st.b + ' × ' + st.a + ' = ' + p + '. ' : '') + 'In this table, ' + p + ' is ' + pairs.join(', ') + '.';
  } else out += 'Tap a cell to see its multiplication fact.';
  if (st.row) out += '<br>The ' + st.row + 's: ' + [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(function (k) { return k * st.row; }).join(', ') + (st.row === 5 ? ' — they end in 5 or 0.' : st.row % 2 === 0 ? ' — all even.' : st.row === 9 ? ' — the digits add to 9.' : '.');
  if (st.msg) out += '<br>' + st.msg;
  $('mtOut').innerHTML = out; st.msg = '';
  T.update({ a: st.a, b: st.b, row: st.row, even: st.even, sq: st.sq, picked: Object.assign({}, st.picked), solved: st.solved });
}
function pick(a, b) {
  st.a = a; st.b = b; st.picked[a + 'x' + b] = 1;
  if (st.pz >= 0) { var z = PZ[st.pz]; if (a * b === z[2] && (z[0] ? (a === z[0] || b === z[0]) : (a === z[1] || b === z[1]))) { st.solved++; st.msg = '<span class="el-ok">Solved! The missing factor is ' + z[2] / (z[0] || z[1]) + '.</span>'; st.pz = -1; } }
  draw();
}
var CH = [
  { text: 'Find 6 × 7.', test: function (s) { return s.picked['6x7']; } },
  { text: 'Highlight the 4s. What pattern do you see?', test: function (s) { return s.row === 4; } },
  { text: 'Find 7 × 6. How does it compare with 6 × 7?', test: function (s) { return s.picked['6x7'] && s.picked['7x6']; } },
  { text: 'Find every cell with the product 12.', test: function (s) { return ['2x6', '3x4', '4x3', '6x2'].every(function (k) { return s.picked[k]; }); } },
  { text: 'Shade the even products. What do you notice?', test: function (s) { return s.even; } },
  { text: 'Solve a missing-factor puzzle.', test: function (s) { return s.solved > 0; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
$('mtModel').addEventListener('click', function (e) { var g = e.target.closest('.el-cell'); if (g) pick(+g.dataset.a, +g.dataset.b); });
T.steppers($('mtCtl'), function (k, d) { st.row = K.clamp(st.row + d, 0, 10); draw(); });
$('mtEven').onclick = function () { st.even = !st.even; draw(); };
$('mtSq').onclick = function () { st.sq = !st.sq; draw(); };
$('mtPz').onclick = function () { st.pz = (st.pz + 1 + (st.pz < 0 ? st.solved : 0)) % PZ.length; st.a = st.b = 0; draw(); };
window.addEventListener('keydown', function (e) { var m = { ArrowRight: [0, 1], ArrowLeft: [0, -1], ArrowDown: [1, 0], ArrowUp: [-1, 0] }[e.key]; if (!m) return; e.preventDefault(); pick(K.clamp((st.a || 1) + m[0], 1, 10), K.clamp((st.b || 1) + m[1], 1, 10)); });
reset();
""",
     [("Use the table: 8 × 9 = __", "72"),
      ("Highlight the 5s. What digits do the products end in?", "0 or 5"),
      ("Find every way to make 24 in the table.", "3 × 8, 4 × 6, 6 × 4, 8 × 3"),
      ("Why does the table look the same on both sides of the diagonal?", "a × b = b × a, so each product appears in two matching places."),
      ("Solve: 9 × __ = 63", "7"),
      ("Shade the even products. Is 4 times any number even or odd? Why?", "Even, because 4 × a number is double 2 × that number."),
      ("Reflect: How can a pattern help you remember a hard fact like 9 × 6?", "For example, 9s products go up by 10 and down by 1 (54 is 60 − 6), and the digits add to 9.")],
     ["The table is symmetric: 6 × 7 and 7 × 6 are the same product.",
      "Every product in the 2s, 4s, 6s, 8s and 10s rows is even.",
      "The 5s end in 0 or 5; the 10s end in 0.",
      "A missing factor can be found by looking along a row for the product."],
     ["Ask students to explain a pattern using properties: 4 × n is even because it is 2 × (2 × n).",
      "Use the puzzle button for unknown-factor practice (3.OA.A.4); each press shows a new puzzle.",
      "Arrow keys move the selected cell, which works well on a projector."])

# ------------------------------------------------------------------ Rounding Number Line
tool(G, "rounding-number-line", ["addition-subtraction-1000"], "Rounding Number Line",
     "See any number from 0 to 999 between two tens or two hundreds, find the halfway point and round. Then estimate sums and differences.",
     "Set a number with + and −. Choose nearest 10 or nearest 100. Turn on Estimate to round two numbers and add or subtract.",
     ["Rounding to the nearest 10 and 100", "Estimating sums and differences"], "3.NBT.A.1, 3.NBT.A.2, 3.OA.D.8",
     """<div class="tl-controls el-view" role="group" aria-label="Round to"><button type="button" class="tl-btn" data-p="10">Nearest 10</button><button type="button" class="tl-btn" data-p="100">Nearest 100</button><button type="button" class="tl-btn" id="rnEst" aria-pressed="false">Estimate</button></div>
<div class="tl-model" id="rnModel"></div><div class="tl-controls" id="rnCtl"></div><div class="tl-out" id="rnOut" aria-live="polite"></div>""",
     r"""
var st;
function reset() { st = { n: 132, p: 10, est: false, m: 245, op: '+' }; draw(); }
function rnd(v, p) { return Math.floor(v / p) * p + (v % p >= p / 2 ? p : 0); }
function line(v, p, y, col) {
  var lo = Math.floor(v / p) * p, hi = lo + p, X0 = 60, X1 = 740, sc = function (x) { return X0 + (x - lo) / p * (X1 - X0); }, s = '', i, r = rnd(v, p);
  s += '<line x1="' + (X0 - 20) + '" y1="' + y + '" x2="' + (X1 + 20) + '" y2="' + y + '" stroke="#1d2a3a" stroke-width="3"/>';
  for (i = 0; i <= 10; i++) { var t = lo + i * p / 10, big = i === 0 || i === 10, mid = i === 5; s += '<line x1="' + sc(t) + '" y1="' + (y - (big ? 16 : mid ? 14 : 8)) + '" x2="' + sc(t) + '" y2="' + (y + (big ? 16 : mid ? 14 : 8)) + '" stroke="' + (mid ? '#8a4fd6' : '#1d2a3a') + '" stroke-width="' + (big || mid ? 3 : 1.6) + '"/>'; if (big || mid) s += K.txt(sc(t), y + 38, t, { size: big ? 20 : 16, fill: mid ? '#8a4fd6' : '#1d2a3a' }); }
  s += K.txt(sc(lo + p / 2), y + 56, 'halfway', { size: 13, w: 700, fill: '#8a4fd6' });
  s += '<path d="M' + sc(v) + ' ' + (y - 30) + ' Q' + ((sc(v) + sc(r)) / 2) + ' ' + (y - 70) + ' ' + sc(r) + ' ' + (y - 22) + '" fill="none" stroke="#1fa565" stroke-width="3" marker-end="url(#ar' + col.slice(1) + ')"/>';
  s += '<defs><marker id="ar' + col.slice(1) + '" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#1fa565"/></marker></defs>';
  s += '<circle cx="' + sc(v) + '" cy="' + y + '" r="10" fill="' + col + '" stroke="#1d2a3a" stroke-width="2"/>' + K.txt(sc(v), y - 38, v, { size: 20, fill: col });
  return s;
}
function draw() {
  Array.prototype.forEach.call(document.querySelectorAll('[data-p]'), function (b) { b.setAttribute('aria-pressed', +b.dataset.p === st.p); });
  $('rnEst').setAttribute('aria-pressed', st.est);
  var s = line(st.n, st.p, 110, '#d63c7a'), H = 180;
  if (st.est) { s += line(st.m, st.p, 290, '#1f78c8'); H = 360; }
  $('rnModel').innerHTML = K.svg(800, H, s, st.n + ' rounds to ' + rnd(st.n, st.p) + ' to the nearest ' + st.p);
  $('rnCtl').innerHTML = K.step('n', st.est ? 'First number' : 'Number', [1, 10, 100], st.n) + (st.est ? K.step('m', 'Second number', [1, 10, 100], st.m) + '<div class="tl-field"><span class="lab">Operation</span><div class="tl-step"><button type="button" class="tl-btn" data-op="+" aria-pressed="' + (st.op === '+') + '">Add</button><button type="button" class="tl-btn" data-op="-" aria-pressed="' + (st.op === '-') + '">Subtract</button></div></div>' : '');
  var lo = Math.floor(st.n / st.p) * st.p, r = rnd(st.n, st.p), half = lo + st.p / 2;
  var out = '<b>' + st.n + '</b> is between <b>' + lo + '</b> and <b>' + (lo + st.p) + '</b>. Halfway is ' + half + '. ' +
    (st.n === half ? st.n + ' is exactly halfway, so we round <b>up</b> to <b>' + r + '</b>.' : st.n % st.p === 0 ? st.n + ' is already a multiple of ' + st.p + '.' : st.n + ' is ' + (st.n > half ? 'past' : 'before') + ' halfway, so it rounds to <b>' + r + '</b>.') +
    '<br>Nearest 10: <b>' + rnd(st.n, 10) + '</b> · Nearest 100: <b>' + rnd(st.n, 100) + '</b>';
  if (st.est) {
    var a = rnd(st.n, st.p), b = rnd(st.m, st.p), sub = st.op === '-';
    if (sub && st.m > st.n) out += '<br>Make the first number the bigger one to subtract.';
    else out += '<br><b>Estimate:</b> ' + a + (sub ? ' − ' : ' + ') + b + ' = <b>' + (sub ? a - b : a + b) + '</b> · <b>Exact:</b> ' + st.n + (sub ? ' − ' : ' + ') + st.m + ' = <b>' + (sub ? st.n - st.m : st.n + st.m) + '</b>. The exact answer is reasonable if it is close to the estimate.';
  }
  $('rnOut').innerHTML = out;
  T.update({ n: st.n, p: st.p, est: st.est, m: st.m, op: st.op, r10: rnd(st.n, 10), r100: rnd(st.n, 100) });
}
var CH = [
  { text: 'Round 47 to the nearest 10.', test: function (s) { return s.n === 47 && s.p === 10; } },
  { text: 'Find a number less than 50 that rounds to 50 (nearest 10).', test: function (s) { return s.p === 10 && s.n >= 45 && s.n < 50; } },
  { text: 'Round 365 to the nearest 100.', test: function (s) { return s.n === 365 && s.p === 100; } },
  { text: 'Show a number exactly halfway between two hundreds. Which way does it round?', test: function (s) { return s.p === 100 && s.n % 100 === 50; } },
  { text: 'Find a number that rounds to 300 to the nearest 10 AND to the nearest 100.', test: function (s) { return s.r10 === 300 && s.r100 === 300; } },
  { text: 'Estimate 386 + 214 by rounding to the nearest 100.', test: function (s) { return s.est && s.n === 386 && s.m === 214 && s.p === 100 && s.op === '+'; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
T.steppers($('rnCtl'), function (k, d) { st[k] = K.clamp(st[k] + d, 0, 999); draw(); });
document.addEventListener('click', function (e) { var b = e.target.closest('[data-p],[data-op],#rnEst'); if (!b) return; if (b.dataset.p) st.p = +b.dataset.p; else if (b.dataset.op) st.op = b.dataset.op; else st.est = !st.est; draw(); });
reset();
""",
     [("Round 63 to the nearest 10.", "60"),
      ("Round 85 to the nearest 10.", "90 (85 is exactly halfway, so round up)"),
      ("Round 449 to the nearest 100.", "400"),
      ("Round 650 to the nearest 100.", "700"),
      ("List all the whole numbers that round to 70 (nearest 10).", "65, 66, 67, 68, 69, 70, 71, 72, 73, 74"),
      ("Estimate 278 + 419 to the nearest 100. Then find the exact sum.", "300 + 400 = 700. Exact: 697."),
      ("Reflect: Why do we look at the halfway point when we round?", "Numbers before halfway are closer to the lower ten or hundred; numbers at or after halfway round up.")],
     ["Every number sits between two tens (and between two hundreds).",
      "Before the halfway point, round down; at halfway or after, round up.",
      "A number can round differently to the nearest 10 and to the nearest 100.",
      "Rounding first gives an estimate you can use to check an exact answer."],
     ["Have students predict the rounded number before switching between Nearest 10 and Nearest 100.",
      "Ask for all the numbers that round to 70 — a good way to see the halfway rule.",
      "Use Estimate to check reasonableness of written addition and subtraction (3.OA.D.8)."])

# ------------------------------------------------------------------ Fraction Explorer
tool(G, "fraction-explorer", ["understanding-fractions", "equivalent-comparing-fractions"], "Fraction Bars and Number Lines",
     "Build a fraction from unit fractions on a bar and on a number line from 0 to 2. Turn on Compare to find equivalent fractions and compare fractions.",
     "Choose the number of equal parts (the denominator), then add parts with + and −. Turn on Compare for a second fraction.",
     ["Unit fractions", "Fractions on a number line", "Equivalent and comparing fractions"], "3.NF.A.1, 3.NF.A.2, 3.NF.A.3",
     """<div class="tl-model" id="fxModel"></div><div class="tl-big" id="fxEq" aria-live="polite"></div>
<div class="tl-controls" id="fxCtl"></div><div class="tl-controls" style="margin-top:.6rem"><button type="button" class="tl-btn" id="fxCmp" aria-pressed="false">Compare</button></div>
<div class="tl-controls" id="fxCtlB" hidden style="margin-top:.6rem"></div><div class="tl-out" id="fxOut"></div>""",
     r"""
var DEN = [2, 3, 4, 6, 8], st;
function reset() { st = { a: 1, b: 3, c: 2, d: 6, cmp: false }; $('fxCtlB').hidden = true; $('fxCmp').setAttribute('aria-pressed', false); draw(); }
function block(a, b, y, col, name) {
  var X0 = 60, U = 340, s = '', i;
  for (var w = 0; w < 2; w++) for (i = 0; i < b; i++) { var k = w * b + i; s += '<rect x="' + (X0 + w * U + i * U / b) + '" y="' + y + '" width="' + U / b + '" height="46" fill="' + (k < a ? col : '#fff') + '" stroke="#1d2a3a" stroke-width="2.2"/>'; if (U / b > 34) s += K.txt(X0 + w * U + (i + 0.5) * U / b, y + 30, '1/' + b, { size: 14, w: 700, fill: k < a ? '#fff' : '#9aa8b8' }); }
  s += '<rect x="' + X0 + '" y="' + y + '" width="' + U + '" height="46" fill="none" stroke="#1d2a3a" stroke-width="4"/><rect x="' + (X0 + U) + '" y="' + y + '" width="' + U + '" height="46" fill="none" stroke="#1d2a3a" stroke-width="4"/>';
  var L = y + 86; s += '<line x1="' + (X0 - 10) + '" y1="' + L + '" x2="' + (X0 + 2 * U + 10) + '" y2="' + L + '" stroke="#1d2a3a" stroke-width="3"/>';
  for (i = 0; i <= 2 * b; i++) { var x = X0 + i * U / b, whole = i % b === 0; s += '<line x1="' + x + '" y1="' + (L - (whole ? 14 : 9)) + '" x2="' + x + '" y2="' + (L + (whole ? 14 : 9)) + '" stroke="#1d2a3a" stroke-width="' + (whole ? 3 : 1.8) + '"/>'; if (whole) s += K.txt(x, L + 34, i / b, { size: 18 }); else if (U / b > 30) s += K.txt(x, L + 30, i + '/' + b, { size: 12, w: 700, fill: '#55657a' }); }
  if (a > 0) s += '<path d="M' + X0 + ' ' + (L - 6) + ' H' + (X0 + a * U / b) + '" stroke="' + col + '" stroke-width="6" stroke-linecap="round"/>';
  s += '<circle cx="' + (X0 + a * U / b) + '" cy="' + L + '" r="10" fill="' + col + '" stroke="#1d2a3a" stroke-width="2"/>' + K.txt(X0 - 34, y + 30, name, { size: 18, fill: col });
  return s;
}
function draw() {
  var s = block(st.a, st.b, 14, '#d63c7a', 'A'), H = 160;
  if (st.cmp) { s += block(st.c, st.d, 174, '#1f78c8', 'B'); H = 320; }
  $('fxModel').innerHTML = K.svg(800, H, s, 'Fraction ' + st.a + '/' + st.b + (st.cmp ? ' and ' + st.c + '/' + st.d : '') + ' on bars and number lines from 0 to 2');
  function denBtns(key, cur) { return '<div class="tl-field"><span class="lab">Equal parts in 1 whole</span><div class="tl-step">' + DEN.map(function (d) { return '<button type="button" class="tl-btn" data-den="' + key + '" data-v="' + d + '" aria-pressed="' + (d === cur) + '">' + d + '</button>'; }).join('') + '</div></div>'; }
  $('fxCtl').innerHTML = denBtns('b', st.b) + K.step('a', 'Fraction A: parts', [1], st.a);
  $('fxCtlB').innerHTML = denBtns('d', st.d) + K.step('c', 'Fraction B: parts', [1], st.c);
  var f = T.frac(st.a, st.b), out = f + ' is <b>' + st.a + '</b> part' + (st.a === 1 ? '' : 's') + ' of size ' + T.frac(1, st.b) + '. ';
  out += st.a % st.b === 0 ? 'It is a whole number: ' + f + ' = <b>' + st.a / st.b + '</b>.' : st.a < st.b ? 'It is less than 1.' : 'It is more than 1.';
  if (st.cmp) {
    var l = st.a * st.d, r = st.c * st.b, sym = l > r ? '>' : l < r ? '<' : '=';
    $('fxEq').innerHTML = f + ' ' + sym + ' ' + T.frac(st.c, st.d);
    out += '<br>' + (sym === '=' ? '<b>Equivalent!</b> Both fractions are at the same point on the number line and cover the same amount of the bar.' :
      st.b === st.d ? 'Same denominator: the parts are the same size, so the one with more parts is greater.' :
        st.a === st.c ? 'Same numerator: the same number of parts, so the one with bigger parts (fewer parts in a whole) is greater.' :
          'Look at the number lines: the fraction farther to the right is greater.');
  } else $('fxEq').innerHTML = f;
  $('fxOut').innerHTML = out;
  T.update({ a: st.a, b: st.b, c: st.c, d: st.d, cmp: st.cmp, eq: st.a * st.d === st.c * st.b });
}
var CH = [
  { text: 'Show 3/4 on the bar and the number line.', test: function (s) { return s.a === 3 && s.b === 4; } },
  { text: 'Show 1 whole as a fraction.', test: function (s) { return s.a === s.b; } },
  { text: 'Turn on Compare. Find a fraction in eighths that equals 1/2.', test: function (s) { return s.cmp && s.eq && ((s.a === 1 && s.b === 2 && s.d === 8) || (s.c === 1 && s.d === 2 && s.b === 8)); } },
  { text: 'Compare 3/8 and 3/4. Which is greater?', test: function (s) { return s.cmp && s.a === 3 && s.c === 3 && ((s.b === 8 && s.d === 4) || (s.b === 4 && s.d === 8)); } },
  { text: 'Show 6/3. What whole number is it?', test: function (s) { return s.a === 6 && s.b === 3; } },
  { text: 'Compare two fractions with the same denominator.', test: function (s) { return s.cmp && s.b === s.d && s.a !== s.c; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
function step(k, d) { var den = k === 'a' ? st.b : st.d; st[k] = K.clamp(st[k] + d, 0, 2 * den); draw(); }
T.steppers($('fxCtl'), step); T.steppers($('fxCtlB'), step);
document.addEventListener('click', function (e) { var b = e.target.closest('[data-den]'); if (!b) return; var k = b.dataset.den, v = +b.dataset.v; st[k] = v; if (k === 'b') st.a = Math.min(st.a, 2 * v); else st.c = Math.min(st.c, 2 * v); draw(); });
$('fxCmp').onclick = function () { st.cmp = !st.cmp; this.setAttribute('aria-pressed', st.cmp); $('fxCtlB').hidden = !st.cmp; draw(); };
reset();
""",
     [("Show 2/3. How many equal parts are in one whole? How many are colored?", "3 equal parts; 2 are colored"),
      ("Where is 1/4 on the number line from 0 to 1?", "At the first mark after 0 when the space from 0 to 1 is cut into 4 equal parts"),
      ("Find a fraction equal to 2/4.", "1/2 (or 4/8, or 3/6)"),
      ("Compare 2/6 and 5/6. Write >, = or <.", "2/6 < 5/6"),
      ("Compare 1/3 and 1/6. Write >, = or <.", "1/3 > 1/6, because thirds are bigger parts than sixths"),
      ("What whole number is 8/8? What whole number is 6/3?", "8/8 = 1 and 6/3 = 2"),
      ("Reflect: Why is 1/8 smaller than 1/4 even though 8 is bigger than 4?", "The whole is cut into more parts, so each part is smaller.")],
     ["The denominator tells how many equal parts make one whole; the numerator tells how many parts you have.",
      "Each fraction is made of unit fractions: 3/4 is three 1/4 parts.",
      "Equivalent fractions are at the same point on the number line.",
      "With the same denominator, more parts is greater. With the same numerator, bigger parts (smaller denominator) is greater."],
     ["Keep both bars and number lines visible so students connect the area model with the length model.",
      "Use Compare to find all fractions equal to 1/2 with denominators 2, 4, 6 and 8.",
      "Fractions up to 2 let students see whole numbers as fractions (3.NF.A.3c): 4/4 = 1, 6/3 = 2."])

# ------------------------------------------------------------------ Elapsed Time
tool(G, "clock-elapsed-time", ["time-volume-mass"], "Clocks and Elapsed Time",
     "Set a start clock and an end clock to the nearest minute. A number-line timeline shows the jump to the next hour, whole hours and minutes, and the total elapsed time.",
     "Choose the Start or End clock, then move it with + and −. Read the elapsed time on the timeline.",
     ["Time to the nearest minute", "Elapsed time"], "3.MD.A.1",
     """<div class="tl-controls el-view" role="group" aria-label="Which clock"><button type="button" class="tl-btn" data-c="s">Set the start clock</button><button type="button" class="tl-btn" data-c="e">Set the end clock</button></div>
<div class="el-clock-row" style="grid-template-columns:1fr 1fr"><div><h2 style="text-align:center">Start</h2><div class="tl-model el-clock" id="etS"></div><div class="el-digital" id="etSd"></div></div><div><h2 style="text-align:center">End</h2><div class="tl-model el-clock" id="etE"></div><div class="el-digital" id="etEd"></div></div></div>
<div class="tl-controls" id="etCtl" style="margin-top:.6rem"></div><div class="tl-model" id="etLine"></div><div class="tl-out" id="etOut" aria-live="polite"></div>""",
     r"""
var st;
function reset() { st = { s: 60, e: 90, cur: 's' }; draw(); }
function hm(t) { var h = Math.floor(t / 60) % 12 || 12; return [h, t % 60]; }
function show(t) { var x = hm(t); return x[0] + ':' + K.pad(x[1]); }
function dur(m) { var h = Math.floor(m / 60), mm = m % 60; return (h ? h + ' hour' + (h > 1 ? 's' : '') : '') + (h && mm ? ' ' : '') + (mm || !h ? mm + ' minute' + (mm === 1 ? '' : 's') : ''); }
function draw() {
  Array.prototype.forEach.call(document.querySelectorAll('[data-c]'), function (b) { b.setAttribute('aria-pressed', b.dataset.c === st.cur); });
  var S = hm(st.s), E = hm(st.e);
  $('etS').innerHTML = K.clockSvg(S[0], S[1], { face: st.cur === 's' ? '#fffbe9' : '#fff' }); $('etE').innerHTML = K.clockSvg(E[0], E[1], { face: st.cur === 'e' ? '#fffbe9' : '#fff' });
  $('etSd').textContent = show(st.s); $('etEd').textContent = show(st.e);
  $('etCtl').innerHTML = '<div class="tl-field"><span class="lab">Move the ' + (st.cur === 's' ? 'start' : 'end') + ' clock</span><div class="tl-step tl-step-wide">' + [[-60, '−1 hr'], [-5, '−5 min'], [-1, '−1 min'], [1, '+1 min'], [5, '+5 min'], [60, '+1 hr']].map(function (b) { return '<button type="button" data-k="t" data-s="' + b[0] + '" aria-label="' + b[1].replace('−', 'minus ').replace('+', 'plus ') + '">' + b[1] + '</button>'; }).join('') + '</div></div>';
  var el = ((st.e - st.s) % 720 + 720) % 720, s = '', X0 = 40, X1 = 760, sc = function (m) { return X0 + (el ? m / el : 0) * (X1 - X0); }, Y = 90;
  s += '<line x1="' + X0 + '" y1="' + Y + '" x2="' + X1 + '" y2="' + Y + '" stroke="#1d2a3a" stroke-width="3"/>';
  var stops = [0], first = (60 - st.s % 60) % 60;
  if (first && first < el) stops.push(first);
  for (var t = first + 60; t < el; t += 60) stops.push(t);
  if (el) stops.push(el);
  stops.forEach(function (m, i) {
    s += '<line x1="' + sc(m) + '" y1="' + (Y - 10) + '" x2="' + sc(m) + '" y2="' + (Y + 10) + '" stroke="#1d2a3a" stroke-width="2.5"/>' + K.txt(sc(m), Y + 32, show(st.s + m), { size: 15 });
    if (i) { var a = sc(stops[i - 1]), b = sc(m), d = m - stops[i - 1]; s += '<path d="M' + a + ' ' + Y + ' Q' + (a + b) / 2 + ' ' + (Y - 70) + ' ' + b + ' ' + Y + '" fill="none" stroke="' + (d === 60 ? '#1f78c8' : '#1fa565') + '" stroke-width="3.5"/>' + K.txt((a + b) / 2, Y - 42, d === 60 ? '1 hr' : d + ' min', { size: 14, fill: d === 60 ? '#1f78c8' : '#0d6b3c' }); }
  });
  $('etLine').innerHTML = K.svg(800, 130, s, 'Timeline from ' + show(st.s) + ' to ' + show(st.e));
  var parts = [], prev = 0; stops.slice(1).forEach(function (m) { parts.push(m - prev === 60 ? '1 hr' : (m - prev) + ' min'); prev = m; });
  $('etOut').innerHTML = el ? '<b>Elapsed time:</b> from ' + show(st.s) + ' to ' + show(st.e) + ' is <b>' + dur(el) + '</b> (' + el + ' minutes).<br>Jumps: ' + parts.join(' + ') + '.' + (st.e % 720 < st.s % 720 ? ' (This trip goes past 12 o’clock.)' : '') : 'The start and end times are the same. Move the end clock.';
  T.update({ s: show(st.s), e: show(st.e), el: el });
}
var CH = [
  { text: 'Set the start clock to 4:37.', test: function (s) { return s.s === '4:37'; } },
  { text: 'Set the end clock to 9:52.', test: function (s) { return s.e === '9:52'; } },
  { text: 'Make the elapsed time 45 minutes.', test: function (s) { return s.el === 45; } },
  { text: 'Start at 2:15 and end at 3:40. How long is that?', test: function (s) { return s.s === '2:15' && s.e === '3:40'; } },
  { text: 'Make the elapsed time exactly 2 hours.', test: function (s) { return s.el === 120; } },
  { text: 'A show starts at 10:50 and lasts 25 minutes. Set the end clock.', test: function (s) { return s.s === '10:50' && s.e === '11:15'; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
T.steppers($('etCtl'), function (k, d) { st[st.cur] = ((st[st.cur] + d) % 720 + 720) % 720; draw(); });
document.addEventListener('click', function (e) { var b = e.target.closest('[data-c]'); if (b) { st.cur = b.dataset.c; draw(); } });
reset();
""",
     [("A clock shows the hour hand just past 7 and the minute hand 3 marks past the 4. What time is it?", "7:23"),
      ("How much time passes from 3:10 to 3:55?", "45 minutes"),
      ("How much time passes from 8:40 to 9:15?", "35 minutes (20 minutes to 9:00, then 15 more)"),
      ("Recess starts at 1:25 and lasts 50 minutes. When does it end?", "2:15"),
      ("How long is it from 11:30 to 1:05?", "1 hour 35 minutes"),
      ("A movie ended at 4:00. It lasted 1 hour 20 minutes. When did it start?", "2:40"),
      ("Reflect: Why is it helpful to jump to the next hour first?", "Whole hours are easy to count; the leftover minutes are added at the start and end.")],
     ["Count by fives on the clock, then by ones for the extra minutes.",
      "To find elapsed time, jump to the next hour first, then count whole hours, then the extra minutes.",
      "60 minutes make 1 hour.",
      "You can work backward from an end time to find a start time."],
     ["Have students sketch the timeline in their notebooks while the tool shows it.",
      "Use school events (lunch 11:45 to 12:20) for real elapsed-time problems.",
      "For start-time problems, set the end clock first and move the start clock back."])

# ------------------------------------------------------------------ Scaled Graphs
tool(G, "graph-builder", ["graphs-measurement-data"], "Scaled Graph Builder",
     "Show pet votes on a scaled picture graph (each face can stand for 2, 5 or 10) and on a bar graph that counts by 2s, 5s or 10s. Answer how many more and how many fewer.",
     "Change the votes with + and −. Pick a picture key and a bar scale, and switch between the graphs and the table.",
     ["Scaled picture graphs", "Scaled bar graphs", "How many more and fewer"], "3.MD.B.3",
     """<div id="grTool"></div>""",
     r"""
var CH = [
  { text: 'With a key of 2, give Dogs 8 votes. How many faces?', test: function (s) { return s.view === 'pic' && s.key === 2 && s.c[0] === 8; } },
  { text: 'Give Cats 15 votes. Choose a key that shows 15 with only whole faces.', test: function (s) { return s.view === 'pic' && s.c[1] === 15 && s.key === 5; } },
  { text: 'Make a bar graph that counts by 10s with Fish at 40.', test: function (s) { return s.view === 'bar' && s.scale === 10 && s.c[2] === 40; } },
  { text: 'Make Dogs 15 more than Birds.', test: function (s) { return s.c[0] === s.c[3] + 15; } },
  { text: 'Make 50 votes in all.', test: function (s) { return s.total === 50; } },
  { text: 'Show half of a face with a key of 2.', test: function (s) { return s.view === 'pic' && s.key === 2 && s.c.some(function (v) { return v % 2; }); } }];
K.graphTool(Object.assign({}, META, { toolTitle: META.title, title: 'Our Favorite Pet', cats: ['Dogs', 'Cats', 'Fish', 'Birds'], counts: [12, 8, 20, 6], max: 60, steps: [1, 5], views: ['pic', 'bar', 'table'], keys: [1, 2, 5, 10], key0: 2, scales: [1, 2, 5, 10], scale0: 2, challenges: CH }));
""",
     [("With a key of 2, how many faces show Fish (20 votes)?", "10 faces"),
      ("With a key of 5, how many faces show Fish?", "4 faces"),
      ("Dogs have 12 votes. Can a key of 5 show 12 with whole faces? Explain.", "No. 12 is 2 faces (10) and part of a face for 2 more."),
      ("How many votes are there in all? (Dogs 12, Cats 8, Fish 20, Birds 6)", "46"),
      ("How many more votes does Fish have than Birds?", "14 more"),
      ("On a bar graph that counts by 5s, between which two numbers does the Dogs bar end?", "Between 10 and 15 (at 12)"),
      ("Reflect: When is a bigger key or scale helpful?", "When the numbers are big, so the graph is not too long and is quicker to read.")],
     ["In a scaled picture graph, each picture stands for more than one vote: read the key first.",
      "Part of a picture stands for part of the key: half a face with a key of 2 is 1 vote.",
      "A bar graph scale counts by the same amount each step (2s, 5s or 10s).",
      "To find how many more, subtract the smaller count from the bigger one."],
     ["Ask students to choose the best key for a set of data and explain why (no partial faces, not too many pictures).",
      "Pose two-step questions: How many more Fish than Cats and Birds together?",
      "Students can step votes by 5 to build larger data sets quickly."])

# ------------------------------------------------------------------ Area and Perimeter Grid
tool(G, "area-perimeter-grid", ["area", "perimeter-shapes"], "Area and Perimeter Grid",
     "Build rectangles on a grid or paint your own shapes from unit squares. Area and perimeter update as you go, so you can find shapes with the same area and different perimeters.",
     "Choose Rectangle to set the sides, or Paint to tap squares and build any shape.",
     ["Area", "Perimeter", "Same area, different perimeter"], "3.MD.C.5, 3.MD.C.6, 3.MD.C.7, 3.MD.D.8",
     """<div class="tl-controls el-view" role="group" aria-label="Mode"><button type="button" class="tl-btn" data-mode="rect">Rectangle</button><button type="button" class="tl-btn" data-mode="paint">Paint squares</button><button type="button" class="tl-btn" id="apClear">Clear painting</button></div>
<div class="tl-model" id="apModel"></div><div class="tl-controls" id="apCtl"></div><div class="tl-out" id="apOut" aria-live="polite"></div>""",
     r"""
var C = 12, R = 8, U = 52, st;
function reset() { st = { mode: 'rect', w: 3, h: 2, cells: {}, cur: [0, 0], rects: {} }; draw(); }
function paintStats() {
  var n = 0, p = 0, minr = 99, maxr = -1, minc = 99, maxc = -1;
  Object.keys(st.cells).forEach(function (k) { var a = k.split(',').map(Number); n++; [[0, 1], [0, -1], [1, 0], [-1, 0]].forEach(function (d) { if (!st.cells[(a[0] + d[0]) + ',' + (a[1] + d[1])]) p++; }); minr = Math.min(minr, a[0]); maxr = Math.max(maxr, a[0]); minc = Math.min(minc, a[1]); maxc = Math.max(maxc, a[1]); });
  return { n: n, p: p, rect: n > 0 && (maxr - minr + 1) * (maxc - minc + 1) === n };
}
function draw() {
  Array.prototype.forEach.call(document.querySelectorAll('[data-mode]'), function (b) { b.setAttribute('aria-pressed', b.dataset.mode === st.mode); });
  $('apClear').hidden = st.mode !== 'paint';
  var s = '', i, j, X = 30, Y = 30;
  for (i = 0; i < R; i++) for (j = 0; j < C; j++) {
    var on = st.mode === 'rect' ? (i < st.h && j < st.w) : st.cells[i + ',' + j];
    s += '<rect class="el-cell" data-r="' + i + '" data-c="' + j + '" x="' + (X + j * U) + '" y="' + (Y + i * U) + '" width="' + U + '" height="' + U + '" fill="' + (on ? '#bfe6d0' : '#fff') + '" stroke="' + (on ? '#0d6b3c' : '#cfd8e3') + '" stroke-width="' + (on ? 2 : 1.2) + '"/>';
  }
  if (st.mode === 'rect') {
    s += '<rect x="' + X + '" y="' + Y + '" width="' + st.w * U + '" height="' + st.h * U + '" fill="none" stroke="#d63c7a" stroke-width="5"/>';
    s += K.txt(X + st.w * U / 2, Y - 8, st.w + ' units', { size: 18, fill: '#d63c7a' }) + K.txt(X + st.w * U + 8, Y + st.h * U / 2 + 6, st.h + ' units', { a: 'start', size: 18, fill: '#d63c7a' });
  } else s += '<rect x="' + (X + st.cur[1] * U + 3) + '" y="' + (Y + st.cur[0] * U + 3) + '" width="' + (U - 6) + '" height="' + (U - 6) + '" fill="none" stroke="#ffb000" stroke-width="4" stroke-dasharray="6 4"/>';
  $('apModel').innerHTML = K.svg(C * U + 130, R * U + 50, s, st.mode === 'rect' ? 'A ' + st.w + ' by ' + st.h + ' rectangle' : 'Painted shape');
  var out, A, P, isRect;
  if (st.mode === 'rect') {
    A = st.w * st.h; P = 2 * (st.w + st.h); isRect = true;
    $('apCtl').innerHTML = K.step('w', 'Length (across)', [1], st.w) + K.step('h', 'Width (down)', [1], st.h);
    out = '<b>Area:</b> ' + st.h + ' rows of ' + st.w + ' = ' + st.h + ' × ' + st.w + ' = <b>' + A + ' square units</b><br><b>Perimeter:</b> ' + st.w + ' + ' + st.h + ' + ' + st.w + ' + ' + st.h + ' = <b>' + P + ' units</b>';
    var key = Math.min(st.w, st.h) + 'x' + Math.max(st.w, st.h); st.rects[key] = { A: A, P: P };
    var same = Object.keys(st.rects).filter(function (k) { return k !== key && st.rects[k].A === A; });
    if (same.length) out += '<br>Same area as ' + same.map(function (k) { return k.replace('x', ' by ') + ' (perimeter ' + st.rects[k].P + ')'; }).join(', ') + '.';
  } else {
    var ps = paintStats(); A = ps.n; P = ps.p; isRect = ps.rect;
    $('apCtl').innerHTML = '<p class="tl-sub" style="margin:0">Tap squares to paint or erase them. Keyboard: arrow keys move the yellow box, Space paints.</p>';
    out = A ? '<b>Area:</b> <b>' + A + ' square units</b> (count the squares)<br><b>Perimeter:</b> <b>' + P + ' units</b> (count the outside edges)' + (isRect ? '<br>Your shape is a rectangle.' : '<br>Tip: break the shape into rectangles and add their areas.') : 'Tap squares to build a shape.';
  }
  $('apOut').innerHTML = out;
  T.update({ mode: st.mode, w: st.w, h: st.h, A: A, P: P, isRect: isRect, rects: JSON.parse(JSON.stringify(st.rects)) });
}
function vals(s, f) { return Object.keys(s.rects).map(function (k) { return s.rects[k]; }).filter(f); }
var CH = [
  { text: 'Make a rectangle with an area of 12 square units.', test: function (s) { return s.mode === 'rect' && s.A === 12; } },
  { text: 'Make two rectangles with area 12 but different perimeters.', test: function (s) { var p = {}; vals(s, function (r) { return r.A === 12; }).forEach(function (r) { p[r.P] = 1; }); return Object.keys(p).length >= 2; } },
  { text: 'Make a rectangle with a perimeter of 20 units.', test: function (s) { return s.mode === 'rect' && s.P === 20; } },
  { text: 'Make two rectangles with perimeter 16 but different areas.', test: function (s) { var a = {}; vals(s, function (r) { return r.P === 16; }).forEach(function (r) { a[r.A] = 1; }); return Object.keys(a).length >= 2; } },
  { text: 'Paint a shape that is not a rectangle with an area of 10 square units.', test: function (s) { return s.mode === 'paint' && s.A === 10 && !s.isRect; } },
  { text: 'Make a square with an area of 25 square units.', test: function (s) { return s.mode === 'rect' && s.w === 5 && s.h === 5; } }];
T.init(Object.assign({}, META, { challenges: CH, reset: reset, printables: true }));
T.steppers($('apCtl'), function (k, d) { st[k] = K.clamp(st[k] + d, 1, k === 'w' ? C : R); draw(); });
function toggle(r, c) { var k = r + ',' + c; if (st.cells[k]) delete st.cells[k]; else st.cells[k] = 1; st.cur = [r, c]; draw(); }
$('apModel').addEventListener('click', function (e) { var t = e.target.closest('.el-cell'); if (t && st.mode === 'paint') toggle(+t.dataset.r, +t.dataset.c); });
document.addEventListener('click', function (e) { var b = e.target.closest('[data-mode]'); if (b) { st.mode = b.dataset.mode; draw(); } });
$('apClear').onclick = function () { st.cells = {}; draw(); };
window.addEventListener('keydown', function (e) {
  if (st.mode !== 'paint' || (e.target.closest && e.target.closest('button,input,select'))) return;
  var m = { ArrowRight: [0, 1], ArrowLeft: [0, -1], ArrowDown: [1, 0], ArrowUp: [-1, 0] }[e.key];
  if (m) { e.preventDefault(); st.cur = [K.clamp(st.cur[0] + m[0], 0, R - 1), K.clamp(st.cur[1] + m[1], 0, C - 1)]; draw(); }
  if (e.key === ' ') { e.preventDefault(); toggle(st.cur[0], st.cur[1]); }
});
reset();
""",
     [("What are the area and perimeter of a rectangle 6 units long and 4 units wide?", "Area 24 square units; perimeter 20 units"),
      ("Find two rectangles with an area of 18 square units.", "For example 3 by 6 and 2 by 9 (also 1 by 18 on a big enough grid)"),
      ("What is the perimeter of a 5 by 5 square?", "20 units"),
      ("Rectangles with perimeter 12 can be 1 by 5, 2 by 4 or 3 by 3. What is the area of each?", "5, 8 and 9 square units"),
      ("A rectangle has a perimeter of 14 units and a width of 3 units. How long is it?", "4 units (3 + 4 + 3 + 4 = 14)"),
      ("Paint an L-shape made of a 4 by 2 rectangle and a 2 by 1 rectangle. What is its area?", "10 square units (8 + 2)"),
      ("Reflect: How are area and perimeter different?", "Area counts the unit squares inside; perimeter measures the distance around the outside.")],
     ["Area is the number of unit squares that cover a shape; for a rectangle it is rows × columns.",
      "Perimeter is the distance around: add all the side lengths.",
      "Rectangles can have the same area and different perimeters, or the same perimeter and different areas.",
      "To find the area of an L-shape, break it into rectangles and add."],
     ["Ask students to list every rectangle with area 12 and compare their perimeters (a long thin one has the biggest).",
      "Paint mode lets students build rectilinear figures for 3.MD.C.7d and check their own decomposition.",
      "Unknown side problems: give the perimeter and one side, then build it to check."])
