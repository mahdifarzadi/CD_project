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


def generate_code(action, token):
    global temp_index
    global symbol_index
    if action == "#pid":
        # print("pid", token)
        if token not in symbol_table.keys():
            symbol_table[token] = symbol_index
            program_block.append("(ASSIGN pid, #0, " + str(symbol_index) + ", )")
            symbol_index += 4
        # if token in symbol_table:
        # p = find_addr(token)
        semantic_stack.append(symbol_table[token])

        # else:
        #     symbol_table[symbol_index] = token
        #     print(symbol_table)



    elif action == "#add":
        t = get_temp()

        print()


    elif action == "#mult":
        print()

    elif action == "#assign":
        # print("assign")
        op2 = semantic_stack.pop()
        op1 = semantic_stack.pop()
        semantic_stack.append(op1)
        program_block.append("(ASSIGN as, " + str(op2) + ", " + str(op1) + ", )")

    elif action == "#add":
        print()

    elif action == "#pnum":

        # print("num")
        # t = temp_index
        # p = find_addr(arg)
        semantic_stack.append(temp_index)
        # p = semantic_stack.pop()
        program_block.append("(ASSIGN num, #" + str(token) + ", " + str(temp_index) + ", )")
        temp_index += 4

    elif action == "#pop":
        semantic_stack.pop()

    elif action == "#sign":
        semantic_stack.append(token)

    elif action == "#signed_num":
        num = semantic_stack.pop()
        sign = semantic_stack.pop()
        if sign == '-':
            num = -num
        # global temp_index
        semantic_stack.append(temp_index)
        program_block.append("(ASSIGN num, #" + str(num) + ", " + str(temp_index) + ", )")
        temp_index += 4

    elif action == "#print":
        p = semantic_stack.pop()
        program_block.append("(PRINT, " + str(p) + ", , )")

    print(action, token)
    print(semantic_stack)
    print(symbol_table)
    print(program_block)
    print()
