# Guides overview

This directory collects human-readable guides for planning, running, and synthesizing park cleanups. Most people can ignore the full repo structure and just grab the guide that matches what they are doing.

## Park-specific cleanup guides

- **`mission-dolores-cleanup-guide.md`** – how to run a Mission Dolores cleanup in San Francisco. Includes suggested meeting spots, target areas, and notes about local politics and fragility.
- **`devoe-park-cleanup-guide.md`** – how to run a Devoe Park cleanup in the Bronx. Focuses on access points, likely litter zones, and how to coordinate with local volunteers.

## Intake and local rules

- **`google-form-intake.md`** – how our Google Form is structured, how responses land in the private Sheet, and what agents should do with new rows (at an aggregate level, with no PII in this repo).
- **`google-form-integration-plan.md`** – how the form, Sheet, monitoring scripts, and counts-only verification artifact fit together.
- **`sf-group-volunteer-requirements.md`** – San Francisco Parks & Recreation expectations for group volunteer events, especially relevant for Mission Dolores.

## Day-of operations at the park

- **`day-of-operations-checklist.md`** – a short, printable checklist for the person physically at the park on cleanup day. Covers safety, before/during/after photos, bag counts, and same-day notes. This is the main "day-of" document referenced from the root `README.md`.

## Post-event synthesis docs

There are two complementary post-event synthesis guides:

- **`post-event-synthesis-feb-14-15.md`** – a **weekend-specific plan** for the Feb 14–15, 2026 cleanups at Mission Dolores (SF) and Devoe Park (Bronx). It assumes:
  - Evidence folders exist at:
    - `evidence/mission-dolores/2026-02-14/`
    - `evidence/devoe-park-bronx/2026-02-15/`
  - Each folder contains `report.md`, `retrospective.md`, and vetted photos under `before/`, `during/` (optional), and `after/`.
  - Aggregate signup context comes from `monitoring/volunteer_counts_verification.json`.

  It walks through:
  - Verifying the evidence folders and reports.
  - Creating/finalizing retrospectives.
  - Updating `candidates/mission-dolores.md` and `candidates/devoe-park-bronx.md` with a “Feb 2026 cleanup” history entry.
  - Comparing pre-weekend signups to actual attendance (optionally using `analysis/feb-14-15-signups-vs-attendance.md`).
  - Drafting an internal weekend summary under `analysis/` (for example, `analysis/feb-14-15-weekend-summary.md`).

- **`post-event-synthesis-guide.md`** – a **generic, privacy-first synthesis guide** suitable for any cleanup, not just Feb 14–15. It assumes you already have an evidence folder (under `evidence/<park-slug>/<YYYY-MM-DD>/`) and helps you:
  - Pick a small set of before/after photos.
  - Update the event’s `report.md` with a simple, counts-only summary.
  - Capture a short reflection and next steps.

For future cleanups, start with `post-event-synthesis-guide.md`. For the Feb 14–15 weekend specifically, use `post-event-synthesis-feb-14-15.md` which builds on top of the same evidence and retrospective patterns.
