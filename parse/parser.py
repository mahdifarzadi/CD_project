import io

from parse.first_follow import read_first_follow
from parse.grammar import read_grammar
from parse.parsing_table import generate_parsing_table


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
    return terminals


def get_non_terminals(first, follow):
    return list(first.keys())


def parse():
    grammar = read_grammar("test_grammar.txt")
    (first, follow) = read_first_follow("test_first.csv", "test_follow.csv")
    terminals = get_terminals(first, follow)
    non_terminals = get_non_terminals(first, follow)
    # print(terminals)
    # print(non_terminals)
    generate_parsing_table(non_terminals, terminals, first, follow, grammar)


if __name__ == '__main__':
    parse()
