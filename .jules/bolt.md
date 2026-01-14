## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-20 - Hoisting Scale Calculation in Accompaniment
**Learning:** `ChordGenerator.get_chord_notes` was calling `get_scale_notes` (an O(N) operation with string parsing) inside the progression loop. Moving this to `__init__` reduced generation time from ~1.57s to ~0.26s (6x speedup).
**Action:** Always check if helper functions called inside loops depend only on instance state (invariant) and can be cached in `__init__`.
