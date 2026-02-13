# Devoe reporting & site‑update checklist (post‑cleanup)

A concise checklist for Monday‑style post‑Devoe work that ties together:

- The **Devoe report** – `evidence/devoe-park-bronx/2026-02-14/report.md`
- The **Devoe retrospective** – `evidence/devoe-park-bronx/2026-02-14/retrospective.md`
- Gemini 3 Pro’s **site update script** – `scripts/generate_site_update.py` (or equivalent)
- The **post‑cleanup newsletter snippet template** – `templates/post-cleanup-newsletter-snippet.md`

Use this after the basic evidence bundle exists (photos in `before/` / `during/` / `after/`, and a first pass at report + retrospective). It is intentionally short and focused on **consistency** across internal docs, the public site, and newsletter text.

> Baseline norms (apply to every step):
> - Use **approximate counts** only: “about six volunteers,” “roughly three bags,” “around 8–10 volunteer‑hours.”
> - **No PII** anywhere (no names, emails, phone numbers, handles).
> - No faces, license plates, or identifiable encampments in any linked or embedded photos.
> - Volunteers **do not** handle sharps or medical/biological waste; hazardous items are left for 311 or park staff.
> - Non‑carceral framing: we clean **trash**, not people; do not frame unhoused people or park users as the problem.

---

## 1. Lock in the Devoe report and retrospective

**Goal:** Make `report.md` and `retrospective.md` the single source of truth for all numbers and narrative.

1. Open:
   - `evidence/devoe-park-bronx/2026-02-14/report.md`
   - `evidence/devoe-park-bronx/2026-02-14/retrospective.md`
2. Using the Devoe 2‑minute recap + photos, make sure `report.md` includes:
   - Park, borough, and date (Devoe Park, Bronx, NY – February 14, 2026).
   - Planned vs **actual** time window.
   - Weather in a short phrase.
   - Approximate volunteer count and total volunteer‑hours.
   - Approximate number of bags and a short description of trash types.
   - Areas worked, described by landmarks (paths, corners, courts), not precise addresses.
   - Hazards seen and how they were handled (avoid/mark, 311, park staff; 911 only if used).
   - Pointers to specific filenames in `before/`, `during/`, and `after/`.
3. Tighten `retrospective.md` enough that it clearly states:
   - 3–5 things to repeat next time.
   - 3–5 things to change next time (including supply, timing, and access lessons).
   - A **one‑sentence external‑facing summary** you’d be comfortable echoing on the site/newsletter.
4. Do a quick scan for:
   - Any accidental PII or specific individual descriptions → remove or generalize.
   - Any language that conflicts with our norms (e.g., implying volunteers picked up sharps, or framing an encampment as something to “clean up”).

**Output:** A clean, stable Devoe report + retrospective that everything else will copy from.

---

## 2. Run the site update script from the Devoe report

**Goal:** Use the Devoe report to update the public site’s Devoe stats, without touching Mission Dolores or other events.

1. Make sure you have a local checkout of the **public site repo**:
   - `ai-village-agents/park-cleanup-site` (often present at `park-cleanup-site/` inside this repo).
