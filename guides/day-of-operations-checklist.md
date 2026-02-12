# Day-of operations checklist for park cleanups

This checklist is for humans who are **physically at the park** on the day of a cleanup. It is meant to be lightweight, printable, and easy to scan on a phone.

It assumes:
- You have already picked a park and date.
- There is a simple plan for how volunteers will find you (issue, email, or DM thread).
- You’ve read the general [Safety & Best Practices Guide](../safety.md) and any park-specific guide under guides/.

---

## 0. Before you leave home

- [ ] **Personal safety + comfort**
  - [ ] Closed-toe shoes
  - [ ] Weather-appropriate clothing (layers, sun/ rain protection)
  - [ ] Work or gardening gloves (plus a spare pair if you can)
  - [ ] Water and a small snack


- [ ] **Cleanup gear** (as available)
  - [ ] Trash bags (contractor or heavy-duty if possible)
  - [ ] Trash grabbers or tongs
  - [ ] Hand sanitizer or wipes
  - [ ] Optional: sharps container or thick plastic bottle with lid (if you have one and know how to use it safely)

- [ ] **Docs to glance at once** (no need to memorize)
  - [ ] safety.md
  - [ ] Park-specific guide (e.g., guides/mission-dolores-cleanup-guide.md, guides/devoe-park-cleanup-guide.md)
  - [ ] Any local rules (e.g., SF group volunteer requirements for Mission Dolores)

---

## 1. On arrival at the park

- [ ] **Pick a safe, visible meetup spot**
  - Somewhere easy to describe (e.g., near the playground entrance or by the tennis courts).
  - Not blocking paths, vendors, or park staff.

- [ ] **Quick safety huddle (5 minutes)** with anyone helping
  - [ ] PPE on (gloves at minimum).
  - [ ] Eyes before hands rule — look carefully before reaching anywhere you can’t clearly see.
  - [ ] Do not handle needles, broken glass, or other sharp/medical waste unless you are trained and equipped.
  - [ ] Respect all park users, including unhoused neighbors and vendors.
  - [ ] Do not disturb tents or personal belongings. Use 311 or park staff for hazards.
  - [ ] Keep bags small enough to lift safely; don’t overload.

- [ ] **Decide who is doing what**
  - [ ] One person notes bag counts, approximate volunteer count, and rough area covered.
  - [ ] One person is photo lead for before/after shots.

---

## 2. Before photos (5–10 minutes)

Goal: a small set of photos that show starting conditions without exposing PII.

- [ ] Choose 3–5 vantage points that:
  - [ ] Show littered areas you plan to work on.
  - [ ] Avoid faces, license plates, or identifiable bystanders if possible.
  - [ ] Avoid focusing on encampments or personal belongings.

- [ ] From each vantage point:
  - [ ] Take 1–2 clear before photos.
  - [ ] Mentally note something you can replicate later (a tree, bench, path, or sign) so after photos line up.

If people are in the frame and can’t be avoided, wait a moment if possible, or shift your angle so they’re not the focus.

---

## 3. During the cleanup (30–90 minutes)

- [ ] Work in pairs or small clusters where possible.
- [ ] Keep bags where you can see them and avoid blocking paths.
- [ ] If you encounter hazards (needles, medical waste, suspicious containers, large dumped items):
  - [ ] Stop and step back.
  - [ ] Use local non-emergency channels (311, park staff) instead of handling it yourself.

Optional during photos:
- [ ] If you want a few in-progress photos, take them from similar angles as your before set.
- [ ] Avoid close-ups of faces; aim for wide shots where people are not identifiable.

Ongoing notes (can be mental or in your phone):
- [ ] Approximate number of helpers.
- [ ] Rough time spent (e.g., 4 people for a bit over an hour → ~4 volunteer-hours).
- [ ] Any notable items removed (large furniture, unusual dumping patterns, etc.).

---

## 4. Wrap-up and after photos

When you are ready to stop:

- [ ] Cluster filled bags together in a safe, visible location.
  - [ ] Keep them off fragile vegetation if possible.
  - [ ] Place them where city staff or maintenance crews can reach them.

- [ ] Count bags
  - [ ] Note the number of full (or mostly full) bags.
  - [ ] If bags are different sizes, note that (e.g., 6 kitchen bags + 2 large contractor bags).

- [ ] Take after photos from the same vantage points as your before set.
  - [ ] Try to line up angles so that before/after comparisons are obvious.
  - [ ] Again, avoid faces and identifiable bystanders where possible.

- [ ] Check for anything left behind
  - [ ] Tools, personal items, or stray bags.

---

## 5. Same-day evidence notes

Before you leave the park or soon after you get home, capture a short summary while it is fresh:

- [ ] Park and rough area cleaned (e.g., lower slope near tennis courts).
- [ ] Date and approximate time window.
- [ ] Approximate volunteer count and volunteer-hours.
- [ ] Bag count (and any large items or hazards you escalated to 311 or park staff).
- [ ] Anything that felt important: interactions with neighbors, what surprised you, what was harder/easier than expected.

You can put this into:
- A comment on the relevant GitHub Issue, or
- A short note in the evidence report.md if you have direct repo access.

## 6. How this connects to the repo

If you or an agent are mirroring the cleanup into this repository:

- [ ] Create or locate the evidence folder:

  evidence/<park-slug>/<YYYY-MM-DD>/
    before/
    during/   # optional
    after/

- [ ] Upload or move vetted photos into before/, during/ (optional), after/.
- [ ] Copy templates/cleanup-report-template.md into that folder as report.md.
- [ ] Use your same-day notes to fill out report.md.
- [ ] Later (same day or soon after), copy templates/post-cleanup-retrospective.md into the same folder as retrospective.md and fill it out.

For what to do after reports and retrospectives are in place (especially for the Feb 14–15 weekend), see guides/post-event-synthesis-feb-14-15.md.
