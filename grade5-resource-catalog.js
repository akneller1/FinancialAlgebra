/* Staging-only Grade 5 resource integration.
   Source bank files, uploaded projects and interactive tools are referenced, not duplicated.
   The independent Grade 5 scope/sequence in grade5.html stays unchanged. */
(function (G) {
  'use strict';
  var library=G.LIBRARY, course=library&&library.courses.find(function(c){return c.id==='math5';});
  if(!course)return;
  var projects={
    'place-value-number-sense':'sports-stats-showdown',
    'multi-digit-multiplication-division':'school-carnival-planner',
    'decimal-operations':'class-party-budget',
    'numerical-expressions-patterns':'theme-park-points',
    'fraction-addition-subtraction':'school-garden-plan',
    'fraction-multiplication-division':'recipe-remix',
    'measurement-conversions':'field-trip-packing',
    'volume-three-dimensional-figures':'miniature-city-builder',
    'coordinate-plane-graphing':'playground-designer',
    'classifying-two-dimensional-figures':'shape-mosaic-designer',
    'data-line-plots-problem-solving':'plant-growth-investigation'
  };
  var tools={
    'place-value-number-sense':['place-value-builder'],
    'multi-digit-multiplication-division':['area-model-explorer'],
    'numerical-expressions-patterns':['expression-builder'],
    'fraction-addition-subtraction':['fraction-explorer'],
    'fraction-multiplication-division':['fraction-explorer','area-model-explorer'],
    'measurement-conversions':['measurement-converter'],
    'volume-three-dimensional-figures':['volume-builder'],
    'coordinate-plane-graphing':['coordinate-explorer']
  };
  var gameDefs=[
    ['math-quest','Math Quest','quest'],['treasure-trail','Treasure Trail','treasure'],
    ['space-explorer','Space Explorer','space'],['math-builders','Math Builders','builders'],
    ['picture-reveal','Picture Reveal','reveal'],['math-race','Math Race','race'],
    ['math-soccer','Math Soccer','soccer'],['connect-four','Connect 4','connect4'],
    ['puzzle-masters','Puzzle Masters','puzzle']
  ];
  var generators=[
    ['Lesson Plan','lesson','thumbs/math5-generator-lesson.svg','Build a complete lesson with kid-friendly goals, vocabulary, worked examples, guided practice, an exit ticket and a teacher key.'],
    ['Worksheet','worksheet','thumbs/math5-generator-worksheet.svg','Choose skills, level, question format and work space, then print a Letter-size worksheet with a matching answer key.'],
    ['Assessment','assessment','thumbs/math5-generator-assessment.svg','Build a points-based assessment with standards, a time limit and a separate teacher key that reconciles to the total.'],
    ['Activity','activity','thumbs/math5-generator-activity.svg','Print a maze, color by number, matching puzzle, station set, error analysis or partner check with a teacher key.']
  ];
  var title=function(slug){return slug.split('-').map(function(x){return x.charAt(0).toUpperCase()+x.slice(1)}).join(' ');};
  var mk=function(title,path,type,thumb,description){return {title:title,path:path,type:type,thumb:thumb,description:description};};
  course.units.forEach(function(u){
    var id=u.id,e=encodeURIComponent(id),a=[]; // staged links only: omit copied Classroom generator URLs not deployed here
    function add(resource){
      if(!a.some(function(x){return x.path===resource.path;}))a.push(resource);
    }
    gameDefs.forEach(function(g){
      add(mk(g[1],'worksheet-generator/grade5-games.html?unit='+e+'&game='+g[0],
        'Game','thumbs/math5-game-'+g[2]+'.svg','Choose a level and play with questions from this unit.'));
    });
    if(id==='fraction-addition-subtraction'||id==='fraction-multiplication-division') {
      add(mk('Fraction Frenzy','worksheet-generator/grade5-games.html?unit='+e+'&game=fraction-frenzy',
        'Game','thumbs/math5-game-frenzy.svg','Match visual fractions and equivalent forms.'));
    }
    add(mk('Flashcards','worksheet-generator/grade5-flashcards.html?unit='+e,
      'Study Guide','thumbs/math5-flashcards.svg','Pictures, vocabulary and examples for independent review.'));
    add(mk('Understanding Check','worksheet-generator/grade5-understanding-check.html?unit='+e,
      'Study Guide','thumbs/math5-understanding-check.svg','Check your understanding with feedback and explanations.'));
    add(mk('Cheat Sheet','math5-'+id+'-cheat-sheet/worksheet.pdf',
      'Study Guide','thumbs/math5-'+id+'-cheat-sheet.jpg','Printable reference for this unit.'));
    generators.forEach(function(g){
      add(mk(g[0]+' Generator','worksheet-generator/grade5-generators.html?unit='+e+'&mode='+g[1],
        'Printable',g[2],g[3]));
    });
    // Error Analysis is its own discoverable resource in every unit.
    // It shares the verified Grade 5 activity engine; do not create a second bank.
    add(mk('Error Analysis','worksheet-generator/grade5-generators.html?unit='+e+'&mode=activity&kind=error',
      'Printable','thumbs/math5-generator-activity.svg',
      'Find and explain mistakes using verified Grade 5 misconceptions.'));
    (tools[id]||[]).forEach(function(slug){
      add(mk(title(slug),'math5-'+slug+'/index.html','Interactive',
        'thumbs/math5-'+slug+'.jpg','Explore an interactive model and its printable activity.'));
    });
    var project=projects[id];
    if(project) {
      add(mk(title(project),'math5-project-'+project+'/index.html','Project',
        'thumbs/math5-project-'+project+'.jpg','Student packets at three levels, slides and a teacher guide.'));
    }
    u.artifacts=a;
  });
  G.MK_GRADE5_RESOURCES={course:course,projects:projects,tools:tools,games:gameDefs};
})(typeof window!=='undefined'?window:globalThis);
