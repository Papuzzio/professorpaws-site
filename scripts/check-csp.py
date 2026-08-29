#!/usr/bin/env python3
"""The Content-Security-Policy pages must stay compatible with the policy they declare.

WHY. A CSP that has to allow 'unsafe-inline' for scripts does not stop script injection, which is the
one thing it is for. These pages can declare `script-src 'self'` only because their script lives in
/assets/site.js. If someone later puts an inline <script> back into one of them, the browser silently
blocks it: the page still renders, so the breakage is invisible until whatever that script did is
noticed missing.

Rules, per page that declares a policy:
  1. no inline <script> of any kind (an inline JSON-LD block is blocked too, and loses rich results)
  2. script-src must not contain 'unsafe-inline' or 'unsafe-eval'
  3. no frame-ancestors — it is IGNORED in <meta> and only works as a response header, which GitHub
     Pages cannot set. Listing it looks like clickjacking protection the site does not have.

    python3 scripts/check-csp.py
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
# The pages that MUST carry a policy. index.html is deliberately absent: its two inline scripts would
# force 'unsafe-inline', and the owner ruled (2026-08-29) that no policy beats a hollow one.
MUST_HAVE_CSP = ['privacy.html', 'terms.html', 'support.html', '404.html', 'confirm.html', 'reset.html']
# confirm/reset are hand-maintained auth pages, out of scope, and each carries a legacy
# frame-ancestors. Recorded here rather than silently skipped.
LEGACY_FRAME_ANCESTORS = {'confirm.html', 'reset.html'}

bad = []
for rel in MUST_HAVE_CSP:
    p = ROOT / rel
    if not p.exists():
        bad.append(f'{rel}: MISSING'); continue
    html = p.read_text()
    m = re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]*)"', html)
    if not m:
        bad.append(f'{rel}: declares no Content-Security-Policy, but is on the list that must')
        continue
    csp = m.group(1)

    inline = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>', html)
    if inline:
        bad.append(f'{rel}: {len(inline)} inline <script> under a CSP — the browser will block it silently')

    script_src = re.search(r'script-src([^;]*)', csp)
    if script_src:
        for unsafe in ("'unsafe-inline'", "'unsafe-eval'"):
            if unsafe in script_src.group(1):
                bad.append(f'{rel}: script-src contains {unsafe} — that policy does not stop script injection')

    if 'frame-ancestors' in csp and rel not in LEGACY_FRAME_ANCESTORS:
        bad.append(f'{rel}: frame-ancestors is ignored in a <meta> tag; it reads as protection that is not there')

if bad:
    print('\n'.join('  ' + b for b in bad)); print(f'\n{len(bad)} finding(s).'); sys.exit(1)
print(f'  clean — {len(MUST_HAVE_CSP)} pages declare a policy; none allows inline or eval script')
