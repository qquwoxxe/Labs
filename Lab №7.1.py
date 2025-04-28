import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
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

def run_algorithms():
    global points
    try:
        points = eval(points_entry.get())
    except:
        output_text.insert(tk.END, "Некорректный ввод точек. Используйте [(x1, y1), (x2, y2), ...]\n")
        return

    output_text.delete("1.0", tk.END) # Очищаем окно вывода

    max_distance = 1
    start = time.time()
    alg_result = algorithmic_approach(points, max_distance)
    alg_time = time.time() - start
    output_text.insert(tk.END,
                       f"[Алгоритмический подход] Время: {alg_time:.4f} сек, Найдено: {len(alg_result)} подмножеств\n")

    for i, subset in enumerate(alg_result[:5]):
        output_text.insert(tk.END, f"  {subset}\n")

    if len(alg_result) > 0:
        max_alg = max(len(s) for s in alg_result)
        output_text.insert(tk.END, f"Максимальное подмножество: {max_alg} точек\n")

    start = time.time()
    opt_result = optimized_approach(points, max_distance)
    opt_time = time.time() - start
    output_text.insert(tk.END,
                       f"[Оптимизированный подход] Время: {opt_time:.4f} сек, Найдено: {len(opt_result)} подмножеств\n")

    for i, subset in enumerate(opt_result[:5]):
        output_text.insert(tk.END, f"  {subset}\n")
    if len(opt_result) > 0:
        max_opt = max(len(s) for s in opt_result)
        output_text.insert(tk.END, f"Максимальное подмножество: {max_opt} точек\n")


# --- Графический интерфейс ---
root = tk.Tk()
root.title("Поиск коллинеарных точек")

# Поле ввода точек
points_label = ttk.Label(root, text="Введите координаты точек (пример: [(0,0), (1,1), (2,2)]):")
points_label.pack(pady=5)
points_entry = ttk.Entry(root, width=50)
points_entry.insert(0,
                    "[(0,0), (1,1), (2,2), (0,1), (1,0), (2,0), (0,2), (1,2), (2,1), (3,3),(0,3), (1,3), (2,3), (3,0), (3,1), (3,2)]")
points_entry.pack(pady=5)

# Кнопка запуска алгоритмов
run_button = ttk.Button(root, text="Запустить", command=run_algorithms)
run_button.pack(pady=10)

# Окно вывода
output_text = scrolledtext.ScrolledText(root, width=60, height=20)
output_text.pack(pady=5)

root.mainloop()

