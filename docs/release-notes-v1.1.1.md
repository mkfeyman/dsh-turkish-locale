# dsh-turkish-locale v1.1.1 — 0.2.2-rc.2 coverage

**Date:** 2026-11-13 · **Target:** DSH `0.2.2-rc.2` (commit `a6b1b85`)

## What changed

- **Full coverage refreshed:** 73 → **75 namespaces**, 3,838 → **4,223 strings**;
  the **430 strings** added in `0.2.2-rc.2` were translated (100 % coverage
  restored).
- **2 new namespaces:** `cuaPermissions` (66 — Computer Use permission
  management) and `account.notifications` (1).
- **Grown namespaces:** `forgePanel` +174 (change-request overviews,
  branch/commit ranges, reviewer states), `settings.models` +37 (Gemini
  protocol, retry strategies), `sidebarFiles` +32 (ignore files, search hints),
  `settings` +23 and `settings.webSearch` +23 (channel labels, billing/override,
  legacy-key hint), `agent-team` +18, `chat`/`conversation` +12 each,
  `liveshare` +9, `subagent` +7, `sidebarTerminal` +5, and more.
- **45 removed strings** pruned from the pack (e.g. `agent-team` −13,
  `liveshare` −11, `settings.webSearch` −7).
- **2 keys whose English source changed** were fixed for placeholder drift:
  `pluginManager.updateStepInstalling` (`{source}`) and
  `settings.webSearch.baseUrlHint` (`{path}`).

## Compatibility

- The locale runtime API did not change: the `addLanguage`,
  `register(ns, locale, dict)`, `resolveText`, snapshot, and
  `locale.preference` contracts are the same in rc.2. The
  `dsh-client-locale@0.2.2-rc.2` tag differs from rc.1 only in `package.json`
  (the version), so the ordered-preference patch draft `0003` also applies to
  rc.2 unchanged.
- **Profile install fixed:** in rc.2 the profile `node_modules` is pnpm-managed,
  and the old hand-copied directory was no longer mounted by the Loader. The
  pack is now linked through `plugin_manager install_bundle` (re-linked with
  `remove_bundle` + `install_bundle`) and has returned to the boot graph.

## Verification

- Four parallel translation chunks (430/430 entries); placeholder check clean.
- Live test (DSH 0.2.2-rc.2): the pack loads from the boot graph (`rev
  2fe8ccdf`), the UI reports `lang=tr`, and the language selector works.
- The `engines.dsh` range was kept (`>=0.2.1-rc.3 <0.3.0`).

## Files

- `dsh-turkish-locale-1.1.1.tgz` — npm-style package (`package/` root)
- `SHA256SUMS.txt` — 1.0.0, 1.1.0 and 1.1.1 digests
