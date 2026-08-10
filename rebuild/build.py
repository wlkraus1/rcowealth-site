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

# ------------------------------------------------------------ CARRIER WALL
# Layout approved by Tyler 2026-08-10 from a mockup: gold numeral, serif claim,
# rule-flanked proof strip, 5x2 logo grid, expandable full roster.
#
# LOGOS: drop a file at assets/carriers/<slug>.svg (or .png) and rerun this
# script - the cell switches to the image automatically, no code change, and it
# is sized by optical area from the file's own dimensions. Art must already be
# cream (#f6ecd0); there is no invert filter, because inverting flattens the
# warm tone the rest of the band uses. A slug with no file falls back to a
# styled wordmark, so a missing logo degrades instead of leaving a hole.
FEATURED = [
 ("Prudential","prudential",""),   ("Lincoln Financial","lincoln-financial",""),
 ("Pacific Life","pacific-life",""), ("John Hancock","john-hancock",""),
 ("Mutual of Omaha","mutual-of-omaha",""),
 ("Nationwide","nationwide","s"),  ("Principal","principal","s"),
 ("Protective","protective","s"),  ("Banner Life","banner-life","s"),
 ("Transamerica","transamerica",""),
]
# Verified 2026-08-10 against BackNine's published Life carrier list at
# back9ins.com/carriers (the Life tab, not the Annuity tab). 53 raw entries,
# minus 5 NY-domiciled twins of carriers already listed and 2 second legal
# entities of the same brand, leaves 46 distinct life brands. All 10 featured
# logos are on that list.
#
# The previous roster was hand-written from memory and had four wrong entries:
# Thrivent (not a BackNine life carrier at all), MassMutual Ascend (that is the
# annuity entity - the life one is MassMutual), American General (legacy name,
# now Corebridge, already listed) and Legal & General (BackNine lists it as
# Banner, already a logo). Never hand-write this list again - re-pull it.
ROSTER = ["Allianz", "American Heritage Life", "Ameritas", "Assurity", "Brighthouse Financial",
          "Cincinnati Life", "Corebridge", "EquiTrust", "F&amp;G", "Fidelity Life", "Foresters",
          "Gerber Life", "Great Western", "Guardian", "LaFayette Life", "Liberty Mutual Life",
          "Life of the Southwest", "MassMutual", "National Life Group", "National Western",
          "New York Life", "North American", "OneAmerica", "Oxford Life", "Penn Mutual",
          "Petersen International", "SBLI", "Sagicor", "Securian", "State Life",
          "Sun Life Financial", "Symetra", "U.S. Life", "United Home Life", "United of Omaha",
          "William Penn"]

def art_size(p):
    """Intrinsic width/height, stdlib only: PNG straight out of the IHDR header,
    SVG out of the viewBox."""
    if p.suffix == ".svg":
        m = re.search(r'viewBox="[\d.\-]+\s+[\d.\-]+\s+([\d.]+)\s+([\d.]+)"', p.read_text())
        return (float(m.group(1)), float(m.group(2))) if m else (1.0, 1.0)
    b = p.read_bytes()[16:24]
    return int.from_bytes(b[:4], "big"), int.from_bytes(b[4:], "big")

def carrier_cells():
    """Logos are sized by optical area, not by a flat max-height. A flat height
    makes a 3.7:1 wordmark like Prudential render twice as wide as a stacked
    2:1 lockup like Pacific Life, and the wall reads lopsided. Scaling by
    1/sqrt(aspect) holds the perceived mass even across the grid."""
    out = []
    for name, slug, cls in FEATURED:
        art = next((p for e in (".svg", ".png")
                    if (p := OUT.parent/"assets"/"carriers"/(slug+e)).exists()), None)
        if art:
            w, h = art_size(art)
            px = min(48, round(62 / (w/h) ** .5))
            inner = (f'<img src="../assets/carriers/{art.name}" alt="{name}" '
                     f'width="{round(w)}" height="{round(h)}" style="height:{px}px" decoding="async">')
        else:
            inner = f'<span class="wm {cls}">{name}</span>'
        out.append(f'      <div class="cell">{inner}</div>')
    return "\n".join(out)

# ------------------------------------------------------------- LEAD FORM
# THE thing the rebuild was missing. Live runs 9 of these; the rebuild had 1,
# so every self-service path ended offsite at BackNine or Square and nobody who
# looked-but-did-not-buy was ever captured. Tyler: "that is how we collect their
# data and reach out later."
#
# Wiring is byte-identical to the live forms and must stay that way: oid
# 00Dfn00000AW6kiEAD, POST to the Pi Funnel intake (queue-first -> FSC ->
# Telegram), retURL to the live thank-you page, honeypot named website_url.
# NEVER submit one of these while testing - it posts to the real org.
FORM_HIDDEN = """      <input type="hidden" name="oid" value="00Dfn00000AW6kiEAD">
      <input type="hidden" name="retURL" value="https://rcowealth.com/thank-you.html">
      <input type="hidden" name="lead_source" value="Web">
      <input type="hidden" name="company" value="Individual / Household">
      <input type="hidden" name="00Nfn0000089jHR" value="Website">
      <label class="hp2" aria-hidden="true">Website<input name="website_url" autocomplete="off" tabindex="-1" data-honeypot="true"></label>"""

FORM_CHECKS = """        <div class="checks2">
          <label class="ckline"><input type="checkbox" name="00NbV000003Urbb" value="1">Yes, I would like to receive Rae &amp; Co Capital market notes and educational updates.</label>
          <label class="ckline"><input type="checkbox" name="00NbV000003ZxDB" value="1">I consent to receive text messages from Rae &amp; Co Capital at the phone number provided, including follow-up about my inquiry. Message and data rates may apply. Consent is not required to work with Rae &amp; Co Capital.</label>
        </div>"""

FORM_FINE = ("Submitting this form does not create an advisory relationship. Do not include sensitive "
             "personal financial information. Rae &amp; Co Capital does not provide individualized "
             "advice until an advisory agreement is in place.")

def lead_form(campaign, asset, purpose, heading, blurb, interest, next_step,
              cta="Send it", placeholder="Example: I am five years from retirement and want to know if the plan holds up.",
              uid="", insurance=False):
    """One form, many pages. `uid` suffixes every id so two forms can share a
    page without colliding label[for] targets. `insurance` sets the same
    00NbV000002pcrh="Yes" flag the four live life-insurance forms carry, which
    is what routes the lead correctly in Salesforce - it is easy to miss because
    only the insurance pages set it."""
    i = lambda n: n + uid
    flag = ('\n      <input type="hidden" name="00NbV000002pcrh" value="Yes">'
            if insurance else "")
    return f"""<form class="lform campaign-form contact-lead-form" data-rv id="leadForm{uid}"
          action="https://pi-nas.tail34488a.ts.net/" method="POST"
          data-campaign="{campaign}" data-asset="{asset}" data-form-purpose="{purpose}">
{FORM_HIDDEN}
      <input type="hidden" name="00Nfn0000089jXZ" value="{interest}">{flag}
      <input type="hidden" name="preferred_next_step_display" value="{next_step}">
      <h2 class="sub">{heading}</h2>
      <p class="lsub">{blurb}</p>
      <div class="fgrid">
        <div class="fld2"><label for="{i('first_name')}">First name</label><input id="{i('first_name')}" name="first_name" autocomplete="given-name" required></div>
        <div class="fld2"><label for="{i('last_name')}">Last name</label><input id="{i('last_name')}" name="last_name" autocomplete="family-name" required></div>
        <div class="fld2"><label for="{i('email')}">Email</label><input id="{i('email')}" type="email" name="email" autocomplete="email" required></div>
        <div class="fld2"><label for="{i('phone')}">Phone</label><input id="{i('phone')}" type="tel" name="phone" autocomplete="tel"></div>
        <div class="fld2 full"><label for="{i('description')}">What would you like help with?</label>
          <textarea id="{i('description')}" name="description" placeholder="{placeholder}"></textarea></div>
{FORM_CHECKS}
      </div>
      <button class="btn btn-ink" type="submit" style="width:100%;margin-top:18px">{cta} <span class="arr">&rarr;</span></button>
      <p class="lfine">{FORM_FINE}</p>
    </form>"""

def form_section(kicker, h2, lede, form, cream=False):
    """Standard closing lead-capture band, so every ported page ends on a
    capture rather than a dead end."""
    return f"""
<section class="section{' cream' if cream else ''}">
  <div class="wrap split c">
    <div>
      <p class="kicker" data-rv>{kicker}</p>
      <h2 data-rv>{h2}</h2>
      <p class="lede" data-rv>{lede}</p>
      <div class="reachrow" data-rv style="max-width:420px">
        <a class="reach" href="tel:+18645588440"><span><b>Call</b>864-558-8440</span></a>
        <a class="reach" href="sms:+18645588440?&amp;body=Hi%20Tyler%2C%20I%20have%20a%20question%20about%20"><span><b>Text</b>Most people start here</span></a>
      </div>
    </div>
    {form}
  </div>
</section>
"""

def legal_page(h1, kicker, blocks):
    """Legal/utility pages must live INSIDE the shell. Before this they linked out
    to the old site, which had the old header and no route back - a one-way door
    Tyler hit while reviewing."""
    body = "\n".join(f'<h2 class="sub" style="margin-top:26px">{t}</h2><p style="font:400 15px/1.7 var(--sans);color:var(--muted);max-width:74ch">{b}</p>' for t,b in blocks)
    return f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <p class="kicker" data-rv>{kicker}</p>
    <h1 data-rv style="font-size:clamp(40px,5vw,68px)">{h1}</h1>
  </div>
