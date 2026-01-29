## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - Lookup Table for Note Indexing
**Learning:** Replacing linear search and string normalization in `get_note_index` with a pre-calculated `NOTE_TO_INDEX` dictionary improved lookup speed by ~10x (1.32µs -> 0.13µs).
**Action:** When working with finite, known sets of string keys (like musical notes), prefer static dictionary lookups over runtime parsing and list searches.
