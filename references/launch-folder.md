# Launch folder

Every launch keeps its working files inside the project being launched, in `docs/launch/<slug>/`, where `<slug>` is the tool's name in kebab case.

```text
docs/launch/<slug>/
├── kit.md        # the asset kit: names, taglines, descriptions, comparison, URLs (launch-kit)
├── assets/       # generated icon, gallery and cover images (launch-kit)
├── drafts/       # posts and community texts for the maker to edit (launch-community-drafts)
└── tracker.md    # where the tool is published, status and links (launch-tracker)
```

Rules:

- Read `kit.md` before writing anything for a channel; never invent facts that are not in it or in the project.
- Paths inside `kit.md` are relative to the project root.
- If the project keeps launch notes elsewhere, the user's location wins; record it at the top of `kit.md`.
