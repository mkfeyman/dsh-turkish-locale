# DSH 0.2.2-rc.1 update — Turkish plugin analysis and debugging report

**Date:** 2026-11-05 · **Measured version:** `0.2.2-rc.1` (commit `c59d10a`,
nightly channel) · **GUI:** `http://127.0.0.1:61914`

---

## 1. Update detection

| Item | Value |
|---|---|
| Previously installed version | 0.2.1-rc.3 (commit `be72761`) |
| Newly installed version | **0.2.2-rc.1** (commit `c59d10a`) |
| Channel | `nightly` (app-update.yml) |
| Boot graph `release` | `{"version":"0.2.2-rc.1","commit":"c59d10a"}` |
| GUI port | 61914 (the app restarted after the update) |

## 2. Plugin health check (live)

| Check | Result |
|---|---|
| `dsh-turkish-locale` row in the boot graph | ✓ present; `inject: ["@deepseek-ai/dsh-client-locale"]`, rev `99640a40d87e`, no error marker |
| Bundle served through `/plugins` | ✓ |
| Language selector | ✓ **9 languages**: 中文, English, 日本語, Español, Français, Deutsch, Русский, Português + **Türkçe** (the 8 built-in 0.2.2 languages plus our pack) |
| Active language | ✓ `lang=tr`, Turkish UI |
| Language round-trip (Türkçe → English → Türkçe) | ✓ works |
| Persistence | ✓ `cordis.patch.yml` → `locale.preference: tr` |
| Plugins → Installed | ✓ "Türkçe dil paketi" listed with its Turkish description; no `Problem` state |
| Crash/console error | None in the visual/DOM check (UI fully interactive) |

**Conclusion: the update did not break the plugin.** No code change is required.

## 3. Locale API compatibility (0.2.1-rc.3 → 0.2.2-rc.1)

The installed `dsh-client-locale@0.2.2-rc.1` client package was inspected:

| API | Status |
|---|---|
| `addLanguage({id,label,fallback})` | Unchanged — single fallback, chain terminates at `en` |
| `register(ns, locale, dict)` (per-locale) | Unchanged — the form this pack uses |
| `register(ns, {zh,en,...})` (typed) | Widened in 0.2.2 to "baseline zh/en required + additional languages optional"; our pack is unaffected |
| `resolveText`, `fallbackChain`, `translate` | Same (the chain is language-defined; ordered preference still absent) |
| Snapshot `{active, locales, revision}` | Same |
| `LOCALE_IDS` baseline | `["zh","en"]` — unchanged; the 8 built-in dictionaries are registered inside `apply()` through `addLanguage` + `register` |
| `detectBrowserLocale` | Still first-match (the ordered list is still a proposal) |
| Our `engines.dsh` range (`>=0.2.1-rc.3 <0.3.0`) | ✓ covers 0.2.2-rc.1 |

## 4. Coverage delta (measured)

The dictionaries were re-extracted from the new version:

| Metric | rc.3 | 0.2.2-rc.1 | Delta |
|---|---|---|---|
| Namespaces | 64 | **73** | +10, −1 |
| English keys | 2,910 | **3,838** | **+981, −52** |
| Changed English values | — | — | **60** |
| Missing Turkish | 0 | — | **981 missing** |

New namespaces: `forgePanel` 253, `liveshare` 225, `stats` 177,
`creationRecommendations` 55, `pluginRecommendations` 25, `actionCards` 14,
`fileActions` 12, `contextMenu` 1, `fileDrag` 1, `messageQuotes` 1; another 217
keys were added to existing namespaces (largest: `pluginManager` +72,
`schedule.manager` +70). Removed namespace: `deepseek-model-label-1017`.
`fixtures/version-coverage.json` records the measured values.

**Visual check:** on the updated app the new 0.2.2 panels (forge/stats/liveshare,
etc.) appear in English because they were not translated yet, while the core UI
stays Turkish. The English source text of 60 existing translations changed (low
semantic-drift risk, but worth reviewing).

## 5. Debugging findings

1. **No plugin defect.** The runtime is compatible; round-trip and persistence
   were verified.
2. **Two real bugs in our extraction tooling were found and fixed**
   (`tools/extract_dicts.js`):
   - OOM/crash (exit 134) on the new, larger bundles: definition lookup was
     O(key × file) and deep object recursion exploded → a single-pass
     `buildDefs()` index, a size/shape filter, and a `trimStart` fix (array `[`
     definitions included). Result: **73/3,838/0 diagnostics** at ~second speed.
3. **No misleading states:** the `Update available` badges on the Plugins page
   belong to the Codex/Claude subagent rows (the app's own catalog), not to our
   pack.
4. **Pack metadata resolves correctly:** the "Türkçe dil paketi" row is shown
   with the `tr` language (manifest `locale/tr.json`).

## 6. Recommendations

| Recommendation | Description |
|---|---|
| Translate the 981 new strings | Refresh the pack against the 0.2.2-rc.1 source (parallel translation, 4-5 chunks) |
| Review the 60 changed `en` values | Update the Turkish where the meaning moved |
| Release the pack as **1.1.0** | Keep the `engines.dsh` range, pin the new commit in the market index |
| Move the fixture to the rc.1 base | `fixtures/version-coverage.json` is already up to date; `tr-partial` should also partially cover the new namespaces |
| Ordered-preference patch | `0002` is alpha.2-based; compare once more against the rc.1 source and rebase if needed |

## 7. Evidence

- [`docs/settings-tr.png`](settings-tr.png) — Settings, language selector, Turkish
- [`docs/partial-pack-demo.png`](partial-pack-demo.png) — partial-pack fallback demo
- Raw extraction artifacts (`source.json`, delta JSON) are produced by the
  workspace tooling and are not published in this repository; the measured
  values are recorded in [`fixtures/version-coverage.json`](../fixtures/version-coverage.json).
