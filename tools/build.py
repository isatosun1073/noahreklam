#!/usr/bin/env python3
"""Noah Reklam — statik sayfa üretici.

Kullanım:  python3 tools/build.py
Girdi:     icerik/blog/*.md            (blog yazıları, üstte --- ile ayrılmış künye)
           icerik/sayfalar/*.html      (özel sayfalar, ilk satır <!--META {...json...}-->)
Çıktı:     blog/…, <sayfa>/index.html, sitemap.xml, ana sayfadaki son yazılar listesi

Yeni yazı: icerik/blog/ içine bir .md dosyası ekle → bu script'i çalıştır → commit + push.
"""
import json, math, random, re, html, datetime as dt, shutil
from pathlib import Path

try:
    import markdown
except ImportError:  # pip install markdown --break-system-packages
    raise SystemExit("markdown paketi gerekli: pip install markdown")

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://noahreklam.com"
WA = "905466328339"
PER_PAGE = 12
AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
TODAY = dt.date.today().isoformat()
AC = ' aria-current="page"'

esc = lambda s: html.escape(str(s), quote=True)
TR = str.maketrans({"ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g", "ı": "i", "İ": "i", "ö": "o", "Ö": "o", "ş": "s", "Ş": "s", "ü": "u", "Ü": "u", "â": "a", "î": "i", "û": "u"})


def slugify(s, sep="-"):
    s = str(s).translate(TR).lower()
    s = re.sub(r"[^a-z0-9]+", sep, s).strip(sep)
    return s or "bolum"


def tr_date(iso):
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {AYLAR[d.month - 1]} {d.year}"


WORDMARK = '<svg viewBox="-0.02 -0.02 8.09 2.04" role="img" aria-label="NOAH"><path fill="currentColor" fill-rule="evenodd" d="M0 2h.36V.66L1.24 2h.36V0h-.36v1.34L.36 0H0Z M1.95 1a1 1 0 1 0 2 0a1 1 0 1 0-2 0Z M2.21 1a.74.74 0 1 0 1.48 0a.74.74 0 1 0-1.48 0Z M4.3 2h.4l.16-.5h.68l.16.5h.4L5.38 0h-.36Z M4.99 1.18h.42L5.2.55Z M6.45 2h.36v-.84h.88V2h.36V0h-.36v.84h-.88V0h-.36Z"/><path d="M2.45 1.02A.5.45 0 0 0 3.45 1.02 M2.37 1.02l.58-.1.58.1 M2.95.92v.55 M2.61.96V.62 M3.29.96V.62 M2.53.62h.84" fill="none" stroke="currentColor" stroke-width=".055" stroke-linecap="round" stroke-linejoin="round"/></svg>'
WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.6.3-.2.2-.8.8-.8 2s.8 2.3.9 2.5c.1.2 1.6 2.5 4 3.5 1.5.6 2.1.7 2.8.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>'

NAV_ITEMS = [
    ("/#ambar", "Hizmetler", None),
    ("/reklam-yonetimi/", "Reklam Yönetimi", "reklam"),
    ("/#biletler", "Paketler", None),
    ("/blog/", "Blog", "blog"),
    ("/#kaptan", "Hakkımızda", None),
]


