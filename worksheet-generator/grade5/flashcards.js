/* Grade 5 interactive flashcards: vocabulary, concept and visual cards for one unit (grade5/flashcards/<unit>.json).
   Flip (click, Space or Enter), next/previous (arrow keys), shuffle, filter by card type, "Got it / Practice again" sorting.
   Nothing is saved. */
(function (G) {
  'use strict';
  var g5 = G.G5, el = g5.el, D = G.document, P = g5.P;
  var KINDS = [['all', 'All cards'], ['vocabulary', 'Words'], ['concept', 'Big ideas'], ['visual', 'Pictures'], ['strategy', 'Mental math'], ['watch', 'Watch out!']];
  var GROUP = { vocabulary: 'vocabulary', visual: 'visual', mental: 'strategy', misconception: 'watch' };
  function grp(k) { return GROUP[k] || 'concept'; }
  var st = { data: null, deck: [], i: 0, flipped: false, known: {}, filter: 'all' };
  var main, cardBox, counter, bar;

  var css = D.createElement('style');
  css.textContent = '.fc-stage{perspective:1400px;margin:1rem auto;max-width:44rem}' +
    '.fc-card{position:relative;width:100%;min-height:20rem;transform-style:preserve-3d;transition:transform .5s;cursor:pointer;border:0;padding:0;background:none;font:inherit;color:inherit;display:block}' +
    '.fc-card.flip{transform:rotateY(180deg)}' +
    '.fc-face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;border-radius:1.4rem;padding:1.4rem;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;box-shadow:0 8px 26px rgba(30,60,120,.16);border:3px solid #cfe0fb;background:#fff}' +
    '.fc-back{transform:rotateY(180deg);background:#fffdf3;border-color:#ffd34d}' +
    '.fc-kind{position:absolute;top:.8rem;left:1rem;font-size:.75rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;color:#55657a}' +
    '.fc-front-text{font-size:1.9rem;font-weight:900;color:#22408a}.fc-front-text.long{font-size:1.35rem}' +
    '.fc-back-text{font-size:1.25rem;font-weight:700}.fc-ex{margin-top:.8rem;color:#55657a;font-size:1.05rem}' +
    '.fc-svg{max-width:100%;max-height:13rem;margin:.6rem auto 0}.fc-svg svg{max-width:100%;height:auto;max-height:13rem}' +
    '.fc-tap{position:absolute;bottom:.7rem;font-size:.75rem;color:#7a8799}' +
    '.fc-nav{display:flex;justify-content:center;gap:.6rem;flex-wrap:wrap;margin:.6rem 0}' +
    '.fc-progress{height:.7rem;background:#e6efff;border-radius:999px;overflow:hidden;margin:.4rem 0}.fc-progress div{height:100%;background:linear-gradient(90deg,#2f7fd8,#1aa37a);transition:width .3s}' +
    '@media (prefers-reduced-motion:reduce){.fc-card{transition:none}}' +
    '@media print{.fc-stage,.fc-nav,.fc-progress,.g5-pills{display:none!important}.fc-print{display:block!important}}' +
    '.fc-print{display:none}.fc-print table{width:100%;border-collapse:collapse}.fc-print td{border:1px solid #999;padding:.4rem;vertical-align:top;width:50%}';
  D.head.appendChild(css);

  function buildDeck() {
    st.deck = st.data.cards.filter(function (c) { return st.filter === 'all' || grp(c.kind) === st.filter; });
    st.i = 0; st.flipped = false; show();
  }

  function show() {
    cardBox.innerHTML = '';
    var c = st.deck[st.i];
    if (!c) { el('p', cardBox, 'g5-panel', 'No cards of this type in this unit.'); counter.textContent = ''; return; }
    var btn = el('button', cardBox, 'fc-card' + (st.flipped ? ' flip' : ''));
    btn.setAttribute('aria-label', (st.flipped ? 'Back of card. ' : 'Front of card. ') + 'Press to flip.');
    var f = el('div', btn, 'fc-face fc-front');
    el('span', f, 'fc-kind', label(c.kind));
    g5.math(el('div', f, 'fc-front-text' + (c.front.length > 40 ? ' long' : '')), c.front);
    if (c.svg) { var sv = el('div', f, 'fc-svg'); sv.innerHTML = c.svg; var s = sv.querySelector('svg'); if (s) { s.setAttribute('role', 'img'); s.setAttribute('aria-label', 'Picture for: ' + c.front); } }
    el('span', f, 'fc-tap', 'Tap or press Space to flip');
    var b = el('div', btn, 'fc-face fc-back');
    el('span', b, 'fc-kind', label(c.kind));
    g5.math(el('div', b, 'fc-back-text'), c.back);
    if (c.example) g5.math(el('div', b, 'fc-ex'), 'Example: ' + c.example);
    if (st.known[key(c)]) el('span', b, 'fc-tap', '✓ You marked this one “Got it”');
    btn.setAttribute('aria-live', 'polite');
    btn.onclick = flip;
    counter.textContent = 'Card ' + (st.i + 1) + ' of ' + st.deck.length;
    var k = st.deck.filter(function (x) { return st.known[key(x)]; }).length;
    bar.firstChild.style.width = (100 * k / st.deck.length) + '%';
    bar.setAttribute('aria-valuenow', k); bar.setAttribute('aria-valuemax', st.deck.length);
    bar.title = k + ' of ' + st.deck.length + ' marked “Got it”';
  }
  function label(k) { return { vocabulary: 'Vocabulary', visual: 'Picture', mental: 'Mental math', misconception: 'Watch out!', symbol: 'Math symbol', rule: 'Rule' }[k] || 'Big idea'; }
  function key(c) { return c.front + '|' + c.back; }
  function flip() { st.flipped = !st.flipped; var b = cardBox.querySelector('.fc-card'); if (b) { b.classList.toggle('flip', st.flipped); b.setAttribute('aria-label', (st.flipped ? 'Back of card. ' : 'Front of card. ') + 'Press to flip.'); } }
  function go(d) { if (!st.deck.length) return; st.i = (st.i + d + st.deck.length) % st.deck.length; st.flipped = false; show(); }
  function mark(ok) {
    var c = st.deck[st.i]; if (!c) return;
    if (ok) st.known[key(c)] = 1; else delete st.known[key(c)];
    var left = st.deck.filter(function (x) { return !st.known[key(x)]; });
    if (!left.length) { celebrate(); return; }
    go(1);
  }
  function celebrate() {
    cardBox.innerHTML = '';
    var p = el('div', cardBox, 'g5-panel g5-celebrate');
    el('div', p, 'big', '🌟'); el('h2', p, null, 'You know every card in this set!');
    var again = el('button', p, 'g5-btn primary', 'Go through them again'); again.onclick = function () { st.known = {}; st.deck = g5.shuffle(st.deck); st.i = 0; st.flipped = false; show(); };
    counter.textContent = 'All ' + st.deck.length + ' cards marked “Got it”'; bar.firstChild.style.width = '100%';
  }

  function printable() {
    var pr = el('div', main, 'fc-print');
    el('h2', pr, null, st.data.unitName + ' · Flashcards');
    var t = el('table', pr);
    st.data.cards.forEach(function (c) {
      var r = el('tr', t); var a = el('td', r); g5.math(el('strong', a), c.front); if (c.svg) { var s = el('div', a, 'fc-svg'); s.innerHTML = c.svg; }
      var b = el('td', r); g5.math(el('div', b), c.back); if (c.example) g5.math(el('div', b, 'fc-ex'), 'Example: ' + c.example);
    });
  }

  function boot() {
    main = D.getElementById('app');
    var unitId = P.get('unit');
    if (!unitId || !/^[a-z0-9-]+$/.test(unitId)) { g5.errorBox(main, 'Choose a Grade 5 unit from Mr. K’s Classroom.'); return; }
    fetch('grade5/flashcards/' + unitId + '.json').then(function (r) { if (!r.ok) throw new Error('These flashcards could not be found.'); return r.json(); }).then(function (data) {
      st.data = data;
      D.title = 'Flashcards · ' + data.unitName + ' · Grade 5';
      g5.chrome('🃏 Flashcards', 'Grade 5 · Unit ' + data.number + ': ' + data.unitName);
      var top = el('section', main, 'g5-panel');
      var fs = el('fieldset', top, 'g5-pills'); el('legend', fs, null, 'Which cards?');
      KINDS.forEach(function (k) {
        var n = data.cards.filter(function (c) { return k[0] === 'all' || grp(c.kind) === k[0]; }).length;
        if (!n) return;
        var lab = el('label', fs, 'g5-pill'); var r = el('input', lab); r.type = 'radio'; r.name = 'fckind'; r.value = k[0]; r.checked = k[0] === 'all';
        el('span', lab, null, k[1] + ' (' + n + ')');
        r.onchange = function () { st.filter = k[0]; buildDeck(); };
      });
      counter = el('div', top, 'g5-chip'); counter.setAttribute('aria-live', 'polite');
      bar = el('div', top, 'fc-progress'); el('div', bar).style.width = '0%'; bar.setAttribute('role', 'progressbar'); bar.setAttribute('aria-label', 'Cards marked Got it'); bar.setAttribute('aria-valuemin', 0);
      var stage = el('div', main, 'fc-stage'); cardBox = el('div', stage);
      var nav = el('div', main, 'fc-nav');
      [['← Back', function () { go(-1); }, ''], ['Flip', flip, 'primary'], ['Next →', function () { go(1); }, '']].forEach(function (x) { var b = el('button', nav, 'g5-btn ' + x[2], x[0]); b.onclick = x[1]; });
      var nav2 = el('div', main, 'fc-nav');
      var ok = el('button', nav2, 'g5-btn', '✓ Got it'); ok.style.borderColor = '#16865c'; ok.style.color = '#16865c'; ok.onclick = function () { mark(true); };
      var again = el('button', nav2, 'g5-btn', '↻ Practice again'); again.style.borderColor = '#b4590b'; again.style.color = '#b4590b'; again.onclick = function () { mark(false); };
      var sh = el('button', nav2, 'g5-btn ghost', '🔀 Shuffle'); sh.onclick = function () { st.deck = g5.shuffle(st.deck); st.i = 0; st.flipped = false; show(); };
      var pb = el('button', nav2, 'g5-btn ghost', '🖨 Print cards'); pb.onclick = function () { G.print(); };
      el('p', main, 'g5-hint-text', 'Keyboard: Space or Enter flips · ← → move · G = got it · P = practice again · S = shuffle.').style.textAlign = 'center';
      printable();
      buildDeck();
      D.addEventListener('keydown', function (e) {
        if (e.target && /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) return;
        if (e.key === 'ArrowRight') { go(1); e.preventDefault(); }
        else if (e.key === 'ArrowLeft') { go(-1); e.preventDefault(); }
        else if ((e.key === ' ' || e.key === 'Enter') && !(e.target && e.target.tagName === 'BUTTON' && !e.target.classList.contains('fc-card'))) { flip(); e.preventDefault(); }
        else if (e.key === 'g' || e.key === 'G') mark(true);
        else if (e.key === 'p' || e.key === 'P') mark(false);
        else if (e.key === 's' || e.key === 'S') { st.deck = g5.shuffle(st.deck); st.i = 0; st.flipped = false; show(); }
      });
    }).catch(function (e) { g5.chrome('🃏 Flashcards', 'Grade 5'); g5.errorBox(main, e.message); });
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
})(window);
