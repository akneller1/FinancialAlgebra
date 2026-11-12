import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const read = path => fs.readFileSync(new URL('../' + path, import.meta.url), 'utf8');
const css = read('worksheet-generator/grade5/generators.css');
const app = read('worksheet-generator/grade5/generators.js');

test('print-only pages remain hidden during normal preview', () => {
  assert.match(css, /#printRoot\s*\{\s*display:\s*none\s*;/);
});

test('the pagination measurement stage remains layoutable during Ctrl+P', () => {
  const printRules = css.slice(css.indexOf('@media print'));
  assert.match(printRules, /\.pl-measure-stage\s*\{\s*display:\s*block\s*!important/);
  assert.doesNotMatch(printRules, /\.pl-measure-stage\s*\{\s*display:\s*none/);
});

test('printing waits for stable preview assets and page measurements', () => {
  assert.match(app, /doc\.fonts\s*&&\s*doc\.fonts\.ready/);
  assert.match(app, /img\.decode\(\)/);
  assert.match(app, /Promise\.resolve\(previewReady\)\.then/);
});
