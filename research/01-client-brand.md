# 01 — Client Brand Extraction

## Brand Snapshot
- **Company:** Rae & Co Capital, LLC (d/b/a RcoWealth)
- **Primary Color:** `#06111f` (deep navy)
- **Secondary Color:** `#0a192b` (navy-2) / `#040b13` (near-black footer)
- **Accent Color:** `#c8a15a` (gold) with light gold `#efd8a4`
- **Neutrals:** `#fbf7ef` paper, `#f6efe3` cream, `#111927` ink, `#687386` muted
- **Fonts:** Display — refined serif (was system Baskerville stack; upgraded to **Fraunces** in V11). Body/UI — **Inter** (was Avenir Next stack).
- **Tone:** Authoritative, calm, premium, plain-spoken (no hype, compliance-aware)
- **Core Message:** "Premium advice. No office visit required." — serious, coordinated wealth management delivered 100% virtually.

## Logo
- Gold "growing leaf" mark in a circle + navy wordmark "RAE & CO / CAPITAL / WEALTH MANAGEMENT".
- Assets present in `/assets/`: `rae-co-logo-light.png` (primary, used in header/footer), `rae-co-capital-logo-transparent.png`, header/email/small variants, and phone/desk wallpapers.

## Positioning & Messaging
- **Headline:** Premium advice. No office visit required.
- **Value prop:** A focused virtual advisory relationship coordinating four disciplines so clients see how decisions affect each other before acting.
- **Differentiator:** 100% virtual + coordinated (investments + retirement income + financial planning + protection) + fiduciary RIA.

## Services (four disciplines)
1. **Investment management** — risk, allocation, liquidity, taxes, account structure.
2. **Retirement income planning** — withdrawal strategy, reserves, income sources, survivor needs.
3. **Life insurance / protection planning** — coverage tied to obligations, beneficiaries, liquidity.
4. **Financial planning** — cash flow, tax, estate, business decisions organized into action.

## Institutional Relationships
- **Custodian:** Charles Schwab (investment accounts).
- **Insurance carrier:** Mutual of Omaha.
- **Registration:** South Carolina Registered Investment Adviser.

## Contact & Conversion Infrastructure
- **Phone:** 864-558-8440 · **Email:** info@rcowealth.com
- **Lead capture:** Salesforce Web-to-Lead (OID `00Dfn00000AW6kiEAD`), returns to `thank-you.html`. Honeypot + SMS/newsletter consent + description enrichment handled in `site.js`. **Preserved unchanged in V11.**
- **Tracking:** GTM `GTM-N49D7RC`, GA4 `G-HQTS4WYCQC`, Google Ads `AW-9718091691`, Meta Pixel `1272338378394957` (`tracking-tags.js`); UTM/click-id attribution in `campaign-tracking.js`. **Preserved.**

## Site Structure (existing)
- Home (`index.html`), Services (`services.html`), Contact (`contact.html`), Client Login (`client-login.html`).
- Local SEO pages: investment-management / retirement-planning / financial-advisor / life-insurance — all `-greenville-sc.html`.
- Life-insurance funnels: `life-insurance-protection-review.html`, `life-insurance-review-checklist.html`.
- Legal: `privacy.html`, `disclosures.html`, `form-crs.html`.
- `sitemap.xml`, `robots.txt` present. Separate `mobile.html` + `mobile-redirect.js` (redirect **retired in V11** in favor of one responsive site).

## Tone Guidance for Copy
- Concrete over adjectives; never overpromise returns; always pair claims with the fiduciary/disclosure posture already in the footer.
