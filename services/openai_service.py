"""
OpenAI service implementation for AI reviews.
Updated for OpenAI Python SDK >= 1.90 (July 2025).

Key updates
-----------
* Uses the `response_format={"type": "json_object"}` parameter so the model
  returns a structured JSON payload we can parse reliably.
* Defaults to the `o4-mini` reasoning model (fast & affordable) but lets callers
  override the model name.
* Falls back gracefully to older parsing strategy if the model ever deviates
  from the expected JSON structure.
* Accepts the API key from the constructor **or** the ``OPENAI_API_KEY`` env var.
* Uses ``logging`` instead of bare ``print`` statements.

This class retains the same public interface as before:
``is_available()`` and ``generate_review(game) -> Tuple[str, Optional[int]]``.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Optional, Tuple

try:
    from openai import OpenAI
    from openai.types.chat import ChatCompletion
    OPENAI_AVAILABLE = True
except ImportError:  # pragma: no cover
    OPENAI_AVAILABLE = False

from models import Game  # domain model
from services.base import AIReviewService

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

DEFAULT_MODEL: str = "gpt-4.1"  # fast, multimodal reasoning model (April 2025)
MAX_TOKENS: int = 400           # JSON output is short; keep a comfortable head‑room
TEMPERATURE: float = 0.7

logger = logging.getLogger(__name__)


class OpenAIReviewService(AIReviewService):
    """
    AIReviewService implementation backed by the OpenAI Chat Completions API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
    ) -> None:
        self.api_key: str | None = api_key or os.getenv("OPENAI_API_KEY")
        self.model: str = model
        self.client: OpenAI | None = None

        if not OPENAI_AVAILABLE:
            logger.warning(
                "⚠️  openai package not installed — AI reviews will be disabled."
            )
            return

        if not self.api_key:
            logger.info(
                "ℹ️  OPENAI_API_KEY not provided — AI reviews will be disabled."
            )
            return

        try:
            self.client = OpenAI(api_key=self.api_key)
            logger.info("🤖 OpenAI configured correctly — AI reviews enabled!")
        except Exception as exc:  # pragma: no cover
            logger.error("⚠️  Failed to configure OpenAI: %s", exc, exc_info=True)

    # --------------------------------------------------------------------- API

    def is_available(self) -> bool:
        """Return ``True`` when the OpenAI client is ready to use."""
        return self.client is not None

    def generate_review(self, game: Game) -> Tuple[Optional[str], Optional[int]]:
        """
        Ask OpenAI to produce a short Italian review (2‑3 sentences) and a
        numeric rating (1–10) for *game*.

        Returns
        -------
        review
            The review text, or ``None`` if generation failed.
        rating
            An int between 1 and 10 or ``None``.
        """
        if not self.client:
            return None, None

        try:
            prompt: str = self._build_prompt(game)

            # --- Chat Completions request ----------------------------------
            response: ChatCompletion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Sei un critico di videogiochi esperto e severo. "
                            "Rispondi in italiano con un JSON che abbia esattamente "
                            'due chiavi: "review" (stringa) e "rating" (intero 1‑10). '
                            "Nessun markdown, nessun testo extra."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )
            content: str = response.choices[0].message.content

            return self._parse_json_response(content)
        except Exception as exc:  # pragma: no cover
            logger.error("⚠️  Error generating AI review: %s", exc, exc_info=True)
            return None, None

    # ------------------------------------------------------------------ Helpers

    @staticmethod
    def _build_prompt(game: Game) -> str:
        """Return a natural‑language prompt describing *game*."""
        return (
            f'Scrivi una mini‑recensione per il videogioco "{game.title}".\n'
            f"- Generi: {game.genres_str}\n"
            f"- Piattaforme: {game.platforms_str}\n"
            f"- Data di rilascio: {game.release_date}\n\n"
            "La recensione deve essere:\n"
            "- Massimo 2‑3 frasi (circa 50‑80 parole)\n"
            "- Scritta in italiano, professionale ma accessibile\n"
            "- Concentrata sui punti di forza di genere e gameplay\n"
            "- Seguita da un voto da 1 a 10\n"
        )

    # -------------------- Response parsing -----------------------------------

    @staticmethod
    def _parse_json_response(content: str) -> Tuple[Optional[str], Optional[int]]:
        """
        Parse the JSON response returned by the model.

        Falls back to heuristic parsing if JSON decoding fails or the schema
        isn't respected, ensuring the method never raises.
        """
        try:
            data = json.loads(content)
            review = str(data.get("review", "")).strip()
            rating_raw = data.get("rating")
            rating = int(rating_raw) if isinstance(rating_raw, (int, str)) else None
            if rating is not None and not (1 <= rating <= 10):
                rating = None
            if review:
                return review, rating
        except Exception:
            # fall through to legacy parsing
            pass
        return OpenAIReviewService._legacy_parse(content)

    @staticmethod
    def _legacy_parse(content: str) -> Tuple[Optional[str], Optional[int]]:
        """
        Legacy parser compatible with earlier prompt format (RECENSIONE/VOTO).
        """
        lines = content.splitlines()
        review, rating = "", None

        for line in lines:
            if line.upper().startswith("RECENSIONE:"):
                review = line.partition(":")[2].strip()
            elif line.upper().startswith("VOTO:"):
                digits = "".join(filter(str.isdigit, line))
                if digits:
                    rating = int(digits[:2])
                    if not (1 <= rating <= 10):
                        rating = None

        if not review:
            # as a last resort treat everything except trailing digits as review
            review_lines = [
                ln for ln in lines if not ln.strip().isdigit() and not ln.upper().startswith("VOTO:")
            ]
            review = " ".join(review_lines).strip()

        return review or None, rating
