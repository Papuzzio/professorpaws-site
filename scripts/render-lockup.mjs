// render-lockup.mjs <svg> <out.png> <w> <h> — transparent-background raster of a lockup SVG.
// Same method as the 2026-08-19 header raster: headless Chrome at 2x CSS size, alpha preserved.
import { spawn } from 'node:child_process';
import { writeFileSync, readFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
const [,, svgPath, out, W, H] = process.argv;
const dir = mkdtempSync(path.join(tmpdir(), 'lockup-'));
writeFileSync(path.join(dir, 'm.svg'), readFileSync(svgPath));
writeFileSync(path.join(dir, 'i.html'),
  `<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent}
   img{display:block;width:${W}px;height:${H}px}</style></head><body><img src="m.svg"></body></html>`);
const port = 9700 + Math.floor(Math.random()*200);
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ['--headless=new','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=1',
   `--remote-debugging-port=${port}`,`--user-data-dir=${dir}/prof`,'about:blank'], { stdio:'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let t; for (let i=0;i<60;i++){ try { const r=await fetch(`http://127.0.0.1:${port}/json`); const l=await r.json(); t=l.find(x=>x.type==='page'); if(t)break; } catch{} await sleep(250); }
const ws=new WebSocket(t.webSocketDebuggerUrl); await new Promise(r=>ws.onopen=r);
let id=0; const p=new Map();
ws.onmessage=e=>{const m=JSON.parse(e.data); if(m.id&&p.has(m.id)){p.get(m.id)(m);p.delete(m.id);}};
const send=(m,q={})=>new Promise(r=>{const i=++id;p.set(i,r);ws.send(JSON.stringify({id:i,method:m,params:q}));});
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride',{width:+W,height:+H,deviceScaleFactor:2,mobile:false});
await send('Emulation.setDefaultBackgroundColorOverride',{color:{r:0,g:0,b:0,a:0}});
await send('Page.navigate',{url:`file://${dir}/i.html`});
await sleep(1400);
const {result:{data}}=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});
writeFileSync(out, Buffer.from(data,'base64'));
console.log(`  ${out}`);
ws.close(); chrome.kill();
