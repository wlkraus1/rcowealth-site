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
                    if (p := OUT/"assets"/"carriers"/(slug+e)).exists()), None)
        if art:
            w, h = art_size(art)
            px = min(48, round(62 / (w/h) ** .5))
            inner = (f'<img src="/assets/carriers/{art.name}" alt="{name}" '
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
# NEVER submit one of these while testing - it creates a real lead in FSC
# and pings Tyler's Telegram. The lead path is Pi funnel -> FSC -> Telegram;
# Salesforce is NOT in it (out since 2026-08-06, the field names are legacy schema).
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
    is what routes the lead correctly in FSC - it is easy to miss because
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
          <a href="https://www.tiktok.com/@rcowealth" target="_blank" rel="noopener" aria-label="Rae &amp; Co Capital on TikTok"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19.6 7.3a5 5 0 0 1-3.4-1.3 5 5 0 0 1-1.6-3.1h-3.1v12.4a2.9 2.9 0 1 1-2.1-2.8V9.3a6 6 0 1 0 5.2 6V9.6a8 8 0 0 0 4.9 1.6z"/></svg></a>
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
  "areaServed":[
    {"@type":"City","name":"Greenville","containedInPlace":{"@type":"State","name":"South Carolina"}},
    {"@type":"City","name":"Spartanburg","containedInPlace":{"@type":"State","name":"South Carolina"}},
    {"@type":"City","name":"Anderson","containedInPlace":{"@type":"State","name":"South Carolina"}},
    {"@type":"City","name":"Simpsonville","containedInPlace":{"@type":"State","name":"South Carolina"}},
    {"@type":"City","name":"Mauldin","containedInPlace":{"@type":"State","name":"South Carolina"}},
    {"@type":"City","name":"Greer","containedInPlace":{"@type":"State","name":"South Carolina"}},
    {"@type":"City","name":"Taylors","containedInPlace":{"@type":"State","name":"South Carolina"}},
    {"@type":"City","name":"Easley","containedInPlace":{"@type":"State","name":"South Carolina"}},
    {"@type":"City","name":"Travelers Rest","containedInPlace":{"@type":"State","name":"South Carolina"}},
    {"@type":"City","name":"Fountain Inn","containedInPlace":{"@type":"State","name":"South Carolina"}},
    {"@type":"State","name":"South Carolina"},
    "US"],
  "address":{"@type":"PostalAddress","addressLocality":"Greenville","addressRegion":"SC","addressCountry":"US"},
  "sameAs":["https://www.instagram.com/rcowealth/","https://www.facebook.com/RcoWealth","https://www.youtube.com/@rcowealth","https://www.tiktok.com/@rcowealth"],
  "founder":{"@type":"Person","name":"Tyler Krause","jobTitle":"Founder & Private Wealth Advisor","alumniOf":"Arizona State University","knowsAbout":["Behavioral finance","Psychology of money","Financial planning","Life insurance"]}
}"""

def shell(slug, title, desc, body, canvas=False, extra_ld=""):
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
                      f'<meta property="og:image" content="{ORIGIN}/assets/og-card.png">\n'
                      f'<meta property="og:image:width" content="1200">\n'
                      f'<meta property="og:image:height" content="630">\n'
                      f'<meta name="twitter:image" content="{ORIGIN}/assets/og-card.png">\n'
                      f'<meta name="twitter:card" content="summary_large_image">\n'
                      f'<meta name="twitter:title" content="{title}">\n'
                      f'<meta name="twitter:description" content="{desc}">')
    ld = f'\n<script type="application/ld+json">{LD}</script>'  # org schema on every page for entity SEO
    ld += extra_ld  # page-level FAQPage / Service / Breadcrumb blocks, see page_ld()
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{index_meta}
<meta name="google-site-verification" content="VYQlcefljOic4ThdXdbPbbdZ1O5wRNZ5QuVxPpeNEB4">
{'<meta name="robots" content="noindex">' if slug == "start-plan.html" else ''}
<meta name="theme-color" content="#06111f">
<link rel="icon" href="/favicon.ico?v=goldleaf-20260521-1647">
<link rel="stylesheet" href="rco.css?v={asset_v('rco.css')}">
<noscript><style>[data-rv],.stagger>*{{opacity:1!important;transform:none!important}}</style></noscript>{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hd">
  <div class="wrap bar">
    <a class="brand" href="index.html" aria-label="Rae &amp; Co Capital home"><img src="/assets/rae-co-logo-header.png" alt="Rae &amp; Co Capital Wealth Management"></a>
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
        <img src="/assets/rae-co-logo-light.png" alt="Rae &amp; Co Capital">
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
      <nav aria-label="Greenville"><p class="ftlabel">Greenville, SC</p>
        <a href="financial-advisor-greenville-sc.html">Financial advisor</a>
        <a href="life-insurance-greenville-sc.html">Life insurance</a>
        <a href="retirement-planning-greenville-sc.html">Retirement planning</a>
        <a href="investment-management-greenville-sc.html">Investment management</a>
        <a href="services.html">All services</a>
      </nav>
      <nav aria-label="Legal"><p class="ftlabel">Legal</p>
        <a href="disclosures.html">Disclosures</a>
        <a href="form-crs.html">Form CRS</a>
        <a href="/form-crs.pdf" target="_blank" rel="noopener">Form CRS (PDF)</a>
        <a href="privacy.html">Privacy</a>
        <a href="client-login.html">Client login</a>
      </nav>
    </div>
    <p class="legal">{LEGAL}</p>
  </div>
</footer>
<script src="rco.js?v={asset_v('rco.js')}"></script>
<script src="/campaign-tracking.js?v={asset_v('campaign-tracking.js')}" defer></script>
<script src="/tracking-tags.js?v={asset_v('tracking-tags.js')}" defer></script>
</body>
</html>
"""

# ------------------------------------------------------------ FAQ + LOCAL DEPTH
# SEO depth pass, 2026-08-23. Two facts drove it: (1) the four Greenville pages
# were one template with the nouns swapped (488/488/490/524 words), which is the
# doorway-page fingerprint Google demotes; (2) the FAQPage schema that shipped
# 2026-08-10 did not survive the rebuild. FAQ copy lives once, in FAQS, and is
# rendered twice: visible <details> on the page (Google requires the answers to
# be on-page) and a FAQPage JSON-LD block in <head>. Every answer here is
# educational and carries no performance, guarantee, or fee-only language.
import json as _json, html as _html

def _plain(s):
    """HTML answer -> plain text for JSON-LD."""
    return _html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

