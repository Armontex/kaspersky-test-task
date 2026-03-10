import pytest
from unittest.mock import MagicMock
from src.services.analyzer.domain.logic.word_analyzer import WordAnalyzer
from src.services.analyzer.domain.models import Result


class TestWordAnalyzer:

    @pytest.fixture
    def mock_lemmatizer(self):
        lemmatizer = MagicMock()
        lemmatizer.get_lemma.side_effect = lambda w: f"лемма_{w}"
        return lemmatizer

    @pytest.fixture
    def mock_collector(self):
        collector = MagicMock()
        collector.get_data.return_value = {"лемма_кот": "1,0", "лемма_dog": "0,2"}
        return collector

    @pytest.fixture
    def analyzer(self, mock_lemmatizer, mock_collector):
        return WordAnalyzer(mock_lemmatizer, mock_collector)

    class TestProcessLine:

        def test_process_line_tokenization(self, analyzer, mock_lemmatizer, mock_collector):
            line = "Кот, пёс! And... кот?"
            analyzer.process_line(line)

            assert mock_lemmatizer.get_lemma.call_count == 4
            mock_lemmatizer.get_lemma.assert_any_call("кот")
            mock_lemmatizer.get_lemma.assert_any_call("пёс")
            mock_lemmatizer.get_lemma.assert_any_call("and")

            mock_collector.add.assert_any_call("лемма_кот", 2, 1)
            mock_collector.add.assert_any_call("лемма_пёс", 1, 1)
            mock_collector.add.assert_any_call("лемма_and", 1, 1)

        def test_multiple_lines_counting(self, analyzer, mock_collector):
            analyzer.process_line("тест")
            analyzer.process_line("тест тест")

            assert analyzer._current_line_idx == 2

            assert analyzer._global_counts["лемма_тест"] == 3

            mock_collector.add.assert_any_call("лемма_тест", 2, 2)
            
    class TestGenerateData:

        def test_generate_data(self, analyzer, mock_collector):
            analyzer._current_line_idx = 2
            analyzer._global_counts = {"лемма_кот": 5, "лемма_dog": 2}

            results = list(analyzer.generate_data())

            mock_collector.get_data.assert_called_once_with(2)

            assert len(results) == 2
            assert (
                Result(lemma="лемма_кот", global_count=5, count_from_lines="1,0") in results
            )
            assert (
                Result(lemma="лемма_dog", global_count=2, count_from_lines="0,2") in results
            )
