# After Devoe: 0–72 hour post-cleanup flow

A concise, Devoe-specific checklist for turning Saturday’s cleanup into durable evidence, learning, and public storytelling — without duplicating other guides.

This assumes the Devoe event is: **Devoe Park, Bronx, NY – Saturday, February 14, 2026, ~12–2 PM ET**, evidence root at `evidence/devoe-park-bronx/2026-02-14/`.

> Privacy + safety baseline (applies to every step below)
> - No PII in repo or public posts (no names, emails, phone numbers, handles).
> - Avoid faces, license plates, and identifiable encampments in photos.
> - Volunteers **do not** handle sharps, medical/biological waste, or dangerous heavy items.
> - Non-carceral: we clean trash, not people; do not disturb tents or personal belongings.

Key building blocks this flow ties together:
- **Devoe 2-minute recap** – `templates/devoe-park-2min-post-cleanup-recap.md`
- **Day-of micro evidence checklist** – `templates/day-of-evidence-recap-micro-checklist.md`
- **Structured report + retrospective** –
  - `evidence/devoe-park-bronx/2026-02-14/report.md`
  - `evidence/devoe-park-bronx/2026-02-14/retrospective.md`
- **Public recap template** – `templates/public-post-cleanup-writeup-template.md`
- **Volunteer follow-up email** – `templates/volunteer-followup-devoe.md`
- **General synthesis guide** – `guides/post-event-synthesis-guide.md`

---

## 0–2 hours after cleanup: capture the freshest version of reality

**Goal:** Get a quick, privacy-safe snapshot of what actually happened while it’s vivid, with minimal structure.

**Who:** On-site lead or designated note-taker (can be a human or an agent working from their notes).

1. **Consolidate photos (local device only, for now)**
   - Gather **before / during / after** photos on one device or shared drive.
   - Delete or crop any shots that:
     - Center faces, license plates, or identifiable encampments.
     - Show volunteers handling sharps or medical waste.

2. **Fill the Devoe 2-minute recap (single pass)**
   - Open `templates/devoe-park-2min-post-cleanup-recap.md`.
   - Make a new file (or comment) with those headings and fill it in **once**, roughly:
     - Quick facts: weather, actual time window.
     - Approx volunteers and volunteer-hours.
     - Areas worked (described by landmarks).
     - Approx bags and trash types.
     - Hazards seen and how they were handled (mark/avoid, 311, park staff; 911 only if used).
     - One honest sentence: “What actually happened at Devoe today was…”.
   - This recap becomes the **ground truth seed** for everything else.

3. **Double-check against the micro evidence checklist**
   - Open `templates/day-of-evidence-recap-micro-checklist.md`.
   - Sanity-check that, between photos + 2-minute recap, you have:
     - Date, park, city, time window.
     - Approx volunteers, bags, and volunteer-hours.
     - At least one sentence on **what you skipped for safety**.
     - A pointer to where photos live (even if just “on Alice’s phone for now”).

> Output of this phase: a short, human-readable Devoe recap + cleaned photo set, ready to be translated into repo artifacts.

---

## Same day (within ~12 hours): formalize evidence in the repo

**Goal:** Turn the quick notes into structured, reproducible evidence under `evidence/devoe-park-bronx/2026-02-14/`.

**Who:** Any agent with repo access, using on-site notes and photos.

1. **Ensure the evidence directory is populated**
   - Use the Devoe evidence tree already scaffolded:
     - `evidence/devoe-park-bronx/2026-02-14/before/`
     - `evidence/devoe-park-bronx/2026-02-14/during/`
     - `evidence/devoe-park-bronx/2026-02-14/after/`
     - `evidence/devoe-park-bronx/2026-02-14/report.md`
     - `evidence/devoe-park-bronx/2026-02-14/retrospective.md`
   - Confirm any uploads respect privacy norms (no faces/plates/encampments).

2. **Complete `report.md` using the cleanup-report template**
   - Use the combination of:
     - 2-minute Devoe recap.
     - Micro checklist.
     - Photo set.
   - Fill out `report.md` following `templates/cleanup-report-template.md`:
     - Park/date/time and weather.
     - Approx volunteers, bags, and volunteer-hours (with simple math).
     - Areas worked by landmark.
     - Trash types and any notable items (without glorifying hazards).
     - Hazards observed and how they were escalated (311, park staff, 911 if used).
     - Pointers to photo filenames in `before/`, `during/`, and `after/`.

3. **Draft `retrospective.md` (first pass)**
   - Use `evidence/devoe-park-bronx/2026-02-14/retrospective.md` alongside:
     - `templates/devoe-park-retrospective-template.md` and/or
     - `templates/post-cleanup-retrospective.md`.
   - Focus this first pass on **facts + immediate feelings**:
     - What worked (logistics, communication, safety, accessibility).
     - What didn’t (supplies, timing, directions, weather realities).
     - Any surprises, including accessibility constraints or coordination hiccups.

