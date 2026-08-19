# Homepage simplification — section-by-section spec (OWNER-RULED 2026-08-19; implementation plan below)

Status: RULINGS A–E RECEIVED AND FOLDED IN. Implementation on ONE branch, NO intermediate production deploys; ONE deploy after owner review. Written from the owner's
critique of 2026-08-19 ("radical simplification pass, not another redesign"; "delete sections, don't keep adding
better-designed sections"; "implement from a precise section-by-section spec").

KEPT (not touched by this pass): cream ground + orange action accent · Fraunces headings · the approved B/D/A
lockups + favicon · current nav styling · restrained borders · rounded CTA · the three REAL product screenshots
(`1/2 = ?/8` fractions proof, times array, reading) · the typed-input hero screenshot (`426 × 38`) · the
site-event first-party counter · privacy/terms/support pages · the claims discipline (nothing unsupported).

Target journey: Promise → Wow, show me → Okay, this is different → I understand how it works → I trust this → Sign me up.
Target length: ~half of today's page; SIX major sections + footer.

---

## 1. HERO — promise + much bigger product
- H1 (**RULING A — APPROVED**: overrides the 2026-08-12 headline hold; the emotionally specific frustration language
  moves lower on the page / to secondary pages, never the first brand impression):
  > **Homework help that teaches.**
  > **Not just answers.**
- Sub (one sentence): *Professor Paws turns schoolwork into calm, step-by-step learning that keeps your child doing the thinking.*
- Primary CTA: **Request Free Beta Access** → `#beta`
- Tiny trust line: *Ages 8–13 · No ads · Parent-controlled*
- Product: the SAME typed-input screenshot, **~half the hero width on desktop** (≈ 480–520 px display vs 300 today);
  on phones it stacks under the copy at full content width. Layout/scale change only — no new or restaged image.
- Removed from the hero: the free-beta line (moves to the final CTA), the long trust sentence (moves to Trust).
- SEO: `<title>`/description keep "homework help"; H1 keeps the head term "Homework help". The old H1's intent
  ("kids who shut down…") is served by the FAQ/`/homework-help` page (section 7).

## 2. PRODUCT PROOF — "See it work" (the visual centrepiece)
- H2: **They don't just watch. They do.**
- The three real screenshots, larger (≈ 300–340 px each on desktop, 3-up ≥ 744 px, 1-up stacked on phones), captions only:
  - *Fractions they can move*
  - *Math they can build*
  - *Reading one step at a time*
- No bullets, no paragraph. Alt text stays descriptive (SEO + a11y).

## 3. DIFFERENTIATION — one concise comparison
- H2: **More than an answer box.** (kept)
- Table cut from five rows to three:
  | Typical homework AI | Professor Paws |
  |---|---|
  | Gives the answer | Teaches the next step |
  | Starts with a blank chat | Starts with guided learning |
  | Child watches | Child moves, builds & answers |

## 4. HOW IT WORKS — three steps only
Merges today's: "When a ten-minute worksheet…", "What changes at homework time", "From schoolwork to a calmer plan",
the three schoolwork subject cards.
- H2: **Real schoolwork. A calmer way through it.**
- 1. **Add the work** — *Type or paste what school assigned.* (photo stays "coming soon" ONLY if mentioned; default: not mentioned)
- 2. **Work one step at a time** — *Professor Paws uses visual, spoken and interactive guidance.*
- 3. **See where help was needed** — *Parents can see what was practiced and where support helped.*
- One subject line beneath: *Math · Reading · Spelling · Fractions · Multiplication · Money · Time* (claims-safe: all shipped strands)
- No subject cards.

## 5. TRUST — one compact premium section
Merges: "Encouragement without pressure", "Who it's for", Safety checklist, the learning-difference line, founder credibility.
- H2: **Built for learning. Designed for families.**
- Four points (verbatim from the owner's brief):
  - **No answer machine** — *Guidance gets smaller when your child gets stuck.*
  - **No pressure mechanics** — *No streaks, timers or leaderboards.*
  - **Parent-controlled** — *No open-ended child chat or social features.*
  - **Privacy taken seriously** — *No ads. No third-party ad tracking. Children's data isn't sold or used to train AI.*
- Founder line beneath (one sentence): *Built by an application security engineer after watching a child he loves struggle with homework.*
- **RULING B — the explicit ADHD/autism/dyslexia line comes OFF the homepage.** Homepage uses only:
  *Designed with different ways of learning in mind.* (one short line under the four trust points). The detailed,
  carefully qualified learning-difference explanation ("Designed with ADHD, autism, and dyslexia in mind: one step at a
  time, no timers, and no penalty for a wrong answer" + the design principles behind it) moves to `/how-it-works`
  and the FAQ. No diagnosis, treatment, or outcome claims anywhere.
- Links: *Privacy Policy · Terms · Safety* (the full safety checklist moves to `/safety`).

## 6. FAQ + one frictionless conversion
- H2: **Questions parents ask** — SIX questions max on the homepage (proposed: Does it give the answer? · Is it an AI
  tutor? · What data do you collect? · What ages and subjects? · Is a diagnosis required? · What device, what cost?).
  The remaining two (purchases; replaces school/tutoring) move to `/faq`.
- Final CTA H2: **Make homework feel possible again.**
- **RULING C — email-first conversion, APPROVED.** Initial form = parent email + **Request Free Beta Access**.
  After success: *"You're on the list. Want to help us find the right beta families?"* → OPTIONAL second step
  (country, age range, homework note with the no-name/no-diagnosis microcopy) posted as a second Formspree
  submission keyed by the same email; the initial conversion never depends on it. One sentence under the button:
  *We review requests and email beta access when the iPad app is ready to test.* Analytics: `beta_form_submitted`
  stays a bare count — no email, no free text, ever.
- Footer unchanged (A wordmark, Privacy · Terms · Support · email, founder line).

---

## DELETED from the homepage (removed or relocated — not hidden)
| Today | Fate |
|---|---|
| Full founder story (5 paragraphs + CTA) | → new `/about` ("Why I built Professor Paws"), verbatim copy; homepage keeps the one-line founder credit |
| "When a ten-minute worksheet turns into an hour…" | deleted (redundant with Hero + How it works) |
| "What changes at homework time" (4 cards) | deleted (redundant) |
| "From schoolwork to a calmer plan" (3 steps) | absorbed into §4 |
| 3-column schoolwork cards | absorbed into §4's subject line |
| "Encouragement without pressure" grid | absorbed into Trust ("No pressure mechanics") |
| Learning progression (Objects → Pictures → Numbers → On their own) | → `/how-it-works` (expandable detail) |
| "Who Professor Paws is for" cards | → `/how-it-works` + FAQ |
| Giant Safety checklist | → `/safety`; homepage keeps the Trust summary |
| "What happens next" 4-step box | → one sentence under the form |
| FAQ items 7–8 | → `/faq` |

## NEW secondary pages — RULING D APPROVED (genuine parent value; depth moves OFF the homepage)
- NOT all four go into the primary nav: top nav stays restrained — *How it works · Safety · FAQ* + the CTA; `/about`
  is linked from the founder line and the footer. No additional thin SEO landing pages in this pass
  (`/homework-help`, `/math-help`, `/reading-help` are NOT built now).
- `/about` — the founder story (verbatim, non-identifying).
- `/how-it-works` — the 3 steps + learning progression + who it's for + the photo-homework status line.
- `/safety` — the full checklist + privacy summary + links to policy/terms.
- `/faq` — all questions (homepage shows six).
- Later, content pages only when real: `/homework-help`, `/math-help`, `/reading-help`.
- Each page: canonical, description, OG, `<main>`, the site-event page_view beacon (page enum extended), sitemap entries.
  Crawlable copy moves, it does not disappear — SEO territory is preserved and deepened.

## Visual rhythm rules for the build
More breathing room between the six sections · fewer cards/border boxes · product imagery much larger · shorter
headlines and body · alternate visual → text → visual → text · ONE primary CTA repeated logically (hero, after
proof/compare, final) · left-align explanatory prose where possible · slightly stronger background contrast between
sections (cream / paper / tint alternation already in the token set).

## Guard-rails (from the standing rulings)
Real product proof only (no restaging) · photo homework stays unclaimed/“coming soon” · no unsupported absolutes ·
ADHD line per Decision B · frozen lockups unchanged · claims matrix re-run on the new copy before deploy ·
accessibility checks re-run (landmarks, contrast, focus, form) · screenshot diff 375/768/1280 · per-step commits ·
deploy on the owner's word.

## OWNER RULINGS (2026-08-19) — all received
A. H1 replaced — APPROVED. B. ADHD/autism/dyslexia line OFF the homepage; "different ways of learning" only; detail
to /how-it-works + FAQ. C. Email-first form + optional second step — APPROVED. D. /about, /how-it-works, /safety,
/faq — APPROVED; restrained nav; no thin landing pages. E. ONE branch, scoped commits, NO intermediate deploys; QA;
owner review; ONE production deploy.

## IMPLEMENTATION PLAN (the order the work will follow — one branch `homepage-simplification`)
1. **Hero** — new H1/sub/CTA/trust line; product image at ~half the desktop hero width (same screenshot). Commit.
2. **Product proof** — "They don't just watch. They do." + three larger screenshots with three captions. Commit.
3. **Differentiation** — comparison table cut to the three rows. Commit.
4. **How it works** — merged three steps + subject line; delete the four redundant sections/cards. Commit.
5. **Trust** — four points + "different ways of learning" line + one-line founder credit + links. Delete the
   encouragement grid, who-for cards, the safety checklist, the learning-progression strip from the homepage. Commit.
6. **FAQ (six) + email-first form** with the optional second step and the one-sentence follow-up; "What happens
   next" box removed. Commit.
7. **Secondary pages** — `/about` (founder story verbatim), `/how-it-works` (3 steps, learning progression, who
   it's for, the qualified learning-difference explanation, photo status), `/safety` (full checklist + privacy
   summary), `/faq` (all eight+). Each: cream/orange site tokens, the B header, canonical, description, OG,
   `<main>`, page_view beacon (enum extended server-side in a follow-up function deploy), sitemap entries. Nav:
   How it works · Safety · FAQ. Commit(s).
8. **Checks** — claims matrix re-run on every new/moved line; SEO (title/description/H1/H2 per page, sitemap,
   canonicals, internal links); accessibility (landmarks, contrast, focus, labels, the two-step form's live
   region/focus); performance (no new third parties; hero image size budget); responsive 375/390/430/768/1280
   + header measurement; site-event beacon test (page_view per new page, form events). Commit fixes.
9. **Preview QA** — full-page renders of every page at 375/768/1280 + a before/after sheet vs live → owner review.
10. **ONE deploy** after approval: fast-forward main, push, live-vs-branch byte compare, launch-log entry.
