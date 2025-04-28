# Задание состоит из двух частей.
# 1 часть – написать программу в соответствии со своим вариантом задания.
# Написать 2 варианта формирования (алгоритмический и с помощью функций Питона), сравнив по времени их выполнение.
# 2 часть – усложнить написанную программу,
# введя по своему усмотрению в условие минимум одно ограничение
# на характеристики объектов (которое будет сокращать количество переборов) и целевую функцию для нахождения оптимального решения.
# Вариант 17. На плоскости задано К точек. Сформировать все возможные варианты выбора множества точек из них на проверку того,
# что они принадлежат одной прямой.

import time
from collections import defaultdict

def compute_gcd(a, b, c):
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    return gcd(gcd(abs(a), abs(b)), abs(c))

def get_line(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    a = y2 - y1
    b = x1 - x2
    c = x2 * y1 - x1 * y2
    current_gcd = compute_gcd(a, b, c)
    if current_gcd == 0:
        return None
    a //= current_gcd
    b //= current_gcd
    c //= current_gcd
    sign = 1
    if a != 0:
        sign = a // abs(a)
    elif b != 0:
        sign = b // abs(b)
    else:
        sign = c // abs(c) if c != 0 else 1
    a *= sign
    b *= sign
    c *= sign
    return (a, b, c)

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def are_colinear(points, max_distance):
    if len(points) <= 2:
        return True
    x1, y1 = points[0]
    x2, y2 = points[1]
    dx = x2 - x1
    dy = y2 - y1

    # Проверка расстояния между первой и каждой последующей точкой
    for i in range(2, len(points)):
        x, y = points[i]
        if dx * (y - y1) != dy * (x - x1):
            return False
        if distance(points[0], points[i]) > max_distance:
            return False
    return True

def algorithmic_approach(points, max_distance):
    n = len(points)
    unique_subsets = set()
    for mask in range(1, 1 << n):
        subset = [points[i] for i in range(n) if (mask >> i) & 1]
        if are_colinear(subset, max_distance):
            unique = frozenset((x, y) for (x, y) in subset)
            unique_subsets.add(unique)
    return [list(s) for s in unique_subsets]

def optimized_approach(points, max_distance):
    n = len(points)
    lines = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = points[i], points[j]
            line = get_line(p1, p2)
            if line is not None:
                lines[line].update({i, j})
    unique_subsets = set()
    for indices in lines.values():
        m = len(indices)
        indices_list = list(indices)
        for mask in range(1, 1 << m):
            subset_indices = [indices_list[k] for k in range(m) if (mask >> k) & 1]
            subset = [points[i] for i in subset_indices]
            if are_colinear(subset, max_distance):  # Добавлена проверка коллинеарности и расстояния
                unique_subsets.add(frozenset(subset_indices)) # сохраняем индексы, а не точки
    return [[points[i] for i in s] for s in unique_subsets]

# Фильтрация точек: только чётные координаты
points = list({
    (i, i) for i in range(8)
} | {
    (i, 0) for i in range(8)
})

max_distance = 0.1

# Замер времени и вывод результатов
start = time.time()

# Вывод статистики
alg_result = algorithmic_approach(points, max_distance)
print(f"[Алгоритмический подход] Время: {time.time() - start:.4f} сек, Найдено: {len(alg_result)} подмножеств")
for subset in alg_result[:5]:
    print(f"  {subset}")
if len(alg_result) > 0:
    max_alg = max(len(s) for s in alg_result)
    print(f"Максимальное подмножество: {max_alg} точек")

opt_result = optimized_approach(points, max_distance)
print(f"[Оптимизированный подход] Время: {time.time() - start:.4f} сек, Найдено: {len(opt_result)} подмножеств")
for subset in opt_result[:5]:
    print(f"  {subset}")
if len(opt_result) > 0:
    max_opt = max(len(s) for s in opt_result)
    print(f"Максимальное подмножество: {max_opt} точек")

