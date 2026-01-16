## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-20 - Optimizing Frequent Lookups and Invariant Calculations
**Learning:** `get_note_index` was a hot path called thousands of times. By pre-calculating lookup tables (`NOTE_TO_INDEX`), we achieved a ~6.7x speedup in this utility. Similarly, `ChordGenerator` was recalculating the full scale on every chord generation; moving this to `__init__` yielded another 2x improvement for that component.
**Action:** Always verify if utility functions used in loops (like note parsing) are O(1). Pre-calculate any data that depends only on initialization parameters.
