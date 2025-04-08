import numpy as np
from vector import Vector


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


def runge_kutta_n_steps(table, system_func, initial_params,
                        system_params, h, steps):
    """
    Выполняет n шагов метода Рунге-Кутты.
    """

    history = [initial_params.copy()]
    current_params = initial_params.copy()

    for _ in range(steps):
        current_params = runge_kutta_step(
            table, system_func, current_params, system_params, h)
        history.append(current_params.copy())

    return history
