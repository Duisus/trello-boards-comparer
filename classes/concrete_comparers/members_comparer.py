from trello import *

from ..base_comparers import *

__all__ = ["MembersComparer"]

from ..compare_result import TrelloElement


class MembersComparer(AvailabilityComparer):

    @property
    def _element_type(self) -> TrelloElement:
        return TrelloElement.MEMBER

    def _has_element(self, card_to_check: Card):
        return len(card_to_check.member_id) != 0
