## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - O(1) Note Lookup
**Learning:** `get_note_index` relied on recreating a dictionary and linear search (`list.index`) on every call. Pre-computing a `NOTE_TO_INDEX` hash map (including normalized variants) reduced execution time from ~1.4µs to ~0.12µs (11x speedup).
**Action:** Replace `list.index` with dictionary lookups for fixed sets of strings, and pre-normalize keys where possible to avoid repeated string manipulation.
