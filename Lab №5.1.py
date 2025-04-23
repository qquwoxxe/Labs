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

def are_colinear(points):
    if len(points) < 3:
        return False  # Ограничение: минимум 3 точки
    x1, y1 = points[0]
    x2, y2 = points[1]
    dx = x2 - x1
    dy = y2 - y1
    for (x, y) in points[2:]:
        if dx * (y - y1) != dy * (x - x1):
            return False
    return True

def algorithmic_approach_optimized(points):
    n = len(points)
    unique_subsets = set()
    max_size = 0
    # Перебор масок только для подмножеств >=3 точек
    for mask in range(1, 1 << n):
        bit_count = bin(mask).count('1')
        if bit_count < 3:
            continue  # Пропускаем маски с <3 точками
        subset = [points[i] for i in range(n) if (mask >> i) & 1]
        if are_colinear(subset):
            unique = frozenset((x, y) for (x, y) in subset)
            unique_subsets.add(unique)
            if bit_count > max_size:
                max_size = bit_count
    # Фильтрация подмножеств по максимальному размеру
    result = [list(s) for s in unique_subsets if len(s) == max_size]
    return result, max_size

def optimized_approach_enhanced(points):
    n = len(points)
    lines = defaultdict(set)
    # Группируем точки по прямым
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = points[i], points[j]
            line = get_line(p1, p2)
            if line is not None:
                lines[line].add(i)
                lines[line].add(j)
    # Удаляем прямые с <3 точками
    lines_filtered = {k: v for k, v in lines.items() if len(v) >= 3}
    max_size = 0
    result = []
    # Генерируем подмножества >=3 точек для каждой прямой
    for line, indices in lines_filtered.items():
        m = len(indices)
        indices_list = list(indices)
        # Перебор масок только для подмножеств >=3 точек
        for mask in range(1, 1 << m):
            bit_count = bin(mask).count('1')
            if bit_count < 3:
                continue
            subset_indices = {indices_list[k] for k in range(m) if (mask >> k) & 1}
            subset = [points[i] for i in subset_indices]
            # Обновляем максимальный размер
            if bit_count > max_size:
                max_size = bit_count
                result = [subset]
            elif bit_count == max_size:
                result.append(subset)
    # Удаляем дубликаты
    unique_result = []
    seen = set()
    for subset in result:
        key = frozenset((x, y) for (x, y) in subset)
        if key not in seen:
            seen.add(key)
            unique_result.append(subset)
    return unique_result, max_size

points = [(i, i) for i in range(9)] + [(i, 0) for i in range(8)]

start = time.time()
alg_result, alg_max = algorithmic_approach_optimized(points)
print(f"Алгоритмический подход (оптимизированный): {time.time() - start:.4f} сек")
print(f"Максимальный размер подмножества: {alg_max}, найдено {len(alg_result)} подмножеств")

start = time.time()
opt_result, opt_max = optimized_approach_enhanced(points)
print(f"\nОптимизированный подход (усложненный): {time.time() - start:.4f} сек")
print(f"Максимальный размер подмножества: {opt_max}, найдено {len(opt_result)} подмножеств")