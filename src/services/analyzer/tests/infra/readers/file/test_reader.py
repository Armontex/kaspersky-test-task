import pytest
from src.services.analyzer.infra.readers import StreamFileReader


class TestStreamFileReader:
    def test_read_lines_success(self, tmp_path):
        file_content = "line1\nline2\nline3"
        file_path = tmp_path / "test.txt"
        file_path.write_text(file_content, encoding="UTF-8")

        with StreamFileReader(str(file_path)) as reader:
            lines = list(reader.read_lines())

        assert [line.strip() for line in lines] == ["line1", "line2", "line3"]

    def test_closes_file_handle(self, tmp_path):
        file_path = tmp_path / "test.txt"
        file_path.write_text("data", encoding="UTF-8")

        reader = StreamFileReader(str(file_path))
        with reader as r:
            assert not r._file.closed  # type: ignore

        assert reader._file.closed  # type: ignore

    def test_raises_error_outside_context(self, tmp_path):
        file_path = tmp_path / "test.txt"
        file_path.write_text("data", encoding="UTF-8")

        reader = StreamFileReader(str(file_path))

        with pytest.raises(RuntimeError, match="Файл не открыт"):
            next(reader.read_lines())

    def test_handles_broken_utf8(self, tmp_path):
        file_path = tmp_path / "broken.txt"
        with open(file_path, "wb") as f:
            f.write(b"good text\n")
            f.write(b"\xff\xfe\xfd\n")

        with StreamFileReader(str(file_path)) as reader:
            lines = list(reader.read_lines())

        assert len(lines) == 2
        assert "" in lines[1]
