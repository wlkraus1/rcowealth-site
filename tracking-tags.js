(() => {
  const GTM_ID = 'GTM-N49D7RC';
  const GA4_ID = 'G-HQTS4WYCQC';
  const GOOGLE_ADS_ID = 'AW-9718091691';
  const META_PIXEL_ID = '1272338378394957';
  const w = window;
  w.dataLayer = w.dataLayer || [];
  w.gtag = w.gtag || function gtag(){ w.dataLayer.push(arguments); };
  w.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });

  const firstScript = document.getElementsByTagName('script')[0];
  const gtmScript = document.createElement('script');
  gtmScript.async = true;
  gtmScript.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(GTM_ID);
  firstScript.parentNode.insertBefore(gtmScript, firstScript);

  const gaScript = document.createElement('script');
  gaScript.async = true;
  gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA4_ID);
  firstScript.parentNode.insertBefore(gaScript, firstScript);
  w.gtag('js', new Date());
  w.gtag('config', GA4_ID, { send_page_view: true });
  w.gtag('config', GOOGLE_ADS_ID);

  if (!w.fbq) {
    const fbq = function fbq(){ fbq.callMethod ? fbq.callMethod.apply(fbq, arguments) : fbq.queue.push(arguments); };
    w.fbq = fbq;
    if (!w._fbq) w._fbq = fbq;
    fbq.push = fbq;
    fbq.loaded = true;
    fbq.version = '2.0';
    fbq.queue = [];

    const metaScript = document.createElement('script');
    metaScript.async = true;
    metaScript.src = 'https://connect.facebook.net/en_US/fbevents.js';
    firstScript.parentNode.insertBefore(metaScript, firstScript);
  }
  w.fbq('init', META_PIXEL_ID);
  w.fbq('track', 'PageView');

  function pushEvent(event, data = {}) {
    const payload = {
      event,
      page_path: w.location.pathname,
      page_title: document.title,
      ...data,
    };
    w.dataLayer.push(payload);
    w.gtag('event', event, {
      page_path: payload.page_path,
      page_title: payload.page_title,
      ...data,
    });

    if (event === 'generate_lead') {
      w.fbq('track', 'Lead', {
        content_name: payload.form_name || 'website_form',
        campaign: payload.campaign || undefined,
      });
    } else if (['schedule_click', 'phone_click', 'email_click', 'client_portal_click'].includes(event)) {
      w.fbq('trackCustom', event, {
        content_name: payload.link_text || event,
        link_url: payload.link_url || undefined,
      });
    }
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
