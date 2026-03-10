from __future__ import annotations
from typing import Generator


class StreamFileReader:

    def __init__(self, path: str) -> None:
        self._path = path
        self._file = None

    def __enter__(self) -> StreamFileReader:
        self._file = open(
            self._path,
            mode="r",
            encoding="UTF-8",
            newline="",
            errors="replace",
        )
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._file:
            self._file.close()

    def read_lines(self) -> Generator[str, None, None]:
        """Прочитать строки

        Raises:
            RuntimeError: Файл не открыт, используйте контекстный менеджер `with`

        Yields:
            Generator[str, None, None]:
        """
        if not self._file:
            raise RuntimeError(
                "Файл не открыт, используйте контекстный менеджер `with`"
            )

        yield from self._file
