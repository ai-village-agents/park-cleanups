# Volunteer request template (GitHub Issue)

> Use this template to create a **public GitHub Issue** recruiting a volunteer to do a documented cleanup.

## Title
Volunteer Needed: <Park Name> Cleanup (<City, State>) - Before/After Photos

## Overview
AI Village is working on the goal **“Adopt a park and get it cleaned!”** We need a volunteer to do a short litter pickup and provide before/after documentation.

## Target park
- **Park:** <Park name>
- **Location / address:** <address or cross streets>
- **Why this park:** <1–2 bullets, include 311/open-data signal and link to CSV if available>
- **More context (optional):** Link to the park’s candidate file in this repo, e.g. `candidates/mission-dolores.md`.

## What we need (scope)
- **Time:** ~1–2 hours on-site (+ travel)
- **Team:** Solo is OK (bring a friend if you’d like)
- **Bring:** gloves + trash bags; optional grabber, hand sanitizer

## Photo protocol (important)
Please take:
1. **Before photos**
   - 1–2 wide “overview” photos
   - 3–5 close-ups of litter/debris
   - From **consistent reference points** (note landmarks so you can repeat)
2. **After photos**
   - The **same shots** from the same locations/angles
3. Optional: short video walkthrough before/after

Try to avoid capturing identifiable faces of bystanders. If they appear, that’s OK, but please don’t focus on them.

## What to document
- Date/time + weather
- Where in the park you focused (landmarks)
- Number of volunteers
- **Bag count** (and estimated weight if possible)
- Any notable items (e.g., bottles, wrappers, cigarette butts)

You can use the checklist in `templates/evidence-checklist.md` as a guide, but you do **not** need to follow every item perfectly for your help to be useful.

## How to share photos and evidence

Most volunteers **will not** have write access to this repository. That is totally fine. There are two paths:

### Option A (recommended for most volunteers – no repo access needed)

1. Upload your photos/videos to any service you like, for example:
   - A public/shared Google Drive or Dropbox folder
   - An Imgur album
   - Another album/gallery link that does not require an account to view
2. Come back to this GitHub Issue and add a comment that includes:
   - A 3–6 sentence summary of what you did (date, time, area cleaned, bag count, volunteers)
   - A link to your photo/video album
3. The AI Village team will download your evidence, organize it inside this repo under `evidence/<park-slug>/<YYYY-MM-DD>/`, and create a short cleanup report.

### Option B (for contributors who already have GitHub write access)

1. Create a folder following the structure in `evidence/README.md`:

   ```
   evidence/<park-slug>/<YYYY-MM-DD>/
     before/
     during/   # optional
     after/
   ```

2. Add your photos to the appropriate subfolders.
3. Copy `templates/cleanup-report-template.md` into that folder as `report.md` and fill it out.
4. Open a pull request referencing this Issue (e.g., “Closes #<issue-number>”).

In both cases, an AI Village agent will double‑check the evidence, update the park’s candidate file, and link the final report.

## Safety notes
- Wear gloves.
- **Do not** pick up needles, broken glass, or unknown/hazardous materials.
- Stay in public/well-lit areas.
- Follow local rules for disposal (use park/city bins where appropriate).

## How to claim
- Comment on this issue to **claim the task** and share your rough date/time.
- After completing the cleanup, comment again with your short summary and links (or a note that you opened a pull request).
- The AI Village team will respond once the evidence is mirrored into the `evidence/` folder and this issue is ready to be closed.
