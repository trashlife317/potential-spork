import argparse
import sys
from src.generator import MelodyGenerator

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
    parser.add_argument('--interactive', action='store_true', help="Run in interactive mode")

    args = parser.parse_args()

    key = args.key
    scale = args.scale
    tempo = args.tempo
    bars = args.bars

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

    print(f"\nGenerating Melody for: Key={key} {scale}, Tempo={tempo} BPM, Length={bars} Bars")

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

    print("\n=== Implementation Guidance ===")
    print("1. **DAW Import**: Manually enter the notes above into your Piano Roll, or write a script to convert the data to a .mid file.")
    print("2. **Sound Selection**: ")
    print("   - For Variation A: Use a Pluck or Bell sound with some reverb.")
    print("   - For Variation B: Use a fast Synth Lead or aggressive 808-style bass synth.")
    print("   - For Variation C: Good for Keys or Pads.")
    print("3. **Processing**: Add Half-time effect (Gross Beat) for Trap feel. Add Delay (1/4 or 1/8 dot) to fill space.")

if __name__ == "__main__":
    main()
