import numpy as np
from vector import Vector
import butcher_tables as tb
from runge_kutta import runge_kutta_n_steps
import visual as vsl


def pendulum_system_derivatives(state, system_params):
    """
    Вычисляет производные состояния системы для маятника на упругой нити.
    """
    # Распаковываем текущее состояние
    x, y, vx, vy = state.x, state.y, state.vx, state.vy

    # Распаковываем параметры системы
    m = system_params.m
    gamma = system_params.gamma
    k = system_params.k
    l = system_params.l
    g = system_params.g

    # Вычисляем расстояние от точки подвеса до маятника
    r = np.sqrt(x**2 + y**2)

    # Упругая сила (предотвращаем деление на ноль)
    if r < 1e-6:  # Если нить почти нулевой длины
        elastic_x, elastic_y = 0.0, 0.0
    else:
        elastic_term = k * (1 - l / r)
        elastic_x = -elastic_term * x
        elastic_y = -elastic_term * y

    # Сила трения
    friction_x = -gamma * vx
    friction_y = -gamma * vy

    # Сила тяжести (действует только по оси Y)
    gravity_y = -m * g

    # Ускорения (вторые производные)
    ax = (elastic_x + friction_x) / m
    ay = (elastic_y + friction_y + gravity_y) / m

    # Возвращаем производные состояния [dx/dt, dy/dt, dvx/dt, dvy/dt]
    return Vector({'x': vx, 'y': vy, 'vx': ax, 'vy': ay})


state = Vector({
    'x': 3.0,  # Начальная координата X
    'y': 0.0,  # Начальная координата Y
    'vx': -5.0,  # Начальная скорость по X
    'vy': 0.0  # Начальная скорость по Y
})

params = Vector({
    'm': 0.5,      # Масса маятника
    'gamma': 0.1,  # Коэффициент вязкого трения
    'k': 3.0,     # Жёсткость упругой нити
    'l': 1.0,      # Естественная длина нити
    'g': 9.81,     # Ускорение свободного падения
})

table = tb.rk4_table  # таблица бучера для рк
h = 0.01  # размер шага одной итерации
steps = 1000  # количество шагов


history = runge_kutta_n_steps(
    table, pendulum_system_derivatives, state, params, h, steps
)

vsl.create_animation(history, h)
