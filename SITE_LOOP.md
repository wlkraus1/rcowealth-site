# rcowealth.com — Site Loop

Queue for the website `/loop`. **Tyler: reorder, add, or delete items freely — the loop reads this file every iteration and works the topmost unchecked item.**

Each iteration does ONE smallest reviewable step, verifies it in a real browser at real viewports, and commits **to the branch**. Notes are appended to the Log at the bottom.

## Goal

Tyler's words, 2026-08-05, verbatim:

> "we need to run /loop on our live website. use against competitors and all our life insurnace is our core business and it is so hidden. with the new elements for claculator and all quoting embedded ext, there are links and al lthat need fixing. we also need a cleaner UI on the site. it is dark and boring we need pop and a focus on protection to sell life insurance as well as our wealth managmetn but life is bread and butter for right now income we can revamp later but still have financial plannign and wealth mangmetn as that is what we do and are"

So, in order of what it is for: **life insurance is the revenue engine and it is buried** — surface it. **Fix the links** the calculator and quoter work left behind. **Lighten and sharpen the UI** — it is dark and boring. **Keep financial planning and wealth management present**, because that is what the firm actually is. Benchmark against real competitors rather than taste.

## Guardrails (never break)

- **NEVER `git push`.** This repo deploys to IONOS on push — a push IS a publish to the live site. Local commits only, on a branch.
- **Never commit to `main`.** Work on `life-forward-revamp`. `main` must stay equal to `origin/main` so nothing can reach the public site by accident.
- **Every word of public copy is a DRAFT until Tyler approves it.** RIA rule, no exceptions. No performance guarantees, no "you'll earn/make X", no specific investment/tax/legal advice, and **never** describe Rae & Co as "fee-only".
- **Public copy reads human.** No em-dashes. Short sentences. Educator, not salesman.
- **Do not break lead capture.** Four Salesforce web-to-lead field ids and the honeypot must survive every edit — check them before every commit. A styling pass that silently kills the form costs real leads.
- **`campaign-tracking.js` matches on the exact `app.back9ins.com` URL.** Rerouting any of those links needs its own attribution check first, or the tracking goes quiet without erroring.
- **Verify in a browser at a real viewport, not by reading the diff.** `resize_window` with explicit `{width, height}` — the `desktop` preset leaves `innerWidth` at 0 when the pane is hidden and every measurement reads as zero.
- **Measure before queueing.** Two claims in the handoff notes were worth checking and one was wrong; see the Log.

## Queue

**Reset 2026-08-07 at Tyler's direction.** Everything above the fold has been iterated on by taste
for three days. He called it: *"we need to do real analysis on competitors, other local firms, local
agents sites, ext, to see what is working and what is not and then design this site the correct
way!"* So research comes first and design follows it. Items 1 to 4b and the old item 5/6 are in Done
and the Log; do not re-open them from here.

- [x] **R1. RESEARCH FIRST, and nothing below R1 starts until R1 has produced findings.** Tyler has
  asked for the competitor benchmark three times and no iteration has done it. It is now the gate.
  - **Cohort, three tiers, because they compete for different things.** (a) **Upstate SC RIAs and
    financial advisors** — Greenville, Greer, Simpsonville, Spartanburg, Anderson. (b) **Local
    life-insurance agents and agencies**, including the captive shops (State Farm, Northwestern
    Mutual, NYL agents in the Upstate) because those are who a protection prospect actually compares
    against. (c) **The virtual-first national RIAs** already benchmarked in June: Farther, Facet,
    Domain Money, Range, Savvy Wealth.
  - **What to bring back, per site, as data and not vibes.** Word count and longest paragraph.
    Number of pages and what the top-level nav is (this is the answer to the homepage-split
    question). What is above the fold. Whether protection/life is visible at all and where. Whether
    there is a calculator, a quoter, or online scheduling. Whether pricing is published. What trust
    device they use in place of performance numbers. Load feel and whether they animate.
  - **Use `/firecrawl-competitive-intel` and `/firecrawl-market-research`.** Both skills exist and
    are pointed at exactly this. `/firecrawl-seo-audit` for the SERP comparison on
    "financial advisor greenville sc" and "life insurance greenville sc".
  - **Output is a comparison TABLE plus a ranked list of what to change**, appended to this file as
    new queue items with measurements attached. **Not a report nobody opens** — see
    [[feedback-obsidian-never-opened]]. Push a Telegram link when it lands.
  - ⚠️ **Do not copy a competitor's copy.** Read for structure and pattern, write our own words.

- [x] **R1 — PHASE 1 DONE 2026-08-07, five sites measured. Phase 2 owed: 5+ more, and the SERP check.**
  - ⚠️ **Method note: Firecrawl was not available.** The `/firecrawl-*` skills are installed but their MCP
    tools are not loaded in the session, so every number below was taken by loading the page in a real
    browser at 1440x900 and measuring the rendered DOM — the same method used on our own pages, which
    makes the comparison like-for-like rather than skill-versus-skill.

  | Site | Type | Words | Longest para | Top nav | Calc | Quoter | Scheduling | Price |
  |---|---|---|---|---|---|---|---|---|
  | **rcowealth.com** (branch) | **ours** | **1,072** | 37 | 6 | **yes** | **yes** | **yes** | no |
  | 1st & Main Investment Advisors | local RIA | **449** | 32 | 5 | no | no | no | no |
  | Wealth Enhancement (was Fintrust) | national | 389 | 80 | 8 | no | no | no | no |
  | Strategic Benefits | local agency | 986 | 87 | 7 | no | form only | no | no |
  | The Sullivan Agency | local agency | 692 | 99 | 8 | no | no | no | no |

  - **1. We are the wordiest site in the cohort, and it is not close.** 1,072 against a 449–986 range,
    and 449 is the closest local RIA comparable. **Tyler's read was right and this is the number that
    proves it.** Target for R4: **under 600 on the homepage**, which is only reachable by moving
    sections out, not by trimming sentences. That is the same conclusion R2 reaches from a different
    direction, which is worth trusting.
  - **2. THE MOAT IS REAL AND IT IS BIGGER THAN EXPECTED. Not one competitor measured has a
    calculator, an instant quoter, or online scheduling. We have all three.** The June research said no
    local incumbent publishes pricing or offers online scheduling; that still holds, and the tooling gap
    is wider. **This should be the loudest thing on the site and it currently is not.**
  - **3. Nobody publishes pricing.** The flat fee schedule remains an uncontested position. Still
    Tyler's business call, still not re-asked.
  - **4. THE ANSWER TO THE SPLIT QUESTION, and it is unanimous.** Every site runs a **multi-page nav,
    5 to 8 top-level items, with services as their own pages**. Not one runs an eleven-block
    single-page homepage. 1st & Main is the cleanest model: Services / Advisors / Locations / Contact /
    Resources, with four service children. **R2 is confirmed by evidence, not taste. Proceed.**
  - **5. The Sullivan Agency carries "Our Carriers" as a top-level nav item.** Independent agencies
    treat the carrier list as a trust asset worth its own page, not a band. Reconsider where ours lives.
  - **6. Products.** Term and whole life are universal. **Final expense appears on Sullivan.** IUL and
    VUL appear on neither local agency measured, though Southern Insurance Group advertises
    Term/IUL/VUL/final expense in its search listing. So R3 is a genuine differentiator locally rather
    than table stakes — worth doing, and worth doing carefully.
  - **7. ZERO animation libraries across all five sites.** No GSAP, no Lottie, no AOS, no Framer.
    Motion is genuinely differentiating in this market rather than expected, which supports the
    restrained approach already shipped and argues against the heavy-animation advice Tyler was given.
  - **8. Market signal worth more than a layout note: Fintrust Capital Advisors, the largest Greenville
    independent at roughly $1.3B, now redirects to wealthenhancement.com. It has been acquired.** The
    local independents are being rolled up, which makes "actually independent, actually local, actually
    a person who answers the phone" a stronger and more defensible position than it was in June.
  - **Phase 2, still owed:** Southeast Financial Advisors (sole proprietor, the closest size match),
    Godsey & Gibb Greenville, Allen Thomas Group, Southern Insurance Group, at least one captive
    (Northwestern Mutual or NYL Greenville), plus the five virtual-first nationals from the June set,
    plus the `/firecrawl-seo-audit`-style SERP comparison on "financial advisor greenville sc" and
    "life insurance greenville sc".

- [x] **R1 — PHASE 2, 2026-08-07. ⚠️ THIS PHASE OVERTURNS PHASE 1'S MAIN CONCLUSION. Read it before acting on anything above.**

  | Site | Page height | Screens | **Fold words** | Total words |
  |---|---|---|---|---|
  | **rcowealth.com** (branch) | **10,307px** | **11.5** | **16** | 1,072 |
  | Facet | 8,090px | 9.0 | 24 | 1,492 |
  | Farther | not captured | — | 22 | 1,534 |
  | 1st & Main | 4,600px | 5.1 | 3 | 449 |

  - ❌ **Phase 1 said "target under 600 words on the homepage". That was wrong, and it was wrong
    because the comparison set was wrong.** It drew the target from local sites only. The two
    virtual-first nationals that are Tyler's actual stated north star both carry **more** words than we
    do — Facet 1,492 and Farther 1,534 against our 1,072. A word target taken from a solo local RIA
    would have made the site thinner than the firms it wants to be mistaken for.
  - ✅ **The metric that actually separates them is WORDS IN THE FIRST SCREEN, and ours is already
    fine.** Farther 22, Facet 24, ours **16**. The hero is not the problem and has not been the problem;
    three days of cutting hero copy were spent on a healthy number.
  - 🚩 **THE REAL DEFECT, and it is the one Tyler named: our homepage is the TALLEST page measured at
    11.5 screens.** Facet does a bigger job in **9.0** screens while carrying 40% more words, so its
    sections are denser and fewer. 1st & Main does it in **5.1**. We are not too wordy; **we are too
    long, and the length comes from section count, not sentence length.** Ten sections on one page.
  - **So the prescription changes. Stop cutting copy. Move sections.** That is R2, and Tyler said it
    before any of this was measured: *"its like everything is on one page."* The evidence now says he
    was right for a more precise reason than either of us had.
  - 📌 **Section heights, ours, tallest first** — this is the split shortlist:
    `#advisor` **2,288px**, `#wealth` 1,468, `#hero` 1,308, `#method` 1,061, `#contact` 1,002,
    `#clients` 664, `#client-access` 603, `#virtual` 595, `#process` 542, `strip-section` 245.
  - ⚠️ **And the biggest block on the page is the About section I built earlier today.** 2,288px, more
    than a fifth of the page, taller than the hero. It is good work in the wrong place: it belongs on
    its own page, with a short version linking to it from home. **Whoever does R2 should not treat
    recent work as protected.**
  - ✅ **Facet publishes pricing and runs a calculator.** Both nationals publish pricing. That is a
    second, independent argument for the flat-fee question — still Tyler's business call, still not
    being re-asked here, just recorded that the comparison set is one-sided.
  - **Confirmed again: zero animation libraries on Facet or Farther either.** Seven sites now, no GSAP,
    no Lottie, no AOS, no Framer Motion. The restrained CSS approach is right and the heavy-animation
    advice remains wrong for this market.
  - **Still owed in phase 3:** Farther page height, Southeast Financial Advisors, Godsey & Gibb,
    Southern Insurance Group (advertises IUL/VUL/final expense, so it is the R3 comparable), one
    captive shop, Domain Money, Range, Savvy Wealth, and the SERP comparison.

