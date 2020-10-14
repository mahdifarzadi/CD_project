from scanner.scanner import *


def read_file():
    with open("input.txt") as file:
        return file.read()


def compile():
    input_text = read_file()
    #get_next_token(input_text)
    lex = Lexer(input_text)
    lex.make_tokens()

if __name__ == '__main__':
    compile()
