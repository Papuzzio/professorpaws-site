/*
  Professor Paws — account-confirmation landing on the HOMEPAGE.
  Ships at /auth-landing.js, loaded in index.html's <head> WITHOUT defer, so it runs before the page paints.

  WHY THIS EXISTS (reported 2026-09-14, reproduced on the owner's own new account)
  A new parent's "Confirm your email address" link verifies on Supabase, which then redirects to the
  project's Site URL — this homepage — carrying the outcome in the URL FRAGMENT:
      success   #access_token=…&refresh_token=…&expires_in=3600&token_type=bearer&type=signup
      failure   #error=access_denied&error_code=otp_expired&error_description=…
  The homepage read neither. A confirmed parent and a parent whose link had died (expired, or replaced by
  a newer email) saw the same marketing page with no next step, went back to the app, and found it still on
  "Check your email". And a successful confirmation left a LIVE SESSION TOKEN sitting in the address bar.

  WHAT THIS DOES — all of it:
    1. read the fragment (and, for error parameters only, the query string);
    2. if it is an account-confirmation landing, or carries any session token: REMOVE it from the address bar
       at once (history.replaceState), then hand the parent to /email-confirmed.html with a CANONICAL fragment
       rebuilt from validated parts — `#type=signup` or `#error_code=<code>` — which carries NO token;
    3. anything else (a section anchor like #faq, a ?src= flyer link) is left exactly as it was.
  No network request, no cookie, no storage, no timer. Nothing is sent anywhere; the token is never forwarded.

  WHY AUTO-NAVIGATION IS SAFE HERE, UNLIKE /reset.html. reset.html stays inert because its link is still
  single-use when the page loads. By the time this page loads, Supabase has ALREADY verified the link server-
  side; landing here consumes nothing, and the tokens are not needed — the parent signs in with their password.

  THE FRAGMENT IS ATTACKER-CONTROLLED. Only validated values are used; unknown keys are ignored. A crafted
  `/#type=signup` can at worst show someone a "confirmed" card — the app still checks the real account.
*/
(function () {
  'use strict';

  var CODE_RE = /^[a-z0-9_]{1,64}$/;
  var AUTH_QUERY_KEYS = ['error', 'error_code', 'error_description'];

  function parse(raw) {
    var out = {};
    if (!raw) { return out; }
    var parts = raw.split('&');
    for (var i = 0; i < parts.length; i++) {
      var eq = parts[i].indexOf('=');
      if (eq <= 0) { continue; }
      out[parts[i].slice(0, eq)] = parts[i].slice(eq + 1);
    }
    return out;
  }

  var hash = '';
  var search = '';
  try {
    hash = (window.location.hash || '').replace(/^#/, '');
    search = (window.location.search || '').replace(/^\?/, '');
  } catch (e) { return; }

  var h = parse(hash);
  var q = parse(search);
  var errorCode = h.error_code || h.error || q.error_code || q.error || '';
  var carriesToken = !!(h.access_token || h.refresh_token);
  var isSignup = h.type === 'signup';
  var isAuthError = !!errorCode;

  if (!carriesToken && !isSignup && !isAuthError) { return; }   // not an auth landing — leave the page alone

  // 1. Clear the address bar FIRST, before anything else can go wrong. Keep any unrelated query parameters.
  try {
    var kept = search.split('&').filter(function (p) {
      var k = p.split('=')[0];
      return p && AUTH_QUERY_KEYS.indexOf(k) === -1;
    }).join('&');
    window.history.replaceState(null, '', window.location.pathname + (kept ? '?' + kept : ''));
  } catch (e) { /* the hand-off below still carries no token */ }

  // 2. Hand off with a canonical, token-free fragment.
  var target = '/email-confirmed.html';
  if (isAuthError) {
    target += CODE_RE.test(errorCode) ? '#error_code=' + errorCode : '';
  } else if (isSignup) {
    target += '#type=signup';
  } else {
    return; // a token for some other flow: cleared from the address bar, nothing to hand off
  }
  // Hide the homepage for the instant the hand-off takes, so a parent does not see the marketing page flash
  // before their confirmation card. Only when forwarding, and undone if the hand-off itself throws.
  var root = document.documentElement;
  try { root.style.visibility = 'hidden'; } catch (e) { /* cosmetic only */ }
  try {
    window.location.replace(target);
  } catch (e) {
    try { root.style.visibility = ''; } catch (e2) { /* cosmetic only */ }
    // stay on the homepage — the token is already gone from the address bar
  }
})();
