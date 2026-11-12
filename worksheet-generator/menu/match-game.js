/* Function Matching Game — the interactive version of the printable Matching Card Sort.
   Uses the same builder (PR.buildMatch in menu/printables-match.js), so a link with the same unit, level,
   function types, number of sets, seed and version gives exactly the cards of that printable
   (same card numbers G1…, E1…, T1…, D1…). Blank cards are not used here: every card is filled in.

   Students sort the cards into sets (one graph, equation, table and description of the same function):
     • the card tray shows one card type at a time (tabs with counts), so 24–40 cards never appear at once;
     • drag a card onto a set (mouse, or press-and-hold on a tablet), or tap a card and then tap a set,
       or press 1–9 to send the selected card to that set;
     • 🔍 opens any card large, with a coordinate read-out on graphs, arrows to flip through the cards of
       that type, and a side panel to compare it with a set before placing it;
     • Check locks every complete, correct set (and collapses it); Hint points out a misplaced card or
       lights up a card that belongs to a set;
     • progress is saved in this browser; "Copy student link" shares the same cards with a class.
   Hash: #unit=<id>&level=cp2|cp1|honors&sets=4..10&fams=a,b&seed=<n>&v=0..2&eq=1|0&hints=1|0
   Needs: KaTeX, core/rng.js, menu/engine.js, menu/printables-match.js. */
