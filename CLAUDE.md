# rcowealth.com — Rae & Co Capital site

This is the ONLY live repo for rcowealth.com (git `wlkraus1/rcowealth-site` → deploys to IONOS). `~/Claude_Code/rcowealth-fintech/` is media-assets source only — never copy site code from it. (Other abandoned rcowealth experiment folders were trashed 2026-07-05.)

## Stack

Static HTML/CSS/JS — no build step, no framework. Pages are standalone `.html` files (index, about, contact, disclosures, form-crs, SEO landing pages like `financial-advisor-greenville-sc.html`). `campaign-tracking.js` + `campaigns.json` handle attribution.

## Compliance (RIA — non-negotiable)

- **Never say "fee-only"** anywhere on the site. Rae & Co is RIA + insurance.
- No performance guarantees, no "you'll earn/make X", no specific investment/tax/legal advice.
- Don't touch `disclosures.html` or `form-crs.html` content without Tyler's explicit sign-off.
- Copy reads human: no em-dashes, no AI-tell phrasing, short sentences. Educator, not salesman.

## Design

- Light-led: cream body, navy + gold accents only. Never a dark theme.
- Premium/cinematic feel — this brand targets affluent pre-retirees, veterans, HNW.

## Ship rules

- Changes are live-site changes once pushed — **preview-verify locally first**, then ask Tyler before deploying anything visible.
- Surgical edits only; the 2026-06-17 cinematic revamp is the approved design baseline.
