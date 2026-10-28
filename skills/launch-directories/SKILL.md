---
name: launch-directories
description: "Trigger: submit to directory, AlternativeTo, MacUpdate, Indie Hackers product, AppAddict, iOS Dev Weekly. Fill app directory and newsletter forms, stopping before submit."
license: MIT
metadata:
  author: alvaldes
  version: "0.1.0"
---

## Activation Contract

Use when the user wants a tool listed in app directories or suggested to newsletters through their web forms.

## Hard Rules

- Values come from `docs/launch/<slug>/kit.md` and its `assets/`. A required field that the kit lacks is a gap: ask, do not invent.
- Before filling, check the directory's fit and gate in `references/channels.md` (for example MacMenuBar needs an email on the app's own domain; Applite only lists official Homebrew casks). If it does not fit, say why and skip it.
- The user signs in; never type passwords. Fill forms with the available browser automation; if there is none, give field-by-field values.
- Stop before the final submit button: show what was filled and ask. Never pay: paid review or promotion options are the user's decision.
- Use a contact email the user has already made public, or ask for one.
- Mark claims you verified in code (for example "no network requests") and do not tick feature boxes you could not verify.

## Decision Gates

| Directory | Notes |
|---|---|
| AlternativeTo | After submitting, add existing apps as alternatives, or the listing stays nearly invisible. The free queue is slow; mention the paid option without choosing it |
| MacUpdate | Transparent PNG icon, up to 5 PNG/JPG screenshots; put first-run caveats (for example not notarized) in the reviewer comments |
| Indie Hackers | Product page first; then fill motivation, start date, founders, model, funding, commitment, platforms, tags so it appears in the directory |
| AppAddict | Review form; for a free app answer No to the NFR license and say it is free |
| iOS Dev Weekly | Suggest the technical post, not the app page |
| Indie Goodies | Icon and screenshot as public URLs |

## Execution Steps

1. Read the kit; list missing fields per directory.
2. For each directory: check fit and gate, open the form, fill it, screenshot or read back the values.
3. Ask before submitting; after submitting, read the confirmation page.
4. Record the result with launch-tracker, including queue or review status.

## Output Contract

Return per directory: submitted, skipped (reason) or blocked (gap), the confirmation text or URL, and any follow-up such as adding alternatives.

## References

- `../../references/channels.md`: fields, gates and gotchas per directory.
- `../launch-kit/SKILL.md`: how the kit and assets are produced.
