#!/usr/bin/env python3
"""Check a launch draft against a channel's mechanical rules.

Usage: check-draft.py DRAFT.md --channel {x,threads,linkedin,reddit,reddit-pcp,show-hn,product-hunt}

X drafts separate thread posts with a line containing only '---'. Show HN drafts start with 'title: ...'.
Exit codes: 0 no problems, 1 problems listed on stdout, 2 bad input.
"""
import argparse
import pathlib
import re
import sys

LIMITS = {"x": 280, "threads": 500, "linkedin": 3000}
DOWNLOAD = re.compile(r"https?://\S+\.(dmg|zip|pkg|exe)\b", re.I)


def problems(text, channel):
    found = []
    if "—" in text:
        found.append(f"em dash found {text.count(chr(0x2014))} time(s): communities flag it as AI-written; rewrite the sentence")
    if channel == "x":
        posts = [p.strip() for p in re.split(r"^\s*---\s*$", text, flags=re.M) if p.strip()]
        for n, post in enumerate(posts, 1):
            if len(post) > LIMITS["x"]:
                found.append(f"post {n}: {len(post)}/{LIMITS['x']} characters")
    elif channel in LIMITS:
        if len(text.strip()) > LIMITS[channel]:
            found.append(f"{len(text.strip())}/{LIMITS[channel]} characters")
    if channel == "reddit-pcp":
        for part in ("Problem:", "Comparison:", "Pricing:"):
            if part not in text:
                found.append(f"missing '{part}' (PCP format)")
        for m in DOWNLOAD.finditer(text):
            found.append(f"direct download link ({m.group(0)}): link the website instead of a .{m.group(1)}")
    if channel == "show-hn":
        first = text.strip().splitlines()[0] if text.strip() else ""
        if not first.lower().startswith("title: show hn:"):
            found.append("first line must be 'title: Show HN: ...'")
        elif len(first) - len("title: ") > 80:
            found.append(f"title is {len(first) - len('title: ')}/80 characters")
    if channel == "product-hunt":
        m = re.search(r"^tagline:\s*(.+)$", text, re.M)
        if not m:
            found.append("missing 'tagline:' line")
        elif len(m.group(1).strip()) > 60:
            found.append(f"tagline is {len(m.group(1).strip())}/60 characters")
    if re.search(r"\b(upvote|vote for)\b", text, re.I) and channel in ("show-hn", "product-hunt", "reddit", "reddit-pcp"):
        found.append("asks for votes: not allowed on this channel")
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("draft")
    parser.add_argument("--channel", required=True)
    args = parser.parse_args()
    channels = {"x", "threads", "linkedin", "reddit", "reddit-pcp", "show-hn", "product-hunt"}
    if args.channel not in channels:
        print(f"unknown channel; use one of: {', '.join(sorted(channels))}", file=sys.stderr)
        return 2
    found = problems(pathlib.Path(args.draft).read_text(), args.channel)
    for p in found:
        print(f"- {p}")
    if not found:
        print("ok")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
