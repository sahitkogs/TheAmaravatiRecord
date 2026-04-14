/* ================================================================
   The Amaravati Record — Shared Header, Nav, Footer & Theme Toggle
   ----------------------------------------------------------------
   Bilingual EN/TE support. Drop into any page, then call:
     AmaravatiHeader.render({ page: 'about' })

   Language detection: URL path → localStorage → default 'en'.
   Theme toggle: sun/moon icon. Persists in localStorage.
   ================================================================ */

// --- Theme: apply saved preference immediately (before render) to avoid flash ---
(function () {
  var THEME_KEY = 'amaravati_theme';
  var saved = null;
  try { saved = localStorage.getItem(THEME_KEY); } catch (e) {}
  document.documentElement.setAttribute('data-theme', (saved === 'dark' || saved === 'light') ? saved : 'light');
})();

var AmaravatiHeader = (function () {
  'use strict';

  var THEME_KEY = 'amaravati_theme';
  var LANG_KEY = 'amaravati_lang';

  var STRINGS = {
    en: {
      meta1: 'VOL. I &middot; NO. 001',
      meta2: 'FRIDAY, APRIL 10, 2026',
      meta3: 'FOUNDING EDITION &middot; AMARAVATI, A.P.',
      title: 'The Amaravati Record',
      tagline: '&ldquo;Independent reporting on the making of a capital&rdquo; &mdash; Est. 2026',
      home: 'Home', reports: 'Reports', about: 'About', support: 'Support',
      footer1: 'THE AMARAVATI RECORD &middot; FOUNDING EDITION &middot; APRIL 2026',
      privacy: 'Privacy', cookies: 'Cookies', terms: 'Terms',
      editorial: 'Editorial', corrections: 'Corrections', ai: 'AI',
      licenses: 'Licenses', contact: 'Contact', tracker: 'Tracker',
      cookieSettings: 'Cookie settings',
      footer3: 'Independent &middot; Public Interest &middot; Reader-Supported',
      langLabel: '\u0C24\u0C46'
    },
    te: {
      meta1: '\u0C38\u0C02\u0C2A\u0C41\u0C1F\u0C3F I &middot; \u0C38\u0C02\u0C1A\u0C3F\u0C15 001',
      meta2: '\u0C36\u0C41\u0C15\u0C4D\u0C30\u0C35\u0C3E\u0C30\u0C02, \u0C0F\u0C2A\u0C4D\u0C30\u0C3F\u0C32\u0C4D 10, 2026',
      meta3: '\u0C38\u0C4D\u0C25\u0C3E\u0C2A\u0C15 \u0C38\u0C02\u0C1A\u0C3F\u0C15 &middot; \u0C05\u0C2E\u0C30\u0C3E\u0C35\u0C24\u0C3F, \u0C06.\u0C2A\u0C4D\u0C30.',
      title: '\u0C26\u0C3F \u0C05\u0C2E\u0C30\u0C3E\u0C35\u0C24\u0C3F \u0C30\u0C3F\u0C15\u0C3E\u0C30\u0C4D\u0C21\u0C4D',
      tagline: '&ldquo;\u0C30\u0C3E\u0C1C\u0C27\u0C3E\u0C28\u0C3F \u0C28\u0C3F\u0C30\u0C4D\u0C2E\u0C3E\u0C23\u0C02\u0C2A\u0C48 \u0C38\u0C4D\u0C35\u0C24\u0C02\u0C24\u0C4D\u0C30 \u0C2A\u0C30\u0C3F\u0C36\u0C4B\u0C27\u0C28\u0C3E \u0C2A\u0C24\u0C4D\u0C30\u0C3F\u0C15&rdquo; &mdash; \u0C38\u0C4D\u0C25\u0C3E\u0C2A\u0C28 2026',
      home: '\u0C39\u0C4B\u0C2E\u0C4D', reports: '\u0C28\u0C3F\u0C35\u0C47\u0C26\u0C3F\u0C15\u0C32\u0C41', about: '\u0C17\u0C41\u0C30\u0C3F\u0C02\u0C1A\u0C3F', support: '\u0C2E\u0C26\u0C4D\u0C26\u0C24\u0C41',
      footer1: '\u0C26\u0C3F \u0C05\u0C2E\u0C30\u0C3E\u0C35\u0C24\u0C3F \u0C30\u0C3F\u0C15\u0C3E\u0C30\u0C4D\u0C21\u0C4D &middot; \u0C38\u0C4D\u0C25\u0C3E\u0C2A\u0C15 \u0C38\u0C02\u0C1A\u0C3F\u0C15 &middot; \u0C0F\u0C2A\u0C4D\u0C30\u0C3F\u0C32\u0C4D 2026',
      privacy: '\u0C17\u0C4B\u0C2A\u0C4D\u0C2F\u0C24', cookies: '\u0C15\u0C41\u0C15\u0C40\u0C32\u0C41', terms: '\u0C28\u0C3F\u0C2C\u0C02\u0C27\u0C28\u0C32\u0C41',
      editorial: '\u0C38\u0C02\u0C2A\u0C3E\u0C26\u0C15\u0C40\u0C2F\u0C02', corrections: '\u0C38\u0C35\u0C30\u0C23\u0C32\u0C41', ai: 'AI',
      licenses: '\u0C32\u0C48\u0C38\u0C46\u0C28\u0C4D\u0C38\u0C41\u0C32\u0C41', contact: '\u0C38\u0C02\u0C2A\u0C4D\u0C30\u0C26\u0C3F\u0C02\u0C1A\u0C02\u0C21\u0C3F', tracker: '\u0C1F\u0C4D\u0C30\u0C3E\u0C15\u0C30\u0C4D',
      cookieSettings: '\u0C15\u0C41\u0C15\u0C40 \u0C38\u0C46\u0C1F\u0C4D\u0C1F\u0C3F\u0C02\u0C17\u0C4D\u200C\u0C32\u0C41',
      footer3: '\u0C38\u0C4D\u0C35\u0C24\u0C02\u0C24\u0C4D\u0C30 &middot; \u0C2A\u0C4D\u0C30\u0C1C\u0C3E\u0C39\u0C3F\u0C24\u0C02 &middot; \u0C2A\u0C3E\u0C20\u0C15 \u0C2E\u0C26\u0C4D\u0C26\u0C24\u0C41',
      langLabel: 'EN'
    }
  };

  // ── Theme ──

  function getTheme() {
    var saved = null;
    try { saved = localStorage.getItem(THEME_KEY); } catch (e) {}
    if (saved === 'dark' || saved === 'light') return saved;
    return 'light';
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
    var btns = document.querySelectorAll('.theme-toggle');
    var icon = theme === 'dark' ? '\u2600' : '\u263D';
    for (var i = 0; i < btns.length; i++) btns[i].textContent = icon;
  }

  // ── Language ──

  function getLang() {
    var p = location.pathname;
    if (p.indexOf('/en/') !== -1) return 'en';
    if (p.indexOf('/te/') !== -1) return 'te';
    var saved = null;
    try { saved = localStorage.getItem(LANG_KEY); } catch (e) {}
    if (saved === 'en' || saved === 'te') return saved;
    return 'en';
  }

  function setLang(lang) {
    try { localStorage.setItem(LANG_KEY, lang); } catch (e) {}
  }

  function switchLang() {
    var current = getLang();
    var target = current === 'en' ? 'te' : 'en';
    try { localStorage.setItem(LANG_KEY, target); } catch (e) {}
    var path = location.pathname;
    location.href = path.replace('/' + current + '/', '/' + target + '/');
  }

  // ── Path helpers ──

  function getBase() {
    var scripts = document.getElementsByTagName('script');
    for (var i = scripts.length - 1; i >= 0; i--) {
      var src = scripts[i].getAttribute('src') || '';
      if (src.indexOf('site-header.js') !== -1) {
        return src.replace(/site-header\.js.*$/, '');
      }
    }
    var p = location.pathname;
    if (p.indexOf('/pages/') !== -1 || p.indexOf('/reports/') !== -1) return '../../';
    return '../';
  }

  function getLangBase() {
    var p = location.pathname;
    if (p.indexOf('/pages/') !== -1 || p.indexOf('/reports/') !== -1) return '../';
    return '';
  }

  function injectCSS(base) {
    var href = base + 'site-header.css';
    if (!document.querySelector('link[href="' + href + '"]')) {
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = href;
      document.head.appendChild(link);
    }
  }

  // ── Render ──

  function render(opts) {
    opts = opts || {};
    var page = opts.page || '';
    var base = getBase();
    var lang = getLang();
    var s = STRINGS[lang];
    var langBase = getLangBase();
    var pagesBase = langBase + 'pages/';
    var theme = getTheme();

    // Set html lang attribute
    document.documentElement.lang = lang;

    // Inject shared header CSS
    injectCSS(base);

    // Apply theme
    setTheme(theme);

    // Save detected language
    setLang(lang);

    // ── Masthead ──
    var mastheadEl = document.getElementById('site-masthead');
    if (mastheadEl) {
      var icon = theme === 'dark' ? '\u2600' : '\u263D';
      mastheadEl.innerHTML =
        '<header class="masthead">' +
        '  <div class="masthead__meta">' +
        '    <span>' + s.meta1 + '</span>' +
        '    <span>' + s.meta2 + '</span>' +
        '    <span>' + s.meta3 + ' &ensp;|&ensp;' +
              '<button class="theme-toggle theme-toggle--desktop" aria-label="Toggle dark mode" title="Toggle dark mode">' + icon + '</button>' +
              ' &ensp;|&ensp;' +
              '<button class="lang-toggle lang-toggle--desktop" aria-label="Switch language" title="Switch language">' + s.langLabel + '</button>' +
        '    </span>' +
        '    <button class="theme-toggle theme-toggle--mobile" aria-label="Toggle dark mode" title="Toggle dark mode">' + icon + '</button>' +
        '    <button class="lang-toggle lang-toggle--mobile" aria-label="Switch language" title="Switch language">' + s.langLabel + '</button>' +
        '  </div>' +
        '  <h1 class="masthead__title"><a href="' + langBase + 'index.html" style="color:inherit;text-decoration:none;">' + s.title + '</a></h1>' +
        '  <p class="masthead__tagline">' + s.tagline + '</p>' +
        '</header>';

      // Bind theme toggles
      var themeBtns = mastheadEl.querySelectorAll('.theme-toggle');
      for (var b = 0; b < themeBtns.length; b++) {
        themeBtns[b].addEventListener('click', function () {
          var current = getTheme();
          setTheme(current === 'dark' ? 'light' : 'dark');
        });
      }

      // Bind lang toggles
      var langBtns = mastheadEl.querySelectorAll('.lang-toggle');
      for (var l = 0; l < langBtns.length; l++) {
        langBtns[l].addEventListener('click', switchLang);
      }
    }

    // ── Nav ──
    var navEl = document.getElementById('site-nav');
    if (navEl) {
      var links = [
        { href: langBase + 'index.html',          label: s.home,    id: 'index' },
        { href: pagesBase + 'reports.html',        label: s.reports, id: 'reports' },
        { href: pagesBase + 'about.html',          label: s.about,   id: 'about' },
        { href: pagesBase + 'support.html',        label: s.support, id: 'support' }
      ];
      var html = '<nav class="nav" aria-label="Primary">';
      for (var i = 0; i < links.length; i++) {
        var cls = (links[i].id === page) ? ' class="is-current"' : '';
        html += '<a href="' + links[i].href + '"' + cls + '>' + links[i].label + '</a>';
      }
      html += '</nav>';
      navEl.innerHTML = html;
    }

    // ── Footer ──
    var footerEl = document.getElementById('site-footer');
    if (footerEl) {
      footerEl.innerHTML =
        '<footer class="colophon">' +
        '  <span>' + s.footer1 + '</span>' +
        '  <span>' +
        '    <a href="' + pagesBase + 'privacy.html">' + s.privacy + '</a> &middot; ' +
        '    <a href="' + pagesBase + 'cookies.html">' + s.cookies + '</a> &middot; ' +
        '    <a href="' + pagesBase + 'terms.html">' + s.terms + '</a> &middot; ' +
        '    <a href="' + pagesBase + 'editorial.html">' + s.editorial + '</a> &middot; ' +
        '    <a href="' + pagesBase + 'corrections.html">' + s.corrections + '</a> &middot; ' +
        '    <a href="' + pagesBase + 'ai-disclosure.html">' + s.ai + '</a> &middot; ' +
        '    <a href="' + pagesBase + 'licenses.html">' + s.licenses + '</a> &middot; ' +
        '    <a href="' + pagesBase + 'contact.html">' + s.contact + '</a> &middot; ' +
        '    <a href="https://sahitkogs.github.io/amaravati-tracker-staging/" target="_blank" rel="noopener">' + s.tracker + '</a>' +
        (typeof AmaravatRecord_openConsent === 'function'
          ? ' &middot; <a href="#" onclick="return AmaravatRecord_openConsent();">' + s.cookieSettings + '</a>'
          : '') +
        '  </span>' +
        '  <span>' + s.footer3 + '</span>' +
        '</footer>';
    }
  }

  return {
    render: render,
    setTheme: setTheme,
    getTheme: getTheme,
    getLang: getLang,
    setLang: setLang,
    switchLang: switchLang
  };
})();
