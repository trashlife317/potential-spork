## 2024-05-23 - [Pre-calculation in Data Classes]
**Learning:** Pre-calculating derived subsets of data (like `stable_notes` from `scale_notes`) in `__init__` is far more effective than filtering inside a loop, especially when the loop runs frequently (per phrase end). Even if the `__init__` cost is per-request, the reduced complexity in the generation logic simplifies the code and improves theoretical bounds (O(N) -> O(1) or O(small_set)).
**Action:** Always check if repetitive checks inside a generation loop can be hoisted to the initialization phase.
