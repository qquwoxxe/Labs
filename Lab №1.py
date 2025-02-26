# Написать программу, которая читая символы из бесконечной последовательности (эмулируется конечным файлом, читающимся поблочно), распознает, преобразует и выводит на экран лексемы по определенному правилу. Лексемы разделены пробелами. Преобразование делать по возможности через словарь. Для упрощения под выводом числа прописью подразумевается последовательный вывод всех цифр числа. Регулярные выражения использовать нельзя.
# Нечетные двоичные числа, не превышающие 409510, в которых встречается ровно одна серия из трех подряд идущих нуля. Выводит на экран цифры числа, исключая нули. Отдельно выводится прописью номер позиции, с которой начинается эта серия.
def check_number(number):
    if number % 2 != 0 and number <= 4095:
        binary_number = format(number, '012b')

        for i in range(len(binary_number) - 2):
            if binary_number[i:i+3] == '000':
                return True, i
    return False, 0

def infinite_sequence():
    num = 1
    while True:
        yield num
        num += 1

numbers = infinite_sequence()

for number in numbers:
    result, start_position = check_number(number)
    if result:
        binary_number = format(number, '012b')
        transformed_number = ''.join([digit for digit in binary_number if digit != '0'])
        print(f'{transformed_number} {start_position}')
    if number >= 4095:
        break



