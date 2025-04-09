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

from typing import List

def read_numbers_from_file(filename: str, count: int) -> List[int]:
    '''Чтение чисел из файла'''
    numbers = []
    with open(filename, 'r') as f:
        for line in f:
            numbers.extend(map(int, line.strip().split()))
            if len(numbers) >= count:
                break
    return numbers[:count]

def create_matrix_from_numbers(numbers: List[int], n: int) -> List[List[int]]:
    '''Преобразование списка чисел в матрицу'''
    return [numbers[i * n:(i + 1) * n] for i in range(n)]

def print_matrix(matrix: List[List[int]], title: str = ""):

    if title:
        print(title)
    for row in matrix:
        print(" ".join(f"{elem:4}" for elem in row))
    print()

def count_greater_than_k_in_area4(matrix: List[List[int]], k: int) -> int:
    '''Подсчёт чисел > K в нечетных строках области 4'''
    n = len(matrix)
    count = 0
    center = n // 2
    for i in range(n):
        for j in range(n):
            if i == j or i + j == n - 1:
                continue
            if not (i < center and j > i and j < n - i - 1) and \
                    not (j > center and (i < j or i + j >= n)) and \
                    not (i > center and j < i and j > n - i - 1):
                if i % 2 != 0 and matrix[i][j] > k:
                    count += 1
    return count

def product_in_area2(matrix: List[List[int]]) -> int:
    '''Произведение чисел в нечетных строках области 2'''
    n = len(matrix)
    product = 1
    center = n // 2
    for i in range(n):
        if i % 2 != 0:
            for j in range(n):
                if j > center and i < j and i != j and i + j != n - 1 and i + j >= n - 1:
                    product *= matrix[i][j]
    return product

def swap_areas_1_3_symmetrically(matrix: List[List[int]]) -> List[List[int]]:
    '''Симметричный обмен областей 1 и 3'''
    n = len(matrix)
    new_matrix = [row.copy() for row in matrix]
    center = n // 2
    for i in range(center):
        for j in range(i + 1, n - i - 1):
            mirror_i = n - 1 - i
            if i < center and j > i and j < n - i - 1:
                if mirror_i > center and j < mirror_i and j > n - mirror_i - 1:
                    new_matrix[i][j], new_matrix[mirror_i][j] = new_matrix[mirror_i][j], new_matrix[i][j]
    return new_matrix

def swap_areas_1_2_asymmetrically(matrix: List[List[int]]) -> List[List[int]]:
    '''Несимметричный обмен областей 1 и 2'''
    n = len(matrix)
    new_matrix = [row.copy() for row in matrix]
    center = n // 2

    area1 = []
    area2 = []

    for i in range(n):
        for j in range(n):
            if i == j or i + j == n - 1:
                continue
            if i < center and j > i and j < n - i - 1:
                area1.append((i, j))
            elif j > center and (i < j or i + j >= n):
                area2.append((i, j))

    for (i1, j1), (i2, j2) in zip(area1, area2):
        new_matrix[i1][j1], new_matrix[i2][j2] = new_matrix[i2][j2], new_matrix[i1][j1]
    return new_matrix

def matrix_multiply(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    """Умножение матриц"""
    n = len(a)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result

def matrix_transpose(matrix: List[List[int]]) -> List[List[int]]:
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix))]

def matrix_add(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    return [[a[i][j] + b[i][j] for j in range(len(a))] for i in range(len(a))]

def scalar_multiply_matrix(k: int, matrix: List[List[int]]) -> List[List[int]]:
    return [[k * matrix[i][j] for j in range(len(matrix))] for i in range(len(matrix))]

def main():
    FILENAME = "numbers.txt"
    K = int(input("Введите число K: "))
    N = int(input("Введите размер матрицы N: "))

    numbers = read_numbers_from_file(FILENAME, N * N)
    if len(numbers) < N * N:
        print(f"Нужно {N * N} чисел, в файле {len(numbers)}")
        return

    A = create_matrix_from_numbers(numbers, N)
    print_matrix(A, "Исходная матрица A:")

    F = [row.copy() for row in A]

    count4 = count_greater_than_k_in_area4(A, K)
    product2 = product_in_area2(A)

    print(f"Чисел > K в области 4: {count4}")
    print(f"Произведение в области 2: {product2}")

    if count4 > product2:
        print("Меняем области 1 и 3 симметрично")
        F = swap_areas_1_3_symmetrically(F)
    else:
        print("Меняем области 1 и 2 несимметрично")
        F = swap_areas_1_2_asymmetrically(F)

    print_matrix(F, "Матрица F после преобразования:")

    KA = scalar_multiply_matrix(K, A)
    print_matrix(KA, "Матрица K*A:")

    KAF = matrix_multiply(KA, F)
    print_matrix(KAF, "Матрица (K*A)*F:")

    FT = matrix_transpose(F)
    print_matrix(FT, "Матрица F^T:")

    KFT = scalar_multiply_matrix(K, FT)
    print_matrix(KFT, "Матрица K*F^T:")

    result = matrix_add(KAF, KFT)
    print_matrix(result, "Результат ((K*A)*F + K*F^T):")

if __name__ == "__main__":
    main()