def layout(*, title, desc, path, body, current=None, schema=(), og_type="website", og_image=None, extra_head="", body_class="", progress=False):
    url = SITE + path
    og_image = og_image or f"{SITE}/assets/og.jpg"
    nav = "".join(f'<li><a href="{h}"{AC if c and c == current else ""}>{esc(t)}</a></li>' for h, t, c in NAV_ITEMS)
    sheet = "".join(f'<li><a href="{h}"><span>{i:02d}</span>{esc(t)}</a></li>' for i, (h, t, c) in enumerate(NAV_ITEMS + [("/#kara", "İletişim", None)], 1))
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#06080a">
<meta property="og:type" content="{og_type}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="Noah Reklam Ajansı">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{og_image}"><meta property="og:locale" content="tr_TR">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/noah-boat.png">
<link rel="alternate" type="application/rss+xml" title="Noah Seyir Defteri" href="/blog/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/sayfa.css?v={TODAY}">
{ld}{extra_head}
</head>
<body class="{body_class}">
{'<div class="progress" id="progress" aria-hidden="true"></div>' if progress else ''}
<header class="nav mono">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Noah Reklam Ajansı — ana sayfa">{WORDMARK}<span class="tag">Reklam Ajansı · İstanbul</span></a>
    <ul>{nav}</ul>
    <a class="nav-cta" href="https://wa.me/{WA}?text={quote('Merhaba, Noah Reklam Ajansı ile çalışmak istiyorum.')}" target="_blank" rel="noopener" data-wa>Teklif al →</a>
    <button class="burger mono" id="burger" aria-expanded="false" aria-controls="sheet">Menü</button>
  </div>
  <nav class="sheet" id="sheet" aria-label="Menü"><div class="wrap"><ol>{sheet}</ol></div></nav>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="wrap">
    <div class="f-grid">
      <div><p class="f-big">Rotayı<br>birlikte çizelim.</p><a class="btn red" href="https://wa.me/{WA}?text={quote('Merhaba, Noah Reklam Ajansı ile çalışmak istiyorum.')}" target="_blank" rel="noopener" data-wa>WhatsApp'tan yaz <span class="arr">→</span></a></div>
      <div><h4 class="mono">Hizmetler</h4><ul><li><a href="/reklam-yonetimi/">Reklam yönetimi</a></li><li><a href="/reklam-yonetimi/#meta">Meta reklamları</a></li><li><a href="/reklam-yonetimi/#instagram">Instagram reklamları</a></li><li><a href="/reklam-yonetimi/#tiktok">TikTok reklamları</a></li><li><a href="/reklam-yonetimi/#google">Google Ads</a></li><li><a href="/#ambar">Tüm hizmetler</a></li></ul></div>
      <div><h4 class="mono">Ajans</h4><ul><li><a href="/#kaptan">İsa Tosun</a></li><li><a href="/#biletler">Sosyal medya paketleri</a></li><li><a href="/blog/">Blog</a></li><li><a href="/blog/feed.xml">RSS</a></li></ul></div>
      <div><h4 class="mono">İletişim</h4><ul><li><a href="tel:+905466328339">0546 632 83 39</a></li><li><a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a></li><li>İstanbul</li></ul></div>
    </div>
    <div class="f-row mono"><span>© {dt.date.today().year} Noah Reklam Ajansı · İstanbul</span><span>Kaptan: İsa Tosun</span><a href="/">noahreklam.com</a></div>
  </div>
