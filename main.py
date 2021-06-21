from trello import *

from classes import method_cache_manager, render
from classes.compare import default_comparers_provider
from classes.mark_calculation import board_elements_counter, mark_calculator

CONFIG_FILE = "config.json"


def checktrellolab(board_id_actual):
    with open(CONFIG_FILE, "r") as file:
        config_data = json.load(file)

    client = TrelloClient(
        api_key=config_data["api_key"],
        token=config_data["token"]
    )

    board_actual = client.get_board(board_id_actual)
    board_id_expected = "E4ew5UjV"  # хардкод (temporary)
    board_expected = client.get_board(board_id_expected)
    mcm_expected = method_cache_manager.MethodCacheManager(board_expected)
    comparer = default_comparers_provider.DefaultComparersProvider.create_board_comparer()
    compare_result = comparer.start_compare(board_actual, mcm_expected)
    num_of_checks = board_elements_counter.BoardElementsCounter.count(mcm_expected)
    grade = mark_calculator.MarkCalculator.calculate(num_of_checks, compare_result)
    render.get_report(compare_result, grade)

    return {grade, render.get_report(compare_result, grade)}
