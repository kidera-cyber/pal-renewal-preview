import re,io
import sys
# 既定は最新の取り込み元。別の WP プレビュー保存 HTML を使う場合は第1引数で渡す。
SRC=sys.argv[1] if len(sys.argv)>1 else '/Users/2ka3kidera/Downloads/FDE導入事例｜無線DASで仕分け・出荷工程を改善.html'
# 出力先も第2引数で渡せる（省略時は従来どおり FDE 導入事例）
DST=sys.argv[2] if len(sys.argv)>2 else '/Users/2ka3kidera/Desktop/pal-renewal-preview/pages/case-fde-food-logistics.html'
import os
if not os.path.exists(SRC):
    sys.exit('取り込み元HTMLが見つかりません: %s\n'
             '使い方: python3 -I tools/sanitize-wp-preview.py <保存したWPプレビューHTML> <出力先HTML>' % SRC)
orig=io.open(SRC,encoding='utf-8').read()
s=orig

# 出典の post_type / 投稿ID は、元HTMLの canonical から読み取る（手書きしない）
m=re.search(r'<link rel="canonical" href="[^"]*post_type=([a-z_]+)[^"]*?p=(\d+)', orig)
SRC_TYPE, SRC_ID = (m.group(1), m.group(2)) if m else ('(不明)','(不明)')
log=[]
warn=[]
def cut(label,pat,count=None,repl=''):
    global s
    n=len(re.findall(pat,s))
    # 取り込み元（post_type / プラグイン構成）により出現数は変わる。
    # 想定と違っても止めず、完了報告に ※要確認 として出す。
    if count is not None and n!=count:
        warn.append('%s: 想定%d件 / 実際%d件'%(label,count,n))
    s=re.sub(pat,lambda _:repl,s)
    log.append((label,n))

cut('GA4 gtag',            r'<!-- Google tag \(gtag\.js\) -->\n<script async src="https://www\.googletagmanager\.com[\s\S]*?</script>\n<script>\n[\s\S]*?</script>\n',1)
cut('GTM head',            r'<!-- Google Tag Manager -->[\s\S]*?<!-- End Google Tag Manager -->',1)
cut('GTM noscript iframe', r'<noscript><iframe src="https://www\.googletagmanager\.com/ns\.html[\s\S]*?</noscript>',1)
cut('Microsoft Clarity',   r'<script type="text/javascript">\(function\(c,l,a,r,i,t,y\)[\s\S]*?</script>',1)
cut('reCAPTCHA script',    r'<script[^>]*recaptcha[^>]*></script>\n?',2)
cut('reCAPTCHA inline',    r'<script id="google-recaptcha-js-after"[\s\S]*?</script>\n?')
cut('wpcf7 recaptcha js',  r'<script[^>]*wpcf7-recaptcha[^>]*></script>\n?')
cut('CF7 recaptcha inline', r'<script id="wpcf7-recaptcha-js-before">[\s\S]*?</script>',1)
cut('管理バー CSS',        r"<link rel='stylesheet' id='admin-bar-css'[^>]*>\n?",1)
cut('管理バー inline CSS', r'<style id="admin-bar-inline-css">[\s\S]*?</style>\n?',1)
cut('管理バー JS',         r'<script id="admin-bar-js"[^>]*></script>\n?',1)
cut('管理バー DOM',        r'<div id="wpadminbar"[\s\S]*?\n\t*</div>\n',1)
cut('WPプレビューJS',      r'<script>\n\t\( function\(\) \{[\s\S]*?sourceURL=wp_post_preview_js\t\n</script>\n?',1)
# AIOSEO の管理画面用スクリプト（WP管理者ログイン時のみ機能する SEO 編集UI。
# 中身は翻訳辞書で、全体の81%・約506KBを占める。共有ページには不要）
cut('AIOSEO 管理UI inline', r'<script id="aioseo/js/src/vue/standalone/[^"]*-js-extra">[\s\S]*?</script>')
cut('AIOSEO 管理UI JS',     r'<script type="module" id="aioseo/[^"]*"[^>]*></script>\n?',2)
cut('canonical',           r'<link rel="canonical"[^>]*>\n?',1)
cut('og:url',              r'\s*<meta property="og:url"[^>]*>')
cut('robots→noindex',      r'<meta name="robots"[^>]*>',1,
    '<meta name="robots" content="noindex,nofollow,noarchive,nosnippet">')

# 本番のWebフォント(woff2)は Access-Control-Allow-Origin が www.pal-style.co.jp 固定で、
# 他ホストからはCORSで弾かれる。同名フォントを Google Fonts から補って見た目を揃える。
fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Lato:wght@400;700;900&family=Noto+Sans+JP:wght@400;500;600;700;900&display=swap">\n')
old_css = '<link rel="stylesheet" href="https://www.pal-style.co.jp/wp-content/themes/PCL/style.css">\n'
if s.count(old_css)==1:
    s = s.replace(old_css, old_css + fonts, 1)
    log.append(('Google Fonts 補完',1))
else:
    warn.append('テーマCSS(style.css)が1件見つからず、Google Fonts を補完できませんでした')

n=len(re.findall(r'(?:src|href)="(/[a-z][^"]*)"',s))
s=re.sub(r'(src|href)="(/[a-z][^"]*)"', lambda m:'%s="https://www.pal-style.co.jp%s"'%(m.group(1),m.group(2)), s)
log.append(('相対パス→絶対URL',n))

s=s.replace('<!DOCTYPE html>','''<!DOCTYPE html>
<!-- ============================================================
     社内共有用プレビュー（WP-SHARE v3）
     出典：www.pal-style.co.jp の WordPress 下書き（post_type=%(t)s / p=%(i)s）を
           ブラウザ保存したもの。本番サイトには未公開。
     公開前に外したもの
       GA4(G-J9HX086VMV) / GTM(GTM-WCR7XHZW) / Microsoft Clarity / reCAPTCHA
         … GitHub Pages から発火して本番の計測データを汚さないため
       WordPress 管理バー・プレビュー用スクリプト
       canonical / og:url（本番の未公開URLを指していたため）
     加えたもの
       robots: noindex,nofollow,noarchive,nosnippet
       サイト内相対リンクの絶対URL化
     本文・見出し・数値・図版は一切変更していない。
     CSS・JS・画像は www.pal-style.co.jp を参照しているため、
     本番側で差し替え・削除されると、この共有ページの表示も変わる。
     ============================================================ -->''' % {'t':SRC_TYPE,'i':SRC_ID},1)
io.open(DST,'w',encoding='utf-8').write(s)
for k,n in log: print('  %-22s %d'%(k,n))
if warn:
    print('\n※要確認')
    for w in warn: print('  - '+w)
print('\n出力: %s\nサイズ: %d → %d bytes'%(DST,len(orig.encode()),len(s.encode())))
