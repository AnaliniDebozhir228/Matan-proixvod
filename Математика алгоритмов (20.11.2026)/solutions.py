import heapq
import random
import statistics
import time


# ЗАДАНИЕ 1. Подсчёт количества выполнений
def task1():
    print("ЗАДАНИЕ 1")
    print("a) n выполнений, O(n)")
    print("b) n * n = n^2 выполнений, O(n^2)")
    print("c) примерно log2(n) выполнений, O(log n)")


# ЗАДАНИЕ 2. Бинарный поиск со счётчиком шагов
def binary_search(a, x):
    lo, hi = 0, len(a) - 1
    steps = 0

    while lo <= hi:
        steps += 1
        mid = lo + (hi - lo) // 2

        if a[mid] == x:
            return mid, steps
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1, steps


def task2():
    print("\nЗАДАНИЕ 2")
    a = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    print("x = 23:", binary_search(a, 23))
    print("x = 7:", binary_search(a, 7))


# ЗАДАНИЕ 3. Максимальное число шагов бинарного поиска
def task3():
    print("\nЗАДАНИЕ 3")
    print("1000 элементов:", 10, "шагов")
    print("1 000 000 элементов:", 20, "шагов")


# ЗАДАНИЕ 4. Сортировки и сравнение времени
def bubble_sort(a):
    result = a.copy()
    n = len(result)

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break

    return result


