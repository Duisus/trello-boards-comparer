from enum import Enum, unique
from typing import *


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
    LIST = (2, "колонка")
    CARD = (3, "карточка")
    CHECKLIST = (4, "чек-лист")
    CHECKLIST_ITEM = (5, "элемент чек-листа")
    DESCRIPTION = (6, "описание")
    LABEL = (7, "метка")
    DUE = (8, "срок")
    MEMBER = (9, "участник")
    ATTACHMENT = (10, "вложение")
    COVER = (11, "обложка")

    def __init__(self, value, element_name):
        self._value_ = value
        self.element_name = element_name


class CompareResult:
    def __init__(self,
                 compared_element: TrelloElement,
                 compared_element_name: str = "",
                 compare_result_type: CompareResultType = CompareResultType.SUCCESS):
        self.compared_element = compared_element
        self.type = compare_result_type
        self.compared_element_name = compared_element_name

    def add_inner_compare_result(self, compare_result: "CompareResult"):
        pass
