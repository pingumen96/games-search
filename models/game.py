"""
Game model with data validation and transformation.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Game:
    """Game data model"""
    title: str
    platforms: List[str]
    release_date: Optional[str]
    genres: List[str]
    ai_review: Optional[str] = None
    ai_rating: Optional[int] = None

    @property
    def platforms_str(self) -> str:
        """Get platforms as comma-separated string"""
        return ", ".join(self.platforms)

    @property
    def genres_str(self) -> str:
        """Get genres as comma-separated string"""
        return ", ".join(self.genres)

    @property
    def ai_rating_str(self) -> str:
        """Get AI rating as formatted string"""
        return f"{self.ai_rating}/10" if self.ai_rating else "N/A"

    def to_dict(self) -> dict:
        """Convert to dictionary for export"""
        result = {
            "Title": self.title,
            "Platforms": self.platforms_str,
            "Release Date": self.release_date or "N/A",
            "Genres": self.genres_str
        }

        if self.ai_review is not None:
            result["AI Review"] = self.ai_review or "N/A"
            result["AI Rating"] = self.ai_rating_str

        return result

    def matches_platform_filter(self, platform_filter: List[str]) -> bool:
        """Check if game matches platform filter"""
        if not platform_filter:
            return True

        return any(
            filter_platform.lower() in platform.lower()
            for platform in self.platforms
            for filter_platform in platform_filter
        )
