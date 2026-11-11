# AI usage and human verification log

This log distinguishes AI assistance used during engineering from AI features included in the running application.

| Date | Activity | AI contribution | Human verification | Outcome |
|---|---|---|---|---|
| 2026-11-11 | Initial Flask troubleshooting | Suggested using Colab's iframe port helper and a server-readiness check | User ran the revised startup cell and confirmed the dashboard opened | User-confirmed working in Colab |
| 2026-11-11 | Project planning | Helped structure epics, user stories, tasks and acceptance criteria for Jira | Project scope was grounded in the supplied Flask prototype; unimplemented features were labelled as planned | Jira backlog created |
| 2026-11-11 | Repository organization | Prepared a Flask/template split, documentation, and automated test scaffolding | Reviewed the branch and workflow output; GitHub Actions executed the test suite | 10 tests passed in GitHub Actions; merged after review |
| 2026-11-11 | CI failure diagnosis | Analyzed the first Actions failure and identified the test import-path problem; changed the workflow to use `python -m pytest` | Verified the subsequent pull-request Actions run and test log | CI passed; initial failure and corrective action retained as case-study evidence |
| 2026-11-11 | SQLite persistence design | Proposed a request-scoped SQLite connection, parameterized queries, stable complaint IDs, and isolated temporary test databases | Pending: review implementation and execute the SQLite test suite in CI | Pending |

## Responsible-use rules
- AI output is a proposal, not proof of correctness.
- A human must review code and execute tests.
- Record errors, changes, and verification evidence.
- Do not place real student personal data or secrets in AI prompts.
- The application does not yet include an AI runtime feature. Any classifier or prioritization service is a proposed enhancement until implemented and evaluated.
