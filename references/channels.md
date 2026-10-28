# Launch channels

What each channel accepts, what it requires and how a submission works. Every rule was read on the site itself in October 2026. Rules change: before acting on a channel, re-read its rules page and flag any difference to the user.

Automation levels:

- `CLI`: done with `gh` or a public API.
- `browser`: a form filled with the available browser automation.
- `draft`: text prepared for the human, who posts it.
- `manual`: the human does it; the skill only checks it against the rules.

Never press the final publish, submit, schedule or merge control without an explicit yes in that turn. Sign-ins, payments and CAPTCHAs are always the human's.

## Asset kit

| Asset | Spec | Used by |
|---|---|---|
| Name | Official spelling, no tagline | Everywhere |
| Tagline | One line, under 60 characters, says what it does | Product Hunt, Indie Hackers, AlternativeTo |
| Short description | One sentence, ends with a period | Awesome lists, AlternativeTo |
| Long description | 200 to 500 words: problem, how it works, platform, price, license | AppAddict, AlternativeTo, Product Hunt, MacUpdate |
| Comparison | 1 or 2 named competitors and what is better, honestly | r/macapps, Product Hunt, Show HN |
| Icon | Transparent PNG, 512×512 or larger | MacUpdate, AlternativeTo, Indie Hackers, lists |
| Screenshots | PNG or JPG; the first one shows the tool in action | Every directory |
| Gallery images | 1270×760 PNG | Product Hunt |
| Article covers | 1000×420 (Dev.to), 1600×840 (Hashnode) | Article cross-posts |
| Canonical post | A write-up on the maker's own site | Cross-posts, iOS Dev Weekly |
| Raw asset URLs | Icon and screenshots reachable without a login | open-source-mac-os-apps, Indie Goodies |
| Repo metadata | Description, homepage, topics | GitHub search |

The canonical URL must be the final URL, not one that redirects. Check it with `curl -sIL <url>`.

Write in the maker's voice. r/macapps, r/opensource and several lists remove or ban text that reads as AI-written; em dashes are a known trigger.

## Owned and social

| Channel | Fit | Format | Level |
|---|---|---|---|
| Own blog | Anything; the canonical source | Post with cover image | CLI |
| GitHub repo | Open source | `gh repo edit <repo> --add-topic a,b`; description and homepage | CLI |
| LinkedIn | Anything | Text plus a PDF carousel; the link goes in the first comment, links in the post cut reach | draft |
| X | Anything | 280 characters per post; carousel 2 to 6 cards; thread with the link last. Do not tag competitors | draft |
| Threads | Anything | 500 characters; attach images, text-only posts get less attention | draft |
| Instagram | Visual tools | 4:5 carousel at 1080×1350; links in captions are not clickable; at most 5 hashtags | draft |

Profile bios are part of the launch: visitors read them.

## Article cross-posts

All three carry the same article; the canonical URL keeps search engines crediting the original.

### Dev.to
- Gate: an account.
- Format: title, up to 4 tags, cover 1000:420, Markdown body, canonical URL in **Advanced Options**. The default editor ignores front matter, so fill each field. Tags commit on a real comma key press.
- Verify: `GET https://dev.to/api/articles/<user>/<slug>` returns `published_at` and `canonical_url`.
- Level: browser (CLI with a Dev.to API key).

### Hashnode
- Gate: an account and a publication (blog); the subdomain is chosen once.
- Format: Markdown mode, cover 1600×840, subheading; tags, SEO description and canonical URL ("Are you republishing?") in **Draft settings → Discovery**. The header Publish button opens Draft settings; the final Publish is inside it.
- Level: browser.

### Medium
- How: **Stories → Import a story** with the canonical URL; the importer sets the canonical and the original date.
- Gotchas: no tables (replace them with a list); the importer copies the page `<title>`, so a site suffix lands in the story title. Fix the title after importing.
- Level: draft plus a manual import.

## Launch communities

### Product Hunt
- Format: name, tagline, description, product categories (up to 3), launch tags (up to 3), pricing, links, logo, gallery (the first image is the share preview), optional video, maker's first comment. Choose **I made this**.
- How: Submit → product URL → the draft autosaves → **Schedule launch** (launches start at 12:01 a.m. Pacific).
- Rules: do not ask for upvotes; invite people to look.
- Level: browser for the draft; the human schedules.

### r/macapps
- Fit: macOS apps.
- Gate: 10 karma earned in r/MacApps, rules marked as read, verified email. Main-feed posts need Tier 1 (Mac App Store, or a repo with one year of history or 100+ stars) or Tier 2 (a real-identity portfolio with LinkedIn and contact details, and an app website with a Privacy Policy and Terms of Service). Everyone else posts in the monthly megathread.
- Format: PCP: Problem, Comparison (name 1 or 2 competitors), Pricing with amounts and a link (no direct .dmg or .zip). Open-source titles start with `[OS]`. Flair Free for free apps.
- Rules: one promotion per developer every 30 days, counted even if removed; disclose that you are the developer.
- Level: draft.

