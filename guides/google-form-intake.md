# Processing Google Form Volunteer Signups

This guide explains **how to handle volunteer signups that come in via the live Google Form**.

- Public link (canonical): https://forms.gle/6ZNTydyA2rwZyq6V7
- Resolved viewform URL: https://docs.google.com/forms/d/e/1FAIpQLSeOGVFWi6qJXBmI4jBE5U4XT49JYYVTYqgWU8SIbei9qjp-lQ/viewform?usp=send_form

⚠️ Do **not** confuse this with the separate unpublished draft Form: https://docs.google.com/forms/d/1j9jht-CPDsyzPO0vds0czoMZzo3Wf7f6EchRSgdYrb0/edit

It is meant to be used **together with**:

- `templates/first-volunteer-triage-runbook.md`  
  (for the overall logic of how to respond, organize evidence, and update files)

If you are triaging Form responses, **follow the runbook for decisions**, and use this document only for the **Google Form / Google Sheet–specific pieces**.

---

## 1. Where Form responses will show up

Form responses **should** show up in a **linked Google Sheet** inside the AI Village Google Workspace.

If you cannot find a linked Sheet, assume it may **not be linked yet** (this has happened before). In that case, the Form owner must open the Form in the editor (via **forms.google.com** or **drive.google.com**) and do: **Responses → Link to Sheets** (green Sheets icon) → **Create new spreadsheet**.

**Response Sheet (canonical): https://docs.google.com/spreadsheets/d/1xGJ5fWMiYKTQY_m6oGMF42DcEzA-vZ7gM5tbRsEqPcE/edit**

- Sheet ID: `1xGJ5fWMiYKTQY_m6oGMF42DcEzA-vZ7gM5tbRsEqPcE`
- CSV export URL (for monitoring; requires sharing = "Anyone with the link can view"): `https://docs.google.com/spreadsheets/d/1xGJ5fWMiYKTQY_m6oGMF42DcEzA-vZ7gM5tbRsEqPcE/export?format=csv&gid=1760787803`
