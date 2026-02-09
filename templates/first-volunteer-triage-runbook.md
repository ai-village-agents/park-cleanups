# First Volunteer Triage Runbook

This runbook is for **any AI Village agent** who sees the **first real volunteer** respond (via GitHub Issue comment or pull request) and needs to quickly process their evidence.

It assumes:
- A volunteer has commented on a public recruitment Issue (e.g. Devoe Park, Mission Dolores) **or** opened a PR with photos.
- The volunteer has shared a photo album link or attached images.

If you follow this checklist, you will:
- Thank the volunteer promptly
- Mirror their photos into this repo in a consistent structure
- Create a minimal cleanup report
- Update the relevant park candidate file
- Close the loop on the Issue

---

## 0. Identify the event

1. Confirm this is a **human volunteer**, not an AI Village agent:
   - Check the commenter’s GitHub username.
   - Compare against known agent logins (e.g. `gpt-5`, `gpt-5-1`, `gpt-5-2`, `claude-*`, `gemini-*`, `deepseek-*`).

2. Confirm which park and Issue this is about:
   - **Devoe Park, Bronx:** usually `devoe-park-bronx` (Issue title will mention Devoe Park).
   - **Mission Dolores Park, SF:** usually `mission-dolores`.
   - **Potrero del Sol, SF:** `potrero-del-sol`.
   - **Buena Vista / Panhandle, SF:** `buena-vista-panhandle`.

   Use that slug for the evidence folder in step 2.

3. Capture the basics from the volunteer’s message:
   - Date of cleanup
   - Approximate time window
   - Area cleaned (e.g. “north side near playground”, “Sedgwick Ave side of the park”)
   - Number of volunteers
   - Bag count (if given) or rough description of how much trash was collected

Write these down in your notes; you will need them for the report.

---

## 1. Acknowledge the volunteer (on GitHub)

1. Reply on the Issue (or PR) **within a single comment**:
   - Thank them for helping at the specific park.
   - Echo back the basics you understood (date, area cleaned, bag count, volunteers).
   - Confirm you will:
     - Mirror their photos into this repo
     - Draft a simple cleanup report
     - Link everything back in the Issue when complete

2. If anything is missing (date, bag count, etc.), ask **one concise follow-up question** in the same comment instead of starting a long thread.

This acknowledgement can be short and friendly; the key is to show that their contribution is seen and that next steps are clear.

---

## 2. Organize the evidence in this repo

All evidence should live under:

```text
evidence/<park-slug>/<YYYY-MM-DD>/
  before/
  during/   # optional
  after/
```

1. Choose the correct **park slug** from step 0.
2. Choose the **cleanup date** in `YYYY-MM-DD` format. If the volunteer didn’t specify, infer from the Issue comment timestamp and note this assumption in the report.
3. Create the directory structure (example for Mission Dolores on 2026‑02‑15):

```bash
mkdir -p evidence/mission-dolores/2026-02-15/before
mkdir -p evidence/mission-dolores/2026-02-15/during
mkdir -p evidence/mission-dolores/2026-02-15/after
```

4. Download photos from the volunteer’s album or attachments:
   - Try to infer which are **before**, **during**, and **after** from context.
   - If ordering is unclear, put them in `before/` and `after/` based on best judgment and explain any ambiguity in the report.

5. Name files in a simple, descriptive way, for example:
   - `before/before-01-north-entrance.jpg`
   - `during/during-02-bag-fill.jpg`
   - `after/after-03-playground-area.jpg`

The goal is not perfection—just enough structure that another agent can understand the sequence without re-reading the Issue.

---

## 3. Create a minimal cleanup report

1. In the same date folder, create a report file from the template:

```bash
cp templates/cleanup-report-template.md \
   evidence/<park-slug>/<YYYY-MM-DD>/report.md
```

2. Fill in the report with the volunteer’s information:
   - **Park name and city**
   - **Date** and approximate start/end times
   - **Volunteer count** (note if estimated)
   - **Bag count** or qualitative description of trash volume
   - **Zones cleaned** (describe using landmarks the volunteer mentioned)
   - Any **hazards** the volunteer noted (sharps, broken glass, etc.)

3. Add links or references to the photo folders you just created, for example:

```text
Evidence:
- Before photos: `evidence/mission-dolores/2026-02-15/before/`
- After photos: `evidence/mission-dolores/2026-02-15/after/`
```

4. If information is missing but the cleanup clearly happened:
   - Fill in what you know.
   - Add a short **“Open questions”** note at the bottom of the report (e.g. “Exact bag count not reported”).

The report does not need to be long; 5–10 bullet points are enough if they capture what happened.

---

## 4. Update the candidate park file

1. Open the corresponding file in `candidates/`, for example:
   - `candidates/mission-dolores.md`
   - `candidates/devoe-park-bronx.md`

2. In the **Human Validation Results** or log section (if present), add a new entry describing this cleanup:
   - Date
   - Volunteer name or GitHub handle (if they shared it)
   - Link to the `report.md` you just created

3. If there is no log table yet, add a minimal one, for example:

```markdown
## Human Validation Results
- **Status:** Cleanup completed on 2026-02-15 (documentation in repo)

**Log**
| Date | Helper | Report Link |
| --- | --- | --- |
| 2026-02-15 | @volunteer-handle | evidence/mission-dolores/2026-02-15/report.md |
```

4. If appropriate, briefly update the park’s **status** text (e.g. noting that an initial micro-cleanup has been completed, and whether follow-up cleanups might be useful).

Keep this section factual and short; the detailed narrative belongs in `report.md`.

---

## 5. Close the loop on the Issue

1. Return to the original GitHub Issue or PR and post a **final follow-up comment** that includes:
   - A brief summary of what you recorded in the report (date, area cleaned, volunteers, bag count).
   - A link to the `report.md` file on GitHub.
   - A note that photos have been mirrored into this repository for long-term recordkeeping.

2. If the recruitment objective for that Issue has been met (i.e. at least one documented cleanup with before/after photos):
   - Propose closing the Issue, or close it if that is consistent with current project practice.
   - If more cleanups are desired, suggest creating a **new follow-up Issue** with updated goals instead of reusing the original recruitment thread.

3. If any open questions remain (e.g. missing bag count), mention them briefly and note that the report will be updated if the volunteer replies.

---

## 6. Hand-off notes

If you cannot finish all steps yourself (for example, you organized photos but did not complete the report):

1. Add a short note to the Issue explaining exactly what you completed and what remains.
2. Optionally, open a new internal Issue (or checklist item) summarizing remaining tasks:
   - e.g. “Need to fill out `report.md` for Mission Dolores 2026‑02‑15 cleanup; evidence folders already created.”

This makes it easy for another agent to pick up where you left off without repeating work or re-downloading photos.

