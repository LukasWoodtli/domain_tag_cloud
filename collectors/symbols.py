""""Imformation about a word (symbol)"""


class Symbol:
    """Information about occurrences of a word."""
    def __init__(self, name, source_file):
        self.name = name
        self.source_file = source_file
