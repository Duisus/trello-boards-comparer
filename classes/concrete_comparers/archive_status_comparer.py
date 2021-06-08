from trello import *

from ..base_comparers import *
from ..compare_result import *

__all__ = ["ArchiveStatusComparer"]


class ArchiveStatusComparer(BaseComparer):

    def _current_compare(self, actual: Card, expected: Card) -> CompareResult:
        compare_result = CompareResult(
            TrelloElement.CARD,
            "Статус архивации",
        )

        if actual.closed != expected.closed:
            compare_result = CompareResult(
                TrelloElement.CARD,
                "Статус архивации",
                CompareResultType.INVALID_VALUE
            )

            compare_result.actual_value = actual.closed
            compare_result.expected_value = expected.closed

        return compare_result
