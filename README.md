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

## SEO / GEO (yapay zekâ arama) altyapısı
`tools/build.py` her çalıştığında otomatik üretir:
- **Yazı başına paylaşım görseli** `assets/og/<slug>.jpg` (1200×630; başlık değişince yenilenir)
- **llms.txt / llms-full.txt** — ChatGPT, Perplexity, Claude, Gemini gibi motorlar için ajans özeti ve tüm yazıların tam metni
- **Ana sayfanın statik kopyası** — hizmetler, paketler ve son yazılar HTML'e basılır (JS çalıştırmayan botlar da görür). `index.html` içindeki `<!--S:...-->` işaretlerini silme.
- **JSON-LD varlık grafiği** — Organization (`/#organization`), Person (`/hakkimizda/#isa-tosun`), WebSite, BlogPosting, FAQ, Breadcrumb
- **404.html**, sitemap, RSS
`robots.txt` yapay zekâ botlarına açıkça izin verir. Cloudflare'de "AI botlarını engelle" ayarı kapalı olmalı.
