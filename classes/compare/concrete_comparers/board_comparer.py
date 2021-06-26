from trello import *

from ..base_comparers import *
from ..compare_result import *

__all__ = ["BoardComparer"]


class BoardComparer(BaseComparer):

    def _current_compare(self, actual: Board, expected: Board) -> CompareResult:
        return CompareResult(TrelloElement.BOARD, actual.name)
