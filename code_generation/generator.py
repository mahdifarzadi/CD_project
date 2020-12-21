semantic_stack = []
program_block = []
symbol_table = {}
temp_index = 1000
symbol_index = 500


def find_addr(symbol):
    global symbol_index
    if symbol not in symbol_table.keys():
        symbol_table[symbol] = symbol_index
        symbol_index += 4
    return symbol_table[symbol]


def get_temp():
    pass


def generate_code(action, arg=None):
    if action == "#pid":
        print("piiid")
        p = find_addr(arg)
        semantic_stack.append(p)
        program_block.append("(ASSIGN pid, #0, " + str(p) + ", )")
        print(semantic_stack)
        print(symbol_table)
        print(program_block)

    elif action == "#add":
        t = get_temp()

        print()


    elif action == "#mult":
        print()

    elif action == "#assign":
        op2 = semantic_stack.pop()
        op1 = semantic_stack.pop()
        semantic_stack.append(op1)
        program_block.append("(ASSIGN as, " + str(op2) + ", " + str(op1) + ", )")

    elif action == "#add":
        print()

    elif action == "#pnum":
        # print("num")
        t = get_temp()
        # p = find_addr(arg)
        semantic_stack.append(t)
        program_block.append("(ASSIGN num, #" + str(arg) + ", " + str(t) + ", )")
