import typing

from ..base_comparers import *
from ..compare_result import *

__all__ = ["ChecklistItemComparer"]


class ChecklistItemComparer(BaseComparer):

    def _current_compare(self, actual: typing.Dict,
                         expected: typing.Dict) -> CompareResult:
        compare_result = CompareResult(TrelloElement.CHECKLIST_ITEM)

        if actual['checked'] != expected['checked']:
            checked_compare = CompareResult(
                TrelloElement.CHECKLIST_ITEM,
                'Маркер',
                CompareResultType.INVALID_VALUE)

            checked_compare.set_actual_and_expected(
                'отмеченный' if actual['checked'] else 'неотмеченый',
                'отмеченый' if expected['checked'] else 'неотмеченый'
            )

            compare_result.add_inner_compare_result(checked_compare)

        else:
            compare_result.add_inner_compare_result(CompareResult(
                TrelloElement.CHECKLIST_ITEM,
                'Маркер'))

        if actual['name'] != expected['name']:
            value_compare = CompareResult(
                TrelloElement.CHECKLIST_ITEM,
                'Значение',
                CompareResultType.INVALID_VALUE)

            value_compare.set_actual_and_expected(
                actual['name'], expected['name'])

            compare_result.add_inner_compare_result(value_compare)

        else:
            compare_result.add_inner_compare_result(CompareResult(
                TrelloElement.CHECKLIST_ITEM,
                'Значение'))

        return compare_result
