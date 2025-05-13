"""
Unit tests for the Track entity
"""
import unittest
from uuid import UUID

from src.domain.entities.track import Track
from src.domain.entities.cue_point import CuePoint, CueType
from src.domain.entities.loop import Loop, LoopType


class TestTrack(unittest.TestCase):
    """Test cases for the Track entity"""
    
    def test_track_creation(self):
        """Test creating a track"""
        track = Track(
            title="Test Track",
            artist="Test Artist",
            album="Test Album",
            genre="Test Genre",
            bpm=128.0,
            key="C",
            duration=180.0,
            file_path="/path/to/track.mp3"
        )
        
        self.assertEqual(track.title, "Test Track")
        self.assertEqual(track.artist, "Test Artist")
        self.assertEqual(track.album, "Test Album")
        self.assertEqual(track.genre, "Test Genre")
        self.assertEqual(track.bpm, 128.0)
        self.assertEqual(track.key, "C")
        self.assertEqual(track.duration, 180.0)
        self.assertEqual(track.file_path, "/path/to/track.mp3")
        self.assertIsInstance(track.id, UUID)
        
    def test_add_cue_point(self):
        """Test adding a cue point to a track"""
        track = Track(title="Test Track")
        cue = CuePoint(name="Test Cue", position=10.0, type=CueType.HOT_CUE, index=1)
        
        track.add_cue_point(cue)
        
        self.assertEqual(len(track.cue_points), 1)
        self.assertEqual(track.cue_points[0].name, "Test Cue")
        self.assertEqual(track.cue_points[0].position, 10.0)
        self.assertEqual(track.cue_points[0].type, CueType.HOT_CUE)
        self.assertEqual(track.cue_points[0].index, 1)
        
    def test_add_loop(self):
        """Test adding a loop to a track"""
        track = Track(title="Test Track")
        loop = Loop(name="Test Loop", start_position=10.0, end_position=20.0, type=LoopType.REGULAR)
        
        track.add_loop(loop)
        
        self.assertEqual(len(track.loops), 1)
        self.assertEqual(track.loops[0].name, "Test Loop")
        self.assertEqual(track.loops[0].start_position, 10.0)
        self.assertEqual(track.loops[0].end_position, 20.0)
        self.assertEqual(track.loops[0].type, LoopType.REGULAR)
        
    def test_add_custom_tag(self):
        """Test adding a custom tag to a track"""
        track = Track(title="Test Track")
        
        track.add_custom_tag("energy", "high")
        
        self.assertEqual(len(track.custom_tags), 1)
        self.assertEqual(track.custom_tags["energy"], "high")


if __name__ == "__main__":
    unittest.main()
