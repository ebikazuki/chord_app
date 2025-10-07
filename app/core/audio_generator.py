import numpy as np
from scipy.io import wavfile
from pathlib import Path

def generate_chord_sample(notes_midi: list, duration_sec: float = 1.0, 
                         sample_rate: int = 44100) -> np.ndarray:
    """Generate a simple chord audio sample using sine waves"""
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec))
    
    audio = np.zeros_like(t)
    for midi_note in notes_midi:
        freq = 440.0 * (2.0 ** ((midi_note - 69) / 12.0))
        audio += np.sin(2 * np.pi * freq * t)
    
    audio = audio / len(notes_midi)
    
    fade_samples = int(0.01 * sample_rate)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    audio[:fade_samples] *= fade_in
    audio[-fade_samples:] *= fade_out
    
    audio_16bit = (audio * 32767).astype(np.int16)
    stereo = np.stack([audio_16bit, audio_16bit], axis=1)
    
    return stereo

def generate_dummy_samples():
    """Generate a few dummy samples for testing"""
    Path("assets/audio").mkdir(parents=True, exist_ok=True)
    
    test_chords = [
        ("C_Ionian_I_maj_drop2_root__oct4.wav", [60, 64, 67]),
        ("C_Ionian_V_maj_drop2_root__oct4.wav", [67, 71, 74]),
        ("C_Ionian_vi_min_drop2_root__oct4.wav", [69, 72, 76]),
        ("C_Ionian_IV_maj_drop2_root__oct4.wav", [65, 69, 72]),
    ]
    
    for filename, notes in test_chords:
        audio = generate_chord_sample(notes, duration_sec=1.5)
        wavfile.write(f"assets/audio/{filename}", 44100, audio)
        print(f"Generated: {filename}")

def generate_all_chord_samples():
    """Generate all chord samples for production use"""
    from app.core.theory import (
        KEYS, MODES, MODE_INTERVALS, MODE_QUALITIES,
        DEGREE_NAMES, note_to_midi
    )

    output_dir = Path("assets/audio")
    output_dir.mkdir(parents=True, exist_ok=True)

    voicings = ["drop2"]
    inversions = ["root"]
    tension_sets = [[], [7]]
    octaves = [3, 4, 5]

    total_count = 0

    for key in KEYS:
        for mode in MODES:
            intervals = MODE_INTERVALS[mode]
            qualities = MODE_QUALITIES[mode]

            for degree_idx in range(7):
                degree_name = DEGREE_NAMES[degree_idx]
                base_quality = qualities[degree_idx]

                for octave in octaves:
                    tonic_midi = note_to_midi(key, octave)
                    root_midi = tonic_midi + intervals[degree_idx]

                    for voicing in voicings:
                        for inversion in inversions:
                            for tensions in tension_sets:
                                quality = base_quality
                                third_interval = 3 if base_quality in ["min", "dim"] else 4
                                fifth_interval = 6 if base_quality == "dim" else 7

                                notes = [root_midi, root_midi + third_interval, root_midi + fifth_interval]

                                if 7 in tensions:
                                    if base_quality == "maj":
                                        seventh_interval = 11
                                    elif base_quality == "min":
                                        seventh_interval = 10
                                    elif base_quality == "dim":
                                        seventh_interval = 9
                                    notes.append(root_midi + seventh_interval)
                                    quality += "7"

                                tensions_str = "-".join(map(str, tensions)) if tensions else ""

                                filename = (f"{key}_{mode}_{degree_name}_{quality}_"
                                           f"{voicing}_{inversion}_{tensions_str}_oct{octave}.wav")

                                audio = generate_chord_sample(notes, duration_sec=1.5)
                                filepath = output_dir / filename
                                wavfile.write(filepath, 44100, audio)

                                total_count += 1
                                if total_count % 50 == 0:
                                    print(f"Generated {total_count} samples...")

    print(f"\nCompleted: Generated {total_count} chord samples in total")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        generate_all_chord_samples()
    else:
        generate_dummy_samples()