### r/opensource
- Gate: an account with history; self-promotion under about 10% of posts; no drive-by posting. The repo needs an OSI license file.
- Rules: "All AI-generated content is low-effort and ban worthy"; flair Promotional.
- Level: manual.

### Hacker News (Show HN)
- Fit: something people can run, made by the poster, non-trivial. Link the repo, not a landing page.
- Gate: new accounts are redirected to `/showlim`.
- Format: title starting with `Show HN:`, URL, and text with the backstory (it shows at the top of the thread). Do not ask for upvotes.
- Level: draft.

### Indie Hackers
- Gate: posts are open to established members; product pages to everyone.
- Format (product page): name, tagline (60 characters), website, square logo of 200×200 or larger; then motivation (220 characters), start date, founder skillset, founders, employees, business model, funding, commitment, platforms and tags, all required to appear in the directory.
- Level: browser.

## Directories

### AlternativeTo
- Format: name, website, short and full description (no links), pricing, license model and license, source URL, tags, features, platforms with notes, author with country and website, icon, screenshots with captions.
- How: submit, then add existing apps as alternatives; without alternatives the app barely shows up.
- Gotchas: the free review queue can take a very long time; paid priority review exists. The human decides whether to pay.
- Level: browser.

### MacUpdate (macOS)
- Format: name, developer, download URL, product page, support URL, version, price; short and long description, version changes, system requirements; one transparent PNG icon (512×512 preferred); up to 5 PNG or JPG screenshots under 8 MB; comments for reviewers.
- Gotchas: mention an unnotarized build in the comments.
- Level: browser.

### Indie Goodies, Open Source Mac Apps (macOS)
- Format (Airtable form): name, description, link, icon URL, screenshot URL, category.
- Level: browser.

### MacMenuBar (macOS)
- Fit: apps that live in the menu bar, where removing the icon would break how people use them.
- Gate: an email address on the app's own domain; free mail providers are refused and the submit button does not appear.
- Format: name, URL, optional YouTube demo, pricing, message, at least 3 screenshots showing the app in the actual menu bar.
- Level: browser.

### Applite (macOS)
- Fit: apps in the official Homebrew cask catalog only; no submission form.
- Gate: an accepted cask in `homebrew/cask` (passes Gatekeeper, so notarized, and meets Homebrew's notability metrics).

## Curated lists on GitHub

### awesome-mac (jaywcjlove/awesome-mac)
- Format: one line per app in `README.md`, `README-zh.md`, `README-ja.md` and `README-ko.md`, in the closest category by comparable apps, alphabetical, one-sentence description, then the icons used by the section: `[![Open-Source Software][OSS Icon]](<repo>) ![Freeware][Freeware Icon] ![Native App][Native Icon]`. One PR per app; the PR body follows the repo's template.
- Level: CLI.

### open-source-mac-os-apps (serhii-londar/open-source-mac-os-apps)
- Format: one entry appended to `applications.json` (never `README.md`): `title`, `short_description` ending with a period, `categories` (ids from `categories.json`), `repo_url`, `icon_url`, `screenshots`, `official_site`, `languages`. One PR per app with the repo's template.
- Level: CLI.

### awesome-macOS (iCHAIT/awesome-macOS)
- Closed to public submissions since 2026-10-27; pull requests are limited to collaborators. Skip it unless that changes.

## Newsletters and niche media

| Channel | Fit | How | Level |
|---|---|---|---|
| AppAddict | Independent Mac apps | "Submit your app for review" form: developer, contact email, app name, 200 to 500 word description, download link, NFR license yes/no (for a free app answer No and say it is free) | browser |
| iOS Dev Weekly | Content for Apple-platform developers: send the technical post, not the app page | `suggest.iosdevweekly.com`: name, email, link, who wrote it, blog post yes/no, Swift library yes/no, why | browser |
| Brett Terpstra | Keyboard and productivity tools | Email only, short and personal | draft |
| Daring Fireball | Skip: the contact page is for feedback, not pitches | | |
| Swift Weekly Brief | Skip: inactive since June 2022 | | |

## Accounts to warm up

Several gates open only for accounts with history. Before a launch, the maker participates genuinely, without promoting, on Reddit (r/macapps, r/opensource), Hacker News and Indie Hackers.

## Launch order

1. Asset kit, canonical post, repo topics.
2. Social posts, written by the maker.
3. Article cross-posts with the canonical URL.
4. Lists and directories.
5. Communities, respecting each gate; Product Hunt scheduled.
6. Newsletters.
7. Every link and status recorded in the tracker.
