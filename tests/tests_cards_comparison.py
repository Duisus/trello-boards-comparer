import unittest

from trello import *
from parameterized import parameterized

from classes.compare.compare_result import *
from classes.compare.default_comparers_provider import DefaultComparersProvider

CONFIG_FILE = r"..\config.json"


class TrelloCardComparerTests(unittest.TestCase):
    def setUp(self):
        with open(CONFIG_FILE, "r") as file:
            config_data = json.load(file)

        self._client = TrelloClient(
            api_key=config_data["api_key"],
            token=config_data["token"]
        )

        self.comparer = DefaultComparersProvider.create_card_comparer()

    def card_comparer_test(
            self, compared_card_id, expected_card_id, expected_result=None):
        expected_result = expected_result or []
        compared_card = self._client.get_card(compared_card_id)
        expected_card = self._client.get_card(expected_card_id)

        compare_result = self.comparer.start_compare(compared_card, expected_card)

        result_types = [result.type for result in compare_result.get_not_success_results()]
        self.assertEqual(expected_result, result_types)

    @parameterized.expand([
        ("38Pm4D5y",),
        ("qOt96HfB",
         [CompareResultType.FAILED, CompareResultType.FAILED,
          CompareResultType.FAILED, CompareResultType.INVALID_VALUE,
          CompareResultType.FAILED, CompareResultType.INVALID_VALUE, CompareResultType.INVALID_VALUE,
          CompareResultType.EXTRA_ELEMENT])
    ])
    def test_checklist_items_comparing(self, compared_card_id, expected_result=None):
        expected_card_id = "xXq2tR5U"
        self.card_comparer_test(compared_card_id, expected_card_id, expected_result)

    @parameterized.expand([
        ("UNt8K4Wu",),
        ("uXQGvleB",
         [CompareResultType.FAILED,
          CompareResultType.EXTRA_ELEMENT,
          CompareResultType.DOES_NOT_CONTAIN_ELEMENT])
    ])
    def test_checklists_comparing(self, compared_card_id, expected_result=None):
        expected_card_id = "0MdRCgTy"
        self.card_comparer_test(compared_card_id, expected_card_id, expected_result)

    @parameterized.expand([
        ("8LpNCzDa",),
        ("havOVdMx",
         [CompareResultType.FAILED, CompareResultType.INVALID_VALUE])
    ])
    def test_description_with_link_comparing(self, compared_card_id, expected_result=None):
        expected_card_id = "gl6IqA7c"
        self.card_comparer_test(compared_card_id, expected_card_id, expected_result)

    @parameterized.expand([
        ("2Hx23sXX",),
        ("jnd0PbWY", [CompareResultType.FAILED, CompareResultType.INVALID_VALUE])
    ])
    def test_mention_in_comments_comparing(self, compared_card_id, expected_result=None):
        expected_card_id = "jo8qijTo"
        self.card_comparer_test(compared_card_id, expected_card_id, expected_result)

    @parameterized.expand([
        ("YldYBOxa",),
        ("I9z6krUS", [CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT])
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

    @parameterized.expand([
        ("fGSFx7h9",),
        ("0CbCb036", [CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT])
    ])
    def test_cover_in_cards(self, compared_card_id, expected_result=None):
        expected_cards_id = "vvEBx3nm"
        self.card_comparer_test(compared_card_id, expected_cards_id, expected_result)

    @parameterized.expand([
        ("dS3oWEx9",),
        ("EEhz0a7l",
         [CompareResultType.FAILED,
          CompareResultType.EXTRA_ELEMENT,
          CompareResultType.DOES_NOT_CONTAIN_ELEMENT])
    ])
    def test_compare_label_in_cards(self, compared_card_id, expected_result=None):
        expected_cards_id = "A9Z6CrJF"
        self.card_comparer_test(compared_card_id, expected_cards_id, expected_result)

    @parameterized.expand([
        ("809GQr9b",),
        ("oy9DktBm", [CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT])
    ])
    def test_check_due_in_cards(self, compared_card_id, expected_result=None):
        expected_cards_id = "mmaACkHa"
        self.card_comparer_test(compared_card_id, expected_cards_id, expected_result)

    @parameterized.expand([
        ("1aEjgmDJ",),
        ("kh7wgpqW", [CompareResultType.FAILED, CompareResultType.DOES_NOT_CONTAIN_ELEMENT])
    ])
    def test_check_member_in_cards(self, compared_card_id, expected_result=None):
        expected_cards_id = "AJNZsT8W"
        self.card_comparer_test(compared_card_id, expected_cards_id, expected_result)

    def test_comparer_equal_complex_cards(self):
        self.card_comparer_test("2l4SfS5E", "jrpqIHyO")

    @parameterized.expand([
        ("jnd0PbWY",
         [
             CompareResultType.FAILED,  # card result
             CompareResultType.DOES_NOT_CONTAIN_ELEMENT,  # checklist result
             CompareResultType.INVALID_VALUE,  # description result
             CompareResultType.DOES_NOT_CONTAIN_ELEMENT,  # labels result
             CompareResultType.DOES_NOT_CONTAIN_ELEMENT,  # cover result
             CompareResultType.DOES_NOT_CONTAIN_ELEMENT,  # due result
             CompareResultType.DOES_NOT_CONTAIN_ELEMENT,  # members result
             CompareResultType.DOES_NOT_CONTAIN_ELEMENT,  # attachments result
         ])
    ])
    def test_functionality(self, compared_card_id, expected_result=None):
        expected_cards_id = "2l4SfS5E"
        self.card_comparer_test(compared_card_id, expected_cards_id, expected_result)