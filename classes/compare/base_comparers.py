import typing
from abc import ABC, abstractmethod

from trello import *

from .compare_result import *

__all__ = ["BaseComparer", "BaseCollectionComparer", "AvailabilityComparer"]


class BaseComparer(ABC):

    def __init__(self, inner_comparers: typing.List["BaseComparer"] = None):
        self._inner_comparers = inner_comparers or []

    def start_compare(self, actual, expected) -> CompareResult:
        result = self._current_compare(actual, expected)

        for comparer in self._inner_comparers:
            inner_result = comparer.start_compare(actual, expected)
            if type(inner_result) is list:  # todo REFACTOR
                for inner in inner_result:
                    result.add_inner_compare_result(inner)
            else:
                result.add_inner_compare_result(inner_result)

        return result

    @abstractmethod
    def _current_compare(self, actual, expected) -> CompareResult:  # todo change with Union
        pass


# TODO мб вынести сюда компаратор для коллекций,
## от которого будут наследоваться компараторы листов, карточек и т.д.
## Здесь же наверное будет код который помечен тудушкой: "Вынести в абстрактный класс"
class BaseCollectionComparer(BaseComparer, ABC):

    def __init__(self, element_comparer: BaseComparer,
                 inner_comparers: typing.List["BaseComparer"] = None):
        super().__init__(inner_comparers)
        self._element_comparer = element_comparer

    def _compare_elements(self, actual_element, expected_element):
        return self._element_comparer.start_compare(actual_element, expected_element)


class AvailabilityComparer(BaseComparer, ABC):  # todo Maybe is ExistenceComparer, rename?

    def _current_compare(self, actual: Card, expected: Card) -> CompareResult:
        if self._has_element(actual) == self._has_element(expected):
            return CompareResult(self._element_type)

        elif self._has_element(expected):
            return CompareResult(
                self._element_type,
                result_type=CompareResultType.DOES_NOT_CONTAIN_ELEMENT)

        return CompareResult(
            self._element_type,
            result_type=CompareResultType.EXTRA_ELEMENT)

    @abstractmethod
    def _has_element(self, card_to_check: Card):
        pass

    @property
    @abstractmethod
    def _element_type(self) -> TrelloElement:
        pass
