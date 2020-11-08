import io


def read_grammar(grammar_file_name):
    grammar_file = io.open(grammar_file_name, mode="r", encoding="utf-8")
    grammar = dict()
    for line in grammar_file:
        line = line.replace("\n", "")
        non_terminal = line.split("->")[0].strip()
        production = line.split("->")[1].strip()
        if non_terminal in grammar:
            grammar[non_terminal].append(production)
        else:
            grammar[non_terminal] = [production]
    return grammar
