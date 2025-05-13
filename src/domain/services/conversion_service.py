"""
Domain service for converting between different DJ software formats
"""
from typing import Dict, List, Optional
from uuid import UUID

from src.domain.entities.collection import Collection
from src.domain.entities.track import Track
from src.domain.entities.cue_point import CuePoint, CueType
from src.domain.value_objects.cue_type import CueTypeMapping


class ConversionService:
    """
    Domain service for handling conversion logic between different DJ software formats
    """
    
    def __init__(self, cue_type_mapping: Optional[CueTypeMapping] = None):
        self.cue_type_mapping = cue_type_mapping or CueTypeMapping()
        
    def convert_hot_cues_to_memory_cues(self, collection: Collection) -> Collection:
        """
        Convert all hot cues in the collection to memory cues
        
        Args:
            collection: The collection to convert
            
        Returns:
            The converted collection
        """
        for track_id, track in collection.tracks.items():
            converted_cues = []
            for cue in track.cue_points:
                if cue.type == CueType.HOT_CUE:
                    converted_cues.append(cue.to_memory_cue())
                else:
                    converted_cues.append(cue)
            track.cue_points = converted_cues
            
        return collection
    
    def merge_collections(self, source: Collection, target: Collection) -> Collection:
        """
        Merge two collections, adding tracks and playlists from source to target
        
        Args:
            source: The source collection
            target: The target collection
            
        Returns:
            The merged collection
        """
        # Track ID mapping from source to target
        id_mapping: Dict[UUID, UUID] = {}
        
        # Add tracks from source to target
        for track_id, track in source.tracks.items():
            # Check if track already exists in target (by file path)
            existing_track = next(
                (t for t in target.tracks.values() if t.file_path == track.file_path), 
                None
            )
            
            if existing_track:
                id_mapping[track_id] = existing_track.id
            else:
                # Create a new track in target
                new_track = Track(
                    title=track.title,
                    artist=track.artist,
                    album=track.album,
                    genre=track.genre,
                    bpm=track.bpm,
                    key=track.key,
                    duration=track.duration,
                    file_path=track.file_path,
                    file_size=track.file_size,
                    bitrate=track.bitrate,
                    sample_rate=track.sample_rate,
                    comment=track.comment,
                    year=track.year,
                    rating=track.rating,
                    cue_points=track.cue_points.copy(),
                    loops=track.loops.copy(),
                    beat_grid=track.beat_grid.copy(),
                    custom_tags=track.custom_tags.copy()
                )
                target.add_track(new_track)
                id_mapping[track_id] = new_track.id
        
        # Add playlists from source to target
        for playlist_id, playlist in source.playlists.items():
            # Create a new playlist in target
            from src.domain.entities.playlist import Playlist
            new_playlist = Playlist(
                name=playlist.name,
                description=playlist.description,
                track_ids=[id_mapping.get(tid) for tid in playlist.track_ids if tid in id_mapping],
                parent_id=None  # Will be set later
            )
            
            # Add the playlist to target
            target.add_playlist(new_playlist)
            
        return target
