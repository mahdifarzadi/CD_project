import io


def generate_parsing_table(non_terminals, terminals, first, follow, grammar):
    # print(first)
    # print(follow
    # parsing_table = [[] for j in range]
    # init_parsing_table(first, follow)
    parsing_table = [[""] * len(terminals) for i in range(len(non_terminals))]

    for (i, non_terminal) in enumerate(non_terminals):
        for (j, terminal) in enumerate(terminals):
            production = ""
            # print(terminal)
            # print(grammar_first[non_terminal])
            if terminal in first[non_terminal]:
                for p in grammar[non_terminal]:
                    if p.find(terminal) == 0 or (
                            p[0].isupper() and p.split(" ")[0] != "ID" and p.split(" ")[0] != "NUM" and terminal in
                            first[p.split(" ")[0]]):
                        production = p
                        break
            elif "ε" in first[non_terminal] and terminal in follow[non_terminal]:
                production = "ε"

            elif terminal in follow[non_terminal]:
                production = "sync"

            parsing_table[i][j] = production

    # print(non_terminals)
    # print(terminals)
    # print(*parsing_table, sep="\n")
    write_to_file(parsing_table, terminals, non_terminals)
    return parsing_table


def generate_parsing_table2(non_terminals, terminals, first, follow, grammar):
    parsing_table = [[""] * len(terminals) for i in range(len(non_terminals))]
    for (non_terminal, productions) in grammar.items():
        for p in productions:
            rules = p.split(" ")
            for rule in rules:
                if rule in non_terminals:
                    for t in first[rule]:
                        if t != "ε":
                            # if parsing_table[non_terminals.index(non_terminal)][terminals.index(t)] == "":
                                parsing_table[non_terminals.index(non_terminal)][terminals.index(t)] = p
                    if "ε" in first[rule]:
                        for t in follow[non_terminal]:
                            # if parsing_table[non_terminals.index(non_terminal)][terminals.index(t)] == "":
                                # parsing_table[non_terminals.index(non_terminal)][terminals.index(t)] = "ε"
                                parsing_table[non_terminals.index(non_terminal)][terminals.index(t)] = p
                elif rule != "ε":
                    # if parsing_table[non_terminals.index(non_terminal)][terminals.index(rule)] == "":
                        parsing_table[non_terminals.index(non_terminal)][terminals.index(rule)] = p
                else:
                    for t in follow[non_terminal]:
                        # if parsing_table[non_terminals.index(non_terminal)][terminals.index(t)] == "":
                            parsing_table[non_terminals.index(non_terminal)][terminals.index(t)] = p
                if rule in terminals or (rule in non_terminals and "ε" not in first[rule]):
                    break
    for A in non_terminals:
        for a in terminals:
            if parsing_table[non_terminals.index(A)][terminals.index(a)] == "":
                if a in follow[A]:
                    parsing_table[non_terminals.index(A)][terminals.index(a)] = "synch"
    write_to_file2(parsing_table, terminals, non_terminals)
    return parsing_table


# def generate_parsing_table3(non_terminals, terminals, first, follow, grammar):
#     parsing_table = [[""] * len(terminals) for i in range(len(non_terminals))]
#     for (non_terminal, productions) in grammar.items():
#         for p in productions:



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


def write_to_file2(parsing_table, terminals, non_terminals):
    text = " \t"
    tab = "\t"
    text += tab.join(terminals)
    text += "\n"
    for (r, row) in enumerate(parsing_table):
        text += non_terminals[r] + tab
        for col in row:
            text += col + tab
        text += "\n"
    file = io.open("./parse/parsing_table2.csv", mode="w", encoding="utf-8")
    file.write(text)
