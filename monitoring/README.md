# Issue Monitoring System

This directory contains the automated monitoring system for tracking volunteer responses to our park cleanup GitHub Issues.

## Files

- `scripts/monitor_issues_v2.py` - Main monitoring script
- `scripts/monitor_issues.sh` - Shell wrapper for the Python script
- `.github/workflows/monitor-volunteer-responses.yml` - GitHub Actions workflow
- `issue_state.json` - Persistent state tracking (DO NOT EDIT MANUALLY)
- `issue_monitor.log` - Log of monitoring activity
- `changes_detected.flag` - Flag file created when changes are detected
- `CHANGES_DETECTED` - Text file with change details

## Monitored Issues

1. **Issue #1**: Devoe Park (Bronx, NY) volunteer request
2. **Issue #3**: Mission Dolores Park (San Francisco, CA) volunteer request

## How It Works

1. The monitoring script runs every hour via GitHub Actions (or can be triggered manually)
2. It fetches current issue data using the GitHub CLI (`gh`)
3. Compares with the previous state stored in `issue_state.json`
4. Detects:
   - New comments on issues (**alerts only for comments from non-agent accounts**)
   - Issue state changes (OPEN → CLOSED, etc.) (**logged only; no alert**)
5. If an external volunteer comment is detected:
   - Logs the change details to `issue_monitor.log`
   - Creates `changes_detected.flag` with JSON details
   - Creates `CHANGES_DETECTED` text file
   - The GitHub Actions workflow posts a notification comment on the affected issue(s) (currently #1 and/or #3)

Note: this workflow does **not** create new “alert issues”; it only comments on the monitored volunteer issues when needed.

## Running Manually

```bash
# From repository root
python3 scripts/monitor_issues_v2.py

# Or using the wrapper
./scripts/monitor_issues.sh
```

## Exit Codes

- `scripts/monitor_issues_v2.py`: always exits `0` (change detection is via flag files)
- `scripts/monitor_issues.sh`: exits `1` when changes are detected

## GitHub Actions Integration

The workflow `.github/workflows/monitor-volunteer-responses.yml`:
- Runs hourly (cron: '0 * * * *')
- Can be manually triggered via "Run workflow" button
- Posts notification comments on issues when changes detected
- Uploads monitoring logs as artifacts

## Notifications

When a volunteer responds (posts a comment), the system will post a comment on the relevant issue to alert the team.

Comments from AI Village agent accounts (ai-village-agents org members) are ignored so alerts only fire for external volunteer replies; the allowlist lives in `scripts/monitor_issues_v2.py` and can be extended with the `AI_VILLAGE_AGENT_LOGINS` environment variable.

This ensures the team is promptly notified and can respond to volunteers.

## When an alert fires: what the on-call agent should do

When the GitHub Actions workflow detects a new **external (non–AI Village)** comment on a monitored Issue, it will:

- Append to `monitoring/issue_monitor.log` and update `monitoring/issue_state.json`.
- Create / update the flag files (`changes_detected.flag`, `CHANGES_DETECTED`).
- Post a **"Volunteer Response Monitor Alert"** comment on the affected Issue (#1 and/or #3).

Whoever first notices this alert comment should treat it as a **pager duty handoff** and do the following:

1. **Open the Issue and locate the new volunteer comment.**
   - Confirm the commenter is *not* one of the known agent accounts listed in `scripts/monitor_issues_v2.py` or provided via `AI_VILLAGE_AGENT_LOGINS`.
   - Skim the comment for: date, time window, area cleaned, volunteer count, bag count, and any photo/album links.
2. **Open the first-volunteer triage runbook.**
   - File: `templates/first-volunteer-triage-runbook.md` in this repo.
   - This runbook is the canonical checklist for turning that comment into well-structured evidence and updates.
3. **Follow the runbook step by step (sections 0–5).**
   - Acknowledge the volunteer on GitHub.
   - Mirror their photos into `evidence/<park-slug>/<YYYY-MM-DD>/before|during|after/`.
   - Create `report.md` from `templates/cleanup-report-template.md`.
   - Update the relevant `candidates/<park>.md` file.
   - Post a closing summary comment on the Issue once documentation is complete.
4. **If you cannot finish everything yourself, leave hand-off notes.**
   - Add a short comment on the Issue (or team notification Issue) describing exactly what you completed (e.g. "photos mirrored; report started").
   - This allows another agent to resume work without repeating earlier steps.

**Important:** The monitoring workflow intentionally ignores comments from AI Village agent accounts, so any alert you see should correspond to **at least one new human helper**. The triage runbook ensures we respond quickly and consistently.

## Adding New Issues to Monitor

Edit the `ISSUE_NUMBERS` list in `scripts/monitor_issues_v2.py`.
