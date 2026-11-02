"""Standalone audit for language-pack dictionary gaps (Discussion #11699, layer 2).

Reads a dictionary dump of the shape a locale pack registers:

    { "namespace": { "locale": { "key": "value" } } }

and reports the cases an ordered preference *cannot* fix by itself:

  * namespaces that never register English (`en`),
  * keys whose raw source is CJK (Han) and therefore would render as Chinese
    text when every dictionary misses,
  * which namespaces look "typed" (zh+en pairs) versus "per-locale".

Run it locally — only the printed counts need to be shared.

Usage: python tools/audit_locale_gaps.py <dump.json>
"""

import json
import re
import sys

HAN = re.compile(r"[\u4e00-\u9fff]")


def audit(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)

    rows = []
    for namespace, locales in data.items():
        normalized = {str(locale).lower(): entries for locale, entries in locales.items()}
        has_en = "en" in normalized
        has_zh = "zh" in normalized
        cjk_keys = []
        for locale, entries in locales.items():
            for key in entries:
                if HAN.search(key):
                    cjk_keys.append({"locale": locale, "key": key})
        rows.append({
            "namespace": namespace,
            "locales": sorted(normalized),
            "typed": has_en and has_zh,
            "hasEn": has_en,
            "cjkKeys": cjk_keys,
        })

    missing_en = [row for row in rows if not row["hasEn"]]
    leak_risk = [
        {"namespace": row["namespace"], "key": item["key"], "locale": item["locale"]}
        for row in missing_en for item in row["cjkKeys"]
    ]

    print(f"namespaces: {len(rows)}")
    print(f"typed (zh+en): {sum(r['typed'] for r in rows)}")
    print(f"per-locale or non-typed: {sum(not r['typed'] for r in rows)}")
    print(f"namespaces missing 'en': {len(missing_en)}")
    print(f"CJK keys inside namespaces missing 'en' (would render Chinese raw keys): {len(leak_risk)}")
    for entry in leak_risk[:40]:
        print("  LEAK", entry["namespace"], "::", entry["key"], f"({entry['locale']})")
    for row in missing_en[:20]:
        print("  NO-EN", row["namespace"], "locales:", row["locales"])
    return rows, missing_en, leak_risk


if __name__ == "__main__":
    audit(sys.argv[1])
