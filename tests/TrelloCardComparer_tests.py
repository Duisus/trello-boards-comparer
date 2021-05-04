import unittest

from trello import *

from classes.TrelloCardComparer import *

CONFIG_FILE = r"..\config.json"


class TrelloCardComparerTests(unittest.TestCase):
    def setUp(self):
        with open(CONFIG_FILE, "r") as file:
            config_data = json.load(file)

        self._client = TrelloClient(
            api_key=config_data["api_key"],
            token=config_data["token"]
        )

    def card_comparer_test(
            self, compared_card_id, expected_card_id, expected_result=None):
        expected_result = expected_result or []
        compared_card = self._client.get_card(compared_card_id)
        expected_card = self._client.get_card(expected_card_id)

        compare_result = TrelloCardComparer.compare_cards(compared_card, expected_card)

        result_types = [result.type for result in compare_result.get_not_success_results()]
        self.assertEqual(expected_result, result_types)
