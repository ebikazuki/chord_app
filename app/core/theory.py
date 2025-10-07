from typing import List, Dict, Tuple
from app.models import KeySetting, ChordEvent

KEYS = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
MODES = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"]

MODE_INTERVALS = {
    "Ionian": [0, 2, 4, 5, 7, 9, 11],
    "Dorian": [0, 2, 3, 5, 7, 9, 10],
    "Phrygian": [0, 1, 3, 5, 7, 8, 10],
    "Lydian": [0, 2, 4, 6, 7, 9, 11],
    "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "Aeolian": [0, 2, 3, 5, 7, 8, 10],
    "Locrian": [0, 1, 3, 5, 6, 8, 10],
}

MODE_QUALITIES = {
    "Ionian": ["maj", "min", "min", "maj", "maj", "min", "dim"],
    "Dorian": ["min", "min", "maj", "maj", "min", "dim", "maj"],
    "Phrygian": ["min", "maj", "maj", "min", "dim", "maj", "min"],
    "Lydian": ["maj", "maj", "min", "dim", "maj", "min", "min"],
    "Mixolydian": ["maj", "min", "dim", "maj", "min", "min", "maj"],
    "Aeolian": ["min", "dim", "maj", "min", "min", "maj", "maj"],
    "Locrian": ["dim", "maj", "min", "min", "maj", "maj", "min"],
}

DEGREE_NAMES = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]

def note_to_midi(note: str, octave: int) -> int:
    """Convert note name and octave to MIDI number"""
    note_values = {"C": 0, "Db": 1, "D": 2, "Eb": 3, "E": 4, "F": 5,
                   "Gb": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11}
    return 12 * (octave + 1) + note_values[note]

def degree_to_chord(key_setting: KeySetting, degree_idx: int) -> Dict:
    """Generate chord specification from key and degree index (0-6)"""
    intervals = MODE_INTERVALS[key_setting.mode]
    
    tonic_midi = note_to_midi(key_setting.tonic, key_setting.octave_base)
    root_midi = tonic_midi + intervals[degree_idx]
    
    quality = MODE_QUALITIES[key_setting.mode][degree_idx]
    
    third_interval = 3 if quality == "min" or quality == "dim" else 4
    fifth_interval = 6 if quality == "dim" else 7
    
    notes = [root_midi, root_midi + third_interval, root_midi + fifth_interval]
    
    if 7 in key_setting.tensions:
        seventh_interval = 10 if quality == "maj" or quality == "min" else 11
        if quality == "dim":
            seventh_interval = 9
        notes.append(root_midi + seventh_interval)
        quality += "7"
    
    return {
        "notes": notes,
        "quality": quality,
        "degree": DEGREE_NAMES[degree_idx],
        "tensions": key_setting.tensions,
        "voicing": key_setting.voicing,
        "inversion": key_setting.inversion,
    }

def chord_to_asset_path(key_setting: KeySetting, degree_idx: int) -> str:
    """Map chord to audio asset filename"""
    chord = degree_to_chord(key_setting, degree_idx)
    
    tensions_str = "-".join(map(str, key_setting.tensions)) if key_setting.tensions else ""
    
    filename = (f"{key_setting.tonic}_{key_setting.mode}_"
                f"{chord['degree']}_{chord['quality']}_"
                f"{key_setting.voicing}_{key_setting.inversion}_"
                f"{tensions_str}_oct{key_setting.octave_base}.wav")
    
    return f"audio/{filename}"
