// Builds the public copy of the site into _site/ for GitHub Pages.
// Run by .github/workflows/deploy-site.yml on every push to main.
// Local preview: node scripts/build-site.mjs  (then open _site/index.html)
//
// What it does:
//  1. Copies the site, leaving out working files (audits, scripts, answer-key audits…).
//     Stops with an error if a published page still points at a left-out file.
//  2. Writes the activity catalog from data.js into index.html as plain HTML,
//     so search engines, link previews and visitors without JavaScript see it.
//  3. Makes one page per unit (u/<course>/<unit>/) plus sitemap.xml.
//  4. Adds a description, link-preview tags and a favicon to index.html.
//  5. Hides the Back button on the home page and points the logo at the home page.
//  6. Downloads the Google Fonts and serves them from the site itself
//     (falls back to Google if the download fails).

import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import crypto from "node:crypto";

const ROOT = process.cwd();
const OUT = path.join(ROOT, "_site");
const SITE_URL = (process.env.SITE_URL || "https://mrksclassroom.com/").replace(/\/?$/, "/");
const SITE_NAME = "Mr. K's Classroom";

// ---------- 1. Copy the site, minus working files ----------
const EXCLUDE_DIRS = new Set([
  ".git", ".github", "_site", "node_modules",
  "audits", "incoming", "scripts", "shots", "docs", "tools", "patches",
]);
const EXCLUDE_FILES = new Set([
  "README.md", "README-UPLOAD.txt", "teacher-key-audit.txt",
  ".git", ".gitignore", ".DS_Store",
]);
const isExcludedFile = (name) =>
  EXCLUDE_FILES.has(name) || /\.(py|pyc)$/.test(name) || /\(\d+\)\.[a-z0-9]+$/i.test(name); // "file (1).pdf" duplicates

function copyTree(src, dst, rel = "") {
  fs.mkdirSync(dst, { recursive: true });
  for (const ent of fs.readdirSync(src, { withFileTypes: true })) {
    const r = rel ? `${rel}/${ent.name}` : ent.name;
    if (ent.isDirectory()) {
      if (rel === "" && EXCLUDE_DIRS.has(ent.name)) continue;
      if (ent.name === "__pycache__" || ent.name === ".git") continue;
      copyTree(path.join(src, ent.name), path.join(dst, ent.name), r);
    } else if (ent.isFile()) {
      if (rel === "" ? isExcludedFile(ent.name) : /\.(py|pyc)$/.test(ent.name) || ent.name === ".DS_Store") continue;
      fs.copyFileSync(path.join(src, ent.name), path.join(dst, ent.name));
    }
  }
}

function walkFiles(dir, exts) {
  const out = [];
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) out.push(...walkFiles(p, exts));
    else if (exts.test(ent.name)) out.push(p);
  }
  return out;
}

fs.rmSync(OUT, { recursive: true, force: true });
copyTree(ROOT, OUT);
fs.writeFileSync(path.join(OUT, ".nojekyll"), "");

