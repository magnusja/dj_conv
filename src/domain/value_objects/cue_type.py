"""
Value objects for cue types and mappings between different DJ software
"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class TraktorCueType(Enum):
    """Cue types in Traktor"""
    CUE = "cue"
    FADE_IN = "fade-in"
    FADE_OUT = "fade-out"
    LOAD = "load"
    GRID = "grid"
    LOOP = "loop"


class RekordboxCueType(Enum):
    """Cue types in Rekordbox"""
    MEMORY = "memory"
    HOT = "hot"
    LOOP = "loop"


@dataclass(frozen=True)
class CueTypeMapping:
    """Mapping between cue types in different DJ software"""
    traktor_to_rekordbox: Dict[TraktorCueType, RekordboxCueType] = None
    
    def __post_init__(self):
        # Default mapping if none provided
        if self.traktor_to_rekordbox is None:
            object.__setattr__(self, "traktor_to_rekordbox", {
                TraktorCueType.CUE: RekordboxCueType.HOT,
                TraktorCueType.FADE_IN: RekordboxCueType.MEMORY,
                TraktorCueType.FADE_OUT: RekordboxCueType.MEMORY,
                TraktorCueType.LOAD: RekordboxCueType.MEMORY,
                TraktorCueType.GRID: RekordboxCueType.MEMORY,
                TraktorCueType.LOOP: RekordboxCueType.LOOP
            })
    
    def get_rekordbox_type(self, traktor_type: TraktorCueType) -> Optional[RekordboxCueType]:
        """Get the corresponding Rekordbox cue type for a Traktor cue type"""
        return self.traktor_to_rekordbox.get(traktor_type)
