import {mountOutline} from './outline-template.js';
const main=document.getElementById('main');
fetch('./course-outlines/grade5.json')
 .then(response=>{if(!response.ok)throw Error('Could not load Grade 5 course data');return response.json();})
 .then(course=>mountOutline(course,{page:'grade5.html'}))
 .catch(error=>{main.innerHTML='<div class="wrap"><section class="empty"><h2>Grade 5 outline unavailable</h2><p>Please refresh the page or see the repository for its curriculum data.</p></section></div>';console.error(error);});
