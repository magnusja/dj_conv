"""
Playlist entity representing a playlist in a DJ library
"""
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4, UUID


@dataclass
class Playlist:
    """
    Represents a playlist in a DJ library
    """
    id: UUID = None
    name: str = ""
    description: str = ""
    track_ids: List[UUID] = field(default_factory=list)
    parent_id: Optional[UUID] = None
    children: List['Playlist'] = field(default_factory=list)
    
    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
            
    def add_track(self, track_id: UUID):
        """Add a track to the playlist"""
        if track_id not in self.track_ids:
            self.track_ids.append(track_id)
            
    def remove_track(self, track_id: UUID):
        """Remove a track from the playlist"""
        if track_id in self.track_ids:
            self.track_ids.remove(track_id)
            
    def add_child(self, playlist: 'Playlist'):
        """Add a child playlist"""
        playlist.parent_id = self.id
        self.children.append(playlist)
        
    def remove_child(self, playlist_id: UUID):
        """Remove a child playlist"""
        for i, child in enumerate(self.children):
            if child.id == playlist_id:
                self.children.pop(i)
                break
