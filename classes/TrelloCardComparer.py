from trello import *
from .CompareResult import *
from typing import *
from collections import Counter


class TrelloCardComparer:
    @classmethod
    def compare_cards(cls,
                      card_to_compare: Card,
                      expected_card: Card) -> CompareResult:
        compare_result = CompareResult(TrelloElement.CARD, card_to_compare.name)

        for item in cls._compare_all_checklists(card_to_compare, expected_card):
            compare_result.add_inner_compare_result(item)

        return compare_result

    @classmethod
    def _compare_all_checklists(cls,
                                card_to_compare: Card,
                                expected_card: Card) -> List[CompareResult]:
        compare_results = []

        checklists_to_compare = card_to_compare.checklists
        expected_checklists = expected_card.checklists

        checklists_to_compare_names = (item.name for item in checklists_to_compare)
        expected_checklists_names = (item.name for item in expected_checklists)

        for i in range(len(checklists_to_compare)):
            if checklists_to_compare[i].name not in expected_checklists_names:
                compare_results.append(CompareResult(
                    TrelloElement.CHECKLIST,
                    checklists_to_compare[i].name,
                    CompareResultType.HAS_EXTRA_ELEMENT
                ))

            for j in range(len(expected_checklists)):
                if checklists_to_compare[i].name == expected_checklists[j].name:
                    compare_results.append(
                        cls._compare_checklist(checklists_to_compare[i],
                                               expected_checklists[j])
                    )
                elif expected_checklists[j].name not in checklists_to_compare_names:
                    compare_results.append(CompareResult(
                        TrelloElement.CHECKLIST,
                        expected_checklists[j].name,
                        CompareResultType.DOES_NOT_CONTAIN_ELEMENT
                    ))

        return compare_results

    @classmethod
    def _compare_checklist(cls,
                           checklist_to_compare: Checklist,
                           expected_checklist: Checklist) -> CompareResult:
        compare_result = CompareResult(TrelloElement.CHECKLIST,
                                       checklist_to_compare.name)

        checklist_items_to_compare = checklist_to_compare.items
        expected_checklist_items = expected_checklist.items

        min_length = min(len(checklist_items_to_compare), len(expected_checklist_items))
        max_length = max(len(checklist_items_to_compare), len(expected_checklist_items))

        for i in range(min_length):
            compare_result.add_inner_compare_result(
                cls._compare_checklist_item(checklist_items_to_compare[i],
                                            expected_checklist_items[i]))

        if len(checklist_items_to_compare) > len(expected_checklist_items):
            for i in range(min_length, max_length):
                compare_result.add_inner_compare_result(CompareResult(
                    TrelloElement.CHECKLIST_ITEM,
                    checklist_items_to_compare[i]['name'],
                    CompareResultType.HAS_EXTRA_ELEMENT
                ))

        if len(checklist_items_to_compare) < len(expected_checklist_items):
            for i in range(min_length, max_length):
                compare_result.add_inner_compare_result(CompareResult(
                    TrelloElement.CHECKLIST_ITEM,
                    expected_checklist_items[i]['name'],
                    CompareResultType.DOES_NOT_CONTAIN_ELEMENT
                ))

        return compare_result

    @classmethod
    def _compare_checklist_item(cls,
                                checklist_item_to_compare: Dict,
                                expected_checklist_item: Dict) -> CompareResult:
        compare_result = CompareResult(TrelloElement.CHECKLIST_ITEM,
                                       checklist_item_to_compare['name'])

        if checklist_item_to_compare['checked'] != checklist_item_to_compare['checked']:
            compare_result.add_inner_compare_result(CompareResult(
                TrelloElement.CHECKLIST_ITEM,
                'Маркер',
                CompareResultType.INVALID_VALUE))

            compare_result.expected_value('отмеченый' if expected_checklist_item['checked']
                                          else 'неотмеченый')
            compare_result.actual_value('отмеченный' if checklist_item_to_compare['checked']
                                        else 'неотмеченый')
        else:
            compare_result.add_inner_compare_result(CompareResult(
                TrelloElement.CHECKLIST_ITEM,
                'Маркер'))

        if checklist_item_to_compare['name'] != expected_checklist_item['name']:
            compare_result.add_inner_compare_result(CompareResult(
                TrelloElement.CHECKLIST_ITEM,
                'Элемент чек-листа',
                CompareResultType.INVALID_VALUE))

            compare_result.expected_value(expected_checklist_item['name'])
            compare_result.actual_value(checklist_item_to_compare['name'])
        else:
            compare_result.add_inner_compare_result(CompareResult(
                TrelloElement.CHECKLIST_ITEM,
                'Элемент чек-листа'))

        return compare_result

    @classmethod
    def _compare_description(cls) -> CompareResult:
        pass

    @classmethod
    def _compare_label(cls,
                       labels_to_compare: List[Label],
                       expected_labels: List[Label]) -> List[CompareResult]:
        compare_results = []

        labels_to_compare_colors = (item.color for item in labels_to_compare)
        expected_labels_colors = (item.color for item in expected_labels)

        for compare_color in labels_to_compare_colors:
            if compare_color not in expected_labels_colors:
                compare_results.append(CompareResult(
                    TrelloElement.LABEL,
                    compare_color,
                    CompareResultType.HAS_EXTRA_ELEMENT
                ))
            else:
                compare_results.append(CompareResult(
                    TrelloElement.LABEL,
                    compare_color
                ))

        for expected_color in expected_labels_colors:
            if expected_color not in labels_to_compare_colors:
                compare_results.append(CompareResult(
                    TrelloElement.LABEL,
                    expected_color,
                    CompareResultType.DOES_NOT_CONTAIN_ELEMENT
                ))

        return compare_results

    @classmethod
    def _check_cover(cls) -> CompareResult:
        pass

    @classmethod
    def _check_due(cls) -> CompareResult:
        pass

    @classmethod
    def _check_members(cls) -> CompareResult:
        pass

    @classmethod
    def _check_attachments(cls) -> CompareResult:
        pass
