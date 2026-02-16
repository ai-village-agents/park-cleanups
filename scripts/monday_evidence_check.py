#!/usr/bin/env python3
"""
Monday Morning Evidence Check — Devoe Park Cleanup (Feb 14, 2026)

Scans GitHub Issue #1 in ai-village-agents/park-cleanups for:
  - Image attachments (photos uploaded as .png, .jpg, .jpeg, .gif, .webp)
  - Markdown image embeds (![alt](url))
  - Links to external image hosts
  - Comments mentioning evidence-related keywords

Generates a quick status summary for the Monday morning standup.

Usage:
  python3 monday_evidence_check.py
  # or with a GitHub token:
  GH_TOKEN=<token> python3 monday_evidence_check.py
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO = "ai-village-agents/park-cleanups"
ISSUE_NUMBER = 1
CLEANUP_DATE = "2026-02-14"

# Logins to ignore for evidence keyword scanning (bots/agents)
IGNORE_LOGINS = {
    "github-actions[bot]",
    "github-actions",
}


# Image patterns
IMAGE_EXTENSIONS = re.compile(r'\.(png|jpg|jpeg|gif|webp|heic|heif)(\?|$)', re.IGNORECASE)
MARKDOWN_IMAGE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
HTML_IMG = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\']', re.IGNORECASE)
GITHUB_ASSET_URL = re.compile(r'https://(?:user-images\.githubusercontent\.com|github\.com/.*?/assets)', re.IGNORECASE)

# Evidence keywords
EVIDENCE_KEYWORDS = re.compile(
    r'\b(photo|picture|image|pic|evidence|before|after|during|cleaned|trash|bag|'
    r'bucket|glove|litter|garbage|debris|volunteer|turnout|showed up|attended|'
    r'cleanup|clean-up|recap|result|done|finished|completed)\b',
    re.IGNORECASE
)

ATTENDANCE_KEYWORDS = re.compile(
    r'\b(\d+)\s*(people|person|volunteer|folk|showed|came|attended|of us)\b',
    re.IGNORECASE
)


def gh_api(endpoint):
    """Call GitHub API via gh CLI."""
    result = subprocess.run(
        ["gh", "api", endpoint, "--paginate"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error calling GitHub API: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def extract_images(text):
    """Extract all image references from a comment body."""
    images = []
    # Markdown images
    for match in MARKDOWN_IMAGE.finditer(text):
        images.append({"type": "markdown_embed", "alt": match.group(1), "url": match.group(2)})
    # HTML img tags
    for match in HTML_IMG.finditer(text):
        images.append({"type": "html_img", "url": match.group(1)})
    # Raw URLs that look like images
    urls = re.findall(r'https?://\S+', text)
    for url in urls:
        if IMAGE_EXTENSIONS.search(url) and url not in [i.get("url") for i in images]:
            images.append({"type": "raw_url", "url": url})
    # GitHub asset uploads
    for match in GITHUB_ASSET_URL.finditer(text):
        url_full = re.search(r'https?://\S+', text[match.start():])
        if url_full:
            full_url = url_full.group(0).rstrip(')')
            if full_url not in [i.get("url") for i in images]:
                images.append({"type": "github_asset", "url": full_url})
    return images


def extract_attendance(text):
    """Try to extract attendance numbers from text."""
    matches = ATTENDANCE_KEYWORDS.findall(text)
    return matches



def list_evidence_images():
    """List image files in evidence/devoe-park-bronx/2026-02-14/{before,during,after}."""
    base_path = f"/repos/{REPO}/contents/evidence/devoe-park-bronx/{CLEANUP_DATE}"
    images = []
    try:
        base = gh_api(base_path)
        if not isinstance(base, list):
            return images
        for d in ("before", "during", "after"):
            listing = gh_api(f"{base_path}/{d}")
            if isinstance(listing, list):
                for f in listing:
                    name = f.get("name", "") or ""
                    # IMAGE_EXTENSIONS matches both URLs and file names
                    if IMAGE_EXTENSIONS.search(name):
                        images.append({
                            "folder": d,
                            "name": name,
                            "url": f.get("html_url") or f.get("download_url")
                        })
    except Exception:
        return images
    return images

def analyze_issue():
    """Fetch and analyze Issue #1 and its comments."""
    print("=" * 60)
    print("  MONDAY MORNING EVIDENCE CHECK")
    print(f"  Devoe Park Cleanup — {CLEANUP_DATE}")
    print(f"  Scanned at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 60)
    print()

    # Fetch issue body
    issue = gh_api(f"/repos/{REPO}/issues/{ISSUE_NUMBER}")
    # Fetch all comments
    comments = gh_api(f"/repos/{REPO}/issues/{ISSUE_NUMBER}/comments")

    total_images = []
    evidence_comments = []
    attendance_mentions = []
    post_cleanup_comments = []

    # Check issue body
    body = issue.get("body", "") or ""
    body_images = extract_images(body)
    if body_images:
        total_images.extend(body_images)

    # Analyze each comment
    for comment in comments:
        c_body = comment.get("body", "") or ""
        c_user = comment.get("user", {}).get("login", "unknown")
        c_date = comment.get("created_at", "")
        c_url = comment.get("html_url", "")

        # Check if comment is after cleanup date
        is_post_cleanup = c_date >= f"{CLEANUP_DATE}T00:00:00Z"

        # Extract images
        images = extract_images(c_body)
        if images:
            total_images.extend(images)
            evidence_comments.append({
                "user": c_user,
                "date": c_date,
                "url": c_url,
                "image_count": len(images),
                "images": images,
                "post_cleanup": is_post_cleanup
            })

        # Check for evidence keywords
        if is_post_cleanup and EVIDENCE_KEYWORDS.search(c_body) and c_user.lower() not in IGNORE_LOGINS:
            post_cleanup_comments.append({
                "user": c_user,
                "date": c_date,
                "url": c_url,
                "snippet": c_body[:200].replace("\n", " ")
            })

        # Check for attendance mentions
        att = extract_attendance(c_body)
        if att and is_post_cleanup:
            attendance_mentions.append({
                "user": c_user,
                "matches": att,
                "url": c_url
            })

    # --- Report ---
    print(f"📋 Issue #1: {issue.get('title', 'N/A')}")
    print(f"   State: {issue.get('state', 'N/A')}")
    print(f"   Total comments: {len(comments)}")
    print()

    # Photo evidence
    print("📸 PHOTO EVIDENCE")
    print("-" * 40)
    if evidence_comments:
        post_cleanup_evidence = [e for e in evidence_comments if e["post_cleanup"]]
        pre_cleanup_evidence = [e for e in evidence_comments if not e["post_cleanup"]]

        if post_cleanup_evidence:
            print(f"  ✅ Found {len(post_cleanup_evidence)} comment(s) with images AFTER cleanup date:")
            for e in post_cleanup_evidence:
                print(f"     - {e['user']} ({e['date'][:10]}): {e['image_count']} image(s)")
                for img in e["images"]:
                    print(f"       → {img['url'][:80]}...")
                print(f"       Link: {e['url']}")
        else:
            print("  ⚠️  No post-cleanup image attachments found yet.")

        if pre_cleanup_evidence:
            print(f"\n  ℹ️  {len(pre_cleanup_evidence)} comment(s) with images from BEFORE cleanup date (pre-event).")
    else:
        print("  ⚠️  No image attachments found in any comments.")
    print()

    # Attendance
    print("👥 ATTENDANCE MENTIONS")
    print("-" * 40)
    if attendance_mentions:
        for a in attendance_mentions:
            print(f"  - {a['user']}: mentioned {a['matches']}")
            print(f"    Link: {a['url']}")
    else:
        print("  ℹ️  No explicit attendance numbers found in post-cleanup comments.")
    print()

    # Post-cleanup activity
    print("💬 POST-CLEANUP COMMENTS (evidence-related)")
    print("-" * 40)
    if post_cleanup_comments:
        for c in post_cleanup_comments:
            print(f"  - {c['user']} ({c['date'][:10]}):")
            print(f"    \"{c['snippet'][:120]}...\"")
            print(f"    Link: {c['url']}")
    else:
        print("  ℹ️  No post-cleanup evidence-related comments found yet.")
    print()

    # Also check evidence directory
    evidence_images = list_evidence_images()

    print("📁 EVIDENCE DIRECTORY CHECK")
    print("-" * 40)
    try:
        evidence_path = f"/repos/{REPO}/contents/evidence/devoe-park-bronx/2026-02-14"
        evidence_files = gh_api(evidence_path)
        if isinstance(evidence_files, list):
            print(f"  Found {len(evidence_files)} item(s) in evidence/devoe-park-bronx/2026-02-14/:")
            for f in evidence_files:
                ftype = "📂" if f.get("type") == "dir" else "📄"
                print(f"    {ftype} {f.get('name', 'unknown')}")
            if evidence_images:
                print(f"\n  ✅ Evidence images committed in repo: {len(evidence_images)}")
                for img in evidence_images:
                    print(f"    - {img['folder']}/{img['name']}")
            else:
                print("\n  ℹ️  No image files found inside evidence subfolders yet.")
        else:
            print(f"  Found directory: {evidence_files.get('name', 'unknown')}")
    except Exception:
        print("  ℹ️  Evidence directory not yet populated or inaccessible.")
    print()

    # Summary
    print("=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    post_evidence = [e for e in evidence_comments if e["post_cleanup"]]
    total_post_images = sum(e["image_count"] for e in post_evidence)
    total_evidence_dir_images = len(evidence_images)

    if total_post_images > 0 or total_evidence_dir_images > 0:
        if total_post_images > 0:
            print(f"  🟢 EVIDENCE FOUND (Issue comments): {total_post_images} post-cleanup image(s) from {len(post_evidence)} comment(s)")
        if total_evidence_dir_images > 0:
            print(f"  🟢 EVIDENCE FOUND (repo evidence/): {total_evidence_dir_images} image(s) committed under evidence/devoe-park-bronx/{CLEANUP_DATE}/")
    else:
        print("  🟡 NO POST-CLEANUP IMAGES YET — check if volunteers posted elsewhere")
        print("     Action items:")
        print("     1. Check Issue #1 for text updates about the cleanup")
        print("     2. Check bearsharktopus-dev's Tumblr (@reachartwork) for photos")
        print("     3. Check Bluesky for tagged posts")
        print("     4. Post a friendly request for photos on Issue #1")
        print("     5. Check Google Form responses for any updates")

    if post_cleanup_comments:
        print(f"  💬 {len(post_cleanup_comments)} evidence-related comment(s) found post-cleanup")
    if attendance_mentions:
        print(f"  👥 Attendance mentioned in {len(attendance_mentions)} comment(s)")

    print()
    print("  Next steps: See MONDAY_MORNING_ACTION_PLAN.md for full checklist")
    print("=" * 60)

    return {
        "total_images": total_post_images,
        "evidence_comments": len(post_evidence),
        "post_cleanup_comments": len(post_cleanup_comments),
        "attendance_mentions": len(attendance_mentions),
        "evidence_dir_images": len(evidence_images)
    }


if __name__ == "__main__":
    results = analyze_issue()
