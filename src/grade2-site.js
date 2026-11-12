import {mountOutline} from './outline-template.js?v=preload-20261112';
const root=document.getElementById('main');
fetch('./course-outlines/grade2.json')
  .then(r=>{if(!r.ok)throw new Error('Grade 2 curriculum could not be loaded');return r.json()})
  .then(course=>mountOutline(course,{page:'grade2.html'}))
  .catch(error=>{
    root.innerHTML='<div class="wrap"><section class="empty"><h2>Course outline unavailable</h2><p>Refresh the page or inspect the source data on GitHub.</p></section></div>';
    console.error(error);
  });
