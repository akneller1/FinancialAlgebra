/* Grade 5 game collection. Every move forward requires a correct answer to a verified bank question.
   Individual modes: retries, hints, no timers. Whole-class modes: teams, large text, clear turn indicators.
   Engines: adventure-path (Math Quest, Treasure Trail, Space Explorer), builder (Math Builders, Picture Reveal),
   team-race (Math Race, Math Soccer), Connect 4, card-match (Puzzle Masters) and Fraction Frenzy (generated fraction models). */
(function (G) {
  'use strict';
  var g5 = G.G5, el = g5.el, D = G.document, P = g5.P;
  var TEAM_COLORS = ['#2f7fd8', '#f08c1a', '#1aa37a', '#d63c7a'];
  var TEAM_NAMES = ['Blue Team', 'Orange Team', 'Green Team', 'Pink Team'];

  var GAMES = {
    'math-quest': { title: 'Math Quest', icon: '🗺️', engine: 'path', modes: [['solo', 'On my own'], ['class', 'Whole class together']],
      intro: 'Travel through six lands. Answer two questions correctly in each land to unlock the next one!',
      stops: ['Whispering Woods', 'Rainbow River', 'Crystal Cave', 'Snowy Peak', 'Cloud Castle', 'Treasure Vault'], per: 2, theme: 'quest' },
    'treasure-trail': { title: 'Treasure Trail', icon: '💎', engine: 'path', modes: [['solo', 'On my own'], ['class', 'Whole class together']],
      intro: 'Follow the map stone by stone. Each correct answer moves you forward and adds a gem to your chest.',
      stops: ['Start', 'Palm Beach', 'Old Bridge', 'Parrot Cove', 'Hidden Cave', 'Waterfall', 'Volcano Path', 'Shipwreck', 'Lighthouse', 'X Marks the Spot'], per: 1, theme: 'trail' },
    'space-explorer': { title: 'Space Explorer', icon: '🚀', engine: 'path', modes: [['solo', 'On my own'], ['class', 'Whole class together']],
      intro: 'Fuel your rocket with correct answers and visit every planet in the Math Galaxy.',
      stops: ['Launch Pad', 'Moon Base', 'Planet Ember', 'Planet Aqua', 'Ring World', 'Star Station'], per: 2, theme: 'space' },
    'math-builders': { title: 'Math Builders', icon: '🏗️', engine: 'builder', modes: [['solo', 'On my own'], ['class', 'Whole class together']],
      intro: 'Every correct answer earns a building for your town. Build all 12 to finish!', count: 12, theme: 'town' },
    'picture-reveal': { title: 'Picture Reveal', icon: '🖼️', engine: 'builder', modes: [['solo', 'On my own'], ['class', 'Whole class together']],
      intro: 'Answer correctly to uncover the hidden picture, one tile at a time.', count: 12, theme: 'reveal' },
    'math-race': { title: 'Math Race', icon: '🏁', engine: 'race', modes: [['class2', '2 teams'], ['class3', '3 teams'], ['class4', '4 teams']],
      intro: 'Teams take turns. A correct answer moves your car one space. First team to the finish line wins!', length: 8 },
    'math-soccer': { title: 'Math Soccer', icon: '⚽', engine: 'soccer', modes: [['class2', '2 teams']],
      intro: 'A correct answer kicks the ball toward the other goal and keeps the ball. A miss is a turnover. Score 3 goals to win!' },
    'connect-four': { title: 'Connect 4', icon: '🔴', engine: 'c4', modes: [['class2', '2 teams']],
      intro: 'Answer correctly to drop a disc in your column. Get four in a row to win!' },
    'puzzle-masters': { title: 'Puzzle Masters', icon: '🧩', engine: 'match', modes: [['solo', 'On my own'], ['pairs', 'With a partner']],
      intro: 'Flip two cards. Work out each problem and match it to its answer. Match all the pairs to solve the puzzle.' },
    'fraction-frenzy': { title: 'Fraction Frenzy', icon: '🍕', engine: 'frenzy', modes: [['solo', 'On my own'], ['class', 'Whole class together']],
      intro: 'Look at each fraction model and choose the matching fraction. Watch for equivalent fractions!' }
  };

  var state = { deck: [], used: 0, stats: {}, info: null, level: 'cp1', mode: 'solo', teacher: P.get('student') !== '1' };
  var main, stage;

  function record(p, ok) {
    var s = state.stats[p.skillId] || (state.stats[p.skillId] = { right: 0, tries: 0 });
    s.tries++; if (ok) s.right++;
  }
  function next(choiceOnly) {
    for (var k = 0; k < state.deck.length; k++) {
      var p = state.deck[state.used++ % state.deck.length];
      var c = choiceOnly ? g5.asChoice(p) : (p.kind === 'parts' ? null : p);
      if (c) return c;
    }
    return null;
  }
  function ask(host, opts) {
    var p = next(opts.choiceOnly);
    if (!p) { g5.errorBox(host, 'No questions match these settings. Try another level or more skills.'); return; }
    g5.card(host, p, { label: opts.label, teacher: state.teacher && /class|pairs/.test(state.mode), tries: opts.tries || (/class/.test(state.mode) ? 1 : 2),
      onAnswer: function (ok) { record(p, ok); opts.done(ok); }, onNext: opts.onNext, nextLabel: opts.nextLabel, showAnswer: true });
  }
  function summary(host, headline, emoji) {
    var box = el('section', host, 'g5-panel g5-celebrate');
    el('div', box, 'big', emoji || '🎉');
    el('h2', box, null, headline);
    var tot = 0, right = 0;
    Object.keys(state.stats).forEach(function (k) { tot += state.stats[k].tries; right += state.stats[k].right; });
    el('p', box, null, right + ' correct answers out of ' + tot + ' questions. Every question you worked on made your brain stronger!');
    if (state.teacher) {
      var det = el('details', box, 'g5-summary'); el('summary', det, null, 'Teacher view: results by skill (not saved anywhere)');
      var t = el('table', det), h = el('tr', t); ['Skill', 'Correct', 'Tried'].forEach(function (x) { el('th', h, null, x); });
      state.info.skills.forEach(function (s) { var st = state.stats[s.id]; if (!st) return; var r = el('tr', t); el('td', r, null, s.name); el('td', r, null, st.right); el('td', r, null, st.tries); });
    }
    var again = el('button', box, 'g5-btn primary big', 'Play again'); again.onclick = function () { G.location.reload(); };
  }

  /* ---------- engine: adventure path ---------- */
  function pathScene(cfg, pos, progress) {
    var n = cfg.stops.length, W = 900, H = 300;
    var pts = cfg.stops.map(function (_, i) { return [70 + i * (W - 140) / (n - 1), 150 + Math.sin(i * 1.3) * 70]; });
    var bg = { quest: ['#dff3e3', '#bfe6c8'], trail: ['#fdf1d6', '#f6dca5'], space: ['#1b2350', '#2b3570'] }[cfg.theme];
    var s = '<svg class="g5-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Progress map: ' + pos + ' of ' + (n - 1) + ' steps complete">';
    s += '<rect width="' + W + '" height="' + H + '" rx="22" fill="' + bg[0] + '"/>';
    if (cfg.theme === 'space') for (var k = 0; k < 40; k++) s += '<circle cx="' + ((k * 97) % W) + '" cy="' + ((k * 53) % H) + '" r="' + (1 + k % 3) + '" fill="#fff" opacity=".7"/>';
    else s += '<path d="M0 ' + (H - 50) + ' Q ' + W / 2 + ' ' + (H - 110) + ' ' + W + ' ' + (H - 40) + ' L ' + W + ' ' + H + ' L 0 ' + H + 'Z" fill="' + bg[1] + '"/>';
    s += '<polyline points="' + pts.map(function (p) { return p.join(','); }).join(' ') + '" fill="none" stroke="' + (cfg.theme === 'space' ? '#8fa6ff' : '#b07a3a') + '" stroke-width="6" stroke-dasharray="14 10"/>';
    pts.forEach(function (p, i) {
      var done = i < pos, here = i === pos;
      var col = done ? '#1aa37a' : here ? '#ffb000' : (cfg.theme === 'space' ? '#5a62d8' : '#ffffff');
      s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="' + (here ? 26 : 20) + '" fill="' + col + '" stroke="#1d2a3a" stroke-width="3"/>';
      s += '<text x="' + p[0] + '" y="' + (p[1] + 7) + '" text-anchor="middle" font-size="20" font-weight="900" fill="' + (done || here ? '#fff' : '#1d2a3a') + '">' + (done ? '✓' : i + 1) + '</text>';
      s += '<text x="' + p[0] + '" y="' + (p[1] + (i % 2 ? -36 : 50)) + '" text-anchor="middle" font-size="15" font-weight="800" fill="' + (cfg.theme === 'space' ? '#fff' : '#1d2a3a') + '">' + g5.esc(cfg.stops[i]) + '</text>';
    });
    var me = pts[Math.min(pos, n - 1)];
    var token = { quest: '🧭', trail: '🏴‍☠️', space: '🚀' }[cfg.theme];
    s += '<text x="' + me[0] + '" y="' + (me[1] - 30) + '" text-anchor="middle" font-size="34">' + token + '</text>';
    if (cfg.per > 1 && pos < n - 1) s += '<text x="' + (W - 20) + '" y="34" text-anchor="end" font-size="18" font-weight="800" fill="' + (cfg.theme === 'space' ? '#fff' : '#1d2a3a') + '">This stop: ' + progress + ' of ' + cfg.per + ' correct</text>';
    return s + '</svg>';
  }
  function playPath(cfg) {
    var pos = 0, progress = 0, gems = 0;
    var scene = el('div', stage, 'g5-board'), hud = el('div', stage, 'g5-hud'), qhost = el('div', stage);
    function draw() {
      scene.innerHTML = pathScene(cfg, pos, progress);
      hud.innerHTML = '';
      el('span', hud, 'g5-chip', (cfg.theme === 'trail' ? '💎 Gems: ' : cfg.theme === 'space' ? '⛽ Fuel cells: ' : '⭐ Stars: ') + gems);
      el('span', hud, 'g5-chip', 'Level: ' + g5.levelName(state.level));
    }
    function round() {
      draw();
      if (pos >= cfg.stops.length - 1) { qhost.innerHTML = ''; summary(qhost, cfg.theme === 'trail' ? 'You found the treasure!' : cfg.theme === 'space' ? 'Mission complete!' : 'Quest complete!', cfg.theme === 'space' ? '🌟' : '🏆'); return; }
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
    var W = 600, H = 400, s = '<svg class="g5-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Hidden picture, ' + shown.filter(Boolean).length + ' of 12 tiles revealed">';
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
    var s = '<svg class="g5-svg" viewBox="0 0 600 300" role="img" aria-label="Town with ' + built + ' of 12 buildings"><rect width="600" height="300" rx="20" fill="#e6f6ff"/><rect y="200" width="600" height="100" fill="#9fdc9f"/><rect y="236" width="600" height="22" fill="#9aa4b2"/>';
    for (var i = 0; i < 12; i++) {
      var x = 30 + (i % 6) * 95, y = i < 6 ? 150 : 270;
      s += i < built ? '<text x="' + x + '" y="' + y + '" font-size="54">' + BUILD[i] + '</text>' : '<rect x="' + (x + 2) + '" y="' + (y - 48) + '" width="56" height="50" rx="8" fill="none" stroke="#7a8aa0" stroke-width="3" stroke-dasharray="6 5"/>';
    }
    return s + '</svg>';
  }
  function playBuilder(cfg) {
    var built = 0, shown = new Array(12).fill(false), asked = 0;
    var scene = el('div', stage, 'g5-board'), hud = el('div', stage, 'g5-hud'), qhost = el('div', stage);
    function draw() {
      scene.innerHTML = cfg.theme === 'town' ? townScene(built) : revealPicture(shown);
      hud.innerHTML = ''; el('span', hud, 'g5-chip', (cfg.theme === 'town' ? '🏗️ Buildings: ' : '🖼️ Tiles: ') + built + ' / 12'); el('span', hud, 'g5-chip', 'Questions tried: ' + asked);
    }
    function round() {
      draw();
      if (built >= 12) { qhost.innerHTML = ''; summary(qhost, cfg.theme === 'town' ? 'Your town is complete!' : 'You revealed the whole picture!', cfg.theme === 'town' ? '🏙️' : '🎈'); return; }
      ask(qhost, { label: cfg.theme === 'town' ? 'Earn building ' + (built + 1) : 'Uncover tile ' + (built + 1), choiceOnly: state.mode === 'class',
        done: function (ok) { asked++; if (ok) { shown[built] = true; built++; } draw(); }, onNext: round });
    }
    round();
  }

  /* ---------- engine: team race ---------- */
  function playRace(cfg) {
    var teams = +(state.mode || 'class2').slice(-1), pos = new Array(teams).fill(0), turn = 0, L = cfg.length;
    var scene = el('div', stage, 'g5-board'), hud = el('div', stage, 'g5-hud'), qhost = el('div', stage);
    function draw() {
      var W = 900, lane = 60, H = teams * lane + 40, s = '<svg class="g5-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Race track">';
      s += '<rect width="' + W + '" height="' + H + '" rx="18" fill="#5c6b7a"/>';
      for (var i = 0; i <= L; i++) { var x = 80 + i * (W - 160) / L; s += '<line x1="' + x + '" y1="20" x2="' + x + '" y2="' + (H - 20) + '" stroke="#fff" stroke-width="' + (i === L ? 8 : 2) + '" stroke-dasharray="' + (i === L ? '8 8' : '0') + '"/>'; }
      for (var t = 0; t < teams; t++) {
        var y = 20 + t * lane + lane / 2;
        // The race advances rightward: mirror the default left-facing emoji around its center.
        // SVG transforms preserve the car's race position as it moves between lanes/steps.
        var carX = 80 + pos[t] * (W - 160) / L;
        s += '<text x="' + carX + '" y="' + (y + 14) + '" text-anchor="middle" font-size="40"' +
          ' transform="translate(' + (2 * carX) + ' 0) scale(-1 1)">🏎️</text>';
        s += '<rect x="8" y="' + (y - 16) + '" width="64" height="32" rx="10" fill="' + TEAM_COLORS[t] + '" stroke="' + (t === turn ? '#ffd34d' : 'none') + '" stroke-width="5"/>';
        s += '<text x="40" y="' + (y + 7) + '" text-anchor="middle" font-size="18" font-weight="900" fill="#fff">' + (t + 1) + '</text>';
      }
      scene.innerHTML = s + '</svg>';
      hud.innerHTML = '';
      for (var k = 0; k < teams; k++) { var c = el('span', hud, 'g5-team' + (k === turn ? ' g5-turn' : ''), TEAM_NAMES[k] + ': ' + pos[k]); c.style.background = TEAM_COLORS[k]; }
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
    var scene = el('div', stage, 'g5-board'), hud = el('div', stage, 'g5-hud'), qhost = el('div', stage);
    function draw(msg) {
      var W = 900, H = 320, x = W / 2 + ball * 110;
      var s = '<svg class="g5-svg" viewBox="0 0 900 320" role="img" aria-label="Soccer field; Blue ' + score[0] + ', Orange ' + score[1] + '"><rect width="900" height="320" rx="20" fill="#3fae5a"/>';
      for (var i = 0; i < 9; i++) s += '<rect x="' + i * 100 + '" width="50" height="320" fill="#45b862"/>';
      s += '<rect x="20" y="20" width="860" height="280" fill="none" stroke="#fff" stroke-width="5"/><line x1="450" y1="20" x2="450" y2="300" stroke="#fff" stroke-width="4"/><circle cx="450" cy="160" r="55" fill="none" stroke="#fff" stroke-width="4"/>';
      s += '<rect x="0" y="110" width="26" height="100" fill="#fff" opacity=".8"/><rect x="874" y="110" width="26" height="100" fill="#fff" opacity=".8"/>';
      s += '<text x="60" y="60" font-size="22" font-weight="900" fill="' + TEAM_COLORS[1] + '" stroke="#fff" stroke-width="0.6">Orange goal</text><text x="840" y="60" text-anchor="end" font-size="22" font-weight="900" fill="' + TEAM_COLORS[0] + '" stroke="#fff" stroke-width="0.6">Blue goal</text>';
      s += '<text x="' + x + '" y="178" text-anchor="middle" font-size="44">⚽</text>';
      if (msg) s += '<text x="450" y="300" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">' + msg + '</text>';
      scene.innerHTML = s + '</svg>';
      hud.innerHTML = '';
      [0, 1].forEach(function (t) { var c = el('span', hud, 'g5-team' + (t === turn ? ' g5-turn' : ''), TEAM_NAMES[t] + ': ' + score[t] + ' goal' + (score[t] === 1 ? '' : 's')); c.style.background = TEAM_COLORS[t]; });
      el('span', hud, 'g5-chip', 'Blue kicks right ➜ · Orange kicks left ⬅');
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
    var hud = el('div', stage, 'g5-hud'), scene = el('div', stage, 'g5-board'), qhost = el('div', stage);
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
      [0, 1].forEach(function (t) { var c = el('span', hud, 'g5-team' + (t === turn ? ' g5-turn' : ''), TEAM_NAMES[t]); c.style.background = TEAM_COLORS[t]; });
      el('span', hud, 'g5-chip', pickable ? 'Choose a column for your disc!' : 'Answer correctly to earn a disc.');
      var s = '<svg class="g5-svg" viewBox="0 0 700 600" style="max-width:34rem;margin:auto" role="img" aria-label="Connect 4 board"><rect width="700" height="600" rx="30" fill="#2f5fd8"/>';
      for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) s += '<circle cx="' + (50 + c * 100) + '" cy="' + (50 + r * 100) + '" r="40" fill="' + (grid[r][c] < 0 ? '#eef4ff' : TEAM_COLORS[grid[r][c]]) + '"/>';
      scene.innerHTML = s + '</svg>';
      if (pickable) {
        var bar = el('div', scene, 'g5-grid-btns'); bar.style.gridTemplateColumns = 'repeat(7, 1fr)'; bar.style.maxWidth = '34rem'; bar.style.margin = '.5rem auto';
        for (var col = 0; col < C; col++) (function (col) {
          var b = el('button', bar, 'g5-btn primary', '⬇'); b.setAttribute('aria-label', 'Drop in column ' + (col + 1));
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
        done: function (ok) { if (ok) { qhost.querySelector('.g5-q-tools') && null; draw(true); } },
        onNext: function () { var picking = scene.querySelector('.g5-grid-btns'); if (picking) { qhost.innerHTML = ''; el('p', qhost, 'g5-chip', 'Pick a column above!'); return; } turn = 1 - turn; round(); }, nextLabel: 'Continue →' });
    }
    round();
  }

  /* ---------- engine: card match ---------- */
  function playMatch() {
    var pool = state.deck.filter(function (p) { return p.kind === 'sa' && String(p.answer).length <= 18 && p.prompt.length <= 110 && !p.img && p.prompt.indexOf('\n') < 0; });
    var seen = {}, pairs = [];
    pool.forEach(function (p) { var k = g5.parseNum(p.answer); var key = k ? k.join('/') : String(p.answer).toLowerCase(); if (!seen[key] && pairs.length < 6) { seen[key] = 1; pairs.push(p); } });
    if (pairs.length < 4) { g5.errorBox(stage, 'This unit and level do not have enough short-answer questions for Puzzle Masters. Try another game.'); return; }
    var cards = [];
    pairs.forEach(function (p, i) { cards.push({ pair: i, text: p.prompt, kind: 'q', p: p }); cards.push({ pair: i, text: p.answer, kind: 'a', p: p }); });
    cards = g5.shuffle(cards);
    var open = [], matched = 0, tries = 0, turn = 0, pts = [0, 0];
    var hud = el('div', stage, 'g5-hud'), grid = el('div', stage, 'g5-grid-btns'), qhost = el('div', stage);
    grid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(10rem, 1fr))';
    function drawHud() {
      hud.innerHTML = ''; el('span', hud, 'g5-chip', 'Pairs found: ' + matched + ' / ' + pairs.length); el('span', hud, 'g5-chip', 'Flips: ' + tries);
      if (state.mode === 'pairs') [0, 1].forEach(function (t) { var c = el('span', hud, 'g5-team' + (t === turn ? ' g5-turn' : ''), 'Player ' + (t + 1) + ': ' + pts[t]); c.style.background = TEAM_COLORS[t]; });
    }
    cards.forEach(function (c, i) {
      var b = el('button', grid, 'g5-choice'); b.style.minHeight = '6rem'; b.style.justifyContent = 'center';
      b.setAttribute('aria-label', 'Card ' + (i + 1));
      el('span', b, 'g5-ct', c.kind === 'q' ? '❓ Problem' : '🔑 Answer');
      c.btn = b;
      b.onclick = function () {
        if (c.done || open.indexOf(c) >= 0 || open.length >= 2) return;
        open.push(c); b.innerHTML = ''; g5.math(el('span', b, 'g5-ct'), c.text); b.classList.add('on');
        if (open.length === 2) {
          tries++;
          var a = open[0], z = open[1];
          var ok = a.pair === z.pair && a.kind !== z.kind;
          setTimeout(function () {
            if (ok) { a.done = z.done = true; a.btn.classList.add('right'); z.btn.classList.add('right'); matched++; pts[turn]++; record(a.p, true); qhost.innerHTML = ''; var f = el('div', qhost, 'g5-feedback good', g5.pick(g5.PRAISE) + ' That is a match.'); }
            else {
              [a, z].forEach(function (x) { x.btn.classList.remove('on'); x.btn.innerHTML = ''; el('span', x.btn, 'g5-ct', x.kind === 'q' ? '❓ Problem' : '🔑 Answer'); });
              qhost.innerHTML = ''; el('div', qhost, 'g5-feedback try', 'Not a match yet. Remember where those cards are!');
              if (state.mode === 'pairs') turn = 1 - turn;
            }
            open = []; drawHud();
            if (matched === pairs.length) { qhost.innerHTML = ''; summary(qhost, state.mode === 'pairs' ? (pts[0] === pts[1] ? 'A tie! Great teamwork.' : 'Player ' + (pts[0] > pts[1] ? 1 : 2) + ' found the most pairs!') : 'Puzzle solved in ' + tries + ' flips!', '🧩'); }
          }, ok ? 300 : 1400);
        }
      };
    });
    drawHud();
  }

  /* ---------- engine: Fraction Frenzy (exactly constructed fraction models) ---------- */
  function fracModel(n, d, shape) {
    var s = '<svg class="g5-svg" viewBox="0 0 420 220" style="max-width:26rem;margin:auto" role="img" aria-label="Fraction model: ' + n + ' of ' + d + ' equal parts shaded">';
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
    var d = g5.pick(dens), n = 1 + Math.floor(Math.random() * (d - 1));
    var kind = level === 'cp2' ? 'name' : g5.pick(['name', 'equiv', 'simplest']);
    var gcd = function (a, b) { while (b) { var t = a % b; a = b; b = t; } return a; };
    var g = gcd(n, d), sn = n / g, sd = d / g;
    var good, bad = [], prompt;
    if (kind === 'name') { good = n + '/' + d; prompt = 'What fraction of the model is shaded?'; bad = [(d - n) + '/' + d, n + '/' + (d + 1), d + '/' + n]; }
    else if (kind === 'equiv') { var k = 2 + Math.floor(Math.random() * 2); good = n * k + '/' + d * k; prompt = 'Which fraction is equivalent to the shaded part?'; bad = [(n + k) + '/' + (d + k), n * k + '/' + d, (d - n) * k + '/' + d * k]; }
    else { if (g === 1) return frenzyQuestion(level); good = sn + '/' + sd; prompt = 'Which fraction in simplest form names the shaded part?'; bad = [n + '/' + (d * 2), sd + '/' + sn, (sd - sn || 1) + '/' + sd]; }
    var val = function (t) { var p = t.split('/'); return +p[0] / +p[1]; };
    bad = bad.filter(function (b, i, a) { return a.indexOf(b) === i && b !== good && Math.abs(val(b) - val(good)) > 1e-9 && +b.split('/')[1] > 0; });
    if (bad.length < 2) return frenzyQuestion(level);
    var opts = g5.shuffle(bad.slice(0, 3).map(function (t) { return { text: t, correct: false }; }).concat([{ text: good, correct: true }]));
    return { id: 'frenzy', skillId: 'frenzy', prompt: prompt, kind: 'mc', options: opts, answer: good, steps: ['Count the equal parts: ' + d + '. Count the shaded parts: ' + n + '.', 'The shaded part is ' + n + '/' + d + (g > 1 ? ' = ' + sn + '/' + sd : '') + '.'], svg: fracModel(n, d, Math.random() < 0.5 ? 'bar' : 'circle') };
  }
  function playFrenzy() {
    var round = 0, right = 0, total = 10;
    var hud = el('div', stage, 'g5-hud'), qhost = el('div', stage);
    function go() {
      hud.innerHTML = ''; el('span', hud, 'g5-chip', 'Round ' + Math.min(round + 1, total) + ' of ' + total); el('span', hud, 'g5-chip', '🍕 Correct: ' + right);
      if (round >= total) { qhost.innerHTML = ''; state.stats.frenzy = { right: right, tries: total }; state.info.skills.unshift({ id: 'frenzy', name: 'Fraction models' }); summary(qhost, 'Fraction Frenzy complete!', '🍕'); return; }
      var p = frenzyQuestion(state.level);
      var box = g5.card(qhost, p, { label: 'Fraction model', tries: state.mode === 'class' ? 1 : 2, teacher: state.teacher && state.mode === 'class',
        onAnswer: function (ok) { if (ok) right++; }, onNext: function () { round++; go(); } });
      var holder = D.createElement('div'); holder.innerHTML = p.svg; box.insertBefore(holder, box.children[2]);
    }
    go();
  }

  /* ---------- boot ---------- */
  function boot() {
    main = D.getElementById('app');
    var unitId = P.get('unit'), gameId = P.get('game') || 'math-quest', cfg = GAMES[gameId];
    if (!cfg) { g5.errorBox(main, 'Unknown game.'); return; }
    var info = g5.unitInfo(unitId);
    if (!info.unit) { g5.errorBox(main, 'Choose a ' + g5.COURSE_NAME + ' unit from Mr. K’s Classroom.'); return; }
    state.info = info;
    D.title = cfg.title + ' · ' + info.unit.name + ' · ' + g5.COURSE_NAME;
    g5.chrome(cfg.icon + ' ' + cfg.title, g5.COURSE_NAME + ' · Unit ' + info.number + ': ' + info.unit.name);
    var loading = el('div', main, 'g5-panel', 'Loading questions…');
    var bankP = cfg.engine === 'frenzy' && g5.COURSE === 'math5' ? Promise.resolve([]) : g5.load(unitId);
    bankP.then(function (qs) {
      loading.remove();
      function afterSkills(ids) {
        g5.setupPanel(main, { heading: cfg.icon + ' ' + cfg.title, intro: cfg.intro, modes: cfg.modes, startLabel: 'Play ▶',
          start: function (o) {
            state.level = o.level; state.mode = o.mode;
            state.deck = g5.shuffle(qs.filter(function (q) { return q.level === o.level && ids.indexOf(q.skillId) >= 0; }).map(g5.prepare));
            main.innerHTML = ''; stage = el('div', main, 'g5-stage');
            ({ path: playPath, builder: playBuilder, race: playRace, soccer: playSoccer, c4: playC4, match: playMatch, frenzy: playFrenzy })[cfg.engine](cfg);
          } });
      }
      if (cfg.engine === 'frenzy') afterSkills([]); else g5.chooseSkills(info, afterSkills);
    }).catch(function (e) { g5.errorBox(main, e.message); });
  }
  G.G5_GAMES = GAMES;
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
})(window);
