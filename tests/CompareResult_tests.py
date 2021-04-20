import unittest

from parametrized import parametrized

from classes.CompareResult import *


class CompareResultTests(unittest.TestCase):

    def setUp(self):
        self.compare_result = CompareResult(
            TrelloElement.BOARD, "name of element")

    @parametrized([  # похоже он не работает, просто в unittest модуле вроде как нет встроенного параметризатора
        CompareResultType.FAILED,
        CompareResultType.DOES_NOT_CONTAIN_ELEMENT,
        CompareResultType.HAS_EXTRA_ELEMENT,
        CompareResultType.INVALID_VALUE
    ])
    def test_add_inner_result_IfTypeOfAddedCompareResultIsNotSuccess_ContainerElementHasFailedType(
            self, compare_result_type):
        inner = CompareResult(TrelloElement.BOARD, compare_result_type=compare_result_type)

        self.compare_result.add_inner_compare_result(inner)

        self.assertEqual(self.compare_result.type, CompareResultType.FAILED)
