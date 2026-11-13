# dsh-turkish-locale v1.1.0 — 0.2.2-rc.1 coverage

**Date:** 2026-11-05 · **Target:** DSH `0.2.2-rc.1` (commit `c59d10a`)

## What changed

- **Full coverage refreshed:** 64 → **73 namespaces**, 2,910 → **3,838 strings**;
  the **981 strings** added in `0.2.2-rc.1` were translated (100 % coverage
  restored).
- **10 new namespaces translated:** `forgePanel` (253), `liveshare` (225),
  `stats` (177), `creationRecommendations` (55), `pluginRecommendations` (25),
  `actionCards` (14), `fileActions` (12), `contextMenu` (1), `fileDrag` (1),
  `messageQuotes` (1).
- **60 changed English source values** reviewed: 40 Turkish values were updated
  to match the new wording (e.g. "reminder" → "automation task", the plugin
  index rename, model-list refresh copy), 20 were kept because the meaning did
  not move.
- **52 removed strings and 1 removed namespace** (`deepseek-model-label-1017`)
  were pruned from the pack.
- Two older labels fixed: `command/token.feedback` → "Geri bildirim",
  `command/token.permission` → "İzin".

## Verification

- Placeholder check: 3,838/3,838 keys match the source, no placeholder
  violations, zero English function-word residue.
- Live test (DSH 0.2.2-rc.1): the pack loads from the boot graph, the language
  selector lists the 8 built-in languages plus Türkçe, round-trip switching and
  `locale.preference: tr` persistence were verified, and the new copy appears in
  the UI (e.g. "Model sağlayıcısı ekle").
- Installation and usage are unchanged; the `engines.dsh` range was kept
  (`>=0.2.1-rc.3 <0.3.0`).

## Files

- `dsh-turkish-locale-1.1.0.tgz` — npm-style package (`package/` root)
- `SHA256SUMS.txt` — 1.0.0 and 1.1.0 digests