</section>
<section class="section">
  <div class="wrap" data-rv>{body}
    <div class="acts" style="margin-top:34px"><a class="btn btn-ink" href="index.html">Back to Rae &amp; Co <span class="arr">&rarr;</span></a></div>
  </div>
</section>
"""

LEGAL = ("Rae &amp; Co Capital, LLC (d/b/a RcoWealth) is a South Carolina registered investment adviser. "
 "Registration does not imply a certain level of skill or training. Investing involves risk, including "
 "possible loss of principal. Insurance products are subject to underwriting and carrier approval; "
 "commissions may create a conflict of interest and are disclosed. This website is for informational "
 "purposes only and should not be treated as individualized investment, tax, legal, or insurance advice.")

# Social. Footer only, on purpose. Verified 2026-08-10 before linking anything:
# Instagram 115 posts / 55 followers, Facebook 77 followers with posts and reels,
# YouTube channel live with videos. TikTok (@rcowealth) has 5 followers and ZERO
# posts, so it is deliberately left off - an empty profile costs more credibility
# than the icon buys. Add it back the moment the reel batch starts posting there.
SOCIAL = """<div class="social">
          <a href="https://www.instagram.com/rcowealth/" target="_blank" rel="noopener" aria-label="Rae &amp; Co Capital on Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.07 1.2.05 1.8.25 2.2.42.6.22 1 .48 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c0 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2 0-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c0-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 1.8c-3.1 0-3.5 0-4.7.07-1.1.05-1.7.24-2.1.4-.5.2-.9.44-1.2.78-.35.34-.57.7-.77 1.2-.16.4-.35 1-.4 2.1C2.76 9.75 2.76 10.1 2.76 12s0 2.25.06 3.45c.05 1.1.24 1.7.4 2.1.2.5.42.86.77 1.2.33.34.7.57 1.2.77.4.16 1 .35 2.1.4 1.2.06 1.6.06 4.7.06s3.5 0 4.7-.06c1.1-.05 1.7-.24 2.1-.4.5-.2.87-.43 1.2-.77.35-.34.57-.7.77-1.2.16-.4.35-1 .4-2.1.06-1.2.06-1.55.06-3.45s0-2.25-.06-3.45c-.05-1.1-.24-1.7-.4-2.1-.2-.5-.42-.86-.77-1.2-.33-.34-.7-.58-1.2-.78-.4-.16-1-.35-2.1-.4C15.5 4 15.1 4 12 4zm0 3.1a4.9 4.9 0 1 1 0 9.8 4.9 4.9 0 0 1 0-9.8zm0 8.08a3.18 3.18 0 1 0 0-6.36 3.18 3.18 0 0 0 0 6.36zm6.24-8.28a1.14 1.14 0 1 1-2.29 0 1.14 1.14 0 0 1 2.29 0z"/></svg></a>
          <a href="https://www.facebook.com/RcoWealth" target="_blank" rel="noopener" aria-label="Rae &amp; Co Capital on Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.5-3.89 3.78-3.89 1.1 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.45 2.89h-2.33v6.99A10 10 0 0 0 22 12z"/></svg></a>
          <a href="https://www.youtube.com/@rcowealth" target="_blank" rel="noopener" aria-label="Rae &amp; Co Capital on YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.58 7.19a2.5 2.5 0 0 0-1.77-1.77C18.25 5 12 5 12 5s-6.25 0-7.81.42a2.5 2.5 0 0 0-1.77 1.77A26 26 0 0 0 2 12a26 26 0 0 0 .42 4.81 2.5 2.5 0 0 0 1.77 1.77C5.75 19 12 19 12 19s6.25 0 7.81-.42a2.5 2.5 0 0 0 1.77-1.77A26 26 0 0 0 22 12a26 26 0 0 0-.42-4.81zM10 15.02V8.98L15.2 12 10 15.02z"/></svg></a>
        </div>"""

ORIGIN = "https://rcowealth.com"

def asset_v(name):
    """Content hash appended to rco.css / rco.js. Without it a returning
    visitor keeps the cached copy after a deploy and sees the new HTML driven
    by the old stylesheet and old script - which is exactly how the retirement
    tool appeared dead during testing while its code was sitting right there.
    The favicon already did this by hand; now the two files that change every
    build do it automatically."""
    import hashlib
    return hashlib.sha1((OUT/name).read_bytes()).hexdigest()[:10]
# BackNine quote-and-apply, the only place on the site where someone can buy
# without talking to anyone. Append &utm_content=<where> at each call site.
B9 = ("https://app.back9ins.com/apply/rcowealth?utm_source=website&amp;utm_medium=internal"
      "&amp;utm_campaign=rebuild")

# STAGING keeps the whole rebuild out of the index while it lives at /rebuild/.
# Flip it to False in the same commit that moves these files to the site root,
# and every page swaps noindex for a real canonical in one build. Shipping the
# rebuild with the blanket noindex still on would take the site off Google.
STAGING = False

# Ported from the live site's head, which the rebuild had dropped entirely.
LD = """{
  "@context":"https://schema.org",
  "@type":"FinancialService",
  "name":"Rae & Co Capital, LLC",
  "alternateName":"RcoWealth",
  "description":"Veteran-owned, 100% virtual wealth management: investment management, retirement income, financial planning, and protection planning.",
  "url":"https://rcowealth.com",
  "telephone":"+1-864-558-8440",
  "email":"info@rcowealth.com",
  "areaServed":"US",
  "address":{"@type":"PostalAddress","addressRegion":"SC","addressCountry":"US"},
  "sameAs":["https://www.instagram.com/rcowealth/","https://www.facebook.com/RcoWealth","https://www.youtube.com/@rcowealth"],
  "founder":{"@type":"Person","name":"Tyler Krause","jobTitle":"Founder & Private Wealth Advisor","alumniOf":"Arizona State University","knowsAbout":["Behavioral finance","Psychology of money","Financial planning","Life insurance"]}
}"""

def shell(slug, title, desc, body, canvas=False):
    nav = "\n".join(
        f'      <a href="{h}"{" aria-current=\"page\"" if h==slug else ""}>{t}</a>'
        for h,t in NAV)
    url = ORIGIN + "/" + ("" if slug == "index.html" else slug)
    plain = re.sub(r"&amp;", "&", title)
    if STAGING:
        index_meta = '<meta name="robots" content="noindex, nofollow">'
    else:
        index_meta = (f'<link rel="canonical" href="{url}">\n'
                      f'<meta property="og:type" content="website">\n'
                      f'<meta property="og:site_name" content="Rae &amp; Co Capital">\n'
                      f'<meta property="og:title" content="{title}">\n'
                      f'<meta property="og:description" content="{desc}">\n'
                      f'<meta property="og:url" content="{url}">\n'
                      f'<meta property="og:image" content="{ORIGIN}/assets/rae-co-logo-header.png">\n'
                      f'<meta name="twitter:card" content="summary_large_image">\n'
                      f'<meta name="twitter:title" content="{title}">\n'
                      f'<meta name="twitter:description" content="{desc}">')
    ld = f'\n<script type="application/ld+json">{LD}</script>' if slug == "index.html" else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{index_meta}
<meta name="theme-color" content="#06111f">
<link rel="icon" href="../favicon.ico?v=goldleaf-20260521-1647">
<link rel="stylesheet" href="rco.css?v={asset_v('rco.css')}">{ld}
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
    <span class="hdreach">
      <a class="callbtn" href="sms:+18645588440?&amp;body=Hi%20Tyler%2C%20I%20have%20a%20question%20about%20" aria-label="Text Rae &amp; Co Capital">Text</a>
      <a class="callbtn" href="tel:+18645588440">864-558-8440</a>
    </span>
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
        {SOCIAL}
      </div>
      <nav aria-label="Start"><p class="ftlabel">Start</p>
        <a href="https://app.back9ins.com/apply/rcowealth?utm_source=website&amp;utm_medium=internal&amp;utm_campaign=rebuild&amp;utm_content=footer" target="_blank" rel="noopener">Quote &amp; apply</a>
        <a href="life-insurance-calculator.html">Coverage calculator</a>
        <a href="planning.html">Buy a plan</a>
      </nav>
      <nav aria-label="Firm"><p class="ftlabel">Firm</p>
        <a href="advisor.html">Your advisor</a>
        <a href="wealth.html">Wealth management</a>
        <a href="protection.html">Protection</a>
        <a href="contact.html">Contact</a>
      </nav>
      <nav aria-label="Legal"><p class="ftlabel">Legal</p>
        <a href="disclosures.html">Disclosures</a>
        <a href="form-crs.html">Form CRS</a>
        <a href="privacy.html">Privacy</a>
        <a href="client-login.html">Client login</a>
      </nav>
    </div>
    <p class="legal">{LEGAL}</p>
  </div>
</footer>
<script src="rco.js?v={asset_v('rco.js')}"></script>
</body>
</html>
"""

