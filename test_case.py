import unittest
from utils import country_to_continent, gender_rearrange

class TestCountryToContinent(unittest.TestCase):

    def test_country_continent(self):
        countries = ['India', 'Canada', 'France', 'Singapore', 'New Zealand']
        expected = ['Asia', 'North America', 'Europe', 'Asia', 'Oceania']
        self.assertListEqual([country_to_continent(country) for country in countries],
                              expected)
        
if __name__ == '__main__':
    unittest.main()
