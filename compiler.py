from scanner.scanner import *


def read_file(file_name):
    with open(file_name) as file:
        return file.read()


def write_file(file_name, data):
    with open(file_name, 'w') as file:
        file.write(data)


def compile():
    input_text = read_file("input.txt")
    find_tokens(input_text)


if __name__ == '__main__':
    compile()
