/* Paths are relative to the course site's root. Previews are bundled local assets. */
export function resourceThumbnail(path, unitId) {
 const url=new URL(path,'https://classroom.invalid/');
 if (/\/artifacts\/financial-algebra-project-/.test(url.pathname)) return url.pathname.slice(1).replace(/index\.html$/,'hero.svg');
 let kind=url.searchParams.get('mode');
 if(url.pathname.includes('/flashcards/'))kind='flashcards';
 if(url.pathname.includes('-cheat-sheet/'))kind='cheat-sheet';
 if(url.pathname.includes('/decision-lab/'))kind=url.searchParams.has('teacher')?'guide':'lab';
 return `thumbs/financial-algebra/${unitId}-${kind||'worksheet'}.${kind==='cheat-sheet'?'jpg':'svg'}`;
}
