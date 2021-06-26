from trello import *

from ..base_comparers import *
from ..compare_result import *

__all__ = ["ListComparer"]


class ListComparer(BaseCollectionComparer):

    def _current_compare(self, actual: List, expected: List) -> CompareResult:
        compare_result = CompareResult(TrelloElement.LIST, actual.name)

        actual_cards = actual.list_cards(card_filter="all")
        expected_cards = expected.list_cards(card_filter="all")

        actual_cards_names = (item.name for item in actual_cards)
        expected_cards_names = (item.name for item in expected_cards)

        for i in range(len(actual_cards)):
            if actual_cards[i].name not in expected_cards_names:
                compare_result.add_inner_compare_result(CompareResult(
                    TrelloElement.CARD,
                    actual_cards[i].name,
                    CompareResultType.EXTRA_ELEMENT
                ))

            for j in range(len(expected_cards)):
                if actual_cards[i].name == expected_cards[j].name:
                    compare_result.add_inner_compare_result(
                        self._compare_elements(actual_cards[i], expected_cards[j])
                    )

        for expected_card in expected_cards:
            if expected_card.name not in actual_cards_names:
                compare_result.add_inner_compare_result(CompareResult(
                    TrelloElement.CARD,
                    expected_card.name,
                    CompareResultType.DOES_NOT_CONTAIN_ELEMENT
                ))

        return compare_result
