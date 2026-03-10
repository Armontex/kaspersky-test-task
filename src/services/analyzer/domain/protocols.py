from typing import Protocol


class ILemmatizer(Protocol):

    def get_lemma(self, word: str) -> str: ...


class ICollector(Protocol):

    def add(self, lemma: str, count: int, current_line: int) -> None: ...

    def get_data(self, total_lines: int) -> dict[str, str]: ...
