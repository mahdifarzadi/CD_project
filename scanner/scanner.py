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
                #print(text[Position.index], s)
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
            if state in stars_states:
                Position.index -= 1
            elif Position.index > len(text):
                state = list(tokens_dfa[state].values())[-1]
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
        if Position.index < len(text) and text[Position.index-1] == '\n':
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
        # pos = 0

        while Position.index < len(self.text):
            (token, line) = get_next_token(self.text)
            #print(token)
            if token[0] == "WHITESPACE":
                continue
            #print(token,line)
            if line in tokens:
                tokens[line].append(token)
            else:
                tokens[line] = [token]
        #print(tokens)
        for row in tokens:
            print(row,"-",tokens[row])
        # print(Position.index)

            # self.advance()
