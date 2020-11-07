from anytree import Node, RenderTree, PostOrderIter, PreOrderIter, LevelOrderGroupIter


def print_tree(root):
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))


a = Node("A")
b = Node("B", parent=a)
c = Node("C", parent=a)

print_tree(a)

print(a.children)

c.parent = None

for child in a.children:
    if child.name == "C":
        child = None

print_tree(a)