FAQS = {
 "life-insurance-greenville-sc.html": [
  ("How much does term life insurance cost in Greenville, SC?",
   "It depends on age, health, tobacco use, the amount, the term length and which carrier writes it. "
   "In August 2026 a healthy 35-year-old non-smoker running a $500,000, 20-year term quote through our tool saw starting rates around $25 a month. "
   "Your number will differ, and a quote is an estimate rather than an offer. <a href=\"life-insurance-quote.html\">Run your own quote</a> and you will see the actual range for your situation in about two minutes."),
  ("Is the life insurance I get through work enough?",
   "Usually not on its own. Group plans at most Upstate employers pay one or two times salary, sometimes with a cap, and the coverage ends when you leave the job. "
   "Add up the mortgage, the years of income your family would need, and anything you want set aside for the kids, then compare that to the group number. The <a href=\"life-insurance-calculator.html\">coverage calculator</a> does the arithmetic without asking for your name."),
  ("Can I get a life insurance quote without a phone call?",
   "Yes. The quote tool shows real carrier pricing and lets you apply online in the same sitting. Nobody calls you to unlock a number. If you want a second set of eyes before you buy, I do that too, and I will tell you if you already have enough."),
  ("Do I need a medical exam?",
   "Often not. Many carriers now use accelerated underwriting for healthy applicants under a certain age and amount, which means health questions and a records check instead of a paramedical exam. "
   "Larger amounts, older ages or certain health histories still get an exam. The quoter shows which path each carrier offers before you apply."),
  ("What is the difference between term and whole life?",
   "Term covers you for a set number of years at a fixed price and then ends. It is the cheapest way to buy a large death benefit while the mortgage and the kids are still there. "
   "Whole life is permanent, builds cash value, and costs many times more for the same death benefit. For most Greenville families with a mortgage and children, term comes first. The <a href=\"types-of-life-insurance.html\">types page</a> walks the whole menu, including when permanent coverage makes sense."),
  ("Do you only sell one company's policies?",
   "No. Coverage is shopped across 40+ carriers through one application, and you see the same pricing I see. Rae &amp; Co Capital is paid a commission by the carrier when a policy is placed. That is a conflict of interest, it is disclosed, and it is the reason the advice here starts with whether you need coverage at all."),
  ("What happens to my SGLI when I leave the military?",
   "SGLI coverage continues for 120 days after separation, then ends. You can convert to VGLI, or you can buy a private term policy, and for healthy people in their 20s and 30s private term is often the cheaper route for the same amount. "
   "Compare both before the 120 days are up. I am a Marine Corps veteran and this is a conversation I have often."),
 ],
 "financial-advisor-greenville-sc.html": [
  ("Do I need a financial advisor if I just have a 401(k) and a mortgage?",
   "Maybe not an ongoing one. A lot of households in that spot need one clear plan, not a relationship. That is what the $750 Foundations plan is for: cash flow, the debt-versus-invest question, a retirement savings roadmap, and a one-page action list. "
   "If you do not need me yet, I will say so on the first call."),
  ("What does a financial advisor cost in Greenville?",
   "It depends on how they are paid, and many will not tell you until after a meeting. Here the prices are published. Flat-fee planning is $750, $2,000 or $3,000 one time. Investment management is 1% per year of the assets I manage, with planning included. "
   "When insurance is placed through the firm, a carrier commission is paid and disclosed."),
  ("Are you a fiduciary?",
   "For advice, yes. I hold the Series 65 and act as an investment adviser representative, which carries a fiduciary duty to you. I am also licensed for life, accident and health insurance in South Carolina, and when a policy is placed I am paid by commission. "
   "I tell you which role I am in and how I am paid every time, and it is all in the Form CRS and disclosures."),
  ("Is everything virtual?",
   "Yes, by design. Meetings are by Zoom or phone, documents are shared securely, and you keep everything in writing. I am based in Greenville, and that lets me work with households across the Upstate and the rest of South Carolina without anyone driving anywhere."),
  ("What is the difference between a financial planner and a financial advisor?",
   "Legally, not much. Both titles are used loosely. What matters is how the person is registered and paid. An investment adviser representative owes you a fiduciary duty. A broker is held to a best-interest standard on recommendations. An insurance agent is paid by the carrier. "
   "Ask anyone you are considering which of those they are, and what the fee is, before the second meeting."),
  ("What should I bring to a first call?",
   "Your rough numbers are enough: income, what you owe, what you have saved, what insurance you carry through work, and the one or two decisions you are stuck on. No statements are needed for the first conversation. "
   "Please leave account numbers and Social Security numbers out of any form you send."),
  ("Do you work with people outside Greenville?",
   "Yes. Most clients are in the Upstate, including Spartanburg, Anderson, Easley, Greer, Simpsonville and Mauldin, and the firm works with households across South Carolina. If you live in another state, ask, and I will tell you whether I can help there."),
 ],
 "retirement-planning-greenville-sc.html": [
  ("Does South Carolina tax retirement income?",
   "South Carolina does not tax Social Security benefits and fully exempts military retirement pay from state income tax. Pension, 401(k) and IRA withdrawals are taxable, with a retirement income deduction and a further deduction once you reach 65. "
   "This is general information, not tax advice. Your tax preparer can tell you what applies to your return."),
  ("When should I take Social Security?",
   "There is no single right answer. Claiming at 62 gives a smaller check for longer. Waiting past full retirement age grows the check each year until 70. Health, whether you are still working, a spouse's record and what else you can draw on all change the answer. "
   "The retirement income plan works this out with your numbers rather than a rule of thumb."),
  ("How much do I need to retire in Greenville?",
   "Start with what you actually spend in a year, not a national average. A common starting point is yearly spending times 25, then stress-test it against your pension, Social Security and how the first few years of withdrawals would go in a bad market. "
   "The <a href=\"wealth.html#tool\">retirement income check</a> on the wealth page gives you a first read in about a minute."),
  ("Should I roll my 401(k) into an IRA when I leave my employer?",
   "Not automatically. You generally have four options: leave it, move it to a new employer's plan, roll it to an IRA, or cash out. Each has different costs, investment choices, creditor protection and tax consequences. "
   "Rolling it to an account I manage pays me 1% a year, so that is a conflict of interest. I will show you the leave-it-where-it-is math before anything moves."),
  ("What does retirement planning cost?",
   "On its own, it is a flat fee: $750, $2,000 or $3,000 one time, depending on scope, agreed in writing before work begins. If I manage your investments, planning is already included in the 1% and there is no second fee."),
  ("Do you sell annuities?",
   "Fixed and indexed annuities are placed when they fit a retirement income plan, and never as a requirement. When one is placed, the carrier pays a commission, which is disclosed. If a simpler answer works, that is the one you will get."),
 ],
 "investment-management-greenville-sc.html": [
  ("What does investment management cost?",
   "1% per year of the assets I manage, billed quarterly, with a $750 annual minimum, and financial planning is included. Fund expense ratios and any custodian charges are separate and shown to you. "
   "There are no commissions on managed accounts and no trading fee from me."),
  ("Where is my money held?",
   "At Charles Schwab, in an account in your name. I never take custody. You can log in to Schwab Alliance and see every holding and transaction at any time, and Schwab sends its own statements."),
  ("Is there a minimum?",
   "There is no hard minimum, but the $750 annual minimum fee means that below roughly $75,000 the fee is more than 1%. On a smaller balance I will tell you to buy a flat-fee plan and invest it yourself. "
   "That is a worse deal for me and the right one for you."),
  ("Do you pick stocks or try to beat the market?",
   "No. Portfolios are built from low-cost, diversified funds, set by the plan rather than by headlines, and rebalanced on a schedule. Investing involves risk, including loss of principal, and nobody can promise a return. "
   "The work I am paid for is the allocation, the tax placement, the withdrawal order, and keeping you from selling at the bottom."),
  ("Can you manage my 401(k) where it is?",
   "Generally no. Workplace plans stay with the plan's record keeper. I can review the fund lineup and recommend an allocation as part of planning. Old 401(k)s, IRAs, Roth IRAs and taxable accounts can be managed directly at Schwab."),
  ("How often will we talk?",
   "A scheduled review at least once a year, and more often when something changes: a job, a house, a child, an inheritance, a retirement date. Between reviews you call or text and I answer. The firm is deliberately small so that stays true."),
 ],
 "life-insurance-quote.html": [
  ("How much does life insurance cost in South Carolina?",
   "Cost depends on your age, health, coverage amount, term length, and the carrier's underwriting. Healthy applicants in their 30s often find term coverage costs less than a monthly streaming bundle. "
   "You can compare real quotes from major carriers yourself in about two minutes using the quoting tool on this page, with no phone call required."),
  ("Can I get a life insurance quote without talking to an agent?",
   "Yes. The quote tool on this page lets you run your own quotes across major carriers and start an application on your own. Rae &amp; Co Capital is available if you want a second set of eyes, but no call is required to see rates."),
  ("How much life insurance do I need?",
   "A common approach adds up debts including the mortgage, the income your family would need replaced for a set number of years, and goals for the children, then subtracts existing savings and coverage. "
   "The free <a href=\"life-insurance-calculator.html\">needs calculator</a> walks through this with no contact information required."),
  ("Is employer life insurance enough?",
   "Most group plans through work provide one to two times salary and typically end when the job ends. Many families find that amount falls short of replacing income, clearing a mortgage, and covering children's needs, which is why individual coverage is often reviewed alongside it."),
  ("What happens after I apply online?",
   "The carrier underwrites the application. For many healthy applicants that is a records check and no exam; others are asked for a short paramedical exam. Approval can take anywhere from a day to a few weeks depending on the carrier and your history. "
   "Nothing is in force until the carrier issues the policy and the first premium is paid."),
  ("Can I cancel if I change my mind?",
   "Yes. South Carolina law gives you at least 10 days from the date a life insurance policy is delivered to return it for a full refund of premium, and 30 days for a policy sold by mail. After that, term coverage can be cancelled at any time by stopping premium payments; there is no surrender charge on term."),
 ],
 "life-insurance-calculator.html": [
  ("How accurate is this life insurance calculator?",
   "It is an estimate built only from the numbers you enter. It does not know about a spouse's income, Social Security survivor benefits, savings, or taxes, so treat the result as a starting point for a conversation rather than a final number."),
  ("What number should I use for income replacement years?",
   "A common approach is the years until your youngest child is independent, or until the mortgage is paid off, whichever is longer. Some families plan to a spouse's retirement date instead. Pick the one that matches what you would want to happen."),
  ("Should I include my coverage through work?",
   "Yes, in the existing coverage field, but use the real number from your benefits summary. It is usually one or two times salary, and it ends when the job does, so many people choose not to count all of it."),
 ],
 "types-of-life-insurance.html": [
  ("Which type of life insurance is best for a young family?",
   "For most young families with a mortgage and children, level term is the right first policy. It buys the largest death benefit for the least money during the years the family is most exposed. Permanent coverage can make sense later, for specific reasons, after term is in place."),
  ("Is whole life a good investment?",
   "It is insurance first. Cash value grows slowly, early-year costs are high, and surrendering in the first several years usually returns less than was paid. It can fit estate, special-needs or business situations, or someone who wants a guaranteed death benefit for life. "
   "For investing, most people are better served by low-cost funds in a retirement account, and I will say that plainly when it is true."),
  ("How long a term should I buy?",
   "Match it to the obligation. If the youngest child is 3 and the mortgage has 27 years left, a 20- or 30-year term covers the window that matters. Shorter terms cost less per month but leave you re-qualifying later at an older age."),
  ("What is indexed universal life and should I buy it?",
   "IUL is permanent coverage whose cash value is credited based on an index, with caps and floors set by the carrier, and it carries internal costs that rise with age. It is sold hard, and I do not lead with it. "
   "Read the IUL section above, and if someone is pitching it to you as a retirement plan, get a second read first."),
  ("Can I have more than one life insurance policy?",
   "Yes. It is common to stack a term policy on top of group coverage, or to ladder two term policies with different lengths so coverage steps down as obligations shrink. Carriers will ask about existing coverage during underwriting and total coverage has to be justifiable by income and obligations."),
 ],
 "wealth.html": [
  ("What is included in the 1% management fee?",
   "Portfolio management, rebalancing, tax-aware account placement, withdrawal sequencing in retirement, and full financial planning. One fee per household, billed quarterly on the assets I manage, with a $750 annual minimum. Fund expenses and custodian charges are separate and disclosed."),
  ("Where are client assets held?",
   "At Charles Schwab, in accounts titled in your name. The firm never takes custody of client money. You can log in to Schwab at any time and see everything."),
  ("What does the retirement income check actually tell me?",
   "Whether the savings, the monthly contribution and the growth rate you assume add up to the income you want at the age you pick. The growth rate is yours to set because nobody can promise one, and moving it shows how much the answer depends on that one assumption."),
  ("When would you tell someone not to hire you for management?",
   "When the balance is small enough that the $750 minimum makes the fee a poor deal, when someone already runs a disciplined low-cost portfolio and just needs a plan, or when what they really want is a trader. In each case a flat-fee plan is the better buy and I will say so."),
 ],
 "planning.html": [
  ("Which plan should I pick?",
   "Most households land on Household at $2,000. If you have one or two specific questions, Foundations at $750 is enough. If you want help actually opening accounts and making the changes, Household + Implementation at $3,000 adds guided execution. "
   "If you are unsure, text me which one and I will tell you the cheaper answer when it is the right one."),
  ("Is planning included if you manage my investments?",
   "Yes. If I manage your assets, planning is already part of the 1% and you do not buy a flat-fee plan on top. These prices are for people who want the plan and will run it themselves."),
  ("What is not included in a flat-fee plan?",
   "Tax preparation, legal documents, trade execution, and ongoing investment management. Insurance is never required, and when it is placed through the firm a carrier commission is paid and disclosed."),
  ("What if we stop early?",
   "Every plan is a one-time engagement completed within six months. The fee is agreed in writing before any work begins, and if we stop early the unearned prepaid portion is returned."),
 ],
}

def faq_block(slug, kicker="Questions people ask", h2="Straight answers, before the call.", lede="", dark=False):
    items = FAQS[slug]
    rows = "".join(
        f'\n      <details><summary>{q}</summary><div class="faq-a"><p>{a}</p></div></details>'
        for q, a in items)
    lede_html = f'\n    <p class="lede" data-rv style="max-width:74ch">{lede}</p>' if lede else ""
    return f"""
<section class="section{' dark' if dark else ' cream'}" id="faq">
  <div class="wrap">
    <p class="kicker" data-rv>{kicker}</p>
    <h2 class="sub" data-rv>{h2}</h2>{lede_html}
    <div class="faq" data-rv>{rows}
    </div>
  </div>
</section>"""

