from trello import *
from .CompareResult import *


__all__ = ["MarkCalculator"]


class MarkCalculator:
    @classmethod
    def get_compare_mark(cls, compare_amount, compare_result: CompareResult):
        success_compare = cls._get_success_results(compare_result)

        return round(success_compare / compare_amount * 100)

    @classmethod
    def _get_success_results(cls, compare_result: CompareResult):
        success_result_amount = len(list(compare_result.get_results_by_type(
            CompareResultType.SUCCESS
        )))

        failed_results_amount = len(list(compare_result.get_results_by_type(
            CompareResultType.FAILED
        )))

        extra_element_amount = len(list(compare_result.get_results_by_type(
            CompareResultType.HAS_EXTRA_ELEMENT
        )))

        return success_result_amount + failed_results_amount - extra_element_amount
