import io


def read_first_follow(first_file_name, follow_file_name):
    first_file = io.open(first_file_name, mode="r", encoding="utf-8")
    follow_file = io.open(follow_file_name, mode="r", encoding="utf-8")

    first = dict()
    follow = dict()

    for line in first_file:
        # print(line)
        line = line.replace("\n", "").split(" ")
        # print(line)
        first[line[0]] = list(line[1:])
        # print(first)

    for line in follow_file:
        # print(line)
        line = line.replace("\n", "").split(" ")
        # print(line)
        follow[line[0]] = list(line[1:])
        # print(first)

    # print(first)
    # print(follow)

    return first, follow

    # print(first_file)
    # print(follow_file)


if __name__ == '__main__':
    read_first_follow("test_first.csv", "test_follow.csv")

