import re

from trello import *

from ..base_comparers import *
from ..compare_result import *

__all__ = ["DescriptionComparer"]


class DescriptionComparer(BaseComparer):
    _markdown_link_re = re.compile(r"\[.+]\(\S+\)")

    def _current_compare(self, actual: Card, expected: Card) -> CompareResult:
        actual_description = actual.description.strip()
        expected_description = expected.description.strip()

        expected_description_without_link = self._markdown_link_re.sub(
            ' ', expected_description)
        actual_description_without_link = self._markdown_link_re.sub(
            ' ', actual_description)

        if expected_description_without_link != actual_description_without_link:
            result = CompareResult(TrelloElement.DESCRIPTION,
                                   result_type=CompareResultType.INVALID_VALUE)
            result.set_actual_and_expected(
                actual_description, expected_description)

            return result

        return CompareResult(TrelloElement.DESCRIPTION)
