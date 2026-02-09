#!/usr/bin/env python3
"""
Monitor GitHub issues for volunteer responses.
Tracks Issues #1 (Devoe Park) and #3 (Mission Dolores Park).
Logs new comments and state changes.
Outputs machine-readable flag file for GitHub Actions.
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Default AI agent logins that should not trigger alerts
AGENT_LOGINS = {
    "claude-3-7-sonnet",
    "claude-opus-4-5",
    "claude-opus-4-6",
    "claude-sonnet-45",
    "claudehaiku45",
    "deepseek-v32",
    "gemini-25-pro-collab",
    "gemini-3-pro-ai-village",
    "gpt-5-1",
    "gpt-5-2",
    "gpt-5-ai-village",
    "opus-4-5-claude-code",
}

# Configuration
REPO_DIR = Path(__file__).parent.parent
LOG_FILE = REPO_DIR / "monitoring" / "issue_monitor.log"
STATE_FILE = REPO_DIR / "monitoring" / "issue_state.json"
FLAG_FILE = REPO_DIR / "monitoring" / "changes_detected.flag"
CHANGES_TEXT_FILE = REPO_DIR / "monitoring" / "CHANGES_DETECTED"
ISSUE_NUMBERS = [1, 3]

def ensure_monitoring_dir():
    """Create monitoring directory if it doesn't exist."""
    monitoring_dir = REPO_DIR / "monitoring"
    monitoring_dir.mkdir(exist_ok=True)
    # Clear flag files at start
    if FLAG_FILE.exists():
        FLAG_FILE.unlink()
    if CHANGES_TEXT_FILE.exists():
        CHANGES_TEXT_FILE.unlink()

def load_previous_state():
    """Load previous issue state from JSON file."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_current_state(state):
    """Save current issue state to JSON file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_agent_logins():
    """Return combined set of default and env-provided agent logins."""
    extra_logins = os.getenv("AI_VILLAGE_AGENT_LOGINS", "")
    parsed_extra = {
        login.strip().lower()
        for login in extra_logins.split(",")
        if login.strip()
    }
    return {login.lower() for login in AGENT_LOGINS}.union(parsed_extra)

def get_issue_data(issue_num):
    """Get issue data using gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "issue", "view", str(issue_num), "--json", 
             "number,title,state,comments,createdAt,updatedAt,url,author,labels"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error fetching issue {issue_num}: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON for issue {issue_num}: {e}")
        return None

def log_event(message):
    """Log event to log file and stdout."""
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {message}"
    
    print(log_entry)
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + "\n")

def compare_comments(old_comments, new_comments, issue_num):
    """Detect new comments and return list of new ones."""
    if not old_comments:
        return new_comments
    
    old_ids = {c.get('id') for c in old_comments if c.get('id')}
    new_ones = []
    
    for comment in new_comments:
        if comment.get('id') not in old_ids:
            new_ones.append(comment)
    
    return new_ones

def format_comment_info(comment, issue_num):
    """Format comment info for logging."""
    author = comment.get('author', {}).get('login', 'unknown')
    created = comment.get('createdAt', 'unknown')
    body_preview = comment.get('body', '')[:100].replace('\n', ' ')
    if len(comment.get('body', '')) > 100:
        body_preview += "..."
    
    return f"Issue #{issue_num}: Comment by @{author} at {created}: {body_preview}"

def main():
    """Main monitoring function."""
    ensure_monitoring_dir()
    
    agent_logins = get_agent_logins()
    
    # Load previous state
    previous_state = load_previous_state()
    current_state = {}
    
    log_event(f"Starting issue monitor for issues {ISSUE_NUMBERS}")
    
    any_changes = False
    change_details = []
    
    for issue_num in ISSUE_NUMBERS:
        log_event(f"Checking issue #{issue_num}")
        
        issue_data = get_issue_data(issue_num)
        if not issue_data:
            log_event(f"Failed to fetch issue #{issue_num}")
            continue
        
        issue_key = f"issue_{issue_num}"
        current_state[issue_key] = {
            'number': issue_data['number'],
            'title': issue_data['title'],
            'state': issue_data['state'],
            'comments_count': len(issue_data.get('comments', [])),
            'updated_at': issue_data['updatedAt'],
            'url': issue_data['url'],
            'comments': issue_data.get('comments', []),
            'labels': [label.get('name') for label in issue_data.get('labels', [])]
        }
        
        # Compare with previous state
        old_state = previous_state.get(issue_key, {})
        
        # Check for state changes
        if old_state and old_state.get('state') != issue_data['state']:
            change_msg = f"Issue #{issue_num} state changed from {old_state.get('state')} to {issue_data['state']}"
            log_event(change_msg)
            change_details.append(change_msg)
            any_changes = True
        
        # Check for new comments
        old_comments = old_state.get('comments', [])
        new_comments = compare_comments(old_comments, issue_data.get('comments', []), issue_num)
        
        if new_comments:
            external_comments = []
            ignored_agent_comments = []
            for comment in new_comments:
                author_login = comment.get('author', {}).get('login') or ''
                if author_login.lower() in agent_logins:
                    ignored_agent_comments.append(comment)
                else:
                    external_comments.append(comment)

            if external_comments:
                log_event(f"Issue #{issue_num} has {len(external_comments)} new external comment(s)!")
                change_details.append(f"Issue #{issue_num}: {len(external_comments)} new external comment(s)")
                for comment in external_comments:
                    comment_info = format_comment_info(comment, issue_num)
                    log_event(f"  New comment: {comment_info}")
                    change_details.append(comment_info)
                any_changes = True

            if ignored_agent_comments:
                log_event(f"Issue #{issue_num} has {len(ignored_agent_comments)} new agent comment(s) ignored for alerts")
        
        # Log current status
        log_event(f"Issue #{issue_num}: {issue_data['state']}, {len(issue_data.get('comments', []))} comments, last updated {issue_data['updatedAt']}")
    
    # Save current state
    save_current_state(current_state)
    
    if any_changes:
        log_event("Changes detected - consider notifying team")
        # Create flag file with change details
        with open(FLAG_FILE, 'w') as f:
            json.dump({
                'changes_detected': True,
                'timestamp': datetime.now().isoformat(),
                'details': change_details
            }, f, indent=2)
        # Also write a simple text flag for shell scripts
        with open(CHANGES_TEXT_FILE, 'w') as f:
            f.write("CHANGES_DETECTED\n")
            for detail in change_details:
                f.write(f"{detail}\n")
    else:
        log_event("No changes detected")
        # Write empty flag file
        with open(FLAG_FILE, 'w') as f:
            json.dump({'changes_detected': False, 'timestamp': datetime.now().isoformat()}, f, indent=2)
        # Ensure stale text flag is removed
        if CHANGES_TEXT_FILE.exists():
            CHANGES_TEXT_FILE.unlink()
    
    log_event("Monitoring complete")
    
    # Always return 0 so downstream CI steps continue; detection is via flag files
    return 0

if __name__ == "__main__":
    sys.exit(main())
