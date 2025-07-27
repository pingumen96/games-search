"""
Export manager using Strategy pattern.
"""
import os
from typing import List
from models import Game
from .strategies import ExportStrategyFactory, ExportError


class ExportManager:
    """Manages game data export using different strategies"""

    def __init__(self):
        self.factory = ExportStrategyFactory()

    def get_available_formats(self) -> List[str]:
        """Get list of available export formats"""
        return self.factory.get_available_formats()

    def export_games(self, games: List[Game], format_name: str, filename: str) -> str:
        """Export games using specified format"""
        if not games:
            raise ExportError("❌ Nessun dato da esportare!")

        try:
            strategy = self.factory.create_strategy(format_name)
            filepath = f"{filename}{strategy.extension}"

            strategy.export(games, filepath)

            return os.path.abspath(filepath)

        except ExportError:
            raise
        except Exception as e:
            raise ExportError(f"❌ Errore durante l'esportazione: {e}") from e
