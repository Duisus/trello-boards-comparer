import unittest

from trello import *

from classes.board_elements_counter import *
from classes.mark_calculator import *
from classes.TrelloBoardComparer import *

CONFIG_FILE = r"..\config.json"


class MarkCalculatorTests(unittest.TestCase):
    def setUp(self):
        with open(CONFIG_FILE, "r") as file:
            config_data = json.load(file)

        self._client = TrelloClient(
            api_key=config_data["api_key"],
            token=config_data["token"]
        )

    def calculate_mark(self, expected_board_id, actual_board_id):
        expected_board = self._client.get_board(expected_board_id)

        compare_amount = BoardElementsCounter.count(expected_board)

        compare_result = TrelloBoardComparer(self._client).compare_boards(actual_board_id, expected_board_id)

        compare_mark = MarkCalculator.calculate(compare_amount, compare_result)

        return compare_mark

    def test_same_board(self):
        board_id = "8JvX2Rw7"
        self.assertEqual(100, self.calculate_mark(board_id, board_id))

    def test_board_has_extra_element(self):
        expected_board_id = "E4ew5UjV"
        actual_board_id = "GCDV6cxz"
        self.assertEqual(67, self.calculate_mark(expected_board_id, actual_board_id))

    def test_does_not_contain_checklist(self):
        expected_board_id = "ERpuzOKl"
        actual_board_id = "5FKYgQ1m"
        self.assertEqual(75, self.calculate_mark(expected_board_id, actual_board_id))

    def test_does_not_contain_labels(self):
        expected_board_id = "ERpuzOKl"
        actual_board_id = "3DAQjIdM"
        self.assertEqual(98, self.calculate_mark(expected_board_id, actual_board_id))

    def test_does_not_contain_checklist_items(self):
        expected_board_id = "ERpuzOKl"
        actual_board_id = "Mu2PHTu1"
        self.assertEqual(88, self.calculate_mark(expected_board_id, actual_board_id))

    def test_functionality(self):
        expected_board_id = "ERpuzOKl"
        actual_board_id = "OdRRYJK4"
        self.assertEqual(50, self.calculate_mark(expected_board_id, actual_board_id))
