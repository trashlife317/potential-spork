import unittest
import base64
import io
import os
from src.server import generate_beat

class TestMCPServer(unittest.TestCase):
    def test_generate_beat_tool(self):
        # Simulate calling the tool
        b64_output = generate_beat(
            key="C",
            scale="phrygian",
            tempo=140,
            bars=4,
            variation="B",
            add_chords=True,
            add_drums=True
        )

        # Verify it returns a string
        self.assertIsInstance(b64_output, str)
        self.assertTrue(len(b64_output) > 0)

        # Decode and verify it looks like a MIDI file
        midi_bytes = base64.b64decode(b64_output)

        # Check MIDI Header 'MThd'
        self.assertEqual(midi_bytes[0:4], b'MThd')

        # Verify size (should be substantial given 3 tracks)
        self.assertGreater(len(midi_bytes), 500)

        # Optional: Write to file to check manually if needed
        # with open("test_mcp_output.mid", "wb") as f:
        #     f.write(midi_bytes)

if __name__ == '__main__':
    unittest.main()
