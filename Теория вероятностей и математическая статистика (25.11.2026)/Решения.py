import math
import random


def left_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(n))


def midpoint_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + (i + 0.5) * h) for i in range(n))


def trapezoids(f, a, b, n):
    h = (b - a) / n
    total = (f(a) + f(b)) / 2
    total += sum(f(a + i * h) for i in range(1, n))
    return h * total


def monte_carlo_pi(n):
    hits = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            hits += 1
    return 4 * hits / n


def falling_ball(dt, update_velocity_first):
    g = 9.8
    y = 100.0
    v = 0.0
    steps = round(2.0 / dt)

    for _ in range(steps):
        if update_velocity_first:
            v += g * dt
            y -= v * dt
        else:
            y -= v * dt
            v += g * dt

    return y


def midpoint_error_for_x_squared(n):
    return abs(midpoint_rectangles(lambda x: x * x, 0, 1, n) - 1 / 3)


def main():
    print("Код-задача 1: метод средних прямоугольников")
    print("Интеграл sin(x) от 0 до pi:", midpoint_rectangles(math.sin, 0, math.pi, 10000))
    print("Интеграл x^2 от 0 до 1:", midpoint_rectangles(lambda x: x**2, 0, 1, 10000))

    print("\nКод-задача 2: сравнение методов для sin(x) на [0, pi]")
    exact = 2.0
    print("n | левые | ошибка | средние | ошибка | трапеции | ошибка")
    for n in (10, 100, 1000):
        left = left_rectangles(math.sin, 0, math.pi, n)
        middle = midpoint_rectangles(math.sin, 0, math.pi, n)
        trap = trapezoids(math.sin, 0, math.pi, n)
        print(
            n,
            round(left, 10), round(abs(left - exact), 10),
            round(middle, 10), round(abs(middle - exact), 10),
            round(trap, 10), round(abs(trap - exact), 10),
            sep=" | "
        )

    print("\nКод-задача 3: оценка pi методом Монте-Карло")
    for n in (10**3, 10**4, 10**5, 10**6):
        estimate = monte_carlo_pi(n)
        print(n, estimate, "ошибка:", abs(estimate - math.pi))

    print("\nКод-задача 4: падающий мяч, точная высота при t=2:", 100 - 0.5 * 9.8 * 2**2)
    for dt in (0.1, 0.001):
        y_explicit = falling_ball(dt, False)
        y_velocity_first = falling_ball(dt, True)
        print("dt =", dt)
        print("Сначала y, затем v:", y_explicit)
        print("Сначала v, затем y:", y_velocity_first)

    print("\nКод-задача 5: оценка количества разбиений")
    n = math.floor(math.sqrt(1 / (12 * 10**-8))) + 1
    print("Минимальное n:", n)
    print("Оценка ошибки:", 1 / (12 * n**2))
    print("Проверка численным методом:", midpoint_error_for_x_squared(n))


if __name__ == "__main__":
    main()
