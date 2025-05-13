"""
Exporter for Pioneer Rekordbox library (XML format)
"""
import os
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, Any, List, Optional

from src.domain.entities.collection import Collection
from src.domain.entities.track import Track
from src.domain.entities.playlist import Playlist
from src.domain.entities.cue_point import CuePoint, CueType
from src.domain.entities.loop import Loop
from src.infrastructure.adapters.exporters.exporter_interface import ExporterInterface


class RekordboxExporter(ExporterInterface):
    """
    Exporter for Pioneer Rekordbox library (XML format)
    """
    
    @property
    def format_name(self) -> str:
        return "Rekordbox"
    
    def export_library(self, collection: Collection, file_path: str, options: Dict[str, Any] = None) -> bool:
        """Export a collection to a Rekordbox XML file"""
        options = options or {}
        
        try:
            # Create the root element
            root = ET.Element('DJ_PLAYLISTS', {
                'Version': '1.0.0',
                'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                'xsi:noNamespaceSchemaLocation': 'https://raw.githubusercontent.com/rekordbox/xml-schema/master/rekordbox_xml_schema.xsd'
            })
            
            # Add product info
            product = ET.SubElement(root, 'PRODUCT', {
                'Name': 'DJ Library Converter',
                'Version': '1.0.0',
                'Company': 'DJ Library Converter'
            })
            
            # Add collection
            collection_elem = ET.SubElement(root, 'COLLECTION', {
                'Entries': str(len(collection.tracks))
            })
            
            # Add tracks to collection
            for track_id, track in collection.tracks.items():
                self._add_track_to_collection(track, collection_elem, options)
            
            # Add playlists
            playlists_elem = ET.SubElement(root, 'PLAYLISTS')
            root_node = ET.SubElement(playlists_elem, 'NODE', {
                'Type': '0',
                'Name': 'ROOT',
                'Count': str(len(collection.root_playlists))
            })
            
            # Add root playlists
            for playlist_id in collection.root_playlists:
                playlist = collection.get_playlist(playlist_id)
                if playlist:
                    self._add_playlist_to_node(playlist, root_node, collection, options)
            
            # Write the XML file
            tree = ET.ElementTree(root)
            
            # Pretty print the XML
            xml_string = ET.tostring(root, encoding='utf-8')
            dom = minidom.parseString(xml_string)
            pretty_xml = dom.toprettyxml(indent="  ")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(pretty_xml)
                
            return True
        except Exception as e:
            print(f"Error exporting Rekordbox library: {str(e)}")
            return False
    
    def _add_track_to_collection(self, track: Track, collection_elem: ET.Element, options: Dict[str, Any]):
        """Add a track to the collection element"""
        # Create track element
        track_elem = ET.SubElement(collection_elem, 'TRACK', {
            'TrackID': str(track.id).replace('-', ''),
            'Name': track.title,
            'Artist': track.artist,
            'Album': track.album,
            'Genre': track.genre,
            'TotalTime': str(int(track.duration)),
            'Location': self._format_location(track.file_path),
            'Rating': str(track.rating),
            'Tonality': track.key,
            'AverageBpm': str(track.bpm),
            'DateAdded': datetime.now().strftime('%Y-%m-%d')
        })
        
        # Add cue points
        self._add_cue_points_to_track(track, track_elem, options)
        
    def _format_location(self, file_path: str) -> str:
        """Format a file path for Rekordbox XML"""
        # Convert to URI format
        if os.name == 'nt':  # Windows
            # Handle Windows paths
            if file_path.startswith('\\\\'):  # UNC path
                return 'file:///' + file_path.replace('\\', '/')
            else:
                return 'file:///' + file_path.replace('\\', '/').lstrip('/')
        else:  # Unix/Mac
            return 'file://' + file_path
    
    def _add_cue_points_to_track(self, track: Track, track_elem: ET.Element, options: Dict[str, Any]):
        """Add cue points to a track element"""
        convert_hot_cues = options.get('convert_hot_cues_to_memory_cues', False)
        
        for cue in track.cue_points:
            cue_type = 0  # Memory cue
            if cue.type == CueType.HOT_CUE and not convert_hot_cues:
                cue_type = 1  # Hot cue
            
            position_ms = int(cue.position * 1000)  # Convert to milliseconds
            
            # Create cue point element
            cue_elem = ET.SubElement(track_elem, 'POSITION_MARK', {
                'Name': cue.name,
                'Type': str(cue_type),
                'Start': str(position_ms),
                'Num': str(cue.index if cue.index >= 0 else 0)
            })
        
        # Add loops
        for loop in track.loops:
            start_ms = int(loop.start_position * 1000)  # Convert to milliseconds
            end_ms = int(loop.end_position * 1000)  # Convert to milliseconds
            
            # Create loop element
            loop_elem = ET.SubElement(track_elem, 'POSITION_MARK', {
                'Name': loop.name,
                'Type': '2',  # Loop
                'Start': str(start_ms),
                'End': str(end_ms),
                'Num': str(loop.index if loop.index >= 0 else 0)
            })
    
    def _add_playlist_to_node(self, playlist: Playlist, parent_node: ET.Element, collection: Collection, options: Dict[str, Any]):
        """Add a playlist to a node element recursively"""
        # Check if this is a folder or a regular playlist
        if playlist.children:
            # This is a folder
            folder_node = ET.SubElement(parent_node, 'NODE', {
                'Type': '0',  # Folder
                'Name': playlist.name,
                'Count': str(len(playlist.children))
            })
            
            # Add child playlists
            for child in playlist.children:
                self._add_playlist_to_node(child, folder_node, collection, options)
        else:
            # This is a regular playlist
            playlist_node = ET.SubElement(parent_node, 'NODE', {
                'Type': '1',  # Playlist
                'Name': playlist.name,
                'KeyType': '0',
                'Entries': str(len(playlist.track_ids))
            })
            
            # Add tracks to playlist
            for track_id in playlist.track_ids:
                track = collection.get_track(track_id)
                if track:
                    ET.SubElement(playlist_node, 'TRACK', {
                        'Key': str(track_id).replace('-', '')
                    })
