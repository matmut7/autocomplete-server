import unittest
import os
from files import _load_unix_separated_file, _load_windows_separated_file


class TestLoadWordsFromDirectory(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), "decoded_dictionaries")
        self.unix_separated_dicts = [
            "eff_large.txt",
        ]
        self.windows_separated_dicts = [
            "game_of_thrones.txt",
            "harry_potter.txt",
            "memory_alpha.txt",
            "star_wars.txt",
        ]

    def _load_expected(self, filename):
        path = os.path.join(self.test_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            return sorted([line.strip().lower() for line in f if line.strip()])

    def test_all_dicts_loaded(self):
        for filename in self.unix_separated_dicts:
            result = _load_unix_separated_file(
                os.path.join(os.path.dirname(__file__), "..", "dictionaries", filename)
            )
            expected = self._load_expected(filename)
            print(len(expected))
            self.assertEqual(result, expected)

        for filename in self.windows_separated_dicts:
            result = _load_windows_separated_file(
                os.path.join(os.path.dirname(__file__), "..", "dictionaries", filename)
            )
            expected = self._load_expected(filename)
            print(len(expected))
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

