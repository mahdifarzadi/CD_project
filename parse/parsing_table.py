import io

import re


def generate_parsing_table(non_terminals, terminals, first, follow, grammar):
    parsing_table = [[""] * len(terminals) for i in range(len(non_terminals))]
    for (non_terminal, productions) in grammar.items():
        for p in productions:
            rules = p.split(" ")
            for rule in rules:
                if rule in non_terminals:
                    for t in first[rule]:
                        if t != "ε":
                            parsing_table[non_terminals.index(non_terminal)][terminals.index(t)] = p
                    if "ε" in first[rule]:
                        for t in follow[non_terminal]:
                            parsing_table[non_terminals.index(non_terminal)][terminals.index(t)] = p
                elif rule != "ε" and not re.match('^#\w+$', rule):
                    parsing_table[non_terminals.index(non_terminal)][terminals.index(rule)] = p
                elif rule == "ε":
                    for t in follow[non_terminal]:
                        parsing_table[non_terminals.index(non_terminal)][terminals.index(t)] = p
                if rule in terminals or (rule in non_terminals and "ε" not in first[rule]):
                    break
    for A in non_terminals:
        for a in terminals:
            if parsing_table[non_terminals.index(A)][terminals.index(a)] == "":
                if a in follow[A]:
                    parsing_table[non_terminals.index(A)][terminals.index(a)] = "synch"
    write_to_file(parsing_table, terminals, non_terminals)
    return parsing_table


def write_to_file(parsing_table, terminals, non_terminals):
    text = " \t"
    tab = "\t"
    text += tab.join(terminals)
    text += "\n"
    for (r, row) in enumerate(parsing_table):
        text += non_terminals[r] + tab
        for col in row:
            text += col + tab
        text += "\n"
    file = io.open("./parse/parsing_table.csv", mode="w", encoding="utf-8")
    file.write(text)


def read_from_file(address):
    file = io.open(address, mode="r", encoding="utf-8")
    p = file.read()
    parsing_table = list()
    for e in p.split("\n")[1:-1]:
        parsing_table.append(e.split("\t")[1:-1])
    return parsing_table
