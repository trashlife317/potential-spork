import unittest
import os
from src.midi_utils import MidiWriter
from src.accompaniment import ChordGenerator, DrumGenerator

class TestAccompaniment(unittest.TestCase):
    def test_chord_generation(self):
        # Test C Minor progression
        gen = ChordGenerator('C', 'minor')
        progression = gen.generate_progression(length_bars=4)
        self.assertEqual(len(progression), 4)
        for chord_notes in progression:
            # Check for at least triad (3 notes)
            self.assertTrue(len(chord_notes) >= 3)
            # Check range (roughly around octave 3-5)
            for note in chord_notes:
                self.assertTrue(40 <= note <= 80)

    def test_drum_generation(self):
        # Default Trap
        gen = DrumGenerator(140)
        pattern = gen.generate_pattern(length_bars=1)
        self.assertTrue(len(pattern) > 0)
        notes = [e['note'] for e in pattern]
        self.assertIn(38, notes) # Snare

    def test_drum_styles(self):
        # Boom Bap
        gen_bb = DrumGenerator(90, style='boombap')
        pattern_bb = gen_bb.generate_pattern(length_bars=1)
        self.assertTrue(len(pattern_bb) > 0)
        notes_bb = [e['note'] for e in pattern_bb]
        self.assertIn(36, notes_bb) # Kick
        self.assertIn(38, notes_bb) # Snare

        # Lo-fi
        gen_lofi = DrumGenerator(80, style='lofi')
        pattern_lofi = gen_lofi.generate_pattern(length_bars=1)
        self.assertTrue(len(pattern_lofi) > 0)
        # Lo-fi might use rimshot (37) or snare (38)
        notes_lofi = [e['note'] for e in pattern_lofi]
        self.assertTrue(38 in notes_lofi or 37 in notes_lofi)

class TestMultitrackMidi(unittest.TestCase):
    def test_write_multitrack(self):
        writer = MidiWriter()

        # Melody
        melody = [{'note': 60, 'duration': 1.0, 'velocity': 100, 'offset': 0.0}]
        writer.add_track(melody, channel=0)

        # Drums
        drums = [{'note': 36, 'duration': 1.0, 'velocity': 100, 'offset': 0.0}]
        writer.add_track(drums, channel=9)

        filename = 'test_multi_unit.mid'
        writer.write_file(filename)

        self.assertTrue(os.path.exists(filename))
        # Should be larger than single track file
        self.assertGreater(os.path.getsize(filename), 50)
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
