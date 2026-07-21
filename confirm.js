/*
  Professor Paws — parental consent confirmation, token reader.
  Ships at /confirm.js, loaded by /confirm.html with <script src="/confirm.js" defer>.

  WHY THIS IS A FILE AND NOT AN INLINE BLOCK
  The previous version was inline and allowed by a sha256 hash pinned in the page's CSP. That made a
  whitespace change anywhere in the block a silent, total outage: the browser blocks the script, the
  page stays on its fail-closed "this link isn't valid" card, and every parent is told their good link
  is bad — with no test, no CI, and no error anyone would see. Same-origin 'self' has no hash to drift.

  WHAT THIS DOES — all of it:
    read the URL fragment -> validate -> fill a hidden input -> swap which card is visible.
  It makes no network request, sets no cookie or storage, starts no timer, and never submits the form.
  The page stays inert until a human presses the button. Keep it that way: an email security scanner
  that prefetches the link must consume nothing.

  WHY THE FRAGMENT (this is the security property, not a style choice)
  Browsers strip everything after "#" before issuing the request. The fragment is not in the request
  line and not in any header, so GitHub Pages — and any CDN or proxy in front of it — never receives
  the token and cannot log it. With "?token=" they all logged a live 24-hour credential that grants
  consent on a child's account. If anyone ever "fixes" this back to a query string, that is a
  regression, not a cleanup.
*/
(function () {
  'use strict';

  // location.hash includes the leading "#" when present, and is "" when absent.
  // Accepted shapes, both tolerated because different mail clients rewrite links differently:
  //     #token=XXXX   (what consent-email sends)
  //     #XXXX         (bare, if something strips the key)
  var raw = '';
  try {
    raw = window.location.hash || '';
  } catch (e) {
    return; // Leave the invalid card up. Fail closed.
  }

  if (raw.charAt(0) === '#') { raw = raw.slice(1); }
  if (raw.slice(0, 6).toLowerCase() === 'token=') { raw = raw.slice(6); }

  // The fragment is ATTACKER-CONTROLLED — anyone can hand a parent a link with any "#" they like.
  // Accept ONLY our own alphabet and length. No decodeURIComponent: our tokens are alphanumeric, so a
  // well-formed link needs no decoding, and decoding first would only widen what we accept. Anything
  // that fails this test leaves the page on the invalid state, which is the correct answer for a link
  // we cannot read.
  var token = raw;
  if (!/^[A-Za-z0-9]{1,128}$/.test(token)) { return; }

  var field = document.getElementById('tokenField');
  var invalid = document.getElementById('invalidState');
  var confirmCard = document.getElementById('confirmState');
  if (!field || !invalid || !confirmCard) { return; }

  // Property assignment ONLY. Never innerHTML / insertAdjacentHTML / document.write with URL-derived
  // data. Assigning .value hands the string to the DOM as a value, so it can never be parsed as markup
  // — that is the security property, and it holds regardless of what the token contains.
  //
  // What it does NOT do, so nobody mistakes it for concealment: on <input type="hidden"> the value IDL
  // attribute is in "default" mode, which means this assignment writes through to the value CONTENT
  // attribute. Verified in-browser — outerHTML afterwards reads value="<the token>", and devtools shows
  // it plainly. The token is genuinely in the live DOM. It is kept off GitHub Pages' logs by the
  // fragment, not hidden from the page.
  field.value = token;

  invalid.hidden = true;
  confirmCard.hidden = false;

  // NOT DONE ON PURPOSE: we do not history.replaceState() the fragment away. Scrubbing it would look
  // tidier, but a refresh or a restored tab would then land the parent on the invalid card holding a
  // token they can no longer see or recover. The fragment staying in local history is the accepted
  // cost; keeping it out of other people's server logs was the point.
})();
