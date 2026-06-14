from typing import Optional

from .types import SaolEntry
from .wordlist import saol14


def all_upos_by_word(wordlist: Optional[list[SaolEntry]] = None) -> dict[str, set[str]]:
    if not wordlist:
        wordlist = saol14

    result = dict()
    for entry in wordlist:
        if entry.word not in result:
            result[entry.word] = set()

        result[entry.word].add(entry.upos)

    return result


def lookup_word(
    word: str, wordlist: Optional[list[SaolEntry]] = None
) -> list[SaolEntry]:
    if not wordlist:
        wordlist = saol14

    return [entry for entry in wordlist if entry.word == word]


def lookup_upos(word: str, wordlist: Optional[list[SaolEntry]] = None) -> set[str]:
    matching_entries = lookup_word(word, wordlist)
    return {entry.upos for entry in matching_entries}
