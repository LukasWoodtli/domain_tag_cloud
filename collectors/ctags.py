"""Collect sentences and words from source files using ctags"""

import collections
import os
import re
import subprocess

from collectors.symbols import Symbol

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TAG_FILE = os.path.join(SCRIPT_DIR, 'tags')


def find_source_files(root_path, file_extensions):
    """Recursively search for source files with the given extension"""
    headers = []
    for root, _, files in os.walk(root_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in file_extensions:
                headers.append(os.path.join(root, file))
    return headers


def chunks(files_list, chunk_size):
    """Yield successive chunk_size-sized chunks from files_list.
       Taken from: https://stackoverflow.com/a/312464/1272072"""
    for i in range(0, len(files_list), chunk_size):
        yield files_list[i:i + chunk_size]


def run_ctags(source_files):
    """Run the ctags command for all the given files."""
    for chunk in chunks(source_files, 50):
        if os.path.exists(TAG_FILE):
            os.remove(TAG_FILE)
        command_line = ['ctags', '--append', f'-f{TAG_FILE}']
        command_line.extend(chunk)
        subprocess.check_call(command_line)


def read_tag_file():
    """Extract information from the tag files"""
    all_symbols = []
    with open(TAG_FILE, 'r') as tag_file:
        for line in tag_file.readlines():
            symbol, source_file, _ = line.split("\t")
            # check type in rest of list
            all_symbols.append(Symbol(symbol, source_file))

    return all_symbols


def camel_case_split(identifier):
    """Split symbols that are written in camel case
       Taken from: https://stackoverflow.com/a/29920015/1272072"""
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


def extract_words(symbol):
    """Split 'sentences' into words."""
    words = []
    parts = camel_case_split(symbol.name)
    for part in parts:
        words.extend(re.split(r":|_", part))
    return words


def extract_all_words_from_symbols(symbols_list):
    """Get all words from a list of sentences."""
    all_words = collections.defaultdict(lambda: 0)
    for symbol in symbols_list:
        for word in extract_words(symbol):
            if len(word) > 2:
                all_words[word.lower()] = all_words[word.lower()] + 1
    return all_words
