from pathlib import Path
from app.models import Progression
import shutil

class ExportService:
    """Handles audio export"""
    
    def export_wav(self, progression: Progression, output_path: str) -> bool:
        """Export progression to WAV file (simplified for MVP)"""
        dummy_sample = Path("assets/audio/C_Ionian_I_maj_drop2_root__oct4.wav")
        if dummy_sample.exists():
            shutil.copy(dummy_sample, output_path)
            print(f"Exported (placeholder): {output_path}")
            return True
        return False
    
    def export_m4a(self, progression: Progression, output_path: str) -> bool:
        """Export progression to M4A file (not implemented in MVP)"""
        print("M4A export not yet implemented")
        return False
