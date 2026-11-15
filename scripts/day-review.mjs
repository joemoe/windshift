// Evening review: replays the Windshift model fit for a day, detects a "good sailing window"
// (>= 8 kn mean over >= 2 h, steady speed and direction, daytime) and posts a 2-slide carousel.
// Also logs the 10-min model fit of the day to the database.
import { chromium } from 'playwright';
import fs from 'node:fs';

const SITE = process.env.SITE || 'https://joemoe.at/windshift/';
const FN = 'https://lfiadqrbacphpoeihfpg.supabase.co/functions/v1/ig-post';
const DB = 'https://lfiadqrbacphpoeihfpg.supabase.co', KEY = 'sb_publishable_Nd6UwPbp1kpRb1AOu5aKbA_K8Zwgwsi';
const DRY = process.env.DRY === 'true', FORCE = process.env.FORCE === 'true';
const DAY = process.env.DAY || new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Vienna' }).format(new Date());
const KN = 1.94384, LAKE = ['lindau', 'bregenz', 'rohrspitz', 'altenrhein'];

// ---- local-day boundaries (Europe/Vienna) ----
const off = d => { const p = new Intl.DateTimeFormat('en-US', { timeZone: 'Europe/Vienna', timeZoneName: 'shortOffset' }).formatToParts(d).find(x => x.type === 'timeZoneName').value; const m = p.match(/([+-]\d+)/); return (m ? +m[1] : 0) * 3600e3; };
const t0 = Date.parse(DAY + 'T00:00:00Z') - off(new Date(Date.parse(DAY + 'T12:00:00Z'))), t1 = t0 + 24 * 3600e3;
const hh = t => new Intl.DateTimeFormat('de-AT', { timeZone: 'Europe/Vienna', hour: '2-digit', minute: '2-digit' }).format(new Date(t));

// ---- observations of the day ----
const rows = [];
for (let off2 = 0; ; off2 += 1000) {
  const r = await fetch(`${DB}/rest/v1/observations?select=station_id,ts,dd,ff,fx&ts=gte.${new Date(t0 - 3600e3).toISOString()}&ts=lt.${new Date(t1).toISOString()}&order=ts.asc,station_id.asc&limit=1000&offset=${off2}`, { headers: { apikey: KEY, Authorization: 'Bearer ' + KEY } }).then(r => r.json());
  rows.push(...r); if (r.length < 1000) break;
}
console.log(DAY, 'rows', rows.length);

// ---- good-window detection on raw lake observations ----
function detect() {
  let best = null;
  for (const id of LAKE) {
    const a = rows.filter(r => r.station_id === id && r.ff != null && r.dd != null).map(r => ({ t: Date.parse(r.ts), ff: r.ff, dd: r.dd, fx: r.fx }));
    const ok = [];   // window end indices that qualify
    for (let i = 0; i < a.length; i++) {
      const end = a[i].t, w = a.filter(x => x.t > end - 120 * 60e3 && x.t <= end);
      const loc = (end - t0) / 3600e3; if (loc < 9 || loc > 20.01 || w.length < 11) continue;
      const m = w.reduce((s, x) => s + x.ff, 0) / w.length, mn = Math.min(...w.map(x => x.ff));
      const sd = Math.sqrt(w.reduce((s, x) => s + (x.ff - m) ** 2, 0) / (w.length - 1));
      const S = w.reduce((s, x) => s + Math.sin(x.dd * Math.PI / 180), 0) / w.length, C = w.reduce((s, x) => s + Math.cos(x.dd * Math.PI / 180), 0) / w.length;
      const R = Math.min(0.999999, Math.hypot(S, C)), dstd = Math.sqrt(-2 * Math.log(R)) * 180 / Math.PI;
      if (m * KN >= 8 && m * KN <= 22 && mn * KN >= 5.5 && sd / m <= 0.3 && dstd <= 25) ok.push(end);
    }
    if (!ok.length) continue;
    // merge consecutive window ends into periods
    let ps = [], cur = [ok[0], ok[0]];
    for (const e of ok.slice(1)) { if (e - cur[1] <= 20 * 60e3) cur[1] = e; else { ps.push(cur); cur = [e, e]; } }
    ps.push(cur);
    for (const [e0, e1] of ps) {
      const start = e0 - 110 * 60e3, w = a.filter(x => x.t >= start && x.t <= e1);
      const m = w.reduce((s, x) => s + x.ff, 0) / w.length, gx = Math.max(...w.map(x => x.fx || 0));
      const S = w.reduce((s, x) => s + Math.sin(x.dd * Math.PI / 180), 0) / w.length, C = w.reduce((s, x) => s + Math.cos(x.dd * Math.PI / 180), 0) / w.length;
      const dir = (Math.atan2(S, C) * 180 / Math.PI + 360) % 360, dstd = Math.sqrt(-2 * Math.log(Math.min(0.999999, Math.hypot(S, C)))) * 180 / Math.PI;
      const cand = { id, start, end: e1, hours: (e1 - start) / 3600e3, mean: m, gust: gx, dir, dstd };
      if (!best || cand.hours * cand.mean > best.hours * best.mean) best = cand;
    }
  }
  return best;
}
const win = detect();
console.log('window', win && { ...win, start: hh(win.start), end: hh(win.end) });

