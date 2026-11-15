// Posts an approved image (posts/manual/<name>.jpg) or carousel (posts/manual/<name>/1.jpg, 2.jpg …) with caption <name>.txt.
import fs from 'node:fs';
const name = process.env.POST_NAME; if (!name) throw new Error('POST_NAME missing');
const DRY = process.env.DRY === 'true';
const FN = 'https://lfiadqrbacphpoeihfpg.supabase.co/functions/v1/ig-post';
const caption = fs.readFileSync(`posts/manual/${name}.txt`, 'utf8').trim();
const oidc = await fetch(`${process.env.ACTIONS_ID_TOKEN_REQUEST_URL}&audience=windshift-ig`, { headers: { Authorization: `bearer ${process.env.ACTIONS_ID_TOKEN_REQUEST_TOKEN}` } }).then(r => r.json());
const auth = { Authorization: `Bearer ${oidc.value}` };
const dir = `posts/manual/${name}`;
let res;
if (fs.existsSync(dir) && fs.statSync(dir).isDirectory()) {
  const files = fs.readdirSync(dir).filter(f => /\.jpe?g$/i.test(f)).sort((a, b) => parseInt(a) - parseInt(b));
  const urls = [];
  for (const f of files) {   // upload each slide (dry = store only)
    const r = await fetch(`${FN}?kind=slide&dry=1`, { method: 'POST', headers: { ...auth, 'Content-Type': 'image/jpeg' }, body: fs.readFileSync(`${dir}/${f}`) }).then(r => r.json());
    if (!r.ok) throw new Error('upload failed: ' + JSON.stringify(r)); urls.push(r.image_url); console.log('uploaded', f);
  }
  if (DRY) { console.log(urls); process.exit(0); }
  res = await fetch(`${FN}?kind=carousel`, { method: 'POST', headers: { ...auth, 'Content-Type': 'application/json' }, body: JSON.stringify({ urls, caption }) });
} else {
  const q = new URLSearchParams({ caption, kind: 'manual' }); if (DRY) q.set('dry', '1');
  res = await fetch(`${FN}?${q}`, { method: 'POST', headers: { ...auth, 'Content-Type': 'image/jpeg' }, body: fs.readFileSync(`${dir}.jpg`) });
}
const body = await res.text(); console.log(res.status, body); if (!res.ok) process.exit(1);
