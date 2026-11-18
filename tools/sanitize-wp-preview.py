import re,io
SRC='/Users/2ka3kidera/Downloads/FDE導入事例｜食品製造拠点の物流DX・仕分け改善.html'
DST='/Users/2ka3kidera/Desktop/pal-renewal-preview/pages/case-fde-food-logistics.html'
orig=io.open(SRC,encoding='utf-8').read()
s=orig
log=[]
def cut(label,pat,count=None,repl=''):
    global s
    n=len(re.findall(pat,s))
    if count is not None: assert n==count,'%s: %d != %d'%(label,n,count)
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
assert s.count(old_css)==1
s = s.replace(old_css, old_css + fonts, 1)
log.append(('Google Fonts 補完',1))

n=len(re.findall(r'(?:src|href)="(/[a-z][^"]*)"',s))
s=re.sub(r'(src|href)="(/[a-z][^"]*)"', lambda m:'%s="https://www.pal-style.co.jp%s"'%(m.group(1),m.group(2)), s)
log.append(('相対パス→絶対URL',n))

s=s.replace('<!DOCTYPE html>','''<!DOCTYPE html>
<!-- ============================================================
     社内共有用プレビュー（CASE-SHARE v1）
     出典：www.pal-style.co.jp の WordPress 下書き（post_type=case / p=8474）を
           ブラウザ保存したもの。本番サイトには未公開。
     公開前に外したもの
       GA4(G-J9HX086VMV) / GTM(GTM-WCR7XHZW) / Microsoft Clarity / reCAPTCHA
         … GitHub Pages から発火して本番の計測データを汚さないため
       WordPress 管理バー・プレビュー用スクリプト
       canonical / og:url（本番の未公開URLを指していたため）
     加えたもの
       robots: noindex,nofollow,noarchive,nosnippet
       サイト内相対リンクの絶対URL化（/case/ ほか）
     本文・見出し・数値・図版は一切変更していない。
     CSS・JS・画像は www.pal-style.co.jp を参照しているため、
     本番側で差し替え・削除されると、この共有ページの表示も変わる。
     ============================================================ -->''',1)
io.open(DST,'w',encoding='utf-8').write(s)
for k,n in log: print('  %-22s %d'%(k,n))
print('\n出力: %s\nサイズ: %d → %d bytes'%(DST,len(orig.encode()),len(s.encode())))
