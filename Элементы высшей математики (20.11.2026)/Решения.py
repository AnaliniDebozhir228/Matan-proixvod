"""
Элементы высшей математики — кривые второго порядка.
IT TOP College · 2 курс
Дата: 20.11.2026
Решения заданий 11–16 и вспомогательные функции.
"""

from math import cos, sin, cosh, sinh, sqrt, hypot, pi
import numpy as np
import matplotlib.pyplot as plt


# Задание 11. Ближайшая и дальняя точки орбиты.
def apsides(a, e):
    return a * (1 - e), a * (1 + e)


# Задание 13. Координаты точек гиперболы при заданном x.
def hyperbola_y(x, a=3, b=4):
    value = b**2 * (x**2 / a**2 - 1)
    if value < 0:
        return ()
    root = sqrt(value)
    return (-root, root)


# Задание 14. Проверка принадлежности эллипсу.
def inside_ellipse(px, py, x0, y0, a, b):
    if a <= 0 or b <= 0:
        raise ValueError("Полуоси a и b должны быть положительными")
    return ((px - x0)**2 / a**2 +
            (py - y0)**2 / b**2 <= 1)


# Задание 15. Определение типа по старшим коэффициентам.
def kind(A, B, C):
    delta = B**2 - 4*A*C
    if delta > 0:
        return "гипербола"
    if delta == 0:
        return "парабола"
    if B == 0 and A == C:
        return "окружность"
    return "эллипс"


# Проверка задач 1–10 и функций.
if __name__ == "__main__":
    print("Задание 11 — орбиты")
    print("Земля, млн км:", apsides(149.6, 0.0167))
    print("Комета Галлея, а.е.:", apsides(17.8, 0.967))

    print("\nЗадание 12 — тарелка")
    a = 0.25
    print("Расстояние до фокуса:", 1 / (4*a), "м")

    print("\nЗадание 13 — гипербола")
    ys = hyperbola_y(6)
    print("При x=6, y =", ys)
    for y in ys:
        d1 = hypot(6 + 5, y)
        d2 = hypot(6 - 5, y)
        print(f"Проверка: d1={d1:.6f}, d2={d2:.6f}, |d1-d2|={abs(d1-d2):.6f}")

    print("\nЗадание 14 — эллипс")
    print(inside_ellipse(2, 1, 0, 0, 3, 2))  # True
    print(inside_ellipse(4, 0, 0, 0, 3, 2))  # False

    print("\nЗадание 15 — типы кривых")
    tests = [
        (3, 0, 3),   # окружность
        (1, 0, 2),   # эллипс
        (1, 0, -1),  # гипербола
        (2, 0, 0),   # парабола
        (0, 1, 0),   # xy=1, гипербола
    ]
    for values in tests:
        print(values, "->", kind(*values))

    print("\nЗадание 16 — графики")
    t = np.linspace(0, 2*pi, 400)
    s = np.linspace(-1.5, 1.5, 400)
    x = np.linspace(-2, 2, 400)

    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
    axes[0].plot(2*np.cos(t), 2*np.sin(t))
    axes[0].set_title("Окружность")

    axes[1].plot(3*np.cos(t), 2*np.sin(t))
    axes[1].set_title("Эллипс")

    axes[2].plot(2*np.cosh(s), 1.5*np.sinh(s))
    axes[2].plot(-2*np.cosh(s), 1.5*np.sinh(s))
    axes[2].set_title("Гипербола")

    axes[3].plot(x, 0.5*x**2)
    axes[3].set_title("Парабола")

    for ax in axes:
        ax.set_aspect("equal")
        ax.grid(True)

    plt.tight_layout()
    plt.show()
