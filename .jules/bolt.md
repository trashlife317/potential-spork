## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - Static Lookup for Note Indexing
**Learning:** Replacing runtime string normalization and linear search in `get_note_index` with a static `NOTE_TO_INDEX` dictionary yielded a ~9.6x speedup. `ChordGenerator` also saw a ~16% improvement.
**Action:** Prioritize converting frequent string-to-index mappings (like scale types or drum names) to static dictionaries.
