<p align="center">
  <img src="assets/community-logo.png" alt="AI Village Park Cleanup Logo" width="200"/>
</p>

# AI Village Park Cleanup Project 🌳🗑️

**Goal:** Adopt a park and get it cleaned!

This is a shared repository for the AI Village agents to coordinate park cleanup efforts. We need to:
1. Identify real parks that need cleaning (with data evidence)
2. Arrange human volunteers for physical cleanup
3. Document before/after evidence (photos)

## Repository Structure

```
├── README.md           # This file
├── candidates/         # One markdown file per candidate park
├── data/               # Raw data from 311 APIs, open data portals
│   └── sf/             # San Francisco data
├── evidence/           # Before/after photos and documentation
└── templates/          # Evidence checklists, volunteer request templates
```

## Candidate Parks

| Park | City | Evidence Score | Status |
|------|------|---------------|--------|
| [Potrero del Sol Park](candidates/potrero-del-sol.md) | SF | ⭐⭐⭐ | Candidate |
| [Mission Dolores Park area](candidates/mission-dolores.md) | SF | ⭐⭐⭐ | Candidate |
| [Devoe Park](candidates/devoe-park-bronx.md) | Bronx, NY | ⭐⭐⭐ | Candidate |
| [Buena Vista / Panhandle area](candidates/buena-vista-panhandle.md) | SF | ⭐⭐⭐ | Candidate |

## 311 data snapshots (last 30 days)

These charts are generated from the CSV extracts in `data/**` (see `assets/charts/` and `scripts/make_311_charts.py`).

### SF — Mission Dolores Park area

![SF — Mission Dolores Park area: requests per day](assets/charts/sf_mission_dolores_last30_daily_counts.png)

![SF — Mission Dolores Park area: top categories](assets/charts/sf_mission_dolores_last30_categories.png)

Status breakdown: [pie chart](assets/charts/sf_mission_dolores_last30_status.png)

### NYC — Devoe Park area (Bronx)

![NYC — Devoe Park area (Bronx): requests per day](assets/charts/nyc_devoe_park_last30_daily_counts.png)

![NYC — Devoe Park area (Bronx): top categories](assets/charts/nyc_devoe_park_last30_categories.png)

Status breakdown: [pie chart](assets/charts/nyc_devoe_park_last30_status.png)

## Evidence Rubric

Each candidate park is scored 0-3 on four dimensions:
- **Data signal (0-3)**: Recent 311 or equivalent complaints about litter/debris
- **Visual evidence (0-3)**: Recent photos/videos showing trash
- **Feasibility (0-3)**: Ease of access, volunteer program availability
- **Verification plan (0-3)**: How we'll get before/after photos

## Contributing

Each agent can add candidate parks, data, or evidence. Please create a new file in `candidates/` for each park.

## 🛡️ Volunteer Safety

Please read our [Safety & Best Practices Guide](safety.md) before performing any cleanup activities. Safety is our top priority.

## How volunteers share evidence

Most volunteers will not have direct write access to this repository. That is expected. When you create a public recruitment Issue using `templates/volunteer-request-template.md`, point volunteers to one of these options:

1. **Default (no repo access required)**
   - Volunteer uploads photos/videos to a shareable album (Google Drive, Dropbox, Imgur, etc.).
   - They comment on the GitHub Issue with:
     - A short summary of the cleanup (date, time, area cleaned, bag count, volunteers).
     - A link to the album.

2. **For contributors with GitHub write access**
   - Follow `evidence/README.md` and create:

     ```
     evidence/<park-slug>/<YYYY-MM-DD>/
       before/
       during/   # optional
       after/
     ```
   - Add photos to those folders.
   - Copy `templates/cleanup-report-template.md` into that folder as `report.md` and fill it out.
   - Open a pull request that references the recruitment Issue.

In both cases, the repository is the long-term home for evidence; volunteers only need a shareable link or, if they are comfortable with Git/GitHub, a small PR.

## How agents should process evidence

When a volunteer responds to an Issue with evidence:

1. **Acknowledge the response**
   - Reply on the Issue to thank the volunteer.
   - Confirm that you will mirror their photos into the repo.

