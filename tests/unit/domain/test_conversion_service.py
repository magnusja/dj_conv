"""
Unit tests for the ConversionService
"""
import unittest
from uuid import uuid4

from src.domain.entities.collection import Collection
from src.domain.entities.track import Track
from src.domain.entities.cue_point import CuePoint, CueType
from src.domain.services.conversion_service import ConversionService


class TestConversionService(unittest.TestCase):
    """Test cases for the ConversionService"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.conversion_service = ConversionService()
        
        # Create a test collection
        self.collection = Collection(name="Test Collection")
        
        # Create a test track with hot cues
        self.track = Track(
            title="Test Track",
            artist="Test Artist",
            bpm=128.0,
            file_path="/path/to/track.mp3"
        )
        
        # Add hot cues to the track
        self.track.add_cue_point(CuePoint(
            name="Cue 1",
            position=10.0,
            type=CueType.HOT_CUE,
            index=0
        ))
        self.track.add_cue_point(CuePoint(
            name="Cue 2",
            position=20.0,
            type=CueType.HOT_CUE,
            index=1
        ))
        self.track.add_cue_point(CuePoint(
            name="Grid",
            position=0.0,
            type=CueType.GRID_MARKER
        ))
        
        # Add the track to the collection
        self.collection.add_track(self.track)
        
    def test_convert_hot_cues_to_memory_cues(self):
        """Test converting hot cues to memory cues"""
        # Convert hot cues to memory cues
        converted_collection = self.conversion_service.convert_hot_cues_to_memory_cues(self.collection)
        
        # Get the converted track
        converted_track = next(iter(converted_collection.tracks.values()))
        
        # Check that hot cues were converted to memory cues
        for cue in converted_track.cue_points:
            if cue.name in ["Cue 1", "Cue 2"]:
                self.assertEqual(cue.type, CueType.MEMORY_CUE)
            elif cue.name == "Grid":
                self.assertEqual(cue.type, CueType.GRID_MARKER)
                
    def test_merge_collections(self):
        """Test merging collections"""
        # Create a second collection
        collection2 = Collection(name="Second Collection")
        
        # Create a track for the second collection
        track2 = Track(
            title="Second Track",
            artist="Second Artist",
            bpm=140.0,
            file_path="/path/to/second_track.mp3"
        )
        
        # Add the track to the second collection
        collection2.add_track(track2)
        
        # Merge the collections
        merged_collection = self.conversion_service.merge_collections(collection2, self.collection)
        
        # Check that the merged collection has both tracks
        self.assertEqual(len(merged_collection.tracks), 2)
        
        # Check that the tracks have the correct titles
        track_titles = [track.title for track in merged_collection.tracks.values()]
        self.assertIn("Test Track", track_titles)
        self.assertIn("Second Track", track_titles)


if __name__ == "__main__":
    unittest.main()
