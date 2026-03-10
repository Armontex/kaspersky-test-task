from __future__ import annotations
from typing import TYPE_CHECKING, Iterable
from xlsxwriter import Workbook

if TYPE_CHECKING:
    from xlsxwriter.worksheet import Worksheet
    from src.services.analyzer.domain import Result


class ExcelWriter:
    COLUMNS = ["Словоформа", "Общее количество", "Статистика по строкам"]

    def create_report(self, results: Iterable[Result], output_path: str) -> None:
        """Создать отчёт

        Args:
            results (Iterable[Result]): результат
            output_path (str):
        """
        wb = Workbook(output_path, {"constant_memory": True})
        sheet = wb.add_worksheet("Анализ")

        self._write_headers(sheet)
        self._write_results(results, sheet)

        wb.close()

    def _write_headers(self, sheet: Worksheet) -> None:
        for col, column_name in enumerate(self.COLUMNS):
            sheet.write(0, col, column_name)

    def _write_results(self, results: Iterable[Result], sheet: Worksheet) -> None:
        for row, res in enumerate(results, start=1):
            sheet.write(row, 0, res.lemma)
            sheet.write(row, 1, res.global_count)
            sheet.write(row, 2, res.count_from_lines)