/* Refresh the common classroom presentation CSS and JavaScript on all labs
   in the built site, without editing each individual source activity. */
{
  let refreshed = 0;
  for (const file of walkFiles(path.join(OUT, "artifacts"), /index\.html$/i)) {
    const html = fs.readFileSync(file, "utf8");
    if (!html.includes("../interactive-math/lab.js")) continue;
    const next = html
      .replace(/(\.\.\/interactive-math\/lab\.js)\?v=[^"'<>\s]+/g, "$1?v=present-whole-page-20261110")
      .replace(/(\.\.\/interactive-math\/lab\.css)\?v=[^"'<>\s]+/g, "$1?v=present-whole-page-20261110");
    if (next !== html) { fs.writeFileSync(file, next); refreshed++; }
  }
  console.log("Interactive Math presentation assets versioned in " + refreshed + " published labs.");
}


// Safety check: no published page may load something that was left out.
{
  const problems = [];
  const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const dirRes = [...EXCLUDE_DIRS].filter((d) => !d.startsWith(".") && d !== "_site" && d !== "node_modules")
    .map((d) => [d + "/", new RegExp(`["'\`(=]\\.{0,2}/?${esc(d)}/`)]);
  const fileRes = [...EXCLUDE_FILES].filter((f) => !f.startsWith(".") && !/^README/.test(f))
    .map((f) => [f, new RegExp(`["'\`(=/]${esc(f)}\\b`)]);
  const rootDupes = fs.readdirSync(ROOT).filter((n) => /\(\d+\)\.[a-z0-9]+$/i.test(n));
  for (const f of walkFiles(OUT, /\.(html?|js|mjs|css|json)$/i)) {
    let text = fs.readFileSync(f, "utf8");
    if (f.endsWith(".json")) text = JSON.stringify(JSON.parse(text), (key,value) => key === "sourceNotes" ? "" : value);
    for (const [name, re] of [...dirRes, ...fileRes]) {
      if (re.test(text)) problems.push(`${path.relative(OUT, f)} refers to ${name}`);
    }
    for (const d of rootDupes) {
      if (text.includes(d) || text.includes(encodeURI(d))) problems.push(`${path.relative(OUT, f)} refers to ${d}`);
    }
  }
  if (problems.length) {
    console.error("\nThese published files point at files that are not published:\n  " + problems.join("\n  "));
    console.error("\nEither move the needed file into a published folder, or remove its name from the");
    console.error("EXCLUDE lists at the top of scripts/build-site.mjs. Nothing was deployed.\n");
    process.exit(1);
  }
}

// ---------- 2–3. Read data.js and build the catalog ----------
const htmlEsc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const slug = (s) => String(s || "").toLowerCase().normalize("NFKD").replace(/[\u0300-\u036f]/g, "")
  .replace(/&/g, " and ").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60) || "item";
const label = (o) => o && (o.title || o.name || o.label || o.id);

function loadData() {
  const src = fs.readFileSync(path.join(ROOT, "data.js"), "utf8");
  const names = [...src.matchAll(/^(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=/gm)].map((m) => m[1]);
  const grab = names.map((n) => `${JSON.stringify(n)}: typeof ${n} !== "undefined" ? ${n} : undefined`).join(",");
  const sandbox = { console: { log() {}, warn() {}, error() {} } };
  sandbox.window = sandbox; sandbox.self = sandbox; sandbox.globalThis = sandbox;
  sandbox.document = { addEventListener() {}, querySelector: () => null, getElementById: () => null };
  vm.createContext(sandbox);
  vm.runInContext(`${src}\n;globalThis.__mkTopLevel = {${grab}};`, sandbox, { filename: "data.js", timeout: 5000 });
  // Include resources attached by the same runtime supplements as the homepage.
  for (const filename of ["unit-specific-arcade.js", "resource-details.js", "course-catalog.js"]) {
    const file = path.join(ROOT, filename);
    if (fs.existsSync(file)) vm.runInContext(fs.readFileSync(file,"utf8"),sandbox,{filename,timeout:5000});
  }
  return sandbox;
}

function findCourses(root) {
  // A "unit" is any object with an `artifacts` array; its course is the nearest
  // named object above it that holds a list of units.
  const courses = new Map();
  const seen = new WeakSet();
  (function walk(v, chain) {
    if (!v || typeof v !== "object" || seen.has(v)) return;
    seen.add(v);
    if (!Array.isArray(v) && Array.isArray(v.artifacts)) {
      let course = null;
      for (let i = chain.length - 1; i >= 0; i--) {
        const c = chain[i];
        if (!Array.isArray(c) && label(c)) { course = c; break; }
      }
      const key = course || "_";
      if (!courses.has(key)) courses.set(key, { course, units: [] });
      courses.get(key).units.push(v);
      return;
    }
    const next = chain.concat([v]);
    for (const k of Object.keys(v)) {
      try { walk(v[k], next); } catch { /* getters etc. */ }
    }
  })(root, []);
  return [...courses.values()];
}

let catalog = [];
try {
  const sb = loadData();
  const roots = { ...sb.__mkTopLevel };
  for (const k of Object.keys(sb)) if (!["window", "self", "globalThis", "document", "console", "__mkTopLevel"].includes(k)) roots[k] = sb[k];
  const usedCourse = new Set();
  const hiddenCourses = new Set();
  for (const { course, units } of findCourses(roots)) {
    if (hiddenCourses.has(course?.id) || course?.hidden === true) continue;
    const cTitle = label(course) || "Activities";
    let cSlug = slug(course?.id || cTitle);
    while (usedCourse.has(cSlug)) cSlug += "-2";
    usedCourse.add(cSlug);
    const usedUnit = new Set();
    const unitList = units.map((u) => {
      let uSlug = slug(u.id || label(u));
      while (usedUnit.has(uSlug)) uSlug += "-2";
      usedUnit.add(uSlug);
      return {
        id: u.id, title: label(u) || "Unit", slug: uSlug, description: u.description || "",
        skills: sb.MK_COURSE_CATALOG.getSkills(course.id, u.id),
        items: (() => {
          if (course.planned) return [];
          const items = u.artifacts.filter((a) => a && typeof a === "object" && (a.title || a.path));
          const aliases = {algebra:{"foundations-algebra":"foundations","exponents-exponential-functions":"exponents-scientific-notation","polynomials-factoring":"polynomials"},geometry:{"foundations-geometry":"basics-reasoning","triangle-congruence":"triangles-congruence"}};
          const setId = (course.id === "algebra" ? "algebra1" : course.id) + "-" + (aliases[course.id]?.[u.id] || u.id);
          for (const [title,page] of [["Lesson Plan Generator","lesson-planner.html"],["Worksheet Generator","worksheet.html"],["Activity Generator","printables.html"],["Assessment Generator","menu-assessment.html"]]) {
            if (!items.some(a => (a.path || "").includes("worksheet-generator/" + page))) items.push({title,type:"Generator",path:"worksheet-generator/"+page+"#unit="+setId});
          }
          return items;
        })(),
      };
    });
    catalog.push({ id: course?.id, title: cTitle, slug: cSlug, color: course?.color, planned: course?.planned, units: unitList });
  }
} catch (e) {
  console.warn("Could not read data.js, so the catalog was not pre-written:", e.message);
  catalog = [];
}
const totalItems = catalog.reduce((n, c) => n + c.units.reduce((m, u) => m + u.items.length, 0), 0);
console.log(`Catalog: ${catalog.length} courses, ${catalog.reduce((n, c) => n + c.units.length, 0)} units, ${totalItems} activities`);

const courseNames = catalog.map((c) => c.title).filter((t) => t !== "Activities");
const listNames = (a) => a.length <= 1 ? a.join("") : a.slice(0, -1).join(", ") + " and " + a[a.length - 1];
const DESCRIPTION = "Free math games, printable worksheets, lesson plans, assessments, flashcards and interactive activities for Algebra 1, Geometry, Algebra 2 and more.";
const HOME_TITLE = "Free Math Games, Worksheets & Lesson Plans | Mr. K's Classroom";

// These summaries describe the resources teachers can actually find on each course page.
// Keep them readable and useful rather than repeating keywords for search engines.
const COURSE_SEO = {
  algebra: {
    title: "Free Algebra 1 Worksheets, Games & Lesson Plans",
    description: "Free Algebra 1 worksheets, math games, escape rooms, lesson plans, assessments and flashcards. Find classroom activities organized by unit and skill."
  },
  geometry: {
    title: "Free Geometry Worksheets, Games & Activities",
    description: "Explore free Geometry worksheets, interactive math activities, lesson plans, assessments and games for teachers, organized by geometry topic."
  },
  algebra2: {
    title: "Free Algebra 2 Worksheets, Games & Activities",
    description: "Free Algebra 2 worksheets, classroom math games, lesson plans, flashcards and assessments for teaching functions, equations and more."
  },
  prealgebra: {
    title: "Free 8th Grade Pre-Algebra Worksheets & Games",
    description: "Teach 8th grade Pre-Algebra with free worksheets, interactive math games, practice activities, lesson plans and assessment generators."
  },
  prealgebra7: {
    title: "Free 7th Grade Pre-Algebra Activities & Worksheets",
    description: "Free 7th grade math worksheets, games, lesson plans and practice activities for integers, equations, ratios, geometry and more."
  },
  math5: {
    title: "Free 5th Grade Math Worksheets, Games & Activities",
    description: "Free 5th grade math games, worksheets, flashcards, cheat sheets, projects and interactive tools for place value, decimals, fractions, volume, the coordinate plane and more."
  },
  math6: {
    title: "Free 6th Grade Math Worksheets & Games",
    description: "Free 6th grade math worksheets, games, lesson plans and activities for ratios, fractions, equations, geometry and data."
  },
  precalculus: {
    title: "Free Precalculus Worksheets, Games & Tools",
    description: "Explore free Precalculus worksheets, lesson plans and interactive math tools for functions, trigonometry, vectors, conics and more."
  },
  calculus: {
    title: "Free Calculus Worksheets & Interactive Math Tools",
    description: "Free Calculus lesson plans, worksheets and interactive math activities for limits, derivatives, integrals and applications."
  },
  statistics: {
    title: "Free Statistics Activities, Worksheets & Games",
    description: "Free Statistics worksheets, interactive data labs, classroom activities and lesson plans on sampling, probability and inference."
  },
  discrete: {
    title: "Free Discrete Math Worksheets & Classroom Activities",
    description: "Explore free Discrete Math worksheets, games and activities on logic, proof, counting, graph theory and optimization."
  }
};

function seoCourse(c) {
  if (c.planned) return {
    title: `${c.title} Curriculum Units & Topics | ${SITE_NAME}`,
    heading: `${c.title} Curriculum Units`,
    description: `Explore the ${c.title} course outline and topics across ${c.units.length} units. Additional teaching activities are in development.`
  };
  const seo = COURSE_SEO[c.id] || {};
  return {
    title: `${seo.title || `Free ${c.title} Math Activities & Worksheets`} | ${SITE_NAME}`,
    heading: `${c.title} Worksheets, Games & Lessons`,
    description: seo.description || `Free ${c.title} worksheets, lesson plans, math games and assessments organized by unit for teachers.`
  };
}

function seoUnit(c, u) {
  const base = `${u.title} – ${c.title}`;
  if (c.planned) return {
    title: `${base} Unit Outline | ${SITE_NAME}`,
    heading: `${u.title}: ${c.title} Unit Outline`,
    description: `Explore ${u.title} in the ${c.title} curriculum, including the skills and topics in this unit. Classroom activities are in development.`
  };
  const hasGames = u.items.some((a) => a.type === "Game" || /escape room|showdown|connect 4|tic tac toe|detective game/i.test(a.title || ""));
  const hasStudy = u.items.some((a) => /flashcard|cheat sheet|study guide/i.test(a.title || ""));
  const extras = [hasGames ? "math games" : "practice activities", ...(hasStudy ? ["study guides"] : [])];
  const description = `Free ${c.title} resources for ${u.title}: lesson plans, worksheet and assessment generators, ${listNames(extras)}. Browse ${u.items.length} classroom activities and tools.`;
  return {
    title: `${base} ${base.length < 56 ? "Worksheets & Activities" : "Resources"} | ${SITE_NAME}`,
    heading: `${u.title}: ${c.title} Worksheets & Activities`,
    description: description.length <= 175 ? description : description.slice(0, 172).replace(/\s+\S*$/, "") + "…"
  };
}

const isExternal = (p) => /^(https?:)?\/\//i.test(p);
const href = (p, depth) => isExternal(p) ? p : "../".repeat(depth) + String(p).replace(/^\.?\//, "");
const courseUrl = (c) => `u/${c.slug}/`;
const unitUrl = (c, u) => `u/${c.slug}/${u.slug}/`;

function itemHtml(a, depth) {
  const meta = [a.type, Array.isArray(a.level) ? a.level.join(" / ") : a.level].filter(Boolean).join(", ");
  const topics = Array.isArray(a.topics) && a.topics.length ? `<p class="mk-topics">Topics: ${htmlEsc(a.topics.join(", "))}</p>` : "";
  return `<li>${a.path ? `<a href="${htmlEsc(href(a.path, depth))}">${htmlEsc(a.title || a.path)}</a>` : htmlEsc(a.title)}`
    + (meta ? ` <span class="mk-meta">(${htmlEsc(meta)})</span>` : "")
    + (a.description ? `<p>${htmlEsc(a.description)}</p>` : "") + topics + `</li>`;
}

// ---------- unit pages ----------
const PAGE_CSS = `
:root{--bg:#fbfcfe;--ink:#18212f;--muted:#566173;--line:#d9dee7;--link:#1f5fbf;--accent:#1f5fbf}
@media (prefers-color-scheme:dark){:root{--bg:#12161d;--ink:#e8ecf2;--muted:#a3adbb;--line:#2b3340;--link:#8fb6ff;--accent:#8fb6ff}}
*{box-sizing:border-box}
html{color-scheme:light dark}
body{margin:0;background:var(--bg);color:var(--ink);font:1.0625rem/1.6 "Atkinson Hyperlegible",system-ui,-apple-system,"Segoe UI",sans-serif;
  padding:env(safe-area-inset-top,0) 0 env(safe-area-inset-bottom,0)}
.wrap{max-width:46rem;margin:0 auto;padding:1.5rem 1.25rem 3rem}
a{color:var(--link)}
a:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.crumbs{font-size:.95rem;color:var(--muted);margin:0 0 1.5rem}
h1{font:800 clamp(1.8rem,5vw,2.6rem)/1.1 "Bricolage Grotesque",system-ui,sans-serif;margin:0 0 .5rem;border-left:.4rem solid var(--accent);padding-left:.75rem}
.lede{color:var(--muted);margin:0 0 2rem}
ul.mk-items{list-style:none;padding:0;margin:0}
ul.mk-items li{padding:1rem 0;border-top:1px solid var(--line)}
ul.mk-items li>a{font-weight:700;font-size:1.1rem}
ul.mk-items p{margin:.25rem 0 0}
.mk-meta,.mk-topics{color:var(--muted);font-size:.95rem}
.open-app{display:inline-block;margin-top:2rem;font-weight:700}
footer{color:var(--muted);font-size:.9rem;margin-top:3rem}
`;
const COLOR = { blue: "#1f5fbf", orange: "#c4570f", green: "#1d7a46", purple: "#6b3fb8" };

function headTags({ title, description, url, depth, fontsHref }) {
  const pre = "../".repeat(depth);
  return `<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${htmlEsc(title)}</title>
<meta name="description" content="${htmlEsc(description)}">
<link rel="canonical" href="${htmlEsc(url)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="${htmlEsc(SITE_NAME)}">
<meta property="og:title" content="${htmlEsc(title)}">
<meta property="og:description" content="${htmlEsc(description)}">
<meta property="og:url" content="${htmlEsc(url)}">
<meta property="og:image" content="${SITE_URL}assets/social-preview.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="${pre}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="${pre}assets/apple-touch-icon.png">
${fontsHref ? `<link rel="stylesheet" href="${fontsHref}">` : ""}`;
}

const GOOGLE_FONTS_HOME = "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&display=swap";
const sitemapUrls = [SITE_URL];

for (const c of catalog) {
  // Indexable course landing pages give teachers (and search engines) a clear
  // subject-level directory without hiding Grade 6/7 on the public site.
  const courseDepth = 2;
  const courseAddress = SITE_URL + courseUrl(c);
  const courseMeta = seoCourse(c);
  const courseDescription = courseMeta.description;
  const coursePage = `<!doctype html>
<html lang="en">
<head>
${headTags({ title: courseMeta.title, description: courseDescription, url: courseAddress, depth: courseDepth, fontsHref: GOOGLE_FONTS_HOME })}
<style>${PAGE_CSS}</style>
</head>
<body>
<div class="wrap">
<p class="crumbs"><a href="../../">${htmlEsc(SITE_NAME)}</a> / ${htmlEsc(c.title)}</p>
<main>
<h1>${htmlEsc(courseMeta.heading)}</h1>
<p class="lede">${htmlEsc(courseDescription)}</p>
<h2>Explore ${htmlEsc(c.title)} units</h2>
<ul class="mk-items">
${c.units.map((u) => `<li><a href="${htmlEsc(u.slug)}/">${htmlEsc(u.title)}</a> <span class="mk-meta">${c.planned ? "(curriculum outline)" : `(${u.items.length} classroom resources)`}</span></li>`).join("\n")}
</ul>
<a class="open-app" href="../../#${encodeURIComponent(c.id)}">Open ${htmlEsc(c.title)} in the full classroom site</a>
</main>
<footer>© 2026 ${htmlEsc(SITE_NAME)} · <a href="https://github.com/akneller1/classroom/issues/new?title=Website%20feedback">Send feedback</a></footer>
</div>
</body>
</html>
`;
  const courseDir = path.join(OUT, courseUrl(c));
  fs.mkdirSync(courseDir, { recursive: true });
  fs.writeFileSync(path.join(courseDir, "index.html"), coursePage);
  sitemapUrls.push(courseAddress);
  for (const u of c.units) {
    if (!u.items.length && !c.planned) continue;
    const depth = 3;
    const url = SITE_URL + unitUrl(c, u);
    const unitMeta = seoUnit(c, u);
    const desc = unitMeta.description;
    const accent = COLOR[c.color] ? `<style>:root{--accent:${COLOR[c.color]}}@media (prefers-color-scheme:dark){:root{--accent:var(--link)}}</style>` : "";
    const appLink = u.id ? `../../../#${encodeURIComponent(c.id + "." + u.id)}` : "../../../";
    const page = `<!doctype html>
<html lang="en">
<head>
${headTags({ title: unitMeta.title, description: desc, url, depth, fontsHref: GOOGLE_FONTS_HOME })}
<style>${PAGE_CSS}</style>${accent}
</head>
<body>
<div class="wrap">
<p class="crumbs"><a href="../../../">${htmlEsc(SITE_NAME)}</a> / <a href="../">${htmlEsc(c.title)}</a> / ${htmlEsc(u.title)}</p>
<main>
<h1>${htmlEsc(unitMeta.heading)}</h1>
<p class="lede">${htmlEsc(desc)}</p>
<ul class="mk-items">
${c.planned ? u.skills.map(skill => `<li>${htmlEsc(skill)}</li>`).join("\n") : u.items.map((a) => itemHtml(a, depth)).join("\n")}
</ul>
<a class="open-app" href="${appLink}">Open this unit in the full classroom site</a>
</main>
<footer>© 2026 ${htmlEsc(SITE_NAME)} · <a href="https://github.com/akneller1/classroom/issues/new?title=Website%20feedback">Send feedback</a></footer>
</div>
</body>
</html>
`;
    const dir = path.join(OUT, unitUrl(c, u));
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, "index.html"), page);
    sitemapUrls.push(url);
  }
}

// The generated /u/ pages remain authoritative for courses and units.
// Include other standalone public tools in the sitemap without duplicating course URLs.
for (const relative of ["about.html", "guide.html", "skills.html", "backup.html", "courses/"]) {
  const target = path.join(OUT, relative, relative.endsWith("/") ? "index.html" : "");
  if (fs.existsSync(target)) sitemapUrls.push(SITE_URL + relative);
}

// Keep /u/ as the authoritative, fully generated course and unit URLs.
// The older /courses/*.html landing pages stay accessible for saved links,
// but search engines should not index them as duplicates.
for (const c of catalog) {
  const paths = [
    ["courses/" + c.id + ".html", SITE_URL + courseUrl(c)],
    ...c.units.map((u) => ["courses/" + c.id + "/" + u.id + ".html", SITE_URL + unitUrl(c, u)])
  ];
  for (const [relative, canonical] of paths) {
    const file = path.join(OUT, relative);
    if (!fs.existsSync(file)) continue;
    let html = fs.readFileSync(file, "utf8");
    html = html.replace(/<link\s+rel=["']canonical["']\s+href=["'][^"']+["']\s*\/?\s*>/i,
      '<link rel="canonical" href="' + htmlEsc(canonical) + '">');
    if (!/name=["']robots["']/i.test(html)) {
      html = html.replace(/<head>/i, '<head><meta name="robots" content="noindex,follow">');
    }
    fs.writeFileSync(file, html);
  }
}

const today = new Date().toISOString().slice(0, 10);
fs.writeFileSync(path.join(OUT, "sitemap.xml"),
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`
  + sitemapUrls.map((u) => `  <url><loc>${htmlEsc(u)}</loc><lastmod>${today}</lastmod></url>`).join("\n")
  + `\n</urlset>\n`);

// ---------- 2, 4, 5. Update index.html ----------
{
  const file = path.join(OUT, "index.html");
  let html = fs.readFileSync(file, "utf8");

  // Clear homepage title identifies the free resources rather than only the site name.
  html = html.replace(/<title>[^<]*<\/title>/i, `<title>${htmlEsc(HOME_TITLE)}</title>`);

  // Head tags (only ones that are not already there)
  const add = [];
  if (!/name=["']description["']/i.test(html)) add.push(`<meta name="description" content="${htmlEsc(DESCRIPTION)}">`);
  if (!/rel=["']canonical["']/i.test(html)) add.push(`<link rel="canonical" href="${SITE_URL}">`);
  if (!/property=["']og:/i.test(html)) add.push(
    `<meta property="og:type" content="website">`,
    `<meta property="og:site_name" content="${htmlEsc(SITE_NAME)}">`,
    `<meta property="og:title" content="${htmlEsc(SITE_NAME)}">`,
    `<meta property="og:description" content="${htmlEsc(DESCRIPTION)}">`,
    `<meta property="og:url" content="${SITE_URL}">`,
    `<meta property="og:image" content="${SITE_URL}assets/social-preview.png">`,
    `<meta property="og:image:width" content="1200">`,
    `<meta property="og:image:height" content="630">`,
    `<meta name="twitter:card" content="summary_large_image">`);
  if (!/rel=["'](shortcut )?icon["']/i.test(html)) add.push(
    `<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">`,
    `<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">`);
  // Hide Back on the home page (works whatever app.js does with the button)
  add.push(`<style>html.mk-home #backBtn{display:none!important}.mk-static ul{padding-left:1.25rem}.mk-static li{margin:.35rem 0}</style>`,
    `<script>(function(){function s(){var h=location.hash;document.documentElement.classList.toggle("mk-home",!h||h==="#"||h==="#home");}s();addEventListener("hashchange",s);})();</script>`);
  html = html.replace(/<\/title>/i, (m) => m + "\n" + add.join("\n"));

  // Logo goes to the home page instead of "#"
  html = html.replace(/(<a\s+class=["']brand["']\s+href=)["']#["']/i, `$1"./"`);

  // Plain-HTML catalog inside <main>, cleared just before app.js draws the real page
  if (catalog.length && totalItems) {
    const staticHtml = `<div class="wrap mk-static">
<h1>Free math activities for teachers</h1>
<p>${htmlEsc(DESCRIPTION)}</p>
${catalog.map((c) => `<h2><a href="${courseUrl(c)}">${htmlEsc(c.title)}</a></h2>
<ul>
${c.units.map((u) => u.items.length
    ? `<li><a href="${unitUrl(c, u)}">${htmlEsc(u.title)}</a> (${u.items.length} activit${u.items.length === 1 ? "y" : "ies"})</li>`
    : `<li>${htmlEsc(u.title)} (coming soon)</li>`).join("\n")}
</ul>`).join("\n")}
</div>`;
    const mainRe = /(<main\b[^>]*\bid=["']main["'][^>]*>)\s*(<\/main>)/i;
    const appRe = /<script\b[^>]*\bsrc=["']app\.js[^"']*["'][^>]*>\s*<\/script>/i;
    if (mainRe.test(html) && appRe.test(html)) {
      html = html.replace(mainRe, `$1\n${staticHtml}\n$2`);
      html = html.replace(appRe, (m) => `<script>(function(){var m=document.getElementById("main");if(m)m.innerHTML="";})();</script>\n${m}`);
    } else {
      console.warn("index.html layout changed: catalog not inserted.");
    }
  }
  fs.writeFileSync(file, html);
}

// ---------- 6. Serve Google Fonts from the site ----------
async function selfHostFonts() {
  const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36";
  const fontsDir = path.join(OUT, "assets", "fonts");
  const files = walkFiles(OUT, /\.(html?|css)$/i);
  const linkRe = /<link\b[^>]*href=["'](https:\/\/fonts\.googleapis\.com\/css2?\?[^"']+)["'][^>]*>/gi;
  const importRe = /@import\s+url\(\s*["']?(https:\/\/fonts\.googleapis\.com\/css2?\?[^"')]+)["']?\s*\)\s*;?/gi;
  const urls = new Set();
  for (const f of files) {
    const t = fs.readFileSync(f, "utf8");
    for (const m of t.matchAll(linkRe)) urls.add(m[1]);
    for (const m of t.matchAll(importRe)) urls.add(m[1]);
  }
  if (!urls.size) return;
  const local = new Map(); // google URL (as written) -> path under _site
  for (const raw of urls) {
    try {
      const real = raw.replace(/&amp;/g, "&");
      if (real === GOOGLE_FONTS_HOME) {
        // The site already bundles its primary fonts. Reuse them even in offline builds.
        const bundled = path.join(ROOT,"worksheet-generator/vendor/fonts");
        const faces = [["Bricolage Grotesque","bricolage-grotesque-latin-wght-normal.woff2","100 900","normal"],["Atkinson Hyperlegible","atkinson-hyperlegible-latin-400-normal.woff2","400","normal"],["Atkinson Hyperlegible","atkinson-hyperlegible-latin-700-normal.woff2","700","normal"],["Atkinson Hyperlegible","atkinson-hyperlegible-latin-400-italic.woff2","400","italic"]];
        if (faces.every(f=>fs.existsSync(path.join(bundled,f[1])))) {
          fs.mkdirSync(fontsDir,{recursive:true});
          for (const f of faces) fs.copyFileSync(path.join(bundled,f[1]),path.join(fontsDir,f[1]));
          for (const name of ["LICENSE-atkinson.txt","LICENSE-bricolage.txt"]) fs.copyFileSync(path.join(bundled,name),path.join(fontsDir,name));
          fs.writeFileSync(path.join(fontsDir,"classroom-fonts.css"),faces.map(f=>`@font-face{font-family:'${f[0]}';font-style:${f[3]};font-weight:${f[2]};font-display:swap;src:url('${f[1]}') format('woff2');}`).join("\n"));
          local.set(raw,"assets/fonts/classroom-fonts.css");continue;
        }
      }
      const res = await fetch(real, { headers: { "User-Agent": UA }, signal: AbortSignal.timeout(3000) });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      let css = await res.text();
      const fontUrls = [...new Set([...css.matchAll(/url\((https:\/\/fonts\.gstatic\.com\/[^)]+)\)/g)].map((m) => m[1]))];
      if (!fontUrls.length) throw new Error("no font files listed");
      fs.mkdirSync(fontsDir, { recursive: true });
      for (const fu of fontUrls) {
        const name = crypto.createHash("sha1").update(fu).digest("hex").slice(0, 16) + path.extname(new URL(fu).pathname);
        const target = path.join(fontsDir, name);
        if (!fs.existsSync(target)) {
          const r = await fetch(fu, { signal: AbortSignal.timeout(3000) });
          if (!r.ok) throw new Error(`font HTTP ${r.status}`);
          fs.writeFileSync(target, Buffer.from(await r.arrayBuffer()));
        }
        css = css.split(fu).join(name);
      }
      const cssName = "fonts-" + crypto.createHash("sha1").update(real).digest("hex").slice(0, 10) + ".css";
      fs.writeFileSync(path.join(fontsDir, cssName), css);
      local.set(raw, "assets/fonts/" + cssName);
    } catch (e) {
      console.warn(`Kept Google Fonts link (download failed: ${e.message}): ${raw}`);
    }
  }
  if (!local.size) return;
  for (const f of files) {
    let t = fs.readFileSync(f, "utf8");
    const before = t;
    const rel = (p) => path.relative(path.dirname(f), path.join(OUT, p)).split(path.sep).join("/");
    for (const [raw, p] of local) t = t.split(raw).join(rel(p));
    if (t !== before) {
      if (![...t.matchAll(linkRe)].length && !/fonts\.googleapis\.com\/css/.test(t)) {
        t = t.replace(/<link\b[^>]*rel=["']preconnect["'][^>]*fonts\.(googleapis|gstatic)\.com[^>]*>\s*/gi, "");
      }
      fs.writeFileSync(f, t);
    }
  }
  console.log(`Fonts: ${local.size} Google Fonts stylesheet(s) now served from the site.`);
}
await selfHostFonts();

fs.writeFileSync(path.join(OUT,"robots.txt"),`User-agent: *\nAllow: /\nSitemap: ${SITE_URL}sitemap.xml\n`);

console.log(`Done. ${catalog.length} course pages and ${sitemapUrls.length - catalog.length - 1} unit pages written. Output: _site/`);
