/* One Grade 5-compatible resource contract for current and future elementary outlines.
   No questions are fabricated and no unfinished course is promoted to production. */
export const GAMES = [
 ['math-quest','Math Quest','quest'], ['treasure-trail','Treasure Trail','treasure'],
 ['space-explorer','Space Explorer','space'], ['math-builders','Math Builders','builders'],
 ['picture-reveal','Picture Reveal','reveal'], ['math-race','Math Race','race'],
 ['math-soccer','Math Soccer','soccer'], ['connect-four','Connect 4','connect4'],
 ['puzzle-masters','Puzzle Masters','puzzle']
];
export const GENERATORS = [['lesson','Lesson Plan'],['worksheet','Worksheet'],['activity','Activity'],['assessment','Assessment']];
export const ACTIVITIES = [['maze','Maze'],['color','Color by Number'],['matching','Matching'],['stations','Station Work'],['error','Error Analysis'],['partner','Partner Check']];
export function resourceUrl(course,unit,tool,extra={}) {
 const params = new URLSearchParams({course:course.id,unit:unit.id,tool,...extra});
 return 'worksheet-generator/elementary-resource.html?' + params;
}
export function unitResources(course,unit) {
 const make = (id,title,group,tool,extra,thumb) => ({id,title,group,path:resourceUrl(course,unit,tool,extra),thumb:'thumbs/'+thumb+'.svg'});
 const resources = GENERATORS.map(([mode,name])=>make(mode,name+' Generator','Generators','generators',{mode},'math5-generator-'+mode));
 resources.push(...ACTIVITIES.map(([kind,name])=>make('activity-'+kind,name,'Generators','generators',{mode:'activity',kind},'math5-generator-activity')));
 resources.push(...GAMES.map(([game,name,thumb])=>make(game,name,'Games','games',{game},'math5-game-'+thumb)));
 // Fraction Frenzy is deliberately unit-specific; do not advertise fraction practice in unrelated units.
 if (/fraction/i.test(unit.name)) resources.push(make('fraction-frenzy','Fraction Frenzy','Games','games',{game:'fraction-frenzy'},'math5-game-frenzy'));
 resources.push(make('flashcards','Flashcards','Study Guides','flashcards',{},'math5-flashcards'));
 resources.push(make('readiness','Readiness Check','Study Guides','check',{},'math5-understanding-check'));
 return resources;
}
