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

process_file('Числа.txt')

