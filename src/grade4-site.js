import {mountOutline} from './outline-template.js';
const main=document.getElementById('main');
fetch('./course-outlines/grade4.json')
 .then(response=>{if(!response.ok)throw Error('Could not load Grade 4 curriculum');return response.json();})
 .then(course=>mountOutline(course,{page:'grade4.html'}))
 .catch(error=>{main.innerHTML='<div class="wrap"><section class="empty"><h2>Grade 4 outline unavailable</h2><p>Please refresh the page or inspect the curriculum data in the repository.</p></section></div>';console.error(error);});
