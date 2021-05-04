import unittest

from trello import *
from parameterized import parameterized

from classes.CompareResult import *
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

    @parameterized.expand([
        ("2Hx23sXX",),
        ("jnd0PbWY", [CompareResultType.FAILED, CompareResultType.INVALID_VALUE])
    ])
    def test_mention_in_comments(self, compared_card_id, expected_result=None):
        expected_card_id = "jo8qijTo"
        self.card_comparer_test(compared_card_id, expected_card_id, expected_result)

    @parameterized.expand([
        ("YldYBOxa",),
        ("I9z6krUS", [CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT,
                      CompareResultType.HAS_EXTRA_ELEMENT])
    ])
    def test_card_has_attachments(self, compared_card_id, expected_result=None):
        expected_card_id = "3lS576gC"
        self.card_comparer_test(compared_card_id, expected_card_id, expected_result)

    @parameterized.expand([
        ("REjsydqK",),
        ("AAAeeUAw", [CompareResultType.FAILED, CompareResultType.INVALID_VALUE])
    ])
    def test_card_was_archived(self, compared_card_id, expected_result=None):
        expected_card_id = "BnBcwd5E"
        self.card_comparer_test(compared_card_id, expected_card_id, expected_result)

    @parameterized.expand([
        ("ZCugeiMP",),
        ("CFwMzfS1", [CompareResultType.FAILED, CompareResultType.INVALID_VALUE])
    ])
    def test_description_without_link(self, compared_card_id, expected_result=None):
        expected_card_id = "RShk1cfR"
        self.card_comparer_test(compared_card_id, expected_card_id, expected_result)

    @parameterized.expand([
        ("hNgThNym",),
        ("ytmkj5qE", [CompareResultType.FAILED, CompareResultType.INVALID_VALUE])
    ])
    def test_comment_without_mentions(self, compared_card_id, expected_result=None):
        expected_card_id = "jtv2DrFZ"
        self.card_comparer_test(compared_card_id, expected_card_id, expected_result)

    def test_comparer_equal_card(self):
        self.card_comparer_test("2l4SfS5E", "jrpqIHyO")
