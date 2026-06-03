(() => {
  const storageKey = 'raeCoCampaignAttribution';
  const params = new URLSearchParams(window.location.search);
  const keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'utm_id', 'gclid', 'fbclid', 'msclkid'];

  function safeJsonParse(value) {
    try { return JSON.parse(value || '{}') || {}; } catch { return {}; }
  }

  function getStoredAttribution() {
    try { return safeJsonParse(window.sessionStorage?.getItem(storageKey)); } catch { return {}; }
  }

  const stored = getStoredAttribution();
  const captured = { ...stored };
  for (const key of keys) {
    const value = params.get(key);
    if (value) captured[key] = value.slice(0, 180);
  }

  const referrer = document.referrer || captured.referrer || '';
  if (referrer) captured.referrer = String(referrer).slice(0, 240);
  if (!captured.first_landing_page) captured.first_landing_page = window.location.pathname;
  captured.last_seen_page = window.location.pathname;

  try { window.sessionStorage?.setItem(storageKey, JSON.stringify(captured)); } catch {}

  function sourceDetail() {
    const source = String(captured.utm_source || '').toLowerCase();
    const medium = String(captured.utm_medium || '').toLowerCase();
    const ref = String(captured.referrer || '').toLowerCase();
    if (captured.gclid || source.includes('google') || ref.includes('google.')) return 'Google Search';
    if (captured.msclkid || source.includes('bing') || ref.includes('bing.')) return 'Bing Search';
    if (source.includes('instagram') || source === 'ig' || ref.includes('instagram.com')) return 'Instagram';
    if (captured.fbclid || source.includes('facebook') || source === 'fb' || ref.includes('facebook.com') || ref.includes('l.facebook.com')) return 'Facebook';
    if (source.includes('linkedin') || ref.includes('linkedin.com')) return 'LinkedIn';
    if (source.includes('youtube') || ref.includes('youtube.com') || ref.includes('youtu.be')) return 'YouTube';
    if (source.includes('backnine')) return 'BackNine';
    if (medium.includes('referral')) return 'Referral';
    return 'Website';
  }

  function leadSourceForDetail(detail) {
    const value = String(detail || '');
    if (value.startsWith('Google')) return 'Google';
    if (value === 'Instagram') return 'Instagram';
    if (value === 'Facebook') return 'Facebook';
    if (value === 'Bing Search') return 'Web';
    if (['LinkedIn', 'YouTube'].includes(value)) return 'Web';
    return 'Web';
  }

  function ensureHidden(form, name, value) {
    let input = form.querySelector(`input[name="${name}"]`);
    if (!input) {
      input = document.createElement('input');
      input.type = 'hidden';
      input.name = name;
      form.appendChild(input);
    }
    input.value = value;
    return input;
  }

  function ensureHoneypot(form) {
    if (form.querySelector('input[name="website_url"], input[data-honeypot="true"]')) return;
    const label = document.createElement('label');
    label.className = 'hp-field';
    label.setAttribute('aria-hidden', 'true');
    label.setAttribute('tabindex', '-1');
    label.style.cssText = 'position:absolute!important;left:-10000px!important;top:auto!important;width:1px!important;height:1px!important;overflow:hidden!important;opacity:0!important;pointer-events:none!important;z-index:-1!important;';
    label.innerHTML = 'Website <input name="website_url" autocomplete="off" tabindex="-1" data-honeypot="true">';
    form.insertBefore(label, form.firstElementChild || null);
  }

  function buildTrackingText(form, detail) {
    const data = {
      campaign: form.dataset.campaign || captured.utm_campaign || 'website',
      asset: form.dataset.asset || captured.utm_content || 'unknown',
      form_purpose: form.dataset.formPurpose || '',
      lead_source_detail: detail,
      page: window.location.pathname,
      first_landing_page: captured.first_landing_page,
      ...captured,
    };
    return '\n\n--- Marketing attribution ---\n' + Object.entries(data)
      .filter(([, value]) => value)
      .map(([key, value]) => `${key}: ${String(value).replace(/\s+/g, ' ').trim()}`)
      .join('\n');
  }

  function compactBackNineMetadata(content) {
    const meta = {
      src: captured.utm_source || 'web',
      med: captured.utm_medium || '',
      camp: captured.utm_campaign || '',
      asset: content || captured.utm_content || 'quote',
      term: captured.utm_term || '',
      gclid: captured.gclid || '',
    };
    let text = JSON.stringify(Object.fromEntries(Object.entries(meta).filter(([, value]) => value)), null, 0);
    if (text.length <= 240) return text;
    delete meta.term;
    text = JSON.stringify(Object.fromEntries(Object.entries(meta).filter(([, value]) => value)), null, 0);
    if (text.length <= 240) return text;
    delete meta.gclid;
    return JSON.stringify(Object.fromEntries(Object.entries(meta).filter(([, value]) => value)), null, 0).slice(0, 240);
  }

  function hydrateBackNineQuoteLinks() {
    document.querySelectorAll('a[href*="app.back9ins.com/apply/rcowealth"]').forEach((link) => {
      let url;
      try { url = new URL(link.href); } catch { return; }
      const cta = link.dataset.quoteCta || url.searchParams.get('utm_content') || 'quote_cta';
      const passthrough = {
        utm_source: captured.utm_source || 'google',
        utm_medium: captured.utm_medium || 'cpc',
        utm_campaign: captured.utm_campaign || 'life-insurance-protection-review',
        utm_content: cta,
        utm_term: captured.utm_term || '',
        utm_id: captured.utm_id || '',
        gclid: captured.gclid || '',
        msclkid: captured.msclkid || '',
        fbclid: captured.fbclid || '',
        lead_source: sourceDetail(),
        campaign: captured.utm_campaign || 'life-insurance-protection-review',
        asset: cta,
        metadata: compactBackNineMetadata(cta),
      };
      Object.entries(passthrough).forEach(([key, value]) => {
        if (value) url.searchParams.set(key, String(value).slice(0, 255));
      });
      link.href = url.toString();
      link.setAttribute('data-attribution-ready', 'true');
    });
  }

  function applyNewsletterFields(form) {
    const optedIn = !!form.querySelector('input[name="newsletter_opt_in_display"]')?.checked;
    if (!optedIn) return;
    const today = new Date().toISOString().slice(0, 10);
    ensureHidden(form, '00NbV000003Urbb', '1'); // Lead.Newsletter_Enrolled__c
    ensureHidden(form, '00NbV000003Urbc', 'Active'); // Lead.Newsletter_Status__c
    ensureHidden(form, '00NbV000003Urba', today); // Lead.Newsletter_Enrolled_Date__c
  }

  function applySmsConsentField(form) {
    const optedIn = !!form.querySelector('input[name="sms_consent_display"]')?.checked;
    const existing = form.querySelector('input[name="00NbV000003ZxDB"]'); // Lead.SMS_Consent__c
    if (!optedIn) {
      if (existing) existing.remove();
      return;
    }
    ensureHidden(form, '00NbV000003ZxDB', '1'); // Lead.SMS_Consent__c
  }

  function ready(fn) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  ready(() => {
    hydrateBackNineQuoteLinks();

    document.querySelectorAll('form.campaign-form, form.lead-form, form.newsletter-form').forEach((form) => {
      form.dataset.startedAt = String(Date.now());
      ensureHoneypot(form);

      form.addEventListener('submit', (event) => {
        const honeypot = form.querySelector('input[name="website_url"], input[data-honeypot="true"]');
        const elapsed = Date.now() - Number(form.dataset.startedAt || Date.now());
        if ((honeypot && honeypot.value.trim()) || elapsed < 900) {
          event.preventDefault();
          event.stopImmediatePropagation();
          const ret = form.querySelector('input[name="retURL"]')?.value || '/thank-you.html';
          window.location.assign(ret);
          return;
        }

        const detail = sourceDetail();
        ensureHidden(form, 'lead_source', leadSourceForDetail(detail));
        ensureHidden(form, '00Nfn0000089jHR', detail); // Lead_Source_Detail__c
        const campaign = form.dataset.campaign || captured.utm_campaign || '';
        if (campaign) ensureHidden(form, '00NbV000003RzSl', campaign.slice(0, 255)); // Insurance_Campaign__c / campaign identifier
        applyNewsletterFields(form);
        applySmsConsentField(form);

        let description = form.querySelector('textarea[name="description"], input[name="description"]');
        if (!description) {
          description = document.createElement('input');
          description.type = 'hidden';
          description.name = 'description';
          form.appendChild(description);
        }
        const tracking = buildTrackingText(form, detail);
        if (!description.value.includes('--- Marketing attribution ---')) {
          description.value = `${description.value || ''}${tracking}`.slice(0, 32000);
        }
      }, { capture: true });
    });
  });
})();
