"""
CuePoint entity representing a cue point in a track
"""
from dataclasses import dataclass
from enum import Enum, auto
from uuid import uuid4, UUID


class CueType(Enum):
    """Types of cue points in DJ software"""
    HOT_CUE = auto()
    MEMORY_CUE = auto()
    GRID_MARKER = auto()
    LOOP_IN = auto()
    LOOP_OUT = auto()
    LOAD_MARKER = auto()
    FADE_IN = auto()
    FADE_OUT = auto()


@dataclass
class CuePoint:
    """
    Represents a cue point in a track
    """
    id: UUID = None
    name: str = ""
    position: float = 0.0  # in seconds
    type: CueType = CueType.HOT_CUE
    color: str = "#FFFFFF"
    index: int = -1  # For hot cues, this is the pad number (0-7 typically)
    
    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
            
    def to_memory_cue(self):
        """Convert a hot cue to a memory cue"""
        self.type = CueType.MEMORY_CUE
        return self
