# Google Sheet Monitoring System

This system monitors the Google Sheet linked to our volunteer signup Google Form for new responses.

## Overview

When volunteers sign up via the Google Form (https://forms.gle/6ZNTydyA2rwZyq6V7), their responses are stored in a Google Sheet. This monitoring system checks for new rows in that sheet and alerts the team via:

1. Comments on GitHub Issues #1 and #3
2. A dedicated notification issue for team coordination
3. Log files and artifacts

## Prerequisites

1. **Google Sheet must exist and be linked to the Form**
   - Gemini 2.5 Pro (owner) needs to link Form to Sheet
   - Sheet should be in AI Village Google Workspace

2. **Sheet sharing permissions**
   - For CSV export method: "Anyone with link can view"
   - For API method: Service account or OAuth token with `https://www.googleapis.com/auth/spreadsheets.readonly` scope

3. **GitHub repository secrets**
   - `GOOGLE_SHEET_ID`: The Sheet ID from URL (e.g., `1aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890`)
   - `GOOGLE_SHEET_CSV_URL`: Full CSV export URL (optional, for CSV method)

## Setup Steps

### 1. Once Sheet is created/linked by the Form owner (Gemini 2.5 Pro):

```
1. Get the Sheet URL (e.g., https://docs.google.com/spreadsheets/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890/edit)
2. Extract Sheet ID: `1aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890`
3. Set sharing to "Anyone with link can view" (for CSV method)
4. Add GitHub repository secrets:
   - GOOGLE_SHEET_ID = [Sheet ID]
   - GOOGLE_SHEET_CSV_URL = https://docs.google.com/spreadsheets/d/[Sheet ID]/gviz/tq?tqx=out:csv&sheet=Form Responses 1
   (Alternative that also works: https://docs.google.com/spreadsheets/d/[Sheet ID]/export?format=csv&gid=<GID>)
```

### 2. GitHub Secrets Configuration:

Go to repository Settings → Secrets and variables → Actions → New repository secret

Add:
- `GOOGLE_SHEET_ID`: The Sheet ID from the URL
- `GOOGLE_SHEET_CSV_URL`: CSV export URL (recommended for simplicity)

### 3. Verify Monitoring Works:

- Manual trigger: Go to Actions → "Monitor Google Sheet Responses" → Run workflow
- Check logs for success/failure
- Test with a dummy form submission

## Files

- `scripts/monitor_google_sheet.py` - Main monitoring script
- `scripts/monitor_sheet.sh` - Shell wrapper
- `.github/workflows/monitor-google-sheet.yml` - GitHub Actions workflow
- `monitoring/sheet_state.json` (excluded from artifacts) - Persistent state (automatically managed)
- `monitoring/sheet_monitor.log` - Log file
- `monitoring/sheet_changes_detected.flag` - Flag when changes detected
- `monitoring/SHEET_CHANGES_DETECTED` - Human-readable change details

## How It Works

### Detection Logic

1. **Fetch data**: Uses CSV export (preferred) or Google Sheets API
2. **Filter agent submissions**: Ignores rows from known AI Village agent emails
3. **Compare with previous state**: Uses row hashes to detect new submissions
4. **Alert generation**: Creates flag files and posts notifications

### State Persistence

- The workflow restores the previous `monitoring/sheet_state.json` from the GitHub Actions cache before each run, then saves an updated copy afterward.
- Restore uses a stable key prefix (OS + branch) so newer runs can reuse earlier state. Save uses a content-hash key derived from `monitoring/sheet_state.json`, so a new cache is only created when the state file actually changes.
- Practical effect: alerts are incremental across runs, not one-off; each run builds on the last known Sheet state.

### Alert Flow

```
New Form submission → Sheet updated → Monitor runs (every 15 min)
  → Detects new row → Posts comment on Issues #1 & #3
  → Creates/updates team notification issue
  → Team can triage using `templates/first-volunteer-triage-runbook.md`
```

### Integration with Existing Systems

- **Issue monitoring**: Posts alerts to same Issues (#1, #3) as GitHub comment monitoring
- **Triage workflow**: Same `first-volunteer-triage-runbook.md` used for both GitHub and Form responses
- **Form intake guide**: Follow `guides/google-form-intake.md` for Sheet-specific processing

## Testing

To test the monitoring system:

1. **Submit test form** (use non-agent email)
2. **Wait for next monitoring run** (or trigger manually)
3. **Verify alerts appear** on Issues #1 and #3
4. **Check notification issue** is created/updated

## Troubleshooting

### Common Issues

1. **"CSV fetch failed with status 403"**
   - Sheet not shared publicly
   - Solution: Set sharing to "Anyone with link can view"

2. **"Token lacks Sheets API scope"**
   - Using API method without proper OAuth token
   - Solution: Use CSV method or get token with sheets scope

3. **No alerts despite new submissions**
   - Check if email matches agent filter list
   - Verify Sheet ID in secrets is correct
   - Check monitoring logs in workflow artifacts

4. **Duplicate alerts**
   - State file may be out of sync
   - Solution: The workflow state comes from the Actions cache; if a hard reset is ever needed, bump the cache key prefix in `.github/workflows/monitor-google-sheet.yml` or clear the cache in GitHub Settings. Deleting `monitoring/sheet_state.json` locally does not reset the cached state used by Actions runs.

### Debugging Commands

```bash
# Test script manually
cd /home/computeruse/park-cleanups
GOOGLE_SHEET_ID="your-sheet-id" python3 scripts/monitor_google_sheet.py

# Check logs
cat monitoring/sheet_monitor.log

# Local-only reset for ad-hoc testing (does not affect Actions cache)
rm monitoring/sheet_state.json
```

## Maintenance

- **State file**: Restored and saved via the GitHub Actions cache; to force a hard reset, bump the version prefix in the cache key in `.github/workflows/monitor-google-sheet.yml` or clear the cache in repository Settings (rarely needed in normal operation)
- **Log rotation**: Logs uploaded as artifacts, retained 7 days
- **Agent email list**: Update in script or via `AI_VILLAGE_AGENT_EMAILS` env var
- **Schedule**: Currently every 15 minutes, can be adjusted in workflow

## Security Considerations

- **State file privacy**: `monitoring/sheet_state.json` contains per-row hashes and is persisted via the GitHub Actions cache for incremental monitoring. It is **explicitly excluded from uploaded artifacts** and should not be shared publicly.
- **Logs vs internal state**: `monitoring/sheet_monitor.log` and `monitoring/SHEET_CHANGES_DETECTED` are designed to record aggregate counts and high-level summaries only; they never include raw row contents, names, or email addresses.
- **State file (membership inference risk)**: `monitoring/sheet_state.json` stores per-row MD5 hashes of filtered external responses. While these hashes are not reversible into readable text, they *can* be used for membership inference by someone who already knows a row's exact contents. The workflow persists this file via the GitHub Actions cache for incremental monitoring and **explicitly excludes it from uploaded artifacts**. Treat this file as internal debugging state and do not upload/share it publicly.
- **Agent filtering**: Prevents self-notifications from internal testing
- **GitHub secrets**: Sheet access credentials stored securely
- **Public sharing**: CSV export method requires public read access (no edit)

## Counts-only verification artifact

In addition to the internal `sheet_state.json` used for incremental monitoring, the workflow now generates a small, strictly aggregate verification file:

- Script: `scripts/generate_counts_verification.py`
- Output: `monitoring/volunteer_counts_verification.json` (uploaded as a separate `volunteer-counts-verification` artifact)

This file contains only:

- Per-park counts of filtered **external** responses (e.g., Mission Dolores, Devoe Park)
- A total external response count
- A SHA-256 hash computed **only** over those aggregate counts

It deliberately avoids per-row hashes or any PII, so it can be used as a limited, counts-only verification artifact that collaborators can recompute independently if they have access to the same Sheet, without exposing individual volunteer responses.

## Related Documentation

- `guides/google-form-intake.md` - Processing Form responses
- `templates/first-volunteer-triage-runbook.md` - Volunteer response handling
- `monitoring/README.md` - Issue monitoring system
- `templates/response-sheet-coordination-workflow.md` - Team coordination
