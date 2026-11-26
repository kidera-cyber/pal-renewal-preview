# -*- coding: utf-8 -*-
"""
CORE-TIME-LP-SHARE v1
~/Desktop/core-time（本番 /core-time/ のPHPソース一式）を、
GitHub Pages で表示できる静的HTMLへ変換して社内共有用に配置する。

PHPはこの環境に無いため、index.php のテンプレート変数を
functions.php の値で機械的に解決する（echo 16箇所 + if 1箇所のみ）。
本文・見出し・画像・CSS・JSは一切変更しない。
"""
import re, io, os, shutil, sys

SRC = '/Users/2ka3kidera/Desktop/core-time'
DST = '/Users/2ka3kidera/Desktop/pal-renewal-preview/core-time-lp'
PROD_FORM = 'https://www.pal-style.co.jp/core-time/form/'

log = []

# ---- 1. functions.php の値を解決（PHPを実行せず、代入文を読む） ----
fn = io.open(os.path.join(SRC, 'functions.php'), encoding='utf-8').read()
V = {}
def resolve(expr):
    # 'リテラル' と $arr['key'] の連結のみ対応
    out = ''
    for tok in re.findall(r"'((?:[^'\\]|\\.)*)'|\$(\w+)\['(\w+)'\]", expr):
        if tok[0] or tok[0] == '':
            if tok[1] == '' and tok[2] == '':
                out += tok[0].replace("\\'", "'")
                continue
        out += V['%s.%s' % (tok[1], tok[2])]
    return out
for m in re.finditer(r"\$(\w+)\['(\w+)'\]\s*=\s*(.+?);\s*(?:/\*|$|\n)", fn, re.M):
    V['%s.%s' % (m.group(1), m.group(2))] = resolve(m.group(3))
log.append(('functions.php 解決した変数', len(V)))

# ---- 2. index.php を静的化 ----
s = io.open(os.path.join(SRC, 'index.php'), encoding='utf-8').read()
s = s.replace("\n<?php include('functions.php');?>", '', 1)

# if($site['touchicon'] != ''): ... endif;  → touchicon は空なので丸ごと落とす
tic = re.search(r"<\?php if\(\$site\['touchicon'\] != ''\):\?>.*?<\?php endif;\?>", s, re.S)
if tic:
    assert V.get('site.touchicon', '') == '', 'touchicon が空でない。手当てが必要'
    s = s[:tic.start()] + s[tic.end():]
    log.append(('touchicon の if を除去（値が空のため）', 1))

n = 0
def echo(m):
    global n
    n += 1
    return V['%s.%s' % (m.group(1), m.group(2))]
s = re.sub(r"<\?php\s*echo\s*\$(\w+)\['(\w+)'\]\s*;?\s*\?>", echo, s)
log.append(('テンプレート変数の展開', n))
assert '<?php' not in s, 'PHPタグが残っている'
assert '<?=' not in s, '短縮PHPタグが残っている'

# ---- 3. 計測タグ除去（レビュー環境から本番の計測を汚さない） ----
def cut(label, pat, expect=None):
    global s
    c = len(re.findall(pat, s))
    if expect is not None and c != expect:
        log.append(('※要確認 %s' % label, c))
    s = re.sub(pat, '', s)
    log.append((label, c))

cut('GTM head',            r'<!-- Google Tag Manager -->[\s\S]*?<!-- End Google Tag Manager -->\n?', 1)
cut('GTM noscript',        r'<!-- Google Tag Manager \(noscript\) -->[\s\S]*?<!-- End Google Tag Manager \(noscript\) -->\n?', 1)
cut('GTM その他',          r'<noscript><iframe src="https://www\.googletagmanager\.com/ns\.html[\s\S]*?</noscript>\n?')
cut('GTM script',          r'<script[^>]*googletagmanager[^>]*>[\s\S]*?</script>\n?')
cut('Google Analytics',    r'<script[^>]*google-analytics[^>]*>[\s\S]*?</script>\n?')
cut('ga/UA inline',        r"<script[^>]*>[^<]*(?:UA-25847455-14|ga\('create')[\s\S]*?</script>\n?")

# ---- 4. robots: noindex を付与 ----
assert '<meta name="robots"' not in s
s = s.replace('<meta charset="utf-8">',
              '<meta charset="utf-8">\n'
              '<meta name="robots" content="noindex,nofollow,noarchive,nosnippet">', 1)
log.append(('robots: noindex 付与', 1))

# ---- 5. フォームリンクを本番フォームへ（PHP必須でPages上では動かないため） ----
fn_cnt = 0
def formlink(m):
    global fn_cnt
    fn_cnt += 1
    q = m.group(1) or ''
    return 'href="%s%s" target="_blank" rel="noopener noreferrer"' % (PROD_FORM, q)
s = re.sub(r'href="\./form/(\?[^"]*)?"', formlink, s)
log.append(('フォームリンク→本番フォーム（別タブ）', fn_cnt))

# ---- 6. 出典ヘッダ ----
hdr = '''<!DOCTYPE html>
<!-- ============================================================
     社内共有用プレビュー（CORE-TIME-LP-SHARE v1）
     出典：本番 https://www.pal-style.co.jp/core-time/ のソース一式
           （~/Desktop/core-time、全ファイル 2026-01-20 17:22 時点）
     PHPはGitHub Pagesで動かないため、index.php のテンプレート変数を
     functions.php の値で解決し、静的HTMLとして出力している。
     本文・見出し・画像・CSS・JSは一切変更していない。
     公開前に外したもの
       Google Tag Manager(GTM-NMBTTWS) / Google Analytics(UA-25847455-14)
         … レビュー環境から発火して本番の計測データを汚さないため
     加えたもの
       robots: noindex,nofollow,noarchive,nosnippet
       フォームリンク（3箇所）→ 本番フォームを別タブで開く
         … form/ はPHPのメールフォームでPages上では動作しないため
     ============================================================ -->'''
assert s.count('<!doctype html>') == 1
s = s.replace('<!doctype html>', hdr, 1)

# ---- 7. 静的アセットを複製（PHP・Windows生成物・未参照ファイルは除外） ----
if os.path.isdir(DST):
    shutil.rmtree(DST)
skipped = []
for root, dirs, files in os.walk(SRC):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'form']
    for f in files:
        p = os.path.join(root, f)
        rel = os.path.relpath(p, SRC)
        if f.startswith('.') or f.endswith('.php') or f == 'Thumbs.db' or '・' in f:
            skipped.append(rel)
            continue
        d = os.path.join(DST, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(p, d)
io.open(os.path.join(DST, 'index.html'), 'w', encoding='utf-8').write(s)

copied = sum(len(fs) for _, _, fs in os.walk(DST))
print('■ 変換ログ')
for k, v in log: print('  %-34s %s' % (k, v))
print('\n■ 複製')
print('  コピーしたファイル数   %d（index.html を含む）' % copied)
print('  除外したファイル       %d' % len(skipped))
for r in sorted(skipped): print('    - %s' % r)
print('\n出力: %s' % DST)
print('index.html: %d bytes' % len(s.encode()))
