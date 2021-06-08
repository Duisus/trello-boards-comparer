from trello import TrelloClient

from .concrete_comparers.archive_status_comparer import ArchiveStatusComparer
from .concrete_comparers.attachment_comparer import AttachmentComparer
from .concrete_comparers.board_comparer import BoardComparer
from .concrete_comparers.card_comparer import CardComparer
from .concrete_comparers.checklist_collection_comparer import ChecklistCollectionComparer
from .concrete_comparers.checklist_comparer import ChecklistComparer
from .concrete_comparers.checklist_item_comparer import ChecklistItemComparer
from .concrete_comparers.cover_comparer import CoverComparer
from .concrete_comparers.description_comparer import DescriptionComparer
from .concrete_comparers.due_comparer import DueComparer
from .concrete_comparers.first_comment_comparer import FirstCommentComparer
from .concrete_comparers.label_comparer import LabelComparer
from .concrete_comparers.list_collection_comparer import ListCollectionComparer
from .concrete_comparers.list_comparer import ListComparer
from .concrete_comparers.members_comparer import MembersComparer


class DefaultComparersProvider:

    @classmethod
    def create_board_comparer(cls, trello_client: TrelloClient):
        return BoardComparer(trello_client, [cls.create_lists_comparer()])

    @classmethod
    def create_lists_comparer(cls):
        list_comparer = ListComparer(
            cls.create_card_comparer())
        return ListCollectionComparer(list_comparer)

    @classmethod
    def create_card_comparer(cls):
        checklist_collection_comparer = ChecklistCollectionComparer(
            ChecklistComparer(ChecklistItemComparer()))

        return CardComparer([
            ArchiveStatusComparer(), checklist_collection_comparer,
            DescriptionComparer(), FirstCommentComparer(),
            LabelComparer(), CoverComparer(),
            DueComparer(), MembersComparer(),
            AttachmentComparer()
        ])
