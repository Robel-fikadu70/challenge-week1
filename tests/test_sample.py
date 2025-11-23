import unittest
import sys
import os

# Add src to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.loader import DataLoader

class TestSetup(unittest.TestCase):
    def test_dataloader_init(self):
        """Test that DataLoader can be initialized"""
        loader = DataLoader(data_path='../data')
        self.assertIsNotNone(loader)
        self.assertEqual(loader.data_path, '../data')

if __name__ == '__main__':
    unittest.main()