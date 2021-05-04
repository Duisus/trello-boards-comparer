import unittest
from classes.TrelloBoardComparer import *

class TrelloBoardComparerTests(unittest.TestCase):
    def setUp(self):
        self._trello_client = TrelloClient

    def test_compare_equal_boards(self):
        self.assertEqual(TrelloBoardComparer.compare_boards(self, "Z8ZkJYlR", "2mhoAmxb").type, CompareResultType.SUCCESS)


if __name__ == '__main__':
    unittest.main()