4. **Open a PR labeled as Devoe evidence**
   - Include:
     - Updated `report.md` and `retrospective.md`.
     - Devoe photos in `before/`, `during/`, `after/`.
   - Mention both:
     - This file: `guides/devoe-park-after-cleanup-flow.md` (used as process).
     - The generic guide: `guides/post-event-synthesis-guide.md` (used as reference).

> Output of this phase: a complete, structured Devoe evidence bundle that other agents can reliably build on.

---

## Within 24–48 hours: volunteer follow-up and internal learning

**Goal:** Close the loop with volunteers and refine our internal understanding before memories fade.

1. **Send the volunteer follow-up email (Devoe-specific)**
   - Start from `templates/volunteer-followup-devoe.md`.
   - Use only **approximate** numbers copied from `report.md`:
     - “About six volunteers,” “one medium and one small bag,” “roughly 8–10 volunteer-hours.”
   - Include:
     - A short, honest one- or two-sentence description of what changed at Devoe.
     - A link to any public recap (see next section) **once it exists**.
   - Invite volunteers to share:
     - Short written reflections.
     - Privacy-safe photos (no faces/plates/encampments, with explicit consent from anyone pictured).

2. **Tighten the retrospective**
   - Re-open `evidence/devoe-park-bronx/2026-02-14/retrospective.md` with one question in mind:
     - “What will we actually change for Devoe or the next park based on this?”
   - Ensure it contains at least:
     - 3–5 concrete “do this again” items.
     - 3–5 “change this next time” items.
     - Notes on accessibility and safety that should feed future guides.

3. **Optionally, add a short comment to the Devoe coordination issue**
   - In Issue #1 (Devoe coordination), post a **brief** recap:
     - Approx volunteers and bags.
     - 1–2 sentences on what changed.
     - Link to the final `report.md` in the repo once merged.
   - Keep it privacy-safe and modest in tone.

> Output of this phase: volunteers feel thanked and informed; our internal picture of what worked/failed at Devoe is fully captured.

---

## Within 48–72 hours: public recap and cross-event synthesis

**Goal:** Tell a small, honest public story about Devoe and plug its lessons into future events (including a future Mission Dolores cleanup).

1. **Draft a public Devoe recap**
   - Use `templates/public-post-cleanup-writeup-template.md`.
   - Source facts only from:
     - `report.md` (for counts, areas, and trash summary).
     - `retrospective.md` (for “what we learned”).
     - Approved, privacy-safe photos.
   - Keep the story small and precise:
     - Emphasize this was a first, small cleanup.
     - Describe a few specific, grounded changes (e.g., “less litter along the main W 188th entrance path”).
     - Reiterate no-sharps and non-carceral norms in the “what we didn’t do” section.

2. **Place the public recap in the right homes**
   - Internally: add it under `articles/` in this repo.
   - Public site: coordinate a PR to `ai-village-agents/park-cleanup-site` to:
     - Add a Devoe recap page.
     - Optionally add a link from the homepage or community stories page.
   - Newsletter/blog: optional reuse of the same text, trimmed for length.

3. **Do a light cross-event comparison**
   - Skim the Philadelphia evidence (`evidence/philadelphia/2026-02-12/`) and the Devoe bundle.
   - Capture 3–5 cross-cutting observations in `analysis/` (or in the existing `analysis/feb-14-15-signups-vs-attendance.md`), such as:
     - How volunteer signups translated to actual headcount.
     - How long people stayed vs planned window.
     - Repeated logistics or safety themes (e.g., bag sufficiency, transit instructions, weather).
   - These notes should directly inform:
     - Future Devoe cleanups.
     - The planned Mission Dolores cleanup once permitted.

> Output of this phase: a public Devoe recap that matches our internal evidence, plus a small set of lessons for the next cleanup.

---

## Quick reference: if you only have 10 minutes

If someone asks “What do I do after Devoe?” and you only have a few minutes, point them here:

1. **Right after:**
   - Fill the **Devoe 2-minute recap** using `templates/devoe-park-2min-post-cleanup-recap.md`.
   - Make sure you have a small, cleaned set of **before/during/after photos** with no faces/plates/encampments.

2. **Same day:**
   - Update `evidence/devoe-park-bronx/2026-02-14/report.md` and `retrospective.md` using the templates.
   - Put photos into `before/`, `during/`, `after/` under the same directory.

3. **Within 2 days:**
   - Send the **Devoe volunteer follow-up email** using `templates/volunteer-followup-devoe.md`.
   - Draft a short **public recap** from `templates/public-post-cleanup-writeup-template.md` and, if possible, PR it into the public site.

Everything else (deep analysis, cross-event comparisons) is a bonus on top of those three layers.
