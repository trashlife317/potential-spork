## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-20 - Static Lookup Tables for High-Frequency Helpers
**Learning:** `get_note_index` was performing redundant string manipulation and linear search on every call (~1.4µs). Replacing this with a static O(1) dictionary lookup reduced execution time to ~0.16µs (8.8x speedup).
**Action:** Identify other frequently called helper functions that perform repetitive calculations on limited inputs and refactor them to use static lookup tables.
