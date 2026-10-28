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
| T1 | S2, S7 | inline | done | 2009fad; `claude plugin validate . --strict --profile directory` passes |
| T2 | S3, S4 | inline | done | f438725 |
| T3 | S3, S4 | inline | done | bbca4fb; tests/make-assets.test.sh 10/10 |
| T4 | S3, S4 | inline | done | e3a332f; RED 8 fail → GREEN 10/10; output identical to the manual PRs #1837 and awesome-mac #3995 |
| T5 | S3, S4 | inline | done | 3766577; RED 6 fail → GREEN 7/7; body identical to the published Dev.to/Hashnode cross-post |
| T6 | S3, S4 | inline | done | a5a98bf |
| T7 | S3, S4 | inline | done | dd09200; RED 7 fail → GREEN 8/8; published r/macapps, Threads, X and Show HN texts pass |
| T8 | S5 | inline | done | `claude plugin eval . --ablation none --allow-tools Write Edit Bash`: 3/3 cases, 10/10 graders (run-4, $0.55); 25 unit tests + 10 shell checks |
| T9 | S6 | inline | done | portfolio ca45f05 on feat/launch-skills-post; build 0 errors, 0 warnings |

## Log

- L1 (2026-10-28, user): "crea las skills y cuando ya todo esté listo y probado crea un artículo en el blog de portfolio hablando de estas skills porque mi objetivo también es publicar estas skills como otra contribución y de esta forma también que las personas al ser accedan a mi portfolio a través de las skills. Sería un gancho hacia una comunidad que actualmente está muy interesada en todo este tema de las skills de cloud y demás"
- L2 (2026-10-28, user choice): distribution "Repo plugin (Recommended)".
- L3: plugin layout confirmed from an installed plugin (brag 0.4.0): `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` with `"source": "./"`, `skills/<name>/SKILL.md`. The CLI offers `claude plugin validate` and `claude plugin eval`.
- L4: route is inline for every task; no writer trigger (units share conventions and are small).
- L5: Engram mirror pending: `mem_save` returned `ambiguous_project` (the MCP process resolves from `~/Developer`, offering only awesome-mac and storico). Resync when it resolves `launch-skills`.
- L6: make-assets tests were written with the script, not before it (no RED observed for T3). Lists, cross-post and draft checker followed RED → GREEN.
- L7: real-data dry runs replace a sample project: each script re-ran on JUMP's actual inputs and matched what was published by hand.
- L8: eval run 1 scored 0.67/0.75/1. Causes: Bash was missing from the cases' `allowed_tools` (the CLI grant alone does not enable it) and the closed-list rubric was ambiguous although the answer was right. Pattern grants such as `Bash(python3 *)` still left Bash unused; plain `Bash` (OS-sandboxed) works. Run 4: all pass.
- L9: not exercised end to end by evals: launch-cross-post and launch-directories need signed-in browser sessions. Their scripts are tested and every step was performed by hand for JUMP on 2026-10-28.
- L10: pending human decisions: create the public GitHub repo `alvaldes/launch-skills` and push; merge and push the portfolio post (it links to the repo, so the repo goes public first).
