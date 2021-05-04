import unittest

from parameterized import parameterized

from classes.CompareResult import *


class CompareResultTests(unittest.TestCase):

    def setUp(self):
        self.compare_result = CompareResult(
            TrelloElement.BOARD, "name of element")

    @parameterized.expand([
        (CompareResultType.FAILED,),
        (CompareResultType.DOES_NOT_CONTAIN_ELEMENT,),
        (CompareResultType.HAS_EXTRA_ELEMENT,),
        (CompareResultType.INVALID_VALUE,)
    ])
    def test_add_inner_result_if_TypeOfAddedCompareResultIsNotSuccess_ContainerElementHasFailedType(
            self, compare_result_type):
        inner = CompareResult(TrelloElement.BOARD, compare_result_type=compare_result_type)

        self.compare_result.add_inner_compare_result(inner)

        self.assertEqual(self.compare_result.type, CompareResultType.FAILED)

    def test_add_inner_result(self):
        inner = CompareResult(TrelloElement.BOARD)
        self.compare_result.add_inner_compare_result(inner)
        assert inner in self.compare_result._inner_compare_results

    def test_get_not_success_result_if_no_failed_results(self):
        inner = CompareResult(TrelloElement.BOARD)
        self.assertEqual(list(inner.get_not_success_results()), [])

    def test_get_not_success_result_contains_CompareResult(self):
        self = CompareResult(TrelloElement.BOARD, '', CompareResultType.FAILED)
        assert self in list(self.get_not_success_results())

    def test_get_no_success_result_contains_all_failed_results(self):
        self = CompareResult(TrelloElement.BOARD, 'еуые', CompareResultType.FAILED)
        self.add_inner_compare_result(self)
        inner = CompareResult(TrelloElement.LIST,  "", CompareResultType.FAILED)
        self.add_inner_compare_result(inner)
        assert self in self._inner_compare_results and inner in self._inner_compare_results
