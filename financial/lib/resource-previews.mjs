/* Paths are relative to the course site's root. Previews are bundled local assets. */
export function resourceThumbnail(path, unitId) {
 const url=new URL(path,'https://classroom.invalid/');
 if (/\/artifacts\/financial-algebra-project-/.test(url.pathname)) return `thumbs/financial-algebra/${unitId}-project-${url.pathname.split('/financial-algebra-project-')[1].split('/')[0]}.svg?v=distinct-2`;
 let kind=url.searchParams.get('mode');
 if(url.pathname.includes('/flashcards/'))kind='flashcards';
 if(url.pathname.includes('-cheat-sheet/'))kind='cheat-sheet';
 if(url.pathname.includes('/decision-lab/'))kind=url.searchParams.has('teacher')?'guide':'lab';
 return `thumbs/financial-algebra/${unitId}-${kind||'worksheet'}.${kind==='cheat-sheet'?'jpg':'svg'}?v=distinct-2`;
}

// A new URL prevents a cached pre-redesign PDF from masking the updated sheet.
export function resourceHref(path) {
 return path.includes('-cheat-sheet/cheat-sheet.pdf') ? path + (path.includes('?') ? '&' : '?') + 'v=classroom-design-2' : path;
}
