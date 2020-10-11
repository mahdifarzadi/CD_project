from scanner.scanner import *
#test

def read_file():
    with open("input.txt") as file:
        return file.read()


def compile():
    input_text = read_file()
    get_next_token(input_text)


if __name__ == '__main__':
    compile()
