// YouTube: OAuth bağlantısı ve zamanlanmış (publishAt) Shorts yükleme.
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const store = require('./store'), { readEnv } = require('./ai');
const ENVF = path.join(store.ROOT, '.env');
const REDIRECT = port => `http://localhost:${port}/oauth/google/callback`;
let states = new Set();

function setEnv(patch) { const o = readEnv(); Object.assign(o, patch); fs.writeFileSync(ENVF, Object.entries(o).map(([k, v]) => `${k}=${v}`).join('\n') + '\n'); }
const ytReady = () => { const e = readEnv(); return !!(e.YT_CLIENT_ID && e.YT_CLIENT_SECRET && e.YT_REFRESH_TOKEN); };
const ytConfigured = () => { const e = readEnv(); return !!(e.YT_CLIENT_ID && e.YT_CLIENT_SECRET); };

function authUrl(port) {
  const e = readEnv(); if (!ytConfigured()) throw new Error('Önce Client ID ve Client Secret kaydet');
  const st = crypto.randomBytes(16).toString('hex'); states.add(st);
  const q = new URLSearchParams({ client_id: e.YT_CLIENT_ID, redirect_uri: REDIRECT(port), response_type: 'code', scope: 'https://www.googleapis.com/auth/youtube.upload', access_type: 'offline', prompt: 'consent', state: st });
  return 'https://accounts.google.com/o/oauth2/v2/auth?' + q;
}
async function callback(port, code, state) {
  if (!states.delete(state)) throw new Error('Geçersiz oturum, tekrar dene'); const e = readEnv();
  const r = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ code, client_id: e.YT_CLIENT_ID, client_secret: e.YT_CLIENT_SECRET, redirect_uri: REDIRECT(port), grant_type: 'authorization_code' }) });
  const j = await r.json(); if (!r.ok || !j.refresh_token) throw new Error('Google yanıtı: ' + (j.error_description || j.error || 'refresh_token gelmedi'));
  setEnv({ YT_REFRESH_TOKEN: j.refresh_token }); store.log('YouTube hesabı bağlandı');
}
async function accessToken() {
  const e = readEnv(); const r = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ client_id: e.YT_CLIENT_ID, client_secret: e.YT_CLIENT_SECRET, refresh_token: e.YT_REFRESH_TOKEN, grant_type: 'refresh_token' }) });
  const j = await r.json(); if (!r.ok) throw new Error('Token alınamadı: ' + (j.error_description || j.error)); return j.access_token;
}
// Gizli yükler, publishAt zamanında YouTube kendisi yayına alır
async function ytUpload(ep, videoFile, zaman) {
  const tok = await accessToken(), size = fs.statSync(videoFile).size;
  const body = { snippet: { title: (ep.baslik + ' #Shorts').slice(0, 100), description: ep.aciklama, tags: ep.etiketler, categoryId: '23', defaultLanguage: 'tr' }, status: { privacyStatus: 'private', publishAt: new Date(zaman).toISOString(), selfDeclaredMadeForKids: false, containsSyntheticMedia: true } };
  const init = await fetch('https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status', { method: 'POST', headers: { Authorization: 'Bearer ' + tok, 'Content-Type': 'application/json; charset=UTF-8', 'X-Upload-Content-Length': String(size), 'X-Upload-Content-Type': 'video/mp4' }, body: JSON.stringify(body) });
  if (!init.ok) throw new Error('YouTube başlatma ' + init.status + ': ' + (await init.text()).slice(0, 250));
  const up = await fetch(init.headers.get('location'), { method: 'PUT', headers: { 'Content-Length': String(size), 'Content-Type': 'video/mp4' }, body: fs.readFileSync(videoFile) });
  const j = await up.json().catch(() => ({})); if (!up.ok) throw new Error('YouTube yükleme ' + up.status + ': ' + JSON.stringify(j).slice(0, 250));
  return { id: j.id, url: 'https://youtube.com/shorts/' + j.id };
}
module.exports = { ytReady, ytConfigured, authUrl, callback, ytUpload, setEnv };
