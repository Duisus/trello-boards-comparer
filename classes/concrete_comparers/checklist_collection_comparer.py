from trello import *

from ..base_comparers import *
from ..compare_result import *

__all__ = ["ChecklistCollectionComparer"]


class ChecklistCollectionComparer(BaseCollectionComparer):

    def _current_compare(self, actual: Card,
                         expected: Card) -> CompareResult:
        compare_results = []

        checklists_to_compare = actual.checklists
        expected_checklists = expected.checklists

        checklists_to_compare_names = (item.name for item in checklists_to_compare)
        expected_checklists_names = (item.name for item in expected_checklists)

        for i in range(len(checklists_to_compare)):
            if checklists_to_compare[i].name not in expected_checklists_names:
                compare_results.append(CompareResult(
                    TrelloElement.CHECKLIST,
                    checklists_to_compare[i].name,
                    CompareResultType.HAS_EXTRA_ELEMENT
                ))

            for j in range(len(expected_checklists)):
                if checklists_to_compare[i].name == expected_checklists[j].name:
                    compare_results.append(
                        self._compare_elements(checklists_to_compare[i],
                                               expected_checklists[j])
                    )

        for expected_checklist in expected_checklists:
            if expected_checklist.name not in checklists_to_compare_names:
                compare_results.append(CompareResult(
                    TrelloElement.CHECKLIST,
                    expected_checklist.name,
                    CompareResultType.DOES_NOT_CONTAIN_ELEMENT
                ))

        return compare_results
