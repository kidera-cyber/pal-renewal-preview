/* ============================================================
   PAL 社内レビュー用ポータル：タブ切替 + URL パラメータ同期
   ============================================================ */
(function () {
  'use strict';

  const PAGES = {
    home:   { file: 'pages/home.html',   name: 'ホーム' },
    role:   { file: 'pages/role.html',   name: '私たちの役割' },
    reason: { file: 'pages/reason.html', name: 'PALの強み' },
    service:{ file: 'pages/service.html',name: 'サービス一覧' }
  };
  const DEFAULT_PAGE = 'home';

  const frame       = document.getElementById('previewFrame');
  const openLink    = document.getElementById('openPage');
  const currentName = document.getElementById('currentPageName');
  const tabs        = Array.from(document.querySelectorAll('.portal-tab'));

  function switchTo(pageKey, opts) {
    opts = opts || {};
    const page = PAGES[pageKey] || PAGES[DEFAULT_PAGE];
    const key  = PAGES[pageKey] ? pageKey : DEFAULT_PAGE;

    // iframe src 切替（同一なら再ロードしない）
    if (frame.getAttribute('src') !== page.file) {
      frame.setAttribute('src', page.file);
    }
    frame.setAttribute('title', '株式会社PAL コーポレートサイト改修プレビュー ／ ' + page.name);

    // 「新しいタブで開く」リンクを同期
    openLink.setAttribute('href', page.file);

    // 現在ページ名
    if (currentName) currentName.textContent = page.name;

    // タブの aria-selected 切替
    tabs.forEach(function (t) {
      const isActive = t.dataset.page === key;
      t.setAttribute('aria-selected', isActive ? 'true' : 'false');
      if (isActive) t.classList.add('is-active');
      else t.classList.remove('is-active');
    });

    // URL パラメータ同期（履歴を汚さないよう replaceState）
    if (!opts.skipUrl) {
      const url = new URL(window.location.href);
      url.searchParams.set('page', key);
      window.history.replaceState({ page: key }, '', url.toString());
    }
    document.title = '株式会社PAL コーポレートサイト改修｜' + page.name + '｜社内確認用';
  }

  // タブクリック
  tabs.forEach(function (t) {
    t.addEventListener('click', function () { switchTo(t.dataset.page); });
    // キーボード操作（← → で切替）
    t.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault();
      const idx = tabs.indexOf(t);
      const next = e.key === 'ArrowRight'
        ? tabs[(idx + 1) % tabs.length]
        : tabs[(idx - 1 + tabs.length) % tabs.length];
      next.focus();
      switchTo(next.dataset.page);
    });
  });

  // 初期表示：URL パラメータ ?page=xxx を尊重
  const initialParam = new URLSearchParams(window.location.search).get('page');
  const initialPage  = PAGES[initialParam] ? initialParam : DEFAULT_PAGE;
  switchTo(initialPage, { skipUrl: !initialParam });

  // ブラウザ戻る/進む対応
  window.addEventListener('popstate', function () {
    const p = new URLSearchParams(window.location.search).get('page');
    switchTo(PAGES[p] ? p : DEFAULT_PAGE, { skipUrl: true });
  });
})();
