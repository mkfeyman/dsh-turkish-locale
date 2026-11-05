# dsh-turkish-locale v1.1.0 — 0.2.2-rc.1 kapsamı

**Tarih:** 2026-11-05 · **Hedef:** DSH `0.2.2-rc.1` (commit `c59d10a`)

## Ne değişti

- **Tam kapsam güncellendi:** 64 → **73 ad alanı**, 2.910 → **3.838 dizgi**;
  `0.2.2-rc.1` ile eklenen **981 yeni dizgi** Türkçeye çevrildi (%100 kapsam
  yeniden sağlandı).
- **10 yeni ad alanı çevrildi:** `forgePanel` (253), `liveshare` (225),
  `stats` (177), `creationRecommendations` (55), `pluginRecommendations` (25),
  `actionCards` (14), `fileActions` (12), `contextMenu` (1), `fileDrag` (1),
  `messageQuotes` (1).
- **60 değişen kaynak metin** gözden geçirildi: 40'ının Türkçesi yeni metne göre
  güncellendi (ör. "hatırlatıcı" → "otomasyon görevi" geçişi, plugin index
  yeniden adlandırması, model listesi yenileme metinleri), 20'si anlam
  değişmediği için korundu.
- **Kaldırılan 52 dizgi ve 1 ad alanı** (`deepseek-model-label-1017`) paketten
  temizlendi.
- İki eski etiket düzeltildi: `command/token.feedback` → "Geri bildirim",
  `command/token.permission` → "İzin".

## Doğrulama

- Yer tutucu denetimi: 3.838/3.838 anahtar kaynakla eşleşiyor, placeholder
  ihlali yok; İngilizce işlev sözcüğü kalıntısı 0.
- Canlı test (DSH 0.2.2-rc.1): paket boot graph'ta yükleniyor, dil seçicide
  8 yerleşik dil + Türkçe, round-trip geçiş ve `locale.preference: tr` kalıcılığı
  doğrulandı; yeni metinler arayüzde görünüyor (ör. "Model sağlayıcısı ekle").
- Kurulum/kullanım değişmedi; `engines.dsh` aralığı korundu
  (`>=0.2.1-rc.3 <0.3.0`).

## Dosyalar

- `dsh-turkish-locale-1.1.0.tgz` — npm tarzı paket (`package/` kökü)
- `SHA256SUMS.txt` — 1.0.0 ve 1.1.0 özetleri
