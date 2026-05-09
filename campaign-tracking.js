(() => {
  const params = new URLSearchParams(window.location.search);
  const keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'fbclid'];
  const captured = {};
  for (const key of keys) {
    const value = params.get(key);
    if (value) captured[key] = value.slice(0, 180);
  }

  const referrer = document.referrer || '';
  if (referrer) captured.referrer = referrer.slice(0, 240);

  function sourceDetail() {
    const source = String(captured.utm_source || '').toLowerCase();
    const medium = String(captured.utm_medium || '').toLowerCase();
    const ref = String(captured.referrer || '').toLowerCase();
    if (captured.gclid || source.includes('google') || ref.includes('google.')) return 'Google Search';
    if (source.includes('instagram') || source === 'ig' || ref.includes('instagram.com')) return 'Instagram';
    if (captured.fbclid || source.includes('facebook') || source === 'fb' || ref.includes('facebook.com') || ref.includes('l.facebook.com')) return 'Facebook';
    if (source.includes('backnine')) return 'BackNine';
    if (medium.includes('referral')) return 'Referral';
    return 'Website';
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

  function buildTrackingText(form, detail) {
    const data = {
      campaign: form.dataset.campaign || captured.utm_campaign || 'website',
      asset: form.dataset.asset || captured.utm_content || 'unknown',
      lead_source_detail: detail,
      page: window.location.pathname,
      ...captured,
    };
    return '\n\n--- Marketing attribution ---\n' + Object.entries(data)
      .filter(([, value]) => value)
      .map(([key, value]) => `${key}: ${String(value).replace(/\s+/g, ' ').trim()}`)
      .join('\n');
  }

  document.querySelectorAll('form.campaign-form, form.lead-form, form.newsletter-form').forEach((form) => {
    form.addEventListener('submit', () => {
      const detail = sourceDetail();
      ensureHidden(form, '00Nfn0000089jHR', detail); // Lead_Source_Detail__c
      const campaign = form.dataset.campaign || captured.utm_campaign || '';
      if (campaign) ensureHidden(form, '00NbV000003RzSl', campaign.slice(0, 255)); // Insurance_Campaign__c / campaign identifier

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
    });
  });
})();
