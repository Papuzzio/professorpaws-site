# Website launch log — playprofessorpaws.com

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

---

## 2026-08-27 — the approved primary logo, rescued into version control

The owner approved a **primary logo** on 2026-08-27. The only copy on the build machine was
**untracked**, inside an unrelated rollback worktree
(`~/dev/tandem-rollback-v135/assets/puppy/Puppy_logo.png`) — one `git clean -fdx` from permanent
loss, with no remote and no backup.

Committed here as `assets/professor-paws-logo.png`, and in the app repo as
`assets/brand/professor-paws-logo.png`. Byte-identical to the original in both places, verified by
hash after each copy:

```
sha256  a349e0151ff11c1fdf0370e5632c34ce590399cfed3b8f10f755a5462ba866bd
        1292 × 1218, alpha, 1,201,910 bytes
```

Provenance is recorded in the app repo's `docs/ASSET_PROVENANCE.md`. Established, not assumed: the
puppy in the logo is the **same artwork** as the app mascot (mean absolute difference 33.5/765
composited on white and squared to 256px), so the logo **inherits the mascot's AI-generated
origin** and the ownership caveat that comes with it.

**Not yet rendered anywhere.** This commit is a rescue, not the header work.

## 2026-08-27 — the approved logo in the header, and the new palette (website-only)

**Header, all eight pages.** The B horizontal lockup is replaced by the approved primary logo,
rendered from the approved source by trimming its transparent margin and resizing (LANCZOS) —
never retyped, recoloured or rebuilt in CSS. `assets/brand/professor-paws-logo-header.{webp,png}`,
180×176, WebP **16.4 KB** (the 1.2 MB master is never served). Rendered 74×72 desktop, 57×56 phones.

Three pages needed more than a swap:
- `privacy.html` and `terms.html` rendered an **emoji paw + the retyped words "Professor Paws"**.
- `support.html` had **no brand at all**.
- Both legal pages carried an off-brand **purple** accent `#6b4ea0` → `#0F7A76`.

**MEASURED CAVEAT.** The logo is a stacked badge; its wordmark is **8.8% of its height**, so at
72px the cap is **6.3px** and reads as an emblem, not as words. A legible 10px cap needs a ~114px
logo and a ~138px bar. Shipped at 72/56 as proportionate to the bar — **owner's call**, see
`BRAND_FREEZE_2026-08-27.md` §6. Incidentally this fixes the 2026-08-19 phone squeeze: the badge is
57px wide where the lockup was 150px, so the header CTA no longer competes for room, and the
"knowingly below the ≥180px B rule" exception no longer applies to anything.

**Palette.** Professor Orange `#F59A23`, Paws Teal `#14AAA3` (unchanged), Garden Green `#63A65F`
(new), Warm Cream `#FFF8ED`, Deep Ink `#14213D`, Soft White `#FFFCF7`. Website only — no app token
was touched.

**Two regressions the swap would have introduced silently, caught by measuring, not by eye:**
1. Professor Orange as a 2px ghost-button border is **2.15:1** on paper — below the 3:1 non-text
   minimum, and worse than the orange it replaced (2.96:1). Border → `--orange-deep` (4.91:1).
2. `--field-line` was `rgba(44,44,44,.42)` ≈ 3.2:1. Deep Ink is lighter than the warm grey, so the
   **same alpha fell to 2.56:1**. Re-solved to `.52` = 3.38:1.

Buttons were already compliant: white on `--teal-deep #0F7A76` = 5.17:1, exactly what the ruling
sanctions. Deep Ink on Professor Orange = 7.25:1.

**Marks NOT regenerated, deliberately.** `apple-touch-icon.png` (diff 0.3), `favicon-32.png` (10.1)
and `favicon.ico` (7.6) already derive from the shipped orange icon, not the superseded teal
(90+ each). `90f9823` did that. Regenerating would churn approved bytes for nothing.

Pinned by `scripts/check-brand-contrast.py` (token values + allowed pairs, `--selftest` positive
control). Verified in-browser: all 8 pages HTTP 200, no console errors, logo served as WebP.

## 2026-08-27 — the action colour: teal STANDS, hover fixed, and a ruling recovered from a held branch

**READ THIS BEFORE LIFTING `c1bb720`.** That commit is titled *"Site buttons back to ORANGE (owner
reversal 2026-08-20)"* and it is real — but it is **SUPERSEDED, NOT LOST**, and it must not be
cherry-picked on the assumption that a ruling went missing.

**How it got stranded.** `c1bb720` lives ONLY on `site-brand-system`, a branch held for an unrelated
reason (the brand system itself was not ready). Holding the branch held a decision that had nothing
to do with why it was held, so the 2026-08-20 reversal never reached `main` and the live site stayed
teal for a week. **A decision must never live only on a branch held for an unrelated reason.**

**Why teal stands (owner 2026-08-27).** The reversal predates the contrast work. Deep teal `#0F7A76`
carries a white label at **5.17:1**; the frozen brand teal `#14AAA3` is **2.87:1** and fails AA. Teal
is already live and working, and reversing now reopens a decision on taste that is settled on
measurement.

