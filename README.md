# Rae & Co Capital — Premium Virtual Wealth Website (V11)

A cinematic, scroll-animated rebuild of the RcoWealth homepage. Keeps the approved navy + gold brand and all working infrastructure (Salesforce lead form, tabs, analytics) while adding a genuinely premium, conversion-focused experience grounded in competitive research.

## What's new in V11
- **Cinematic homepage** (`index.html`): animated hero (parallax gold orbs + masked headline reveal), animated proof/stat band, institutional-partner trust strip, scroll-reveal sections, animated process timeline, and premium micro-interactions.
- **New layers:** `premium.css` (cinematic visual layer) + `premium.js` (GSAP + ScrollTrigger engine). Both load on top of the existing `styles.css` / `site.js`.
- **Loaded typography:** Fraunces (display) + Inter (UI) via Google Fonts.
- **SEO upgrades:** Open Graph + Twitter cards, canonical URL, and `FinancialService` schema (previously missing).
- **One responsive site:** the old `mobile.html` redirect is retired so every device gets the premium experience. `mobile.html` is kept as a backup.
- **Compliance-ready testimonials section:** hidden placeholder with SEC Marketing Rule disclosure slots baked in.

## Safe by design
- All animation respects `prefers-reduced-motion`.
- If GSAP fails to load or JS is disabled, **all content stays fully visible** — animation only enhances.
- The Salesforce Web-to-Lead form and all tracking are unchanged. **Form submissions create real leads.**

## ⚠️ Fill these in before launch (no placeholders should ship)
1. **Credentials strip** (in the proof section of `index.html`, marked `data-editable`): real **years advising**, **designations** (CFP®, ChFC®, Series 65), **insurance licenses/states**.
2. **Testimonials** (`#testimonials` section, currently `hidden`): replace bracketed quotes with **real** client testimonials, keep the `tm-disclosure` line truthful, then remove the `hidden` attribute to show the section.
3. Optional: add a fee-transparency line (research shows it's a strong trust signal) and a `404.html`.

## File map
```
index.html            # Cinematic premium homepage (rebuilt)
premium.css           # Cinematic visual layer (homepage)
premium.js            # GSAP scroll-animation engine (fail-safe)
styles.css            # Base design system (all pages)
site.js               # Tabs, form enrichment, menu (preserved)
campaign-tracking.js  # UTM / click-id attribution (preserved)
tracking-tags.js      # GTM / GA4 / Google Ads / Meta (preserved)
mobile-redirect.js    # Retired no-op (kept so old pages don't 404)
research/             # Brand, competitor, brief, audit, niche-analysis deliverables
  ├── 01-client-brand.md
  ├── 02-competitor-analysis.md
  ├── 03-build-brief.md
  ├── 04-quality-audit.md
  └── niche-analysis-report.md
... (services, contact, SEO pages, legal pages — unchanged)
```

## Local preview
```bash
python3 -m http.server 8080
# open http://localhost:8080/
```

## Deploy (static — Netlify / Vercel / Cloudflare Pages / GitHub Pages)
The site is fully static. Any static host works.
- **Netlify:** drag the folder into the dashboard, or connect the repo (build command: none; publish directory: `/`).
- **Vercel:** `vercel` from the project root (framework preset: Other).
- Ensure the domain `rcowealth.com` points to the host; the Salesforce `retURL` and canonical assume that domain.

## Cost note
Built with free, open tooling (vanilla HTML/CSS/JS + GSAP via CDN + Google Fonts). No license or subscription required to run.
