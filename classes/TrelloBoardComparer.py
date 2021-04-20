from trello import *
from .CompareResult import *


class TrelloBoardComparer:
    def __int__(self, trello_client: TrelloClient):
        self._trello_client = trello_client

    def compare_boards(self,
                       board_to_compare_id: str,
                       expected_board_id: str) -> CompareResult:
        board_to_compare = self._trello_client.get_board(board_to_compare_id)
        expected_board = self._trello_client.get_board(expected_board_id)

        lists_to_compare = board_to_compare.list_lists()
        expected_lists = expected_board.list_lists()

        compare_result = CompareResult(TrelloElement.BOARD, board_to_compare.name)

        lists_to_compare_names = (item.name for item in lists_to_compare)
        expected_lists_names = (item.name for item in expected_lists)

        for i in range(len(lists_to_compare)):
            if lists_to_compare[i].name not in expected_lists_names:
                compare_result.add_inner_compare_result(CompareResult(
                    TrelloElement.LIST,
                    lists_to_compare[i].name,
                    CompareResultType.HAS_EXTRA_ELEMENT
                ))

            for j in range(len(expected_lists)):
                if lists_to_compare[i].name == expected_lists[j].name:
                    compare_result.add_inner_compare_result(
                        self._compare_lists(lists_to_compare[i], expected_lists[j])
                    )
                elif expected_lists[j].name not in lists_to_compare_names:
                    compare_result.add_inner_compare_result(CompareResult(
                        TrelloElement.LIST,
                        expected_lists[j].name,
                        CompareResultType.DOES_NOT_CONTAIN_ELEMENT
                    ))

        return compare_result

    def _compare_lists(self,
                       list_to_compare: "List",
                       expected_list: "List") -> CompareResult:
        compare_result = CompareResult(TrelloElement.LIST, list_to_compare.name)

        cards_to_compare = list_to_compare.list_cards(card_filter="all")
        expected_cards = expected_list.list_cards(card_filter="all")

        cards_to_compare_names = (item.name for item in cards_to_compare)
        expected_cards_names = (item.name for item in expected_cards)

        for i in range(len(cards_to_compare)):
            if cards_to_compare[i].name not in expected_cards_names:
                compare_result.add_inner_compare_result(CompareResult(
                    TrelloElement.CARD,
                    cards_to_compare[i].name,
                    CompareResultType.HAS_EXTRA_ELEMENT
                ))

            for j in range(len(expected_cards)):
                if cards_to_compare[i].name == expected_cards[j].name:
                    compare_result.add_inner_compare_result(
                        self._compare_lists(cards_to_compare[i], expected_cards[j])
                    )
                elif expected_cards[j].name not in cards_to_compare_names:
                    compare_result.add_inner_compare_result(CompareResult(
                        TrelloElement.LIST,
                        expected_cards[j].name,
                        CompareResultType.DOES_NOT_CONTAIN_ELEMENT
                    ))

        return compare_result

    def _compare_cards(self,
                       card_to_compare: Card,
                       expected_card: Card) -> CompareResult:
        pass
