from trello import *


__all__ = ["BoardCompareCounter"]


class BoardCompareCounter:
    _element_to_compare_in_card = 8
    _element_to_compare_in_checklist_item = 3

    @classmethod
    def get_board_compare_amount(cls, board: Board):
        amount = 1

        for list in board.list_lists(list_filter="open"):
            amount += cls._get_list_compare_amount(list)

        return amount

    @classmethod
    def _get_list_compare_amount(cls, list: "List"):
        amount = 1

        for card in list.list_cards(card_filter="all"):
            amount += cls._get_card_compare_amount(card)

        return amount

    @classmethod
    def _get_card_compare_amount(cls, card: Card):
        amount = cls._element_to_compare_in_card

        for checklist in card.checklists:
            amount += \
                len(checklist.items) * cls._element_to_compare_in_checklist_item + 1

        if card.labels is not None:
            amount += len(card.labels)

        return amount
