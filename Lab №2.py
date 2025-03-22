# Написать программу, которая читая символы из бесконечной последовательности (эмулируется конечным файлом, читающимся поблочно), распознает, преобразует и выводит на экран лексемы по определенному правилу. Лексемы разделены пробелами. Преобразование делать по возможности через словарь. Для упрощения под выводом числа прописью подразумевается последовательный вывод всех цифр числа. Регулярные выражения использовать нельзя.
# Нечетные двоичные числа, не превышающие 409510, в которых встречается ровно одна серия из трех подряд идущих нуля. Выводит на экран цифры числа, исключая нули. Отдельно выводится прописью номер позиции, с которой начинается эта серия.
# Изменения:
# 1.Входной файл является обыкновенным (т.е. нет требования на «бесконечность» файла);
# 2.Распознавание и обработку делать  через регулярные выражения;
# 3.В вариантах, где есть параметр (например К), допускается его заменить на любое число(константу);

import re

index_dict = {
    0: "ноль", 1: "один", 2: "два", 3: "три", 4: "четыре",
    5: "пять", 6: "шесть", 7: "семь", 8: "восемь", 9: "девять",
}

def extract_binary(part):
    matched = re.match(r'^[01]{1,12}$', part)
    return matched.group(0) if matched else None

def check_number(binary_number):
    if int(binary_number, 2) % 2 != 0 and int(binary_number, 2) <= 4095:
        position = binary_number.find('000')
        if position != -1 and binary_number.count('000') == 1:
            return True, position
    return False, 0


def process_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            for part in line.strip().split():
                binary_number = extract_binary(part)
                if binary_number:
                    result, start_position = check_number(binary_number)
                    if result:
                        transformed_number = binary_number.replace('0', '')
                        index_word = index_dict.get(start_position, str(start_position))
                        print(f'{transformed_number} {index_word}')


process_file('numbers.txt')
