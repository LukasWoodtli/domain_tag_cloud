"""General integration tests (approval tests)."""

import operator
import os
import unittest
import json

from approvaltests import verify

from collectors.ctags import find_source_files, run_ctags, read_tag_file, extract_all_words_from_symbols
from output import word_cloud

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
WORD_CLOUD_FILE = os.path.join(SCRIPT_DIR, "words.png")


class TestRegression(unittest.TestCase):
    """Test ctags collector and word cloud output."""

    def setUp(self):
        files = find_source_files(os.path.join(SCRIPT_DIR, "test_data"), [".h", ".hpp"])
        run_ctags(files)
        symbols = read_tag_file()
        self.words = extract_all_words_from_symbols(symbols)

    def test_regression(self):
        """Check that the expected words are extracted"""
        sorted_words = sorted(self.words.items(), key=operator.itemgetter(1), reverse=True)
        verify(json.dumps(sorted_words, indent=2))

    def test_word_cloud(self):
        """check if image file exists after creation of word cloud"""
        word_cloud.generate_word_cloud(WORD_CLOUD_FILE, self.words)
        self.assertTrue(os.path.isfile(WORD_CLOUD_FILE))


if __name__ == '__main__':
    unittest.main()
