"""
Abstract base classes for API services.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from models import Game


class APIServiceError(Exception):
    """API service error exception"""


class GameAPIService(ABC):
    """Abstract base class for game API services"""

    @abstractmethod
    def fetch_games(self, year: int, month: int, platform_filter: Optional[List[str]] = None) -> List[Game]:
        """Fetch games from API"""
        pass


class AIReviewService(ABC):
    """Abstract base class for AI review services"""

    @abstractmethod
    def generate_review(self, game: Game) -> tuple[Optional[str], Optional[int]]:
        """Generate AI review and rating for a game"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if AI service is available"""
        pass
