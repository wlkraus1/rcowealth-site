/* rcowealth.com revamp — scroll reveals + sticky-nav state.
   Additive only; does not touch site.js form/tab logic. */
(() => {
  // sticky header state on scroll
  const header = document.querySelector('[data-header]');
  if (header) {
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 24);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // ---- Live coverage band -------------------------------------------------
  // Two sliders and a number that moves while your thumb is still down. The
  // point is that a visitor gets an answer without clicking anything, so the
  // maths is deliberately the simplest honest version and the note under it
  // says exactly what it does and does not include.
  const lc = document.getElementById('liveCover');
  if (lc) {
    const inc = document.getElementById('lcIncome');
    const mor = document.getElementById('lcMortgage');
    const out = document.getElementById('lcOut');
    const full = document.getElementById('lcFull');
    const YEARS = 10; // stated in the note beside the number
    const money = n => '$' + Math.round(n).toLocaleString('en-US');
    const paint = r => {
      const min = +r.min, max = +r.max;
      r.style.setProperty('--p', max > min ? (+r.value - min) / (max - min) : 0);
    };
    const baseHref = full ? full.getAttribute('href') : '';
    const run = () => {
      const need = (+inc.value) * YEARS + (+mor.value);
      out.textContent = money(need);
      document.getElementById('lcIncomeOut').textContent = money(+inc.value);
      document.getElementById('lcMortgageOut').textContent = money(+mor.value);
      // Carry the two values into the full calculator so nothing is retyped.
      if (full) full.href = baseHref + '&income=' + (+inc.value) + '&mortgage=' + (+mor.value);
      paint(inc); paint(mor);
    };
    [inc, mor].forEach(r => r.addEventListener('input', run));
    run();
  }

  // scroll-reveal
  const targets = document.querySelectorAll('.reveal, .stagger');
  if (!targets.length) return;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) {
    targets.forEach(t => t.classList.add('in'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
  targets.forEach(t => io.observe(t));

  // Failsafe: reveal anything already in the viewport immediately on load
  // (above-the-fold content must never flash blank), and force-reveal all
  // remaining targets shortly after as a hard backstop.
  const revealInView = () => {
    targets.forEach(t => {
      const r = t.getBoundingClientRect();
      if (r.top < (window.innerHeight || 0) && r.bottom > 0) { t.classList.add('in'); io.unobserve(t); }
    });
  };
  revealInView();
  requestAnimationFrame(revealInView);
  setTimeout(() => targets.forEach(t => t.classList.add('in')), 1500);
})();
