---
name: launch-community-drafts
description: "Trigger: Show HN, r/macapps post, Product Hunt launch, launch post, X thread, LinkedIn post. Draft community and social launch texts, checked against each channel's rules."
license: MIT
metadata:
  author: alvaldes
  version: "0.1.0"
---

## Activation Contract

Use when the user wants launch texts for communities (Reddit, Hacker News, Product Hunt, Indie Hackers) or social networks (LinkedIn, X, Threads).

## Hard Rules

- These are drafts for the maker to rewrite in their own voice. Several communities ban AI-written posts (r/opensource) or auto-remove them (r/macapps); say so with every draft.
- Facts come from `docs/launch/<slug>/kit.md` and the maker's own texts; quote their phrasing where it exists. Never invent anecdotes, numbers or competitor facts.
- Check each channel's gate before drafting (`references/channels.md`): account karma or age, cooldowns, main feed versus megathread. If the gate is closed, say when it opens and draft for the allowed place.
- Run `scripts/check-draft.py <draft> --channel <channel>` on every draft and fix what it reports.
- Never post, submit or schedule. The maker does, or the user says yes explicitly for that one action.
- Never ask for votes.

## Decision Gates

| Channel | Template | Check |
|---|---|---|
| r/macapps (main feed or megathread) | `assets/reddit-pcp.md` | `reddit-pcp` |
| Show HN | `assets/show-hn.md` | `show-hn` |
| Product Hunt | `assets/product-hunt.md` | `product-hunt` |
| LinkedIn, X, Threads | `assets/social.md` | `linkedin`, `x`, `threads` |
| r/opensource | No draft: the maker writes it; offer a rules check only | `reddit` |

## Execution Steps

1. Read the kit and any existing posts by the maker for voice.
2. Check the gate for each requested channel; re-read the live rules page when one is cited.
3. Fill the template into `docs/launch/<slug>/drafts/<channel>.md`.
4. Run the checker; fix and re-run until it prints `ok`.
5. Present each draft with its gate status and what the maker should personalize.

## Output Contract

Return per channel: draft path, checker result, gate status (open, megathread, blocked until a date), and the personalization notes.

## References

- `../../references/channels.md`: gates, formats and rules per channel.
- `scripts/check-draft.py --help`: mechanical checks (length, em dashes, PCP parts, direct downloads, Show HN title, vote requests).
