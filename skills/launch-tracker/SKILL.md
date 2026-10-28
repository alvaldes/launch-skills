---
name: launch-tracker
description: "Trigger: launch tracker, where is it published, launch status, record a submission. Keep the table of channels, statuses and links for a tool's launch."
license: MIT
metadata:
  author: alvaldes
  version: "0.1.0"
---

## Activation Contract

Use when the user wants to start, update or review the record of where a tool is published: after any submission, post, PR or rejection, or when they ask what is left.

## Hard Rules

- The tracker lives at `docs/launch/<slug>/tracker.md` in the launched project (see `references/launch-folder.md`).
- Record only what was observed: a live URL, a PR number, a confirmation page. If the user reports a post you cannot see, record it as reported and say it is unverified.
- Never delete a row; change its status and note why.
- Dates are absolute (`YYYY-MM-DD`), never "yesterday".
- One row per channel. Use the statuses listed in the template.

## Decision Gates

| Situation | Action |
|---|---|
| No tracker yet | Copy `assets/tracker-template.md`, fill `{NAME}` and `{DATE}` |
| A URL is given | Check it loads (`curl -sIL`, or the browser for pages behind a login) before marking `published` |
| A PR is given | Read its state with `gh pr view <n> -R <repo> --json state,mergedAt` |
| A gate has a reopening date | Add it under **Waiting** |
| User asks "what is left" | List channels from `references/channels.md` that have no row, grouped by level |

## Execution Steps

1. Find or create the tracker.
2. Apply the change the user reported or the skill just completed.
3. Refresh stale rows when asked: PR states, review queues, cooldown dates.
4. Show the changed rows.

## Output Contract

Return the tracker path, the rows added or changed, anything left unverified, and the next gate that opens.

## References

- `../../references/launch-folder.md`: where launch files live.
- `../../references/channels.md`: the channel list and their gates.
