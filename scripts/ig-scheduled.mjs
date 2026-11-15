// Checks posts/schedule.txt and posts due entries (via ig-manual.mjs logic, one per run).
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
const now = Date.now();
const offset = d => { const p = new Intl.DateTimeFormat('en-US', { timeZone: 'Europe/Vienna', timeZoneName: 'shortOffset' }).formatToParts(d).find(x => x.type === 'timeZoneName').value; const m = p.match(/([+-]\d+)/); return (m ? +m[1] : 0) * 3600e3; };
for (const line of fs.readFileSync('posts/schedule.txt', 'utf8').split('\n')) {
  const m = line.trim().match(/^(\d{4}-\d\d-\d\dT\d\d:\d\d)\s+(\S+)/); if (!m) continue;
  const t = Date.parse(m[1] + ':00Z') - offset(new Date(Date.parse(m[1] + ':00Z')));
  if (now >= t && now - t < 3 * 3600e3) {
    console.log('due:', m[2]);
    try { execFileSync('node', ['scripts/ig-manual.mjs'], { stdio: 'inherit', env: { ...process.env, POST_NAME: m[2], DRY: 'false' } }); }
    catch (e) { console.log('post failed or already done:', m[2]); }
  }
}
