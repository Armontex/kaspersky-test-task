import pytest

from src.services.analyzer.domain import StringCollector


class TestCollector:

    @pytest.fixture
    def collector(self):
        return StringCollector()

    class TestAdd:

        def test_new_lemma_at_start(self, collector):
            collector.add("кот", 1, 1)
            assert collector.get_data(1) == {"кот": "1"}

        def test_new_lemma_with_offset(self, collector):
            collector.add("собака", 2, 3)
            assert collector.get_data(3) == {"собака": "0,0,2"}

        def test_existing_lemma_same_line(self, collector):
            collector.add("птица", 1, 2)
            collector.add("птица", 5, 2)

            assert collector.get_data(2) == {"птица": "0,6"}

        def test_existing_lemma_same_line_first_word(self, collector):
            collector.add("лес", 1, 1)
            collector.add("лес", 2, 1)
            assert collector.get_data(1) == {"лес": "3"}

        def test_existing_lemma_with_gap(self, collector):

            collector.add("дом", 1, 1)
            collector.add("дом", 1, 4)
            assert collector.get_data(4) == {"дом": "1,0,0,1"}

    class TestFinalize:

        def test_finalize_padding(self, collector):
            collector.add("окно", 1, 1)
            data = collector.get_data(5)
            assert data == {"окно": "1,0,0,0,0"}

        def test_multiple_get_data_calls(self, collector):
            collector.add("мир", 1, 1)
            first_call = collector.get_data(3)
            second_call = collector.get_data(3)

            assert first_call == second_call == {"мир": "1,0,0"}
