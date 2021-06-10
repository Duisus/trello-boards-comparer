import unittest

from classes.method_cache_manager import MethodCacheManager


class TestClass:
    def __init__(self, number):
        self.number = number

    def sum_method(self, summand):
        return self.number + summand

    def subtraction_method(self, deductible):
        return self.number - deductible

    def get_decorate_object(self):
        return TestDecorateClass()

    def get_decorate_objects_list(self):
        return [TestDecorateClass(), TestDecorateClass(), TestDecorateClass()]

    def get_decorate_objects_tuple(self):
        return (TestDecorateClass(), TestDecorateClass(), TestDecorateClass())

    def __getitem__(self, item):
        return item * 3


class TestDecorateClass:
    pass


class MethodCacheManagerTests(unittest.TestCase):

    def setUp(self):
        self.test_obj = TestClass(1)
        self.decorated_obj = MethodCacheManager(self.test_obj, [TestDecorateClass])
        self.argument = 4

    def test_if_method_of_origin_object_change_return_value_cache_is_not_changed(self):
        self.decorated_obj.sum_method(self.argument)
        self.test_obj.number += 10000

        self.assertNotEqual(
            self.decorated_obj.sum_method(self.argument),
            self.test_obj.sum_method(self.argument))

    def test_returns_correct_value_of_method_called_with_different_args(self):
        other_arg = self.argument + 1234
        expected = [self.test_obj.sum_method(self.argument),
                    self.test_obj.sum_method(other_arg)]

        actual = [self.decorated_obj.sum_method(self.argument),
                  self.decorated_obj.sum_method(other_arg)]

        self.assertEqual(expected, actual)

    def test_cache_all_return_values_of_method_called_with_different_args(self):
        other_arg = self.argument + 1234

        cached = [self.decorated_obj.sum_method(self.argument),
                  self.decorated_obj.sum_method(other_arg)]
        self.test_obj.number += 123

        self.assertNotEqual(
            cached,
            [self.test_obj.sum_method(self.argument),
             self.test_obj.sum_method(other_arg)]
        )

    def test_cache_manager_method_return_same_value_as_origin_object(self):
        expected = self.test_obj.sum_method(self.argument)

        actual = self.decorated_obj.sum_method(self.argument)

        self.assertEqual(expected, actual)

    def test_all_called_methods_return_correct_values(self):
        expected = [self.test_obj.sum_method(self.argument),
                    self.test_obj.subtraction_method(self.argument)]

        actual = [self.decorated_obj.sum_method(self.argument),
                  self.decorated_obj.subtraction_method(self.argument)]

        self.assertEqual(expected, actual)

    def test_correct_cache_if_method_is_called_several_times(self):
        expected = self.test_obj.sum_method(self.argument)

        self.decorated_obj.sum_method(self.argument)
        self.decorated_obj.sum_method(self.argument)
        self.decorated_obj.sum_method(self.argument)

        self.assertEqual(expected, self.decorated_obj.sum_method(self.argument))

    def test_if_method_return_obj_of_decorate_type_it_is_decorated_by_cache_manager(self):
        self.assertIsInstance(
            self.decorated_obj.get_decorate_object(),
            MethodCacheManager
        )

    def test_if_return_value_type_is_not_decorate_type_it_is_not_decorated(self):
        assert not isinstance(
            self.decorated_obj.sum_method(self.argument), MethodCacheManager
        )

    def test_all_objects_of_decorate_type_in_tuple_is_decorated_by_cache_manager(self):
        for value in self.decorated_obj.get_decorate_objects_tuple():
            self.assertIsInstance(value, MethodCacheManager)

    def test_all_objects_of_decorate_type_in_list_is_decorated_by_cache_manager(self):
        for value in self.decorated_obj.get_decorate_objects_list():
            self.assertIsInstance(value, MethodCacheManager)

    def test__try_get_attribute_that_not_contains_in_origin_obj__AttributeError_is_raised(self):
        self.assertRaises(
            AttributeError,
            lambda: self.decorated_obj.does_not_have)

    def test__getitem_return_same_result_as_origin_object(self):
        arg = (1, 2, 3)

        self.assertEqual(
            self.test_obj[arg],
            self.decorated_obj[arg])
