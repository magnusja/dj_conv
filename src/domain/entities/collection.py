"""
Collection entity representing a DJ library collection
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import UUID

from src.domain.entities.track import Track
from src.domain.entities.playlist import Playlist


@dataclass
class Collection:
    """
    Represents a DJ library collection containing tracks and playlists
    """
    name: str = "DJ Collection"
    tracks: Dict[UUID, Track] = field(default_factory=dict)
    playlists: Dict[UUID, Playlist] = field(default_factory=dict)
    root_playlists: List[UUID] = field(default_factory=list)
    
    def add_track(self, track: Track):
        """Add a track to the collection"""
        self.tracks[track.id] = track
        return track.id
        
    def get_track(self, track_id: UUID) -> Optional[Track]:
        """Get a track by ID"""
        return self.tracks.get(track_id)
        
    def add_playlist(self, playlist: Playlist):
        """Add a playlist to the collection"""
        self.playlists[playlist.id] = playlist
        if playlist.parent_id is None:
            self.root_playlists.append(playlist.id)
        return playlist.id
        
    def get_playlist(self, playlist_id: UUID) -> Optional[Playlist]:
        """Get a playlist by ID"""
        return self.playlists.get(playlist_id)
        
    def get_playlist_tracks(self, playlist_id: UUID) -> List[Track]:
        """Get all tracks in a playlist"""
        playlist = self.get_playlist(playlist_id)
        if not playlist:
            return []
        
        return [self.tracks[track_id] for track_id in playlist.track_ids if track_id in self.tracks]
