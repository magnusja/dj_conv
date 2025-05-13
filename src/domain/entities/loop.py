"""
Loop entity representing a loop in a track
"""
from dataclasses import dataclass
from enum import Enum, auto
from uuid import uuid4, UUID


class LoopType(Enum):
    """Types of loops in DJ software"""
    REGULAR = auto()
    SAVED = auto()
    AUTOLOOP = auto()


@dataclass
class Loop:
    """
    Represents a loop in a track
    """
    id: UUID = None
    name: str = ""
    start_position: float = 0.0  # in seconds
    end_position: float = 0.0  # in seconds
    type: LoopType = LoopType.REGULAR
    color: str = "#FFFFFF"
    index: int = -1  # For saved loops, this is the pad number
    
    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
            
    @property
    def length(self) -> float:
        """Get the length of the loop in seconds"""
        return self.end_position - self.start_position
