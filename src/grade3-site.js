import {mountOutline} from './outline-template.js?v=preload-20261112';
const main=document.getElementById('main');
fetch('./course-outlines/grade3.json')
 .then(response=>{if(!response.ok)throw Error('Could not load Grade 3 course data');return response.json();})
 .then(course=>mountOutline(course,{page:'grade3.html'}))
 .catch(error=>{main.innerHTML='<div class="wrap"><section class="empty"><h2>Grade 3 outline unavailable</h2><p>Please refresh the page or check the course JSON in GitHub.</p></section></div>';console.error(error);});
