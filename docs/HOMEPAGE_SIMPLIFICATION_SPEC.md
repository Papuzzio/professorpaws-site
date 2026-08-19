# Homepage simplification — section-by-section spec (DRAFT for owner approval, 2026-08-19)

Status: PROPOSAL. Nothing on the live site changes until the owner approves this document. Written from the owner's
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
- H1 (replaces "Homework help for kids who shut down, rush, or melt down over schoolwork." — **DECISION A**: this
  overrides the 2026-08-12 "headline held by owner" ruling; the pain language moves lower):
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
- **DECISION B — the ADHD/autism/dyslexia line.** The owner ruled on 2026-08-19 that the homepage KEEPS "Designed with
  ADHD, autism, and dyslexia in mind: one step at a time, no timers, and no penalty for a wrong answer." This spec
  proposes it stays on the homepage as a fifth short line under the four trust points (it is how the audience finds
  us) — owner to confirm placement, or move it to `/how-it-works`.
- Links: *Privacy Policy · Terms · Safety* (the full safety checklist moves to `/safety`).

## 6. FAQ + one frictionless conversion
- H2: **Questions parents ask** — SIX questions max on the homepage (proposed: Does it give the answer? · Is it an AI
  tutor? · What data do you collect? · What ages and subjects? · Is a diagnosis required? · What device, what cost?).
  The remaining two (purchases; replaces school/tutoring) move to `/faq`.
- Final CTA H2: **Make homework feel possible again.**
- **DECISION C — email-only form.** Proposed: one field (parent email) + the button. After success:
  *"You're on the list. Want to help us find the right beta families?"* → optional second step (country, age range,
  homework note with the no-name/no-diagnosis microcopy). Operationally: the same Formspree endpoint accepts a
  second POST with the extra fields (or one POST with only email). Trade-off: the beta-fit signal arrives later and
  optionally. The success message then truly matches ("on the list"), and "What happens next" collapses to ONE
  sentence under the button: *We review requests and email beta access when the iPad app is ready to test.*
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

## NEW secondary pages (genuine parent value; deeper search intent moves OFF the homepage)
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

## OWNER DECISIONS REQUIRED
A. Replace the held H1 with "Homework help that teaches. / Not just answers." (yes/no, or alternative wording).
B. ADHD/autism/dyslexia line: homepage Trust section (proposed) or `/how-it-works`.
C. Email-only form with optional second step (yes/no).
D. New pages `/about`, `/how-it-works`, `/safety`, `/faq` — approve the set.
E. Build order: one branch, six section commits + pages, full QA, then one deploy — or staged deploys.
