# С клавиатуры вводится два числа K и N.
# Квадратная матрица А(N,N) заполняется случайным образом целыми числами в интервале [-10,10].
# Для тестирования использовать не случайное заполнение, а целенаправленное, введенное из файла или полученное генератором.
# Условно матрица разделена на 4 части: цифра 1 сверху, цифра 2 справа, цифра 3 снизу, цифра 4 слева
# Формируется матрица F следующим образом:
# Скопировать в нее матрицу А и если  количество чисел, больших К в нечетных столбцах в области 4 больше,
# чем произведение чисел в нечетных строках в области 2, то поменять симметрично области 1 и 3 местами,
# иначе 1 и 2 поменять местами несимметрично. При этом матрица А не меняется.
# После чего вычисляется выражение: ((К*A)*F+ K* F T .
# Выводятся по мере формирования А, F и все матричные операции последовательно.
# Решить на python, библиотечными методами numpy пользоваться нельзя.

import random

# Ввод чисел K и N
K = int(input("Введите число K: "))
N = int(input("Введите размер матрицы N: "))

# Генерация матрицы A с целыми числами в диапазоне [-10, 10]
A = [[random.randint(-10, 10) for _ in range(N)] for _ in range(N)]
print("Матрица A:")
for row in A:
    print(row)

# Копируем матрицу A в F
F = [row[:] for row in A]

# Разделяем матрицу на области
area1 = A[:N//2]
area2 = [row[N//2:] for row in A]
area3 = A[N//2:]
area4 = [row[:N//2] for row in A]

# Подсчет чисел > K в нечетных столбцах области 4
count_greater_K = sum(1 for i in range(len(area4)) for j in range(1, N//2, 2) if area4[i][j] > K)

# Подсчет произведения чисел в нечетных строках области 2
odd_rows = 1
for row in range(1, len(area2), 2):
    for col in range(len(area2[row])):
        odd_rows *= area2[row][col]

# Меняем области в зависимости от условия
if count_greater_K > odd_rows:
    # Симметричный обмен областей 1 и 3
    for i in range(N//2):
        F[i], F[i + N//2] = A[i + N//2], A[i]
else:
    # Несимметричный обмен областей 1 и 2
    for i in range(N//2):
        F[i][:N//2] = area2[i][:N//2]

print("Матрица F:")
for row in F:
    print(row)

# Вычисляем итоговое выражение ((K*A)*F + K*F^T)
def matrix_mult(mat1, mat2):
    result = [[0] * len(mat2[0]) for _ in range(len(mat1))]
    for i in range(len(mat1)):
        for j in range(len(mat2[0])):
            for k in range(len(mat2)):
                result[i][j] += mat1[i][k] * mat2[k][j]
    return result

# Транспонирование матрицы F
def transpose(mat):
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]

# Умножение K*A на F
KA_mult_F = matrix_mult([[K * val for val in row] for row in A], F)

# Умножение K на транспонированное F
K_F_T = [[K * val for val in row] for row in transpose(F)]

# Суммируем
result = [[KA_mult_F[i][j] + K_F_T[i][j] for j in range(len(KA_mult_F[0]))] for i in range(len(KA_mult_F))]

print("Результат матричных операций:")
for row in result:
    print(row)