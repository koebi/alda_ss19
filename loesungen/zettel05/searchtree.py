import unittest

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = self.right = None

    def __repr__(self):
        return f'({self.key}: {self.value})'


class SearchTree:
    def __init__(self):
        self.root = None
        self.size = 0
    
    def __len__(self):
        return self.size

    def __insert(self, node, key, value):
        if node is None:
            self.size += 1 # key not yet in tree, hence size is increased
            return Node(key, value)
        elif key < node.key:
            node.left = self.__insert(node.left, key, value)
            return node
        elif key > node.key:
            node.right = self.__insert(node.right, key, value)
            return node
        elif key == node.key:
            node.value = value
            return node
        else:
            raise RuntimeError(f'Keys {key} and {node.key} do not compare')

    def insert(self, key, value):
        self.root = self.__insert(self.root, key, value)

    def __remove(self, node, key):
        if node is None:
            raise KeyError(f'Key {key} not in tree')
        elif key < node.key:
            # the Node to remove is in the left subtree
            node.left = self.__remove(node.left, key)
            return node
        elif key > node.key:
            # the Node to remove is in the right subtree
            node.right = self.__remove(node.right, key)
            return node
        elif key == node.key:
            # node must be removed
            if node.left is None and node.right is None:
                # node is replaced by None
                return None
            elif node.left is None:
                # node is replaced by node.right
                return node.right
            elif node.right is None:
                # node is replaced by node.left
                return node.left
            else:
                # pred is the Node below node with the next smaller key, i.e.
                # n.key < pred.key < node.key for all n in the subtree with
                # root node.left
                pred = node.left
                while pred.right is not None:
                    pred = pred.right
                # remove pred from left subtree as it will replace node
                left = self.__remove(node.left, pred.key)
                pred.left = left
                pred.right = node.right
                return pred
        else:
            raise RuntimeError(f'Keys {key} and {node.key} do not compare')

    def remove(self, key):
        self.root = self.__remove(self.root, key)
        self.size -= 1

    def __find(self, node, key):
        if node is None:
            return None
        elif key < node.key:
            return self.__find(node.left, key)
        elif key > node.key:
            return self.__find(node.right, key)
        elif key == node.key:
            return node
        else:
            raise RuntimeError(f'Keys {key} and {node.key} do not compare')

    def find(self, key):
        return self.__find(self.root, key)

    def __depth(self, node):
        if node is None:
            return 0
        else:
            return max(self.__depth(node.left), self.__depth(node.right)) + 1

    def depth(self):
        return self.__depth(self.root)

def treeEqual(t1, t2):
    if t1 is None and t1 is None:
        return True
    elif not t1 is None and not t2 is None:
        return (t1.key == t2.key and
                treeEqual(t1.left, t2.left) and
                treeEqual(t1.right, t2.right))
    else:
        return False

class TreeTests(unittest.TestCase):

    def buildTree1(self):
        """Baut einen Testbaum"""
        #Benutze kein treeInsert, da wir dies explizit testen wollen
        t = SearchTree()
        t.root = Node(0, 3)
        t.root.right = Node(4, 3)
        t.root.right.right = Node(5, 3)
        u = t.root.right.left = Node(2, 3)
        u.left = Node(1, 3)
        u.right = Node(3, 3)
        return t

    def buildTree2(self):
        """Baut einen unbalancierten Testbaum"""
        t = SearchTree()
        t.root = Node(0, 3)
        t.root.right = Node(1, 3)
        t.root.right.right = Node(2, 3)
        t.root.right.right.right = Node(3, 3)
        t.root.right.right.right.right = Node(4, 3)
        return t

    def testInsert(self):
        t = SearchTree()
        t.root = Node(0, 3)
        t.insert(4, 3)
        t.insert(2, 3)
        t.insert(5, 3)
        t.insert(1, 3)
        t.insert(3, 3)
        self.assertEqual(0, t.root.key)
        self.assertEqual(None, t.root.left)
        self.assertEqual(4, t.root.right.key)
        self.assertEqual(2, t.root.right.left.key)
        self.assertEqual(5, t.root.right.right.key)
        self.assertEqual(None, t.root.right.right.right)
        self.assertEqual(None, t.root.right.right.left)
        self.assertEqual(1, t.root.right.left.left.key)
        self.assertEqual(3, t.root.right.left.right.key)
        self.assertEqual(None, t.root.right.left.right.right)
        self.assertEqual(None, t.root.right.left.right.left)
        self.assertEqual(None, t.root.right.left.left.right)
        self.assertEqual(None,t.root.right.left.left.left)
        self.assertTrue(treeEqual(t.root, self.buildTree1().root))

    def testTreeRemove1(self):
        t = self.buildTree1()
        t.remove(5)
        t.remove(4)
        self.assertEqual(0, t.root.key)
        self.assertEqual(2, t.root.right.key)
        self.assertEqual(1, t.root.right.left.key)
        self.assertEqual(3, t.root.right.right.key)
        self.assertRaises(KeyError, t.remove, 10)

    def testTreeHasKey(self):
        t = self.buildTree1()

        for ii in range(6):
            node = t.find(ii)
            self.assertTrue(isinstance(node, Node), "konnte %u nicht im Baum finden" % ii)
            self.assertEqual(node.key, ii, "treeHasKey returnd falsches Node Objekt")

        for ii in range(6, 10):
            self.assertIs(t.find(ii), None, "%u im Baum gefunden obwohl nicht vorhanden" % ii)

        for ii in range(1, 10):
            self.assertIs(t.find(-ii), None, "%u im Baum gefunden obwohl nicht vorhanden" % -ii)

    def testTreeDepth(self):
        t = self.buildTree2()
        self.assertEqual(4, t.depth())
        t = self.buildTree1()
        self.assertEqual(3, t.depth())


if __name__ == "__main__":
    unittest.main()
