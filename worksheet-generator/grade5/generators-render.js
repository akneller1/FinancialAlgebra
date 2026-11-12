/* HTML renderers for the Grade 5 teacher generators.
   All math strings pass through the shared math display renderer, so fractions,
   exponents and symbols print correctly. Teacher pages add answers and worked steps. */
(function (G) {
  'use strict';
  var Core = G.G5_GENERATORS_CORE;
  var Content = G.G5_GENERATOR_CONTENT || { units: {}, themes: {}, colorNames: [] };

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function rich(s) {
    var text = String(s == null ? '' : s);
    // The shared math display converts slash-form numeric fractions into
    // stacked fractions. Preserve the explicit ÷ operator in pedagogical
    // prompts such as "Write 1 ÷ 7 as a fraction" to avoid tautologies.
    if (G.MK_MATH_DISPLAY) return G.MK_MATH_DISPLAY.html(text);
    return esc(text).replace(/\n/g, '<br>');
  }
  function lines(n) { var out = ''; for (var i = 0; i < n; i++) out += '<div class="g5lines"></div>'; return out; }
  function workLines(o) { return '<div class="g5q-work" style="--g5-space:' + (o.space === 'extra' ? '.95in' : o.space === 'compact' ? '.32in' : '.52in') + '"></div>'; }
  function answerOf(q) { return Array.isArray(q.answer) ? q.answer.join('; ') : String(q.answer == null ? '' : q.answer); }
  function standardsOf(plan) {
    var seen = {}, out = [];
    (plan.sections || []).forEach(function (s) { s.blocks.forEach(function (b) { var q = b.q || b.example; ((q && q.standards) || []).forEach(function (st) { if (!seen[st]) { seen[st] = true; out.push(st); } }); }); });
    (plan.items || []).forEach(function (x) { ((x.standards || (x.q && x.q.standards)) || []).forEach(function (st) { if (!seen[st]) { seen[st] = true; out.push(st); } }); });
    return out.sort();
  }
  function unitLabel(plan) {
    var u = plan.unit, num = u.number ? 'Unit ' + u.number : 'Grade 5';
    return 'GRADE 5 MATH · ' + num + ' · ' + Core.levelName(plan.options.level).toUpperCase();
  }
  function sheetHead(plan, teacher, title, note) {
    var o = plan.options, u = plan.unit;
    var stds = standardsOf(plan);
    return '<header class="g5sh">' +
      '<div class="g5sh-kicker">' + esc(unitLabel(plan)) + (teacher ? ' · TEACHER KEY' : ' · STUDENT HANDOUT') + '</div>' +
      '<h1>' + esc(title || (u.name + ' · ' + Core.FORMATS[o.format])) + '</h1>' +
      (o.showName ? '<div class="g5sh-meta"><span>Name ______________________________</span><span>Date __________ &nbsp; Class ______</span></div>' : '') +
      (note ? '<p class="g5sh-note">' + rich(note) + '</p>' : '') +
      '<div class="g5sh-meta"><span>' + esc(u.name) + '</span><span>Version ' + esc(o.version || 'A') + '</span></div>' +
      (o.showStandards && stds.length ? '<div class="g5standards">Standards: ' + esc(stds.join(' · ')) + '</div>' : '') +
      '</header>';
  }

  function optionList(q, teacher) {
    if (!q.options) return '';
    var one = q.options.every(function (o) { return String(o.text).length > 26; }) ? ' one' : '';
    return '<ul class="g5q-options' + one + '">' + q.options.map(function (o, i) {
      return '<li' + (teacher && o.correct ? ' class="correct"' : '') + '><span class="g5q-letter">' + 'ABCDEF'[i] + '.</span><span>' + rich(o.text) + (teacher && o.correct ? ' ✓' : '') + '</span></li>';
    }).join('') + '</ul>';
  }
  function partsHTML(q, teacher) {
    if (!q.parts) return '';
    return '<ol class="g5q-parts">' + q.parts.map(function (p, i) {
      return '<li><strong>' + 'abcd'[i] + '.</strong> ' + rich(p.prompt) + (teacher ? ' <span class="g5q-key" style="display:inline-block;padding:1px 5px">' + rich(p.answer) + '</span>' : '<span style="display:inline-block;min-width:2.6in;border-bottom:1px solid #33405a">&nbsp;</span>') + '</li>';
    }).join('') + '</ol>';
  }
  function stepsHTML(q) {
    return '<ol class="g5q-steps">' + (q.solutionSteps || []).map(function (s) { return '<li>' + rich(s) + '</li>'; }).join('') + '</ol>';
  }

  function questionHTML(q, n, o, teacher) {
    var points = o.points ? '<span class="g5q-points">' + o.points + ' pt' + (o.points === 1 ? '' : 's') + '</span>' : '';
    var out = '<div class="g5q"><div class="g5q-head"><span class="g5q-n">' + n + '.</span><div class="g5q-body">' + points + '<p class="g5q-prompt">' + rich(q.prompt) + '</p>';
    if (q.diagram && q.diagram.type === 'image' && q.diagram.spec) out += '<img class="g5q-fig" src="../' + esc(q.diagram.spec.src) + '" alt="' + esc(q.diagram.spec.alt || '') + '">';
    if (q.format === 'select-all') out += '<p class="g5sh-note">Select all that apply.</p>';
    out += optionList(q, teacher);
    if (q.format === 'open-response') out += partsHTML(q, teacher);
    else if (q.format === 'short-answer' || (!q.options && !q.parts)) out += teacher ? '' : (workLines(o) + '<div class="g5answerline">Answer: ________________________________</div>');
    if (teacher) {
      out += '<div class="g5q-key"><b>Answer:</b> ' + rich(answerOf(q)) + '</div>';
      if (q.solutionSteps && q.solutionSteps.length) out += stepsHTML(q);
      out += '<div class="g5checkline"><span>☐ Accurate</span><span>☐ Work shown</span><span>☐ Units labeled</span></div>';
    }
    return out + '</div></div></div>';
  }

  /* ---------------- Lesson plan ---------------- */
  function lessonHTML(plan, teacher) {
    var o = plan.options, u = plan.unit, c = u.content || {}, qn = 0;
    var title = o.title.trim() || ('Lesson Plan · ' + u.name);
    var h = '<section class="pl-sheet">' + sheetHead(plan, teacher, title,
      'Big idea: ' + (c.bigIdea || '') + '\nTime: ' + o.duration + ' minutes · Level: ' + Core.levelName(o.level) + ' · Skills: ' + plan.skills.map(function (s) { return s.name; }).join(' · '));
    if (teacher) {
      var misconception = (c.misconceptions || [])[0];
      var support = (c.support || [])[0];
      var extend = (c.extend || [])[0];
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Teacher facilitation notes</div>' +
        '<ol class="g5idealist">' +
        '<li><b>Launch:</b> Ask students to explain the central idea in their own words: ' + rich(c.bigIdea || 'Describe what you notice.') + '</li>' +
        (misconception ? '<li><b>Diagnose:</b> Pose this misconception without endorsing it: “' + rich(misconception[0]) + '” Ask students to agree or disagree and justify. <b>Listen for:</b> ' + rich(misconception[1]) + '</li>' : '') +
        '<li><b>Model:</b> Work through the selected example aloud. Name each mathematical decision and invite an alternative strategy before revealing the final answer.</li>' +
        (support ? '<li><b>Scaffold:</b> ' + rich(support) + '</li>' : '') +
        '<li><b>Check for understanding:</b> After guided practice, ask a student to explain how they know their answer is reasonable. Use their explanation to decide whether to reteach or move to independent practice.</li>' +
        (extend ? '<li><b>Extend:</b> ' + rich(extend) + '</li>' : '') +
        '</ol></section>';
    }
    plan.sections.forEach(function (sec) {
      var head = esc(sec.title) + (sec.id === 'vocabulary' ? ' <small>· ' + esc(teacher || o.notes === 'completed' ? 'Completed' : o.notes === 'blank' ? 'Blank organizer' : 'Guided notes') + '</small>' : '');
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">' + head + '</div>';
      sec.blocks.forEach(function (b) {
        if (b.kind === 'objectives') {
          h += '<div class="g5bigidea"><b>Big idea:</b> ' + rich(b.bigIdea) + '</div><ul class="g5obj">' + b.items.map(function (x) { return '<li>' + rich(x) + '</li>'; }).join('') + '</ul>';
        } else if (b.kind === 'vocab') {
          h += '<table class="g5vocab"><thead><tr><th>Word</th><th>What it means</th></tr></thead><tbody>' + b.items.map(function (v) {
            var show = teacher || o.notes === 'completed';
            return '<tr><th>' + esc(v.term) + '</th><td>' + (show ? rich(v.def) : (o.notes === 'blank' ? '<div style="height:.42in"></div>' : '<div style="height:.42in;border-bottom:1px dotted #aab4c0"></div>')) + '</td></tr>';
          }).join('') + '</tbody></table>';
        } else if (b.kind === 'example') {
          var e = b.example, answersOn = teacher || o.worked;
          h += '<div class="g5example"><p><b>Example ' + b.n + '.</b> ' + rich(e.prompt) + '</p>' +
            (e.diagram && e.diagram.spec ? '<img class="g5q-fig" src="../' + esc(e.diagram.spec.src) + '" alt="' + esc(e.diagram.spec.alt || '') + '">' : '') +
            (answersOn ? stepsHTML(e) + '<div class="g5answer"><b>Answer:</b> ' + rich(answerOf(e)) + '</div>' : workLines(o)) + '</div>';
        } else if (b.kind === 'question') {
          h += questionHTML(b.q, ++qn, o, teacher);
        } else if (b.kind === 'reflection') {
          h += b.items.map(function (x) { return '<div class="g5note"><p>' + rich(x) + '</p>' + (teacher ? '<p class="g5sh-note">Accept any clear response supported by the lesson.</p>' : lines(2)) + '</div>'; }).join('');
        } else if (b.kind === 'differentiation') {
          h += '<div class="g5diff"><div><h4>Support</h4><ul class="g5idealist">' + b.support.map(function (x) { return '<li>' + rich(x) + '</li>'; }).join('') + '</ul></div>' +
            '<div><h4>Extend</h4><ul class="g5idealist">' + b.extend.map(function (x) { return '<li>' + rich(x) + '</li>'; }).join('') + '</ul></div></div>';
        }
      });
      h += '</section>';
    });
    if (teacher && (c.misconceptions || []).length) {
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Watch for these misconceptions</div><table class="g5vocab"><thead><tr><th>If a student thinks…</th><th>Redirect with…</th></tr></thead><tbody>' +
        c.misconceptions.map(function (m) { return '<tr><td>' + rich(m[0]) + '</td><td>' + rich(m[1]) + '</td></tr>'; }).join('') + '</tbody></table></section>';
    }
    if (teacher) h += '<p class="g5foot">Answers and worked steps come from this unit’s question bank. Written explanations should be judged for reasoning, not exact wording. ' + esc(c.bigIdea || '') + '</p>';
    return h + '</section>';
  }

  /* ---------------- Worksheet / assessment ---------------- */
  function paperHTML(plan, teacher) {
    var o = plan.options, u = plan.unit, assessment = plan.mode === 'assessment';
    var blocks = plan.sections.reduce(function (a, sec) { return a.concat(sec.blocks); }, []), qn = 0;
    var total = blocks.reduce(function (a, b) { return a + (b.points || 0); }, 0);
    var title = o.title.trim() || ((assessment ? 'Assessment' : 'Practice Worksheet') + ' · ' + u.name);
    var instr = assessment
      ? 'Show your work. Circle the letter of each correct choice. Write every answer in the space provided.' + (o.timeLimit ? ' Time limit: ' + o.timeLimit + ' minutes.' : '')
      : 'Show your work. Circle the letter of each correct choice, or write your answer on the line.';
    var h = '<section class="pl-sheet">' + sheetHead(plan, teacher, title,
      instr + (assessment && o.showPoints ? '\nTotal: ' + total + ' points' : ''));
    plan.sections.forEach(function (sec) {
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">' + esc(sec.title) + ' <small>· ' + sec.blocks.length + ' questions</small></div>';
      sec.blocks.forEach(function (b) {
        h += questionHTML(b.q, ++qn, { space: o.space, points: assessment && o.showPoints ? b.points : null }, teacher);
      });
      h += '</section>';
    });
    if (teacher) {
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Scoring guide</div><table class="g5rubric"><thead><tr><th>Question</th><th>Answer</th><th>Points</th></tr></thead><tbody>' +
        blocks.map(function (b, i) { return '<tr><td>' + (i + 1) + '</td><td>' + rich(answerOf(b.q)) + '</td><td>' + (assessment && o.showPoints ? b.points : '—') + '</td></tr>'; }).join('') +
        (assessment && o.showPoints ? '<tr><th colspan="2">Total</th><th>' + total + '</th></tr>' : '') + '</tbody></table></section>';
    }
    return h + '</section>';
  }
  function cloneQ(q) { return q; }

  /* ---------------- Activities ---------------- */
  function themeOf(plan) { return Content.themes[plan.theme] || Content.themes.space || { name: 'Space Adventure', icon: '🚀' }; }
  function activityIntro(plan) {
    var d = Core.ACTIVITIES[plan.kind], theme = themeOf(plan);
    return theme.icon + ' ' + theme.name + ' · ' + d.name + ' · ' + d.blurb;
  }
  function routeSlots(n) { var out = []; for (var i = 1; i <= n; i++) out.push('<span class="slot">&nbsp;</span>' + (i < n ? ' → ' : '')); return out.join(' '); }

  function mazeHTML(plan, teacher) {
    var o = plan.options, rooms = plan.rooms || [], h = '';
    if (!rooms.length) return '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Maze · ' + plan.unit.name, 'No maze rooms matched these choices.') + '</section>';
    if (teacher) {
      h += '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Maze Answer Key · ' + plan.unit.name, activityIntro(plan));
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Correct route</div><div class="g5route">Start → ' + routeSlots(rooms.length) + ' → Finish</div>' +
        '<table class="g5rubric" style="margin-top:9px"><thead><tr><th>Room</th><th>Correct answer</th><th>Worked solution</th></tr></thead><tbody>' +
        rooms.map(function (r) { return '<tr><td>' + r.n + '</td><td>' + rich(answerOf(r.q)) + '</td><td>' + (r.q.solutionSteps || []).map(rich).join(' ') + '</td></tr>'; }).join('') +
        '</tbody></table></section></section>';
      return h;
    }
    h += '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Maze · ' + plan.unit.name, activityIntro(plan) + '\nDirections: Begin at Room 1. Solve the problem, then choose the door with your answer. A wrong door is a dead end. Record your route at the bottom.');
    for (var start = 0; start < rooms.length; start += 6) {
      var chunk = rooms.slice(start, start + 6);
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Rooms ' + (start + 1) + '–' + (start + chunk.length) + '</div><div class="g5maze">' +
        chunk.map(function (room) {
          return '<div class="g5room"><div class="g5room-h"><span>Room ' + room.n + '</span><span>' + esc(themeOf(plan).icon) + '</span></div><p>' + rich(room.q.prompt) + '</p><div class="g5doors">' +
            room.doors.map(function (d, i) { return '<div class="g5door"><b>' + 'ABC'[i] + '.</b> ' + rich(d.text) + '</div>'; }).join('') + '</div></div>';
        }).join('') + '</div></section>';
    }
    h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">My route</div><div class="g5route">Room 1 → ' + routeSlots(rooms.length - 1) + ' → Finish</div><p class="g5sh-note">Write the room number you enter next after each correct answer.</p></section></section>';
    return h;
  }

  function colorHTML(plan, teacher) {
    var o = plan.options, h = '';
    var grid = plan.grid || [], colors = plan.colorSet || [], items = plan.colorItems || [];
    if (!items.length) return '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Color by Number · ' + plan.unit.name, 'No problems matched these choices.') + '</section>';
    h += '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Color by Number · ' + plan.unit.name,
      activityIntro(plan) + '\nDirections: Solve each problem. Find its answer in the picture and color every shape with that answer using the matching color.');
    h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Picture</div><div class="g5colorgrid">' +
      grid.map(function (c) {
        var style = teacher ? 'background:' + (colors[c.color] ? colors[c.color].hex : '#fff') + ';' : '';
        return '<div class="g5cell' + (c.label ? '' : ' blank') + '" style="' + style + '">' + (c.label ? rich(c.label) : '') + '</div>';
      }).join('') + '</div></section>';
    h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Color key</div><table class="g5colorkey"><thead><tr><th>Problem</th><th>Answer</th><th>Color</th></tr></thead><tbody>' +
      items.map(function (q, i) {
        var c = colors[i % colors.length] || { name: 'Any color', hex: '#fff' };
        return '<tr><td>' + (i + 1) + '</td><td>' + (teacher ? rich(answerOf(q)) : '<span style="display:inline-block;min-width:1.2in;border-bottom:1px solid #33405a">&nbsp;</span>') + '</td><td><span class="g5swatch" style="background:' + c.hex + '"></span>' + esc(c.name) + '</td></tr>';
      }).join('') + '</tbody></table></section>';
    h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Solve</div><div class="g5colorproblems"><ol>' +
      items.map(function (q) { return '<li>' + rich(q.prompt) + (teacher ? ' <b>(' + rich(answerOf(q)) + ')</b>' : '') + '</li>'; }).join('') + '</ol></div></section>';
    if (teacher) h += '<p class="g5foot">The completed picture uses only the six key colors. Shapes with no answer from this set stay white.</p>';
    return h + '</section>';
  }

  function matchingHTML(plan, teacher) {
    var items = plan.items || [], answers = plan.answers || [], h = '';
    var shuffled = answers.map(function (a, i) { return { a: a, i: i }; });
    h += '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Matching · ' + plan.unit.name,
      activityIntro(plan) + '\nDirections: Solve each problem in the left column. Write the letter of its answer from the right column on the line.');
    h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Match each problem to its answer</div><div class="g5match">' +
      '<div><h3>Problems</h3><ol>' + items.map(function (q, i) {
        return '<li><span class="tag">' + (i + 1) + '.</span><span>' + rich(q.prompt) + '</span><span class="slot">&nbsp;</span></li>';
      }).join('') + '</ol></div>' +
      '<div><h3>Answers</h3><ol>' + shuffled.map(function (a, i) {
        return '<li><span class="tag">' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i] + '.</span><span>' + rich(a.a) + '</span></li>';
      }).join('') + '</ol></div></div></section>';
    if (teacher) {
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Answer key</div><table class="g5pairs"><thead><tr><th>Problem</th><th>Answer</th><th>Letter</th></tr></thead><tbody>' +
        items.map(function (q, i) {
          var letter = shuffled.map(function (x) { return Core.norm(x.a); }).indexOf(Core.norm(answerOf(q)));
          return '<tr><td>' + (i + 1) + '</td><td>' + rich(answerOf(q)) + '</td><td>' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[letter] + '</td></tr>';
        }).join('') + '</tbody></table>' + items.map(function (q) { return '<p class="g5sh-note"><b>' + (items.indexOf(q) + 1) + '.</b> ' + (q.solutionSteps || []).map(rich).join(' ') + '</p>'; }).join('') + '</section>';
    }
    return h + '</section>';
  }

  function stationsHTML(plan, teacher) {
    var stations = plan.stations || [], h = '';
    if (!stations.length) return '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Stations · ' + plan.unit.name, 'No station questions matched these choices.') + '</section>';
    h += '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Station Work · ' + plan.unit.name,
      activityIntro(plan) + '\nDirections: Move through the four stations with your group. Show your work and record each answer on the recording sheet.');
    stations.forEach(function (s) {
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Station ' + s.n + ' <small>· ' + s.items.length + ' problems</small></div><div class="g5station">' +
        s.items.map(function (q, i) { return '<div class="g5q"><div class="g5q-head"><span class="g5q-n">' + 'abcdefghijklmnopqrstuvwxyz'[i] + '.</span><div class="g5q-body"><p class="g5q-prompt">' + rich(q.prompt) + '</p>' +
          (q.diagram && q.diagram.spec ? '<img class="g5q-fig" src="../' + esc(q.diagram.spec.src) + '" alt="' + esc(q.diagram.spec.alt || '') + '">' : '') +
          optionList(q, teacher) + (teacher ? '<div class="g5q-key"><b>Answer:</b> ' + rich(answerOf(q)) + '</div>' : workLines(plan.options)) + '</div></div></div>'; }).join('') +
        '</div></section>';
    });
    if (!teacher) {
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Recording sheet</div><div class="g5record"><table><thead><tr><th>Station</th><th>Problem a</th><th>Problem b</th><th>Problem c</th></tr></thead><tbody>' +
        stations.map(function (s) { return '<tr><td><b>' + s.n + '</b></td>' + [0, 1, 2].map(function (i) { return '<td>' + (s.items[i] ? '&nbsp;' : '—') + '</td>'; }).join('') + '</tr>'; }).join('') +
        '</tbody></table></div></section>';
    }
    return h + '</section>';
  }

  function errorHTML(plan, teacher) {
    var items = plan.items || [], h = '';
    if (!items.length) return '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Error Analysis · ' + plan.unit.name, 'No error-analysis prompts matched these choices.') + '</section>';
    h += '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Error Analysis · ' + plan.unit.name,
      activityIntro(plan) + '\nDirections: Read each problem and the answer a classmate gave. Find the mistake, explain it in your own words, then solve the problem correctly.');
    for (var start = 0; start < items.length; start += 3) {
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Problems ' + (start + 1) + '–' + Math.min(start + 3, items.length) + '</div><div class="g5errors">' +
        items.slice(start, start + 3).map(function (it, i) {
          var n = start + i + 1;
          return '<div class="g5error"><div class="g5error-h"><span>Problem ' + n + '</span><span>🔎 Find the mistake</span></div><p>' + rich(it.q.prompt) + '</p>' +
            '<div class="wrong"><b>Classmate’s answer:</b> ' + rich(it.wrong) + '</div>' +
            (teacher ? '<div class="g5q-key"><b>The mistake:</b> ' + rich(it.reason) + '<br><b>Correct answer:</b> ' + rich(answerOf(it.q)) + '</div><ol class="g5q-steps">' + (it.q.solutionSteps || []).map(function (s) { return '<li>' + rich(s) + '</li>'; }).join('') + '</ol>'
              : '<p class="asks"><b>1.</b> What mistake did the classmate make? ' + lines(1) + '<b>2.</b> Solve it correctly. ' + workLines(plan.options) + '</p>') + '</div>';
        }).join('') + '</div></section>';
    }
    return h + '</section>';
  }

  function partnerHTML(plan, teacher) {
    var pairs = plan.pairs || [], h = '';
    if (!pairs.length) return '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Partner Check · ' + plan.unit.name, 'No matched-answer pairs were available for this selection.') + '</section>';
    var half = Math.ceil(pairs.length / 2);
    function partnerCard(side, list) {
      return '<div class="g5partner"><h3>Partner ' + side + '</h3>' + list.map(function (p, i) {
        var q = side === 'A' ? p.a : p.b;
        return '<div class="g5q"><div class="g5q-head"><span class="g5q-n">' + (i + 1) + '.</span><div class="g5q-body"><p class="g5q-prompt">' + rich(q.prompt) + '</p>' +
          (teacher ? '<div class="g5q-key"><b>Answer:</b> ' + rich(answerOf(q)) + '</div>' : workLines(plan.options)) + '</div></div></div>';
      }).join('') + '</div>';
    }
    h += '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Partner Check · ' + plan.unit.name,
      activityIntro(plan) + '\nDirections: Each partner solves their own column. Then compare answers. If your answers match, explain why. If they do not, work together to find the error.');
    h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Partner A and Partner B</div><div class="g5partners">' +
      partnerCard('A', pairs.slice(0, half)) + partnerCard('B', pairs.slice(0, half)) +
      '</div></section>';
    if (pairs.length > half) {
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Partner A and Partner B (continued)</div><div class="g5partners">' +
        partnerCard('A', pairs.slice(half)) + partnerCard('B', pairs.slice(half)) + '</div></section>';
    }
    if (teacher) {
      h += '<section class="pl-sbox g5sec"><div class="pl-shd g5sec-h">Matched answers</div><table class="g5pairs"><thead><tr><th>#</th><th>Partner A answer</th><th>Partner B answer</th><th>Shared answer</th></tr></thead><tbody>' +
        pairs.map(function (p, i) { return '<tr><td>' + (i + 1) + '</td><td>' + rich(answerOf(p.a)) + '</td><td>' + rich(answerOf(p.b)) + '</td><td>' + rich(answerOf(p.a)) + '</td></tr>'; }).join('') + '</tbody></table></section>';
    }
    return h + '</section>';
  }

  function activityHTML(plan, teacher) {
    if (plan.kind === 'maze') return mazeHTML(plan, teacher);
    if (plan.kind === 'color') return colorHTML(plan, teacher);
    if (plan.kind === 'matching') return matchingHTML(plan, teacher);
    if (plan.kind === 'stations') return stationsHTML(plan, teacher);
    if (plan.kind === 'error') return errorHTML(plan, teacher);
    if (plan.kind === 'partner') return partnerHTML(plan, teacher);
    return '<section class="pl-sheet">' + sheetHead(plan, teacher, 'Activity', '') + '</section>';
  }

  function render(plan, teacher) {
    if (plan.mode === 'lesson') return lessonHTML(plan, teacher);
    if (plan.mode === 'activity') return activityHTML(plan, teacher);
    return paperHTML(plan, teacher);
  }

  G.G5_GENERATORS_RENDER = { render: render, rich: rich, esc: esc, questionHTML: questionHTML, answerOf: answerOf, standardsOf: standardsOf };
})(typeof window !== 'undefined' ? window : globalThis);
