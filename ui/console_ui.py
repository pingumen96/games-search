"""
User interface layer using Template Method pattern.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
import questionary
from tabulate import tabulate
from models import Game


class UIError(Exception):
    """UI error exception"""


class BaseUI(ABC):
    """Abstract base class for user interfaces"""

    def run(self):
        """Template method for running the UI"""
        try:
            self.initialize()
            while True:
                if not self.show_menu():
                    break
        except KeyboardInterrupt:
            self.handle_keyboard_interrupt()
        except Exception as e:
            self.handle_error(e)
        finally:
            self.cleanup()

    @abstractmethod
    def initialize(self):
        """Initialize the UI"""
        pass

    @abstractmethod
    def show_menu(self) -> bool:
        """Show menu and handle user choice. Return False to exit."""
        pass

    def handle_keyboard_interrupt(self):
        """Handle keyboard interrupt (Ctrl+C)"""
        print("\n\n👋 Uscita forzata. Arrivederci!")

    def handle_error(self, error: Exception):
        """Handle unexpected errors"""
        print(f"\n❌ Errore imprevisto: {error}")

    def cleanup(self):
        """Cleanup resources"""
        pass


class ConsoleUI(BaseUI):
    """Console-based user interface"""

    def __init__(self, game_controller):
        self.game_controller = game_controller

    def initialize(self):
        """Initialize console UI"""
        print("\n🎮 === GAMES DATABASE ===")

    def show_menu(self) -> bool:
        """Show main menu"""
        print("\n" + "="*50)
        print("🎮 GAMES DATABASE - Menu Principale")
        print("="*50)

        choice = questionary.select(
            "Scegli un'azione:",
            choices=[
                "🔍 Cerca giochi per data",
                "🎲 Cerca giochi casuali",
                "📊 Mostra ultimi risultati",
                "📁 Esporta ultimi risultati",
                "❌ Esci"
            ]
        ).ask()

        if choice == "🔍 Cerca giochi per data":
            self._handle_search_games()
        elif choice == "🎲 Cerca giochi casuali":
            self._handle_random_search()
        elif choice == "📊 Mostra ultimi risultati":
            self._handle_show_results()
        elif choice == "📁 Esporta ultimi risultati":
            self._handle_export_results()
        elif choice == "❌ Esci":
            print("\n👋 Arrivederci!")
            return False

        return True

    def _handle_search_games(self):
        """Handle game search workflow"""
        print("\n🎮 === RICERCA GIOCHI ===")

        # Get search parameters
        year = self._get_year_input()
        month = self._get_month_input()
        platform_filter = self._get_platform_filter()
        include_ai_reviews = self._ask_ai_reviews()

        # Search and display
        games = self.game_controller.search_games(year, month, platform_filter, include_ai_reviews)
        self._display_games(games)

        # Offer export
        if games:
            self._offer_export(games)

    def _handle_random_search(self):
        """Handle random game search workflow"""
        print("\n🎲 === RICERCA GIOCHI CASUALI ===")

        # Get year range
        min_year = self._get_min_year_input()
        max_year = self._get_max_year_input(min_year)
        platform_filter = self._get_platform_filter()
        include_ai_reviews = self._ask_ai_reviews()

        # Search and display
        games, random_year, random_month = self.game_controller.search_random_games(
            min_year, max_year, platform_filter, include_ai_reviews
        )

        print(f"\n🎯 Periodo selezionato: {random_month}/{random_year}")
        self._display_games(games)

        # Offer export
        if games:
            self._offer_export(games)

    def _handle_show_results(self):
        """Handle showing last results"""
        games = self.game_controller.get_last_results()
        if games:
            self._display_games(games)
        else:
            print("\n❌ Nessun risultato precedente disponibile. Effettua prima una ricerca!")

    def _handle_export_results(self):
        """Handle exporting last results"""
        games = self.game_controller.get_last_results()
        if games:
            self._offer_export(games)
        else:
            print("\n❌ Nessun dato da esportare! Effettua prima una ricerca.")

    def _get_year_input(self) -> int:
        """Get year input with validation"""
        current_year = datetime.now().year

        while True:
            year_input = questionary.text(
                f"Inserisci anno (1970-{current_year}) o premi Invio per anno corrente ({current_year}):"
            ).ask()

            if not year_input:
                return current_year

            try:
                year = int(year_input)
                if 1970 <= year <= current_year:
                    return year
                else:
                    print(f"Errore: L'anno deve essere tra 1970 e {current_year}")
            except ValueError:
                print("Errore: Inserisci un numero valido")

    def _get_month_input(self) -> int:
        """Get month input with validation"""
        current_month = datetime.now().month

        while True:
            month_input = questionary.text(
                f"Inserisci mese (1-12) o premi Invio per mese corrente ({current_month}):"
            ).ask()

            if not month_input:
                return current_month

            try:
                month = int(month_input)
                if 1 <= month <= 12:
                    return month
                else:
                    print("Errore: Il mese deve essere tra 1 e 12")
            except ValueError:
                print("Errore: Inserisci un numero valido")

    def _get_min_year_input(self) -> int:
        """Get minimum year input for random search"""
        current_year = datetime.now().year

        while True:
            year_input = questionary.text(
                f"Inserisci anno minimo (1970-{current_year}) o premi Invio per 1970:"
            ).ask()

            if not year_input:
                return 1970

            try:
                year = int(year_input)
                if 1970 <= year <= current_year:
                    return year
                else:
                    print(f"Errore: L'anno deve essere tra 1970 e {current_year}")
            except ValueError:
                print("Errore: Inserisci un numero valido")

    def _get_max_year_input(self, min_year: int) -> int:
        """Get maximum year input for random search"""
        current_year = datetime.now().year

        while True:
            year_input = questionary.text(
                f"Inserisci anno massimo ({min_year}-{current_year}) o premi Invio per anno corrente ({current_year}):"
            ).ask()

            if not year_input:
                return current_year

            try:
                year = int(year_input)
                if min_year <= year <= current_year:
                    return year
                else:
                    print(f"Errore: L'anno deve essere tra {min_year} e {current_year}")
            except ValueError:
                print("Errore: Inserisci un numero valido")

    def _get_platform_filter(self) -> Optional[List[str]]:
        """Get platform filter from user"""
        common_platforms = [
            "PC", "PlayStation", "Xbox", "Nintendo Switch", "iOS", "Android",
            "NES", "SNES", "Game Boy", "Arcade", "Atari", "Sega Genesis"
        ]

        choice = questionary.select(
            "Vuoi filtrare per piattaforme?",
            choices=[
                "No, mostra tutte le piattaforme",
                "Sì, scegli da lista comuni",
                "Sì, inserimento manuale"
            ]
        ).ask()

        if choice == "No, mostra tutte le piattaforme":
            return None
        elif choice == "Sì, scegli da lista comuni":
            selected = questionary.checkbox(
                "Seleziona le piattaforme (spazio per selezionare, Invio per confermare):",
                choices=common_platforms
            ).ask()
            return selected if selected else None
        else:
            manual_input = questionary.text(
                "Inserisci piattaforme separate da virgola (es: NES, SNES, Game Boy):"
            ).ask()
            if manual_input:
                return [p.strip() for p in manual_input.split(',')]
            return None

    def _ask_ai_reviews(self) -> bool:
        """Ask if user wants AI reviews"""
        if not self.game_controller.is_ai_available():
            return False

        return questionary.confirm(
            "🤖 Vuoi generare recensioni AI per i giochi trovati? (può richiedere tempo)"
        ).ask()

    def _display_games(self, games: List[Game]):
        """Display games in a table"""
        if not games:
            print("\n❌ Nessun gioco trovato per i criteri specificati.")
            return

        # Ask for sorting
        sorted_games = self._sort_games(games)

        # Check if AI reviews are present
        has_ai_reviews = any(game.ai_review is not None for game in sorted_games)

        # Prepare table
        if has_ai_reviews:
            headers = ["Titolo", "Piattaforme", "Data Rilascio", "Generi", "Recensione AI", "Voto AI"]
            table_data = []
            for game in sorted_games:
                review = game.ai_review or "N/A"
                if len(review) > 50:
                    review = review[:50] + "..."
                table_data.append([
                    game.title,
                    game.platforms_str,
                    game.release_date or "N/A",
                    game.genres_str,
                    review,
                    game.ai_rating_str
                ])
        else:
            headers = ["Titolo", "Piattaforme", "Data Rilascio", "Generi"]
            table_data = []
            for game in sorted_games:
                table_data.append([
                    game.title,
                    game.platforms_str,
                    game.release_date or "N/A",
                    game.genres_str
                ])

        print(f"\n📋 Trovati {len(sorted_games)} giochi:")
        print("=" * 120)
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))

    def _sort_games(self, games: List[Game]) -> List[Game]:
        """Sort games according to user choice"""
        if not games:
            return games

        sort_choice = questionary.select(
            "Come vuoi ordinare i risultati?",
            choices=[
                "Data di rilascio",
                "Titolo (A-Z)",
                "Titolo (Z-A)",
                "Piattaforma",
                "Non ordinare"
            ]
        ).ask()

        if sort_choice == "Data di rilascio":
            return sorted(games, key=lambda x: x.release_date or '9999-12-31')
        elif sort_choice == "Titolo (A-Z)":
            return sorted(games, key=lambda x: x.title.lower())
        elif sort_choice == "Titolo (Z-A)":
            return sorted(games, key=lambda x: x.title.lower(), reverse=True)
        elif sort_choice == "Piattaforma":
            return sorted(games, key=lambda x: x.platforms_str)
        else:
            return games

    def _offer_export(self, games: List[Game]):
        """Offer to export games"""
        export = questionary.confirm("Vuoi esportare i risultati?").ask()
        if export:
            self._handle_export_workflow(games)

    def _handle_export_workflow(self, games: List[Game]):
        """Handle the export workflow"""
        try:
            # Get available formats
            formats = self.game_controller.get_export_formats()

            # Choose format
            format_choice = questionary.select(
                "Scegli il formato di esportazione:",
                choices=formats
            ).ask()

            # Check if format is available
            if "Non disponibile" in format_choice:
                if "XLSX" in format_choice:
                    print("❌ La libreria openpyxl non è installata. Installa con: pip install openpyxl")
                else:
                    print("❌ Formato non disponibile")
                return

            # Generate automatic filename
            filename = self.game_controller.get_automatic_filename()
            print(f"📄 Nome file automatico: {filename}")

            # Export
            filepath = self.game_controller.export_games(games, format_choice)
            print(f"✅ File esportato con successo: {filepath}")

        except Exception as e:
            print(f"❌ Errore durante l'esportazione: {e}")
