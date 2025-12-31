import random
from src.music_theory import get_scale_notes, get_note_name, analyze_interval, is_stable_scale_degree

class MelodyGenerator:
    def __init__(self, key, scale_type, tempo, length_bars=4, time_signature='4/4', range_octaves=(3, 5)):
        self.key = key
        self.scale_type = scale_type
        self.tempo = tempo
        self.length_bars = length_bars
        self.time_signature = time_signature
        self.range_octaves = range_octaves

        # Get valid notes for the scale
        self.scale_notes = get_scale_notes(key, scale_type, range_octaves[0], range_octaves[1])
        # Identify stable notes within the scale_notes (Tonic, 3rd, 5th)
        self.stable_notes = [n for n in self.scale_notes if is_stable_scale_degree(n, key, scale_type)]

        # Parsing time signature
        try:
            num, den = map(int, time_signature.split('/'))
        except:
            num, den = 4, 4
        self.beats_per_bar = num
        self.beat_unit = den # usually 4
        self.total_beats = self.length_bars * self.beats_per_bar

    def generate_motif(self, length_in_notes=4):
        """Generates a short seed motif."""
        motif = []
        # Start on a stable note (Tonic, 3rd, or 5th) roughly in the middle
        start_index = len(self.scale_notes) // 2
        current_index = start_index

        for _ in range(length_in_notes):
            # Prefer small steps
            step = random.choices([-2, -1, 0, 1, 2, 3, -3], weights=[1, 4, 2, 4, 1, 0.5, 0.5])[0]
            current_index = max(0, min(len(self.scale_notes) - 1, current_index + step))
            motif.append(self.scale_notes[current_index])

        return motif

    def generate_rhythm_pattern(self, num_beats, density='medium', style='trap'):
        """
        Generates a rhythm pattern (list of durations in beats).
        E.g., [0.5, 0.5, 1.0, ...]
        """
        pattern = []
        beats_filled = 0.0

        # Basic durations
        durations = [0.25, 0.5, 0.75, 1.0] # 16th, 8th, dotted 8th, quarter
        weights = [10, 40, 10, 40]

        if style == 'trap':
            # Add triplet feel
            # 1/3 beat (triplet 8th) = 0.333... hard to represent in float beats nicely without grid
            # Let's stick to 16th grid for simplicity but emphasize syncopation
            durations = [0.25, 0.5, 1.0, 1.5]
            weights = [30, 30, 30, 10]

        while beats_filled < num_beats:
            dur = random.choices(durations, weights=weights)[0]
            # check if it fits
            if beats_filled + dur > num_beats:
                dur = num_beats - beats_filled

            # Avoid tiny remainders
            if dur < 0.25:
                dur = num_beats - beats_filled # take the rest

            pattern.append(dur)
            beats_filled += dur

        return pattern

    def generate_phrase_structure(self, total_bars):
        """Generates a list of rhythm patterns for full length based on structure."""
        bar_rhythm_A = self.generate_rhythm_pattern(self.beats_per_bar, style='trap')
        bar_rhythm_B = self.generate_rhythm_pattern(self.beats_per_bar, style='trap')

        full_rhythm = []
        # Common structure: A A B A or A B A C
        structure_type = random.choice(['AABA', 'ABAB'])

        for char in structure_type:
            if char == 'A':
                full_rhythm.extend(bar_rhythm_A)
            elif char == 'B':
                full_rhythm.extend(bar_rhythm_B)
            else:
                 full_rhythm.extend(self.generate_rhythm_pattern(self.beats_per_bar, style='trap'))

        # Adjust for total bars if not 4
        if total_bars != 4:
            # Fallback simple repeat
            full_rhythm = []
            for _ in range(total_bars):
                full_rhythm.extend(bar_rhythm_A)

        return full_rhythm

    def apply_voice_leading(self, current_note, target_note=None, variation='A'):
        """
        Selects the next note based on voice leading rules.
        """
        # Find index of current note
        try:
            curr_idx = self.scale_notes.index(current_note)
        except ValueError:
            curr_idx = len(self.scale_notes) // 2

        if variation == 'A': # Smooth
            # Stepwise motion preferred
            steps = [-1, 1, 0]
            weights = [4, 4, 1]
        elif variation == 'B': # Aggressive/Trap
            # More leaps, repeated notes
            steps = [-2, 2, 0, -3, 3, 7, -7] # 7 is a fifth in diatonic scale roughly
            weights = [2, 2, 3, 1, 1, 0.5, 0.5]
        else: # C - Balanced/Motivic
            steps = [-1, 1, -2, 2, 0]
            weights = [3, 3, 1, 1, 1]

        step = random.choices(steps, weights=weights)[0]
        next_idx = max(0, min(len(self.scale_notes) - 1, curr_idx + step))
        return self.scale_notes[next_idx]

    def generate_variation(self, variation_type='A'):
        """
        Generates a full melody based on the variation type.
        Returns a list of dicts: {'note': midi, 'name': str, 'duration': float, 'velocity': int, 'offset': float}
        """
        melody = []

        # 1. Determine Rhythm
        # Use structured phrasing for better musicality
        full_rhythm = self.generate_phrase_structure(self.length_bars)

        # 2. Generate Notes
        current_note = self.scale_notes[len(self.scale_notes) // 2] # Start mid-range

        # Motivic Development for Variation C
        motif = []
        if variation_type == 'C':
            motif = self.generate_motif(4)
            motif_idx = 0

        time_cursor = 0.0
        total_duration = sum(full_rhythm)
        current_beat = 0.0

        for i, dur in enumerate(full_rhythm):
            velocity = random.randint(80, 110)

            # End of phrase resolution detection
            is_end_of_phrase = (i == len(full_rhythm) - 1) or (current_beat + dur) % (self.beats_per_bar * 4) == 0

            # Note Selection
            if variation_type == 'C' and motif:
                # Use motif note, cycling
                note = motif[motif_idx % len(motif)]
                motif_idx += 1

                # Transpose motif every 2 bars?
                if int(current_beat / (self.beats_per_bar * 2)) % 2 == 1:
                     # Simple diatonic transposition (shift index in scale)
                     try:
                         orig_idx = self.scale_notes.index(note)
                         new_idx = min(len(self.scale_notes)-1, orig_idx + 2) # Shift up a third
                         note = self.scale_notes[new_idx]
                     except:
                         pass

            else:
                note = self.apply_voice_leading(current_note, variation=variation_type)

            # Enforce Resolution at end of phrase
            if is_end_of_phrase:
                # Try to find nearest stable tone
                closest_stable = note
                min_dist = 100
                for sn in self.stable_notes:
                     dist = abs(sn - note)
                     if dist < min_dist:
                         min_dist = dist
                         closest_stable = sn
                note = closest_stable

            # Rest logic (Trap leaves space)
            is_rest = False
            if variation_type == 'B' and random.random() < 0.2 and not is_end_of_phrase:
                 is_rest = True

            if not is_rest:
                # Humanize
                if variation_type == 'B': # Trap - rigid timing or triplets, high velocity variation
                     velocity = random.choice([100, 110, 120, 60]) # Accent patterns

                melody.append({
                    'note': note,
                    'name': get_note_name(note),
                    'duration': dur,
                    'velocity': velocity,
                    'offset': time_cursor
                })
                current_note = note

            time_cursor += dur
            current_beat += dur

        return melody

    def get_theory_explanation(self, variation_type):
        if variation_type == 'A':
            return ("**Variation A (Melodic/Smooth):** Focuses on stepwise motion and smooth voice leading. "
                    "This creates a lyrical, singable quality suitable for hooks or emotional sections. "
                    "Consonant intervals (3rds, 6ths) are prioritized.")
        elif variation_type == 'B':
            return ("**Variation B (Trap/Aggressive):** Incorporates rhythmic syncopation, silence (rests), and wider intervallic leaps. "
                    "Uses characteristic Trap articulations and velocity accents to create a percussive feel. "
                    "Emphasizes tension through repetition and dissonance.")
        elif variation_type == 'C':
            return ("**Variation C (Motivic/Thematic):** Establishes a short melodic motif and develops it through sequence and repetition. "
                    "This balances predictability (catchiness) with variation, a hallmark of professional composition.")
        return ""
