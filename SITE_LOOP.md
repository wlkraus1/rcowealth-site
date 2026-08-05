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

- [x] **1. A mobile visitor to any deep link lands on the homepage instead.** Done 2026-08-05 (`545aaa8`). Highest value in this file: it is a conversion defect and an SEO defect at once, and it is exactly the "links that need fixing".
  - **Measured, not assumed.** `mobile-redirect.js` runs `window.location.replace('/mobile.html' + hash)` — it **drops the path entirely**. Ten pages load it: `index`, `services`, `contact`, `client-login`, `financial-advisor-greenville-sc`, `investment-management-greenville-sc`, `retirement-planning-greenville-sc`, plus the three that are in its own exclusion list.
  - So a phone tapping through to **Services**, **Investment Management**, **Retirement Planning** or **Contact** is bounced to the mobile homepage and has to find the page again. Traffic is reels and social, i.e. almost entirely mobile, so this is most visitors.
  - **And it is an SEO problem, not only a UX one.** Googlebot Smartphone's UA matches `Android` + `Mobile` and it renders at a mobile viewport, so under mobile-first indexing every one of those URLs redirects to the homepage for the crawler too.
  - **Three pages load the script AND are excluded by it** (`life-insurance-protection-review`, `life-insurance-review-checklist`, `life-insurance-greenville-sc`) — dead weight, harmless, tidy it in the same pass.
  - ✅ **Checked and NOT a defect, so nobody re-opens it:** `life-insurance-calculator.html` and `life-insurance-quote.html` do **not** load the redirect at all, so the new funnel pages are reachable on a phone. I expected a trap here and there is none.
  - Direction: the fix is a mobile-friendly destination per page, not a single `mobile.html` catch-all. That is bigger than one iteration — start by making the redirect **preserve the path** for pages that have a mobile equivalent and leave the rest alone, then take pages one at a time.

- [ ] **2. `mobile.html` is dark, and mobile is what nearly every prospect actually sees.** Tyler's "it is dark and boring". The June cinematic revamp lit up desktop and never touched mobile. Repo rule is light/bright for business work.
  - **Measured:** `--navy:#050b13` on `body`, 91KB, inline CSS, and roughly **65 colour decisions that assume a dark background** — 34 `rgba(246,239,224,…)`, 11 `rgba(255,255,255,…)`, 20 dark hex literals. **Not a variable swap.**
  - **Staged across iterations, not one pass** — my call, since Tyler did not answer the question. This is the single highest-risk change in the file: it is the page every prospect sees, on a branch nobody has reviewed yet. Order: (a) the token layer and body/hero, (b) cards and bands, (c) forms and footer, (d) a full-page read at 390 and 430 wide.

- [ ] **3. Contrast bug on the desktop homepage.** The "Virtual Model" strip text is near-invisible — light text left on cream after the section flipped light. Opacity is 1, so it is a colour choice and not the reveal animation. Small, and it is on the live site today.

- [ ] **4. Em-dashes out of public copy.** 7 occurrences in `index.html`, 4 in `mobile.html`, 0 `&mdash;` entities. Counted as occurrences, not lines.

- [ ] **5. Competitor benchmark — Tyler asked for it and no iteration has done it.** Use `/firecrawl-competitive-intel` against Upstate SC life-insurance and RIA sites. What to bring back: how they surface protection above the fold, what their quote/calculator funnel looks like, and where Rae & Co's page loses the comparison. **Findings become queue items here, not a report nobody opens** — see [[feedback-obsidian-never-opened]].

- [ ] **6. Life insurance prominence across all 17 pages.** Iteration 2 fixed the two homepages. The other 15 have not been looked at against "life is bread and butter". Audit, then fix the worst offenders one page per iteration. Financial planning and wealth management stay visible throughout — the ask was to lead with protection, not to hide what the firm is.

## Done

- [x] **Life Insurance in the nav, and a protection band on both homepages** (`d1f6919`, iteration 2, 2026-08-05). Desktop nav and mobile menu, plus a band offering both funnel steps: *Estimate your coverage need* → calculator, *Compare real quotes* → on-site quoter. Points at the **on-site** pages rather than straight out to `app.back9ins.com`, so prospects keep Rae & Co framing and the BackNine disclosure block instead of being handed to a third-party domain. Existing `app.back9ins.com` links deliberately left alone pending the attribution check.

## Log

- **2026-08-05 — loop handed over to a new session.** The original ran in a session titled "Fsc zoom sync" (titles inherit from whatever scheduled task opened the session) and went idle after iteration 2. State at handover: branch `life-forward-revamp` at `d1f6919`, two commits ahead of `main`, working tree clean, **nothing pushed and nothing deployed**. ⚠️ **Two older website loops exist in other sessions** — one from 2026-08-04 in a session titled "Higgsfield credits refresh" — and two loops on one repo is how merge pain starts. Resume only one.
- **2026-08-05 — this file created, queue built from measurement rather than from the handoff notes.** Both handoff claims were checked: the em-dash counts (7 / 4) were right, and `body{background:#050b13}` was right in substance (it is `var(--navy)`, defined as `#050b13`). The suspected funnel trap — mobile visitors bounced off the new calculator and quote pages — **does not exist**, and item 1's real defect was found while checking it.
- **2026-08-05 — iteration 1, item 1 done (`545aaa8`).** The redirect is an **allow-list** now: the homepage redirects to `mobile.html`, everything else stays on the page the visitor asked for. Deny-list → allow-list is the load-bearing half — the old shape swallowed every page added after it, which is how the calculator and quoter escaped by *not loading the script* rather than by being spared. **Query strings now survive** alongside the hash, so a mobile visitor from an Instagram link keeps `utm_source`/`utm_campaign` instead of having attribution stripped at the door. **Verified in a browser rather than read off the diff:** all six previously-trapped pages land on themselves at 390px with no horizontal overflow and zero elements past the viewport; the homepage still redirects at 390 and 500 and stays put at 1440. ⚠️ **One false alarm worth recording:** an early probe read `/ @1440px -> /mobile.html` and looked like a regression. It was the harness — `resize_window` under 768px puts the pane into Android emulation, so `pointer: coarse` and a mobile UA stay true inside a wide iframe and the second redirect condition fires. Measure desktop behaviour at a real desktop viewport, not in a wide iframe inside a narrow window. Salesforce web-to-lead ids and the honeypot checked intact in `index`, `mobile` and `contact`.
- **Next: item 2, the mobile light conversion**, staged — (a) token layer and body/hero first.
