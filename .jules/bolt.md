## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-05-21 - Optimizing Hot Path Note Lookup
**Learning:** `get_note_index` was rebuilding a dictionary and performing a linear search on every call. In high-frequency loops (like checking scale degrees for every note generated), this added up. Extracting constants to module level and using O(1) dictionary lookups improved the function's performance by ~4x (0.3µs vs 1.3µs).
**Action:** Identify helper functions that are called in loops and ensure they don't perform unnecessary allocations or linear searches. Use module-level constants for immutable lookup tables.
