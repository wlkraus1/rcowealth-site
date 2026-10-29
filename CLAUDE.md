# rcowealth.com — Rae & Co Capital site

This is the ONLY live repo for rcowealth.com (git `wlkraus1/rcowealth-site` → deploys to IONOS). `~/Claude_Code/rcowealth-fintech/` is media-assets source only — never copy site code from it. (Other abandoned rcowealth experiment folders were trashed 2026-07-05.)

## Stack

Static HTML/CSS/JS, no framework, but there IS a generator: `build.py` writes 26 of the pages (everything except the redirect stubs, `your-rates.html` and the Google verification file) plus `sitemap.xml`. **Edit `build.py`, then run `python3 build.py`, then commit both.** Never hand-edit a generated page: on 2026-10-29 a rebuild silently reverted two hand-made commits (the capture-first quote flow and 39 repointed quote CTAs) and the revert went live. Page-specific inline scripts live in `PAGE_SCRIPTS` in `build.py`. `campaign-tracking.js` handles attribution (`campaigns.json` is documentation only). Deploy excludes live in `.deploy-now/rcowealth-site/config.yaml`.

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
