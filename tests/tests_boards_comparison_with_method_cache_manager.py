import unittest

from trello import *

from classes.compare.compare_result import *
from classes.compare.default_comparers_provider import DefaultComparersProvider
from classes.method_cache_manager import *

CONFIG_FILE = r"..\config.json"


class BoardCompareTestsWhenExpectedBoardCached(unittest.TestCase):
    def setUp(self):
        with open(CONFIG_FILE, "r") as file:
            config_data = json.load(file)

        client = TrelloClient(
            api_key=config_data["api_key"],
            token=config_data["token"]
        )
        self._board_comparer = DefaultComparersProvider.create_board_comparer()
        self.client = client

    def board_compare_test_with_cache(self, compare_board_id, expected_board_id, expected_result_types):
        compare_board = self.client.get_board(compare_board_id)
        expected_board = self.client.get_board(expected_board_id)
        mcm_expected = MethodCacheManager(expected_board, [Card, List])
        compare_result = self._board_comparer.start_compare(compare_board, mcm_expected)
        result_list = list(compare_result.get_not_success_results())
        result_type_list = [result.type for result in result_list]
        self.assertEqual(result_type_list,
                         expected_result_types)

    def test_compare_equal_boards_when_expected_board_cached(self):
        expected_board = self.client.get_board("2mhoAmxb")
        mcm_expected = MethodCacheManager(expected_board, [Card, List])
        compare_board = self.client.get_board("Z8ZkJYlR")
        self.assertEqual(
            CompareResultType.SUCCESS,
            self._board_comparer.start_compare(compare_board, mcm_expected).type)

    def test_board_does_not_contain_enough_list_when_expected_board_cached(self):
        self.board_compare_test_with_cache(
            "GdxsVtcc", "E4ew5UjV",
            [CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT])

    def test_board_has_extra_list_when_expected_board_cached(self):
        self.board_compare_test_with_cache(
            "GCDV6cxz", "E4ew5UjV",
            [CompareResultType.FAILED, CompareResultType.EXTRA_ELEMENT])

    def test_empty_board_when_expected_board_cached(self):
        self.board_compare_test_with_cache(
            "qhV58pO0", "E4ew5UjV",
            [CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT,
             CompareResultType.DOES_NOT_CONTAIN_ELEMENT])

    def test_compare_equal_boards_without_cards_when_expected_board_cached(self):
        expected_board = self.client.get_board("E4ew5UjV")
        mcm_expected = MethodCacheManager(expected_board, [Card, List])
        compare_board = self.client.get_board("rK9EgGYp")
        self.assertEqual(
            CompareResultType.SUCCESS,
            self._board_comparer.start_compare(compare_board, mcm_expected).type)

    def test_when_lists_has_different_names_when_expected_board_cached(self):
        self.board_compare_test_with_cache(
            "xvSU42Bj", "E4ew5UjV",
            [CompareResultType.FAILED, CompareResultType.EXTRA_ELEMENT,
             CompareResultType.DOES_NOT_CONTAIN_ELEMENT])


class BoardCompareTestsWhenBothBoardsCached(unittest.TestCase):
    def setUp(self):
        with open(CONFIG_FILE, "r") as file:
            config_data = json.load(file)

        client = TrelloClient(
            api_key=config_data["api_key"],
            token=config_data["token"]
        )
        self._board_comparer = DefaultComparersProvider.create_board_comparer()
        self.client = client

    def board_compare_test_when_both_boards_cached(self, compare_board_id, expected_board_id, expected_result_types):
        compare_board = self.client.get_board(compare_board_id)
        expected_board = self.client.get_board(expected_board_id)
        mcm_expected = MethodCacheManager(expected_board, [Card, List])
        mcm_compare = MethodCacheManager(compare_board, [Card, List])
        compare_result = self._board_comparer.start_compare(mcm_compare, mcm_expected)
        result_list = list(compare_result.get_not_success_results())
        result_type_list = [result.type for result in result_list]
        self.assertEqual(result_type_list,
                         expected_result_types)

    def test_compare_equal_boards_when_both_boards_cached(self):
        expected_board = self.client.get_board("2mhoAmxb")
        mcm_expected = MethodCacheManager(expected_board, [Card, List])
        compare_board = self.client.get_board("Z8ZkJYlR")
        self.assertEqual(
            CompareResultType.SUCCESS,
            self._board_comparer.start_compare(compare_board, mcm_expected).type)

    def test_board_does_not_contain_enough_list_when_both_boards_cached(self):
        self.board_compare_test_when_both_boards_cached(
            "GdxsVtcc", "E4ew5UjV",
            [CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT])

    def test_board_has_extra_list_when_both_boards_cached(self):
        self.board_compare_test_when_both_boards_cached(
            "GCDV6cxz", "E4ew5UjV",
            [CompareResultType.FAILED, CompareResultType.EXTRA_ELEMENT])

    def test_empty_board_when_both_boards_cached(self):
        self.board_compare_test_when_both_boards_cached(
            "qhV58pO0", "E4ew5UjV",
            [CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT,
             CompareResultType.DOES_NOT_CONTAIN_ELEMENT])

    def test_compare_equal_boards_without_cards_when_both_boards_cached(self):
        expected_board = self.client.get_board("E4ew5UjV")
        mcm_expected = MethodCacheManager(expected_board, [Card, List])
        compare_board = self.client.get_board("rK9EgGYp")
        self.assertEqual(
            CompareResultType.SUCCESS,
            self._board_comparer.start_compare(compare_board, mcm_expected).type)

    def test_when_lists_has_different_names_when_both_boards_cached(self):
        self.board_compare_test_when_both_boards_cached(
            "xvSU42Bj", "E4ew5UjV",
            [CompareResultType.FAILED, CompareResultType.EXTRA_ELEMENT,
             CompareResultType.DOES_NOT_CONTAIN_ELEMENT])


if __name__ == '__main__':
    unittest.main()
