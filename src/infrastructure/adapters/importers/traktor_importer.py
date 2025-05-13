"""
Importer for Native Instruments Traktor library (NML format)
"""
import os
from typing import Dict, List, Optional
from datetime import datetime
from uuid import uuid4
import xml.etree.ElementTree as ET

from src.domain.entities.collection import Collection
from src.domain.entities.track import Track
from src.domain.entities.playlist import Playlist
from src.domain.entities.cue_point import CuePoint, CueType
from src.domain.entities.loop import Loop, LoopType
from src.infrastructure.adapters.importers.importer_interface import ImporterInterface


class TraktorImporter(ImporterInterface):
    """
    Importer for Native Instruments Traktor library (NML format)
    """
    
    @property
    def format_name(self) -> str:
        return "Traktor"
    
    def can_import(self, file_path: str) -> bool:
        """Check if the file is a valid Traktor NML file"""
        if not file_path.lower().endswith('.nml'):
            return False
            
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            return root.tag == 'NML'
        except Exception:
            return False
    
    def import_library(self, file_path: str) -> Optional[Collection]:
        """Import a Traktor library from an NML file"""
        if not self.can_import(file_path):
            return None
            
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            collection = Collection(name="Traktor Collection")
            
            # Import tracks
            self._import_tracks(root, collection)
            
            # Import playlists
            self._import_playlists(root, collection)
            
            return collection
        except Exception as e:
            print(f"Error importing Traktor library: {str(e)}")
            return None
    
    def _import_tracks(self, root: ET.Element, collection: Collection):
        """Import tracks from the NML file"""
        collection_node = root.find('.//COLLECTION')
        if collection_node is None:
            return
            
        for entry in collection_node.findall('./ENTRY'):
            track = self._parse_track(entry)
            if track:
                collection.add_track(track)
    
    def _parse_track(self, entry: ET.Element) -> Optional[Track]:
        """Parse a track from an ENTRY element"""
        try:
            location = entry.find('./LOCATION')
            if location is None:
                return None
                
            # Get file path
            volume = location.get('VOLUME', '')
            dir_path = location.get('DIR', '')
            file_name = location.get('FILE', '')
            file_path = os.path.join(volume, dir_path.lstrip('/'), file_name)
            
            # Create track
            track = Track(
                id=uuid4(),
                title=entry.get('TITLE', ''),
                artist=entry.get('ARTIST', ''),
                album=entry.get('ALBUM', ''),
                genre=entry.get('GENRE', ''),
                bpm=float(entry.get('TEMPO', '0')),
                key=entry.get('KEY', ''),
                file_path=file_path,
                comment=entry.get('COMMENT', '')
            )
            
            # Parse cue points
            cue_points = entry.findall('./CUE_V2')
            for cue in cue_points:
                track.add_cue_point(self._parse_cue_point(cue))
                
            # Parse loops
            loops = entry.findall('./LOOP')
            for loop in loops:
                track.add_loop(self._parse_loop(loop))
                
            return track
        except Exception as e:
            print(f"Error parsing track: {str(e)}")
            return None
    
    def _parse_cue_point(self, cue_element: ET.Element) -> CuePoint:
        """Parse a cue point from a CUE_V2 element"""
        cue_type_str = cue_element.get('TYPE', 'cue')
        position = float(cue_element.get('START', '0')) / 1000.0  # Convert from milliseconds to seconds
        
        # Map Traktor cue type to our CueType enum
        cue_type_map = {
            'cue': CueType.HOT_CUE,
            'fade-in': CueType.HOT_CUE,
            'fade-out': CueType.HOT_CUE,
            'load': CueType.HOT_CUE,
            'grid': CueType.GRID_MARKER,
            'loop': CueType.HOT_CUE
        }
        
        cue_type = cue_type_map.get(cue_type_str, CueType.HOT_CUE)
        
        # Get hot cue number
        hot_cue_number = -1
        if cue_type == CueType.HOT_CUE:
            hot_cue_number = int(cue_element.get('HOTCUE', '-1'))
            
        return CuePoint(
            name=cue_element.get('NAME', ''),
            position=position,
            type=cue_type,
            color=cue_element.get('COLOR', '#FFFFFF'),
            index=hot_cue_number
        )
    
    def _parse_loop(self, loop_element: ET.Element) -> Loop:
        """Parse a loop from a LOOP element"""
        start_position = float(loop_element.get('START', '0')) / 1000.0  # Convert from milliseconds to seconds
        end_position = float(loop_element.get('END', '0')) / 1000.0  # Convert from milliseconds to seconds
        
        return Loop(
            name=loop_element.get('NAME', ''),
            start_position=start_position,
            end_position=end_position,
            type=LoopType.REGULAR,
            color=loop_element.get('COLOR', '#FFFFFF')
        )
    
    def _import_playlists(self, root: ET.Element, collection: Collection):
        """Import playlists from the NML file"""
        playlists_node = root.find('.//PLAYLISTS')
        if playlists_node is None:
            return
            
        # Find the root node containing all playlists
        root_node = playlists_node.find('./NODE[@TYPE="FOLDER"]')
        if root_node is None:
            return
            
        # Process all playlists recursively
        self._process_playlist_node(root_node, None, collection)
    
    def _process_playlist_node(self, node: ET.Element, parent_id: Optional[str], collection: Collection):
        """Process a playlist node recursively"""
        node_type = node.get('TYPE', '')
        node_name = node.get('NAME', '')
        
        if node_type == 'FOLDER':
            # Create a folder playlist
            playlist = Playlist(
                name=node_name,
                parent_id=parent_id
            )
            playlist_id = collection.add_playlist(playlist)
            
            # Process child nodes
            for child in node.findall('./NODE'):
                self._process_playlist_node(child, playlist_id, collection)
                
        elif node_type == 'PLAYLIST':
            # Create a playlist
            playlist = Playlist(
                name=node_name,
                parent_id=parent_id
            )
            playlist_id = collection.add_playlist(playlist)
            
            # Add tracks to the playlist
            for entry in node.findall('./PLAYLIST/ENTRY'):
                location = entry.find('./PRIMARYKEY')
                if location is not None:
                    # Find the track by its location
                    volume = location.get('VOLUME', '')
                    dir_path = location.get('DIR', '')
                    file_name = location.get('FILE', '')
                    file_path = os.path.join(volume, dir_path.lstrip('/'), file_name)
                    
                    # Find the track in the collection
                    track = next(
                        (t for t in collection.tracks.values() if t.file_path == file_path),
                        None
                    )
                    
                    if track:
                        playlist = collection.get_playlist(playlist_id)
                        if playlist:
                            playlist.add_track(track.id)
