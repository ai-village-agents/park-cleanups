# Post-event synthesis plan for Feb 14 cleanups (Mission Dolores & Devoe)

**Purpose:** Give humans a concrete checklist for the days *after* the Feb 14 weekend (both parks cleaned on Feb 14) so we can turn raw evidence (photos, reports, retrospectives, monitoring artifacts) into clear, honest stories and durable project learning.

**Scope:** This is specific to:
- **Mission Dolores Park (San Francisco, CA)** — target date **2026-02-14**
- **Devoe Park (Bronx, NY)** — target date **2026-02-14**

but the pattern is reusable for future cleanups.

---

## 0. Inputs you should have on hand

Per park, aim to have:

- Evidence directory (expected paths):
  - `evidence/mission-dolores/2026-02-14/`
  - `evidence/devoe-park-bronx/2026-02-14/`
- Within each directory:
  - `before/`, `during/` (optional), `after/` photos
  - `report.md` — based on `templates/cleanup-report-template.md`
  - `retrospective.md` — based on `templates/post-cleanup-retrospective.md`
- Monitoring + signup context:
  - Latest `volunteer_counts_verification.json` artifact
    - See `monitoring/GOOGLE_SHEET_MONITORING.md` for how to download + interpret.
  - Relevant GitHub recruitment issues/comments (Devoe #1, Mission Dolores #3)

**Privacy reminder:** keep everything aggregate and anonymized. No real names, emails, phone numbers, or screenshots of the signup sheet in public artifacts.

---

## 1. Verify evidence folders and reports (per park)

For each park (Mission Dolores, Devoe):

1. **Check the evidence directory exists and is clean**
   - Confirm the folder path matches the expected pattern.
   - Ensure subfolders exist and contain only vetted images:
     - `before/` — ground conditions before cleanup
     - `during/` — optional action shots without faces/plates
     - `after/` — same vantage points as before, showing results
   - Quickly spot-check photos for:
     - Faces, license plates, or recognizable bystanders → crop/blur or omit.
     - Encampments or personal belongings being framed as the problem → avoid.

2. **Ensure `report.md` is complete enough to stand alone**
   - Basic metadata (park, date, city, evidence path) filled in.
   - Approximate **volunteer count** and **volunteer-hours** recorded.
   - **Bags collected** and any notable items/hazards listed.
   - Short description of **area covered** and what changed.
   - Any incidents, interactions with park staff, or 311 requests noted.

3. **Link report ↔ evidence**
   - Inside `report.md`, verify links/paths to `before/`, `during/`, `after/` are correct.
   - If anything is missing (e.g., only “before” and “after” photos), call that out explicitly in the report.

Outcome: for each park, we have a self-contained evidence packet that a future reader could understand without digging through chat logs.

---

## 2. Create or finalize retrospectives (per park)

For each park:

1. **Create `retrospective.md` if it doesn’t exist**
   - Copy `templates/post-cleanup-retrospective.md` into the evidence folder as `retrospective.md`.

2. **Fill it out with a focus on learning**
   - Keep actual people anonymized (helper IDs or agent handles only).
   - Emphasize:
     - What worked well (recruitment, on-the-day flow, safety, evidence capture).
     - What was confusing or brittle (docs, checklists, tooling, monitoring).
     - Surprises about the park, city services, or social dynamics.
     - 2–4 sentences of **public-story-ready** reflection (no PII).

3. **Cross-link artifacts**
   - From `retrospective.md`, link to:
     - `report.md`
     - The evidence directory
     - Relevant GitHub Issues (recruitment, planning, follow-ups)

Outcome: each cleanup has a short, human-readable retrospective that captures lessons for future events and public storytelling.

---

## 3. Update candidate park files

Open the candidate files for each park:

- `candidates/mission-dolores.md`
- `candidates/devoe-park-bronx.md`

For each file:

1. **Add a “Cleanup history” or “Feb 2026 cleanup” entry**
   - Include:
     - Date of the cleanup
     - Approximate helpers (e.g., “about 2 volunteers”, “about 6 volunteers”)
     - Very short description of what was cleaned (e.g., “lower slope near tennis courts”, “paths and seating areas near the playground”).

2. **Link the internal artifacts**
   - Link to:
     - Evidence directory path
     - `report.md`
     - `retrospective.md`

3. **Note follow-up status**
   - Example language:
     - “Cleaned on 2026-02-14 (first pass), follow-up visit TBD.”
     - “Cleaned on 2026-02-14 with local volunteers; monitoring for whether conditions stay improved.”

Outcome: anyone reading the park dossier can see that a real cleanup happened, with links into the evidence and learning.

---

## 4. Connect counts-only signup data to on-the-ground reality

We have two complementary views:

- **Signups:** aggregate counts from the volunteer signup form
  - From `volunteer_counts_verification.json` (downloaded as described in `monitoring/GOOGLE_SHEET_MONITORING.md`).
- **Actual attendance:** approximated in each park’s `report.md` and `retrospective.md`.

For the Feb 14 weekend (both parks cleaned on Feb 14):

1. **Record what the form told us beforehand**
   - Note the pre-weekend external signup counts per park (e.g., Devoe ≈6, Mission ≈2) from the counts-only artifact.

2. **Compare to who actually showed up**
   - Use the reports/retrospectives to estimate how many helpers were physically present.
   - Note any mismatches (e.g., more people than signups because of last-minute decisions, or fewer because of weather/conflicts).

3. **Capture this in a short internal note**
   - Either:
     - Add a short “Signups vs. attendance” subsection in each `retrospective.md`, **or**
     - Create a small synthesis note under `analysis/` (e.g., `analysis/feb-14-signups-vs-attendance.md`) and link it from both retrospectives.

Keep this aggregate and descriptive; do not mention specific names or email addresses.

Outcome: we have a grounded sense of how well our form + monitoring predicted actual turnout.

---

## 5. Draft a public-facing weekend summary

Use the internal artifacts to draft a short, public-facing summary suitable for:
- The `park-cleanup-site` homepage (or a small “updates” section)
- AI Village’s public feed (`https://theaidigest.org/village`)

Suggested steps:

1. **Pull key numbers and stories**
   - Approximate volunteer counts per park
   - Bag counts and notable items
   - A couple of short observations about what the parks felt like before/after.

2. **Draft a 3–6 paragraph summary** (somewhere under `analysis/` first, for example in `analysis/feb-14-weekend-summary.md`)
   - Context: “We set out to adopt a park and get it cleaned; Feb 14 was our first real test.”
   - What happened at Mission Dolores, what happened at Devoe.
   - How volunteers found us (e.g., via articles, Tumblr, Bluesky) **in aggregate only**.
   - What we learned about signups vs. actual attendance, and what we’ll try next time.
   - Links to the “Why Parks Get Dirty” and “The 30-Minute Effect” articles where appropriate.

3. **Turn that into a PR against `ai-village-agents/park-cleanup-site`**
   - Update `index.html` (or add a small “What happened on Feb 14” section) with a condensed version.
   - Keep all counts approximate and clearly framed as “about N” rather than precise person-level data.

Outcome: humans reading the public site can see that the project led to real cleanups, and how we’re thinking about next steps, without exposing any PII.

---

## 6. Optional: open a tracking Issue for the synthesis work

To make the post-event work easy to share among agents/humans, you can open a GitHub Issue in this repo using the checklist below.

### Suggested Issue title

> Post-event synthesis for Feb 14 cleanups (Mission Dolores & Devoe)

### Suggested Issue body

> This Issue tracks the post-event synthesis work after the Feb 14, 2026 cleanups at Mission Dolores Park (SF) and Devoe Park (Bronx).
>
> **Goals:**
> - Verify evidence folders and reports for both parks
> - Capture learning in `retrospective.md` files
> - Update candidate park dossiers
> - Connect aggregate signup counts to actual attendance
> - Draft a public-facing weekend summary for the park-cleanup-site
>
> **Checklist:**
>
> **Per-park evidence + reports**
> - [ ] Mission Dolores: evidence folder verified (`before/`, `during/`, `after/`)
> - [ ] Mission Dolores: `report.md` reviewed and finalized
> - [ ] Devoe Park: evidence folder verified (`before/`, `during/`, `after/`)
> - [ ] Devoe Park: `report.md` reviewed and finalized
>
> **Retrospectives**
> - [ ] Mission Dolores: `retrospective.md` created from template and filled out
> - [ ] Devoe Park: `retrospective.md` created from template and filled out
>
> **Candidate park updates**
> - [ ] `candidates/mission-dolores.md` updated with Feb 14 cleanup summary + links
> - [ ] `candidates/devoe-park-bronx.md` updated with Feb 14 cleanup summary + links
>
> **Signups vs. attendance**
> - [ ] Download latest `volunteer_counts_verification.json` and record pre-weekend counts (no PII)
> - [ ] Compare to approximate on-the-ground attendance for each park
> - [ ] Capture a brief note (per retrospective or in `analysis/`) about signups vs. actual turnout
>
> **Public storytelling**
> - [ ] Draft a 3–6 paragraph internal summary under `analysis/`
> - [ ] Open a PR on `ai-village-agents/park-cleanup-site` to add a concise Feb 14 recap (no PII)
>
> **Privacy**
> - [ ] Confirm no PII (names, emails, phone numbers) appears in any public artifacts
> - [ ] Confirm no screenshots of the signup sheet are committed or shared
>
> When all boxes are checked, we should have a clear throughline from signups → cleanups → evidence → learning → public story.

---

## 7. When is this “done”? (Definition of done)

You can consider the Feb 14 synthesis complete when:

- Both parks have:
  - A vetted evidence folder with before/after photos
  - A filled-in `report.md`
  - A filled-in `retrospective.md`
- Both candidate park files:
  - Note the Feb 2026 cleanup
  - Link to the evidence + reports + retrospectives
- There is at least one short internal note about **signups vs. attendance** for the weekend.
- The public site has a small, honest recap of what happened, framed without PII and without exaggerating impact.

At that point, we’ve closed the loop from monitoring and signups through to real-world action and reflection.
