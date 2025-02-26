# Написать программу, которая читая символы из бесконечной последовательности (эмулируется конечным файлом, читающимся поблочно), распознает, преобразует и выводит на экран лексемы по определенному правилу. Лексемы разделены пробелами. Преобразование делать по возможности через словарь. Для упрощения под выводом числа прописью подразумевается последовательный вывод всех цифр числа. Регулярные выражения использовать нельзя.
# Нечетные двоичные числа, не превышающие 409510, в которых встречается ровно одна серия из трех подряд идущих нуля. Выводит на экран цифры числа, исключая нули. Отдельно выводится прописью номер позиции, с которой начинается эта серия.
# Изменения:
# 1.Входной файл является обыкновенным (т.е. нет требования на «бесконечность» файла);
# 2.Распознавание и обработку делать  через регулярные выражения;
# 3.В вариантах, где есть параметр (например К), допускается его заменить на любое число(константу);
import re

def check_number(number):
    if number % 2 != 0 and number <= 4095:
        binary_number = format(number, '012b')
        if re.search(r'000', binary_number):
            start_position = binary_number.index('000')
            return True, start_position
    return False, 0

def process_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            number = int(line.strip())
            result, start_position = check_number(number)
            if result:
                binary_number = format(number, '012b')
                transformed_number = ''.join(digit for digit in binary_number if digit != '0')
                print(f'{transformed_number} {start_position}')

process_file('input.txt')

