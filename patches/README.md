# Patch draft: ordered locale preference (Discussion #11699)

**Status:** draft, not a submitted pull request — upstream `CONTRIBUTING.md`
does not accept external PRs at the moment. Shared for review under
[Discussions #11699](https://github.com/deepseek-ai/deepseek-harness/discussions/11699).

Three variants are provided:

| Patch | Base | Purpose |
|---|---|---|
| [`0003-ordered-locale-preference-0.2.2-rc1.patch`](0003-ordered-locale-preference-0.2.2-rc1.patch) | **`dsh-v0.2.2-rc.1`** (tag commit `66491b05…`) | **Current draft, CI-validated.** 17 files: the locale package changes plus 5 sibling test fixtures whose `LocaleSnapshot` literals gain the `preference` field (they stopped typechecking once the snapshot carries the ordered list). Real repo validation: vitest **79/79**, sanctioned typecheck gate **5/5**. |
| [`0002-ordered-locale-preference-0.2.2.patch`](0002-ordered-locale-preference-0.2.2.patch) | `dsh-v0.2.2-alpha.2` (commit `f3803c96…`) | Kept for comparison; superseded by `0003`. |
| [`0001-ordered-locale-preference.patch`](0001-ordered-locale-preference.patch) | `dsh-v0.2.1-rc.3` (commit `1f81c047…`) | Kept for the originally installed desktop build and for comparison. |

## What it changes

`packages/client/locale` only (11 files):

| File | Change |
|---|---|
| `src/locale-settings.ts` | `preference` accepts an ordered list (`string[]`) or the legacy single string; shared `normalizeLocalePreference()`; schema union |
| `src/index.ts` | Host `Config.preference` type widened; exports `LocalePreference` |
| `src/client/bootstrap.ts` | Native-shell bootstrap accepts a list preference as well as the legacy string |
| `src/client/index.ts` | Runtime walks the ordered preference per key (each entry followed by its declared fallback chain, then `en`); snapshot gains `preference`; `active` is the first registered entry; `setPreferences`/`addPreference`/`removePreference`/`movePreference`; `setLocale` keeps writing the legacy string; `detectBrowserLocales` keeps the browser's whole order |
| `src/client/settings-store.ts` | Mirrors the ordered preference into the Language row |
| `src/client/LanguageRow.tsx` | Reorderable preference list with add/move/remove, replacing the single-select pill |
| `src/client/LanguageRow.module.css` | Styles for the list controls (merged with the 0.2.2 responsive/hover rules) |
| `src/locales/settings.ts` | New row copy for **all eight** shipped languages (`zh`, `en`, `ja`, `es`, `fr`, `de`, `ru`, `pt`) |
| `tests/ordered-preference.client.spec.ts` | New coverage: legacy string migration, per-key order, `resolveText`, browser order, persistence, events |
| `tests/language-row.client.spec.tsx` | Updated for the list UI |
| `tests/settings-store.client.spec.ts` | Updated for the `preference` mirror |
| `tests/apply.client.spec.ts` | Fixture literal gains `preference` (snapshot now requires it) |
| `ui-input-trigger`, `ui-plugin-manager`, `ui-plugin-market` (×2), `client-ui-cot-translation` tests | Sibling `LocaleSnapshot` fixtures gain the `preference` field so the client aggregate typechecks |

## Design decisions

- **Backwards compatible storage.** A stored `string` is read as a one-element
  list; the Host schema accepts both forms. Existing profiles keep loading, and
  `setLocale()` still writes the legacy string so current call sites and tests
  keep their exact persistence behaviour. New UI writes an array through
  `setPreferences()`.
- **Active language = first registered entry.** `snapshot.active` stays a single
  id, so `<html lang>`, `locale/change`, the native bridge `onChange`, and current
  snapshot consumers keep working. The new `snapshot.preference` carries the
  ordered list.
- **Lookup order.** For each preferred language, its declared fallback chain is
  expanded and deduplicated, then `en` is appended if missing:
  `[ru, en, zh]` → `ru, en, zh`; `[uk, ru]` → `uk, ru, en`. A one-element
  preference therefore reproduces today's chain exactly (`tr` → `tr, en`).
- **Browser detection keeps the order** instead of narrowing to one match, which
  also addresses the `es-AR` / `fr-be` mis-detection class mentioned in the
  proposal.
- **`locale/change` only fires when the active language changes**; reorder-only
  updates bump the revision so the settings row and rendered text refresh without
  the event storm the current code deliberately avoids.
- **0.2.2 built-ins.** The six extra dictionaries 0.2.2 registers through
  `addLanguage` are untouched; they simply appear in the ordered catalog and can
  be reordered/removed like any other language.

## Verification status

- Patch hunks are generated from pristine tag sources and re-applied
  programmatically: **self-check passes** for every variant (applying `0003` to a
  pristine rc.1 tree reproduces the patched tree exactly, 17 file sections).
- **Real repository validation (base rc.1):** the zipball of `dsh-v0.2.2-rc.1`
  was checked out, the patch applied, dependencies installed
  (`pnpm@11.28.5`, 1,434 packages), and the repo's own tooling run:
  - `vitest run packages/client/locale` → **9/9 files, 79/79 tests pass**
    (including the new `ordered-preference.client.spec.ts` and the list-UI
    `language-row.client.spec.tsx`).
  - `pnpm run typecheck` (sanctioned gate) → **5/5 gates pass**: Host Typert,
    host compiler, client compiler, host aggregate check, client aggregate check.
    The first run failed on 8 sibling test fixtures that construct
    `LocaleSnapshot` literals without `preference`; the patch updates those
    fixtures, so the client aggregate is green.
  - `tsc -b packages/client/locale/tsconfig.client.json` → no errors in the
    locale package.
- The patched `src/client/index.ts` is additionally bundled with its framework
  imports stubbed and executed against the 59.4% fixture in a standalone harness
  (`tools/harness/run.mjs` in the workspace):
  - base `dsh-v0.2.2-rc.1`: **17/17 semantic checks pass**, 10/10 changed/new
    TypeScript files pass a syntax/transpile check →
    [`validation-report-0.2.2-rc1.json`](validation-report-0.2.2-rc1.json)
  - base `dsh-v0.2.2-alpha.2`: same results →
    [`validation-report-0.2.2.json`](validation-report-0.2.2.json)
  - base `dsh-v0.2.1-rc.3`: same results →
    [`validation-report.json`](validation-report.json)
- Coverage: ordered lookup (`[tr,en]` vs `[en,tr]`), legacy string migration,
  `resolveText`, browser-order retention, persistence shapes, revision and
  `locale/change` behaviour on reorder, and a zh-only dictionary reached before
  the raw key.
- API shapes the surrounding packages consume (`getSnapshot().active`,
  `locale/change`, `slots.installLocale`, injected `t`) are preserved on purpose;
  the only cross-package edits are the sibling test fixtures above.

## Apply

```sh
# current draft (0.2.2-rc.1 source)
git checkout dsh-v0.2.2-rc.1
git apply /path/to/0003-ordered-locale-preference-0.2.2-rc1.patch
pnpm install
pnpm --filter @deepseek-ai/dsh-client-locale test

# installed-build variant (0.2.1-rc.3 source)
git checkout dsh-v0.2.1-rc.3
git apply /path/to/0001-ordered-locale-preference.patch
```

## Fixture

`../fixtures/` contains a deterministic 59.4% Turkish subset, expected lookup
samples, and a `version-coverage.json` note: the fixture is rc.3-based, so the
0.2.2 delta (9 namespaces / 853 strings) exercises the English fallback rather
than Turkish coverage.
