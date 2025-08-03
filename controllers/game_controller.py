"""
Game controller using Facade pattern to coordinate services.
"""
from typing import List, Optional, Tuple
from models import Game
from services import RAWGService, OpenAIReviewService
from exporters import ExportManager
from config import Config


class GameController:
    """Main controller that coordinates all services (Facade pattern)"""

    def __init__(self):
        # Initialize configuration
        self.config = Config()

        # Initialize services
        self.rawg_service = RAWGService(self.config.rawg_api_key)
        self.ai_service = OpenAIReviewService(self.config.openai_api_key)
        self.export_manager = ExportManager()

        # Store last results
        self._last_results: List[Game] = []
        self._last_search_year: Optional[int] = None
        self._last_search_month: Optional[int] = None

    def search_games(self, year: int, month: int, platform_filter: Optional[List[str]] = None,
                    include_ai_reviews: bool = False) -> List[Game]:
        """Search for games and optionally generate AI reviews"""
        # Fetch games from RAWG API
        games = self.rawg_service.fetch_games(year, month, platform_filter)

        # Generate AI reviews if requested and available
        if include_ai_reviews and self.ai_service.is_available():
            total_games = len(games)
            for i, game in enumerate(games, 1):
                print(f"🤖 Generando recensione AI per '{game.title}' ({i}/{total_games})...")
                review, rating = self.ai_service.generate_review(game)
                game.ai_review = review
                game.ai_rating = rating

        # Store results
        self._last_results = games
        self._last_search_year = year
        self._last_search_month = month
        return games

    def search_random_games(self, min_year: int, max_year: int, platform_filter: Optional[List[str]] = None,
                           include_ai_reviews: bool = False) -> Tuple[List[Game], int, int]:
        """Search for games from a random year and month"""
        # Fetch games from random period
        games, random_year, random_month = self.rawg_service.fetch_random_games(min_year, max_year, platform_filter)

        # Generate AI reviews if requested and available
        if include_ai_reviews and self.ai_service.is_available():
            total_games = len(games)
            for i, game in enumerate(games, 1):
                print(f"🤖 Generando recensione AI per '{game.title}' ({i}/{total_games})...")
                review, rating = self.ai_service.generate_review(game)
                game.ai_review = review
                game.ai_rating = rating

        # Store results
        self._last_results = games
        self._last_search_year = random_year
        self._last_search_month = random_month
        return games, random_year, random_month

    def get_last_results(self) -> List[Game]:
        """Get the last search results"""
        return self._last_results.copy()

    def get_automatic_filename(self) -> str:
        """Generate automatic filename based on last search"""
        if self._last_search_year is not None and self._last_search_month is not None:
            return f"games_results_{self._last_search_year}_{self._last_search_month}"
        else:
            # Fallback to default name if no search has been performed
            return "games_results"

    def is_ai_available(self) -> bool:
        """Check if AI service is available"""
        return self.ai_service.is_available()

    def get_export_formats(self) -> List[str]:
        """Get available export formats"""
        return self.export_manager.get_available_formats()

    def export_games(self, games: List[Game], format_name: str, filename: Optional[str] = None) -> str:
        """Export games to specified format"""
        if filename is None:
            filename = self.get_automatic_filename()
        return self.export_manager.export_games(games, format_name, filename)
