# Website launch log — playprofessorpaws.com

## 2026-08-19 · wordmark tail REMOVED + s terminal REDRAWN (branch teal-buttons) — NOT DEPLOYED
Owner ruling: a tester read the swash tail as a SNAKE, not a dog's tail. Options were rendered at header sizes
beside the mascot head (shorten / dog geometry / remove); the owner chose REMOVE, and correctly noted that
removal alone is not the job — deleting the flourish left the s's lower arm as a blunt diagonal stub, and a
half-removed flourish reads as a rendering fault, which is worse than a snake. **So the terminal was redrawn.**

WHAT CHANGED. The lower arm no longer dives below the baseline to a point (it reached y +4.59 where the 'a'
overshoots only +1.40 and P/w sit at 0 — that depth existed only to lead into the tail). It is now cut across
its FULL stroke width (5.68 units) at x=215.6, the letter's own left sidebearing. 29 quadratic segments are
preserved.

PROVENANCE DEBT FROM THE NAVY-S PASS IS CLEARED. Full Disk Access was granted, so ~/Documents became readable
and all three assets are now RE-RENDERED FROM THE FROZEN MASTERS rather than recoloured from the approved
raster. The masters are untouched and still read-only (B sha256 6e05d33dfd96beac… unchanged, verified after).
The teal lived ONLY inside the tail group, so removing the tail removes the last teal from the wordmark — the
earlier pixel recolour is superseded, not merely re-verified.

REPRODUCIBLE: `python3 scripts/finish-wordmark.py <outdir>` derives all three from the frozen masters and
asserts its own preconditions (exactly one tail group, exactly one teal fill) and postconditions (no tail, no
teal). `node scripts/render-lockup.mjs <svg> <out.png> 374 120` rasterises the header at 2x with alpha.

APPLIED TOGETHER, as the owner required — two different marks on one page would be worse than either option:
  - assets/brand/B_primary_horizontal_lockup-374w.png / .webp  (header at every width, 748x240, 0 teal px)
  - assets/brand/A_wordmark.svg   (footer)
  - assets/brand/D_wordmark_one_line.svg
Verified after install: 0 teal pixels in both raster formats, 0 '#14AAA3' and 0 tail groups in both SVGs, and
0 teal-ish pixels in the wordmark region of the rendered page at 1280.

TWO MISTAKES MADE AND CAUGHT WHILE DRAWING THE TERMINAL, recorded because neither was catchable by a test:
  1. a naive coordinate extraction turned the s's 30 quadratic CONTROL POINTS into vertices and faceted the
     whole letter — fixed with a real path parser;
  2. clamping the outer edge flat squashed the terminal from its natural ~5.5 units to 2.13, a weak point —
     the clamp was removed. Both were visible only by rendering and looking.

## 2026-08-19 · teal action colour + all-navy wordmark S (branch teal-buttons) — BUILT, NOT DEPLOYED
Owner rulings 2026-08-19.
1. BUTTONS: orange -> teal. The BRAND teal #14AAA3 cannot be the button: white on it is 2.87:1 and FAILS AA.
   New token --teal-deep #0F7A76 is a darkened step, exactly as --orange-deep #B4530A darkens --orange #EE6F1E
   for the same reason. White on #0F7A76 = 5.17:1 vs 5.02:1 for the orange it replaces — contrast improves.
   Side effect: the teal now matches the app's own teal "My homework" bar in the hero screenshot.
