from mcp.server.fastmcp import FastMCP
import io
import base64
import os
import sys

# Allow imports from project root when running directly
sys.path.append(os.getcwd())

from src.generator import MelodyGenerator
from src.midi_utils import MidiWriter
from src.accompaniment import ChordGenerator, DrumGenerator

# Initialize MCP Server
mcp = FastMCP("Beat Starter Composer")

@mcp.tool()
def generate_beat(key: str = "C", scale: str = "minor", tempo: int = 140, bars: int = 4, variation: str = "B", add_chords: bool = True, add_drums: bool = True, drum_style: str = "trap") -> str:
    """
    Generates a MIDI beat starter with optional chords and drums.
    Returns a base64 encoded MIDI string.

    Args:
        key: The musical key (e.g., "C", "F#").
        scale: The scale type (minor, harmonic_minor, phrygian, pentatonic_minor).
        tempo: BPM of the track (e.g., 140 for Trap).
        bars: Length in bars (usually 4 or 8).
        variation: Melody style ('A' for Smooth, 'B' for Trap, 'C' for Motivic).
        add_chords: Whether to include a backing chord progression.
        add_drums: Whether to include a drum pattern.
        drum_style: Style of drums ('trap', 'boombap', 'lofi').
    """

    # 1. Generate Melody
    generator = MelodyGenerator(key, scale, tempo, length_bars=bars)
    melody = generator.generate_variation(variation)

    writer = MidiWriter()

    # Track 1: Melody (Channel 0)
    writer.add_track(melody, track_name=f"Melody Var {variation}", channel=0)

    # Track 2: Chords (Channel 1)
    if add_chords:
        chord_gen = ChordGenerator(key, scale)
        progression_notes = chord_gen.generate_progression(bars)
        chord_events = []
        for bar_idx, notes in enumerate(progression_notes):
            for n in notes:
                chord_events.append({
                    'note': n,
                    'duration': 4.0, # Whole note chords
                    'velocity': 80,
                    'offset': bar_idx * 4.0
                })
        writer.add_track(chord_events, track_name="Chords", channel=1)

    # Track 3: Drums (Channel 9)
    if add_drums:
        drum_gen = DrumGenerator(tempo, style=drum_style)
        drum_events = drum_gen.generate_pattern(bars)
        writer.add_track(drum_events, track_name=f"Drums ({drum_style})", channel=9)

    # Write to Memory Buffer
    buffer = io.BytesIO()
    writer.write_to_stream(buffer)
    midi_bytes = buffer.getvalue()

    # Encode to Base64
    b64_string = base64.b64encode(midi_bytes).decode('utf-8')

    return b64_string

if __name__ == "__main__":
    mcp.run()