// ---- page: replay fit + render ----
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1500, height: 1000 }, timezoneId: 'Europe/Vienna', locale: 'de-AT' });
await page.addInitScript(() => { localStorage.setItem('wind-lang', 'de'); localStorage.setItem('wind-unit', 'kn'); localStorage.setItem('wind-color', 'sys'); });
page.on('pageerror', e => console.log('pageerror', e.message));
await page.goto(SITE + '?review=' + Date.now(), { waitUntil: 'networkidle' });
await page.waitForFunction(() => { try { return !!UPDATED && typeof refit === 'function' && !!MAP; } catch (e) { return false; } }, null, { timeout: 60000 });

const out = await page.evaluate(async ({ rows, t0, t1, win, DAY }) => {
  DATA = {}; for (const r of rows) (DATA[r.station_id] || (DATA[r.station_id] = [])).push({ t: new Date(r.ts), dd: r.dd, ff: r.ff, fx: r.fx });
  MODE = 'live';
  const fits = [];
  for (let t = t0; t < t1 && t <= Date.now(); t += 10 * 60e3) { refit(t); if (FIT) fits.push({ ts: new Date(t).toISOString(), s: FIT.S, n: Object.keys(FIT.S).length }); }
  if (!win) return { fits, version: MODEL_VERSION };

  // average system strengths over the window
  const inWin = fits.filter(f => { const t = Date.parse(f.ts); return t >= win.start && t <= win.end; });
  const avg = {}; for (const q of SYSTEMS) avg[q.id] = inWin.reduce((s, f) => s + (f.s[q.id] || 0), 0) / Math.max(1, inWin.length);
  const sd = inWin.map(f => f.s.synDir).filter(x => x != null);
  const synDir = sd.length ? (Math.atan2(sd.reduce((s, d) => s + Math.sin(d * DEG), 0), sd.reduce((s, d) => s + Math.cos(d * DEG), 0)) / DEG + 360) % 360 : null;

  // slide 1: map at the middle of the window
  const mid = Math.round((win.start + win.end) / 2 / 600e3) * 600e3; refit(mid);
  const toJpg = async blob => { const b = await createImageBitmap(blob); const c = document.createElement('canvas'); c.width = b.width; c.height = b.height; c.getContext('2d').drawImage(b, 0, 0); return c.toDataURL('image/jpeg', 0.9).split(',')[1]; };
  const s1 = await toJpg(await shareRender({ at: mid, badge: 'RÜCKBLICK' }));

  // slide 2: analysis
  const W = 1080, H = 1350, cv = document.createElement('canvas'); cv.width = W; cv.height = H; const c = cv.getContext('2d');
  const F = (w, s) => `${w} ${s}px Inter, system-ui, sans-serif`;
  const g = c.createRadialGradient(W / 2, 300, 50, W / 2, 300, 1100); g.addColorStop(0, '#14293a'); g.addColorStop(1, '#0b1620'); c.fillStyle = g; c.fillRect(0, 0, W, H);
  const logo = await new Promise(r => { const i = new Image(); i.onload = () => r(i); i.onerror = () => r(null); i.src = 'favicon.svg'; }); if (logo) c.drawImage(logo, 44, 40, 64, 64);
  c.fillStyle = '#e8f1f5'; c.font = F(800, 32); c.fillText('Windshift', 118, 84);
  const dstr = new Date(win.start).toLocaleDateString('de-AT', { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'Europe/Vienna' });
  c.fillStyle = '#4fc3a1'; c.font = F(700, 26); c.fillText('GUTER SEGELTAG · ' + dstr.toUpperCase(), 60, 176);
  const st = STATIONS.find(s => s.id === win.id), k = v => Math.round(v * 1.94384);
  const hm = t => new Date(t).toLocaleTimeString('de-AT', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Vienna' });
  c.fillStyle = '#e8f1f5'; c.font = F(800, 62); c.fillText(`${st.name}, ${hm(win.start)}–${hm(win.end)}`, 60, 252);
  // stat tiles
  const tiles = [[`${k(win.mean)} kn`, 'Ø Wind'], [`${k(win.gust)} kn`, 'max. Böe'], [`${dirName(win.dir)}`, 'Richtung'], [`±${Math.round(win.dstd)}°`, 'Drehung']];
  tiles.forEach(([v, l], i) => { const x = 60 + i * 245; c.fillStyle = '#112230'; shRound(c, x, 290, 225, 130, 18); c.fill(); c.strokeStyle = '#21414f'; c.lineWidth = 2; c.stroke();
    c.fillStyle = i < 2 ? shCol(color(i ? win.gust : win.mean)) : '#e8f1f5'; c.font = F(800, 44); c.fillText(v, x + 22, 358); c.fillStyle = '#8aa6b3'; c.font = F(600, 22); c.fillText(l, x + 22, 396); });
  // chart: lake stations 08–20 h
  const cx = 110, cy = 470, cw = 900, ch = 280, ta = t0 + 8 * 3600e3, tb = t0 + 20 * 3600e3, vmax = Math.max(16, Math.ceil(k(win.gust) / 4) * 4);
  const X = t => cx + (t - ta) / (tb - ta) * cw, Y = v => cy + ch - Math.min(vmax, v * 1.94384) / vmax * ch;
  c.fillStyle = 'rgba(79,195,161,.14)'; c.fillRect(X(win.start), cy, X(win.end) - X(win.start), ch);
  c.font = F(500, 20); c.fillStyle = '#8aa6b3'; c.strokeStyle = 'rgba(255,255,255,.12)'; c.lineWidth = 1;
  for (let v = 0; v <= vmax; v += vmax / 4) { const y = cy + ch - v / vmax * ch; c.beginPath(); c.moveTo(cx, y); c.lineTo(cx + cw, y); c.stroke(); c.textAlign = 'right'; c.fillText(v, cx - 12, y + 7); }
  c.textAlign = 'center'; for (let h = 8; h <= 20; h += 2) c.fillText(h, X(t0 + h * 3600e3), cy + ch + 32); c.textAlign = 'left';
  const SC = { lindau: '#9fb4ff', bregenz: '#4fc3a1', rohrspitz: '#c9d85a', altenrhein: '#ef8a5b' };
  for (const s of STATIONS) { const a = (DATA[s.id] || []).filter(r => r.ff != null && +r.t >= ta && +r.t <= tb); c.strokeStyle = SC[s.id] || '#888'; c.lineWidth = s.id === win.id ? 5 : 2.5; c.globalAlpha = s.id === win.id ? 1 : 0.6;
    c.beginPath(); a.forEach((r, i) => i ? c.lineTo(X(+r.t), Y(r.ff)) : c.moveTo(X(+r.t), Y(r.ff))); c.stroke(); c.globalAlpha = 1; }
  let lx = 60; c.font = F(600, 21); for (const s of STATIONS) { c.fillStyle = SC[s.id]; c.fillRect(lx, cy + ch + 56, 22, 6); c.fillStyle = '#c8d7de'; c.fillText(s.name, lx + 30, cy + ch + 65); lx += c.measureText(s.name).width + 64; }
  c.fillStyle = '#8aa6b3'; c.font = F(500, 20); c.fillText('Mittelwind in kn · 10-Min-Werte', cx + cw - 300, cy - 12);
  // why: systems
  let y = 870; c.fillStyle = '#e8f1f5'; c.font = F(800, 34); c.fillText('Warum? Das sagt das Modell', 60, y); y += 22;
  const act = SYSTEMS.filter(q => Math.abs(avg[q.id]) > 0.1).sort((a, b) => Math.abs(avg[b.id]) - Math.abs(avg[a.id])).slice(0, 4);
  for (const q of act) { const v = avg[q.id], a = Math.min(1, Math.abs(v)); y += 54;
    let name = T().sys[q.id][0]; if (q.id === 'rheintal') name = v > 0 ? 'Rheintal: Föhn / Bergwind' : 'Rheintal: Talwind'; if (q.id === 'thermal') name = v > 0 ? 'Landwind' : 'Seewind'; if (q.id === 'syn' && synDir != null) name = `Großwetterlage aus ${dirName(synDir)}`;
    c.fillStyle = '#c8d7de'; c.font = F(600, 25); c.fillText(name, 60, y); c.fillStyle = '#16303f'; shRound(c, 560, y - 22, 380, 26, 13); c.fill(); c.fillStyle = SYSCOL[q.id]; shRound(c, 560, y - 22, Math.max(26, 380 * a), 26, 13); c.fill();
    c.fillStyle = SYSCOL[q.id]; c.font = F(800, 25); c.fillText(Math.round(a * 100) + '%', 955, y); }
  y += 70; c.fillStyle = '#f2c94c'; c.font = F(700, 27); c.fillText('Warst du draußen? Hat es sich so angefühlt? 👇', 60, y);
  c.strokeStyle = '#21414f'; c.lineWidth = 2; c.beginPath(); c.moveTo(60, H - 92); c.lineTo(W - 60, H - 92); c.stroke();
  c.fillStyle = '#e8f1f5'; c.font = F(700, 24); c.fillText('joemoe.at/windshift', 60, H - 46); c.textAlign = 'right'; c.fillStyle = '#8aa6b3'; c.font = F(600, 22); c.fillText('Messung: GeoSphere · MeteoSwiss · DWD · Modell v' + MODEL_VERSION, W - 60, H - 46); c.textAlign = 'left';
  const s2 = cv.toDataURL('image/jpeg', 0.9).split(',')[1];

  // caption
  const why = act.map(q => { const v = avg[q.id];
    return ({ syn: `die Großwetterlage brachte Wind aus ${synDir != null ? dirName(synDir) : '?'}, vom See entlang seiner Achse gelenkt`,
      rheintal: v > 0 ? 'Föhn bzw. Bergwind aus dem Rheintal fächerte über das Delta auf' : 'Talwind zog Seeluft ins Rheintal',
      rhein: 'kalte Luft floss als Strahl aus der Rheinmündung', wald: 'Abflusswind aus dem Bregenzerwald erreichte den See zwischen Bregenz und Hard',
      pfaender: 'Pfänder-Fallwind drückte auf Lochau und Bregenz', swiss: 'Hangabwind kam von den Appenzeller Hängen',
      thermal: v > 0 ? 'Landwind floss von den Ufern aufs Wasser' : 'die Thermik zog als Seewind Luft zu den Ufern' })[q.id] + ` (${Math.round(Math.abs(v) * 100)} %)`; });
  const dom = act[0] ? Math.abs(avg[act[0].id]) / act.reduce((s, q) => s + Math.abs(avg[q.id]), 0) : 0;
  const caption = [
    `⛵ Guter Segeltag: ${st.name}, ${dstr}, ${hm(win.start)}–${hm(win.end)}`, '',
    `Ø ${k(win.mean)} kn aus ${dirName(win.dir)}, Böen bis ${k(win.gust)} kn – und die Richtung blieb auf ±${Math.round(win.dstd)}° stabil.`, '',
    `Warum? Unser Modell sagt: ${why.join('; ')}.` + (dom > 0.6 ? ' Ein System dominierte – darum so konstant.' : ''), '',
    'Warst du draußen? Hat es sich so angefühlt? Schreib es in die Kommentare 👇', '',
    'Kein Meteorologe am Werk: echte Messdaten + ein vereinfachtes Erklär-Modell. Live: joemoe.at/windshift (Link in Bio)', '',
    '#bodensee #segeln #segeltag #wind #vorarlberg #lakeconstance #windshift',
  ].join('\n');
  return { fits, version: MODEL_VERSION, s1, s2, caption };
}, { rows, t0, t1, win, DAY });
await browser.close();
console.log('fits', out.fits.length, 'model', out.version);

fs.mkdirSync('out', { recursive: true });
fs.writeFileSync('out/fits.json', JSON.stringify(out.fits));

const oidc = await fetch(`${process.env.ACTIONS_ID_TOKEN_REQUEST_URL}&audience=windshift-ig`, { headers: { Authorization: `bearer ${process.env.ACTIONS_ID_TOKEN_REQUEST_TOKEN}` } }).then(r => r.json());
const auth = { Authorization: `Bearer ${oidc.value}` };
// log fits
const fl = await fetch(`${FN}?kind=fitlog`, { method: 'POST', headers: { ...auth, 'Content-Type': 'application/json' }, body: JSON.stringify({ version: out.version, rows: out.fits }) });
console.log('fitlog', fl.status, (await fl.text()).slice(0, 200));

if (!win) { console.log('No good window today.'); process.exit(0); }
const imgs = [out.s1, out.s2].map(b => Buffer.from(b, 'base64'));
imgs.forEach((b, i) => fs.writeFileSync(`out/slide${i + 1}.jpg`, b)); fs.writeFileSync('out/caption.txt', out.caption);
console.log(out.caption);
const urls = [];
for (const b of imgs) { const r = await fetch(`${FN}?kind=slide&dry=1`, { method: 'POST', headers: { ...auth, 'Content-Type': 'image/jpeg' }, body: b }).then(r => r.json()); if (!r.ok) throw new Error(JSON.stringify(r)); urls.push(r.image_url); }
console.log('slides', urls);
if (DRY) process.exit(0);
const res = await fetch(`${FN}?kind=carousel`, { method: 'POST', headers: { ...auth, 'Content-Type': 'application/json' }, body: JSON.stringify({ urls, caption: out.caption, lock: FORCE ? undefined : `review-${DAY}` }) });
const body = await res.text(); console.log(res.status, body); if (!res.ok && res.status !== 409) process.exit(1);
