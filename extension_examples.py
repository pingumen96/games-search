"""
Example of how to extend the refactored code with new features.
Demonstrates the extensibility benefits of the refactoring.
"""
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Game
from exporters.strategies import ExportStrategy
from services.base import AIReviewService
from typing import List, Optional, Tuple
import json


# Example 1: Adding a new export format (JSON)
class JSONExportStrategy(ExportStrategy):
    """JSON export strategy - demonstrates extensibility"""

    @property
    def extension(self) -> str:
        return ".json"

    @property
    def is_available(self) -> bool:
        return True  # JSON is always available

    def export(self, games: List[Game], filepath: str) -> None:
        """Export games to JSON file"""
        if not games:
            raise Exception("No games to export")

        # Convert games to JSON-serializable format
        games_data = {
            "metadata": {
                "total_games": len(games),
                "export_format": "JSON",
                "has_ai_reviews": any(game.ai_review is not None for game in games)
            },
            "games": [game.to_dict() for game in games]
        }

        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(games_data, jsonfile, indent=2, ensure_ascii=False)


# Example 2: Adding a new AI service (Mock service for demonstration)
class MockAIReviewService(AIReviewService):
    """Mock AI service - demonstrates how to add new AI providers"""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def is_available(self) -> bool:
        return self.enabled

    def generate_review(self, game: Game) -> Tuple[Optional[str], Optional[int]]:
        """Generate a mock review based on game genres"""
        if not self.enabled:
            return None, None

        # Simple logic based on genres
        genre_ratings = {
            "Action": (8, "Emozionante gioco d'azione con combattimenti dinamici."),
            "Adventure": (7, "Avventura coinvolgente con una trama interessante."),
            "RPG": (9, "Gioco di ruolo profondo con progressione del personaggio."),
            "Strategy": (6, "Strategia che richiede pianificazione e tattica."),
            "Sports": (5, "Simulazione sportiva realistica e divertente."),
            "Racing": (7, "Corse adrenaliniche con buona fisica di guida.")
        }

        # Find the first matching genre
        for genre in game.genres:
            if genre in genre_ratings:
                rating, review = genre_ratings[genre]
                return f"{review} Ottimo per gli amanti del genere {genre}.", rating

        # Default fallback
        return "Gioco interessante con meccaniche solid.", 6


# Example 3: Extending the Game model with validation
class ValidatedGame(Game):
    """Extended Game model with validation - demonstrates model extensibility"""

    def __post_init__(self):
        """Validate game data after initialization"""
        if not self.title or not self.title.strip():
            raise ValueError("Game title cannot be empty")

        if self.ai_rating is not None and not (1 <= self.ai_rating <= 10):
            raise ValueError("AI rating must be between 1 and 10")

        if self.release_date:
            # Basic date format validation
            import re
            if not re.match(r'\d{4}-\d{2}-\d{2}', self.release_date):
                raise ValueError("Release date must be in YYYY-MM-DD format")

    @property
    def release_year(self) -> Optional[int]:
        """Extract release year from date"""
        if self.release_date:
            try:
                return int(self.release_date.split('-')[0])
            except (ValueError, IndexError):
                return None
        return None


# Example 4: Custom export manager with additional features
class AdvancedExportManager:
    """Advanced export manager with additional features"""

    def __init__(self):
        from exporters import ExportStrategyFactory
        self.factory = ExportStrategyFactory()

        # Add our custom JSON strategy to the factory
        self.factory._strategies["JSON"] = JSONExportStrategy

    def export_with_filtering(self, games: List[Game], format_name: str,
                            filename: str, min_rating: Optional[int] = None) -> str:
        """Export games with optional rating filtering"""
        # Filter games by rating if specified
        if min_rating is not None:
            filtered_games = [
                game for game in games
                if game.ai_rating is not None and game.ai_rating >= min_rating
            ]
        else:
            filtered_games = games

        if not filtered_games:
            raise Exception("No games match the filtering criteria")

        # Use the standard export logic
        strategy = self.factory.create_strategy(format_name)
        filepath = f"{filename}{strategy.extension}"
        strategy.export(filtered_games, filepath)

        return os.path.abspath(filepath)


def demonstrate_extensions():
    """Demonstrate the new extensions"""
    print("🚀 Demonstrating code extensions...")

    # Create some sample games
    games = [
        Game(
            title="Super Action Game",
            platforms=["PC", "PlayStation 5"],
            release_date="2023-01-15",
            genres=["Action", "Adventure"],
            ai_review="Amazing action game",
            ai_rating=8
        ),
        Game(
            title="Strategy Master",
            platforms=["PC"],
            release_date="2023-03-10",
            genres=["Strategy"],
            ai_review="Complex strategy game",
            ai_rating=6
        )
    ]

    # Demonstrate JSON export
    print("\n📄 Testing JSON Export Strategy...")
    json_strategy = JSONExportStrategy()
    json_strategy.export(games, "demo_export.json")
    print("✅ JSON export completed: demo_export.json")

    # Demonstrate Mock AI Service
    print("\n🤖 Testing Mock AI Service...")
    mock_ai = MockAIReviewService()
    for game in games:
        review, rating = mock_ai.generate_review(game)
        print(f"Game: {game.title}")
        print(f"Mock Review: {review}")
        print(f"Mock Rating: {rating}/10\n")

    # Demonstrate Advanced Export Manager
    print("\n📊 Testing Advanced Export Manager...")
    advanced_manager = AdvancedExportManager()
    try:
        filepath = advanced_manager.export_with_filtering(
            games, "JSON", "filtered_games", min_rating=7
        )
        print(f"✅ Filtered export completed: {filepath}")
    except Exception as e:
        print(f"Error in advanced export: {e}")

    # Cleanup
    for filename in ["demo_export.json", "filtered_games.json"]:
        if os.path.exists(filename):
            os.unlink(filename)
            print(f"🗑️ Cleaned up: {filename}")


if __name__ == "__main__":
    demonstrate_extensions()
