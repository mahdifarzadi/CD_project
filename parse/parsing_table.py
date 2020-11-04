def generate_parsing_table(non_terminals, terminals, first, follow, grammar):
    # print(first)
    # print(follow
    # parsing_table = [[] for j in range]
    # init_parsing_table(first, follow)
    parsing_table = [[""]*len(terminals) for i in range(len(non_terminals))]

    for (i, non_terminal) in enumerate(non_terminals):
        for (j, terminal) in enumerate(terminals):
            production = ""
            # print(terminal)
            # print(grammar_first[non_terminal])
            if terminal in first[non_terminal]:
                for p in grammar[non_terminal]:
                    if p.find(terminal) == 0 or (p[0].isupper() and terminal in first[p.split(" ")[0]]):
                        production = p
                    # elif production[0].isupper() and terminal in first[production.split(" ")[0]]:
                    #     rule = production
                # pass
                # rule = get_rule(non_terminal, terminal, grammar, grammar_first)
                # print(rule)

            elif "ε" in first[non_terminal] and terminal in follow[non_terminal]:
                production = "ε"

            elif terminal in follow[non_terminal]:
                production = "sync"

            parsing_table[i][j] = production

    # print(non_terminals)
    # print(terminals)
    # print(*parsing_table, sep="\n")
    return parsing_table


