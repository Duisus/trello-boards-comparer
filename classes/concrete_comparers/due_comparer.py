from trello import *

from ..base_comparers import *

__all__ = ["DueComparer"]

from ..compare_result import TrelloElement


class DueComparer(AvailabilityComparer):

    @property
    def _element_type(self) -> TrelloElement:
        return TrelloElement.DUE

    def _has_element(self, card_to_check: Card):
        return card_to_check.due != "" and card_to_check.due is not None
