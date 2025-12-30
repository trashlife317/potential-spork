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
        gen = DrumGenerator(140)
        pattern = gen.generate_pattern(length_bars=1)
        self.assertTrue(len(pattern) > 0)

        # Check for mandatory elements (Kick or Snare)
        notes = [e['note'] for e in pattern]
        self.assertIn(38, notes) # Snare
        self.assertIn(42, notes) # Hi-hat

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
