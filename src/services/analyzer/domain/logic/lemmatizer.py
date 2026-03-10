from __future__ import annotations

from pymorphy3 import MorphAnalyzer
from functools import lru_cache


class Lemmatizer:

    def __init__(self, cache_size: int = 10000) -> None:
        self._analyzer = MorphAnalyzer()
        self.get_lemma = lru_cache(maxsize=cache_size)(self._get_lemma_internal)

    def _get_lemma_internal(self, word: str) -> str:
        return self._analyzer.parse(word)[0].normal_form

    def get_lemma(self, word: str) -> str:
        """Получить начальную форму (лемму)

        Args:
            word (str): Слово

        Returns:
            str: Начальная форма слова
        """
        ...
