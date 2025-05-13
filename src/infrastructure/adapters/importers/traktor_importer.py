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

            # Get file path components
            volume = location.get('VOLUME', '')
            dir_path = location.get('DIR', '')
            file_name = location.get('FILE', '')

            # Traktor uses a special path format with '/:', normalize it
            # Format the path in Traktor's format for consistency with playlist entries
            if dir_path.startswith('/:'):
                dir_path = dir_path[2:]  # Remove leading '/:'
            dir_parts = dir_path.split('/:')  # Split on '/:'
            dir_path = '/'.join(dir_parts)  # Join with normal slashes

            # Create the file path
            file_path = os.path.join(volume, dir_path, file_name)

            # Also store the original Traktor path format for matching with playlists
            traktor_path = f"{volume}/:" + "/:" .join([*dir_parts, file_name])

            # Get additional track info
            info = entry.find('./INFO')
            album_elem = entry.find('./ALBUM')
            tempo_elem = entry.find('./TEMPO')

            # Extract more metadata if available
            genre = ''
            comment = ''
            duration = 0.0
            rating = 0
            album = ''

            if info is not None:
                genre = info.get('GENRE', '')
                comment = info.get('COMMENT', '')
                duration = float(info.get('PLAYTIME', '0'))
                rating = int(info.get('RANKING', '0'))

            if album_elem is not None:
                album = album_elem.get('TITLE', '')

            bpm = 0.0
            if tempo_elem is not None:
                bpm = float(tempo_elem.get('BPM', '0'))

            # Create track with more complete metadata
            track = Track(
                id=uuid4(),
                title=entry.get('TITLE', ''),
                artist=entry.get('ARTIST', ''),
                album=album,
                genre=genre,
                bpm=bpm,
                key=entry.get('KEY', ''),
                file_path=file_path,
                comment=comment,
                duration=duration,
                rating=rating
            )

            # Store the Traktor path in custom tags for matching with playlists
            track.add_custom_tag('traktor_path', traktor_path)

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

        # Find all root nodes (could be folders or playlists)
        root_nodes = playlists_node.findall('./NODE')
        if not root_nodes:
            return

        # Process all playlists recursively
        for node in root_nodes:
            self._process_playlist_node(node, None, collection)

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

            # Process child nodes (SUBNODES in Traktor)
            subnodes = node.find('./SUBNODES')
            if subnodes is not None:
                for child in subnodes.findall('./NODE'):
                    self._process_playlist_node(child, playlist_id, collection)
            else:
                # Try direct child nodes as well
                for child in node.findall('./NODE'):
                    self._process_playlist_node(child, playlist_id, collection)

        elif node_type == 'PLAYLIST':
            # Create a playlist
            playlist = Playlist(
                name=node_name,
                parent_id=parent_id
            )
            playlist_id = collection.add_playlist(playlist)

            # Find the PLAYLIST element
            playlist_elem = node.find('./PLAYLIST')
            if playlist_elem is None:
                return

            # Add tracks to the playlist
            for entry in playlist_elem.findall('./ENTRY'):
                location = entry.find('./PRIMARYKEY')
                if location is not None:
                    # Get the track key (full path in Traktor format)
                    track_key = location.get('KEY', '')
                    if not track_key:
                        continue

                    # Convert Traktor path format to standard path
                    # Format is typically: "Volume/:dir1/:dir2/:filename"
                    parts = track_key.split('/:')  # Split on '/:'
                    if len(parts) < 2:
                        continue

                    volume = parts[0]
                    file_name = parts[-1]  # Last part is the filename
                    dir_path = '/'.join(parts[1:-1])  # Middle parts form the directory path

                    # Reconstruct the file path in a format matching our tracks
                    file_path = os.path.join(volume, dir_path, file_name)

                    # Try to find the track in the collection using multiple methods
                    track = None

                    # Method 1: Try to match using the stored Traktor path
                    for t in collection.tracks.values():
                        if 'traktor_path' in t.custom_tags and t.custom_tags['traktor_path'] == track_key:
                            track = t
                            break

                    # Method 2: If not found, try matching by filename (less precise but more robust)
                    if track is None:
                        for t in collection.tracks.values():
                            # Compare the end parts of the paths (most unique part)
                            if t.file_path.endswith(file_name):
                                track = t
                                break

                    if track:
                        playlist = collection.get_playlist(playlist_id)
                        if playlist:
                            playlist.add_track(track.id)
