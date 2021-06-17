import typing

from trello import *

from .board_comparer import BoardComparer
from ..base_comparers import *
from ..compare_result import *

__all__ = ["BoardComparerUsingId"]


class BoardComparerUsingId(BoardComparer):

    def __init__(self, trello_client: TrelloClient,
                 inner_comparers: typing.List[BaseComparer] = None):
        super().__init__(inner_comparers)
        self._trello_client = trello_client

    def start_compare(self, actual: str, expected: str) -> CompareResult:
        actual_board = self._trello_client.get_board(actual)
        expected_board = self._trello_client.get_board(expected)
        return super().start_compare(actual_board, expected_board)
