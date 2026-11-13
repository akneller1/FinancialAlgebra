#!/usr/bin/env node
// Independent learning-target/check contract, including every derived subquestion.
const fs=require('node:fs'),assert=require('node:assert/strict');
const outline=JSON.parse(fs.readFileSync('course-outlines/grade1.json'));
const specs=[
 ['add/sub','add/missing_part','add/sub/missing_part','sort_count','survey_count','survey_count','tally_one','graph_one','graph_diff'],
 ['add/sub','missing_part','eq_text','missing_part','missing_part','add/sub/missing_part','missing_part','sub','sub','sub','add/sub/missing_part','missing_part','story_equations','constructed_story'],
 ['add/missing_part','sub/missing_part','sub','bundle','tens_ones/sub','add/sub','missing_part','add/missing_part/sub','add','add3','missing_part','sub','sub','sub','sub/missing_part'],
 ['bundle','add/sub','add/sub','tens_ones','model_parts','digit_value','add/sub','which_number','symbol','sorted','equiv_ones','equiv_ones','tens_ones'],
 ['add','add','place_equation','add','regroup_remainder','place_equation','add','regroup_tens','regroup_reason'],
 ['direct_length','indirect_length','order_len','unit_layout','ruler','tens_ones','sub','sub','add/missing_part','eq_text'],
 ['shape_sides/shape_corners','solid_name','composition_shape/composition_count/composition_missing','solid_composition','partition_count','partition_count','fair_parts','partition_word','clock','clock','clock','clock_hands'],
 ['add/sub/missing_part','add/sub/missing_part','sub','missing_part','sub','missing_part','eq_text','tens_ones','tens_ones','equiv_ones','tens_ones']
];
let questions=0,leaves=0;
function leafChecks(c){
 assert(c&&c.k==='fn','Missing named mathematical check');
 if(c.fn==='tf')return leafChecks(c.inner);
 if(c.fn==='claims')return Object.values(c.table).flatMap(x=>leafChecks(x.inner));
 return [c];
}
for(const [ui,u] of outline.units.entries()){
 assert.equal(specs[ui].length,u.skills.length);
 const bank=JSON.parse(fs.readFileSync('question-banks/math1/'+u.id+'.json'));
 const checks=JSON.parse(fs.readFileSync('tools/grade1-authoring/out/'+u.id+'.checks.json'));
 for(const q of bank.questions){
  const si=Number(q.skillId.slice(-2))-1,allowed=specs[ui][si].split('/'),c=checks[q.id];
  const target='target_u'+String(ui+1).padStart(2,'0')+'_s'+String(si+1).padStart(2,'0');
  assert(c.family.includes(target),'Wrong target source '+q.id);
  for(const ck of c.parts?c.parts.flatMap(leafChecks):leafChecks(c.q)){
   assert(allowed.includes(ck.fn),'Off-target check '+ck.fn+' for '+q.id+' / '+u.skills[si]);leaves++;
  }
  questions++;
 }
}
assert.equal(questions,8370);
console.log(JSON.stringify({passed:true,skills:specs.flat().length,questions,independentTargetChecks:leaves}));
