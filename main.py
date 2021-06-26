from trello import *

from classes.method_cache_manager import MethodCacheManager
from classes.render import get_report
from classes.compare.default_comparers_provider import DefaultComparersProvider
from classes.mark_calculation.board_elements_counter import BoardElementsCounter
from classes.mark_calculation.mark_calculator import MarkCalculator

CONFIG_FILE = "config.json"


def check_trello_lab(board_id_actual, board_id_expected):
    with open(CONFIG_FILE, "r") as file:
        config_data = json.load(file)

    client = TrelloClient(
        api_key=config_data["api_key"],
        token=config_data["token"]
    )

    board_actual = client.get_board(board_id_actual)
    board_expected = client.get_board(board_id_expected)
    mcm_expected = MethodCacheManager(board_expected)
    comparer = DefaultComparersProvider.create_board_comparer()
    compare_result = comparer.start_compare(board_actual, mcm_expected)
    num_of_checks = BoardElementsCounter.count(mcm_expected)
    grade = MarkCalculator.calculate(num_of_checks, compare_result)

    return grade, get_report(compare_result, grade)
