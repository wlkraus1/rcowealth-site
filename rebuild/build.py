#!/usr/bin/env python3
"""
Generates every rebuilt page from ONE shell, so the header, footer, branding,
disclosure and nav cannot drift page to page. Run: python3 rebuild/build.py

Tyler, 2026-08-07: "keep the live version idea and implement these new designs
and less of a word salad and cleaner pages not all crammed on a home screen"
plus "this new revamp takes away a bit from wealth management which aum is
still needed". So: multi-page, and wealth management gets its own page with
equal billing to protection rather than being a footnote under life insurance.
"""
import pathlib, re

OUT = pathlib.Path(__file__).parent
NAV = [("index.html","Home"),("wealth.html","Wealth"),("protection.html","Protection"),
       ("planning.html","Planning"),("advisor.html","Your advisor"),("contact.html","Contact")]

LEGAL = ("Rae &amp; Co Capital, LLC (d/b/a RcoWealth) is a South Carolina registered investment adviser. "
 "Registration does not imply a certain level of skill or training. Investing involves risk, including "
 "possible loss of principal. Insurance products are subject to underwriting and carrier approval; "
 "commissions may create a conflict of interest and are disclosed. This website is for informational "
 "purposes only and should not be treated as individualized investment, tax, legal, or insurance advice.")

