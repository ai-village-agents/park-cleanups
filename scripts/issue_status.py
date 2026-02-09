#!/usr/bin/env python3
"""
Quick status dashboard for monitored issues.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
ISSUE_NUMBERS = [1, 3]

def get_issue_data(issue_num):
    """Get issue data using gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "issue", "view", str(issue_num), "--json", 
             "number,title,state,comments,updatedAt,url"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error fetching issue {issue_num}: {e}")
        return None

def print_status():
    """Print current status of all monitored issues."""
    print("=" * 80)
    print("PARK CLEANUP VOLUNTEER ISSUE STATUS")
    print("=" * 80)
    print(f"Time: {datetime.now().isoformat()}")
    print()
    
    for issue_num in ISSUE_NUMBERS:
        issue = get_issue_data(issue_num)
        if not issue:
            print(f"Issue #{issue_num}: ERROR fetching data")
            continue
            
        state_symbol = "🟢" if issue['state'] == 'OPEN' else "🔴"
        comment_symbol = "💬" if issue['comments'] else "🔇"
        
        print(f"{state_symbol} Issue #{issue['number']}: {issue['title']}")
        print(f"   State: {issue['state']}")
        print(f"   Comments: {len(issue['comments'])} {comment_symbol}")
        print(f"   Updated: {issue['updatedAt']}")
        print(f"   URL: {issue['url']}")
        
        # Show recent comments
        if issue['comments']:
            print("   Recent comments:")
            for i, comment in enumerate(issue['comments'][-3:]):  # Last 3 comments
                author = comment.get('author', {}).get('login', 'unknown')
                created = comment.get('createdAt', '')[:19]
                preview = comment.get('body', '')[:80].replace('\n', ' ')
                if len(comment.get('body', '')) > 80:
                    preview += "..."
                print(f"     {i+1}. @{author} ({created}): {preview}")
        else:
            print("   No comments yet - awaiting volunteer response")
        
        print()
    
    print("=" * 80)
    print("Monitoring active via .github/workflows/monitor-volunteer-responses.yml")
    print("Next scheduled run: Hourly at minute 0")
    print("=" * 80)

if __name__ == "__main__":
    print_status()
