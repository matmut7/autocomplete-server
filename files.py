import os

UNIX_SEPARATED_DICTS = ["eff_large.txt"]
WINDOWS_SEPARATED_DICTS = [
    "game_of_thrones.txt",
    "harry_potter.txt",
    "memory_alpha.txt",
    "star_wars.txt",
]


def load_words_from_directory(directory):
    """Load all words from every file in a directory into memory."""
    words = set()

    for filename in UNIX_SEPARATED_DICTS:
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            words.update(_load_unix_separated_file(path))

    for filename in WINDOWS_SEPARATED_DICTS:
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            words.update(_load_windows_separated_file(path))

    return sorted(words)


def _load_unix_separated_file(path):
    result = set()

    with open(path, "r", encoding="utf-8", newline=None) as f:
        for line in f:
            # remove numeric identifier before each word
            word = line.split()[1].strip()
            if word:
                result.add(word.lower())

    return sorted(result)


def _load_windows_separated_file(path):
    """These files use distinct newline separators and contain a preamble we need to skip."""

    result = set()
    skipping_preamble = True

    with open(path, "r", encoding="utf-8", newline="", errors="replace") as f:
        for line in f:
            if skipping_preamble:
                if line.startswith("1-1-1"):
                    skipping_preamble = False
                else:
                    continue

            # remove numeric identifier before each word
            word = line.split()[1].strip()
            if word:
                result.add(word.lower())

    return sorted(result)
