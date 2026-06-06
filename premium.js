/* =========================================================
   Rae & Co Capital — Premium animation engine (V11)
   GSAP + ScrollTrigger scroll choreography.

   Design rules:
   - Content is ALWAYS visible if anything fails. The .anim class
     (set in <head>) is the only thing that hides reveal elements;
     we strip it the moment we know animations can't run.
   - Respect prefers-reduced-motion (the .anim class is never added
     in that case, so reveals are visible by default).
   ========================================================= */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGSAP = typeof window.gsap !== 'undefined';

  /* ---- Always-on, framework-free enhancements ---- */
  initScrollProgress();
  initHeaderState();
  if (!reduce) initMagnetic();

  /* ---- If GSAP is missing or motion is off, reveal everything and stop ---- */
  if (!hasGSAP || reduce) {
    root.classList.remove('anim');
    return;
  }

  var gsap = window.gsap;
  window.__raeAnimReady = true; // tells the head failsafe the engine is live
  if (window.ScrollTrigger) gsap.registerPlugin(window.ScrollTrigger);

  /* Safety net: if something throws mid-setup, never leave content hidden. */
  try {
    runChoreography(gsap);
  } catch (err) {
    root.classList.remove('anim');
    if (window.console) console.warn('Animation setup skipped:', err);
  }

  /* ===================================================== */

  function runChoreography(gsap) {
    var ST = window.ScrollTrigger;

    /* ---- Hero entrance timeline ---- */
    gsap.set('.hero-title .line-inner', { yPercent: 110 });
    var tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
    tl.to('.virtual-flag[data-reveal]', { opacity: 1, y: 0, duration: .6 })
      .to('.hero-copy .eyebrow[data-reveal]', { opacity: 1, y: 0, duration: .5 }, '-=.35')
      .to('.hero-title .line-inner', { yPercent: 0, duration: .9, stagger: .12, ease: 'power4.out' }, '-=.3')
      .to('.hero-copy .lead[data-reveal]', { opacity: 1, y: 0, duration: .6 }, '-=.5')
      .to('.hero-actions[data-reveal]', { opacity: 1, y: 0, duration: .55 }, '-=.4')
      .to('.hero-meta[data-reveal]', { opacity: 1, y: 0, duration: .55 }, '-=.4')
      .to('.virtual-office-card[data-reveal]', { opacity: 1, x: 0, y: 0, duration: .9, ease: 'power3.out' }, '-=.9')
      .to('.workflow-row[data-stagger]', { opacity: 1, y: 0, duration: .5, stagger: .08 }, '-=.5');

    /* ---- Scroll reveals (everything not in the hero) ---- */
    if (ST) {
      var heroReveals = document.querySelectorAll('.virtual-hero [data-reveal], .virtual-hero [data-stagger]');
      var inHero = new Set(Array.prototype.slice.call(heroReveals));

      document.querySelectorAll('[data-reveal]').forEach(function (el) {
        if (inHero.has(el)) return;
        gsap.to(el, {
          opacity: 1, x: 0, y: 0, duration: .8, ease: 'power3.out',
          scrollTrigger: { trigger: el, start: 'top 86%', once: true }
        });
      });

      document.querySelectorAll('[data-stagger]').forEach(function (el) {
        if (inHero.has(el)) return;
        gsap.to(el, {
          opacity: 1, y: 0, duration: .55, ease: 'power3.out',
          scrollTrigger: { trigger: el, start: 'top 90%', once: true }
        });
      });

      /* ---- Parallax layers ---- */
      document.querySelectorAll('[data-parallax]').forEach(function (el) {
        var speed = parseFloat(el.getAttribute('data-parallax')) || .15;
        gsap.to(el, {
          yPercent: speed * 100,
          ease: 'none',
          scrollTrigger: { trigger: el.closest('section') || el, start: 'top bottom', end: 'bottom top', scrub: true }
        });
      });

      /* ---- Count-up stats ---- */
      document.querySelectorAll('.count[data-count]').forEach(function (el) {
        var target = parseFloat(el.getAttribute('data-count')) || 0;
        var suffix = el.getAttribute('data-suffix') || '';
        var obj = { v: 0 };
        gsap.to(obj, {
          v: target, duration: 1.6, ease: 'power2.out',
          scrollTrigger: { trigger: el, start: 'top 88%', once: true },
          onUpdate: function () { el.textContent = Math.round(obj.v) + suffix; },
          onComplete: function () { el.textContent = target + suffix; }
        });
      });

      /* ---- Process drawing line ---- */
      var fill = document.querySelector('.process-line i');
      if (fill) {
        gsap.to(fill, {
          height: '100%', ease: 'none',
          scrollTrigger: { trigger: '.process-card', start: 'top 70%', end: 'bottom 75%', scrub: true }
        });
      }
    } else {
      /* No ScrollTrigger: just reveal non-hero content immediately. */
      document.querySelectorAll('[data-reveal],[data-stagger]').forEach(function (el) {
        if (el.closest('.virtual-hero')) return;
        el.style.opacity = '1';
        el.style.transform = 'none';
      });
    }
  }

  /* ---- Scroll progress bar ---- */
  function initScrollProgress() {
    var bar = document.querySelector('.scroll-progress span');
    if (!bar) return;
    var ticking = false;
    function update() {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      var pct = max > 0 ? (h.scrollTop || window.pageYOffset) / max * 100 : 0;
      bar.style.width = pct + '%';
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  /* ---- Header condense on scroll ---- */
  function initHeaderState() {
    var header = document.querySelector('[data-header]');
    if (!header) return;
    var ticking = false;
    function update() {
      header.classList.toggle('scrolled', (window.pageYOffset || document.documentElement.scrollTop) > 24);
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  /* ---- Magnetic buttons (fine pointers only) ---- */
  function initMagnetic() {
    if (!window.matchMedia || !window.matchMedia('(pointer: fine)').matches) return;
    document.querySelectorAll('.magnetic').forEach(function (el) {
      var strength = 0.28;
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - (r.left + r.width / 2)) * strength;
        var y = (e.clientY - (r.top + r.height / 2)) * strength;
        el.style.transform = 'translate(' + x + 'px,' + y + 'px)';
      });
      el.addEventListener('pointerleave', function () {
        el.style.transform = 'translate(0,0)';
      });
    });
  }
})();
