from __future__ import annotations


class StringCollector:
    def __init__(self):
        """
        >>> collector = StringAppendCollector()
        >>> collector.add(...)
        >>> result = collector.get_data(total_lines)
        """
        self._data: dict[str, str] = {}  # {lemma: "0,1,0"}
        self._last_line: dict[str, int] = {}  # {lemma: last_line_index}

    def add(self, lemma: str, count: int, current_line: int) -> None:
        """Добавить лемму в коллекцию

        Args:
            lemma (str): лемма
            count (int): кол-во
            current_line (int): индекс текущей строки
        """
        if lemma not in self._data:  # Если новая
            prefix = "0," * (current_line - 1)
            self._data[lemma] = prefix + str(count)
        else:
            diff = current_line - self._last_line[lemma] - 1

            if diff < 0:  # Если add вызвали с одной и той же леммой несколько раз
                line = self._data[lemma]
                last_separator_idx = line.rfind(",")

                update_last_number = str(int(line[last_separator_idx + 1 :]) + count)
                new_line = line[: last_separator_idx + 1] + update_last_number

                self._data[lemma] = new_line
                return

            self._data[lemma] += "," + "0," * diff + str(count)

        self._last_line[lemma] = current_line

    def _finalize(self, total_lines: int) -> None:
        for lemma in self._data:
            diff = total_lines - self._last_line[lemma]
            if diff > 0:
                self._data[lemma] += "," + "0," * (diff - 1) + "0"
                self._last_line[lemma] = total_lines

    def get_data(self, total_lines: int) -> dict[str, str]:
        self._finalize(total_lines)
        return self._data
