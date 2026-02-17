# Contributing

Thanks for helping keep our park cleanup docs organized and safe for volunteers. Most contributions are simple additions to candidates, guides, or evidence; please keep changes focused and reproducible.

## Core Principles

- **Evidence**: Ground updates in verifiable observations or logs; cite sources or attach supporting evidence where possible.
- **Privacy**: Minimize personal data collection and exposure; default to aggregate, de-identified information.
- **Non-Carceral**: Avoid language or actions that could facilitate punitive surveillance; design for community support over enforcement.
- **Safety**: Prioritize volunteer and community safety in process and language; document hazards and mitigations clearly.

- Keep files small, plain-text, and versioned (no giant binaries). Charts, flyers, or infographics should already be exported assets under `assets/` or `flyers/`.
- Follow the project structure in `README.md` when adding candidate parks, evidence folders, or runbooks.
- Prefer aggregated counts and anonymized summaries when describing volunteer activity. Helper IDs or agent handles are fine; personal contact details are not needed.

## Privacy and PII

We do not store volunteer phone numbers or email addresses in this repository. Keep everything aggregate (bag counts, dates, park areas, links to shared albums) and avoid committing sign-in sheets or screenshots with contact info. Continuous integration will block pull requests if it detects non-allowlisted emails or US phone numbers; sanitize files before pushing.

## Workflow

Create a feature branch from `main` (do not fork), push your changes, then open a pull request for review.
