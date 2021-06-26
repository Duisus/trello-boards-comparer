from trello import *

from ..base_comparers import *
from ..compare_result import *

__all__ = ["LabelComparer"]


class LabelComparer(BaseComparer):  # todo BaseCollectionComparer?

    def _current_compare(self, actual: Card,
                         expected: Card) -> CompareResult:
        actual_labels = actual.labels
        expected_labels = expected.labels
        compare_results = []

        if actual_labels is None and expected_labels is None:
            return compare_results

        elif actual_labels is None:
            for label in expected_labels:
                compare_results.append(CompareResult(
                    TrelloElement.LABEL,
                    label.color,
                    CompareResultType.DOES_NOT_CONTAIN_ELEMENT
                ))

            return compare_results

        elif expected_labels is None:
            for label in actual_labels:
                compare_results.append(CompareResult(
                    TrelloElement.LABEL,
                    label.color,
                    CompareResultType.EXTRA_ELEMENT
                ))

            return compare_results

        labels_to_compare_colors = [item.color for item in actual_labels]
        expected_labels_colors = [item.color for item in expected_labels]

        for compare_color in labels_to_compare_colors:
            if compare_color not in expected_labels_colors:
                compare_results.append(CompareResult(
                    TrelloElement.LABEL,
                    compare_color,
                    CompareResultType.EXTRA_ELEMENT
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
