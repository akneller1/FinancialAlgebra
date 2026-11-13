/* Development-only compatibility candidate. Never registers or approves a bank.
 * Staging integrator can adopt this visual-card matching behavior in the shared engine.
 * Duplicate answer values are matched by mathematical text value, never hidden pair ID.
 */
(function (global) {
  'use strict';
  function key(value) { return String(value).trim().toLowerCase().replace(/−/g, '-').replace(/\s+/g, ' ').replace(/\.$/, ''); }
  function prepare(questions, skillId, level) {
    var seen = new Set();
    var eligible = questions.filter(function (q) {
      if (q.skillId !== skillId || q.level !== level || q.format !== 'short-answer' || !q.answer) return false;
      var identity = q.prompt + '|' + (q.diagram && q.diagram.spec.src || '');
      if (seen.has(identity)) return false;
      seen.add(identity); return true;
    });
    // Prefer different answer values, then fill from the SAME selected scope.
    var values = new Set(), selected = [], rest = [];
    eligible.forEach(function (q) { var k = key(q.answer); if (values.has(k)) rest.push(q); else { values.add(k); selected.push(q); } });
    selected = selected.concat(rest).slice(0, 6);
    if (selected.length < 4) throw new Error('Need at least four short-answer questions in the selected skill and level.');
    var cards = [];
    selected.forEach(function (q) {
      cards.push({ id: q.id + ':q', kind: 'question', value: key(q.answer), text: q.prompt, image: q.diagram && q.diagram.spec, questionId: q.id });
      cards.push({ id: q.id + ':a', kind: 'answer', value: key(q.answer), text: String(q.answer), questionId: q.id });
    });
    for (var i = cards.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var temp = cards[i]; cards[i] = cards[j]; cards[j] = temp; }
    return { cards: cards, pairs: selected.length, distinctAnswers: new Set(selected.map(function (q) { return key(q.answer); })).size, skillId: skillId, level: level };
  }
  function mount(root, questions, skillId, level, assetBase) {
    var model = prepare(questions, skillId, level), open = [], matched = new Set(), flips = 0;
    root.replaceChildren();
    var status = document.createElement('p'); status.setAttribute('role', 'status');root.appendChild(status);
    var grid = document.createElement('div'); grid.className = 'g1-puzzle-grid'; root.appendChild(grid);
    var buttons = new Map();
    function update() {
      status.textContent = matched.size / 2 === model.pairs ? 'Puzzle solved!' : 'Pairs found: ' + matched.size / 2 + ' / ' + model.pairs + ' · Flips: ' + flips;
      model.cards.forEach(function (c) {
        var button = buttons.get(c.id), visible = open.includes(c.id) || matched.has(c.id);
        button.replaceChildren();button.disabled = matched.has(c.id);
        button.setAttribute('aria-label', visible ? c.kind + ': ' + c.text : 'Hidden ' + c.kind + ' card');
        if (visible) {
          var text = document.createElement('span');text.textContent = c.text;button.appendChild(text);
          if (c.image) { var img = document.createElement('img'); img.src = (assetBase || '') + c.image.src; img.alt = c.image.alt; button.appendChild(img); }
        } else button.textContent = c.kind === 'question' ? 'Problem' : 'Answer';
        button.dataset.face = visible ? 'up' : 'down';
      });
    }
    function flip(id) {
      if (matched.has(id) || open.includes(id)) return;
      if (open.length === 2) open = [];
      open.push(id);flips++;
      if (open.length === 2) {
        var a = model.cards.find(function (c) { return c.id === open[0]; }), b = model.cards.find(function (c) { return c.id === open[1]; });
        if (a.kind !== b.kind && a.value === b.value) { matched.add(a.id);matched.add(b.id);open = []; }
      }
      update();
    }
    model.cards.forEach(function (c) { var b = document.createElement('button');b.type = 'button';b.dataset.cardId = c.id;b.onclick = function () { flip(c.id); };buttons.set(c.id, b);grid.appendChild(b); });
    update();
    return { model: model, flip: flip, state: function () { return { matchedPairs: matched.size / 2, flips: flips, solved: matched.size === model.cards.length }; } };
  }
  global.G1StagingPuzzle = { prepare: prepare, mount: mount, key: key };
})(typeof window === 'undefined' ? globalThis : window);
