#!/usr/bin/env python3
"""
THE 2026-08-27 BRAND FREEZE, PINNED.

Owner rulings this enforces:
  * "Deep Ink labels on orange."
  * "#0F7A76 wherever a white label is needed."
  * "Never white on Professor Orange or Paws Teal."

A palette is not a set of hex values, it is a set of PAIRS that are allowed to sit on each other.
The site has already shipped a token swap that silently weakened an alpha rule (--field-line held
the same .42 while the ink under it changed, dropping 3.2:1 -> 2.56:1). Values are checked here,
but so are the pairs, because the pair is what a reader actually sees.

Run:  python3 scripts/check-brand-contrast.py          (add --selftest for the positive control)
Exit: 0 clean, 1 violations.
"""
import re, sys, pathlib, itertools

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ['index.html','about/index.html','how-it-works/index.html','safety/index.html',
         'faq/index.html','privacy.html','terms.html','support.html','404.html','confirm.html','reset.html']

APPROVED = {'--orange':'#F59A23','--teal':'#14AAA3','--green':'#63A65F',
            '--cream':'#FFF8ED','--paper':'#FFFCF7','--ink':'#14213D'}
RETIRED  = ['#EE6F1E','#2C2C2C','#FBF8F3','#FDFBF5','#6B665E','#6b4ea0','#1a1a2e','rgba(44,44,44']
# never carries a white label (all below 3:1 against white)
NO_WHITE = {'--orange','--teal','--green'}

def lin(c):
    c /= 255
    return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
def lum(h):
    h = h.lstrip('#')
    return 0.2126*lin(int(h[0:2],16)) + 0.7152*lin(int(h[2:4],16)) + 0.0722*lin(int(h[4:6],16))
def ratio(a,b):
    la, lb = lum(a), lum(b)
    return (max(la,lb)+.05)/(min(la,lb)+.05)

def strip_comments(css):                      # §14.1 — a record is not a declaration
    return re.sub(r'/\*.*?\*/', ' ', css, flags=re.S)

WHITE = re.compile(r'color\s*:\s*(#fff(?:fff)?\b|white\b|#FFFCF7|var\(--paper\))', re.I)

MIN_AA = 4.5   # normal-size body text

def resolve(css, name, seen=None):
    """Resolve a custom property to a literal hex, following var() chains.

    THE PAIR RULE COULD NOT SEE THROUGH INDIRECTION. `.btn` now reads
    `background:var(--action)`, and --action is itself `var(--teal-deep)`. Checked against the
    literal token names alone, a --action set to the FROZEN brand teal (2.87:1 with white) passed
    as clean — verified by mutating it and watching this script say "clean". A checker that cannot
    fire on the one line the token set exists to protect is not a guard.
    """
    m = re.search(rf'{re.escape(name)}\s*:\s*([^;]+);', css)
    if not m: return None
    val = m.group(1).strip()
    vm = re.fullmatch(r'var\(\s*(--[\w-]+)\s*\)', val)
    if vm:
        seen = seen or set()
        if vm.group(1) in seen: return None          # circular — refuse rather than loop
        seen.add(vm.group(1))
        return resolve(css, vm.group(1), seen)
    if val.lower() in ('white', '#fff', '#ffffff'): return '#FFFFFF'
    if re.fullmatch(r'#[0-9A-Fa-f]{6}', val): return val.upper()
    m3 = re.fullmatch(r'#([0-9A-Fa-f]{3})', val)
    if m3: return ('#' + ''.join(c * 2 for c in m3.group(1))).upper()
    return None

