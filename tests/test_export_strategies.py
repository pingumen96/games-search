"""
Unit tests for export strategies.
"""
import unittest
import tempfile
import os
from unittest.mock import patch
from models import Game
from exporters.strategies import (
    CSVExportStrategy,
    MarkdownExportStrategy,
    XMLExportStrategy,
    ExportStrategyFactory,
    ExportError,
    OPENPYXL_AVAILABLE
)


class TestExportStrategies(unittest.TestCase):
    """Test cases for export strategies"""

    def setUp(self):
        """Set up test data"""
        self.games = [
            Game(
                title="Game 1",
                platforms=["PC"],
                release_date="2023-01-15",
                genres=["Action"],
                ai_review="Great game",
                ai_rating=8
            ),
            Game(
                title="Game 2",
                platforms=["PlayStation 5"],
                release_date="2023-02-20",
                genres=["Adventure"],
                ai_review="Amazing story",
                ai_rating=9
            )
        ]

        self.games_no_ai = [
            Game(
                title="Game 1",
                platforms=["PC"],
                release_date="2023-01-15",
                genres=["Action"]
            )
        ]

    def test_csv_export_strategy(self):
        """Test CSV export strategy"""
        strategy = CSVExportStrategy()

        self.assertEqual(strategy.extension, ".csv")
        self.assertTrue(strategy.is_available)

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            filepath = f.name

        try:
            strategy.export(self.games, filepath)

            # Verify file exists and has content
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("Game 1", content)
                self.assertIn("Game 2", content)
                self.assertIn("AI Review", content)
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_markdown_export_strategy(self):
        """Test Markdown export strategy"""
        strategy = MarkdownExportStrategy()

        self.assertEqual(strategy.extension, ".md")
        self.assertTrue(strategy.is_available)

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            filepath = f.name

        try:
            strategy.export(self.games_no_ai, filepath)

            # Verify file exists and has content
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("# Games Database Results", content)
                self.assertIn("Game 1", content)
                self.assertIn("Total games found: 1", content)
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_xml_export_strategy(self):
        """Test XML export strategy"""
        strategy = XMLExportStrategy()

        self.assertEqual(strategy.extension, ".xml")
        self.assertTrue(strategy.is_available)

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xml') as f:
            filepath = f.name

        try:
            strategy.export(self.games, filepath)

            # Verify file exists and has content
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("<games_database>", content)
                self.assertIn("<title>Game 1</title>", content)
                self.assertIn("<includes_ai_reviews>true</includes_ai_reviews>", content)
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_export_empty_games_list(self):
        """Test export with empty games list raises error"""
        strategy = CSVExportStrategy()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            filepath = f.name

        try:
            with self.assertRaises(ExportError):
                strategy.export([], filepath)
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_export_strategy_factory_available_formats(self):
        """Test factory returns available formats"""
        formats = ExportStrategyFactory.get_available_formats()

        self.assertIn("CSV", formats)
        self.assertIn("Markdown", formats)
        self.assertIn("XML", formats)

        # XLSX availability depends on openpyxl
        if OPENPYXL_AVAILABLE:
            self.assertIn("XLSX (Excel)", formats)
        else:
            self.assertIn("XLSX (Excel) - Non disponibile", formats)

    def test_export_strategy_factory_create_strategy(self):
        """Test factory creates correct strategies"""
        csv_strategy = ExportStrategyFactory.create_strategy("CSV")
        self.assertIsInstance(csv_strategy, CSVExportStrategy)

        md_strategy = ExportStrategyFactory.create_strategy("Markdown")
        self.assertIsInstance(md_strategy, MarkdownExportStrategy)

        xml_strategy = ExportStrategyFactory.create_strategy("XML")
        self.assertIsInstance(xml_strategy, XMLExportStrategy)

    def test_export_strategy_factory_unknown_format(self):
        """Test factory raises error for unknown format"""
        with self.assertRaises(ExportError):
            ExportStrategyFactory.create_strategy("UNKNOWN")

    def test_export_strategy_factory_unavailable_format(self):
        """Test factory handles unavailable formats"""
        # Test with a format that includes "Non disponibile"
        with self.assertRaises(ExportError):
            ExportStrategyFactory.create_strategy("XLSX (Excel) - Non disponibile")


if __name__ == '__main__':
    unittest.main()
