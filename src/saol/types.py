from typing import NamedTuple


class SaolEntry(NamedTuple):
    word: str  # Normaliserat ord i grundform
    upos: str  # Ordklass
    conj: str  # Information om böjningsformer
