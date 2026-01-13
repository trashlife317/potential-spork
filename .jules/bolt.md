## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - Library-level Lookups
**Learning:** Optimizing `get_note_index` with O(1) dictionary lookups (replacing list searches and string parsing) provided a ~6x speedup for that specific function. Since this is a low-level utility called everywhere (scales, stability checks), it lifts performance globally.
**Action:** Prioritize optimizing low-level utility functions ("leaf nodes" of the call graph) that are called inside loops of higher-level generators.
