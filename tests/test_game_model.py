"""
Unit tests for the Game model.
"""
import unittest
from models import Game


class TestGame(unittest.TestCase):
    """Test cases for Game model"""

    def setUp(self):
        """Set up test data"""
        self.game = Game(
            title="Test Game",
            platforms=["PC", "PlayStation 5"],
            release_date="2023-01-15",
            genres=["Action", "Adventure"],
            ai_review="Great game with amazing graphics",
            ai_rating=8
        )

    def test_platforms_str(self):
        """Test platforms string representation"""
        expected = "PC, PlayStation 5"
        self.assertEqual(self.game.platforms_str, expected)

    def test_genres_str(self):
        """Test genres string representation"""
        expected = "Action, Adventure"
        self.assertEqual(self.game.genres_str, expected)

    def test_ai_rating_str(self):
        """Test AI rating string representation"""
        expected = "8/10"
        self.assertEqual(self.game.ai_rating_str, expected)

    def test_ai_rating_str_no_rating(self):
        """Test AI rating string when rating is None"""
        game = Game(
            title="Test",
            platforms=["PC"],
            release_date=None,
            genres=["Action"]
        )
        self.assertEqual(game.ai_rating_str, "N/A")

    def test_to_dict_without_ai(self):
        """Test dictionary conversion without AI data"""
        game = Game(
            title="Test Game",
            platforms=["PC"],
            release_date="2023-01-15",
            genres=["Action"]
        )
        expected = {
            "Title": "Test Game",
            "Platforms": "PC",
            "Release Date": "2023-01-15",
            "Genres": "Action"
        }
        self.assertEqual(game.to_dict(), expected)

    def test_to_dict_with_ai(self):
        """Test dictionary conversion with AI data"""
        expected = {
            "Title": "Test Game",
            "Platforms": "PC, PlayStation 5",
            "Release Date": "2023-01-15",
            "Genres": "Action, Adventure",
            "AI Review": "Great game with amazing graphics",
            "AI Rating": "8/10"
        }
        result = self.game.to_dict()
        self.assertEqual(result, expected)

    def test_matches_platform_filter_no_filter(self):
        """Test platform matching with no filter"""
        self.assertTrue(self.game.matches_platform_filter(None))
        self.assertTrue(self.game.matches_platform_filter([]))

    def test_matches_platform_filter_match(self):
        """Test platform matching with matching filter"""
        filter_platforms = ["PC", "Xbox"]
        self.assertTrue(self.game.matches_platform_filter(filter_platforms))

    def test_matches_platform_filter_no_match(self):
        """Test platform matching with non-matching filter"""
        filter_platforms = ["Xbox", "Nintendo Switch"]
        self.assertFalse(self.game.matches_platform_filter(filter_platforms))

    def test_matches_platform_filter_case_insensitive(self):
        """Test platform matching is case insensitive"""
        filter_platforms = ["pc"]
        self.assertTrue(self.game.matches_platform_filter(filter_platforms))


if __name__ == '__main__':
    unittest.main()