2. WORDMARK S: all navy. Owner's reasoning, recorded because it supersedes the freeze rationale — the teal tail
   was kept to make the mark ownable when ORANGE was the action colour; now that TEAL is the action colour, a
   teal letterform reads as something clickable, and a brand accent that looks like a control is worse than a
   plain one. Applied to header, footer and phone lockups together: one fill value (#14AAA3 -> #14213D), which
   is exactly ONE fill in each asset against 13 navy, and trivially reversible.
   - assets/brand/A_wordmark.svg (footer) and D_wordmark_one_line.svg: one fill each, verified count == 1 first.
   - assets/brand/B_primary_horizontal_lockup-374w.{png,webp} (header, all widths incl. the 150x48 phone size):
     **PROVENANCE CAVEAT — this pair was RECOLOURED FROM THE APPROVED RASTER, not re-rendered from the frozen B
     master.** The master is unreadable from this shell (macOS TCC blocks reads of ~/Documents; `ls` works,
     `open()` does not), so a re-render was impossible. The recolour is blend-aware — every pixel on the
     navy->teal ramp collapses to the navy end keeping its own antialias offset (130 px) — and was verified at
     4x zoom with clean edges and no fringing, plus 0 teal-ish pixels remaining in both png and webp.
     TO DO when the folder is readable: re-render this pair from the untouched master and byte-compare.
   Verified: 0 teal-ish pixels in the wordmark region of the rendered page; the only teal left on the page is
   the CTA button, by design.
   TOOLING NOTE: scripts/cdp-shot.mjs reuses /tmp/cdp-<port> per width, so its DISK CACHE served the old teal
   webp and showed a phantom teal glint after the swap. Renders that verify a changed ASSET need a fresh
   profile (rm -rf /tmp/cdp-<port>) or a cache-busted asset URL — the page query string is not enough.
3. Rendered 390 and 1280; no contrast failures, no overflow. NOT DEPLOYED.

## 2026-08-19 · homepage simplification — DEPLOYED (owner-approved, main c1a25fd → 9af46bd)
Deployed in one coordinated window, in the approved order. Pre-deploy rollback points: site main `c1a25fd`
(live homepage sha256 `2cc788d6…`), site-event function **v2**, site_events CHECKs =
page {'/', '/privacy.html', '/terms.html', '/support.html'} · cta {'', 'header', 'hero', 'founder'}.
1. **Migration 20260819000002 applied ALONE** (targeted SQL through the management API, never `db push`).
   Post-state verified: page enum = the 8 values, cta enum = the 5. Ledger row `20260819000002 / site_events_pages`
   inserted. Data intact across the change: 12 rows / 71 events before AND after.
2. **site-event function deployed** from `~/dev/tandem-site-events` @ `ff3cc68` with `--use-api`.
   Read back from the API: **v2 → v3, ACTIVE, verify_jwt false**. Positive control: POSTs for `/about/`,
   `/how-it-works/`, `/safety/`, `/faq/` each stored a row; NEGATIVE control `/nope/` returned 204 and stored
   nothing (the enum still rejects). Probe rows deleted; count back to 12 / 71.
3. **main fast-forwarded** c1a25fd → 9af46bd and pushed. Pages rebuilt in ~40s.
4. **Verification on the path a user takes:**
   - homepage live sha256 == branch index.html sha256 (`09d17b30…`) — byte identical.
   - `/about/` `/how-it-works/` `/safety/` `/faq/` → **HTTP 200 and byte-identical** to the branch files.
   - **`/docs/LAUNCH_LOG.md`, `/README.md`, `/pages/about.html`, `/scripts/build-pages.py` → 404** (were 200 for
     docs/README before this deploy — owner ruling: a marketing site should not serve its engineering log,
     deployment records and file hashes).
   - No regression: `/`, `/privacy.html`, `/terms.html`, `/support.html`, `/sitemap.xml`, `/robots.txt`,
     `/assets/screen-times.webp`, `/favicon.ico` all 200.
   - **Beacon end-to-end positive control:** zero `/about/` rows before; a real headless browser loaded the LIVE
     `/about/`; a genuine `page_view` row landed (`vw=desktop, ref_host=direct, n=1`). That row is a real visit and
     was left in place.
Still open: OG image (N-4) has a retyped wordmark + the old sub-line; Search Console verification is the owner's click.

## 2026-08-19 · homepage simplification (branch homepage-simplification) — BUILT, NOT DEPLOYED (awaiting owner preview approval)
Owner rulings A–E (2026-08-19) + final guardrails. ONE branch, scoped commits 1/6 … 8, ONE deploy after approval.
1. Starting point: main @ c1a25fd (live). Secondary-page bodies in pages/*.html; generated by scripts/build-pages.py FROM index.html's
   own <style>/sprite/header/footer (identity cannot drift); generated files about/ how-it-works/ safety/ faq/ (GitHub Pages serves /slug/).
2. Homepage = SIX sections: Hero (H1 HELD — "Homework help for kids who shut down, rush, or melt down over schoolwork."; the
   owner's 2026-08-19 follow-up ruling reversed the earlier H1 change: the differentiator lives in the subhead, deliberately) · Product proof ("They don't just watch.
   They do.", three real screenshots, captions only) · Differentiation (3-row table) · How it works (3 steps + subject line) · Trust (four
   points + "Designed with different ways of learning in mind." — ruling B + one-line founder credit → /about/) · FAQ (six) + EMAIL-FIRST
   form with the OPTIONAL second step (ruling C). Page height at 1280: 4346px (live 7519px, −42%); at 375: 6272px (live ≈11,800px).
3. Deleted from the homepage (all relocated, nothing silently lost): founder story → /about/ (verbatim); "When a ten-minute worksheet…" and
   "What changes at homework time" → /how-it-works/ (the latter as a checklist); "From schoolwork to a calmer plan" → merged into §4;
   schoolwork cards, encouragement grid, learning progression, who-it's-for, the ADHD/autism/dyslexia sentence → /how-it-works/; the nine-item
   safety checklist → /safety/; FAQ 7–8 + "What does the AI actually do?" → /faq/; "What happens next" box → one sentence under the button.
4. PRODUCT-PROOF BREAKPOINT — chosen from renders, not assumed (owner guardrail 1): three-up at 744/768 rendered 205–220px frames whose in-app
   text was illegible → three-up only ≥900px (frames ≥~250px; 305px at 1280); ≤899 stacks one frame at a time at 340px. Screenshots untouched.
5. HERO PADDING — a LIVE defect found by measurement and fixed here: `section.wrap{padding-block:0}` (0,1,1) out-specified `.hero{padding-block}`
   (0,1,0), so the hero's block padding was 0 at 375/768/1280 on live (h1.top == header.bottom). Now `.hero.wrap` / `section.hero.wrap`.
   Same class of bug fixed for the desktop hero-shot cap (`.hero .hero-shot` now beats the later phone cap): product 480×671 at 1280 (was 420).
6. Header: unchanged (B lockup 187×60 ≥601 / 150×48 ≤600 per the 2026-08-19 owner exception; CTA measured unclipped at 375/390/430 on every
   page). Nav restrained to How it works · Safety · FAQ (+CTA); on secondary pages the nav targets the pages; footer nav gains About · How
   it works · Safety · FAQ.
7. BEACON: the site-event page enum widened (+/about/ /how-it-works/ /safety/ /faq/) and cta (+'page') — migration 20260819000002 + function
   mirror + enums.test.ts pin on branch site-events @ ff3cc68 in ~/dev/tandem-site-events. NOT deployed: rides only in the coordinated release
   window (owner guardrail 2). Until then the deployed function drops those page_views with 204 (by design — no error, no data).
   Analytics stay bare counts: beta_form_submitted carries no email and no free text; the optional step 2 emits no event.
8. CLAIMS MATRIX (every new or moved line; "kept" = already verified in the 2026-08-19 claims pass):
   | Line | Where | Status |
   |---|---|---|
   | Homework help for kids who shut down, rush, or melt down over schoolwork. | hero H1 | HELD headline (unchanged from live) |
   | turns schoolwork into calm, step-by-step learning that keeps your child doing the thinking | hero sub | design-intent; consistent with the no-answer + step teaching verified earlier |
   | Ages 8–13 · No ads · Parent-controlled | hero trust line | kept (all three verified) |
   | They don't just watch. They do. / Fractions they can move / Math they can build / Reading one step at a time | proof | captions describe the three REAL screenshots shown |
   | Gives the answer / Starts with a blank chat / Child watches vs Teaches the next step / Starts with guided learning / Child moves, builds & answers | compare | comparative positioning; right column verified behaviour |
   | Type or paste what school assigned. | how 1 | kept; photo NOT claimed on the homepage (FAQ + /how-it-works/ say "coming soon") |
   | Professor Paws uses visual, spoken and interactive guidance. | how 2 | owner wording; spoken steps + visual manipulatives + interactions all shipped |
   | Parents can see what was practiced and where support helped. | how 3 | kept (parent dashboard) |
   | Math · Reading · Spelling · Fractions · Multiplication · Money · Time | how subject line | every strand is a shipped lesson type (kept list in FAQ) |
   | No answer machine — Guidance gets smaller when your child gets stuck. | trust | kept ("the step gets smaller") |
   | No pressure mechanics — No streaks, timers or leaderboards. | trust | kept |
   | Parent-controlled — No open-ended child chat or social features. | trust | kept |
   | Privacy taken seriously — No ads. No third-party ad tracking. Children's data isn't sold or used to train AI. | trust | kept |
   | Designed with different ways of learning in mind. | trust | ruling B — design intent only |
   | Built by an application security engineer after watching a child he loves struggle with homework. | trust | kept (footer line, fuller form) |
   | FAQ ×6 | faq | kept verbatim; "Is it an AI tutor?" now also carries the moved AI sentence (kept) |
   | Free private beta for families of children ages 8–13. No payment required. / We review requests and email beta access when the iPad app is ready to test. | form | kept facts |
   | You're on the list. … / Want to help us find the right beta families? / Optional — a few details… | form step 2 | process copy, no product claim |
   | /about/ story | about | VERBATIM owner copy; "What that turned into" paragraph = kept claims only |
   | /how-it-works/ all lines | how-it-works | moved verbatim from the homepage (verified 2026-08-19) + the ruling-B explanation, explicitly "a design intent, not a promise… not a diagnosis tool and not a treatment… no claims about outcomes" |
   | /safety/ checklist + summary | safety | nine bullets verbatim; sub-lines restate Privacy Policy / Support facts (US servers, in-app deletion path, no chat box) |
   | /faq/ new: ADHD/autism/dyslexia design-intent; "Can I photograph the homework?" → coming soon | faq | ruling B + photo discipline |
   NOT claimed anywhere: outcomes, diagnosis, treatment, "everything spoken aloud", photo homework as shipped, testimonials.
   Secondary pages kept to ONE job each (owner, 2026-08-19): /about/ story only; /how-it-works/ three steps + progression + three
   one-line strands + photo status + qualified learning-difference explanation + fit; /safety/ checklist + privacy summary (absolutes
   tightened to "no third-party ad tracking", "no advertising in the app"); /faq/ all questions, concise answers.
9. SEO: titles/descriptions unique per page; one H1 per page; canonicals (directory URLs with trailing slash); OG/Twitter on every page
   (image unchanged — ruling N-4 later; NOTE: assets/og-image.png renders the HELD H1 — which matches the page again
   after the owner's reversal — but a retyped wordmark and the old sub-line, so the card still differs from the page's frozen lockup and
   subhead until N-4 is done; og:image:alt left truthful to the current image; flagged for the owner); sitemap.xml +4 URLs; robots unchanged; JSON-LD
   unchanged (Organization + WebSite); internal links: homepage → all four pages (How it works "More →", Trust "Read why →"/Safety, FAQ "All
   questions →", footer), pages ↔ pages. "Homework help" head term kept in <title>, description and H1 (H1 unchanged from live). Crawlable copy moved, not removed.
10. Accessibility (CDP measurements, all 5 pages × 375/390/430/768/1280 on the homepage, 375/768/1280 on the pages): no horizontal overflow;
    header/nav/main/footer ×1 (nav ×2: sections + footer); one H1; no heading-level skips; every <img> has alt; decorative SVGs aria-hidden;
    every visible form control labelled; no text under 4.5:1 (large text ≥3:1) after the .subjects size fix; tap targets ≥44px except none;
    the two-step form keeps a role=status live region in the tree before it is populated, focus lands on the message on success/error, the
    step-2 form is `hidden` until success and its heading is focusable; no reliance on colour alone.
11. Performance: no new third parties; hero image file unchanged (rendered larger, same bytes); secondary pages 35–41 KB HTML each (inline CSS
    lifted from the homepage, no extra requests beyond the shared assets); lazy-loading kept on the proof screenshots.
12. Tests: HTML tag-balance on all five pages; script syntax on all five; site-event enums.test.ts (3 pins, both sides mutation-checked red).

### Step 8/9 RESULTS (measured, 2026-08-19 — branch only, nothing deployed)
- **Homepage height by viewport (live → branch):** 375 12,063 → 6,318 (−48%) · 390 11,923 → 6,358 (−47%) · 430 11,385 → 6,202 (−46%) · 768 8,553 → 5,933 (−31%) · 1280 7,667 → 4,401 (−43%).
- **Secondary page heights:** /about/ 1,364 (375) / 1,101 (1280) · /how-it-works/ 3,463 / 2,557 · /safety/ 2,546 / 1,971 · /faq/ 1,692 / 1,552. None is a long-form landing page.
- **Accessibility (5 pages × 375/768/1280, CDP):** zero horizontal overflow · one H1 per page · zero heading-level skips · zero duplicate ids (incl. across the two forms) · zero <img> without alt · zero non-decorative svg without aria · zero unlabelled form controls · zero contrast failures (AA: 4.5:1 body / 3:1 large) · lang + skip link on every page · every standalone link row and button ≥44px. The only sub-44px targets are links INSIDE a sentence (WCAG 2.5.8 inline exception).
- **Form flow (4 scripted tests against the real page, fetch stubbed):** (T1) step 1 posts email/_subject/source only and succeeds independently; success message + focus lands on the live region; step 2 revealed, opacity 1, email carried in a hidden field; step 2 posts its own submission. (T2) step 2 submitted EMPTY sends nothing — one POST total, friendly message, still usable. (T3) a step-2 network failure leaves step 1's success message intact and offers a retry — the captured signup is never undone. (T4) an empty email posts nothing and never reveals step 2.
- **Analytics privacy:** the ONLY event the form emits is `beta_form_submitted` with `{event,page,cta,src,ref_host,vw}` — grep of the captured beacon bodies for the email address and for the free-text note: zero hits. Step 2 emits no event at all.
- **Beacon (positive control, all five pages):** page_view carries the right page value on each (`/`, `/about/`, `/how-it-works/`, `/safety/`, `/faq/`); `primary_cta_click`+`cta=header` and `privacy_opened` fire; `/about/index.html` normalises to `/about/`; with GPC on, **zero** beacons are sent.
- **Comparison table on phones:** two 167/174/194px columns at 375/390/430, rows 74px (two lines max) — readable without scroll; no horizontal overflow at any width.
- **Performance:** homepage 53.4 KB raw / **17.3 KB gzipped** (live homepage is 60.9 KB raw); secondary pages 35–39 KB raw / 11.5–12.5 KB gzipped each, and they add NO new requests (CSS/sprite/header are inlined from the homepage; fonts + brand assets are already cached). No new third parties; image bytes unchanged (the hero renders larger from the same file); proof screenshots stay lazy-loaded.
- **Build sources excluded from the published site:** `_config.yml` excludes `pages/` and `scripts/` (they would otherwise be served — verified that `docs/LAUNCH_LOG.md` and `README.md` currently return 200 on live), plus robots Disallow.
- **Adversarial review:** 6 independent reviewers (rulings, claims, a11y, concision, form, SEO) with a skeptic verifying each finding; 11 of 17 confirmed and fixed, 6 refuted and left alone. The a11y reviewer died mid-run (usage limit) and its dimension was re-run directly by measurement (results above).

## 2026-08-19 · brand-header pass (branch brand-header-2026-08-19)
1. Starting branch/commit: main @ f51e01d (the launch-audit deploy of the same day; before that, beab053).
2. Ending commit: recorded at merge.
3. Files changed: index.html (header/footer lockup swap + logo CSS), assets/brand/{B_primary_horizontal_lockup-374w.webp,.png, D_wordmark_one_line.svg, A_wordmark.svg} (new), assets/apple-touch-icon.png, assets/favicon-32.png, favicon.ico (replaced), docs/LAUNCH_LOG.md (new).
4. Reasons: owner rulings N-1(b), N-1b, N-2, N-3 of 2026-08-19 — the frozen identity on the site; one identity across tab, bookmark and App Store listing.
5. Frozen sources (READ-ONLY, never modified):
   - $B/svg_masters/B_primary_horizontal_lockup.svg — sha256 6e05d33dfd96beac98568e618dddfed1783e9e8c13137d088ec64b2fc2176c10
   - $B/svg_masters/D_wordmark_one_line.svg — sha256 b27685333d9a4a8a0818e9d8c56eef7b0c32d34d54de969f091ee3351c85b5f5
   - $B/svg_masters/A_wordmark.svg — sha256 726b9568f21f05e3f8d2540540e76d5ff0eb9a42af71f27d76b94aaa8ac490a9
   - ~/Documents/professor_paws_icon/professor_paws_icon_FINAL.png — sha256 2b0a57099e16446ded8dc8faeba495605e3a668e743bdc35919429038bdbf2f3
   ($B = ~/Documents/professor_paws_brand/APPROVED_LOCKED_2026-08-18)
6. Destinations + provenance:
   - assets/brand/D_wordmark_one_line.svg — BYTE-FOR-BYTE copy, dest sha256 b27685333d9a4a8a0818e9d8c56eef7b0c32d34d54de969f091ee3351c85b5f5 (== source)
   - assets/brand/A_wordmark.svg — BYTE-FOR-BYTE copy, dest sha256 726b9568f21f05e3f8d2540540e76d5ff0eb9a42af71f27d76b94aaa8ac490a9 (== source)
   - assets/brand/B_primary_horizontal_lockup-374w.{png,webp} — RASTER RENDERED FROM THE UNTOUCHED B MASTER at 748×240 (374×120 css @2x; headless Chrome, full viewBox, transparent bg), owner ruling N-1(b): the 933,661-byte master (embedded canonical head) would triple the page; sha256 png 8adc643239ce11401233ed4e9cd5138dcc7ad40afad69e669d13f0906edcb26b, webp 831e3efb0e95679336359df91c8a7d2136f7e1008e421a05f6029eb769badd81
   - favicon.ico / assets/favicon-32.png / assets/apple-touch-icon.png — RESIZED (LANCZOS, artwork unchanged) from the frozen App Store icon 2b0a5709…, owner ruling N-3; sha256 ico 28455dcdb558cb8bbc0b68c24c68bf432a4ad3205aff6831c0241fd073f40c67, 32 43400ec95f7acfb5b66b512c9c4d1be33563787a199df494a55167d0a82a3c41, 180 86dc1e2f22252ad8ae9f40659f3dd3187204e28d66708961a58af13ebc86122d
7. Tracking/analytics on the site: first-party site-event beacon only (aggregate counts; privacy policy §15); no third-party analytics of any kind.
8. Network destinations after this pass: playprofessorpaws.com (all assets incl. self-hosted fonts), formspree.io (beta form POST), mlokvzsjrrwlcejjonck.supabase.co (site-event beacon; confirm-page form action).
9. Claims changed: none in this pass (claims pass shipped earlier today @ 65da1b6).
10. SEO changes: none in this pass (canonical/robots/sitemap/OG/JSON-LD shipped @ 65da1b6 / 9aea9b3).
11. Accessibility: logos carry alt "Professor Paws" + aria-label on both brand links; picture has display:contents.
12. Performance: header logo 27.8 KB webp (desktop) / 33.3 KB svg (phone) replacing 8.8 KB png+text — net ≈ +20 KB first view; icon set 32 KB total (was 71 KB).
13. Tests run: HTML tag-balance on index.html; CDP full-page diff 375/768/1280 (+600 boundary) vs live f51e01d; post-deploy live-vs-branch byte comparison.
14. Build/lint: static site — n/a.
15. Responsive QA: 375 (D one-line ~205×20), 600 boundary, 768/1280 (B lockup 187×60); no horizontal overflow.
16. Deployment: fast-forward main + push per the owner's 2026-08-19 ruling (diff-before-deploy honoured).
17. OG image: unchanged (owner ruling N-4 — later).
18. Frozen brand directory: read + hashed only; never written.

## 2026-08-19 · launch-audit pass (deployed earlier today, main beab053 → f51e01d)
Ten owner rulings executed: responsive ship + tablet fixes · metadata/claims/US-English · WebP + self-hosted Fraunces (dead 'Hanken Grotesque' removed) · contrast/forms (--orange-deep buttons) · privacy §15 + processors · first-party site-event counter (fn v2 --no-verify-jwt; migration 20260819000001 applied alone, targeted). Evidence: ~/Documents/site-launch-audit-2026-08-19-evidence.md + per-step diffs in the session scratchpad.

## 2026-08-19 · header fix (branch header-fix-2026-08-19) — phone CTA clipped; mobile logo = B small
- Defect (measured with CDP, not eyeballed): at 375/390/430 the header's minimum width was 20 + 243.5 (D one-line
  wordmark at 22px tall = 225.5px wide) + 12 gap + 163.3 CTA + 20 = 458.8px > viewport; `.brand` is flex-shrink:0 and the
  CTA nowrap, so the visual viewport zoomed to 439/481px and the primary CTA rendered past the right edge
  (btn.right 438.9 on a 375 layout; `btnClipped:true` at 430).
- Options measured at 375/390/430 (screenshots: session scratchpad hdr-proto/options-sheet.png):
  - A — frozen head mark (30×28) + one-line wordmark shrunk to 15px: brand 210.8px → STILL clipped (viewport 406–448).
  - B — the B primary lockup raster at 150×48: brand 159px → CTA right edge 355/370/410, docScrollWidth == viewport, bar 72px.
- Owner ruling: OPTION B. ⚠ KNOWINGLY BELOW THE FROZEN SYSTEM'S RULE: the APPROVED_LOCKED README sets B's minimum at
  ~180px wide (below that: the one-line wordmark or the app icon). The one-line wordmark cannot share a phone bar with
  this CTA (measurement above), so B is used at 150px (20px under the guideline) ON PHONES ONLY, authorised by the
  owner on 2026-08-19 with the measurement as justification; the mascot stays visible on mobile, which the owner
  ruled is the recognition that matters there. Same raster, same bytes (derived from the untouched master
  6e05d33d…); no new variant was invented.
- Files: index.html (picture source for phones removed; .brand img.brand-logo phone size 150×48 + comment), docs/LAUNCH_LOG.md.
- QA: CDP measurements at 375/390/430 (no clip, no overflow), full-page screenshot diff 375/768/1280 vs live fd063b0, live-vs-branch byte compare after deploy.

## 2026-08-20 — Logo system, Option A (owner ruling)

The board supplies the COMPOSITION; the dog stays frozen. The board's own dog is an AI-generated
retriever with a collar and tag — a different animal from the approved mascot (sha `2b0a5709…`),
which is what build 21 ships as its App Store icon. Adopting the board's dog would have put one dog
on the website and another on the home screen. Owner ruled Option A: keep the frozen mascot, take
the navy card, the badge, the heavier PROFESSOR and the script "Paws".

**Type.** PROFESSOR is Nunito 800 (already self-hosted, already the body face). "Paws" is
Grandstander italic 800 — tested against Pacifico, Baloo 2 800 and Fredoka 600. Pacifico is the most
literally script-like but reads retro-cafe against the "premium/modern" direction; Baloo and Fredoka
are rounded but upright, so they are not script at all. Grandstander italic is bold, slanted and
rounded — the closest to the board's marker script while staying modern. SIL OFL, latin subset,
self-hosted, build-time only (the lockups ship as rasters).

**The teal dashes and the trailing paw print are OMITTED**, on the owner's instruction to keep them
only if the mark is objectively stronger with them. Rendered both ways at 126px, on a dark card, and
at 60/44/32px. It is not stronger: a single leading dash reads as a hyphen — "-Paws" looks like a
typographic error rather than a flourish — and at 32px the whole flourish collapses into noise. If
they are ever wanted, they need proper symmetric vector marks and belong only on the primary lockup,
never on the compact one.

**The badge is ringed in white only on dark grounds**, matching the board; on a light ground the
teal disc stands alone.

**Trap recorded:** headless Chrome paints an opaque page unless
`Emulation.setDefaultBackgroundColorOverride` is set to alpha 0 — the first render shipped a cream
rectangle behind every lockup, plainly visible against the header. `background:transparent` on
`html,body` is not sufficient.

**Subset trap recorded (again):** the Google Fonts `css2` response lists cyrillic-ext FIRST. Taking
the first `.woff2` URL yields a font with no Latin glyphs, and the page silently falls back to a
serif. Always select the `@font-face` block whose `unicode-range` contains `U+0000-00FF`.

