from copy import deepcopy
import unittest, random, math

class Node:
    def __init__(self, key, value, priority = 1):
        self.key = key
        self.value = value
        self.priority = priority
        self.left = self.right = None

    def __repr__(self):
        return f'({self.key}: {self.value})'


class SearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def __insert(self, node, key, value, is_dynamic_treap):

        if node is None:
            self.size += 1 # key not yet in tree, hence size is increased
            if is_dynamic_treap:          # dynamic Treap modus
                return Node(key, value)
            else:                         # random Treap modus
                return Node(key, value, random.randint(0, 4294967295))
        elif key < node.key:
            node.left = self.__insert(node.left, key, value, is_dynamic_treap)
            # Da der rekursive Aufruf von __insert() dafuer sorgt, dass
            # im linken Teilbaum die Treapbedingung bereits erfuellt ist,
            # muss man jetzt nur noch schauen ob die Priority des
            # linken Kindes groesser als die der Wurzel ist und entsprechend rotieren
            if node.left.priority > node.priority:
                node = self.rotateRight(node)

            return node
        elif key > node.key:
            node.right = self.__insert(node.right, key, value, is_dynamic_treap)

            if node.right.priority > node.priority:
                node = self.rotateLeft(node)

            return node
        elif key == node.key:             # Schluessel wurde gefunden
            node.value = value
            if is_dynamic_treap:          # dynamic Treap modus
                node.priority += 1    # => Prioritaet inkrementieren
            return node
        else:
            raise RuntimeError(f'Keys {key} and {node.key} do not compare')

    def treapInsert(self, key, value, is_dynamic_treap):
        self.root = self.__insert(self.root, key, value, is_dynamic_treap)

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

    def rotateLeft(self,rootnode):
        if rootnode.right is None:
            raise RuntimeError('Root does not have right child')
        newroot = rootnode.right
        rootnode.right = newroot.left
        newroot.left = rootnode
        return newroot

    def rotateRight(self,rootnode):
        if rootnode.left is None:
            raise RuntimeError('Root does not have left child')
        newroot = rootnode.left
        rootnode.left = newroot.right
        newroot.right = rootnode
        return newroot

class RandomTreap(SearchTree):
    def insert(self, key, value):
        self.treapInsert(key, value, False)


class DynamicTreap(SearchTree):
   def insert(self, key, value):
        self.treapInsert(key, value, True)




def treeEqual(t1, t2):
    """
    Hilfsfunktion für die Unittests
    """
    if t1 is None and t1 is None:
        return True
    elif not t1 is None and not t2 is None:
        return t1.key == t2.key and treeEqual(t1.left, t2.left) and treeEqual(t1.right, t2.right)
    else:
        return False


class TestTreap(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)
        self.keyValue = 7              # Im Test soll key == value/keyValue sein

    def testRotateRight(self):
        t = DynamicTreap()
        t.insert(5,'Q')
        t.insert(2,'P')
        t.insert(6,'C')
        t.insert(1,'A')
        t.insert(3,'B')

        root = t.rotateRight(t.root)
        self.assertEqual(root.value, 'P')
        self.assertEqual(root.left.value, 'A')
        self.assertEqual(root.right.value,'Q')
        self.assertEqual(root.right.right.value, 'C')
        self.assertEqual(root.right.left.value, 'B')

        self.assertEqual(root.left.left , None)
        self.assertEqual(root.left.right , None)
        self.assertEqual(root.right.left.right , None)
        self.assertEqual(root.right.left.left , None)
        self.assertEqual(root.right.right.right , None)
        self.assertEqual(root.right.right.left , None)

    def testRotateLeft(self):
        t = DynamicTreap()
        t.insert(5,'P')
        t.insert(4,'A')
        t.insert(7,'Q')
        t.insert(6,'B')
        t.insert(8,'C')

        root = t.rotateLeft(t.root)
        self.assertEqual(root.value, 'Q')
        self.assertEqual(root.left.value, 'P')
        self.assertEqual(root.right.value,'C')
        self.assertEqual(root.left.right.value, 'B')
        self.assertEqual(root.left.left.value, 'A')

        self.assertEqual(root.right.left ,None)
        self.assertEqual(root.right.right, None)
        self.assertEqual(root.left.left.right, None)
        self.assertEqual(root.left.left.left, None)
        self.assertEqual(root.left.right.right, None)
        self.assertEqual(root.left.right.left, None)

    def testRaiseRotateLeft(self):
        #Falls Root kein rechtes Kind hat kann nicht rotiert werden.
        t = DynamicTreap()
        t.insert(5,'P')
        t.insert(3,'S')
        self.assertRaises(RuntimeError, t.rotateLeft, t.root)

    def testRaiseRotateRight(self):
        #Falls Root kein linkes Kind hat kann nicht rotiert werden.
        t = DynamicTreap()
        t.insert(5,'P')
        t.insert(6,'S')
        self.assertRaises(RuntimeError, t.rotateRight, t.root)

    def testRandomTreapInsert(self):
        #Die Idee: Es reicht jeden Knoten auf Priority und
        #Sortierung zu überprüfen. Fülle einen Stack mit der Wurzel.
        #Jedes mal wenn eine pop() operation durchgeführt wird füge die
        #Kinder in den Stack. und überprüfe die Bedingungen an dem
        #gerade entfernten Knoten.
        t = RandomTreap()
        t.insert(10,10*self.keyValue)
        #teste Treapbedingungen:
        for i in range(1000):
            p = random.randint(0,10000)
            root = t.insert(p,p*self.keyValue)
        a = []
        a.append(t.root)

        while(len(a) > 0):
            cursor = a.pop()
            if cursor.right is not None:
                self.assertTrue(cursor.right.key > cursor.key)
                self.assertTrue(cursor.right.priority <= cursor.priority)
                a.append(cursor.right)
            if cursor.left is not None:
                self.assertTrue(cursor.left.key < cursor.key)
                self.assertTrue(cursor.left.priority <= cursor.priority)
                a.append(cursor.left)

    def testDynamicTreapInsert(self):
        t = DynamicTreap()
        t.insert(10,10*self.keyValue)
        #teste Treapbedingungen:
        for i in range(1000):
            p = random.randint(0,10000)
            root = t.insert(p,p*self.keyValue)
        a = []
        a.append(t.root)

        while(len(a) > 0):
            cursor = a.pop()
            if cursor.right is not None:
                self.assertTrue(cursor.right.key > cursor.key)
                self.assertTrue(cursor.right.priority <= cursor.priority)
                a.append(cursor.right)
            if cursor.left is not None:
                self.assertTrue(cursor.left.key < cursor.key)
                self.assertTrue(cursor.left.priority <= cursor.priority)
                a.append(cursor.left)

    def testDynamicTreapPriority(self):
        t = DynamicTreap()
        t.insert(10,10*self.keyValue)
        t.insert(3,3*self.keyValue)
        t.insert(15,15*self.keyValue)

        self.assertEqual(t.root.right.key, 15)
        self.assertEqual(t.root.right.priority, 1)

        t.insert(15,15*self.keyValue)
        self.assertEqual(t.root.key, 15)
        self.assertEqual(t.root.priority, 2)