- [x] **R1 — PHASE 3, 2026-08-07. GATE CLOSED. The prescription is density and structure, not word count.**

  | Site | Words | Screens | **Words per screen** |
  |---|---|---|---|
  | **rcowealth.com** (branch) | 1,072 | **11.5** | **93** |
  | Facet | 1,492 | 9.0 | **166** |
  | Farther | 1,534 | 9.6 | **160** |
  | 1st & Main | 449 | 5.1 | 88 |

  - 🎯 **THE FINDING THE WHOLE GATE WAS FOR. Our layout is roughly HALF as dense as the two premium
    references.** They fit 160–166 words per screen; we fit 93. Farther carries 43% more words than we
    do in 1.9 fewer screens. **We are not writing too much. We are spending about twice the vertical
    space per word.** At Farther's density our existing 1,072 words would occupy **6.7 screens instead
    of 11.5, with nothing deleted.**
  - **So the three phases land here, and each one corrected the last:** phase 1 said cut words (wrong,
    drawn from the wrong cohort); phase 2 said move sections (half right); phase 3 says **tighten the
    vertical rhythm first, then move what is still too long.** Padding, section min-heights, oversized
    gaps and full-viewport blocks are the actual defect. That is also the cheapest fix and the one
    least likely to break compliance copy, because no words change.
  - ⚠️ **Note for whoever does R4: 1st & Main sits at 88 words per screen, close to ours.** Low density
    is the local norm and the premium references are the outlier. Copying local practice here is
    copying the thing that makes a site feel amateur.

  - 🚩 **SERP CHECK, and it is the worst result in this whole gate. rcowealth.com does not appear in the
    top ten for EITHER money keyword.**
    - `life insurance Greenville SC` → top ten is captive carriers (Western & Southern, Globe Life,
      New York Life, Bankers Life, Nationwide) and local independents (Life Insurance Upstate, Kendall
      & Associates, Premier Insurance Consultants, SC Insurance Brokers). **We are not on it**, despite
      shipping a dedicated `life-insurance-greenville-sc.html`.
    - `financial advisor Greenville SC` → directories (Unbiased, Indyfin, FinTRX) plus Godsey & Gibb,
      1st & Main, HB Wealth. **We are not on it either.**
    - **This reframes the whole project.** Every design decision in this loop improves the conversion
      of traffic that arrives. **Nothing in this loop creates traffic**, and the measurement says there
      is almost none arriving from search. The site polish is worth doing and is not the constraint.
      This belongs in front of Tyler as a business finding, not buried as a queue item — it is the same
      conclusion [[sf-pipeline-brief]] reached about outbound: the problem is volume at the top.

  - **Products, for R3.** Southern Insurance Group (SC, the closest product comparable) names term,
    whole, universal, **IUL and final expense** — and does **not** name VUL. Publishes an indicative
    price ("$22 to $26 per month for a healthy 35-year-old, $500,000 term"), runs an online quote path
    and promises a reply in 15 minutes. **So: final expense and IUL are normal in this market and
    Tyler should have them. VUL is absent even from the agency that advertises it in search snippets,
    which is one more reason to leave it until the Series 6/7 question is answered.**
  - **Cohort total: 8 sites measured across three tiers, plus two SERPs.** Enough to design from.
    Remaining nice-to-haves, not blockers: Godsey & Gibb, Southeast Financial Advisors, a captive shop,
    Domain Money, Savvy Wealth.

- [x] **R1 — CORRECTION, 2026-08-07, issued one iteration after phase 3. The "half as dense" finding was WRONG and the arithmetic error is worth understanding.**
  - **What happened:** ours was measured at a **1200px-tall** viewport (10,307px page) and then divided by
    **900** to get "11.5 screens". Every competitor was measured at 900 and divided by 900. Dividing a
    tall-viewport measurement by a short-viewport denominator inflated our height by about 33% and
    deflated our words-per-screen to match. **A hero with `min-height:88vh` also literally changes size
    with the viewport, so the page is not the same height at both.**
  - **Re-measured, all at 1440x900, all with `innerText`, like for like:**

  | Site | Page height | Screens | Words | **Words per screen** |
  |---|---|---|---|---|
  | **rcowealth.com** (branch) | 8,603px | **9.6** | 1,289 | **135** |
  | Facet | 8,090px | 9.0 | 1,492 | 166 |
  | Farther | 8,675px | **9.6** | 1,534 | 160 |
  | 1st & Main | 4,600px | 5.1 | 449 | 88 |

  - ❌ **"We are the tallest page measured" was false.** We are **9.6 screens, identical to Farther's
    9.6**, and 0.6 taller than Facet. We are in line with the premium references on height.
  - ❌ **"Roughly half as dense" was false.** 135 against 160–166 is a **15 to 19% gap**, not 80%. The
    modelled "6.7 screens with nothing deleted" does not survive; the honest number is around 8.4
    screens if we hit 160, i.e. **about one screen of savings**, not five.
  - ✅ **What survives.** There is still a real but modest density gap, and **the duplication is
    untouched by any of this** — `#wealth` and `#method` are the same four services twice, which is a
    fact about the DOM and not about measurement. Tyler spotted that by eye and he is still right.
  - ⚠️ **STANDING RULE, now earned the hard way: always divide page height by the SAME viewport height
    you measured it at, and measure every site in a comparison at one fixed viewport.** This is the
    fourth false reading automated measurement has produced in this loop, after the alpha compositing,
    the photograph contrast, and the stale-CSS "blank hero". **Same lesson every time: the tool is for
    finding candidates, the verdict comes from checking.**
  - 🚩 **Consequence for the plan: R2(a), the rhythm pass, is now a MINOR item, not the headline.**
    Roughly one screen is available from tightening padding. **The duplication and the split are where
    the real length is.** Reordered below.

- [x] **R2. The homepage does too much, and it repeats itself. Tyler, 2026-08-07:** *"the homepage
  feels like alot maybe we split that up ya know its like everything is on one page and some tings
  are duplicated like the services offered."*
  - **Measured and he is right.** `index.html` carries **eleven blocks**: hero, virtual strip, About,
    four-disciplines, live coverage, carriers, planning-area tabs, who-it-serves, process, client
    access, contact. **The four services appear twice on one page** — `#wealth` renders them as four
    cards and `#method` renders the same four as tabs, and the cards even link into the tabs
    (`data-service` → `data-tab`). One of the two goes.
  - **Do the split AFTER R1**, because the right page structure is the single thing the competitor
    nav survey answers directly. Likely shape, to be confirmed by the data, not by me: homepage
    becomes hero + proof + the two funnel entrances + About, with services, planning areas, process
    and who-it-serves moving to their own pages. `services.html` already exists and is thin.
  - Watch the mobile redirect: it is an allow-list now, so **any new page needs a mobile plan** or it
    ships desktop-only to most of the traffic.
  - ✅ **R1 IS CLOSED, so R2 IS UNBLOCKED. Order revised after the correction above:**
    ~~**(a) DEDUPLICATION FIRST**~~ **DONE 2026-08-07.** And it was worse than reported: **the four
    services appeared THREE times site-wide** — `#wealth` cards, `#method` tabs on the same page, and
    the same four again on `services.html` linking to four dedicated service pages that already exist.
    **`#wealth`'s cards were removed and `#method` kept**, decided by dependency rather than taste:
    nothing anywhere links to `#wealth`, while **fifteen files link to `index.html#method`** (the
    "Planning Areas" nav destination), and `#method` additionally drives `prefillForm()` in `site.js`,
    which fills the Salesforce interest and next-step fields — deleting it would have broken lead
    capture. The section itself survives because the live coverage band and carrier band sit inside it;
    it is `#coverage` now. **Result: 8,603 → 8,181px, 9.6 → 9.1 screens, "Investment management"
    appears once on the homepage instead of twice.** Tabs, prefill button, Salesforce action, oid and
    honeypot all verified intact after the cut; no console errors.
    **(b) The split — IN PROGRESS. ⚠️ SECOND CORRECTION TO THE HEIGHT NUMBERS.** Re-measured at a
    consistent 1440x900, `#advisor` is **1,090px, not the 2,288px reported earlier** — that figure was
    the same bad-viewport artifact as "11.5 screens". **There is no dominant block.** The nine
    remaining sections run 245–1,090px and cluster tightly: advisor 1,090, method 1,061, coverage
    1,056, contact 1,002, hero 792, clients 664, virtual 595, process 542, strip 245. **So the split
    cannot be driven by height. It has to be driven by purpose: which sections restate a page that
    already exists.** That test has now found two in two iterations, so use it first.
    ~~`#client-access`~~ **REMOVED 2026-08-07, 603px.** Near-verbatim duplicate of `client-login.html`,
    which exists and is linked from the nav on all 16 pages. Nothing linked to the anchor.
    ⚠️ **The credential-security sentence it carried is gone from the site verbatim** — the first
    version of the removal comment claimed it survived and that was wrong, caught by grepping instead
    of trusting the claim. `client-login.html` carries the same protection in different words, on the
    page a person about to log in actually lands on. Equivalent in substance, not identical.
    ~~virtual-model strip~~ **REMOVED 2026-08-07, 245px. THIRD duplicate, and this one duplicated a
    SECTION rather than a page**, so widen the rule: *does anything else on this page already say
    this?* Item for item — strip "Meet remotely" = `#virtual` "Access"; strip "Organize digitally" =
    `#virtual` "Workflow"; strip "Access directly" = `#virtual` "Portals". Three of three, and
    `#virtual` adds a fourth card the strip did not have. Same dependency rule decided it again:
    **16 files link to `index.html#virtual`** (the "Virtual Model" nav item) and **nothing linked to
    the strip**. Its now-unused `.strip-section` CSS is deliberately left in revamp.css — deleting
    live-looking CSS in the same commit as markup is how the iteration 6 and 7 contrast defects
    happened.
    **Still to test:** `#method` (services.html + 4 service pages already exist — but 15 files link
    to it, so it needs a nav repoint, not a delete), `#process`, `#clients`, `#advisor`.
    📊 **Split running total: 9.6 → 8.1 screens, 10 sections → 8, three duplicates removed, no copy
    rewritten and nothing lost that another page or section did not already carry.**
    Nav is still 6 items (Virtual Model, Life Insurance, Services, Planning Areas, Client Login,
    Contact) which is already inside the cohort's 5–8, so the nav does not need reshaping yet.
    ~~**(c) Vertical rhythm**~~ **DONE 2026-08-07.** 82px section padding to 60px, section-head margin
    34 to 26, and `.card{min-height:224px}` released so a four-word card stops being padded to the
    height of a forty-word one. **8.1 → 7.8 screens, 131 → 136 words per screen.** Real but modest, as
    the correction predicted; no words touched, so no compliance copy was at risk. Checked by
    screenshot as well as by number — the About section still breathes, it is not cramped.

  - ✅ **R2 IS DONE. Stopping the split here is a judgement call, and here is the evidence for it:**

  | | Words | Screens | Words/screen | Fold words |
  |---|---|---|---|---|
  | **ours, before the split** | 1,289 | 9.6 | 134 | 16 |
  | **ours, now** | **1,060** | **7.8** | **136** | 25 |
  | Facet | 1,492 | 9.0 | 166 | 24 |
  | Farther | 1,534 | 9.6 | 160 | 22 |
  | 1st & Main | 449 | 5.1 | 88 | 3 |

    **We are now shorter than both premium references and our fold sits in their band.** Cutting
    further would move us toward 1st & Main's thin local shape, which R1 phase 3 explicitly warned
    against copying. The one gap left is density, 136 against 160–166, and that is a typography and
    spacing question for R4, not more deletion.
  - ✅ **`#process` and `#clients` were TESTED AND KEPT.** The duplicate rule does not flag them: both
    appear only on `index.html` and `mobile.html`, and no other page says either. They are genuine
    homepage content, not repetition.
  - 🚩 **`#method` deliberately NOT removed, and the reasoning should survive.** The service pages do
    carry most of its panel detail, so it is largely redundant — but removing it needs a nav repoint
    across **15 files** plus preservation of `prefillForm()`, and the page is already shorter than both
    references, so the benefit is small and the risk is real. **Revisit only if R4 needs the room.** R1 phase 3 measured our layout at 93 words per screen
    against 160–166 for the premium references. Tighten section padding, kill full-viewport
    min-heights below the hero, and reduce oversized gaps. **No words change, so no compliance copy is
    at risk, and the modelled result is 11.5 screens down to about 6.7 with nothing deleted.** Measure
    words-per-screen before and after; that is the acceptance test.
    **(b) Then cut the duplication.** `#wealth` (four cards) and `#method` (same four as tabs) are the
    same content twice. Keep one. The tabs carry more detail; the cards are the better skim. Decide by
    looking, not by preference.
    **(c) Then move what is still too long.** Shortlist by measured height: `#advisor` 2,288px is the
    tallest block on the page and belongs on its own page with a short version linking to it.
    Structure the nav to match the cohort: 5–8 top-level items, services as their own pages.

