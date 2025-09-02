def search_with_prefix(words, prefix, limit):
    """Return words starting with prefix, sorted alphabetically."""
    prefix = prefix.lower()
    result = []

    if limit == 0:
        return result

    for word in words:
        starts_with, word_is_past_prefix = _str_starts_with(word, prefix)
        if starts_with:
            result.append(word)
            if len(result) >= limit:
                break
        elif word_is_past_prefix:
            break

    return result


def _str_starts_with(str, prefix):
    """
    First return value is whether the string begins with prefix.
    Second return value is, if the string does not begin with prefix,
    whether the word is past the prefix alphabetically.
    This allows to stop the search as soon as we have no longer any
    chance to find a matching word.
    """
    for index, char in enumerate(prefix):
        if index >= len(str):
            # if word is shorter than prefix, it's not a match
            # but we need to continue search
            return False, False
        if char < str[index]:
            return False, True
        elif char > str[index]:
            return False, False
    return True, None
