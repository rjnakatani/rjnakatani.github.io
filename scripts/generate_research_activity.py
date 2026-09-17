#!/usr/bin/env python3
"""Generate assets/charts/research_activity.json from news.md.

Each bullet in news.md starts with a year-month (e.g. ``- 2026-07 — ...``).
The bullet text is classified by keyword into one or more categories and
tallied per year:

- "first author" : mentions of a first-author paper/publication
- "presentation" : presented / speaker / poster / conference
- "award"        : award / grant / allowance
- "fellowship"   : fellow (e.g. "JSPS DC1 fellow")

If a bullet contains an explicit year range such as "2024-2027" (e.g. a
multi-year fellowship), every year from the start up to and including the
end of the current year is counted.

Usage:
    python3 scripts/generate_research_activity.py
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEWS_PATH = ROOT / "news.md"
OUT_PATH = ROOT / "assets" / "charts" / "research_activity.json"

CATEGORIES = [
    ("first author", re.compile(r"first-author|paper|publication", re.I)),
    ("presentation", re.compile(r"present|speaker|poster|conference", re.I)),
    ("award", re.compile(r"award|grant|allowance", re.I)),
    ("fellowship", re.compile(r"fellow", re.I)),
]

# Bullet: "- 2026-07 — text..." (also accepts : or - as separator)
BULLET_RE = re.compile(r"^\s*-\s*(\d{4})-\d{2}\s*(?:—|:|-)\s*(.*)$")
# Explicit year range in the text, e.g. "2024-2027" / "2024–2027"
YEAR_RANGE_RE = re.compile(r"(20\d{2})\s*[-–]\s*(20\d{2})")


def tally(path: Path) -> dict:
    current_year = datetime.now().year
    counts = {cat: {} for cat, _ in CATEGORIES}

    for line in path.read_text(encoding="utf-8").splitlines():
        m = BULLET_RE.match(line)
        if not m:
            continue
        year = int(m.group(1))
        text = m.group(2)

        # Expand explicit year ranges (multi-year fellowships etc.),
        # clamped to the current year.
        years = {year}
        for start_s, end_s in YEAR_RANGE_RE.findall(text):
            start, end = int(start_s), int(end_s)
            if start <= end:
                years.update(range(start, min(end, current_year) + 1))

        for cat, pattern in CATEGORIES:
            if pattern.search(text):
                for y in years:
                    counts[cat][y] = counts[cat].get(y, 0) + 1

    return counts


def to_series(counts: dict) -> dict:
    return {
        cat: [{"x": year, "y": n} for year, n in sorted(years.items())]
        for cat, years in counts.items()
    }


def main() -> int:
    if not NEWS_PATH.is_file():
        print(f"error: {NEWS_PATH} not found", file=sys.stderr)
        return 1

    data = to_series(tally(NEWS_PATH))
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(data, separators=(", ", ": ")) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
