"""
RAWG API service implementation.
"""
import calendar
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

        games = []
        page_size = 40
        max_pages = 4

        for page in range(1, max_pages + 1):
            print(f"  📄 Caricando pagina {page}/{max_pages}...")

            url = f"{self.base_url}?dates={start_date},{end_date}&page_size={page_size}&page={page}&key={self.api_key}&ordering=-rating"

            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as e:
                raise APIServiceError(f"Errore nella richiesta API: {e}")

            # Check if there are results in this page
            results = data.get('results', [])
            if not results:
                print(f"  ⚠️  Nessun risultato nella pagina {page}, interrompendo la ricerca")
                break

            page_games = []
            for game_data in results:
                game = self._parse_game_data(game_data)

                # Apply platform filter
                if game.matches_platform_filter(platform_filter):
                    page_games.append(game)

            games.extend(page_games)
            print(f"  ✅ Trovati {len(page_games)} giochi validi nella pagina {page}")

            # Check if this is the last page based on API response
            if not data.get('next'):
                print(f"  🏁 Raggiunta l'ultima pagina disponibile ({page})")
                break

        print(f"🎮 Totale giochi trovati: {len(games)}")
        return games

    def _build_date_range(self, year: int, month: int) -> tuple[str, str]:
        """Build date range for API query"""

        start_date = f"{year}-{month:02d}-01"

        # Get the last day of the specified month
        last_day = calendar.monthrange(year, month)[1]
        end_date = f"{year}-{month:02d}-{last_day}"

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
