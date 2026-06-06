# 04 — Quality Audit (V11)

Audited the rebuilt homepage (`index.html` + `premium.css` + `premium.js`). Static verification (no browser/Lighthouse available in this environment — those checks are marked "verify on deploy").

## SEO
- [x] Unique, descriptive `<title>` + meta description
- [x] Canonical URL added (`https://rcowealth.com/`)
- [x] Open Graph + Twitter Card tags added (were missing)
- [x] One `<h1>` per page (verified: exactly 1); logical H2/H3 hierarchy
- [x] `FinancialService` JSON-LD schema added (name, telephone, email, services, areaServed)
- [x] `robots.txt` + `sitemap.xml` present (unchanged)
- [x] Alt text on all images (logo images)
- [ ] (Verify on deploy) Validate schema in Google Rich Results Test

## Accessibility
- [x] Skip-to-content link
- [x] Semantic landmarks (`header`/`main`/`footer`/`section`/`nav`)
- [x] `prefers-reduced-motion` fully respected (no `.anim` class added; CSS also force-shows content; JS skips choreography)
- [x] Keyboard-operable interactive cards (`tabindex="0"` + Enter/Space handlers in `site.js`); visible focus styles retained from `styles.css`
- [x] ARIA: `aria-expanded` menu, `aria-live` tab panel, decorative layers `aria-hidden`
- [ ] (Verify on deploy) Color-contrast spot-check of gold-on-navy small text (WCAG AA) — primary body text uses high-contrast values; muted gold captions are large/secondary

## Performance
- [x] Animations are transform/opacity only (compositor-friendly); `will-change` hints set
- [x] GSAP + ScrollTrigger loaded `defer` (non-render-blocking); site fully functional without them
- [x] No layout shift from reveals (elements occupy final space; only opacity/transform animate)
- [x] Images have explicit `width`/`height` to reserve space
- [x] Fonts loaded with `display=swap` + preconnect
- [ ] (Verify on deploy) Lighthouse 90+ pass; consider self-hosting GSAP + subsetting fonts if needed

## Fail-safe / robustness
- [x] If GSAP CDN is blocked → `premium.js` strips `.anim`, all content visible
- [x] If JS disabled entirely → no `.anim` class effect beyond head script; CSS only hides under `.anim`, and reduced-motion shows everything; content remains readable
- [x] Magnetic buttons only on fine pointers; no touch interference
- [x] JS syntax validated (`node --check`) for `premium.js`, `site.js`, `mobile-redirect.js`, `campaign-tracking.js`

## Lead capture / integrations (preserved)
- [x] Salesforce Web-to-Lead action, OID, retURL, hidden fields intact
- [x] Honeypot + SMS/newsletter consent + description enrichment (`site.js`) intact
- [x] GTM/GA4/Ads/Meta tracking + UTM attribution intact
- [x] Interactive Planning-Areas tabs render (hooks present: `#tabPanel`, `[data-tab]`, `[data-service]`)

## Client-ready checklist
- [x] All editable placeholders clearly marked (credentials strip, testimonials section `hidden` with EDIT notes)
- [x] Forms point to a real endpoint (Salesforce) and `thank-you.html` exists
- [x] Favicon + apple-touch-icon set; OG image set
- [x] Mobile redirect retired → one responsive site (mobile.html kept as backup)
- [ ] 404 page — none present in repo; recommend adding `404.html` (host-dependent)
- [x] README updated with what's new, fill-ins, and deploy steps

## Recommended follow-ups (phase 2)
1. Apply the Fraunces/Inter + reveal layer to inner pages for full-site consistency.
2. Add real credentials, years, and testimonials; unhide testimonials.
3. Add a `404.html`; consider self-hosting GSAP/fonts for max Lighthouse.
4. Optional booking scheduler ("Book Your Intro Call") to complement the form.