# ---------------------------------------------------------------- HOME
HOME = """
<section class="section" style="position:relative;overflow:hidden;padding-top:clamp(48px,6vw,86px)">
  <canvas data-field aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;z-index:0"></canvas>
  <div class="wrap split a" style="position:relative;z-index:2">
    <div>
      <p class="kicker">Veteran-owned &middot; 100% virtual &middot; South Carolina RIA</p>
      <h1>Money is <em class="g">behavior,</em> not math.</h1>
      <p class="lede">Investments, retirement income, planning, and protection, coordinated by one Marine Corps veteran who answers the phone. Start any of it yourself, tonight, without an appointment.</p>
      <div class="acts">
        <a class="btn btn-ink" data-magnetic href="#paths">Start it yourself <span class="arr">&rarr;</span></a>
        <a class="btn-line" href="https://scheduler.zoom.us/raecocapital/introductory-consultation" target="_blank" rel="noopener">Or book a call</a>
      </div>
      <p style="margin:28px 0 0;font:600 13px/1.6 var(--sans);color:var(--muted)"><b style="color:var(--ink)">Series 65 fiduciary</b> &middot; Assets custodied at Charles Schwab &middot; 46 insurance carriers</p>
    </div>
    <div class="tool" data-rv>
      <p class="tag" style="font:800 12px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase;color:var(--gold-ink);margin:0 0 6px">60-second answer</p>
      <h2 class="sub" style="margin-bottom:20px">What would your family need if your income stopped?</h2>
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
        <a id="full" href="life-insurance-calculator.html">Run the full number &rarr;</a>
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
        <p>Real pricing from 46 carriers, application and e-sign in one sitting.</p>
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
  <div class="wrap">
    <p class="kicker" data-rv>The other half of the firm</p>
    <h2 data-rv style="max-width:19ch">Insurance protects it. <em class="g">Managing it</em> is the rest of the job.</h2>
    <p class="lede" data-rv style="max-width:64ch">Rae &amp; Co is a registered investment adviser that also places insurance, not an insurance agency with a planning page. Portfolios sit at Charles Schwab in your name, priced at 1% a year with a $750 annual minimum, and the retirement income work is where most of the value actually shows up.</p>
    <div class="grid g3 stagger" data-rv style="margin-top:38px">
      <div class="card"><p class="tag">Investments</p><h3>Held at Schwab, in your name</h3>
        <p>I never hold your money. Allocation is matched to the goal and the horizon, and rebalancing happens for a reason rather than on a calendar.</p></div>
      <div class="card"><p class="tag">Retirement income</p><h3>Turning it into a paycheck</h3>
        <p>Withdrawal order, Social Security timing, cash reserves sized so a bad year is not a forced sale, and survivor income if one of you goes first.</p></div>
      <div class="card"><p class="tag">The honest limit</p><h3>When not to hire me</h3>
        <p>On a small balance the $750 minimum is a poor deal. If that is you, buy a flat-fee plan and invest it yourself. I will say so before you ask.</p></div>
    </div>
    <div class="acts" data-rv style="margin-top:34px">
      <a class="btn btn-ink" data-magnetic href="wealth.html">See how management works <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="wealth.html#tool">Or check your retirement number</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split b">
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
{CARRIERWALL}
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

<section class="section cream" id="tool">
  <div class="wrap split a">
    <div>
      <p class="kicker" data-rv>60-second answer</p>
      <h2 data-rv style="max-width:17ch">Will the money still be there at <em class="g">85</em>?</h2>
      <p class="lede" data-rv>Protection has a calculator, planning has a price list, and until now wealth had a phone number. Drag four sliders and see whether the plan holds. Nothing is stored and no contact details are asked for.</p>
      <p class="lede" data-rv style="font-size:15px">The growth rate is yours to set, not mine to promise. Move it and watch how much the answer depends on an assumption nobody can guarantee. That sensitivity is the actual lesson.</p>
      <div class="acts" data-rv>
        <a class="btn btn-ink" href="contact.html">Have it checked properly <span class="arr">&rarr;</span></a>
        <a class="btn-line" href="planning.html">Or buy a flat-fee plan</a>
      </div>
    </div>
    <div class="tool" data-rv>
      <p class="tag" style="font:800 12px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase;color:var(--gold-ink);margin:0 0 6px">Retirement income check</p>
      <h3 style="margin-bottom:18px">What would you retire on?</h3>
      <div class="chips" role="group" aria-label="Retirement age">
        <button class="rchip" type="button" aria-pressed="false" data-age="60">Retire at 60</button>
        <button class="rchip" type="button" aria-pressed="true"  data-age="65">at 65</button>
        <button class="rchip" type="button" aria-pressed="false" data-age="70">at 70</button>
      </div>
      <div class="frow"><label for="wAge">Your age now <output id="wAgeOut">40</output></label>
        <input type="range" id="wAge" min="22" max="69" step="1" value="40" aria-label="Your age now"></div>
      <div class="frow"><label for="wPot">Saved so far <output id="wPotOut">$150,000</output></label>
        <input type="range" id="wPot" min="0" max="2000000" step="10000" value="150000" aria-label="Amount saved so far"></div>
      <div class="frow"><label for="wAdd">Added each month <output id="wAddOut">$1,000</output></label>
        <input type="range" id="wAdd" min="0" max="6000" step="50" value="1000" aria-label="Added each month"></div>
      <div class="frow"><label for="wRet">Growth you assume <output id="wRetOut">6.0%</output></label>
        <input type="range" id="wRet" min="2" max="9" step="0.5" value="6" aria-label="Assumed annual growth rate"></div>
      <div class="frow"><label for="wWant">Income you want <output id="wWantOut">$6,000/mo</output></label>
        <input type="range" id="wWant" min="1000" max="20000" step="250" value="6000" aria-label="Monthly income you want in retirement"></div>
      <div class="wresult" aria-live="polite">
        <p class="rlabel" id="wLabel">Monthly income this plan supports</p>
        <p class="rbig" id="wNum">$0</p>
        <p class="wbar" aria-hidden="true"><span id="wFill"></span></p>
        <div class="rline"><span>Income you want</span><b id="wWantEcho">$0</b></div>
        <div class="rline"><span id="wGapLabel">Short each month</span><b id="wGap">$0</b></div>
        <div class="ractions" style="margin-top:18px">
          <a class="btn btn-gold" id="wCta" href="contact.html">Close the gap <span class="arr">&rarr;</span></a>
        </div>
      </div>
      <p class="fine" id="wFine">An illustration built only from the numbers above, using your growth assumption and a 4% withdrawal rate. It is not a projection of any actual portfolio, not a promise of returns, and not individualized advice. It ignores taxes, fees, Social Security and inflation.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 class="sub" data-rv style="margin-bottom:26px">What managing the money actually covers.</h2>
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
      <a class="btn-line" href="life-insurance-calculator.html">Run the coverage numbers</a>
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

{CARRIERWALL}
"""

CARRIERWALL = """
<section class="section dark">
  <div class="wrap center">
    <p class="cnum" data-rv>{TOTAL}</p>
    <h2 class="cclaim" data-rv>life insurance carriers, available through one application</h2>
    <p class="lede" data-rv style="margin:14px auto 0;max-width:52ch">Compare coverage and pricing across leading life insurance carriers without filling out the same information over and over.</p>
    <p class="cstrip" data-rv><b>Independent access</b><i>&middot;</i><b>No single-carrier bias</b><i>&middot;</i><b>You see the pricing we see</b></p>
    <div class="cgrid" data-rv>
{CELLS}
    </div>
    <p class="cmore" data-rv>{MORE}</p>
    <div class="acts" data-rv style="justify-content:center;margin-top:30px">
      <a class="btn btn-gold" href="https://app.back9ins.com/apply/rcowealth?utm_source=website&amp;utm_medium=internal&amp;utm_campaign=rebuild&amp;utm_content=protection_carriers" target="_blank" rel="noopener">Start my quote <span class="arr">&rarr;</span></a>
    </div>
    <div style="margin-top:14px">
      <button class="btn-line" type="button" data-carriers aria-expanded="false" aria-controls="carrierlist"
        style="background:none;border:0;cursor:pointer">See all carriers</button>
    </div>
    <div class="cnames" id="carrierlist">
{ROSTERCELLS}
    </div>
    <p class="cnote" id="carriernote">That is the complete list, verified against BackNine's carrier roster. Availability varies by product, state, health and underwriting, so not every carrier can write every case, and the quoter shows the ones that can write yours.</p>
    <p style="margin:30px auto 0;max-width:78ch;font:400 12px/1.65 var(--sans);color:rgba(244,239,228,.5);border-top:1px solid rgba(244,239,228,.11);padding-top:24px" data-rv>Rae &amp; Co Capital is compensated by commission on insurance placed, and permanent products generally pay more than term. That is a conflict of interest and it is disclosed in our Form CRS. Insurance is optional and never required to work with the firm. Availability, pricing and features vary by product, state, health and underwriting.</p>
  </div>
</section>
"""

CARRIERWALL = (CARRIERWALL
  .replace("{TOTAL}", str(len(FEATURED)+len(ROSTER)))
  .replace("{MORE}", f"+ {len(ROSTER)} more, all named below")
  .replace("{CELLS}", carrier_cells())
  .replace("{ROSTERCELLS}", "".join(f"<span>{n}</span>" for n in ROSTER)))