- [x] **R3. Products: final expense, IUL and VUL. Tyler, 2026-08-07:** *"we need to offer final
  expense and IULs for sure VUL as well!!"* **Closed 2026-08-07** — the page shipped and expanded to
  8 sections, VUL is closed on licensing, and the one open sub-item (the site-wide sub-40px tap
  targets logged here rather than smuggled into that change) was fixed in R6(c). Box had been left
  unticked while the work underneath was complete.
  - 🚩 **This reverses two of his own standing rules**, recorded from the v2 research and the 80/20
    pivot: *final expense stays OFF the main site, separate landing pages only*, and *IUL never
    leads*. His call, and it is his business; the rules were his too, so both memory files need
    updating rather than silently contradicting the site.
  - ✅ **DONE 2026-08-07 as ONE page, not two: `types-of-life-insurance.html`, 904 words.**
    **Checked the duplicate rule first, and it passed:** across the three existing life pages, "final
    expense" appears once, and whole life, universal life and IUL appear **zero** times. The product
    menu was genuinely missing, not repeated. **One page rather than two on purpose** — two thin
    product pages is how the duplication problem this loop just spent four iterations removing gets
    recreated.
    **Order is the argument:** term, whole, universal, IUL, final expense — simplest and cheapest
    first, so a reader meets term before IUL and can tell whether they are being sold a solution or a
    product. Each type gets the same three boxes: what it solves, **what it costs you**, and **when it
    is the wrong tool**. Naming when a product is wrong is the trust device an RIA can actually use.
    **Compliance, deliberate:** the term section says plainly that term usually wins for under-50
    households *and that it pays the firm least*; the commission conflict is stated in its own block
    with a pointer to Form CRS; the IUL section says the projected columns are **not a forecast and
    not guaranteed** and tells a reader to ask for the guaranteed column and years one to ten costs.
    No performance language, no projections, no "you'll earn".
    Wired from the life-insurance hub hero, that page's footer, the homepage carrier band, and
    sitemap.xml. Verified 1440 and 390: no overflow, mobile does not redirect away, 230 words/screen.
  - **EXPANDED 2026-08-07 after Tyler: "doesnt mention variable ul or disability income any of those
    others i sent u." He was right — the first version covered 5 of the 14 product types in his
    BackNine console.** Now 8 sections, 1,305 words: term, whole, universal, IUL, **disability
    income**, **long-term care and linked-benefit hybrids**, **no-medical term / return-of-premium
    term / accidental death**, final expense.
    **Disability income was not in the console list at all** — Tyler named it separately, it sits
    under his SC Life, Accident & Health licence, and it is arguably the strongest section on the
    page because the employer-coverage gap is real and specific.
    **Annuities (MYGA, income riders) are pointed to the retirement planning page rather than covered
    here**, because they are retirement income products and this is a protection page. Putting them
    here would have started the duplication cycle again.
  - ⛔ **VUL: CLOSED 2026-08-07. Tyler: "no leave the VUL out then." DO NOT RE-RAISE IT.** Kept off the site. The reasoning, for the record: VUL is a variable product, i.e. a security, and selling or soliciting it needs a FINRA Series 6 or 7 through a broker-dealer; the firm holds Series 65 plus SC Life, Accident & Health. If Tyler ever adds that registration, the section is fifteen minutes of work.
  - ⚠️ **Two sub-40px tap targets on the new page (menu toggle 37px, breadcrumb 19px) are SITE-WIDE
    patterns inherited from the template, not introduced here.** Fixing them is a separate change
    across every page; logged, not smuggled in.
  - ⛔ **VUL IS BLOCKED, and this is a licensing question rather than a design one.** VUL is a
    **variable** product, i.e. a security. Selling or soliciting it needs a **FINRA registration
    (Series 6 or Series 7) held through a broker-dealer**. The site currently states Series 65 (IAR)
    and SC Life, Accident & Health, and **Series 65 does not permit variable products**. BackNine
    listing "Protection VUL" in the console is not evidence of a registration, the same way "All
    Carriers Enabled" was not evidence of appointment. **Do not put VUL on a public page until Tyler
    confirms an active Series 6 or 7 and the BD relationship.**

- [ ] **R4. Design. ⚠️ DIAGNOSIS CHANGED 2026-08-07 — the problem was never motion.** Tyler, third
  time: *"the site still doesnt flow or look has i imagined... things stick out things are clickable
  internactive and motion and all that."*
  - **Measured Wise, an Awwwards winner in finance, against ours:**

  | | h1 size | h1 weight | Hero background | CTAs in fold | Tool position | Animation libs |
  |---|---|---|---|---|---|---|
  | Wise | 89px | **900** | one flat saturated colour | **1** | starts before the fold ends | **0** |
  | ours | 80px | **400** | photograph + scrim | 2 | **three screens down** | 0 |

  - 🎯 **Wise runs ZERO animation libraries. That is now NINE sites measured with zero.** Tyler keeps
    asking for motion, but the sites he would call good are not moving — **they are LOUD and they put
    the interactive thing at the top.** Chasing "more motion" would have been chasing the wrong
    variable for a third time.
  - **The two real variables are TYPE WEIGHT and TOOL POSITION.** Georgia 400 over a photograph is a
    refined register; Inter 900 on flat colour is a loud one. Both are legitimate and we picked
    refined without ever asking. And the coverage slider — the one thing on this site no competitor
    has — is buried three screens down while Wise starts its currency widget above the fold.
  - ✅ **`direction-preview.html` built (noindex, unlinked, nothing wired in): the SAME real copy in
    both registers, A refined and B bold, with the coverage tool promoted to the fold in B.** Tyler
    picks one and it becomes the system for the whole site. This is the same method that settled the
    hero in one message earlier today; describing design to him has failed three times, showing him
    two versions has worked twice.
  - **Whichever he picks, promote the tool.** That part is not a taste question: it is the only
    genuinely differentiated thing on the site and it is currently below three screens of prose.

- [x] **R4. DECIDED 2026-08-07: Tyler picked A, refined.** *"A i guess"* — lukewarm, and that is
  recorded on purpose. **A is the register he has called quiet three times.** Choosing it means the
  presence has to come from somewhere other than type weight, so the two levers that remain are
  **(1) promoting the tool** and **(2) spending boldness in one place per page** rather than raising
  the volume everywhere. Do not re-open the A/B question; do not drift toward B by degrees.
  - **The design system, now fixed:** Georgia serif at 400 for display, photography leads, gold accent,
    two-button heroes allowed, restrained CSS motion only, zero animation libraries.

- [x] **R5. PROMOTE THE COVERAGE TOOL. DONE 2026-08-07 — tool now starts 991px in, 1.1 screens, first thing after the hero; was three screens down. Section order: hero, coverage, advisor, virtual, method, clients, process, contact. Carrier band travelled with it, tabs and prefill intact, 7.8 screens unchanged. Not a taste question, and it survived the A/B decision.**
  Nine sites measured, zero animation libraries, and the ones that feel alive put the interactive
  thing at the top. Our slider is the only feature no Upstate competitor has and it sits three
  screens down inside `#coverage`. Move it directly under the hero on `index.html` and keep the mobile
  order matching. Watch: `#coverage` also holds the carrier band, and `prefillForm()` must keep
  working. Verify at 1440 and 390, measure position before and after.

