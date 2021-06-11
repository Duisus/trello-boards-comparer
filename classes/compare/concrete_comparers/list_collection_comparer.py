from trello import *

from ..base_comparers import *
from ..compare_result import *

__all__ = ["ListCollectionComparer"]


class ListCollectionComparer(BaseCollectionComparer):

    def _current_compare(self, actual: Board,
                         expected: Board) -> CompareResult:
        actual_lists = actual.list_lists(list_filter="open")
        expected_lists = expected.list_lists(list_filter="open")

        results = []

        actual_lists_names = [item.name for item in actual_lists]
        expected_lists_names = [item.name for item in expected_lists]

        # TODO вынести в абстрактый класс
        for i in range(len(actual_lists)):
            if actual_lists[i].name not in expected_lists_names:
                results.append(CompareResult(
                    TrelloElement.LIST,
                    actual_lists[i].name,
                    CompareResultType.EXTRA_ELEMENT
                ))

            for j in range(len(expected_lists)):
                if actual_lists[i].name == expected_lists[j].name:
                    results.append(
                        self._compare_elements(actual_lists[i],
                                               expected_lists[j])
                    )

        for expected_list in expected_lists:
            if expected_list.name not in actual_lists_names:
                results.append(CompareResult(
                    TrelloElement.LIST,
                    expected_list.name,
                    CompareResultType.DOES_NOT_CONTAIN_ELEMENT
                ))

        return results
