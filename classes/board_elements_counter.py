from trello import *


__all__ = ["BoardElementsCounter"]


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class BoardElementsCounter:
    @classproperty
    def _elements_in_card(cls):
        return 7

    @classproperty
    def _elements_in_checklist_item(cls):
        return 3

    @classproperty
    def _itself(cls):
        return 1

    @classmethod
    def count(cls, board: Board):
        amount = cls._itself

        for list in board.list_lists(list_filter="open"):
            amount += cls._get_list_elements_amount(list)

        return amount

    @classmethod
    def _get_list_elements_amount(cls, list: "List"):
        amount = cls._itself

        for card in list.list_cards(card_filter="all"):
            amount += cls._get_card_elements_amount(card)

        return amount

    @classmethod
    def _get_card_elements_amount(cls, card: Card):
        amount = cls._elements_in_card + cls._itself

        for checklist in card.checklists:
            amount += cls._itself
            amount += \
                len(checklist.items) * cls._elements_in_checklist_item

        if card.labels is not None:
            amount += len(card.labels)

        return amount
