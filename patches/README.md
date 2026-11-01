# Patch draft: ordered locale preference (Discussion #11699)

**Status:** draft, generated against the public source of **`dsh-v0.2.1-rc.3`**
(tag commit `1f81c047fc48fa190a683e469daa699857e9afe8`). It is not a submitted
pull request — upstream `CONTRIBUTING.md` does not accept external PRs at the
moment. It is shared for review under [Discussions #11699](https://github.com/deepseek-ai/deepseek-harness/discussions/11699).

## What it changes

`packages/client/locale` only (11 files, ~723 changed lines):

| File | Change |
|---|---|
| `src/locale-settings.ts` | `preference` accepts an ordered list (`string[]`) or the legacy single string; shared `normalizeLocalePreference()`; schema union |
| `src/index.ts` | Host `Config.preference` type widened; exports `LocalePreference` |
| `src/client/bootstrap.ts` | Native-shell bootstrap accepts a list preference as well as the legacy string |
| `src/client/index.ts` | Runtime walks the ordered preference per key (each entry followed by its declared fallback chain, then `en`); snapshot gains `preference`; `active` is the first registered entry; `setPreferences`/`addPreference`/`removePreference`/`movePreference`; `setLocale` keeps writing the legacy string; `detectBrowserLocales` keeps the browser's whole order |
| `src/client/settings-store.ts` | Mirrors the ordered preference into the Language row |
| `src/client/LanguageRow.tsx` | Reorderable preference list with add/move/remove, replacing the single-select pill |
| `src/client/LanguageRow.module.css` | Styles for the list controls |
| `src/locales/settings.ts` | en/zh copy for the new row controls |
| `tests/ordered-preference.client.spec.ts` | New coverage: legacy string migration, per-key order, `resolveText`, browser order, persistence, events |
| `tests/language-row.client.spec.tsx` | Updated for the list UI |
| `tests/settings-store.client.spec.ts` | Updated for the `preference` mirror |

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

## Verification status

- The patch hunks were generated from the pristine tag sources and re-applied to
  them programmatically: **self-check passes (11 files)**.
- The repository's own toolchain (pnpm install + vitest + tsc) was **not**
  available in the environment where this draft was produced, so the updated
  tests have **not been executed** and the TypeScript has not been type-checked
  against the real dependency tree. Expect small adjustments before it builds.
- API shapes the surrounding packages consume (`getSnapshot().active`,
  `locale/change`, `slots.installLocale`, injected `t`) are preserved on purpose.

## Apply

```sh
git checkout dsh-v0.2.1-rc.3
git apply /path/to/0001-ordered-locale-preference.patch
pnpm install
pnpm --filter @deepseek-ai/dsh-client-locale test
```

## Fixture

`../fixtures/` contains a deterministic 59.4% Turkish subset and expected lookup
samples to exercise the ordered list against the current single-chain behaviour.
