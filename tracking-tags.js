(() => {
  const GTM_ID = 'GTM-N49D7RC';
  const w = window;
  w.dataLayer = w.dataLayer || [];
  w.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });

  const firstScript = document.getElementsByTagName('script')[0];
  const gtmScript = document.createElement('script');
  gtmScript.async = true;
  gtmScript.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(GTM_ID);
  firstScript.parentNode.insertBefore(gtmScript, firstScript);

  function pushEvent(event, data = {}) {
    w.dataLayer.push({
      event,
      page_path: w.location.pathname,
      page_title: document.title,
      ...data,
    });
  }

  function linkLabel(link) {
    return (link.dataset.trackingLabel || link.textContent || link.getAttribute('aria-label') || link.href || '')
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, 120);
  }

  document.addEventListener('DOMContentLoaded', () => {
    pushEvent('rae_page_view');

    document.querySelectorAll('form.campaign-form, form.lead-form, form.newsletter-form').forEach((form) => {
      form.addEventListener('submit', () => {
        pushEvent('generate_lead', {
          form_id: form.id || '',
          form_name: form.dataset.formPurpose || form.dataset.campaign || 'website_form',
          campaign: form.dataset.campaign || '',
        });
      }, { capture: true });
    });

    document.querySelectorAll('a[href]').forEach((link) => {
      link.addEventListener('click', () => {
        const href = link.href || '';
        if (/scheduler\.zoom\.us/i.test(href)) {
          pushEvent('schedule_click', { link_url: href, link_text: linkLabel(link) });
        } else if (/client\.schwab\.com|mutualofomaha\.com/i.test(href)) {
          pushEvent('client_portal_click', { link_url: href, link_text: linkLabel(link) });
        } else if (/^tel:/i.test(link.getAttribute('href') || '')) {
          pushEvent('phone_click', { link_url: link.getAttribute('href'), link_text: linkLabel(link) });
        } else if (/^mailto:/i.test(link.getAttribute('href') || '')) {
          pushEvent('email_click', { link_url: link.getAttribute('href'), link_text: linkLabel(link) });
        }
      });
    });
  });
})();