(function (G) {
  'use strict';
  var doc = G.document, NS = G.MKMENU, PR = NS.printables, M = PR.MATCH;
  var $ = function (s, r) { return (r || doc).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || doc).querySelectorAll(s)); };
  var TYPES = M.TYPES;   // graph G, eq E, table T, desc D
  var TNAME = { graph: 'Graph', eq: 'Equation', table: 'Table', desc: 'Description' }, TPLUR = { graph: 'Graphs', eq: 'Equations', table: 'Tables', desc: 'Descriptions' };
  var SLOT_ORDER = ['graph', 'eq', 'table', 'desc'];
  function esc(s) { return String(s === undefined || s === null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function lsGet(k) { try { return G.localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { G.localStorage.setItem(k, v); } catch (e) { /* storage off */ } }

  /* ---------------- math rendering ---------------- */
  function tex(s, display) { try { return G.katex.renderToString(String(s), { throwOnError: false, displayMode: !!display }); } catch (e) { return esc(s); } }
  function mathText(t) { return String(t).split(/(⟨[^⟩]*⟩)/).map(function (p) { return /^⟨/.test(p) ? tex(p.slice(1, -1)) : esc(p); }).join(''); }
  function nt(v) {
    if (Math.abs(v - Math.round(v)) < 1e-9) return String(Math.round(v));
    for (var d = 2; d <= 32; d++) { var n = Math.round(v * d); if (Math.abs(n / d - v) < 1e-9) return (n < 0 ? '-' : '') + '\\frac{' + Math.abs(n) + '}{' + d + '}'; }
    return String(Math.round(v * 100) / 100);
  }

  /* ---------------- card faces ---------------- */
  var VB = 320, PAD = 20;
  function graphGeom(g) { var sx = (VB - 2 * PAD) / (g.xmax - g.xmin), sy = (VB - 2 * PAD) / (g.ymax - g.ymin); return { sx: sx, sy: sy, X: function (x) { return PAD + (x - g.xmin) * sx; }, Y: function (y) { return PAD + (g.ymax - y) * sy; } }; }
  function svgGraph(g, big) {
    var q = graphGeom(g), X = function (x) { return q.X(x).toFixed(1); }, Y = function (y) { return q.Y(y).toFixed(1); };
    var h = '<svg class="mg-svg" viewBox="0 0 ' + VB + ' ' + VB + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="graph">';
    h += '<rect x="0" y="0" width="' + VB + '" height="' + VB + '" fill="#fff"/>';
    for (var gx = g.xmin; gx <= g.xmax + 1e-9; gx += g.xstep) h += '<path d="M' + X(gx) + ' ' + Y(g.ymin) + 'V' + Y(g.ymax) + '" stroke="#c7cfdb" stroke-width="1"/>';
    for (var gy = g.ymin; gy <= g.ymax + 1e-9; gy += g.ystep) h += '<path d="M' + X(g.xmin) + ' ' + Y(gy) + 'H' + X(g.xmax) + '" stroke="#c7cfdb" stroke-width="1"/>';
    var y0 = Math.min(Math.max(0, g.ymin), g.ymax), x0 = Math.min(Math.max(0, g.xmin), g.xmax);
    h += '<path d="M' + X(g.xmin) + ' ' + Y(y0) + 'H' + X(g.xmax) + '" stroke="#16202e" stroke-width="1.8"/><path d="M' + X(x0) + ' ' + Y(g.ymin) + 'V' + Y(g.ymax) + '" stroke="#16202e" stroke-width="1.8"/>';
    var lab = function (s) { return s === 'a_{n}' ? 'aₙ' : s; };
    h += '<text x="' + (+X(g.xmax) + 3) + '" y="' + (+Y(y0) + 4) + '" font-size="13" font-style="italic" font-family="Georgia,serif" fill="#16202e">' + lab(g.lab[0]) + '</text><text x="' + (+X(x0) + 5) + '" y="' + (+Y(g.ymax) + 3) + '" font-size="13" font-style="italic" font-family="Georgia,serif" fill="#16202e">' + lab(g.lab[1]) + '</text>';
    var lx = (g.xmax - g.xmin) / g.xstep > 8 && !big ? 2 : 1, ly = (g.ymax - g.ymin) / g.ystep > 8 && !big ? 2 : 1, fs = big ? 11 : 15;
    var num = function (v) { return (v < 0 ? '−' : '') + Math.abs(v); }, tl = function (x, y, anchor, s) { return '<text x="' + x + '" y="' + y + '" text-anchor="' + anchor + '" font-size="' + fs + '" font-family="Arial,sans-serif" fill="#222" stroke="#fff" stroke-width="3" paint-order="stroke">' + s + '</text>'; };
    for (var tx = Math.ceil(g.xmin / (g.xstep * lx)) * g.xstep * lx; tx <= g.xmax; tx += g.xstep * lx) if (Math.abs(tx) > 1e-9 && tx > g.xmin && tx < g.xmax) h += tl(X(tx), (+Y(y0) + fs + 2).toFixed(1), 'middle', num(tx));
    for (var ty = Math.ceil(g.ymin / (g.ystep * ly)) * g.ystep * ly; ty <= g.ymax; ty += g.ystep * ly) if (Math.abs(ty) > 1e-9 && ty > g.ymin && ty < g.ymax) h += tl((+X(x0) - 4).toFixed(1), (+Y(ty) + fs / 3).toFixed(1), 'end', num(ty));
    (g.asym || []).forEach(function (a) { h += a.x !== undefined ? '<path d="M' + X(a.x) + ' ' + Y(g.ymin) + 'V' + Y(g.ymax) + '" stroke="#475569" stroke-width="2" stroke-dasharray="7 5"/>' : '<path d="M' + X(g.xmin) + ' ' + Y(a.y) + 'H' + X(g.xmax) + '" stroke="#475569" stroke-width="2" stroke-dasharray="7 5"/>'; });
    (g.curves || []).forEach(function (c) { h += '<polyline fill="none" stroke="#1d4ed8" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round" points="' + c.map(function (p) { return q.X(p[0]).toFixed(1) + ',' + q.Y(p[1]).toFixed(1); }).join(' ') + '"/>'; });
    (g.dots || []).forEach(function (d) { h += '<circle cx="' + X(d[0]) + '" cy="' + Y(d[1]) + '" r="4.6" fill="#1d4ed8" stroke="#fff" stroke-width="1.2"/>'; });
    if (big) h += '<g class="mg-cross" visibility="hidden"><circle r="6" fill="none" stroke="#dc2626" stroke-width="2.4"/><rect class="mg-cbg" rx="4" height="22" fill="#16202e"/><text class="mg-ctx" font-size="14" font-family="Arial,sans-serif" font-weight="700" fill="#fff"></text></g>';
    return h + '</svg>';
  }
  function tableHtml(t, flat) {
    var hd = t.head.map(function (s) { return tex(s); });
    if (flat) return '<table class="mg-tbl flat"><tr><th>' + hd[0] + '</th>' + t.rows.map(function (r) { return '<td>' + tex(nt(r[0])) + '</td>'; }).join('') + '</tr><tr><th>' + hd[1] + '</th>' + t.rows.map(function (r) { return '<td>' + tex(nt(r[1])) + '</td>'; }).join('') + '</tr></table>';
    return '<table class="mg-tbl"><thead><tr><th>' + hd[0] + '</th><th>' + hd[1] + '</th></tr></thead><tbody>' + t.rows.map(function (r) { return '<tr><td>' + tex(nt(r[0])) + '</td><td>' + tex(nt(r[1])) + '</td></tr>'; }).join('') + '</tbody></table>';
  }
  var faceCache = {};
  function face(card, mode) {   // mode: 'full' (tray), 'mini' (in a set), 'big' (zoom)
    var k = card.key + '|' + mode; if (faceCache[k]) return faceCache[k];
    var fn = S.B.fns[card.si], h;
    if (card.type === 'graph') h = '<div class="mg-gbox">' + svgGraph(fn.graph, mode === 'big') + '</div>';
    else if (card.type === 'eq') h = '<div class="mg-eq">' + tex('\\displaystyle ' + fn.eq) + '</div>';
    else if (card.type === 'table') h = '<div class="mg-tbox">' + tableHtml(fn.table, false) + '</div>';
    else h = '<div class="mg-desc">' + fn.desc.map(function (f) { return '<p>' + mathText(f.text) + '</p>'; }).join('') + '</div>';
    return (faceCache[k] = h);
  }

  /* ---------------- configuration ---------------- */
  function supportedUnits() {
    var out = [];
    NS.CATALOG.forEach(function (g) { g.units.forEach(function (u) { if (M.supported(u[0])) out.push({ id: u[0], name: u[1], course: g.course }); }); });
    return out;
  }
  function levelName(unit,id){return /^(prealgebra7?|math[56])-/.test(unit)?{cp2:'Remedial',cp1:'Standard',honors:'Advanced'}[id]:NS.LEVELS[id].name;}
  function unitName(id) { var u = supportedUnits().filter(function (x) { return x.id === id; })[0]; return u ? u.name : id; }
  function parseHash() {
    var o = {}; String(G.location.hash || '').replace(/^#/, '').split('&').forEach(function (kv) { var i = kv.indexOf('='); if (i > 0) o[decodeURIComponent(kv.slice(0, i))] = decodeURIComponent(kv.slice(i + 1)); });
    var units = supportedUnits(), unit = o.unit && M.supported(o.unit) ? o.unit : (units[0] && units[0].id);
    var U = M.UNITS[unit], fams = (o.fams ? o.fams.split(',') : U.def).filter(function (f) { return U.fams.indexOf(f) >= 0; });
    if (!fams.length) fams = U.def.slice();
    return {
      unit: unit, level: NS.LEVELS[o.level] ? o.level : 'cp1', sets: Math.max(4, Math.min(10, (+o.sets) || 6)), fams: fams,
      seed: o.seed !== undefined && o.seed !== '' && isFinite(+o.seed) ? +o.seed : null, v: Math.max(0, Math.min(2, (+o.v) || 0)),
      eq: o.eq === '0' ? 0 : 1, hints: o.hints === '0' ? 0 : 1
    };
  }
  function hashOf(c) { return 'unit=' + c.unit + '&level=' + c.level + '&sets=' + c.sets + '&fams=' + c.fams.join(',') + (c.seed !== null ? '&seed=' + c.seed : '') + (c.v ? '&v=' + c.v : '') + '&eq=' + c.eq + '&hints=' + c.hints; }
  function linkOf(c) { return G.location.href.split('#')[0] + '#' + hashOf(c); }
  function builderCfg(c) { var fam = {}; M.UNITS[c.unit].fams.forEach(function (f) { fam[f] = c.fams.indexOf(f) >= 0; }); return { unitId: c.unit, kind: 'match', level: c.level, sets: c.sets, seed: c.seed, blanks: 'none', families: fam }; }
  function storeKey(c) { return 'mkmatch:' + [c.unit, c.level, c.sets, c.fams.join('+'), c.seed, c.v, c.eq].join(':'); }

  /* ---------------- state ---------------- */
  var S = null;   // { cfg, B, cards{}, order{type:[keys]}, eqOrder, place{key:row|-1}, ok{row}, bad{row}, checks, hints, wrongChecks, elapsed, t0, done, tab, sel, active, size, compare }
  function newState(cfg) {
    var B = PR.buildMatch(builderCfg(cfg), cfg.v);
    if (B.error) return { error: B.error };
    faceCache = {};
    var cards = {}, order = {};
    TYPES.forEach(function (ty) {
      order[ty.id] = [];
      B.fns.forEach(function (fn, si) { var n = B.ids[ty.id][si], key = ty.id + n; cards[key] = { key: key, type: ty.id, si: si, n: n, label: ty.L + n }; order[ty.id][n - 1] = key; });
    });
    var st = { cfg: cfg, B: B, N: B.N, cards: cards, order: order, place: {}, ok: {}, bad: {}, checks: 0, hints: 0, wrongChecks: 0, elapsed: 0, t0: Date.now(), done: false, sel: null, active: 0, compare: 0, tab: cfg.eq ? 'graph' : 'eq', fixed: {} };
    Object.keys(cards).forEach(function (k) { st.place[k] = -1; });
    if (cfg.eq) order.eq.forEach(function (k, r) { st.place[k] = r; st.fixed[k] = true; });   // E1 in Set 1, E2 in Set 2, …
    var saved = null; try { saved = JSON.parse(lsGet(storeKey(cfg)) || 'null'); } catch (e) { saved = null; }
    if (saved && saved.place) {
      Object.keys(saved.place).forEach(function (k) { if (k in st.place && !st.fixed[k]) st.place[k] = saved.place[k]; });
      ['ok', 'bad'].forEach(function (f) { st[f] = saved[f] || {}; });
      ['checks', 'hints', 'wrongChecks', 'elapsed', 'done', 'tab'].forEach(function (f) { if (saved[f] !== undefined) st[f] = saved[f]; });
      st.resumed = Object.keys(st.place).some(function (k) { return !st.fixed[k] && st.place[k] >= 0; });
    }
    if (cfg.eq && st.tab === 'eq') st.tab = 'graph';
    return st;
  }
  function save() { if (!S || S.error) return; lsSet(storeKey(S.cfg), JSON.stringify({ place: S.place, ok: S.ok, bad: S.bad, checks: S.checks, hints: S.hints, wrongChecks: S.wrongChecks, elapsed: elapsedNow(), done: S.done, tab: S.tab })); }
  function elapsedNow() { return S.done ? S.elapsed : S.elapsed + (Date.now() - S.t0); }
  function rowCards(r) { var o = {}; Object.keys(S.place).forEach(function (k) { if (S.place[k] === r) o[S.cards[k].type] = k; }); return o; }
  function rowFull(r) { var o = rowCards(r); return SLOT_ORDER.every(function (t) { return o[t]; }); }
  function rowRight(r) { var o = rowCards(r); return rowFull(r) && SLOT_ORDER.every(function (t) { return S.cards[o[t]].si === S.cards[o.eq].si; }); }
  function unplaced(type) { return S.order[type].filter(function (k) { return S.place[k] < 0; }); }
  function nOk() { return Object.keys(S.ok).filter(function (r) { return S.ok[r]; }).length; }

  /* ---------------- moves ---------------- */
  function say(msg, kind) { var t = $('#mgToast'); if (t) { t.innerHTML = msg; t.className = 'mg-toast show' + (kind ? ' ' + kind : ''); clearTimeout(say.t); say.t = setTimeout(function () { t.className = 'mg-toast'; }, kind === 'long' ? 7000 : 3800); } $('#mgLive').textContent = String(msg).replace(/<[^>]+>/g, ''); }
  function place(key, r, quiet) {
    var c = S.cards[key]; if (!c) return false;
    if (S.fixed[key]) { if (!quiet) say('The equation cards stay in their sets. Move the other cards to them.'); return false; }
    if (r >= 0 && S.ok[r]) { if (!quiet) say('Set ' + (r + 1) + ' is already matched.'); return false; }
    var from = S.place[key];
    if (from >= 0 && S.ok[from]) { if (!quiet) say('That set is already matched.'); return false; }
    if (from === r) return false;
    if (r >= 0) {
      var occ = rowCards(r)[c.type];
      if (occ) {
        if (S.fixed[occ]) return false;
        S.place[occ] = from;   // swap (or back to the tray when the card came from the tray)
        delete S.bad[from];
      }
    }
    S.place[key] = r; delete S.bad[r]; if (from >= 0) delete S.bad[from];
    if (r >= 0) S.active = r;
    S.sel = null; save(); draw();
    if (!quiet) {
      var tt = $('#mgToast'); if (tt) tt.className = 'mg-toast';
      if (r >= 0 && rowFull(r)) say('Set ' + (r + 1) + ' has all four cards. Press <b>Check</b> when you are ready.');
      if (Object.keys(S.place).every(function (k) { return S.place[k] >= 0; })) pulseCheck();
    }
    return true;
  }
  function pulseCheck() { var b = $('#mgCheck'); if (b) { b.classList.remove('pulse'); void b.offsetWidth; b.classList.add('pulse'); } }
  function check() {
    var right = [], wrong = [], open = [];
    for (var r = 0; r < S.N; r++) {
      if (S.ok[r]) continue;
      if (!rowFull(r)) { if (Object.keys(rowCards(r)).length > (S.cfg.eq ? 1 : 0)) open.push(r + 1); continue; }
      if (rowRight(r)) { S.ok[r] = true; delete S.bad[r]; right.push(r + 1); } else { S.bad[r] = true; wrong.push(r + 1); }
    }
    S.checks++; if (wrong.length) S.wrongChecks++;
    var parts = [];
    if (right.length) parts.push('<b>' + (right.length === 1 ? 'Set ' + right[0] + ' matches!' : 'Sets ' + right.join(', ') + ' match!') + '</b>');
    if (wrong.length) parts.push((wrong.length === 1 ? 'Set ' + wrong[0] + ' has' : 'Sets ' + wrong.join(', ') + ' have') + ' a card that belongs somewhere else.');
    if (open.length) parts.push((open.length === 1 ? 'Set ' + open[0] + ' is' : 'Sets ' + open.join(', ') + ' are') + ' not complete yet.');
    if (!right.length && !wrong.length) parts.push(open.length ? 'Fill a set with all four cards, then check it.' : 'Put four cards in a set, then check it.');
    if (nOk() === S.N) { S.elapsed = elapsedNow(); S.done = true; }
    save(); draw(); say(parts.join(' '), wrong.length ? 'warn' : right.length ? 'good' : '');
    if (S.done) setTimeout(finish, 450);
  }
  function anchorOf(r) {   // the function a set is "about": its equation, else the most common card
    var o = rowCards(r); if (o.eq) return S.cards[o.eq].si;
    var cnt = {}, best = null; SLOT_ORDER.forEach(function (t) { if (o[t]) { var si = S.cards[o[t]].si; cnt[si] = (cnt[si] || 0) + 1; if (best === null || cnt[si] > cnt[best]) best = si; } });
    return best;
  }
  function flash(sel, cls) { $$(sel).forEach(function (el) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); }); }
  function hint() {
    if (!S.cfg.hints) return;
    for (var r = 0; r < S.N; r++) {   // 1. a misplaced card
      if (S.ok[r]) continue;
      var o = rowCards(r), keys = SLOT_ORDER.map(function (t) { return o[t]; }).filter(Boolean);
      if (keys.length < 2) continue;
      var a = anchorOf(r), off = keys.filter(function (k) { return S.cards[k].si !== a && !S.fixed[k]; });
      if (!off.length) continue;
      var tie = !o.eq && keys.length - off.length === off.length;
      S.hints++; save(); S.active = r; draw();
      flash('.mg-row[data-row="' + r + '"] .mg-card[data-key="' + off[0] + '"]', 'hinted');
      say(tie ? 'In Set ' + (r + 1) + ', <b>' + S.cards[off[0]].label + '</b> and <b>' + S.cards[keys.filter(function (k) { return off.indexOf(k) < 0; })[0]].label + '</b> are not the same function.' : '<b>' + S.cards[off[0]].label + '</b> does not belong in Set ' + (r + 1) + '. Drag it back to the tray or to another set.', 'long');
      return;
    }
    var order = [S.active].concat(Array.apply(null, Array(S.N)).map(function (_, i) { return i; }));
    for (var i = 0; i < order.length; i++) {   // 2. a card that belongs in a started set
      var rr = order[i]; if (S.ok[rr]) continue;
      var oo = rowCards(rr), si = anchorOf(rr); if (si === null) continue;
      var miss = SLOT_ORDER.filter(function (t) { return !oo[t]; })[0]; if (!miss) continue;
      var want = S.order[miss].filter(function (k) { return S.cards[k].si === si; })[0];
      S.hints++; S.tab = miss; S.active = rr; save(); draw();
      var el = $('.mg-tray .mg-card[data-key="' + want + '"]');
      if (el) { el.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); flash('.mg-tray .mg-card[data-key="' + want + '"]', 'glow'); }
      say('The ' + TNAME[miss].toLowerCase() + ' for Set ' + (rr + 1) + ' is glowing in the tray: <b>' + S.cards[want].label + '</b>.', 'long');
      return;
    }
    S.hints++; save();
    say('Start with one card and look for a feature you can see on every card: the <i>y</i>-intercept, a point the function passes through, the slope or rate of change, a vertex, or an asymptote.', 'long');
  }
  function restart() {
    Object.keys(S.place).forEach(function (k) { if (!S.fixed[k]) S.place[k] = -1; });
    S.ok = {}; S.bad = {}; S.checks = 0; S.hints = 0; S.wrongChecks = 0; S.elapsed = 0; S.t0 = Date.now(); S.done = false; S.sel = null;
    save(); draw(); say('All cards are back in the tray.');
  }

  /* ---------------- views ---------------- */
  function cardHtml(key, mode, r) {
    var c = S.cards[key], fixed = S.fixed[key], locked = r >= 0 && S.ok[r];
    return '<div class="mg-card t-' + c.type + (mode === 'mini' ? ' mini' : '') + (S.sel === key ? ' sel' : '') + (fixed ? ' fixed' : '') + '" data-key="' + key + '" tabindex="0" role="button" aria-pressed="' + (S.sel === key) + '" aria-label="' + TNAME[c.type] + ' card ' + c.label + (r >= 0 ? ', in Set ' + (r + 1) : '') + '">' +
      '<span class="mg-id">' + c.label + '</span>' +
      '<span class="mg-tools"><button type="button" class="mg-zoom" data-zoom="' + key + '" title="Zoom in" aria-label="Zoom in on ' + c.label + '">' + ICON_ZOOM + '</button>' +
      (mode === 'mini' && !fixed && !locked ? '<button type="button" class="mg-out" data-out="' + key + '" title="Back to the tray" aria-label="Move ' + c.label + ' back to the tray">×</button>' : '') + '</span>' +
      '<div class="mg-face">' + face(c, mode) + '</div></div>';
  }
  var ICON_ZOOM = '<svg viewBox="0 0 20 20" width="15" height="15" aria-hidden="true"><circle cx="8" cy="8" r="5.6" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M12.2 12.2 17.5 17.5" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/><path d="M5.4 8h5.2M8 5.4v5.2" stroke="currentColor" stroke-width="1.8"/></svg>';
  function tabsHtml() {
    var types = SLOT_ORDER.slice().sort(function (a, b) { return (a === 'eq' ? -1 : 0) - (b === 'eq' ? -1 : 0); }).filter(function (t) { return !(S.cfg.eq && t === 'eq'); });
    return '<div class="mg-tabs" role="tablist" aria-label="Card type">' + types.map(function (t) {
      var n = unplaced(t).length;
      return '<button type="button" role="tab" class="mg-tab t-' + t + '" data-tab="' + t + '" aria-selected="' + (S.tab === t) + '"><span class="mg-tl">' + TPLUR[t] + '</span><span class="mg-cnt' + (n ? '' : ' none') + '">' + (n ? n : '✓') + '</span></button>';
    }).join('') + '<button type="button" role="tab" class="mg-tab" data-tab="all" aria-selected="' + (S.tab === 'all') + '"><span class="mg-tl">All</span><span class="mg-cnt">' + Object.keys(S.place).filter(function (k) { return S.place[k] < 0; }).length + '</span></button></div>';
  }
  function trayHtml() {
    var types = S.tab === 'all' ? SLOT_ORDER : [S.tab], h = '';
    types.forEach(function (t) {
      var ks = unplaced(t);
      if (S.tab === 'all') { if (!ks.length) return; h += '<h3 class="mg-th">' + TPLUR[t] + '</h3>'; }
      h += '<div class="mg-grid t-' + t + '">' + ks.map(function (k) { return cardHtml(k, 'full', -1); }).join('') + '</div>';
    });
    if (!h || (S.tab !== 'all' && !unplaced(S.tab).length)) {
      var left = SLOT_ORDER.filter(function (t) { return unplaced(t).length; });
      h = '<div class="mg-empty">' + (S.done ? 'All ' + S.N + ' sets are matched. Nice work!' : left.length ? 'Every ' + TNAME[S.tab === 'all' ? 'graph' : S.tab].toLowerCase() + ' card is in a set. <button type="button" class="link" data-tab="' + left[0] + '">Show the ' + TPLUR[left[0]].toLowerCase() + '</button>' : 'Every card is in a set. Press <b>Check</b> to see which sets match.') + '</div>';
    }
    return h;
  }
  function rowHtml(r) {
    var o = rowCards(r), ok = S.ok[r], bad = S.bad[r], cnt = SLOT_ORDER.filter(function (t) { return o[t]; }).length;
    var st = ok ? '<span class="mg-st ok">✓ Matched</span>' : bad ? '<span class="mg-st bad">Not quite: one card belongs somewhere else</span>' : '<span class="mg-st">' + cnt + ' of 4 cards</span>';
    if (ok && !S.expand[r]) {
      return '<section class="mg-row ok collapsed" data-row="' + r + '" aria-label="Set ' + (r + 1) + ', matched"><header><b>Set ' + (r + 1) + '</b>' + st +
        '<span class="mg-sum">' + tex(S.B.fns[S.cards[o.eq].si].eq) + '</span><button type="button" class="link" data-expand="' + r + '">Show cards</button></header></section>';
    }
    return '<section class="mg-row' + (ok ? ' ok' : '') + (bad ? ' bad' : '') + (S.active === r && !ok ? ' active' : '') + '" data-row="' + r + '" tabindex="0" aria-label="Set ' + (r + 1) + '"><header><b>Set ' + (r + 1) + '</b>' + st +
      (ok ? '<button type="button" class="link" data-expand="' + r + '">Hide cards</button>' : '<span class="mg-kbd" aria-hidden="true">' + (r < 9 ? 'key ' + (r + 1) : '') + '</span>') + '</header>' +
      '<div class="mg-slots">' + SLOT_ORDER.map(function (t) {
        return '<div class="mg-slot t-' + t + (o[t] ? ' full' : '') + '" data-row="' + r + '" data-type="' + t + '">' + (o[t] ? cardHtml(o[t], 'mini', r) : '<span class="mg-ph">' + TNAME[t] + '</span>') + '</div>';
      }).join('') + '</div></section>';
  }
  function fmtTime(ms) { var s = Math.floor(ms / 1000); return Math.floor(s / 60) + ':' + ('0' + s % 60).slice(-2); }
  function shell() {
    var c = S.cfg, L = NS.LEVELS[c.level];
    if (/^prealgebra-/.test(c.unit)) { const back=$('#backBtn'),brand=$('.brand');if(back)back.hidden=true;if(brand)brand.hidden=true; }
    $('#mgApp').innerHTML =
      '<div class="mg-bar card">' +
        '<div class="mg-title"><h1>' + esc(unitName(c.unit).replace(/^Unit \d+ · /, '')) + ' <span>Matching</span></h1>' +
          '<div class="mg-meta">' + esc(levelName(c.unit,c.level)) + ' · ' + S.N + ' sets · ' + c.fams.map(function (f) { return esc(M.FAMILIES[f]); }).join(', ') + (c.v ? ' · Version ' + 'ABC'[c.v] : '') + '</div></div>' +
        '<div class="mg-prog" aria-label="Progress"><div class="mg-pt"><b id="mgOk">0</b> of ' + S.N + ' sets matched</div><div class="mg-pbar"><i id="mgPbar"></i></div><div class="mg-time" id="mgTime" aria-hidden="true"></div></div>' +
        '<div class="mg-acts">' +
          '<button type="button" class="btn" id="mgCheck">✔ Check sets</button>' +
          (c.hints ? '<button type="button" class="btn sec2" id="mgHint">Hint</button>' : '') +
          '<details class="mg-more"><summary class="btn ghost">More ▾</summary><div class="mg-menu">' +
            '<button type="button" id="mgHelp">How to play</button><button type="button" id="mgRestart">Start over (same cards)</button>' +
            '<button type="button" id="mgNew">New cards (same settings)</button><button type="button" id="mgSettings">Change settings</button>' +
            '<button type="button" id="mgShare">Copy student link</button><a href="printables.html#unit=' + c.unit + '&kind=match">Print these as a card sort</a></div></details>' +
        '</div>' +
      '</div>' +
      '<div class="mg-main">' +
        '<section class="mg-pane mg-tray" aria-label="Card tray">' +
          '<div class="mg-trayhead">' + '<div id="mgTabs"></div>' +
            '<label class="mg-size" title="Card size"><span aria-hidden="true">A</span><input type="range" id="mgSize" min="1" max="4" step="1" value="' + (+lsGet('mkmatch-size') || 2) + '" aria-label="Card size"><span aria-hidden="true" class="big">A</span></label></div>' +
          '<div class="mg-scroll" id="mgTrayScroll"><div id="mgHow"></div><div id="mgTray"></div></div>' +
        '</section>' +
        '<section class="mg-pane mg-board" aria-label="Sets"><div class="mg-scroll" id="mgBoardScroll"><div id="mgBoard"></div></div></section>' +
      '</div>' +
      '<div id="mgToast" class="mg-toast" role="status"></div>';
    applySize();
    $('#mgCheck').onclick = check;
    if ($('#mgHint')) $('#mgHint').onclick = hint;
    var closeMenu = function () { $('.mg-more').open = false; };
    $('#mgHelp').onclick = function () { closeMenu(); lsSet('mkmatch-how', ''); showHow(true); };
    $('#mgRestart').onclick = function () { closeMenu(); if (G.confirm('Put every card back in the tray and start over?')) restart(); };
    $('#mgNew').onclick = function () { closeMenu(); var n = Object.assign({}, S.cfg, { seed: Math.floor(Math.random() * 1e9), v: 0 }); go(n); };
    $('#mgSettings').onclick = function () { closeMenu(); setup(S.cfg); };
    if (/^prealgebra-/.test(c.unit)) { const print=$('a[href^="printables.html"]');if(print)print.remove(); }
    $('#mgShare').onclick = function () { closeMenu(); copy(linkOf(S.cfg), 'Link copied. Students who open it get these same cards.'); };
    $('#mgSize').oninput = function (e) { lsSet('mkmatch-size', e.target.value); applySize(); };
    showHow(!lsGet('mkmatch-how'));
  }
  function applySize() {   // on a phone the smallest sizes still fit two cards across
    var v = +($('#mgSize') ? $('#mgSize').value : 2), px = [0, 150, 190, 240, 310][v];
    if (G.innerWidth < 600) px = Math.round([0, 0.36, 0.42, 0.6, 0.9][v] * G.innerWidth);
    doc.documentElement.style.setProperty('--mg-cw', px + 'px');
  }
  G.addEventListener('resize', function () { if ($('#mgSize')) applySize(); });
  function showHow(on) {
    var box = $('#mgHow'); if (!box) return;
    box.innerHTML = on ? '<div class="mg-how"><b>How to play</b><ol>' +
      '<li>Each set is one function: its <b>graph</b>, <b>equation</b>, <b>table</b> and <b>description</b>.' + (S.cfg.eq ? ' Each set already has its equation.' : '') + '</li>' +
      '<li>Pick a card type above. <b>Drag</b> a card onto a set, or <b>tap</b> a card and then tap a set (or press its number key). On a tablet, press and hold to drag.</li>' +
      '<li>Press ' + ICON_ZOOM + ' to see a card up close. On a big graph, point at the grid to read coordinates.</li>' +
      '<li>When a set has four cards, press <b>Check sets</b>. Matched sets fold away so you can focus on the rest.</li></ol>' +
      '<button type="button" class="btn sm" id="mgHowOk">Got it</button></div>' : '';
    if (on) $('#mgHowOk').onclick = function () { lsSet('mkmatch-how', '1'); showHow(false); };
  }
  function draw() {
    if (!$('#mgBoard')) return;
    $('#mgTabs').innerHTML = tabsHtml();
    $('#mgTray').innerHTML = trayHtml();
    $('#mgBoard').innerHTML = Array.apply(null, Array(S.N)).map(function (_, r) { return rowHtml(r); }).join('');
    $('#mgOk').textContent = nOk(); $('#mgPbar').style.width = (100 * nOk() / S.N) + '%';
    doc.body.classList.toggle('mg-selecting', !!S.sel);
    if (S.sel && doc.activeElement === doc.body) { var el = $('.mg-card[data-key="' + S.sel + '"]'); if (el) el.focus({ preventScroll: true }); }
  }
  function tick() { if (S && !S.error && $('#mgTime')) $('#mgTime').textContent = '⏱ ' + fmtTime(elapsedNow()); }
  G.setInterval(tick, 1000);
  G.addEventListener('beforeunload', function () { if (S && !S.error) save(); });
  doc.addEventListener('visibilitychange', function () { if (S && !S.error && doc.hidden) save(); });

  function copy(text, msg) {
    var ok = function () { say(msg, 'good'); }, fail = function () { G.prompt('Copy this link:', text); };
    if (G.navigator.clipboard && G.isSecureContext) G.navigator.clipboard.writeText(text).then(ok, fail); else fail();
  }

  /* ---------------- tap / keyboard ---------------- */
  var suppressClick = false;
  doc.addEventListener('click', function (e) {
    if (!S || S.error || !$('#mgBoard')) return;
    if (suppressClick) { suppressClick = false; e.preventDefault(); return; }
    var t = e.target;
    if (t.closest('.mg-modal')) return;
    var z = t.closest('[data-zoom]'); if (z) { zoom(z.getAttribute('data-zoom')); return; }
    var out = t.closest('[data-out]'); if (out) { place(out.getAttribute('data-out'), -1); return; }
    var tab = t.closest('[data-tab]'); if (tab) { S.tab = tab.getAttribute('data-tab'); save(); draw(); $('#mgTrayScroll').scrollTop = 0; return; }
    var ex = t.closest('[data-expand]'); if (ex) { var r0 = +ex.getAttribute('data-expand'); S.expand[r0] = !S.expand[r0]; draw(); return; }
    var card = t.closest('.mg-card');
    var row = t.closest('.mg-row');
    if (card && !(S.sel && row && S.place[card.getAttribute('data-key')] !== +row.getAttribute('data-row'))) {
      var k = card.getAttribute('data-key');
      if (S.fixed[k] || S.ok[S.place[k]]) { if (S.sel && row) { place(S.sel, +row.getAttribute('data-row')); } else zoom(k); return; }
      S.sel = S.sel === k ? null : k; draw();
      if (S.sel) say('<b>' + S.cards[k].label + '</b> selected. Tap a set to put it there' + (S.N <= 9 ? ' (or press 1–' + S.N + ')' : '') + '.');
      return;
    }
    if (row && S.sel) { place(S.sel, +row.getAttribute('data-row')); return; }
    if (row && !S.ok[+row.getAttribute('data-row')]) { S.active = +row.getAttribute('data-row'); draw(); return; }
    if (t.closest('.mg-tray') && S.sel && S.place[S.sel] >= 0) { place(S.sel, -1); return; }
  });
  doc.addEventListener('keydown', function (e) {
    if (!S || S.error || !$('#mgBoard')) return;
    if ($('.mg-modal')) return;   // the zoom window has its own keys
    var t = e.target;
    if (/^(INPUT|SELECT|TEXTAREA)$/.test(t.tagName)) return;
    if (e.key === 'Escape' && S.sel) { S.sel = null; draw(); return; }
    if ((e.key === 'Enter' || e.key === ' ') && t.classList && (t.classList.contains('mg-card') || t.classList.contains('mg-row'))) { e.preventDefault(); t.click(); return; }
    if (S.sel && /^[1-9]$/.test(e.key) && +e.key <= S.N) { e.preventDefault(); place(S.sel, +e.key - 1); return; }
    if (S.sel && (e.key === '0' || e.key === 'Backspace' || e.key === 'Delete') && S.place[S.sel] >= 0) { e.preventDefault(); place(S.sel, -1); return; }
    if ((e.key === 'z' || e.key === 'Z') && t.classList && t.classList.contains('mg-card')) { zoom(t.getAttribute('data-key')); }
  });
  doc.addEventListener('contextmenu', function (e) { if (e.target.closest && e.target.closest('.mg-card') && drag) e.preventDefault(); });

  /* ---------------- drag and drop (mouse, pen, touch) ---------------- */
  var drag = null;
  doc.addEventListener('pointerdown', function (e) {
    if (!S || S.error || e.button > 0) return;
    var el = e.target.closest && e.target.closest('.mg-card');
    if (!el || e.target.closest('button') || el.closest('.mg-modal')) return;
    var k = el.getAttribute('data-key');
    if (S.fixed[k] || S.ok[S.place[k]]) return;
    drag = { key: k, el: el, x0: e.clientX, y0: e.clientY, x: e.clientX, y: e.clientY, id: e.pointerId, started: false, armed: e.pointerType !== 'touch' };
    if (!drag.armed) drag.timer = setTimeout(function () { if (drag && !drag.started) { drag.armed = true; el.classList.add('armed'); if (G.navigator.vibrate) G.navigator.vibrate(12); } }, 230);
  });
  doc.addEventListener('touchmove', function (e) { if (drag && drag.armed) e.preventDefault(); }, { passive: false });
  doc.addEventListener('pointermove', function (e) {
    if (!drag || e.pointerId !== drag.id) return;
    drag.x = e.clientX; drag.y = e.clientY;
    var dist = Math.hypot(e.clientX - drag.x0, e.clientY - drag.y0);
    if (!drag.started) {
      if (!drag.armed) { if (dist > 8) endDrag(); return; }
      if (dist < 6) return;
      startDrag();
    }
    e.preventDefault();
    moveGhost(); hover();
  });
  doc.addEventListener('pointerup', function (e) { if (!drag || e.pointerId !== drag.id) return; if (drag.started) { drop(); suppressClick = true; setTimeout(function () { suppressClick = false; }, 0); } endDrag(); });
  doc.addEventListener('pointercancel', function (e) { if (drag && e.pointerId === drag.id) endDrag(); });
  function startDrag() {
    drag.started = true; S.sel = null;
    var r = drag.el.getBoundingClientRect(), w = Math.min(r.width, 230), g = drag.el.cloneNode(true);
    g.classList.add('mg-ghost'); g.classList.remove('sel', 'armed'); g.style.width = w + 'px';
    drag.dx = Math.min(Math.max(10, drag.x0 - r.left), w - 20); drag.dy = Math.min(drag.y0 - r.top, 40);
    doc.body.appendChild(g); drag.ghost = g; drag.el.classList.add('dragging'); doc.body.classList.add('mg-dragging');
    moveGhost(); scrollLoop();
  }
  function moveGhost() { if (drag && drag.ghost) drag.ghost.style.transform = 'translate(' + (drag.x - drag.dx) + 'px,' + (drag.y - drag.dy) + 'px) rotate(-2deg)'; }
  function target() {
    var el = doc.elementFromPoint(drag.x, drag.y); if (!el) return null;
    var row = el.closest('.mg-row'); if (row && !row.classList.contains('ok')) return { row: +row.getAttribute('data-row'), el: row };
    var tray = el.closest('.mg-tray'); if (tray) return { row: -1, el: tray };
    return null;
  }
  function hover() {
    var t = target();
    $$('.drop-over').forEach(function (x) { if (!t || x !== t.el) x.classList.remove('drop-over'); });
    if (t && (t.row >= 0 || S.place[drag.key] >= 0)) t.el.classList.add('drop-over');
  }
  function scrollLoop() {
    if (!drag || !drag.started) return;
    var panes = $$('.mg-scroll'), y = drag.y, x = drag.x, edge = 56, moved = false;
    panes.forEach(function (p) {
      var r = p.getBoundingClientRect(); if (x < r.left || x > r.right || p.scrollHeight <= p.clientHeight + 2) return;
      if (y < r.top + edge && y > r.top - 30) { p.scrollTop -= Math.ceil((r.top + edge - y) / 4); moved = true; }
      else if (y > r.bottom - edge && y < r.bottom + 30) { p.scrollTop += Math.ceil((y - (r.bottom - edge)) / 4); moved = true; }
    });
    if (!moved) { if (y < edge) G.scrollBy(0, -Math.ceil((edge - y) / 4)); else if (y > G.innerHeight - edge) G.scrollBy(0, Math.ceil((y - G.innerHeight + edge) / 4)); }
    hover();
    G.requestAnimationFrame(scrollLoop);
  }
  function drop() {
    var t = target(); if (!t) return;
    if (t.row === -1) { if (S.place[drag.key] >= 0) place(drag.key, -1); return; }
    place(drag.key, t.row);
  }
  function endDrag() {
    if (!drag) return;
    clearTimeout(drag.timer);
    if (drag.ghost) drag.ghost.remove();
    drag.el.classList.remove('dragging', 'armed'); doc.body.classList.remove('mg-dragging');
    $$('.drop-over').forEach(function (x) { x.classList.remove('drop-over'); });
    drag = null;
  }

  /* ---------------- zoom window ---------------- */
  function zoom(key) {
    var old = $('.mg-modal'); if (old) old.remove();
    var c = S.cards[key], list = S.order[c.type], i = list.indexOf(key), here = S.place[key];
    if (here >= 0) S.compare = here; else if (S.ok[S.compare] || S.compare >= S.N) S.compare = firstOpen();
    var canMove = !S.fixed[key] && !(here >= 0 && S.ok[here]);
    var m = doc.createElement('div'); m.className = 'mg-modal'; m.setAttribute('role', 'dialog'); m.setAttribute('aria-modal', 'true'); m.setAttribute('aria-label', TNAME[c.type] + ' card ' + c.label);
    m.innerHTML = '<div class="mg-mbox t-' + c.type + '"><header class="mg-mhead">' +
      '<button type="button" class="btn ghost sm" data-step="-1" aria-label="Previous ' + TNAME[c.type].toLowerCase() + '">←</button>' +
      '<b>' + TNAME[c.type] + ' ' + c.label + '</b><span class="mg-mwhere">' + (here >= 0 ? 'in Set ' + (here + 1) + (S.ok[here] ? ' ✓' : '') : 'in the tray') + ' · ' + (i + 1) + ' of ' + list.length + '</span>' +
      '<button type="button" class="btn ghost sm" data-step="1" aria-label="Next ' + TNAME[c.type].toLowerCase() + '">→</button><span class="sp"></span>' +
      '<button type="button" class="btn ghost sm mg-x" aria-label="Close">✕ Close</button></header>' +
      '<div class="mg-mbody"><div class="mg-big">' + face(c, 'big') + (c.type === 'graph' ? '<p class="mg-cap">Point at the grid to read coordinates.</p>' : '') + '</div>' +
      (canMove ? '<aside class="mg-cmp"><div class="mg-cmph">Compare with a set</div><div class="mg-setbtns">' + Array.apply(null, Array(S.N)).map(function (_, r) { return '<button type="button" class="mg-sb' + (S.ok[r] ? ' ok' : '') + '" data-cmp="' + r + '" aria-pressed="' + (S.compare === r) + '"' + (S.ok[r] ? ' disabled title="Matched"' : '') + '>' + (r + 1) + '</button>'; }).join('') + '</div><div class="mg-pl"></div><div class="mg-cset"></div></aside>' : '') +
      '</div></div>';
    doc.body.appendChild(m); doc.body.classList.add('mg-modal-open');
    var close = function () { m.remove(); doc.body.classList.remove('mg-modal-open'); var back = $('.mg-card[data-key="' + key + '"]'); if (back) back.focus({ preventScroll: true }); doc.removeEventListener('keydown', keys, true); };
    var keys = function (e) {
      if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); close(); }
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); e.stopPropagation(); step(e.key === 'ArrowLeft' ? -1 : 1); }
      else if (canMove && /^[1-9]$/.test(e.key) && +e.key <= S.N) { e.preventDefault(); e.stopPropagation(); var r = +e.key - 1; if (!S.ok[r]) { close(); place(key, r); } }
    };
    var step = function (d) { close(); zoom(list[(i + d + list.length) % list.length]); };
    doc.addEventListener('keydown', keys, true);
    m.addEventListener('click', function (e) {
      if (e.target === m || e.target.closest('.mg-x')) { close(); return; }
      var s = e.target.closest('[data-step]'); if (s) { step(+s.getAttribute('data-step')); return; }
      var cb = e.target.closest('[data-cmp]'); if (cb) { S.compare = +cb.getAttribute('data-cmp'); $$('[data-cmp]', m).forEach(function (b) { b.setAttribute('aria-pressed', b === cb); }); fillCompare(); return; }
      if (e.target.closest('[data-put]')) { var r = S.compare; close(); place(key, r); return; }
      if (e.target.closest('[data-back]')) { close(); place(key, -1); return; }
      var z2 = e.target.closest('[data-zoom]'); if (z2) { close(); zoom(z2.getAttribute('data-zoom')); }
    });
    function fillCompare() {
      if (!canMove) return;
      var r = S.compare, o = rowCards(r), occ = o[c.type];
      $('.mg-cset', m).innerHTML = '<div class="mg-cseth">Set ' + (r + 1) + '</div>' + SLOT_ORDER.filter(function (t) { return o[t] && o[t] !== key; }).map(function (t) { return '<div class="mg-cc' + (t === c.type ? ' swap' : '') + '">' + (t === c.type ? '<div class="mg-swap">Now in this spot (would swap):</div>' : '') + cardHtml(o[t], 'full', r) + '</div>'; }).join('') +
        (SLOT_ORDER.filter(function (t) { return o[t] && o[t] !== key; }).length ? '' : '<p class="hint">This set is empty.</p>');
      $('.mg-pl', m).innerHTML = (here === r ? '<p class="hint">' + c.label + ' is in this set.</p>' : '<button type="button" class="btn" data-put="1">Put ' + c.label + ' in Set ' + (r + 1) + (occ && occ !== key ? ' (swap with ' + S.cards[occ].label + ')' : '') + '</button>') +
        (here >= 0 ? ' <button type="button" class="btn ghost" data-back="1">Back to the tray</button>' : '');
    }
    fillCompare();
    var svg = $('.mg-big svg', m); if (svg) readout(svg, S.B.fns[c.si].graph);
    $('.mg-x', m).focus();
  }
  function firstOpen() { for (var r = 0; r < S.N; r++) if (!S.ok[r]) return r; return 0; }
  function readout(svg, g) {
    var q = graphGeom(g), cross = $('.mg-cross', svg), txt = $('.mg-ctx', svg), bg = $('.mg-cbg', svg);
    var show = function (e) {
      var pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
      var p = pt.matrixTransform(svg.getScreenCTM().inverse());
      var gx = g.xmin + (p.x - PAD) / q.sx, gy = g.ymax - (p.y - PAD) / q.sy;
      if (gx < g.xmin - 0.3 || gx > g.xmax + 0.3 || gy < g.ymin - 0.3 || gy > g.ymax + 0.3) { cross.setAttribute('visibility', 'hidden'); return; }
      gx = Math.round(gx / g.xstep) * g.xstep; gy = Math.round(gy / g.ystep) * g.ystep;
      gx = Math.max(g.xmin, Math.min(g.xmax, gx)); gy = Math.max(g.ymin, Math.min(g.ymax, gy));
      var cx = q.X(gx), cy = q.Y(gy), s = '(' + gx + ', ' + gy + ')';
      $('circle', cross).setAttribute('cx', cx); $('circle', cross).setAttribute('cy', cy);
      var w = s.length * 8 + 10, tx = cx + 10 + w > VB ? cx - 10 - w : cx + 10, ty = cy - 30 < 0 ? cy + 10 : cy - 30;
      bg.setAttribute('x', tx); bg.setAttribute('y', ty); bg.setAttribute('width', w); txt.setAttribute('x', tx + 5); txt.setAttribute('y', ty + 16); txt.textContent = s.replace(/-/g, '−');
      cross.setAttribute('visibility', 'visible');
    };
    svg.addEventListener('pointermove', show); svg.addEventListener('pointerdown', show);
    svg.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') cross.setAttribute('visibility', 'hidden'); });
  }

  /* ---------------- finish ---------------- */
  function finish() {
    if ($('.mg-done')) return;
    var m = doc.createElement('div'); m.className = 'mg-modal mg-done'; m.setAttribute('role', 'dialog'); m.setAttribute('aria-modal', 'true'); m.setAttribute('aria-label', 'All sets matched');
    m.innerHTML = '<div class="mg-mbox mg-win"><div class="mg-burst" aria-hidden="true">★</div><h2>All ' + S.N + ' sets matched!</h2>' +
      '<p class="mg-stats"><span><b>' + fmtTime(S.elapsed) + '</b> time</span><span><b>' + S.checks + '</b> check' + (S.checks === 1 ? '' : 's') + '</span><span><b>' + S.hints + '</b> hint' + (S.hints === 1 ? '' : 's') + '</span></p>' +
      '<p class="hint">' + esc(unitName(S.cfg.unit)) + ' · ' + esc(levelName(S.cfg.unit,S.cfg.level)) + (S.cfg.v ? ' · Version ' + 'ABC'[S.cfg.v] : '') + ' · ' + (S.wrongChecks ? S.wrongChecks + ' check' + (S.wrongChecks === 1 ? '' : 's') + ' found a mistake' : 'no mistakes found by Check') + '</p>' +
      '<div class="mg-wbtn"><button type="button" class="btn ghost" data-act="review">Review my sets</button><button type="button" class="btn" data-act="again">Play again with new cards</button></div></div>';
    doc.body.appendChild(m);
    m.addEventListener('click', function (e) {
      var a = e.target.closest('[data-act]'); if (!a && e.target !== m) return;
      m.remove();
      if (a && a.getAttribute('data-act') === 'again') go(Object.assign({}, S.cfg, { seed: Math.floor(Math.random() * 1e9), v: 0 }));
      else { S.expand = {}; for (var r = 0; r < S.N; r++) S.expand[r] = true; draw(); }
    });
    $('[data-act="again"]', m).focus();
  }

  /* ---------------- setup ---------------- */
  function setup(c) {
    S = null; $$('.mg-modal').forEach(function (m) { m.remove(); }); doc.body.classList.remove('mg-modal-open', 'mg-selecting');
    var units = supportedUnits(), U = M.UNITS[c.unit];
    var famBox = function (unit, chosen) { var u = M.UNITS[unit]; return u.fams.length > 1 ? u.fams.map(function (f) { return '<label class="chk"><input type="checkbox" class="mgFam" value="' + f + '"' + (chosen.indexOf(f) >= 0 ? ' checked' : '') + '><span>' + esc(M.FAMILIES[f]) + '</span></label>'; }).join('') : '<p class="hint">Function type: ' + esc(M.FAMILIES[u.fams[0]]) + '.</p>'; };
    $('#mgApp').innerHTML = '<div class="mg-setup card"><h1>Function Matching Game</h1>' +
      '<p class="hint">Match each function’s <b>graph</b>, <b>equation</b>, <b>table</b> and <b>description</b>. Every card fits exactly one set. These are the same verified cards as the printable Matching Card Sort.</p>' +
      '<label class="field"><span class="lbl">Unit</span><select id="suUnit">' + Array.from(new Set(units.map(function(u){return u.course;}))).map(function (course) { var us = units.filter(function (u) { return u.course === course; }); return us.length ? '<optgroup label="' + course + '">' + us.map(function (u) { return '<option value="' + u.id + '"' + (u.id === c.unit ? ' selected' : '') + '>' + esc(u.name) + '</option>'; }).join('') + '</optgroup>' : ''; }).join('') + '</select></label>' +
      '<fieldset class="field"><legend class="lbl">Level</legend><div class="mg-levels">' + Object.keys(NS.LEVELS).map(function (id) { return '<label class="chk"><input type="radio" name="suLevel" value="' + id + '"' + (c.level === id ? ' checked' : '') + '><span>' + esc(/^(prealgebra7?|math6)-/.test(c.unit)?levelName(c.unit,id):NS.LEVELS[id].long) + '</span></label>'; }).join('') + '</div></fieldset>' +
      '<fieldset class="field"><legend class="lbl">Function types</legend><div id="suFams">' + famBox(c.unit, c.fams) + '</div></fieldset>' +
      '<label class="field"><span class="lbl">Number of sets</span><select id="suSets">' + [4, 6, 8, 10].map(function (n) { return '<option value="' + n + '"' + (c.sets === n ? ' selected' : '') + '>' + n + ' sets (' + 4 * n + ' cards)</option>'; }).join('') + '</select></label>' +
      '<label class="chk"><input type="checkbox" id="suEq"' + (c.eq ? ' checked' : '') + '><span>Start with each equation already in its set <small>Recommended: students find the graph, table and description for each equation.</small></span></label>' +
      '<label class="chk"><input type="checkbox" id="suHints"' + (c.hints ? ' checked' : '') + '><span>Allow hints</span></label>' +
      '<div class="mg-sbtn"><button type="button" class="btn" id="suGo">Start matching</button><button type="button" class="btn ghost" id="suLink">Copy student link</button></div>' +
      '<p class="hint">“Copy student link” makes one set of cards for the whole class. To play the cards you printed, use <b>Play online</b> in the printable generator.</p><p class="hint" id="suErr"></p></div>';
    var read = function () {
      var unit = $('#suUnit').value, u = M.UNITS[unit];
      var fams = u.fams.length > 1 ? $$('.mgFam').filter(function (b) { return b.checked; }).map(function (b) { return b.value; }) : u.fams.slice();
      return { unit: unit, level: ($$('input[name=suLevel]').filter(function (r) { return r.checked; })[0] || {}).value || 'cp1', sets: +$('#suSets').value, fams: fams, seed: c.unit === unit && c.seed !== null ? c.seed : null, v: 0, eq: $('#suEq').checked ? 1 : 0, hints: $('#suHints').checked ? 1 : 0 };
    };
    $('#suUnit').onchange = function () { var u = M.UNITS[$('#suUnit').value]; $('#suFams').innerHTML = famBox($('#suUnit').value, u.def); };
    var start = function (link) {
      var n = read();
      if (!n.fams.length) { $('#suErr').textContent = 'Choose at least one function type.'; return; }
      n.seed = Math.floor(Math.random() * 1e9);
      var test = PR.buildMatch(builderCfg(n), 0);
      if (test.error) { $('#suErr').textContent = test.error; return; }
      if (link) { copy(linkOf(n), 'Student link copied.'); $('#suErr').innerHTML = 'Link copied: <a href="' + esc(linkOf(n)) + '">' + esc(linkOf(n)) + '</a>'; return; }
      go(n);
    };
    $('#suGo').onclick = function () { start(false); };
    $('#suLink').onclick = function () { start(true); };
    if (!$('#mgToast')) { var t = doc.createElement('div'); t.id = 'mgToast'; t.className = 'mg-toast'; $('#mgApp').appendChild(t); }
    $('#mgCrumb').textContent = 'Function Matching Game';
  }
  function go(cfg) {
    try { G.history.replaceState(null, '', '#' + hashOf(cfg)); } catch (e) { G.location.hash = hashOf(cfg); }
    start(cfg);
  }
  function start(cfg) {
    var st = newState(cfg);
    if (st.error) { setup(cfg); $('#suErr').textContent = st.error; return; }
    $$('.mg-modal').forEach(function (m) { m.remove(); }); doc.body.classList.remove('mg-modal-open', 'mg-selecting', 'mg-dragging');
    S = st; S.expand = {};
    $('#mgCrumb').textContent = 'Function Matching · ' + unitName(cfg.unit);
    doc.title = 'Function Matching Game · ' + unitName(cfg.unit).replace(/^Unit \d+ · /, '') + (/^prealgebra-/.test(cfg.unit) ? '' : ' · Mr. K\'s Classroom');
    shell(); draw(); tick();
    if (S.done) say('You matched every set. Press <b>More ▸ Start over</b> to play again.', 'good');
    else if (S.resumed) say('Welcome back! Your cards are where you left them.');
  }
  G.addEventListener('hashchange', function () { var c = parseHash(); if (c.seed === null) setup(c); else if (!S || hashOf(c) !== hashOf(S.cfg)) start(c); });

  /* ---------------- theme + boot ---------------- */
  $('#themeBtn') && ($('#themeBtn').onclick = function () { var cur = doc.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'; doc.documentElement.setAttribute('data-theme', cur); lsSet('mkws-theme', cur); });
  (function () { var t = lsGet('mkws-theme'); if (t) doc.documentElement.setAttribute('data-theme', t); })();
  var c0 = parseHash();
  if (c0.seed === null) setup(c0); else start(c0);
  G.MKMATCHGAME = { state: function () { return S; }, place: function (k, r) { return place(k, r, true); }, check: check, hint: hint, restart: restart, link: function () { return S && linkOf(S.cfg); } };   // for tests
})(window);