- [x] **R6. REVIEW PASSES — Tyler asked for "tested and reviewed multiple times", so this is a real
  queue item, not a formality.** Run each pass as its own iteration, log findings, fix, re-verify:
  - ✅ **(a) Link integrity — DONE 2026-08-07. 20 pages, 0 broken file or asset references, 0 broken
    anchors on any real page.** `#wealth` and `#client-access` have no inbound links anywhere, so the
    R2 removals left nothing dangling, and `#method` is still present for the 15 files that point at
    it. ⚠️ **The first run of the checker reported 90 broken links and every one was false** — it
    compared hrefs against the list of HTML files only, so `styles.css`, the favicons and every image
    counted as missing. Fifth false reading from automated tooling in this loop. Check the filesystem,
    not a list you built.
    🚩 **What the pass actually caught was not a link.** `hero-preview.html` and
    `direction-preview.html` are internal scaffolding and were **tracked in git, so the IONOS deploy
    would have published them** at `rcowealth.com/hero-preview.html`. Both carry noindex, so Google
    would have stayed away, but they were publicly reachable pages on a regulated firm's site showing
    half-finished design options. **Both deleted now that Tyler has chosen A**; git history retains
    them and the decisions they drove are recorded above. The published comparison Tyler is looking at
    is a separate copy outside the repo, so removing these does not break that link.
  - **(a-orig) Link integrity.** Every internal href on all 18 pages resolves; no anchor points at a
    section removed during R2 (`#wealth`, `#client-access`, the strip). 15 files still point at
    `index.html#method` — confirm it is still there.
  - ✅ **(b) Lead capture — DONE 2026-08-07. 10 forms audited, never submitted.** All 10 carry the
    same Salesforce action and the same `oid` (`00Dfn00000AW6kiEAD`), and all 10 have `oid`, `retURL`,
    `lead_source` and `company` present.
    🚩 **TWO FORMS HAD NO HONEYPOT AT ALL** — `life-insurance-calculator.html` and
    `life-insurance-protection-review.html`. Both are lead-magnet pages, and bot leads are a
    documented past problem for this org (see [[sf-web-lead-spam-defense]]). **Fixed:** the canonical
    `hp-field` markup added to both, verified present, positioned at `left:-9999px`, and
    `tabindex="-1"` so it stays unreachable by keyboard. The calculator's maths still works after the
    edit (income 95,000 gives a $1,270,000 gap). Re-audit: **zero Salesforce forms without a
    honeypot.**
  - ✅ **(b2) RESOLVED 2026-08-07, and the diagnosis above was wrong in a way worth keeping.** Both
    halves of the "contradiction" were true of different refs. **The live site was never on
    Salesforce** — `rcowealth.com` serves the Funnel action and fetches clean (0 Salesforce hits, 1
    `pi-nas.tail34488a.ts.net` hit on `/` and `/contact.html`). [[website-lead-flow]] was right.
    **This branch was the stale one:** it was cut from local `main` at `e563b41` (Aug 5), and the
    form flip `dd1bc2d` landed on `origin/main` on Aug 6, *after* the branch point. So the branch
    never had it. **Shipping this branch as-is would have silently reverted the cutover** and killed
    lead capture on cancel day — the opposite of the risk described above.
    **Fixed by merging `origin/main` (`2b69591`)**, not by hand-editing endpoints. Conflicts in
    `index.html` and `life-insurance-greenville-sc.html` were the revamp's newer copy versus the old
    copy carrying the new action; kept the revamp markup, applied the Funnel endpoint, after
    confirming `origin/main` changed nothing but `action=` in those two files.
    🚫 **`lead.php` is NOT the target and must never be wired to.** [[website-lead-flow]]: IONOS Deploy
    Now is static, **it will not run PHP** — the file sits in the repo inert (403). The real chain is
    **form → `https://pi-nas.tail34488a.ts.net/` (Tailscale Funnel) → `lead-intake.service` on
    pi-nas → queue append FIRST → FSC `/api/public/lead` → Telegram.** Endpoint confirmed live (303).
    Verified after the merge, in a real browser over `http://localhost:5187` rather than off the diff:
    all 10 forms on the Funnel action, `oid` and `retURL` present on all 10, both consent ids
    (`00NbV000003Urbb`, `00NbV000003ZxDB`) and the `website_url` honeypot (`tabindex="-1"`) intact on
    all 10. **The Salesforce field vocabulary is kept on purpose** — the Pi handler and
    `/api/public/lead` accept it as aliases, so only `action=` ever needed to change. **Never actually
    submit** — a POST creates a real lead.
  - ✅ **(c) Mobile. DONE 2026-08-07 (`c01ba5d`). 18 pages at 390 and 430.** **Overflow was already
    clean** — 0 horizontal overflow and 0 elements past the viewport on all 18, at both widths. **The
    real finding was that iteration 4's tap-target fixes only ever existed on `mobile.html`**, in that
    page's inline `<style>`, and `mobile.html` links no shared stylesheet. So the 16 pages on
    `styles.css` still had **21px footer links (12 per page), a 37px menu button and a 19px
    breadcrumb** — the fix had looked done for two days because the page it was tested on was the one
    page that had it. **A fix applied in a page-local stylesheet is not a site fix; check where the
    rule lives, not just that it works on the page in front of you.**
    Offenders per page went **13–17 → 0** on 12 of 17, with the rest exempt by category (below).
    Raised in the shared sheet: `.footer a` 21→44, `.menu-toggle` 37→44, `.breadcrumb` 19→44.
    ⚠️ **The checkbox fix half-worked and the half that failed is the instructive part.** Setting
    `width:18px;height:18px` produced **13x18** — `.checkline` is `display:flex`, so the long consent
    sentence beside it shrank the box back on the cross axis and only the height took. **`flex:none`
    is what made it 18x18.** A size set on a flex child is a suggestion until you say otherwise.
    Calculator and `mobile.html` sliders 34→44 (page-local copies, fixed in both); calculator number
    inputs 37→43 via padding rather than `min-height`, because `.sf-val` is `align-items:baseline` and
    a min-height drags the dashed "editable" underline away from the digits.
    **Exempt by category, deliberately, not overlooked:** the consent checkboxes (18x18 — the label
    wraps the text and is the real target, same logic recorded in iteration 4), inline prose links
    inside sentences (`a 170x20`, `.quote-link 193x19` — WCAG 2.5.8 exempts these and forcing 44px
    would wreck line spacing), and the honeypot.
    **Redirect allow-list correct:** `index.html` → `mobile.html` at 390; the six pages added since,
    including `types-of-life-insurance.html`, all stay put.
    **Lead capture re-verified after the CSS change** (guardrail): 8 lead forms, all on the Funnel
    action, `oid` + `retURL` + 2 consent ids + honeypot on every one. **Calculator maths re-verified
    against the documented case — income 95,000 still gives $1,270,000.**
    ⚠️ **The `?cb=` stylesheet trap caught me too, and it cost a full measurement round.** The first
    re-measure came back byte-identical to the baseline and read as "the fix did nothing". A buster on
    the HTML does not refetch the stylesheet; the numbers only moved once the `<link href>` itself was
    re-pointed. **This is the sixth false reading from automated measurement in this loop** and the
    second from this exact cause. Bust the sheet, not the page.
  - ✅ **(d) Contrast. DONE 2026-08-07. 18 pages. 4 real defects fixed, 20 false alarms rejected —
    and the checker produced a false reading AGAIN, so the warning above stands and now has a cause.**
    **The blind spot was pseudo-element backdrops.** A checker that walks ancestor `background-color`
    cannot see `.pm-card::after{position:absolute;inset:0;z-index:-1;background:linear-gradient(...)}`,
    which is how the people-media cards paint their dark panel. It read the cream section behind them
    and reported **12 failures at 1.0–1.23 on both homepages — all fake.** Adding pseudo-backdrop
    detection dropped those 12 to 0. **Anything painted by `::before`/`::after` is invisible to
    `getComputedStyle(el).backgroundColor`; a contrast checker that ignores pseudo-elements will
    condemn every scrim-backed card on the site.**
    ⚠️ **Then the fix caused its own false reading.** Busting the stylesheet (the cure for the `?cb=`
    trap in R6(c)) races the page: `life-insurance-quote.html` also pulls
    `cdn.quoteandapply.io/css/widget.css`, which cannot be fetched here, and measuring at ~180ms
    caught the nav **mid-restyle, showing browser-default link blue** `rgb(0,0,238)` — 5 fake
    failures at 1.44 that reproduce every run. A live probe of the same nav shows the correct
    `rgba(246,239,224,.78)`. **Reproducible is not the same as real.** Not fixed, because it is not
    broken.
    **The 4 real defects were all one family — a light surface carrying dark-surface styling:**
    1. `h3 "Important notes"` was **white on a white `.content-panel`, i.e. invisible, on a
       compliance disclosure block.** `.content-panel` sets `background:#fff` but never set `color`,
       so inside a dark `.section` it inherited white. `p` and `li` were already overridden, which is
       exactly why only the heading showed the bug. Fixed at the root: `.content-panel{color:var(--ink)}`.
       Now 17.61:1.
    2. `.eyebrow` "How the review works" — gold on cream, 1.31.
    3. `.lead` "The goal is to identify…" — cream on cream, 1.05, a whole paragraph unreadable.
    4. `.btn-secondary` "Use the Form" and "Talk it through on a call" — cream on white, 1.14.
    **2–4 needed no CSS at all — `.eyebrow.dark`, `.lead.dark` and `.btn-secondary.dark` already
    exist.** The markup just omitted the modifier. **The section indicts itself: "Schedule a Review"
    already carried `.dark` while its sibling "Use the Form", inside the same `<div>`, did not.**
    Someone fixed one button and missed the two beside it. Now 4.61 / 9.32 / 16.48, all screenshotted.
    ⚠️ **This is the SEVENTH occurrence of the light-surface/dark-typography family** (`.private-room`,
    `.strip-item`, `.protect-band`, the hero-wide `.btn-secondary` rule, the mobile protect-band,
    and now these). **The pattern is never "the colour is wrong" — it is "a `.dark`/`.on-light`
    modifier was omitted on one element while its siblings got it."** Grep for `btn-secondary`,
    `eyebrow` and `lead` without a modifier whenever a section changes polarity.
  - ✅ **(e) Copy and compliance. DONE 2026-08-07. Five of six checks were already clean; the sixth
    was on 2 pages out of 10.**
    **Clean, verified rather than assumed:** em-dashes **zero** across all HTML (and none introduced —
    re-checked after the edit); **"fee-only" absent**; **VUL absent**, matching Tyler's "no leave the
    VUL out then"; **no performance language** — the only two `guarantee` hits are the MYGA product
    name and the IUL disclaimer *"not a forecast and are not guaranteed"*, i.e. compliance text doing
    its job; **TCPA consent, form disclaimer and credential warning present on all 10 form pages.**
    🚩 **The gap: the fiduciary/compensation disclosure existed on `index.html` and `mobile.html` only.
    The other 8 lead-capture pages had none** — no fiduciary-standard statement, no compensation and
    conflicts language, no pointer to Form CRS or disclosures. **Every one of those 8 pages asks a
    prospect for their contact details.** The homepage set the framing and the pages that actually
    capture the lead did not carry it.
    **Fixed by propagating the homepage's existing, already-live wording verbatim — no new claims
    drafted.** All 10 now carry one canonical sentence (verified: `sort -u` over the rendered string
    returns exactly **1**, so there is no per-page drift to review).
    ⚠️ **Polarity was the trap again, and it nearly caught me an eighth time.** `.transparency-note`
    is cream, built for the dark `#contact` sections — correct on 7 pages, invisible on the two it
    would have been wrong on. **The calculator's form sits on `.section.alt` (`#fff`)** and
    **`mobile.html`'s on `.section-soft` (`#fbf8f0`) with a white card**, so both got an ink variant
    instead: a new `.transparency-note.dark` following the existing `.eyebrow.dark`/`.lead.dark`
    convention, and — because **`mobile.html` links no shared stylesheet** (the R6(c) lesson) — a
    self-contained rule in that page's own `<style>`.
    **Measured after, not assumed:** dark sections screenshotted and legible; calculator 6.68 body /
    17.61 strong / 4.92 link; mobile 6.29 / 16.64 / 4.64; no overflow.
    ⚠️ **One more self-inflicted false reading, same shape as the last two.** My verifier reported the
    7 dark-section notes at 1.0–1.4 "failing". They were not: the ancestor walk hit a
    `background-image`, set its `skip` flag, and **fell back to white as the assumed background — then
    I printed a ratio against that fallback.** A checker must not emit a number when it has just
    admitted it could not determine the background. **Undetermined is a third state, not a fail.**
    📝 **For Tyler, not a loop decision:** the disclosure is verbatim from what is already live, so it
    introduces no claim he has not approved. **If he wants different wording on the campaign pages
    than the homepage, that is a copy decision and it is his.**
  - ✅ **(f) Console and network. DONE 2026-08-07. Genuinely clean — and this time the instrument was
    tested before the result was believed.**
    **0 console errors and 0 resource errors across all 18 pages** (each loaded, scrolled and resized
    to exercise the observer/reveal paths). **0 broken same-origin assets out of 35** — every `src`,
    `href`, `srcset` and `url()` in the pages *and* inside `styles.css`/`revamp.css`, HEAD-checked.
    ⚠️ **A clean result from an untested checker is worth nothing, and this loop has now produced
    three false readings in three iterations.** So the sweep was validated with a **control**: a
    deliberate `ReferenceError` and a deliberate 404 image injected into a loaded page. Both were
    caught (`instrumentWorks:true`). **Only then was the zero trusted.** Do this every time a checker
    reports all-clear — a broken detector and a clean site produce identical output.
    **Only one externally loaded resource exists site-wide:** Google Fonts on `index.html`, with
    `display=swap` and `preconnect`, so it degrades to system fonts rather than blocking. No page
    depends on an external stylesheet for layout.
    🚩 **Real finding, flagged not fixed — the quote page cannot tell "widget loaded" from "widget
    loaded an error".** `life-insurance-quote.html` embeds the BackNine/Strife widget and guards it
    with `setTimeout(… if(!container.children.length){ fallback.classList.add("show") })`. **The test
    is whether a child element exists, not whether that child is the widget.** Locally the iframe
    returns **403 Forbidden** and renders it at full size, the container therefore *has* a child, the
    `.quote-fallback` never shows, and the page displays a giant **"403 Forbidden"** where the quoter
    should be.
    ⚠️ **The 403 itself is an artifact, and saying so matters:** the iframe src carries
    `parent_url=http%3A%2F%2Flocalhost%3A5187%2F…`, so BackNine is domain-gating an unauthorised
    origin. **On `rcowealth.com` this will load.** **The gap it exposed is not an artifact** — any
    production condition where BackNine answers with an error *page* rather than failing to connect
    (account, plan, appointment or domain misconfiguration) will show a raw vendor error on the
    firm's own quote page, with the designed fallback sitting hidden behind it.
    **Not fixed on purpose.** The iframe is cross-origin, so its contents cannot be inspected;
    `children.length` really is the only cheap signal available. A robust fix needs BackNine's
    `postMessage`/ready contract, and **guessing at the failure handling of the page that hands
    prospects to the quoter risks breaking a working revenue path to fix a hypothetical one.**
    📝 **For Tyler:** worth asking BackNine whether the widget emits a ready or error event. If it
    does, the fallback becomes three lines and the failure mode disappears.

