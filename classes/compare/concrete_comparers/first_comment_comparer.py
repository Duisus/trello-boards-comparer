import re
import typing

from trello import *

from ..base_comparers import *
from ..compare_result import *

__all__ = ["FirstCommentComparer"]


class FirstCommentComparer(BaseComparer):
    _member_mention_re = re.compile(r"@[a-zA-Z0-9_]+")

    def _current_compare(self, actual: Card, expected: Card) -> CompareResult:
        actual_comments = self._get_comments(actual)
        expected_comments = self._get_comments(expected)

        if len(expected_comments) == 0 and len(actual_comments) != 0:
            return CompareResult(
                TrelloElement.COMMENT,
                result_type=CompareResultType.EXTRA_ELEMENT)
        elif len(expected_comments) != 0 and len(actual_comments) == 0:
            return CompareResult(
                TrelloElement.COMMENT,
                result_type=CompareResultType.DOES_NOT_CONTAIN_ELEMENT)
        elif len(expected_comments) == 0 and len(actual_comments) == 0:
            return CompareResult(TrelloElement.COMMENT)

        expected_first_comment = expected_comments[0]
        actual_first_comment = actual_comments[0]

        if self._comment_has_mention(expected_first_comment):
            if self._comment_has_mention(actual_first_comment):
                return CompareResult(TrelloElement.COMMENT)

            return CompareResult(
                TrelloElement.COMMENT,
                "нет упоминания",
                CompareResultType.INVALID_VALUE)

        if expected_first_comment != actual_first_comment:
            result = CompareResult(
                TrelloElement.COMMENT,
                result_type=CompareResultType.INVALID_VALUE)
            result.set_actual_and_expected(
                actual_first_comment, expected_first_comment)

            return result

        return CompareResult(TrelloElement.COMMENT)

    @staticmethod
    def _get_comments(card: Card) -> typing.List[str]:
        return [comment_data['data']['text'].strip() for comment_data in card.comments]

    @classmethod
    def _comment_has_mention(cls, comment: str):
        return cls._member_mention_re.search(comment) is not None