PROTECTION = PROTECTION.replace("{CARRIERWALL}", CARRIERWALL)
# Same wall closes the home page, with its own utm_content so the two entry
# points stay separable in reporting.
HOME = HOME.replace("{CARRIERWALL}",
  CARRIERWALL.replace("utm_content=protection_carriers","utm_content=home_carriers"))

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
<section class="section" style="padding-bottom:0">
  <div class="wrap split b top">
    <figure style="margin:0" data-rv>
      <img src="../assets/tyler-krause.jpg" alt="Tyler Krause, Founder and Private Wealth Advisor" style="width:100%;aspect-ratio:7/10;object-fit:cover;object-position:50% 22%;border-radius:14px;box-shadow:0 40px 90px -46px rgba(6,17,31,.55)">
      <figcaption style="margin-top:12px;text-align:center;font:700 11px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;color:var(--gold-ink)">Greenville, South Carolina</figcaption>
    </figure>
    <div>
      <p class="kicker" data-rv>Your advisor</p>
      <h1 data-rv style="font-size:clamp(44px,5.6vw,78px)">Tyler Krause</h1>
      <p style="font:700 12.5px/1.5 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--gold-ink);margin:0 0 26px" data-rv>Founder &amp; Private Wealth Advisor &middot; U.S. Marine Corps veteran</p>
      <p class="lede" data-rv>Fifteen years in this industry taught me that the plan is rarely the problem. People usually know roughly what they should do. What stops them is that no one has organized it, priced it, or told them which part matters first.</p>
      <p class="lede" data-rv>So that is the job I built the firm around: protect the household, put the rest in an order that makes sense, and be one person who can be reached.</p>
      <div class="acts" data-rv><a class="btn btn-ink" data-magnetic href="https://scheduler.zoom.us/raecocapital/introductory-consultation" target="_blank" rel="noopener">Book your call now <span class="arr">&rarr;</span></a>
        <a class="btn-line" href="planning.html">Or just buy a plan</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="kicker" data-rv>The mission</p>
    <h2 data-rv style="max-width:20ch">Most money decisions are <em class="g">behavior</em>, not math.</h2>
    <div class="grid g3 stagger" data-rv style="margin-top:34px">
      <div class="card"><p class="tag">Why psychology</p><h3>The gap is not knowledge</h3>
        <p>I went and got a master&rsquo;s in psychology because I kept watching capable people know the right answer and not act on it. Understanding why is more useful than repeating the answer louder.</p></div>
      <div class="card"><p class="tag">Why protection first</p><h3>Coverage before growth</h3>
        <p>A portfolio does not survive an uninsured disaster. Protection is the cheapest, least glamorous part of a plan and it is the part that decides whether the rest survives contact with a bad year.</p></div>
      <div class="card"><p class="tag">Why one person</p><h3>No handoffs</h3>
        <p>You are not passed to a service team after the sale. The person who builds the plan is the person who answers the phone, which is only possible because the firm is deliberately small.</p></div>
    </div>
  </div>
</section>

<section class="section cream">
  <div class="wrap">
    <p class="kicker" data-rv>How it actually goes</p>
    <h2 data-rv style="max-width:16ch">Three steps, no mystery.</h2>
    <div class="grid g3 stagger" data-rv style="margin-top:34px">
      <div class="card"><p class="tag">Step one</p><h3>We agree the scope</h3>
        <p>You tell me what you are trying to solve. We agree the engagement and the flat fee in writing before any work begins. If you do not need me yet, I will say so.</p></div>
      <div class="card"><p class="tag">Step two</p><h3>I build it on your real numbers</h3>
        <p>Not a template. We walk through the reasoning behind every recommendation so you can explain it to your spouse without me in the room.</p></div>
      <div class="card"><p class="tag">Step three</p><h3>You leave able to act</h3>
        <p>A written plan you keep, in an order you can follow. Implement it yourself or have me help. Both are fine and only one of them costs more.</p></div>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <p class="kicker" data-rv>Where I draw lines</p>
    <h2 data-rv style="max-width:18ch">The things I will <em class="g" style="color:var(--gold-2)">not</em> do.</h2>
    <p class="lede" data-rv>Confidence in an adviser comes from knowing what they refuse, not from a list of services. These are in my Form ADV, not just on a website.</p>
    <div class="grid g2 stagger" data-rv style="margin-top:32px">
      <div class="card"><h3 style="font-size:22px">No hourly, no retainer</h3><p>Flat fees only, one time, completed within six months. If we stop early, the unearned portion comes back to you.</p></div>
      <div class="card"><h3 style="font-size:22px">No required insurance</h3><p>Insurance is never a condition of working with me. When you do buy it here, I am paid a commission, and that conflict is disclosed rather than buried.</p></div>
      <div class="card"><h3 style="font-size:22px">No pushing AUM that does not fit</h3><p>Management is 1% a year with a $750 annual minimum. On a small balance that is a poor deal, and I will tell you to buy a flat-fee plan and invest it yourself.</p></div>
      <div class="card"><h3 style="font-size:22px">No performance promises</h3><p>Planning is analysis and education. Investing involves risk including loss of principal, and anyone promising otherwise is selling something.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="kicker" data-rv>Credentials</p>
    <h2 data-rv style="max-width:15ch">The paperwork behind it.</h2>
    <div class="badges" data-rv style="border-top:0;padding-top:8px">
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
    <div class="clines" data-rv style="margin-top:30px;max-width:70ch">
      <span><b>Licensed</b>South Carolina Life, Accident &amp; Health</span>
      <span><b>Credential</b>Certified Corporate Financial Planning Analyst (CCFPA)</span>
      <span><b>Studied</b>Multiple degrees, including an M.S. in Psychology from Arizona State</span>
      <span><b>Built</b>Businesses started and sold before this one</span>
      <a href="form-crs.html"><b>Filed</b>Form CRS and disclosures, in full</a>
    </div>
  </div>
</section>
"""

# ---------------------------------------------------------------- CONTACT
CONTACT = """
<section class="section">
  <div class="wrap split c">
    <div>
      <p class="kicker" data-rv>Start here</p>
      <h1 data-rv style="font-size:clamp(42px,5.2vw,72px)">One call. <em class="g">No pitch.</em></h1>
      <p class="lede" data-rv>Tell me what is on your mind and I will tell you whether I can help. If the answer is that you do not need me yet, that is the answer you will get.</p>
      <div data-rv>
      <!-- Click to call AND click to text. Tyler: "alot of ppl txt first."
           sms: with a prefilled body is supported on iOS and Android; the ?&body=
           form is the one that works on both. 864-558-8440 is a Zoom Phone line
           that receives SMS, which is why it must never move to an auto
           receptionist. -->
      <div class="reachrow">
        <a class="reach" href="tel:+18645588440">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>
          <span><b>Call</b>864-558-8440</span>
        </a>
        <a class="reach" href="sms:+18645588440?&amp;body=Hi%20Tyler%2C%20I%20have%20a%20question%20about%20">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 9.9 9.9 0 0 1-2.8-.4L3 21l1.6-4.1A8.2 8.2 0 0 1 3.6 11 8.4 8.4 0 0 1 12 3h.5a8.4 8.4 0 0 1 8.5 8z"/></svg>
          <span><b>Text</b>Most people start here</span>
        </a>
      </div>
      </div>
      <div class="clines" data-rv>
        <a href="https://scheduler.zoom.us/raecocapital/introductory-consultation" target="_blank" rel="noopener"><b>Book</b>Pick a time that suits you</a>
        <span><b>Where</b>100% virtual, serving South Carolina</span>
        <span><b>Hours</b>Texts answered fastest, usually same day</span>
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
      <h2 class="sub">Send a note</h2>
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


DISCLOSURES = legal_page("Disclosures","Legal",[
 ("Registration","Rae &amp; Co Capital, LLC (d/b/a RcoWealth) is registered as an investment adviser with the State of South Carolina. Registration does not imply a certain level of skill or training."),
 ("Investment risk","Investing involves risk, including possible loss of principal. Past performance is not indicative of future results. No strategy assures a profit or protects against loss."),
 ("Insurance","Insurance products are subject to underwriting and carrier approval. Rae &amp; Co Capital may receive commissions on insurance placed, which is a conflict of interest and is disclosed. Insurance is optional and is never required to work with the firm."),
 ("Advisory fees","Investment advisory services are billed at 1% per year of assets under management with a $750 annual minimum, charged quarterly under a signed advisory agreement. Financial planning is a flat, one-time fee agreed in writing before work begins and completed within six months; any unearned prepaid portion is refundable."),
 ("Not advice","This website is for informational purposes only and should not be treated as individualized investment, tax, legal, or insurance advice. No advice is provided until an advisory agreement is in place."),
 ("Third parties","Links to third parties, including carrier quoting and payment tools, are provided for convenience. Rae &amp; Co Capital does not control and is not responsible for the content or privacy practices of those sites."),
])

FORMCRS = legal_page("Form CRS Summary","Legal",[
 ("Relationship summary","Rae &amp; Co Capital, LLC (d/b/a RcoWealth) is registered as an investment adviser with the State of South Carolina. Investment advisory services and fees differ from brokerage services, and it is important that you understand the differences. Free and simple tools are available at Investor.gov/CRS."),
 ("Relationships and services","We provide discretionary and non-discretionary investment advisory services, financial planning, and insurance consulting. Services are ongoing and tailored to goals, time horizon, and risk tolerance."),
 ("Fees, costs, conflicts and standard of conduct","Our standard annual advisory fee is 1.00% of assets under management with a $750 annual minimum, billed quarterly. Financial planning is a flat one-time fee. We may also receive commissions on insurance placed, which is a conflict of interest because it creates an incentive to recommend insurance. You should understand and ask us about this conflict."),
 ("Questions worth asking","Given my financial situation, should I choose an investment advisory service? Why or why not? How will you choose investments to recommend? What is your relevant experience, and what do your licenses mean? How might your conflicts of interest affect me, and how will you address them?"),
 ("Full document","This is a summary. The complete Form CRS and Form ADV Part 2A are available on request and through the "
  "<a href='https://adviserinfo.sec.gov/' target='_blank' rel='noopener'>Investment Adviser Public Disclosure website</a>. "
  "Free and simple tools to research firms and advisers are at "
  "<a href='https://www.investor.gov/CRS' target='_blank' rel='noopener'>Investor.gov/CRS</a>."),
])

