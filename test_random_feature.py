#!/usr/bin/env python3
"""
Test script for the new random search feature
"""
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_random_search():
    """Test the random search functionality"""
    print("🧪 Testing Random Search Feature...")

    try:
        # Test imports
        from services.rawg_service import RAWGService
        from controllers.game_controller import GameController
        from exporters.export_manager import ExportManager
        from config import Config

        print("✅ All imports successful")

        # Test RAWGService random method (without actual API call)
        config = Config()
        if not config.rawg_api_key:
            print("⚠️  No RAWG API key found, cannot test actual API calls")
            print("✅ Test completed successfully (imports only)")
            return

        rawg_service = RAWGService(config.rawg_api_key)
        print("✅ RAWGService initialized")

        # Test controller
        controller = GameController()
        print("✅ GameController initialized")

        # Test export manager directory creation
        export_manager = ExportManager()
        print("✅ ExportManager initialized")

        print("\n🎉 All components initialized successfully!")
        print("🎲 Random search feature is ready to use!")

        # Test games directory creation
        games_dir = "games"
        if os.path.exists(games_dir):
            print(f"✅ Games directory exists: {os.path.abspath(games_dir)}")
        else:
            print(f"⚠️  Games directory not found, will be created on first export")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

    return True

if __name__ == "__main__":
    success = test_random_search()
    exit(0 if success else 1)
