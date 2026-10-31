#!/usr/bin/env python3
"""Insert a Markdown list line into a section, in alphabetical order by link title.

Usage: insert-list-line.py FILE --section "### Productivity" --line "* [Name](url) - Description."

Exit codes: 0 inserted, 1 the name is already in the section, 2 bad input (nothing written).
"""
import argparse
import pathlib
import re
import sys
import unicodedata

ITEM = re.compile(r"^\s*[*-] \[([^\]]+)\]")


def name_of(line):
    match = ITEM.match(line)
    return match.group(1) if match else None


def sort_key(name):
    """Compare names by their base letters, so 'Çentik' sorts with C, not after Z."""
    decomposed = unicodedata.normalize("NFKD", name)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).casefold()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file")
    parser.add_argument("--section", required=True, help="exact heading line, e.g. '### Productivity'")
    parser.add_argument("--line", required=True)
    args = parser.parse_args()

    new_name = name_of(args.line)
    if not new_name:
        print("--line must start with '* [Name]' or '- [Name]'", file=sys.stderr)
        return 2

    path = pathlib.Path(args.file)
    lines = path.read_text().split("\n")
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == args.section.strip())
    except StopIteration:
        print(f"section not found: {args.section}", file=sys.stderr)
        return 2

    level = len(args.section) - len(args.section.lstrip("#"))
    end = len(lines)
    for i in range(start + 1, len(lines)):
        stripped = lines[i].lstrip()
        if stripped.startswith("#") and len(stripped) - len(stripped.lstrip("#")) <= level:
            end = i
            break

    items = [i for i in range(start + 1, end) if name_of(lines[i])]
    if not items:
        print(f"no list items under {args.section}", file=sys.stderr)
        return 2
    if any(name_of(lines[i]).casefold() == new_name.casefold() for i in items):
        print(f"{new_name} is already in {args.section}", file=sys.stderr)
        return 1

    position = items[-1] + 1
    for i in items:
        if sort_key(name_of(lines[i])) > sort_key(new_name):
            position = i
            break
    lines.insert(position, args.line)
    path.write_text("\n".join(lines))
    print(f"{path}:{position + 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
