/* Independent check of the four skills added 2026-11-16: every numeric answer is recomputed from the numbers in
 * its prompt, without FA_MATH, and the new skills are wired into the course, banks, lessons and decks. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { course } from '../src/course.js';
const root = new URL('../', import.meta.url);
const bank = (u) => JSON.parse(readFileSync(new URL(`financial/banks/${u}.json`, root), 'utf8'));
const money = (s) => [...s.matchAll(/[−-]?\$([\d,]+(?:\.\d+)?)/g)].map(m => Number(m[1].replace(/,/g, '')));
const pcts = (s) => [...s.matchAll(/([\d.]+)%/g)].map(m => Number(m[1]) / 100);
const n = (s, re) => Number(s.match(re)[1].replace(/,/g, ''));
const r2 = (x) => Math.round(x * 100 + 1e-9) / 100;

const CHECK = {
  'cs-score-cost': (p) => { const [, a, b] = money(p), m = n(p, /for (\d+) months/); return b * m - a * m; },
  'cs-overall-util': (p) => { const [b1, l1, b2, l2] = money(p); return (b1 + b2) / (l1 + l2) * 100; },
  'cs-avg-age': (p) => { const [a, b, c] = p.match(/are (\d+), (\d+) and (\d+) years old/).slice(1).map(Number); return (b + c) / 2; },
  'tco-annual': (p) => { const [pay, ins, gas, maint] = money(p), miles = n(p, /drives ([\d,]+) miles/), mpg = n(p, /at (\d+) MPG/); return r2(pay * 12 + ins * 12 + r2(miles / mpg * gas) + maint); },
  'fuel-compare': (p) => { const [gas] = money(p), miles = n(p, /drives ([\d,]+) miles/), a = n(p, /Car A gets (\d+)/), b = n(p, /Car B gets (\d+)/); return miles / a * gas - miles / b * gas; },
  'car-depreciate': (p) => { const [price] = money(p), [rate] = pcts(p), y = n(p, /after (\d+) years/); return price * (1 - rate) ** y; },
  'cost-mile': (p) => { const [tot] = money(p), miles = n(p, /drives ([\d,]+) miles/); return tot / miles; },
  'rent-30': (p) => { const [h] = money(p); return h * 40 * 52 / 12 * 0.3; },
  'move-in': (p) => { const [rent, dep, app, truck] = money(p), last = /last month/.test(p); return rent * (last ? 2 : 1) + dep + app + truck; },
  'prorate': (p) => { const [rent] = money(p), day = n(p, /on day (\d+)/), days = n(p, /of a (\d+)-day/); return rent / days * (days - day + 1); },
  'roommate-split': (p) => { const [rent, util] = money(p), [share] = pcts(p); return rent * share + util / 2; },
  'deposit-back': (p) => { const [dep, clean, hole] = money(p); return dep - clean - hole; },
  'fake-check': (p) => { const [price, check, fee] = money(p); return check - price + fee; },
  'debit-liability': (p) => { const m = money(p), stolen = m[0]; return Math.min(stolen, /within two business days of learning/.test(p.split('reports it')[1]) ? 50 : 500); },
  'credit-vs-debit': (p) => { const [stolen] = money(p); return Math.min(stolen, 500) - Math.min(stolen, 50); }
};
const TOL = { 'cs-score-cost': 0.06, 'cs-overall-util': 0.06, 'tco-annual': 0.03, 'fuel-compare': 0.03 };

test('new skills are in the course and every unit bank, with a lesson each', () => {
  const want = { banking: 'Spot scams and protect your identity', credit: 'Understand credit scores and reports', borrowing: 'Calculate the total cost of car ownership', housing: 'Plan the costs of renting' };
  for (const [u, name] of Object.entries(want)) {
    assert.equal(course.units.find(x => x.id === u).skills[4], name);
    const b = bank(u), id = `${u}-skill-05`;
    assert.equal(b.skills[4].id, id); assert.equal(b.lessons.filter(l => l.skill === 5).length, 1);
    assert.ok(b.questions.filter(q => q.skillId === id).length >= 30, id + ' needs 30+ questions');
    assert.ok(b.vocab.some(v => v.skill === 5), id + ' vocabulary');
  }
});

test('every new-skill numeric answer recomputes independently from its prompt', () => {
  let count = 0; const used = new Set();
  for (const u of ['banking', 'credit', 'borrowing', 'housing']) for (const q of bank(u).questions.filter(q => q.skillId.endsWith('-05') && q.format === 'short-answer')) {
    const f = CHECK[q.family]; assert.ok(f, 'no check for ' + q.family); used.add(q.family);
    const want = f(q.prompt), got = q.numeric.value;
    assert.ok(Math.abs(want - got) <= (TOL[q.family] ?? 0.011), `${q.id}: prompt gives ${want}, key ${got}\n${q.prompt}`);
    count++;
  }
  assert.equal(used.size, Object.keys(CHECK).length);
  assert.ok(count >= 90, 'found ' + count);
});
