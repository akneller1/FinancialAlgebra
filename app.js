(function () {
  'use strict';

  var L = window.LIBRARY;
  var courseOrder = { math5: -1, math6: 0, prealgebra7: 1, prealgebra: 2, algebra: 3, geometry: 4, algebra2: 5, precalculus: 6, calculus: 7, statistics: 8, discrete: 9 };
  L.courses.sort(function (a, b) {
    return (courseOrder[a.id] == null ? 99 : courseOrder[a.id]) -
      (courseOrder[b.id] == null ? 99 : courseOrder[b.id]);
  });
  /* Course visibility switches; all current courses are public. */
  var HIDDEN_COURSES = {};
  var SOON = L.courses.filter(function (c) { return c.comingSoon && !HIDDEN_COURSES[c.id]; });
  L.courses = L.courses.filter(function (c) { return !c.comingSoon && !HIDDEN_COURSES[c.id]; });
  var app = document.getElementById('main');
  var nav = document.getElementById('nav');
  var q = document.getElementById('q');
  var skip = document.getElementById('skip');

  var token = '';
  var query = '';
  var filters = {};
  var focusKey = null;
  var firstRender = true;
  var ignoreHash = false;
  var saved = loadSaved();
  L.courses.forEach(function(c){c.units.forEach(function(u){u.artifacts.forEach(function(a){if((a.legacyPaths||[]).some(function(path){return saved.indexOf(path)>=0;})&&saved.indexOf(a.path)<0)saved.push(a.path);});});});
  storeSaved();

  /* ---------- storage ---------- */
  function loadSaved() {
    try {
      var v = JSON.parse(localStorage.getItem('mrk-saved') || '[]');
      return Array.isArray(v) ? v : [];
    } catch (e) { return []; }
  }
  function storeSaved() {
    try { localStorage.setItem('mrk-saved', JSON.stringify(saved)); } catch (e) {}
  }
  function isSaved(path) { return saved.indexOf(path) >= 0; }
  function toggleSaved(path) {
    var i = saved.indexOf(path);
    if (i >= 0) saved.splice(i, 1); else saved.push(path);
    storeSaved();
  }

  /* ---------- helpers ---------- */
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function toArr(v) { return v == null ? [] : (Array.isArray(v) ? v : [v]); }
  function acts(n) { return n === 1 ? '1 activity' : n + ' activities'; }
  function units(n) { return n === 1 ? '1 unit' : n + ' units'; }
  function courseToken(c) { return c.id; }
  function unitToken(c, u) { return c.id + '.' + u.id; }
  /* Units are numbered in course order: "Unit 3: Linear Inequalities". */
  function unitNum(c, u) { return c.units.indexOf(u) + 1; }
  function unitLabel(c, u) { return 'Unit ' + unitNum(c, u) + ': ' + u.name; }
  function href(t) { return '#' + encodeURIComponent(t).replace(/%2E/g, '.'); }
  /* Per-unit printable generator links (Maze, Tarsia, …) are reached through the Activity Generator,
     so they are not listed or counted as activities (unit pages still use them for the generator shortcut). */
  function listed(a) { return activityFormat(a) !== 'printable-generator'; }
  function courseCount(c) {
    return c.units.reduce(function (n, u) { return n + u.artifacts.filter(listed).length; }, 0);
  }
  function unitsWithActivities(c) {
    return c.units.filter(function (u) { return u.artifacts.some(listed); }).length;
  }
  function everything() {
    var out = [];
    L.courses.forEach(function (c) {
      c.units.forEach(function (u) {
        u.artifacts.filter(listed).forEach(function (a) { out.push({ a: a, c: c, u: u }); });
      });
    });
    return out;
  }
  function isNew(a) {
    var t = a.added ? Date.parse(a.added) : NaN;
    if (isNaN(t)) return false;
    return (Date.now() - t) < (L.newDays || 30) * 86400000;
  }
  var ACTIVITY_FORMATS = [
    { id: 'lesson-planner', name: 'Daily Lesson Planner', description: 'Plan any of the 180 Algebra 1 days from the scope and sequence: objectives, vocabulary, sentence frame and misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Prints a student handout and a teacher key with every answer checked.' },
    { id: 'worksheet-generator', name: 'Worksheet Generator', description: 'Build practice worksheets for any unit: choose skills and CP2, CP1 or Honors difficulty, short answer or multiple choice, up to three versions, and an answer key with worked solutions. Every answer is checked.' },
    { id: 'assessment-generator', name: 'Assessment Generator', description: 'Build a standard unit test (multiple choice and short answer) or a choice-based restaurant-menu assessment: pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys.' },
    { id: 'printable-generator', name: 'Printable Generators', description: 'Make a maze, color-by-number page, Tarsia puzzle, error analysis or partner check for any unit: CP2, CP1 or Honors, up to three versions, and an answer key with every answer checked.' },
    { id: 'partner-checks', name: 'Partner Checks', description: 'Partners solve different problems with matching answers, compare results, and work together to resolve mistakes. Includes Partner A and Partner B worksheets.' },
    { id: 'showdown', name: 'Showdown / Jeopardy', description: 'Choose a category and point value, solve the problem, then reveal the worked solution. A game-show format for class or team review.' },
    { id: 'connect-four', name: 'Connect 4', description: 'Solve math problems to earn a disc. Teams take turns building a row of four while blocking their opponents.' },
    { id: 'tic-tac-toe', name: 'Tic-Tac-Toe', description: 'Two teams solve multiple-choice math problems to claim squares and make three in a row. A wrong answer gives the other team a chance to steal. Includes an optional timer.' },
    { id: 'millionaire', name: 'Math Millionaire', description: 'A whole-class game show. Fifteen multiple-choice questions climb from warm-up to challenge on a prize ladder. Groups take turns in the hot seat, with 50:50, Ask the Class and Hint lifelines. Every game draws fresh questions.' },
    { id: 'interactive-math', name: 'Interactive Math', description: 'Hands-on tools students explore on their own device: sliders, draggable graphs and models with built-in Try this challenges. Each comes with a printable Explore & Reflect worksheet and a teacher key.' },
    { id: 'mazes', name: 'Mazes', description: 'Solve each problem and follow the matching answer through a printable maze. Show your work as you find the path to the finish.' },
    { id: 'interactive-practice-test', name: 'Assessment Readiness Check', description: 'Complete a generated online assessment, receive worked solutions and skill-by-skill feedback, and practice missed concepts with fresh questions.' },
    { id: 'flashcards', name: 'Flashcards', description: 'Practice at your own pace, reveal worked solutions, and mark cards to revisit. Useful for independent study and quick review.' },
    { id: 'color-by-number', name: 'Color by Number', description: 'Solve math problems, match each answer to a color, and complete a themed picture. Printable activities for practice and review.' },
    { id: 'picture-reveal', name: 'Picture Reveal', description: 'Answer math questions to uncover a hidden picture, with feedback and worked solutions along the way.' },
    { id: 'error-analysis', name: 'Error Analysis', description: 'Examine a worked example, identify the mistake, and explain how to fix it. Printable practice that builds mathematical reasoning.' },
    { id: 'detective-games', name: 'Detective Games', description: 'Solve math problems to unlock clues, eliminate suspects, and crack a themed mystery. Type your answers and use the case board to identify the culprit.' },
    { id: 'escape-rooms', name: 'Escape Rooms', description: 'Work together to solve math puzzles, decode clues, and unlock five rooms before the timer runs out. Includes hints and a final challenge.' },
    { id: 'topic-games', name: 'Topic-Specific Games', description: 'Explore focused math challenges such as Slope Links Mini Golf and Zombie Fence, where the topic becomes part of the game.' },
    { id: 'cheat-sheets', name: 'Cheat Sheets', description: 'Colorful, printable front-and-back study guides with key vocabulary, formulas, worked examples, graphs, and reminders.' },
    { id: 'whodunnit', name: 'Whodunnit', description: 'Solve problems on printable clue cards, eliminate suspects on a case board, and solve the mystery. Includes space to show your work.' },
    { id: 'tarsia', name: 'Tarsia Puzzles', description: 'Cut out triangles and match math problems to their answers to build a hexagon. Printable puzzles with space to show your work.' },
    { id: 'assessment-menus', name: 'Assessment Menus', description: 'Choose problems from a menu of point values to demonstrate your understanding. Printable assessments with student choice, scoring guidance, and teacher keys.' },
    { id: 'stations', name: 'Stations', description: 'Printable station-work activities with sets of problems for small-group rotation, review, and independent practice.' },
    { id: 'other', name: 'More Activities', description: 'Explore additional practice and resources.' }
  ];
  function activityFormat(a) {
    if (a.bankFormat) return a.bankFormat;
    // Grade 6–8 games share the generator page, but remain games, not worksheets.
    var middleGame = /worksheet-generator\/middle-school-game\.html\?/i.test(a.path || '') &&
      /[?&]game=([a-z-]+)/i.exec(a.path || '');
    if (middleGame) {
      var game = middleGame[1].toLowerCase();
      return ({'tic-tac-toe':'tic-tac-toe','connect-four':'connect-four',
        'picture-reveal':'picture-reveal','showdown':'showdown','flashcards':'flashcards'})[game] || 'other';
    }
    // Matching games remain games even though their player lives in worksheet-generator/.
    if (/worksheet-generator\/match-game\.html/i.test(a.path || '')) return 'topic-games';
    if (/worksheet-generator\/practice-test\.html/i.test(a.path || '')) return 'interactive-practice-test';
    if (/worksheet-generator\/lesson-planner\.html/i.test(a.path || '')) return 'lesson-planner';
    if (/worksheet-generator\/printables\.html/i.test(a.path || '')) return 'printable-generator';
    if (/worksheet-generator\/menu-assessment/i.test(a.path || '')) return 'assessment-generator';
    if (/worksheet-generator\//i.test(a.path || '')) return 'worksheet-generator';
    if (/partner-check/i.test(a.path || '')) return 'partner-checks';
    if (/congruence-proofs/i.test(a.path || '')) return 'proofs';
    var path = a.path || '';
    if (/jeopardy|showdown/i.test(path)) return 'showdown';
    if (/connect-four|inequality-four/i.test(path)) return 'connect-four';
    if (/tic-tac-toe/i.test(path)) return 'tic-tac-toe';
    if (/whodunnit/i.test(path)) return 'whodunnit';
    if (/tarsia/i.test(path)) return 'tarsia';
    if (/assessment-menu/i.test(path)) return 'assessment-menus';
    if (/escape-room/i.test(path)) return 'escape-rooms';
    if (/maze/i.test(path)) return 'mazes';
    if (/flashcards/i.test(path)) return 'flashcards';
    if (/color-by-number/i.test(path)) return 'color-by-number';
    if (/picture-reveal/i.test(path)) return 'picture-reveal';
    if (/stations/i.test(path) || /stations/i.test(a.title || '')) return 'stations';
    if (/cheat.sheet/i.test(path) || /cheat.sheet/i.test(a.title || '')) return 'cheat-sheets';
    if (/error-analysis/i.test(path)) return 'error-analysis';
    if (toArr(a.topics).some(function (topic) { return /detective game/i.test(topic); })) return 'detective-games';
    if (toArr(a.type).indexOf('Game') >= 0) return 'topic-games';
    return 'other';
  }
  /* Teaching mode metadata: derived from game mechanics, not the generic 'Game' type. */
  function gameMode(a) {
    if (a.gameMode) return a.gameMode;
    var f = activityFormat(a);
    if (a.unitSpecific === true) return 'Unit-specific';
    if (['showdown', 'connect-four', 'tic-tac-toe', 'millionaire'].indexOf(f) >= 0) return 'Team Games';
    if (f === 'escape-rooms') return 'Collaborative Challenges';
    if (['picture-reveal', 'detective-games', 'topic-games'].indexOf(f) >= 0) return 'Individual Review';
    return '';
  }
  var GAME_MODES = ['Individual Review', 'Team Games', 'Collaborative Challenges', 'Unit-specific'];
  function formatItems(format) {
    return everything().filter(function (it) { return activityFormat(it.a) === format.id; });
  }
  /* One order everywhere. Games: Showdown (Jeopardy-style), Connect 4, Tic-Tac-Toe, Detective, Escape Room,
     Picture Reveal, then unit-specific activities and games. Study Guides: Assessment Readiness, Flashcards, Cheat Sheets. */
  var ACTIVITY_ORDER = ['showdown', 'connect-four', 'tic-tac-toe', 'millionaire', 'detective-games', 'escape-rooms', 'picture-reveal', 'topic-games',
    'interactive-practice-test', 'flashcards', 'cheat-sheets'];
  function orderRank(a) { var i = ACTIVITY_ORDER.indexOf(activityFormat(a)); return i < 0 ? ACTIVITY_ORDER.length : i; }
  function sortByActivityOrder(list, get) {
    get = get || function (it) { return it.a; };
    var unitOrder = [];
    list.forEach(function (it) { var k = it.c && it.u ? it.c.id + '.' + it.u.id : ''; if (unitOrder.indexOf(k) < 0) unitOrder.push(k); });
    return list.map(function (it, i) { return { it: it, i: i }; }).sort(function (x, y) {
      var kx = x.it.c && x.it.u ? x.it.c.id + '.' + x.it.u.id : '', ky = y.it.c && y.it.u ? y.it.c.id + '.' + y.it.u.id : '';
      return (unitOrder.indexOf(kx) - unitOrder.indexOf(ky)) || (orderRank(get(x.it)) - orderRank(get(y.it))) || (x.i - y.i);
    }).map(function (o) { return o.it; });
  }
  var RESOURCE_GROUPS = [
    { id: 'generators', name: 'Generators', formats: ['lesson-planner', 'worksheet-generator', 'assessment-generator', 'printable-generator'] },
    { id: 'games', name: 'Games', formats: ['showdown', 'connect-four', 'tic-tac-toe', 'millionaire', 'detective-games', 'escape-rooms', 'picture-reveal', 'topic-games'] },
    { id: 'study-guides', name: 'Study Guides', formats: ['interactive-practice-test', 'flashcards', 'cheat-sheets'] },
    { id: 'interactive', name: 'Interactive Math', formats: ['interactive-math'] },
    { id: 'practice', name: 'Practice Activities', formats: ['proofs'] },
    { id: 'projects', name: 'Projects', formats: ['projects'] },
    { id: 'worksheets', name: 'Printable Worksheets', formats: ['partner-checks', 'mazes', 'color-by-number', 'error-analysis', 'stations', 'whodunnit', 'tarsia', 'assessment-menus', 'other'] }
  ];
  // Keep the game's catalog type authoritative across all Browse Activities sections.
  function belongsToGroup(a, group) {
    var isGame = toArr(a.type).indexOf('Game') >= 0;
    var formatMatches = group.formats.indexOf(activityFormat(a)) >= 0;
    return group.id === 'games' ? (isGame || formatMatches) : (!isGame && formatMatches);
  }
  var FORMAT_SUMMARIES = {
    'lesson-planner': 'Plan a day: Do Now, notes, practice and exit ticket from the 180-day scope and sequence.',
    'worksheet-generator': 'Choose skills and create customized printable worksheets with answer keys.',
    'assessment-generator': 'Build a test or a menu assessment with verified answer keys.',
    'printable-generator': 'Make mazes, color-by-number pages, Tarsia puzzles, error analysis and partner checks with answer keys.',
    'partner-checks': 'Solve different problems, compare matching answers, and check each other’s work.',
    'proofs': 'Two-column proofs on accurate diagrams, from drag-and-drop statements to written CPCTC proofs, checked row by row.',
    'showdown': 'Choose a question and point value for team review.',
    'connect-four': 'Solve problems to earn discs and connect four.',
    'tic-tac-toe': 'Answer correctly to claim a square and make three in a row.',
    'interactive-math': 'Explore a concept hands-on, then reflect on a printable worksheet.',
    'millionaire': 'Climb a 15-question prize ladder as a class, with three lifelines.',
    'picture-reveal': 'Solve problems to uncover a hidden picture.',
    'detective-games': 'Unlock clues, eliminate suspects, and solve the mystery.',
    'escape-rooms': 'Solve math puzzles and unlock rooms before time runs out.',
    'topic-games': 'Explore focused challenges, from mini golf to Zombie Fence.',
    'cheat-sheets': 'Review key vocabulary, formulas, and worked examples.',
    'flashcards': 'Practice at your own pace and reveal worked solutions.',
    'interactive-practice-test': 'Take a unit-style assessment, identify weak skills, and check your improvement.',
    'mazes': 'Follow correct answers to find a path through the maze.',
    'color-by-number': 'Match answers to colors to complete a themed picture.',
    'error-analysis': 'Find the mistake and explain how to correct it.',
    'whodunnit': 'Solve clue cards, clear suspects, and crack a printable mystery.',
    'tarsia': 'Match problems and answers on triangle pieces to build a hexagon.',
    'assessment-menus': 'Choose problems at different point values to build your assessment.',
    'stations': 'Rotate through problem sets for practice and review.',
    'other': 'Explore more practice resources.'
  };
  function activityDirectoryHtml() {
    return '<div class="resource-columns">' + RESOURCE_GROUPS.filter(function (group) { return group.id !== 'worksheets'; }).map(function (group) {
      var formats = group.formats.map(function (id) {
        return ACTIVITY_FORMATS.filter(function (format) { return format.id === id; })[0];
      });
      return '<section class="resource-column" aria-labelledby="resource-' + group.id + '">' +
        '<h3 id="resource-' + group.id + '">' + esc(group.name) + '</h3><ul class="resource-types">' +
        formats.map(function (format) {
          var items = formatItems(format);
          if (!items.length) return '';
          var preview = items.filter(function (it) { return !!it.a.thumb; })[0];
          return '<li><a class="resource-type" href="' + href('activity.' + format.id) + '">' +
            (preview ? '<img src="' + esc(preview.a.thumb) + '" alt="" width="144" height="90" loading="lazy">' : '') +
            '<h4>' + esc(format.name) + '</h4><p>' + esc(FORMAT_SUMMARIES[format.id]) + '</p>' +
            '<span class="resource-count">' + acts(items.length) + '</span></a></li>';
        }).join('') + '</ul></section>';
    }).join('') + '</div>';
  }

  /* ---------- decorative art ---------- */
  var ART = {
    linear:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="35" y="20" width="140" height="115" rx="6"/>' +
      '<path class="s-thin" d="M 35 45 H 175 M 35 75 H 175 M 35 105 H 175 M 65 20 V 135 M 100 20 V 135 M 135 20 V 135"/>' +
      '<path class="s" d="M 20 135 H 185 M 35 145 V 10"/>' +
      '<path class="s" d="M 45 120 L 165 30"/>' +
      '<circle class="f" cx="65" cy="105" r="6"/><circle class="f" cx="105" cy="75" r="6"/><circle class="f" cx="145" cy="45" r="6"/>' +
      '</svg>',
    network:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="25" y="23" width="150" height="114" rx="8"/>' +
      '<path class="s-thin" d="M 45 80 L 85 35 L 145 45 L 165 110 L 100 130 Z M 45 80 L 145 45 M 85 35 L 100 130 M 45 80 L 165 110"/>' +
      '<circle class="f" cx="45" cy="80" r="9"/><circle class="f" cx="85" cy="35" r="9"/>' +
      '<circle class="f" cx="145" cy="45" r="9"/><circle class="f" cx="165" cy="110" r="9"/><circle class="f" cx="100" cy="130" r="9"/>' +
      '</svg>',
    distribution:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="25" y="23" width="150" height="114" rx="8"/>' +
      '<path class="s-thin" d="M 20 135 H 185 M 30 145 V 20"/>' +
      '<path class="f-soft" d="M 45 135 V 116 H 65 V 87 H 85 V 51 H 105 V 51 H 125 V 87 H 145 V 116 H 165 V 135 Z"/>' +
      '<path class="s" d="M 35 133 C 65 133 72 40 105 40 S 145 133 175 133"/>' +
      '<path class="s-thin" d="M 105 40 V 135"/>' +
      '</svg>',
    tangent:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="25" y="23" width="150" height="114" rx="8"/>' +
      '<path class="s-thin" d="M 15 135 H 190 M 30 15 V 150"/>' +
      '<path class="s" d="M 35 125 Q 105 125 175 25"/>' +
      '<path class="s-thin" d="M 49 140 L 161 60"/>' +
      '<circle class="f" cx="105" cy="100" r="7"/>' +
      '</svg>',
    wave:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="25" y="23" width="150" height="114" rx="8"/>' +
      '<path class="s-thin" d="M 15 80 H 185 M 100 10 V 150"/>' +
      '<path class="s" d="M 20 80 C 33 20 47 20 60 80 S 87 140 100 80 S 127 20 140 80 S 167 140 180 80"/>' +
      '<circle class="f" cx="40" cy="35" r="7"/><circle class="f" cx="100" cy="80" r="7"/><circle class="f" cx="160" cy="125" r="7"/>' +
      '</svg>',
    curve:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="100" y="20" width="80" height="110" rx="6"/>' +
      '<line class="s-thin" x1="20" y1="130" x2="190" y2="130"/>' +
      '<line class="s-thin" x1="100" y1="10" x2="100" y2="150"/>' +
      '<path class="s" d="M 30 20 Q 100 200 170 20"/>' +
      '<circle class="f" cx="65" cy="87.5" r="7"/><circle class="f" cx="135" cy="87.5" r="7"/><circle class="f" cx="100" cy="110" r="7"/>' +
      '</svg>',
    fifth:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="24" y="26" width="152" height="108" rx="10"/>' +
      '<path class="f" d="M 70 80 L 70 40 A 40 40 0 0 1 110 80 Z"/><circle class="s" cx="70" cy="80" r="40" fill="none"/>' +
      '<path class="s-thin" d="M 30 80 H 110 M 70 40 V 120"/>' +
      '<rect class="f" x="126" y="94" width="14" height="14"/><rect class="f" x="140" y="94" width="14" height="14"/><rect class="f" x="126" y="80" width="14" height="14"/><rect class="s-thin" x="126" y="66" width="28" height="42" fill="none"/>' +
      '</svg>',
    sixth:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="28" y="23" width="144" height="112" rx="8"/>' +
      '<path class="s-thin" d="M 43 57 H 157 M 43 96 H 157 M 80 36 V 123 M 119 36 V 123"/>' +
      '<circle class="f" cx="61" cy="46" r="8"/><circle class="f" cx="99" cy="46" r="8"/><circle class="f" cx="138" cy="46" r="8"/>' +
      '<path class="s" d="M 54 83 H 106 M 80 68 V 97 M 128 82 H 153 M 128 91 H 153"/>' +
      '</svg>',
    seventh:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="20" y="28" width="160" height="105" rx="8"/>' +
      '<path class="s" d="M 39 70 H 162 M 99 43 V 113"/>' +
      '<text x="63" y="61" text-anchor="middle" font-size="25" font-weight="800" fill="currentColor">3</text>' +
      '<text x="137" y="61" text-anchor="middle" font-size="25" font-weight="800" fill="currentColor">4</text>' +
      '<text x="99" y="105" text-anchor="middle" font-size="27" font-weight="800" fill="currentColor">7</text>' +
      '</svg>',
    eighth:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="25" y="23" width="150" height="114" rx="8"/>' +
      '<path class="s" d="M 47 79 H 150 M 53 49 L 103 79 L 151 40"/>' +
      '<circle class="f" cx="53" cy="49" r="7"/><circle class="f" cx="103" cy="79" r="7"/><circle class="f" cx="151" cy="40" r="7"/>' +
      '<path class="s-thin" d="M 103 79 L 103 113 M 47 113 H 150"/>' +
      '</svg>',
    triangle:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<polygon class="f-soft" points="100,20 30,130 170,130"/>' +
      '<circle class="s-thin" cx="100" cy="91.6" r="38.4"/>' +
      '<polygon class="s" points="100,20 30,130 170,130"/>' +
      '<path class="s" d="M 52 130 A 22 22 0 0 0 44 114"/>' +
      '<circle class="f" cx="100" cy="20" r="7"/><circle class="f" cx="30" cy="130" r="7"/><circle class="f" cx="170" cy="130" r="7"/>' +
      '</svg>'
  };
  function artFor(c) { var byCourse = { math5: 'fifth', math6: 'sixth', prealgebra7: 'seventh', prealgebra: 'eighth', algebra: 'linear', geometry: 'triangle', algebra2: 'curve' }; return ART[byCourse[c.id] || c.art] || ''; }

  var STAR =
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2 6.3 20.3l1.2-6.4L2.8 9.5l6.4-.8z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>';
  var STAR_ON =
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2 6.3 20.3l1.2-6.4L2.8 9.5l6.4-.8z" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>';

  /* ---------- pieces ---------- */
  function crumbs(list) {
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + list.map(function (item, i) {
      var last = i === list.length - 1;
      return '<li>' + (last ? '<span aria-current="page">' + esc(item[0]) + '</span>'
                            : '<a href="' + item[1] + '">' + esc(item[0]) + '</a>') + '</li>';
    }).join('') + '</ol></nav>';
  }

  function saveBtnHtml(path) {
    var on = isSaved(path);
    return '<button type="button" class="btn btn-ghost save" data-path="' + esc(path) + '" aria-pressed="' + on + '">' +
      (on ? STAR_ON : STAR) + '<span>' + (on ? 'Saved' : 'Save') + '</span></button>';
  }

  function activityUrl(a) { var path=a.path||''; if (path === 'artifacts/relations-functions-function-machine-factory/index.html' || path === 'artifacts/polynomials-garden-planner/index.html' || path === 'artifacts/exponential-functions-outbreak-simulator/index.html' || path === 'artifacts/geometry-shipwreck-salvage/index.html') return path; if (/^artifacts\/math-arcade\/index\.html\?game=(rocket|inequality|laser|mirror|cannon|portal|catapult)$/.test(path)) return path; return /^worksheet-generator\/[a-z0-9_\-/]+\.html(#unit=[a-z0-9\-]+(&kind=[a-z]+)?)?$/i.test(path) || /^worksheet-generator\/(approved-flashcards|approved-games|grade-practice|middle-school-game|algebra2-game|algebra2-practice|bank-printable|course-game|course-activity)\.html\?[a-z0-9_=&%\-]+$/i.test(path) ? path : 'activity.html?path=' + encodeURIComponent(path); }

  function actionLabel(a) {
    var format = activityFormat(a);
    if (/worksheet-generator\/printables\.html/.test(a.path || '')) return 'Make printable';
    if (format === 'lesson-planner') return 'Plan a day';
    if (format === 'worksheet-generator') return 'Create worksheet';
    if (format === 'assessment-generator') return 'Build assessment';
    if (format === 'cheat-sheets') return 'View study guide';
    if (format === 'interactive-math') return 'Explore';
    if (format === 'interactive-practice-test') return 'Take practice test';
    if (format === 'flashcards') return 'Study flashcards';
    if (/\.pdf$/i.test(a.path)) return 'Open PDF';
    return toArr(a.type).indexOf('Game') >= 0 ? 'Play' : 'Open activity';
  }
  function resourceInfo(a) {
    if (a.worksheet) return '<p class="resource-info">Printable: <a href="' + esc(a.worksheet) + '" target="_blank" rel="noopener">Explore &amp; Reflect worksheet</a>' +
      (a.answerKey ? ' · <a href="' + esc(a.answerKey) + '" target="_blank" rel="noopener">Teacher key</a>' : '') + '</p>';
    var m = (window.RESOURCE_DETAILS || {})[a.path];
    if (!m) return '';
    var labels = [m.pages + (m.pages === 1 ? ' page' : ' pages')];
    if (m.embeddedKey) labels.push('Answer key included');
    if (m.answerKey) labels.push('Separate teacher key');
    if (m.studentOnly) labels.push('Student worksheets only');
    if (m.referenceSheet) labels.push('Reference sheet');
    return '<p class="resource-info">' + labels.map(esc).join(' · ') + '</p>';
  }
  function reportUrl(a) {
    var url = 'https://akneller1.github.io/classroom/' + activityUrl(a);
    var body = 'Activity: ' + a.title + '\nLink: ' + url + '\n\nProblem (broken link, incorrect answer, unclear directions, or other):\n\nProblem number / steps to reproduce:\n\nExpected result:\n';
    return 'mailto:akneller@gmail.com?subject=' + encodeURIComponent('Mr. K\'s Classroom — Resource problem: ' + a.title) + '&body=' + encodeURIComponent(body);
  }

  // Use game-board previews rather than captured setup/question dialogs.
  // These are illustrations of the existing game modes, not generated questions.
  function gameBoardThumbnail(a, it) {
    // Each game with an authored thumbnail must use it rather than a generated generic preview.
    if (a.thumb && (activityFormat(a) === 'topic-games' || /slope-links-mini-golf|zombie-fence/i.test(a.path || ''))) return a.thumb;
    if (/^artifacts\/math-arcade\/index\.html\?game=/.test(a.path || '')) return a.thumb || '';
    var f = activityFormat(a);
    var supported = ['tic-tac-toe','connect-four','showdown','millionaire','picture-reveal','flashcards','escape-rooms','whodunnit','detective-games','topic-games'];
    if (supported.indexOf(f) < 0) return a.thumb || '';
    var topic = (it.u && (it.u.name || it.u.title)) || (it.c && it.c.name) || '';
    var title = {'tic-tac-toe':'TIC-TAC-TOE','connect-four':'CONNECT 4','millionaire':'MATH MILLIONAIRE',
      'showdown':'SHOWDOWN','picture-reveal':'PICTURE REVEAL',
      'flashcards':'FLASHCARDS','escape-rooms':'ESCAPE ROOM',
      'whodunnit':'DETECTIVE','detective-games':'DETECTIVE','topic-games':'TEAM GAME'}[f];
    function rect(x,y,w,h,fill,rx,stroke) {
      return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="'+(rx||0)+
        '" fill="'+fill+'"'+(stroke?' stroke="'+stroke+'" stroke-width="2"':'')+'/>';
    }
    function txt(x,y,value,size,color,weight,anchor) {
      return '<text x="'+x+'" y="'+y+'" font-family="Arial,sans-serif" font-size="'+size+
        '" font-weight="'+(weight||600)+'" fill="'+(color||'#172d53')+
        '" text-anchor="'+(anchor||'start')+'">'+esc(value)+'</text>';
    }
    var art = '';
    if (f === 'tic-tac-toe') {
      art += rect(159,62,162,162,'#ffffff',12,'#c7d6f0');
      for(var i=1;i<3;i++) {
        art += '<path d="M '+(159+54*i)+' 69 V 217 M 166 '+(62+54*i)+' H 314" stroke="#7287ad" stroke-width="4"/>';
      }
      [[186,99,'X'],[240,99,'O'],[294,99,'X'],[186,153,'O'],[240,153,'X'],[294,153,'O'],[186,207,'X']].forEach(function(v){
        art += txt(v[0],v[1],v[2],33,v[2]==='X'?'#5a49d6':'#ee8c42',700,'middle');
      });
    } else if (f === 'connect-four') {
      art += rect(123,62,234,157,'#4568b7',14);
      for(var row=0;row<4;row++)for(var col=0;col<7;col++){
        var colors=['#f1f5fc','#f1f5fc','#f1f5fc','#f1f5fc','#f1f5fc','#f1f5fc','#f1f5fc'];
        if(row===3)colors=['#f6c453','#f6c453','#7063d7','#7063d7','#f6c453','#7063d7','#f6c453'];
        if(row===2)colors=['#f1f5fc','#7063d7','#f6c453','#7063d7','#f1f5fc','#f6c453','#f1f5fc'];
        if(row===1)colors=['#f1f5fc','#f1f5fc','#f1f5fc','#f6c453','#f1f5fc','#f1f5fc','#f1f5fc'];
        art += '<circle cx="'+(143+col*33)+'" cy="'+(83+row*38)+'" r="12" fill="'+colors[col]+'"/>';
      }
    } else if (f === 'showdown') {
      art += rect(100,58,280,166,'#1f458b',12);
      for(var rr=0;rr<4;rr++)for(var cc=0;cc<4;cc++){
        var xx=108+cc*67, yy=65+rr*38;
        art+=rect(xx,yy,60,33,rr===0?'#527bd2':'#173673',5,'#6387ca');
        art+=txt(xx+30,yy+22,rr===0?['A','B','C','D'][cc]:String(rr*100),rr===0?12:17,'#ffffff',700,'middle');
      }
    } else if (f === 'millionaire') {
      art += rect(96,56,288,172,'#0d1660',12);
      function lozenge(x,y,w,h,fill){
        var c=12;return '<path d="M '+(x+c)+' '+y+' H '+(x+w-c)+' L '+(x+w)+' '+(y+h/2)+' L '+(x+w-c)+' '+(y+h)+' H '+(x+c)+' L '+x+' '+(y+h/2)+' Z" fill="'+fill+'" stroke="#c5cff0" stroke-width="2"/>';
      }
      art += lozenge(108,68,180,46,'#1d2c9e');
      art += txt(198,96,'Question 15',14,'#ffffff',700,'middle');
      art += lozenge(108,126,86,30,'#1d2c9e')+txt(122,146,'A',13,'#f7a21b',700);
      art += lozenge(202,126,86,30,'#f7a21b')+txt(216,146,'B',13,'#ffffff',700);
      art += lozenge(108,164,86,30,'#1d2c9e')+txt(122,184,'C',13,'#f7a21b',700);
      art += lozenge(202,164,86,30,'#22b84a')+txt(216,184,'D',13,'#ffffff',700);
      ['$1,000,000','$500,000','$250,000','$125,000','$64,000','$32,000'].forEach(function(v,i){
        if(i===2)art += rect(300,64+i*24,76,20,'#f7a21b',4);
        art += txt(338,79+i*24,v,11,i===2?'#140b00':(i===0||i===5?'#ffffff':'#f7a21b'),700,'middle');
      });
    } else if (f === 'picture-reveal') {
      art += rect(138,58,204,164,'#e9f7ed',12,'#abc7b5');
      art += '<circle cx="240" cy="129" r="51" fill="#f4c75b"/><path d="M 191 162 Q 240 101 289 162" fill="#75ae85"/>';
      for(var pr=0;pr<4;pr++)for(var pc=0;pc<5;pc++){
        if((pr+pc)%3!==0)art+=rect(140+pc*40,60+pr*40,39,39,'#5976bb',2,'#d8e4f7');
      }
    } else if (f === 'flashcards') {
      art += rect(145,69,205,142,'#c7d5f0',12);
      art += rect(131,59,205,142,'#ffffff',12,'#9bb0d8');
      art += txt(233,108,'REVIEW CARD',15,'#5b6fa3',700,'middle');
      art += '<path d="M 170 124 H 296" stroke="#c1cee4" stroke-width="3"/>';
      art += txt(233,156,'Flip to reveal',18,'#283d70',700,'middle');
      art += txt(233,177,'the answer',15,'#5d7199',500,'middle');
    } else if (f === 'escape-rooms') {
      art += rect(147,59,186,159,'#243e72',12);
      art += '<path d="M 191 116 V 96 Q 191 54 240 54 Q 289 54 289 96 V 116" fill="none" stroke="#e6b863" stroke-width="11"/>';
      art += rect(177,112,126,83,'#e6b863',10);
      art += '<circle cx="240" cy="144" r="10" fill="#243e72"/><path d="M 236 150 H 244 L 248 174 H 232 Z" fill="#243e72"/>';
    }
    if (f === 'whodunnit' || f === 'detective-games' || f === 'topic-games') {
      art += rect(137,61,206,157,'#e6edf9',12,'#adbfdf');
      art += rect(157,77,166,124,'#ffffff',7,'#afc3e0');
      art += '<circle cx="228" cy="122" r="32" fill="none" stroke="#596fb6" stroke-width="9"/>';
      art += '<path d="M 252 144 L 289 181" stroke="#334d83" stroke-width="13" stroke-linecap="round"/>';
      art += txt(237,190,'CLUE 1 / 4',13,'#687ca5',700,'middle');
    }
    var topicLabel = String(topic).replace(/&/g,'&amp;').replace(/</g,'&lt;').slice(0,45);
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 272" role="img" aria-label="'+esc(title)+' game board preview">'+
      rect(0,0,480,272,'#f2f6fd',0)+rect(8,8,464,256,'#ffffff',15,'#d4e0f3')+
      rect(8,8,464,37,'#e4ebfa',15)+txt(24,32,title,16,'#233f75',700)+
      art+txt(240,250,topicLabel,16,'#465c82',600,'middle')+'</svg>';
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  }
  function presentationUrl(a) {
    var url = activityUrl(a);
    var hashAt = url.indexOf('#'), fragment = hashAt >= 0 ? url.slice(hashAt) : '';
    var page = hashAt >= 0 ? url.slice(0, hashAt) : url;
    return page + (page.indexOf('?') >= 0 ? '&' : '?') + 'present=1' + fragment;
  }
  function cardHtml(it, showWhere, compact) {
    var a = it.a;
    var tags = [];
    if (isNew(a)) tags.push('<li class="tag tag-new">New</li>');
    toArr(a.type).concat(toArr(a.level)).forEach(function (t) { tags.push('<li class="tag">' + esc(t) + '</li>'); });
    var topics = toArr(a.topics);
    return '<li class="card" data-color="' + esc(it.c.color || '') + '" data-course="' + esc(it.c.id) + '" data-path="' + esc(a.path) + '">' +
      '<a class="thumb" href="' + esc(activityUrl(a)) + '" tabindex="-1" aria-hidden="true">' +
        (gameBoardThumbnail(a, it) ? '<img src="' + esc(gameBoardThumbnail(a, it)) + '" alt="" loading="lazy">' : '') + '</a>' +
      '<div class="card-body">' +
        (showWhere ? '<p class="where">' + esc(it.c.name) + ', ' + esc(unitLabel(it.c, it.u)) + '</p>' : '') +
        '<h3><a href="' + esc(activityUrl(a)) + '">' + esc(a.title) +
          '</a></h3>' +
        (gameMode(a) ? '<span class="game-mode-tag">' + esc(gameMode(a)) + '</span>' : '') +
        '<p class="desc">' + esc(shortDescription(a)) + '</p>' + resourceInfo(a) +
        '<div class="actions"><a class="btn btn-open" href="' + esc(activityUrl(a)) + '">' + esc(actionLabel(a)) + '</a>' +
          (activityFormat(a) === 'interactive-math' ? '<a class="btn btn-ghost" href="' + esc(presentationUrl(a)) + '" aria-label="Present ' + esc(a.title) + ' to the class">▣ Present</a>' : '') +
          saveBtnHtml(a.path) + (/practice-test\.html#unit=([a-z0-9-]+)/i.test(a.path || '') ? '<button type="button" class="btn btn-ghost readiness-activity-share" data-readiness-unit="' + esc(/#unit=([a-z0-9-]+)/i.exec(a.path)[1]) + '">Copy student link</button>' : '') + '</div>' +
        '<a class="report-problem" href="' + esc(reportUrl(a)) + '">Report a problem<span class="sr"> with ' + esc(a.title) + ' — choose an email application</span></a>' +
      '</div></li>';
  }

  function chip(field, val, label) {
    var on = (filters[field] || '') === val;
    return '<button type="button" class="chip" data-field="' + field + '" data-val="' + esc(val) +
           '" aria-pressed="' + on + '">' + esc(label) + '</button>';
  }
  function chipsHtml(items) {
    var out = '';
    [['type', 'Type'], ['level', 'Level']].forEach(function (f) {
      var seen = [];
      items.forEach(function (it) {
        toArr(it.a[f[0]]).forEach(function (v) { if (seen.indexOf(v) < 0) seen.push(v); });
      });
      if (seen.length < 2) return;
      out += '<div class="chips" role="group" aria-label="Filter by ' + f[1].toLowerCase() + '">' +
             '<span class="chips-label">' + f[1] + '</span>' + chip(f[0], '', 'All');
      seen.forEach(function (v) { out += chip(f[0], v, v); });
      out += '</div>';
    });
    return out ? '<div class="filters">' + out + '</div>' : '';
  }
  function applyFilters(items) {
    return items.filter(function (it) {
      return Object.keys(filters).every(function (k) {
        return !filters[k] || toArr(it.a[k]).indexOf(filters[k]) >= 0;
      });
    });
  }
  function cardsHtml(items, showWhere) {
    var shown = applyFilters(items);
    if (!shown.length) {
      return '<div class="empty"><h2>No matches</h2><p>No activities fit these filters. Choose All to see everything here.</p></div>';
    }
    return '<ul class="cards grouped-cards">' + shown.map(function (it) { return cardHtml(it, showWhere); }).join('') + '</ul>';
  }

  /* ---------- views ---------- */
  function homeView() {
    var tasks = [
      { title: 'Read the Teacher Guide', description: 'Get to know the tools, choose resources, and plan your first lesson.', url: 'guide.html', icon: '?', color: 'blue', action: 'Open the teacher guide' },
      { title: 'Plan a Lesson', description: 'Build your day with notes, examples, practice, and an exit ticket.', url: 'worksheet-generator/lesson-planner.html', icon: '▤', color: 'blue', action: 'Start planning' },
      { title: 'Create a Worksheet', description: 'Choose skills, difficulty, and versions. Print with worked answer keys.', url: 'worksheet-generator/worksheet.html', icon: '≡', color: 'teal', action: 'Build a worksheet' },
      { title: 'Create an Activity', description: 'Make mazes, Tarsia puzzles, partner checks, vocabulary, and more.', url: 'worksheet-generator/printables.html', icon: '✦', color: 'purple', action: 'Choose an activity' },
      { title: 'Build an Assessment', description: 'Create a test or choice-based assessment, then edit before printing.', url: 'worksheet-generator/menu-assessment.html', icon: '☑', color: 'orange', action: 'Build an assessment' },
      { title: 'Play a Math Game', description: 'Bring on team review, escape rooms, mysteries, and individual challenges.', url: '#activities?category=games', icon: '◈', color: 'coral', action: 'Find a game' },
      { title: 'Explore Interactive Math', description: 'Make concepts click with hands-on graphs, models, and investigations.', url: '#activities?category=interactive', icon: '⟡', color: 'green', action: 'Explore the tools' },
      { title: 'Review & Study', description: 'Find flashcards, cheat sheets, and reference guides for your next unit.', url: '#activities?category=study-guides', icon: '▥', color: 'purple', action: 'Find study resources' },
      { title: 'Create a Seating Chart', description: 'Arrange desks, add your class list, and assign seats. Save, print, or export your chart.', url: 'worksheet-generator/seating-chart.html', icon: '▦', color: 'purple', action: 'Arrange your classroom' },
    ];
    return {
      title: L.title,
      html: '<section class="task-home"><div class="wrap home-dashboard"><aside class="course-sidebar" aria-label="Choose a course"></aside><div class="task-workspace">' +
        '<div class="task-intro"><p class="section-kicker">MORE LEARNING. LESS PLANNING.</p>' +
        '<h1 tabindex="-1">What would you like to do today?</h1>' +
        '<p class="lede">Choose a task below or explore a course from the menu.</p>' +
        '</div>' +
        '<ul class="task-grid" aria-label="Teaching tasks">' + tasks.map(function (task) {
          return '<li><a class="task-card" data-color="' + task.color + '" href="' + esc(task.url) + '">' +
            '<span class="task-icon" aria-hidden="true">' + task.icon + '</span><h2>' + task.title + '</h2>' +
            '<p>' + task.description + '</p><span class="task-action">' + task.action + ' <span aria-hidden="true">→</span></span></a></li>';
        }).join('') + '</ul><p class="task-browse">Looking for something specific? <a href="#activities">Browse all resources →</a></p></div></div></section>'
    };
  }

  function bandHtml(c, inner, extra) {
    return '<section class="band' + (extra === 'unit' ? ' unit-band' : extra === 'course' ? ' course-band' : '') + '"' + (c ? ' data-color="' + esc(c.color || '') + '" data-course="' + esc(c.id) + '"' : '') + '><div class="wrap">' + inner + '</div></section>';
  }


  function shortDescription(a) {
    var text = (a.description || FORMAT_SUMMARIES[activityFormat(a)] || '').trim();
    if (text.length <= 155) return text;
    var sentence = text.match(/^.{40,154}?[.!?](?:\s|$)/);
    if (sentence) return sentence[0].trim();
    return text.slice(0, 152).replace(/\s+\S*$/, '') + '…';
  }

  function groupedCardsHtml(items, showWhere) {
    var shown = applyFilters(items);
    if (!shown.length) return '<div class="empty"><h2>No matches</h2><p>No activities fit these filters. Choose All to see everything here.</p></div>';
    return '<div class="activity-groups">' + RESOURCE_GROUPS.map(function (group) {
      var members = sortByActivityOrder(shown.filter(function (it) { return belongsToGroup(it.a, group); }));
      if (!members.length) return '';
      return '<section class="activity-group" aria-labelledby="group-' + group.id + '">' +
        '<h2 id="group-' + group.id + '">' + esc(group.name) + '<span>' + acts(members.length) + '</span></h2>' +
        '<ul class="cards grouped-cards">' + members.map(function (it) { return cardHtml(it, showWhere, true); }).join('') + '</ul></section>';
    }).join('') + '</div>';
  }

  // Shared Geometry-style lesson previews for every course and future additions.
  function subskillsHtml(u, courseId) {
    var skills = window.MK_COURSE_CATALOG.getSkills(courseId, u.id);
    if (!skills.length) {
      var candidates = u.skills || u.lessons || u.objectives || [];
      if (Array.isArray(candidates)) skills = candidates.map(function (entry) {
        return typeof entry === 'string' ? entry : (entry && (entry.name || entry.title || entry.text) || '');
      }).filter(Boolean);
    }
    if (!skills.length) return '';
    function lines(list) {
      return '<ul class="unit-skills">' + list.map(function (skill) {
        return '<li class="unit-skill">' + esc(skill) + '</li>';
      }).join('') + '</ul>';
    }
    if (skills.length <= 4) return lines(skills);
    return lines(skills.slice(0, 4)) +
      '<details class="unit-lesson-details"><summary><span class="show-label">Show all ' + skills.length + ' lessons</span>' +
      '<span class="hide-label">Show fewer lessons</span></summary>' +
      lines(skills.slice(4)) + '</details>';
  }

  function lessonCount(c) {
    return c.units.reduce(function (sum, unit) {
      return sum + window.MK_COURSE_CATALOG.getSkills(c.id, unit.id).length;
    }, 0);
  }
  function courseView(c) {
    var n = courseCount(c);
    var inner =
      '<div class="band-grid"><div>' +
        crumbs([['Home', '#'], [c.name, null]]) +
        '<h1 tabindex="-1">' + esc(c.name) + '</h1>' +
        (['algebra', 'geometry', 'algebra2', 'prealgebra', 'prealgebra7', 'math6', 'math5', 'precalculus', 'calculus', 'statistics', 'discrete'].indexOf(c.id) >= 0 ? '' : '<span class="course-wip-label">Coming Soon</span>') +
        (c.blurb ? '<p class="band-blurb">' + esc(c.blurb) + '</p>' : '') +
        '<p class="band-meta">' + (c.planned ? units(c.units.length) + ' · course outline · activities coming soon' : (c.id === 'math5' || c.id === 'math6' || c.id === 'prealgebra7' || c.id === 'prealgebra') ? units(c.units.length) + ' with ' + lessonCount(c) + ' lessons with generators, games, and study guides' : (c.id === 'algebra' || c.id === 'geometry' || c.id === 'algebra2' || c.id === 'precalculus' || c.id === 'calculus' || c.id === 'statistics' || c.id === 'discrete') ? units(c.units.length) + ' with skills, generators, games, and study guides' : (n ? acts(n) + ' in ' + unitsWithActivities(c) + ' of ' + units(c.units.length) : units(c.units.length) + ', activities coming soon')) + '</p>' +
      '</div>' + (c.art ? '<div class="band-art" aria-hidden="true">' + artFor(c) + '</div>' : '') + '</div>';
    return {
      title: c.name,
      html: bandHtml(c, inner, 'course') +
        (c.planned ? '' : '<section class="section"><div class="wrap">' + generatorLinks(c, null, true) + '</div></section>') +
        '<section class="section"><div class="wrap"><h2 class="course-units-title">Browse by unit</h2><ul class="units">' +
        c.units.map(function (u) {
          var lessons = subskillsHtml(u, c.id);
          var resourceCount = u.artifacts.filter(listed).length;
          return '<li><div class="unit algebra-unit-card" data-color="' + esc(c.color || '') + '" data-course="' + esc(c.id) + '">' +
            '<h3><a class="unit-title-link" href="' + href(unitToken(c, u)) + '">' +
            '<span class="unit-num">Unit ' + unitNum(c, u) + '</span>' + esc(u.name) + '</a></h3>' +
            (lessons ? '<div class="unit-meta" data-lesson-list="true">' + lessons + '</div>' :
              '<p class="unit-outline-fallback">' + (resourceCount ? 'Explore the available resources in this unit.' : 'Lesson outline coming soon.') + '</p>') +
            '<a class="unit-open-link" href="' + href(unitToken(c, u)) + '">Open unit →</a></div></li>';
        }).join('') + '</ul></div></section>'
    };
  }

  /* Algebra 1 unit pages prioritize the four creation tools; legacy printables remain
     in the library, global search, and activity browser rather than being duplicated here. */
  var GENERATOR_ACTIONS = [
    { format: 'lesson-planner', title: 'Lesson Plan', icon: '📖', description: 'Objectives, notes, examples, practice, and exit tickets.', page: 'lesson-planner.html' },
    { format: 'worksheet-generator', title: 'Worksheet', icon: '📝', description: 'Differentiated questions, versions, and answer keys.', page: 'worksheet.html' },
    { format: 'printable-generator', title: 'Activity', icon: '🧩', description: 'Mazes, puzzles, partner checks, and more.', page: 'printables.html' },
    { format: 'assessment-generator', title: 'Assessment', icon: '📋', description: 'Tests and choice-based assessments.', page: 'menu-assessment.html' }
  ];
  function generatorLinks(c, u, compact) {
    var items = u ? u.artifacts : [];
    var unitId = '';
    if (u) {
      if (c.id === 'geometry') {
        items.some(function (a) { var m = /#unit=([a-z0-9-]+)/.exec(a.path || ''); if (m) { unitId = m[1]; return true; } return false; });
      } else unitId = 'algebra1-' + u.id;
    }
    return '<div class="generator-banner' + (compact ? ' compact' : '') + '">' +
      '<div class="generator-banner-heading"><h2>' + (compact ? (u ? 'Create Resources for This Unit' : 'Create Resources for This Course') : 'What would you like to do today?') + '</h2>' +
      (!compact ? '<p>Choose a generator, select your unit, and make classroom-ready resources.</p>' : '') + '</div>' +
      '<ul class="generator-shortcuts">' + GENERATOR_ACTIONS.map(function (tool) {
        var match = items.filter(function (a) { return activityFormat(a) === tool.format; })[0];
        var url = match ? activityUrl(match) : 'worksheet-generator/' + tool.page;
        if (c && c.id === 'geometry') {
          var supported = !u || !!unitId;
          if (!supported) return '<li><span class="generator-shortcut" aria-disabled="true" title="Geometry question banks still in development"><span class="generator-shortcut-icon" aria-hidden="true">◌</span><span class="generator-shortcut-copy"><strong>' + esc(tool.title) + '</strong><small>Coming soon</small></span></span></li>';
          url = 'worksheet-generator/' + tool.page + (unitId ? '#unit=' + unitId : '');
        }
        if (c && ['algebra2', 'prealgebra', 'prealgebra7', 'math6', 'math5', 'precalculus', 'calculus', 'statistics', 'discrete'].indexOf(c.id) >= 0) {
          var selectedUnit = u ? u.id : c.units[0].id;
          // Algebra 2 uses the same Lesson Planner, Worksheet and Assessment Generators as Algebra 1 and Geometry
          // (bank-printable.html stays available for old links).
          url = 'worksheet-generator/' + ({ 'printable-generator': 'printables.html', 'lesson-planner': 'lesson-planner.html', 'assessment-generator': 'menu-assessment.html', 'worksheet-generator': 'worksheet.html' }[tool.format] || tool.page) + '#unit=' + c.id + '-' + selectedUnit;
        }
        if (match && tool.format === 'printable-generator') url = url.replace(/&kind=[a-z]+$/, '');
        return '<li><a class="generator-shortcut" href="' + esc(url) + '">' +
          '<span class="generator-shortcut-icon" aria-hidden="true">' + ({'lesson-planner':'▤','worksheet-generator':'≡','printable-generator':'✦','assessment-generator':'☑'}[tool.format]) + '</span>' +
          '<span class="generator-shortcut-copy"><strong>' + (compact ? esc(tool.title) : 'Create a ' + esc(tool.title)) + '</strong>' +
          (!compact ? '<small>' + esc(tool.description) + '</small>' : '') +
          '</span></a></li>';
      }).join('') +
      ['games', 'study-guides', 'interactive'].filter(function (category) {
        if (category !== 'interactive') return true;
        // Only offer Interactive Math where this course (or unit) has tools.
        return (c ? (u ? [u] : c.units) : L.courses.reduce(function (all, cc) { return all.concat(cc.units); }, [])).some(function (uu) {
          return uu.artifacts.some(function (a) { return activityFormat(a) === 'interactive-math'; });
        });
      }).map(function (category) {
        var params = new URLSearchParams();
        if (c) params.set('subject', c.id);
        if (u) params.set('unit', unitToken(c, u));
        params.set('category', category);
        var isGames = category === 'games', label = { games: 'Games', 'study-guides': 'Study Guides', interactive: 'Interactive Math' }[category];
        return '<li><a class="generator-shortcut resource-shortcut" href="#activities?' + params.toString() + '">' +
          '<span class="generator-shortcut-icon" aria-hidden="true">' + ({ games: '◈', 'study-guides': '▤', interactive: '⟡' }[category]) + '</span>' +
          '<span class="generator-shortcut-copy"><strong>' + label + '</strong>' +
          (!compact ? '<small>' + ({ games: 'Interactive challenges and team review.', 'study-guides': 'Flashcards, practice tests, and reference sheets.', interactive: 'Hands-on tools with printable reflection worksheets.' }[category]) + '</small>' : '') +
          '</span></a></li>';
      }).join('') + '</ul></div>';
  }
  function unitPager(c, u) {
    var list = c.units.filter(function (x) { return c.planned || x === u || x.artifacts.length || c.id === 'geometry' || c.id === 'prealgebra' || c.id === 'prealgebra7' || c.id === 'math6' || c.id === 'math5' || c.id === 'algebra2'; });
    var i = list.indexOf(u);
    if (list.length < 2) return '';
    function link(t, dir) {
      if (!t) return '<span class="pager-spot"></span>';
      var arrow = '<span class="pager-arrow" aria-hidden="true">' + (dir === 'prev' ? '&larr;' : '&rarr;') + '</span>';
      var text = '<span class="pager-text"><span class="pager-dir">' + (dir === 'prev' ? 'Previous unit' : 'Next unit') + '</span>' +
        '<span class="pager-name">' + esc(unitLabel(c, t)) + '</span></span>';
      return '<a class="pager-link pager-' + dir + '" href="' + href(unitToken(c, t)) + '" rel="' + dir + '">' +
        (dir === 'prev' ? arrow + text : text + arrow) + '</a>';
    }
    return '<nav class="unit-pager" data-color="' + esc(c.color || '') + '" data-course="' + esc(c.id) + '" aria-label="Unit navigation">' +
      link(list[i - 1], 'prev') + link(list[i + 1], 'next') + '</nav>';
  }
  function algebraUnitView(c, u) {
    var items = u.artifacts.map(function (a) { return { a: a, c: c, u: u }; });
    var gameFormats = RESOURCE_GROUPS.filter(function (g) { return g.id === 'games'; })[0].formats;
    var guideFormats = RESOURCE_GROUPS.filter(function (g) { return g.id === 'study-guides'; })[0].formats;
    var interactiveFormats = RESOURCE_GROUPS.filter(function (g) { return g.id === 'interactive'; })[0].formats;
    var practiceFormats = RESOURCE_GROUPS.filter(function (g) { return g.id === 'practice'; })[0].formats;
    // Unit pages must expose the online practice test directly, just like the global directory.
    // Keep one card per unit even when older cached catalogs or format filters are in use.
    var hasPractice = c.id === 'geometry' || items.some(function(it){return /practice-test[.]html/i.test(it.a.path||'');});
    if (!hasPractice) {
      var unitMap = {'foundations-algebra':'algebra1-foundations','expressions-equations':'algebra1-expressions-equations','inequalities':'algebra1-inequalities','relations-functions':'algebra1-relations-functions','linear-equations-slope':'algebra1-linear-equations-slope','systems-of-equations':'algebra1-systems-of-equations','exponents-exponential-functions':'algebra1-exponents-scientific-notation','exponential-functions':'algebra1-exponential-functions','polynomials-factoring':'algebra1-polynomials','factoring-zero-product':'algebra1-factoring-zero-product','quadratics':'algebra1-quadratics','statistics-data-modeling':'algebra1-statistics-data-modeling'};
      if(unitMap[u.id]) items.push({a:{title:'Interactive Practice Test',path:'worksheet-generator/practice-test.html#unit='+unitMap[u.id],thumb:'thumbs/practice-test.svg',description:'Online practice assessment with worked solutions and targeted skill review.',type:'Study Guide'},c:c,u:u});
    }
    function category(id, title, formats) {
      var matches = items.filter(function (it) { return formats.indexOf(activityFormat(it.a)) >= 0; });
      // Include the practice test deterministically in each supported Algebra 1 unit.
      // Use the same card renderer and thumbnail as the other study guides.
      if (id === 'study-guides') {
        var current = items.filter(function (it) { return /practice-test[.]html/i.test(it.a.path || ''); });
        if (current.length && !matches.some(function (it) { return /practice-test[.]html/i.test(it.a.path || ''); })) matches.push(current[0]);
      }
      if (!matches.length) return '';
      matches = sortByActivityOrder(matches);
      return '<section class="algebra-unit-section" aria-labelledby="algebra-' + id + '">' +
        '<h2 id="algebra-' + id + '">' + esc(title) + '</h2>' +
        '<ul class="cards grouped-cards">' + matches.map(function (it) { return cardHtml(it, false, true); }).join('') + '</ul>' +
        '</section>';
    }
    var inner = crumbs([['Home', '#'], [c.name, href(courseToken(c))], [unitLabel(c, u), null]]) +
      '<h1 tabindex="-1">' + esc(unitLabel(c, u)) + '</h1>' +
      '<p class="band-meta">Create custom resources or explore games and study guides for this unit.</p>';
    return {
      title: unitLabel(c, u) + ', ' + c.name,
      html: bandHtml(c, inner, 'unit') +
        '<section class="section"><div class="wrap algebra-unit-layout">' + unitPager(c, u) +
        generatorLinks(c, u, true) +
        category('games', 'Games', gameFormats) +
        category('study-guides', 'Study Guides', guideFormats) +
        category('interactive', 'Interactive Math', interactiveFormats) +
        category('practice', 'Practice Activities', practiceFormats) +
        category('projects', 'Projects', ['projects']) +
        unitPager(c, u) + '</div></section>'
    };
  }

  function contentReadinessSection(c, u) {
    var list = [
      ['flashcards', 'Flashcards'], ['connect-4', 'Connect 4'],
      ['tic-tac-toe', 'Tic-Tac-Toe'], ['picture-reveal', 'Picture Reveal'],
      ['showdown', 'Showdown'], ['detective', 'Detective'],
      ['escape-room', 'Escape Rooms'], ['worksheets', 'Worksheets'],
      ['assessments', 'Assessments'], ['readiness-check', 'Assessment Readiness Check']
    ];
    var adapter = window.MK_RESOURCE_ELIGIBILITY;
    return '<section class="algebra-unit-section"><h2>Content readiness</h2>' +
      '<p class="course-skill-hint">These resources use the shared Algebra 2 bank. Games use existing multiple-choice items; availability varies by skill and difficulty.</p>' +
      '<div class="resource-readiness-grid">' + list.map(function (item) {
        var status = adapter.describe(item[0], c.id, u.id);
        return '<div class="resource-readiness-row"><strong>' + esc(item[1]) + '</strong><span>' +
          (status.ready ? status.count + ' approved questions' : 'Awaiting approved questions') + '</span>' +
          (status.ready ? '<a href="' + esc((function(){
            var games={'flashcards':'flashcards','connect-4':'connect-four','tic-tac-toe':'tic-tac-toe','picture-reveal':'picture-reveal','showdown':'showdown','detective':'detective','escape-room':'escape-room'};
            if(games[item[0]])return 'worksheet-generator/'+(['detective','escape-room'].includes(games[item[0]])?'course-activity':'course-game')+'.html?course='+c.id+'&unit='+u.id+'&game='+games[item[0]]+'&v=showdown-fix-20261031';
            if(item[0]==='readiness-check')return 'worksheet-generator/algebra2-practice.html?unit='+u.id;
            return 'worksheet-generator/'+(item[0]==='assessments'?'menu-assessment.html':'worksheet.html')+'#unit=algebra2-'+u.id;
          })()) + '">Open resource</a>' : '') + '</div>';
      }).join('') + '</div></section>';
  }
  function contentBriefSection(c, u) {
    var skills = window.MK_COURSE_CATALOG.getSkillRecords(c.id, u.id);
    return '<section class="algebra-unit-section"><h2>Lessons and Subskills</h2>' +
      '<p class="course-skill-hint">Select lessons for a content brief. <a href="coverage.html?course=' + encodeURIComponent(c.id) + '">View course question coverage</a>.</p>' +
      '<div class="course-skill-actions"><button type="button" class="course-skill-select" data-skill-action="all">Select all</button><button type="button" class="course-skill-select" data-skill-action="none">Clear</button><button type="button" class="course-skill-select" data-skill-action="copy">Copy content brief</button><span class="course-skill-status" role="status" aria-live="polite"></span></div>' +
      '<ol class="course-skill-checklist" data-course-id="' + esc(c.id) + '" data-unit-id="' + esc(u.id) + '">' + skills.map(function (s) {return '<li><label><input type="checkbox" value="' + esc(s.id) + '" checked><span>' + esc(s.name) + '</span></label></li>';}).join('') + '</ol></section>';
  }
  function gradePracticeLinks(c, u) {
    var crosswalk = window.MK_SKILL_CROSSWALK;
    if (!crosswalk || typeof crosswalk.matches !== 'function') return '';
    var topics = crosswalk.matches().filter(function (m) {
      return m.targets.some(function (t) { return t && t.courseId === c.id && t.unitId === u.id; });
    });
    if (!topics.length) return '';
    var base = 'worksheet-generator/', common = '?course=' + encodeURIComponent(c.id) + '&unit=' + encodeURIComponent(u.id);
    var first = topics[0].key;
    var practice = base + 'grade-practice.html?course=' + encodeURIComponent(c.id) + '&topic=' + encodeURIComponent(first) + '&level=cp1';
    var games = topics.flatMap(function(m) {
      var target=m.targets.find(function(t){return t&&t.courseId===c.id&&t.unitId===u.id;});
      return [
        {mode:'tic-tac-toe',title:'Tic-Tac-Toe',thumb:'thumbs/foundations-algebra-tic-tac-toe.jpg'},
        {mode:'connect-four',title:'Connect 4',thumb:'thumbs/foundations-algebra-connect-four.jpg'},
        {mode:'picture-reveal',title:'Picture Reveal',thumb:'thumbs/foundations-algebra-picture-reveal.jpg'},
        {mode:'showdown',title:'Showdown',thumb:'thumbs/foundations-algebra-showdown.jpg'}
      ].map(function(item){
        var formatDetails = {
          'tic-tac-toe': 'Tic-Tac-Toe for two teams. Answer a multiple-choice problem to claim a square; a wrong answer lets the other team steal.',
          'connect-four': 'Teams solve problems to place discs and connect four in a row.',
          'picture-reveal': 'Answer questions correctly to uncover a hidden picture.',
          'showdown': 'Choose a category and point value, solve a problem, and reveal the answer.',
          'flashcards': 'Flip cards to reveal answers and worked solutions. Shuffle and review missed problems.'
        };
        return {title:target.name+' '+item.title,
          path:base+'middle-school-game.html?course='+encodeURIComponent(c.id)+'&topic='+encodeURIComponent(m.key)+'&game='+item.mode,
          thumb:item.thumb,type:item.mode==='flashcards'?'Study Guide':'Game',
          description:formatDetails[item.mode]};
      });
    });
    var guides = [
      ...topics.map(function(m) {
        var target=m.targets.find(function(t){return t&&t.courseId===c.id&&t.unitId===u.id;});
        return {title:target.name+' Flashcards',
          path:base+'middle-school-game.html?course='+encodeURIComponent(c.id)+'&topic='+encodeURIComponent(m.key)+'&game=flashcards',
          thumb:'thumbs/foundations-algebra-flashcards.jpg',type:'Study Guide',
          description:'Flip cards for answers and worked solutions, shuffle and practice missed questions.'};
      }),
      {title:'Interactive Practice',path:practice+'&mode=practice',
       thumb:'thumbs/practice-test.svg',type:'Study Guide',description:'Answer questions online with immediate feedback. Select a lesson topic and difficulty.'}
    ];
    var printables = [
      {title:'Draft Practice Worksheets',path:practice+'&mode=worksheet',
       thumb:'thumbs/worksheet-generator-expressions-equations.svg',type:'Worksheet',description:'Teacher-preview worksheet from the mapped legacy question bank. Review mathematics and grade suitability before using.'}
    ];
    function group(title, resources) {
      return '<section class="algebra-unit-section"><h2>' + esc(title) + '</h2>' +
        '<ul class="cards grouped-cards">' + resources.map(function (a) { return cardHtml({a:a,c:c,u:u},false,true); }).join('') + '</ul></section>';
    }
    var lessons = '<section class="algebra-unit-section"><h2>Practice by Lesson</h2>' +
      '<p class="course-skill-hint">Open the matching topic in a resource. The shared question generators currently cover these lessons.</p>' +
      '<ul class="unit-skills">' + topics.map(function(m) {
        var target = m.targets.find(function(t) { return t && t.courseId === c.id && t.unitId === u.id; });
        return '<li class="unit-skill"><a href="' +
          esc(base+'grade-practice.html?course='+encodeURIComponent(c.id)+'&topic='+encodeURIComponent(m.key)+'&level=cp1') +
          '">' + esc(target.name) + '</a></li>';
      }).join('') + '</ul></section>';
    return group('Games', games) + group('Study Guides',guides) + group('Printable Resources',printables) + lessons;
  }
  function unitView(c, u) {
    if (c.planned) {
      var outline = window.MK_COURSE_CATALOG.getSkills(c.id, u.id);
      var heading = crumbs([['Home', '#'], [c.name, href(courseToken(c))], [unitLabel(c, u), null]]) +
        '<h1 tabindex="-1">' + esc(unitLabel(c, u)) + '</h1><p class="band-meta">Course outline · Activities coming soon</p>';
      return { title: unitLabel(c, u) + ', ' + c.name,
        html: bandHtml(c, heading, 'unit') + '<section class="section"><div class="wrap">' + unitPager(c, u) +
          '<h2>Topics in this unit</h2><ul class="unit-skills">' + outline.map(function (skill) {
            return '<li class="unit-skill">' + esc(skill) + '</li>';
          }).join('') + '</ul><div class="empty"><h2>Activities coming soon</h2>' +
          '<p>Lessons, games, and practice resources will be added as this course is built out.</p></div>' +
          unitPager(c, u) + '</div></section>' };
    }
    if (c.id === 'prealgebra' || c.id === 'prealgebra7' || c.id === 'math6' || c.id === 'math5' || c.id === 'precalculus' || c.id === 'calculus' || c.id === 'statistics' || c.id === 'discrete') return algebraUnitView(c, u);
    if (c.id === 'prealgebra' || c.id === 'prealgebra7' || c.id === 'math6') {
      var skills = window.MK_COURSE_CATALOG.getSkillRecords(c.id, u.id);
      var intro = crumbs([['Home', '#'], [c.name, href(courseToken(c))], [unitLabel(c, u), null]]) +
        '<h1 tabindex="-1">' + esc(unitLabel(c, u)) + '</h1>' +
        '<p class="band-meta">' + skills.length + ' lessons · ' + esc(c.name) + ' curriculum</p>';
      return { title: unitLabel(c, u) + ', ' + c.name,
        html: bandHtml(c, intro, 'unit') + '<section class="section"><div class="wrap algebra-unit-layout">' +
          unitPager(c, u) + gradePracticeLinks(c, u) +
          unitPager(c, u) + '</div></section>' };
    }
    if (c.id === 'algebra' || c.id === 'geometry' || c.id === 'algebra2' || c.id === 'precalculus' || c.id === 'calculus' || c.id === 'statistics' || c.id === 'discrete') return algebraUnitView(c, u);
    var items = u.artifacts.map(function (a) { return { a: a, c: c, u: u }; });
    var planner = u.artifacts.filter(function (a) { return activityFormat(a) === 'lesson-planner'; })[0];
    var generator = u.artifacts.filter(function (a) { return activityFormat(a) === 'worksheet-generator'; })[0];
    var menuGen = u.artifacts.filter(function (a) { return activityFormat(a) === 'assessment-generator'; })[0];
    var inner =
      crumbs([['Home', '#'], [c.name, href(courseToken(c))], [unitLabel(c, u), null]]) +
      '<h1 tabindex="-1">' + esc(unitLabel(c, u)) + '</h1>' +
      '<p class="band-meta">' + (items.length ? acts(items.length) : 'Coming soon') + '</p>' +
      (planner ? '<div class="unit-generator"><a class="btn" href="' + esc(activityUrl(planner)) + '">Plan a lesson</a><p>Pick any day of this unit: objectives, vocabulary, Do Now, notes, practice and exit ticket, printed as a student handout and a teacher key.</p></div>' : '') +
      (generator ? '<div class="unit-generator"><a class="btn" href="' + esc(activityUrl(generator)) + '">Create a worksheet</a><p>Practice with short-answer or multiple-choice questions. Choose skills and CP2, CP1 or Honors difficulty; prints with an answer key.</p></div>' : '') +
      (menuGen ? '<div class="unit-generator"><a class="btn" href="' + esc(activityUrl(menuGen)) + '">Build an assessment</a><p>A standard test (multiple choice and short answer) or a choice menu. Choose skills and CP2, CP1 or Honors difficulty, then edit every problem before you print.</p></div>' : '');
    return {
      title: unitLabel(c, u) + ', ' + c.name,
      html: bandHtml(c, inner, 'unit') +
        '<section class="section"><div class="wrap">' + unitPager(c, u) +
        (items.length ? chipsHtml(items) + groupedCardsHtml(items, false)
                      : '<div class="empty"><h2>Coming soon</h2><p>No activities in this unit yet. <a href="' + href(courseToken(c)) + '">Back to ' + esc(c.name) + '</a></p></div>') +
        unitPager(c, u) + '</div></section>'
    };
  }


  function browseState(defaultFormat) {
    var params = new URLSearchParams(token.split('?')[1] || '');
    return { subject: params.get('subject') || '', unit: params.get('unit') || '', category: params.get('category') || '', gameMode: params.get('gameMode') || '',
      format: params.get('format') || defaultFormat || '', page: Math.max(1, parseInt(params.get('page'), 10) || 1) };
  }
  function browseToken(state) {
    var params = new URLSearchParams();
    ['subject', 'unit', 'category', 'format', 'gameMode'].forEach(function (key) { if (state[key]) params.set(key, state[key]); });
    if (state.page > 1) params.set('page', state.page);
    return 'activities' + (params.toString() ? '?' + params.toString() : '');
  }
  function browseResults(state) {
    return everything().filter(function (it) {
      return (!state.subject || it.c.id === state.subject) &&
        (!state.unit || unitToken(it.c, it.u) === state.unit) &&
        (!state.category || RESOURCE_GROUPS.some(function (g) { return g.id === state.category && belongsToGroup(it.a, g); })) &&
        (!state.format || activityFormat(it.a) === state.format) &&
        (!state.gameMode || gameMode(it.a) === state.gameMode);
    });
  }
  function browseSelect(id, label, choices, selected, allLabel) {
    return '<label for="browse-' + id + '">' + label +
      '<select id="browse-' + id + '" data-browse="' + id + '"><option value="">' + allLabel + '</option>' +
      choices.map(function (choice) { return '<option value="' + esc(choice.id) + '"' +
        (choice.id === selected ? ' selected' : '') + '>' + esc(choice.name) + '</option>'; }).join('') +
      '</select></label>';
  }
  function activityIndexView(defaultFormat) {
    var state = browseState(defaultFormat);
    var unitChoices = [];
    L.courses.forEach(function (c) {
      if (state.subject && state.subject !== c.id) return;
      c.units.forEach(function (u) { if (u.artifacts.some(listed)) unitChoices.push({
        id: unitToken(c, u), name: (state.subject ? '' : c.name + ' — ') + unitLabel(c, u)
      }); });
    });
    var formats = [];
    // Only offer formats in the selected category (e.g. games, not worksheets).
    RESOURCE_GROUPS.filter(function (g) { return !state.category || g.id === state.category; }).forEach(function (group) {
      group.formats.forEach(function (id) {
        var format = ACTIVITY_FORMATS.filter(function (f) { return f.id === id; })[0];
        if (format && formatItems(format).length) formats.push(format);
      });
    });
    var items = sortByActivityOrder(browseResults(state));
    var pages = Math.max(1, Math.ceil(items.length / 24));
    state.page = Math.min(state.page, pages);
    var offset = (state.page - 1) * 24;
    var visible = items.slice(offset, offset + 24);
    var controls = '<div class="browse-filters" role="group" aria-label="Filter activities">' +
      browseSelect('subject', 'Subject', L.courses, state.subject, 'All subjects') +
      browseSelect('unit', 'Unit', unitChoices, state.unit, 'All units') +
      browseSelect('category', 'Category', RESOURCE_GROUPS.map(function (g) { return { id: g.id, name: g.name }; }), state.category, 'All categories') +
      browseSelect('format', 'Activity Type', formats, state.format, 'All activity types') +
      ((state.category === 'games' || state.gameMode) ? browseSelect('gameMode', 'Game Mode', GAME_MODES.map(function (name) { return { id: name, name: name }; }), state.gameMode, 'All game modes') : '') +
      '<button type="button" class="btn browse-clear" id="browse-clear">Clear filters</button></div>';
    var pager = '';
    if (pages > 1) {
      var previous = Object.assign({}, state, { page: state.page - 1 });
      var next = Object.assign({}, state, { page: state.page + 1 });
      pager = '<nav class="browse-pagination" aria-label="Results pages">' +
        (state.page > 1 ? '<a class="btn" href="' + esc(href(browseToken(previous))) + '">Previous</a>' : '') +
        '<span>Page ' + state.page + ' of ' + pages + '</span>' +
        (state.page < pages ? '<a class="btn" href="' + esc(href(browseToken(next))) + '">Next</a>' : '') + '</nav>';
    }
    return {
      title: 'Browse activities',
      html: bandHtml(null, crumbs([['Home', '#'], ['Activities', null]]) +
        '<h1 tabindex="-1">Browse activities</h1><p class="band-blurb">Choose a subject, unit, or activity type to find what you need.</p>') +
        '<section class="section"><div class="wrap">' + controls +
        '<p class="browse-count" role="status" aria-live="polite">' + acts(items.length) +
        (items.length ? ' · Showing ' + (offset + 1) + '–' + (offset + visible.length) : '') + '</p>' +
        (visible.length ? '<ul class="cards grouped-cards">' + visible.map(function (it) { return cardHtml(it, true, true); }).join('') + '</ul>' :
          '<div class="empty"><h2>No matching activities</h2><p>Try a different activity type or clear the filters to browse everything.</p></div>') +
        pager + '</div></section>'
    };
  }
  function activityView(format) { return activityIndexView(format.id); }

  function savedView() {
    var items = everything().filter(function (it) { return isSaved(it.a.path); });
    var inner = crumbs([['Home', '#'], ['Saved', null]]) + '<h1 tabindex="-1">Saved activities</h1>' +
      '<p class="band-meta">' + acts(items.length) + '</p>' +
      '<p class="band-blurb">Saved activities are stored in this browser. <a href="backup.html">Export or import your saved work</a> to move it between devices.</p>';
    return {
      title: 'Saved activities',
      html: bandHtml(null, inner) +
        '<section class="section"><div class="wrap">' +
        (items.length ? chipsHtml(items) + cardsHtml(items, true)
                      : '<div class="empty"><h2>Nothing saved yet</h2><p>Choose Save on any activity and it will be listed here. Saved activities stay in this browser.</p></div>') +
        '</div></section>'
    };
  }


  function searchWords(text) {
    return String(text || '').toLowerCase().replace(/flash\s+cards/g, 'flashcards')
      .replace(/connect\s*(?:four|4)/g, 'connect4').replace(/algebra\s*1/g, 'algebra1')
      .replace(/algebra\s*2/g, 'algebra2').replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function searchView(text) {
    var terms = searchWords(text).split(/\s+/).filter(Boolean);
    var items = everything().filter(function (it) {
      var format = ACTIVITY_FORMATS.filter(function (f) { return f.id === activityFormat(it.a); })[0];
      var hay = searchWords([it.a.title, it.a.description, it.u.name, 'unit ' + unitNum(it.c, it.u), it.c.name, format ? format.name : '']
        .concat(toArr(it.a.type), toArr(it.a.level), toArr(it.a.topics)).join(' '));
      return terms.every(function (term) { return hay.indexOf(term) >= 0; });
    });
    items.sort(function (a, b) {
      function score(it) { var title = searchWords(it.a.title); return terms.filter(function (t) { return title.indexOf(t) >= 0; }).length; }
      return score(b) - score(a);
    });
    var inner = crumbs([['Home', '#'], ['Search', null]]) +
      '<h1 tabindex="-1">Results for “' + esc(text) + '”</h1><p class="band-meta" role="status">' +
      acts(applyFilters(items).length) + '</p>';
    return {
      title: 'Search: ' + text,
      html: bandHtml(null, inner) +
        '<section class="section"><div class="wrap"><button class="btn clear-search" type="button" id="clear-search">Clear search</button>' +
        (items.length ? chipsHtml(items) + cardsHtml(items, true) :
          '<div class="empty"><h2>No matches</h2><p>Try a topic such as slope, an activity type such as flashcards, or a subject such as Algebra 1.</p><p><a href="#activities">Browse with subject, unit, and activity filters</a></p></div>') +
        '</div></section>'
    };
  }

  function soonView(c) {
    return {
      title: c.name + ': coming soon',
      html: bandHtml(c, '<h1 tabindex="-1">' + esc(c.name) + '</h1>') +
        '<section class="section"><div class="wrap"><div class="empty"><h2>Coming soon</h2><p>' + esc(c.name) + ' activities are being rebuilt in the same style as Algebra 1. <a href="#algebra">Browse Algebra 1</a> in the meantime.</p></div></div></section>'
    };
  }
  function notFoundView() {
    return {
      title: 'Page not found',
      html: bandHtml(null, '<h1 tabindex="-1">Page not found</h1>') +
        '<section class="section"><div class="wrap"><div class="empty"><h2>That page does not exist</h2><p><a href="#">Go to the home page</a> and choose a course.</p></div></div></section>'
    };
  }

  function resolve(t) {
    t = t.split('?')[0];
    if (!t) return { name: 'home' };
    if (t === 'saved') return { name: 'saved' };
    if (t === 'activities') return { name: 'activities' };
    if (t.indexOf('activity.') === 0) {
      var format = ACTIVITY_FORMATS.filter(function (f) { return f.id === t.slice(9); })[0];
      return format ? { name: 'activity', format: format } : { name: 'nf' };
    }
    var parts = t.split('.');
    var c = L.courses.filter(function (x) { return x.id === parts[0]; })[0];
    var hid = SOON.filter(function (x) { return x.id === parts[0]; })[0];
    if (!c && hid) return { name: 'soon', c: hid };
    if (!c) return { name: 'nf' };
    if (!parts[1]) return { name: 'course', c: c };
    var u = c.units.filter(function (x) { return x.id === parts[1]; })[0];
    return u ? { name: 'unit', c: c, u: u } : { name: 'nf' };
  }

  /* ---------- render ---------- */
  function updateNav(r) {
    var expanded = r && r.name === 'home';
    var courses = L.courses.concat(SOON).slice().sort(function (a, b) {
      return (courseOrder[a.id] == null ? 99 : courseOrder[a.id]) - (courseOrder[b.id] == null ? 99 : courseOrder[b.id]);
    });
    var cards = courses.map(function (c) {
      var current = r && r.c && r.c.id === c.id;
      var soon = c.comingSoon || c.planned;
      return '<a class="course-nav-card" data-course="' + esc(c.id) + '" data-color="' + esc(c.color || '') + '" href="' + href(courseToken(c)) + '"' +
        (current ? ' aria-current="page"' : '') + '><span class="course-nav-copy"><strong>' + esc(c.name) + '</strong>' +
        '<small>' + (soon ? 'Coming soon · course outline' : units(c.units.length) + ' · Explore resources') + '</small></span>' + artFor(c) + '</a>';
    }).join('');
    cards += '<a class="course-nav-card" data-course="financial-algebra" data-color="purple" href="financial-algebra.html">' +
      '<span class="course-nav-copy"><strong>Financial Algebra</strong><small>10 units · Activities, study guides &amp; projects</small></span>' +
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true"><rect class="f-soft" x="20" y="25" width="150" height="110" rx="12"/>' +
      '<path class="s" d="M40 110 L75 85 L105 95 L150 50"/><circle class="f" cx="158" cy="33" r="25"/>' +
      '<text x="158" y="44" text-anchor="middle" font-size="32" fill="white" font-family="Arial">$</text></svg></a>';
    var sidebar = expanded && app.querySelector('.course-sidebar');
    if (sidebar) {
      sidebar.appendChild(nav);
      nav.setAttribute('aria-label', 'Courses');
      nav.innerHTML = '<div class="sidebar-heading"><h2>Courses</h2></div><div class="course-nav-grid">' + cards + '</div>';
    } else {
      document.querySelector('.site-header .bar').appendChild(nav);
      nav.setAttribute('aria-label', 'Courses');
      nav.innerHTML = '<details class="course-menu"><summary><span>Courses' +
        (r && r.c ? ' <span class="course-menu-current">/ ' + esc(r.c.name) + '</span>' : '') +
        '</span><span class="course-menu-hint">Choose your course <span aria-hidden="true">⌄</span></span></summary>' +
        '<div class="course-nav-grid">' + cards + '</div></details>';
    }
    if (backBtn) backBtn.hidden = !query && r && r.name === 'home';
  }

  function render(keepFocus) {
    var r = resolve(token);
    var view;
    if (query) view = searchView(query);
    else if (r.name === 'home') view = homeView();
    else if (r.name === 'course') view = courseView(r.c);
    else if (r.name === 'unit') view = unitView(r.c, r.u);
    else if (r.name === 'saved') view = savedView();
    else if (r.name === 'activities') view = activityIndexView();
    else if (r.name === 'activity') view = activityView(r.format);
    else if (r.name === 'soon') view = soonView(r.c);
    else view = notFoundView();

    app.innerHTML = view.html;
    try { document.title = view.title === L.title ? L.title : view.title + ' | ' + L.title; } catch (e) {}
    updateNav(query ? null : r);

    if (focusKey) {
      Array.prototype.forEach.call(app.querySelectorAll('.chip'), function (b) {
        if (b.getAttribute('data-field') + '|' + b.getAttribute('data-val') === focusKey) b.focus();
      });
      focusKey = null;
    } else if (!keepFocus && !firstRender) {
      var h = app.querySelector('h1');
      if (h) h.focus({ preventScroll: true });
      window.scrollTo(0, 0);
    }
    firstRender = false;
  }

  function go(t) {
    token = t;
    query = '';
    q.value = '';
    filters = {};
    try {
      if (location.hash.replace(/^#/, '') !== t) { ignoreHash = true; location.hash = t; }
    } catch (e) { ignoreHash = false; }
    render(false);
  }

  /* ---------- events ---------- */
  document.addEventListener('change', function (e) {
    var key = e.target.getAttribute && e.target.getAttribute('data-browse');
    if (!key) return;
    var route = resolve(token);
    var state = browseState(route.format ? route.format.id : '');
    state[key] = e.target.value;
    state.page = 1;
    if (key === 'subject') state.unit = '';
    if (key === 'category') { state.format = ''; state.gameMode = ''; }
    if (key === 'unit' && state.unit) state.subject = state.unit.split('.')[0];
    go(browseToken(state));
    var control = document.getElementById('browse-' + key);
    if (control) control.focus({ preventScroll: true });
  });

  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('#clear-search')) { go(token); q.focus(); return; }
    var skillButton = e.target.closest ? e.target.closest('[data-skill-action]') : null;
    if (skillButton) {
      var list = app.querySelector('.course-skill-checklist');
      if (!list) return;
      var checks = Array.prototype.slice.call(list.querySelectorAll('input[type="checkbox"]'));
      var action = skillButton.getAttribute('data-skill-action');
      if (action === 'all' || action === 'none') { checks.forEach(function (input) { input.checked = action === 'all'; }); return; }
      if (action === 'copy') {
        var courseId = list.getAttribute('data-course-id'), unitId = list.getAttribute('data-unit-id');
        var records = window.MK_COURSE_CATALOG.getSkillRecords(courseId, unitId);
        var chosen = checks.filter(function (input) { return input.checked; }).map(function (input) { return records.filter(function (s) { return s.id === input.value; })[0]; }).filter(Boolean);
        var status = app.querySelector('.course-skill-status');
        if (!chosen.length) { if (status) status.textContent = 'Select at least one lesson.'; return; }
        var course = L.courses.filter(function (item) { return item.id === courseId; })[0];
        var unit = course && course.units.filter(function (item) { return item.id === unitId; })[0];
        var brief = JSON.stringify({schemaVersion:1,courseId:courseId,courseName:course.name,unitId:unitId,unitName:unit.name,selectedSkills:chosen,difficulties:['cp2','cp1','honors'],formats:['short-answer','multiple-choice','select-all','open-response'],requirements:['Generate verified answers and worked solutions','Multiple-choice answers and distractors must be independently checked','Open-response questions must contain at least four parts','Supply precise diagram specifications where needed','Do not modify existing course question banks'],questionBankSchema:'schemas/question-bank.schema.json'},null,2);
        function fallback() {
          var box = document.createElement('textarea'); box.value = brief; box.style.position = 'fixed'; box.style.opacity = '0'; document.body.appendChild(box); box.select();
          var ok = false; try { ok = document.execCommand('copy'); } catch (_) {}
          document.body.removeChild(box); if (status) status.textContent = ok ? 'Content brief copied.' : 'Copy unavailable in this browser.';
        }
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(brief).then(function(){if(status) status.textContent='Content brief copied.';}, fallback);
        else fallback();
        return;
      }
    }
    if (e.target.closest && e.target.closest('#browse-clear')) {
      go('activities');
      var subject = document.getElementById('browse-subject');
      if (subject) subject.focus({ preventScroll: true });
      return;
    }
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (a && !e.metaKey && !e.ctrlKey && !e.shiftKey && a.getAttribute('target') !== '_blank') {
      e.preventDefault();
      var h = a.getAttribute('href').replace(/^#/, '');
      var t = h; try { t = decodeURIComponent(h); } catch (err) {}
      go(t);
      return;
    }

    var s = e.target.closest ? e.target.closest('.save') : null;
    if (s) {
      var path = s.getAttribute('data-path');
      toggleSaved(path);
      var r = resolve(token);
      if (!query && r.name === 'saved') {
        render(true);
        var first = app.querySelector('.save');
        if (first) first.focus(); else { var h1 = app.querySelector('h1'); if (h1) h1.focus({ preventScroll: true }); }
        return;
      }
      Array.prototype.forEach.call(document.querySelectorAll('.save'), function (b) {
        if (b.getAttribute('data-path') !== path) return;
        var on = isSaved(path);
        b.setAttribute('aria-pressed', on);
        b.innerHTML = (on ? STAR_ON : STAR) + '<span>' + (on ? 'Saved' : 'Save') + '</span>';
      });
      updateNav(query ? null : r);
      return;
    }

    var c = e.target.closest ? e.target.closest('.chip') : null;
    if (c) {
      var field = c.getAttribute('data-field'), val = c.getAttribute('data-val');
      if (val) filters[field] = val; else delete filters[field];
      focusKey = field + '|' + val;
      render(true);
      return;
    }


  });

  document.getElementById('searchForm').addEventListener('submit', function (e) { e.preventDefault(); });
  /* Back: the previous page in this tab (course, unit, browse page or search); home when there is none. */
  var backBtn = document.getElementById('backBtn');
  if (backBtn) backBtn.addEventListener('click', function () {
    var fromSite = document.referrer && document.referrer.indexOf(location.origin) === 0;
    if (history.length > 1 && (fromSite || (history.state && history.state.mk) || sessionStorageGet())) history.back();
    else if (location.hash && location.hash !== '#') location.hash = '';
    else history.back();
  });
  function sessionStorageGet() { try { return sessionStorage.getItem('mk-nav') === '1'; } catch (e) { return false; } }
  window.addEventListener('hashchange', function () { try { sessionStorage.setItem('mk-nav', '1'); } catch (e) { /* ignore */ } });
  q.addEventListener('input', function () {
    query = q.value.trim();
    filters = {};
    render(true);
  });
  q.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && q.value) { q.value = ''; query = ''; filters = {}; render(true); }
  });
  skip.addEventListener('click', function () { app.focus(); });

  window.addEventListener('hashchange', function () {
    if (ignoreHash) { ignoreHash = false; return; }
    var t = location.hash.replace(/^#/, '');
    try { t = decodeURIComponent(t); } catch (e) {}
    if (t === token && !query) return;
    token = t; query = ''; q.value = ''; filters = {};
    render(false);
  });

  window.addEventListener('mk-banks-ready', function () { if (!query && resolve(token).name === 'unit') render(true); });

  /* ---------- start ---------- */
  (function init() {
    var foot = document.getElementById('foot');
    if (foot) foot.textContent = L.footer || '';
    var bn = document.getElementById('brandName');
    if (bn) bn.textContent = L.title.replace(/'/g, '’');
    var t = '';
    try { t = decodeURIComponent(location.hash.replace(/^#/, '')); } catch (e) {}
    token = t;
    render(true);
  })();
})();


