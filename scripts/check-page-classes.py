#!/usr/bin/env python3
"""Every class a page's body uses must have at least one CSS rule on that page.

WHY THIS EXISTS. On 2026-08-28 a rewrite of index.html's stylesheet dropped nine classes that only
the generated secondary pages used (.arrow .checks .chip .cta-row .faq .method-strip .paw .trail
.trust-points). Nothing failed: the homepage was visually verified and looked perfect, the contrast
checker passed, the build script ran clean. /how-it-works/ shipped a 568px book icon, because an
unstyled <svg> falls back to its intrinsic size. The homepage cannot catch this class of bug — only
the pages that consume the shell can.

A class with no rule is not always a defect: some classes exist purely as JS or test hooks. Those are
listed in HOOKS, individually, with the reason. Anything not listed is a finding.

    python3 scripts/check-page-classes.py
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ['index.html', 'about/index.html', 'how-it-works/index.html',
         'safety/index.html', 'faq/index.html',
         'evidence/index.html', 'evidence/method/index.html', 'evidence/limits/index.html',
         'privacy.html', 'terms.html', 'support.html', '404.html', 'confirm.html', 'reset.html']

# Classes that are deliberately not styled. Each needs a reason, so the next person can tell an
# intentional hook from a rule that went missing.
HOOKS = {
    'beta-2':    'JS selector hook — form.beta:not(.beta-2) / form.beta-2 in index.html',
    'hero-copy': 'unstyled layout wrapper; the grid rules live on its parent',
    'brand':     'styled inline on the transactional pages (header.brand + inline style attr)',
}

def strip_tags(html, tag):
    return re.sub(rf'<{tag}\b[^>]*>.*?</{tag}>', '', html, flags=re.S | re.I)

bad = []
for rel in PAGES:
    p = ROOT / rel
    if not p.exists():
        bad.append(f'{rel}: MISSING — the page list names a file that does not exist')
        continue
    html = p.read_text()
    css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', html, flags=re.S))
    # STRIP CSS COMMENTS FIRST. This file's own comments name the selectors they explain
    # (".paw svg in particular sized the inline icons"), so a checker that greps raw CSS passes
    # while every real rule is gone — it reads the explanation of the missing rule as the rule.
    # Proven: the first version of this script did exactly that and stayed green on the mutant.
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    # class= inside <style>/<script> is not markup; ignore those regions when collecting usage.
    body = strip_tags(strip_tags(html, 'style'), 'script')
    used = set()
    for m in re.findall(r'class="([^"]*)"', body):
        used.update(c for c in m.split() if c)
    for c in sorted(used):
        if c in HOOKS:
            continue
        if not re.search(r'\.' + re.escape(c) + r'(?![\w-])', css):
            bad.append(f'{rel}: .{c} is used in the markup but has no CSS rule on this page')

if bad:
    print('\n'.join('  ' + b for b in bad))
    print(f'\n{len(bad)} finding(s).')
    sys.exit(1)
print(f'  clean — {len(PAGES)} pages: every class used in the markup has a rule on its own page')
