## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - Optimization of String Normalization via Lookup Tables
**Learning:** `get_note_index` used runtime string normalization (capitalization, flat mapping) and linear search. Replacing this with a pre-computed `NOTE_TO_INDEX` dictionary containing all permutations (case, flats) resulted in a >10x speedup (4.79us -> 0.44us).
**Action:** When a function performs static string normalization on a finite set of inputs (like notes, modes, keys), pre-compute a lookup map for O(1) access instead of parsing at runtime.
