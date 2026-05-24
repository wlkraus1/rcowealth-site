(() => {
  const schedulerUrl = window.RAE_CO_LIFE_INSURANCE_SCHEDULER_URL;
  if (!schedulerUrl) return;
  const params = new URLSearchParams(window.location.search);
  const defaults = {
    utm_source: params.get('utm_source') || 'website',
    utm_medium: params.get('utm_medium') || 'landing-page',
    utm_campaign: params.get('utm_campaign') || 'life-insurance-family-protection',
    utm_content: params.get('utm_content') || 'landing-life-insurance-greenville'
  };
  const url = new URL(schedulerUrl);
  for (const [key, value] of Object.entries(defaults)) {
    if (value && !url.searchParams.has(key)) url.searchParams.set(key, value);
  }
  document.querySelectorAll('a.schedule-link').forEach((link) => {
    link.href = url.toString();
    link.removeAttribute('target');
    link.removeAttribute('rel');
    link.addEventListener('click', (event) => {
      // Some in-app/mobile browsers silently block or hide new tabs.
      // Keep scheduling in the same tab so every tap visibly navigates.
      event.preventDefault();
      window.location.assign(url.toString());
    });
  });
})();
