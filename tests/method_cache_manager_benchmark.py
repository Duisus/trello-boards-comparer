from trello import *

from classes.compare.default_comparers_provider import DefaultComparersProvider
from classes.method_cache_manager import MethodCacheManager

CONFIG_FILE = r"..\config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)

client = TrelloClient(
    api_key=config_data["api_key"],
    token=config_data["token"]
)


def benchmark(iters):
    def actual_decorator(func):
        import time

        def wrapper(*args, **kwargs):
            for i in range(5):
                func(*args, **kwargs)
            total = 0
            for i in range(iters):
                start = time.time()
                return_value = func(*args, **kwargs)
                end = time.time()
                total = total + (end - start)
            print('{} среднее время выполнения: {} секунд.'.format(func.__name__, total / iters))
            return return_value

        return wrapper

    return actual_decorator


def board_compare_test_with_cache(compare_board_id, expected_board_id):
    compare_board = client.get_board(compare_board_id)
    expected_board = client.get_board(expected_board_id)
    mcm_expected = MethodCacheManager(expected_board, [Card, List])
    mcm_compare = MethodCacheManager(compare_board, [Card, List])
    compare = DefaultComparersProvider.create_board_comparer()
    compare_result = compare.start_compare(mcm_compare, mcm_expected)
    result_list = list(compare_result.get_not_success_results())
    result_type_list = [result.type for result in result_list]
    return result_type_list


@benchmark(50)
def test_compare_equal_boards_with_cache():
    expected_board = client.get_board("2mhoAmxb")
    mcm_expected = MethodCacheManager(expected_board, [Card, List])
    compare_board = client.get_board("Z8ZkJYlR")
    compare = DefaultComparersProvider.create_board_comparer()
    compare_result = compare.start_compare(compare_board, mcm_expected).type


@benchmark(50)
def test_board_does_not_contain_enough_list_with_cache():
    compare_result = board_compare_test_with_cache("GdxsVtcc", "E4ew5UjV")


@benchmark(50)
def test_board_has_extra_list_with_cache():
    compare_result = board_compare_test_with_cache("GCDV6cxz", "E4ew5UjV")


@benchmark(50)
def test_empty_board_with_cache():
    compare_result = board_compare_test_with_cache("qhV58pO0", "E4ew5UjV")


@benchmark(50)
def test_compare_equal_boards_without_cards_with_cache():
    expected_board = client.get_board("E4ew5UjV")
    mcm_expected = MethodCacheManager(expected_board, [Card, List])
    compare_board = client.get_board("rK9EgGYp")
    compare = DefaultComparersProvider.create_board_comparer()
    compare_result = compare.start_compare(compare_board, mcm_expected).type


@benchmark(50)
def test_when_lists_has_different_names_with_cache():
    compare_result = board_compare_test_with_cache("xvSU42Bj", "E4ew5UjV")


def board_compare_test(compared_board_id, expected_board_id):
    compare = DefaultComparersProvider.create_board_comparer_using_id(client)
    compare_result = compare.start_compare(compared_board_id, expected_board_id)
    result_list = list(compare_result.get_not_success_results())
    result_type_list = [result.type for result in result_list]
    return result_type_list


@benchmark(50)
def test_compare_equal_boards():
    compare = DefaultComparersProvider.create_board_comparer_using_id(client)
    compare_result = compare.start_compare("Z8ZkJYlR", "2mhoAmxb").type


@benchmark(50)
def test_board_does_not_contain_enough_list():
    result = board_compare_test("GdxsVtcc", "E4ew5UjV")


@benchmark(50)
def test_board_has_extra_list():
    result = board_compare_test("GCDV6cxz", "E4ew5UjV")


@benchmark(50)
def test_empty_board():
    result = board_compare_test("qhV58pO0", "E4ew5UjV")


@benchmark(50)
def test_compare_equal_boards_without_cards():
    compare = DefaultComparersProvider.create_board_comparer_using_id(client)
    compare_result = compare.start_compare("rK9EgGYp", "E4ew5UjV").type


@benchmark(50)
def test_when_lists_has_different_names():
    result = board_compare_test("xvSU42Bj", "E4ew5UjV")


test_compare_equal_boards_with_cache()
test_compare_equal_boards()

test_board_does_not_contain_enough_list_with_cache()
test_board_does_not_contain_enough_list()

test_board_has_extra_list_with_cache()
test_board_has_extra_list()

test_empty_board_with_cache()
test_empty_board()

test_compare_equal_boards_without_cards_with_cache()
test_compare_equal_boards_without_cards()

test_when_lists_has_different_names_with_cache()
test_when_lists_has_different_names()
