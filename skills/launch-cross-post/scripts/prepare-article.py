#!/usr/bin/env python3
"""Turn a blog post (Markdown with front matter) into a cross-post body and its metadata.

Usage: prepare-article.py POST.md --canonical URL --out DIR [--asset ./img.webp=https://...]... [--footer TEXT]

Writes DIR/body.md (no front matter, relative images replaced by public URLs, footer linking the
canonical post) and DIR/meta.json (title, description, tags, cover, canonical_url).
Exit codes: 0 written, 2 bad input (nothing written).
"""
import argparse
import json
import pathlib
import re
import sys

IMAGE = re.compile(r"(!\[[^\]]*\]\()(\.{1,2}/[^)\s]+)(\))")
FENCE = re.compile(r"^(```|~~~)")


def front_matter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.index("\n---", 4)
    meta = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("["):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass
        elif len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        meta[key.strip()] = value
    return meta, text[end + 4:].lstrip("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("post")
    parser.add_argument("--canonical", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--asset", action="append", default=[], help="RELATIVE=URL, repeatable")
    parser.add_argument("--footer", default="Originally published on [my blog]({url}).")
    args = parser.parse_args()

    if not args.canonical.startswith("https://"):
        print("--canonical must be an https URL", file=sys.stderr)
        return 2
    assets = dict(a.split("=", 1) for a in args.asset)
    meta, body = front_matter(pathlib.Path(args.post).read_text())

    out_lines, unmapped, in_code = [], [], False
    for line in body.split("\n"):
        if FENCE.match(line.lstrip()):
            in_code = not in_code
        elif not in_code:
            def swap(m):
                if m.group(2) not in assets:
                    unmapped.append(m.group(2))
                    return m.group(0)
                return m.group(1) + assets[m.group(2)] + m.group(3)
            line = IMAGE.sub(swap, line)
        out_lines.append(line)
    if unmapped:
        print("relative images without --asset: " + ", ".join(sorted(set(unmapped))), file=sys.stderr)
        return 2

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    footer = "*" + args.footer.format(url=args.canonical) + "*"
    (out / "body.md").write_text("\n".join(out_lines).rstrip("\n") + "\n\n" + footer + "\n")
    (out / "meta.json").write_text(json.dumps({
        "title": meta.get("title", ""),
        "description": meta.get("description", ""),
        "tags": meta.get("tags", []),
        "cover": meta.get("cover", ""),
        "canonical_url": args.canonical,
    }, indent=2, ensure_ascii=False) + "\n")
    print(out / "body.md")
    print(out / "meta.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
