(function(){
  var path = window.location.pathname || '/';
  if (path.indexOf('/mobile.html') !== -1 || path.indexOf('/thank-you') !== -1) return;
  var isMobileWidth = window.matchMedia && window.matchMedia('(max-width: 820px)').matches;
  var isCoarse = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
  var isMobileUA = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent || '');
  if (!(isMobileWidth || (isCoarse && isMobileUA))) return;
  var target = '/mobile.html' + (window.location.hash || '');
  window.location.replace(target);
})();
