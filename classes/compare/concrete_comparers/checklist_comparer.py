from trello import *

from ..base_comparers import *
from ..compare_result import *

__all__ = ["ChecklistComparer"]


class ChecklistComparer(BaseCollectionComparer):

    def _current_compare(self, actual: Checklist,
                         expected: Checklist) -> CompareResult:
        compare_result = CompareResult(TrelloElement.CHECKLIST,
                                       actual.name)

        checklist_items_to_compare = actual.items
        expected_checklist_items = expected.items

        min_length = min(len(checklist_items_to_compare), len(expected_checklist_items))
        max_length = max(len(checklist_items_to_compare), len(expected_checklist_items))

        for i in range(min_length):
            compare_result.add_inner_compare_result(
                self._compare_elements(checklist_items_to_compare[i],
                                       expected_checklist_items[i]))

        if len(checklist_items_to_compare) > len(expected_checklist_items):
            for i in range(min_length, max_length):
                compare_result.add_inner_compare_result(CompareResult(
                    TrelloElement.CHECKLIST_ITEM,
                    checklist_items_to_compare[i]['name'],
                    CompareResultType.EXTRA_ELEMENT
                ))

        if len(checklist_items_to_compare) < len(expected_checklist_items):
            for i in range(min_length, max_length):
                compare_result.add_inner_compare_result(CompareResult(
                    TrelloElement.CHECKLIST_ITEM,
                    expected_checklist_items[i]['name'],
                    CompareResultType.DOES_NOT_CONTAIN_ELEMENT
                ))

        return compare_result
