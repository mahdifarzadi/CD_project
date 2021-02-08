semantic_stack = []
program_block = []
symbol_addr = {}
temp_table = {}
temp_index = 1000
symbol_index = 500

# symbol_index = 0
symbol_table = {}
scope_stack = [0]  # to do
cur_scope = 1
num_args = 1

functions = {}

return_stack = []

return_pointer = 5000
return_value_pointer = 6000


symbol_addr["output"] = symbol_index
symbol_table[symbol_index] = ["output", "func", "", 1, cur_scope, "void"]
symbol_index += 4


def generate_code(action, token):
    global temp_index
    global symbol_index
    global cur_scope
    global num_args
    global semantic_stack
    print(action, token)
    if action == "#pid":
        # semantic_stack.append(token)
        if token not in symbol_addr.keys():
            # name = semantic_stack.pop()
            type = semantic_stack.pop()
            symbol_addr[token] = symbol_index
            symbol_table[symbol_index] = [token, "var", type, 0, cur_scope, ""]
            program_block.append("(ASSIGN, #0, " + str(symbol_index) + ", )")
            symbol_index += 4
            # print("err")
        # else:
        semantic_stack.append(symbol_addr[token])

    elif action == "#ptype":
        semantic_stack.append(token)

    elif action == "#pvar":
        semantic_stack.append(token)

    elif action == "#var_dec":
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        name = semantic_stack.pop()
        type = semantic_stack.pop()
        symbol_addr[name] = symbol_index
        symbol_table[symbol_index] = [name, "var", type, 0, cur_scope, ""]
        program_block.append("(ASSIGN, #0, " + str(symbol_index) + ", )")
        symbol_index += 4

    elif action == "#func_dec":
        # to doooooooooooo array
        print("................................")
        name = semantic_stack.pop()
        type = semantic_stack.pop()
        symbol_addr[name] = symbol_index
        symbol_table[symbol_index] = [name, "func", "", 0, cur_scope, type, len(program_block)]
        # program_block.append("(ASSIGN, #0, " + str(symbol_index) + ", )")
        symbol_index += 4
        # semantic_stack.append("*func")
        cur_scope += 1
        functions[name] = []

    elif action == "#add_param":
        name = semantic_stack.pop()
        type = semantic_stack.pop()
        print(symbol_table)
        print(symbol_addr)
        # if name not in symbol_addr.keys():
        symbol_addr[name] = symbol_index
        symbol_table[symbol_index] = [name, "var", type, 0, cur_scope, ""]
        # program_block.append("(ASSIGN, #0, " + str(symbol_index) + ", )")

        functions[symbol_table[symbol_index - num_args * 4][0]].append(symbol_table[symbol_addr[name]])
        symbol_index += 4
        num_args += 1

    elif action == "#add_params":
        symbol_table[symbol_index - num_args * 4][3] = num_args - 1
        if symbol_table[symbol_index - num_args * 4][0] != "main":
            # semantic_stack.append(len(program_block))
            program_block.append("")
            print(symbol_index, num_args)
            symbol_table[symbol_index - num_args * 4][6] = len(program_block)
        num_args = 1

    elif action == "#func_end":
        cur_scope -= 1
        # remove scope variables
        # to_remove = [key for key in symbol_table if symbol_table[key][4] > cur_scope]
        # for key in to_remove:
        #     symbol_table.pop(key)

        # to do pb
        # if list(functions)[-1] != "main":
        #     program_block[semantic_stack.pop()] = "(JP, " + str(len(program_block)) + ", ,)"
        # print()
        if list(functions)[-1] == "main":
            for f in list(functions)[:-1]:
                print(f, symbol_table[symbol_addr[f]])
                p_i = int(symbol_table[symbol_addr[f]][6])
                main_i = int(symbol_table[symbol_addr["main"]][6])
                print(p_i, main_i)
                program_block[p_i-1] = "(JP, " + str(main_i) + ", ,)"
        else:
            program_block.append("(JP, @" + str(return_pointer) + ", ,)")

    elif action == "#func_call":
        num_args = 0
        pass

    elif action == "#get_arg":
        num_args += 1
        pass

    elif action == "#get_args":
        # get args and func name
        args = semantic_stack[-num_args:]
        semantic_stack = semantic_stack[:-num_args]
        func_name_addr = semantic_stack.pop()
        func_name = symbol_table[func_name_addr][0]
        print(func_name, args)
        num_args = 1

        # output
        if func_name == "output":
            program_block.append("(PRINT, " + str(args[0]) + ", , )")
            semantic_stack.append("pop")

        else:

            for i, a in enumerate(functions[func_name]):
                program_block.append("(ASSIGN, " + str(args[i]) + ", " + str(symbol_addr[a[0]]) + ", )")

            # program_block.append("(ASSIGN, #" + str(len(program_block)+3) + ", " + str(temp_index) + ", )")
            # program_block.append("(ASSIGN, #" + str(temp_index) + ", " + str(return_pointer) + ", )")
            # temp_index += 4

            program_block.append("(ASSIGN, #" + str(len(program_block)+2) + ", " + str(return_pointer) + ", )")

            func_addr = symbol_table[symbol_addr[func_name]][6]
            program_block.append("(JP, " + str(func_addr) + ", ,)")

            if symbol_table[symbol_addr[func_name]][5] == "int":
                program_block.append("(ASSIGN, @" + str(return_value_pointer) + ", " + str(temp_index) + ", )")
                semantic_stack.append(temp_index)
                temp_index += 4
            else:
                semantic_stack.append("pop")




    elif action == "#return_value":
        program_block.append("(ASSIGN, #" + str(semantic_stack.pop()) + ", " + str(return_value_pointer) + ", )")
        program_block.append("(JP, @" + str(return_pointer) + ", ,)")

    elif action == "#return_void":
        program_block.append("(JP, @" + str(return_pointer) + ", ,)")

    elif action == "#assign":
        op2 = semantic_stack.pop()
        op1 = semantic_stack.pop()
        semantic_stack.append(op1)
        program_block.append("(ASSIGN, " + str(op2) + ", " + str(op1) + ", )")

    elif action == "#pnum":
        temp_table[temp_index] = int(token)
        semantic_stack.append(temp_index)
        program_block.append("(ASSIGN, #" + str(token) + ", " + str(temp_index) + ", )")
        temp_index += 4

    elif action == "#pop":
        if len(semantic_stack) > 0:
            semantic_stack.pop()

    elif action == "#sign":
        semantic_stack.append(token)

    elif action == "#s_num":
        num_t = semantic_stack.pop()
        num = temp_table[num_t]
        sign = semantic_stack.pop()
        if sign == '-':
            num = -num
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
            ("(ADD, " if op == "+" else "(SUB, ") + str(o2) + ", " + str(o1) + ", " + str(temp_index) + ")")
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
        name = semantic_stack.pop()
        type = semantic_stack.pop()
        symbol_addr[name] = symbol_index
        symbol_table[symbol_index] = [name, "arr", type, 0, cur_scope, ""]
        program_block.append("(ASSIGN, #0, " + str(symbol_index) + ", )")
        symbol_index += 4
        for i in range(1, temp_table[length_t]):
            program_block.append("(ASSIGN, #0, " + str(symbol_index) + ", )")
            symbol_index += 4
        print("to doooooooooooooooo")

    elif action == "#access_arr":
        index = semantic_stack.pop()
        address = semantic_stack.pop()
        program_block.append("(MULT, #4, "+str(index)+", "+str(temp_index)+")")
        temp_index += 4
        semantic_stack.append("@"+str(temp_index))
        program_block.append("(ADD, "+str(address)+", " + str(temp_index-4) + ", " + str(temp_index) + ")")
        temp_index += 4

    # phase 4
    elif action == "#tmp_save":
        i = len(program_block)
        program_block.append("(JP, " + str(i+2) + ", ,)")
        program_block.append("")
        semantic_stack.append(i+1)

    elif action == "#cmp_save":
        op1 = semantic_stack.pop()
        op2 = semantic_stack[-1]
        program_block.append("(EQ, " + str(op1) + ", " + str(op2) + ", " + str(temp_index) + ")")
        semantic_stack.append(temp_index)
        temp_index += 4
        semantic_stack.append(len(program_block))
        program_block.append("")

    elif action == "#jp_break":
        program_block.append("(JP, " + str(semantic_stack[-4]) + ", ,)")

    elif action == "#jpf_switch":
        ind = semantic_stack[-1]
        i = len(program_block)
        program_block[ind] = "(JPF, " + str(semantic_stack[-2]) + ", " + str(i) + ",)"
        semantic_stack.pop()
        semantic_stack.pop()

    elif action == "#jp_switch":
        i = len(program_block)
        ind = semantic_stack[-2]
        program_block[ind] = "(JP, " + str(i) + ", ,)"
        semantic_stack.pop()
        semantic_stack.pop()

    # function
    elif action == "#fun_dec":
        print("***************************", token, semantic_stack)
        pass

    elif action == "#fun_call":
        pass


    print("semantic_stack: ", semantic_stack)
    print("symbol_table: ", symbol_table)
    print("symbol_addr: ", symbol_addr)
    print("program_block: ", program_block)
    print("functions: ", functions)
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