from operator import itemgetter

if __name__ == '__main__':
   # unittest.main(exit=False)

    # Teilaufgabe c)
    def readText(filename):
        s = open(filename, encoding='latin_1').read()
        for k in ',;.:-"\'!?':
            s = s.replace(k, '')       # Sonderzeichen entfernen
        s = s.lower()                  # alles klein schreiben
        return s.split()               # string in array von Woertern umwandeln

    def treeSort(node,array):
        if node is None:
            return
        treeSort(node.left, array)
        array.append(node.key)
        treeSort(node.right, array)

    def compareTreaps(treap1, treap2):
        array1, array2 = list(), list()
        treeSort(treap1, array1)
        treeSort(treap2, array2)

        if array1 == array2:
            return True
        return False

    randomTreap = None
    dynamicTreap = None

    print ("insert from 'die-drei-musketiere.txt':")
    musketiere = readText('die-drei-musketiere.txt')

    rt = RandomTreap()
    dt = DynamicTreap()
    for word in musketiere:
        rt.insert(word,' ') # value = ' ' weil nocht benoetigt
        dt.insert(word,' ')

    totalWordCount = len(musketiere)
    uniqueWordCount = dt.size

    print ("total number of words:", totalWordCount, "(unique:", uniqueWordCount, ")")

    if compareTreaps(rt.root, dt.root):
        print ("sorting of both treaps is equal")
    else:
        print ("Huston, we've got a problem")

    # Teilaufgabe d)

    def treeDepths(node, array, depth=0):
        if node is None:
            return
        treeDepths(node.left, array, depth+1)
        array.append(depth)
        treeDepths(node.right, array, depth+1)

    def treePriorities(node, array):
        if node is None:
            return
        treePriorities(node.left, array)
        array.append(node.priority)
        treePriorities(node.right, array)

    randomDepth = []
    dynamicDepth = []
    treeDepths(rt.root, randomDepth)
    treeDepths(dt.root, dynamicDepth)

    print ("\nmaximum depth:\n---------------")
    print ("random treap", max(randomDepth))
    print ("dynamic treap", max(dynamicDepth))
    print ("perfectly balanced tree", int(math.ceil(math.log(uniqueWordCount) / math.log(2.0))))


    priorities = []
    treePriorities(dt.root, priorities)

    randomAccessSum = 0.0
    dynamicAccessSum = 0.0

    for k in range(uniqueWordCount):
        randomAccessSum += priorities[k] * randomDepth[k]
        dynamicAccessSum += priorities[k] * dynamicDepth[k]

    print ("\nmean access times:\n-----------------")
    print ("random treap", (randomAccessSum / totalWordCount))
    print ("dynamic treap", (dynamicAccessSum / totalWordCount))

    # Teilaufgabe e)

    print ("\nfrequent words:\n------------")
    def treapTop(treap, my_priority):
        result = []
        treapTopImpl(treap, my_priority, result)
        return sorted(result, key=itemgetter(1), reverse=True)

    def treapTopImpl(treap, my_priority, result):
        if treap is None or treap.priority < my_priority:
            return
        result.append((treap.key, treap.priority))
        treapTopImpl(treap.left, my_priority, result)
        treapTopImpl(treap.right, my_priority, result)

    frequentWords = treapTop(dt.root, 200)
    print ("frequent words including stopwords")
    for k in frequentWords:
        print ("(%s, %d)" % k, end=' ')
    print()

    # store stop words in a set() so that 'if word not in stopWords:'
    # can be executed efficiently in the loop below

    stopWords = set(open('stopwords.txt', encoding='latin_1').read().split())

    cleanedTreap = DynamicTreap()
    for word in musketiere:
        if word not in stopWords:
            cleanedTreap.insert(word, ' ')

    frequentWordsCleaned = treapTop(cleanedTreap.root, 100)
    print ("frequent words excluding stopwords")
    for k in frequentWordsCleaned:
        print ("(%s, %d)" % k, end=' ')
    print()


