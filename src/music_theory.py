
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Create lookup maps
NOTE_TO_INDEX = {note: i for i, note in enumerate(NOTES)}
NOTE_NORM_MAP = {
    'DB': 'C#', 'EB': 'D#', 'GB': 'F#', 'AB': 'G#', 'BB': 'A#',
    # Common flats mapped to their sharp equivalents
    'CB': 'B',  # C flat is B
    'FB': 'E',  # F flat is E
}

# Scale intervals (semitones from root)
SCALES = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],  # Natural Minor
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'phrygian': [0, 1, 3, 5, 7, 8, 10], # Common in Trap
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'pentatonic_minor': [0, 3, 5, 7, 10],
    'pentatonic_major': [0, 2, 4, 7, 9],
    'blues': [0, 3, 5, 6, 7, 10] # Minor Blues
}

def get_note_index(note_name):
    """Returns the index of the note in the chromatic scale (0-11)."""
    # Normalize input
    note_name = note_name.upper()

    # Check normalization map first (O(1))
    if note_name in NOTE_NORM_MAP:
        note_name = NOTE_NORM_MAP[note_name]

    # Check if direct match in index map (O(1))
    if note_name in NOTE_TO_INDEX:
        return NOTE_TO_INDEX[note_name]

    # Fallback for complex cases (like 'Db' mixed case if upper() wasn't enough?)
    # upper() handles 'Db' -> 'DB', which is in map.
    # 'C#' -> 'C#', which is in index map.

    # Special case: simple flats not in map?
    # e.g. if we get "Dbb" or something weird.
    # The original code only handled simple flats via explicit check if len==2 and [1]=='b'.
    # My map handles DB, EB, GB, AB, BB, CB, FB.
    # That covers all 7 diatonic flats.

    raise ValueError(f"Invalid note name: {note_name}")

def get_scale_notes(root_note, scale_type, start_octave=3, end_octave=5):
    """Returns a list of MIDI numbers for the scale across specified octaves."""
    try:
        root_idx = get_note_index(root_note)
    except ValueError:
        # Default to C if invalid
        root_idx = 0

    scale_key = scale_type.lower().replace(' ', '_')
    if scale_key not in SCALES:
        scale_key = 'minor' # Default to minor for hip hop context

    intervals = SCALES[scale_key]

    midi_notes = []
    # Loop through octaves
    for octave in range(start_octave, end_octave + 1):
        # MIDI note 0 is C-1. C4 is 60.
        root_midi = root_idx + (octave + 1) * 12
        for interval in intervals:
            midi_note = root_midi + interval
            if 0 <= midi_note <= 127:
                midi_notes.append(midi_note)

    # Notes are generated in strictly increasing order (octave increasing, interval increasing)
    # Intervals are distinct within an octave.
    # Max interval is 11, so no overlap with next octave (start + 12).
    # Thus, no need for set() or sorted().
    return midi_notes

def get_note_name(midi_number):
    """Converts MIDI number to Note Name (e.g., 60 -> C4)."""
    if not (0 <= midi_number <= 127):
        return "Unknown"
    octave = (midi_number // 12) - 1
    note_idx = midi_number % 12
    return f"{NOTES[note_idx]}{octave}"

def analyze_interval(note1, note2):
    """Returns the interval in semitones."""
    return abs(note1 - note2)

def is_stable_scale_degree(midi_note, root_note_name, scale_type):
    """Checks if a note is the Tonic, 3rd (mediant), or 5th (dominant) of the scale."""
    try:
        root_idx = get_note_index(root_note_name)
    except:
        root_idx = 0

    note_chromatic_idx = midi_note % 12
    interval_from_root = (note_chromatic_idx - root_idx) % 12

    # Stable degrees: 0 (Tonic), 7 (Dominant)
    # 3rd depends on scale (Major=4, Minor=3)

    scale_key = scale_type.lower().replace(' ', '_')
    is_major = 'major' in scale_key and 'minor' not in scale_key # Simple check

    if interval_from_root == 0 or interval_from_root == 7:
        return True

    if is_major and interval_from_root == 4:
        return True
    if not is_major and interval_from_root == 3:
        return True

    return False
