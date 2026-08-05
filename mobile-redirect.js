(function(){
  // mobile.html is a mobile version of the HOMEPAGE and of nothing else. This script used to send a
  // phone from ANY page to it with `location.replace('/mobile.html')`, which drops the path — so a
  // visitor tapping through to Services, Investment Management, Retirement Planning or Contact
  // landed on the mobile homepage and had to find the page again. Traffic here is reels and social,
  // i.e. almost entirely mobile, so that was most visitors.
  //
  // It was an SEO problem in the same breath: Googlebot Smartphone matches the UA test and renders
  // at a mobile viewport, so under mobile-first indexing every one of those URLs redirected to the
  // homepage for the crawler too.
  //
  // So the rule is now the narrow one it should always have been: redirect the homepage, and only
  // the homepage. Everything else stays on the page the visitor actually asked for. The site's
  // breakpoints live in styles.css and revamp.css (17 media queries between them), which is what
  // those pages lay out with — the per-page grep for `@media` reads zero because the CSS is
  // external, and that is the thing that makes this look scarier than it is.
  //
  // An allow-list of pages to redirect rather than a deny-list of pages to spare: a page added later
  // gets the correct behaviour by default, whereas the old shape silently swallowed every new page
  // the moment it shipped. That is exactly how life-insurance-calculator.html and
  // life-insurance-quote.html escaped only by not loading this script at all.
  var path = window.location.pathname || '/';
  var isHome = path === '/' || path === '/index.html' || path === '/index.htm';
  if (!isHome) return;
  var isMobileWidth = window.matchMedia && window.matchMedia('(max-width: 820px)').matches;
  var isCoarse = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
  var isMobileUA = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent || '');
  if (!(isMobileWidth || (isCoarse && isMobileUA))) return;
  var target = '/mobile.html' + (window.location.search || '') + (window.location.hash || '');
  window.location.replace(target);
})();
