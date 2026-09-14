/*
  Professor Paws — account-confirmation landing page, fragment reader.
  Ships at /email-confirmed.js, loaded by /email-confirmed.html with <script src="/email-confirmed.js" defer>.

  Reached two ways, both handled identically:
    • from the homepage (auth-landing.js), with a canonical token-free fragment: #type=signup or #error_code=…
    • directly, once the app's confirmation emails point here, with Supabase's own fragment:
      #access_token=…&refresh_token=…&type=signup   or   #error=…&error_code=…&error_description=…

  WHAT THIS DOES: read the fragment -> REMOVE it from the address bar (the tokens are never needed: the parent
  signs in with their password) -> reveal the matching card. No network request, no cookie, no storage, no timer.

  FAIL CLOSED, KINDLY. The default card is the GENERIC one ("open the app and sign in"), true in every case.
  That is also what a refresh shows after the fragment has been cleared — deliberately: keeping the outcome
  would mean keeping the tokens.

  THE FRAGMENT IS ATTACKER-CONTROLLED: only a validated error code or the literal type=signup is acted on,
  and nothing from the URL is ever written into the page.
*/
(function () {
  'use strict';

  var CODE_RE = /^[a-z0-9_]{1,64}$/;

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

  var h = {};
  var q = {};
  try {
    h = parse((window.location.hash || '').replace(/^#/, ''));
    q = parse((window.location.search || '').replace(/^\?/, ''));
  } catch (e) { return; }

  // Clear the address bar before anything else, whatever the outcome.
  try {
    if (window.location.hash || q.error || q.error_code) {
      window.history.replaceState(null, '', window.location.pathname);
    }
  } catch (e) { /* nothing below depends on it */ }

  var generic = document.getElementById('genericState');
  var confirmed = document.getElementById('confirmedState');
  var expired = document.getElementById('expiredState');
  if (!generic || !confirmed || !expired) { return; }

  var errorCode = h.error_code || h.error || q.error_code || q.error || '';
  if (errorCode && CODE_RE.test(errorCode)) {
    generic.hidden = true;
    expired.hidden = false;
    return;
  }
  if (h.type === 'signup') {
    generic.hidden = true;
    confirmed.hidden = false;
  }
  // Anything else: the generic card stays.
})();