**AN HONEST CAVEAT, recorded because it cuts against the ruling.** That measurement compares teal to
TEAL. The orange pairing beats it either way, and the two numbers in circulation are BOTH RIGHT
because they are different swatches — record them with their source or the next reader will think one
is a mistake:
  * Deep Ink `#14213D` on **`#FF8C42`** = **6.91:1** — the orange `c1bb720` actually shipped.
  * Deep Ink `#14213D` on **`#F59A23`** = **7.25:1** — *Professor Orange*, the post-freeze `--orange`
    and the value the hero-polish brief specifies. (Lane A raised the discrepancy; recomputed here
    independently — Deep Ink luminance 0.015734, Professor Orange 0.426450.)
Against white-on-teal at 5.17:1, both beat the teal they would replace. So contrast alone does not defeat navy-on-orange;
what settles it is that teal is live, working, and one line away from being changed. A concurrent
hero-polish brief (Lane A, also dated 2026-08-27) specifies the orange pairing, so this is an OPEN
CONFLICT for the owner, not a closed one. Neither lane treated the other's brief as authority.

**THE DEFECT actually fixed (1de4d55).** `.btn` was teal and `.btn:hover` was `#9A4708`, a dark
orange: every button on all five button-bearing pages changed colour under the cursor, live for about
a week. The teal pass changed the button and not the hover. Contrast was never the issue (6.4:1) —
it was the wrong colour. Hover is now `#0C6A66` at 6.42:1.

**Lifted off `site-brand-system` WITHOUT the brand system:** the `--action` / `--action-hover` /
`--action-ink` token set, with TEAL values. The action colour is now **one line in `index.html`**
plus a `build-pages.py` regenerate. Switching to orange is
`--action:#F59A23; --action-hover:<darker>; --action-ink:#14213D;`.

**NOT lifted, and deliberately so:** the `header.top nav a` out-specifies `.btn` fix. That paints the
header CTA navy-on-navy only where the CTA sits INSIDE the nav. On `main` it is a SIBLING of `<nav>`
on all five pages, so `.top nav a` never matches it and the label is already white. Porting it would
have been a change with no defect under it. **If a future polish moves the CTA inside the nav, that
fix becomes real here.**

**The checker was blind to all of this.** `check-brand-contrast.py` matched
`background:var(--orange|--teal|--green)` literally and could not follow indirection, so
`.btn { background:var(--action) }` was invisible — proven by pointing `--action` at the failing
brand teal and watching it still print "clean". It now resolves `var()` chains and checks the action
pair at rest AND on hover, with that exact mutant in `--selftest`.

Verified live by fetching all seven pages: the token is served on all five button pages, zero orange
remains in CSS (comments excluded), `/privacy` and `/terms` have no buttons.

### CORRECTION — the inventory was SIXTEEN, not fifteen

`reset.html` carries **two** controls, not one: `a.openBtn#openApp` and `a.openBtn#openAppExpired`
(the expired-link variant). Both are correct at `rgb(15,122,118)`. Verified count:

| pages | controls |
|---|---|
| index (4) + about/how-it-works/safety/faq (2 each) | 12 `.btn` |
| `404.html` | 1 `a.home` |
| `confirm.html` | 1 `button` |
| `reset.html` | **2** `a.openBtn` |
| | **16** |

**Both were fixed** — the file was edited, not the inventory applied — so nothing shipped wrong. But
**the number 15 was SELECTOR-DERIVED, not SURFACE-DERIVED**: neither lane had `openBtn` in a class
list, and it surfaced only because a sweep returned *zero* for that page and the zero was
investigated. A slightly wider selector would have found one of the two and silently missed the
other. **Count controls by COMPUTED BACKGROUND across `a, button, input, [role=button], summary`,
filtering transparent — never by class name.** A class list can only find controls you already knew
about. (Found by Lane B; independently confirmed in-browser on the live domain.)

The same sweep also surfaces the controls rule 5 is **not** designed to see: `a.skip` (paper
background, ink label, 15.61:1) and three form inputs. All correct as designed — recorded so a green
run is never read as "all controls checked". The rule's own comment now says this.

**`--action-active` was defined and unchecked** for one commit, at `#0A5A57` / 8.04:1. It passed,
which is exactly why it was worth closing: an unchecked token that passes today is the one that
silently stops passing tomorrow. Rule 4 now checks every action state — rest, hover **and active** —
with the mutant in the selftest.

---

## STANDING LESSON — pages no build step reaches do not receive decisions

**Owner ruling, 2026-08-27.** `scripts/build-pages.py` generates `/about/`, `/how-it-works/`,
`/safety/` and `/faq/` from `index.html`. It reaches **six** of the site's eleven pages. It does not
reach:

