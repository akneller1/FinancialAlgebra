/* Elementary game collection (configured per course by window.MK_ELEMENTARY.games, see grade4/config.js).
   Every move forward requires a correct answer to a verified bank question.
   Individual modes: retries, hints, no timers. Whole-class modes: teams, large text, clear turn indicators.
   Engines: adventure path, builder (scene pieces or picture reveal), team race, soccer, four in a row, card match,
   fraction models (generated) and arrays (generated). Themes, names and instructions come from the course config. */
(function (G) {
  'use strict';
  var K = G.MKEL, el = K.el, D = G.document, P = K.P;
  var TEAM_COLORS = ['#2f7fd8', '#f08c1a', '#1aa37a', '#d63c7a'];
  var TEAM_NAMES = ['Blue Team', 'Orange Team', 'Green Team', 'Pink Team'];
  var GAMES = K.CFG.games || {};

  var state = { deck: [], used: 0, stats: {}, info: null, level: 'cp1', mode: 'solo', teacher: P.get('student') !== '1' };
  var main, stage;

  function record(p, ok) {
    var s = state.stats[p.skillId] || (state.stats[p.skillId] = { right: 0, tries: 0 });
    s.tries++; if (ok) s.right++;
  }
  function next(choiceOnly) {
    for (var k = 0; k < state.deck.length; k++) {
      var p = state.deck[state.used++ % state.deck.length];
      var c = choiceOnly ? K.asChoice(p) : (p.kind === 'parts' ? null : p);
      if (c) return c;
    }
    return null;
  }
  function ask(host, opts) {
    var p = next(opts.choiceOnly);
    if (!p) { K.errorBox(host, 'No questions match these settings. Try another level or more skills.'); return; }
    K.card(host, p, { label: opts.label, teacher: state.teacher && /class|pairs/.test(state.mode), tries: opts.tries || (/class/.test(state.mode) ? 1 : 2),
      onAnswer: function (ok) { record(p, ok); opts.done(ok); }, onNext: opts.onNext, nextLabel: opts.nextLabel, showAnswer: true });
  }
  function summary(host, headline, emoji) {
    var box = el('section', host, 'el-panel el-celebrate');
    el('div', box, 'big', emoji || '🎉');
    el('h2', box, null, headline);
    var tot = 0, right = 0;
    Object.keys(state.stats).forEach(function (k) { tot += state.stats[k].tries; right += state.stats[k].right; });
    el('p', box, null, right + ' correct answers out of ' + tot + ' questions. Every question you worked on made your brain stronger!');
    if (state.teacher) {
      var det = el('details', box, 'el-summary'); el('summary', det, null, 'Teacher view: results by skill (not saved anywhere)');
      var t = el('table', det), h = el('tr', t); ['Skill', 'Correct', 'Tried'].forEach(function (x) { el('th', h, null, x); });
      state.info.skills.forEach(function (s) { var st = state.stats[s.id]; if (!st) return; var r = el('tr', t); el('td', r, null, s.name); el('td', r, null, st.right); el('td', r, null, st.tries); });
    }
    var again = el('button', box, 'el-btn primary big', 'Play again'); again.onclick = function () { G.location.reload(); };
  }

  /* ---------- engine: adventure path ---------- */
  var PATH_THEMES = {
    treasure: { bg: ['#fdf1d6', '#f6dca5'], line: '#b07a3a', token: '🧭', counter: '💎 Gems: ', done: 'You found the treasure!', emoji: '🏆', dark: false, extra: 'beach' },
    space: { bg: ['#1b2350', '#2b3570'], line: '#8fa6ff', token: '🚀', counter: '🧑‍🚀 Astronauts rescued: ', done: 'Rescue complete! Everyone is safe.', emoji: '🌟', dark: true, extra: 'stars' },
    island: { bg: ['#cdeffd', '#7fd0f0'], line: '#8a5a2b', token: '⛵', counter: '🧩 Puzzle pieces: ', done: 'You solved Puzzle Island!', emoji: '🏝️', dark: false, extra: 'islands' },
    quest: { bg: ['#dff3e3', '#bfe6c8'], line: '#b07a3a', token: '🧭', counter: '⭐ Stars: ', done: 'Quest complete!', emoji: '🏆', dark: false, extra: 'hills' }
  };
  function pathScene(cfg, pos, progress) {
    var T = PATH_THEMES[cfg.theme] || PATH_THEMES.quest;
    var n = cfg.stops.length, W = 900, H = 300;
    var pts = cfg.stops.map(function (_, i) { return [70 + i * (W - 140) / (n - 1), 150 + Math.sin(i * 1.3) * 70]; });
    var ink = T.dark ? '#fff' : '#1d2a3a';
    var s = '<svg class="el-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Progress map: ' + pos + ' of ' + (n - 1) + ' steps complete">';
    s += '<rect width="' + W + '" height="' + H + '" rx="22" fill="' + T.bg[0] + '"/>';
    if (T.extra === 'stars') for (var k = 0; k < 40; k++) s += '<circle cx="' + ((k * 97) % W) + '" cy="' + ((k * 53) % H) + '" r="' + (1 + k % 3) + '" fill="#fff" opacity=".7"/>';
    else if (T.extra === 'islands') { s += '<path d="M0 ' + (H - 30) + ' q 30 -14 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 V' + H + ' H0Z" fill="' + T.bg[1] + '"/>'; pts.forEach(function (p) { s += '<ellipse cx="' + p[0] + '" cy="' + (p[1] + 14) + '" rx="46" ry="20" fill="#f6dca5" stroke="#d9b56c" stroke-width="2"/>'; }); }
    else s += '<path d="M0 ' + (H - 50) + ' Q ' + W / 2 + ' ' + (H - 110) + ' ' + W + ' ' + (H - 40) + ' L ' + W + ' ' + H + ' L 0 ' + H + 'Z" fill="' + T.bg[1] + '"/>';
    s += '<polyline points="' + pts.map(function (p) { return p.join(','); }).join(' ') + '" fill="none" stroke="' + T.line + '" stroke-width="6" stroke-dasharray="14 10"/>';
    pts.forEach(function (p, i) {
      var done = i < pos, here = i === pos;
      var col = done ? '#1aa37a' : here ? '#ffb000' : (T.dark ? '#5a62d8' : '#ffffff');
      s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="' + (here ? 26 : 20) + '" fill="' + col + '" stroke="#1d2a3a" stroke-width="3"/>';
      s += '<text x="' + p[0] + '" y="' + (p[1] + 7) + '" text-anchor="middle" font-size="20" font-weight="900" fill="' + (done || here ? '#fff' : '#1d2a3a') + '">' + (done ? '✓' : i + 1) + '</text>';
      s += '<text x="' + p[0] + '" y="' + (p[1] + (i % 2 ? -36 : 50)) + '" text-anchor="middle" font-size="15" font-weight="800" fill="' + ink + '">' + K.esc(cfg.stops[i]) + '</text>';
    });
    var me = pts[Math.min(pos, n - 1)];
    s += '<text x="' + me[0] + '" y="' + (me[1] - 30) + '" text-anchor="middle" font-size="34">' + T.token + '</text>';
    if (cfg.per > 1 && pos < n - 1) s += '<text x="' + (W - 20) + '" y="34" text-anchor="end" font-size="18" font-weight="800" fill="' + ink + '">This stop: ' + progress + ' of ' + cfg.per + ' correct</text>';
    return s + '</svg>';
  }
  function playPath(cfg) {
    var T = PATH_THEMES[cfg.theme] || PATH_THEMES.quest;
    var pos = 0, progress = 0, gems = 0;
    var scene = el('div', stage, 'el-board'), hud = el('div', stage, 'el-hud'), qhost = el('div', stage);
    function draw() {
      scene.innerHTML = pathScene(cfg, pos, progress);
      hud.innerHTML = '';
      el('span', hud, 'el-chip', T.counter + gems);
      el('span', hud, 'el-chip', 'Level: ' + K.levelName(state.level));
    }
    function round() {
      draw();
      if (pos >= cfg.stops.length - 1) { qhost.innerHTML = ''; summary(qhost, T.done, T.emoji); return; }
      ask(qhost, { label: 'Next stop: ' + cfg.stops[pos + 1], choiceOnly: state.mode === 'class',
        done: function (ok) { if (ok) { gems++; progress++; if (progress >= cfg.per) { pos++; progress = 0; } } draw(); },
        onNext: round, nextLabel: 'Keep going →' });
    }
    round();
  }

  /* ---------- engine: builder (town or picture reveal) ---------- */
  var BUILD = ['🏠', '🌳', '🏫', '🏪', '🌳', '🏥', '⛲', '🏡', '🚒', '🌻', '🏟️', '🎡'];
  function revealPicture(shown) {
    // original scene: hot-air balloons over hills, drawn in SVG; tiles cover it until revealed
    var W = 600, H = 400, s = '<svg class="el-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Hidden picture, ' + shown.filter(Boolean).length + ' of 12 tiles revealed">';
    s += '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7cc4ff"/><stop offset="1" stop-color="#d9f0ff"/></linearGradient></defs>';
    s += '<rect width="600" height="400" fill="url(#sky)"/><circle cx="510" cy="70" r="40" fill="#ffd34d"/>';
    s += '<path d="M0 300 Q150 220 300 290 T600 270 V400 H0Z" fill="#7ccf8a"/><path d="M0 340 Q200 290 400 340 T600 330 V400 H0Z" fill="#4fb36a"/>';
    [[150, 140, '#f08c1a', '#ffd34d'], [330, 100, '#d63c7a', '#8a4fd6'], [450, 190, '#2f7fd8', '#1aa37a']].forEach(function (b) {
      s += '<ellipse cx="' + b[0] + '" cy="' + b[1] + '" rx="48" ry="58" fill="' + b[2] + '"/><path d="M' + (b[0] - 48) + ' ' + b[1] + ' Q' + b[0] + ' ' + (b[1] + 20) + ' ' + (b[0] + 48) + ' ' + b[1] + '" stroke="' + b[3] + '" stroke-width="10" fill="none"/>';
      s += '<line x1="' + (b[0] - 22) + '" y1="' + (b[1] + 50) + '" x2="' + (b[0] - 12) + '" y2="' + (b[1] + 82) + '" stroke="#6b4a2b" stroke-width="3"/><line x1="' + (b[0] + 22) + '" y1="' + (b[1] + 50) + '" x2="' + (b[0] + 12) + '" y2="' + (b[1] + 82) + '" stroke="#6b4a2b" stroke-width="3"/>';
      s += '<rect x="' + (b[0] - 15) + '" y="' + (b[1] + 82) + '" width="30" height="20" rx="4" fill="#a86b35"/>';
    });
    s += '<text x="300" y="380" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">Great job, mathematicians!</text>';
    for (var i = 0; i < 12; i++) {
      if (shown[i]) continue;
      var x = (i % 4) * 150, y = Math.floor(i / 4) * 133.3;
      s += '<rect x="' + x + '" y="' + y + '" width="150" height="134" fill="' + ['#8a4fd6', '#2f7fd8', '#0f97b5', '#5a62d8'][(i + Math.floor(i / 4)) % 4] + '" stroke="#fff" stroke-width="3"/>';
      s += '<text x="' + (x + 75) + '" y="' + (y + 80) + '" text-anchor="middle" font-size="44" font-weight="900" fill="#fff" opacity=".85">' + (i + 1) + '</text>';
    }
    return s + '</svg>';
  }
  function townScene(built) {
    var s = '<svg class="el-svg" viewBox="0 0 600 300" role="img" aria-label="Town with ' + built + ' of 12 buildings"><rect width="600" height="300" rx="20" fill="#e6f6ff"/><rect y="200" width="600" height="100" fill="#9fdc9f"/><rect y="236" width="600" height="22" fill="#9aa4b2"/>';
    for (var i = 0; i < 12; i++) {
      var x = 30 + (i % 6) * 95, y = i < 6 ? 150 : 270;
      s += i < built ? '<text x="' + x + '" y="' + y + '" font-size="54">' + BUILD[i] + '</text>' : '<rect x="' + (x + 2) + '" y="' + (y - 48) + '" width="56" height="50" rx="8" fill="none" stroke="#7a8aa0" stroke-width="3" stroke-dasharray="6 5"/>';
    }
    return s + '</svg>';
  }
  function castleScene(built) {
    /* Castle Conquest: 12 pieces appear in order (ground, walls, towers, gate, flags). Original drawing. */
    var s = '<svg class="el-svg" viewBox="0 0 600 320" role="img" aria-label="Castle with ' + built + ' of 12 parts built"><rect width="600" height="320" rx="20" fill="#dff1ff"/><circle cx="520" cy="60" r="34" fill="#ffd34d"/>';
    var P_ = [
      '<path d="M0 270 Q300 235 600 270 V320 H0Z" fill="#7ccf8a"/>',
      '<rect x="170" y="170" width="260" height="100" fill="#c9ccd6" stroke="#59607a" stroke-width="3"/>',
      '<rect x="110" y="120" width="70" height="150" fill="#b7bbc9" stroke="#59607a" stroke-width="3"/>',
      '<rect x="420" y="120" width="70" height="150" fill="#b7bbc9" stroke="#59607a" stroke-width="3"/>',
      '<path d="M170 170 v-18 h26 v18 h26 v-18 h26 v18 h26 v-18 h26 v18 h26 v-18 h26 v18 h26 v-18 h26 v18" fill="#c9ccd6" stroke="#59607a" stroke-width="3"/>',
      '<path d="M270 270 v-52 a30 30 0 0 1 60 0 v52z" fill="#8a5a2b" stroke="#59607a" stroke-width="3"/>',
      '<path d="M104 120 L145 70 L186 120Z" fill="#d63c7a" stroke="#59607a" stroke-width="3"/>',
      '<path d="M414 120 L455 70 L496 120Z" fill="#2f7fd8" stroke="#59607a" stroke-width="3"/>',
      '<rect x="262" y="96" width="76" height="74" fill="#d5d8e2" stroke="#59607a" stroke-width="3"/><path d="M254 96 L300 50 L346 96Z" fill="#8a4fd6" stroke="#59607a" stroke-width="3"/>',
      '<rect x="132" y="160" width="26" height="36" rx="13" fill="#3a4466"/><rect x="442" y="160" width="26" height="36" rx="13" fill="#3a4466"/><rect x="288" y="118" width="24" height="30" rx="12" fill="#3a4466"/>',
      '<line x1="145" y1="70" x2="145" y2="38" stroke="#59607a" stroke-width="3"/><path d="M145 38 l26 9 l-26 9z" fill="#f08c1a"/><line x1="455" y1="70" x2="455" y2="38" stroke="#59607a" stroke-width="3"/><path d="M455 38 l26 9 l-26 9z" fill="#f08c1a"/>',
      '<line x1="300" y1="50" x2="300" y2="14" stroke="#59607a" stroke-width="3"/><path d="M300 14 l34 11 l-34 11z" fill="#1aa37a"/><text x="300" y="306" text-anchor="middle" font-size="22" font-weight="900" fill="#22408a">The castle is yours!</text>'
    ];
    for (var i = 0; i < 12; i++) s += i < built ? P_[i] : '';
    if (built < 12) s += '<text x="300" y="306" text-anchor="middle" font-size="18" font-weight="800" fill="#22408a">' + built + ' of 12 castle parts built</text>';
    return s + '</svg>';
  }
  function detectivePicture(shown) {
    /* Math Detective: an original night scene (clock tower, moon, the missing trophy) hidden under clue tiles. */
    var s = '<svg class="el-svg" viewBox="0 0 600 400" role="img" aria-label="Mystery picture, ' + shown.filter(Boolean).length + ' of 12 clues uncovered">';
    s += '<rect width="600" height="400" fill="#1d2a55"/><circle cx="500" cy="70" r="38" fill="#ffe9a8"/><circle cx="486" cy="60" r="34" fill="#1d2a55" opacity=".35"/>';
    for (var k = 0; k < 26; k++) s += '<circle cx="' + ((k * 83 + 20) % 600) + '" cy="' + ((k * 37 + 15) % 190) + '" r="' + (1 + k % 2) + '" fill="#fff" opacity=".8"/>';
    s += '<rect x="0" y="330" width="600" height="70" fill="#2f3f73"/>';
    s += '<rect x="60" y="230" width="90" height="100" fill="#3d4d86"/><rect x="170" y="200" width="70" height="130" fill="#46568f"/><rect x="430" y="220" width="110" height="110" fill="#3d4d86"/>';
    [80, 110, 185, 210, 450, 480, 510].forEach(function (x, i) { s += '<rect x="' + x + '" y="' + (250 + (i % 2) * 28) + '" width="14" height="16" fill="#ffd34d"/>'; });
    s += '<rect x="270" y="120" width="90" height="210" fill="#6b7bb5" stroke="#1d2a3a" stroke-width="3"/><path d="M262 120 L315 60 L368 120Z" fill="#d63c7a" stroke="#1d2a3a" stroke-width="3"/>';
    s += '<circle cx="315" cy="170" r="30" fill="#fff" stroke="#1d2a3a" stroke-width="3"/><line x1="315" y1="170" x2="315" y2="150" stroke="#1d2a3a" stroke-width="4"/><line x1="315" y1="170" x2="330" y2="176" stroke="#1d2a3a" stroke-width="4"/>';
    s += '<path d="M297 262 h36 v10 a18 18 0 0 1 -36 0z" fill="#ffd34d" stroke="#8a6a00" stroke-width="2"/><rect x="311" y="288" width="8" height="12" fill="#ffd34d"/><rect x="300" y="300" width="30" height="8" rx="2" fill="#ffd34d" stroke="#8a6a00" stroke-width="2"/>';
    s += '<text x="300" y="376" text-anchor="middle" font-size="24" font-weight="900" fill="#fff">Case closed: the trophy was in the clock tower!</text>';
    for (var i = 0; i < 12; i++) {
      if (shown[i]) continue;
      var x = (i % 4) * 150, y = Math.floor(i / 4) * 133.3;
      s += '<rect x="' + x + '" y="' + y + '" width="150" height="134" fill="' + ['#f08c1a', '#1aa37a', '#d63c7a', '#0f97b5'][(i + Math.floor(i / 4)) % 4] + '" stroke="#fff" stroke-width="3"/>';
      s += '<text x="' + (x + 75) + '" y="' + (y + 62) + '" text-anchor="middle" font-size="34">🔍</text><text x="' + (x + 75) + '" y="' + (y + 104) + '" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">Clue ' + (i + 1) + '</text>';
    }
    return s + '</svg>';
  }
  var BUILD_THEMES = {
    town: { scene: function (b) { return townScene(b); }, hud: '🏗️ Buildings: ', label: 'Earn building ', done: 'Your town is complete!', emoji: '🏙️' },
    castle: { scene: function (b) { return castleScene(b); }, hud: '🏰 Castle parts: ', label: 'Earn castle part ', done: 'You conquered the castle!', emoji: '🏰' },
    reveal: { scene: function (b, shown) { return revealPicture(shown); }, hud: '🖼️ Tiles: ', label: 'Uncover tile ', done: 'You revealed the whole picture!', emoji: '🎈' },
    detective: { scene: function (b, shown) { return detectivePicture(shown); }, hud: '🔍 Clues: ', label: 'Uncover clue ', done: 'Case closed! You solved the mystery.', emoji: '🕵️' }
  };
  function playBuilder(cfg) {
    var T = BUILD_THEMES[cfg.theme] || BUILD_THEMES.town;
    var built = 0, shown = new Array(12).fill(false), asked = 0;
    var scene = el('div', stage, 'el-board'), hud = el('div', stage, 'el-hud'), qhost = el('div', stage);
    function draw() {
      scene.innerHTML = T.scene(built, shown);
      hud.innerHTML = ''; el('span', hud, 'el-chip', T.hud + built + ' / 12'); el('span', hud, 'el-chip', 'Questions tried: ' + asked);
    }
    function round() {
      draw();
      if (built >= 12) { qhost.innerHTML = ''; summary(qhost, T.done, T.emoji); return; }
      ask(qhost, { label: T.label + (built + 1), choiceOnly: state.mode === 'class',
        done: function (ok) { asked++; if (ok) { shown[built] = true; built++; } draw(); }, onNext: round });
    }
    round();
  }

  /* ---------- engine: team race ---------- */
  function playRace(cfg) {
    var teams = +(state.mode || 'class2').slice(-1), pos = new Array(teams).fill(0), turn = 0, L = cfg.length;
    var scene = el('div', stage, 'el-board'), hud = el('div', stage, 'el-hud'), qhost = el('div', stage);
    function draw() {
      var W = 900, lane = 60, H = teams * lane + 40, s = '<svg class="el-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Race track">';
      s += '<rect width="' + W + '" height="' + H + '" rx="18" fill="' + (cfg.track || '#5c6b7a') + '"/>';
      for (var i = 0; i <= L; i++) { var x = 80 + i * (W - 160) / L; s += '<line x1="' + x + '" y1="20" x2="' + x + '" y2="' + (H - 20) + '" stroke="#fff" stroke-width="' + (i === L ? 8 : 2) + '" stroke-dasharray="' + (i === L ? '8 8' : '0') + '"/>'; }
      for (var t = 0; t < teams; t++) {
        var y = 20 + t * lane + lane / 2;
        s += '<text x="' + (80 + pos[t] * (W - 160) / L) + '" y="' + (y + 14) + '" text-anchor="middle" font-size="40">' + (cfg.token || '🏎️') + '</text>';
        s += '<rect x="8" y="' + (y - 16) + '" width="64" height="32" rx="10" fill="' + TEAM_COLORS[t] + '" stroke="' + (t === turn ? '#ffd34d' : 'none') + '" stroke-width="5"/>';
        s += '<text x="40" y="' + (y + 7) + '" text-anchor="middle" font-size="18" font-weight="900" fill="#fff">' + (t + 1) + '</text>';
      }
      scene.innerHTML = s + '</svg>';
      hud.innerHTML = '';
      for (var k = 0; k < teams; k++) { var c = el('span', hud, 'el-team' + (k === turn ? ' el-turn' : ''), TEAM_NAMES[k] + ': ' + pos[k]); c.style.background = TEAM_COLORS[k]; }
    }
    function round() {
      draw();
      var win = pos.indexOf(L);
      if (win >= 0) { qhost.innerHTML = ''; summary(qhost, TEAM_NAMES[win] + ' crossed the finish line first!', '🏁'); return; }
      ask(qhost, { label: '★ ' + TEAM_NAMES[turn] + '’s turn', choiceOnly: true, tries: 1,
        done: function (ok) { if (ok) pos[turn] = Math.min(L, pos[turn] + 1); draw(); },
        onNext: function () { turn = (turn + 1) % teams; round(); }, nextLabel: 'Next team →' });
    }
    round();
  }

  /* ---------- engine: soccer ---------- */
  function playSoccer() {
    var ball = 0, score = [0, 0], turn = 0, keep = false;
    var scene = el('div', stage, 'el-board'), hud = el('div', stage, 'el-hud'), qhost = el('div', stage);
    function draw(msg) {
      var W = 900, H = 320, x = W / 2 + ball * 110;
      var s = '<svg class="el-svg" viewBox="0 0 900 320" role="img" aria-label="Soccer field; Blue ' + score[0] + ', Orange ' + score[1] + '"><rect width="900" height="320" rx="20" fill="#3fae5a"/>';
      for (var i = 0; i < 9; i++) s += '<rect x="' + i * 100 + '" width="50" height="320" fill="#45b862"/>';
      s += '<rect x="20" y="20" width="860" height="280" fill="none" stroke="#fff" stroke-width="5"/><line x1="450" y1="20" x2="450" y2="300" stroke="#fff" stroke-width="4"/><circle cx="450" cy="160" r="55" fill="none" stroke="#fff" stroke-width="4"/>';
      s += '<rect x="0" y="110" width="26" height="100" fill="#fff" opacity=".8"/><rect x="874" y="110" width="26" height="100" fill="#fff" opacity=".8"/>';
      s += '<text x="60" y="60" font-size="22" font-weight="900" fill="' + TEAM_COLORS[1] + '" stroke="#fff" stroke-width="0.6">Orange goal</text><text x="840" y="60" text-anchor="end" font-size="22" font-weight="900" fill="' + TEAM_COLORS[0] + '" stroke="#fff" stroke-width="0.6">Blue goal</text>';
      s += '<text x="' + x + '" y="178" text-anchor="middle" font-size="44">⚽</text>';
      if (msg) s += '<text x="450" y="300" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">' + msg + '</text>';
      scene.innerHTML = s + '</svg>';
      hud.innerHTML = '';
      [0, 1].forEach(function (t) { var c = el('span', hud, 'el-team' + (t === turn ? ' el-turn' : ''), TEAM_NAMES[t] + ': ' + score[t] + ' goal' + (score[t] === 1 ? '' : 's')); c.style.background = TEAM_COLORS[t]; });
      el('span', hud, 'el-chip', 'Blue kicks right ➜ · Orange kicks left ⬅');
    }
    function round(msg) {
      draw(msg);
      if (score[0] >= 3 || score[1] >= 3) { qhost.innerHTML = ''; summary(qhost, TEAM_NAMES[score[0] >= 3 ? 0 : 1] + ' wins the match!', '🏆'); return; }
      ask(qhost, { label: '★ ' + TEAM_NAMES[turn] + '’s kick', choiceOnly: true, tries: 1,
        done: function (ok) {
          /* possession: a correct answer moves the ball and keeps the ball; a miss or a goal passes it to the other team */
          var m = '';
          keep = ok;
          if (ok) { ball += turn === 0 ? 1 : -1; if (Math.abs(ball) >= 3) { score[turn]++; ball = 0; keep = false; m = 'GOAL for ' + TEAM_NAMES[turn] + '!'; } else m = TEAM_NAMES[turn] + ' keeps the ball!'; }
          else m = 'Turnover! ' + TEAM_NAMES[1 - turn] + '’s ball.';
          draw(m);
        },
        onNext: function () { if (!keep) turn = 1 - turn; round(); }, nextLabel: 'Next kick →' });
    }
    round();
  }

  /* ---------- engine: Connect 4 ---------- */
  function playC4() {
    var R = 6, C = 7, grid = [], turn = 0;
    for (var r = 0; r < R; r++) grid.push(new Array(C).fill(-1));
    var hud = el('div', stage, 'el-hud'), scene = el('div', stage, 'el-board'), qhost = el('div', stage);
    function win(t) {
      var dirs = [[0, 1], [1, 0], [1, 1], [1, -1]];
      for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) for (var d = 0; d < 4; d++) {
        var k = 0; while (k < 4) { var rr = r + dirs[d][0] * k, cc = c + dirs[d][1] * k; if (rr < 0 || rr >= R || cc < 0 || cc >= C || grid[rr][cc] !== t) break; k++; }
        if (k === 4) return true;
      }
      return false;
    }
    function draw(pickable) {
      hud.innerHTML = '';
      [0, 1].forEach(function (t) { var c = el('span', hud, 'el-team' + (t === turn ? ' el-turn' : ''), TEAM_NAMES[t]); c.style.background = TEAM_COLORS[t]; });
      el('span', hud, 'el-chip', pickable ? 'Choose a column for your disc!' : 'Answer correctly to earn a disc.');
      var s = '<svg class="el-svg" viewBox="0 0 700 600" style="max-width:34rem;margin:auto" role="img" aria-label="Connect 4 board"><rect width="700" height="600" rx="30" fill="#2f5fd8"/>';
      for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) s += '<circle cx="' + (50 + c * 100) + '" cy="' + (50 + r * 100) + '" r="40" fill="' + (grid[r][c] < 0 ? '#eef4ff' : TEAM_COLORS[grid[r][c]]) + '"/>';
      scene.innerHTML = s + '</svg>';
      if (pickable) {
        var bar = el('div', scene, 'el-grid-btns'); bar.style.gridTemplateColumns = 'repeat(7, 1fr)'; bar.style.maxWidth = '34rem'; bar.style.margin = '.5rem auto';
        for (var col = 0; col < C; col++) (function (col) {
          var b = el('button', bar, 'el-btn primary', '⬇'); b.setAttribute('aria-label', 'Drop in column ' + (col + 1));
          b.disabled = grid[0][col] >= 0;
          b.onclick = function () {
            for (var r = R - 1; r >= 0; r--) if (grid[r][col] < 0) { grid[r][col] = turn; break; }
            if (win(turn)) { draw(false); qhost.innerHTML = ''; summary(qhost, TEAM_NAMES[turn] + ' connected four!', '🎉'); return; }
            if (grid[0].every(function (x) { return x >= 0; })) { draw(false); qhost.innerHTML = ''; summary(qhost, 'The board is full. It’s a tie — great teamwork!', '🤝'); return; }
            turn = 1 - turn; round();
          };
        })(col);
      }
    }
    function round() {
      draw(false);
      ask(qhost, { label: '★ ' + TEAM_NAMES[turn] + '’s turn', choiceOnly: true, tries: 1,
        done: function (ok) { if (ok) { qhost.querySelector('.el-q-tools') && null; draw(true); } },
        onNext: function () { var picking = scene.querySelector('.el-grid-btns'); if (picking) { qhost.innerHTML = ''; el('p', qhost, 'el-chip', 'Pick a column above!'); return; } turn = 1 - turn; round(); }, nextLabel: 'Continue →' });
    }
    round();
  }

  /* ---------- engine: card match ---------- */
  function playMatch(cfg) {
    var QL = (cfg.cardIcons || ['❓', '🔑'])[0] + ' Problem', AL = (cfg.cardIcons || ['❓', '🔑'])[1] + ' Answer';
    var pool = state.deck.filter(function (p) { return p.kind === 'sa' && String(p.answer).length <= 18 && p.prompt.length <= 110 && !p.img && p.prompt.indexOf('\n') < 0; });
    var seen = {}, pairs = [];
    pool.forEach(function (p) { var k = K.parseNum(p.answer); var key = k ? k.join('/') : String(p.answer).toLowerCase(); if (!seen[key] && pairs.length < 6) { seen[key] = 1; pairs.push(p); } });
    if (pairs.length < 4) { K.errorBox(stage, 'This unit and level do not have enough short-answer questions for ' + cfg.title + '. Try another game.'); return; }
    var cards = [];
    pairs.forEach(function (p, i) { cards.push({ pair: i, text: p.prompt, kind: 'q', p: p }); cards.push({ pair: i, text: p.answer, kind: 'a', p: p }); });
    cards = K.shuffle(cards);
    var open = [], matched = 0, tries = 0, turn = 0, pts = [0, 0];
    var hud = el('div', stage, 'el-hud'), grid = el('div', stage, 'el-grid-btns'), qhost = el('div', stage);
    grid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(10rem, 1fr))';
    function drawHud() {
      hud.innerHTML = ''; el('span', hud, 'el-chip', 'Pairs found: ' + matched + ' / ' + pairs.length); el('span', hud, 'el-chip', 'Flips: ' + tries);
      if (state.mode === 'pairs') [0, 1].forEach(function (t) { var c = el('span', hud, 'el-team' + (t === turn ? ' el-turn' : ''), 'Player ' + (t + 1) + ': ' + pts[t]); c.style.background = TEAM_COLORS[t]; });
    }
    cards.forEach(function (c, i) {
      var b = el('button', grid, 'el-choice'); b.style.minHeight = '6rem'; b.style.justifyContent = 'center';
      b.setAttribute('aria-label', 'Card ' + (i + 1));
      el('span', b, 'el-ct', c.kind === 'q' ? QL : AL);
      c.btn = b;
      b.onclick = function () {
        if (c.done || open.indexOf(c) >= 0 || open.length >= 2) return;
        open.push(c); b.innerHTML = ''; K.math(el('span', b, 'el-ct'), c.text); b.classList.add('on');
        if (open.length === 2) {
          tries++;
          var a = open[0], z = open[1];
          var ok = a.pair === z.pair && a.kind !== z.kind;
          setTimeout(function () {
            if (ok) { a.done = z.done = true; a.btn.classList.add('right'); z.btn.classList.add('right'); matched++; pts[turn]++; record(a.p, true); qhost.innerHTML = ''; var f = el('div', qhost, 'el-feedback good', K.pick(K.PRAISE) + ' That is a match.'); }
            else {
              [a, z].forEach(function (x) { x.btn.classList.remove('on'); x.btn.innerHTML = ''; el('span', x.btn, 'el-ct', x.kind === 'q' ? QL : AL); });
              qhost.innerHTML = ''; el('div', qhost, 'el-feedback try', 'Not a match yet. Remember where those cards are!');
              if (state.mode === 'pairs') turn = 1 - turn;
            }
            open = []; drawHud();
            if (matched === pairs.length) { qhost.innerHTML = ''; summary(qhost, state.mode === 'pairs' ? (pts[0] === pts[1] ? 'A tie! Great teamwork.' : 'Player ' + (pts[0] > pts[1] ? 1 : 2) + ' found the most pairs!') : 'All pairs matched in ' + tries + ' flips!', cfg.icon || '🧩'); }
          }, ok ? 300 : 1400);
        }
      };
    });
    drawHud();
  }

  /* ---------- engine: Fraction Frenzy (exactly constructed fraction models) ---------- */
  function fracModel(n, d, shape) {
    var s = '<svg class="el-svg" viewBox="0 0 420 220" style="max-width:26rem;margin:auto" role="img" aria-label="Fraction model: ' + n + ' of ' + d + ' equal parts shaded">';
    if (shape === 'circle') {
      var cx = 210, cy = 110, R = 95;
      for (var i = 0; i < d; i++) {
        var a0 = -Math.PI / 2 + 2 * Math.PI * i / d, a1 = -Math.PI / 2 + 2 * Math.PI * (i + 1) / d;
        s += d === 1 ? '<circle cx="' + cx + '" cy="' + cy + '" r="' + R + '" fill="' + (n ? '#ffc27a' : '#fff') + '" stroke="#1d2a3a" stroke-width="3"/>' :
          '<path d="M' + cx + ',' + cy + ' L' + (cx + R * Math.cos(a0)).toFixed(1) + ',' + (cy + R * Math.sin(a0)).toFixed(1) + ' A' + R + ',' + R + ' 0 ' + (a1 - a0 > Math.PI ? 1 : 0) + ' 1 ' + (cx + R * Math.cos(a1)).toFixed(1) + ',' + (cy + R * Math.sin(a1)).toFixed(1) + ' Z" fill="' + (i < n ? '#ffc27a' : '#fff') + '" stroke="#1d2a3a" stroke-width="3"/>';
      }
    } else {
      var w = 380 / d;
      for (var j = 0; j < d; j++) s += '<rect x="' + (20 + j * w).toFixed(1) + '" y="70" width="' + w.toFixed(1) + '" height="80" fill="' + (j < n ? '#7fb6f0' : '#fff') + '" stroke="#1d2a3a" stroke-width="3"/>';
    }
    return s + '</svg>';
  }
  function frenzyQuestion(level) {
    var dens = level === 'cp2' ? [2, 3, 4, 5, 6, 8] : [3, 4, 5, 6, 8, 10, 12];
    var d = K.pick(dens), n = 1 + Math.floor(Math.random() * (d - 1));
    var kind = level === 'cp2' ? 'name' : K.pick(['name', 'equiv', 'simplest']);
    var gcd = function (a, b) { while (b) { var t = a % b; a = b; b = t; } return a; };
    var g = gcd(n, d), sn = n / g, sd = d / g;
    var good, bad = [], prompt;
    if (kind === 'name') { good = n + '/' + d; prompt = 'What fraction of the model is shaded?'; bad = [(d - n) + '/' + d, n + '/' + (d + 1), d + '/' + n]; }
    else if (kind === 'equiv') { var k = 2 + Math.floor(Math.random() * 2); good = n * k + '/' + d * k; prompt = 'Which fraction is equivalent to the shaded part?'; bad = [(n + k) + '/' + (d + k), n * k + '/' + d, (d - n) * k + '/' + d * k]; }
    else { if (g === 1) return frenzyQuestion(level); good = sn + '/' + sd; prompt = 'Which fraction in simplest form names the shaded part?'; bad = [n + '/' + (d * 2), sd + '/' + sn, (sd - sn || 1) + '/' + sd]; }
    var val = function (t) { var p = t.split('/'); return +p[0] / +p[1]; };
    bad = bad.filter(function (b, i, a) { return a.indexOf(b) === i && b !== good && Math.abs(val(b) - val(good)) > 1e-9 && +b.split('/')[1] > 0; });
    if (bad.length < 2) return frenzyQuestion(level);
    var opts = K.shuffle(bad.slice(0, 3).map(function (t) { return { text: t, correct: false }; }).concat([{ text: good, correct: true }]));
    return { id: 'frenzy', skillId: 'frenzy', prompt: prompt, kind: 'mc', options: opts, answer: good, steps: ['Count the equal parts: ' + d + '. Count the shaded parts: ' + n + '.', 'The shaded part is ' + n + '/' + d + (g > 1 ? ' = ' + sn + '/' + sd : '') + '.'], svg: fracModel(n, d, Math.random() < 0.5 ? 'bar' : 'circle') };
  }
  function playFrenzy(cfg) {
    var round = 0, right = 0, total = 10;
    var hud = el('div', stage, 'el-hud'), qhost = el('div', stage);
    function go() {
      hud.innerHTML = ''; el('span', hud, 'el-chip', 'Round ' + Math.min(round + 1, total) + ' of ' + total); el('span', hud, 'el-chip', (cfg.icon || '🍕') + ' Correct: ' + right);
      if (round >= total) { qhost.innerHTML = ''; state.stats.frenzy = { right: right, tries: total }; state.info.skills.unshift({ id: 'frenzy', name: 'Fraction models' }); summary(qhost, cfg.title + ' complete!', cfg.icon || '🍕'); return; }
      var p = frenzyQuestion(state.level);
      var box = K.card(qhost, p, { label: 'Fraction model', tries: state.mode === 'class' ? 1 : 2, teacher: state.teacher && state.mode === 'class',
        onAnswer: function (ok) { if (ok) right++; }, onNext: function () { round++; go(); } });
      var holder = D.createElement('div'); holder.innerHTML = p.svg; box.insertBefore(holder, box.children[2]);
    }
    go();
  }

  /* ---------- engine: arrays (exactly constructed multiplication arrays and area models) ---------- */
  function arraySvg(r, c, split) {
    var s0 = Math.min(34, 520 / c, 250 / r), W = c * s0 + 40, H = r * s0 + 40;
    var s = '<svg class="el-svg" viewBox="0 0 ' + W.toFixed(0) + ' ' + H.toFixed(0) + '" style="max-width:' + Math.max(16, W / 16).toFixed(0) + 'rem;margin:auto" role="img" aria-label="Array with ' + r + ' rows and ' + c + ' columns' + (split ? ', split after column ' + split : '') + '">';
    for (var i = 0; i < r; i++) for (var j = 0; j < c; j++) s += '<circle cx="' + (20 + j * s0 + s0 / 2).toFixed(1) + '" cy="' + (20 + i * s0 + s0 / 2).toFixed(1) + '" r="' + (s0 * 0.36).toFixed(1) + '" fill="' + (split && j >= split ? '#f08c1a' : '#2f7fd8') + '"/>';
    if (split) s += '<line x1="' + (20 + split * s0) + '" y1="8" x2="' + (20 + split * s0) + '" y2="' + (H - 8) + '" stroke="#1d2a3a" stroke-width="3" stroke-dasharray="7 6"/>';
    return s + '</svg>';
  }
  function arrayQuestion(level) {
    var r = 2 + Math.floor(Math.random() * (level === 'cp2' ? 4 : 5)), c = (level === 'cp2' ? 3 : 6) + Math.floor(Math.random() * (level === 'honors' ? 9 : 7));
    var kind = level === 'cp2' ? K.pick(['product', 'product', 'equation']) : K.pick(['product', 'missing', 'split', 'equation']);
    var n = r * c, good, bad, prompt, steps, split = 0;
    if (kind === 'product') { prompt = 'How many dots are in the array?'; good = String(n); bad = [String(r + c), String(n + r), String(n - c)]; steps = ['The array has ' + r + ' rows of ' + c + '.', r + ' × ' + c + ' = ' + n + '.']; }
    else if (kind === 'missing') { prompt = 'The array has ' + n + ' dots in ' + r + ' equal rows. Which division equation tells how many dots are in each row?'; good = n + ' ÷ ' + r + ' = ' + c; bad = [n + ' ÷ ' + r + ' = ' + (c + 1), n + ' − ' + r + ' = ' + (n - r), r + ' ÷ ' + n + ' = ' + c]; steps = ['Divide the total by the number of rows.', n + ' ÷ ' + r + ' = ' + c + '.']; }
    else if (kind === 'split') { split = 1 + Math.floor(Math.random() * (c - 1)); if (c >= 10) split = 5 * Math.max(1, Math.round(split / 5)); if (split >= c) split = c - 1; prompt = 'The dashed line splits the array into two parts. Which expression matches the two parts?'; good = '(' + r + ' × ' + split + ') + (' + r + ' × ' + (c - split) + ')'; bad = ['(' + r + ' × ' + split + ') × (' + r + ' × ' + (c - split) + ')', '(' + r + ' + ' + split + ') + (' + r + ' + ' + (c - split) + ')', '(' + r + ' × ' + split + ') + ' + (c - split)]; steps = ['The blue part is ' + r + ' × ' + split + ' and the orange part is ' + r + ' × ' + (c - split) + '.', 'Together: ' + r * split + ' + ' + r * (c - split) + ' = ' + n + '.']; }
    else { prompt = 'Which multiplication equation matches the array?'; good = r + ' × ' + c + ' = ' + n; bad = [r + ' + ' + c + ' = ' + (r + c), r + ' × ' + c + ' = ' + (n + c), (r + 1) + ' × ' + c + ' = ' + (n + c)]; steps = ['Count the rows and the dots in each row.', r + ' rows of ' + c + ' is ' + r + ' × ' + c + ' = ' + n + '.']; }
    bad = bad.filter(function (b, i, a) { return a.indexOf(b) === i && b !== good; });
    if (bad.length < 3 || (kind === 'product' && (n - c <= 0 || r + c === n))) return arrayQuestion(level);
    var opts = K.shuffle(bad.slice(0, 3).map(function (t) { return { text: t, correct: false }; }).concat([{ text: good, correct: true }]));
    return { id: 'arrays', skillId: 'arrays', prompt: prompt, kind: 'mc', options: opts, answer: good, steps: steps, svg: arraySvg(r, c, split), meta: {} };
  }
  function playArrays(cfg) {
    var round = 0, right = 0, total = 10;
    var hud = el('div', stage, 'el-hud'), qhost = el('div', stage);
    function go() {
      hud.innerHTML = ''; el('span', hud, 'el-chip', 'Round ' + Math.min(round + 1, total) + ' of ' + total); el('span', hud, 'el-chip', (cfg.icon || '🔵') + ' Correct: ' + right);
      if (round >= total) { qhost.innerHTML = ''; state.stats.arrays = { right: right, tries: total }; state.info.skills.unshift({ id: 'arrays', name: 'Arrays and area models' }); summary(qhost, cfg.title + ' complete!', cfg.icon || '🔵'); return; }
      var p = arrayQuestion(state.level);
      var box = K.card(qhost, p, { label: 'Array ' + (round + 1), tries: state.mode === 'class' ? 1 : 2, teacher: state.teacher && state.mode === 'class',
        onAnswer: function (ok) { if (ok) right++; }, onNext: function () { round++; go(); } });
      var holder = D.createElement('div'); holder.innerHTML = p.svg; box.insertBefore(holder, box.children[2]);
    }
    go();
  }

  /* ---------- boot ---------- */
  function boot() {
    main = D.getElementById('app');
    var unitId = P.get('unit'), gameId = P.get('game') || Object.keys(GAMES)[0], cfg = GAMES[gameId];
    if (!cfg) { K.errorBox(main, 'Unknown game.'); return; }
    var info = K.unitInfo(unitId);
    if (!info.unit) { K.errorBox(main, 'Choose a ' + K.CFG.label + ' unit from Mr. K’s Classroom.'); return; }
    state.info = info;
    D.title = cfg.title + ' · ' + info.unit.name + ' · ' + K.CFG.label;
    K.chrome(cfg.icon + ' ' + cfg.title, K.CFG.label + ' · Unit ' + info.number + ': ' + info.unit.name);
    var loading = el('div', main, 'el-panel', 'Loading questions…');
    var generated = cfg.engine === 'frenzy' || cfg.engine === 'arrays';
    var bankP = generated ? Promise.resolve([]) : K.load(unitId);
    bankP.then(function (qs) {
      loading.remove();
      function afterSkills(ids) {
        K.setupPanel(main, { heading: cfg.icon + ' ' + cfg.title, intro: cfg.intro, modes: cfg.modes, startLabel: 'Play ▶', skills: ids,
          start: function (o) {
            state.level = o.level; state.mode = o.mode;
            state.deck = K.shuffle(qs.filter(function (q) { return q.level === o.level && ids.indexOf(q.skillId) >= 0; }).map(K.prepare));
            main.innerHTML = ''; stage = el('div', main, 'el-stage');
            ({ path: playPath, builder: playBuilder, race: playRace, soccer: playSoccer, c4: playC4, match: playMatch, frenzy: playFrenzy, arrays: playArrays })[cfg.engine](cfg);
          } });
      }
      if (generated) afterSkills([]); else K.chooseSkills(info, afterSkills);
    }).catch(function (e) { K.errorBox(main, e.message); });
  }
  G.MKEL_GAMES = GAMES;
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
})(window);