PRIVACY = legal_page("Privacy Policy","Legal",[
 ("What we collect","We collect only the information you give us: your name, contact details, and whatever you choose to share about your financial situation so we can do the work. The coverage calculator on this site requires no name or email and stores nothing about you."),
 ("How we use it","To respond to you, to provide the services you engage us for, and to meet our record-keeping obligations as a registered investment adviser. We do not sell your information, ever."),
 ("Who else sees it","Only the parties needed to deliver the service, such as the custodian holding your accounts or an insurance carrier processing an application you chose to submit. Each has its own privacy practices."),
 ("Security","Do not send account numbers, policy numbers, passwords, Social Security numbers, or other sensitive financial data through any website form. Use the secure channels we set up with you instead."),
 ("Your choices","You can ask what we hold, ask us to correct it, or opt out of marketing messages at any time by replying to any message or calling 864-558-8440."),
])

CLIENTLOGIN = legal_page("Client access","Portals",[
 ("Use the provider portal directly","Rae &amp; Co Capital does not ask for portal credentials. The firm can help point you in the right direction, but credential entry should happen only through the provider&rsquo;s own site."),
 ("Investment accounts","Schwab Alliance is where Schwab-custodied investment and retirement accounts live. Go to schwaballiance.com directly rather than through a link in an email."),
 ("Insurance accounts","Policy, billing and customer access is handled through your carrier&rsquo;s own portal. Which one depends on who issued the policy; ask and we will tell you."),
 ("A warning worth repeating","Do not send account numbers, policy numbers, passwords, Social Security numbers, or sensitive financial data through any website form, including ours. If a message asks you to, it is not from us."),
])


# ---------------------------------------------------------------- CALCULATOR
# Ported into the shell because it was the LAST and worst one-way door: linked
# from every page footer, and it dropped a visitor onto the old layout with no
# route back. Field ids, the digit-stripping parse fix and the Salesforce
# wiring are preserved exactly; only the chrome changes.
CALCFIELDS = [
 ("income","Your annual income",True,0,400000,5000,75000,"$"),
 ("years","Years to replace it",False,0,40,1,10,""),
 ("mortgage","Mortgage balance",True,0,750000,5000,250000,"$"),
 ("debts","Other debt (cars, cards, loans)",True,0,150000,2500,25000,"$"),
 ("kids","Number of children",False,0,8,1,2,""),
 ("percollege","Education support per child",True,0,150000,5000,40000,"$"),
 ("final","Final expenses",True,0,40000,1000,15000,"$"),
 ("existing","Existing life insurance",True,0,1000000,10000,50000,"$"),
]
def calcfield(f):
    fid,label,money,lo,hi,step,val,cur=f
    curspan=f'<span class="sf-cur">{cur}</span>' if cur else ''
    return f"""<div class="slide-field">
        <label for="{fid}">{label}</label>
        <div class="sf-val">{curspan}<input id="{fid}" type="text" inputmode="numeric" value="{val:,}"></div>
        <input class="sf-range" type="range" min="{lo}" max="{hi}" step="{step}" value="{val}" data-for="{fid}" aria-label="{label}, slider">
      </div>"""

CALCULATOR = """
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <p class="kicker" data-rv>Free tool &middot; no email required</p>
    <h1 data-rv style="font-size:clamp(40px,5vw,72px)">How much cover do you <em class="g">actually</em> need?</h1>
    <p class="lede" data-rv>Most people guess, or assume what they have through work is enough. Drag the sliders and watch the number move. Nothing is stored and nobody is emailed.</p>
  </div>
</section>

<section class="section">
  <div class="wrap calcgrid">
    <div class="calcpanel" data-rv>
      <div class="calcgroup">
        <h2 class="sub">Replacing your income</h2>
        <p class="ghint">The paycheck your family would lose, for the years until the kids are grown or the house is paid off.</p>
        <div class="calcrow">""" + calcfield(CALCFIELDS[0]) + calcfield(CALCFIELDS[1]) + """</div>
      </div>
      <div class="calcgroup">
        <h2 class="sub">Debts you would leave behind</h2>
        <p class="ghint">What would have to be paid off so nobody inherits a payment they cannot make.</p>
        <div class="calcrow">""" + calcfield(CALCFIELDS[2]) + calcfield(CALCFIELDS[3]) + """</div>
      </div>
      <div class="calcgroup">
        <h2 class="sub">Children</h2>
        <p class="ghint">If you want to help with school, put in what you would set aside per child.</p>
        <div class="calcrow">""" + calcfield(CALCFIELDS[4]) + calcfield(CALCFIELDS[5]) + """</div>
      </div>
      <div class="calcgroup">
        <h2 class="sub">Final expenses and what you already have</h2>
        <p class="ghint">Include coverage through work, and check the real number. Employer cover is usually smaller than people assume and it ends when the job does.</p>
        <div class="calcrow">""" + calcfield(CALCFIELDS[6]) + calcfield(CALCFIELDS[7]) + """</div>
      </div>
      <p class="ghint" style="margin-top:18px">This is an estimate built from the numbers you entered. It is a starting point for a conversation, not individualized advice, and it does not account for savings, taxes, Social Security survivor benefits, or a spouse's income. Life insurance is subject to underwriting and carrier approval.</p>
    </div>

    <aside class="resultcard" id="resultCard" data-rv>
      <p class="rlabel">Estimated coverage gap</p>
      <p class="rbig" id="gapOut">$0</p>
      <p class="rsub" id="gapNote">Drag any slider to begin.</p>
      <div class="rline"><span>Total need</span><b id="needOut">$0</b></div>
      <div class="rline"><span>Existing coverage</span><b id="haveOut">$0</b></div>
      <div class="ractions">
        <a class="btn btn-gold" href="https://app.back9ins.com/apply/rcowealth?utm_source=website&amp;utm_medium=internal&amp;utm_campaign=rebuild&amp;utm_content=calculator_result" target="_blank" rel="noopener">Quote this amount <span class="arr">&rarr;</span></a>
        <a class="btn-line" href="protection.html">What kind should it be?</a>
      </div>
    </aside>
  </div>
</section>
"""

# ------------------------------------------------- TYPES OF LIFE INSURANCE
# The single strongest content asset on the property at 1,342 words, and the
# rebuild had deleted it. Ported whole. VUL stays out - Tyler's explicit call
# on licensing, "no leave the VUL out then", closed, do not re-raise.
TYPES = [
 ("Start here","Term life",
  "Coverage for a set number of years, usually 10, 20 or 30. If you die during the term, it pays. If you outlive it, it ends and pays nothing. That is the entire product, and it is why it costs the least per dollar of coverage by a wide margin.",
  [("What it solves","A mortgage, the years until children are grown, a business loan, an income that other people depend on."),
   ("What it costs you","Nothing builds up. When the term ends you have paid for protection you did not use, which is how insurance is supposed to work."),
   ("When it is wrong","When the need genuinely never ends, or when the policy has a job to do inside an estate or a business succession.")],
  "Where most people land","For most households under 50 with a mortgage and dependents, term does the job, and the money not spent on premium is usually better invested elsewhere. We will say that even though it pays us the least."),

 ("Permanent","Whole life",
  "Coverage for your whole life with a premium that does not change and a cash value that grows at a rate the insurer sets. Predictable, and expensive relative to term for the same death benefit.",
  [("What it solves","A need that does not expire: estate liquidity, a special-needs dependent, business continuity, final costs."),
   ("What it costs you","Premium is several times term for the same benefit, and early years are heavily front-loaded with costs."),
   ("When it is wrong","When it is bought as an investment. It is insurance with a savings component, not a portfolio.")],
  None,None),

 ("Permanent","Universal life",
  "Permanent coverage with a flexible premium. You can pay more or less within limits, and the policy draws its internal costs from the cash value. That flexibility is the feature and it is also the risk.",
  [("What it solves","A permanent need with income that varies year to year."),
   ("What it costs you","Attention. Underfund it for long enough and the policy can lapse, which is the worst outcome in insurance."),
   ("When it is wrong","When nobody is going to review it. A flexible policy left alone for twenty years is a problem waiting.")],
  None,None),

 ("Permanent &middot; the complicated one","Indexed universal life (IUL)",
  "Universal life where the cash value is credited based on the movement of a market index, subject to a cap on the upside and a floor that protects against index losses. It is the most oversold product in this industry, so here is the plain version.",
  [("What it solves","A permanent need for someone who wants index-linked crediting with a floor, and who will actually review the policy."),
   ("What it costs you","Caps, participation rates and spreads limit the credited amount, insurance charges rise with age, and the carrier can change some of those terms."),
   ("When it is wrong","When you have term needs, unused 401(k) or IRA space, or no emergency reserve. Those come first.")],
  "How to read an IUL illustration","The projected columns are not a forecast and are not guaranteed. Ask for the guaranteed column, ask what happens if the credited rate is lower than illustrated, and ask what the policy costs in years one through ten. If those answers are not offered without being asked for, that is information about the seller."),

 ("Income protection","Disability income",
  "Life insurance protects your family from losing you. Disability income protects them from losing your paycheck while you are still here, which is statistically the likelier event during working years. It replaces a percentage of income when illness or injury stops you working.",
  [("What it solves","The mortgage and the groceries during a long recovery, when the income stops but the bills do not."),
   ("What it costs you","Premium rises with how quickly benefits start, how long they last, and how strictly the policy defines disability."),
   ("When it is wrong","Rarely, during working years. The usual mistake is assuming a small group policy at work is enough.")],
  "The gap most people have","Employer coverage typically replaces around 60% of base pay, is taxable when the employer pays the premium, often excludes bonus and commission, and ends the day you leave the job."),

 ("Long-term care","Long-term care, and hybrid policies",
  "Standalone long-term care insurance pays for care at home or in a facility. A hybrid, sometimes called a linked-benefit policy, combines that with life insurance: if care is never needed, the policy pays a death benefit instead.",
  [("What it solves","Care costs that Medicare largely does not pay for, and the burden that otherwise lands on adult children."),
   ("What it costs you","Standalone premiums can be raised by the carrier. Hybrids fix that by charging more up front."),
   ("When it is wrong","When protection and retirement income are not handled first, or when assets are small enough that Medicaid is the realistic path.")],
  None,None),

 ("Variants worth knowing","Term variants, and accidental death",
  "Three products get sold as if they were ordinary term. They are not, and the differences matter more than the names suggest.",
  [("No-medical term","No exam, faster approval, and you generally pay more for the convenience. Useful when time or health makes a full exam impractical."),
   ("Return-of-premium term","Refunds premiums if you outlive the term. The premium is substantially higher, and the refund is not interest-bearing, so compare it against buying plain term and investing the difference."),
   ("Accidental death","Pays only if death is accidental, which is a small share of deaths. Cheap because it covers little. It is a supplement, never a substitute for real coverage.")],
  None,None),

 ("Small and specific","Final expense",
  "A small whole life policy, commonly $10,000 to $25,000, meant to cover a funeral, burial and the immediate bills that land on a family in the first few weeks. Underwriting is limited, which is the point.",
  [("What it solves","End-of-life costs for someone who cannot get, or does not need, a larger fully underwritten policy."),
   ("What it costs you","A high price per dollar of coverage, and many policies have a graded benefit for the first two years."),
   ("When it is wrong","When you are healthy enough to qualify for a normal policy, or when savings already cover it.")],
  None,None),
]

