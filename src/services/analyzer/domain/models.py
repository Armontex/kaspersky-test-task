from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    lemma: str
    global_count: int
    count_from_lines: str
