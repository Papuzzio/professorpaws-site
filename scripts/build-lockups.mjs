// build-lockups.mjs — the Professor Paws lockup system (owner ruling "Option A", 2026-08-20).
//
// The board supplies the COMPOSITION: navy card, badge, heavy rounded PROFESSOR, script Paws.
// The DOG is the frozen mascot (sha 2b0a5709…), never the board's AI-generated retriever — the
// board's dog is not the app's dog, and build 21 ships the frozen one as its App Store icon.
//
// The teal decorative dashes and the trailing paw print are OMITTED. They were rendered both ways
// (see docs/LAUNCH_LOG.md): a single dash reads as a hyphen — "-Paws" looks like a typo — and at
// 32px the whole flourish is noise. The owner's instruction was to keep them only if the mark is
// objectively stronger with them. It is not.
//
// Lockups ship as RASTERS because the wordmark is set in self-hosted webfonts; the fonts are
// embedded as data URIs at build time so this is reproducible offline and the page loads one image.
//
//   node scripts/build-lockups.mjs
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';

const b64 = p => readFileSync(p).toString('base64');
const MASCOT = b64('assets/logo/mascot-only.png');
const NUNITO = b64('assets/fonts/nunito-var-latin.woff2');
const SCRIPT = b64('assets/fonts/grandstander-italic800-latin.woff2');
const NAVY = '#14213D', TEAL = '#14AAA3', ORANGE = '#FF8C42', CREAM = '#FFF8EE';

const CSS = `
@font-face{font-family:Nunito;src:url(data:font/woff2;base64,${NUNITO}) format("woff2");font-weight:400 800}
@font-face{font-family:PPScript;src:url(data:font/woff2;base64,${SCRIPT}) format("woff2");font-style:italic;font-weight:800}
*{box-sizing:border-box}
html,body{margin:0;background:transparent}
.lk{display:inline-flex;align-items:center;gap:calc(var(--b)*.13);font-family:Nunito}
.badge{width:var(--b);height:var(--b);border-radius:50%;background:var(--ring);display:grid;place-items:center;flex:0 0 auto}
.disc{width:calc(var(--b)*.89);height:calc(var(--b)*.89);border-radius:50%;background:${TEAL};display:grid;place-items:center;overflow:hidden}
.disc img{width:calc(var(--b)*.79);height:calc(var(--b)*.79);object-fit:contain;display:block}
.pro{font-weight:800;font-size:calc(var(--b)*.345);letter-spacing:-.015em;color:var(--ink);line-height:.95;text-transform:uppercase;white-space:nowrap}
.pw{font-family:PPScript;font-style:italic;font-weight:800;font-size:calc(var(--b)*.52);color:${ORANGE};line-height:.9;margin-top:calc(var(--b)*-.05);white-space:nowrap}
.card{background:${NAVY};border-radius:calc(var(--b)*.20);padding:calc(var(--b)*.17) calc(var(--b)*.28);display:inline-block}
.stack{display:inline-flex;flex-direction:column;align-items:center;gap:calc(var(--b)*.10);font-family:Nunito;text-align:center}
`;
const lockup = (b, ink, ring) =>
  `<div class="lk" style="--b:${b}px;--ink:${ink};--ring:${ring}"><div class="badge"><div class="disc">` +
  `<img src="data:image/png;base64,${MASCOT}"></div></div>` +
  `<div><div class="pro">Professor</div><div class="pw">Paws</div></div></div>`;
const stack = (b, ink, ring) =>
  `<div class="stack" style="--b:${b}px;--ink:${ink};--ring:${ring}"><div class="badge"><div class="disc">` +
  `<img src="data:image/png;base64,${MASCOT}"></div></div>` +
  `<div><div class="pro">Professor</div><div class="pw" style="margin-top:calc(var(--b)*-.03)">Paws</div></div></div>`;
const wordmark = (b, ink) =>
  `<div style="--b:${b}px;font-family:Nunito;display:inline-block"><div class="pro" style="--ink:${ink}">Professor</div>` +
  `<div class="pw">Paws</div></div>`;

const VARIANTS = {
  'lockup-horizontal-light': { html: lockup(120, NAVY, 'transparent'), bg: 'transparent' },
  'lockup-horizontal-dark':  { html: lockup(120, '#FFFFFF', '#FFFFFF'), bg: 'transparent' },
  'lockup-card-dark':        { html: `<div class="card" style="--b:120px">${lockup(120, '#FFFFFF', '#FFFFFF')}</div>`, bg: 'transparent' },
  'lockup-compact':          { html: lockup(60, NAVY, 'transparent'),  bg: 'transparent' },
  'lockup-compact-dark':     { html: lockup(60, '#FFFFFF', '#FFFFFF'), bg: 'transparent' },
  'lockup-stacked-light':    { html: stack(140, NAVY, 'transparent'),  bg: 'transparent' },
  'wordmark-light':          { html: wordmark(120, NAVY),        bg: 'transparent' },
  'wordmark-dark':           { html: wordmark(120, '#FFFFFF'),   bg: 'transparent' },
};

const dir = mkdtempSync(path.join(tmpdir(), 'lockups-'));
const port = 9500 + Math.floor(Math.random() * 200);
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${dir}`, '--hide-scrollbars',
   '--force-device-scale-factor=2', '--no-first-run', 'about:blank'], { stdio: 'ignore' });
const wait = ms => new Promise(r => setTimeout(r, ms));
let tabs; for (let i = 0; i < 60; i++) { try { tabs = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); break; } catch { await wait(150); } }
const sock = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl);
let id = 0; const pend = new Map();
sock.onmessage = e => { const m = JSON.parse(e.data); if (pend.has(m.id)) { pend.get(m.id)(m.result); pend.delete(m.id); } };
await new Promise(r => sock.onopen = r);
const send = (m, p = {}) => new Promise(r => { const i = ++id; pend.set(i, r); sock.send(JSON.stringify({ id: i, method: m, params: p })); });
await send('Page.enable');
await send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });
for (const [name, v] of Object.entries(VARIANTS)) {
  const page = `<!DOCTYPE html><html><head><meta charset="utf-8"><style>${CSS}</style></head>` +
               `<body><div id="t" style="display:inline-block;padding:8px">${v.html}</div></body></html>`;
  writeFileSync(path.join(dir, 'p.html'), page);
  await send('Emulation.setDeviceMetricsOverride', { width: 1400, height: 500, deviceScaleFactor: 2, mobile: false });
  await send('Page.navigate', { url: 'file://' + path.join(dir, 'p.html') });
  await wait(900);
  await send('Runtime.evaluate', { expression: 'document.fonts.ready', awaitPromise: true });
  await wait(250);
  const box = (await send('Runtime.evaluate', { returnByValue: true, expression:
    `(()=>{const r=document.getElementById('t').getBoundingClientRect();return JSON.stringify({x:r.x,y:r.y,w:r.width,h:r.height})})()` })).result.value;
  const { x, y, w, h } = JSON.parse(box);
  const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
    clip: { x, y, width: w, height: h, scale: 2 } });
  writeFileSync(`assets/logo/${name}.png`, Buffer.from(shot.data, 'base64'));
  console.log(`  ${name}.png  ${Math.round(w)}×${Math.round(h)} css @2x`);
}
sock.close(); chrome.kill(); process.exit(0);
