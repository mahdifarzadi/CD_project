
semantic_stack = []
program_block = []
symbol_table = {}
temp_index = 1000
symbol_index = 500


def findAddr(symbol):
    for s in symbol_table:
        if s[0] == symbol:
            return s[1]


def getTemp():
    pass

def generate_code(action,token):
    if action == "#pid":
        print("pid",token)
        if token in symbol_table:
            p = findAddr(input)
            semantic_stack.append(p)
        else:
            symbol_table[symbol_index] = token
            print(symbol_table)
            symbol_index = 4


    elif action == "#add":
        t = getTemp()

        print()


    elif action == "#mult":
        print()

    elif action == "#assign":
        print()

    elif action == "#add":
        print()