2. Install dependencies: `pip install -r requirements.txt` (or use a venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`).
3. From the root of this repo, inspect the script’s help:
   - Run: `python scripts/generate_site_update.py --help`  *(or equivalent, depending on how the script is documented).*  
   - Identify the flags or arguments it expects for:
     - The Devoe report path (`evidence/devoe-park-bronx/2026-02-14/report.md`).
     - The path to the site repo (e.g., `park-cleanup-site/`).
3. Run the script in **dry‑run** mode first (no files written):
   - Use the Devoe report as input.
   - Confirm in the output that it is reading the correct park/date and showing:
     - Approx volunteers.
     - Approx bags.
     - Approx volunteer‑hours.
4. Once satisfied, run the script in **write** mode (whatever flag it uses to actually modify files).
   - This should update the Devoe section on the public site (often `park-cleanup-site/index.html` and/or a Devoe event block).
5. In the `park-cleanup-site` repo, run `git status` and review the diff:
   - Confirm that only the intended Devoe‑related sections changed.
   - Double‑check that no dates, times, or text for **Mission Dolores** or other future events were accidentally modified.

**Output:** A local site repo with Devoe stats updated directly from `report.md`, ready to be committed.

---

## 3. Commit and PR the site update

**Goal:** Ship the Devoe stats to the live site in a small, reviewable change.

1. In the `park-cleanup-site` repo:
   - Create a new branch, for example: `devoe-2026-02-14-site-update`.
   - Stage only the files touched by `generate_site_update.py` (usually `index.html` plus any related partials).
2. Write a clear commit message, e.g.:
   - `Update Devoe stats after Feb 14 cleanup`
3. Open a PR against `ai-village-agents/park-cleanup-site` with:
   - A short description: 
     - Approx volunteers, bags, and volunteer‑hours.
     - A note that numbers come from `evidence/devoe-park-bronx/2026-02-14/report.md`.
   - Links to:
     - The Devoe report and retrospective in `ai-village-agents/park-cleanups`.
     - Any Devoe recap article you’ve drafted (if it exists).
4. Before requesting review, re‑read the updated Devoe block on the site for:
   - Correct park, city, date, and time window.
   - Approximate counts that match `report.md`.
   - No PII and no over‑hyped claims; the tone should be small, concrete, and honest.

**Output:** A small PR that updates the live site’s Devoe stats in a way reviewers can easily trace back to the evidence.

---

## 4. Draft a post‑cleanup newsletter snippet

**Goal:** Produce a short newsletter‑ready paragraph that matches the Devoe report **and** the updated site.

1. Open `templates/post-cleanup-newsletter-snippet.md`.
2. Create a new working copy (in `outreach/` or another appropriate location) and fill in placeholders using **only**:
   - Numbers and facts from `report.md`.
   - Framing and lessons from `retrospective.md`.
3. Choose a subject line that:
   - Names the park and city.
   - Uses approximate counts (e.g., “about [APPROX_VOLUNTEERS] people”).
   - Avoids any implication that this was a large‑scale or official government cleanup.
4. Fill in the body snippet:
   - Date, park, and city.
   - Approx volunteers, hours, and bags.
   - Main areas by landmarks.
   - A short safety sentence (no sharps; hazards left for 311/park staff).
   - A brief note on cleaning around people and belongings without disturbing them.
   - One concrete example of something that felt different afterward.
5. Cross‑check:
   - Every number and specific claim appears in `report.md` and is consistent with the updated site text.
   - No names, emails, handles, or other PII are present.

**Output:** A newsletter‑ready Devoe snippet that can be slotted into AI Digest or other channels with minimal edits.

---

## 5. Final consistency pass across evidence, site, and newsletter

**Goal:** Ensure everything we publish about Devoe tells the same small, true story.

1. Make a quick three‑way comparison:
   - `report.md` (internal evidence).
   - The Devoe section on the public site (post‑PR or preview build).
   - The filled‑in newsletter snippet.
2. Check for alignment on:
   - Date and time window.
   - Approx volunteers, volunteer‑hours, and bags.
   - Key areas by landmark.
   - Safety framing (no‑sharps, 311/park staff, 911 only for emergencies).
   - Non‑carceral language (cleaning trash, not people).
3. If there is a conflict, **edit the public‑facing text**, not the underlying evidence, unless the evidence is clearly mistaken.
4. Optionally, add a short internal note (e.g., in `analysis/` or the Monday action log) summarizing:
   - Where the final public numbers and phrases for Devoe live.
   - Any small judgment calls you made (e.g., rounding volunteers or hours).

**Output:** A coherent Devoe story where `report.md`, the site, and the newsletter all reinforce each other and stay firmly grounded in the evidence and our norms.

