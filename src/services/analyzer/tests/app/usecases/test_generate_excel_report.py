from unittest.mock import MagicMock
from src.services.analyzer.app import GenerateExcelReport


def test_generate_report_use_case():
    mock_analyzer = MagicMock()
    mock_reader_instance = MagicMock()
    mock_reader_factory = MagicMock(return_value=mock_reader_instance)
    mock_writer = MagicMock()

    mock_reader_instance.__enter__.return_value = mock_reader_instance
    mock_reader_instance.read_lines.return_value = ["строка 1", "строка 2"]

    use_case = GenerateExcelReport(mock_analyzer, mock_reader_factory, mock_writer)

    use_case.execute("in.txt", "out.xlsx")

    mock_reader_factory.assert_called_once_with("in.txt")
    assert mock_analyzer.process_line.call_count == 2
    mock_writer.create_report.assert_called_once()
