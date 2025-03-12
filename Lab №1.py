# Написать программу, которая читая символы из бесконечной последовательности (эмулируется конечным файлом, читающимся поблочно),
# распознает, преобразует и выводит на экран лексемы по определенному правилу.
# Лексемы разделены пробелами.
# Преобразование делать по возможности через словарь.
# Для упрощения под выводом числа прописью подразумевается последовательный вывод всех цифр числа.
# Регулярные выражения использовать нельзя.
# Нечетные двоичные числа, не превышающие 4095(10), в которых встречается ровно одна серия из трех подряд идущих нуля.
# Выводит на экран цифры числа, исключая нули. Отдельно выводится прописью номер позиции, с которой начинается эта серия.
index_dict = {
    0: "ноль", 1: "один", 2: "два", 3: "три", 4: "четыре",
    5: "пять", 6: "шесть", 7: "семь", 8: "восемь", 9: "девять",
}

def check_number(binary_number):
    if int(binary_number) % 2 != 0 and int(binary_number, 2) <= 4095:
        count = binary_number.count('000')
        if count == 1:
            position = binary_number.find('000')
            return True, position
    return False, 0

def process_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            binary_number = line.strip()
            result, start_position = check_number(binary_number)
            if result:
                transformed_number = binary_number.replace('0', '')
                index_word = index_dict.get(start_position, str(start_position))
                print(f'{transformed_number} {index_word}')

process_file('numbers.txt')