- [x] **R6 COMPLETE 2026-08-07 — all six slices (a)–(f) done.** Across the block: 2 forms with no
  honeypot, 2 preview pages that would have deployed publicly, 16 pages of missed mobile tap targets,
  4 contrast defects including invisible text on a compliance block, and the fiduciary disclosure
  missing from 8 of 10 lead-capture pages. ⚠️ **The review passes also produced more false readings
  than real defects.** Standing rule earned the hard way: **verify the checker before believing the
  check**, and treat *undetermined* as its own state rather than folding it into pass or fail.

- [x] **R7. Rebase onto `origin/main` before any merge.** ✅ **Done 2026-08-07 (`2b69591`)** — merged
  rather than rebased, to keep the 56 commits of revamp history intact and reviewable. The feared
  duplicate did not materialise: `127b4da` and `b3f8b01` carry identical content, so `lead.php`
  merged clean and `git ls-files` shows it exactly once. Branch is now **0 behind `origin/main`**.
  **Nothing pushed.** Safety ref before the merge: `life-forward-revamp-pre-funnel-merge` (`c1194ca`).
  ⚠️ **The lesson is the standing one:** this branch went 56 commits and two days without noticing
  `origin/main` had moved underneath it, and the drift was in the lead path. **Check
  `git rev-list --count HEAD..origin/main` at the top of every iteration, not just before a merge.**

- [ ] **R4b. Design the site from R1's findings.** Only after R1 and R2. Tyler wants professional and
  attention-grabbing without the AI-template look, and has explicitly rejected the generic
  bento/neon/Lottie vocabulary. What has worked so far: photography, editorial typography, motion
  with a job (the hero drift, the line-by-line headline, the coverage slider that answers you).
  Extend that from evidence rather than adding decoration.
  - 🎯 **RE-MEASURED 2026-08-07, iteration 16 — and the premise this item was built on is now gone.**
    R1's evidence predated R2's section removal, the photo hero and R5's coverage promotion, so it was
    stale. Re-measured like for like, **1440x900, `innerText`, `/900`**, same method as the correction:

    | Site | Page height | Screens | Words | **Words per screen** |
    |---|---|---|---|---|
    | **rcowealth.com — R1 correction** | 8,603px | 9.6 | 1,289 | **135** |
    | **rcowealth.com — NOW** | **7,019px** | **7.8** | 1,108 | **142** |
    | Facet | 8,090px | 9.0 | 1,492 | 166 |
    | Farther | 8,675px | 9.6 | 1,534 | 160 |

  - **The homepage is now SHORTER than both premium references** — 7.8 screens against Facet's 9.0 and
    Farther's 9.6 — having lost **1,584px (18%)** since the correction was written. **The "we spend
    about twice the vertical space per word" finding is dead.** It was wrong once (phase 3's viewport
    arithmetic), corrected to "19% behind", and is now **11% behind Farther on density while being 1.8
    screens shorter.** There is no layout-bloat defect left to fix.
  - **The two least dense sections were measured rather than guessed, and both are load-bearing:**
    the coverage-tool section (**1,030px, 136 words, 120 w/s**) is `.live-cover` + `.carriers`, and the
    About section (**1,046px, 140 words, 119 w/s**) is a 606px portrait beside a 926px editorial
    column. **Both are exactly the vocabulary this item names as working** — the interactive tool that
    answers you, and photography with editorial type. **Compressing them would attack the things that
    are working to chase a number.** The hero is sparser still (52 w/s) and is supposed to be.
  - 🚩 **What is left is a content decision, not a layout one, and it is Tyler's.** We now say **380–430
    fewer words than the references in less vertical space.** The options are (a) leave it lean, which
    is defensible and reads faster than either reference, or (b) add substance somewhere specific.
    **The loop should not pick.** Adding words to hit a density benchmark is exactly the "decoration"
    this item forbids, and any new public copy is a draft for him regardless.
  - ✅ **Method note, since this file has a history of bad measurements:** the number was validated with
    a control — the same page measured by normal load and by `document.write` returned **7,019px /
    1,108 words / 142 w/s both ways, delta 0** — and `index.html` was confirmed **not** to redirect at
    1440, so the desktop homepage is what got measured.

- [ ] **R5. Life insurance prominence across the other 15 pages.** Carried over. Both homepages are
  done; the rest have not been looked at against "life is bread and butter". One page per iteration.
  - 🚨 **NAV FIXED SITE-WIDE 2026-08-08, iteration 17 — and this was not a one-page job.** Measured
    first: **"Life Insurance" was in the nav on `index.html` and `mobile.html` and nowhere else.**
    14 of 18 pages had no nav path to life insurance at all — **including
    `life-insurance-greenville-sc.html`, the life hub itself, whose own nav did not mention it.**
    Iteration 2 recorded "Life Insurance in the nav" as done; it was done on the two homepages.
  - ⚠️ **Third time this loop has found the same shape.** R6(c): tap targets fixed on `mobile.html`
    only. R6(e): the fiduciary disclosure on the two homepages only. Now the nav. **"Verified on the
    page I edited" keeps getting recorded as "done site-wide."** The check that catches it is cheap —
    dump the component from every page and diff — and it should be the default for any change to a
    shared header, footer or nav.
  - **Why it matters more than a missing link:** the campaign pages are where paid traffic lands
    (they carry the `utm_*` plumbing), the [[insurance-8020-pivot]] makes life the revenue priority,
    and a visitor arriving on any of them had **no navigation route to the life funnel** — they would
    have had to go back to the homepage to find it.
  - **Fixed by inserting the identical anchor in the identical position** (after "Virtual Model",
    `href="life-insurance-greenville-sc.html"`), not by rewriting navs. 14 pages changed, 3 already
    had it, `mobile.html` has its own menu and already carried it.
    **Verified in a browser at 1440 and 390:** all 17 `.navlinks` pages carry the link, one canonical
    href, **no horizontal overflow and no collision with the header CTA** at 1440 — the interior nav
    went from 5 items to 6, matching the homepage that already fit. At 390 the menu opens with all six
    items at **44px each**, inheriting R6(c)'s tap-target rule for free.
  - 📝 **Observed, deliberately not touched:** in headless capture the open mobile menu appears to let
    hero text bleed through. **The evidence disagrees with itself and I did not act on it:** the
    computed background is `rgba(6,17,31,0.97)`, `elementFromPoint` at the panel centre returns the
    nav anchor, so the menu is genuinely on top and clickable. The likeliest explanation is the
    header's `backdrop-filter:blur(18px)` compositing oddly in screenshots rather than a real
    translucency defect. **Nothing in this iteration changed that background**, so it is pre-existing
    either way. Worth one look on a real phone before anyone "fixes" it.
  - **Still open under R5:** per-page body prominence on the four commercial pages (`services`,
    `financial-advisor`, `investment-management`, `retirement-planning`) — each currently has exactly
    **one** in-body life link and no life CTA. That is the one-page-per-iteration work; the nav was
    the site-wide blocker sitting in front of it.

## Done

