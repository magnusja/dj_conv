"""
Repository for track entities
"""
from typing import Dict, List, Optional
from uuid import UUID

from src.domain.entities.track import Track


class TrackRepository:
    """
    Repository for track entities
    """
    
    def __init__(self):
        self.tracks: Dict[UUID, Track] = {}
        
    def add(self, track: Track) -> UUID:
        """
        Add a track to the repository
        
        Args:
            track: The track to add
            
        Returns:
            The ID of the added track
        """
        self.tracks[track.id] = track
        return track.id
        
    def get(self, track_id: UUID) -> Optional[Track]:
        """
        Get a track by ID
        
        Args:
            track_id: The ID of the track to get
            
        Returns:
            The track or None if not found
        """
        return self.tracks.get(track_id)
        
    def get_all(self) -> List[Track]:
        """
        Get all tracks
        
        Returns:
            A list of all tracks
        """
        return list(self.tracks.values())
        
    def update(self, track: Track) -> bool:
        """
        Update a track
        
        Args:
            track: The track to update
            
        Returns:
            True if the track was updated, False otherwise
        """
        if track.id not in self.tracks:
            return False
            
        self.tracks[track.id] = track
        return True
        
    def delete(self, track_id: UUID) -> bool:
        """
        Delete a track
        
        Args:
            track_id: The ID of the track to delete
            
        Returns:
            True if the track was deleted, False otherwise
        """
        if track_id not in self.tracks:
            return False
            
        del self.tracks[track_id]
        return True
        
    def find_by_path(self, file_path: str) -> Optional[Track]:
        """
        Find a track by its file path
        
        Args:
            file_path: The file path to search for
            
        Returns:
            The track or None if not found
        """
        for track in self.tracks.values():
            if track.file_path == file_path:
                return track
                
        return None
