#!/usr/bin/env node
/* Grade 2 preview gate: run on an assembled development site, never raw sources.
 * No public deployment occurs here. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const root=path.resolve(process.argv[2]||'_site');
const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.woff2':'font/woff2'};
const server=http.createServer((req,res)=>{
 let u;try{u=decodeURIComponent(new URL(req.url,'http://localhost').pathname);}catch{res.writeHead(400);res.end();return;}
 const file=path.resolve(root,'.'+u+(u.endsWith('/')?'index.html':''));
 if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404);res.end('not found');return;}
 res.writeHead(200,{'content-type':types[path.extname(file)]||'application/octet-stream'});fs.createReadStream(file).pipe(res);
});
(async()=>{
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'question-banks/manifest.json'),'utf8'));
 const entries=manifest.banks.filter(b=>b.courseId==='grade2');
 assert.equal(entries.length,12,'Grade 2 must have 12 assembled native banks');
 const unit=entries[0].unitId;
 assert.ok(fs.existsSync(path.join(root,'grade2/question-banks/math2/checks',unit+'.json')),'Dedicated check bank missing from assembly');
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base='http://127.0.0.1:'+server.address().port+'/';
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 try{
  await page.goto(base+'#grade2.'+unit,{waitUntil:'load'});
  await page.waitForSelector('[data-path*="grade2-games.html"]',{timeout:25000});
  const courses=await page.evaluate(()=>window.LIBRARY.courses.filter(c=>c.id==='grade2'));
  assert.equal(courses.length,1,'Exactly one Grade 2 course must appear');
  assert.equal(courses[0].units.length,12,'All 12 Grade 2 units must appear');
  const gameCard=page.locator('[data-path*="grade2-games.html"]').first();
  const href=await gameCard.locator('a[href*="grade2-games.html"]').first().getAttribute('href');
  assert.ok(href&&href.startsWith('grade2/worksheet-generator/grade2-games.html?'),'Game must link directly to the Grade 2 engine');
  await gameCard.locator('button.share-student').click();
  const dialog=page.locator('#integrated-skill-share-dialog');
  await dialog.waitFor({state:'visible',timeout:10000});
  const boxes=dialog.locator('fieldset input[type=checkbox]');
  assert.ok(await boxes.count()>0,'Share dialog must offer unit skill selection');
  if(await boxes.count()>1)await boxes.last().uncheck();
  await dialog.getByText('Generate student link',{exact:true}).click();
  const studentUrl=await dialog.locator('input[aria-label="Student link"]').inputValue();
  const parsed=new URL(studentUrl);
  assert.equal(parsed.searchParams.get('student'),'1');
  assert.ok(parsed.searchParams.get('skills'),'Student link must preserve selected skills');
  assert.equal(JSON.parse(parsed.searchParams.get('skills')).length,await boxes.count()-(await boxes.count()>1?1:0));
  await dialog.getByText('Cancel',{exact:true}).click();
  const student=await browser.newPage(),studentErrors=[];
  student.on('pageerror',e=>studentErrors.push(e.message));
  await student.goto(new URL(parsed.pathname+parsed.search,base).href,{waitUntil:'load'});
  try { await student.waitForSelector('.el-setup, .el-stage',{timeout:15000}); } catch(e) { console.error('Student URL',student.url(),'JS errors',studentErrors,'body',(await student.locator('body').innerText().catch(()=>'')).slice(0,500)); throw e; }
  assert.deepEqual(studentErrors,[],'Student game must boot without JS errors');
  await student.close();
  const check=await browser.newPage(),checkErrors=[],checkRequests=[];
  check.on('pageerror',e=>checkErrors.push(e.message));
  check.on('request',req=>{if(req.url().includes('/question-banks/math2/checks/'))checkRequests.push(req.url());});
  await check.goto(base+'grade2/worksheet-generator/grade2-understanding-check.html?unit='+encodeURIComponent(unit),{waitUntil:'load'});
  try {
    await check.waitForSelector('dialog.teacher-skills, .el-setup, .el-stage',{timeout:15000});
    const teacherSkills=check.locator('dialog.teacher-skills');
    if(await teacherSkills.count()) {
      await teacherSkills.getByText('Continue',{exact:true}).click();
      await check.waitForSelector('.el-setup, .el-stage',{timeout:15000});
    }
  }
  catch (e) {
    console.error('Understanding Check URL:',check.url(),
      'page errors:',checkErrors,
      'bank requests:',checkRequests,
      'body:',(await check.locator('body').innerText().catch(()=>'')).slice(0,900));
    throw e;
  }
  assert.ok(checkRequests.some(u=>u.includes('/checks/'+unit+'.json')),'Understanding Check must request its dedicated 318-question check-bank family');
  assert.deepEqual(checkErrors,[],'Understanding Check must boot without JS errors');
  await check.close();
  assert.deepEqual(errors,[],'Grade 2 unit view must have no JS errors');
  console.log('PASS Grade 2: 12 native banks, direct game route, skill selection and student URL, student game startup, dedicated check-bank request');
 }finally{await page.close();await browser.close();server.close();}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
