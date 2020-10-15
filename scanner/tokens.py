import re


# class Token:
#     def __init__(self, type, value):
#         self.type = type
#         self.value = value
#
#     def __repr__(self):
#         return '(%s, %s)' % (self.type, self.value)


digit = "[0-9]"
not_digit = "[^0-9]"
letter = "[A-Za-z]"
letter_or_digit = letter + "|" + digit
#not_letter_and_digit = "[^A-Za-z0-9]"
not_letter_and_digit = "[;:,\[\](){}+<=\/\*\s-]"
symbol = "[;:,\[\](){}+<-]"
whitespace = "\s"

keywords = ['if','else','void','int','while','break','switch','default','case','return','main']
symbol_table = ['if','else','void','int','while','break','switch','default','case','return','main']
error_names = ['Invalid number','Invalid input','Unmatched comment']

stars_states = [2, 4, 9]


tokens_dfa = {0: {letter: 1, digit: 3, symbol: 5, '=': 6, '\*': 8, '\/': 'a', whitespace: 'f'},
              1: {letter_or_digit: 1, not_letter_and_digit: 2}, 2: 'ID',
              3: {digit: 3, not_letter_and_digit: 4}, 4: 'NUM',
              5: 'SYMBOL',
              6: {'=': 5, '[^=]': 9}, 9: 'SYMBOL',
              8: {'[^/]': 9},
              'a': {'\/': 'b', '\*': 'd'}, 'b': {'[^\\n]': 'b', '\\n': 'c'}, 'd': {'[^\*]': 'd', '\*': 'e'}, 'e': {'[^\*\/]': 'd', '\*': 'e', '[\/]': 'c'}, 'c': 'COMMENT',
              'f': 'WHITESPACE'
              }


def get_error_type(text):
    if re.search("\*\/",text):
        return 'Unmatched comment'
    elif re.search("^\d", text):
        return 'Invalid number'
    else:
        return 'Invalid input'


if __name__ == '__main__':
    print(re.search(not_letter_and_digit, "d"))




