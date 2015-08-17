from unittest import TestCase
from app.main.utils import normalize_for_search


class TestUtils(TestCase):
    def test_normalize_for_search(self):
        brewery_name = 'Zywiec Zdroj'
        beer_name = 'Zrodlane Slabe'
        normalized = normalize_for_search(brewery_name, beer_name)
        expected = 'zywiec zdroj zrodlane slabe'
        self.assertEquals(normalized, expected)