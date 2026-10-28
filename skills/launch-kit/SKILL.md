---
name: launch-kit
description: "Trigger: launch kit, prepare a launch, launch assets, taglines, gallery images. Build the asset kit every launch channel reads from."
license: MIT
metadata:
  author: alvaldes
  version: "0.1.0"
---

## Activation Contract

Use before launching a tool, or when another launch skill finds `docs/launch/<slug>/kit.md` missing or incomplete.

## Hard Rules

- Every fact comes from the project: README, code, release notes, the canonical post. Mark anything inferred _(assumption)_ and ask about it.
- Do not write the problem or comparison in a voice the maker has not used. Quote or adapt their own text (README, post); if there is none, leave a draft and flag it for rewriting.
- Never claim a competitor's price, license or status without a source; put the source next to the claim.
- The canonical post URL must not redirect: check with `curl -sIL` and record the final URL.
- Public asset URLs must load without a login: check each with `curl -sI`.

## Decision Gates

| Situation | Action |
|---|---|
| No kit yet | Copy `assets/kit-template.md` to `docs/launch/<slug>/kit.md` |
| Source images exist | Run `scripts/make-assets.sh` (ImageMagick 7) into `docs/launch/<slug>/assets/` |
| No `magick` | Ask the user to install it (`brew install imagemagick`); list the sizes needed meanwhile |
| Repo has no topics | Propose them; set with `gh repo edit <repo> --add-topic a,b` only after a yes |
| A required fact is unknown | Leave it under **Gaps**; do not guess |

## Execution Steps

1. Read the README, release notes, license, the canonical post and existing launch notes.
2. Fill **Identity** and **Copy**; keep the tagline under 60 characters and the short description to one sentence ending with a period.
3. Generate images: `scripts/make-assets.sh --out docs/launch/<slug>/assets --icon <1024px icon> --cover <cover> <screenshots in display order>`. Put the screenshot that shows the tool in action first.
4. Verify the canonical URL and every public asset URL.
5. List **Gaps**: missing assets, unverified claims, gates the maker must clear.

## Output Contract

Return the kit path, the generated files with their sizes, the verified URLs, and the gaps.

## References

- `../../references/launch-folder.md`: where launch files live.
- `../../references/channels.md`: asset sizes per channel.
- `scripts/make-assets.sh`: image generation; `--help` for options.
