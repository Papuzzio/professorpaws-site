# Orange divergence — app vs site. SCOPED TASK, NOT ACTIONED.

**Owner ruling 2026-08-28: leave it.** "Two oranges nobody sees together isn't worth a token
migration across a live colour system." This document exists so the decision is *recorded with its
inventory* rather than rediscovered, and so that if it is ever picked up, the work is already scoped.

**Nothing in the app was changed to produce this document.** It is a read-only inventory.

---

## The finding

The website and the app do not use the same orange, and the app is not internally consistent either.

| Colour | Where it lives | Status |
|---|---|---|
| `#F59A23` | website tokens, roundel, wordmark, buttons — **and the app icon artwork** | brand-frozen "Professor Orange" (ICON-ORANGE ruling: O1 beat O2 `#FF8A00`) |
| `#FF8C42` | app UI + splash + native config | the app's live "launch orange" |
| `#EE6F1E` | app, 3 places | **on the website's RETIRED list** — see below |

`#F59A23` appears **zero times** in the app's source as a hex token. It is present in the app only as
*pixels* — the app icon PNG that was rebuilt from the frozen brand package — which is why a naive
grep suggests the brand orange is absent from the app entirely. It is not absent; it is unreferenced
by the token system. That is the real shape of the divergence: **the app's icon is one orange and the
app's interface is another.**

---

## Full inventory — every file, every occurrence

### `#FF8C42` — the app's launch orange (8 occurrences, 7 live + 1 comment)

| File | Line | Occurrence |
|---|---|---|
| `app.json` | 21 | `"backgroundColor": "#FF8C42"` — native splash |
| `app.json` | 61 | `"backgroundColor": "#FF8C42"` — second splash/config block |
| `src/theme.ts` | 42 | `ground: '#FF8C42'` — *"the launch orange — icon, native splash, Welcome"* |
| `src/theme.ts` | 21 | *(comment)* records white-on-it as 2.31:1 |
| `src/kid/kidTheme.ts` | 25 | `orange: '#FF8C42'` — **primary action** in the kid theme |
| `src/lib/splashHold.ts` | 15 | *(comment)* `splash-mark.png on #FF8C42` |
| `src/kid/Confetti.tsx` | 14 | first entry in the confetti `COLORS` array |
| `src/screens/HomeworkInputScreen.tsx` | 1126 | *(comment)* contrast note |

### `#EE6F1E` — the retired one (3 occurrences, all live)

| File | Line | Occurrence |
|---|---|---|
| `src/kid/kidTheme.ts` | 26 | `orangeDark: '#EE6F1E'` — the token itself |
| `src/screens/HomeworkInputScreen.tsx` | 1238 | `validationMsg` text colour |
| `src/screens/SessionWalkthroughScreen.tsx` | 5204 | `outroGoalFill` progress-bar fill |

---

## Measured contrast — what would actually change

Computed, not judged (same WCAG 2.1 relative-luminance method the site's
`scripts/check-brand-contrast.py` uses):

| Orange | on white | on Deep Ink `#14213D` | on cream `#FFF8ED` |
|---|---|---|---|
| app `#FF8C42` | 2.31:1 | **6.91:1** | 2.19:1 |
| app `#EE6F1E` | 3.03:1 | 5.27:1 | 2.87:1 |
| site `#F59A23` | 2.20:1 | **7.25:1** | 2.09:1 |

**Migrating `#FF8C42` → `#F59A23` would not break any contrast pair.** Deep Ink on it *improves*
6.91 → 7.25:1. Both oranges already fail white text (2.31 vs 2.20), and the app already knows this —
`theme.ts:21` states the rule outright, and its action pair is navy-fill/white-label precisely to
avoid it. So the migration is a token swap with no accessibility consequence in either direction.

Perceptually the two are close but not interchangeable: RGB `(255,140,66)` vs `(245,154,35)` —
the site orange is **less red, more yellow, and more saturated** (per-channel delta `+10, −14, +31`).
Side by side they read as two different oranges; apart, neither looks wrong.

---

## `#EE6F1E` — fix this first if anything is ever fixed

**This is the part worth doing, and it is separable from the rest.**

`#EE6F1E` is on the website's formally **retired** palette list — `scripts/check-brand-contrast.py`
fails the build if it reappears in any site page. The app still ships it in three live places. So the
two codebases currently disagree about whether this colour exists at all: the site treats its presence
as a defect; the app renders it to children.

It is also the weakest of the three on Deep Ink (5.27:1 against 7.25:1), and one of its two uses is a
**validation message** — error text, where legibility matters most.

Scope if picked up: 3 occurrences, 3 files, no native config, no splash, no icon, no store asset.
Replace `orangeDark` with a darkened step off the *frozen* orange rather than the launch one, then
re-run `node scripts/contrast.mjs` (the app's own positive-controlled contrast script).

---

## Why the full migration was declined

Rejected deliberately, not overlooked:

- `#FF8C42` is wired into **native config** (`app.json` splash ×2) and `splashHold.ts`. Changing it
  touches the native splash, which means a rebuild and a new TestFlight/store submission — not a
  CSS-level edit.
- `kidTheme.orange` is the **primary action colour of the child-facing app**. Swapping it is a live
  change to the surface children use, for a benefit no user can perceive: nobody sees the marketing
  site and the app UI in the same field of view.
- The app's own `themeTokens.test.ts` fails if a screen names its own action colour, so the token set
  is already disciplined — the divergence is between two *systems*, not a drift inside one.

---

## Status

Read-only inventory. No app file touched. Website unchanged by this document.
Revisit only if the app icon's orange and the in-app orange ever appear together in one frame
(a store screenshot, a press kit, an onboarding screen showing the icon) — that is the case where
the divergence becomes visible, and the reason to act.
