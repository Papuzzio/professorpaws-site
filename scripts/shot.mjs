// shot.mjs <url> <out.png> <width> [height] — full-page screenshot at a TRUE viewport width.
// Headless Chrome floors its window at ~500px, so narrow widths must come from CDP's
// Emulation.setDeviceMetricsOverride, not from --window-size. Pass a height to capture the
// fold only; omit it for the full page.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
const [,, url, out, W, H] = process.argv;
const width = +W, height = H ? +H : 900;
const dir = mkdtempSync(path.join(tmpdir(), 'shot-'));          // a FRESH profile per run: Chrome's disk cache
const port = 9300 + Math.floor(Math.random() * 300);            // once served a stale asset and faked a defect.
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${dir}`,
   '--hide-scrollbars', '--force-device-scale-factor=2', '--no-first-run', '--disable-extensions', 'about:blank'],
  { stdio: 'ignore' });
const wait = ms => new Promise(r => setTimeout(r, ms));
const json = async p => (await fetch(`http://127.0.0.1:${port}${p}`)).json();
let tabs; for (let i = 0; i < 60; i++) { try { tabs = await json('/json/list'); break; } catch { await wait(120); } }
const ws = new (await import('node:module')).default.createRequire(import.meta.url);
const WebSocket = globalThis.WebSocket;
const sock = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl);
let id = 0; const pending = new Map();
sock.onmessage = e => { const m = JSON.parse(e.data); if (pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); } };
await new Promise(r => sock.onopen = r);
const send = (method, params = {}) => new Promise(r => { const i = ++id; pending.set(i, r); sock.send(JSON.stringify({ id: i, method, params })); });
await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 2, mobile: width < 768 });
await send('Page.enable');
await send('Page.navigate', { url });
await wait(2600);
// reveal every .fade so a full-page shot is not half-empty
await send('Runtime.evaluate', { expression: "document.querySelectorAll('.fade').forEach(e=>e.classList.add('in')); document.fonts.ready" , awaitPromise:true });
await wait(700);
const metrics = await send('Page.getLayoutMetrics');
const full = Math.ceil(metrics.cssContentSize.height);
if (!H) { await send('Emulation.setDeviceMetricsOverride', { width, height: full, deviceScaleFactor: 2, mobile: width < 768 }); await wait(500); }
const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: !H });
writeFileSync(out, Buffer.from(shot.data, 'base64'));
console.log(`${out}  ${width}px viewport  full-page height ${full}px`);
sock.close(); chrome.kill();
process.exit(0);
