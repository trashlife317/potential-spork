# AGENTS.md

## Project Overview
This repository contains a **MIDI Beat Starter Generator**. It is a Python-based tool that uses music theory algorithms to generate hip-hop/trap melodies, chord progressions, and drum patterns. It functions as both a **CLI tool** (`src/main.py`) and an **MCP Server** (`src/server.py`) for AI assistants.

## Codebase Structure
The source code is located in the `src/` directory:

*   **`src/music_theory.py`**: Defines scales, intervals, and stability rules. **Always use this** for musical logic; do not hardcode scale notes.
*   **`src/generator.py`**: Contains `MelodyGenerator`. Implements phrasing (AABA), voice leading, and variations.
*   **`src/accompaniment.py`**: Contains `ChordGenerator` and `DrumGenerator`. Handles backing tracks.
*   **`src/midi_utils.py`**: A **custom, dependency-free** MIDI writer.
    *   *Constraint*: Do not introduce external MIDI libraries (like `mido` or `music21`) for writing files. Maintain this binary writer to keep the core lightweight.
*   **`src/main.py`**: The CLI entry point.
*   **`src/server.py`**: The MCP (Model Context Protocol) server entry point using `FastMCP`.

## Development Guidelines

1.  **Imports**: When creating entry points (scripts that run `if __name__ == "__main__":`), you must ensure they can import the `src` package.
    *   Use `sys.path.append(os.getcwd())` if running from the root is expected.
2.  **Binary Artifacts**: Never commit `__pycache__` directories or `.pyc` files.
3.  **Tests**:
    *   All new logic must be tested.
    *   Run tests using: `python3 -m unittest discover -s src -p "test_*.py"`
4.  **Formatting**: Follow PEP 8 guidelines.

## MCP Server Instructions
The `src/server.py` exposes a single tool: `generate_beat`.
*   **Input**: Key, Scale, Tempo, Bars, etc.
*   **Output**: A Base64-encoded string representing the MIDI binary data.
*   **Testing**: Use `src/test_mcp_logic.py` to verify that the server logic produces valid Base64 MIDI data without needing to actually run the full HTTP server.

## Future Agents
If you are asked to extend the music capabilities:
1.  Add new scales/modes to `SCALES` in `src/music_theory.py`.
2.  Implement new rhythmic styles in `MelodyGenerator.generate_rhythm_pattern`.
3.  Add new instrument tracks (e.g., Bassline) by creating a new class in `src/accompaniment.py` and updating `src/main.py`/`src/server.py` to write the track.
