# 03 — Website Build Brief (V11 "Premium Cinematic")

Master document driving the homepage rebuild. Combines the brand extraction (`01`) and competitor analysis (`02`).

## Strategic Thesis
Competitor analysis found the leaders (Facet, Empower, Domain Money) win on **content depth + quantified social proof + fee transparency** — *not* visual flash — and that **no major competitor owns the "premium serif, navy-and-gold, boutique-luxury" aesthetic.** That lane is open. Rae & Co's edge = **the human, fiduciary, coordinated relationship delivered 100% virtually**, dressed in a genuinely premium visual language no competitor has.

## Design Direction
- **Palette:** Keep navy `#06111f` + gold `#c8a15a` (refined). Add depth via animated gold orbs, gold-line reveals, dark/light section rhythm.
- **Typography:** **Fraunces** (luxury optical serif) for display + **Inter** for UI. High-contrast serif headlines = the "private-office luxury" cue competitors lack.
- **Imagery:** No stock-handshake clichés. Abstract premium (light, grain, glass) + the "virtual office" glass card motif. Slot left for a future 3D/scroll asset if desired.
- **Motion (cinematic but restrained):** masked headline line-reveal, parallax orbs + floating cards, scroll-reveal sections, count-up stats, a gold process line that draws on scroll, magnetic buttons, scroll-progress bar. All behind `prefers-reduced-motion` and fail-safe (content never hidden if JS fails).
- **Avoid:** tech-startup coldness (Savvy/Wealthfront), corporate stiffness (Mercer), decorative motion, opacity about the model.

## Site Architecture (homepage flow)
1. Sticky header (condenses on scroll) + scroll-progress bar.
2. **Hero** — flag, eyebrow, masked H1, lead, dual CTA, trust pills, glass "virtual office" card, scroll cue.
3. **Proof band** — count-up stats (100% virtual · 4 disciplines · 2 institutional partners · Fiduciary) + editable credentials strip.
4. **Partner strip** — Schwab · Mutual of Omaha · SC RIA · secured intake (typographic trust lockup).
5. **Virtual by design** — 4 cards.
6. **Four disciplines** — clickable cards → Planning Areas.
7. **Planning Areas** — interactive tabs (existing deep content preserved).
8. **Who it serves** — persona cards (self-qualifying).
9. **How it works** — animated 4-step process with drawing gold line.
10. **Client access** — Schwab / Mutual of Omaha portals.
11. **Testimonials** — compliance-ready placeholder (hidden until real quotes added).
12. **Contact** — Salesforce lead form (preserved) + phone/email.
13. Footer (services / firm / legal).

## CTA Strategy
- **Primary (repeated, consultative):** "Start a virtual conversation" / "Virtual intro" / "Request a Virtual Follow-Up" → the Salesforce form. Per research, consultative > "Contact Us." (Consider standardizing to **"Book Your Intro Call"** if a scheduler is added.)
- **Secondary:** "See how virtual works" (educational scroll).

## Content Framework
- **Headline (kept):** "Premium advice. No office visit required." (A/B ideas: "Serious wealth management, run entirely online." / "Your whole financial picture — coordinated, virtually." / "A private wealth office that comes to you.")
- **Value structure:** problem (decisions affect each other) → coordinated four-discipline view → virtual delivery → fiduciary trust.
- **Quantify where truthful** (research pattern #2): the proof band uses honest counts; firm-specific performance numbers intentionally avoided per SEC Marketing Rule.

## Conversion / Trust Playbook
- Goal: virtual intro requests via the Salesforce form.
- Trust stack: custodian (Schwab) + carrier (Mutual of Omaha) + SC RIA registration + (to add) years + CFP®/designations + real testimonials with baked-in disclosures.
- Security reassurance retained ("never send credentials/SSNs via the form").

## What the owner must supply (no fabrication policy)
- **Years advising** (the count for the credentials strip).
- **Designations / licenses** (CFP®, ChFC®, Series 65, insurance + states).
- **Real client testimonials** (then unhide the testimonials section).
- Optional: fee model line if they want fee-transparency as a trust weapon (research pattern #1).

## SEO Targets (from `02`)
Own the **virtual + fiduciary + retirement-income** intersection nationwide, plus Greenville/Upstate local terms. Added in V11: Open Graph + Twitter cards, canonical, `FinancialService` JSON-LD.
