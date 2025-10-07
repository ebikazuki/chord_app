import flet as ft
from flet import Audio
from pathlib import Path
from typing import Dict, Optional
from app.models import KeySetting

class AudioEngine:
    """Manages audio playback with flet Audio control"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.audio_controls: Dict[str, Audio] = {}
        self.active_voices: Dict[str, str] = {}
        self.max_voices = 8
        
    def preload_assets(self, key_setting: KeySetting):
        """Preload audio samples for current key/mode (stub for MVP)"""
        pass
    
    def play_sample(self, path: str, sustain: bool = False, gain: float = 1.0) -> str:
        """Play audio sample and return voice ID"""
        if not Path(f"assets/{path}").exists():
            print(f"Warning: Audio file not found: assets/{path}")
            path = "audio/C_Ionian_I_maj_drop2_root__oct4.wav"
            if not Path(f"assets/{path}").exists():
                print("Error: No audio samples available")
                return "error"
        
        voice_id = f"voice_{len(self.audio_controls)}"
        audio = Audio(
            src=path,
            autoplay=True,
            volume=gain,
            on_state_changed=lambda e: self._on_audio_complete(voice_id, e),
        )
        
        self.page.overlay.append(audio)
        self.audio_controls[voice_id] = audio
        self.active_voices[voice_id] = path
        
        if len(self.active_voices) > self.max_voices:
            oldest_voice = list(self.active_voices.keys())[0]
            self.stop_voice(oldest_voice)
        
        self.page.update()
        return voice_id
    
    def _on_audio_complete(self, voice_id: str, event):
        """Handle audio completion"""
        if event.data == "completed":
            if voice_id in self.active_voices:
                del self.active_voices[voice_id]
    
    def stop_voice(self, voice_id: str):
        """Stop specific audio voice"""
        if voice_id in self.audio_controls:
            audio = self.audio_controls[voice_id]
            audio.pause()
            if voice_id in self.active_voices:
                del self.active_voices[voice_id]
    
    def stop_all(self):
        """Stop all playing voices"""
        for voice_id in list(self.active_voices.keys()):
            self.stop_voice(voice_id)