def types_page():
    blocks = []
    for i,(tag,h2,intro,cells,ct,cx) in enumerate(TYPES):
        callout = (f'<div class="callout" data-rv><b>{ct}</b> {cx}</div>' if ct else "")
        blocks.append(f"""
<section class="section{' cream' if i%2 else ''}" style="padding-top:clamp(44px,5vw,68px);padding-bottom:clamp(44px,5vw,68px)">
  <div class="wrap">
    <p class="kicker" data-rv>{tag}</p>
    <h2 data-rv>{h2}</h2>
    <p class="lede" data-rv style="max-width:74ch">{intro}</p>
    <div class="prow stagger" data-rv>{"".join(f'<div><b>{a}</b><p>{b}</p></div>' for a,b in cells)}</div>
    {callout}
  </div>
</section>""")
    return f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <p class="kicker" data-rv>Plain language &middot; Protection planning</p>
    <h1 data-rv>The whole menu, and what each one is <em class="g">actually for</em>.</h1>
    <p class="lede" data-rv>Most people are sold a product before anyone tells them what the products are. Here is the range we place, in order of how simple it is, with the costs stated as plainly as the benefits.</p>
    <div class="acts" data-rv>
      <a class="btn btn-ink" data-magnetic href="life-insurance-calculator.html">Estimate what you need <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="{B9}&amp;utm_content=types_hero" target="_blank" rel="noopener">Compare real quotes</a>
    </div>
  </div>
</section>
{"".join(blocks)}
<section class="section dark">
  <div class="wrap">
    <p class="kicker" data-rv>No small print</p>
    <h2 data-rv style="max-width:20ch">How we are paid, so you can <em class="g" style="color:var(--gold-2)">weigh the advice</em>.</h2>
    <p class="lede" data-rv style="max-width:76ch">Rae &amp; Co Capital is compensated by commission on insurance placed. Different products pay different amounts, and permanent products generally pay more than term. That is a conflict of interest, it is disclosed in our Form CRS and disclosures, and it is the reason the term section above says what it says.</p>
    <p class="lede" data-rv style="max-width:76ch">Coverage is shopped across 46 carriers rather than sold from one shelf. Availability, pricing and features vary by product, state, health and underwriting. Nothing on this page is individualized insurance, tax, legal or investment advice, and no coverage exists until a carrier issues a policy.</p>
    <p class="lede" data-rv style="max-width:76ch">Fixed and indexed annuities, including multi-year guaranteed annuities and income riders, are placed as part of retirement income planning rather than protection planning. Those are covered on the retirement planning page.</p>
    <div class="acts" data-rv style="margin-top:8px">
      <a class="btn btn-gold" href="life-insurance-calculator.html">Estimate your coverage need <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="contact.html">Talk it through</a>
    </div>
  </div>
</section>
{form_section("Get it checked", "Have what you own reviewed before you buy anything else.",
  "Send what you already have and I will tell you whether it still fits. If the answer is that you do not need anything, that is the answer you will get.",
  lead_form("types-of-life-insurance","types-of-life-insurance.html","life-insurance-planning",
            "Request a policy review","Replies come from me, usually the same day.",
            "Insurance","Life insurance planning", cta="Request a review", insurance=True), cream=True)}"""

# ------------------------------------------------------- REMAINING PORTS
# thank-you.html is NOT optional: every form on the site carries
# retURL=https://rcowealth.com/thank-you.html, so the moment the rebuild
# becomes the root this file has to exist or every submission 404s.
THANKYOU = """
<section class="section" style="padding-bottom:0">
  <div class="wrap" style="max-width:760px">
    <p class="kicker" data-rv>Message received</p>
    <h1 data-rv>Thank you. It <em class="g">landed</em>.</h1>
    <p class="lede" data-rv>Your note is with me, not a queue. I read them myself and reply personally, usually the same day. If it is urgent, text 864-558-8440 and you will get me faster.</p>
    <div class="reachrow" data-rv style="max-width:420px">
      <a class="reach" href="tel:+18645588440"><span><b>Call</b>864-558-8440</span></a>
      <a class="reach" href="sms:+18645588440?&amp;body=Hi%20Tyler%2C%20I%20just%20sent%20a%20note%20about%20"><span><b>Text</b>Usually the fastest</span></a>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <h2 class="sub" data-rv style="margin-bottom:24px">While you wait, these need nobody's permission.</h2>
    <div class="grid g3 stagger" data-rv>
      <a class="card" style="text-decoration:none" href="life-insurance-calculator.html"><p class="tag">Free, no signup</p><h3>Run your coverage number</h3><p>Drag the sliders and see the gap. Nothing is stored and no contact details are asked for.</p></a>
      <a class="card" style="text-decoration:none" href="types-of-life-insurance.html"><p class="tag">Plain language</p><h3>Read what the products do</h3><p>All eight, with what each costs you and when it is the wrong tool.</p></a>
      <a class="card" style="text-decoration:none" href="planning.html"><p class="tag">Published prices</p><h3>See the planning fees</h3><p>Flat fees from $750, listed, no discovery call needed to find out.</p></a>
    </div>
    <div class="acts" data-rv style="margin-top:34px">
      <a class="btn btn-ink" href="index.html">Back to home <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="client-login.html">Client access</a>
    </div>
  </div>
</section>
"""

QUOTE = f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <p class="kicker" data-rv>Instant quotes &middot; No agent call</p>
    <h1 data-rv>Compare real quotes from <em class="g">major carriers</em>.</h1>
    <p class="lede" data-rv>Answer a few health and coverage questions and see actual pricing across 46 carriers. You can apply online in the same session. Nobody phones you to unlock a number.</p>
    <div class="acts" data-rv>
      <a class="btn btn-gold" data-magnetic href="{B9}&amp;utm_content=quote_hero" target="_blank" rel="noopener">Open quote &amp; apply <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="life-insurance-calculator.html">Work out the amount first</a>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <h2 class="sub" data-rv style="margin-bottom:24px">What happens, in order.</h2>
    <div class="grid g3 stagger" data-rv>
      <div class="card"><p class="tag">Step one</p><h3>Health and coverage questions</h3><p>A couple of minutes. No exam at this stage and no commitment to anything.</p></div>
      <div class="card"><p class="tag">Step two</p><h3>Real pricing, side by side</h3><p>You see the same carrier pricing I see. There is no version of this where I get a better number than you do.</p></div>
      <div class="card"><p class="tag">Step three</p><h3>Apply and e-sign</h3><p>In the same sitting if you want. Underwriting and carrier approval come after, and nothing is in force until a carrier issues.</p></div>
    </div>
    <div class="callout" data-rv style="margin-top:30px"><b>If the quoter will not load</b>
      Some corporate networks block it. <a href="{B9}&amp;utm_content=quote_fallback" target="_blank" rel="noopener">Open it in a new window</a>, or text 864-558-8440 and I will send pricing manually.</div>
    <p class="lede" data-rv style="margin-top:26px;max-width:78ch;font-size:13px">Quoting and applications are processed through BackNine Insurance. Pricing shown is an estimate and is not a binding offer. All coverage is subject to underwriting and carrier approval, and final rates may differ from quoted rates. Rae &amp; Co Capital may receive a commission on insurance products, a conflict of interest that is disclosed. Rae &amp; Co Capital is licensed for life insurance in South Carolina; availability elsewhere depends on licensing and carrier approval.</p>
  </div>
</section>
{form_section("Rather not self-serve", "Want the number checked before you buy?",
  "Send what you already have and what you are trying to protect. I will tell you whether the coverage fits, including when the answer is that you do not need more.",
  lead_form("life-insurance-quote","life-insurance-quote.html","life-insurance-planning",
            "Have it checked first","Replies come from me, usually the same day.",
            "Insurance","Life insurance planning", cta="Send it over", insurance=True), cream=True)}"""

CHECK_ITEMS = [
 ("Income replacement","What income would need to continue, for whom, and for how long?"),
 ("Debt and liquidity","What debt, taxes, estate costs or cash needs could appear at the wrong time?"),
 ("Family obligations","Dependents, education, caregiving and long-term family priorities."),
 ("Business exposure","Key-person, buy-sell, continuity and ownership transition questions."),
 ("Beneficiaries","Ownership and beneficiary designations should match the planning intent."),
 ("Policy fit","Term, permanent, employer and legacy coverage all have different jobs."),
]

