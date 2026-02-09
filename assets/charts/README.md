# 311 charts

These PNGs are generated from the CSV extracts in `data/**`.

Regenerate locally:

```bash
python scripts/make_311_charts.py
```

Notes:
- These charts visualize *the extract in this repo* (generally last-30-days 311 pulls), not a full historical dataset.
- Categories reflect whatever the upstream 311 API returned for the given query (e.g., SF `service_name`, NYC `complaint_type`).
