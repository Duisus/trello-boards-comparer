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

    def test_get_not_success_result_contains_all_not_success_results(self):
        upper = CompareResult(TrelloElement.BOARD, 'еуые', CompareResultType.FAILED)
        inner = CompareResult(TrelloElement.LIST, "", CompareResultType.DOES_NOT_CONTAIN_ELEMENT)
        upper.add_inner_compare_result(inner)
        self.assertCountEqual(
            (upper, inner),
            upper.get_not_success_results())

    def test_get_not_success_result_does_not_return_success_CompareResults(self):
        upper = CompareResult(TrelloElement.BOARD, compare_result_type=CompareResultType.FAILED)
        upper.add_inner_compare_result(
            CompareResult(TrelloElement.LIST, compare_result_type=CompareResultType.FAILED))
        success_result = CompareResult(
            TrelloElement.LIST, compare_result_type=CompareResultType.SUCCESS)
        upper.add_inner_compare_result(success_result)

        assert success_result not in upper.get_not_success_results()

    def test_get_not_success_result_order_is_like_in_depth_first_search(self):  # todo refactor
        names = ["1", "1.1", "1.1.1", "1.1.2", "1.2"]
        upper_result = CompareResult(
            TrelloElement.LIST, names[0], CompareResultType.FAILED)
        inner_result = CompareResult(
            TrelloElement.CARD, names[1], CompareResultType.FAILED)
        inner_result.add_inner_compare_result(
            CompareResult(TrelloElement.DESCRIPTION, names[2], CompareResultType.INVALID_VALUE))
        inner_result.add_inner_compare_result(
            CompareResult(TrelloElement.COVER, names[3], CompareResultType.DOES_NOT_CONTAIN_ELEMENT))
        upper_result.add_inner_compare_result(inner_result)
        upper_result.add_inner_compare_result(
            CompareResult(TrelloElement.CARD, names[4], CompareResultType.HAS_EXTRA_ELEMENT))

        actual = [result.compared_element_name for result in upper_result.get_not_success_results()]

        self.assertEqual(names, actual)
