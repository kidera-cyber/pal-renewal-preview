/* ============================================================
   PAL 社内レビュー用ポータル：タブ切替 + URL パラメータ同期
   ============================================================ */
(function () {
  'use strict';

  const PAGES = {
    home:   { file: 'pages/home.html',   name: 'ホーム' },
    role:   { file: 'pages/role.html',   name: '私たちの役割' },
    reason: { file: 'pages/reason.html', name: 'PALの強み' },
    /* fde タブは廃止（FDE 専用ページを削除し、説明は role.html #fde へ統合）
       ?page=fde でアクセスされた場合は DEFAULT_PAGE（home）へフォールバックする */
    service:{ file: 'pages/service.html',name: 'サービス一覧' }
  };
  const DEFAULT_PAGE = 'home';

  /* ===== CACHE-BUST v2：レビュー環境で旧版が表示される事故を根本的に防ぐ。
     GitHub Pages は全ファイルに Cache-Control: max-age=600（10分）を付けるため、
     固定のビルド番号では「portal.js 自身が古いまま」だと番号も古く、無効化されていた。
     そこでプレビュー対象ページは毎回タイムスタンプを付けて必ず最新を取得する。
     本番化時はこのブロックごと削除し、bust を素通しにしてよい ===== */
  const bust = function (f) { return f + '?t=' + Date.now(); };

  /* 最終更新時刻（push のたびに自動更新される） */
  const BUILD_STAMP = '2026-09-10 17:01';

  const frame       = document.getElementById('previewFrame');
  const openLink    = document.getElementById('openPage');
  const currentName = document.getElementById('currentPageName');
  const tabs        = Array.from(document.querySelectorAll('.portal-tab'));

  /* ===== BUILD STAMP v1：最終更新の表示と強制再取得 ===== */
  const stampEl = document.getElementById('buildStamp');
  if (stampEl) stampEl.textContent = BUILD_STAMP;
  const reloadBtn = document.getElementById('forceReload');
  if (reloadBtn) {
    reloadBtn.addEventListener('click', function () {
      const u = new URL(location.href);
      u.searchParams.set('r', Date.now());
      location.replace(u.toString());
    });
  }

  function switchTo(pageKey, opts) {
    opts = opts || {};
    const page = PAGES[pageKey] || PAGES[DEFAULT_PAGE];
    const key  = PAGES[pageKey] ? pageKey : DEFAULT_PAGE;

    // iframe src 切替（同一なら再ロードしない）
    // タイムスタンプ方式のため毎回セットする（常に最新を読み込む）
    frame.setAttribute('src', bust(page.file));
    frame.setAttribute('title', '株式会社PAL コーポレートサイト改修プレビュー ／ ' + page.name);

    // 「新しいタブで開く」リンクを同期
    openLink.setAttribute('href', bust(page.file));

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
