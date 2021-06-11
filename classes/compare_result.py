from enum import Enum, unique
from typing import *

__all__ = ["CompareResult", "CompareResultType", "TrelloElement"]


@unique
class CompareResultType(Enum):
    SUCCESS = (1, "сравнение успешно")
    FAILED = (2, "не соответствует ожиданиям")
    INVALID_VALUE = (3, "неправильное значение")
    DOES_NOT_CONTAIN_ELEMENT = (4, "нет ожидаемого элемента")
    EXTRA_ELEMENT = (5, "лишний элемент")

    def __init__(self, value, description):
        self._value_ = value
        self.description = description


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
                 result_type: CompareResultType = CompareResultType.SUCCESS):
        self._compared_element = compared_element
        self._type = result_type
        self._compared_element_name = compared_element_name

        self._inner_compare_results = []
        self._expected_value = None
        self._actual_value = None

    @property
    def expected_value(self):
        return self._expected_value

    @property
    def actual_value(self):
        return self._actual_value

    @property
    def inner_results(self):
        return tuple(self._inner_compare_results)

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

    def set_actual_and_expected(self, actual, expected):
        self._actual_value = actual
        self._expected_value = expected

    def add_inner_compare_result(self, compare_result: "CompareResult"):
        if not compare_result.is_success:
            self._type = CompareResultType.FAILED

        self._inner_compare_results.append(compare_result)

    def get_not_success_results(self) -> Generator["CompareResult", None, None]: # todo move to base class for tests
        if self.is_success:
            return

        yield self
        for inner in self._inner_compare_results:
            yield from inner.get_not_success_results()

    def get_results_by_type(self, type: CompareResultType) -> Generator["CompareResult", None, None]:
        if self.type == type:
            yield self

        for inner in self._inner_compare_results:
            yield from inner.get_results_by_type(type)
