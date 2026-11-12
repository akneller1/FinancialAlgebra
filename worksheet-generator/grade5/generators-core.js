/* Grade 5 generator engine (pure logic, no DOM).
   Builds lesson plans, worksheets, assessments and printable activities from the
   approved math5 question banks. Every question, answer and worked step comes from
   the bank; activity distractors come only from the verified distractor list.
   Deterministic: the same options + seed always produce the same handout. */
(function (G) {
  'use strict';

  var LEVELS = [['cp2', 'Remedial'], ['cp1', 'Standard'], ['honors', 'Advanced']];
  var FORMATS = {
    mixed: 'Mixed review',
    'multiple-choice': 'Multiple choice',
    'short-answer': 'Short answer',
    'select-all': 'Select all that apply',
    'open-response': 'Open response',
    diagrams: 'Questions with diagrams'
  };
  var ACTIVITIES = {
    maze: { name: 'Maze', icon: '🧭', count: 12, blurb: 'Solve each room and choose the door with the correct answer to move on.' },
    color: { name: 'Color by Number', icon: '🎨', count: 12, blurb: 'Solve each problem, then color every shape that shows your answer.' },
    matching: { name: 'Matching', icon: '🔗', count: 10, blurb: 'Match each problem to its answer. Write the answer letter on the line.' },
    stations: { name: 'Station Work', icon: '🚉', count: 12, blurb: 'Four short station tasks for rotating groups, with a recording sheet.' },
    error: { name: 'Error Analysis', icon: '🔎', count: 8, blurb: 'A classmate made a mistake. Find it, explain it and solve correctly.' },
    partner: { name: 'Partner Check', icon: '🤝', count: 12, blurb: 'Partners solve different problems that share the same answer, then compare.' }
  };
  var LESSON_SECTIONS = [
    ['objectives', 'Learning goals', 0, true],
    ['vocabulary', 'Key vocabulary', 0, true],
    ['warmup', 'Warm-up', 3, true],
    ['teach', 'Teach and model', 2, true],
    ['guided', 'Guided practice', 4, true],
    ['practice', 'Independent practice', 6, true],
    ['challenge', 'Challenge', 2, false],
    ['summary', 'Lesson summary', 0, true],
    ['exit', 'Exit ticket', 2, true],
    ['differentiation', 'Differentiation', 0, false]
  ];

  function rng(seed) {
    var a = 0;
    String(seed == null ? 'A' : seed).split('').forEach(function (c) { a = Math.imul(a ^ c.charCodeAt(0), 2654435761) >>> 0; });
    return function () {
      a += 0x6D2B79F5;
      var t = Math.imul(a ^ a >>> 15, 1 | a);
      t ^= t + Math.imul(t ^ t >>> 7, 61 | t);
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function shuffle(list, r) {
    list = list.slice(); r = r || rng('S');
    for (var i = list.length - 1; i > 0; i--) { var j = Math.floor(r() * (i + 1)), t = list[i]; list[i] = list[j]; list[j] = t; }
    return list;
  }
  function clone(x) { return JSON.parse(JSON.stringify(x)); }
  function clamp(x, lo, hi) { x = Number(x); if (!isFinite(x)) x = lo; return Math.max(lo, Math.min(hi, Math.round(x))); }
  function plain(s) { return String(s == null ? '' : s).replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim(); }
  function norm(s) { return plain(s).toLowerCase().replace(/[−–]/g, '-').replace(/,/g, '').replace(/\s+/g, ' ').trim(); }
  function unique(list) { var seen = {}; return list.filter(function (x) { var k = norm(x); if (!k || seen[k]) return false; seen[k] = true; return true; }); }
  function answerText(q) {
    if (Array.isArray(q.answer)) return q.answer.join('; ');
    return String(q.answer == null ? '' : q.answer);
  }
  function levelName(id) { var hit = LEVELS.filter(function (l) { return l[0] === id; })[0]; return hit ? hit[1] : 'Mixed levels'; }

  function options(over) {
    var base = {
      level: 'cp1', skills: [], format: 'mixed', response: 'mixed', count: 12, total: 50,
      notes: 'guided', worked: true, space: 'standard', title: '', version: 'A', showPoints: true,
      showStandards: true, showName: true, timeLimit: '', showHints: false,
      activity: 'maze', theme: 'space', color: true, duration: 60,
      sections: LESSON_SECTIONS.map(function (s) { return { id: s[0], count: s[2], on: s[3] }; })
    };
    var out = Object.assign(base, over || {});
    if (over && over.groups) out.groups = questionGroups(over);
    out.sections = (over && over.sections ? over.sections : base.sections).map(function (s) { return Object.assign({}, s); });
    return out;
  }

  // Ordered question groups are the shared elementary printable contract.
  function questionGroups(o) {
    var input = Array.isArray(o.groups) && o.groups.length ? o.groups :
      [{ format: o.format || 'mixed', response: o.response || 'mixed', count: o.count == null ? 12 : o.count }];
    return input.slice(0, 12).map(function (g) {
      return { format: Object.prototype.hasOwnProperty.call(FORMATS, g.format) ? g.format : 'mixed',
        response: ['mixed', 'multiple-choice', 'short-answer', 'select-all', 'open-response'].indexOf(g.response) >= 0 ? g.response : 'mixed',
        count: clamp(g.count, 1, 30) };
    });
  }
  function groupCount(o) { return questionGroups(o).reduce(function (n, g) { return n + g.count; }, 0); }
  function groupedQuestions(unit, o, seed, used, warnings) {
    var groups = questionGroups(o), chosen = [], candidates = groups.map(function (g) {
      return formatPool(unit, Object.assign({}, o, g)).filter(function (q) { return !used[q.id]; });
    });
    // Reserve restricted pools first; a mixed group must not consume all diagrams.
    groups.map(function (g, i) { return i; }).sort(function (a, b) {
      return candidates[a].length - candidates[b].length || a - b;
    }).forEach(function (i) {
      var g = groups[i];
      chosen[i] = take(candidates[i], g.count, used, seed + '|group|' + i);
      if (chosen[i].length < g.count) warnings.push('Group ' + (i + 1) + ' (' + FORMATS[g.format] + '): ' +
        chosen[i].length + ' of ' + g.count + ' distinct matching questions available. Choose more skills or change the group.');
    });
    return chosen.map(function (items, i) { return { group: groups[i], items: items }; });
  }

  function selectedSkills(unit, o) {
    var all = (unit.skills || []).map(function (s) { return s.id; });
    var picked = (o.skills || []).filter(function (id) { return all.indexOf(id) >= 0; });
    return picked.length ? picked : all;
  }
  function inLevel(q, level) { return !level || level === 'mixed' || q.level === level; }
  function matchesFormat(q, format) {
    if (!format || format === 'mixed') return true;
    if (format === 'diagrams') return !!q.diagram;
    return q.format === format;
  }
  function pool(unit, o) {
    var skills = selectedSkills(unit, o);
    return (unit.questions || []).filter(function (q) { return skills.indexOf(q.skillId) >= 0 && inLevel(q, o.level); });
  }
  function formatPool(unit, o) {
    return pool(unit, o).filter(function (q) { return matchesFormat(q, o.format) && (o.response === 'mixed' || q.format === o.response); });
  }

  /* Balanced selection: take from each skill/format family in turn so no single
     template fills the page. Never repeats a question. */
  function pickQuestions(list, n, seed) {
    var r = rng(seed), groups = {}, out = [], used = {};
    shuffle(list, r).forEach(function (q) {
      var fam = (q.skillId || '') + '|' + (q.format || '');
      (groups[fam] = groups[fam] || []).push(q);
    });
    var fams = shuffle(Object.keys(groups), r);
    while (out.length < n && fams.some(function (f) { return groups[f].length; })) {
      fams.forEach(function (f) {
        if (out.length >= n || !groups[f].length) return;
        var q = groups[f].pop();
        if (!used[q.id]) { used[q.id] = true; out.push(q); }
      });
    }
    return out;
  }

  function allocatePoints(items, total) {
    total = Math.round(total);
    if (!items.length) return [];
    if (total < items.length) throw new RangeError('Total points must be at least the number of questions.');
    var weights = items.map(function (q) {
      return q.format === 'open-response' ? 4 : q.format === 'multiple-choice' ? 1 : 2;
    });
    var sum = weights.reduce(function (a, b) { return a + b; }, 0), left = total - items.length;
    var raw = weights.map(function (w) { return left * w / sum; });
    var out = raw.map(function (v) { return 1 + Math.floor(v); });
    var remain = total - out.reduce(function (a, b) { return a + b; }, 0);
    raw.map(function (v, i) { return { i: i, f: v - Math.floor(v) }; })
      .sort(function (a, b) { return b.f - a.f || a.i - b.i; })
      .slice(0, remain).forEach(function (x) { out[x.i]++; });
    return out;
  }

  function blockQuestion(q) { return { kind: 'question', q: clone(q) }; }
  function take(list, n, used, seed) {
    var avail = list.filter(function (q) { return !used[q.id]; });
    var chosen = pickQuestions(avail, n, seed);
    chosen.forEach(function (q) { used[q.id] = true; });
    return chosen;
  }

  /* ---------------- Lesson plan ---------------- */
  function buildLesson(unit, o, seed) {
    var r = rng(seed), used = {}, sections = [], warnings = [];
    var skills = selectedSkills(unit, o);
    var content = unit.content || {};
    var objectives = skills.map(function (id, i) {
      var idx = (unit.skills || []).map(function (s) { return s.id; }).indexOf(id);
      return (content.objectives && content.objectives[idx]) || ('I can ' + ((unit.skills || [])[idx] || {}).name + '.');
    });
    var all = pool(unit, o);
    var lessons = (unit.skills || []).filter(function (s) { return skills.indexOf(s.id) >= 0; });

    o.sections.filter(function (s) { return s.on; }).forEach(function (sec) {
      var blocks = [];
      if (sec.id === 'objectives') {
        blocks = [{ kind: 'objectives', items: unique(objectives), bigIdea: content.bigIdea || '' }];
      } else if (sec.id === 'vocabulary') {
        blocks = [{ kind: 'vocab', items: clone(content.vocabulary || []) }];
      } else if (sec.id === 'warmup') {
        blocks = take(all.filter(function (q) { return q.format !== 'open-response'; }), sec.count, used, seed + 'w').map(blockQuestion);
      } else if (sec.id === 'teach') {
        var examples = take(all.filter(function (q) { return q.format !== 'open-response' && q.format !== 'select-all'; }), sec.count, used, seed + 't');
        blocks = examples.map(function (q, i) { return { kind: 'example', example: clone(q), n: i + 1 }; });
      } else if (sec.id === 'guided') {
        blocks = take(all.filter(function (q) { return q.format !== 'open-response'; }), sec.count, used, seed + 'g').map(blockQuestion);
      } else if (sec.id === 'practice') {
        blocks = take(all, sec.count, used, seed + 'p').map(blockQuestion);
      } else if (sec.id === 'challenge') {
        blocks = take(all.filter(function (q) { return q.format === 'open-response' || q.format === 'select-all'; }), sec.count, used, seed + 'c').map(blockQuestion);
      } else if (sec.id === 'exit') {
        blocks = take(all.filter(function (q) { return q.format !== 'open-response'; }), sec.count, used, seed + 'e').map(blockQuestion);
      } else if (sec.id === 'summary') {
        blocks = [{ kind: 'reflection', items: [
          'Explain the big idea in your own words: ' + (content.bigIdea || 'What did you learn today?'),
          'Which strategy helped you most today, and why?'
        ] }];
      } else if (sec.id === 'differentiation') {
        blocks = [{ kind: 'differentiation', support: clone(content.support || []), extend: clone(content.extend || []) }];
      }
      if (sec.groups && sec.groups.length && ['warmup', 'guided', 'practice', 'challenge', 'exit'].indexOf(sec.id) >= 0) {
        // Undo the legacy draw before applying this section's explicit groups.
        blocks.forEach(function (b) { delete used[b.q.id]; });
        blocks = groupedQuestions(unit, Object.assign({}, o, { groups: sec.groups }), seed + sec.id, used, warnings)
          .reduce(function (a, g) { return a.concat(g.items.map(function (q) {
            return Object.assign(blockQuestion(q), { group: clone(g.group) });
          })); }, []);
      }
      if (blocks.length) sections.push({ id: sec.id, title: (LESSON_SECTIONS.filter(function (x) { return x[0] === sec.id; })[0] || [sec.id, sec.id])[1], blocks: blocks });
      if (['warmup', 'teach', 'guided', 'practice', 'challenge', 'exit'].indexOf(sec.id) >= 0 && !sec.groups && blocks.length < sec.count) {
        warnings.push('Only ' + blocks.length + ' matching questions were available for ' + sec.id + ' (requested ' + sec.count + ').');
      }
    });
    return {
      mode: 'lesson', unit: unit, options: clone(o), sections: sections, warnings: warnings,
      skills: lessons, objectives: objectives, bigIdea: content.bigIdea || '',
      meta: { duration: o.duration, level: o.level }
    };
  }

  /* ---------------- Worksheet and assessment ---------------- */
  function buildPaper(unit, o, mode, seed) {
    var warnings = [], groups = groupedQuestions(unit, o, seed, {}, warnings);
    var items = groups.reduce(function (a, g) { return a.concat(g.items); }, []);
    var points = mode === 'assessment' ? allocatePoints(items, o.total) : [], n = 0;
    return {
      mode: mode, unit: unit, options: clone(o), warnings: warnings,
      sections: groups.map(function (g, i) {
        return { id: 'questions-' + i, title: groups.length === 1 ?
          (mode === 'assessment' ? 'Assessment questions' : 'Practice questions') :
          'Group ' + (i + 1) + ' · ' + FORMATS[g.group.format],
          blocks: g.items.map(function (q) { return { kind: 'question', q: clone(q), group: clone(g.group), points: points[n++] }; }) };
      })
    };
  }

  /* ---------------- Activities ---------------- */
  function wrongAnswers(q, unit, n) {
    var meta = (unit.meta || {})[q.id] || {}, out = [];
    if (q.options) q.options.forEach(function (o) { if (!o.correct) out.push(o.text); });
    Object.keys(meta.distractors || {}).forEach(function (k) { out.push(k); });
    out = unique(out).filter(function (x) { return norm(x) !== norm(answerText(q)); });
    return out.slice(0, n);
  }
  function activityEligible(q, kind, unit) {
    if (q.format === 'open-response' || !answerText(q).trim()) return false;
    var ans = plain(answerText(q));
    if (ans.length > 24) return false;
    if (kind === 'maze') return wrongAnswers(q, unit, 2).length >= 2 && plain(q.prompt).length <= 150 && !q.diagram;
    if (kind === 'color') return plain(q.prompt).length <= 110;
    if (kind === 'matching') return ans.length <= 20 && plain(q.prompt).length <= 90 && !q.diagram;
    if (kind === 'error') return wrongAnswers(q, unit, 1).length >= 1 && plain(q.prompt).length <= 130;
    if (kind === 'partner') return ans.length <= 24;
    return true;
  }
  function activityPool(unit, o, kind) {
    return pool(unit, o).filter(function (q) { return activityEligible(q, kind, unit); });
  }
  function pairQuestions(list, seed) {
    var groups = {};
    list.forEach(function (q) { var k = norm(answerText(q)); (groups[k] = groups[k] || []).push(q); });
    var pairs = [], r = rng(seed);
    shuffle(Object.keys(groups), r).forEach(function (k) {
      var g = shuffle(groups[k], r);
      while (g.length >= 2) { pairs.push([g.pop(), g.pop()]); }
    });
    return pairs;
  }
  function buildActivity(unit, o, seed) {
    var kind = ACTIVITIES[o.activity] ? o.activity : 'maze';
    var def = ACTIVITIES[kind], r = rng(seed), warnings = [];
    var list = activityPool(unit, o, kind);
    var want = o.count || def.count;
    var plan = { mode: 'activity', kind: kind, name: def.name, icon: def.icon, unit: unit, options: clone(o), warnings: warnings, theme: o.theme, meta: {} };

    if (kind === 'partner') {
      var pairs = pairQuestions(list, seed + 'pair').slice(0, Math.floor(want / 2));
      plan.pairs = pairs.map(function (p, i) { return { n: i + 1, a: clone(p[0]), b: clone(p[1]) }; });
      plan.items = pairs.reduce(function (a, p) { return a.concat(p); }, []).map(clone);
      if (pairs.length < Math.floor(want / 2)) warnings.push('Only ' + pairs.length + ' matched-answer pairs were available for this selection.');
    } else if (kind === 'matching') {
      var used = {}, items = [];
      /* Search the full eligible pool before limiting the set: selecting only
         want questions first can produce needless short matching sheets when
         repeated answer values happen to be drawn. */
      pickQuestions(list, list.length, seed + 'm').forEach(function (q) {
        var k = norm(answerText(q));
        if (!used[k] && items.length < want) { used[k] = true; items.push(q); }
      });
      var answers = shuffle(items.map(function (q) { return answerText(q); }), r);
      plan.items = items.map(clone);
      plan.answers = answers;
      if (items.length < want) warnings.push('Only ' + items.length + ' distinct answers were available; the matching set was shortened.');
    } else if (kind === 'stations') {
      var qs = pickQuestions(list, want, seed + 's');
      var per = Math.ceil(qs.length / 4) || 1;
      plan.stations = [0, 1, 2, 3].map(function (i) {
        return { n: i + 1, items: qs.slice(i * per, i * per + per).map(clone) };
      }).filter(function (s) { return s.items.length; });
      plan.items = qs.map(clone);
      if (qs.length < want) warnings.push(qs.length + ' of ' + want + ' requested station questions were available.');
    } else if (kind === 'error') {
      var eq = pickQuestions(list, want, seed + 'e');
      plan.items = eq.map(function (q) {
        var w = wrongAnswers(q, unit, 1);
        return { q: clone(q), wrong: w[0] || '', reason: ((unit.meta || {})[q.id] || {}).distractors && ((unit.meta || {})[q.id].distractors || {})[w[0]] || 'This answer does not match the correct value.' };
      });
      plan.items = plan.items.filter(function (x) { return x.wrong; });
      if (plan.items.length < want) warnings.push('Only ' + plan.items.length + ' error-analysis prompts were available.');
    } else if (kind === 'color') {
      var seenColorAnswers = {};
      var cq = pickQuestions(list, list.length, seed + 'c').filter(function (q) {
        var answer = norm(answerText(q));
        if (seenColorAnswers[answer]) return false;
        seenColorAnswers[answer] = true;
        return true;
      }).slice(0, Math.max(6, Math.min(12, want)));
      var colors = (G.G5_GENERATOR_CONTENT && G.G5_GENERATOR_CONTENT.colorNames) || [['Red', '#e94b3c'], ['Blue', '#2f7fd8'], ['Green', '#1aa37a'], ['Orange', '#f08c1a'], ['Purple', '#8a4fd6'], ['Yellow', '#f2c94c']];
      var colorSet = colors.slice(0, 6);
      var pattern = [
        [0, 1, 1, 1, 1, 0],
        [1, 2, 3, 3, 2, 1],
        [1, 3, 4, 4, 3, 1],
        [1, 2, 3, 3, 2, 1],
        [0, 1, 2, 2, 1, 0],
        [5, 5, 1, 1, 5, 5]
      ];
      plan.colorItems = cq.map(function (q) { return clone(q); });
      plan.colorSet = colorSet.map(function (c) { return { name: c[0], hex: c[1] }; });
      plan.grid = [];
      for (var row = 0; row < 6; row++) for (var col = 0; col < 6; col++) {
        var ci = pattern[row][col];
        plan.grid.push({ row: row, col: col, color: ci, label: '' });
      }
      /* Two problems share each colour; alternate their answers across the colour's cells. */
      var byColor = [[], [], [], [], [], []];
      plan.colorItems.forEach(function (q, i) { byColor[i % 6].push(q); });
      plan.grid.forEach(function (cell) {
        var choices = byColor[cell.color] || [];
        if (!choices.length) return;
        var q = choices[(cell.row + cell.col) % choices.length];
        cell.label = answerText(q);
        cell.qid = q.id;
      });
      plan.items = plan.colorItems;
      if (cq.length < 12) warnings.push('Only ' + cq.length + ' unique-answer color-by-number problems were available.');
    } else {
      var mq = pickQuestions(list, want, seed + 'z');
      plan.rooms = mq.map(function (q) {
        var wrong = wrongAnswers(q, unit, 2);
        return { n: 0, q: clone(q), doors: shuffle([{ text: answerText(q), correct: true }].concat(wrong.map(function (w) { return { text: w, correct: false }; })), r) };
      });
      plan.rooms.forEach(function (room, i) { room.n = i + 1; });
      plan.items = mq.map(clone);
      if (mq.length < want) warnings.push('Only ' + mq.length + ' maze rooms were available; the maze was shortened.');
    }
    plan.meta.count = plan.items.length;
    plan.meta.level = o.level;
    return plan;
  }

  function build(unit, o, mode, seed) {
    if (mode === 'lesson') return buildLesson(unit, o, seed);
    if (mode === 'activity') return buildActivity(unit, o, seed);
    return buildPaper(unit, o, mode, seed);
  }

  G.G5_GENERATORS_CORE = {
    version: 1, LEVELS: LEVELS, FORMATS: FORMATS, ACTIVITIES: ACTIVITIES, LESSON_SECTIONS: LESSON_SECTIONS,
    rng: rng, shuffle: shuffle, options: options, clamp: clamp, plain: plain, norm: norm, unique: unique,
    answerText: answerText, levelName: levelName, selectedSkills: selectedSkills, pool: pool, formatPool: formatPool,
    questionGroups: questionGroups, groupCount: groupCount, groupedQuestions: groupedQuestions,
    pickQuestions: pickQuestions, allocatePoints: allocatePoints, wrongAnswers: wrongAnswers,
    buildLesson: buildLesson, buildPaper: buildPaper, buildActivity: buildActivity, build: build
  };
})(typeof window !== 'undefined' ? window : globalThis);