def faq_ld(slug):
    return _json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": _plain(q),
                        "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}}
                       for q, a in FAQS[slug]]}, ensure_ascii=False, separators=(",", ":"))

CALC_LD = _json.dumps({
  "@context":"https://schema.org","@type":"WebApplication",
  "name":"Life Insurance Needs Calculator","applicationCategory":"FinanceApplication",
  "operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},
  "url":"https://rcowealth.com/life-insurance-calculator.html",
  "description":"Free calculator that estimates how much life insurance coverage a household needs, with no contact information required.",
  "provider":{"@type":"FinancialService","name":"Rae & Co Capital, LLC","telephone":"+1-864-558-8440",
              "areaServed":{"@type":"State","name":"South Carolina"},"url":"https://rcowealth.com"}},
  separators=(",", ":"))

# Per-page Service + BreadcrumbList for the four Greenville pages. serviceType
# is the query the page targets; areaServed is the real service footprint.
GEO_SERVICE = {
 "financial-advisor-greenville-sc.html": ("Financial planning", "Financial planning"),
 "investment-management-greenville-sc.html": ("Investment management", "Investment management"),
 "retirement-planning-greenville-sc.html": ("Retirement income planning", "Retirement planning"),
 "life-insurance-greenville-sc.html": ("Life insurance planning", "Life insurance"),
}
def geo_ld(slug):
    stype, crumb = GEO_SERVICE[slug]
    svc = {"@context":"https://schema.org","@type":"Service","serviceType":stype,
           "name":f"{stype} in Greenville, SC",
           "url":f"{ORIGIN}/{slug}",
           "provider":{"@type":"FinancialService","name":"Rae & Co Capital, LLC","url":ORIGIN,
                       "telephone":"+1-864-558-8440"},
           "areaServed":[{"@type":"City","name":"Greenville"},{"@type":"City","name":"Spartanburg"},
                         {"@type":"City","name":"Anderson"},{"@type":"State","name":"South Carolina"}],
           "availableChannel":{"@type":"ServiceChannel","serviceUrl":f"{ORIGIN}/{slug}",
                               "servicePhone":"+1-864-558-8440","availableLanguage":"en"}}
    bc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
           {"@type":"ListItem","position":1,"name":"Home","item":ORIGIN+"/"},
           {"@type":"ListItem","position":2,"name":"Services","item":ORIGIN+"/services.html"},
           {"@type":"ListItem","position":3,"name":f"{crumb} in Greenville, SC","item":f"{ORIGIN}/{slug}"}]}
    return (_json.dumps(svc, separators=(",", ":")), _json.dumps(bc, separators=(",", ":")))

def page_ld(slug):
    """Everything that goes in <head> after the org block, as script tags."""
    blocks = []
    if slug in FAQS: blocks.append(faq_ld(slug))
    if slug in GEO_SERVICE: blocks.extend(geo_ld(slug))
    if slug == "life-insurance-calculator.html": blocks.append(CALC_LD)
    return "".join(f'\n<script type="application/ld+json">{b}</script>' for b in blocks)


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
      <div class="advisor-clip">
        <video autoplay muted loop playsinline preload="metadata" poster="assets/media/tyler-hero.jpg" aria-label="Tyler Krause working at his desk">
          <source src="assets/media/tyler-hero.mp4" type="video/mp4">
        </video>
        <div class="cap">
          <span class="live" aria-hidden="true"></span>
          <div><b>Tyler Krause</b><small>Series 65 fiduciary &middot; USMC veteran &middot; answers the phone</small></div>
        </div>
      </div>
      <p style="margin:18px 0 0;font:600 13px/1.6 var(--sans);color:var(--muted)">Assets custodied at Charles Schwab &middot; 40+ insurance carriers</p>
    </div>
    <div class="tool" data-rv>
      <p class="tag" style="font:800 12px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase;color:var(--gold-ink);margin:0 0 6px">60-second answer</p>
      <h2 class="sub" style="margin-bottom:20px">What would your family need if your income stopped?</h2>
      <div class="chips" role="group" aria-label="What are you protecting?">
        <button class="chip" type="button" aria-pressed="false" data-add="250000">A home</button>
        <button class="chip" type="button" aria-pressed="false" data-add="80000">Kids' education</button>
        <button class="chip" type="button" aria-pressed="true" data-add="15000">Final expenses</button>
      </div>
      <div class="frow">
        <label for="inc">Your income <output id="incOut">$70,000</output></label>
        <input type="range" id="inc" min="20000" max="400000" step="5000" value="70000" aria-label="Your annual income">
      </div>
      <div class="readout">
        <div><small>Rough coverage need</small><span class="num" id="need">$365,000</span></div>
        <a id="full" href="life-insurance-calculator.html">Run the full number &rarr;</a>
      </div>
      <p class="fine">Five years of income, plus what you selected. A starting point, not advice.</p>
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
        <p>Portfolios at Schwab, retirement income, 1% per year of assets under management with a $750 annual minimum. Planning is included.</p>
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
    <p class="lede" data-rv style="max-width:64ch">Rae &amp; Co is a registered investment adviser that also places insurance, not an insurance agency with a planning page. Portfolios sit at Charles Schwab in your name, priced at 1% per year of assets under management with a $750 annual minimum, and the retirement income work is where most of the value actually shows up.</p>
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

{HOMEFORM}
<section class="section">
  <div class="wrap split b">
    <figure style="margin:0" data-rv>
      <img src="/assets/tyler-krause.jpg" alt="Tyler Krause, Founder and Private Wealth Advisor" style="width:100%;aspect-ratio:7/10;object-fit:cover;object-position:50% 22%;border-radius:14px;box-shadow:0 40px 90px -46px rgba(6,17,31,.55)">
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
  <div class="wrap split a top">
    <div>
      <p class="kicker" data-rv>60-second answer</p>
      <h2 data-rv style="max-width:19ch">Will it pay you <em class="g">enough</em> to stop working?</h2>
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
    <p class="kicker center" data-rv>The management fee</p>
    <h2 data-rv>1% per year, only on what <em class="g" style="color:var(--gold-2)">we manage</em>.</h2>
    <p class="lede" data-rv style="margin-left:auto;margin-right:auto">$750 annual minimum, billed quarterly in arrears under a signed advisory agreement. It applies only to accounts we manage, and nothing else. Planning is part of the job, not a second bill: management clients never pay the flat planning fees. Insurance is priced separately on its own page. No commission on investments, no product quotas, no sales desk above me.</p>
    <div class="grid g3 stagger" data-rv style="margin-top:36px;text-align:left">
      <div class="card"><p class="tag">Custody</p><h3 style="font-size:22px">Charles Schwab</h3><p>Your money sits with Schwab in your name. I never hold it, and you can see it any time.</p></div>
      <div class="card"><p class="tag">Standard</p><h3 style="font-size:22px">Series 65 fiduciary</h3><p>Held to a fiduciary standard on advisory work. Insurance commissions are a separate, disclosed conflict.</p></div>
      <div class="card"><p class="tag">Honest limit</p><h3 style="font-size:22px">When not to hire me</h3><p>On a small balance the $750 minimum is a poor deal. If that is you, buy a flat-fee plan instead and invest it yourself.</p></div>
    </div>
    <div class="acts" data-rv style="justify-content:center;margin-top:36px">
      <a class="btn btn-gold" href="https://scheduler.zoom.us/raecocapital/introductory-consultation" target="_blank" rel="noopener">Book a portfolio review <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="planning.html">See flat-fee planning</a>
    </div>
    <p style="margin:26px auto 0;max-width:74ch;font:400 12px/1.65 var(--sans);color:rgba(244,239,228,.5)" data-rv>Advisory fees are 1% per year of assets under management with a $750 annual minimum, billed quarterly in arrears under a signed advisory agreement. Investing involves risk including possible loss of principal. No advice is provided until that agreement is in place.</p>
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
    <p class="cnum" data-rv>40+</p>
    <h2 class="cclaim" data-rv>leading carriers available through one application</h2>
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
  .replace("{MORE}", f"+ {len(ROSTER)} more, all named below")
  .replace("{CELLS}", carrier_cells())
  .replace("{ROSTERCELLS}", "".join(f"<span>{n}</span>" for n in ROSTER)))
PROTECTION = PROTECTION.replace("{CARRIERWALL}", CARRIERWALL) + form_section(
  "Not ready to quote", "Have what you already own checked first.",
  "Send what you have and who depends on you. If the answer is that you do not need more, "
  "that is the answer you will get. Please leave policy numbers out of the form.",
  lead_form("protection-page","protection.html","life-insurance-planning",
            "Request a coverage review","Replies come from me, usually the same day.",
            "Insurance","Life insurance planning", cta="Request a review", insurance=True,
            placeholder="Example: 20 year term from 2015 plus group cover at work, "
                        "two kids under 10, and I am not sure it is still enough."))
# Same wall closes the home page, with its own utm_content so the two entry
# points stay separable in reporting.
HOME = HOME.replace("{HOMEFORM}", form_section(
  "No appointment needed", "Or just tell me what is going on.",
  "If none of the self-service paths fit, write a sentence about what is on your mind. "
  "I read these myself and reply personally, usually the same day.",
  lead_form("website-general-consultation","index.html","consultation-request",
            "Send a note","Replies come from me, usually the same day.",
            "Not sure","Focused intro call", cta="Send it"), cream=True))
HOME = HOME.replace("{CARRIERWALL}",
  CARRIERWALL.replace("utm_content=protection_carriers","utm_content=home_carriers"))

