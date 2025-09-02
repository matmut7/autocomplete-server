import unittest
from strings import search_with_prefix, _str_starts_with


class TestStrStartsWith(unittest.TestCase):
    def test_starts_with(self):
        self.assertEqual(_str_starts_with("banana", "ba"), (True, None))

    def test_word_past_prefix(self):
        self.assertEqual(_str_starts_with("cat", "ba"), (False, True))
        self.assertEqual(_str_starts_with("bb", "ba"), (False, True))

    def test_word_before_prefix(self):
        self.assertEqual(_str_starts_with("aa", "ab"), (False, False))
        self.assertEqual(_str_starts_with("a", "ab"), (False, False))

    def test_prefix_longer_than_word(self):
        self.assertEqual(_str_starts_with("a", "ab"), (False, False))
        self.assertEqual(_str_starts_with("ab", "abc"), (False, False))


class TestSearchWithPrefix(unittest.TestCase):
    def setUp(self):
        self.words = ["apple", "banana", "band", "bad", "cat", "dog"]

    def test_basic_prefix(self):
        result = search_with_prefix(self.words, "ba", limit=10)
        expected = ["bad", "banana", "band"]
        self.assertEqual(sorted(result), sorted(expected))

    def test_no_match(self):
        result = search_with_prefix(self.words, "z", limit=10)
        self.assertEqual(result, [])

    def test_limit(self):
        result = search_with_prefix(self.words, "b", limit=2)
        self.assertEqual(len(result), 2)

    def test_null_limit(self):
        result = search_with_prefix(self.words, "b", limit=0)
        self.assertEqual(result, [])

    def test_case_insensitive(self):
        result1 = search_with_prefix(self.words, "Ba", limit=10)
        result2 = search_with_prefix(self.words, "ba", limit=10)
        self.assertEqual(sorted(result1), sorted(result2))

    def test_short_circuit(self):
        words = ["a", "b", "da", "e", "db"]
        result = search_with_prefix(words, "d", limit=10)
        expected = ["da"]  # the "e" element should stop the search
        self.assertEqual(result, expected)

    def test_empty_prefix(self):
        result = search_with_prefix(self.words, "", limit=10)
        self.assertEqual(result, self.words)


if __name__ == "__main__":
    unittest.main()

