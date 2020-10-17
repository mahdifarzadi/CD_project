from scanner.scanner import *


# open file with 'file_name' name and return the file data
def read_file(file_name):
    with open(file_name) as file:
        return file.read()


# open file with 'file_name' name and write data into file
def write_file(file_name, data):
    with open(file_name, 'w') as file:
        file.write(data)


def compile():
    input_text = read_file("input.txt")
    find_tokens(input_text)


if __name__ == '__main__':
    compile()
