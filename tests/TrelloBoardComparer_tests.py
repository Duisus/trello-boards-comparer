import unittest

from trello import *

from classes.TrelloBoardComparer import *
from classes.CompareResult import *


CONFIG_FILE = r"..\config.json"


class TrelloBoardComparerTests(unittest.TestCase):
    def setUp(self):
        with open(CONFIG_FILE, "r") as file:
            config_data = json.load(file)

        client = TrelloClient(
            api_key=config_data["api_key"],
            token=config_data["token"]
        )

        self._board_comparer = TrelloBoardComparer(client)

    def board_compare_test(self, compared_board_id, expected_board_id, expected_result_types):
        compare_result = self._board_comparer.compare_boards(compared_board_id, expected_board_id)
        result_list = list(compare_result.get_not_success_results())
        result_type_list = [result.type for result in result_list]

        self.assertEqual(expected_result_types, result_type_list)

    def test_compare_equal_boards(self):
        self.assertEqual(CompareResultType.SUCCESS, self._board_comparer.compare_boards("Z8ZkJYlR", "2mhoAmxb").type)

    def test_board_does_not_contain_enough_list(self):
        self.board_compare_test("GdxsVtcc", "E4ew5UjV",
                                [CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT])

    def test_board_has_extra_list(self):
        self.board_compare_test("GCDV6cxz", "E4ew5UjV",
                                [CompareResultType.FAILED, CompareResultType.HAS_EXTRA_ELEMENT])

    def test_empty_board(self):
        self.board_compare_test("qhV58pO0", "E4ew5UjV", [CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT,
                                            CompareResultType.DOES_NOT_CONTAIN_ELEMENT])

    def test_compare_equal_boards_without_cards(self):
        self.assertEqual(CompareResultType.SUCCESS, self._board_comparer.compare_boards("rK9EgGYp", "E4ew5UjV").type)

    def test_when_lists_has_different_names(self):
        self.board_compare_test("xvSU42Bj", "E4ew5UjV", [CompareResultType.FAILED, CompareResultType.HAS_EXTRA_ELEMENT,
                          CompareResultType.DOES_NOT_CONTAIN_ELEMENT])

