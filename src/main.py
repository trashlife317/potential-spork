import argparse
import sys
import os

from src.generator import MelodyGenerator
from src.midi_utils import MidiWriter
from src.accompaniment import ChordGenerator, DrumGenerator

def print_melody_table(melody):
    print(f"{'Note':<6} | {'Name':<6} | {'Duration (Beats)':<16} | {'Velocity':<8} | {'Offset':<8}")
    print("-" * 60)
    for note in melody:
        print(f"{note['note']:<6} | {note['name']:<6} | {note['duration']:<16.2f} | {note['velocity']:<8} | {note['offset']:<8.2f}")
    print("-" * 60)

def main():
    parser = argparse.ArgumentParser(description="Hip-Hop/Trap MIDI Melody Generator")
    parser.add_argument('--key', type=str, default='C', help="Key (e.g., C, F#)")
    parser.add_argument('--scale', type=str, default='minor', help="Scale type (minor, harmonic_minor, phrygian, pentatonic_minor)")
    parser.add_argument('--tempo', type=int, default=140, help="Tempo in BPM")
    parser.add_argument('--bars', type=int, default=4, help="Length in bars")
    parser.add_argument('--output', type=str, default=None, help="Base filename for MIDI export (e.g., 'melody')")
    parser.add_argument('--chords', action='store_true', help="Include chord progression in output")
    parser.add_argument('--drums', action='store_true', help="Include drum pattern in output")
    parser.add_argument('--style', type=str, default='trap', help="Drum style (trap, boombap, lofi)")
    parser.add_argument('--interactive', action='store_true', help="Run in interactive mode")

    args = parser.parse_args()

    key = args.key
    scale = args.scale
    tempo = args.tempo
    bars = args.bars
    output_base = args.output
    add_chords = args.chords
    add_drums = args.drums
    drum_style = args.style

    if args.interactive:
        print("=== MIDI Melody Composer Assistant ===")
        key = input("Key (default C): ") or "C"
        scale = input("Scale (minor, harmonic_minor, phrygian, pentatonic_minor) [default minor]: ") or "minor"
        try:
            tempo = int(input("Tempo BPM (default 140): ") or "140")
            bars = int(input("Length in bars (default 4): ") or "4")
        except ValueError:
            print("Invalid number input, using defaults.")
            tempo = 140
            bars = 4

        c = input("Add Chords? (y/n): ")
        if c.lower() == 'y': add_chords = True
        d = input("Add Drums? (y/n): ")
        if d.lower() == 'y': add_drums = True

        if add_drums:
            s = input("Drum Style (trap, boombap, lofi) [default trap]: ") or "trap"
            drum_style = s

    print(f"\nGenerating Beat Starter for: Key={key} {scale}, Tempo={tempo} BPM, Length={bars} Bars, Style={drum_style}")

    try:
        generator = MelodyGenerator(key, scale, tempo, length_bars=bars)
    except Exception as e:
        print(f"Error initializing generator: {e}")
        return

    variations = ['A', 'B', 'C']

    for var in variations:
        print(f"\n=== Variation {var} ===")
        explanation = generator.get_theory_explanation(var)
        print(explanation)
        print("\nMIDI Output:")
        melody = generator.generate_variation(var)
        print_melody_table(melody)

        if output_base:
            filename = f"{output_base}_var_{var}.mid"
            try:
                writer = MidiWriter()
                # 1. Melody Track (Channel 0)
                writer.add_track(melody, track_name=f"Melody Var {var}", channel=0)

                # 2. Chords Track (Channel 1)
                if add_chords:
                    chord_gen = ChordGenerator(key, scale)
                    progression_notes = chord_gen.generate_progression(bars)
                    # Convert to event list
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
                    print("   + Added Chords Track")

                # 3. Drums Track (Channel 9)
                if add_drums:
                    drum_gen = DrumGenerator(tempo, style=drum_style)
                    drum_events = drum_gen.generate_pattern(bars)
                    writer.add_track(drum_events, track_name=f"Drums ({drum_style})", channel=9)
                    print(f"   + Added Drums Track ({drum_style})")

                writer.write_file(filename)
                print(f"-> Saved Multi-track MIDI file: {filename}")
            except Exception as e:
                print(f"Error saving MIDI: {e}")

    print("\n=== Implementation Guidance ===")
    if output_base:
        print("1. **DAW Import**: Drag and drop the generated .mid files into your DAW.")
    else:
        print("1. **DAW Import**: Manually enter the notes above into your Piano Roll, or use --output to generate MIDI files.")
    print("2. **Sound Selection**: ")
    print("   - For Variation A: Use a Pluck or Bell sound with some reverb.")
    print("   - For Variation B: Use a fast Synth Lead or aggressive 808-style bass synth.")
    print("   - For Variation C: Good for Keys or Pads.")
    print("3. **Processing**: Add Half-time effect (Gross Beat) for Trap feel. Add Delay (1/4 or 1/8 dot) to fill space.")

if __name__ == "__main__":
    main()
