def rotateRight(node):
    newRoot = node.left
    node.left = newRoot.right
    newRoot.right = node
    return newRoot

def rotateLeft(node):
    newRoot = node.right
    node.right = newRoot.left
    newRoot.left = node
    return newRoot

class AnderssonNode:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None
        self.level = 1

def anderssonTreeInsert(node,key):
    print(f"Inserting {key} into {node.key if node else 'Nothing'}")
    if node is None:
        return AnderssonNode(key)
    if node.key == key:
        return node
    if key < node.key:
        node.left  = anderssonTreeInsert(node.left, key)
        print(f"{node.key}.left is now {node.left.key}")
    else:
        node.right = anderssonTreeInsert(node.right, key)
        print(f"{node.key}.right is now {node.right.key}")
    if node.left is not None and node.level == node.left.level: # linke horizontale Kante
        print(f"rotateRight in node {node.key}:")
        node = rotateRight(node)  # wird zu rechter horizontaler Kante gemacht
        print(f"{node.key} has now left child {node.left.key} and right child {node.right.key}")
    if node.right is not None and node.right.right is not None and node.level==node.right.right.level:  # aufeinanderfolgende horizontale Kanten
        print(f"rotateLeft in node {node.key}:")
        node = rotateLeft(node)   # mache den mittleren Knoten zur Wurzel des Teilbaums
        node.level += 1           # und hebe die Wurzel um ein level an
        print(f"{node.key} in level {node.level} has now left child {node.left.key} and right child {node.right.key}")
    return node

def traverse(rootnode):
    thislevel = [rootnode]
    a = '                                        '
    while thislevel:
        nextlevel = list()
        a = a[:len(a)//2]
        for n in thislevel:
            print(f"{a} {str(n.key) if n else ''},{str(n.level) if n else ''}", end=' ')
            if not n:
                continue
            nextlevel.append(n.left)
            nextlevel.append(n.right)
        print()
        thislevel = nextlevel

# Baum anlegen
root = AnderssonNode(70)
root.left = AnderssonNode(50)
root.right = AnderssonNode(85)
root.left.left = AnderssonNode(35)
root.left.right = AnderssonNode(60)
root.right.left = AnderssonNode(80)
root.right.right = AnderssonNode(90)
root.left.left.right = AnderssonNode(40)
root.left.right.left = AnderssonNode(55)
root.left.right.right = AnderssonNode(65)

# Level passend setzen
root.level = 3
root.left.level = 2
root.right.level = 2
root.left.left.level = 1
root.left.right.level = 2
root.right.left.level = 1
root.right.right.level = 1
root.left.left.right.level = 1
root.left.right.left.level = 1
root.left.right.right.level = 1

traverse(root)

root = anderssonTreeInsert(root, 45)

traverse(root)
