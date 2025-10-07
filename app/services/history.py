from typing import List
from app.models import ChordEvent

class HistoryService:
    """Manages chord event history with undo/redo"""
    
    def __init__(self):
        self.events: List[ChordEvent] = []
        self.current_index = -1
    
    def push_event(self, event: ChordEvent):
        """Add new event to history"""
        self.events = self.events[:self.current_index + 1]
        self.events.append(event)
        self.current_index += 1
    
    def undo(self) -> bool:
        """Undo last event"""
        if self.current_index >= 0:
            self.current_index -= 1
            return True
        return False
    
    def redo(self) -> bool:
        """Redo next event"""
        if self.current_index < len(self.events) - 1:
            self.current_index += 1
            return True
        return False
    
    def get_current_events(self) -> List[ChordEvent]:
        """Get events up to current index"""
        return self.events[:self.current_index + 1]
    
    def clear(self):
        """Clear all history"""
        self.events = []
        self.current_index = -1
