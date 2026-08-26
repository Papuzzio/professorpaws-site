# Domains — observed state

**Recorded 2026-08-26.** Facts as measured on that date, from a shell on the owner's machine.
No recommendation is made or implied here.

## The live site is `playprofessorpaws.com`

- `CNAME` in this repository contains `playprofessorpaws.com`.
- `https://playprofessorpaws.com/` returns **200**.
- `https://papuzzio.github.io/professorpaws-site/` returns **301**, resolving to
  `https://playprofessorpaws.com/`.

## `professorpaws.com` is parked and is not this site

- `professorpaws.com` resolves to **192.64.119.22**.
- `https://professorpaws.com/` **times out** (curl exit 28, connection timed out after 15s).
  A control request to an unrelated host in the same session returned 200, so this is the host,
  not the network.
- `http://professorpaws.com/` returns **200** and serves a domain-parking lander: the document
  has an empty `<title>`, a `<meta name="referrer" content="origin">` whose own comment reads
  *"Send the parked domain's origin as the referrer so the market can attribute the visit to this
  domain's TLD"*, and it loads `https://lander.parity.domains/js/pa-…js`.
- `www.professorpaws.com` resolves via CNAME to **`parkingpage.namecheap.com`** and
  **`parking.d.parity.domains`**.

## How this surfaced

While confirming which git ref was published before changing the site favicons, a fetch of
`professorpaws.com` returned zero bytes. Diagnosing that — rather than assuming the site was down —
produced the above. The published ref was then confirmed against `playprofessorpaws.com` by matching
the live Terms page to the exact wording introduced by `01f10c2`.

## Commands used

```
dig +short professorpaws.com
dig +short www.professorpaws.com
curl -s -o /dev/null -w '%{http_code}' --max-time 15 -L http://professorpaws.com/
curl -sS -o /dev/null --max-time 15 https://professorpaws.com/
curl -s -o /dev/null -w '%{url_effective} (%{http_code})' -L https://papuzzio.github.io/professorpaws-site/
```
