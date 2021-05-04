import typing
import re

from trello import *

from .CompareResult import *


__all__ = ["TrelloCardComparer"]


class TrelloCardComparer:
    _text_link_re = re.compile(r"\[.+]\(\S+\)")
    _mention_member_re = re.compile(r"@[a-zA-Z0-9_]+")

    @classmethod
    def compare_cards(cls,
                      card_to_compare: Card,
                      expected_card: Card) -> CompareResult:
        compare_result = CompareResult(TrelloElement.CARD, card_to_compare.name)

        for result in cls._compare_all_checklists(card_to_compare, expected_card):
            compare_result.add_inner_compare_result(result)

        compare_result.add_inner_compare_result(
            cls._compare_description(
                card_to_compare.description, expected_card.description))

        compare_result.add_inner_compare_result(
            cls._compare_comments(
                cls._get_comments(card_to_compare),
                cls._get_comments(expected_card)))

        for result in cls._compare_label(card_to_compare.labels, expected_card.labels):
            compare_result.add_inner_compare_result(result)

        compare_result.add_inner_compare_result(
            cls._compare_cover(card_to_compare, expected_card))

        compare_result.add_inner_compare_result(
            cls._compare_due(card_to_compare, expected_card))

        compare_result.add_inner_compare_result(
            cls._compare_members(card_to_compare, expected_card))

        compare_result.add_inner_compare_result(
            cls._compare_attachments(card_to_compare, expected_card))

        return compare_result

    @classmethod
    def _get_comments(cls, card: Card) -> typing.List[str]:
        return [comment_data['data']['text'] for comment_data in card.comments]

    @classmethod
    def _compare_all_checklists(cls,
                                card_to_compare: Card,
                                expected_card: Card) -> typing.List[CompareResult]:
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

        for expected_checklist in expected_checklists:
            if expected_checklist.name not in checklists_to_compare_names:
                compare_results.append(CompareResult(
                    TrelloElement.CHECKLIST,
                    expected_checklist.name,
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
                                checklist_item_to_compare: typing.Dict,
                                expected_checklist_item: typing.Dict) -> CompareResult:
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
    def _compare_description(cls,
                             description_to_compare: str,
                             expected_description: str) -> CompareResult:
        expected_description_without_link = cls._text_link_re.sub(' ', expected_description)
        actual_description_without_link = cls._text_link_re.sub(' ', description_to_compare)

        if expected_description_without_link != actual_description_without_link:
            result = CompareResult(TrelloElement.DESCRIPTION,
                                   compare_result_type=CompareResultType.INVALID_VALUE)
            result.expected_value = expected_description
            result.actual_value = description_to_compare
            return result

        return CompareResult(TrelloElement.DESCRIPTION)

    @classmethod
    def _compare_comments(cls,  # TODO fix (strange logic)
                          comments_to_compare: typing.List[str],
                          expected_comments: typing.List[str]):
        if len(expected_comments) == 0 and len(comments_to_compare) != 0:
            return CompareResult(
                TrelloElement.COMMENT, compare_result_type=CompareResultType.HAS_EXTRA_ELEMENT)
        elif len(expected_comments) != 0 and len(comments_to_compare) == 0:
            return CompareResult(
                TrelloElement.COMMENT, compare_result_type=CompareResultType.DOES_NOT_CONTAIN_ELEMENT)
        elif len(expected_comments) == 0 and len(comments_to_compare) == 0:
            return CompareResult(TrelloElement.COMMENT)

        expected_first_comment = expected_comments[0]
        actual_first_comment = comments_to_compare[0]

        if cls._comment_has_mention(expected_first_comment):
            if cls._comment_has_mention(actual_first_comment):
                return CompareResult(TrelloElement.COMMENT)

            return CompareResult(
                TrelloElement.COMMENT,
                "нет упоминания",
                CompareResultType.DOES_NOT_CONTAIN_ELEMENT)

        return CompareResult(TrelloElement.COMMENT)

    @classmethod
    def _compare_label(cls,
                       labels_to_compare: typing.List[Label],
                       expected_labels: typing.List[Label]) -> typing.List[CompareResult]:
        compare_results = []

        if labels_to_compare is None and expected_labels is None:
            return compare_results

        elif labels_to_compare is None:
            for label in expected_labels:
                compare_results.append(CompareResult(
                    TrelloElement.LABEL,
                    label.color,
                    CompareResultType.DOES_NOT_CONTAIN_ELEMENT
                ))

            return compare_results

        elif expected_labels is None:
            for label in labels_to_compare:
                compare_results.append(CompareResult(
                    TrelloElement.LABEL,
                    label.color,
                    CompareResultType.HAS_EXTRA_ELEMENT
                ))

            return compare_results

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
    def _compare_cover(cls,
                       card_to_compare: Card,
                       expected_card: Card):
        return cls._compare_availability(
            card_to_compare, expected_card, TrelloElement.COVER, cls._has_cover)

    @classmethod
    def _compare_due(cls,
                     card_to_compare: Card,
                     expected_card: Card):
        return cls._compare_availability(
            card_to_compare, expected_card, TrelloElement.DUE, cls._has_due)

    @classmethod
    def _compare_members(cls,
                         card_to_compare: Card,
                         expected_card: Card):
        return cls._compare_availability(
            card_to_compare, expected_card, TrelloElement.MEMBER, cls._has_member)

    @classmethod
    def _compare_attachments(cls,
                             card_to_compare: Card,
                             expected_card: Card):
        return cls._compare_availability(
            card_to_compare, expected_card, TrelloElement.ATTACHMENT, cls._has_attachment)

    @classmethod
    def _compare_availability(cls,
                              card_to_compare: Card,
                              expected_card: Card,
                              element: TrelloElement,
                              check_availability_func) -> CompareResult:
        if check_availability_func(card_to_compare) == check_availability_func(expected_card):
            return CompareResult(element)

        elif check_availability_func(card_to_compare):
            return CompareResult(
                element,
                compare_result_type=CompareResultType.DOES_NOT_CONTAIN_ELEMENT)

        return CompareResult(
            element,
            compare_result_type=CompareResultType.HAS_EXTRA_ELEMENT)

    @classmethod
    def _has_cover(cls, card: Card) -> bool:
        return card._json_obj['cover']['idUploadedBackground'] is not None

    @classmethod
    def _has_due(cls, card: Card) -> bool:
        return card.due is not None

    @classmethod
    def _has_member(cls, card: Card) -> bool:
        return len(card.member_id) != 0

    @classmethod
    def _has_attachment(cls, card: Card) -> bool:
        return len(card.attachments) != 0

    @classmethod
    def _comment_has_mention(cls, comment: str):
        return cls._mention_member_re.search(comment) is not None
