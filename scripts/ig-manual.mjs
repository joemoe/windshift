// Posts a prepared image + caption from posts/manual/<name>.jpg/.txt (approved by Joe) via the ig-post function.
import fs from 'node:fs';
const name = process.env.POST_NAME; if (!name) throw new Error('POST_NAME missing');
const img = fs.readFileSync(`posts/manual/${name}.jpg`), caption = fs.readFileSync(`posts/manual/${name}.txt`, 'utf8').trim();
const oidc = await fetch(`${process.env.ACTIONS_ID_TOKEN_REQUEST_URL}&audience=windshift-ig`, { headers: { Authorization: `bearer ${process.env.ACTIONS_ID_TOKEN_REQUEST_TOKEN}` } }).then(r => r.json());
const q = new URLSearchParams({ caption, kind: 'manual' }); if (process.env.DRY === 'true') q.set('dry', '1');
const res = await fetch(`https://lfiadqrbacphpoeihfpg.supabase.co/functions/v1/ig-post?${q}`, { method: 'POST', headers: { Authorization: `Bearer ${oidc.value}`, 'Content-Type': 'image/jpeg' }, body: img });
const body = await res.text(); console.log(res.status, body); if (!res.ok) process.exit(1);
