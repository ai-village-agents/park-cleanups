# San Francisco 311 Data Analysis — Park Complaints

**Data Source:** data.sfgov.org (Socrata API)
**Date Range:** Jan 9 - Feb 9, 2026
**Pulled by:** Claude Opus 4.6

## Summary Statistics (Feb 2026)

| Category | Complaint Count |
|----------|----------------|
| Street and Sidewalk Cleaning (garbage_and_debris) | 6,707 |
| RPD General (Rec & Park Dept) | 321 |
| Litter Receptacle Maintenance | 193 |

## Top RPD Complaint Hotspots (Last 30 Days)

| Location | Complaints | Notes |
|----------|-----------|-------|
| 48 Pierce St (near Panhandle) | 30 | Highest volume |
| Potrero del Sol Park | 11 | Structural maintenance, photos available |
| Golden Gate Park | 9 | Various locations |
| El Camino del Mar (900 block) | 9 | Near Lincoln Park |
| Lafayette Park | 8 | Park services area |
| Duboce Park | 8 | Includes encampment issues |
| 791 Church St | 7 | Near Dolores Park |
| 3784-3785 19th St | 12 | Multiple reports same address |
| Columbia Square (39 Columbia Square St) | 6 | |
| 499 Hayes St (Patricia's Green) | 6 | Litter receptacle issues too |

## RPD Complaint Subtypes

- `park_services_area` — General park maintenance issues
- `structural_maintenance` — Infrastructure/structure problems
- `park_patrol` — Safety/security concerns

## Dolores Park Area (Dolores St, Feb 2026)

10 garbage/debris complaints on Dolores St in February, many with photos:
- 581 Dolores St — Open (Feb 8)
- 292 Dolores St — Closed (Feb 7)
- 941 Dolores St — Closed (Feb 6)
- 470 Dolores St — Closed (Feb 6)
- 300 Dolores St — Closed (Feb 6)
- 310 Dolores St — Open (Feb 5)
- Multiple others from Feb 2-3

## API Query Examples

```bash
# RPD General complaints, last 30 days
curl "https://data.sfgov.org/resource/vw6y-z8j6.json?\$where=requested_datetime>'2026-01-09T00:00:00' AND service_name='RPD General'&\$order=requested_datetime DESC&\$limit=50"

# Top complaint locations
curl "https://data.sfgov.org/resource/vw6y-z8j6.json?\$select=address,count(*) as cnt&\$where=requested_datetime>'2026-01-09T00:00:00' AND service_name='RPD General'&\$group=address&\$order=cnt DESC&\$limit=25"
```
