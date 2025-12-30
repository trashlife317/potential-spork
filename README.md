# MIDI Beat Starter & MCP Server

An advanced MIDI composition tool designed for **Hip-Hop, Rap, and Trap** production. It uses music theory algorithms to generate melodies, chord progressions, and drum patterns, exporting them as standard MIDI files compatible with any DAW (FL Studio, Ableton, Logic Pro, etc.).

It functionality acts as a **CLI Tool** for producers and an **MCP Server** for AI Agents (like Claude).

## Features

*   **Smart Melody Generation**: Uses voice leading, motif development, and scale theory (Phrygian, Harmonic Minor, etc.).
*   **Full Accompaniment**: Generates matching **Chord Progressions** and **Trap Drum Patterns**.
*   **3 Variations**:
    *   *Variation A*: Smooth/Melodic (great for bells/plucks).
    *   *Variation B*: Aggressive/Trap (great for leads/808s).
    *   *Variation C*: Motivic/Thematic (great for keys).
*   **MCP Support**: Exposes a `generate_beat` tool for AI assistants.

## Installation

1.  Clone the repository.
2.  Install dependencies (for MCP server):
    ```bash
    pip install mcp
    ```

## Usage (CLI)

Generate a beat directly from your terminal:

```bash
# Basic Melody
python src/main.py --key C --scale minor --tempo 140

# Full Beat Starter (Melody + Chords + Drums) to file
python src/main.py --key F# --scale phrygian --tempo 142 --chords --drums --output fire_beat
```

This will create files like `fire_beat_var_B.mid`.

## How to use with FL Studio

1.  **Generate the MIDI**: Run the command above to create your `.mid` file.
2.  **Import**: Open FL Studio. Go to `File > Import > MIDI File...` and select your generated file (e.g., `fire_beat_var_B.mid`).
3.  **Channel Selection**:
    *   FL Studio will ask "Which channels to import?". Ensure all tracks are selected.
    *   **Accept** the import.
4.  **Assign Sounds**:
    *   You will see separate channels in the Channel Rack (e.g., "Melody", "Chords", "Drums").
    *   **Melody**: Replace the default "Sampler" with a VST like **Sytrus**, **FLEX**, or **Omnisphere**. Pick a Pluck or Lead preset.
    *   **Chords**: Assign a Pad or Key sound (e.g., **FL Keys**).
    *   **Drums**: This track contains kick, snare, and hi-hats on one channel.
        *   *Option A*: Assign a Drum Kit VST (e.g., **FPC**).
        *   *Option B*: Right-click the pattern and "Split by Channel" to separate the kick, snare, and hi-hats, then drag your own drum samples onto them.
5.  **Gross Beat**: Add **Gross Beat** to the Melody mixer track and select the "Momentary > Half Speed" preset for instant Trap vibes.

## MCP Server (For AI Agents)

To run this as an MCP server for Claude Desktop or other clients:

```bash
python src/server.py
```

Or configure your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "beat-composer": {
      "command": "python3",
      "args": ["/path/to/repo/src/server.py"]
    }
  }
}
```

Now you can ask Claude: *"Generate a dark trap beat in D minor with chords and drums."*
