## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - O(1) Note Lookup
**Learning:** Parsing strings and linear searching in tight loops (`get_note_index`) is costly. Using a pre-computed dictionary with all case variations yielded a ~12x speedup (1.27us -> 0.10us).
**Action:** Replace `list.index()` with dictionary lookups for static sets like notes, scales, or drum mappings.
