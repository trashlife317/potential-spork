## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-20 - Pre-computed Note Index Map
**Learning:** Replacing runtime string normalization and linear search in `get_note_index` with a pre-computed dictionary (`NOTE_TO_INDEX`) reduced execution time by ~10x (3.49µs -> 0.32µs).
**Action:** When refactoring for performance, always ensure edge cases (like "dB") supported by the original inefficient logic (e.g., via `.capitalize()`) are either covered by the new data structure or handled by a lightweight fallback.
