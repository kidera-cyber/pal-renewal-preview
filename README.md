# pal-renewal-preview

株式会社PAL コーポレートサイト改修 社内レビュー用ポータル。

社内メンバーへは、ポータルのトップ URL 1 本だけを共有します。ポータル内のタブから 4 ページを切り替えて確認できます。

## 目的

以下 4 ページの改修案を、1 つの共有 URL からタブ切替で確認できるようにするための静的ポータル。

- ホーム改修案
- 私たちの役割
- PALの強み
- FDE サービス詳細（新規）

## ファイル構成

```
pal-renewal-preview/
├── index.html               ← ポータル本体（タブ + iframe）
├── pages/
│   ├── home.html            ← ホーム改修案
│   ├── role.html            ← 私たちの役割
│   ├── reason.html          ← PALの強み
│   └── fde.html             ← FDE サービス詳細
├── assets/
│   ├── css/
│   │   ├── portal.css       ← ポータル UI 用
│   │   └── common.css       ← 4 ページ共通の PAL デザイントークン
│   └── js/
│       └── portal.js        ← タブ切替 + URL パラメータ同期
└── README.md
```

## 使い方（社内共有）

ポータル URL を 1 本だけ社内共有してください。

```
https://<GitHubユーザー名>.github.io/pal-renewal-preview/
```

- 上部のタブから 4 ページを切替
- 「新しいタブで開く」で単独ページを別窓表示
- URL パラメータ `?page=home|role|reason|fde` でも初期ページ指定可能
- リロードしても選択中のページは維持

## レビュー用マーキング

各ページに `<body class="review-mode">` が付いており、以下の色分けが表示されます：

| 色 | 意味 | クラス |
|---|---|---|
| 黄 | 今回変更 | `.review-changed` |
| 青 | 新規追加 | `.review-added` |
| 赤 | 要確認 | `.review-check` |
| 黄（点線） | 内容変更予定（未確定） | `.review-pending` |
| 赤枠 バッジ | インライン要確認 | `.review-inline-check` |

**本番化する時**：各ページの `<body class="review-mode">` から `review-mode` を外すだけで、すべてのマーキングが非表示になります（`common.css` 側で `body.review-mode` の子孫セレクタで表示制御しているため）。

## ページ追加時

1. `pages/xxxx.html` を配置
2. `index.html` にタブボタンを追加：
   ```html
   <button class="portal-tab" role="tab" data-page="xxxx"
     aria-selected="false" aria-controls="previewFrame">タブ名</button>
   ```
3. `assets/js/portal.js` の `PAGES` に追加：
   ```js
   xxxx: { file: 'pages/xxxx.html', name: 'タブ名' }
   ```

## GitHub Pages 公開手順

1. GitHub で新規リポジトリ `pal-renewal-preview` を作成（Public、README なし）
2. ローカルから push：
   ```bash
   cd /Users/<USER>/Desktop/pal-renewal-preview
   git init -b main
   git add -A
   git commit -m "Initial commit: 社内レビュー用ポータル"
   git remote add origin https://github.com/<USER>/pal-renewal-preview.git
   git push -u origin main
   ```
3. Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` / Folder: `/ (root)` → Save
4. 数分後、Pages 設定画面に公開 URL が表示されます

## noindex の扱い

- ポータル本体 (`index.html`) + 全 4 ページに `<meta name="robots" content="noindex, nofollow">` + `<meta name="googlebot" content="noindex, nofollow">` を設定済
- 検索エンジンのインデックスには載りません
- ただし **URL を知る人からのアクセスは制限されません**（GitHub Pages 通常版）
- 完全な社内限定は GitHub Enterprise Cloud + Private Pages が必要

## 公開前の注意事項

- 掲載事例・実績数値・DTS 画面イメージ・対応温度帯等の情報は「要確認プレースホルダ」として仮置き中
- レビュー完了後、Pages を非公開化する場合：
  ```bash
  gh api --method DELETE repos/<USER>/pal-renewal-preview/pages
  ```
  または Settings → Pages → Unpublish

## 変更履歴

- v1.0：初版。4 ページ（Home / 役割 / 強み / FDE）を iframe 切替で表示するポータル