CHECKLIST = f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <p class="kicker" data-rv>Checklist &middot; Protection planning</p>
    <h1 data-rv>Before changing a policy, know what the coverage is <em class="g">supposed to solve</em>.</h1>
    <p class="lede" data-rv>A useful review starts with obligations, people, ownership, beneficiaries and liquidity. Not just premium and death benefit. Replacing a policy on price alone is how people lose coverage they cannot get back.</p>
    <div class="acts" data-rv>
      <a class="btn btn-ink" data-magnetic href="#ask">Request the checklist <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="types-of-life-insurance.html">Read what each product does</a>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <h2 class="sub" data-rv style="margin-bottom:24px">The six things worth checking.</h2>
    <div class="grid g3 stagger" data-rv>
      {"".join(f'<div class="card"><h3 style="font-size:21px">{t}</h3><p>{b}</p></div>' for t,b in CHECK_ITEMS)}
    </div>
    <div class="callout" data-rv style="margin-top:30px"><b>One warning worth the whole page</b>
      Do not cancel existing coverage until replacement coverage is issued and in force. Health changes, and a policy you already own may be one you could no longer qualify for.</div>
  </div>
</section>
<div id="ask"></div>
{form_section("Request the checklist", "Ask for the checklist, or a full protection review.",
  "I will send the checklist and, if you want, walk your existing policies through it with you. Please leave policy numbers and Social Security numbers out of the form.",
  lead_form("life-insurance-checklist","life-insurance-review-checklist.html","lead-magnet-download",
            "Send me the checklist","Replies come from me, usually the same day.",
            "Insurance","Life insurance planning", cta="Send the checklist", insurance=True,
            placeholder="Example: I have a 20 year term from 2015 and group cover at work, and I am not sure if it is still enough."), cream=True)}"""

SERVICE_CARDS = [
 ("Portfolio","Investment management","Portfolio structure, liquidity, allocation and risk tied to the purpose of the money.","investment-management-greenville-sc.html"),
 ("Income","Retirement planning","Withdrawal strategy, reserves, income timing, and the transition from saving to spending.","retirement-planning-greenville-sc.html"),
 ("Planning","Financial planning","Cash flow, accounts, insurance, tax exposure, family needs and business decisions organized.","financial-advisor-greenville-sc.html"),
 ("Protection","Life insurance planning","Coverage reviewed against income, debt, dependents, business exposure and legacy.","life-insurance-greenville-sc.html"),
]

SERVICES = f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <p class="kicker" data-rv>Virtual services &middot; Greenville, South Carolina</p>
    <h1 data-rv>One relationship. <em class="g">Four connected</em> disciplines.</h1>
    <p class="lede" data-rv>Investments, retirement income, financial planning and protection, coordinated by one person without office logistics. The coordination is the product. Handled separately, these four contradict each other more often than people realize.</p>
    <div class="acts" data-rv>
      <a class="btn btn-ink" data-magnetic href="contact.html">Start a conversation <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="planning.html">Or buy a plan outright</a>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <h2 class="sub" data-rv style="margin-bottom:24px">Where each one goes deeper.</h2>
    <div class="grid g2 stagger" data-rv>
      {"".join(f'<a class="card" style="text-decoration:none" href="{h}"><p class="tag">{t}</p><h3>{n}</h3><p style="margin-bottom:16px">{d}</p><span class="btn-line">Open page &rarr;</span></a>' for t,n,d,h in SERVICE_CARDS)}
    </div>
  </div>
</section>
<section class="section cream">
  <div class="wrap split c">
    <div>
      <p class="kicker" data-rv>Protection planning</p>
      <h2 data-rv style="max-width:18ch">Not sure how much cover your family would need?</h2>
      <p class="lede" data-rv>Start with the estimate, then compare real pricing. The calculator asks for no contact information and stores nothing.</p>
      <div class="acts" data-rv>
        <a class="btn btn-ink" href="life-insurance-calculator.html">Estimate your coverage need <span class="arr">&rarr;</span></a>
        <a class="btn-line" href="{B9}&amp;utm_content=services_quote" target="_blank" rel="noopener">Compare real quotes</a>
      </div>
    </div>
    <div class="card" data-rv>
      <p class="tag">Client access</p><h3>Need a portal?</h3>
      <p style="margin-bottom:16px">Investment and insurance account access is handled through the provider portals, not through this site.</p>
      <a class="btn-line" href="client-login.html">Go to client access &rarr;</a>
    </div>
  </div>
</section>
"""

# The paid-search landing page. Kept separate from the geo page on purpose:
# this one takes ad traffic with buying intent, so it opens on the quoter
# rather than on education.
REVIEW = f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <p class="kicker" data-rv>Protection review</p>
    <h1 data-rv>Make sure the people depending on you are <em class="g">actually protected</em>.</h1>
    <p class="lede" data-rv>Families, homeowners and business owners get existing policies and coverage gaps reviewed against what the money is actually for. Price it yourself in a few minutes, or have what you already own checked first.</p>
    <div class="acts" data-rv>
      <a class="btn btn-gold" data-magnetic href="{B9}&amp;utm_content=review_hero" target="_blank" rel="noopener">Get pricing now <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="life-insurance-calculator.html">Work out the amount first</a>
    </div>
    <p style="margin:26px 0 0;font:600 13px/1.6 var(--sans);color:var(--muted)" data-rv>Mortgage protection &middot; Income replacement &middot; Family obligations &middot; Business-owner risk</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <p class="kicker" data-rv>When to review coverage</p>
    <h2 data-rv style="max-width:22ch">Coverage should match the job it needs to do.</h2>
    <p class="lede" data-rv style="max-width:74ch">People usually review after a mortgage, a marriage, a new child, a business change, a debt increase, a job change or a health change. Existing policies deserve a second look before they are replaced, reduced, borrowed against or allowed to lapse.</p>
    <div class="grid g3 stagger" data-rv style="margin-top:32px">
      <div class="card"><p class="tag">Home</p><h3>Mortgage protection</h3><p>Whether a spouse or family could keep the home, refinance, or pay the debt down if the income stopped.</p></div>
      <div class="card"><p class="tag">Family</p><h3>Income replacement</h3><p>Survivor income, children, caregiving, education, final costs and emergency liquidity.</p></div>
      <div class="card"><p class="tag">Business</p><h3>Owner continuity</h3><p>Key-person, buy-sell, debt, succession and business-continuity exposure.</p></div>
    </div>
  </div>
</section>
<section class="section cream">
  <div class="wrap">
    <p class="kicker" data-rv>How the review works</p>
    <h2 data-rv style="max-width:22ch">A focused conversation before any application.</h2>
    <div class="grid g2 stagger" data-rv style="margin-top:30px">
      <div class="card"><p class="tag">What we establish</p><h3>The inputs</h3>
        <ul class="ticks"><li>What the policy actually needs to protect</li><li>Current employer, term, permanent or legacy coverage</li><li>Rough budget and how long the need lasts</li><li>Health and the likely underwriting path</li></ul></div>
      <div class="card"><p class="tag">What you get</p><h3>The output</h3>
        <ul class="ticks"><li>A gap and overlap summary in plain language</li><li>Carrier and product fit, with the reasoning shown</li><li>Replacement cautions before you change anything</li><li>Or a clear "you do not need more", when that is the answer</li></ul></div>
    </div>
    <div class="callout" data-rv style="margin-top:28px"><b>Before you replace anything</b>
      Do not cancel existing coverage until replacement coverage is issued and in force. Health changes, and a policy you already own may be one you could no longer qualify for.</div>
  </div>
