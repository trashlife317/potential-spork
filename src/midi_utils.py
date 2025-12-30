import struct

def text_to_bytes(text):
    return text.encode('latin1')

class MidiWriter:
    def __init__(self):
        self.tracks = []
        self.resolution = 480 # Ticks per quarter note

    def add_track(self, notes, track_name="Melody"):
        """
        notes: list of dicts {'note': int, 'duration': float (beats), 'velocity': int, 'offset': float}
        """
        track_data = bytearray()

        # Track Name Meta Event
        track_data.extend(b'\x00\xFF\x03')
        name_bytes = text_to_bytes(track_name)
        track_data.append(len(name_bytes))
        track_data.extend(name_bytes)

        # Tempo (Default 120, but we can set it. For simplicity, we stick to default or add meta event later)
        # Time Signature (Default 4/4)

        # Convert absolute offsets to delta times
        # Sort notes by start time just in case
        sorted_notes = sorted(notes, key=lambda x: x['offset'])

        events = []
        for n in sorted_notes:
            start_tick = int(n['offset'] * self.resolution)
            duration_ticks = int(n['duration'] * self.resolution)
            end_tick = start_tick + duration_ticks

            # Note On
            events.append({
                'tick': start_tick,
                'type': 'on',
                'note': n['note'],
                'velocity': n['velocity']
            })

            # Note Off
            events.append({
                'tick': end_tick,
                'type': 'off',
                'note': n['note'],
                'velocity': 0
            })

        events.sort(key=lambda x: x['tick'])

        last_tick = 0
        running_status = None

        for ev in events:
            delta = ev['tick'] - last_tick
            last_tick = ev['tick']

            # Write variable length delta
            track_data.extend(self.encode_variable_length(delta))

            # Event Type
            if ev['type'] == 'on':
                status = 0x90 # Channel 0 Note On
                track_data.append(status)
                track_data.append(ev['note'])
                track_data.append(ev['velocity'])
            else:
                status = 0x80 # Channel 0 Note Off
                track_data.append(status)
                track_data.append(ev['note'])
                track_data.append(ev['velocity'])

        # End of Track
        track_data.extend(b'\x00\xFF\x2F\x00')

        self.tracks.append(track_data)

    def encode_variable_length(self, val):
        bytes_list = []
        bytes_list.append(val & 0x7F)
        val >>= 7
        while val > 0:
            bytes_list.append((val & 0x7F) | 0x80)
            val >>= 7
        return bytes(reversed(bytes_list))

    def write_file(self, filename):
        with open(filename, 'wb') as f:
            # Header Chunk
            f.write(b'MThd')
            f.write(struct.pack('>L', 6)) # Chunk size 6
            f.write(struct.pack('>H', 1)) # Format 1 (Multiple tracks)
            f.write(struct.pack('>H', len(self.tracks))) # Number of tracks
            f.write(struct.pack('>H', self.resolution))

            # Track Chunks
            for track_data in self.tracks:
                f.write(b'MTrk')
                f.write(struct.pack('>L', len(track_data)))
                f.write(track_data)
