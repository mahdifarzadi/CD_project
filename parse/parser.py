import io
from anytree import Node, RenderTree

from parse.first_follow import read_first_follow
from parse.grammar import read_grammar
from parse.parsing_table import generate_parsing_table, read_from_file
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


def get_non_terminals(first):
    return list(first.keys())


def advance_tokens(input_text):
    while True:
        look_ahead = get_next_token(input_text)
        if look_ahead[0][0] not in ["COMMENT", "WHITESPACE"]:
            break
    return look_ahead


def add_node(root, name):
    return Node(name=name, parent=root)


def print_tree(root):
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))


def write_tree(root):
    string = ""
    for pre, fill, node in RenderTree(root):
        string += ("%s%s" % (pre, node.name))
        string += "\n"
    file = io.open("./parse_tree.txt", mode="w", encoding="utf-8")
    file.write(string)


def write_syntax_errors(errors):
    string = ""
    if len(errors) == 0:
        string = "There is no syntax error."
    else:
        for error in errors:
            string += "#" + str(error[0]) + " : syntax error, "
            if error[1] == 1:
                string += "missing "
            elif error[1] == 2:
                string += "illegal "
            elif error[1] == 3:
                string += "missing "
            elif error[1] == 4:
                string += "unexpected "
            string += error[2]
            string += "\n"
    file = io.open("./syntax_errors.txt", mode="w", encoding="utf-8")
    file.write(string)


def clean_tree(node, terminals, non_terminals, remove_eof):
    for l in node.leaves:
        if l.name == "$":
            if remove_eof:
                l.parent = None
        elif l.name in terminals or l.name in non_terminals:
            l.parent = None


def start_parsing(input_text, parsing_table, terminals, non_terminals):
    # initial stack
    stack = list()
    stack.append("$")
    stack.append(non_terminals[0])

    root = Node(non_terminals[0])
    current_node = root

    errors = list()

    advance = True
    look_ahead = None

    while True:
        if advance:
            look_ahead = advance_tokens(input_text)
        token = look_ahead[0][1]
        token_type = look_ahead[0][0]
        line = look_ahead[1]

        if stack[-1] == "$":
            if token == "$":
                print("ACCEPT")
                break
            else:
                print("error 1")
                break
        elif stack[-1] == token or stack[-1] == token_type:
            current_node.name = "(" + token_type + ", " + token + ")"
            advance = True
            stack.pop()
            flag = True
            while flag:
                flag2 = False
                for child in current_node.parent.children:
                    if flag2 and child.name == stack[-1]:
                        current_node = child
                        flag = False
                        break
                    if child.name == current_node.name:
                        flag2 = True
                else:
                    if current_node.depth == 0:
                        flag = False
                    else:
                        current_node = current_node.parent

        # panic-mode 1
        elif stack[-1] in terminals:
            advance = False
            if token == "$":
                errors.append([line, 4, token_type])
                clean_tree(root, terminals, non_terminals, True)
                break
            elif stack[-1] != token and stack[-1] != token_type:
                errors.append([line, 1, stack[-1]])
                stack.pop()
                flag = True
                while flag:
                    flag2 = False
                    for child in current_node.parent.children:
                        if flag2 and child.name == stack[-1]:
                            current_node = child
                            flag = False
                            break
                        if child.name == current_node.name:
                            flag2 = True
                    else:
                        if current_node.depth == 0:
                            flag = False
                        else:
                            current_node = current_node.parent
                continue

        elif stack[-1] in non_terminals:
            advance = False
            if token_type in ["ID", "NUM"]:
                production = parsing_table[non_terminals.index(stack[-1])][terminals.index(token_type)]
                a = token_type
            else:
                production = parsing_table[non_terminals.index(stack[-1])][terminals.index(token)]
                a = token
            # panic-mode 2
            if production == "":
                if token == "$":
                    errors.append([line + 1, 4, token_type])
                    clean_tree(root, terminals, non_terminals, True)
                    break
                errors.append([line, 2, a])
                advance = True
                continue
            # panic-mode 3
            elif production == "synch":
                errors.append([line, 3, stack[-1]])
                stack.pop()
                flag = True
                while flag:
                    flag2 = False
                    for child in current_node.parent.children:
                        if flag2 and child.name == stack[-1]:
                            current_node = child
                            flag = False
                            break
                        if child.name == current_node.name:
                            flag2 = True
                    else:
                        if current_node.depth == 0:
                            flag = False
                        else:
                            current_node = current_node.parent
                continue

            else:
                stack.pop()
                if production == "ε":
                    add_node(current_node, "epsilon")
                    flag = True
                    while flag:
                        flag2 = False
                        for child in current_node.parent.children:
                            if flag2 and child.name == stack[-1]:
                                current_node = child
                                flag = False
                                break
                            if child.name == current_node.name:
                                flag2 = True
                        else:
                            if current_node.depth == 0:
                                flag = False
                            else:
                                current_node = current_node.parent
                p_list = production.split(" ")
                next_node = None
                for t in p_list:
                    if t != "ε":
                        if next_node is None:
                            next_node = add_node(current_node, t)
                        else:
                            add_node(current_node, t)
                if next_node is not None:
                    current_node = current_node.children[0]
                p_list.reverse()
                for t in p_list:
                    if t != "ε":
                        stack.append(t)
        else:
            print("error 3")
            break
    clean_tree(root, terminals, non_terminals, False)
    return root, errors


def parse(input_text):
    grammar = read_grammar("./parse/pa2grammar.txt")
    (first, follow) = read_first_follow("./parse/Firsts.txt", "./parse/Follows.txt")
    terminals = get_terminals(first, follow)
    non_terminals = get_non_terminals(first)
    # parsing_table = generate_parsing_table(non_terminals, terminals, first, follow, grammar)
    parsing_table = read_from_file("./parse/parsing_table.csv")

    (parse_tree_root, errors) = start_parsing(input_text, parsing_table, terminals, non_terminals)

    write_tree(parse_tree_root)
    write_syntax_errors(errors)
