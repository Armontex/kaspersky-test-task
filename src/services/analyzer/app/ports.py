from __future__ import annotations
from typing import TYPE_CHECKING, Protocol, Generator, ContextManager, Iterable, Self

if TYPE_CHECKING:
    from ..domain import Result


class IWordAnalyzer(Protocol):

    def process_line(self, line: str) -> None: ...

    def generate_data(self) -> Generator[Result, None, None]: ...


class IStreamFileReader(ContextManager["IStreamFileReader"], Protocol):

    def read_lines(self) -> Generator[str, None, None]: ...


class IExcelWriter(Protocol):

    def create_report(self, results: Iterable[Result], output_path: str) -> None: ...
