import io

from parse.first_follow import read_first_follow
from parse.grammar import read_grammar
from parse.parsing_table import generate_parsing_table, generate_parsing_table2
from scanner.scanner import get_next_token


def get_terminals(first, follow):
    terminals = list()
    for rule in first.values():
        for terminal in rule:
            if terminal != "ε" and terminals.count(terminal) == 0:
                terminals.append(terminal)
    for rule in follow.values():
        for terminal in rule:
            if terminal != "ε" and terminals.count(terminal) == 0:
                terminals.append(terminal)
    terminals.append(":")
    return terminals


def get_non_terminals(first, follow):
    return list(first.keys())


def advance_tokens(input_text):
    while True:
        look_ahead = get_next_token(input_text)
        # print(look_ahead)
        # print(look_ahead[0])
        # print(look_ahead[0][0])
        if look_ahead[0][0] not in ["COMMENT", "WHITESPACE"]:
            break
    return look_ahead


def start_parsing(input_text, grammar, parsing_table, first, follow, terminals, non_terminals):

    # initial stack
    stack = list()
    stack.append("$")
    stack.append(non_terminals[0])
    # print(non_terminals)
    # print(stack, "\n\n\n")
    # return

    advance = True

    look_ahead = None

    while True:
        if advance:
            look_ahead = advance_tokens(input_text)
        token = look_ahead[0][1]
        token_type = look_ahead[0][0]
        line = look_ahead[1]
        # if token_type in ["ID", "NUM"]:
        #     token = token_type
        # print(look_ahead)
        # print(token_type, token, line)
        # if token_type == "EOF":
        #     break

        if stack[-1] == "$":
            if token == "$":
                print("ACCEPT")
                break
            else:
                print("error")
                break
        elif stack[-1] == token or stack[-1] == token_type:
            print("matched ", token)
            advance = True
            stack.pop()
        elif stack[-1] in non_terminals:
            advance = False
            if token_type in ["ID", "NUM"]:
                production = parsing_table[non_terminals.index(stack[-1])][terminals.index(token_type)]
            else:
                production = parsing_table[non_terminals.index(stack[-1])][terminals.index(token)]
            # print(stack[-1], " -> ", production)
            if production == "":
                print("error")
                break
            else:
                stack.pop()
                p_list = production.split(" ")
                p_list.reverse()
                for t in p_list:
                    if t != "ε":
                        stack.append(t)
        else:
            print("error")
            break

        # print(stack, "\n\n")
        # print(advance_tokens(input_text))
        # print(advance_tokens(input_text))


def parse(input_text):
    # grammar = read_grammar("./parse/test_grammar.txt")
    # (first, follow) = read_first_follow("./parse/test_first.csv", "./parse/test_follow.csv")
    #
    grammar = read_grammar("./parse/grammar.txt")
    (first, follow) = read_first_follow("./parse/Firsts.csv", "./parse/Follows.csv")

    # for (key, value) in first.items():
    #     print(key, " -> ", value)

    terminals = get_terminals(first, follow)
    non_terminals = get_non_terminals(first, follow)

    # print(terminals)
    # print(non_terminals)
    # print(len(non_terminals))
    # print(len(terminals))
    # print(terminals[3], terminals[20])
    parsing_table = generate_parsing_table2(non_terminals, terminals, first, follow, grammar)
    # print(*parsing_table, sep="\n")

    start_parsing(input_text, grammar, parsing_table, first, follow, terminals, non_terminals)


if __name__ == '__main__':
    # parse()
    pass
