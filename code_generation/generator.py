semantic_stack = []
program_block = []
symbol_table = {}
temp_table = {}
temp_index = 1000
symbol_index = 500


# def find_addr(symbol):
#     global symbol_index
#     if symbol not in symbol_table.keys():
#         symbol_table[symbol] = symbol_index
#         symbol_index += 4
#     return symbol_table[symbol]
#
#
# def get_temp():
#     pass


def generate_code(action, token):
    global temp_index
    global symbol_index
    if action == "#pid":
        # print("pid", token)
        if token not in symbol_table.keys():
            symbol_table[token] = symbol_index
            program_block.append("(ASSIGN, #0, " + str(symbol_index) + ", )")
            symbol_index += 4
        # if token in symbol_table:
        # p = find_addr(token)
        semantic_stack.append(symbol_table[token])

        # else:
        #     symbol_table[symbol_index] = token
        #     print(symbol_table)



    elif action == "#add":
        # t = get_temp()

        print()


    elif action == "#mult":
        print()

    elif action == "#assign":
        # print("assign")
        op2 = semantic_stack.pop()
        op1 = semantic_stack.pop()
        semantic_stack.append(op1)
        program_block.append("(ASSIGN, " + str(op2) + ", " + str(op1) + ", )")

    elif action == "#add":
        print()

    elif action == "#pnum":

        # print("num")
        # t = temp_index
        # p = find_addr(arg)
        temp_table[temp_index] = int(token)
        semantic_stack.append(temp_index)
        # p = semantic_stack.pop()
        program_block.append("(ASSIGN, #" + str(token) + ", " + str(temp_index) + ", )")
        temp_index += 4

    elif action == "#pop":
        semantic_stack.pop()

    elif action == "#sign":
        semantic_stack.append(token)

    elif action == "#s_num":
        num_t = semantic_stack.pop()
        num = temp_table[num_t]
        sign = semantic_stack.pop()
        if sign == '-':
            num = -num
        # global temp_index
        semantic_stack.append(temp_index)
        program_block.append("(ASSIGN, #" + str(num) + ", " + str(temp_index) + ", )")
        temp_index += 4

    elif action == "#print":
        p = semantic_stack.pop()
        program_block.append("(PRINT, " + str(p) + ", , )")

    elif action == "#sum":
        o1 = semantic_stack.pop()
        op = semantic_stack.pop()
        o2 = semantic_stack.pop()
        semantic_stack.append(temp_index)
        program_block.append(
            ("(ADD, " if op == "+" else "(SUB, ") + str(o1) + ", " + str(o2) + ", " + str(temp_index) + ")")
        temp_index += 4

    elif action == "#multi":
        o1 = semantic_stack.pop()
        # op = semantic_stack.pop()
        o2 = semantic_stack.pop()
        semantic_stack.append(temp_index)
        program_block.append("(MULT, " + str(o1) + ", " + str(o2) + ", " + str(temp_index) + ")")
        temp_index += 4

    elif action == "#label":
        semantic_stack.append(len(program_block) - 1)

    elif action == "#save":
        program_block.append("")
        semantic_stack.append(len(program_block) - 1)

    elif action == "#jp":
        pi = semantic_stack.pop()
        program_block[pi] = "(JP, " + str(len(program_block)) + ", ,)"

    elif action == "#jpf_save":
        pi = semantic_stack.pop()
        i = semantic_stack.pop()
        semantic_stack.append(len(program_block))
        program_block.append("")
        program_block[pi] = "(JPF, " + str(i) + ", " + str(len(program_block)) + ",)"

    elif action == "#while":
        pi2 = semantic_stack.pop()
        i = semantic_stack.pop()
        pi1 = semantic_stack.pop()
        program_block.append("(JP, " + str(pi1+1) + ", ,)")
        program_block[pi2] = "(JPF, " + str(i) + ", " + str(len(program_block)) + ",)"

    elif action == "#if_s":
        semantic_stack.append(token)

    elif action == "#if":
        o1 = semantic_stack.pop()
        op = semantic_stack.pop()
        o2 = semantic_stack.pop()
        semantic_stack.append(temp_index)
        program_block.append(("(LT, " if op == "<" else "(EQ, ") + str(o2) + ", " + str(o1) + ", " + str(temp_index) + ")")
        temp_index += 4

    elif action == "#init_arr":
        length_t = semantic_stack.pop()
        for i in range(1, temp_table[length_t]):
            program_block.append("(ASSIGN, #0, " + str(symbol_index) + ", )")
            symbol_index += 4

    elif action == "#access_arr":
        index = semantic_stack.pop()
        address = semantic_stack.pop()
        program_block.append("(MULT, #4, "+str(index)+", "+str(temp_index)+")")
        temp_index += 4
        semantic_stack.append("@"+str(temp_index))
        program_block.append("(ADD, "+str(address)+", " + str(temp_index-4) + ", " + str(temp_index) + ")")
        temp_index += 4

    print(action, token)
    print(semantic_stack)
    print(symbol_table)
    print(program_block)
    print()


def write_to_file():
    string = ""
    for i, p in enumerate(program_block):
        string += str(i)
        string += "\t"
        string += p
        string += "\n"
    with open("output.txt", 'w') as file:
        file.write(string)