def check(files):
    bad = []
    for rel in files:
        p = ROOT / rel
        if not p.exists(): continue
        raw = p.read_text()
        css = strip_comments(raw)

        # 1. retired palette values still being DECLARED (comments already stripped)
        for old in RETIRED:
            if old in css:
                bad.append(f'{rel}: retired palette value {old} is still declared')

        # 2. token values must be the approved ones
        for tok, want in APPROVED.items():
            for found in re.findall(rf'{re.escape(tok)}\s*:\s*(#[0-9A-Fa-f]{{6}})', css):
                if found.upper() != want:
                    bad.append(f'{rel}: {tok} is {found}, the approved value is {want}')

        # 3. THE PAIR RULE: no rule may put a white label on a no-white background
        for block in re.findall(r'\{[^{}]*\}', css):
            for tok in NO_WHITE:
                if re.search(rf'background(?:-color)?\s*:\s*var\(\s*{re.escape(tok)}\s*\)', block) and WHITE.search(block):
                    r = ratio('#FFFFFF', APPROVED[tok])
                    bad.append(f'{rel}: white label on {tok} ({APPROVED[tok]}) = {r:.2f}:1 — banned by the 2026-08-27 ruling')

        # 4. THE ACTION PAIR — the one line the token set exists to make changeable, so the one
        #    line that most needs a guard. Resolved through var() chains, at rest AND on hover.
        ink = resolve(css, '--action-ink')
        # EVERY state the user can put the control into, not just the ones we happened to think of.
        # --action-active shipped DEFINED AND UNCHECKED for one commit. It passed at 8.04:1, which is
        # exactly why it was worth closing: an unchecked token that passes today is the one that
        # silently stops passing tomorrow. (Found by Lane B, 2026-08-27.)
        for state in ('--action', '--action-hover', '--action-active'):
            val = resolve(css, state)
            if val and ink:
                r = ratio(ink, val)
                if r < MIN_AA:
                    bad.append(f'{rel}: --action-ink on {state} ({ink} on {val}) = {r:.2f}:1, below {MIN_AA}:1')
        # 5. EVERY CONTROL PAINTS FROM --action. The rule that would have caught what the 2026-08-27
        #    audit found: FIFTEEN action-coloured controls in THREE colours, because each new page
        #    reached for whatever literal was nearby. A block with a solid background AND a light
        #    label is a control; if the background is not var(--action*), it has drifted. Ghost
        #    buttons (transparent) and dark bands that set no colour are not controls.
        #
        #    SCOPE, STATED SO GREEN IS NOT READ AS "ALL CONTROLS CHECKED": this sees DARK action
        #    controls only. A control with a LIGHT background and a dark label is invisible to it —
        #    `a.skip` on the homepage is precisely that (paper background, ink label, 15.61:1,
        #    correct as designed). Widening to "any solid background on an interactive element"
        #    would flag every input and the skip link, and a noisy guard gets switched off. A guard
        #    that documents what it cannot see is worth more than one implying it saw everything.
        for block in re.findall(r'\{[^{}]*\}', css):
            m = re.search(r'background(?:-color)?\s*:\s*([^;}]+)', block)
            if not m:
                continue
            val = m.group(1).strip().lower()
            if 'transparent' in val or 'none' in val or 'var(--action' in val:
                continue
            if WHITE.search(block):
                bad.append(f'{rel}: a control paints from "{val}" instead of var(--action) — the drift the token set exists to prevent')

        # 6. A PAGE THAT USES --action MUST DEFINE IT. An undefined custom property makes the whole
        #    declaration INVALID, so `background:var(--action); color:#fff` renders a white label on
        #    NO background — an invisible control. confirm.html and reset.html are the dangerous
        #    case: fully standalone, reached by no build step, and they are the password-reset and
        #    email-confirm pages, where an invisible submit fails silently.
        for tok in ('--action', '--action-ink', '--action-hover'):
            if 'var(%s)' % tok in css.replace(' ', '') and resolve(css, tok) is None:
                bad.append(f'{rel}: uses var({tok}) but never defines it — CSS drops the declaration, leaving a label on no background (invisible control)')

    return bad

def selftest():
    """POSITIVE CONTROL: a checker that has never been seen to fail is not evidence."""
    tmp = ROOT / '_contrast_selftest.html'
    tmp.write_text(':root { --orange:#F59A23; }\n.x { background:var(--orange); color:#fff; }\n'
                   '/* a comment mentioning #EE6F1E must NOT trip the retired-value check */\n')
    tmp2 = ROOT / '_contrast_selftest_action.html'
    # --action pointed at the FROZEN brand teal through a var() chain: 2.87:1 with a white label.
    # This is the exact mutant that passed as "clean" before check 4 existed.
    tmp2.write_text(':root { --teal:#14AAA3; --action:var(--teal); --action-ink:#fff;'
                    ' --action-hover:var(--teal); --action-active:var(--teal); }\n')
    # RULE 5 mutant: a control painting from a literal instead of --action (the 15-in-3-colours drift).
    tmp3 = ROOT / '_contrast_selftest_drift.html'
    tmp3.write_text('.submit { background:#B4530A; color:#FFFFFF; }\n'
                    '.ghost { background:transparent; color:#fff; }\n'      # must NOT trip: not a control
                    '.band { background:#14213D; }\n')                       # must NOT trip: sets no colour
    # RULE 6 mutant: uses --action but never defines it -> CSS drops the declaration -> invisible control.
    tmp4 = ROOT / '_contrast_selftest_undefined.html'
    tmp4.write_text('.submit { background:var(--action); color:var(--action-ink); }\n')
    try:
        found = check(['_contrast_selftest.html'])
        white  = [b for b in found if 'white label' in b]
        commented = [b for b in found if '#EE6F1E' in b]
        act = [b for b in check(['_contrast_selftest_action.html']) if '--action' in b]
        drift = [b for b in check(['_contrast_selftest_drift.html']) if 'drift' in b]
        undef = [b for b in check(['_contrast_selftest_undefined.html']) if 'never defines it' in b]
        ok = (len(white) == 1 and not commented and len(act) == 3
              and len(drift) == 1 and len(undef) >= 1)
        print(('  SELFTEST PASS — ' if ok else '  SELFTEST FAIL — ') +
              f'{len(white)} white-on-orange caught (want 1), {len(commented)} false hits on a commented value (want 0), '
              f'{len(act)} action-state failures caught (want 3: rest + hover + active), '
              f'{len(drift)} literal-background drift caught (want 1; ghost + dark band must NOT trip), '
              f'{len(undef)} undefined-token invisible-control caught (want >=1)')
        for b in white + act + drift + undef: print(f'    caught: {b}')
        return 0 if ok else 1
    finally:
        tmp.unlink(missing_ok=True)
        tmp2.unlink(missing_ok=True)
        tmp3.unlink(missing_ok=True)
        tmp4.unlink(missing_ok=True)

if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    v = check(PAGES)
    if v:
        print('BRAND CONTRAST VIOLATIONS:')
        for b in v: print('  ' + b)
        sys.exit(1)
    print(f'  clean — {len(PAGES)} pages: approved token values, no retired values, no white label on orange/teal/green')
