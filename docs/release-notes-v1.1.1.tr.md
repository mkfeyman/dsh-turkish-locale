# dsh-turkish-locale v1.1.1 — 0.2.2-rc.2 kapsamı

**Tarih:** 2026-11-13 · **Hedef:** DSH `0.2.2-rc.2` (commit `a6b1b85`)

## Ne değişti

- **Tam kapsam güncellendi:** 73 → **75 ad alanı**, 3.838 → **4.223 dizgi**;
  `0.2.2-rc.2` ile eklenen **430 yeni dizgi** Türkçeye çevrildi (%100 kapsam
  yeniden sağlandı).
- **2 yeni ad alanı:** `cuaPermissions` (66 — bilgisayar kullanımı izin
  yönetimi) ve `account.notifications` (1).
- **Büyüyen ad alanları:** `forgePanel` +174 (değişiklik isteği genel
  bakışları, branch/commit aralıkları, inceleyici durumları), `settings.models`
  +37 (Gemini protokolü, yeniden deneme stratejileri), `sidebarFiles` +32
  (yoksayma dosyaları, arama ipuçları), `settings` +23 ve `settings.webSearch`
  +23 (kanal etiketleri, faturalama/geçersiz kılma, eski anahtar ipucu),
  `agent-team` +18, `chat`/`conversation` +12'şer, `liveshare` +9, `subagent` +7,
  `sidebarTerminal` +5, diğerleri.
- **Kaldırılan 45 dizgi** paketten temizlendi (ör. `agent-team` −13,
  `liveshare` −11, `settings.webSearch` −7).
- **Kaynak metni değişen 2 anahtar düzeltildi** (yer tutucu kayması):
  `pluginManager.updateStepInstalling` (`{source}`) ve
  `settings.webSearch.baseUrlHint` (`{path}`).

## Uyumluluk

- Locale çalışma zamanı API'si değişmedi: `addLanguage`, `register(ns, locale,
  dict)`, `resolveText`, snapshot ve `locale.preference` sözleşmeleri rc.2'de
  aynı. `dsh-client-locale@0.2.2-rc.2` etiketi kaynak olarak yalnızca
  `package.json` (sürüm) farkı taşıyor — sıralı tercih patch taslağı `0003`
  rc.2 için de geçerli.
- **Profil kurulumu düzeltildi:** rc.2'de profil `node_modules` pnpm ile
  yönetiliyor; eski elle kopyalanmış dizin yükleyici tarafından görülmüyordu.
  Paket artık `plugin_manager install_bundle` üzerinden bağlanıyor
  (remove_bundle + install_bundle ile yeniden bağlandı) ve boot graph'ta
  yeniden yerini aldı.

## Doğrulama

- 4 paralel çeviri parçası (430/430 kayıt); yer tutucu denetimi temiz.
- Canlı test (DSH 0.2.2-rc.2): paket boot graph'ta yüklü (`rev 2fe8ccdf`),
  arayüz `lang=tr`, dil seçici çalışıyor.
- `engines.dsh` aralığı korundu (`>=0.2.1-rc.3 <0.3.0`).

## Dosyalar

- `dsh-turkish-locale-1.1.1.tgz` — npm tarzı paket (`package/` kökü)
- `SHA256SUMS.txt` — 1.0.0, 1.1.0 ve 1.1.1 özetleri
