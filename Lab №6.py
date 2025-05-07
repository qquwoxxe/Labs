# Задана рекуррентная функция. Область определения функции – натуральные числа.
# Написать программу сравнительного вычисления данной функции рекурсивно и итерационно (значение, время).
# Определить (смоделировать) границы применимости рекурсивного и итерационного подхода.
# Результаты сравнительного исследования времени вычисления представить в табличной и
# графической форме в виде отчета по лабораторной работе.
# 17. F(1) = 1, F(n) =(-1)n*(F(n–1) /(2n)!-(n + n!)), при четных n > 1 F(n)=sin(n) при нечетных n > 1
import math
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def F_rec(n):
    if n == 1:
        return 1
    if n % 2 == 0:
        return ((-1)**n) * (F_rec(n-1) / math.factorial(2 * n) - (n + math.factorial(n)))
    else:
        return math.sin(n)

def F_iter(n):
    if n == 1:
        return 1
    f_prev = 1.0
    for i in range(2, n+1):
        if i % 2 == 0:
            f_prev = ((-1)**i) * (f_prev / math.factorial(2 * i) - (i + math.factorial(i)))
        else:
            f_prev = math.sin(i)
    return f_prev

def measure_time(func, n):
    start = time.perf_counter()
    result = func(n)
    end = time.perf_counter()
    return end - start, result

ns = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30]
rec_times = []
iter_times = []
rec_values = []
iter_values = []

for n in ns:
    try:
        time_rec, val_rec = measure_time(F_rec, n)
    except Exception as e:
        time_rec = None
        val_rec = None
    time_iter, val_iter = measure_time(F_iter, n)
    rec_times.append(time_rec)
    iter_times.append(time_iter)
    rec_values.append(val_rec)
    iter_values.append(val_iter)

print("Таблица результатов:")
print("n\tRec Time\tIter Time\tRec Value\t\tIter Value")
for i, n in enumerate(ns):
    rt = f"{rec_times[i]:.6f}" if rec_times[i] is not None else "Error"
    it = f"{iter_times[i]:.6f}"
    rv = f"{rec_values[i]:.10f}" if rec_values[i] is not None else "Error"
    iv = f"{iter_values[i]:.10f}"
    print(f"{n}\t{rt}\t{it}\t{rv}\t{iv}")

plt.figure(figsize=(10, 6))
plt.plot(ns, rec_times, label='Recursive')
plt.plot(ns, iter_times, label='Iterative')
plt.xlabel('n')
plt.ylabel('Time (seconds)')
plt.title('Сравнение времени выполнения рекурсивного и итерационного подходов')
plt.legend()
plt.grid(True)
plt.savefig('time_comparison.png')
plt.show()