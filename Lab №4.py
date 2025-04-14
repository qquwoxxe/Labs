# С клавиатуры вводится два числа K и N.
# Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц,
# B,C,D,E заполняется случайным образом целыми числами в интервале [-10,10].
# Для отладки использовать не случайное заполнение, а целенаправленное (ввод из файла и генератором).
# Вид матрицы А: Е В//D С
# На основе матрицы А формируется матрица F. По матрице F необходимо вывести не менее 3 разных графика.
# Программа должна использовать функции библиотек numpy  и matplotlib.
# Формируется матрица F следующим образом: скопировать в нее А и  если в Е количество нулей в нечетных столбцах,
# чем сумма чисел в нечетных строках, то поменять местами В и Е симметрично, иначе С и Е поменять местами несимметрично.
# При этом матрица А не меняется. После чего если определитель матрицы А больше суммы диагональных элементов матрицы F,
# то вычисляется выражение:A-1*AT – K * F-1, иначе вычисляется выражение (A-1 +G-F-1)*K,
# где G-нижняя треугольная матрица, полученная из А.
# Выводятся по мере формирования А, F и все матричные операции последовательно.

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from typing import List

filename = "numbers.txt"
def read_numbers_from_file(count: int) -> List[int]:
    '''Чтение чисел из файла'''
    numbers = []
    with open(filename, 'r') as f:
        for line in f:
            numbers.extend(map(int, line.strip().split()))
            if len(numbers) >= count:
                break
    return numbers[:count]


def create_matrix_a(n: int) -> np.ndarray:
    """Создание матрицы A из 4 подматриц"""
    half = n // 2
    numbers = read_numbers_from_file(4 * half * half)

    # Разделение на подматрицы
    e = np.array(numbers[:half * half]).reshape(half, half)
    print_matrix(e, 'Подматрица E')
    b = np.array(numbers[half * half: 2 * half * half]).reshape(half, half)
    print_matrix(b, 'Подматрица B')
    d = np.array(numbers[2 * half * half: 3 * half * half]).reshape(half, half)
    print_matrix(d, 'Подматрица D')
    c = np.array(numbers[3 * half * half: 4 * half * half]).reshape(half, half)
    print_matrix(c, 'Подматрица С')

    return np.block([[e, b], [d, c]])

def print_matrix(matrix: List[List[int]], title: str = ""):
    if title:
        print(title)
    for row in matrix:
        print(" ".join(f"{elem:4}" for elem in row))
    print()
def form_matrix_f(a: np.ndarray) -> np.ndarray:
    """Формирование матрицы F на основе условий"""
    f = a.copy()
    n = a.shape[0]
    half = n // 2
    e_sub = f[:half, :half].copy()

    zero_count = np.sum(e_sub[:, 1::2] == 0)
    sum_odd = np.sum(e_sub[1::2, :])
    print(f"Количество нулей в нечетных столбцах E: {zero_count}")
    print(f"Сумма в нечетных строках E: {sum_odd}")

    if zero_count > sum_odd:
        # Симметричный обмен B и E
        print("меняем B и E симметрично")
        f[:half, :half], f[:half, half:] = \
            np.fliplr(f[:half, half:]), np.fliplr(e_sub)

    else:
        # Несимметричный обмен C и E
        print("меняем C и E несимметрично")
        f[:half, :half], f[half:, half:] = \
            f[half:, half:].copy(), e_sub.copy()

    return f


def plot_results(f: np.ndarray):
    """Визуализация результатов"""
    plt.figure(figsize=(15, 5))

    # Тепловая карта
    plt.subplot(131)
    plt.imshow(f, cmap='coolwarm')
    plt.title("Тепловая карта F")

    # 3D-визуализация
    plt.subplot(132, projection='3d')
    x, y = np.meshgrid(range(f.shape[0]), range(f.shape[1]))
    plt.gca().plot_surface(x, y, f, cmap='viridis')
    plt.title("3D поверхность")

    # Гистограмма распределения
    plt.subplot(133)
    plt.hist(f.flatten(), bins=20, edgecolor='black')
    plt.title("Распределение значений")

    plt.tight_layout()
    plt.show()



def main():
    K = int(input("Введите K: "))
    N = int(input("Введите N (четное): "))


    A = create_matrix_a(N)
    print_matrix(A, "Собранная матрица A:")

    F = form_matrix_f(A)
    print_matrix(F, "Матрица F после преобразования:")

    # Матричные операции
    det_A = np.linalg.det(A)
    trace_F = np.trace(F)
    print(f"det(A) = {det_A:.2f}")
    print(f"trace(F) = {trace_F:.2f}")

    if det_A > trace_F:
        print("\nВычисляем A⁻¹ * Aᵀ - K * F⁻¹")

        inv_A = np.linalg.inv(A)
        print_matrix(inv_A, "Обратная матрица A⁻¹")

        A_T = A.T
        print_matrix(A_T, "Транспонированная матрица Aᵀ")

        inv_F = np.linalg.inv(F)
        print_matrix(inv_F, "Обратная матрица F⁻¹")

        term1 = inv_A @ A_T
        print_matrix(term1, "Результат A⁻¹ * Aᵀ")

        term2 = K * inv_F
        print_matrix(term2, "Результат K * F⁻¹")

        result = term1 - term2
    else:
        print("\nВычисляем (A⁻¹ + G - F⁻¹) * K")

        inv_A = np.linalg.inv(A)
        print_matrix(inv_A, "Обратная матрица A⁻¹")

        G = np.tril(A)
        print_matrix(G, "Нижняя треугольная матрица G")

        inv_F = np.linalg.inv(F)
        print_matrix(inv_F, "Обратная матрица F⁻¹")

        sum_terms = inv_A + G - inv_F
        print_matrix(sum_terms, "Сумма A⁻¹ + G - F⁻¹")

        result = sum_terms * K

    print_matrix(result, "Финальный результат")
    plot_results(F)


if __name__ == "__main__":
    main()