def shell(slug, title, desc, body, canvas=False):
    nav = "\n".join(
        f'      <a href="{h}"{" aria-current=\"page\"" if h==slug else ""}>{t}</a>'
        for h,t in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#06111f">
<link rel="icon" href="../favicon.ico?v=goldleaf-20260521-1647">
<link rel="stylesheet" href="rco.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hd">
  <div class="wrap bar">
    <a class="brand" href="index.html" aria-label="Rae &amp; Co Capital home"><img src="../assets/rae-co-logo-header.png" alt="Rae &amp; Co Capital Wealth Management"></a>
    <button class="menu" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav id="nav" aria-label="Main">
{nav}
    </nav>
    <a class="callbtn" href="tel:+18645588440">864-558-8440</a>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="ft">
  <div class="wrap">
    <div class="cols">
      <div>
        <img src="../assets/rae-co-logo-light.png" alt="Rae &amp; Co Capital">
        <p style="font:400 14px/1.6 var(--sans);margin:0;max-width:34ch;color:rgba(246,239,224,.72)">
          Veteran-owned, 100% virtual wealth management and protection planning, based in Greenville, South Carolina.</p>
      </div>
      <div><h4>Start</h4>
        <a href="https://app.back9ins.com/apply/rcowealth?utm_source=website&amp;utm_medium=internal&amp;utm_campaign=rebuild&amp;utm_content=footer" target="_blank" rel="noopener">Quote &amp; apply</a>
        <a href="../life-insurance-calculator.html">Coverage calculator</a>
        <a href="planning.html">Buy a plan</a>
      </div>
      <div><h4>Firm</h4>
        <a href="advisor.html">Your advisor</a>
        <a href="wealth.html">Wealth management</a>
        <a href="protection.html">Protection</a>
        <a href="contact.html">Contact</a>
      </div>
      <div><h4>Legal</h4>
        <a href="../disclosures.html">Disclosures</a>
        <a href="../form-crs.html">Form CRS</a>
        <a href="../privacy.html">Privacy</a>
        <a href="../client-login.html">Client login</a>
      </div>
    </div>
    <p class="legal">{LEGAL}</p>
  </div>
</footer>
<script src="rco.js"></script>
</body>
</html>
"""

# ---------------------------------------------------------------- HOME
HOME = """
<section class="section" style="position:relative;overflow:hidden;padding-top:clamp(48px,6vw,86px)">
  <canvas data-field aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;z-index:0"></canvas>
  <div class="wrap" style="position:relative;z-index:2;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(320px,.95fr);gap:clamp(26px,4vw,56px);align-items:center">
    <div>
      <p class="kicker">Veteran-owned &middot; 100% virtual &middot; South Carolina RIA</p>
      <h1>Money is <em class="g">behavior,</em> not math.</h1>
      <p class="lede">Investments, retirement income, planning, and protection, coordinated by one Marine Corps veteran who answers the phone. Start any of it yourself, tonight, without an appointment.</p>
      <div class="acts">
        <a class="btn btn-ink" data-magnetic href="#paths">Start it yourself <span class="arr">&rarr;</span></a>
        <a class="btn-line" href="https://scheduler.zoom.us/raecocapital/introductory-consultation" target="_blank" rel="noopener">Or book a call</a>
      </div>
      <p style="margin:28px 0 0;font:600 13px/1.6 var(--sans);color:var(--muted)"><b style="color:var(--ink)">Series 65 fiduciary</b> &middot; Assets custodied at Charles Schwab &middot; 40+ insurance carriers</p>
    </div>
    <div class="tool" data-rv>
      <p class="tag" style="font:800 12px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase;color:var(--gold-ink);margin:0 0 6px">60-second answer</p>
      <h3 style="margin-bottom:20px">What would your family need if your income stopped?</h3>
      <div class="chips" role="group" aria-label="What are you protecting?">
        <button class="chip" type="button" aria-pressed="true" data-add="250000">A home</button>
        <button class="chip" type="button" aria-pressed="true" data-add="80000">Kids' education</button>
        <button class="chip" type="button" aria-pressed="false" data-add="15000">Final expenses</button>
      </div>
      <div class="frow">
        <label for="inc">Your income <output id="incOut">$75,000</output></label>
        <input type="range" id="inc" min="20000" max="400000" step="5000" value="75000" aria-label="Your annual income">
      </div>
      <div class="readout">
        <div><small>Rough coverage need</small><span class="num" id="need">$1,080,000</span></div>
        <a id="full" href="../life-insurance-calculator.html">Run the full number &rarr;</a>
      </div>
      <p class="fine">Ten years of income, plus what you selected. A starting point, not advice.</p>
    </div>
  </div>
</section>

<section class="section cream" id="paths">
  <div class="wrap center">
    <p class="kicker center" data-rv>No appointment needed</p>
    <h2 data-rv>Shop it, price it, <em class="g">start it</em>.</h2>
    <p class="lede" data-rv>Three ways in. Every one of them finishes without talking to anyone.</p>
    <div class="grid g3 stagger" data-rv style="margin-top:38px;text-align:left">
      <a class="card" style="text-decoration:none;display:flex;flex-direction:column" href="protection.html">
        <p class="tag">Protection</p><h3>Quote it and apply</h3>
        <p>Real pricing from 40+ carriers, application and e-sign in one sitting.</p>
        <span class="btn-line" style="margin-top:18px">See protection &rarr;</span>
      </a>
      <a class="card" style="text-decoration:none;display:flex;flex-direction:column" href="wealth.html">
        <p class="tag">Wealth</p><h3>Grow and draw it down</h3>
        <p>Portfolios at Schwab, retirement income, 1% a year with a $750 annual minimum.</p>
        <span class="btn-line" style="margin-top:18px">See wealth management &rarr;</span>
      </a>
      <a class="card" style="text-decoration:none;display:flex;flex-direction:column" href="planning.html">
        <p class="tag">Planning</p><h3>Buy a plan outright</h3>
        <p>Flat fees from $750, published, one time. Pay by card and start.</p>
        <span class="btn-line" style="margin-top:18px">See the plans &rarr;</span>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap" style="display:grid;grid-template-columns:minmax(260px,.8fr) minmax(0,1.2fr);gap:clamp(28px,5vw,64px);align-items:center">
    <figure style="margin:0" data-rv>
      <img src="../assets/tyler-krause.jpg" alt="Tyler Krause, Founder and Private Wealth Advisor" style="width:100%;aspect-ratio:7/10;object-fit:cover;object-position:50% 22%;border-radius:14px;box-shadow:0 40px 90px -46px rgba(6,17,31,.55)">
      <figcaption style="margin-top:12px;text-align:center;font:700 11px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;color:var(--gold-ink)">Greenville, South Carolina</figcaption>
    </figure>
    <div>
      <p class="kicker" data-rv>Your advisor</p>
      <h2 data-rv>Tyler Krause</h2>
      <p style="font:700 12.5px/1.5 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--gold-ink);margin:0 0 24px" data-rv>Founder &amp; Private Wealth Advisor &middot; U.S. Marine Corps veteran</p>
      <p class="lede" data-rv>I built Rae &amp; Co around a simple idea: protect the household first, then organize the money around the life it needs to support.</p>
      <p class="lede" data-rv>You work directly with me. One person who answers the phone and coordinates coverage, planning, and wealth decisions together.</p>
      <div class="acts" data-rv><a class="btn btn-ink" href="advisor.html">More about me <span class="arr">&rarr;</span></a></div>
    </div>
  </div>
</section>
"""

# ---------------------------------------------------------------- WEALTH
WEALTH = """
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <p class="kicker" data-rv>Wealth management</p>
    <h1 data-rv>The portfolio is the <em class="g">easy</em> part.</h1>
    <p class="lede" data-rv>Anyone can buy index funds. The work is sequencing withdrawals, keeping taxes from eating the gains, and not selling at the bottom because a headline scared you. That is the part I am paid for.</p>
    <div class="acts" data-rv>
      <a class="btn btn-ink" data-magnetic href="https://scheduler.zoom.us/raecocapital/introductory-consultation" target="_blank" rel="noopener">Start a portfolio review <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="planning.html">Or buy a plan first</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid g3 stagger" data-rv>
      <div class="card"><p class="tag">Investments</p><h3>Portfolio management</h3>
        <p style="margin-bottom:14px">Built around what the money is for, not around a model number.</p>
        <ul class="ticks"><li>Allocation matched to the actual goal and time horizon</li><li>Tax-aware placement across taxable, Roth and traditional</li><li>Rebalancing with a reason, not on a calendar</li><li>Held at Charles Schwab in your name</li></ul></div>
      <div class="card"><p class="tag">Retirement income</p><h3>Turning it into a paycheck</h3>
        <p style="margin-bottom:14px">The switch from saving to spending is where small mistakes get expensive.</p>
        <ul class="ticks"><li>Withdrawal order and sequencing</li><li>Social Security timing</li><li>Cash reserve sizing so a bad year is not a forced sale</li><li>Survivor income if one of you goes first</li></ul></div>
      <div class="card"><p class="tag">Coordination</p><h3>One view, not five</h3>
        <p style="margin-bottom:14px">Investments, insurance, taxes and planning decided together.</p>
        <ul class="ticks"><li>Beneficiaries and titling actually checked</li><li>Coverage gaps caught before they matter</li><li>One person accountable for the whole picture</li></ul></div>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap center">
    <p class="kicker center" data-rv>What it costs</p>
    <h2 data-rv>1% a year. <em class="g" style="color:var(--gold-2)">$750 annual minimum.</em></h2>
    <p class="lede" data-rv style="margin-left:auto;margin-right:auto">Billed quarterly under a signed advisory agreement. No commission on investments, no product quotas, no sales desk above me.</p>
    <div class="grid g3 stagger" data-rv style="margin-top:36px;text-align:left">
      <div class="card"><p class="tag">Custody</p><h3 style="font-size:22px">Charles Schwab</h3><p>Your money sits with Schwab in your name. I never hold it, and you can see it any time.</p></div>
      <div class="card"><p class="tag">Standard</p><h3 style="font-size:22px">Series 65 fiduciary</h3><p>Held to a fiduciary standard on advisory work. Insurance commissions are a separate, disclosed conflict.</p></div>
      <div class="card"><p class="tag">Honest limit</p><h3 style="font-size:22px">When not to hire me</h3><p>On a small balance the $750 minimum is a poor deal. If that is you, buy a flat-fee plan instead and invest it yourself.</p></div>
    </div>
    <div class="acts" data-rv style="justify-content:center;margin-top:36px">
      <a class="btn btn-gold" href="https://scheduler.zoom.us/raecocapital/introductory-consultation" target="_blank" rel="noopener">Book a portfolio review <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="planning.html">See flat-fee planning</a>
    </div>
    <p style="margin:26px auto 0;max-width:74ch;font:400 12px/1.65 var(--sans);color:rgba(244,239,228,.5)" data-rv>Advisory fees are 1% per year of assets under management with a $750 annual minimum, billed quarterly under a signed advisory agreement. Investing involves risk including possible loss of principal. No advice is provided until that agreement is in place.</p>
  </div>
</section>
"""

# ---------------------------------------------------------------- PROTECTION
PROTECTION = """
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <p class="kicker" data-rv>Protection</p>
    <h1 data-rv>Coverage is the part that <em class="g">cannot wait</em> for a good year.</h1>
    <p class="lede" data-rv>Pick what is on your mind. Every answer names what it solves, what it costs you, and when it is the wrong tool, because knowing when not to buy something is the part most people never get told.</p>
    <div class="acts" data-rv>
      <a class="btn btn-gold" data-magnetic href="https://app.back9ins.com/apply/rcowealth?utm_source=website&amp;utm_medium=internal&amp;utm_campaign=rebuild&amp;utm_content=protection_hero" target="_blank" rel="noopener">Quote and apply now <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="../life-insurance-calculator.html">Run the coverage numbers</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="pgrid" data-rv>
      <div class="plist" role="tablist" aria-label="Protection options">
        <button class="pbtn" role="tab" aria-selected="true"  data-p="term"><small>Start here</small>Term life</button>
        <button class="pbtn" role="tab" aria-selected="false" data-p="di"><small>Income</small>Disability income</button>
        <button class="pbtn" role="tab" aria-selected="false" data-p="perm"><small>Permanent</small>Whole &amp; universal life</button>
        <button class="pbtn" role="tab" aria-selected="false" data-p="iul"><small>The complicated one</small>Indexed universal life</button>
        <button class="pbtn" role="tab" aria-selected="false" data-p="ltc"><small>Later years</small>Long-term care</button>
        <button class="pbtn" role="tab" aria-selected="false" data-p="fe"><small>Small and specific</small>Final expense</button>
      </div>
      <div class="ppanel" id="ppanel" role="tabpanel" aria-live="polite"></div>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap center">
    <p class="cnum" data-rv>40+</p>
    <p class="lede" data-rv style="margin:8px auto 0;max-width:50ch">carriers shopped on one application, rather than one company's shelf. You see the pricing we see.</p>
    <div class="cnames" data-rv>
      <span>Prudential</span><span>Lincoln Financial</span><span>Pacific Life</span><span>John Hancock</span><span>Transamerica</span><span>Protective</span>
      <span>Nationwide</span><span>Principal</span><span>Symetra</span><span>Mutual of Omaha</span><span>Corebridge</span><span>Securian</span>
      <span>Banner Life</span><span>Allianz</span><span>Thrivent</span><span>SBLI</span><span>MassMutual Ascend</span><span>North American</span>
    </div>
    <div class="acts" data-rv style="justify-content:center;margin-top:34px">
      <a class="btn btn-gold" href="https://app.back9ins.com/apply/rcowealth?utm_source=website&amp;utm_medium=internal&amp;utm_campaign=rebuild&amp;utm_content=protection_carriers" target="_blank" rel="noopener">Start my quote <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="../types-of-life-insurance.html">Read the full product guide</a>
    </div>
    <p style="margin:26px auto 0;max-width:78ch;font:400 12px/1.65 var(--sans);color:rgba(244,239,228,.5)" data-rv>Rae &amp; Co Capital is compensated by commission on insurance placed, and permanent products generally pay more than term. That is a conflict of interest and it is disclosed in our Form CRS. Insurance is optional and never required to work with the firm. Availability, pricing and features vary by product, state, health and underwriting.</p>
  </div>
</section>
"""

# ---------------------------------------------------------------- PLANNING
TIERS = [
 ("Foundations","$750","For a clear starting plan around one or two priorities.",
  ["Discovery meeting plus a plan-delivery meeting","Cash flow and emergency fund review",
   "Debt pay-down vs invest analysis, ranked by your actual rates","Retirement savings starting roadmap",
   "Written one-page action plan you keep","30 days of email follow-up"],
  "https://square.link/u/VJZxUhJ9","Start Foundations",False),
 ("Household","$2,000","For a full picture, usually a couple with a few moving parts.",
  ["Everything in Foundations, plus","Full household cash flow and net worth build-out",
   "Goal planning: retirement, major purchases, education","Insurance needs review, life and disability gaps",
   "Tax-aware account strategy, Roth vs traditional and contribution order",
   "Two working sessions plus a delivery meeting","60 days of email follow-up"],
  "https://square.link/u/23AsoUVF","Start Household",True),
 ("Household + Implementation","$3,000","For help executing, not just a document.",
  ["Everything in Household, plus","Guided implementation support","Account setup walkthroughs",
   "Beneficiary and titling review","Up to three additional working sessions",
   "Completed within the six-month window"],
  "https://square.link/u/oUQEsSoQ","Start Implementation",False),
]
def tier_html(t):
    name,price,forwho,bullets,link,cta,best=t
    badge='<p class="tbadge">Most chosen</p>' if best else ''
    lis="".join(f"<li>{b}</li>" for b in bullets)
    return f"""<div class="tier{' best' if best else ''}">{badge}
        <p class="ttag">{name}</p>
        <p class="tprice">{price} <small>one time</small></p>
        <p class="tfor">{forwho}</p>
        <ul class="ticks">{lis}</ul>
        <a class="tbuy" href="{link}" target="_blank" rel="noopener">{cta} <span class="arr">&rarr;</span></a>
      </div>"""

PLANNING = """
<section class="section" style="padding-bottom:0">
  <div class="wrap center">
    <p class="kicker center" data-rv>Financial planning</p>
    <h1 data-rv>Flat fee. Published. <em class="g">Buy it now.</em></h1>
    <p class="lede" data-rv style="margin-left:auto;margin-right:auto">No hourly, no retainer, and no discovery call before you are allowed to see a price. Here is exactly what lands in your hands for each one.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="tiergrid stagger" data-rv>
      """ + "\n      ".join(tier_html(t) for t in TIERS) + """
    </div>
    <p class="tnote" data-rv>Paying starts the engagement. The written planning agreement comes to you to sign straight after, and the discovery meeting is part of the work rather than a sales call you have to pass first.</p>
    <p style="margin:22px auto 0;max-width:80ch;text-align:center;font:400 12px/1.65 var(--sans);color:var(--muted)" data-rv>Flat fee agreed in writing before any work begins. One-time engagement completed within six months; it is not a subscription. If we stop early, any unearned prepaid portion is returned. Insurance is optional and never required through the firm. Planning is analysis and education; there are no performance promises, and investing involves risk including loss of principal.</p>
  </div>
</section>

<section class="section cream">
  <div class="wrap center">
    <h2 data-rv>Not sure which one?</h2>
    <p class="lede" data-rv style="margin-left:auto;margin-right:auto">Most households land on Household. If you only have one or two questions, Foundations is enough. If in doubt, ask me and I will tell you the cheaper answer when it is the right one.</p>
    <div class="acts" data-rv style="justify-content:center">
      <a class="btn btn-ink" href="contact.html">Ask which one fits <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="wealth.html">Or see ongoing management</a>
    </div>
  </div>
</section>
"""

# ---------------------------------------------------------------- ADVISOR
ADVISOR = """
<section class="section">
  <div class="wrap" style="display:grid;grid-template-columns:minmax(260px,.8fr) minmax(0,1.2fr);gap:clamp(28px,5vw,64px);align-items:start">
    <figure style="margin:0;position:sticky;top:96px" data-rv>
      <img src="../assets/tyler-krause.jpg" alt="Tyler Krause, Founder and Private Wealth Advisor" style="width:100%;aspect-ratio:7/10;object-fit:cover;object-position:50% 22%;border-radius:14px;box-shadow:0 40px 90px -46px rgba(6,17,31,.55)">
      <figcaption style="margin-top:12px;text-align:center;font:700 11px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;color:var(--gold-ink)">Greenville, South Carolina</figcaption>
    </figure>
    <div>
      <p class="kicker" data-rv>Your advisor</p>
      <h1 data-rv style="font-size:clamp(44px,5.6vw,78px)">Tyler Krause</h1>
      <p style="font:700 12.5px/1.5 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--gold-ink);margin:0 0 26px" data-rv>Founder &amp; Private Wealth Advisor &middot; U.S. Marine Corps veteran</p>
      <p class="lede" data-rv>I built Rae &amp; Co around a simple idea: protect the household first, then organize the money around the life it needs to support.</p>
      <p class="lede" data-rv>You work directly with me. One person who answers the phone and coordinates coverage, planning, and wealth decisions together.</p>
      <div class="badges" data-rv>
        <div class="badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 3v5c0 4.4-3 8.4-7 10-4-1.6-7-5.6-7-10V6l7-3z"/><path d="M9 12l2 2 4-4"/></svg>
          <b>15+ years</b><span>Insurance &amp; financial services</span></div>
        <div class="badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 21h16M6 21V10M10 21V10M14 21V10M18 21V10M3 10h18L12 4 3 10z"/></svg>
          <b>Series 65</b><span>Investment Adviser Representative, fiduciary standard</span></div>
        <div class="badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="4" width="17" height="16" rx="2"/><circle cx="12" cy="12" r="3.4"/><path d="M12 10.2v1.8l1.2 1.2"/></svg>
          <b>Custody</b><span>Client assets held at Charles Schwab</span></div>
      </div>
      <p style="margin:20px 0 0;font:600 12.5px/1.6 var(--sans);color:var(--muted)" data-rv>Also: South Carolina Life, Accident &amp; Health licensed &middot; Certified Corporate Financial Planning Analyst (CCFPA) &middot; Multiple degrees, including an M.S. in Psychology from Arizona State.</p>
      <div class="acts" data-rv style="margin-top:30px"><a class="btn btn-ink" data-magnetic href="https://scheduler.zoom.us/raecocapital/introductory-consultation" target="_blank" rel="noopener">Book your call now <span class="arr">&rarr;</span></a></div>
    </div>
  </div>
</section>
"""

# ---------------------------------------------------------------- CONTACT
CONTACT = """
<section class="section">
  <div class="wrap" style="display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(28px,5vw,60px);align-items:start">
    <div>
      <p class="kicker" data-rv>Start here</p>
      <h1 data-rv style="font-size:clamp(42px,5.2vw,72px)">One call. <em class="g">No pitch.</em></h1>
      <p class="lede" data-rv>Tell me what is on your mind and I will tell you whether I can help. If the answer is that you do not need me yet, that is the answer you will get.</p>
      <div class="clines" data-rv>
        <a href="tel:+18645588440"><b>Call</b>864-558-8440</a>
        <a href="https://scheduler.zoom.us/raecocapital/introductory-consultation" target="_blank" rel="noopener"><b>Book</b>Pick a time that suits you</a>
        <span><b>Where</b>100% virtual, serving South Carolina</span>
      </div>
    </div>
    <form class="lform campaign-form contact-lead-form" data-rv id="leadForm"
          action="https://pi-nas.tail34488a.ts.net/" method="POST"
          data-campaign="website-general-consultation" data-asset="rebuild-contact" data-form-purpose="consultation-request">
      <input type="hidden" name="oid" value="00Dfn00000AW6kiEAD">
      <input type="hidden" name="retURL" value="https://rcowealth.com/thank-you.html">
      <input type="hidden" name="lead_source" value="Web">
      <input type="hidden" name="company" value="Individual / Household">
      <input type="hidden" name="00Nfn0000089jHR" value="Website">
      <label class="hp2" aria-hidden="true">Website<input name="website_url" autocomplete="off" tabindex="-1" data-honeypot="true"></label>
      <h3>Send a note</h3>
      <p class="lsub">Replies come from me, usually the same day.</p>
      <div class="fgrid">
        <div class="fld2"><label for="first_name">First name</label><input id="first_name" name="first_name" autocomplete="given-name" required></div>
        <div class="fld2"><label for="last_name">Last name</label><input id="last_name" name="last_name" autocomplete="family-name" required></div>
        <div class="fld2"><label for="email">Email</label><input id="email" type="email" name="email" autocomplete="email" required></div>
        <div class="fld2"><label for="phone">Phone</label><input id="phone" type="tel" name="phone" autocomplete="tel"></div>
        <div class="fld2 full"><label for="interest">What is this about?</label>
          <select id="interest" name="00Nfn0000089jXZ"><option>Not sure yet</option><option>Investments</option><option>Life insurance / protection</option><option>Both investments and insurance</option></select></div>
        <div class="fld2 full"><label for="next_step">Preferred next step</label>
          <select id="next_step" name="preferred_next_step_display"><option>Focused intro call</option><option>Email reply first</option><option>Life insurance planning</option><option>Portfolio or retirement review</option></select></div>
        <div class="fld2 full"><label for="description">Anything useful to know</label>
          <textarea id="description" name="description" placeholder="Example: I am five years from retirement and want to know if the plan holds up."></textarea></div>
        <div class="checks2">
          <label class="ckline"><input type="checkbox" name="00NbV000003Urbb" value="1">Yes, I would like to receive Rae &amp; Co Capital market notes and educational updates.</label>
          <label class="ckline"><input type="checkbox" name="00NbV000003ZxDB" value="1">I consent to receive text messages from Rae &amp; Co Capital at the phone number provided, including follow-up about my inquiry. Message and data rates may apply. Consent is not required to work with Rae &amp; Co Capital.</label>
        </div>
      </div>
      <button class="btn btn-ink" type="submit" style="width:100%;margin-top:18px">Send it <span class="arr">&rarr;</span></button>
      <p class="lfine">Submitting this form does not create an advisory relationship. Do not include sensitive personal financial information. Rae &amp; Co Capital does not provide individualized advice until an advisory agreement is in place.</p>
    </form>
  </div>
</section>
"""

PAGES = [
 ("index.html","Rae &amp; Co Capital | Veteran-Owned Virtual Wealth Management","Veteran-owned, 100% virtual wealth management and protection planning in Greenville, South Carolina. Quote, price and start it yourself.",HOME),
 ("wealth.html","Wealth Management | Rae &amp; Co Capital","Portfolio management and retirement income at 1% a year with a $750 annual minimum. Assets custodied at Charles Schwab.",WEALTH),
 ("protection.html","Protection Planning | Rae &amp; Co Capital","Term, disability, permanent, long-term care and final expense explained plainly. Quote and apply across 40+ carriers.",PROTECTION),
 ("planning.html","Financial Planning Fees | Rae &amp; Co Capital","Flat-fee financial planning from $750. Published prices, real deliverables, buy it online.",PLANNING),
 ("advisor.html","Tyler Krause, Your Advisor | Rae &amp; Co Capital","Marine Corps veteran, Series 65 fiduciary, CCFPA. One person who answers the phone.",ADVISOR),
 ("contact.html","Contact | Rae &amp; Co Capital","One call, no pitch. Reach Tyler Krause at Rae &amp; Co Capital.",CONTACT),
]

for slug,title,desc,body in PAGES:
    (OUT/slug).write_text(shell(slug,title,desc,body),encoding="utf-8")
    print("wrote",slug)
print("done:",len(PAGES),"pages")
