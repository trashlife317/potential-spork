import argparse
import sys
import os

from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

from src.generator import MelodyGenerator
from src.midi_utils import MidiWriter
from src.accompaniment import ChordGenerator, DrumGenerator

console = Console()

def print_melody_table(melody, title="Melody Data"):
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Note", justify="right", style="cyan")
    table.add_column("Name", justify="center", style="green")
    table.add_column("Duration", justify="right")
    table.add_column("Velocity", justify="right", style="yellow")
    table.add_column("Offset", justify="right", style="blue")

    for note in melody:
        table.add_row(
            str(note['note']),
            note['name'],
            f"{note['duration']:.2f}",
            str(note['velocity']),
            f"{note['offset']:.2f}"
        )
    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Hip-Hop/Trap MIDI Melody Generator")
    parser.add_argument('--key', type=str, default='C', help="Key (e.g., C, F#)")
    parser.add_argument('--scale', type=str, default='minor', help="Scale type (minor, harmonic_minor, phrygian, pentatonic_minor)")
    parser.add_argument('--tempo', type=int, default=140, help="Tempo in BPM")
    parser.add_argument('--bars', type=int, default=4, help="Length in bars")
    parser.add_argument('--output', type=str, default=None, help="Base filename for MIDI export (e.g., 'melody')")
    parser.add_argument('--chords', action='store_true', help="Include chord progression in output")
    parser.add_argument('--drums', action='store_true', help="Include drum pattern in output")
    parser.add_argument('--interactive', action='store_true', help="Run in interactive mode")
    parser.add_argument('--seed', type=int, default=None, help="Random seed for reproducible generation")

    args = parser.parse_args()

    key = args.key
    scale = args.scale
    tempo = args.tempo
    bars = args.bars
    output_base = args.output
    add_chords = args.chords
    add_drums = args.drums
    seed = args.seed

    if args.interactive:
        console.print("[bold cyan]=== MIDI Melody Composer Assistant ===[/bold cyan]")
        key = input("Key (default C): ") or "C"
        scale = input("Scale (minor, harmonic_minor, phrygian, pentatonic_minor) [default minor]: ") or "minor"
        try:
            tempo = int(input("Tempo BPM (default 140): ") or "140")
            bars = int(input("Length in bars (default 4): ") or "4")
        except ValueError:
            console.print("[bold red]Invalid number input, using defaults.[/bold red]")
            tempo = 140
            bars = 4

        c = input("Add Chords? (y/n): ")
        if c.lower() == 'y': add_chords = True
        d = input("Add Drums? (y/n): ")
        if d.lower() == 'y': add_drums = True

        s = input("Random Seed (optional): ")
        if s:
            try:
                seed = int(s)
            except ValueError:
                pass

    console.print(f"\n[bold green]Generating Beat Starter for:[/bold green] Key={key} {scale}, Tempo={tempo} BPM, Length={bars} Bars")
    if seed is not None:
        console.print(f"[dim]Using random seed: {seed}[/dim]")

    try:
        generator = MelodyGenerator(key, scale, tempo, length_bars=bars, seed=seed)
    except Exception as e:
        console.print(f"[bold red]Error initializing generator:[/bold red] {e}")
        return

    variations = ['A', 'B', 'C']

    for var in variations:
        console.print(f"\n[bold underline]=== Variation {var} ===[/bold underline]")
        explanation = generator.get_theory_explanation(var)
        console.print(Markdown(explanation))

        melody = generator.generate_variation(var)
        print_melody_table(melody, title=f"MIDI Output - Variation {var}")

        if output_base:
            # Sanitize output base to prevent path traversal
            safe_output = os.path.basename(output_base)
            if output_base != safe_output:
                console.print(f"[bold yellow]Warning:[/bold yellow] Path components removed from output filename. Using '{safe_output}'.")
                output_base = safe_output

            filename = f"{output_base}_var_{var}.mid"
            try:
                writer = MidiWriter()
                # 1. Melody Track (Channel 0)
                writer.add_track(melody, track_name=f"Melody Var {var}", channel=0)

                # 2. Chords Track (Channel 1)
                if add_chords:
                    chord_gen = ChordGenerator(key, scale, seed=seed)
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
                    console.print("   [green]+ Added Chords Track[/green]")

                # 3. Drums Track (Channel 9)
                if add_drums:
                    drum_gen = DrumGenerator(tempo, seed=seed)
                    drum_events = drum_gen.generate_pattern(bars)
                    writer.add_track(drum_events, track_name="Drums", channel=9)
                    console.print("   [green]+ Added Drums Track[/green]")

                writer.write_file(filename)
                console.print(f"[bold blue]-> Saved Multi-track MIDI file:[/bold blue] {filename}")
            except Exception as e:
                console.print(f"[bold red]Error saving MIDI:[/bold red] {e}")

    console.print("\n[bold]=== Implementation Guidance ===[/bold]")
    if output_base:
        console.print("1. [bold]DAW Import[/bold]: Drag and drop the generated .mid files into your DAW.")
    else:
        console.print("1. [bold]DAW Import[/bold]: Manually enter the notes above into your Piano Roll, or use --output to generate MIDI files.")
    console.print("2. [bold]Sound Selection[/bold]: ")
    console.print("   - For Variation A: Use a Pluck or Bell sound with some reverb.")
    console.print("   - For Variation B: Use a fast Synth Lead or aggressive 808-style bass synth.")
    console.print("   - For Variation C: Good for Keys or Pads.")
    console.print("3. [bold]Processing[/bold]: Add Half-time effect (Gross Beat) for Trap feel. Add Delay (1/4 or 1/8 dot) to fill space.")

if __name__ == "__main__":
    main()
