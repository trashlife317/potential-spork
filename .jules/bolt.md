## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - O(1) Note Lookup & Loop Hoisting
**Learning:** `get_note_index` used O(N) list scanning and string ops, which was called thousands of times inside nested loops (scales, chords). Moving invariant calculations (like scale generation in `ChordGenerator`) to `__init__` and replacing list scans with O(1) dict lookups yielded a ~6x speedup for note parsing.
**Action:** Always check basic utility functions used in inner loops. If they do string parsing or list lookups, optimize them first.
