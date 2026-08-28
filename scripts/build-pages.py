#!/usr/bin/env python3
"""Build the secondary pages (/about/ /how-it-works/ /safety/ /faq/) FROM index.html's own shell.

The homepage is the single source of the site's identity: its <style> block, the icon sprite, the header (the frozen
B lockup + restrained nav + CTA) and the footer are lifted verbatim at build time, so the secondary pages can never
drift from it. Page bodies live in pages/*.html (main content only). Run after any change to index.html's shell or to
a page body; commit the generated <slug>/index.html files (GitHub Pages serves /slug/).

    python3 scripts/build-pages.py
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = (ROOT / 'index.html').read_text()

def between(s, a, b, start=0):
    i = s.index(a, start); j = s.index(b, i + len(a)); return s[i:j + len(b)], j + len(b)

# ── pieces lifted from the homepage ───────────────────────────────────────────────────────────────────────────────
font_face, after = between(INDEX, '<style>', '</style>')                 # the @font-face block
style, _ = between(INDEX, '<style>', '</style>', after)                  # the site CSS
sprite, _ = between(INDEX, '<svg width="0" height="0"', '</defs></svg>')
header, _ = between(INDEX, '<header class="top">', '</header>')
footer, _ = between(INDEX, '<footer>', '</footer>')
preload = re.search(r'<link rel="preload"[^>]*fraunces[^>]*/>', INDEX).group(0)
icons = '\n'.join(re.findall(r'<link rel="(?:icon|apple-touch-icon)"[^>]*/>', INDEX))
beacon, _ = between(INDEX, '  // ── FIRST-PARTY AGGREGATE COUNTS', "  ppEvent('page_view');")
beacon = beacon[: -len("  ppEvent('page_view');")]                         # the page_view call is re-added in the shell

# On a secondary page the header nav points at the PAGES (on the homepage it scrolls to the sections).
header = (header.replace('href="#how"', 'href="/how-it-works/"')
                .replace('href="#trust"', 'href="/safety/"')
                .replace('href="#faq"', 'href="/faq/"')
                .replace('href="#beta" data-cta="header"', 'href="/#beta" data-cta="header"'))
# the brand lockup must not lazy-load nor fetch-priority on inner pages — it is above the fold everywhere; unchanged.

PAGES = {
    'about':        dict(title='About — why I built Professor Paws',
                         desc="Professor Paws exists because of one kid who learns differently. The founder's story, in his own words, and why privacy and control came first."),
    'how-it-works': dict(title='How Professor Paws works — one step at a time',
                         desc='How Professor Paws turns real schoolwork into calm, step-by-step practice: add the work, one step at a time, then see where help was needed.'),
    'safety':       dict(title='Safety and privacy — Professor Paws',
                         desc="Parent-created accounts, no ads, no social features, no open-ended AI chat, no third-party ad tracking, and clear controls for deleting your child's data."),
    'faq':          dict(title='Questions parents ask — Professor Paws',
                         desc='Does it give children the answer? Is it an AI tutor? What data do you collect? Ages, subjects, devices, cost — every question parents ask about Professor Paws.'),
}

def shell(slug, meta, body):
    url = f'https://playprofessorpaws.com/{slug}/'
    return f'''<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}" />
<link rel="canonical" href="{url}" />
<meta property="og:title" content="{meta['title']}" />
<meta property="og:description" content="{meta['desc']}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{url}" />
<meta property="og:site_name" content="Professor Paws" />
<meta property="og:locale" content="en_US" />
<meta property="og:image" content="https://playprofessorpaws.com/assets/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="Professor Paws — homework help for kids who shut down, rush, or melt down over schoolwork — beside the iPad app's homework screen" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{meta['title']}" />
<meta name="twitter:description" content="{meta['desc']}" />
<meta name="twitter:image" content="https://playprofessorpaws.com/assets/og-image.png" />
{icons}
{preload}
{font_face}
{style}
<style>
  /* page-specific: a reading column for the secondary pages */
  .page {{ max-width:720px; margin:0 auto; padding-block:40px 72px; }}
  /* CALMER 2026-08-27, same reasoning as index.html's headings: 144 is Fraunces' POSTER cut. At
     this size (~42px max) the text cut is the correct optical size, not a stylistic choice. */
  .page h1 {{ font-size:clamp(1.9rem,5vw,2.6rem); font-weight:600; font-variation-settings:'opsz' 48, 'SOFT' 50, 'WONK' 0; max-width:22ch; }}
  .page .lede {{ font-size:1.12rem; color:var(--ink-soft); margin-top:14px; max-width:var(--measure); }}
  .page h2 {{ font-size:1.45rem; margin-top:44px; }}
  .page h3 {{ font-size:1.1rem; margin-top:22px; }}
  .page p {{ margin-top:10px; max-width:var(--measure); }}
  .page ul.checks {{ list-style:none; margin:12px 0 0; padding:0; display:grid; gap:9px; }}
  .page ul.checks li {{ display:flex; gap:10px; align-items:flex-start; }}
  .page ul.checks svg {{ flex:0 0 16px; width:16px; height:16px; margin-top:6px; color:var(--orange-deep); }}
  .page .cta-row {{ margin-top:36px; }}
  .page .cta-row .btn {{ padding:15px 32px; font-size:1.08rem; min-height:48px; display:inline-block; }}
  .page .back {{ display:inline-block; margin-top:28px; }}
  .page .trail {{ margin:22px 0 0; }}
  .page .method-strip {{ justify-content:flex-start; margin-top:14px; }}
  .page .faq {{ max-width:none; margin:18px 0 0; }}
  .page .trust-points {{ margin-top:18px; max-width:none; }}
  .page .chip {{ flex:0 0 34px; width:34px; height:34px; border-radius:10px; background:var(--paper); border:1px solid var(--line); display:grid; place-items:center; color:var(--orange-deep); }}
  .page .chip svg {{ width:18px; height:18px; }}
  .page .sig {{ color:var(--ink-soft); font-size:.96rem; }}
  a.more {{ color:var(--ink); font-weight:600; text-decoration:underline; text-underline-offset:3px; display:inline-flex; align-items:center; min-height:44px; }}
</style>
</head>
<body>
{sprite}

<a class="skip" href="#main">Skip to content</a>
{header}
<main id="main">
<article class="wrap page">
{body.strip()}
</article>
</main>

{footer}

<script>
  document.documentElement.classList.add('js');
{beacon}  ppEvent('page_view');
  document.querySelectorAll('[data-cta]').forEach(a => a.addEventListener('click', () => ppEvent('primary_cta_click', a.dataset.cta)));
  document.querySelectorAll('a[href="/privacy.html"]').forEach(a => a.addEventListener('click', () => ppEvent('privacy_opened')));
</script>
</body>
</html>
'''

for slug, meta in PAGES.items():
    body = (ROOT / 'pages' / f'{slug}.html').read_text()
    out = ROOT / slug / 'index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(shell(slug, meta, body))
    print(f'wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)')