- [x] **The hero is a photograph now, on both homepages** (`c4ceca7` → `0c42a9c` → `1921288`, 2026-08-06, out of band at Tyler's direction). He said the hero photo "won't cut it" because it is the same file as the about section, and he was right: `assets/tyler-krause.jpg` was in `index.html` twice and `mobile.html` twice. **Pulling up his reference settled the direction** — its hero has no portrait at all, it is one full-bleed environmental photograph under a scrim with a big serif headline and glanceable facts on the bottom edge. Three options were built as `hero-preview.html` (noindex, unlinked) so the choice was made by looking; he picked **A, veteran lead**. Shipped to desktop and mobile: `clients-military.jpg`, two-pass scrim, Georgia headline, the four credentials as a band on the photo. **The headshot now appears exactly once per page**, in the advisor card. The standalone `.trust-band` section is gone because the hero band is the same four facts, and the virtual-model strip moved into its own light section below the hero, with its dark-surface colour overrides retargeted so it did not repeat the iteration 6/7 contrast defect. **The "Virtual office · live" badge and its pulsing dot are gone**, which closes one of the two items that had been waiting on Tyler since iteration 8.

- [x] **Life Insurance in the nav, and a protection band on both homepages** (`d1f6919`, iteration 2, 2026-08-05). Desktop nav and mobile menu, plus a band offering both funnel steps: *Estimate your coverage need* → calculator, *Compare real quotes* → on-site quoter. Points at the **on-site** pages rather than straight out to `app.back9ins.com`, so prospects keep Rae & Co framing and the BackNine disclosure block instead of being handed to a third-party domain. Existing `app.back9ins.com` links deliberately left alone pending the attribution check.

## Log

- **2026-08-05 — loop handed over to a new session.** The original ran in a session titled "Fsc zoom sync" (titles inherit from whatever scheduled task opened the session) and went idle after iteration 2. State at handover: branch `life-forward-revamp` at `d1f6919`, two commits ahead of `main`, working tree clean, **nothing pushed and nothing deployed**. ⚠️ **Two older website loops exist in other sessions** — one from 2026-08-04 in a session titled "Higgsfield credits refresh" — and two loops on one repo is how merge pain starts. Resume only one.
- **2026-08-05 — this file created, queue built from measurement rather than from the handoff notes.** Both handoff claims were checked: the em-dash counts (7 / 4) were right, and `body{background:#050b13}` was right in substance (it is `var(--navy)`, defined as `#050b13`). The suspected funnel trap — mobile visitors bounced off the new calculator and quote pages — **does not exist**, and item 1's real defect was found while checking it.
- **2026-08-05 — iteration 1, item 1 done (`545aaa8`).** The redirect is an **allow-list** now: the homepage redirects to `mobile.html`, everything else stays on the page the visitor asked for. Deny-list → allow-list is the load-bearing half — the old shape swallowed every page added after it, which is how the calculator and quoter escaped by *not loading the script* rather than by being spared. **Query strings now survive** alongside the hash, so a mobile visitor from an Instagram link keeps `utm_source`/`utm_campaign` instead of having attribution stripped at the door. **Verified in a browser rather than read off the diff:** all six previously-trapped pages land on themselves at 390px with no horizontal overflow and zero elements past the viewport; the homepage still redirects at 390 and 500 and stays put at 1440. ⚠️ **One false alarm worth recording:** an early probe read `/ @1440px -> /mobile.html` and looked like a regression. It was the harness — `resize_window` under 768px puts the pane into Android emulation, so `pointer: coarse` and a mobile UA stay true inside a wide iframe and the second redirect condition fires. Measure desktop behaviour at a real desktop viewport, not in a wide iframe inside a narrow window. Salesforce web-to-lead ids and the honeypot checked intact in `index`, `mobile` and `contact`.
- **Next: item 2, the mobile light conversion**, staged — (a) token layer and body/hero first.
- **2026-08-05 — iteration 2, item 2 step (a) (`9b9b1ae`).** Light tokens **added, not swapped**: `--navy`/`--paper` mean the opposite thing in this file than on desktop (here `--navy` is the background and `--paper` is the *text*), so redefining them would have silently inverted ~50 correct uses inside the dark bands. Values lifted from `styles.css` so mobile and desktop are one brand. Converted body, stage, the wide-screen frame and the hero; the alternating band rhythm is untouched and the header keeps its dark glass, matching revamp.css's deliberate desktop call. **Two defects the browser caught and the diff would not have:** `.private-room` is a dark card at **62% opacity** — fine over a near-black stage, muddy grey over a light one, dragging its white and gold text to ~4:1, so it is opaque dark now; and the advisor block was a **5% white veil** with white text that only worked because the stage behind it was near-black, so it is a real white card with ink text. Verified at 390px: zero light-on-light left in the hero or advisor block, every remaining light string sits on the dark private-room card at luminance 16, no horizontal overflow. Lead capture and em-dash count unchanged.
- ⚠️ **Two of my own measurements were wrong before they were right, both recorded so the next stage does not repeat them.** (1) A contrast walk that ignores **alpha** reads `rgba(255,255,255,.05)` over navy as *white*, and flagged 34 phantom failures including white-on-white text that is really white-on-dark. Composite the layers before judging. (2) The header looked broken (dark ink on dark glass) until I checked the actual text leaves — every link sets its own light colour, so it was never inheriting. **Both would have produced a fix for a non-bug.**
- **Still open and NOT mine:** `section-light` and `section-soft` carry light-coloured text on light backgrounds by my count, but a spot check showed most are **gold accent labels** that read fine. Worth a proper alpha-aware audit in step (d) rather than a claim now.
- **Next: item 2 step (b), cards and bands.**
- **2026-08-05 — iteration 3, item 2 step (b) (`1393ad6`).** **Started by measuring desktop rather than deciding by taste:** after the revamp `index.html` renders light at the top and keeps **three dark bands plus a dark footer** at the bottom, which is the shape mobile already has after step (a) — so converting mobile's two `section-dark` bands would have made it **diverge** from desktop, not converge. They stay. Four real fixes instead: **a regression from step (a)** (`.eyebrow` moved to `--gold-ink` for the light hero and dropped to 3.28:1 inside the dark bands — one token cannot serve both surfaces, so dark bands and footer get the pale gold back); **the photo cards' scrim**, which reached `.35` at 56% and transparent above, fine over the two dark photographs and not over the two bright ones, where the gold label and white title sit exactly where it had faded out; **section lead paragraphs** (`--muted` has one consumer and the dark bands already override it, so 3.18:1 → 4.9:1 touched nothing else); and the **footer disclosure** at 4.48:1 against a 4.5 floor. Verified **zero WCAG AA failures across the whole page** excluding the photo cards. Lead capture and em-dash count unchanged.
- ⚠️ **Third measurement lesson, and the most important one: a contrast checker cannot see a photograph.** It reads CSS colours and gradients only, so it scored all twelve strings in the `.pm-card` photo tiles as 1:1 failures against the section *behind* the image — text that a reader sees as white-on-dark-photo. **It also missed the real defect in those same cards**, which was the scrim fading out under the label. Photo-backed content is judged by screenshot; the checker is for CSS-coloured surfaces and must exclude `.pm-card`. Together with the alpha and inheritance lessons above, that is three false readings from automated colour maths in two iterations — **look at the page**.
- **Next: item 2 step (c), forms and footer.**
- **2026-08-05 — iteration 4, item 2 step (c) (`b38815e`).** **The form needed no conversion** — it was already a white card with ink labels, built to sit on the dark page — and **the footer stays dark because desktop's does**. So the step became about what a phone actually touches. **The contact email was breaking mid-word into `rcowealth.c / om`**: `.contact-shortcuts` is a two-column grid, so inside a 390px stage each column is ~150px and `word-break:break-word` split it eagerly; one column fits it whole and gives both shortcuts a full-width 44px target. **Tap targets:** the two **consent checkboxes** rendered at **11x13** — their labels wrap the text so the tap area was already fine (checked, not assumed), but the box is what a reader looks at to confirm they opted in, so 18px with a navy accent; **footer links were 18px** and are 44 now, reusing the `min-height` + `inline-flex` pattern `.contact-shortcuts a` already used rather than inventing one; header Call pill and menu button 38 → 44. **The honeypot was identified and deliberately left alone** — it is the one control that must NOT be reachable, still at `left:-9999px`. Every interactive control now clears the 40px floor except it. **The form was NOT submitted** — it posts to the live Salesforce org and a test submission would create a real lead — so wiring was verified structurally: action, `oid`, `retURL`, `lead_source`, `company`, five hidden fields, both consent ids with `value=1`.
- **Next: item 2 step (d), the full read at 390 and 430** — the pass that catches whatever the per-section steps missed. Then items 3-6.
- **2026-08-05 — iteration 5, item 2 step (d) (`792f784`). ITEM 2 IS DONE — the mobile page is light.** Both 390 and 430 pass the automated sweep: no horizontal overflow, nothing past the viewport, **zero WCAG AA contrast failures**, every interactive control over the tap minimum except the honeypot (which must stay unreachable). **So the value of this step was the two things only looking at the page finds.** (1) **The logo in the virtual card was washed out** — all three logos are the same inlined base64, a light-on-transparent mark built for a dark background; still correct in the header and footer, which are still dark, and wrong on the white card step (a) created. The repo already carried the navy-and-gold version, so the card points at `assets/rae-co-logo-header.png` while the header and footer keep the inlined one (correct there, and inlined to avoid a request above the fold). (2) **The advisor card was `align-items:center`** against a text column much taller than the photo, so at 430 the portrait sat marooned low-left with empty space above it while the name started at the top.
- **Item 2 took four iterations and produced six defects that no diff would have shown** — the 62%-opacity card going muddy, the 5% white veil, the eyebrow regression, the scrim fading under the labels, the mid-word email break, the 11x13 consent boxes — plus the two above. **Every one came from a screenshot or a rendered measurement, not from reading CSS.**
- **Next: item 3, the desktop Virtual Model contrast bug** — small, and it is on the live site today. Then item 4 (em-dashes: 7 in `index.html`, 4 in `mobile.html`), then the competitor benchmark Tyler actually asked for.
- **2026-08-05 — iteration 6, item 3 (`7389983`). Two corrections to this file's own claim.** (1) **It is NOT live.** `revamp.css` does not exist on `main` — 204 lines, branch-only — and main's `index.html` does not load it, so the live hero is still dark and white text there is correct. This is a defect **the revamp introduced on this branch**, not one Tyler has been shipping. I wrote "on the live site today" from the handoff note without checking. (2) **It was not one string:** the revamp converted the eyebrow, h1, lead and pills and stopped, leaving the strip lead-in at 1.32:1, the strong at 1.06:1, three item titles at 2.47:1 and three descriptions at 1.7:1 — the whole band below the fold rendered as near-blank cream. **The item card was the part that mattered:** `.strip-item` carries `background:rgba(6,17,31,.36)`, which read as a subtly darker card over the old dark hero and composites to mid grey-blue over the light one, holding even ink text to 3.87:1 — **the same defect `.private-room` had on mobile**, a translucent dark panel that only worked because of what was behind it. Hero failures **9 → 0**, with **0 hidden elements** in scope (a hidden element returning "no failures" is the trap, so it is now counted rather than skipped).
- ⚠️ **VERIFIED BY MEASUREMENT, NOT BY EYE — the first time in this loop that has been true, and it is worth flagging.** Screenshots came back composited from **stale frames**: the sticky header rendered at the **bottom** of the capture, which is the tell. So the visual check that caught six defects across items 1-2 was unavailable. Computed colours, effective backgrounds, contrast ratios and hit-testing all agree, **but nobody has looked at this one.** Worth a glance at `http://localhost:5187/index.html` before this branch is merged.
- ⚠️ **Two harness traps learned this iteration.** (a) **The stylesheet is served from cache even when the HTML is cache-busted** — a `?cb=` on the page does nothing for `revamp.css`, so an early measurement read the OLD CSS and reported the fix had not applied. Re-point the `<link href>` with a buster and wait. (b) **Measuring immediately after `navigate` reads styles before the stylesheet has applied**, which produced one entirely false "nothing changed" result. Wait ~1s.
- **Next: item 3b** (the 15 remaining desktop failures), then item 4 (em-dashes), then the competitor benchmark.
- **2026-08-05 — iteration 7, item 3b (`4df4025`). The headline number was wrong: 15 flagged, 3 real.** **Twelve are white text over PHOTOGRAPHS** in `.client-card`, scored against the cream section behind the image — the same false positive `.pm-card` produced on mobile, from a skip-list that only knew about `.pm-card`. Those twelve are **deliberately untouched**: `.client-card-body` sits at the **bottom** of the card where the `:after` scrim is at `.92`, so the text is over a near-opaque overlay, not over the section. **The real one:** `revamp.css` lights `#clients` and `#process`, converting the background and inherited colour and leaving the section **lead paragraph** on its dark-section rule at 1.05:1 on cream — the heading above it inherits `--ink` and reads fine, so the section *looked* converted and its one paragraph was invisible. **Same shape as item 3: the revamp converted what it could see and stopped.** Plus two marginal ratios. **`--muted`'s blast radius was measured, not assumed** — 13 consumers across four other pages, **zero on a dark background**, so darkening it is a pure improvement; `mobile.html` is unaffected because it defines its own `--muted` inline. Real failures **3 → 0**.
- ✅ **The screenshot problem is understood and has a workaround.** Captures are reliable **near the top of the document** and come back as **stale frames once the page is scrolled deep** — the tell is the sticky header rendering at the *bottom* of the capture — and it happens whatever drives the scroll (JS or real input). **Workaround: set a very tall viewport (e.g. 1440x1800) so the target sits above the fold, then capture without scrolling.** That is how item 3's hero strip was finally confirmed visually this iteration. It does not reach content 5,000px down, so `#clients` remains measured-but-unseen.
- ⚠️ **Standing lesson, now four times over: the contrast checker cannot see photographs, alpha it does not composite, inherited colour, or gradient-clipped text.** It has produced a false reading in every iteration it has been used. It is useful for finding *candidates* on CSS-coloured surfaces; **the verdict comes from looking.**
- **Next: item 4 (em-dashes — 7 in `index.html`, 4 in `mobile.html`), then the competitor benchmark, then life-insurance prominence across the other 15 pages.**
- **2026-08-05 — iteration 8, item 4 (`ce919c8`). 11 expected, 13 found** — two more on `life-insurance-greenville-sc.html` and `life-insurance-review-checklist.html`, which no earlier count had swept. Site-wide is zero now, `&mdash;`/`&ndash;` entities included. **Rewritten, not swapped:** the rule is copy that reads human, so an em-dash mostly wants to become a full stop, which also shortens the sentence — *"more intentional — not distant"* → *"more intentional. Not distant."* The character survives a find-and-replace; the cadence does not. **Two are compliance sentences** and only the punctuation changed, meaning intact. **Two are META, invisible to a page read** — the description Google renders and the `og:description` that renders when the link is shared, i.e. the first copy a stranger ever sees. **One is the copy-to-clipboard string** a visitor pastes, now using the middot the site already uses elsewhere rather than a new separator. **Verified by parsing each page's rendered text and meta tags, not by grepping source.** Lead capture untouched. ⚠️ **All of it is DRAFT copy pending Tyler's approval** per the RIA rule; it is on the branch and nothing is deployed.
- **Next: item 5, the competitor benchmark** — the one part of Tyler's original brief that no iteration has touched. Then item 6, life-insurance prominence across the other 15 pages.
- **2026-08-05 — out of band, at Tyler's direction (`f0b98be`).** He looked at the branch and said the hero photo had to go back to what is live. **He was right and it was not this loop's change:** `556791f` ("Capture the cinematic revamp on a branch") swapped `assets/tyler-krause.jpg` for a still from `tyler-hero.mp4` in three places — the still catches him mid-word in a dark room. Reverted in all three, and the `tyler-hero` video went with them, because it is the same footage the still came from and a nicer poster would have shown the same frames the moment it played. `hero-ambient.mp4` is untouched (not him). **The frames were built landscape for that clip** (16/10 desktop, 16/11 mobile) and a 4:5 portrait cover-cropped into a landscape box loses the top of his head or everything below the collar — both are **4/5** now, matching the asset at 960x1200 exactly, so nothing is cropped. Verified rendering at 460x575 desktop and 400x500 mobile.
- 🚩 **Flagged, not changed:** the frame still carries a **"Virtual office · live" badge with a pulsing green dot**. It read as a live feed when it sat on a video; over a static headshot it reads as a broken stream. It is public copy, so it is Tyler's call — drop the dot, or drop the word "live".
- **Queue reordered: item 4b (word-heavy / skim / trust) is now ahead of the competitor benchmark**, because Tyler raised it directly and the benchmark was going to produce the same finding more slowly.
- **2026-08-05 — iteration 9, item 4b slice (a) (`149146d`).** **The facts were already on the page and were being wasted:** `index.html` carried a `.trust-marquee` with seven real credentials and it was **`aria-hidden="true"`**, duplicated in the DOM for the scroll loop, and **moving** — so the firm's strongest signals reached neither a skimming eye nor a screen reader, and a crawler saw them as decoration. Now a static four-item band: **15+** years, **100%** virtual, **Series 65** (IAR, fiduciary standard), **Schwab** custody. **Nothing is a new claim** — every value is already stated elsewhere on the page and "more than 15 years" is on `main`, i.e. live copy. **The honest version of a stats band for an RIA is credentials and structure — never performance, never AUM, never a number nobody can substantiate.** Veteran-owned and SC RIA are not lost; they are hero meta-pills directly above. Word count **1,233 → 1,221** measured the same way as the baseline, seven duplicated DOM nodes gone. Verified 4 columns at 1440, 2 at 900, no overflow, nothing clipped. `index.html` is never served below 820px (the redirect), but a window resized *after* load stays, so the small-screen rule is reachable.
- **Next: slice (b)** — the 7 paragraphs over 25 words on `index.html`, starting with the 94-word one. Pure word reduction, no new claims, no new sections.
- **2026-08-05 — iteration 10, item 4b slice (b) (`351189e`). Three cut, four deliberately kept — and the judgement is the point.** Hitting "7 paragraphs over 25 words" blindly would have shortened **compliance copy**, which is the wrong move on an RIA site. **Cut:** the **94-word advisor bio** (now two blocks totalling 56, and it stopped repeating the credential band above it — "15 years" and "custodied at Charles Schwab" are the band's job now, so prose was spending those words twice); the `#virtual` lead's abstract tail; and the **hero lead** 32 → 24 words, four lines to three, because it is the first thing anyone reads. **Left alone on purpose:** the form disclaimer (32w), the fiduciary/compensation disclosure (31w), the **client credential-security warning** (28w — the sentence that makes a phishing attempt obvious), and a 26w block that is already two short sentences. **Longest paragraph 94 → 32, and the 32 is a disclosure that stays. Total 1,233 → 1,164.** All three compliance strings verified present after the edit.
- 🚩 **Two things still waiting on Tyler, both raised and neither answered.** (1) The **"Virtual office · live" badge** with a pulsing dot now sits over a static headshot — drop the dot or drop the word. (2) The **published flat fees** ($750 / $2,000 / $3,000) are the strongest trust signal not on the site; almost no competitor publishes price. **Deliberately not added** — putting prices on a public site is a business decision, not a layout one.
- **Next: slice (c)** — the same treatment on `mobile.html` (920 words, 2 paragraphs over 25, longest 55) plus its own credential band, since it does not load `revamp.css`.
- **2026-08-06 — out of band, the hero, at Tyler's direction (`c4ceca7`, `0c42a9c`, `1921288`).** See the Done entry above for what shipped. **The method is the part worth keeping: three options were built and looked at rather than described.** Reading the reference is what killed the wrong question — the argument had been *which* picture of Tyler to use, and the reference does not put a face in its hero at all.
- ⚠️ **The translucent-panel defect has now happened three times on this site**: `.private-room` (mobile, iteration 2), `.strip-item` (desktop hero, iteration 6), and `.protect-band` over the new photograph. Every time, a light-or-dark panel at partial alpha looked correct only because of what happened to be behind it, and every time it was caught by a screenshot rather than by reading CSS. **If a rule sets a background with an alpha below 1, the surface behind it is part of the design and moving the panel breaks it.**
- ⚠️ **And a fourth of my own making, immediately after fixing the third:** `.photo-hero .btn-secondary` was scoped to the whole hero, so it turned the protection band's "Compare real quotes" button white on cream. **A section-wide colour rule is a trap whenever that section contains a card of the opposite polarity.** Scope to the component, not the section.
- **The desktop and mobile crops of the same photograph are deliberately different** (`72% 32%` vs `40% 22%`). A 3:2 landscape cover-cropped into a tall narrow box keeps about the middle third, and the desktop value puts that third on the back of the child's head: no uniform, no face, nothing that says military family, on the surface that gets nearly all the traffic. **Full-bleed photo heroes need a per-breakpoint `object-position`, chosen by looking at the crop.**
- 🚩 **Still waiting on Tyler, and now it is one item not two.** The pulsing "live" badge is resolved (deleted with the old frame). **The published flat fees ($750 / $2,000 / $3,000) are still the strongest trust signal not on the site** and are still a business decision, not a layout one.
- 🚩 **Raised, not acted on: the uniform in `clients-military.jpg` is Army-pattern, and Tyler is a Marine.** The copy beside it says "led by a Marine Corps veteran". Civilians will not notice; his ICP is veterans, and they will. Defensible as generic imagery of the families the firm serves rather than a picture of the founder, but it is his call. **The durable answer to this and to the whole hero problem is real photography of Tyler, shot wide enough to crop as a hero.**
- **2026-08-06 — a long working session with Tyler, out of band.** Hero is a photograph (family, not the uniform); the four stat tiles are gone from both homepages because he called them AI-generated and he was right; About is editorial with a credential rail; the calculator is drag-first; a live coverage slider sits on both homepages; a carrier band replaced the copy that implied Mutual of Omaha was the only carrier. Words on `index.html` **1,236 → 1,072**, with every compliance string verified present afterwards.
- ⚠️ **Item 4b is NOT closed and the count moved the wrong way first.** Adding the About section took `index.html` from 1,164 to 1,236 before the cut brought it to 1,072. The reference is 934. **Any session that adds a section owes the page a cut in the same pass**, or this ratchets.
- ⚠️ **The translucent-panel defect has now happened five times** (`.private-room`, `.strip-item`, `.protect-band` over the photo, and my own hero-wide `.btn-secondary` rule, plus the mobile protect-band again). **Rule: scope colour rules to the component, never to the section, whenever that section can contain a card of the opposite polarity.**
- ⚠️ **`revamp.css` cache trap cost real time again and produced one false "the hero is blank" diagnosis.** A `?cb=` on the HTML does nothing for the stylesheet. Re-point the `<link href>` with a buster and re-measure **before** believing any visual result. Same for `reveal.js`: a cached copy silently ran the old code and made a working slider look broken.
- ⚠️ **A full-bleed photo hero needs a per-breakpoint `object-position` AND a bounded height.** The mobile hero grew to ~1570px when the funnel blocks went inside it, forcing a 1600x1067 landscape photo into a 1.47x upscale showing a sixth of the frame. Fixed by closing the hero early and moving the blocks to a light section below.
- 🚩 **`origin/main` moved during the session.** `lead.php` was pushed to `main` at 22:01 on 2026-08-06 (`b3f8b01`) and, since push to main auto-deploys, went out. **The same file already exists on this branch as `127b4da` with identical content but a different SHA, so this branch must be rebased onto the new `origin/main` before any merge** or the change lands twice. Local `main` is one commit behind `origin/main`.
- 🚩 **Waiting on Tyler:** publishing the flat fees (he is undecided, do not re-ask); the exact accounting-degree level and school if he wants it named; and whether the surviving **V11 redesign** on `origin/claude/rcowealth-premium-redesign-qjdZ2` should be served for review. Carrier **logos** need his BGA to confirm which carriers permit logo use and to supply approved files.
- **Next: back to the queue — slice (c)**, then item 5 (competitor benchmark) and item 6 (life-insurance prominence across the other 15 pages).

- **2026-08-08 — iteration 17, R5. The life-insurance nav link existed on two pages out of eighteen.** Measured before touching anything, and the result reframed the item: **"Life Insurance" was in the nav on `index.html` and `mobile.html` and nowhere else.** Fourteen pages had no nav route to life insurance — **including `life-insurance-greenville-sc.html`, the life hub itself, whose own nav did not mention life insurance.** Iteration 2 logged "Life Insurance in the nav" as done, and it was, on the two pages it was tested on. ⚠️ **That is the third time this loop has found the identical shape:** R6(c) fixed tap targets on `mobile.html` only, R6(e) had the fiduciary disclosure on the two homepages only, now the nav. **"Verified on the page I edited" keeps getting written down as "done site-wide."** The catch is cheap — dump the shared component from every page and diff it — and it should now be automatic for any header, footer or nav change. **This mattered more than a missing link:** the campaign pages carry the `utm_*` plumbing, so they are where paid traffic lands, life insurance is the revenue priority under the 80/20 pivot, and a prospect landing on any of them had **no navigational route to the life funnel at all** — back to the homepage or nothing. Fixed by inserting the identical anchor in the identical position rather than rewriting navs; 14 pages changed, 3 already had it, `mobile.html` has its own menu and already carried it. **Verified at 1440 and 390:** all 17 pages carry it, one canonical href, no overflow and no collision with the header CTA now that interior navs went from 5 items to 6, and the mobile menu opens with all six at 44px, inheriting R6(c)'s tap-target fix for free. 📝 **One thing observed and deliberately left alone:** the open mobile menu appears to let hero text bleed through in headless capture, but the computed background is `rgba(6,17,31,0.97)` and `elementFromPoint` returns the nav anchor, so it is on top and clickable. **The signals disagree, the likeliest cause is the header's `backdrop-filter` compositing badly in screenshots, and nothing this iteration touched that background** — so it gets logged for a look on a real phone rather than a speculative fix. **R5 is not closed:** the four commercial pages each still have exactly one in-body life link and no life CTA. That is the per-page work; the nav was the site-wide blocker sitting in front of it.

- **2026-08-07 — iteration 16, R4b. Re-measured before designing, and the thing R4b exists to fix is already fixed.** R1's density evidence predated R2's section removal, the photo hero and R5's coverage promotion, so the first honest move was to refresh it rather than build on a stale number. Measured like for like at 1440x900: **the homepage is now 7,019px / 7.8 screens / 1,108 words / 142 words per screen**, against **8,603px / 9.6 / 1,289 / 135** when the correction was written. **It has lost 1,584px — 18% of its height — and it is now shorter than both premium references** (Facet 9.0 screens, Farther 9.6). 🎯 **So the finding this whole item was built on is dead.** "We spend about twice the vertical space per word" was wrong once already (phase 3's viewport arithmetic), was corrected to 19% behind, and now reads **11% behind Farther on density while being 1.8 screens shorter than it**. **There is no layout-bloat defect left to attack.** I measured the two least dense sections rather than assuming: the coverage tool (120 w/s) and About (119 w/s). **Both are precisely the vocabulary R4b names as working** — the interactive tool that answers you, and photography beside editorial type. **Compressing them would damage what works in order to move a benchmark**, so I did not. 🚩 **What remains is a content decision and it is Tyler's, not the loop's:** we say 380–430 fewer words than the references in less space. Leave it lean, which reads faster than either reference and is defensible, or add substance somewhere specific. **Adding words to hit a density number is the exact "decoration" this item forbids**, and any new public copy is his draft to approve regardless. ✅ **Given this file's history of bad measurements, the number was controlled:** normal load and `document.write` load returned **7,019px / 1,108 / 142 both ways, delta 0**, and `index.html` was confirmed not to redirect at 1440, so the desktop homepage is genuinely what was measured. **No code changed this iteration** — the correct output of an evidence item was evidence.

- **2026-08-07 — iteration 15, R6(f) console and network. Clean, and R6 is complete.** **0 console errors and 0 resource errors across 18 pages; 0 broken assets out of 35 same-origin references**, including the `url()`s inside `styles.css` and `revamp.css`. ⚠️ **But the useful part of this iteration is what I did before believing that zero.** Three iterations in a row this loop has been handed confident, wrong numbers, so the sweep was **validated with a control** — a deliberate `ReferenceError` and a deliberate 404 image injected into a real page load. Both were caught, and only then was the all-clear trusted. **A broken detector and a healthy site emit exactly the same output;** the only thing separating them is a planted fault. That is now the standing rule for any check that reports nothing wrong. 🚩 **One real finding, flagged rather than fixed.** `life-insurance-quote.html` guards the BackNine widget with `if(!container.children.length){ show fallback }` — **it tests whether a child exists, not whether that child is the quoter.** Locally the iframe returns **403 Forbidden** and renders it full-size, so the container has a child, the fallback stays hidden, and the page shows a giant "403 Forbidden" where the quoter belongs. ⚠️ **The 403 is an artifact and I checked rather than assumed:** the iframe src carries `parent_url=…localhost:5187…`, so BackNine is domain-gating an unauthorised origin, and this will load fine on `rcowealth.com`. **The logic gap is not an artifact** — any production condition where BackNine returns an error *page* instead of failing to connect puts a raw vendor error on the firm's quote page with the designed fallback hidden behind it. **Left unfixed deliberately:** the iframe is cross-origin so its contents cannot be read, `children.length` genuinely is the only cheap signal, and guessing at the failure handling of the page that hands prospects to the quoter risks breaking a working revenue path to fix a hypothetical one. **Ask BackNine whether the widget emits a ready/error event; if it does, this is a three-line fix.** **R6 is now complete.** Across six slices it found 2 unprotected forms, 2 preview pages that would have deployed publicly, 16 pages of missed tap targets, 4 contrast defects including invisible text on a compliance block, and a fiduciary disclosure missing from 8 of 10 lead-capture pages — **and it produced more false readings than real defects while doing it.**

- **2026-08-07 — iteration 14, R6(e) copy and compliance. Five checks clean, one real gap, and the gap was on the pages that matter most.** **Em-dashes zero, "fee-only" absent, VUL absent, no performance language, TCPA consent and form disclaimer and credential warning on all 10 form pages.** The two `guarantee` hits are the MYGA product name and the IUL *"not a forecast and are not guaranteed"* disclaimer — compliance text doing its job, not a violation. 🚩 **The gap: the fiduciary and compensation disclosure lived on `index.html` and `mobile.html` only. The other 8 lead-capture pages carried none** — no fiduciary standard, no compensation-and-conflicts language, no Form CRS pointer. **The homepage set the framing and the 8 pages that actually take a prospect's contact details did not.** Propagated the homepage's already-live wording verbatim so no new claim was drafted; all 10 now carry one canonical sentence, confirmed by `sort -u` returning exactly 1. ⚠️ **Polarity nearly caught me an eighth time.** `.transparency-note` is cream for the dark `#contact` sections — right on 7 pages, invisible on the two where the form sits on white: the calculator's `.section.alt` and `mobile.html`'s `.section-soft`. Both got an ink variant, and because **`mobile.html` links no shared stylesheet** — straight from R6(c) — its rule had to be self-contained in that page's own `<style>`. **The R6(c) and R6(d) lessons were the two things that made this iteration safe;** without them I would have pasted cream onto white and called it done. ⚠️ **And a third self-inflicted false reading, same family as the last two:** my verifier printed 1.0–1.4 "failures" for the 7 dark-section notes. It had hit a `background-image`, set a `skip` flag meaning *could not determine the background*, **fallen back to assuming white, and then reported a ratio against that assumption.** Screenshots showed all 7 perfectly legible. **Undetermined is a third state, and a checker that collapses it into "fail" will keep manufacturing bugs.** 📝 **Left for Tyler:** the wording is verbatim from what is already published, so nothing new is claimed — but if he wants different disclosure copy on campaign pages than on the homepage, that is his call, not the loop's.

- **2026-08-07 — iteration 13, R6(d) contrast. 4 real defects, 20 false alarms, and the checker lied twice more.** **A whole paragraph and a compliance heading were unreadable on the protection-review page** — `h3 "Important notes"` rendered **white on a white card**, and the `.lead` under "How the review works" was **cream on cream at 1.05**. Both invisible, both live. ⚠️ **But the headline is that this slice's warning earned itself again.** The checker opened with **12 failures on both homepages at ratios near 1.0** — every one fake. The people-media cards paint their dark panel with `.pm-card::after{position:absolute;inset:0;z-index:-1;background:linear-gradient(…)}`, and **a checker that walks ancestor `background-color` cannot see a pseudo-element.** It read the cream section behind the card and condemned text that is actually white-on-near-black. I nearly "fixed" a card that was never broken. **Teaching pseudo-backdrop detection took those 12 to 0.** ⚠️ **Then my own fix produced the next false reading.** Busting the stylesheet — the cure for R6(c)'s `?cb=` trap — races the page load, and `life-insurance-quote.html` also pulls an unreachable external CDN sheet, so the nav was measured **mid-restyle in browser-default link blue**: 5 more fake failures, and they **reproduce identically every run**. A live probe shows the nav styled correctly. **Reproducible is not the same as real** — that is the one lesson from this iteration I would keep if I could keep only one. **All 4 real defects were the same family: a light surface carrying dark-surface styling.** Three of them needed **no CSS whatsoever** — `.eyebrow.dark`, `.lead.dark` and `.btn-secondary.dark` already exist and the markup simply omitted the modifier. **The section indicts itself: "Schedule a Review" already carried `.dark` while "Use the Form", inside the same `<div>`, did not.** A previous pass fixed one button and missed the two beside it. Only the `h3` needed a real change, and it was a root-cause one: `.content-panel` set a white background but never set a colour, so inside a dark section the card inherited white — `p` and `li` were already overridden, which is precisely why only the heading exposed it. **Seventh occurrence of this family.** The recurring shape is never "wrong colour", it is **"a modifier omitted on one element while its siblings got it"**.

- **2026-08-07 — iteration 12, R6(c) mobile, and R3 ticked (`c01ba5d`).** **The pass found no overflow anywhere** — 18 pages at 390 and 430, zero horizontal scroll, zero elements past the viewport, which is the first review slice to come back clean on its headline metric. **What it did find is a category of bug worth naming: a fix that lives in the wrong file looks identical to a fix that is done.** Iteration 4 raised the mobile tap targets and verified them on `mobile.html` — but `mobile.html` is the one page that links no shared stylesheet, so the rules went into its inline `<style>` and never reached the 16 pages on `styles.css`. Those pages carried **12 footer links at 21px, a 37px menu button and a 19px breadcrumb** for two days, on every service and legal page, while the checkbox in this file was effectively ticked. **Verifying on the page you edited proves the rule works, not that it applies.** ⚠️ **Second lesson, smaller and sharper: `width:18px` on the consent box produced `13x18`.** `.checkline` is `display:flex`, so the consent sentence beside it shrank the box on the cross axis and only the height survived — **a dimension on a flex child is advisory until `flex:none` says otherwise.** ⚠️ **And the `?cb=` trap took another round off me**: the first re-measure came back byte-for-byte identical to the baseline and read as a no-op fix. It was the stylesheet cache, exactly as this Log warned two iterations ago — **the numbers only moved when the `<link href>` was re-pointed, not the page URL.** Sixth false automated reading in this loop, second from this cause. Everything left under 40px is exempt by category and now says so in the queue: the consent checkboxes (the label is the target), inline links inside sentences, and the honeypot. **Guardrails re-checked after the CSS change, not assumed:** 8 lead forms still on the Funnel action with `oid`, `retURL`, both consent ids and the honeypot, and the calculator still returns $1,270,000 for the documented 95,000 case.

- **2026-08-07 — out of band, at Tyler's direction from his phone (`2b69591`). R6(b2) and R7 closed together; the loop had stalled and the finding it stopped on was misdiagnosed.** The loop's own tick never fired after 17:05 EDT, so this was done from a separate session. **The "all 10 forms still post to Salesforce" alarm was real about the branch and wrong about the business.** `rcowealth.com` was already serving the Funnel action — fetched live, 0 Salesforce hits — so the cutover Tyler was told was done really was done. What had happened is that **this branch was cut from local `main` before the flip reached `origin/main`**, so it carried the pre-cutover forms forward under 56 commits of revamp work. The danger was therefore **the reverse of what was written**: not that the cutover had never happened, but that merging this branch would have **undone it silently**, with the failure only surfacing on the day the org is cancelled and every website lead dies at once. ⚠️ **The near-miss worth remembering: the previous pass proposed wiring the forms to `lead.php`, which would have taken lead capture from working to dead** — IONOS runs no PHP and that file 403s. A fix aimed at the wrong target is more dangerous than the bug, because it ships with confidence. **Merged `origin/main` instead of hand-editing ten endpoints**, so the branch now carries the real commit rather than a lookalike. Verified in a browser on `localhost:5187`, not off the diff: 10/10 forms on `https://pi-nas.tail34488a.ts.net/` (303, live), `oid` + `retURL` + both consent ids + the `website_url` honeypot intact on all 10. **No form was submitted** — a POST creates a real lead. **Nothing pushed; `main` untouched.**
