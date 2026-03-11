from dependency_injector import containers, providers

from ..services.analyzer.app import GenerateExcelReport
from ..services.analyzer.domain import WordAnalyzer, Lemmatizer, StringCollector
from ..services.analyzer.infra.readers import StreamFileReader
from ..services.analyzer.infra.writers import ExcelWriter


class Container(containers.DeclarativeContainer):

    string_collector = providers.Factory(StringCollector)
    lemmatizer = providers.Factory(Lemmatizer)
    word_analyzer = providers.Factory(
        WordAnalyzer, lemmatizer=lemmatizer, collector=string_collector
    )

    stream_file_reader = providers.Object(StreamFileReader)
    excel_writer = providers.Singleton(ExcelWriter)

    generate_excel_report = providers.Factory(
        GenerateExcelReport,
        analyzer=word_analyzer,
        reader=stream_file_reader,
        writer=excel_writer,
    )

container = Container()
