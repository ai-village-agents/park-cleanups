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
   - New comments on issues
   - Issue state changes (OPEN → CLOSED, etc.)
   - Label changes
5. If changes are detected:
   - Logs the changes to `issue_monitor.log`
   - Creates `changes_detected.flag` with JSON details
   - Creates `CHANGES_DETECTED` text file
   - The GitHub Actions workflow posts a notification comment on the affected issue(s)
   - Creates a team notification issue

## Running Manually

```bash
# From repository root
python3 scripts/monitor_issues_v2.py

# Or using the wrapper
./scripts/monitor_issues.sh
```

## Exit Codes

- `0`: No changes detected
- `1`: Changes detected (new comments or state changes)

## GitHub Actions Integration

The workflow `.github/workflows/monitor-volunteer-responses.yml`:
- Runs hourly (cron: '0 * * * *')
- Can be manually triggered via "Run workflow" button
- Posts notification comments on issues when changes detected
- Creates team notification issues
- Uploads monitoring logs as artifacts

## Notifications

When a volunteer responds (posts a comment), the system will:
1. Post a comment on the issue itself alerting the team
2. Create a new notification issue labeled "notification,volunteer-response"
3. Assign the notification to the ai-village-agents organization

This ensures the team is promptly notified and can respond to volunteers.

## Adding New Issues to Monitor

Edit the `ISSUE_NUMBERS` list in `scripts/monitor_issues_v2.py`.
