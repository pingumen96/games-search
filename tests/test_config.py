"""
Unit tests for configuration management.
"""
import unittest
from unittest.mock import patch, MagicMock
import os
from config import Config, ConfigError


class TestConfig(unittest.TestCase):
    """Test cases for Config class"""

    def setUp(self):
        """Reset singleton instance before each test"""
        Config._instance = None
        Config._initialized = False

    def tearDown(self):
        """Clean up after each test"""
        Config._instance = None
        Config._initialized = False

    @patch.dict(os.environ, {'RAWG_API_KEY': 'test_rawg_key', 'OPENAI_API_KEY': 'test_openai_key'})
    @patch('config.config.load_dotenv')
    def test_config_initialization_with_keys(self, mock_load_dotenv):
        """Test config initialization with both API keys"""
        config = Config()

        mock_load_dotenv.assert_called_once()
        self.assertEqual(config.rawg_api_key, 'test_rawg_key')
        self.assertEqual(config.openai_api_key, 'test_openai_key')
        self.assertTrue(config.has_openai_key)

    @patch.dict(os.environ, {'RAWG_API_KEY': 'test_rawg_key'}, clear=True)
    @patch('config.config.load_dotenv')
    def test_config_initialization_without_openai_key(self, mock_load_dotenv):
        """Test config initialization without OpenAI key"""
        config = Config()

        self.assertEqual(config.rawg_api_key, 'test_rawg_key')
        self.assertIsNone(config.openai_api_key)
        self.assertFalse(config.has_openai_key)

    @patch.dict(os.environ, {}, clear=True)
    @patch('config.config.load_dotenv')
    def test_config_initialization_without_rawg_key(self, mock_load_dotenv):
        """Test config initialization without RAWG key raises error"""
        with self.assertRaises(ConfigError) as context:
            Config()

        self.assertIn("RAWG_API_KEY non trovata", str(context.exception))

    @patch.dict(os.environ, {'RAWG_API_KEY': 'test_key'})
    @patch('config.config.load_dotenv')
    def test_singleton_behavior(self, mock_load_dotenv):
        """Test that Config is a singleton"""
        config1 = Config()
        config2 = Config()

        self.assertIs(config1, config2)
        # load_dotenv should only be called once due to singleton
        mock_load_dotenv.assert_called_once()

    @patch.dict(os.environ, {'RAWG_API_KEY': 'test_key'})
    @patch('config.config.load_dotenv')
    def test_initialization_only_once(self, mock_load_dotenv):
        """Test that initialization happens only once"""
        config1 = Config()
        original_key = config1.rawg_api_key

        # Change environment variable
        with patch.dict(os.environ, {'RAWG_API_KEY': 'new_key'}):
            config2 = Config()

        # Should still have the original key due to singleton behavior
        self.assertEqual(config2.rawg_api_key, original_key)
        self.assertEqual(config1.rawg_api_key, config2.rawg_api_key)


if __name__ == '__main__':
    unittest.main()