# ---------------------------------------------------------------- PLANNING
TIERS = [
 ("Foundations","$750","For a clear starting plan around one or two priorities.",
  ["Discovery meeting plus a plan-delivery meeting","Cash flow and emergency fund review",
   "Debt pay-down vs invest analysis, ranked by your actual rates","Retirement savings starting roadmap",
   "Written one-page action plan you keep","30 days of email follow-up"],
  "start-plan.html?tier=foundations","Start Foundations",False),
 ("Household","$2,000","For a full picture, usually a couple with a few moving parts.",
  ["Four meetings in all: discovery, two working sessions, plan delivery",
   "Full household cash flow and net worth build-out",
   "Goal planning: retirement, major purchases, education","Insurance needs review, life and disability gaps",
   "Tax-aware account strategy, Roth vs traditional and contribution order",
   "Written household plan you keep, plus everything in Foundations",
   "60 days of email follow-up"],
  "start-plan.html?tier=household","Start Household",True),
 ("Household + Implementation","$3,000","For help executing, not just a document.",
  ["Everything in Household, plus","Guided implementation support","Account setup walkthroughs",
   "Beneficiary and titling review","Up to three additional working sessions",
   "You execute every account change; I guide, never take control"],
  "start-plan.html?tier=implementation","Start Implementation",False),
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
    <p class="lede" data-rv style="margin-left:auto;margin-right:auto">One thing before you buy. If I manage your investments, planning is already included in the 1%. These flat fees are for people who want the plan and will run it themselves.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="tiergrid stagger" data-rv>
      """ + "\n      ".join(tier_html(t) for t in TIERS) + """
    </div>
    <p class="tnote" data-rv>Paying starts the engagement. The written planning agreement follows by email the same day for signature, and the discovery meeting is part of the work rather than a sales call you have to pass first.</p>
    <p style="margin:22px auto 0;max-width:80ch;text-align:center;font:400 12px/1.65 var(--sans);color:var(--muted)" data-rv>Every tier is a one-time engagement completed within six months; it is not a subscription. The flat fee is agreed in writing before any work begins. If we stop early, any unearned prepaid portion is returned. Insurance is optional and never required through the firm. Planning is analysis and education; there are no performance promises, and investing involves risk including loss of principal. <b>What is not included, in any tier:</b> tax preparation, legal documents, trade execution, and ongoing investment management. Management is a separate engagement at 1% per year of assets under management, and it includes planning, so these flat fees apply only when planning is bought on its own. I will tell you plainly if you do not need management.</p>
  </div>
</section>

<section class="section cream">
  <div class="wrap center">
    <h2 data-rv>Not sure which one?</h2>
    <p class="lede" data-rv style="margin-left:auto;margin-right:auto">Most households land on Household. If you only have one or two questions, Foundations is enough. If in doubt, ask me and I will tell you the cheaper answer when it is the right one.</p>
    <div class="acts" data-rv style="justify-content:center">
      <a class="btn btn-ink" data-magnetic href="sms:+18645588440?&amp;body=Hi%20Tyler%2C%20not%20sure%20which%20planning%20tier%20fits.%20My%20situation%3A%20">Text me which one fits <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="wealth.html">Or see ongoing management</a>
    </div>
  </div>
</section>
""" + faq_block("planning.html", "Before you buy", "Four questions, answered before checkout.")

# ---------------------------------------------------------------- ADVISOR
ADVISOR = """
<section class="section" style="padding-bottom:0">
  <div class="wrap split b top">
    <figure style="margin:0" data-rv>
      <img src="/assets/tyler-krause.jpg" alt="Tyler Krause, Founder and Private Wealth Advisor" style="width:100%;aspect-ratio:7/10;object-fit:cover;object-position:50% 22%;border-radius:14px;box-shadow:0 40px 90px -46px rgba(6,17,31,.55)">
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
      <div class="card"><h3 style="font-size:22px">No pushing AUM that does not fit</h3><p>Management is 1% per year of assets under management with a $750 annual minimum. On a small balance that is a poor deal, and I will tell you to buy a flat-fee plan and invest it yourself.</p></div>
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
    <div class="clines two" data-rv style="margin-top:30px">
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
 ("Full document","<a href='/form-crs.pdf' target='_blank' rel='noopener'><b>Download the complete Form CRS (PDF)</b></a>, version dated May 9, 2026. Also available: <a href='/form-adv-2a.pdf' target='_blank' rel='noopener'>Form ADV Part 2A Firm Brochure (PDF)</a> and <a href='/form-adv-2b.pdf' target='_blank' rel='noopener'>Form ADV Part 2B Brochure Supplement (PDF)</a>. All are also available through the "
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
 ("Investment accounts","Schwab-custodied investment and retirement accounts live at Schwab Alliance, using the same login as Schwab.com. Never use a login link from an email; use this page or type the address yourself.<br><a class='btn btn-ink' style='margin-top:14px' href='https://www.schwaballiance.com' target='_blank' rel='noopener'>Log in at Schwab Alliance <span class='arr'>&rarr;</span></a>"),
 ("Insurance accounts","Policy, billing and customer access is handled through your carrier&rsquo;s own portal. Our preferred carrier is Mutual of Omaha, which uses Customer Access. For any other carrier, the portal depends on who issued the policy; ask and we will tell you.<br><a class='btn btn-ink' style='margin-top:14px' href='https://www.mutualofomaha.com/welcome/customer-access' target='_blank' rel='noopener'>Log in at Mutual of Omaha <span class='arr'>&rarr;</span></a>"),
 ("A warning worth repeating","Do not send account numbers, policy numbers, passwords, Social Security numbers, or sensitive financial data through any website form, including ours. If a message asks you to, it is not from us."),
])


