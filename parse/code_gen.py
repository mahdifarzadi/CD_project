
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
    #

def generate_code(action):
    if action=="#pid" :
        print()
        p = findAddr(input)
        semantic_stack.append(p)

    elif action == "#add":
        t = getTemp()
        
        print()


    elif action == "#mult":
        print()

    elif action == "#assign":
        print()

    elif action == "#add":
        print()

