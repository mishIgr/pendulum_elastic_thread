import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import numpy as np


def create_animation(history, h, l=None):
    # Соберем все x и y координаты из истории
    x_coords = [state.x for state in history]
    y_coords = [state.y for state in history]

    # Найдем минимальные и максимальные значения
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)

    # Добавим 10% запаса по каждой стороне
    padding_x = (x_max - x_min) * 0.3
    padding_y = (y_max - y_min) * 0.3

    # Создаём фигуру и оси
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(min(x_min - padding_x, -0.1), max(x_max + padding_x, 0.1))
    ax.set_ylim(y_min - padding_y, max(y_max + padding_y, 0.1))
    ax.set_aspect('equal')
    ax.grid(True)
    # ax.set_title('Анимация маятника на упругой нити')

    # Вычисляем базовый размер шарика в зависимости от масштаба графика
    plot_width = (x_max + padding_x) - (x_min - padding_x)
    plot_height = (y_max + padding_y) - (y_min - padding_y)
    plot_size = max(plot_width, plot_height)
    bob_size = min(0.1, plot_size * 0.05)  # 5% от размера графика

    # Точка подвеса (начало координат)
    pivot = plt.Circle((0, 0), bob_size / 10, color='black', zorder=10)
    ax.add_patch(pivot)

    # Маятник (шарик)
    bob = Circle((0, 0), bob_size, color='blue', zorder=10)
    ax.add_patch(bob)

    # Нить (линия)
    line, = ax.plot([], [], 'k-', lw=1)

    # Функция инициализации анимации
    def init():
        bob.center = (0, 0)
        line.set_data([], [])
        return bob, line

    # Функция обновления кадра
    def update(frame):
        state = history[frame]
        x, y = state.x, state.y

        # Обновляем положение шарика
        bob.center = (x, y)

        # Обновляем линию (нить)
        line.set_data([0, x], [0, y])

        if l and np.sqrt(x**2 + y**2) >= l:
            line.set_color('red')
        else:
            line.set_color('black')

        return bob, line

    slowdown_factor = 1  # 1 сек модели = 1 сек анимации
    real_time_per_frame = h * slowdown_factor  # Время модели за кадр
    interval_ms = real_time_per_frame * 1000  # Переводим в миллисекунды

    # Создаём анимацию
    frames = len(history)
    anim = FuncAnimation(
        fig, update, frames=frames,
        init_func=init, blit=True, interval=interval_ms
    )

    plt.show()

    # Сохранение анимации в файл (опционально)
    # anim.save('pendulum_animation.mp4', writer='ffmpeg', fps=30)