# ---------------------------------------------------------------- CALCULATOR
# Ported into the shell because it was the LAST and worst one-way door: linked
# from every page footer, and it dropped a visitor onto the old layout with no
# route back. Field ids, the digit-stripping parse fix and the funnel
# wiring are preserved exactly; only the chrome changes.
CALCFIELDS = [
 ("income","Your annual income",True,0,400000,5000,70000,"$"),
 ("years","Years to replace it",False,0,40,1,5,""),
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
""" + faq_block("life-insurance-calculator.html", "Using the calculator", "Three things people ask about the number.")

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
{faq_block("types-of-life-insurance.html", "Choosing between them", "The questions that come up most.")}
<section class="section dark">
  <div class="wrap">
    <p class="kicker" data-rv>No small print</p>
    <h2 data-rv style="max-width:20ch">How we are paid, so you can <em class="g" style="color:var(--gold-2)">weigh the advice</em>.</h2>
    <p class="lede" data-rv style="max-width:76ch">Rae &amp; Co Capital is compensated by commission on insurance placed. Different products pay different amounts, and permanent products generally pay more than term. That is a conflict of interest, it is disclosed in our Form CRS and disclosures, and it is the reason the term section above says what it says.</p>
    <p class="lede" data-rv style="max-width:76ch">Coverage is shopped across 40+ carriers rather than sold from one shelf. Availability, pricing and features vary by product, state, health and underwriting. Nothing on this page is individualized insurance, tax, legal or investment advice, and no coverage exists until a carrier issues a policy.</p>
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
    <p class="lede" data-rv>Answer a few health and coverage questions and see actual pricing across 40+ carriers. You can apply online in the same session. Nobody phones you to unlock a number.</p>
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
{faq_block("life-insurance-quote.html", "Before you open it", "What people ask before they quote.")}
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
# ------------------------------------------------------- GREENVILLE PAGES
# Four local-intent pages, each written as its own page rather than one
# template with the nouns swapped (that is what shipped 2026-08-10 and it is
# the doorway-page pattern Google's helpful-content system demotes). Every
# local fact below was checked 2026-08-23: SC does not tax Social Security,
# fully exempts military retired pay (TY2022+), gives a 10-day free look on
# delivered life policies (30 by mail), and the named employers are the
# region's largest per the Upstate SC Alliance. No guaranty-association
# mention anywhere: SC law bars using it in solicitation. No fee-only, no
# performance language, no individualized tax advice.
CROSS = [("financial-advisor-greenville-sc.html","Financial planning"),
         ("investment-management-greenville-sc.html","Investment management"),
         ("retirement-planning-greenville-sc.html","Retirement planning"),
         ("life-insurance-greenville-sc.html","Life insurance")]

GEO = [
 dict(slug="life-insurance-greenville-sc.html",
  title="Life Insurance in Greenville, SC | Quote 40+ Carriers Online",
  desc="Life insurance for Greenville and Upstate South Carolina families. See real term rates across 40+ carriers in minutes, or have what you already own checked first. Veteran-owned, SC-licensed.",
  kicker="Protection planning",
  h1='Life insurance placed with <em class="g">real carriers</em>, tied to the plan.',
  lede="Coverage is the part that cannot wait for a good year. Price it yourself in a few minutes, or have what you already own checked before you buy anything else.",
  deep="life-insurance-quote.html", deep_cta="See my rates",
  alt="life-insurance-calculator.html", alt_cta="Run the coverage numbers",
  helps=["Existing policies and employer coverage","New term and permanent coverage needs",
         "Income replacement and debt exposure","Dependents, education, and family obligations",
         "Business-owner, buy-sell, or key-person risk",
         "Carrier fit, underwriting path, ownership, beneficiaries and estate coordination"],
  leave=["A coverage strategy tied to the financial plan","A gap and overlap summary",
         "Carrier, underwriting and application next steps when new coverage makes sense",
         "Replacement considerations before changing anything you already own"],
  sections=[
   dict(kicker="Greenville, specifically", h2="Why Upstate families usually have less coverage than they think.",
    paras=[
     "Most people I talk to in Greenville have life insurance through work and assume that box is checked. Prisma Health, Michelin's North American headquarters, GE's turbine plant, Bon Secours St. Francis, the school district, BMW up the interstate in Spartanburg: the big employers here all offer group life. It is usually one or two times salary, sometimes with a cap, and it is the least portable thing you own. It ends when you leave, and people change jobs.",
     "The second pattern is the mortgage. Greenville County has grown fast and home prices have followed. A household that bought in Simpsonville, Greer, Taylors or Travelers Rest in the last few years often carries a loan that is bigger than all of its group coverage combined. Paying that off is usually the first line in the math, before anyone talks about replacing income.",
     "The third is the small business. A lot of Upstate income comes from a shop, a practice or a trade with one or two owners. If one of them dies, the bank loan does not, and the surviving partner suddenly owns half of a business with the family of someone who is gone. That is where coverage comes in, before anyone talks about a portfolio.",
    ],
    cards=[("Through work","One to two times salary","Ends when the job does. Cannot be taken with you at the group price. Check the real number on your benefits summary, not the number you remember."),
           ("The house","Mortgage first","For most families the loan balance is the largest single obligation. Clear it in the math before you size the income piece."),
           ("The business","Partners and loans","Buy-sell funding and key-person cover are cheap compared with what happens without them. Most owners have neither.")]),
   dict(kicker="How the number works", h2="Three lines of arithmetic, then a quote.", cream=True,
    paras=[
     "Add up what would have to be paid off: the mortgage, car loans, anything with your name on it. Add the years of income your household would need, until the kids are grown or the house is paid, whichever is longer. Add what you want set aside for school. Subtract savings and the coverage you already have. The <a href=\"life-insurance-calculator.html\">coverage calculator</a> does this in about a minute and does not ask for your name.",
     "Then price it. In August 2026 a healthy 35-year-old non-smoker running a $500,000, 20-year term quote through our tool saw starting rates around $25 a month. Your number will differ with age, health, tobacco use, the amount, the term and the carrier, and a quote is an estimate rather than an offer. The point is that for most Greenville families the cost of closing the gap is a fraction of what they assume, and you can see your own range in two minutes without a phone call.",
     "If what comes back is higher than you expected, that is information too. Health, age and tobacco move the price a lot, and there are carriers that specialize in cases others rate up. That is the reason the quote runs across 40+ of them instead of one shelf.",
    ]),
   dict(kicker="South Carolina rules worth knowing", h2="What the state gives you, and what it does not.",
    paras=[
     "South Carolina law gives you at least 10 days from the day a life insurance policy is delivered to return it for a full refund of premium, and 30 days for a policy sold by mail. Nobody is stuck because they signed. Read the policy in that window and send it back if it is not what you were told.",
     "Beneficiary designations generally control who receives a life insurance payout, regardless of what a will says. After a marriage, divorce, birth or death in the family, the designation is the first document to check. That is general information, not legal advice; an attorney can confirm how it applies to you.",
     "Rae &amp; Co Capital is licensed in South Carolina for life, accident and health insurance. Coverage is placed through BackNine Insurance across 40+ carriers, the carrier pays a commission when a policy issues, and that conflict of interest is disclosed. It is also why the advice here starts with whether you need coverage at all.",
    ]),
   dict(kicker="Who this is for", h2="Buy it if this is you. Skip it if it is not.", cream=True,
    cards=[("Buy it","A mortgage, kids, or a spouse who depends on your income","Term, sized by the calculator, bought while you are young and healthy. This is most of the Upstate families I meet."),
           ("Buy it","A business partner, a business loan, or a key employee","Buy-sell or key-person coverage, owned and structured so the money lands where the agreement says."),
           ("Buy it","Leaving the military","SGLI ends 120 days after separation. Compare VGLI against private term before the window closes. For healthy people in their 20s and 30s, private term is often cheaper for the same amount."),
           ("Skip it","No debt, no dependents, and nobody relying on your paycheck","You may need nothing yet, and I will tell you that on the first call rather than quote you anyway."),
           ("Skip it","You already own a term policy for the amount the calculator shows","Keep it. Review the beneficiary and move on. Replacing a policy you own is rarely the right move and never the first one."),
           ("Wait","You want permanent coverage as an investment","Read the <a href=\"types-of-life-insurance.html\">types page</a> first. Term almost always comes first, and permanent coverage is for specific reasons, not for growth.")]),
  ],
  faq_kicker="Questions people ask", faq_h2="Life insurance in Greenville, answered plainly.",
  campaign="life-insurance-family-protection", interest="Insurance", step="Life insurance planning",
  insurance=True,
  placeholder="Example: I have 2x salary through Prisma, a $340,000 mortgage and two kids under 10. Is that enough?"),

 dict(slug="financial-advisor-greenville-sc.html",
  title="Financial Advisor in Greenville, SC | Veteran-Owned Fiduciary",
  desc="A Series 65 fiduciary financial advisor in Greenville, South Carolina. Flat-fee planning from $750, published prices, virtual meetings. Investments, insurance, retirement and taxes decided in one order.",
  kicker="Financial planning",
  h1='Financial planning is the <em class="g">decision system</em>.',
  lede="Most people do not have an information problem. They have a sequencing problem. Planning is where the pieces get put in an order that actually works.",
  deep="planning.html", deep_cta="See flat-fee planning",
  alt="wealth.html#tool", alt_cta="Check your retirement number",
  helps=["Cash flow, savings, and debt decisions","Investment and retirement account structure",
         "Insurance and protection gaps","Business-owner or family obligations",
         "Estate, beneficiary, tax, and liquidity coordination points"],
  leave=["A clean decision map","A practical action sequence, ranked","Ongoing review as life changes"],
  sections=[
   dict(kicker="What the title means here", h2="Three different jobs share the words \"financial advisor.\"",
    paras=[
     "Search the phrase in Greenville and you get the branch offices on Main Street, the national directories, and a long list of people with the same title. Many of them are good at what they do. But the title covers three different jobs, and the difference shows up in how you pay. A broker is paid on what you buy. An insurance agent is paid by the carrier on what you are sold. An investment adviser representative is paid by you and owes you a fiduciary duty.",
     "I hold the Series 65 and act as an investment adviser representative, so for advice I am the third kind. I am also licensed for life, accident and health insurance in South Carolina, and when a policy is placed through the firm a carrier commission is paid. I tell you which role I am in and how I am being paid every time, and it is written in the <a href=\"form-crs.html\">Form CRS</a> and <a href=\"disclosures.html\">disclosures</a>, not just here.",
     "The practical test for anyone you are considering is simple. Ask what it costs before the second meeting. If you cannot get a number, you have learned something.",
    ]),
   dict(kicker="How I am paid", h2="Published, in one paragraph.", cream=True,
    paras=[
     "Flat-fee planning is $750, $2,000 or $3,000, one time, agreed in writing before any work begins and completed within six months. Investment management is 1% per year of the assets I manage, with planning included, so nobody pays both. Insurance is never required, and when it is placed through the firm the carrier pays a commission, which is disclosed. There is no hourly rate, no retainer, and no discovery call you have to pass before you are allowed to see a price. The prices are on the <a href=\"planning.html\">planning page</a> and you can buy one tonight.",
    ]),
   dict(kicker="Who I work with in the Upstate", h2="Life stages, not net worth.",
    paras=[
     "The households that get the most out of planning are usually at a turn. A first house in Simpsonville or Greer and the question of how much insurance the mortgage needs. A new baby and a 529 nobody has opened. A job change out of Prisma, Michelin, GE or BMW with a 401(k) decision attached. A Marine or soldier coming off active duty with SGLI ending and a TSP nobody explained. A small business in Mauldin or Easley that is finally profitable and has no plan for the owner's own retirement.",
     "The firm is virtual by design, which is why it works across Greenville, Spartanburg, Anderson, Pickens and the rest of South Carolina without anyone driving to an office. Meetings are by Zoom or phone, documents move securely, and everything you decide is written down so you can explain it to your spouse without me in the room.",
    ],
    cards=[("First house","Mortgage, insurance, cash reserve","The order matters more than the products. Protection first, then the reserve, then the rest."),
           ("New parents","529, term life, beneficiaries","Three decisions that take an afternoon and get put off for years."),
           ("Job change","401(k), benefits, group life","Four options for the old plan and a group life policy that just ended. Decide before the default decides for you."),
           ("Leaving service","TSP, SGLI to VGLI, SC tax treatment","South Carolina exempts military retired pay from state income tax. That changes the math on where to retire and what to draw first."),
           ("Business owner","Entity, retirement plan, buy-sell","Profitable is not the same as planned. The owner is usually the last person on the payroll with a retirement account."),
           ("Pre-retirement","Income, Social Security, withdrawals","The five years on either side of the date are where small mistakes get expensive. See the <a href=\"retirement-planning-greenville-sc.html\">retirement page</a>.")]),
   dict(kicker="The order of operations", h2="What gets decided first, and why.", cream=True,
    paras=[
     "Protection comes first because a portfolio does not survive an uninsured disaster. Then the cash reserve, sized to your actual job risk rather than a rule of thumb. Then high-cost debt, ranked by real rates against what the same dollars could earn. Then the tax-advantaged accounts in the order that fits your bracket: employer match, Roth or traditional, HSA if you have one. Then taxable investing. Then the estate basics, which for most households means beneficiaries, titling, a will and powers of attorney, not a trust.",
     "That sequence is the whole product. It is why a $750 plan can change more than a year of reading. The information was never secret. Someone finally put it in an order and attached your numbers to it.",
    ]),
   dict(kicker="The first call", h2="Thirty minutes, no pitch, and you leave with a decision.",
    paras=[
     "Bring your rough numbers: income, what you owe, what you have saved, what insurance you carry through work, and the one or two decisions you are stuck on. No statements. I will tell you which plan fits, or that you do not need one yet, and I give that second answer often. If you would rather skip the call, <a href=\"planning.html\">buy the plan</a> and the discovery meeting is part of the work.",
    ]),
  ],
  faq_kicker="Questions people ask", faq_h2="Hiring a financial advisor in Greenville, answered plainly.",
  campaign="financial-advisor-greenville-sc", interest="Not sure", step="Focused intro call",
  insurance=False,
  placeholder="Example: we just bought in Greer, have a baby on the way, and have never talked to anyone about any of this."),

 dict(slug="retirement-planning-greenville-sc.html",
  title="Retirement Planning in Greenville, SC | Rae &amp; Co Capital",
  desc="Retirement income planning for Greenville and Upstate South Carolina. Withdrawal order, Social Security timing, SC tax treatment of retirement income and survivor income, decided before the paycheck stops.",
  kicker="Retirement planning",
  h1='Retirement income before <em class="g">retirement pressure</em>.',
  lede="The switch from saving to spending is where small mistakes get expensive, and most of them are locked in before anyone notices.",
  deep="wealth.html#tool", deep_cta="Check your retirement number",
  alt="planning.html", alt_cta="See flat-fee planning",
  helps=["Income sources and expected spending","Withdrawal sequencing and reserve strategy",
         "Portfolio risk during the retirement transition","Survivor needs and legacy considerations",
         "Flexibility for health, family, and market changes"],
  leave=["A retirement income map","A liquidity and reserve framework",
         "A decision list before the paycheck changes"],
  sections=[
   dict(kicker="Retiring in South Carolina", h2="Why people retire to the Upstate, and what it changes in the plan.",
    paras=[
     "South Carolina does not tax Social Security benefits. It fully exempts military retirement pay from state income tax. Pension, 401(k) and IRA withdrawals are taxable, but there is a retirement income deduction and a further deduction once you turn 65, and owner-occupied property tax here is low by national standards. Those are the reasons the Upstate keeps showing up on retirement lists, and they are also the reason the withdrawal order here is different from the one a national calculator assumes.",
     "None of that is individualized tax advice. Your tax preparer can tell you exactly what applies to your return. What the plan does is put the pieces in an order that uses them: which account to draw first, when to convert, when to claim, and how much of each year's income should come from where.",
    ]),
   dict(kicker="Five decisions that get locked in early", h2="Most of the damage is done before the first withdrawal.", cream=True,
    cards=[("Social Security","62, full retirement age, or 70","Claiming early gives a smaller check for longer. Waiting grows it each year until 70. Health, work, a spouse's record and what else you can draw on all move the answer."),
           ("Withdrawal order","Taxable, traditional, Roth","Which account pays for each year is a tax decision that compounds for decades. Getting it right is worth more than most fund choices."),
           ("The reserve","How many years in cash","Enough that a bad first few years in the market never forces a sale at the bottom. Too much and it quietly costs you. The number is personal."),
           ("Survivor income","What happens to the second person","Pension survivor options, Social Security survivor rules and life insurance all interact. Decide it once, on purpose, before the election is irrevocable."),
           ("Risk in the first five years","Sequence risk is the one that matters","The same average return in a different order produces a different retirement. The plan sizes risk to the date, not to a questionnaire."),
           ("Health and long-term care","The cost nobody budgets","Medicare timing, supplement choices and whether to insure long-term care or self-fund it belong in the plan, not in a panic at 72.")]),
   dict(kicker="Leaving a big Upstate employer", h2="The 401(k) decision, and the conflict in it.",
    paras=[
     "A lot of Greenville retirements start with a separation from Prisma Health, Michelin, GE, Bon Secours, BMW, Fluor or the school district, and a 401(k) or 403(b) that suddenly needs a decision. You generally have four options: leave it where it is, move it into a new employer's plan, roll it to an IRA, or cash it out. Each has different costs, investment menus, creditor protection and tax consequences, and for some people the old plan is the best deal available.",
     "Here is the conflict, stated plainly. If you roll it into an account I manage, I am paid 1% a year. That is why the leave-it-where-it-is math comes first, in writing, before anything moves. If your plan offers a pension or a lump sum, that election is usually irrevocable and deserves the same treatment.",
    ]),
   dict(kicker="Military retirement", h2="Retired pay, TSP, SBP, and the SGLI clock.", cream=True,
    paras=[
     "I am a Marine Corps veteran and the firm started with military families. South Carolina's full exemption of military retired pay changes the picture for anyone weighing where to live after service. The TSP is one of the lowest-cost retirement accounts in the country and there is often no reason to move it. The Survivor Benefit Plan election and what replaces SGLI after the 120-day window are the two decisions that most often get made by default, and both are hard to undo. They belong in the plan before the retirement ceremony, not after.",
    ]),
   dict(kicker="Start with the number", h2="A minute with the tool, then a real plan.",
    paras=[
     "The <a href=\"wealth.html#tool\">retirement income check</a> on the wealth page asks for your age, what you have saved, what you add each month and the growth rate you are willing to assume, and shows whether that adds up to the income you want at the age you pick. The growth rate is yours to set because nobody can promise one. When the answer is close, or when the real question is the order of withdrawals rather than the total, that is when a written plan earns its fee. Planning is a flat fee of $750, $2,000 or $3,000 on its own, and it is included if I manage the money.",
    ]),
  ],
  faq_kicker="Questions people ask", faq_h2="Retirement planning in Greenville, answered plainly.",
  campaign="retirement-planning-greenville-sc", interest="Investments", step="Portfolio or retirement review",
  insurance=False,
  placeholder="Example: I am 58, leaving Michelin in two years with a 401(k) and a pension option, and I do not know which to take."),

 dict(slug="investment-management-greenville-sc.html",
  title="Investment Management in Greenville, SC | Rae &amp; Co Capital",
  desc="Fiduciary investment management in Greenville, South Carolina. 1% per year, planning included, assets held at Charles Schwab in your name. Allocation, taxes and withdrawals run as one decision.",
  kicker="Investment management",
  h1='Investment management that <em class="g">answers to the plan</em>.',
  lede="Anyone can buy index funds. The work is sequencing withdrawals, keeping taxes from eating the gains, and not selling at the bottom because a headline scared you.",
  deep="wealth.html", deep_cta="See how management works",
  alt="wealth.html#tool", alt_cta="Check your retirement number",
  helps=["Current allocation and account structure","Risk exposure and concentration",
         "Liquidity needs and time horizon","Tax-sensitive investment decisions",
         "Rebalancing and ongoing review cadence"],
  leave=["A clearer investment policy","An implementation plan",
         "A review rhythm tied to life changes, not market noise"],
  sections=[
   dict(kicker="What 1% actually buys", h2="One fee, the whole job.",
    paras=[
     "Management is 1% per year of the assets I manage, billed quarterly, with a $750 annual minimum, and financial planning is included. On $300,000 that is $3,000 a year. For that you get the allocation, rebalancing on a schedule, tax-aware placement across taxable and retirement accounts, the withdrawal order once you are drawing, and one person who built the plan answering the phone. Fund expense ratios and any custodian charges are separate and shown to you. There are no commissions on managed accounts.",
     "If the balance is small enough that the $750 minimum makes the fee a poor deal, I will tell you to buy a <a href=\"planning.html\">flat-fee plan</a> and invest it yourself. That is a worse outcome for me and the right one for you, and it is in the Form ADV.",
    ]),
   dict(kicker="Where the money sits", h2="Charles Schwab, in your name, visible any time.", cream=True,
    paras=[
     "Client assets are held at Charles Schwab in accounts titled to you. I never take custody. You log in to Schwab Alliance and see every holding and every transaction, Schwab sends its own statements, and if you ever decide to leave, the account goes with you because it was always yours. That arrangement is the minimum you should accept from anyone managing your money.",
    ]),
   dict(kicker="How a portfolio gets built", h2="By the plan, not by the news.",
    paras=[
     "The allocation comes from the plan: when you need the money, how much of it, and how much of a bad year you can sit through without changing course. It is built from low-cost, diversified funds, written into an investment policy you keep, and rebalanced on a schedule rather than on a feeling. There is no stock picking and no promise of beating anything. Investing involves risk, including loss of principal, and anyone promising otherwise is selling something.",
     "The part that usually matters more than the funds is the behavior around them. I went and got a master's in psychology because I kept watching capable people know the right answer and not act on it, and most of the lost money I have seen in fifteen years was lost by selling after a drop or buying after a run. A large part of the fee is paying for someone whose job is to keep that from happening to you.",
    ]),
   dict(kicker="Upstate balance sheets", h2="The situations that come up most around Greenville.", cream=True,
    cards=[("Concentration","Too much in one company","If a meaningful share of your net worth is your employer's stock, or any single company, that is the first conversation, and unwinding it is a tax question as much as a risk one."),
           ("Old plans","The 401(k) you left at a previous employer","Four options, each with different costs and protections. Rolling it to me pays me 1%, so you see the leave-it math first."),
           ("Real estate heavy","A rental or two and not much else liquid","Common in the Upstate. The plan works out what the portfolio needs to do that the property cannot, and how much cash that requires."),
           ("Inherited accounts","An IRA with a ten-year clock","Inherited IRAs have withdrawal rules that can push income into high brackets if ignored. Sequencing them is planning, and it is included."),
           ("Taxable and retirement side by side","Which fund goes where","Bonds, stocks and funds that throw off income belong in different account types. Placement is free money that most portfolios leave on the table."),
           ("Drawing down","Turning a balance into a paycheck","The withdrawal order, the reserve and the Social Security date are one decision. See the <a href=\"retirement-planning-greenville-sc.html\">retirement page</a>.")]),
   dict(kicker="When not to hire me", h2="Three honest reasons to keep doing it yourself.",
    paras=[
     "If you already run a disciplined, low-cost portfolio and do not touch it when the market drops, you probably need a plan, not a manager. If the balance is small, the minimum fee makes me a poor deal. If what you want is someone to trade, I am the wrong person. In all three cases the <a href=\"planning.html\">flat-fee plan</a> is the better buy, and I would rather say so now than charge you for a year and have you work it out.",
    ]),
  ],
  faq_kicker="Questions people ask", faq_h2="Investment management in Greenville, answered plainly.",
  campaign="investment-management-greenville-sc", interest="Investments", step="Portfolio or retirement review",
  insurance=False,
  placeholder="Example: about $400k across a 401k and a rollover IRA, a lot of it in one stock, retiring in roughly eight years."),
]

def _cards(cards):
    return ('\n    <div class="grid g3 stagger" data-rv style="margin-top:28px">' +
            "".join(f'\n      <div class="card"><p class="tag">{t}</p><h3>{h}</h3><p>{p}</p></div>' for t,h,p in cards) +
            '\n    </div>')

def geo_section(s):
    paras = "".join(f'\n      <p>{p}</p>' for p in s.get("paras", []))
    prose = f'\n    <div class="prose" data-rv>{paras}\n    </div>' if paras else ""
    cards = _cards(s["cards"]) if s.get("cards") else ""
    return f"""
<section class="section{' cream' if s.get('cream') else ''}" style="padding-top:clamp(48px,5.5vw,76px);padding-bottom:clamp(48px,5.5vw,76px)">
  <div class="wrap">
    <p class="kicker" data-rv>{s['kicker']}</p>
    <h2 class="sub" data-rv style="max-width:30ch">{s['h2']}</h2>{prose}{cards}
  </div>
</section>"""

def geo_page(g):
    slug = g["slug"]
    cross = "".join(f'<a class="xlink" href="{h}">{t} <span class="arr">&rarr;</span></a>'
                    for h, t in CROSS if h != slug)
    return f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <p class="kicker" data-rv>{g['kicker']} &middot; Greenville, South Carolina</p>
    <h1 data-rv>{g['h1']}</h1>
    <p class="lede" data-rv>{g['lede']}</p>
    <div class="acts" data-rv>
      <a class="btn btn-ink" data-magnetic href="{g['deep']}">{g['deep_cta']} <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="{g['alt']}">{g['alt_cta']}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 class="sub" data-rv style="margin-bottom:26px">What gets looked at, and what you leave with.</h2>
    <div class="grid g2 stagger" data-rv>
      <div class="card"><p class="tag">What gets reviewed</p><h3>The inputs</h3>
        <ul class="ticks">{"".join(f"<li>{x}</li>" for x in g['helps'])}</ul></div>
      <div class="card"><p class="tag">What you walk away with</p><h3>The output</h3>
        <ul class="ticks">{"".join(f"<li>{x}</li>" for x in g['leave'])}</ul></div>
    </div>
    <p class="lede" data-rv style="margin-top:34px;max-width:74ch">Portfolio, retirement income, insurance, cash flow, taxes and family obligations get reviewed together rather than handled as disconnected projects. That coordination is the whole reason one person does all of it.</p>
  </div>
</section>
{"".join(geo_section(s) for s in g['sections'])}
<section class="section" style="padding-top:0;padding-bottom:0">
  <div class="wrap"><div class="xrow" data-rv style="margin-top:0">{cross}</div></div>
</section>
{faq_block(slug, g['faq_kicker'], g['faq_h2'])}
{form_section("Request follow-up", "Bring this into the conversation.",
  "Tell me what is on your mind and I will tell you whether I can help. Please leave out account numbers, policy numbers and Social Security numbers.",
  lead_form(g['campaign'], slug, "consultation-request", "Request follow-up",
            "Replies come from me, usually the same day.", g['interest'], g['step'],
            cta="Request follow-up", insurance=g['insurance'], placeholder=g['placeholder']), cream=False)}"""


WEALTH = WEALTH + faq_block("wealth.html", "Fees, custody, the tool", "Plain answers on the money part.") + form_section(
  "Start a conversation", "Want a second read on the portfolio?",
  "Tell me what you hold and what it is for. If a flat-fee plan serves you better than "
  "management, I will say so before you ask.",
  lead_form("wealth-page","wealth.html","consultation-request",
            "Request a portfolio review","Replies come from me, usually the same day.",
            "Investments","Portfolio or retirement review", cta="Request a review",
            placeholder="Example: about $400k across a 401k and a rollover IRA, "
                        "retiring in roughly eight years."), cream=True)


# ------------------------------------------------------------ START-PLAN BRIDGE
# Tyler, on tier buttons deep-linking to bare square.link URLs: "it almost
# looks scammy to me so it will for sure to anyone else", and "we have to know
# about them at least bare bones". This page is the branded step between the
# tier card and Square: it captures name/email/phone as a real lead through the
# same Pi funnel as every other form (Telegram pings even if they never pay),
# then forwards to Square checkout.
#
# The Pi's safe_return whitelists rcowealth.com only, so the forward cannot
# ride retURL. Instead the form posts into a hidden iframe and the page
# navigates to Square 1.2s later. JS off = normal submit: lead still captured,
# visitor lands on thank-you and can be called. No server change required.
BRIDGE = """
<section class="section" style="padding-bottom:0">
  <div class="wrap" style="max-width:880px">
    <p class="kicker" data-rv>Start your plan</p>
    <h1 data-rv style="font-size:clamp(40px,5vw,64px)">Start <em class="g" id="bTierName">Household</em>.</h1>
    <p class="lede" data-rv>Two quick things, then Square&rsquo;s secure checkout. The charge shows as <b>Rae &amp; Co Capital, LLC</b> on your statement.</p>
  </div>
</section>
<section class="section">
  <div class="wrap split c" style="max-width:1020px">
    <div>
      <div class="card" data-rv style="margin-bottom:16px">
        <p class="tag">Your plan</p>
        <h2 class="sub" id="bSummaryName">Household</h2>
        <p style="margin:2px 0 10px;font-family:var(--serif);font-size:34px;color:var(--ink)" id="bPrice">$2,000</p>
        <p id="bBlurb">For a full picture, usually a couple with a few moving parts.</p>
      </div>
      <div class="card" data-rv>
        <h2 class="tag" style="font:800 10.5px/1 var(--sans);letter-spacing:.15em;text-transform:uppercase;color:var(--gold-ink);margin:0 0 12px">What happens next</h2>
        <ul class="ticks" style="margin-top:6px">
          <li>Pay on Square&rsquo;s secure checkout. You get a receipt immediately.</li>
          <li>Sign the written planning agreement, which I email you the same day.</li>
          <li>Meet for discovery. It is part of the work, not a sales call you have to pass first.</li>
        </ul>
        <p style="margin:14px 0 0;font:400 12.5px/1.6 var(--sans);color:var(--muted)">One-time engagement completed within six months, not a subscription. If we stop early, any unearned prepaid portion is returned. Questions first? Text 864-558-8440.</p>
      </div>
    </div>
    <div>
    <form class="lform" data-rv id="bridgeForm" action="https://pi-nas.tail34488a.ts.net/" method="POST" target="paysink"
          data-campaign="planning-checkout" data-asset="start-plan.html" data-form-purpose="planning-purchase">
{FORM_HIDDEN}
      <input type="hidden" name="00Nfn0000089jXZ" value="Not sure yet">
      <input type="hidden" name="preferred_next_step_display" value="Buying a planning package">
      <input type="hidden" name="description" id="bDesc" value="Started checkout: Household ($2,000)">
      <h2 class="sub">Who is this plan for?</h2>
      <p class="lsub">So the agreement and the plan carry the right name from the start.</p>
      <div class="fgrid">
        <div class="fld2"><label for="bp_first">First name</label><input id="bp_first" name="first_name" autocomplete="given-name" required></div>
        <div class="fld2"><label for="bp_last">Last name</label><input id="bp_last" name="last_name" autocomplete="family-name" required></div>
        <div class="fld2"><label for="bp_email">Email</label><input id="bp_email" type="email" name="email" autocomplete="email" required></div>
        <div class="fld2"><label for="bp_phone">Phone</label><input id="bp_phone" type="tel" name="phone" autocomplete="tel" required></div>
{FORM_CHECKS}
      </div>
      <button class="btn btn-gold" type="submit" style="width:100%;margin-top:18px">Continue to secure payment <span class="arr">&rarr;</span></button>
      <p class="lfine" id="bWait" style="display:none">Opening Square checkout&hellip; <a id="bFallback" href="#">continue manually</a> if nothing happens.</p>
      <p class="lfine">{FORM_FINE}</p>
    </form>
    <iframe name="paysink" title="hidden" aria-hidden="true" tabindex="-1" style="position:absolute;left:-9999px;width:1px;height:1px"></iframe>
    </div>
  </div>
</section>
<script>
(function(){
  var TIERS={
    foundations:{name:"Foundations",price:"$750",blurb:"For a clear starting plan around one or two priorities.",pay:"https://square.link/u/VJZxUhJ9"},
    household:{name:"Household",price:"$2,000",blurb:"For a full picture, usually a couple with a few moving parts.",pay:"https://square.link/u/23AsoUVF"},
    implementation:{name:"Household + Implementation",price:"$3,000",blurb:"For help executing, not just a document.",pay:"https://square.link/u/oUQEsSoQ"}
  };
  var key=(new URLSearchParams(location.search).get("tier")||"household").toLowerCase();
  var t=TIERS[key]||TIERS.household;
  document.getElementById("bTierName").textContent=t.name;
  document.getElementById("bSummaryName").textContent=t.name;
  document.getElementById("bPrice").textContent=t.price+" one time";
  document.getElementById("bBlurb").textContent=t.blurb;
  document.getElementById("bDesc").value="Started checkout: "+t.name+" ("+t.price+")";
  var f=document.getElementById("bridgeForm");
  f.setAttribute("data-campaign","planning-checkout-"+key);
  document.getElementById("bFallback").href=t.pay;
  f.addEventListener("submit",function(){
    document.getElementById("bWait").style.display="block";
    setTimeout(function(){window.location.href=t.pay;},1200);
  });
})();
</script>
"""
BRIDGE = (BRIDGE.replace("{FORM_HIDDEN}", FORM_HIDDEN)
                .replace("{FORM_CHECKS}", FORM_CHECKS)
                .replace("{FORM_FINE}", FORM_FINE))


# --------------------------------------------------------------- LEAD MAGNETS
# The worksheet and checklist funnels, ported into the shell 2026-08-10 so the
# last four old-shell pages could retire along with styles.css/site.js. Same
# URLs, same campaigns, same gated-download flow: email-first form (no phone -
# magnet forms convert on the shortest field set), retURL to the magnet's own
# thank-you page where the PDF link lives.
def magnet_form(retpage, asset, purpose, cta):
    return f"""<form class="lform" data-rv id="magnetForm" action="https://pi-nas.tail34488a.ts.net/" method="POST"
          data-campaign="{purpose}" data-asset="{asset}" data-form-purpose="{purpose}">
      <input type="hidden" name="oid" value="00Dfn00000AW6kiEAD">
      <input type="hidden" name="retURL" value="{ORIGIN}/{retpage}">
      <input type="hidden" name="lead_source" value="Web">
      <input type="hidden" name="company" value="Individual / Household">
      <input type="hidden" name="00Nfn0000089jHR" value="Website">
      <input type="hidden" name="00Nfn0000089jXZ" value="Insurance">
      <input type="hidden" name="00NbV000002pcrh" value="Yes">
      <input type="hidden" name="preferred_next_step_display" value="Lead magnet download">
      <label class="hp2" aria-hidden="true">Website<input name="website_url" autocomplete="off" tabindex="-1" data-honeypot="true"></label>
      <h2 class="sub">{cta}</h2>
      <p class="lsub">Enter your name and email and the download opens on the next page. No spam, no pressure.</p>
      <div class="fgrid">
        <div class="fld2"><label for="mg_first">First name</label><input id="mg_first" name="first_name" autocomplete="given-name" required></div>
        <div class="fld2"><label for="mg_last">Last name</label><input id="mg_last" name="last_name" autocomplete="family-name" required></div>
        <div class="fld2 full"><label for="mg_email">Email</label><input id="mg_email" type="email" name="email" autocomplete="email" required></div>
        <div class="checks2">
          <label class="ckline"><input type="checkbox" name="00NbV000003Urbb" value="1">Yes, I would like to receive Rae &amp; Co Capital market notes and educational updates.</label>
        </div>
      </div>
      <button class="btn btn-gold" type="submit" style="width:100%;margin-top:18px">{cta} <span class="arr">&rarr;</span></button>
      <p class="lfine">In a hurry? Skip ahead: <a href="{B9}&amp;utm_content={asset.split(".")[0]}_skip" target="_blank" rel="noopener">See my rates &rarr;</a></p>
      <p class="lfine">Submitting this form does not create an advisory relationship. The download is educational only and its results are estimates, not individualized advice.</p>
    </form>"""

def magnet_landing(kicker, h1, lede, chips, steps_kicker, steps_h2, steps, retpage, asset, purpose, cta):
    chiprow = "".join(f'<span class="xlink" style="cursor:default">{c}</span>' for c in chips)
    stepcards = "".join(f'<div class="card"><p class="tag">{t}</p><h3>{h}</h3><p>{b}</p></div>'
                        for t, h, b in steps)
    return f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap split c">
    <div>
      <p class="kicker" data-rv>{kicker}</p>
      <h1 data-rv style="font-size:clamp(40px,5vw,66px)">{h1}</h1>
      <p class="lede" data-rv>{lede}</p>
      <div class="xrow" data-rv style="border-top:0;padding-top:0;margin-top:6px">{chiprow}</div>
    </div>
    {magnet_form(retpage, asset, purpose, cta)}
  </div>
</section>
<section class="section cream">
  <div class="wrap">
    <p class="kicker" data-rv>{steps_kicker}</p>
    <h2 data-rv style="max-width:24ch">{steps_h2}</h2>
    <div class="grid g3 stagger" data-rv style="margin-top:32px">{stepcards}</div>
    <div class="acts" data-rv style="margin-top:32px">
      <a class="btn btn-ink" href="life-insurance-calculator.html">Run the numbers online instead <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="{B9}&amp;utm_content={asset.split(".")[0]}_bottom" target="_blank" rel="noopener">See my rates</a>
    </div>
  </div>
</section>
"""

def magnet_thanks(h1, lede, pdf, label, camp):
    return f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap" style="max-width:820px">
    <p class="kicker" data-rv>You&rsquo;re all set</p>
    <h1 data-rv style="font-size:clamp(40px,5vw,64px)">{h1}</h1>
    <p class="lede" data-rv>{lede}</p>
    <div class="acts" data-rv>
      <a class="btn btn-gold" href="/{pdf}" target="_blank" rel="noopener">{label} <span class="arr">&rarr;</span></a>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap" style="max-width:820px">
    <h2 class="sub" data-rv style="margin-bottom:10px">When you have your number, see what coverage actually costs.</h2>
    <p class="lede" data-rv>Real quotes from major carriers, yourself, right now. No phone call required. If you would rather have a second set of eyes first, that is here too.</p>
    <div class="acts" data-rv>
      <a class="btn btn-ink" href="{B9}&amp;utm_content={camp}_thankyou" target="_blank" rel="noopener">See my rates <span class="arr">&rarr;</span></a>
      <a class="btn-line" href="life-insurance-calculator.html?utm_source=site&amp;utm_medium=magnet&amp;utm_campaign={camp}&amp;utm_content=thankyou_calculator">Run my numbers</a>
      <a class="btn-line" href="https://scheduler.zoom.us/raecocapital/life-insurance-review?utm_source=site&amp;utm_medium=magnet&amp;utm_campaign={camp}&amp;utm_content=thankyou_schedule" target="_blank" rel="noopener">Schedule a free review</a>
    </div>
  </div>
</section>
"""

WORKSHEET = magnet_landing(
  "Free worksheet",
  "Find your household&rsquo;s <em class=\"g\">real</em> life insurance number.",
  "Most families guess at coverage, or take whatever work offers. This one-page worksheet walks the same four questions an adviser would ask, so the number you land on is yours. It takes about ten minutes.",
  ["Debts and mortgage","Income replacement","The kids","What you already have"],
  "Why a worksheet",
  "Because &ldquo;2x salary from work&rdquo; was never your number.",
  [("Step 1","Add up the need","Debts, income replacement years, and goals for the kids, in plain numbers you already know."),
   ("Step 2","Subtract what you have","Savings, existing policies, and the coverage through work, counted honestly."),
   ("Step 3","See your gap","One number. If you want a second set of eyes on it, a free 20-minute review is available. No pitch.")],
  "thank-you-worksheet.html","life-insurance-worksheet.html","lead-magnet-life-worksheet","Send me the worksheet")

CHECKLIST_MAGNET = magnet_landing(
  "Free checklist",
  "New house, new baby, new job. Is the family <em class=\"g\">actually protected</em>?",
  "Every big life event quietly adds financial risk before it adds wealth. This one-page checklist covers the ten things young families should have handled before worrying about picking investments. Protection comes before portfolios.",
  ["Coverage on both parents","Beneficiaries done right","The emergency cushion","A veteran-family section"],
  "What&rsquo;s inside",
  "Ten checkboxes. Five minutes to read. A real picture of where you stand.",
  [("Protect","The people first","Both parents covered, employer coverage understood, disability income considered."),
   ("Paperwork","Then the details","Beneficiaries, wills, guardianship, powers of attorney. The unglamorous things that matter most."),
   ("Build","Then keep building","Emergency cushion, debt plan, retirement contributions still running, nothing forgotten at old jobs.")],
  "thank-you-checklist.html","family-protection-checklist.html","lead-magnet-family-checklist","Send me the checklist")

TY_WORKSHEET = magnet_thanks(
  "Here&rsquo;s your <em class=\"g\">worksheet</em>.",
  "Ten minutes, four questions, one honest number. Grab last month&rsquo;s budget and your latest statements before you start.",
  "assets/Rae-Co-Life-Insurance-Needs-Worksheet.pdf","Download the worksheet (PDF)","life-worksheet")

TY_CHECKLIST = magnet_thanks(
  "Here&rsquo;s your <em class=\"g\">checklist</em>.",
  "Ten boxes, five minutes. Check what is done, circle what is not, and you know exactly what to fix next.",
  "assets/Rae-Co-Young-Family-Protection-Checklist.pdf","Download the checklist (PDF)","family-checklist")

PAGES = [
 ("start-plan.html","Start Your Plan | Rae &amp; Co Capital","Confirm your details and continue to secure checkout for your flat-fee financial plan.",BRIDGE),
 ("life-insurance-worksheet.html","Free Life Insurance Needs Worksheet | Rae &amp; Co Capital","A one-page worksheet that walks the four questions an adviser would ask, so the coverage number you land on is yours.",WORKSHEET),
 ("family-protection-checklist.html","Free Young Family Protection Checklist | Rae &amp; Co Capital","Ten things young families should have handled before picking investments. Protection comes before portfolios.",CHECKLIST_MAGNET),
 ("thank-you-worksheet.html","Your Worksheet Is Ready | Rae &amp; Co Capital","Download the life insurance needs worksheet.",TY_WORKSHEET),
 ("thank-you-checklist.html","Your Checklist Is Ready | Rae &amp; Co Capital","Download the young family protection checklist.",TY_CHECKLIST),
 ("index.html","Rae &amp; Co Capital | Veteran-Owned Virtual Wealth Management","Veteran-owned, 100% virtual wealth management and protection planning in Greenville, South Carolina. Quote, price and start it yourself.",HOME),
 ("wealth.html","Wealth Management | Rae &amp; Co Capital","Portfolio management and retirement income at 1% per year of assets under management with a $750 annual minimum. Assets custodied at Charles Schwab.",WEALTH),
 ("protection.html","Protection Planning | Rae &amp; Co Capital","Term, disability, permanent, long-term care and final expense explained plainly. Quote and apply across 40+ carriers.",PROTECTION),
 ("planning.html","Financial Planning Fees | Rae &amp; Co Capital","Flat-fee financial planning from $750. Published prices, real deliverables, buy it online.",PLANNING),
 ("advisor.html","Tyler Krause, Your Advisor | Rae &amp; Co Capital","Marine Corps veteran, Series 65 fiduciary, CCFPA. One person who answers the phone.",ADVISOR),
 ("contact.html","Contact | Rae &amp; Co Capital","One call, no pitch. Reach Tyler Krause at Rae &amp; Co Capital.",CONTACT),
 ("disclosures.html","Disclosures | Rae &amp; Co Capital","Registration, risk, fees and conflicts, stated plainly.",DISCLOSURES),
 ("form-crs.html","Form CRS Summary | Rae &amp; Co Capital","Relationship summary, services, fees and conflicts.",FORMCRS),
 ("privacy.html","Privacy Policy | Rae &amp; Co Capital","What we collect, how it is used, and what we never do with it.",PRIVACY),
 ("client-login.html","Client Access | Rae &amp; Co Capital","Go to your custodian or carrier portal directly.",CLIENTLOGIN),
 ("life-insurance-calculator.html","Life Insurance Calculator | Rae &amp; Co Capital","Drag the sliders and see your coverage gap. No name, no email, nothing stored.",CALCULATOR),
 ("types-of-life-insurance.html","Types of Life Insurance, Explained Plainly | Rae &amp; Co Capital","Term, whole, universal, IUL, disability income, long-term care, term variants and final expense. What each solves, what it costs you, and when it is the wrong tool.",types_page()),
 ("life-insurance-quote.html","Get a Life Insurance Quote Online | Rae &amp; Co Capital","Compare real life insurance quotes across 40+ carriers and apply online in the same session. No agent call required to see your rates.",QUOTE),
 ("life-insurance-review-checklist.html","Life Insurance Review Checklist | Rae &amp; Co Capital","Six things to check before you change or replace a life insurance policy. Obligations, ownership, beneficiaries and liquidity, not just premium.",CHECKLIST),
 ("services.html","Services | Rae &amp; Co Capital","Investment management, retirement planning, financial planning and life insurance, coordinated in one virtual advisory relationship.",SERVICES),
 ("thank-you.html","Thank You | Rae &amp; Co Capital","Your message reached Rae &amp; Co Capital.",THANKYOU),
 ("life-insurance-protection-review.html","Life Insurance Protection Review | Rae &amp; Co Capital","Have existing life insurance and coverage gaps reviewed against income, debt, dependents and business exposure. Greenville, South Carolina.",REVIEW),
]

for g in GEO:
    PAGES.append((g["slug"],g["title"],g["desc"],geo_page(g)))

for i,(slug,title,desc,body) in enumerate(PAGES):
    if slug == "life-insurance-calculator.html":
        PAGES[i] = (slug, title, desc, body + form_section(
          "You have the number", "Want it turned into real pricing?",
          "Send the figure you just worked out and I will come back with what it actually "
          "costs across the carriers that can write your case.",
          lead_form("needs-calculator","life-insurance-calculator.html","needs-calculator",
                    "Price this amount","Replies come from me, usually the same day.",
                    "Insurance","Life insurance planning", cta="Send my number",
                    insurance=True,
                    placeholder="Example: the calculator said about $600,000 and I am 38, "
                                "non-smoker, in good health."), cream=True))

for slug,title,desc,body in PAGES:
    (OUT/slug).write_text(shell(slug,title,desc,body,extra_ld=page_ld(slug)),encoding="utf-8")
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
    SKIP = {"thank-you.html", "start-plan.html", "thank-you-worksheet.html", "thank-you-checklist.html"}
    allslugs = [s for s,_,_,_ in PAGES if s not in SKIP]
    urls = "\n".join(
      f"  <url><loc>{ORIGIN}/{'' if s=='index.html' else s}</loc>"
      f"<priority>{PRIORITY.get(s,'0.6')}</priority></url>"
      for s in allslugs)
    (OUT/"sitemap.xml").write_text(
      '<?xml version="1.0" encoding="UTF-8"?>\n'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + urls + "\n</urlset>\n")
    print("wrote sitemap.xml (%d urls)" % (len(PAGES)-len(SKIP)))
else:
    print("STAGING=True: noindex on, sitemap NOT regenerated")
