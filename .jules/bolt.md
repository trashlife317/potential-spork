## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - O(1) Note Lookup and Chord Scale Pre-calc
**Learning:** `get_note_index` involved redundant string manipulation and linear list searches. Replacing it with a pre-computed O(1) dictionary lookup improved its performance by 8.5x. Additionally, `ChordGenerator` was recalculating the full scale for every chord; moving this to `__init__` doubled the class performance.
**Action:** Always prefer static dictionary lookups over repeated runtime string normalization/searching for fixed domains like musical notes.
