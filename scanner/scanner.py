# from compiler import write_file
from scanner.tokens import *


# function with while loop that return next tokens after the current position
def get_next_token(text):
    first_index = Position.index
    line = Position.line
    state = 0

    if Position.index >= len(text):
        return ("EOF", "$"), line

    while True:
        if type(tokens_dfa[state]) is dict and Position.index < len(text):
            for s in tokens_dfa[state].keys():
                if re.search(s, text[Position.index]):
                    state = tokens_dfa[state][s]
                    Position.advance(text)
                    break
            else:
                Position.advance(text)
                text_value = text[first_index: Position.index]
                if re.search(".*\n$", text_value):
                    text_value = text[first_index: Position.index - 1]
                return (get_error_type(text_value), text_value), line
        else:
            if Position.index >= len(text) and type(tokens_dfa[state]) is dict:
                if state in comment_states:
                    if Position.index - first_index > 7:
                        text_value = text[first_index: first_index + 7] + "..."
                    else:
                        text_value = text[first_index: Position.index]
                    return (get_error_type(text_value), text_value), line
                state = list(tokens_dfa[state].values())[-1]
            elif state in stars_states:
                Position.index -= 1
            if state == 'z':
                text_value = text[first_index:Position.index - 1]
            else:
                text_value = text[first_index:Position.index]
            if tokens_dfa[state] == "ID":
                if text_value in keywords:
                    return ("KEYWORD", text_value), line
                elif text_value not in symbol_table:
                    symbol_table.append(text_value)
            return (tokens_dfa[state], text[first_index: Position.index]), line


# a class with static func that handle position index and line
class Position:
    index = 0
    line = 1

    @staticmethod
    def advance(text):
        Position.index += 1
        if Position.index < len(text) and text[Position.index - 1] == '\n':
            Position.line += 1


# function that find all tokens of the text and write them in files
def find_tokens(text):
    tokens = {}
    errors = {}
    while Position.index < len(text):
        (token, line) = get_next_token(text)
        if token[0] == "WHITESPACE" or token[0] == "COMMENT":
            continue
        if token[0] in error_names:
            if line in errors:
                errors[line].append(token)
            else:
                errors[line] = [token]
        elif line in tokens:
            tokens[line].append(token)
        else:
            tokens[line] = [token]
    # write_tokens(tokens)
    # write_errors(errors)
    # write_symbols(symbol_table)


def write_file(file_name, data):
    with open(file_name, 'w') as file:
        file.write(data)


def write_tokens(tokens):
    string = ""
    for i, row in zip(tokens.keys(), tokens.values()):
        string += str(i)
        string += ".\t"
        for t in row:
            string += "("
            string += t[0]
            string += ", "
            string += t[1]
            string += ") "
        string += "\n"
    write_file("tokens.txt", string)


def write_errors(errors):
    string = ""
    if len(errors) > 0:
        for i, row in zip(errors.keys(), errors.values()):
            string += str(i)
            string += ".\t"
            for t in row:
                string += "("
                string += t[1]
                string += ", "
                string += t[0]
                string += ") "
            string += "\n"
    else:
        string = "There is no lexical error."
    write_file("lexical_errors.txt", string)


def write_symbols(symbol_table):
    string = ""
    for i, symbol in zip(range(len(symbol_table)), symbol_table):
        string += str(i + 1)
        string += ".\t"
        string += symbol
        string += "\n"
    write_file("symbol_table.txt", string)
