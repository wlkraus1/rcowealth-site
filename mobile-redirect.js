(function(){
  var path = window.location.pathname || '/';
  if (path.indexOf('/mobile.html') !== -1 || path.indexOf('/thank-you') !== -1) return;
  if (
    path.indexOf('/life-insurance-protection-review.html') !== -1 ||
    path.indexOf('/life-insurance-review-checklist.html') !== -1 ||
    path.indexOf('/life-insurance-greenville-sc.html') !== -1
  ) return;
  var isMobileWidth = window.matchMedia && window.matchMedia('(max-width: 820px)').matches;
  var isCoarse = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
  var isMobileUA = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent || '');
  if (!(isMobileWidth || (isCoarse && isMobileUA))) return;
  var target = '/mobile.html' + (window.location.hash || '');
  window.location.replace(target);
})();
