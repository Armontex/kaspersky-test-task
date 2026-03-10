from __future__ import annotations
import re

from typing import TYPE_CHECKING, Generator
from collections import Counter

from ..models import Result

if TYPE_CHECKING:
    from ..protocols import ILemmatizer, ICollector


class WordAnalyzer:

    WORD_PATTERN = r"[а-яёa-z]+"

    def __init__(self, lemmatizer: ILemmatizer, collector: ICollector) -> None:
        """Анализатор слов

        Args:
            lemmatizer (ILemmatizer):
            collector (ICollector):

        >>> wa = WordAnalyzer(...)
        >>> wa.process_line(...)
        >>> result = wa.get_data()
        """
        self._lemmatizer = lemmatizer
        self._collector = collector
        self._current_line_idx = 0
        self._global_counts = Counter()

    def process_line(self, line: str) -> None:
        """Обработать строку

        Args:
            line (str): Строка
        """
        self._current_line_idx += 1
        words = re.findall(self.WORD_PATTERN, line.lower())
        line_counts = Counter()

        for word in words:
            lemma = self._lemmatizer.get_lemma(word)
            self._global_counts[lemma] += 1
            line_counts[lemma] += 1

        for lemma, count in line_counts.items():
            self._collector.add(lemma, count, self._current_line_idx)

    def generate_data(self) -> Generator[Result, None, None]:
        """Сгенерировать данные"""
        data = self._collector.get_data(self._current_line_idx)
        for lemma, count_from_lines in data.items():
            global_count = self._global_counts[lemma]
            yield Result(
                lemma=lemma,
                global_count=global_count,
                count_from_lines=count_from_lines,
            )
