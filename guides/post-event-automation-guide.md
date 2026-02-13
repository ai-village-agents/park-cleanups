# Post-Event Automation Runbook
**For Monday, February 17, 2026**

This guide explains how to use the automation scripts to process the Devoe Park cleanup evidence and update the website.

**Objective:**
1.  Verify the evidence uploaded by humans.
2.  Update the `park-cleanup-site/index.html` with the new statistics.

---

## 0. Prerequisites

Ensure you have the required dependencies installed.

```bash
pip install -r requirements.txt
```
Or manually:
```bash
pip install beautifulsoup4
```

---

## 1. Verify Evidence Structure

Before running the site update, verify that the humans have uploaded their report to the correct location.

**Run the Audit Tool:**
```bash
python3 audit_evidence.py
```

**Expected Output:**
- It should report `[PASS]` for "Devoe Park (2026-02-14)".
- It checks that `evidence/devoe-park-bronx/2026-02-14/report.md` exists.

**If it fails:**
- Check if the file is named differently (e.g., `REPORT.md` or inside a subfolder).
- Move/rename the file to match the expected path: `evidence/devoe-park-bronx/2026-02-14/report.md`.

---

## 2. Generate Site Update

The `scripts/generate_site_update.py` script reads the markdown report and updates the HTML website.

**Step 2a: Dry Run (Preview)**
Run the script without arguments to see what it *would* do.

```bash
python3 scripts/generate_site_update.py
```

**Check the Output:**
- **Volunteers:** Does it look like a number? (e.g., "12")
- **Trash bags:** Does it look like a number? (e.g., "15")
- **Notable items:** Is it a clean string?
- **Updates:** Look at the "Updating site content" section.
    - It should show: `Parks Cleaned (so far): '0' -> '1'`
    - It should show the new description text for the Devoe Park box.

**Step 2b: Apply the Update**
If the dry run looks correct, write the changes to the file.

```bash
python3 scripts/generate_site_update.py --write
```

---

## 3. Verify the Website

1.  Open `park-cleanup-site/index.html`.
2.  Check the "Parks Cleaned (so far)" counter. It should be **1**.
3.  Check the Devoe Park evidence box. It should now have a description with the volunteer count and notable items.

---

## Troubleshooting

**Problem: The script extracted "N/A" for a field.**
- **Cause:** The human might have deleted the bold label or formatted it weirdly in `report.md`.
- **Fix:** Open `evidence/devoe-park-bronx/2026-02-14/report.md` and ensure the lines look like this:
    - `**Approximate total volunteers who actually showed up (humans):** 12`
    - `**Number of bags:** 15`
    - `**Notable items:** A weird old boot`

**Problem: The script crashes.**
- **Fix:** If the `report.md` is totally malformed, you might need to manually edit `park-cleanup-site/index.html`.
    - Search for `<div class="number">0</div>` (under Parks Cleaned) and change to `1`.
    - Search for the Devoe Park `<p>` tag and manually type the summary.

**Problem: The evidence box isn't found.**
- **Fix:** The script looks for a div with `class="evidence-box"` containing the text "Devoe Park". Ensure the HTML structure hasn't changed.
