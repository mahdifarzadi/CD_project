# import re

from scanner.tokens import *


def get_next_token(text):
    # print(text[index], "+", end='')
    # return
    # pos = index
    first_index = Position.index
    line = Position.line
    state = 0
    token = None
    # dfa = tokens_dfa[state]
    while True:
        if type(tokens_dfa[state]) is dict and Position.index < len(text):
            # matched = False
            for s in tokens_dfa[state].keys():
                # print(text[Position.index], s)
                if re.search(s, text[Position.index]):
                    # matched = True
                    state = tokens_dfa[state][s]
                    Position.advance(text)
                    break
                # elif pos >= len(text):
                #     matched = True
                #     break
                #     break
            else:

                Position.advance(text)
                text_value = text[first_index: Position.index]
                # if re.search(get_error_type(text_value), text_value)
                return (get_error_type(text_value), text_value), line

            # if not matched:
            #     pos += 1
            #     return ("e", text[index:pos]), pos
        else:
            if Position.index >= len(text):
                if state in comment_states:
                    # print("---------------", state, Position.index, Position.line)
                    if Position.index - first_index > 7:
                        text_value = text[first_index: first_index + 7] + "..."
                    else:
                        text_value = text[first_index: Position.index]
                    return (get_error_type(text_value), text_value), line
                # print("*********", state)
                state = list(tokens_dfa[state].values())[-1]
                # print("*********2", state)
            elif state in stars_states:
                # print("+++++++++", state, Position.index, Position.line)
                Position.index -= 1
            # elif Position.index > len(text):
            #     if state in comment_states:
            #         print("---------------", state, Position.index, Position.line)
            #     print("*********", state)
            #     state = list(tokens_dfa[state].values())[-1]

            # KEYWORD
            if tokens_dfa[state] == "ID":
                if text[first_index:Position.index] in keywords:
                    return ("KEYWORD", text[first_index: Position.index]), line
                elif text[first_index:Position.index] not in symbol_table:
                    symbol_table.append(text[first_index:Position.index])

            return (tokens_dfa[state], text[first_index: Position.index]), line


##########
# token
##########

# class Token:
#     def __init__(self, type, value):
#         self.type = type
#         self.value = value
#
#     def __repr__(self):
#         return '(%s,%s)' % (self.type, self.value)


############
# POSITION
############

class Position:
    index = 0
    line = 1

    @staticmethod
    def advance(text):
        Position.index += 1
        # print(Position.index, Position.line)
        if Position.index < len(text) and text[Position.index - 1] == '\n':
            Position.line += 1


######
# lexer
#########
class Lexer:
    def __init__(self, text):
        self.text = text
        # self.pos = Position(-1, 0)
        # self.current_char = None
        # self.advance()

    # def advance(self):
    #     self.pos.advance(self.current_char)
    #     if self.pos.index < len(self.text):
    #         self.current_char = self.text[self.pos.index]
    #     else:
    #         self.current_char = None

    def find_tokens(self):
        tokens = {}
        errors = {}
        # pos = 0

        while Position.index < len(self.text):
            (token, line) = get_next_token(self.text)
            # print(token)
            if token[0] == "WHITESPACE" or token[0] == "COMMENT":
                continue

            # errors
            if token[0] in error_names:
                if line in errors:
                    errors[line].append(token)
                else:
                    errors[line] = [token]

            # print(token,line)
            elif line in tokens:
                tokens[line].append(token)
            else:
                tokens[line] = [token]

        # print(tokens)
        write_tokens(tokens)
        # for row in tokens:
        #     print(row, "-", tokens[row])

        write_errors(errors)
        # print("#### ERRORS #####")
        # for row in errors:
        #     print(row, "-", errors[row])

        write_symbols(symbol_table)
        # print("#### SYMBOL_TABLE #####")
        # for i in range(len(symbol_table)):
        #     print(i, " ", symbol_table[i])

        # print(Position.index)

        # self.advance()


def write_tokens(tokens):
    string = ""
    for i, row in zip(tokens.keys(), tokens.values()):
        string += str(i)
        string += ".\t\t"
        # print(row)
        for t in row:
            string += "("
            string += t[0]
            string += ", "
            string += t[1]
            string += ") "
        string += "\n"
    with open("tokens.txt", 'w') as file:
        file.write(string)


def write_errors(errors):
    string = ""
    if len(errors) > 0:
        for i, row in zip(errors.keys(), errors.values()):
            string += str(i)
            string += ".\t\t"
            # print(row)
            for t in row:
                string += "("
                string += t[1]
                string += ", "
                string += t[0]
                string += ") "
            string += "\n"
    else:
        string = "There is no lexical error."

    with open("lexical_errors.txt", 'w') as file:
        file.write(string)


def write_symbols(symbol_table):
    string = ""
    for i, symbol in zip(range(len(symbol_table)), symbol_table):
        string += str(i+1)
        string += ".\t\t"
        # print(row)
        # for t in row:
        # string += "("
        string += symbol
        # string += ", "
        # string += row[0]
        # string += ") "
        string += "\n"

    with open("symbol_table.txt", 'w') as file:
        file.write(string)
