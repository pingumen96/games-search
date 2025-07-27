#!/usr/bin/env python3
"""Test script per verificare le funzioni di recensione AI"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from main import GamesDB

def test_ai_review():
    """Test della funzione di recensione AI"""

    print("🧪 Test della funzione di recensione AI...")

    try:
        # Crea un'istanza della classe senza chiamare __init__ completo
        db = GamesDB.__new__(GamesDB)

        # Setup minimo per il test
        from dotenv import load_dotenv
        load_dotenv()

        db.openai_key = os.getenv("OPENAI_API_KEY")
        db.openai_client = None

        if db.openai_key:
            try:
                from openai import OpenAI
                db.openai_client = OpenAI(api_key=db.openai_key)
                print("✅ OpenAI client configurato")
            except Exception as e:
                print(f"❌ Errore configurazione OpenAI: {e}")
                return
        else:
            print("❌ OPENAI_API_KEY non trovata nel .env")
            return

        # Test con un gioco di esempio
        test_title = "Super Mario Bros"
        test_genres = "Platform, Adventure"
        test_platforms = "NES, Switch"
        test_date = "1985-09-13"

        print(f"🤖 Generando recensione per: {test_title}")

        review, rating = db.generate_ai_review(
            test_title, test_genres, test_platforms, test_date
        )

        if review and rating:
            print(f"✅ Recensione generata:")
            print(f"   📝 Recensione: {review}")
            print(f"   ⭐ Voto: {rating}/10")
        else:
            print("❌ Errore nella generazione della recensione")

    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_review()
