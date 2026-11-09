import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
test('standalone course uses the production classroom design vocabulary',()=>{
  const shell=read('index.html'),site=read('src/site.js'),css=read('styles.css');
  for(const name of ['site-header','brand','band','algebra-unit-card','generator-banner','algebra-unit-section','grouped-cards','unit-pager']) {
    assert.ok(site.includes(name)||shell.includes(name),'Missing classroom component '+name);
    assert.ok(css.includes(name),'Missing copied classroom style '+name);
  }
});
test('links to the real pilot and leaves the other units clearly planned',()=>{
  const site=read('src/site.js');
  assert.ok(site.includes("lab.html#"));
  assert.ok(site.includes('Coming soon'));
  assert.ok(site.includes("lab.html?print=worksheet&unit="));
  assert.ok(existsSync(new URL('../lab.html',import.meta.url)));
  assert.ok(existsSync(new URL('../lab.css',import.meta.url)));
  assert.ok(!site.includes('mrksclassroom.com/worksheet-generator'));
});
