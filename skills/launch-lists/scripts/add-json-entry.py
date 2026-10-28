#!/usr/bin/env python3
"""Append an app entry to open-source-mac-os-apps' applications.json, keeping the file's own formatting.

Usage: add-json-entry.py applications.json entry.json

Exit codes: 0 appended, 1 the repo or title is already listed, 2 bad input (nothing written).
"""
import json
import pathlib
import sys

REQUIRED = ["title", "short_description", "categories", "repo_url", "icon_url", "screenshots", "official_site", "languages"]
CLOSING = "\n        }\n    ]\n}"


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    apps_path, entry_path = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    text = apps_path.read_text()
    data = json.loads(text)
    entry = json.loads(entry_path.read_text())

    missing = [k for k in REQUIRED if k not in entry]
    if missing:
        print(f"entry is missing: {', '.join(missing)}", file=sys.stderr)
        return 2
    if not entry["short_description"].rstrip().endswith("."):
        print("short_description must end with a period", file=sys.stderr)
        return 2
    for app in data["applications"]:
        if app.get("repo_url", "").rstrip("/").lower() == entry["repo_url"].rstrip("/").lower() or app.get("title", "").lower() == entry["title"].lower():
            print(f"{entry['title']} is already listed", file=sys.stderr)
            return 1

    body = text.rstrip("\n")
    if not body.endswith(CLOSING):
        print("unexpected end of applications.json; edit by hand", file=sys.stderr)
        return 2
    rendered = json.dumps({k: entry[k] for k in REQUIRED}, indent=4, ensure_ascii=False)
    rendered = "\n".join("        " + l for l in rendered.split("\n"))
    trailing = text[len(body):]
    new = body[: -len("\n    ]\n}")] + ",\n" + rendered + "\n    ]\n}" + trailing
    json.loads(new)
    apps_path.write_text(new)
    print(f"{apps_path}: appended {entry['title']} ({len(data['applications']) + 1} apps)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
