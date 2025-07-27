"""
RAWG API service implementation.
"""
import requests
from typing import List, Optional
from models import Game
from .base import GameAPIService, APIServiceError


class RAWGService(GameAPIService):
    """RAWG API service implementation"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.rawg.io/api/games"

    def fetch_games(self, year: int, month: int, platform_filter: Optional[List[str]] = None) -> List[Game]:
        """Fetch games from RAWG API"""
        start_date, end_date = self._build_date_range(year, month)

        print(f"\n🔍 Cercando giochi rilasciati nel {month}/{year}...")

        url = f"{self.base_url}?dates={start_date},{end_date}&page_size=100&key={self.api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise APIServiceError(f"Errore nella richiesta API: {e}")

        games = []
        for game_data in data.get('results', []):
            game = self._parse_game_data(game_data)

            # Apply platform filter
            if game.matches_platform_filter(platform_filter):
                games.append(game)

        return games

    def _build_date_range(self, year: int, month: int) -> tuple[str, str]:
        """Build date range for API query"""
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        return start_date, end_date

    def _parse_game_data(self, game_data: dict) -> Game:
        """Parse raw game data into Game model"""
        title = game_data.get('name', '')
        release_date = game_data.get('released')

        platforms_data = game_data.get('platforms', [])
        if not isinstance(platforms_data, list):
            platforms_data = []
        platforms = [p['platform']['name'] for p in platforms_data]

        genres = [g['name'] for g in game_data.get('genres', [])]

        return Game(
            title=title,
            platforms=platforms,
            release_date=release_date,
            genres=genres
        )
