import unittest
from src.music_theory import get_note_index

class TestMusicTheoryExtended(unittest.TestCase):
    def test_get_note_index_standard(self):
        # Test standard notes
        self.assertEqual(get_note_index('C'), 0)
        self.assertEqual(get_note_index('C#'), 1)
        self.assertEqual(get_note_index('B'), 11)

    def test_get_note_index_case_insensitive(self):
        # Test lowercase
        self.assertEqual(get_note_index('c'), 0)
        self.assertEqual(get_note_index('c#'), 1)
        self.assertEqual(get_note_index('db'), 1)

        # Test mixed case
        self.assertEqual(get_note_index('Db'), 1)
        self.assertEqual(get_note_index('DB'), 1)
        self.assertEqual(get_note_index('eb'), 3)
        self.assertEqual(get_note_index('Eb'), 3)

    def test_get_note_index_flats(self):
        # Test flat to sharp conversion logic
        self.assertEqual(get_note_index('Db'), 1) # C#
        self.assertEqual(get_note_index('Eb'), 3) # D#
        self.assertEqual(get_note_index('Gb'), 6) # F#
        self.assertEqual(get_note_index('Ab'), 8) # G#
        self.assertEqual(get_note_index('Bb'), 10) # A#

    def test_get_note_index_invalid(self):
        with self.assertRaises(ValueError):
            get_note_index('H')
        with self.assertRaises(ValueError):
            get_note_index('C##')
        with self.assertRaises(ValueError):
            get_note_index('')

if __name__ == '__main__':
    unittest.main()
