import unittest

from trello import *

from classes.board_compare_counter import *

CONFIG_FILE = r"..\config.json"


class BoardCompareCounterTests(unittest.TestCase):
    def setUp(self):
        with open(CONFIG_FILE, "r") as file:
            config_data = json.load(file)

        self._client = TrelloClient(
            api_key=config_data["api_key"],
            token=config_data["token"]
        )

    def get_board_compare_amount_test(self, board_id):
        board = self._client.get_board(board_id)

        return BoardCompareCounter.get_board_compare_amount(board)

    def test_board_without_cards(self):
        board_id = "rK9EgGYp"
        self.assertEqual(3, self.get_board_compare_amount_test(board_id))

    def test_board_with_empty_cards(self):
        board_id = "wJg6R3Cr"
        self.assertEqual(35, self.get_board_compare_amount_test(board_id))

    def test_board_without_labels_and_checklists_but_not_empty(self):
        board_id = "Z8ZkJYlR"
        self.assertEqual(27, self.get_board_compare_amount_test(board_id))

    def test_board_with_labels(self):
        board_id = "gcWqtT4P"
        self.assertEqual(23, self.get_board_compare_amount_test(board_id))

    def test_board_with_checklists(self):
        board_id = "bFsPh4Ss"
        self.assertEqual(41, self.get_board_compare_amount_test(board_id))

    def test_board_with_labels_and_checklist(self):
        board_id = "ERpuzOKl"
        self.assertEqual(52, self.get_board_compare_amount_test(board_id))
