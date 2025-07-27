"""
Main application entry point.
Refactored using multiple design patterns:
- Singleton (Config)
- Strategy (Export strategies)
- Template Method (UI)
- Facade (GameController)
- Factory (ExportStrategyFactory)
"""
import sys
import os
import traceback

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers import GameController
from ui import ConsoleUI
from config import ConfigError


def main():
    """Main application entry point"""
    try:
        # Initialize controller (Facade pattern)
        controller = GameController()

        # Initialize UI (Template Method pattern)
        ui = ConsoleUI(controller)

        # Run application
        ui.run()

    except ConfigError as e:
        print(f"\n❌ Errore di configurazione: {e}")
        print("Assicurati di avere un file .env con RAWG_API_KEY")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Uscita forzata. Arrivederci!")
    except Exception as e:
        print(f"\n❌ Errore imprevisto: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
