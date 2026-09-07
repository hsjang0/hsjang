/* Theme toggle + scroll spy. No dependencies. */
(function () {
  'use strict';

  var STORAGE_KEY = 'theme';
  var root = document.documentElement;

  /* --- theme ------------------------------------------------------------ */
  function stored() {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }

  function apply(theme) {
    root.setAttribute('data-theme', theme);
    var btn = document.querySelector('.theme-toggle');
    if (btn) {
      btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
      btn.setAttribute('aria-pressed', String(theme === 'dark'));
    }
  }

  function systemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function initTheme() {
    apply(stored() || systemTheme());

    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    var onChange = function () { if (!stored()) apply(systemTheme()); };
    if (mq.addEventListener) { mq.addEventListener('change', onChange); }
    else if (mq.addListener) { mq.addListener(onChange); }

    var btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      apply(next);
      try { localStorage.setItem(STORAGE_KEY, next); } catch (e) { /* private mode */ }
    });
  }

  /* --- sticky bar shadow ------------------------------------------------ */
  function initTopbar() {
    var bar = document.querySelector('.topbar');
    if (!bar) return;
    var onScroll = function () { bar.classList.toggle('is-stuck', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* --- scroll spy ------------------------------------------------------- */
  function initScrollSpy() {
    var links = Array.prototype.slice.call(document.querySelectorAll('.nav a[href*="#"]'));
    if (!links.length || !('IntersectionObserver' in window)) return;

    var byId = {};
    var sections = [];
    links.forEach(function (link) {
      var id = link.getAttribute('href').split('#')[1];
      var el = id && document.getElementById(id);
      if (!el) return;
      byId[id] = link;
      sections.push(el);
    });

    var visible = {};
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { visible[entry.target.id] = entry.isIntersecting; });

      var current = null;
      for (var i = 0; i < sections.length; i++) {
        if (visible[sections[i].id]) { current = sections[i].id; break; }
      }
      links.forEach(function (link) { link.classList.remove('is-active'); });
      if (current && byId[current]) { byId[current].classList.add('is-active'); }
    }, { rootMargin: '-72px 0px -65% 0px', threshold: 0 });

    sections.forEach(function (el) { observer.observe(el); });
  }

  function init() { initTheme(); initTopbar(); initScrollSpy(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
