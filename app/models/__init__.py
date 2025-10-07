from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid

@dataclass
class KeySetting:
    """Musical context configuration"""
    tonic: str
    mode: str
    bpm: int = 100
    octave_base: int = 4
    voicing: str = "drop2"
    inversion: str = "root"
    tensions: List[int] = field(default_factory=list)

@dataclass
class ChordEvent:
    """Single chord play event"""
    degree: str
    quality: str
    tension: List[int] = field(default_factory=list)
    inversion: str = "root"
    voicing: str = "drop2"
    duration_beats: float = 1.0
    sustain: bool = False

@dataclass
class Progression:
    """Complete chord sequence"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Untitled"
    key_setting: Optional[KeySetting] = None
    events: List[ChordEvent] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
