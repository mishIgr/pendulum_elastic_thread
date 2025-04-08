import numpy as np
from vector import Vector
import butcher_tables as tb
import visual as vsl


def runge_kutta_step(butcher_table, system_func, dynamic_params, system_params,
                     step):
    """
    Выполняет один шаг метода Рунге-Кутты.
    """
    A = butcher_table['A']
    b = butcher_table['b']
    c = butcher_table['c']
    s = len(c)  # Количество стадий

    k = np.zeros((s, len(dynamic_params)))

    # Вычисляем коэффициенты k
    for i in range(s):
        sum_Ak = np.zeros_like(dynamic_params)
        for j in range(i):
            sum_Ak += A[i][j] * k[j]
        k[i] = system_func(dynamic_params + step * sum_Ak, system_params)

    # Вычисляем новое значение
    sum_bk = np.zeros_like(dynamic_params)
    for i in range(s):
        sum_bk += b[i] * k[i]

    new_dynamic_params = dynamic_params + step * sum_bk

    return new_dynamic_params


# def runge_kutta_n_steps(butcher_table, system_func, initial_params,
#                         system_params, step, n_steps):
#     """
#     Выполняет n шагов метода Рунге-Кутты.
#     """
#     history = [initial_params.copy()]
#     current_params = initial_params.copy()

#     for _ in range(n_steps):
#         current_params = runge_kutta_step(
#             butcher_table, system_func, current_params, system_params, step)
#         history.append(current_params.copy())

#     return np.array(history)


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
    'x': 1.0,
    'y': 0.0,
    'vx': 0.0,
    'vy': 0.0,
})

params = Vector({
    'm': 0.5,      # Масса маятника
    'gamma': 0.1,  # Коэффициент вязкого трения
    'k': 1.0,     # Жёсткость упругой нити
    'l': 0.1,      # Естественная длина нити
    'g': 9.81,     # Ускорение свободного падения
})

table = tb.rk4_table  # таблица бучера для рк
h = 0.01  # размер шага одной итерации
steps = 1000  # количество шагов


history = [state.copy()]
current_params = state.copy()

for _ in range(steps):
    current_params = runge_kutta_step(
        table, pendulum_system_derivatives, current_params, params, h)
    history.append(current_params.copy())


vsl.create_animation(history, h)
