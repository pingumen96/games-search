#!/usr/bin/env python3
"""Test completo per le funzionalità AI integrate"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_ai_integration():
    """Test delle funzionalità AI integrate"""

    print("🧪 Test integrazione AI completa...")

    try:
        from main import GamesDB, OPENAI_AVAILABLE

        print(f"📦 OpenAI disponibile: {OPENAI_AVAILABLE}")

        # Test senza inizializzazione completa
        db = GamesDB.__new__(GamesDB)

        # Setup minimale
        from dotenv import load_dotenv
        load_dotenv()

        db.api_key = os.getenv("RAWG_API_KEY", "demo_key")
        db.openai_key = os.getenv("OPENAI_API_KEY")
        db.openai_client = None
        db.games_data = []
        db.current_games = []

        # Test configurazione OpenAI
        if db.openai_key and OPENAI_AVAILABLE:
            try:
                from openai import OpenAI
                db.openai_client = OpenAI(api_key=db.openai_key)
                print("✅ OpenAI configurato correttamente")
            except Exception as e:
                print(f"❌ Errore configurazione OpenAI: {e}")
                db.openai_client = None
        else:
            print("ℹ️ OpenAI non configurato (normale se non hai la API key)")

        # Test ask_ai_reviews
        print("🤖 Test ask_ai_reviews...")
        ai_available = db.openai_client is not None
        print(f"   Recensioni AI disponibili: {ai_available}")

        # Test generate_ai_review (solo se configurato)
        if db.openai_client:
            print("🤖 Test generazione recensione...")
            review, rating = db.generate_ai_review(
                "Tetris", "Puzzle", "Game Boy", "1989-06-06"
            )
            if review:
                print(f"   ✅ Recensione: {review[:50]}...")
                print(f"   ✅ Voto: {rating}/10")
            else:
                print("   ⚠️ Recensione non generata")

        # Test dati con AI
        test_games_ai = [
            {
                "Title": "Super Mario Bros",
                "Platforms": "NES, Switch",
                "Release Date": "1985-09-13",
                "Genres": "Platform, Adventure",
                "AI Review": "Un capolavoro del platform che ha definito il genere.",
                "AI Rating": "9/10"
            }
        ]

        test_games_no_ai = [
            {
                "Title": "Super Mario Bros",
                "Platforms": "NES, Switch",
                "Release Date": "1985-09-13",
                "Genres": "Platform, Adventure"
            }
        ]

        # Test esportazioni
        print("📁 Test esportazioni con AI...")

        try:
            db._export_csv(test_games_ai, "test_ai.csv")
            print("   ✅ CSV con AI esportato")
        except Exception as e:
            print(f"   ❌ Errore CSV: {e}")

        try:
            db._export_markdown(test_games_ai, "test_ai.md")
            print("   ✅ Markdown con AI esportato")
        except Exception as e:
            print(f"   ❌ Errore Markdown: {e}")

        try:
            db._export_xml(test_games_ai, "test_ai.xml")
            print("   ✅ XML con AI esportato")
        except Exception as e:
            print(f"   ❌ Errore XML: {e}")

        # Test senza AI
        print("📁 Test esportazioni senza AI...")

        try:
            db._export_csv(test_games_no_ai, "test_no_ai.csv")
            print("   ✅ CSV senza AI esportato")
        except Exception as e:
            print(f"   ❌ Errore CSV: {e}")

        print("\n🎉 Test completato!")

        # Mostra files creati
        print("\n📁 File di test creati:")
        for filename in ['test_ai.csv', 'test_ai.md', 'test_ai.xml', 'test_no_ai.csv']:
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"   - {filename} ({size} bytes)")

        # Cleanup
        print("\n🧹 Pulizia file di test...")
        for filename in ['test_ai.csv', 'test_ai.md', 'test_ai.xml', 'test_no_ai.csv']:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"   ✅ Rimosso {filename}")
            except:
                pass

    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_integration()
