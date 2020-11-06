import io
from anytree import Node, RenderTree, PostOrderIter, PreOrderIter, LevelOrderGroupIter

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
    for error in errors:
        string += "#"+str(error[0])+" : syntax error, "
        if error[1]==1:
            string += "Missing "
        elif error[1]==2:
            string += "illegal "
        elif error[1]==3:
            string += "Missing "
        elif error[1]==4:
            string += "unexpected "

        string += error[2]
        string += "\n"

    file = io.open("./syntax_errors.txt", mode="w", encoding="utf-8")
    file.write(string)


def start_parsing(input_text, grammar, parsing_table, first, follow, terminals, non_terminals):

    # initial stack
    stack = list()
    stack.append("$")
    stack.append(non_terminals[0])
    root = Node(non_terminals[0])
    current_node = root
    errors = list()
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
        print(look_ahead,stack[-1])
        # print(token_type, token, line)
        if token_type == "EOF" and stack[-1] != "$":
            #errors.append([line+1, 4, "EOF"])
            break

        # current_node = stack[-1]

        if stack[-1] == "$":
            if token == "$":
                print("ACCEPT")
                break
            else:
                print("error 1")
                break

        elif stack[-1] == token or stack[-1] == token_type:
            # add_node(current_node, "("+token_type+", "+token+")")
            current_node.name = "("+token_type+", "+token+")"
            print("matched ", token)
            advance = True
            stack.pop()

            flag = True
            while flag:
                flag2 = False
                for child in current_node.parent.children:
                    print(child)
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

        #panic-mode 1
        elif stack[-1] in terminals:
            if stack[-1] != token and stack[-1] != token_type:
                print("panic mode 3")
                errors.append([line, 1, stack[-1]])
                stack.pop()
                continue


        elif stack[-1] in non_terminals:
            advance = False
            if token_type in ["ID", "NUM"]:
                production = parsing_table[non_terminals.index(stack[-1])][terminals.index(token_type)]
                a = token_type
            else:
                production = parsing_table[non_terminals.index(stack[-1])][terminals.index(token)]
                a = token
            print(stack[-1],", ",a, " -> ", production)
            #panic-mode 2
            if production == "":
                print("error 2")
                errors.append([line, 2, a])
                advance = True
                continue
            #panic-mode 3
            elif production == "synch":
                print("synch")
                errors.append([line,3,stack[-1]])
                stack.pop()
                continue

            else:
                stack.pop()
                if production == "ε":
                    add_node(current_node, "epsilon")
                    #print("ε cn: ", current_node)
                    flag = True
                    while flag:
                        flag2 = False
                        for child in current_node.parent.children:
                            #print(child)
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
                        # add_node(current_node, t)
                        stack.append(t)
                    # else:
                    #     add_node(current_node, "epsilon")

        else:
            print("error 3")
            break

        #print(stack)
        # print(advance_tokens(input_text))
        # print(advance_tokens(input_text))
        #print_tree(root)
        #print(current_node)
        #print("\n\n")

    print_tree(root)
    write_tree(root)
    print(errors)
    write_syntax_errors(errors)


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
