from construct_db import *
import unittest

JSONCACHE = "cache.json"
JSONIMDB = "imdb.json"

class TestMapping(unittest.TestCase):
    def test_cache_json(self):
        data = json.load(open(JSONCACHE))
        for key, value in data.items():
            value = ast.literal_eval(value)
            if 'Search' in value:
                item = value['Search'][0]
                self.assertEqual(item['imdbID'].startswith("tt"), True)
                self.assertEqual(len(item['imdbID']), 9)

    def test_imdb_json(self):
        data = json.load(open(JSONIMDB))
        for key, value in data.items():
            item = ast.literal_eval(value)
            self.assertEqual(item['imdbID'].startswith("tt"), True)
            self.assertEqual(len(item['imdbID']), 9)
            self.assertNotEqual(item["Title"], None)
            self.assertNotEqual(int(item["Year"][0:4]), None)

if __name__ == '__main__':
    unittest.main()
