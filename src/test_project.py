import unittest
from src.music_theory import get_scale_notes, get_note_name, analyze_interval
from src.generator import MelodyGenerator

class TestMusicTheory(unittest.TestCase):
    def test_scale_generation(self):
        # C Major
        c_major = get_scale_notes('C', 'major', 3, 3)
        # C3 is 48.
        # Major: 0, 2, 4, 5, 7, 9, 11
        # 48, 50, 52, 53, 55, 57, 59
        expected = [48, 50, 52, 53, 55, 57, 59]
        self.assertEqual(c_major, expected)

    def test_note_name(self):
        self.assertEqual(get_note_name(60), 'C4')
        self.assertEqual(get_note_name(61), 'C#4')

class TestGenerator(unittest.TestCase):
    def test_initialization(self):
        gen = MelodyGenerator('C', 'minor', 140)
        self.assertEqual(gen.key, 'C')
        self.assertEqual(gen.scale_type, 'minor')

    def test_melody_structure(self):
        gen = MelodyGenerator('C', 'minor', 140, length_bars=1)
        melody = gen.generate_variation('A')
        self.assertTrue(len(melody) > 0)
        for note in melody:
            self.assertIn('note', note)
            self.assertIn('duration', note)
            self.assertIn('velocity', note)
            self.assertTrue(0 <= note['note'] <= 127)

if __name__ == '__main__':
    unittest.main()
