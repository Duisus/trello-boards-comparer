from trello import *

from ..base_comparers import *
from ..compare_result import *

__all__ = ["CardComparer"]


class CardComparer(BaseComparer):

    def _current_compare(self, actual: Card, expected: Card) -> CompareResult:
        return CompareResult(TrelloElement.CARD, actual.name)
