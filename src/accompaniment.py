import random
from src.music_theory import get_scale_notes, get_note_index

class ChordGenerator:
    def __init__(self, key, scale_type):
        self.key = key
        self.scale_type = scale_type
        self.scale_notes = get_scale_notes(key, scale_type, start_octave=3, end_octave=4)
        # Pre-calculate full scale for chord generation (octaves 3-5) to optimize loop performance
        self.full_scale_notes = get_scale_notes(key, scale_type, start_octave=3, end_octave=5)

        # We need a way to build chords from scale degrees
        # Simple mapping of scale degree (0-6) to MIDI note index
        # This is tricky because self.scale_notes spans octaves.
        # Let's get one octave of scale notes for degree mapping.
        self.single_octave = get_scale_notes(key, scale_type, start_octave=3, end_octave=3)

    def get_chord_notes(self, degree, octave_offset=0):
        """Returns MIDI notes for a triad on the given scale degree (1-based)."""
        # Degree 1 = index 0
        root_idx = (degree - 1) % len(self.single_octave)
        third_idx = (degree + 1) % len(self.single_octave) # +2 in diatonic
        fifth_idx = (degree + 3) % len(self.single_octave) # +4 in diatonic

        # We need to map these back to MIDI.
        # If the index wrapped around, it means we went up an octave?
        # Ideally we just pick from the large scale list.

        # Better approach:
        # Use pre-calculated full scale
        full_scale = self.full_scale_notes
        # Find the root note in the full scale (first occurrence)
        start_pos = 0
        # If degree is 1, start_pos is 0. If degree is 2, start_pos is 1.
        root_pos = (degree - 1)

        chord_indices = [root_pos, root_pos + 2, root_pos + 4]
        midi_notes = []
        for idx in chord_indices:
            if idx < len(full_scale):
                midi_notes.append(full_scale[idx] + (octave_offset * 12))

        return midi_notes

    def generate_progression(self, length_bars=4):
        """Generates a list of chords (list of notes) for each bar."""
        # Common Minor/Trap Progressions (Degrees)
        progressions = [
            [1, 6, 7, 1], # i - VI - VII - i (Aeolian)
            [1, 4, 5, 1], # i - iv - v - i
            [1, 6, 3, 7], # i - VI - III - VII (Pop/Emotional)
            [1, 2, 1, 5], # i - ii - i - v (Phrygian-ish if ii is flattened)
        ]

        prog = random.choice(progressions)

        # Extend or truncate to length_bars
        result = []
        for i in range(length_bars):
            degree = prog[i % len(prog)]
            notes = self.get_chord_notes(degree)
            result.append(notes)

        return result

class DrumGenerator:
    def __init__(self, tempo):
        self.tempo = tempo

    def generate_pattern(self, length_bars=4):
        """
        Generates drum events.
        Returns list of {'note': int, 'duration': float, 'velocity': int, 'offset': float}
        Using General MIDI:
        36 = Kick (C1)
        38 = Snare (D1) or 42 (Closed Hi-hat) -> Wait, Snare is 38 or 40. Clap is 39.
        42 = Closed Hi-hat
        """
        events = []

        for bar in range(length_bars):
            bar_offset = bar * 4.0 # 4 beats per bar

            # 1. Hi-Hats (8th notes)
            for i in range(8):
                # i * 0.5
                beat = i * 0.5
                # Random Rolls (32nd notes)
                if random.random() < 0.15: # 15% chance of roll
                    for r in range(4):
                        events.append({
                            'note': 42,
                            'duration': 0.125,
                            'velocity': random.randint(70, 90),
                            'offset': bar_offset + beat + (r * 0.125)
                        })
                else:
                    events.append({
                        'note': 42,
                        'duration': 0.5,
                        'velocity': random.randint(80, 100),
                        'offset': bar_offset + beat
                    })

            # 2. Snare / Clap (Beat 3)
            # In Trap (140bpm), snare is on beat 3 of the 4/4 bar
            events.append({
                'note': 38, # Snare
                'duration': 1.0,
                'velocity': 127,
                'offset': bar_offset + 2.0
            })

            # 3. Kick (Beat 1 + Syncopation)
            kick_beats = [0.0]
            # Add random kicks
            possible_spots = [1.5, 2.5, 3.0, 3.5]
            for spot in possible_spots:
                if random.random() < 0.4:
                    kick_beats.append(spot)

            for kb in kick_beats:
                 events.append({
                    'note': 36,
                    'duration': 0.5,
                    'velocity': 120,
                    'offset': bar_offset + kb
                })

        return events
