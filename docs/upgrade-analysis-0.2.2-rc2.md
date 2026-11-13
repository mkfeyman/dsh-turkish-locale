# DSH 0.2.2-rc.2 update — Turkish plugin analysis

**Date:** 2026-11-13 · **Measured version:** `0.2.2-rc.2` (commit `a6b1b85`) ·
**Previous:** `0.2.2-rc.1` (commit `c59d10a`)

## 1. Upgrade-guide review

The installed guide `docs/upgrade-guide/v0.2.2-rc.1/` (rc.1 → rc.2, 19 items) was
read. No item changes a surface this pack uses; the closest one is
`plugin-update-method` (`BundleInfo.updatable` → `BundleInfo.update`), which
affects the plugin-manager UI copy that the pack translates, not the pack itself.

## 2. Locale package comparison

Comparing the `packages/client/locale` trees of tags `dsh-v0.2.2-rc.1` and
`dsh-v0.2.2-rc.2` shows a **single upstream change: `package.json` (version
bump)**. The runtime, settings, row, and test sources are identical, so the
ordered-preference patch draft `0003` applies to rc.2 unchanged and its rc.1
validation (vitest 79/79, typecheck gate 5/5) carries over.

## 3. The one real breakage: pnpm-managed profiles

In rc.2 the profile `node_modules` is managed by pnpm (`.modules.yaml`,
`storeDir`, lockfile), and a hand-copied plugin directory is no longer mounted by
the Loader — the boot graph did not contain `dsh-turkish-locale` at all (its
`link:` target pointed at a workspace subdirectory that no longer existed).

Fix: install through the plugin manager instead of copying files —

```
plugin_manager remove_bundle  dsh-turkish-locale
plugin_manager install_bundle C:\path\to\dsh-turkish-locale
```

The manager writes the profile dependency, the lockfile entry, and the managed
rows (`tr-locale`, `locale` override). After the re-link the plugin returns to
the boot graph (`rev 97ea264c69cc`) and the UI reports `lang=tr`.

## 4. Coverage delta (measured)

Dictionaries were re-extracted from the rc.2 installation (ASAR-aware
extractor):

| Metric | 0.2.2-rc.1 | 0.2.2-rc.2 | Delta |
|---|---|---|---|
| Namespaces | 73 | **75** | +2 |
| English keys | 3,838 | **4,223** | **+430, −45** |

New namespaces: `cuaPermissions` (66 — Computer Use permission management) and
`account.notifications` (1). Largest growth: `forgePanel` +174,
`settings.models` +37, `sidebarFiles` +32, `settings` +23,
`settings.webSearch` +23, `agent-team` +18, `chat`/`conversation` +12 each.
Two keys whose English source changed had placeholder drift and were fixed:
`pluginManager.updateStepInstalling` (`{source}`) and
`settings.webSearch.baseUrlHint` (`{path}`).

All 430 new strings were translated in four parallel chunks; the built pack is
**75 namespaces / 4,223 strings — 100 %** of the rc.2 English source (v1.1.1).

## 5. Verification

- Placeholder check: 4,223/4,223 keys match the source, zero violations.
- Live test: boot graph entry present (`rev 97ea264c69cc`), `lang=tr`, Turkish
  home/settings copy including new rc.2 strings (e.g. "Oluşturucu modu").
- Plugin manager: `dsh-turkish-locale` v1.1.1, `enabled: true`,
  `installed: true`, no `error`; rows `tr-locale`, overrides `locale`.

## 6. Attention: unrelated profile plugins

`@deepseek-ai/dsh-subagent-codex` and `@deepseek-ai/dsh-subagent-claude-code`
are still installed at `0.2.2-rc.1` and report `incompatible-version` on rc.2.
They are not part of this pack; update them from the Plugins page.
