import pytest
from src.services.analyzer.domain.logic.lemmatizer import Lemmatizer


class TestLemmatizer:

    @pytest.fixture
    def lemmatizer(self):
        return Lemmatizer(cache_size=2)

    def test_basic(self, lemmatizer):
        assert lemmatizer.get_lemma("бежал") == "бежать"
        assert lemmatizer.get_lemma("столами") == "стол"

    def test_cache_logic(self, lemmatizer):
        lemmatizer.get_lemma("слово")
        info = lemmatizer.get_lemma.cache_info()
        assert info.misses == 1
        assert info.hits == 0

        lemmatizer.get_lemma("слово")
        info = lemmatizer.get_lemma.cache_info()
        assert info.hits == 1

    def test_cache_overflow(self, lemmatizer):
        lemmatizer.get_lemma("один")
        lemmatizer.get_lemma("два")
        lemmatizer.get_lemma("три")

        info = lemmatizer.get_lemma.cache_info()
        assert info.currsize <= 2
