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

    def test_compare_equal_boards(self):
        self.assertEqual(CompareResultType.SUCCESS, self._board_comparer.compare_boards("Z8ZkJYlR", "2mhoAmxb").type)

    def test_board_does_not_contain_enough_list(self):
        result_list = list(self._board_comparer.compare_boards("GdxsVtcc", "E4ew5UjV").get_not_success_results())
        result_type_list = []
        for i in result_list:
            result_type_list.append(i.type)
        self.assertEqual([CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT], result_type_list)

    def test_board_has_extra_list(self):
        result_list = list(self._board_comparer.compare_boards("GCDV6cxz", "E4ew5UjV").get_not_success_results())
        result_type_list = []
        for i in result_list:
            result_type_list.append(i.type)
        self.assertEqual([CompareResultType.FAILED, CompareResultType.HAS_EXTRA_ELEMENT], result_type_list)

    @unittest.skip("does not work yet")
    def test_empty_board(self):
        result_list = list(self._board_comparer.compare_boards("qhV58pO0", "E4ew5UjV").get_not_success_results())
        result_type_list = []
        for i in result_list:
            result_type_list.append(i.type)
        self.assertEqual(result_type_list, [CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT,
                                            CompareResultType.DOES_NOT_CONTAIN_ELEMENT])

    def test_compare_equal_boards_without_cards(self):
        self.assertEqual(CompareResultType.SUCCESS, self._board_comparer.compare_boards("rK9EgGYp", "E4ew5UjV").type)