</section>
{form_section("Request a review", "Have your coverage checked.",
  "Tell me what you already have and who depends on you. Please leave policy numbers and Social Security numbers out of the form.",
  lead_form("life-insurance-protection-review","life-insurance-protection-review.html",
            "paid-search-protection-review","Request a protection review",
            "Replies come from me, usually the same day.","Insurance","Life insurance planning",
            cta="Request a review", insurance=True,
            placeholder="Example: mortgage of $280k, two kids under 10, group cover at work and a term policy I cannot find the paperwork for."))}"""

# --------------------------------------------------------- GEO LANDING PAGES
# Ported from the live site, filenames unchanged so existing links and whatever
# ranking equity exists survive the swap. These four are the ONLY pages on the
# property built to rank for "greenville sc", and the rebuild had deleted all
# four. Titles now actually carry the geo term, which the live versions did not
# ("Financial Planning | Rae & Co Capital" cannot rank for a Greenville query).
GEO = [
 ("financial-advisor-greenville-sc.html",
  "Financial Advisor in Greenville, SC | Rae &amp; Co Capital",
  "Virtual financial planning from a Greenville, South Carolina fiduciary. Cash flow, investments, protection, retirement and tax decisions organized into one sequence.",
  "Financial planning", "Financial planning is the <em class=\"g\">decision system</em>.",
  "Most people do not have an information problem. They have a sequencing problem. Planning is where the pieces get put in an order that actually works.",
  ["Cash flow, savings, and debt decisions","Investment and retirement account structure",
   "Insurance and protection gaps","Business-owner or family obligations",
   "Estate, beneficiary, tax, and liquidity coordination points"],
  ["A clean decision map","A practical action sequence, ranked","Ongoing review as life changes"],
  "planning.html","See flat-fee planning",
  "financial-advisor-greenville-sc","Not sure","Focused intro call"),

 ("investment-management-greenville-sc.html",
  "Investment Management in Greenville, SC | Rae &amp; Co Capital",
  "Investment management for Greenville, South Carolina, connected to planning, liquidity, retirement income and protection. Assets custodied at Charles Schwab.",
  "Investment management", "Investment management that <em class=\"g\">answers to the plan</em>.",
  "Anyone can buy index funds. The work is sequencing withdrawals, keeping taxes from eating the gains, and not selling at the bottom because a headline scared you.",
  ["Current allocation and account structure","Risk exposure and concentration",
   "Liquidity needs and time horizon","Tax-sensitive investment decisions",
   "Rebalancing and ongoing review cadence"],
  ["A clearer investment policy","An implementation plan",
   "A review rhythm tied to life changes, not market noise"],
  "wealth.html","See how management works",
  "investment-management-greenville-sc","Investments","Portfolio or retirement review"),

 ("retirement-planning-greenville-sc.html",
  "Retirement Planning in Greenville, SC | Rae &amp; Co Capital",
  "Retirement income planning for Greenville, South Carolina. Withdrawal sequencing, Social Security timing, reserves and survivor income, decided before the paycheck stops.",
  "Retirement planning", "Retirement income before <em class=\"g\">retirement pressure</em>.",
  "The switch from saving to spending is where small mistakes get expensive, and most of them are locked in before anyone notices.",
  ["Income sources and expected spending","Withdrawal sequencing and reserve strategy",
   "Portfolio risk during the retirement transition","Survivor needs and legacy considerations",
   "Flexibility for health, family, and market changes"],
  ["A retirement income map","A liquidity and reserve framework",
   "A decision list before the paycheck changes"],
  "wealth.html","See retirement income work",
  "retirement-planning-greenville-sc","Investments","Portfolio or retirement review"),

 ("life-insurance-greenville-sc.html",
  "Life Insurance in Greenville, SC | Rae &amp; Co Capital",
  "Life insurance in Greenville, South Carolina, shopped across 46 carriers on one application. Price it and apply online, or have the coverage checked against the plan first.",
  "Protection planning", "Life insurance placed with <em class=\"g\">real carriers</em>, tied to the plan.",
  "Coverage is the part that cannot wait for a good year. Price it yourself in a few minutes, or have what you already own checked before you buy anything else.",
  ["Existing policies and employer coverage","New term and permanent coverage needs",
   "Income replacement and debt exposure","Dependents, education, and family obligations",
   "Business-owner, buy-sell, or key-person risk",
   "Carrier fit, underwriting path, ownership, beneficiaries and estate coordination"],
  ["A coverage strategy tied to the financial plan","A gap and overlap summary",
   "Carrier, underwriting and application next steps when new coverage makes sense",
   "Replacement considerations before changing anything you already own"],
  "protection.html","See every product explained",
  "life-insurance-family-protection","Insurance","Life insurance planning"),
]

CROSS = [("financial-advisor-greenville-sc.html","Financial planning"),
         ("investment-management-greenville-sc.html","Investment management"),
         ("retirement-planning-greenville-sc.html","Retirement planning"),
         ("life-insurance-greenville-sc.html","Life insurance")]

def geo_page(slug, kicker, h1, lede, helps, leave, deep, deep_cta, campaign, interest, step):
    cross = "".join(f'<a class="xlink" href="{h}">{t} <span class="arr">&rarr;</span></a>'
                    for h, t in CROSS if h != slug)
    return f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <p class="kicker" data-rv>{kicker} &middot; Greenville, South Carolina</p>
    <h1 data-rv>{h1}</h1>
    <p class="lede" data-rv>{lede}</p>
    <div class="acts" data-rv>
      <a class="btn btn-ink" data-magnetic href="{deep}">{deep_cta} <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="life-insurance-calculator.html">Run the coverage numbers</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 class="sub" data-rv style="margin-bottom:26px">What gets looked at, and what you leave with.</h2>
    <div class="grid g2 stagger" data-rv>
      <div class="card"><p class="tag">What gets reviewed</p><h3>The inputs</h3>
        <ul class="ticks">{"".join(f"<li>{x}</li>" for x in helps)}</ul></div>
      <div class="card"><p class="tag">What you walk away with</p><h3>The output</h3>
        <ul class="ticks">{"".join(f"<li>{x}</li>" for x in leave)}</ul></div>
    </div>
    <p class="lede" data-rv style="margin-top:34px;max-width:74ch">Portfolio, retirement income, insurance, cash flow, taxes and family obligations get reviewed together rather than handled as disconnected projects. That coordination is the whole reason one person does all of it.</p>
    <div class="xrow" data-rv>{cross}</div>
  </div>
</section>
{form_section("Request follow-up", "Bring this into the conversation.",
  "Tell me what is on your mind and I will tell you whether I can help. Please leave out account numbers, policy numbers and Social Security numbers.",
  lead_form(campaign, slug, "consultation-request", "Request follow-up",
            "Replies come from me, usually the same day.", interest, step,
            cta="Request follow-up", insurance=(interest == "Insurance")), cream=True)}"""

PAGES = [
 ("index.html","Rae &amp; Co Capital | Veteran-Owned Virtual Wealth Management","Veteran-owned, 100% virtual wealth management and protection planning in Greenville, South Carolina. Quote, price and start it yourself.",HOME),
 ("wealth.html","Wealth Management | Rae &amp; Co Capital","Portfolio management and retirement income at 1% a year with a $750 annual minimum. Assets custodied at Charles Schwab.",WEALTH),
 ("protection.html","Protection Planning | Rae &amp; Co Capital","Term, disability, permanent, long-term care and final expense explained plainly. Quote and apply across 46 carriers.",PROTECTION),
 ("planning.html","Financial Planning Fees | Rae &amp; Co Capital","Flat-fee financial planning from $750. Published prices, real deliverables, buy it online.",PLANNING),
 ("advisor.html","Tyler Krause, Your Advisor | Rae &amp; Co Capital","Marine Corps veteran, Series 65 fiduciary, CCFPA. One person who answers the phone.",ADVISOR),
 ("contact.html","Contact | Rae &amp; Co Capital","One call, no pitch. Reach Tyler Krause at Rae &amp; Co Capital.",CONTACT),
 ("disclosures.html","Disclosures | Rae &amp; Co Capital","Registration, risk, fees and conflicts, stated plainly.",DISCLOSURES),
 ("form-crs.html","Form CRS Summary | Rae &amp; Co Capital","Relationship summary, services, fees and conflicts.",FORMCRS),
 ("privacy.html","Privacy Policy | Rae &amp; Co Capital","What we collect, how it is used, and what we never do with it.",PRIVACY),
 ("client-login.html","Client Access | Rae &amp; Co Capital","Go to your custodian or carrier portal directly.",CLIENTLOGIN),
 ("life-insurance-calculator.html","Life Insurance Calculator | Rae &amp; Co Capital","Drag the sliders and see your coverage gap. No name, no email, nothing stored.",CALCULATOR),
 ("types-of-life-insurance.html","Types of Life Insurance, Explained Plainly | Rae &amp; Co Capital","Term, whole, universal, IUL, disability income, long-term care, term variants and final expense. What each solves, what it costs you, and when it is the wrong tool.",types_page()),
 ("life-insurance-quote.html","Get a Life Insurance Quote Online | Rae &amp; Co Capital","Compare real life insurance quotes across 46 carriers and apply online in the same session. No agent call required to see your rates.",QUOTE),
 ("life-insurance-review-checklist.html","Life Insurance Review Checklist | Rae &amp; Co Capital","Six things to check before you change or replace a life insurance policy. Obligations, ownership, beneficiaries and liquidity, not just premium.",CHECKLIST),
 ("services.html","Services | Rae &amp; Co Capital","Investment management, retirement planning, financial planning and life insurance, coordinated in one virtual advisory relationship.",SERVICES),
 ("thank-you.html","Thank You | Rae &amp; Co Capital","Your message reached Rae &amp; Co Capital.",THANKYOU),
 ("life-insurance-protection-review.html","Life Insurance Protection Review | Rae &amp; Co Capital","Have existing life insurance and coverage gaps reviewed against income, debt, dependents and business exposure. Greenville, South Carolina.",REVIEW),
]

for g in GEO:
    slug,title,desc = g[0],g[1],g[2]
    PAGES.append((slug,title,desc,geo_page(slug,*g[3:])))

for slug,title,desc,body in PAGES:
    (OUT/slug).write_text(shell(slug,title,desc,body),encoding="utf-8")
    print("wrote",slug)
print("done:",len(PAGES),"pages")

# Sitemap is generated from PAGES so it can never drift from what was built.
# Only emitted once STAGING is off, because a sitemap that advertises noindex
# pages just wastes crawl budget.
if not STAGING:
    PRIORITY = {"index.html":"1.0","life-insurance-greenville-sc.html":"0.9",
                "financial-advisor-greenville-sc.html":"0.9",
                "investment-management-greenville-sc.html":"0.9",
                "retirement-planning-greenville-sc.html":"0.9",
                "life-insurance-calculator.html":"0.8","life-insurance-quote.html":"0.8",
                "types-of-life-insurance.html":"0.8","wealth.html":"0.8",
                "protection.html":"0.8","planning.html":"0.8"}
    SKIP = {"thank-you.html"}
    urls = "\n".join(
      f"  <url><loc>{ORIGIN}/{'' if s=='index.html' else s}</loc>"
      f"<priority>{PRIORITY.get(s,'0.6')}</priority></url>"
      for s,_,_,_ in PAGES if s not in SKIP)
    (OUT.parent/"sitemap.xml").write_text(
      '<?xml version="1.0" encoding="UTF-8"?>\n'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + urls + "\n</urlset>\n")
    print("wrote sitemap.xml (%d urls)" % (len(PAGES)-len(SKIP)))
else:
    print("STAGING=True: noindex on, sitemap NOT regenerated")
