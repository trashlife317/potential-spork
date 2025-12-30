import unittest
from unittest.mock import patch
import sys
import io
import os
import glob
from src.main import main

class TestInteractiveMode(unittest.TestCase):
    def tearDown(self):
        # Clean up any generated MIDI files
        for f in glob.glob("dummy_interactive_*.mid"):
            try:
                os.remove(f)
            except OSError:
                pass

    def test_interactive_flow(self):
        # Mock sys.argv to simulate interactive flag AND output to trigger track printing
        test_argv = ['src/main.py', '--interactive', '--output', 'dummy_interactive']

        # Mock inputs:
        # Key: C
        # Scale: minor
        # Tempo: 130
        # Bars: 4
        # Chords: y
        # Drums: y
        # Style: boombap
        inputs = ['C', 'minor', '130', '4', 'y', 'y', 'boombap']

        with patch('sys.argv', test_argv):
            with patch('builtins.input', side_effect=inputs):
                # Capture stdout to avoid clutter
                captured_output = io.StringIO()
                with patch('sys.stdout', new=captured_output):
                    main()

                output = captured_output.getvalue()

                # Verify key outputs
                self.assertIn("Generating Beat Starter for: Key=C minor, Tempo=130 BPM", output)
                self.assertIn("Style=boombap", output)
                self.assertIn("Added Chords Track", output)
                self.assertIn("Added Drums Track (boombap)", output)

    def test_interactive_defaults(self):
        # Test defaults when user hits enter
        test_argv = ['src/main.py', '--interactive']

        # Inputs:
        # Key: Enter (default C)
        # Scale: Enter (default minor)
        # Tempo: Enter (default 140)
        # Bars: Enter (default 4)
        # Chords: n
        # Drums: n
        inputs = ['', '', '', '', 'n', 'n']

        with patch('sys.argv', test_argv):
            with patch('builtins.input', side_effect=inputs):
                captured_output = io.StringIO()
                with patch('sys.stdout', new=captured_output):
                    main()

                output = captured_output.getvalue()
                self.assertIn("Generating Beat Starter for: Key=C minor, Tempo=140 BPM", output)

if __name__ == '__main__':
    unittest.main()
