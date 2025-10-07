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

if __name__ == "__main__":
    generate_dummy_samples()
