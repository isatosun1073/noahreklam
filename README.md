# noahreklam.com

Statik site (GitHub Pages + Cloudflare).

## Yeni blog yazısı
1. `icerik/blog/` içine `yazi-adi.md` ekle. Üst künye:
   ```
   ---
   title: Başlık
   slug: url-adi
   date: 2026-11-09
   category: Reklam Yönetimi
   excerpt: Kartta görünen kısa özet.
   description: Google'da görünecek açıklama (150-160 karakter).
   keywords: anahtar, kelimeler
   ---
   Markdown metin…
   ```
2. `python3 tools/build.py` (gerekirse `pip install markdown`)
3. commit + push. Blog listesi, kategori sayfaları, kapak görseli, RSS, sitemap ve ana sayfadaki son yazılar otomatik güncellenir.

## Özel sayfalar
`icerik/sayfalar/*.html` — ilk satırda `<!--META {...} -->` künyesi. `<details data-faq>` blokları otomatik FAQ şemasına dönüşür.
