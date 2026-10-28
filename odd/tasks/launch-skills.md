Objective: publish the launch playbook as an open-source Claude Code plugin of skills, tested, then announce it with a blog post on the portfolio.
Branch: `feat/launch-skills` in `alvaldes/launch-skills` (new repo); blog post on a branch in `portfolio`. Delivery: ask-on-risk; pushing, the public repo and merges are the user's decisions.
Test runner: `claude plugin validate` and `claude plugin eval` (evals/), plus shell checks for bundled scripts.

## Specs

- S1. Skills automate the launch work defined in `portfolio/docs/launch-playbook.md`: "crea las skills y cuando ya todo esté listo y probado crea un artículo en el blog de portfolio hablando de estas skills".
- S2. Distribution (user choice, 2026-10-28): "Repo plugin": a new public repo `alvaldes/launch-skills` structured as a Claude Code plugin installable with `/plugin`, with a `skills/` folder of standard `SKILL.md` files reusable by other agents, a README linking to the blog, MIT license.
- S3. The six skills from the playbook's "Toward skills" section: launch-kit, launch-cross-post, launch-lists, launch-directories, launch-community-drafts, launch-tracker.
- S4. Every skill stops before the final public action (publish, submit, open PR, push) and asks; sign-ins, payments and CAPTCHAs stay with the human.
- S5. "listo y probado": each skill is validated (`claude plugin validate`) and exercised by eval cases or a recorded dry run; bundled scripts have tests.
- S6. A blog post on the portfolio about these skills, as a hook toward the community interested in Claude skills: "que las personas al ser accedan a mi portfolio a través de las skills".
- S7. Assumption: skills are generic (any tool), not hardcoded to JUMP or to the author; per-launch data lives in the target project. Channel rules ship as a local reference copied from the playbook.

## Tasks

| ID | Specs | Route | Status | Evidence |
|---|---|---|---|---|
| T1 | S2, S7 | inline | pending | Scaffold: plugin.json, marketplace.json, README, LICENSE, channel reference |
| T2 | S3, S4 | inline | pending | launch-tracker |
| T3 | S3, S4 | inline | pending | launch-kit |
| T4 | S3, S4 | inline | pending | launch-lists (+ script and tests) |
| T5 | S3, S4 | inline | pending | launch-cross-post |
| T6 | S3, S4 | inline | pending | launch-directories |
| T7 | S3, S4 | inline | pending | launch-community-drafts |
| T8 | S5 | inline | pending | validate + evals + dry run on a sample project |
| T9 | S6 | inline | pending | Portfolio blog post (en/es) |

## Log

- L1 (2026-10-28, user): "crea las skills y cuando ya todo esté listo y probado crea un artículo en el blog de portfolio hablando de estas skills porque mi objetivo también es publicar estas skills como otra contribución y de esta forma también que las personas al ser accedan a mi portfolio a través de las skills. Sería un gancho hacia una comunidad que actualmente está muy interesada en todo este tema de las skills de cloud y demás"
- L2 (2026-10-28, user choice): distribution "Repo plugin (Recommended)".
- L3: plugin layout confirmed from an installed plugin (brag 0.4.0): `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` with `"source": "./"`, `skills/<name>/SKILL.md`. The CLI offers `claude plugin validate` and `claude plugin eval`.
- L4: route is inline for every task; no writer trigger (units share conventions and are small).
- L5: Engram mirror pending: `mem_save` returned `ambiguous_project` (the MCP process resolves from `~/Developer`, offering only awesome-mac and storico). Resync when it resolves `launch-skills`.
