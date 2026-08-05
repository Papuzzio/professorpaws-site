/*
  Professor Paws — password-reset hand-off, fragment reader.
  Ships at /reset.js, loaded by /reset.html with <script src="/reset.js" defer>.

  WHY THIS PAGE EXISTS (the third break in this class — see confirm.js for the first)
  Supabase's /auth/v1/verify answers a recovery link with an HTTP 303 straight to the app's custom
  scheme (professorpaws://reset-password#...). iOS mail-context browsers refuse a SERVER redirect
  into a custom scheme — no user gesture, no hand-off — and render a blank page. Proven live
  2026-08-01: the 303 and its tokens were perfect; the last hop was the whole failure. So the
  emailed link now lands HERE (an https page iOS is happy to open), and the hand-off to the app
  happens on a BUTTON TAP — a user gesture, which iOS honours.

  WHY THE FRAGMENT (same property as confirm.js, higher stakes)
  Supabase puts the session tokens in the URL FRAGMENT of its redirect. Browsers strip everything
  after "#" before issuing the request, so GitHub Pages — and any CDN in front of it — never
  receives them and cannot log them. This is not cosmetic: the fragment carries a FULL SESSION JWT.
  In a query string it would sit in a third party's access logs as an account-takeover credential.
  If anyone ever "fixes" this to a query string, that is a regression, not a cleanup.

  WHAT THIS DOES — all of it:
    read the fragment -> validate -> rebuild a CANONICAL fragment from the validated parts ->
    assign it to the open-app link's href -> swap which card is visible.
  No network request, no cookie, no storage, no timer, no auto-navigation. The page is inert until
  a human taps. A mail scanner that prefetches the page consumes nothing — and, with the fragment,
  does not even receive the tokens.

  THE FRAGMENT IS ATTACKER-CONTROLLED. Anyone can hand a parent a link with any "#" they like. Every
  part is validated against a tight alphabet and the hand-off fragment is REBUILT from the validated
  parts — never passed through raw — so nothing unvalidated can ride the scheme URL into the app.
  The app then treats the tokens exactly as it always has: they only work if Supabase minted them.
*/
(function () {
  'use strict';

  var raw = '';
  try {
    raw = window.location.hash || '';
  } catch (e) {
    return; // Leave the invalid card up. Fail closed.
  }
  if (raw.charAt(0) === '#') { raw = raw.slice(1); }
  if (!raw) { return; }

  // Tiny fragment parser — URLSearchParams exists everywhere this page supports, but staying
  // dependency-free of URL decoding keeps the accepted alphabet OURS: we split, we test, we keep
  // only what validates. Unknown keys are ignored, never forwarded.
  var parts = raw.split('&');
  var params = {};
  for (var i = 0; i < parts.length; i++) {
    var eq = parts[i].indexOf('=');
    if (eq <= 0) { continue; }
    params[parts[i].slice(0, eq)] = parts[i].slice(eq + 1);
  }

  // JWTs are base64url segments joined by dots; refresh tokens are short alphanumerics. One
  // alphabet covers both and nothing else we would ever forward.
  var TOKEN_RE = /^[A-Za-z0-9._-]{1,4096}$/;
  // Supabase error codes are snake_case identifiers (otp_expired, access_denied, ...).
  var CODE_RE = /^[a-z0-9_]{1,64}$/;

  var openLink = document.getElementById('openApp');
  var openExpired = document.getElementById('openAppExpired');
  var invalid = document.getElementById('invalidState');
  var ready = document.getElementById('readyState');
  var expired = document.getElementById('expiredState');
  if (!openLink || !openExpired || !invalid || !ready || !expired) { return; }

  // ── The expired / already-used link: Supabase redirects with error params instead of tokens.
  // The hand-off still happens (the app shows its own honest message and its "request a new
  // link" flow), but THIS page also says it plainly — the parent shouldn't need the app open
  // to learn the link is dead. The expired card's anchor ships with a static otp_expired href;
  // this refines it to the ACTUAL validated code so the app's message matches reality.
  var errorCode = params.error_code || params.error;
  if (errorCode && CODE_RE.test(errorCode)) {
    openExpired.href = 'professorpaws://reset-password#error_code=' + errorCode;
    invalid.hidden = true;
    expired.hidden = false;
    return;
  }

  // ── The good link: a full recovery token set. All three parts must validate; the hand-off
  // fragment is rebuilt from them alone (expires_* and friends are dropped — the app never
  // reads them, and the smallest forwarded surface is the safest one).
  if (params.type === 'recovery'
    && params.access_token && TOKEN_RE.test(params.access_token)
    && params.refresh_token && TOKEN_RE.test(params.refresh_token)) {
    openLink.href = 'professorpaws://reset-password#access_token=' + params.access_token
      + '&refresh_token=' + params.refresh_token + '&type=recovery';
    invalid.hidden = true;
    ready.hidden = false;
    return;
  }

  // Anything else: stay on the fail-closed invalid card.

  // NOT DONE ON PURPOSE: we do not history.replaceState() the fragment away. A refresh or a
  // restored tab must keep working for the link's one-hour life; keeping the tokens out of other
  // people's server logs was the point, not hiding them from the parent's own address bar.
})();
