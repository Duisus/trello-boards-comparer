import unittest

from trello import *

from classes.TrelloBoardComparer import *


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
