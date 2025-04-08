import numpy as np


class Vector(np.ndarray):
    def __new__(cls, data):
        # Проверяем, что data - словарь
        if not isinstance(data, dict):
            raise TypeError("Vector must be initialized with a dictionary")

        # Создаем массив из значений словаря
        array_data = list(data.values())
        obj = np.asarray(array_data, dtype=float).view(cls)

        # Сохраняем ключи и их порядок
        obj._keys = list(data.keys())
        obj._key_to_index = {key: i for i, key in enumerate(obj._keys)}

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

        # Копируем атрибуты при создании новых представлений
        self._keys = getattr(obj, '_keys', [])
        self._key_to_index = getattr(obj, '_key_to_index', {})

    def __getitem__(self, key):
        # Если ключ - строка, ищем в словаре
        if isinstance(key, str):
            return self[self._key_to_index[key]]
        # Иначе стандартное поведение numpy
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        # Если ключ - строка, ищем в словаре
        if isinstance(key, str):
            self[self._key_to_index[key]] = value
        else:
            super().__setitem__(key, value)

    def __getattr__(self, name):
        # Доступ к элементам как к атрибутам (vec.x)
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'Vector' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        # Установка элементов как атрибутов (vec.x = 5)
        if name in ('_keys', '_key_to_index'):
            super().__setattr__(name, value)
        else:
            try:
                self[name] = value
            except KeyError:
                raise AttributeError(
                    f"'Vector' object has no attribute '{name}'")

    def __repr__(self):
        return f"Vector({dict(zip(self._keys, self))})"

    @property
    def dict(self):
        """Возвращает вектор как словарь"""
        return dict(zip(self._keys, self))


# Пример использования
if __name__ == "__main__":
    # Создаем вектор
    v = Vector({'x': 1.5, 'y': 2.0, 'z': 3.5})
    print("Исходный вектор:", v)
    print("Как словарь:", v.dict)

    # Доступ по ключам
    print("\nДоступ по ключам:")
    print("v['x'] =", v.x)
    print("v.y =", v.y)

    # Изменение по ключу
    print("\nИзменяем по ключу:")
    v['x'] = 10.0
    print("После v['x'] = 10.0:", v)

    # Изменение как атрибута
    v.y = 20.0
    print("После v.y = 20.0:", v)

    # Работа с numpy операциями
    print("\nNumpy операции:")
    print("v + 5 =", v + 5)
    print("Норма вектора:", np.linalg.norm(v))

    # Создание нового вектора из операций
    v2 = Vector({'x': 1.0, 'y': 2.0, 'z': 3.0})
    print("\nВектор v2:", v2)
    print("v + v2 =", v + v2)
