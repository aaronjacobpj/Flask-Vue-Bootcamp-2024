#!/usr/bin/env python3
"""
Scan weeks/bootcamp/<year>/<month>/<course>/ for day zips and slides and
write/update the matching course JSON in src/assets/<year>/<Flask|Vue>/<file>.json.

Files are matched to a day by number:
    day3.zip                                  -> source code for Day 3
    day3.pdf, day3-slides.pdf, Day 3.pptx     -> slides for Day 3

Existing JSON files are merged, never overwritten blindly: sessions that are
already listed (with their youtube ids, notes, names) are kept as-is, missing
days are appended, and slides are only filled in where "slides" is still empty
(so a link you typed in by hand, e.g. Google Slides, is never replaced).

The store picks up every JSON under src/assets/<year>/<track>/ automatically.

Usage:
    python3 scripts/generate_courses.py            # write changes
    python3 scripts/generate_courses.py --dry-run  # only print what would change
"""

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEEKS_DIR = ROOT / "weeks" / "bootcamp"
ASSETS_DIR = ROOT / "src" / "assets"

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

# "MAD l" -> Flask, "MAD ll" -> Vue, with an optional (Morning)/(Evening) batch
COURSE_DIR_RE = re.compile(r"^MAD (?P<level>l{1,2})(?: \((?P<batch>Morning|Evening)\))?$")
DAY_ZIP_RE = re.compile(r"^day ?(?P<num>\d+)\.zip$", re.IGNORECASE)
DAY_SLIDES_RE = re.compile(r"^day ?(?P<num>\d+)(?:[ _-]?slides)?\.(?:pdf|pptx?|key)$", re.IGNORECASE)

TRACKS = {
    "l": ("Flask", "Web Development Bootcamp Using Flask and HTML"),
    "ll": ("Vue", "Web Development Bootcamp Using Flask and Vue"),
}


def norm_url(url):
    return url.rstrip("/") + "/"


def load_existing(track_dir):
    """Return {path: data} for every course JSON already in a track folder."""
    existing = {}
    if track_dir.is_dir():
        for path in sorted(track_dir.glob("*.json")):
            with open(path) as f:
                existing[path] = json.load(f)
    return existing


def find_target(track_dir, month, batch, base_url):
    """Pick the JSON file for a course folder, reusing an existing one if possible."""
    existing = load_existing(track_dir)

    # 1. A file for this month that already points at this folder (MayEve.json, MayM.json, ...)
    for path, data in existing.items():
        if norm_url(data.get("base-url", "")) == base_url and path.stem.startswith(month):
            return path, data

    # 2. The conventional name: <Month>.json, <Month>M.json, <Month>E.json
    suffix = {"Morning": "M", "Evening": "E"}.get(batch, "")
    path = track_dir / f"{month}{suffix}.json"
    return path, existing.get(path)


def session_template(sessions, default_prefix):
    """Reuse the naming style of the existing day sessions, e.g. '... - Day {n}'."""
    for s in reversed(sessions):
        m = re.match(r"^(.*- Day )\d+$", s.get("name", ""))
        if m:
            return m.group(1) + "{n}"
    return default_prefix + " - Day {n}"


def find_session(sessions, num, zip_name):
    """The existing session for a day: by its zip, else by a name ending in 'Day <num>'."""
    for s in sessions:
        if zip_name and s.get("source-code") == zip_name:
            return s
    day_re = re.compile(rf"- Day {num}\b")
    for s in sessions:
        if day_re.search(s.get("name", "")):
            return s
    return None


def build_course(year, month, course_dir):
    m = COURSE_DIR_RE.match(course_dir.name)
    if not m:
        print(f"  skip  {course_dir.relative_to(ROOT)} (unrecognised folder name)")
        return None

    track, prefix = TRACKS[m["level"]]
    batch = m["batch"]
    base_url = norm_url(f"/weeks/bootcamp/{year}/{month}/{course_dir.name}")
    track_dir = ASSETS_DIR / str(year) / track

    # {day number: {"zip": filename, "slides": filename}}
    days = {}
    for p in sorted(course_dir.iterdir()):
        if not p.is_file():
            continue
        if z := DAY_ZIP_RE.match(p.name):
            days.setdefault(int(z["num"]), {})["zip"] = p.name
        elif sl := DAY_SLIDES_RE.match(p.name):
            days.setdefault(int(sl["num"]), {}).setdefault("slides", p.name)

    path, data = find_target(track_dir, month, batch, base_url)
    is_new = data is None
    if is_new:
        data = {
            "name": f"{track} ({batch})" if batch else track,
            "base-url": base_url,
            "term": month,
            "year": year,
            "sessions": [],
        }

    changes = []
    if norm_url(data.get("base-url", "")) != base_url:
        changes.append(f"base-url {data.get('base-url')!r} -> {base_url!r}")
        data["base-url"] = base_url
    if data.get("term") != month or data.get("year") != year:
        changes.append(f"term/year {data.get('term')} {data.get('year')} -> {month} {year}")
        data["term"], data["year"] = month, year

    template = session_template(data["sessions"], prefix)
    for num, files in sorted(days.items()):
        session = find_session(data["sessions"], num, files.get("zip"))
        if session is None:
            session = {
                "source-code": files.get("zip", ""),
                "youtube-video-id": "",
                "notes": "",
                "slides": "",
                "name": template.format(n=num),
            }
            data["sessions"].append(session)
            changes.append(f"add Day {num}")
        elif files.get("zip") and not session.get("source-code"):
            session["source-code"] = files["zip"]
            changes.append(f"source code Day {num}")

        if files.get("slides") and not session.get("slides"):
            session["slides"] = base_url + files["slides"]
            changes.append(f"slides Day {num}")

    return path, data, is_new, changes


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="print changes without writing files")
    args = parser.parse_args()

    for year_dir in sorted(p for p in WEEKS_DIR.iterdir() if p.is_dir() and p.name.isdigit()):
        year = int(year_dir.name)
        for month_dir in sorted(
            (p for p in year_dir.iterdir() if p.is_dir() and p.name in MONTHS),
            key=lambda p: MONTHS.index(p.name),
        ):
            for course_dir in sorted(p for p in month_dir.iterdir() if p.is_dir()):
                result = build_course(year, month_dir.name, course_dir)
                if result is None:
                    continue
                path, data, is_new, changes = result
                rel = path.relative_to(ROOT)
                if not changes:
                    print(f"  ok    {rel}")
                    continue
                print(f"  {'new' if is_new else 'update':<5} {rel}: {', '.join(changes)}")
                if not args.dry_run:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(path, "w") as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                        f.write("\n")


if __name__ == "__main__":
    main()
