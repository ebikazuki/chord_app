import json
from pathlib import Path
from typing import List
from app.models import Progression, KeySetting, ChordEvent
from dataclasses import asdict

class PersistenceService:
    """Manages saving/loading progressions"""
    
    def __init__(self, data_file: str = "data/progressions.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
    
    def save_progression(self, progression: Progression):
        """Save a progression to JSON"""
        progressions = self.list_progressions()
        
        existing_idx = next((i for i, p in enumerate(progressions) 
                           if p["id"] == progression.id), None)
        
        prog_dict = asdict(progression)
        if existing_idx is not None:
            progressions[existing_idx] = prog_dict
        else:
            progressions.append(prog_dict)
        
        with open(self.data_file, 'w') as f:
            json.dump(progressions, f, indent=2)
    
    def list_progressions(self) -> List[dict]:
        """List all saved progressions"""
        if not self.data_file.exists():
            return []
        
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def load_progression(self, prog_id: str) -> Progression:
        """Load a specific progression"""
        progressions = self.list_progressions()
        prog_dict = next((p for p in progressions if p["id"] == prog_id), None)
        
        if not prog_dict:
            raise ValueError(f"Progression {prog_id} not found")
        
        key_setting = KeySetting(**prog_dict["key_setting"])
        events = [ChordEvent(**e) for e in prog_dict["events"]]
        
        return Progression(
            id=prog_dict["id"],
            name=prog_dict["name"],
            key_setting=key_setting,
            events=events,
            created_at=prog_dict["created_at"],
            updated_at=prog_dict["updated_at"],
        )
