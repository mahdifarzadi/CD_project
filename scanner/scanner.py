
def get_next_token(text,index):
    print(text[index],"+",end='')

##########
# token
##########

class Token:
    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __repr__(self):
        return '(%s,%s)' % (self.type,self.value)

############
# POSITION
############

class Position:
    def __init__(self, index, line):
        self.index = index
        self.line = line

    def advance(self, current_char):
        self.index += 1

        if current_char == '\n':
            self.line += 1

        return self

######
# lexer
#########
class Lexer:
    def __init__(self,text):
        self.text = text
        self.pos = Position(-1,0)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.index < len(self.text):
            self.current_char = self.text[self.pos.index]
        else:
            self.current_char = None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            get_next_token(self.text,self.pos.index)
            self.advance()
