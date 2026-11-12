/* Unified Grade 5 staging class. Uses the same Classroom course, unit, banner,
   resource-card and pagination components as Algebra 1/Geometry.
   The thirteen-unit source outline remains available inside the course page;
   published resources use the eleven approved Grade 5 question-bank units. */
(function (G) {
  'use strict';
  var bundle=G.MK_GRADE5_RESOURCES;
  var course=bundle&&bundle.course;
  var main=document.getElementById('main');
  var search=document.getElementById('q');
  var back=document.getElementById('backBtn');
  if(!course||!main||!search||!back){
    if(main)main.innerHTML='<div class="wrap empty"><h2>Grade 5 resources unavailable</h2><p>Please refresh the page.</p></div>';
    return;
  }

  var C='math5';
  var escape=function(v){return String(v==null?'':v).replace(/[&<>"']/g,function(ch){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch];});};
  var unitTitle=function(u){return 'Unit '+(course.units.indexOf(u)+1)+': '+u.name;};
  var unitLink=function(u){return '#'+C+'.'+u.id;};
  var skillNames=function(u){
    var catalog=G.MK_COURSE_CATALOG;
    return catalog&&catalog.getSkills?catalog.getSkills(C,u.id):[];
  };
  var counts=function(u){return u.artifacts.length;};
  function crumbs(items){
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>'+items.map(function(item,i){
      return '<li>'+(i===items.length-1?'<span aria-current="page">'+escape(item[0])+'</span>':
        '<a href="'+escape(item[1])+'">'+escape(item[0])+'</a>')+'</li>';
    }).join('')+'</ol></nav>';
  }
  function hero(contents,showArt){
    return '<section class="band" data-course="'+C+'" data-color="sunshine"><div class="wrap">'+
      (showArt?'<div class="band-grid"><div>'+contents+'</div><div class="band-art" aria-hidden="true">'+
        '<img class="outline-art" width="230" height="195" src="./assets/course-icons/grade5.svg" alt=""></div></div>':contents)+
      '</div></section>';
  }
  function skillChips(names){
    return '<ul class="unit-skills">'+names.map(function(name){return '<li class="unit-skill">'+escape(name)+'</li>';}).join('')+'</ul>';
  }
  function unitCard(u){
    var skills=skillNames(u),first=skills.slice(0,4),more=skills.slice(4);
    return '<li><div class="unit algebra-unit-card" data-course="math5" data-color="sunshine">'+
      '<h3><a class="unit-title-link" href="'+unitLink(u)+'"><span class="unit-num">Unit '+(course.units.indexOf(u)+1)+'</span>'+escape(u.name)+'</a></h3>'+
      '<div class="unit-meta" data-lesson-list="true">'+skillChips(first)+
      (more.length?'<details class="unit-lesson-details"><summary>Show all '+skills.length+' skills</summary>'+skillChips(more)+'</details>':'')+
      '</div><span class="unit-course-status">'+counts(u)+' resources · Remedial / Standard / Advanced</span>'+
      '<a class="unit-open-link" href="'+unitLink(u)+'">Open unit →</a></div></li>';
  }
  function unitPager(u){
    var index=course.units.indexOf(u);
    var link=function(next,direction){
      if(!next)return '<span class="pager-spot"></span>';
      return '<a class="pager-link pager-'+direction+'" href="'+unitLink(next)+'" rel="'+direction+'">'+
        (direction==='prev'?'<span class="pager-arrow" aria-hidden="true">←</span>':'')+
        '<span class="pager-text"><span class="pager-dir">'+(direction==='prev'?'Previous unit':'Next unit')+'</span>'+
        '<span class="pager-name">'+escape(unitTitle(next))+'</span></span>'+
        (direction==='next'?'<span class="pager-arrow" aria-hidden="true">→</span>':'')+'</a>';
    };
    return '<nav class="unit-pager" data-course="math5" data-color="sunshine" aria-label="Unit navigation">'+
      link(course.units[index-1],'prev')+link(course.units[index+1],'next')+'</nav>';
  }
  var sections=[
    {key:'Game',id:'games',title:'Games',icon:'🎮',hint:'Kid-friendly games for independent practice and whole-class review.'},
    {key:'Study Guide',id:'study-guides',title:'Study Guides',icon:'📚',hint:'Flashcards, printable cheat sheets, and an Understanding Check.'},
    {key:'Printable',id:'printables',title:'Teacher Tools',icon:'🖨️',hint:'Build lesson plans, worksheets, assessments and printable activities from this unit’s questions.'},
    {key:'Interactive',id:'interactive',title:'Interactive Math',icon:'📐',hint:'Hands-on visual models with printable student worksheets.'},
    {key:'Project',id:'projects',title:'Projects',icon:'🧩',hint:'Real-life projects with three differentiated versions and a teacher guide.'}
  ];
  function sortCards(items,category){
    var priority=category==='Study Guide'?{'Flashcards':0,'Cheat Sheet':1,'Understanding Check':2}:null;
    if(!priority)return items;
    return items.slice().sort(function(a,b){return (priority[a.title]===undefined?99:priority[a.title])-
      (priority[b.title]===undefined?99:priority[b.title]);});
  }
  function resourceCard(a,category){
    var levelChoices = (G.MK_GRADE5_STUDENT_LINKS && G.MK_GRADE5_STUDENT_LINKS.hasLevel(a)) ?
      '<label class="g5-student-level-label">Student level <select class="g5-student-level" aria-label="Student link level for '+escape(a.title)+'">'+
      '<option value="cp2">Remedial</option><option value="cp1" selected>Standard</option><option value="honors">Advanced</option>'+
      '</select></label>' : '';
    return '<li class="card g5-resource-card" data-course="math5" data-color="sunshine">'+
      '<a class="thumb g5-resource-image-link" href="'+escape(a.path)+'" aria-label="Open '+escape(a.title)+'">'+
      '<img src="'+escape(a.thumb)+'" alt="" width="720" height="450" loading="lazy" decoding="async"></a>'+
      '<div class="card-body"><div class="where">'+escape(category)+'</div>'+
      '<h3><a href="'+escape(a.path)+'">'+escape(a.title)+'</a></h3>'+
      '<p class="desc">'+escape(a.description||'')+'</p>'+
      '<div class="actions g5-card-actions"><a class="btn btn-open" href="'+escape(a.path)+'">Open resource →</a></div>'+
      '<div class="g5-student-share">'+levelChoices+
      '<button type="button" class="g5-student-copy" data-g5-share="1" data-path="'+escape(a.path)+'"'+
      ' data-type="'+escape(a.type)+'" data-title="'+escape(a.title)+'">Copy student link</button>'+
      '<span class="g5-student-status" role="status" aria-live="polite"></span></div>'+
      '</div></li>';
  }
  function sectionHtml(u,group){
    var items=sortCards(u.artifacts.filter(function(a){return a.type===group.key;}),group.key);
    if(!items.length)return '';
    return '<section class="algebra-unit-section g5-content-section" id="g5-'+group.id+'">'+
      '<h2>'+group.title+'</h2><p class="algebra-section-intro">'+escape(group.hint)+'</p>'+
      '<ul class="cards grouped-cards">'+items.map(function(a){return resourceCard(a,group.title);}).join('')+'</ul></section>';
  }
  function shortcuts(u){
    var rows=sections.filter(function(group){
      return u.artifacts.some(function(a){return a.type===group.key;});
    });
    return '<section class="generator-banner compact g5-shortcuts">'+
      '<div class="generator-banner-heading"><h2>What would you like to do with this unit?</h2></div>'+
      '<ul class="generator-shortcuts">'+rows.map(function(group){
        return '<li><button type="button" class="generator-shortcut" data-g5-scroll="g5-'+group.id+'">'+
          '<span class="generator-shortcut-icon" aria-hidden="true">'+group.icon+'</span>'+
          '<span class="generator-shortcut-copy"><strong>'+group.title+'</strong></span></button></li>';
      }).join('')+'</ul></section>';
  }
  function unitView(u){
    var skills=skillNames(u);
    var intro=crumbs([['Home','index.html'],['5th Grade Math','#'],[unitTitle(u),null]])+
      '<h1 tabindex="-1">'+escape(unitTitle(u))+'</h1>'+
      '<p class="band-meta">'+skills.length+' skills · Remedial · Standard · Advanced</p>';
    var body=unitPager(u)+shortcuts(u)+
      sections.map(function(group){return sectionHtml(u,group);}).join('')+
      '<section class="algebra-unit-section" id="g5-skills"><h2>Skills in this unit</h2>'+
      skillChips(skills)+'</section>'+unitPager(u);
    return hero(intro,false)+'<section class="section"><div class="wrap algebra-unit-layout">'+body+'</div></section>';
  }
  function courseView(){
    var term=search.value.trim().toLocaleLowerCase();
    var visible=course.units.filter(function(u){
      return !term||(u.name+' '+skillNames(u).join(' ')).toLocaleLowerCase().includes(term);
    });
    var intro=crumbs([['Home','index.html'],['5th Grade Math',null]])+
      '<h1 tabindex="-1">5th Grade Math</h1>'+
      '<p class="band-blurb">Colorful math games, practice, visual explorations, study guides and projects — designed for fifth graders.</p>'+
      '<p class="band-meta">11 topic units · 55 skills · 4,950 approved questions · three difficulty levels</p>';
    var body='<h2 class="course-units-title">Browse by unit</h2>'+
      '<p class="g5-course-note">Choose a unit to find the same familiar sections: Games, Study Guides, Teacher Tools, Interactive Math, and Projects. Teacher Tools build a lesson plan, worksheet, assessment or printable activity from the same approved questions.</p>'+
      (visible.length?'<ul class="units">'+visible.map(unitCard).join('')+'</ul>':
        '<div class="empty"><h2>No matching units</h2><p>Try a different skill or topic.</p></div>')+
      '<details class="g5-source-outline"><summary>Original curriculum sequence (13 pacing units)</summary>'+
      '<div id="g5OriginalOutline" class="g5-original-content">Loading source curriculum…</div></details>';
    return hero(intro,true)+'<section class="section"><div class="wrap">'+body+'</div></section>';
  }
  function fillSourceOutline(){
    var node=document.getElementById('g5OriginalOutline');
    if(!node)return;
    G.fetch('./course-outlines/grade5.json').then(function(res){
      if(!res.ok)throw Error('Could not load curriculum outline');return res.json();
    }).then(function(data){
      if(!document.getElementById('g5OriginalOutline'))return;
      node.innerHTML='<p>This original 13-unit scope and sequence is retained for reference. The interactive resource library above follows the 11 topic units used by the approved question banks.</p>'+
        '<ol class="g5-original-units">'+data.units.map(function(u){
          return '<li><strong>'+escape(u.name)+'</strong> <span>('+u.skills.length+' learning targets)</span>'+
            '<details><summary>Show learning targets</summary>'+skillChips(u.skills)+'</details></li>';
        }).join('')+'</ol>';
    }).catch(function(){if(node.isConnected)node.textContent='The source curriculum outline could not be loaded.';});
  }
  function currentUnit(){
    var raw=G.location.hash.slice(1).split('?')[0];
    try{raw=decodeURIComponent(raw);}catch(e){}
    if(raw.indexOf(C+'.')!==0)return null;
    return course.units.find(function(u){return u.id===raw.slice(C.length+1);})||null;
  }
  function render(){
    var u=currentUnit();
    main.innerHTML=u?unitView(u):courseView();
    back.style.visibility=u?'visible':'hidden';
    search.style.visibility=u?'hidden':'visible';
    document.title=(u?unitTitle(u)+' | ':'')+'5th Grade Math | Mr. K’s Classroom — Development';
    if(!u)fillSourceOutline();
  }
  document.getElementById('skip').addEventListener('click',function(){main.focus();});
  main.addEventListener('click',function(e){
    var share=e.target.closest('button[data-g5-share]');
    if(share){
      var card=share.closest('.g5-resource-card');
      var status=card.querySelector('.g5-student-status');
      var levelSelect=card.querySelector('.g5-student-level');
      var resource={path:share.getAttribute('data-path'),type:share.getAttribute('data-type'),
        title:share.getAttribute('data-title')};
      var url;
      try{
        url=G.MK_GRADE5_STUDENT_LINKS.destination(resource,levelSelect?levelSelect.value:'cp1',G.location.href);
      }catch(err){status.textContent='Unable to make this link.';return;}
      function manual(){
        status.textContent='Copy the student link from the dialog.';
        if(typeof G.prompt==='function') G.prompt('Copy student link:',url);
        else status.textContent='Copy this student link: '+url;
      }
      if(G.navigator && G.navigator.clipboard && G.navigator.clipboard.writeText){
        G.navigator.clipboard.writeText(url).then(function(){
          status.textContent='Student link copied!';
        }).catch(manual);
      }else manual();
      return;
    }
    var button=e.target.closest('[data-g5-scroll]');
    if(!button)return;
    var target=document.getElementById(button.getAttribute('data-g5-scroll'));
    if(target)target.scrollIntoView({behavior:'smooth',block:'start'});
  });
  back.addEventListener('click',function(){G.location.hash='';render();G.scrollTo(0,0);});
  document.getElementById('searchForm').addEventListener('submit',function(e){
    e.preventDefault();if(currentUnit())G.location.hash='';render();main.focus();
  });
  search.addEventListener('input',function(){if(!currentUnit())render();});
  G.addEventListener('hashchange',function(){render();G.scrollTo(0,0);});
  render();
})(window);
