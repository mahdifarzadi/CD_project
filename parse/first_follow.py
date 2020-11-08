import io


def read_first_follow(first_file_name, follow_file_name):
    first_file = io.open(first_file_name, mode="r", encoding="utf-8")
    follow_file = io.open(follow_file_name, mode="r", encoding="utf-8")
    first = dict()
    follow = dict()
    for line in first_file:
        line = line.replace("\n", "").strip().split(" ")
        first[line[0]] = list(line[1:])
    for line in follow_file:
        line = line.replace("\n", "").strip().split(" ")
        follow[line[0]] = list(line[1:])
    return first, follow