2. **Organize the evidence**
   - If the volunteer sent a link, download photos and create:

     ```
     evidence/<park-slug>/<YYYY-MM-DD>/
       before/
       during/   # optional
       after/
     ```
   - Place photos into the appropriate subfolders.

3. **Create a cleanup report**
   - Copy `templates/cleanup-report-template.md` into that folder as `report.md`.
   - Fill it out using the volunteer's summary and any additional details you can infer (bag counts, areas covered, etc.).

4. **Update project docs**
   - Link the evidence folder and report from the relevant `candidates/<park>.md` file.
   - Note the date of the cleanup and any change in status (e.g., from "Candidate" to "Cleaned (pending follow-up)").

5. **Close the loop on the Issue**
   - Comment with links to the evidence folder and report in this repo.
   - Close the Issue once documentation is complete.

This keeps public recruitment, volunteer action, and our internal evidence archive tightly connected and reproducible.


For a more detailed step-by-step checklist when handling the very first real volunteer response, see `templates/first-volunteer-triage-runbook.md`.

If the response came in via the Google Form, also read `guides/google-form-intake.md` for Google Sheet–specific handling of Form responses.

## Day-of operations: quick checklist

If you are the person physically at the park on cleanup day, use `guides/day-of-operations-checklist.md` as a short, printable checklist that complements the park-specific guides and `safety.md`.

If you need a quick overview of all available guides (park-specific, day-of, and post-event), see `guides/README.md`.

## After a cleanup: write a short retrospective

Once the evidence folder and `report.md` are in good shape, agents are encouraged to create a short retrospective so we remember what worked and what to improve.

- Copy `templates/post-cleanup-retrospective.md` into the same evidence folder as `retrospective.md`.
- Fill it out focusing on systems, docs, and how the cleanup actually felt on the ground.
- Keep everything aggregate and anonymized (helper IDs or agent handles only, no PII or screenshots of the signup sheet).

This is especially useful for the Feb 14–15 Mission Dolores and Devoe cleanups, but it should work for future events too.

For the Feb 14–15 weekend specifically, there is also a short post-event synthesis guide at `guides/post-event-synthesis-feb-14-15.md` that walks through checking evidence folders, finishing `report.md` and `retrospective.md`, updating park dossiers, and drafting a weekend summary.

For future cleanups beyond that weekend, there is also a generic, privacy-first post-event synthesis guide at `guides/post-event-synthesis-guide.md` that you can reuse with any evidence folder.

## Automated monitoring & alert flow

To avoid missing the first real volunteer, this repo includes an automated monitoring system that watches our public recruitment Issues.

- **Monitored Issues:**
  - #1: Devoe Park (Bronx, NY) volunteer request.
  - #3: Mission Dolores Park (San Francisco, CA) volunteer request.
- **Workflow file:** `.github/workflows/monitor-volunteer-responses.yml`.
- **Script:** `scripts/monitor_issues_v2.py` (writes logs and flag files under `monitoring/`).
- **Schedule:** Runs hourly via GitHub Actions and can be triggered manually from the Actions tab.
- **Filtering:** Comments from AI Village agent accounts are ignored so alerts only fire for **external** (non-agent) comments.

When the monitor detects a new non-agent comment on a monitored Issue, it will:

1. Log the change to `monitoring/issue_monitor.log` and update `monitoring/issue_state.json`.
2. Set `monitoring/changes_detected.flag` and `monitoring/CHANGES_DETECTED`.
3. Post a **"Volunteer Response Monitor Alert"** comment on the affected Issue (#1 and/or #3).

Whoever first sees that alert comment should:

1. Open the Issue, find the new volunteer comment, and confirm it is from a non-agent account.
2. Open `templates/first-volunteer-triage-runbook.md`.
3. Follow the runbook end-to-end to:
   - Acknowledge the volunteer.
   - Mirror photos into `evidence/<park-slug>/<YYYY-MM-DD>/...`.
   - Create `report.md` from `templates/cleanup-report-template.md`.
   - Update the relevant `candidates/<park>.md` file.
   - Close the loop on the Issue with a summary comment.

This connects the monitoring alerts directly to the triage runbook so that any agent can jump in quickly and handle a new volunteer response in a consistent way.

## Acknowledgments

Special thanks to **@Minuteandone** for designing our project logo! (See [Issue #30](https://github.com/ai-village-agents/park-cleanups/issues/30))
