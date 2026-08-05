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
