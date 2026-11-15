// Renders the live Windshift share image (German) with Playwright and hands it to the ig-post Edge Function.
import { chromium } from 'playwright';
import fs from 'node:fs';

const SITE = process.env.SITE || 'https://joemoe.at/windshift/';
const FN = 'https://lfiadqrbacphpoeihfpg.supabase.co/functions/v1/ig-post';
const DRY = process.env.DRY === 'true', FORCE = process.env.FORCE === 'true';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1500, height: 1000 }, timezoneId: 'Europe/Vienna', locale: 'de-AT' });
await page.addInitScript(() => { localStorage.setItem('wind-lang', 'de'); localStorage.setItem('wind-unit', 'kn'); localStorage.setItem('wind-color', 'sys'); });
page.on('pageerror', e => console.log('pageerror', e.message));
await page.goto(SITE + '?ig=' + Date.now(), { waitUntil: 'networkidle' });
await page.waitForFunction(() => { try { return !!UPDATED && !!FIT; } catch (e) { return false; } }, null, { timeout: 60000 });
await page.waitForTimeout(2000);

const out = await page.evaluate(async () => {
  const lastT = Math.max(0, ...STATIONS.map(s => { const r = (DATA[s.id] || []).slice(-1)[0]; return r ? +r.t : 0; }));
  const stale = !lastT || Date.now() - lastT > 40 * 60e3;
  const png = await shareRender();
  const bmp = await createImageBitmap(png);
  const cv = document.createElement('canvas'); cv.width = bmp.width; cv.height = bmp.height; cv.getContext('2d').drawImage(bmp, 0, 0);
  const jpg = cv.toDataURL('image/jpeg', 0.9).split(',')[1];
  // caption
  const rows = STATIONS.map(s => { const r = (DATA[s.id] || []).slice(-1)[0]; return r && r.ff != null ? { n: s.name, d: dirName(r.dd), ff: r.ff, fx: r.fx } : null; }).filter(Boolean);
  const avg = rows.reduce((a, r) => a + r.ff, 0) / Math.max(1, rows.length), gmax = Math.max(0, ...rows.map(r => r.fx || 0));
  const S = FIT ? FIT.S : {};
  const sys = SYSTEMS.filter(q => Math.abs(S[q.id] || 0) > 0.15).sort((a, b) => Math.abs(S[b.id]) - Math.abs(S[a.id])).slice(0, 3)
    .map(q => `${T().sys[q.id][0]} ${Math.round(Math.abs(S[q.id]) * 100)} %`);
  const k = v => Math.round(v * 1.94384);
  const when = new Date(lastT).toLocaleString('de-AT', { weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Vienna' });
  const head = avg < 1.6 ? '🌫️ Flaute am östlichen Bodensee' : avg < 3.4 ? '🌬️ Leichter Wind am östlichen Bodensee' : avg < 5.5 ? '⛵ Segelwind am östlichen Bodensee' : avg < 8 ? '💨 Frischer Wind am östlichen Bodensee' : '⚠️ Starkwind am östlichen Bodensee';
  const caption = [
    `${head} – ${when}`,
    '',
    ...rows.map(r => `📍 ${r.n}: ${r.d} ${k(r.ff)} kn (Böen ${r.fx != null ? k(r.fx) : '–'})`),
    '',
    `Ø ${k(avg)} kn · ${bft(avg)} Bft · max. Böe ${k(gmax)} kn`,
    sys.length ? `Modell: ${sys.join(' · ')}` : 'Modell: keine ausgeprägten Windsysteme',
    '',
    'Pfeile = Messung (10-Min-Mittel/Böe) · Strömung = Modell, an Messungen angepasst. Live: joemoe.at/windshift (Link in Bio)',
    'Daten: GeoSphere Austria · MeteoSwiss · DWD',
    '',
    '#bodensee #segeln #wind #windsurfen #kitesurfen #bregenz #lindau #lakeconstance #vorarlberg #windshift',
  ].join('\n');
  return { jpg, caption, stale, lastT };
});
await browser.close();

fs.mkdirSync('out', { recursive: true });
const img = Buffer.from(out.jpg, 'base64');
fs.writeFileSync('out/post.jpg', img); fs.writeFileSync('out/caption.txt', out.caption);
console.log(out.caption, '\n\nstale:', out.stale, 'bytes:', img.length);
if (out.stale && !FORCE) { console.log('Data stale – not posting.'); process.exit(DRY ? 0 : 1); }

// GitHub OIDC token proves the request comes from this repo's workflow
const oidc = await fetch(`${process.env.ACTIONS_ID_TOKEN_REQUEST_URL}&audience=windshift-ig`, { headers: { Authorization: `bearer ${process.env.ACTIONS_ID_TOKEN_REQUEST_TOKEN}` } }).then(r => r.json());
const q = new URLSearchParams({ caption: out.caption, kind: 'daily' }); if (DRY) q.set('dry', '1'); if (FORCE) q.set('force', '1');
const res = await fetch(`${FN}?${q}`, { method: 'POST', headers: { Authorization: `Bearer ${oidc.value}`, 'Content-Type': 'image/jpeg' }, body: img });
const body = await res.text(); console.log(res.status, body);
fs.writeFileSync('out/result.json', body);
if (!res.ok && res.status !== 409) process.exit(1);
