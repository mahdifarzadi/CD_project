import re

# regex
digit = "[0-9]"
not_digit = "[^0-9]"
letter = "[A-Za-z]"
letter_or_digit = letter + "|" + digit
not_letter_and_digit = "[;:,\[\](){}+<=\/\*\r\t\f\v -]"
symbol = "[;:,\[\](){}+<-]"
whitespace = "\s"

# keywords and errors name
keywords = ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return']
symbol_table = ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return']
error_names = ['Invalid number', 'Invalid input', 'Unmatched comment', 'Unclosed comment']

# states that have star (pointer must decrease one)
stars_states = [2, 4, 9]

# states that in comment DFA
comment_states = ['a', 'b', 'c', 'd', 'e']

# implementing main DFA with python built-in dict
tokens_dfa = {0: {letter: 1, digit: 3, symbol: 5, '=': 6, '\*': 8, '\/': 'a', whitespace: 'f'},
              1: {letter_or_digit: 1, not_letter_and_digit: 2, '\n': 'z'}, 2: 'ID', 'z': 'ID',
              3: {digit: 3, not_letter_and_digit: 4}, 4: 'NUM',
              5: 'SYMBOL',
              6: {'=': 5, '[^=]': 9}, 9: 'SYMBOL',
              8: {'[^/]': 9},
              'a': {'\/': 'b', '\*': 'd'}, 'b': {'[^\\n]': 'b', '\\n': 'c'}, 'd': {'[^\*]': 'd', '\*': 'e'},
              'e': {'[^\*\/]': 'd', '\*': 'e', '[\/]': 'c'}, 'c': 'COMMENT',
              'f': 'WHITESPACE'
              }


# return error type of the input text
def get_error_type(text):
    if re.search("\*\/", text):
        return 'Unmatched comment'
    elif re.search('^/\*', text):
        return 'Unclosed comment'
    elif re.search("^\d", text):
        return 'Invalid number'
    else:
        return 'Invalid input'
