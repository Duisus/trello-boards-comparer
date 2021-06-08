from trello import *

from ..base_comparers import *
from ..compare_result import TrelloElement

__all__ = ["AttachmentComparer"]


class AttachmentComparer(AvailabilityComparer):

    @property
    def _element_type(self) -> TrelloElement:
        return TrelloElement.ATTACHMENT

    def _has_element(self, card_to_check: Card):
        return len(card_to_check.attachments) != 0
