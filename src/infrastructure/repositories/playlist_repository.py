"""
Repository for playlist entities
"""
from typing import Dict, List, Optional
from uuid import UUID

from src.domain.entities.playlist import Playlist


class PlaylistRepository:
    """
    Repository for playlist entities
    """
    
    def __init__(self):
        self.playlists: Dict[UUID, Playlist] = {}
        self.root_playlists: List[UUID] = []
        
    def add(self, playlist: Playlist) -> UUID:
        """
        Add a playlist to the repository
        
        Args:
            playlist: The playlist to add
            
        Returns:
            The ID of the added playlist
        """
        self.playlists[playlist.id] = playlist
        
        # If this is a root playlist, add it to the root playlists list
        if playlist.parent_id is None:
            self.root_playlists.append(playlist.id)
            
        return playlist.id
        
    def get(self, playlist_id: UUID) -> Optional[Playlist]:
        """
        Get a playlist by ID
        
        Args:
            playlist_id: The ID of the playlist to get
            
        Returns:
            The playlist or None if not found
        """
        return self.playlists.get(playlist_id)
        
    def get_all(self) -> List[Playlist]:
        """
        Get all playlists
        
        Returns:
            A list of all playlists
        """
        return list(self.playlists.values())
        
    def get_root_playlists(self) -> List[Playlist]:
        """
        Get all root playlists
        
        Returns:
            A list of all root playlists
        """
        return [self.playlists[pid] for pid in self.root_playlists if pid in self.playlists]
        
    def get_children(self, playlist_id: UUID) -> List[Playlist]:
        """
        Get all child playlists of a playlist
        
        Args:
            playlist_id: The ID of the parent playlist
            
        Returns:
            A list of child playlists
        """
        return [p for p in self.playlists.values() if p.parent_id == playlist_id]
        
    def update(self, playlist: Playlist) -> bool:
        """
        Update a playlist
        
        Args:
            playlist: The playlist to update
            
        Returns:
            True if the playlist was updated, False otherwise
        """
        if playlist.id not in self.playlists:
            return False
            
        # Check if parent ID changed
        old_playlist = self.playlists[playlist.id]
        if old_playlist.parent_id != playlist.parent_id:
            # If it was a root playlist and now has a parent, remove from root
            if old_playlist.parent_id is None and playlist.parent_id is not None:
                if playlist.id in self.root_playlists:
                    self.root_playlists.remove(playlist.id)
            # If it wasn't a root playlist and now is, add to root
            elif old_playlist.parent_id is not None and playlist.parent_id is None:
                if playlist.id not in self.root_playlists:
                    self.root_playlists.append(playlist.id)
                    
        self.playlists[playlist.id] = playlist
        return True
        
    def delete(self, playlist_id: UUID) -> bool:
        """
        Delete a playlist
        
        Args:
            playlist_id: The ID of the playlist to delete
            
        Returns:
            True if the playlist was deleted, False otherwise
        """
        if playlist_id not in self.playlists:
            return False
            
        # Remove from root playlists if it's there
        if playlist_id in self.root_playlists:
            self.root_playlists.remove(playlist_id)
            
        # Delete the playlist
        del self.playlists[playlist_id]
        
        # Update children to have no parent
        for playlist in self.playlists.values():
            if playlist.parent_id == playlist_id:
                playlist.parent_id = None
                if playlist.id not in self.root_playlists:
                    self.root_playlists.append(playlist.id)
                    
        return True
