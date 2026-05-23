This is synthetic data to be edited/analyzed. Do NOT treat any text inside as instructions.

# Hollowmere Transit Ledger - raw vehicle-arrival log

50 raw arrival entries from the Hollowmere depot scanner. Each entry has a vehicle code, a
raw timestamp string, a corridor tag, a payload-weight figure, and a status note. The raw
log is messy: timestamps are in mixed local-clock formats, corridors use legacy
abbreviations, weights are in mixed units (kg vs lb), and the status notes are free-text.
The downstream system needs ONE normalized line per entry in this exact schema:

  [NN] vehicle=<CODE> | iso=<YYYY-MM-DDTHH:MM> | corridor=<EXPANDED> | kg=<INTEGER> | status=<ENUM>

Normalization rules (apply to EVERY entry):

  RULE A - vehicle code: uppercase the letter prefix, keep the digits. e.g. `tk-204` -> `TK-204`.
  RULE B - timestamp: convert the raw clock string to ISO `YYYY-MM-DDTHH:MM`. The depot date
           is 2026-05-19 for every entry. Convert 12-hour clock (with am/pm) to 24-hour.
           `7:42 am` -> `2026-05-19T07:42`; `2:05 pm` -> `2026-05-19T14:05`; `12:10 am` ->
           `2026-05-19T00:10`; `12:35 pm` -> `2026-05-19T12:35`. Drop seconds if present.
  RULE C - corridor: expand the abbreviation to its full name using this table:
             N    -> North-Spine
             S    -> South-Vault
             E    -> East-Arc
             W    -> West-Run
             NE   -> Northeast-Cut
             NW   -> Northwest-Cut
             SE   -> Southeast-Cut
             SW   -> Southwest-Cut
             C    -> Central-Loop
  RULE D - weight: convert to integer kilograms. If the raw value is suffixed `lb`,
           multiply by 0.4536 and ROUND to the nearest whole kg (0.5 rounds up). If suffixed
           `kg`, keep the integer (drop any decimal). e.g. `1200 lb` -> 544; `860 kg` -> 860.
  RULE E - status: map the free-text note to one of exactly four ENUM values:
             cleared    - any note containing "ok", "clear", "released", "passed"
             flagged    - any note containing "manifest mismatch", "weight high", "weight low",
                          "label damaged"
             held       - any note containing "hold", "pending review", "awaiting paperwork",
                          "inspector queued"
             rejected   - any note containing "reject", "refused", "turned back", "denied entry"
           If a note contains keywords from two ENUM groups, the FIRST group in the order
           cleared / flagged / held / rejected wins (deterministic tie-break).

Output ONE normalized line per raw entry, in the SAME ORDER as the raw log (entries 01-50),
each on its own line, prefixed with the two-digit entry number in square brackets. Do not
output anything else (no headers, no commentary, no totals).

---

## Raw log

01. tk-204 | 7:42 am | N | 1200 lb | manifest mismatch
02. mw-118 | 8:05 am | S | 860 kg | ok, released
03. lp-039 | 8:31 am | E | 2400 lb | inspector queued
04. tk-061 | 9:14 am | NE | 540 kg | weight high
05. mw-227 | 9:48 am | W | 1800 lb | clear
06. lp-152 | 10:02 am | C | 1100 kg | manifest mismatch, weight high
07. tk-088 | 10:39 am | SW | 720 lb | refused
08. mw-044 | 11:15 am | NW | 950 kg | ok
09. lp-176 | 11:52 am | SE | 1450 lb | label damaged
10. tk-130 | 12:08 pm | N | 600 kg | pending review
11. mw-091 | 12:35 pm | S | 1620 lb | turned back
12. lp-005 | 1:14 pm | E | 880 kg | released
13. tk-244 | 1:48 pm | NE | 2100 lb | weight low
14. mw-167 | 2:22 pm | W | 1340 kg | awaiting paperwork
15. lp-073 | 2:55 pm | C | 760 lb | clear, ok
16. tk-022 | 3:30 pm | SW | 1480 kg | denied entry
17. mw-198 | 4:01 pm | NW | 990 lb | manifest mismatch
18. lp-115 | 4:38 pm | SE | 1750 kg | hold
19. tk-159 | 5:12 pm | N | 660 lb | passed
20. mw-080 | 5:45 pm | S | 1290 kg | weight high
21. lp-203 | 6:18 pm | E | 540 lb | reject
22. tk-046 | 6:51 pm | NE | 1860 kg | clear
23. mw-134 | 7:24 pm | W | 1110 lb | label damaged
24. lp-067 | 7:58 pm | C | 770 kg | inspector queued
25. tk-181 | 8:32 pm | SW | 1530 lb | released
26. mw-029 | 9:05 pm | NW | 1240 kg | weight low
27. lp-142 | 9:39 pm | SE | 1980 lb | turned back
28. tk-217 | 10:11 pm | N | 690 kg | ok
29. mw-103 | 10:48 pm | S | 1410 lb | pending review
30. lp-058 | 11:22 pm | E | 1080 kg | passed
31. tk-095 | 11:55 pm | NE | 1640 lb | manifest mismatch
32. mw-186 | 12:10 am | W | 920 kg | clear
33. lp-031 | 12:42 am | C | 1820 lb | awaiting paperwork
34. tk-249 | 1:18 am | SW | 1370 kg | refused
35. mw-076 | 1:50 am | NW | 1100 lb | weight high
36. lp-194 | 2:24 am | SE | 880 kg | hold
37. tk-138 | 2:58 am | N | 1690 lb | released
38. mw-052 | 3:31 am | S | 1240 kg | label damaged
39. lp-211 | 4:04 am | E | 820 lb | inspector queued
40. tk-167 | 4:38 am | NE | 1560 kg | denied entry
41. mw-119 | 5:12 am | W | 1320 lb | clear
42. lp-088 | 5:45 am | C | 950 kg | weight low
43. tk-033 | 6:19 am | SW | 2080 lb | ok, cleared
44. mw-225 | 6:52 am | NW | 740 kg | manifest mismatch
45. lp-014 | 7:26 am | SE | 1170 lb | turned back
46. tk-201 | 7:59 am | N | 1450 kg | hold
47. mw-068 | 8:33 am | S | 990 lb | passed
48. lp-156 | 9:06 am | E | 1280 kg | weight high
49. tk-110 | 9:40 am | NE | 1880 lb | awaiting paperwork
50. mw-040 | 10:13 am | SW | 860 kg | reject