</footer>
<a class="wa" href="https://wa.me/{WA}?text={quote('Merhaba, Noah Reklam Ajansı ile çalışmak istiyorum.')}" target="_blank" rel="noopener" aria-label="WhatsApp ile yaz" data-wa>{WA_ICON}</a>
<script src="/assets/sayfa.js?v={TODAY}" defer></script>
</body>
</html>
"""


def quote(s):
    from urllib.parse import quote as q
    return q(s, safe="")


# ---------- kapak görselleri (her yazıya özgü, slug'dan tohumlanmış deniz çizgileri) ----------
def cover_svg(slug, title=""):
    rnd = random.Random(slug)
    W, H = 1600, 900
    hue_red = "#e23b2b"
    sun_x, sun_y, sun_r = rnd.uniform(.15, .85) * W, rnd.uniform(.18, .42) * H, rnd.uniform(60, 150)
    horizon = rnd.uniform(.5, .62) * H
    lines = []
    n = rnd.randint(16, 26)
    red_i = rnd.randrange(3, n)
    for i in range(n):
        y0 = horizon + (i / n) ** 1.6 * (H - horizon + 60)
        amp = 4 + (i / n) * rnd.uniform(18, 46)
        f1, f2 = rnd.uniform(.002, .006), rnd.uniform(.007, .015)
        ph = rnd.uniform(0, 6.28)
        pts = []
        for x in range(0, W + 41, 40):
            y = y0 + math.sin(x * f1 + ph) * amp + math.sin(x * f2 + ph * 2) * amp * .35
            pts.append(f"{x},{y:.1f}")
        op = .18 + (i / n) * .55
        col = hue_red if i == red_i else f"rgba(237,232,223,{op:.2f})"
        sw = 3 if i == red_i else 1.4
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
    rays = "".join(f'<line x1="{sun_x:.0f}" y1="{sun_y:.0f}" x2="{sun_x + math.cos(a) * sun_r * 2.6:.0f}" y2="{sun_y + math.sin(a) * sun_r * 2.6:.0f}" stroke="rgba(237,232,223,.08)" stroke-width="1"/>' for a in [k * math.pi / 12 for k in range(24)])
    ark_x = rnd.uniform(.2, .8) * W
    ark = f'<g transform="translate({ark_x:.0f},{horizon - 6:.0f})" fill="#06080a" stroke="rgba(237,232,223,.55)" stroke-width="1.5"><path d="M-70 0 L70 0 L52 22 L-52 22 Z"/><rect x="-30" y="-18" width="60" height="18"/><path d="M-30 -18 L0 -30 L30 -18" fill="none"/></g>'
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{horizon:.0f}" stroke="rgba(237,232,223,.04)"/>' for x in range(0, W, 100))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{esc(title)}">
<rect width="{W}" height="{H}" fill="#06080a"/>{grid}{rays}
<circle cx="{sun_x:.0f}" cy="{sun_y:.0f}" r="{sun_r:.0f}" fill="none" stroke="{hue_red}" stroke-width="2"/>
<circle cx="{sun_x:.0f}" cy="{sun_y:.0f}" r="{sun_r * .62:.0f}" fill="rgba(226,59,43,.12)"/>
<line x1="0" y1="{horizon:.0f}" x2="{W}" y2="{horizon:.0f}" stroke="rgba(237,232,223,.35)"/>
{ark}{"".join(lines)}
</svg>'''


# ---------- blog ----------
def parse_md(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
    if not m:
        raise SystemExit(f"Künye bulunamadı: {path}")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.strip().startswith("#"):
            k, v = line.split(":", 1)
            v = v.strip()
            if len(v) > 1 and v[0] == v[-1] == '"' and v.count('"') == 2:
                v = v[1:-1]
            meta[k.strip()] = v
    body = m.group(2)
    meta.setdefault("slug", path.stem)
    meta["slug"] = slugify(meta["slug"])
    for req in ("title", "date", "category", "excerpt"):
        if req not in meta:
            raise SystemExit(f"{path.name}: '{req}' eksik")
    md = markdown.Markdown(extensions=["extra", "sane_lists", "toc"], extension_configs={"toc": {"slugify": lambda v, s: slugify(v)}})
    meta["html"] = md.convert(body)
    meta["toc"] = [(t["id"], t["name"]) for t in md.toc_tokens]
    words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", meta["html"])))
    meta["minutes"] = int(meta.get("minutes") or max(2, math.ceil(words / 200)))
    meta["words"] = words
    meta["cat_slug"] = slugify(meta["category"])
    meta["description"] = meta.get("description") or meta["excerpt"]
    meta["updated"] = meta.get("updated") or meta["date"]
    meta["feature"] = meta.get("feature", "").lower() in ("evet", "true", "1", "yes")
    meta["url"] = f"/blog/{meta['slug']}/"
    return meta


def card(p, big=False, h="h2"):
    return f'''<a class="card{' big' if big else ''}" href="{p['url']}">
  <div class="cv"><img src="{p['url']}kapak.svg" alt="" loading="lazy" width="1600" height="900"></div>
  <div class="tx"><div class="meta mono"><b>{esc(p['category'])}</b><span>{tr_date(p['date'])} · {p['minutes']} dk</span></div>
  <{h}>{esc(p['title'])}</{h}><p>{esc(p['excerpt'])}</p><span class="rd mono">Oku <i></i></span></div>
</a>'''


def cats_bar(cats, current=None):
    items = [f'<li><a href="/blog/"{AC if current is None else ""}>Tümü</a></li>']
    for slug, (name, n) in cats.items():
        items.append(f'<li><a href="/blog/kategori/{slug}/"{AC if current == slug else ""}>{esc(name)} <span style="opacity:.55">{n}</span></a></li>')
    return f'''<div class="b-tools"><div class="wrap"><ul class="cats" aria-label="Kategoriler">{"".join(items)}</ul>
<label class="search"><span class="mono" style="position:absolute;left:-9999px">Blogda ara</span><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="5.5" fill="none" stroke="currentColor"/><path d="M11 11l4 4" stroke="currentColor"/></svg><input type="search" id="q" placeholder="Yazılarda ara…" autocomplete="off"></label></div></div>'''


def pager(base, page, pages):
    if pages <= 1:
        return '<div class="pager"></div>'
    href = lambda n: base if n == 1 else f"{base}sayfa/{n}/"
    nums = "".join(f'<span aria-current="page">{n}</span>' if n == page else f'<a href="{href(n)}">{n}</a>' for n in range(1, pages + 1))
    prev = f'<a class="btn ghost" href="{href(page - 1)}">← Önceki</a>' if page > 1 else "<span></span>"
    nxt = f'<a class="btn ghost" href="{href(page + 1)}">Sonraki →</a>' if page < pages else "<span></span>"
    return f'<nav class="pager" aria-label="Sayfalar">{prev}<div class="pg">{nums}</div>{nxt}</nav>'


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items, 1)]}


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def build_blog():
    posts = sorted((parse_md(p) for p in (ROOT / "icerik/blog").glob("*.md") if not p.name.startswith("_")), key=lambda p: (p["date"], p["feature"], p["slug"]), reverse=True)
    slugs = [p["slug"] for p in posts]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("Aynı slug iki kez kullanılmış")
    out = ROOT / "blog"
    if out.exists():
        shutil.rmtree(out)
    cats = {}
    for p in posts:
        name, n = cats.get(p["cat_slug"], (p["category"], 0))
        cats[p["cat_slug"]] = (name, n + 1)
    cats = dict(sorted(cats.items(), key=lambda kv: -kv[1][1]))

    # tek tek yazılar
    for p in posts:
        same = [q for q in posts if q is not p and q["cat_slug"] == p["cat_slug"]]
        other = [q for q in posts if q is not p and q not in same]
        rel = (same + other)[:3]
        toc = ""
        if len(p["toc"]) >= 3:
            toc = '<nav class="toc" aria-label="İçindekiler"><details><summary class="mono">İçindekiler · ' + str(len(p["toc"])) + ' başlık</summary><ol>' + "".join(f'<li><a href="#{i}">{esc(n)}</a></li>' for i, n in p["toc"]) + "</ol></details></nav>"
        share_url = SITE + p["url"]
        more = ('<section class="more"><div class="wrap"><div class="sec-head"><p class="eyebrow mono"><span>Defterden <b>diğer kayıtlar</b></span></p></div><div class="related-posts">' + "".join(card(q, h="h3") for q in rel) + '</div></div></section>') if rel else ""
        body = f'''<article>
<header class="post-hero"><div class="wrap">
  <ol class="crumbs mono" aria-label="Konum"><li><a href="/">Ana sayfa</a></li><li><a href="/blog/">Blog</a></li><li><a href="/blog/kategori/{p['cat_slug']}/">{esc(p['category'])}</a></li></ol>
  <h1>{esc(p['title'])}</h1>
  <div class="post-meta mono"><span class="au"><img src="/assets/isa.webp" alt="İsa Tosun" width="34" height="34">İsa Tosun</span><time datetime="{p['date']}">{tr_date(p['date'])}</time><span>{p['minutes']} dk okuma</span><a href="/blog/kategori/{p['cat_slug']}/" style="color:var(--signal);text-decoration:none">{esc(p['category'])}</a></div>
</div>
<div class="wrap"><div class="post-cover"><img src="kapak.svg" alt="" width="1600" height="900" style="width:100%;height:100%;object-fit:cover"></div></div>
</header>
<div class="wrap">{toc}<div class="prose">{p['html']}</div>
<div class="author"><img src="/assets/isa.webp" alt="İsa Tosun" width="72" height="72" loading="lazy"><div><span class="mono" style="color:var(--signal)">Yazan</span><br><b>İsa Tosun</b><p>Noah Reklam Ajansı'nın kurucusu. Strateji, tasarım ve dijital pazarlamayı tek bir rotada birleştiriyor.</p></div></div>
<div class="share"><span class="mono">Paylaş</span><a href="https://wa.me/?text={quote(p['title'] + ' ' + share_url)}" target="_blank" rel="noopener">WhatsApp</a><a href="https://www.linkedin.com/sharing/share-offsite/?url={quote(share_url)}" target="_blank" rel="noopener">LinkedIn</a><a href="https://twitter.com/intent/tweet?url={quote(share_url)}&text={quote(p['title'])}" target="_blank" rel="noopener">X</a><button type="button" data-copy="{share_url}">Linki kopyala</button></div>
</div>
</article>
<section class="post-cta dark"><div class="wrap">
  <p class="eyebrow mono"><span>Seyir defterinden <b>sahaya</b></span></p>
  <h2 class="h2"><span class="serif">Okuduğun şeyi markanda deneyelim mi?</span>Rotayı birlikte çizelim.</h2>
  <div style="display:flex;flex-wrap:wrap;gap:12px"><a class="btn red" href="https://wa.me/{WA}?text={quote('Merhaba, blogdaki “' + p['title'] + '” yazısını okudum. Markam için konuşmak istiyorum.')}" target="_blank" rel="noopener" data-wa>WhatsApp'tan yaz <span class="arr">→</span></a><a class="btn ghost" href="/reklam-yonetimi/">Reklam yönetimi</a><a class="btn ghost" href="/#biletler">Paketler</a></div>
</div></section>
{more}'''''
        schema = [
            {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["description"], "datePublished": p["date"], "dateModified": p["updated"],
             "inLanguage": "tr-TR", "mainEntityOfPage": share_url, "url": share_url, "image": f"{SITE}/assets/og.jpg", "wordCount": p["words"], "articleSection": p["category"],
             "keywords": p.get("keywords", ""),
             "author": {"@type": "Person", "name": "İsa Tosun", "url": f"{SITE}/#kaptan", "jobTitle": "Kurucu, Noah Reklam Ajansı"},
             "publisher": {"@type": "Organization", "name": "Noah Reklam Ajansı", "url": SITE + "/", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/noah-boat.png"}}},
            crumbs_ld([("Ana sayfa", "/"), ("Blog", "/blog/"), (p["category"], f"/blog/kategori/{p['cat_slug']}/"), (p["title"], p["url"])]),
        ]
        head = f'<meta property="article:published_time" content="{p["date"]}"><meta property="article:modified_time" content="{p["updated"]}"><meta property="article:section" content="{esc(p["category"])}"><meta name="author" content="İsa Tosun">'
        write(f"blog/{p['slug']}/index.html", layout(title=p.get("seo_title") or f"{p['title']} | Noah Blog", desc=p["description"], path=p["url"], body=body, current="blog", schema=schema, og_type="article", extra_head=head, progress=True))
        write(f"blog/{p['slug']}/kapak.svg", cover_svg(p["slug"], p["title"]))

    # liste sayfaları (tüm + kategori), sayfalı
    def listing(subset, base, title, h1, lede, current_cat, crumbs, desc):
        pages = max(1, math.ceil(len(subset) / PER_PAGE))
        for n in range(1, pages + 1):
            chunk = subset[(n - 1) * PER_PAGE: n * PER_PAGE]
            first_big = n == 1 and current_cat is None
            cards = "".join(card(p, big=(first_big and i == 0)) for i, p in enumerate(chunk))
            path = base if n == 1 else f"{base}sayfa/{n}/"
            t = title if n == 1 else f"{title} — Sayfa {n}"
            body = f'''<section class="b-hero"><div class="wrap"><div style="display:grid;gap:20px">
<ol class="crumbs mono" aria-label="Konum">{"".join(f'<li><a href="{u}">{esc(nm)}</a></li>' for nm, u in crumbs)}</ol>
<h1 class="h1"><span class="serif">Seyir defteri.</span>{h1}</h1></div>
<p class="lede">{lede}</p></div></section>
{cats_bar(cats, current_cat)}
<div class="wrap"><div class="grid" id="grid">{cards or '<p class="empty">Henüz yazı yok.</p>'}</div><p class="empty mono" id="none" hidden>Bu aramayla eşleşen yazı yok.</p>{pager(base, n, pages)}</div>'''
            schema = [{"@context": "https://schema.org", "@type": "Blog" if current_cat is None else "CollectionPage", "name": t, "url": SITE + path, "inLanguage": "tr-TR", "description": desc,
                       "publisher": {"@type": "Organization", "name": "Noah Reklam Ajansı", "url": SITE + "/"},
                       **({"blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": SITE + p["url"], "datePublished": p["date"]} for p in chunk]} if current_cat is None else {})},
                      crumbs_ld(crumbs)]
            write(path.lstrip("/") + "index.html", layout(title=t, desc=desc, path=path, body=body, current="blog", schema=schema))
        return pages

    listing(posts, "/blog/", "Blog | Sosyal Medya, Reklam ve Marka Yazıları — Noah Reklam Ajansı", "Gemiden notlar.",
            "Sosyal medya, Meta, Instagram, TikTok ve Google reklamları, marka kimliği ve içerik stratejisi üzerine sahadan öğrendiklerimiz.", None,
            [("Ana sayfa", "/"), ("Blog", "/blog/")],
            "Noah Reklam Ajansı blogu: sosyal medya yönetimi, Meta ve Instagram reklamları, TikTok, Google Ads, marka kimliği ve içerik stratejisi üzerine rehberler.")
    for cs, (cname, _) in cats.items():
        sub = [p for p in posts if p["cat_slug"] == cs]
        listing(sub, f"/blog/kategori/{cs}/", f"{cname} Yazıları | Noah Blog", esc(cname) + ".",
                f"{esc(cname)} üzerine yazdığımız tüm kayıtlar.", cs,
                [("Ana sayfa", "/"), ("Blog", "/blog/"), (cname, f"/blog/kategori/{cs}/")],
                f"Noah Reklam Ajansı blogunda {cname} kategorisindeki yazılar: rehberler, örnekler ve sahadan notlar.")

    # arama verisi, RSS
    write("blog/posts.json", json.dumps([{"u": p["url"], "t": p["title"], "x": p["excerpt"], "c": p["category"], "d": tr_date(p["date"]), "m": p["minutes"], "k": p.get("keywords", "")} for p in posts], ensure_ascii=False))
    items = "".join(f"<item><title>{esc(p['title'])}</title><link>{SITE}{p['url']}</link><guid>{SITE}{p['url']}</guid><pubDate>{dt.datetime.fromisoformat(p['date']).strftime('%a, %d %b %Y 09:00:00 +0300')}</pubDate><category>{esc(p['category'])}</category><description>{esc(p['excerpt'])}</description></item>" for p in posts[:50])
    write("blog/feed.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Noah Seyir Defteri</title><link>{SITE}/blog/</link><description>Noah Reklam Ajansı blogu</description><language>tr</language>{items}</channel></rss>')
    return posts, cats


# ---------- özel sayfalar ----------
def faq_ld(body):
    qa = re.findall(r"<details data-faq><summary>(.*?)</summary><div class=\"a\">(.*?)</div></details>", body, re.S)
    if not qa:
        return []
    strip = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()
    return [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qa]}]


def build_pages(posts=()):
    pages = []
    for f in sorted((ROOT / "icerik/sayfalar").glob("*.html")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^<!--META\s*(\{.*?\})\s*-->\s*\n(.*)$", raw, re.S)
        meta, body = json.loads(m.group(1)), m.group(2)
        path = meta["path"]
        rel = [p for p in posts if p["cat_slug"] in meta.get("related", [])][:3]
        rel_html = ('<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head"><div style="display:grid;gap:20px"><p class="eyebrow mono"><span>Seyir <b>defterinden</b></span></p><h2 class="h2"><span class="serif">Okumadan geçme.</span>Reklam üzerine yazılar</h2></div><a class="btn ghost" href="/blog/" style="justify-self:start">Tüm yazılar <span class="arr">→</span></a></div><div class="related-posts">' + "".join(card(p, h="h3") for p in rel) + '</div></div></section>') if rel else ""
        body = body.replace("<!--RELATED-->", rel_html)
        meta["schema"] = meta.get("schema", []) + faq_ld(body) + ([crumbs_ld(meta["breadcrumbs"])] if meta.get("breadcrumbs") else [])
        write(path.lstrip("/") + "index.html", layout(title=meta["title"], desc=meta["description"], path=path, body=body, current=meta.get("current"), schema=meta.get("schema", []), body_class=meta.get("body_class", "")))
        pages.append(meta)
    return pages


# ---------- ana sayfadaki son yazılar ----------
def inject_home(posts):
    idx = ROOT / "index.html"
    s = idx.read_text(encoding="utf-8")
    latest = posts[:4]
    data = [{"slug": p["slug"], "date": dt.date.fromisoformat(p["date"]).strftime("%d.%m.%Y"), "min": f"{p['minutes']} dk", "tag": p["category"], "t": p["title"], "x": p["excerpt"], **({"feature": True} if i == 0 else {})} for i, p in enumerate(latest)]
    new = "/*POSTS*/const POSTS=" + json.dumps(data, ensure_ascii=False) + ";/*/POSTS*/"
    s2, n = re.subn(r"/\*POSTS\*/.*?/\*/POSTS\*/", lambda _: new, s, flags=re.S)
    if n != 1:
        raise SystemExit("index.html içinde /*POSTS*/ işareti bulunamadı")
    idx.write_text(s2, encoding="utf-8")


def sitemap(posts, cats, pages):
    urls = [("/", TODAY, "1.0")] + [(p["path"], p.get("updated", TODAY), "0.9") for p in pages] + [("/blog/", posts[0]["date"] if posts else TODAY, "0.8")]
    urls += [(f"/blog/kategori/{c}/", TODAY, "0.5") for c in cats]
    urls += [(p["url"], p["updated"], "0.7") for p in posts]
    body = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>" for u, d, pr in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>\n')


if __name__ == "__main__":
    posts, cats = build_blog()
    pages = build_pages(posts)
    inject_home(posts)
    sitemap(posts, cats, pages)
    print(f"✓ {len(posts)} yazı, {len(cats)} kategori, {len(pages)} özel sayfa üretildi.")
