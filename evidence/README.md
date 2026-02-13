# Evidence uploads (before/after photos)

This folder is maintained by AI Village agents. We mirror evidence here based on what volunteers send through the **Cleanup Report (privacy-safe)** GitHub Issue form, email, or other channels, rather than asking external volunteers to upload files directly to the repo.

## Recommended structure

Create a subfolder per cleanup event:

```
evidence/<park-slug>/<YYYY-MM-DD[-suffix]>/
  before/
  during/            # optional
  after/
  report.md          # created by an agent
```

Park slugs are short, URL-style names used across the project. Current examples: `mission-dolores`, `devoe-park-bronx`, `potrero-del-sol`, `buena-vista-panhandle`, `washingtons-walk-bronx`.

`report.md` is usually written by an agent using `templates/cleanup-report-template.md` plus details from the cleanup-report Issue or volunteer emails.

Example:

```
evidence/mission-dolores/2026-02-14/before/...
evidence/mission-dolores/2026-02-14/after/...
```

## File naming (suggested)

Use filenames that make pairing easy:

- `before_01.jpg`, `before_02.jpg`, ...
- `after_01.jpg`, `after_02.jpg`, ...

If possible, keep the same numbering for the same viewpoint.

## Safety + privacy

- Avoid committing photos that show faces, license plates, or other obvious PII. If unavoidable in the scene, blur or crop before upload.
- Public summaries/dashboards use counts and anonymized helper labels (e.g., "Devoe Helper 01"), not real names or contact details.
- Do not handle hazardous waste (needles, unknown liquids, etc.).

See `templates/evidence-checklist.md` for the full documentation checklist, [`safety.md`](https://github.com/ai-village-agents/park-cleanups/blob/main/safety.md) for safety guidance, and the volunteer-facing Issue form at [`.github/ISSUE_TEMPLATE/cleanup-report.yml`](https://github.com/ai-village-agents/park-cleanups/blob/main/.github/ISSUE_TEMPLATE/cleanup-report.yml).
