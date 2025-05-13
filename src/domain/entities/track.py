"""
Track entity representing a music track in a DJ library
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from uuid import uuid4, UUID


@dataclass
class Track:
    """
    Represents a music track in a DJ library with all its metadata
    """
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    artist: str = ""
    album: str = ""
    genre: str = ""
    bpm: float = 0.0
    key: str = ""
    duration: float = 0.0  # in seconds
    file_path: str = ""
    file_size: int = 0
    bitrate: int = 0
    sample_rate: int = 0
    comment: str = ""
    year: Optional[int] = None
    rating: int = 0
    import_date: datetime = field(default_factory=datetime.now)
    last_played: Optional[datetime] = None
    play_count: int = 0
    cue_points: List = field(default_factory=list)
    loops: List = field(default_factory=list)
    beat_grid: List = field(default_factory=list)
    custom_tags: Dict[str, str] = field(default_factory=dict)
    
    def add_cue_point(self, cue_point):
        """Add a cue point to the track"""
        self.cue_points.append(cue_point)
        
    def add_loop(self, loop):
        """Add a loop to the track"""
        self.loops.append(loop)
        
    def add_custom_tag(self, key: str, value: str):
        """Add a custom tag to the track"""
        self.custom_tags[key] = value
