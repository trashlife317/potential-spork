## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - ChordGenerator Scale Caching
**Learning:** `ChordGenerator.get_chord_notes` was recalculating the full scale (using `get_scale_notes`) for every single chord in a progression. This involves list construction and sorting. Moving this to `__init__` yielded a ~6x speedup (0.57s -> 0.09s per 10k calls).
**Action:** Always verify if helper functions called inside loops (like `get_scale_notes`) are performing heavy lifting that can be cached.