def merge_sort(a):
    if len(a) <= 1:
        return a.copy()

    middle = len(a) // 2
    left = merge_sort(a[:middle])
    right = merge_sort(a[middle:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    return result + left[i:] + right[j:]


def median_time(function, data, repeats=3):
    measurements = []
    for _ in range(repeats):
        start = time.perf_counter()
        function(data)
        measurements.append(time.perf_counter() - start)
    return statistics.median(measurements)


def task4():
    print("\nЗАДАНИЕ 4")
    rng = random.Random(2026)
    results = []

    for n in (1000, 2000, 4000):
        data = [rng.randint(0, 100000) for _ in range(n)]
        bubble_time = median_time(bubble_sort, data)
        merge_time = median_time(merge_sort, data)
        results.append((n, bubble_time, merge_time))
        print(
            f"n={n}: bubble={bubble_time:.6f} сек, "
            f"merge_sort={merge_time:.6f} сек"
        )

    print("При удвоении n пузырёк ожидаемо замедляется примерно в 4 раза,")
    print("а сортировка слиянием — примерно в 2 раза.")


# ЗАДАНИЕ 5. Жадный выбор непересекающихся мероприятий
def max_events(events):
    events = sorted(events, key=lambda event: event[1])
    chosen = []
    end = float("-inf")

    for start, finish in events:
        if start >= end:
            chosen.append((start, finish))
            end = finish

    return chosen


def task5():
    print("\nЗАДАНИЕ 5")
    events = [
        (1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9),
        (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)
    ]
    print("Выбранные мероприятия:", max_events(events))

    counterexample = [(1, 5), (4, 7), (6, 10)]
    shortest = min(counterexample, key=lambda event: event[1] - event[0])
    print("Контрпример для правила «самое короткое»:", counterexample)
    print("Если первым взять", shortest, "останется только 1 мероприятие.")
    print("Оптимальный выбор: (1, 5) и (6, 10) — всего 2 мероприятия.")


# ЗАДАНИЕ 6. Количество способов подняться по лестнице
def stairs(n):
    if n < 0:
        return 0
    if n == 0:
        return 1

    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def task6():
    print("\nЗАДАНИЕ 6")
    for n in (1, 2, 3, 10, 30):
        print(f"n={n}: {stairs(n)} способов")
    print("Получается последовательность Фибоначчи со сдвигом на один элемент.")


# ЗАДАНИЕ 7. Сравнение жадного размена и динамики
def greedy_coins(coins, amount):
    count = 0
    for coin in sorted(coins, reverse=True):
        count += amount // coin
        amount %= coin
    return count


def dp_coins(coins, amount):
    inf = float("inf")
    dp = [0] + [inf] * amount

    for value in range(1, amount + 1):
        for coin in coins:
            if coin <= value:
                dp[value] = min(dp[value], dp[value - coin] + 1)

    return dp


def task7():
    print("\nЗАДАНИЕ 7")
    coins = [1, 3, 4]
    dp = dp_coins(coins, 20)
    wrong = []

    for amount in range(1, 21):
        greedy = greedy_coins(coins, amount)
        optimal = dp[amount]
        if greedy != optimal:
            wrong.append(amount)

    print("Суммы, где жадный алгоритм ошибается:", wrong)


# ЗАДАНИЕ 8. Алгоритм Евклида вручную
def task8():
    print("\nЗАДАНИЕ 8")
    a, b = 252, 198
    divisions = 0

    while b != 0:
        remainder = a % b
        print(f"{a} = {a // b} * {b} + {remainder}")
        a, b = b, remainder
        divisions += 1

    print("НОД =", a)
    print("Количество делений =", divisions)


# ЗАДАНИЕ 9. Быстрое возведение в степень по модулю
def power_mod(a, n, m):
    if m <= 0 or n < 0:
        raise ValueError("Нужно m > 0 и n >= 0")

    result = 1
    a %= m

    while n > 0:
        if n & 1:
            result = (result * a) % m
        a = (a * a) % m
        n >>= 1

    return result


def task9():
    print("\nЗАДАНИЕ 9")
    print("2^10 mod 1000 =", power_mod(2, 10, 1000))
    print("3^13 mod 1000 =", power_mod(3, 13, 1000))


# ЗАДАНИЕ 10. Решето Эратосфена
def sieve(n):
    if n < 2:
        return []

    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= n:
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1

    return [number for number in range(2, n + 1) if is_prime[number]]


def task10():
    print("\nЗАДАНИЕ 10")
    for n in (100, 1000, 1_000_000):
        print(f"Простых чисел до {n}: {len(sieve(n))}")


# ЗАДАНИЕ 11. Алгоритм Дейкстры
def dijkstra(graph, start):
    distances = {vertex: float("inf") for vertex in graph}
    distances[start] = 0
    heap = [(0, start)]

    while heap:
        current_distance, vertex = heapq.heappop(heap)

        if current_distance > distances[vertex]:
            continue

        for neighbor, weight in graph[vertex]:
            if weight < 0:
                raise ValueError("Алгоритм Дейкстры не работает с отрицательными весами")

            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(heap, (new_distance, neighbor))

    return distances


def task11():
    print("\nЗАДАНИЕ 11")
    graph = {
        "A": [("B", 4), ("C", 1)],
        "B": [("A", 4), ("C", 2), ("D", 1)],
        "C": [("A", 1), ("B", 2), ("D", 5)],
        "D": [("B", 1), ("C", 5)]
    }

    print("Исходный граф:", dijkstra(graph, "A"))

    graph["A"].append(("D", 3))
    graph["D"].append(("A", 3))
    print("После добавления ребра A-D длиной 3:", dijkstra(graph, "A"))


# ЗАДАНИЕ 12. Метод Монте-Карло для приближённого вычисления pi
def monte_carlo_pi(n, seed=42):
    rng = random.Random(seed)
    inside = 0

    for _ in range(n):
        x = rng.random()
        y = rng.random()
        if x * x + y * y <= 1:
            inside += 1

    return 4 * inside / n


def task12():
    print("\nЗАДАНИЕ 12")
    for n in (100, 10_000, 1_000_000):
        print(f"N={n}: pi примерно равно {monte_carlo_pi(n):.6f}")


def main():
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
    task7()
    task8()
    task9()
    task10()
    task11()
    task12()


if __name__ == "__main__":
    main()
