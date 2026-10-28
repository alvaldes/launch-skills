---
name: launch-cross-post
description: "Trigger: cross-post, republish blog post, Dev.to, Hashnode, Medium, canonical URL. Republish a blog post on article platforms as drafts with the canonical link."
license: MIT
metadata:
  author: alvaldes
  version: "0.1.0"
---

## Activation Contract

Use when the user wants a post from their own site republished on Dev.to, Hashnode or Medium without losing search credit.

## Hard Rules

- The canonical URL is the final URL of the original post: check with `curl -sIL`; it must answer 200 without redirects. Every copy sets it.
- Prepare the body with `scripts/prepare-article.py`; never hand-edit image links. Map every relative image to a public URL that loads (`curl -sI`).
- Save as draft first and show the preview. Publish only after an explicit yes for that platform.
- The user signs in; never type credentials. Use the available browser automation (for example ego-browser or Claude in Chrome); if there is none, give the user field-by-field values.
- Do not tick AI-disclosure options for the user; ask.

## Decision Gates

| Platform | How |
|---|---|
| Dev.to | New post. Editor ignores front matter: fill title, cover (1000×420), up to 4 tags (commit each with a real comma key press), body; canonical in **Advanced Options** → Save Draft |
| Hashnode | Needs a publication first (ask for its name and subdomain). Markdown mode; cover 1600×840; subheading; header **Publish** opens Draft settings → Discovery: tags, SEO description, "Are you republishing?" canonical; final Publish is inside |
| Medium | The user imports with **Stories → Import a story** and the canonical URL. Afterwards: replace tables with lists, remove any site suffix the importer added to the title |
| Platform not listed | Read its editor first; same rules |

## Execution Steps

1. Read `docs/launch/<slug>/kit.md` for the canonical URL, cover and tags.
2. `scripts/prepare-article.py <post.md> --canonical <url> --out docs/launch/<slug>/cross-post --asset ./img.webp=<public url> ...`
3. For each platform: open the editor, fill fields from `meta.json` and `body.md`, save the draft, check the preview (images, tables, code blocks).
4. Ask to publish. After publishing, verify the canonical: Dev.to `GET https://dev.to/api/articles/<user>/<slug>`; others, read `link[rel=canonical]` on the public page.
5. Record each URL with launch-tracker.

## Output Contract

Return per platform: draft or public URL, canonical verified or not, and anything the user must fix by hand.

## References

- `../../references/channels.md`: platform specifics.
- `scripts/prepare-article.py --help`: body and metadata builder; exit 2 on unmapped images.