| page | why it matters |
|---|---|
| `404.html` | the page a lost parent actually lands on |
| `confirm.html` | email-confirm — an auth flow |
| `reset.html` | password-reset — an auth flow |
| (`privacy.html`, `terms.html`, `support.html`) | standalone, but carry no controls |

**A decision applied by regenerating lands everywhere except there.** That is how the action colour
reached fifteen controls in three different colours: each new standalone page reached for whatever
literal was nearby, and no rebuild ever corrected it. It is the same shape as `c1bb720`, where a
ruling was applied on a branch nobody merged — a decision that is *implemented* but does not *land*.

**THE RULE: any site-wide ruling must name these three pages explicitly.** "Apply it site-wide and
rebuild" is not a plan; it silently excludes the auth flows and the 404.

**Two corollaries earned the same day:**

* **"In line" means wired to the same TOKEN, not painted the same colour.** `404.html` was brought
  "in line" hours earlier and still drifted, because it took `--teal-deep` rather than `--action` —
  the right colour off the wrong wire, plus a fourth hover teal nobody meant.
* **A standalone page must define a token before it uses it.** `confirm.html` and `reset.html` had no
  `:root` and not one custom property. `background:var(--action)` without a definition is an
  **invalid declaration**, which CSS drops — leaving `color:#fff` on no background: an invisible
  submit button on an auth page, failing silently. `check-brand-contrast.py` rule 6 now catches this
  statically, and rule 5 catches a control painting from a literal at all. Both carry selftest
  mutants; both were watched going red on these very files before the fix.

**And verify by computed style, never by grep.** A file mentioning `--action` says nothing about what
paints. All fifteen controls were confirmed at `rgb(15,122,118)` in a browser, on the live site.

## The hero headline is capped at 427px above 1073 — KNOWN AND ACCEPTED

**Do not re-derive this and propose growing `--maxw`. That was considered and ruled against.**

The 2026-08-27 brief asks for a 450–470px headline. Above 1073px the site gives **427 and cannot
give more**, because `--maxw` is `calc(976px + 2*gutter)` and `.wrap` then removes the gutter again
as padding — **the content box is pinned at 976 at every viewport** (measured identical at 1073,
1280, 1600 and 2560).

Growing `--maxw` reaches 460 only at ≥1164, and the case that actually hurt was a **900px viewport,
where the wrap is viewport-bound at 885 and the column was 348 whatever `--maxw` says**. So the
two-column breakpoint was raised 900 → **1073** instead: below it the hero is stacked and the
headline gets its full 460, and the spec is met at every width below 1073 rather than at 600 and 768
only.

**Full record, including the levers that would work and why each is a design change rather than a
fix: `docs/BRAND_FREEZE_2026-08-27.md` in the app repo (tandem-app), final section.** Kept there
rather than copied here — two records of one finding drift, and the stale one wins arguments it
should not.

## Screenshot frames — two rules, and they are opposites. Read before adding a capture.

**The hero frame takes ANY SHAPE. The three proof cards must be 0.750. Do not "make them
consistent".**

### The hero: `aspect-ratio: auto` — leave it alone

`.hero-shot .frame` deliberately does **not** impose a ratio. It follows whatever image it is given,
so a capture of any shape drops in and nothing is cut.

**Do not re-impose a ratio here to match the cards.** That is exactly the bug it fixes. The generic
`.frame` is 3:4 (0.750); the July hero was 915×1280 (**0.715**); `object-fit:cover` scales to width,
so it overflowed and `overflow:hidden` sliced the bottom — the card ended halfway through the line
*"Ribbon length (metres)"*. The same mechanism was cutting **33px of real content off both other
July cards** at the same time.

The hero is currently **480×337, a wide card**, and that is correct: the entry screen's content is
genuinely wider than it is tall. **Do not pad it taller to look like a device.** A short full frame
beats a tall one with dead cream in it — that is the fractions-card defect in a new costume
(49.9% of that image was empty, which is why it was replaced).

### The three proof cards: 0.750 exactly, or they get sliced

`.shots-proof` is a three-across grid, so those frames keep `aspect-ratio:3/4` — equal heights are
doing real work there. **The consequence is a rule on the assets, not on the frame: any image in a
proof card must be 0.750, or the frame will silently cut its bottom.**

If a capture is not 0.750, **PAD it to 0.750 on its own background — never crop it to fit.** Cropping
removes exactly the content the frame was already hiding: fixing the symptom by committing the crime.
`screen-times` and `screen-reading` are side-padded for this reason; every pixel of content survives.

### Checking it

Blankness is **not** the test. `screen-homework` scored 1.9% blank and was sliced mid-sentence; the
check that caught the fractions card cannot see this defect at all. The question is *does the frame's
visible area end inside content*:

```js
[...document.querySelectorAll('.hero-shot img, .shots-proof img')]
  .map(i => Math.round(i.getBoundingClientRect().height
                       - (i.closest('.frame').getBoundingClientRect().height - 18)))
// every value must be <= 0
```

**A clean run of one instrument is evidence about that instrument's question, and nothing else.**
