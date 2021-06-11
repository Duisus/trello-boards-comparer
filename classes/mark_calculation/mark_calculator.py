from classes.compare.compare_result import *

__all__ = ["MarkCalculator"]


class MarkCalculator:
    @classmethod
    def calculate(cls, compare_amount, compare_result: CompareResult):
        success_compare = cls._get_primary_scores(compare_result)

        return round(success_compare / compare_amount * 100)

    @classmethod
    def _get_primary_scores(cls, compare_result: CompareResult):
        success_result_amount = len(list(compare_result.get_results_by_type(
            CompareResultType.SUCCESS
        )))

        failed_results_amount = len(list(compare_result.get_results_by_type(
            CompareResultType.FAILED
        )))

        extra_element_amount = len(list(compare_result.get_results_by_type(
            CompareResultType.EXTRA_ELEMENT
        )))

        return success_result_amount + failed_results_amount - extra_element_amount
