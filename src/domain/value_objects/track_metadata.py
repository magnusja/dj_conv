"""
Value objects for track metadata
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TrackMetadata:
    """Immutable value object for track metadata"""
    title: str
    artist: str
    album: Optional[str] = None
    genre: Optional[str] = None
    bpm: Optional[float] = None
    key: Optional[str] = None
    year: Optional[int] = None
    comment: Optional[str] = None
    
    def __str__(self) -> str:
        return f"{self.artist} - {self.title}"
