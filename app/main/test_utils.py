from unittest import TestCase
from app.main.utils import normalize_for_search


class TestUtils(TestCase):
    def test_normalize_for_search(self):
        normalized = normalize_for_search('Zywiec Zdroj Zrodlane Slabe')
        self.assertEquals(normalized, 'zywiec zdroj zrodlane slabe')