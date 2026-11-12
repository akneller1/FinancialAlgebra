/* Generated games for any unit that has Menu Assessment skills.
   A page sets <body data-unit="<skill set id>" data-game="flashcards|showdown|connect-four|tic-tac-toe|picture-reveal"
   data-title="..."> and loads this file after games/bank.js. Every question is a fresh, verified problem;
   every wrong choice was rejected by the verifier; typed answers are checked by the verifier. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, GB = G.MKGAMES, WS = G.MKWS, doc = G.document, body = doc.body;
  // A browser may restore an old flashcard document from its back/forward cache.
  // Reinitialize it rather than showing a previous lesson's in-memory deck.
  G.addEventListener('pageshow', function (event) {
    if (event.persisted) G.location.reload();
  });
  var UNIT = body.getAttribute('data-unit'), GAME = body.getAttribute('data-game'), SET = NS.skillSets[UNIT];
  var TITLE = body.getAttribute('data-title') || (SET ? SET.unitName : 'Game');
  var app = doc.getElementById('app');
  var M = G.MK_MATH_DISPLAY ? G.MK_MATH_DISPLAY.html : (typeof NS.mathSafe === 'function' ? NS.mathSafe : (WS.render && WS.render.math)), LETTERS = 'ABCD';
  if (!SET) { app.innerHTML = '<div class="gm-panel">This game is not available for this unit yet.</div>'; return; }

  /* ---------- helpers ---------- */
  function esc(s) { return String(s === undefined || s === null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var rng = WS.rng.make(WS.rng.hash(String(Date.now()) + Math.random()));
  var KEY = 'mk-game-' + GAME + '-' + (G.MK_GRADE_GAME_COURSE || UNIT) + '-' + UNIT;
  function load() { try { return JSON.parse(G.localStorage.getItem(KEY) || '{}') || {}; } catch (e) { return {}; } }
  function save(o) { try { G.localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) { /* private window: settings are not remembered */ } }
  var saved = load();
  if (G.MK_GRADE_GAME_COURSE && (!saved.level || !GB.LEVELS[saved.level])) saved.level = 'cp1';
  function $(s, r) { return (r || doc).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); }
  function on(sel, ev, fn) { $$(sel).forEach(function (e) { e.addEventListener(ev, fn); }); }
  // data-skills="a,b,c" limits a page to some of the unit's skills (e.g. Foundations uses the expression skills)
  var only = (body.getAttribute('data-skills') || '').split(',').map(function (x) { return x.trim(); }).filter(Boolean);
  var sourceCourseId = G.MK_COURSE_ACTIVITY_SOURCE && G.MK_COURSE_ACTIVITY_SOURCE.courseId;
  var nativeQuestionBank = body.hasAttribute('data-algebra2-game') || SET.authoredBank === true || sourceCourseId === 'algebra2';
  var bankBackedGame = nativeQuestionBank || !!G.MK_GRADE_GAME_COURSE;
  var skillIds = SET.skills.map(function (s) { return s.id; }).filter(function (id) { return !only.length || only.indexOf(id) >= 0; });
  // Legacy generated games need an actual game-compatible question. Native
  // bank courses use their own deck builder and format/level rules.
  if (!nativeQuestionBank) skillIds = skillIds.filter(function (id) { return GB.hasGameItems(UNIT, id); });
  var flashcardSkills = bankBackedGame ? skillIds.slice() : skillIds.filter(function (id) { return GB.hasFlashcardItems(UNIT, id); });
  var flashcardAvailability = {};
  function skillsWithCardsAt(level) {
    if (bankBackedGame) return skillIds.slice();
    if (!flashcardAvailability[level]) {
      flashcardAvailability[level] = skillIds.filter(function (id) { return GB.hasFlashcardItems(UNIT, id, level); });
    }
    return skillIds.filter(function (id) { return flashcardAvailability[level].indexOf(id) >= 0; });
  }
  if (GAME === 'flashcards') skillIds = flashcardSkills;
  var tags = Object.keys(SET.tags || {}).filter(function (t) { return skillIds.some(function (id) { return SET.byId[id].tag === t; }); });
  function skillName(id) { return SET.byId[id].name; }

  function qHtml(it, flashcardFront) {
    var q = it.q, prompt = flashcardFront && q.flashcardPrompt ? q.flashcardPrompt : q.prompt;
    var h = '<div class="gm-q">' + M(prompt || '');
    if (!flashcardFront && q.work && q.work.length) h += '<ol class="mm-work-lines">' + q.work.map(function (w, i) { return '<li><span>Line ' + (i + 1) + ':</span> ' + M('⟨' + w + '⟩') + '</li>'; }).join('') + '</ol>';
    if (q.fig) h += NS.figHtml(q.fig);
    if (q.ask) h += '<div class="gm-ask">' + (q.label ? '(' + esc(q.label) + ') ' : '') + M(q.ask) + '</div>';
    return h + '</div>';
  }
  function solHtml(it) {
    return '<div class="gm-sol"><h4>Answer</h4><div>' + M(it.answer) + '</div>' + (it.answerFigures||[]).map(function(fig){return NS.figHtml(fig);}).join('') +
      (it.steps.length ? '<h4 style="margin-top:10px">' + (it.vocabulary ? 'Example' : 'Worked solution') + '</h4><ol>' + it.steps.map(function (st) { return '<li>' + M(st.t || '') + (st.m ? ' ' + M('⟨' + st.m + '⟩') : '') + '</li>'; }).join('') + '</ol>' : '') + '</div>';
  }
  function optsHtml(it, st) {
    return '<div class="gm-opts" role="group" aria-label="Answer choices">' + it.options.map(function (o, i) {
      var cls = 'gm-opt' + (o.graph ? ' gm-graph-choice' : '') + (st.sel === i ? ' sel' : '') + ((st.dead || []).indexOf(i) >= 0 ? ' dead' : '') + (st.reveal && o.ok ? ' right' : '') + (st.reveal && st.sel === i && !o.ok ? ' wrong' : '');
      var dis = st.reveal || (st.dead || []).indexOf(i) >= 0;
      return '<button type="button" class="' + cls + '" data-opt="' + i + '"' + (dis ? ' disabled' : '') + '><span class="ltr">' + LETTERS[i] + '</span><span>' + (o.graph && NS.figHtml ? NS.figHtml(o.graph) : M(o.a)) + '</span></button>';
    }).join('') + '</div>';
  }
  function head(sub, pill) {
    return '<div class="gm-head"><div><div class="gm-eyebrow">Mr. K’s Classroom · ' + esc(SET.courseName || 'Algebra') + '</div><h1>' + esc(TITLE) + '</h1><p>' + sub + '</p></div>' + (pill ? '<span class="gm-pill">' + esc(pill) + '</span>' : '') + '</div>';
  }
  /* flashcards show the levels as Easy / Medium / Hard (CP2 / CP1 / Honors problems underneath) */
  var EASY_NAMES = { cp2: 'Easy', cp1: 'Medium', honors: 'Hard' };
  function levelSel(id, cur, names) {
    return '<select class="gm-sel" id="' + id + '">' + Object.keys(GB.LEVELS).map(function (k) { return '<option value="' + k + '"' + (k === cur ? ' selected' : '') + '>' + ((G.MK_GRADE_GAME_LABELS && G.MK_GRADE_GAME_LABELS[k]) || (names && names[k]) || GB.LEVELS[k].name) + '</option>'; }).join('') + '</select>';
  }
  function loading(msg) { app.innerHTML = '<div class="gm-panel gm-loading" role="status"><div><div class="gm-spin"></div>' + esc(msg || 'Cooking up fresh problems…') + '<div class="gm-muted" id="gmProg"></div></div></div>'; }
  function progress(i, n) { var e = $('#gmProg'); if (e) e.textContent = i + ' of ' + n; }
  function confetti() {
    var c = doc.createElement('div'); c.className = 'confetti'; var cols = ['#f2a33a', '#3456d1', '#e04848', '#1f7a4d', '#f2b705'];
    for (var k = 0; k < 70; k++) { var e = doc.createElement('i'); e.style.left = Math.random() * 100 + '%'; e.style.background = cols[k % 5]; e.style.animationDuration = (2 + Math.random() * 2) + 's'; e.style.animationDelay = Math.random() * 0.6 + 's'; c.appendChild(e); }
    body.appendChild(c); G.setTimeout(function () { c.remove(); }, 5200);
  }
  /* every skill at each of the level's three difficulties, shuffled */
  function levelSlots(level, skills, reps) {
    var out = [], tiers = GB.LEVELS[level].tiers;
    for (var r = 0; r < (reps || 1); r++) skills.forEach(function (s) { tiers.forEach(function (c) { out.push({ skill: s, c: c }); }); });
    return rng.shuffle(out);
  }
  function deck(slots, opts, done) { loading(opts && opts.msg); GB.buildDeck(UNIT, slots, Object.assign({ progress: progress }, opts || {}), function (items) {
    if (!items.length) { app.innerHTML = head('Choose skills and difficulty for this activity.', GAME) + '<div class="gm-panel" role="status">No questions are available for these skills and difficulty yet. <button class="gm-btn" onclick="location.reload()">Choose skills again</button></div>'; return; }
    done(items);
  }); }
  /* a drawing pile of verified items that refills itself */
  function Pile(level) { this.level = level; this.items = []; }
  Pile.prototype.fill = function (done) { var self = this; deck(levelSlots(this.level, skillIds), {}, function (its) { self.items = rng.shuffle(its); done(); }); };
  Pile.prototype.draw = function (done) { var self = this; if (this.items.length) return done(this.items.pop()); this.fill(function () { done(self.items.length ? self.items.pop() : null); }); };

  /* =========================== FLASHCARDS =========================== */
  function flashcards() {
    var vocabCards = G.MK_VOCAB_FLASHCARDS ? G.MK_VOCAB_FLASHCARDS.build(UNIT) : [];
    var S = { mode: vocabCards.length && ['mixed','skills','vocabulary'].indexOf(saved.mode)>=0 ? saved.mode : vocabCards.length?'mixed':'skills', level: saved.level || 'cp1', skill: 'all', cards: [], order: [], i: 0, flip: false, rate: saved.rate || {}, missed: false };
    GB._state = function () { return S; };
    function availableSkills() {
      var visible = skillsWithCardsAt(S.level);
      return skillIds.filter(function (id) { return visible.indexOf(id) >= 0; });
    }
    function build() {
      function ready(its){S.cards=rng.shuffle(its.concat(S.mode==='skills'?[]:vocabCards));S.rate={};S.i=0;S.flip=false;S.missed=false;refilter();persist();render();}
      if(S.mode==='vocabulary'){ready([]);return;}
      var activeSkills = availableSkills();
      if (!activeSkills.length) { if(vocabCards.length && S.mode!=='skills'){ready([]);return;} S.cards = []; S.rate = {}; S.i = 0; S.flip = false; S.missed = false; refilter(); persist(); render(); return; }
      deck(levelSlots(S.level, activeSkills, Math.max(1, Math.ceil(20 / (activeSkills.length * 3)))), { msg: 'Shuffling a fresh deck…' }, function (its) {
        ready(its);
      });
    }
    function persist() { save({ level: S.level, rate: S.rate, mode:S.mode }); }
    function refilter() {
      S.order = S.cards.map(function (_, k) { return k; }).filter(function (k) { var c = S.cards[k]; return (S.skill === 'all' || c.skill === S.skill) && (!S.missed || S.rate[c.id] === 'need'); });
      S.i = Math.min(S.i, Math.max(0, S.order.length - 1));
    }
    function cur() { return S.cards[S.order[S.i]]; }
    function render() {
      var c = cur(), got = 0, need = 0; Object.keys(S.rate).forEach(function (k) { if (S.rate[k] === 'got') got++; else need++; });
      var visibleSkills = S.mode==='vocabulary'?[]:availableSkills();
      var h = head('Flip each card for the answer and the worked solution. Practice your selected skills at this level.') +
        '<div class="gm-ctl">' + (vocabCards.length?'<label for="fcMode">Cards:</label><select class="gm-sel" id="fcMode">'+[['mixed','Skills + vocabulary'],['skills','Skill questions'],['vocabulary','Vocabulary only']].map(function(o){return '<option value="'+o[0]+'"'+(S.mode===o[0]?' selected':'')+'>'+o[1]+'</option>';}).join('')+'</select>':'') + '<label for="fcLevel">Level:</label>' + levelSel('fcLevel', S.level, EASY_NAMES) +
        '<label for="fcSkill">Skill:</label><select class="gm-sel" id="fcSkill"><option value="all">All skills</option>' + visibleSkills.map(function (id) { return '<option value="' + id + '"' + (S.skill === id ? ' selected' : '') + '>' + esc(skillName(id)) + '</option>'; }).join('') + (vocabCards.length&&S.mode==='mixed'?'<option value="__vocabulary"'+(S.skill==='__vocabulary'?' selected':'')+'>Vocabulary</option>':'') + '</select>' +
        '<button class="gm-btn" id="fcShuffle">Shuffle</button><button class="gm-btn" id="fcMissed"' + (need ? '' : ' disabled') + '>' + (S.missed ? 'All cards' : 'Practice missed') + '</button><button class="gm-btn" id="fcNew">New cards</button><button class="gm-btn" id="fcReset">Reset progress</button></div>' +
        '<div class="fc-stats"><span>' + (S.order.length ? 'Card ' + (S.i + 1) + ' of ' + S.order.length : 'No cards') + '</span><span>Got it: ' + got + ' • Need practice: ' + need + '</span></div>' +
        '<div class="gm-bar"><i style="width:' + (S.order.length ? (S.i + 1) / S.order.length * 100 : 0) + '%"></i></div>';
      if (!c) h += '<div class="gm-panel" role="status">' + (S.missed ? 'No missed cards here. Nice work!' : 'No cards for this choice.') + '</div>';
      else h += '<div class="gm-panel fc-card' + (S.flip ? ' back' : '') + '" id="fcCard" tabindex="0" role="button" aria-label="Flip card">' +
        '<div class="fc-top"><span class="gm-tag">' + esc(c.tagName) + ' · ' + esc(c.skillName) + '</span><span class="fc-side">' + (S.flip ? 'Answer side' : 'Question side') + '</span></div>' +
        (S.flip ? qHtml(c) + solHtml(c) : '<div class="gm-muted" style="font-weight:700;margin-top:10px;font-size:.85rem">PROBLEM</div>' + qHtml(c, true)) +
        '<div class="fc-foot">' + (S.flip ? 'How did it go? Rate the card below.' : 'Click the card or press Space to reveal the answer and the worked solution.') + '</div></div>';
      h += '<div class="fc-nav"><button class="gm-btn" id="fcPrev"' + (S.i > 0 ? '' : ' disabled') + '>← Previous</button>' +
        (S.flip ? '<span class="fc-rate gm-row"><button class="gm-btn need" id="fcNeed">Need practice</button><button class="gm-btn got" id="fcGot">Got it</button></span>' : '<button class="gm-btn primary" id="fcFlip"' + (c ? '' : ' disabled') + '>Reveal answer</button>') +
        '<button class="gm-btn" id="fcNext"' + (S.i < S.order.length - 1 ? '' : ' disabled') + '>Next →</button></div>' +
        '<div class="gm-note">Your progress is stored in this browser only. Keyboard: ←/→ to move, Space to flip, 1 = need practice, 2 = got it. “New cards” makes a brand-new deck at this level.</div>';
      app.innerHTML = h; wire();
    }
    function go(d) { S.i = Math.max(0, Math.min(S.order.length - 1, S.i + d)); S.flip = false; render(); }
    function rate(v) { var c = cur(); if (!c) return; S.rate[c.id] = v; persist(); if (S.missed && v === 'got') { refilter(); S.flip = false; render(); } else if (S.i < S.order.length - 1) go(1); else render(); }
    function wire() {
      if($('#fcMode'))$('#fcMode').onchange=function(){S.mode=this.value;S.skill='all';persist();build();};
      $('#fcLevel').onchange = function () { S.level = this.value; var nextSkills = skillsWithCardsAt(S.level); if (S.skill !== 'all' && nextSkills.indexOf(S.skill) < 0) S.skill = 'all'; persist(); build(); };
      $('#fcSkill').onchange = function () { S.skill = this.value; S.i = 0; S.flip = false; refilter(); render(); };
      $('#fcShuffle').onclick = function () { S.cards = rng.shuffle(S.cards); S.i = 0; S.flip = false; refilter(); render(); };
      $('#fcMissed').onclick = function () { S.missed = !S.missed; S.i = 0; S.flip = false; refilter(); render(); };
      $('#fcNew').onclick = build;
      $('#fcReset').onclick = function () { S.rate = {}; persist(); S.missed = false; refilter(); render(); };
      var card = $('#fcCard'); if (card) card.onclick = function () { S.flip = !S.flip; render(); };
      if ($('#fcFlip')) $('#fcFlip').onclick = function () { S.flip = true; render(); };
      $('#fcPrev').onclick = function () { go(-1); }; $('#fcNext').onclick = function () { go(1); };
      if ($('#fcNeed')) { $('#fcNeed').onclick = function () { rate('need'); }; $('#fcGot').onclick = function () { rate('got'); }; }
    }
    doc.addEventListener('keydown', function (e) {
      if (/INPUT|SELECT|TEXTAREA/.test((e.target || {}).tagName || '')) return;
      if (e.key === 'ArrowRight') go(1); else if (e.key === 'ArrowLeft') go(-1);
      else if (e.key === ' ') { e.preventDefault(); S.flip = !S.flip; render(); }
      else if (e.key === '1' && S.flip) rate('need'); else if (e.key === '2' && S.flip) rate('got');
    });
    build();
  }

  /* =========================== SHOWDOWN =========================== */
  function showdown() {
    body.classList.add('dark');
    var PRESETS = { cp1: [1, 2, 3, 4, 5] }; // Financial Algebra has one Standard level.
    var NAMES = G.MK_GRADE_GAME_COURSE ? { cp2:'Remedial',cp1:'Standard',honors:'Advanced',mixed:'Mixed (Remedial → Advanced)' } : { cp2: 'CP2', cp1: 'CP1', honors: 'Honors', mixed: 'Mixed (100 easy → 500 Honors)' };
    if (G.MK_GRADE_GAME_COURSE) { PRESETS = {cp2:[1,1,1,2,2],cp1:[2,2,3,3,3],honors:[3,3,4,4,4],mixed:[1,2,2,3,4]}; }
    NAMES = {cp1:'Standard'};
    var S = { preset: saved.preset || 'cp1', teams: saved.teams || ['Team 1', 'Team 2'], score: [], cells: {}, open: null, showOpts: false, showAns: false };
    GB._state = function () { return S; };
    /* one category per skill group; a unit with fewer than three groups gets one category per skill instead */
    var cols = (tags.length >= 3 ? tags.map(function (t) { return { name: SET.tags[t], skills: skillIds.filter(function (id) { return SET.byId[id].tag === t; }) }; })
      : skillIds.map(function (id) { return { name: SET.byId[id].name, skills: [id] }; })), VALUES = [100, 200, 300, 400, 500];
    function build() {
      if (!cols.length) { app.innerHTML = head('Practice questions are not available for this unit yet.', 'Showdown') + '<div class="gm-panel" role="status">No questions are available for this unit yet.</div>'; return; }
      var slots = [];
      cols.forEach(function (t, ci) {
        var sk = rng.shuffle(t.skills.slice());
        VALUES.forEach(function (v, ri) { slots.push({ skill: sk[ri % sk.length], c: PRESETS[S.preset][ri], level: SET.authoredBank ? S.preset : undefined, col: ci, row: ri }); });
      });
      deck(slots, { msg: 'Setting up the board…', wholeProblem: true }, function (its) {
        S.cells = {}; its.forEach(function (it) { S.cells[it.slot.col + ',' + it.slot.row] = { it: it, used: false }; });
        S.score = S.teams.map(function () { return 0; }); S.open = null; render();
      });
    }
    function render() {
      if (S.open) return renderQ();
      var h = '<h1 class="sd-title">' + esc(TITLE).replace(/Showdown/, '<b>Showdown</b>') + '</h1><p class="sd-sub">' + esc(SET.unitName) + ' review · pick a category and a value</p>' +
        '<div class="gm-ctl"><label for="sdPreset">Board:</label><select class="gm-sel" id="sdPreset">' + Object.keys(PRESETS).map(function (k) { return '<option value="' + k + '"' + (k === S.preset ? ' selected' : '') + '>' + NAMES[k] + '</option>'; }).join('') + '</select>' +
        '<button class="gm-btn" id="sdNew">New board</button><button class="gm-btn" id="sdAddT"' + (S.teams.length >= 8 ? ' disabled' : '') + '>Add team</button><button class="gm-btn" id="sdRemT"' + (S.teams.length <= 1 ? ' disabled' : '') + '>Remove team</button></div>' +
        '<div style="overflow-x:auto"><div class="sd-board" style="grid-template-columns:repeat(' + cols.length + ',minmax(130px,1fr))">' + cols.map(function (t) { return '<div class="sd-cat">' + esc(t.name) + '</div>'; }).join('');
      VALUES.forEach(function (v, ri) { cols.forEach(function (t, ci) {
        var cell = S.cells[ci + ',' + ri];
        h += cell ? '<button class="sd-cell" data-cell="' + ci + ',' + ri + '"' + (cell.used ? ' disabled aria-label="used"' : ' aria-label="' + esc(t.name) + ' for ' + v + '"') + '>' + (cell.used ? '' : v) + '</button>' : '<span class="sd-cell empty" aria-hidden="true"></span>';
      }); });
      h += '</div></div>' + (Object.keys(S.cells).length<cols.length*VALUES.length?'<p class="gm-muted" role="status">Some categories have fewer questions at this difficulty. Only available point values are shown; choose another difficulty for more questions.</p>':'') + teamsHtml() + '<p class="sd-foot">Click a value to open the problem. Press <b>Space</b> to show the answer and solution, <b>Esc</b> to return to the board.</p>';
      app.innerHTML = h;
      $('#sdPreset').onchange = function () { S.preset = this.value; persist(); build(); };
      $('#sdNew').onclick = build;
      $('#sdAddT').onclick = function () { S.teams.push('Team ' + (S.teams.length + 1)); S.score.push(0); persist(); render(); };
      $('#sdRemT').onclick = function () { S.teams.pop(); S.score.pop(); persist(); render(); };
      on('.sd-cell[data-cell]', 'click', function () { var c = S.cells[this.getAttribute('data-cell')]; c.used = true; S.open = c; S.showAns = false; S.showOpts = false; render(); });
      wireTeams();
    }
    function teamsHtml() { return '<div class="sd-teams">' + S.teams.map(function (n, i) { return '<div class="sd-team"><input aria-label="Team name" data-tn="' + i + '" value="' + esc(n) + '"><div class="pts">' + (S.score[i] || 0) + '</div></div>'; }).join('') + '</div>'; }
    function wireTeams() { on('[data-tn]', 'change', function () { S.teams[+this.getAttribute('data-tn')] = this.value || 'Team'; persist(); }); }
    function persist() { save({ preset: S.preset, teams: S.teams }); }
    function renderQ() {
      var it = S.open.it, v = VALUES[it.slot.row];
      var h = '<div class="sd-q"><div class="gm-row"><span class="sd-val">' + esc(cols[it.slot.col].name) + ' · ' + v + '</span><span class="gm-sp"></span><button class="gm-btn" id="sdBack">Back to board (Esc)</button></div>' + qHtml(it) +
        (S.showOpts ? optsHtml(it, { reveal: S.showAns }) : '') +
        '<div class="gm-row" style="margin-top:14px">' + (S.showOpts || !it.options.length ? '' : '<button class="gm-btn" id="sdOpts">Show choices</button>') + (S.showAns ? '' : '<button class="gm-btn primary" id="sdAns">Show answer (Space)</button>') + '</div>' +
        (S.showAns ? solHtml(it) + '<div class="gm-row"><b>Award:</b>' + S.teams.map(function (n, i) { return '<button class="gm-btn" data-aw="' + i + '" data-s="1">+' + v + ' ' + esc(n) + '</button><button class="gm-btn" data-aw="' + i + '" data-s="-1">−' + v + '</button>'; }).join('') + '</div>' : '') + '</div>' + teamsHtml();
      app.innerHTML = h;
      $('#sdBack').onclick = back;
      if ($('#sdOpts')) $('#sdOpts').onclick = function () { S.showOpts = true; render(); };
      if ($('#sdAns')) $('#sdAns').onclick = function () { S.showAns = true; render(); };
      on('[data-aw]', 'click', function () { S.score[+this.getAttribute('data-aw')] += v * +this.getAttribute('data-s'); render(); });
      wireTeams();
    }
    function back() { S.open = null; render(); }
    doc.addEventListener('keydown', function (e) {
      if (!S.open || /INPUT|SELECT/.test((e.target || {}).tagName || '')) return;
      if (e.key === 'Escape') back(); else if (e.key === ' ') { e.preventDefault(); S.showAns = true; render(); }
    });
    build();
  }

  /* =========================== two-team games =========================== */
  function teamSetup(game, intro, rules, start) {
    var nm = saved.names || ['Left side', 'Right side'];
    app.innerHTML = head(intro, game) + '<div class="gm-panel gm-setup"><h2 style="margin-top:0">Set up the game</h2>' +
      '<label for="tA">First team</label><input type="text" id="tA" value="' + esc(nm[0]) + '"><label for="tB">Second team</label><input type="text" id="tB" value="' + esc(nm[1]) + '">' +
      '<div class="gm-row" style="margin-top:12px"><div><label for="tLevel">Level</label>' + levelSel('tLevel', saved.level || 'cp1') + '</div><div><label for="tTimer">Timer per question</label><select class="gm-sel" id="tTimer">' +
      [0, 60, 90, 120, 180].map(function (s) { return '<option value="' + s + '"' + (String(saved.timer || 0) === String(s) ? ' selected' : '') + '>' + (s ? s + ' seconds' : 'Off') + '</option>'; }).join('') + '</select></div></div>' +
      '<ol class="gm-rules">' + rules.map(function (r) { return '<li>' + r + '</li>'; }).join('') + '</ol><button class="gm-btn primary" id="tGo">Start the game</button></div>';
    $('#tGo').onclick = function () {
      var o = { names: [$('#tA').value || 'Left side', $('#tB').value || 'Right side'], level: $('#tLevel').value, timer: +$('#tTimer').value };
      save(o); saved = o; start(o);
    };
  }
  function Timer(sec, tick, end) { this.sec = sec; this.tick = tick; this.end = end; this.h = null; }
  Timer.prototype.start = function () { var self = this; this.stop(); if (!this.sec) return; var t0 = Date.now(); this.h = G.setInterval(function () { var left = self.sec - (Date.now() - t0) / 1000; self.tick(Math.max(0, left)); if (left <= 0) { self.stop(); self.end(); } }, 200); };
  Timer.prototype.stop = function () { if (this.h) G.clearInterval(this.h); this.h = null; };
  function sidesHtml(cfg, turn, wins, extra) {
    return '<div class="tm-sides">' + ['L', 'R'].map(function (s, i) {
      return '<div class="tm-side ' + s + (turn === s ? ' on' : '') + '"><span class="tm-dot">' + esc(cfg.names[i].charAt(0).toUpperCase()) + '</span><div><div class="tm-name">' + esc(cfg.names[i]) + '</div><div class="tm-wins">Wins <b>' + wins[s] + '</b>' + (turn === s ? ' · <b>' + (extra || 'Answering') + '</b>' : '') + '</div></div></div>';
    }).join('') + '</div>';
  }
  function other(s) { return s === 'L' ? 'R' : 'L'; }
  function nameOf(cfg, s) { return cfg.names[s === 'L' ? 0 : 1]; }
  function timerHtml(sec) { return sec ? '<div class="tm-timer"><div class="gm-bar"><i id="tmBar" style="width:100%"></i></div><span id="tmSec">' + sec + 's</span></div>' : ''; }
  function tickUI(sec) { return function (left) { var b = $('#tmBar'), s = $('#tmSec'); if (b) b.style.width = (left / sec * 100) + '%'; if (s) s.textContent = Math.ceil(left) + 's'; }; }

  /* =========================== CONNECT FOUR =========================== */
  function connectFour() {
    teamSetup('Connect 4', 'Answer a problem to earn a disc. Connect four in a row to win.', [
      'Teams take turns. Talk the problem over, then lock in one answer.',
      'A wrong answer or timeout offers the other team a steal on the same problem, with the wrong choice crossed out.',
      'A correct steal earns a disc; the team that missed goes next. Pass or miss the steal and play moves to the other team.',
      'First team to connect four discs across, down or diagonally wins.'], play);
    function play(cfg) {
      var pile = new Pile(cfg.level), S = { board: [], turn: 'L', answerer: 'L', starter: 'L', wins: { L: 0, R: 0 }, phase: 'q', it: null, sel: null, dead: [], win: null, stolen: false };
      GB._state = function () { return S; };
      var timer = new Timer(cfg.timer, tickUI(cfg.timer), function () { answer(true); });
      function reset() { S.board = Array.from({length:6},function(){return Array(7).fill(null);});S.win=null;S.turn=S.starter;next(); }
      function next() { S.phase='q';S.answerer=S.turn;S.sel=null;S.dead=[];S.stolen=false;S.timeout=false;pile.draw(function(it){
        if(!it){app.innerHTML=head('No questions available for the selected skills and level.','Connect 4')+'<div class="gm-panel" role="alert"><button class="gm-btn" onclick="location.reload()">Choose skills again</button></div>';return;}
        S.it=it;render();timer.start();
      }); }
      function answer(timeout) {
        if(!['q','steal'].includes(S.phase)||(!timeout&&S.sel===null))return;
        timer.stop();var ok=!timeout&&S.it.options[S.sel].ok;
        if(ok){S.stolen=S.phase==='steal';S.phase='drop';}
        else if(S.phase==='q'){if(!timeout)S.dead.push(S.sel);S.sel=null;S.phase='steal-offer';S.timeout=!!timeout;}
        else{if(!timeout)S.dead.push(S.sel);S.phase='miss';S.timeout=!!timeout;}
        render();
      }
      function steal(){if(S.phase!=='steal-offer')return;S.answerer=other(S.turn);S.phase='steal';S.sel=null;render();timer.start();}
      function pass(){if(S.phase!=='steal-offer')return;S.phase='miss';S.passed=true;render();}
      function drop(col) {
        if(S.phase!=='drop')return;
        for(var r=5;r>=0;r--)if(!S.board[r][col]){S.board[r][col]=S.answerer;break;}if(r<0)return;
        S.win=winLine();if(S.win){S.wins[S.answerer]++;S.phase='over';S.starter=other(S.starter);render();confetti();return;}
        if(S.board[0].every(Boolean)){S.phase='over';S.starter=other(S.starter);render();return;}
        S.phase='resolved';render();
      }
      function advance(){S.turn=S.stolen?S.turn:other(S.turn);S.passed=false;next();}
      function winLine(){var D=[[0,1],[1,0],[1,1],[1,-1]];for(var r=0;r<6;r++)for(var c=0;c<7;c++){var t=S.board[r][c];if(!t)continue;for(var d=0;d<4;d++){var cells=[[r,c]];for(var k=1;k<4;k++){var rr=r+D[d][0]*k,cc=c+D[d][1]*k;if(rr<0||rr>5||cc<0||cc>6||S.board[rr][cc]!==t)break;cells.push([rr,cc]);}if(cells.length===4)return cells;}}return null;}
      function render(){
        var it=S.it,live=S.phase==='q'||S.phase==='steal',who=S.phase==='steal-offer'?other(S.turn):S.answerer;
        var h=head('Answer a problem to earn a disc. Connect four in a row to win.','Connect 4')+sidesHtml(cfg,S.phase==='over'?null:who,S.wins,S.phase==='steal-offer'?'Steal?':S.phase==='steal'?'Stealing':S.phase==='drop'?'Dropping a disc':'Answering');
        h+='<div class="tm-main"><div class="gm-panel">';
        if(S.phase==='over')h+='<h2>'+(S.win?esc(nameOf(cfg,S.answerer))+' wins!':'The board is full: a tie!')+'</h2>'+solHtml(it)+'<button class="gm-btn primary" id="c4Again">Play again</button>';
        else{
          h+='<div class="gm-row"><span class="tm-who '+who+'"><i></i>'+esc(nameOf(cfg,who))+'</span><span class="gm-sp"></span><span class="gm-tag">'+esc(it.tagName)+'</span></div>'+(live?timerHtml(cfg.timer):'')+qHtml(it)+optsHtml(it,{sel:S.sel,dead:S.dead,reveal:['drop','miss','resolved'].includes(S.phase)});
          if(live)h+='<div class="gm-row"><button class="gm-btn primary" id="c4Lock"'+(S.sel===null?' disabled':'')+'>Lock in answer</button>'+(S.phase==='q'?'<button class="gm-btn" id="c4Skip">Skip this problem</button>':'')+'</div>';
          if(S.phase==='steal-offer')h+='<div class="gm-msg">'+(S.timeout?'Time is up.':'Not quite.')+' '+esc(nameOf(cfg,other(S.turn)))+' can steal this problem.</div><div class="gm-row"><button class="gm-btn primary" id="c4Steal">Steal it</button><button class="gm-btn" id="c4Pass">Pass</button></div>';
          if(S.phase==='steal')h+='<p class="gm-msg">Steal attempt: the previous wrong choice is crossed out.</p>';
          if(S.phase==='drop')h+='<div class="gm-msg good">'+(S.stolen?'Steal successful!':'Correct!')+' Choose a column to drop your disc.</div>';
          if(S.phase==='miss'||S.phase==='resolved')h+='<div class="gm-msg">'+(S.phase==='resolved'?'Disc placed.':S.passed?'Steal passed. No disc this turn.':'The steal missed. No disc this turn.')+' Next up: '+esc(nameOf(cfg,S.stolen?S.turn:other(S.turn)))+'.</div>'+solHtml(it)+'<button class="gm-btn primary" id="c4Next">Next turn →</button>';
        }
        h+='</div><div><div class="c4-cols">'+[1,2,3,4,5,6,7].map(function(n){return '<span>'+n+'</span>';}).join('')+'</div><div class="c4-board'+(S.phase==='drop'?' pick':'')+'">';
        for(var r=0;r<6;r++)for(var c=0;c<7;c++){var t=S.board[r][c],w=S.win&&S.win.some(function(x){return x[0]===r&&x[1]===c;});h+='<button class="c4-hole'+(t?' '+t:'')+(w?' win':'')+'" data-col="'+c+'" aria-label="Column '+(c+1)+'"'+(S.phase==='drop'&&!S.board[0][c]?'':' disabled')+'></button>';}
        h+='</div></div></div>';app.innerHTML=h;
        on('[data-opt]','click',function(){if(live&&S.dead.indexOf(+this.dataset.opt)<0){S.sel=+this.dataset.opt;render();}});
        if($('#c4Lock'))$('#c4Lock').onclick=function(){answer(false);};if($('#c4Steal'))$('#c4Steal').onclick=steal;if($('#c4Pass'))$('#c4Pass').onclick=pass;
        if($('#c4Skip'))$('#c4Skip').onclick=function(){timer.stop();next();};if($('#c4Next'))$('#c4Next').onclick=advance;if($('#c4Again'))$('#c4Again').onclick=reset;
        on('.c4-hole','click',function(){drop(+this.dataset.col);});
      }
      loading();pile.fill(reset);
    }
  }

  /* =========================== TIC-TAC-TOE =========================== */
  function ticTacToe() {
    teamSetup('Tic-Tac-Toe', 'Two teams, one board, nine squares. Earn a square by answering a problem.', [
      'Teams take turns. On your turn, pick an open square and answer the problem that appears.',
      'Correct: your team marks the square. Wrong or out of time: the other team can <b>steal</b> the square by answering the same problem (the wrong choice is crossed out).',
      'If nobody gets it, the square stays open. Either way, the next team picks next.',
      'Three in a row (across, down or diagonal) wins. Show your work on paper!'], play);
    function play(cfg) {
      var pile = new Pile(cfg.level), LINES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
      var S = { b: Array(9).fill(null), turn: 'L', starter: 'L', wins: { L: 0, R: 0 }, quiz: null, over: false, line: null };
    GB._state = function () { return S; };
      var timer = new Timer(cfg.timer, tickUI(cfg.timer), function () { submit(true); });
      var MARK = { L: '✕', R: '◯' };
      function reset() { S.b = Array(9).fill(null); S.quiz = null; S.over = false; S.line = null; S.turn = S.starter; render(); }
      function pick(i) {
        if (S.over || S.b[i] || S.quiz || S.loadingQuestion) return;
        S.loadingQuestion = true;
        // Give immediate visual feedback even if the question pile must refill.
        var status = doc.createElement('div');
        status.className = 'gm-modal';
        status.setAttribute('role','status');
        status.innerHTML = '<div class="gm-panel gm-loading">Loading question…</div>';
        app.appendChild(status);
        function fail(message) {
          S.loadingQuestion = false;
          app.innerHTML = head('Could not open the question.', 'Tic-Tac-Toe') +
            '<div class="gm-panel" role="alert"><h2>Question unavailable</h2><p>' +
            esc(message || 'The selected skill did not generate a verified question.') +
            '</p><button class="gm-btn primary" id="tBack">Return to game setup</button></div>';
          $('#tBack').onclick = function () { G.location.reload(); };
        }
        try {
          pile.draw(function (it) {
            S.loadingQuestion = false;
            if (!it || !it.q || !it.options || !it.options.length) {
              fail('No verified game question was generated at this level.');
              return;
            }
            try {
              S.quiz = { sq:i, it:it, who:S.turn, stage:'ans', sel:null, dead:[] };
              render();
              timer.start();
            } catch (err) {
              S.quiz = null;
              fail('The question could not be displayed: ' + (err && err.message || String(err)));
            }
          });
        } catch (err) {
          fail('The question generator failed: ' + (err && err.message || String(err)));
        }
      }
      function pickError() { app.innerHTML = head('No verified questions are currently available for this selected skill.', 'Tic-Tac-Toe') + '<div class="gm-panel" role="alert"><h2>Questions could not be generated</h2><p>Try another skill or level from the game setup. This topic is not currently producing verified game questions.</p><button class="gm-btn" id="tReload">Return to setup</button></div>'; $('#tReload').onclick = function () { G.location.reload(); }; }
      function submit(timeout) {
        var q = S.quiz; if (!q || q.stage === 'result') return; if (!timeout && q.sel === null) return;
        timer.stop(); var ok = !timeout && q.it.options[q.sel].ok;
        if (ok) { S.b[q.sq] = q.who; q.stage = 'result'; q.ok = true; }
        else if (q.stage === 'ans' && q.it.options.length > 2) { if (q.sel !== null) q.dead.push(q.sel); q.sel = null; q.stage = 'steal'; q.who = other(q.who); q.first = timeout ? 'Time is up!' : 'That answer is not correct.'; render(); timer.start(); return; }
        else { q.stage = 'result'; q.ok = false; }
        render();
      }
      function after() {
        S.quiz = null; S.turn = other(S.turn);
        for (var k = 0; k < LINES.length; k++) { var l = LINES[k]; if (S.b[l[0]] && S.b[l[0]] === S.b[l[1]] && S.b[l[0]] === S.b[l[2]]) { S.line = l; S.over = S.b[l[0]]; } }
        if (S.over) { S.wins[S.over]++; S.starter = other(S.starter); render(); confetti(); return; }
        if (S.b.every(Boolean)) { S.over = 'tie'; S.starter = other(S.starter); }
        render();
      }
      function render() {
        var h = head('Two teams, one board, nine squares. Earn each square by answering a problem.', 'Tic-Tac-Toe') + sidesHtml(cfg, S.over ? null : S.turn, S.wins, 'Picking a square') +
          '<div class="gm-panel"><div style="text-align:center;font-weight:800;font-size:1.15rem;margin-bottom:12px">' +
          (S.over ? (S.over === 'tie' ? 'Cat’s game: a tie!' : esc(nameOf(cfg, S.over)) + ' wins!') + ' <button class="gm-btn primary" id="tAgain">Play again</button>' : esc(nameOf(cfg, S.turn)) + ': pick a square') + '</div><div class="ttt-board">' +
          S.b.map(function (v, i) { return '<button class="ttt-sq' + (v ? ' ' + v : '') + (S.line && S.line.indexOf(i) >= 0 ? ' win' : '') + '" data-sq="' + i + '"' + (v || S.over ? ' disabled' : '') + ' aria-label="Square ' + (i + 1) + (v ? ', ' + nameOf(cfg, v) : '') + '">' + (v ? MARK[v] : '') + '</button>'; }).join('') + '</div></div>';
        var q = S.quiz;
        if (q) {
          h += '<div class="gm-modal" role="dialog" aria-modal="true"><div class="gm-panel ' + (q.stage === 'result' ? (q.ok ? q.who : '') : q.who) + '"><div class="gm-row"><span class="tm-who ' + q.who + '"><i></i>' + esc(nameOf(cfg, q.who)) + '</span>' + (q.stage === 'steal' ? '<span class="gm-steal">Steal!</span>' : '') + '<span class="gm-sp"></span><span class="gm-tag">' + esc(q.it.tagName) + '</span></div>' +
            (q.stage === 'steal' ? '<div class="gm-msg bad">' + esc(q.first) + ' ' + esc(nameOf(cfg, q.who)) + ' can steal the square.</div>' : '') + (q.stage !== 'result' ? timerHtml(cfg.timer) : '') + qHtml(q.it) +
            optsHtml(q.it, { sel: q.sel, dead: q.dead, reveal: q.stage === 'result' });
          if (q.stage !== 'result') h += '<div class="gm-row" style="margin-top:12px"><button class="gm-btn primary" id="tLock"' + (q.sel === null ? ' disabled' : '') + '>Lock in answer</button></div>';
          else h += '<div class="gm-msg ' + (q.ok ? 'good">Correct! ' + esc(nameOf(cfg, q.who)) + ' takes the square.' : 'bad">Nobody got it. The square stays open.') + '</div>' + solHtml(q.it) + '<button class="gm-btn primary" id="tCont">Continue</button>';
          h += '</div></div>';
        }
        app.innerHTML = h;
        on('[data-sq]', 'click', function () { pick(+this.getAttribute('data-sq')); });
        on('[data-opt]', 'click', function () { if (S.quiz && S.quiz.stage !== 'result') { S.quiz.sel = +this.getAttribute('data-opt'); render(); } });
        if ($('#tLock')) $('#tLock').onclick = function () { submit(false); };
        if ($('#tCont')) $('#tCont').onclick = after;
        if ($('#tAgain')) $('#tAgain').onclick = reset;
      }
      loading(); pile.fill(function () { if (!pile.items.length) { pickError(); return; } reset(); });
    }
  }

  /* =========================== PICTURE REVEAL =========================== */
  var ART = [
    function () { return '<svg class="art" viewBox="0 0 500 300" aria-hidden="true"><defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff9a62"/><stop offset=".55" stop-color="#ffd27a"/><stop offset="1" stop-color="#ffe9b8"/></linearGradient></defs><rect width="500" height="300" fill="url(#sky)"/><circle cx="330" cy="150" r="52" fill="#fff3c4"/><path d="M0 200 L90 110 L160 175 L240 90 L330 185 L410 120 L500 190 V300 H0Z" fill="#6c5b9b"/><path d="M0 230 L120 160 L210 225 L300 150 L400 225 L500 170 V300 H0Z" fill="#45407a"/><rect y="240" width="500" height="60" fill="#3b7ea8"/><path d="M0 250 H500 M40 265 H200 M260 262 H460 M90 282 H330" stroke="#a9d6ef" stroke-width="3" opacity=".7"/><path d="M240 90 l-18 18 l10 -2 l8 10 l8 -10 l10 2z" fill="#fff"/></svg>'; },
    function () { var stars = ''; for (var i = 0; i < 60; i++) stars += '<circle cx="' + (i * 83 % 500) + '" cy="' + (i * 47 % 300) + '" r="' + (1 + i % 3 * 0.6) + '" fill="#fff" opacity=".8"/>';
      return '<svg class="art" viewBox="0 0 500 300" aria-hidden="true"><rect width="500" height="300" fill="#121a3d"/>' + stars + '<circle cx="110" cy="260" r="120" fill="#4c7bd9"/><path d="M20 230 q60 -30 120 0 q50 25 90 -5" stroke="#8fd16f" stroke-width="18" fill="none" opacity=".8"/><circle cx="400" cy="70" r="34" fill="#e9c46a"/><ellipse cx="400" cy="70" rx="60" ry="12" fill="none" stroke="#f4a261" stroke-width="5"/>' +
        '<g transform="translate(270 150) rotate(35)"><path d="M0 -70 C25 -40 25 20 18 45 H-18 C-25 20 -25 -40 0 -70Z" fill="#eef1f7"/><circle cy="-20" r="11" fill="#4cc9f0" stroke="#264653" stroke-width="4"/><path d="M-18 25 L-36 55 L-18 45Z M18 25 L36 55 L18 45Z" fill="#e63946"/><path d="M-12 47 Q0 95 12 47Z" fill="#ffb703"/></g></svg>'; },
    function () { return '<svg class="art" viewBox="0 0 500 300" aria-hidden="true"><rect width="500" height="300" fill="#bfe6ff"/><circle cx="80" cy="60" r="34" fill="#fff6b0"/><path d="M0 250 Q120 200 250 240 T500 230 V300 H0Z" fill="#7cc36a"/><path d="M0 270 Q150 240 300 268 T500 262 V300 H0Z" fill="#4fa457"/>' +
        [[150, 110, '#e76f51', '#f4a261'], [300, 80, '#2a9d8f', '#e9c46a'], [410, 140, '#8e5cc4', '#f28482']].map(function (b) { return '<g transform="translate(' + b[0] + ' ' + b[1] + ')"><path d="M0 -50 C38 -50 48 -12 30 18 L12 40 H-12 L-30 18 C-48 -12 -38 -50 0 -50Z" fill="' + b[2] + '"/><path d="M0 -50 C12 -50 16 -12 10 18 L5 40 H-5 L-10 18 C-16 -12 -12 -50 0 -50Z" fill="' + b[3] + '"/><path d="M-12 40 L-9 55 M12 40 L9 55" stroke="#5b4636" stroke-width="2"/><rect x="-10" y="55" width="20" height="14" rx="3" fill="#8d6748"/></g>'; }).join('') +
        '<path d="M330 40 q15 -14 30 0 q15 -14 30 0" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round"/></svg>'; }
  ];
  function pictureReveal() {
    var S = { level: saved.level || 'cp1', items: [], i: 0, st: [], art: 0 };
    GB._state = function () { return S; };
    function build() {
      var sk = rng.shuffle(skillIds), tiers = GB.LEVELS[S.level].tiers, slots = [];
      for (var k = 0; k < 10; k++) slots.push({ skill: sk[k % sk.length], c: tiers[Math.floor(k * 3 / 10)] });
      deck(slots, { msg: 'Hiding a new picture…', preferTyped: true }, function (its) {
        S.items = its; S.i = 0; S.st = its.map(function () { return { done: false, sel: null, val: '', msg: '', tries: 0, sol: false }; }); S.art = rng.int(0, ART.length - 1); render();
      });
    }
    function render() {
      var it = S.items[S.i], st = S.st[S.i], done = S.st.filter(function (x) { return x.done; }).length, n = S.items.length;
      if (!n) { app.innerHTML = head('Practice questions are not available for this unit yet.', 'Picture Reveal') + '<div class="gm-panel" role="status">No questions are available for this unit yet.</div>'; return; }
      var h = head('Solve ' + n + ' problems. Every correct answer uncovers part of a mystery picture.', 'Picture Reveal') + '<div class="pr-main"><div class="gm-panel">' +
        '<div class="gm-row"><h2 style="margin:0;font-size:1.2rem">Question ' + (S.i + 1) + ' of ' + n + '</h2><span class="gm-sp"></span><span style="color:var(--green);font-weight:800">' + done + ' / ' + n + ' revealed</span></div>' +
        '<div class="gm-bar"><i style="width:' + (done / Math.max(1, n) * 100) + '%"></i></div><div class="pr-nums">' + S.items.map(function (_, k) { return '<button class="pr-num' + (k === S.i ? ' on' : '') + (S.st[k].done ? ' done' : '') + '" data-q="' + k + '" aria-label="Question ' + (k + 1) + (S.st[k].done ? ', solved' : '') + '">' + (k + 1) + '</button>'; }).join('') + '</div>';
      if (it) {
        h += '<div class="gm-qbox"><div class="gm-tag">' + esc(it.skillName) + '</div>' + qHtml(it) + '</div>';
        if (it.typed) h += '<label for="prIn" style="font-weight:700">Your answer</label><input class="gm-input" id="prIn" autocomplete="off" value="' + esc(st.val) + '"' + (st.done ? ' disabled' : '') + '><p class="gm-hint">' + esc(GB.HINTS[it.typed]) + '</p>';
        else h += optsHtml(it, { sel: st.sel, reveal: st.done });
        h += '<div class="gm-msg ' + (st.done ? 'good' : 'bad') + '" role="status">' + esc(st.msg) + '</div>' +
          '<div class="gm-row" style="margin-top:10px"><button class="gm-btn primary" id="prCheck"' + (st.done ? ' disabled' : '') + '>Check answer</button><button class="gm-btn" id="prSol">' + (st.sol ? 'Hide' : 'Show') + ' worked solution</button></div>' + (st.sol ? solHtml(it) : '');
      }
      h += '<div class="gm-row" style="margin-top:18px"><button class="gm-btn" id="prPrev"' + (S.i > 0 ? '' : ' disabled') + '>← Previous</button><button class="gm-btn" id="prNext"' + (S.i < n - 1 ? '' : ' disabled') + '>Next →</button><span class="gm-sp"></span>' + levelSel('prLevel', S.level) + '<button class="gm-btn" id="prNew">New game</button></div></div>' +
        '<div class="gm-panel"><div class="gm-row"><h2 style="margin:0;font-size:1.2rem">Mystery Picture</h2><span class="gm-sp"></span><span class="gm-pill">' + n + ' pieces</span></div><div class="pr-pic" style="margin-top:12px">' + ART[S.art]() + '<div class="pr-tiles" style="grid-template-columns:repeat(' + (n === 10 ? 5 : n) + ',1fr);grid-template-rows:repeat(' + (n === 10 ? 2 : 1) + ',1fr)">' +
        S.items.map(function (_, k) { return '<div class="pr-tile' + (S.st[k].done ? ' gone' : '') + '">' + (S.st[k].done ? '' : '?') + '</div>'; }).join('') + '</div></div><p class="gm-muted">Each correct answer uncovers one piece of the picture. Solve all ' + n + ' to see the whole thing!</p></div></div>';
      app.innerHTML = h; wire();
    }
    function check() {
      var it = S.items[S.i], st = S.st[S.i]; if (st.done) return;
      var ok;
      if (it.typed) { st.val = $('#prIn').value; if (!st.val.trim()) { st.msg = 'Type an answer first.'; return render(); } ok = GB.checkTyped(it, st.val).ok; }
      else { if (st.sel === null) { st.msg = 'Pick an answer first.'; return render(); } ok = it.options[st.sel].ok; }
      st.tries++;
      if (ok) { st.done = true; st.msg = 'Correct! A piece of the picture is uncovered.'; if (S.st.every(function (x) { return x.done; })) G.setTimeout(confetti, 300); }
      else st.msg = st.tries > 1 ? 'Not yet. Check your work, or open the worked solution.' : 'Not quite. Try again.';
      render();
      if (ok && S.i < S.items.length - 1) { /* stay so students can read the solution if they want */ }
    }
    function wire() {
      on('[data-q]', 'click', function () { S.i = +this.getAttribute('data-q'); render(); });
      on('[data-opt]', 'click', function () { var st = S.st[S.i]; if (!st.done) { st.sel = +this.getAttribute('data-opt'); st.msg = ''; render(); } });
      if ($('#prCheck')) $('#prCheck').onclick = check;
      if ($('#prIn')) { $('#prIn').onkeydown = function (e) { if (e.key === 'Enter') check(); }; $('#prIn').oninput = function () { S.st[S.i].val = this.value; }; }
      if ($('#prSol')) $('#prSol').onclick = function () { S.st[S.i].sol = !S.st[S.i].sol; render(); };
      $('#prPrev').onclick = function () { S.i--; render(); }; $('#prNext').onclick = function () { S.i++; render(); };
      $('#prLevel').onchange = function () { S.level = this.value; save({ level: S.level }); build(); };
      $('#prNew').onclick = build;
    }
    build();
  }

  var GAMES = { flashcards: flashcards, showdown: showdown, 'connect-four': connectFour, 'tic-tac-toe': ticTacToe, 'picture-reveal': pictureReveal };
  G.TeacherSkills.choose(skillIds.map(function (id) { return { id: id, name: skillName(id) }; }), function (selected) {
    skillIds = selected;
    tags = tags.filter(function (t) { return skillIds.some(function (id) { return SET.byId[id].tag === t; }); });
    (GAMES[GAME] || flashcards)();
  });
  G.MKGAMES.ui = { qHtml: qHtml, solHtml: solHtml };
})(window);

