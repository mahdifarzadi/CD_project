from parse.parser import parse


# mahdi farzadi  97106176
# ali eslami najad 97105747


# open file with 'file_name' name and return the file data
def read_file(file_name):
    with open(file_name) as file:
        return file.read()


# open file with 'file_name' name and write data into file
def write_file(file_name, data):
    with open(file_name, 'w') as file:
        file.write(data)


def compile():
    input_text = read_file("input.txt")
    parse(input_text)


if __name__ == '__main__':
    compile()
