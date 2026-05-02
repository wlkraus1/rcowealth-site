(() => {
  const params = new URLSearchParams(window.location.search);
  const keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'fbclid'];
  const captured = {};
  for (const key of keys) {
    const value = params.get(key);
    if (value) captured[key] = value.slice(0, 180);
  }

  function buildTrackingText(form) {
    const data = {
      campaign: form.dataset.campaign || captured.utm_campaign || 'website',
      asset: form.dataset.asset || captured.utm_content || 'unknown',
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
      let description = form.querySelector('textarea[name="description"], input[name="description"]');
      if (!description) {
        description = document.createElement('input');
        description.type = 'hidden';
        description.name = 'description';
        form.appendChild(description);
      }
      const tracking = buildTrackingText(form);
      if (!description.value.includes('--- Marketing attribution ---')) {
        description.value = `${description.value || ''}${tracking}`.slice(0, 32000);
      }
    });
  });
})();
