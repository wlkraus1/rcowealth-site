
(() => {
  const menu = document.querySelector('[data-menu]');
  const navlinks = document.querySelector('.navlinks');
  if (menu && navlinks) {
    menu.addEventListener('click', () => {
      const open = navlinks.classList.toggle('show');
      menu.setAttribute('aria-expanded', String(open));
    });
    navlinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      navlinks.classList.remove('show');
      menu.setAttribute('aria-expanded', 'false');
    }));
  }

  const tabData = {
    portfolio: {
      kicker:'Investment management',
      title:'Build the portfolio around the job of the money.',
      interest:'Investments', next:'Portfolio or retirement review', page:'investment-management-greenville-sc.html',
      copy:'Portfolio decisions should not live in a vacuum. Rae & Co reviews allocation, risk, liquidity, tax sensitivity, account structure, and the purpose of each dollar so the investment strategy supports the broader plan.',
      reviewed:['Current accounts, allocation, and risk exposure','Liquidity needs, time horizon, and concentration risk','Tax-sensitive decisions, rebalancing, and account location'],
      output:['Portfolio policy priorities','Implementation and review rhythm','Clear tradeoffs before changes are made'],
      decision:'Best fit when you have assets in motion and want the portfolio connected to real obligations instead of market noise.'
    },
    income: {
      kicker:'Retirement income',
      title:'Convert assets into income with fewer unanswered questions.',
      interest:'Investments', next:'Portfolio or retirement review', page:'retirement-planning-greenville-sc.html',
      copy:'The move from saving to spending is where small gaps become expensive. Rae & Co organizes withdrawal order, reserves, Social Security timing, survivor needs, taxes, and market-risk exposure before the paycheck changes.',
      reviewed:['Income sources, spending needs, and timing','Withdrawal sequencing and cash reserves','Longevity, survivor needs, taxes, and market risk'],
      output:['Retirement income map','Reserve and withdrawal framework','Decision list before retirement pressure hits'],
      decision:'Best fit when retirement is close, already here, or becoming too important to manage by guesswork.'
    },
    protection: {
      kicker:'Protection planning',
      title:'Make insurance answer to the plan, not the other way around.',
      interest:'Insurance', next:'Life insurance planning', page:'life-insurance-greenville-sc.html',
      copy:'Life insurance is handled as part of the financial architecture: existing coverage, new policy needs, income, debt, dependents, business exposure, policy ownership, beneficiaries, liquidity, and legacy objectives all matter before applying for or changing coverage.',
      reviewed:['Existing policies and employer coverage','New term or permanent coverage needs','Income replacement, debt, dependents, and business exposure','Carrier fit, ownership, beneficiaries, liquidity, and estate coordination'],
      output:['Coverage strategy tied to the plan','Gap, overlap, and beneficiary summary','Carrier, underwriting, and application next steps when new coverage makes sense'],
      decision:'Best fit when family, business, or estate obligations would be exposed if income or ownership changed.'
    },
    planning: {
      kicker:'Financial planning',
      title:'Turn disconnected financial decisions into a clean sequence.',
      interest:'Both', next:'Focused intro call', page:'financial-advisor-greenville-sc.html',
      copy:'Planning is the decision system. Cash flow, compensation, investments, insurance, tax exposure, debt, estate priorities, business obligations, and family needs are organized so the next move is clear.',
      reviewed:['Cash flow, debt, savings, and compensation decisions','Major family, business, and retirement questions','Insurance, liquidity, tax, and estate coordination points'],
      output:['Clean decision map','Decision sequence','Action list that can actually be implemented'],
      decision:'Best fit when you know something needs attention but want the whole picture organized before acting.'
    }
  };

  const panel = document.getElementById('tabPanel');
  function optionByText(select, text) {
    if (!select || !text) return;
    const match = [...select.options].find(o => o.value.toLowerCase() === text.toLowerCase() || o.textContent.trim().toLowerCase() === text.toLowerCase());
    if (match) select.value = match.value;
  }
  function prefillForm(key, jump = true) {
    const d = tabData[key];
    const form = document.querySelector('#leadForm, form.contact-lead-form');
    if (!d || !form) return;
    optionByText(form.querySelector('select[name="00Nfn0000089jXZ"]'), d.interest);
    optionByText(form.querySelector('select[name="preferred_next_step_display"]'), d.next);
    const hiddenInterest = form.querySelector('input[type="hidden"][name="00Nfn0000089jXZ"]');
    const hiddenNext = form.querySelector('input[type="hidden"][name="preferred_next_step_display"]');
    if (hiddenInterest) hiddenInterest.value = d.interest;
    if (hiddenNext) hiddenNext.value = d.next;
    const desc = form.querySelector('textarea[name="description"]');
    if (desc && !desc.value.trim()) desc.value = `I would like to talk about ${d.kicker.toLowerCase()}.`;
    if (jump) document.getElementById('contact')?.scrollIntoView({behavior:'smooth'});
  }
  function renderTab(key, scroll = false) {
    const d = tabData[key] || tabData.portfolio;
    document.querySelectorAll('[data-tab]').forEach(b => b.classList.toggle('active', b.dataset.tab === key));
    document.querySelectorAll('[data-service]').forEach(card => card.classList.toggle('active', card.dataset.service === key));
    if (panel) {
      panel.innerHTML = `
        <div class="panel-kicker">${d.kicker}</div>
        <h3>${d.title}</h3>
        <p>${d.copy}</p>
        <div class="detail-stack">
          <div class="detail-box"><b>Reviewed</b><ul>${d.reviewed.map(item => `<li>${item}</li>`).join('')}</ul></div>
          <div class="detail-box"><b>Client output</b><ul>${d.output.map(item => `<li>${item}</li>`).join('')}</ul></div>
          <div class="detail-box"><b>When it matters</b><ul><li>${d.decision}</li><li>Useful when decisions need to connect across accounts, income, insurance, and family obligations.</li></ul></div>
        </div>
        <div class="decision-line"><b>Plain-English goal:</b> fewer loose ends, cleaner decisions, and a plan that can be explained without jargon.</div>
        <div class="tab-cta"><button class="btn btn-primary" type="button" data-prefill="${key}">Start with this area →</button><a class="btn btn-secondary" href="${d.page}">Read the page</a></div>`;
    }
    if (scroll) document.getElementById('method')?.scrollIntoView({behavior:'smooth'});
    if (history.replaceState && document.getElementById('method')) history.replaceState(null, '', `#${key}`);
  }
  document.querySelectorAll('[data-tab]').forEach(btn => btn.addEventListener('click', () => renderTab(btn.dataset.tab, false)));
  document.querySelectorAll('[data-service]').forEach(card => {
    card.addEventListener('click', () => renderTab(card.dataset.service, true));
    card.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); renderTab(card.dataset.service, true); } });
  });
  document.addEventListener('click', e => {
    const btn = e.target.closest('[data-prefill]');
    if (btn) prefillForm(btn.dataset.prefill, true);
  });
  if (panel) {
    const hash = location.hash.replace('#','');
    const initial = ['portfolio','income','protection','planning'].includes(hash) ? hash : 'portfolio';
    renderTab(initial, false);
  }

  document.querySelectorAll('form.contact-lead-form').forEach(form => {
    form.addEventListener('submit', e => {
      const honey = form.querySelector('input[name="website_url"], input[data-honeypot="true"]');
      if (honey && honey.value.trim()) { e.preventDefault(); return; }
      const desc = form.querySelector('textarea[name="description"]');
      if (desc && !desc.dataset.enriched) {
        const interest = form.querySelector('select[name="00Nfn0000089jXZ"], input[name="00Nfn0000089jXZ"]')?.value || '';
        const next = form.querySelector('select[name="preferred_next_step_display"], input[name="preferred_next_step_display"]')?.value || '';
        const newsletter = form.querySelector('input[name="newsletter_opt_in_display"]')?.checked ? 'Yes' : 'No';
        const sms = form.querySelector('input[name="sms_consent_display"]')?.checked ? 'Yes' : 'No';
        const base = desc.value.trim();
        desc.value = [base, `Primary interest: ${interest}`, `Preferred next step: ${next}`, `Newsletter opt-in: ${newsletter}`, `SMS consent: ${sms}`, `Source page: ${location.pathname || 'index.html'}`].filter(Boolean).join('\n');
        desc.dataset.enriched = 'true';
      }
    });
  });

  const copyButton = document.getElementById('copyEmail');
  const notice = document.getElementById('notice');
  if (copyButton) {
    copyButton.addEventListener('click', async () => {
      const text = 'Rae & Co Capital — 864-558-8440 — info@rcowealth.com';
      try { await navigator.clipboard.writeText(text); } catch(e) {}
      if (notice) { notice.classList.add('show'); setTimeout(() => notice.classList.remove('show'), 3500); }
    });
  }
})();
