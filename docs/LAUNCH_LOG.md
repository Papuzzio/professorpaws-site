# Website launch log — playprofessorpaws.com

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
