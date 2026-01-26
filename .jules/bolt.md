## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - Optimized Note Index Lookup
**Learning:** `get_note_index` in `music_theory.py` used linear search and repeated dictionary creation, costing ~1.25µs per call. Replacing this with a static pre-computed `NOTE_TO_INDEX` hash map reduced lookup time to ~0.09µs (~13x faster).
**Action:** Replace string normalization and linear list searches with pre-computed dictionaries for frequently accessed static data (like notes, scales, or fixed configurations).
