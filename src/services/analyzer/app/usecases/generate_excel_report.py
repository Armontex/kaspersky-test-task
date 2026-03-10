from __future__ import annotations
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from ..ports import IExcelWriter, IStreamFileReader, IWordAnalyzer


class GenerateExcelReport:
    def __init__(
        self,
        analyzer: IWordAnalyzer,
        reader: Callable[[str], IStreamFileReader],
        writer: IExcelWriter,
    ) -> None:
        self._analyzer = analyzer
        self._reader = reader
        self._writer = writer

    def execute(self, input_file_path: str, output_report_path: str) -> None:
        """Сгенерировать отчёт в формате excel-формате

        Args:
            input_file_path (str): Путь input-файла
            output_report_path (str): Путь output-файла
        """
        with self._reader(input_file_path) as reader:
            for line in reader.read_lines():
                self._analyzer.process_line(line)

        results = self._analyzer.generate_data()
        self._writer.create_report(results, output_report_path)
