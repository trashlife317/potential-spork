import unittest
import os
from src.music_theory import get_scale_notes, is_stable_scale_degree
from src.generator import MelodyGenerator
from src.midi_utils import MidiWriter

class TestMusicTheory(unittest.TestCase):
    def test_scale_generation(self):
        # C Major
        c_major = get_scale_notes('C', 'major', 3, 3)
        # C3 is 48.
        # Major: 0, 2, 4, 5, 7, 9, 11
        # 48, 50, 52, 53, 55, 57, 59
        expected = [48, 50, 52, 53, 55, 57, 59]
        self.assertEqual(c_major, expected)

    def test_stability_check(self):
        # C Major: C(0), E(4), G(7) are stable
        self.assertTrue(is_stable_scale_degree(60, 'C', 'major')) # C4
        self.assertTrue(is_stable_scale_degree(64, 'C', 'major')) # E4
        self.assertTrue(is_stable_scale_degree(67, 'C', 'major')) # G4
        self.assertFalse(is_stable_scale_degree(62, 'C', 'major')) # D4

class TestGenerator(unittest.TestCase):
    def test_initialization(self):
        gen = MelodyGenerator('C', 'minor', 140)
        self.assertEqual(gen.key, 'C')
        self.assertEqual(gen.scale_type, 'minor')

    def test_melody_structure(self):
        gen = MelodyGenerator('C', 'minor', 140, length_bars=4)
        melody = gen.generate_variation('A')
        self.assertTrue(len(melody) > 0)

        total_duration = sum(n['duration'] for n in melody)
        # Should be roughly 16 beats for 4 bars of 4/4
        self.assertAlmostEqual(total_duration, 16.0, delta=0.1)

class TestMidiWriter(unittest.TestCase):
    def test_write_file(self):
        writer = MidiWriter()
        notes = [{'note': 60, 'duration': 1.0, 'velocity': 100, 'offset': 0.0}]
        writer.add_track(notes)
        filename = 'test_unit_output.mid'
        writer.write_file(filename)
        self.assertTrue(os.path.exists(filename))
        self.assertGreater(os.path.getsize(filename), 0)
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
