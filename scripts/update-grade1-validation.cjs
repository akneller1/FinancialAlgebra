#!/usr/bin/env node
// Run only after independent verification and the structural audit succeed.
const fs=require('node:fs'),assert=require('node:assert/strict');
const file='question-banks/math1/manifest.json',manifest=JSON.parse(fs.readFileSync(file)),qa=JSON.parse(fs.readFileSync('grade1-qa-report.json'));
assert.equal(qa.errors.length,0);assert.equal(qa.counts.questions,8370);
assert.equal(manifest.review.editorialApproval.approved,false);
assert(manifest.banks.every(b=>b.approved===false&&b.teacherUse===false&&b.editorialApproval==='pending'));
const rate=Number((qa.counts.exactCrossSkillDuplicateCopies/qa.counts.questions).toFixed(4));
Object.assign(manifest.review.mathematicalValidation,{date:new Date().toISOString().slice(0,10),questionsChecked:qa.counts.questions,diagrams:qa.counts.diagrams,exactCrossSkillDuplicateRate:rate});
Object.assign(manifest.review.deduplication,{exactCrossSkillDuplicates:qa.counts.exactCrossSkillDuplicateCopies,rate,policy:'No duplicate complete questions within a skill and level; repeated facts across different learning targets are allowed.'});
fs.writeFileSync(file,JSON.stringify(manifest,null,2)+'\n');
console.log('Updated validation counts; all editorial approval and bank access flags preserved.');
