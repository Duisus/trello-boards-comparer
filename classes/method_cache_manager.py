class MethodCacheManager:
    def __init__(self, target_obj, decorate_types=None):
        self.__target_obj = target_obj
        self.__cache = {}
        self.__decorate_types = decorate_types or []

    def __getattr__(self, name):
        attribute = getattr(self.__target_obj, name)
        if hasattr(attribute, "__call__"):
            return self.__get_decorated_method(attribute, name)

        return attribute

    def __get_decorated_method(self, method, name):
        def decorator(*args, **kwargs):
            key = self.__get_key(name, *args, **kwargs)
            if key in self.__cache:
                return self.__cache[key]

            result = self.__get_return_value(method(*args, **kwargs))
            self.__cache[key] = result
            return result

        return decorator

    def __get_return_value(self, value):
        if type(value) in self.__decorate_types:
            return MethodCacheManager(value, self.__decorate_types)

        if isinstance(value, (list, tuple)):
            value = self.__decorate_collection_values(value)

        return value

    def __decorate_collection_values(self, collection):
        decorated_values = list(collection)

        for i in range(len(decorated_values)):
            if type(decorated_values[i]) in self.__decorate_types:
                decorated_values[i] = MethodCacheManager(decorated_values[i])

        return decorated_values if isinstance(collection, list) else tuple(decorated_values)

    @staticmethod
    def __get_key(method_name, *args, **kwargs):
        return f"{method_name} ({args},{kwargs})"
