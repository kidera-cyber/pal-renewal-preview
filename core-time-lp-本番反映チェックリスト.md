# Core Time LP 改修｜本番反映チェックリスト

対象プレビュー: `core-time-lp/`（GitHub Pages）
本番: `https://www.pal-style.co.jp/core-time/`
作成日: 2026-11-26

---

## 0. 前提：本番はWordPressではありません

| 確認項目 | 結果 |
|---|---|
| `/core-time/` がWordPressページとして存在するか | **存在しない**（`wp-json/wp/v2/pages?search=core-time` ヒット0件） |
| HTML内の `wp-content` / `wp-includes` / `aioseo` | **0件** |
| 比較：`/about/`（WordPress配下）の同キーワード | 16行ヒット |
| サーバー | Apache/2.4.65（Amazon Linux） |

`/core-time/` は WordPress とは独立した **PHPテンプレートの静的LP**（`index.php` + `functions.php`）です。
したがって **AIOSEOの管理対象外であり、TruSEOスコアは原理的に測定できません。**
本チェックリストのSEO項目は、AIOSEOの公式評価項目に基づく事前診断です。

---

## 1. 反映前（必須）

- [ ] **`<meta name="robots" content="noindex,nofollow,noarchive,nosnippet">` を削除する**
      ← プレビュー用。これを残すと本番LPが検索結果から消えます。**最重要**
- [ ] `<!-- CORE-TIME-LP-SHARE v1 -->` の出典コメントを削除する
- [ ] Google Tag Manager（`GTM-NMBTTWS`）を復帰させる
- [ ] Google Analytics（`UA-25847455-14`）の扱いを確認する（GTM経由に統合済みなら不要）
- [ ] フォームリンク3箇所を `./form/` に戻す
      （プレビューでは `https://www.pal-style.co.jp/core-time/form/` の別タブ遷移にしている）
- [ ] `index.html` の変更内容を `index.php` に反映する
      ※本番は `index.php`。`functions.php` の `$site['title']` / `$site['description']` /
        `$site['keywords']` も更新が必要

## 2. `functions.php` に反映する値

| 変数 | 新しい値 |
|---|---|
| `$site['title']` | `物流現場の勤怠管理・工数可視化システム｜Core Time` |
| `$site['description']` | `Core Timeは物流現場の勤怠管理システムです。静脈認証の打刻でシフト・工数・売上を一元管理し、勤怠データを稼働の可視化に活用できます。` |
| `$site['keywords']` | `物流 勤怠管理システム,物流現場の勤怠管理,倉庫 勤怠管理,勤怠データ活用,工数管理,静脈認証,Core Time` |

`$og['url']` は現在 `$site['protocol'].$site['domain']` が `https://pal-style.co.jp`（www なし）を生成します。
実際の正規URLは `https://www.pal-style.co.jp/core-time/` です。
`$site['domain']` を `www.pal-style.co.jp` に修正してください。

## 3. 反映後（確認）

- [ ] `https://www.pal-style.co.jp/core-time/` を開き、`robots` が noindex でないこと
- [ ] `<link rel="canonical" href="https://www.pal-style.co.jp/core-time/">` が出力されていること
- [ ] Search Console でURL検査 → インデックス登録をリクエスト
- [ ] リッチリザルトテスト（FAQ / SoftwareApplication / BreadcrumbList）でエラー0件
- [ ] GTMのプレビューモードで計測タグが発火すること
- [ ] 問い合わせCTA・資料ダウンロードCTAの遷移先が `./form/` `./form/?type=1` であること
- [ ] sitemap.xml に `/core-time/` が含まれているか確認
- [ ] 料金・IT導入補助金・Windows10表記が本番HTMLに残っていないこと
- [ ] FAQ「利用環境について」に正式な推奨スペック（Windows 11 / Intel Core i5 第12世代以降
      または AMD Ryzen 5 5000番台以降 / 16GB）が反映されていること

## 4. 本番側の既存不具合（今回は未修正）

- [ ] `/js/jquery.min.js` `/js/jquery.easing.min.js` が404
      → `./js/` への修正を推奨（CDN障害時にページが動作しません）
- [ ] `css/owl.carousel.css` の `../images/top/dot.gif` ほか3点が404（表示影響なし）
- [ ] `body{min-width:1200px}` のため、661〜1199px（タブレット）で横スクロールが発生
- [ ] viewport が `document.write` によるJS出力のため、JS無効時にモバイル表示が崩れる

## 5. 推奨利用環境について（2026-11-27 確定）

正式な推奨利用環境を確認済みです。**プレビュー版には反映済み**（コミット `5c62dba`）。

> Windows端末（OS：Windows 11、CPU：Intel Core i5（第12世代以降）または
> AMD Ryzen 5（5000番台以降）同等以上、メモリ：16GB）が推奨

公式LPへの反映は、**推奨利用環境のみを変更した別パッチ**として
`~/Desktop/CoreTime公式LP_推奨利用環境修正_20261127/` に用意しています（本番反映は未承認）。

## 6. 未確認のまま残している項目

- [ ] `管理業務80％削減`（特徴セクション）の根拠
- [ ] `マスタ管理機能`（削除した料金セクション内にのみ記載されていた機能）の扱い
- [ ] Search Console / GA4 の実データ（検索クエリ・表示回数・CTR・Core Web Vitals）
