from trello import *

from ..base_comparers import *

__all__ = ["CoverComparer"]

from ..compare_result import TrelloElement


class CoverComparer(AvailabilityComparer):

    @property
    def _element_type(self) -> TrelloElement:
        return TrelloElement.COVER

    def _has_element(self, card_to_check: Card):
        return card_to_check._json_obj['cover']['idUploadedBackground'] is not None
