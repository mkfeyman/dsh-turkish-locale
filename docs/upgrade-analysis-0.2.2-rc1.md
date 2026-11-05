# DSH 0.2.2-rc.1 güncellemesi — Türkçe eklenti analiz ve hata ayıklama raporu

**Tarih:** 2026-11-05 · **Ölçülen sürüm:** `0.2.2-rc.1` (commit `c59d10a`, nightly
kanalı) · **GUI:** `http://127.0.0.1:61914`

---

## 1. Güncelleme tespiti

| Öğe | Değer |
|---|---|
| Önceki kurulu sürüm | 0.2.1-rc.3 (commit `be72761`) |
| Yeni kurulu sürüm | **0.2.2-rc.1** (commit `c59d10a`) |
| Kanal | `nightly` (app-update.yml) |
| Boot graph `release` | `{"version":"0.2.2-rc.1","commit":"c59d10a"}` |
| GUI portu | 61914 (uygulama güncelleme sonrası yeniden başlatıldı) |

## 2. Eklenti sağlık kontrolü (canlı)

| Kontrol | Sonuç |
|---|---|
| Boot graph'ta `dsh-turkish-locale` satırı | ✓ mevcut; `inject: ["@deepseek-ai/dsh-client-locale"]`, rev `99640a40d87e`, hata işareti yok |
| Paket bundle'ı `/plugins` üzerinden servis ediliyor | ✓ |
| Dil seçici | ✓ **9 dil**: 中文, English, 日本語, Español, Français, Deutsch, Русский, Português + **Türkçe** (0.2.2'nin 8 yerleşik dili + bizim paket) |
| Aktif dil | ✓ `lang=tr`, arayüz Türkçe |
| Dil değiştirme round-trip (Türkçe → English → Türkçe) | ✓ çalışıyor |
| Kalıcılık | ✓ `cordis.patch.yml` → `locale.preference: tr` |
| Plugins → Yüklü | ✓ "Türkçe dil paketi" Türkçe açıklamayla listeleniyor; `Sorun` durumu yok |
| Çökme/console hatası | Görsel/DOM denetiminde yok (UI tam etkileşimli) |

**Sonuç: güncelleme eklentiyi kırmadı.** Hiçbir kod değişikliği gerekmiyor.

## 3. Locale API uyumluluğu (0.2.1-rc.3 → 0.2.2-rc.1)

Kurulu `dsh-client-locale@0.2.2-rc.1` istemci paketi incelendi
(`contrib/locale-analysis-022rc1/`):

| API | Durum |
|---|---|
| `addLanguage({id,label,fallback})` | Değişmedi — tek fallback, `en`'de biten zincir |
| `register(ns, locale, dict)` (per-locale) | Değişmedi — paketimizin kullandığı biçim |
| `register(ns, {zh,en,...})` (typed) | 0.2.2'de "baseline zh/en zorunlu + ek diller opsiyonel" olarak genişledi; paketimiz etkilenmiyor |
| `resolveText`, `fallbackChain`, `translate` | Aynı (zincir dil tanımlı; sıralı tercih hâlâ yok) |
| Snapshot `{active, locales, revision}` | Aynı |
| `LOCALE_IDS` tabanı | `["zh","en"]` — değişmedi; 8 yerleşik sözlük `apply()` içinde `addLanguage`+`register` ile kaydediliyor |
| `detectBrowserLocale` | Hâlâ ilk eşleşme (sıralı liste hâlâ öneri durumunda) |
| `engines.dsh` aralığımız (`>=0.2.1-rc.3 <0.3.0`) | ✓ 0.2.2-rc.1'i kapsıyor |

## 4. Kapsam deltası (ölçüldü)

Sözlükler yeni sürümden yeniden çıkarıldı (`locales/source-0.2.2-rc1.json`,
`locales/delta-0.2.2-rc1.json`):

| Metrik | rc.3 | 0.2.2-rc.1 | Delta |
|---|---|---|---|
| Ad alanı | 64 | **73** | +10, −1 |
| İngilizce anahtar | 2.910 | **3.838** | **+981, −52** |
| Değişen İngilizce değer | — | — | **60** |
| Türkçe eksik | 0 | — | **981 eksik** |

Yeni ad alanları: `forgePanel` 253, `liveshare` 225, `stats` 177,
`creationRecommendations` 55, `pluginRecommendations` 25, `actionCards` 14,
`fileActions` 12, `contextMenu` 1, `fileDrag` 1, `messageQuotes` 1; ayrıca mevcut
ad alanlarına 217 anahtar eklendi (en büyükler: `pluginManager` +72,
`schedule.manager` +70). Kaldırılan ad alanı: `deepseek-model-label-1017`.
`fixtures/version-coverage.json` ölçülen değerlerle güncellendi.

**Görsel doğrulama:** güncellenmiş uygulamada yeni 0.2.2 panelleri
(forge/stats/liveshare vb.) çevrilmemiş olduğundan İngilizce görünecek; çekirdek
arayüz Türkçe kalıyor. Mevcut çevirilerin 60'ının kaynak metni değişmiş
(anlam kayması riski düşük ama incelenmeli).

## 5. Hata ayıklama bulguları

1. **Eklentide hata yok.** Çalışma zamanı uyumlu; round-trip ve kalıcılık doğrulandı.
2. **Çıkarma araç zincirimizde iki gerçek hata bulundu ve düzeltildi** (`tools/extract_dicts.js`):
   - Yeni büyük paketlerde OOM/çökme (exit 134): tanım araması O(anahtar × dosya)
     ve dev nesne özyinelemesi → tek geçişli `buildDefs()` indeksi + boyut/şekil
     filtresi + `trimStart` düzeltmesi (`[` dizileri dahil). Sonuç: **73/3.838/0
     diagnostics**, ~sn hız.
3. **Yanıltıcı durum yok:** Plugins sayfasındaki `Güncelleme var` işaretleri Codex/
   Claude subagent satırlarına ait (uygulamanın kendi kataloğu); paketimize ait değil.
4. **Paket meta verisi doğru çözülüyor:** "Türkçe dil paketi" satırı `tr` diliyle
   gösteriliyor (manifest `locale/tr.json`).

## 6. Öneriler

| Öneri | Açıklama |
|---|---|
| 981 yeni dizgiyi çevir | Paketi 0.2.2-rc.1 kaynağına göre güncelle (paralel çeviri, 4-5 parça) |
| 60 değişen `en` değerini gözden geçir | Anlam değişmişse Türkçe çevirileri düzelt |
| Paketi **1.1.0** olarak yayınla | `engines.dsh` aralığını koru, market indeksine yeni commit'i sabitle |
| Fixture'ı rc.1 tabanına taşı | `fixtures/version-coverage.json` zaten güncel; `tr-partial` yeni ad alanlarını da kısmi içermeli |
| Sıralı tercih patch'i | `0002` zaten 0.2.2-alpha.2 tabanlı; rc.1 kaynağı ile bir kez daha karşılaştırılıp gerekirse rebase edilmeli |

## 7. Kanıtlar

- [`screenshots/upgrade-settings.png`](../screenshots/upgrade-settings.png) — Ayarlar, 9 dilli seçici, Türkçe
- [`screenshots/upgrade-plugins.png`](../screenshots/upgrade-plugins.png) — Yüklü eklentiler, Türkçe paket satırı
- [`screenshots/roundtrip.png`](../screenshots/roundtrip.png) — dil değiştirme testi
- [`locales/delta-0.2.2-rc1.json`](../locales/delta-0.2.2-rc1.json) — tam delta (anahtar listeleri dahil)
- [`locales/source-0.2.2-rc1.json`](../locales/source-0.2.2-rc1.json) — yeni kaynak sözlükler
