from enum import Enum, unique
from typing import *

__all__ = ["CompareResult", "CompareResultType", "TrelloElement"]


@unique
class CompareResultType(Enum):
    SUCCESS = (1, "сравнение {name} успешно")
    FAILED = (2, "{name} не соответствует ожиданиям")
    INVALID_VALUE = (3, "{name} содержит другое значение")
    DOES_NOT_CONTAIN_ELEMENT = (4, "нет ожидаемого элемента {name}")
    HAS_EXTRA_ELEMENT = (5, "имеется лишний элемент {name}")

    def __init__(self, value, description_template):
        self._value_ = value
        self.description_template = description_template


@unique
class TrelloElement(Enum):
    BOARD = (1, "доска")
    LIST = (2, "список")
    CARD = (3, "карточка")
    CHECKLIST = (4, "чек-лист")
    CHECKLIST_ITEM = (5, "элемент чек-листа")
    DESCRIPTION = (6, "описание")
    LABEL = (7, "метка")
    DUE = (8, "срок")
    MEMBER = (9, "участник")
    ATTACHMENT = (10, "вложение")
    COVER = (11, "обложка")
    COMMENT = (12, "комментарий")

    def __init__(self, value, element_name):
        self._value_ = value
        self.element_name = element_name


class CompareResult:
    _inner_compare_results: List["CompareResult"]

    def __init__(self,
                 compared_element: TrelloElement,
                 compared_element_name: str = "",
                 compare_result_type: CompareResultType = CompareResultType.SUCCESS):
        self._compared_element = compared_element
        self._type = compare_result_type
        self._compared_element_name = compared_element_name

        self._inner_compare_results = []
        self.expected_value = None
        self.actual_value = None

    @property
    def compared_element(self):
        return self._compared_element

    @property
    def compared_element_name(self):
        return self._compared_element_name

    @property
    def type(self):
        return self._type

    @property
    def is_success(self):
        return self.type is CompareResultType.SUCCESS

    def add_inner_compare_result(self, compare_result: "CompareResult"):
        if not compare_result.is_success:
            self._type = CompareResultType.FAILED

        self._inner_compare_results.append(compare_result)

    def get_not_success_results(self) -> Generator["CompareResult", None, None]:
        if self.is_success:
            return

        yield self
        for inner in self._inner_compare_results:
            yield from inner.get_not_success_results()
