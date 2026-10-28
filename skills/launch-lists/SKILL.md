---
name: launch-lists
description: "Trigger: awesome list, add to awesome-mac, open-source-mac-os-apps, list PR. Add a tool to curated GitHub lists with one PR per list."
license: MIT
metadata:
  author: alvaldes
  version: "0.1.0"
---

## Activation Contract

Use when the user wants a tool added to a curated GitHub list (awesome-mac, open-source-mac-os-apps or a similar awesome list).

## Hard Rules

- Read the list's CONTRIBUTING and PR template first; they override this skill. Check the list still accepts public PRs: `gh api repos/<owner>/<repo> -q .pull_request_creation_policy` must not be `collaborators_only`, and recent issues must not announce a closure.
- Search open and closed PRs and the list itself for the tool before editing: `gh pr list -R <repo> --state all --search "<name> in:title"`.
- One PR per list per tool. Change only the lines for this tool.
- Pick the category by the closest comparable apps already in the list, not by keyword alone. Follow each file's own structure, even when translations differ.
- Copy comes from `docs/launch/<slug>/kit.md`; descriptions are one sentence ending with a period.
- Forking, pushing and opening the PR are public actions: show the diff and the PR body, then ask before each.
- Work in a clone outside temp folders; never in `/tmp`.

## Decision Gates

| List | How |
|---|---|
| jaywcjlove/awesome-mac | One line in `README.md`, `README-zh.md`, `README-ja.md`, `README-ko.md`; insert with `scripts/insert-list-line.py` per file and section; icons as the section uses them |
| serhii-londar/open-source-mac-os-apps | Write `entry.json`, append with `scripts/add-json-entry.py applications.json entry.json`; categories from `categories.json` |
| iCHAIT/awesome-macOS | Closed to public submissions (2026-10-27); stop and tell the user |
| Another awesome list | Read its rules; use `insert-list-line.py` for Markdown lists |

## Execution Steps

1. Check the gates above and the duplicates search.
2. `gh repo fork <repo> --clone=false`, then `git clone --depth 1` the fork and `git switch -c add-<slug>`.
3. Edit with the scripts; confirm `git diff --stat` touches only the intended files and lines.
4. Validate: JSON parses; Markdown lines sit inside the right section, alphabetical.
5. Commit with a Conventional Commit message; write the PR body from the repo's template.
6. Ask, then push and run `gh pr create -R <repo> --head <user>:add-<slug> --title "Add <Name>" --body-file <body>`.
7. Record the PR in the tracker (launch-tracker).

## Output Contract

Return, per list: category chosen and why, the diff, the PR URL or the reason it was skipped.

## References

- `../../references/channels.md`: list formats and closures.
- `scripts/insert-list-line.py`: exit 1 on duplicates, 2 on bad input.
- `scripts/add-json-entry.py`: keeps the file's formatting; exit 1 on duplicates.
