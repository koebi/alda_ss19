import unittest, random, copy
import timeit
import ringbuffer

# Variante 1:
# push durch Vergrößern um ein Element
# popFirst durch Verschieben nach vorne
class UniversalContainer1:
    def __init__(self):
        self.capacity_ = 1
        self.data_ = [None]*self.capacity_
        self.size_ = 0

    def size(self):
        return self.size_

    def capacity(self):
        return self.capacity_

    def push(self, item):
        if self.capacity_ == self.size_:
            self.capacity_ += 1 # Kapazität wird um eins vergrößert…
            self.data += [None] # …und in data reflektiert
        self.data_[self.size_] = item
        self.size_ += 1

    def popFirst(self):
        if self.size_ == 0:
            raise RuntimeError("popFirst() on empty container")
        self.size_ -= 1
        for i in range(self.size_):
            self.data_[i] = self.data_[i+1]

    def popLast(self):
        if self.size_ == 0:
            raise RuntimeError("popLast() on empty container")
        self.size_ -= 1

    def __getitem__(self, index): # __getitem__ implementiert v = c[index]
        if index < 0 or index >= self.size_:
            raise RuntimeError("index out of range")
        return self.data_[index]

    def __setitem__(self, index, v): # __setitem__ implementiert c[index] = v
        if index < 0 or index >= self.size_:
            raise RuntimeError("index out of range")
        self.data_[index] = v

    def first(self):
        return self.__getitem__(0)

    def last(self):
        return self.__getitem__(self.size_ - 1)

# Variante 2
# push durch Verdoppeln
# popFirst durch Verschieben nach vorne
class UniversalContainer2:
    def __init__(self):
        self.capacity_ = 1
        self.data_ = [None]*self.capacity_
        self.size_ = 0

    def size(self):
        return self.size_

    def capacity(self):
        return self.capacity_

    def push(self, item):
        if self.capacity_ == self.size_:
            self.capacity_ *= 2 # Kapazität verdoppeln…
            self.data_ += [None]*self.size_ # …und in self.data reflektieren
        self.data_[self.size_] = item
        self.size_ += 1

    def popFirst(self):
        if self.size_ == 0:
            raise RuntimeError("popFirst() on empty container")
        self.size_ -= 1
        for i in range(self.size_):
            self.data_[i] = self.data_[i+1]

    def popLast(self):
        if self.size_ == 0:
            raise RuntimeError("popLast() on empty container")
        self.size_ -= 1

    def __getitem__(self, index):
        if index < 0 or index >= self.size_:
            raise RuntimeError("index out of range")
        return self.data_[index]

    def __setitem__(self, index, v):
        if index < 0 or index >= self.size_:
            raise RuntimeError("index out of range")
        self.data_[index] = v

    def first(self):
        return self.__getitem__(0)

    def last(self):
        return self.__getitem__(self.size_ - 1)

# Variante 3:
# push durch Verdoppeln der Kapazität
# popFirst als ringbuffer
class UniversalContainer3:
    def __init__(self):
        self.capacity_ = 1

        # Idee:
        #  * wenn first_ == last_: container ist leer
        #  * wenn first_ == (last_ + 1) % len(data_): container ist voll
        # Wir brauchen also immer ein Element mehr als Kapazität, damit wir auf
        # dieses zeigen können falls voll ist.
        self.data_ = [None]*(self.capacity_+1)
        self.first_ = self.last_ = 0

    def size(self): # Wir berechnen die Größe aus last_ und first_
        return (self.last_ - self.first_) % len(self.data_)

    def capacity(self):
        return self.capacity_

    def push(self, item): # add item at the end
        if self.capacity_ == self.size():
            self.capacity_ *= 2 # Kapazität verdoppeln…
            new_data = [None]*(self.capacity_ + 1)   # …und im Speicher reflektieren

            # Daten kopieren. Hier kann nicht einfach nur angehängt werden, da
            # ggf. Dinge merkwürdig gespeichert sind und wir sie hier wieder
            # "auf Anfang" setzen wollen.
            for i in range(self.size()):
                new_data[i] = self.data_[(self.first_ + i) % len(self.data_)]
            # Aktualisieren der Grenzen. Wir müssen erst last_ ändern, weil
            # size() sonst einen falschen Wert zurückgibt.
            self.last_ = self.size()
            self.first_ = 0
            self.data_ = new_data
        self.data_[self.last_] = item
        self.last_ = (self.last_ + 1) % len(self.data_)

    def popFirst(self):
        if self.size() == 0:
            raise RuntimeError("popFirst() on empty container")
        self.first_ = (self.first_ + 1) % len(self.data_)

    def popLast(self):
        if self.size() == 0:
            raise RuntimeError("popLast() on empty container")
        self.last_ = (self.last_ - 1) % len(self.data_)

    def __getitem__(self, index):
        if index < 0 or index >= self.size():
            raise RuntimeError("index out of range")
        return self.data_[(index + self.first_) % len(self.data_)]

    def __setitem__(self, index, v):
        if index < 0 or index >= self.size():
            raise RuntimeError("index out of range")
        self.data_[(index + self.first_) % len(self.data_)] = v

    def first(self):
        if self.size() == 0:
            raise RuntimeError("first() on empty container")
        return self.data_[self.first_]

    def last(self):
        if self.size() == 0:
            raise RuntimeError("last() on empty container")
        return self.data_[(self.last_ - 1) % len(self.data_)]

    def __str__(self):
        res = '['
        for i in range(self.size()):
            if i > 0:
                res += ', '
            res += str(self[i])
        res +=']'
        return res


def containersEqual(left, right):
    if left.size() != right.size():
        return False
    for i in range(left.size()):
        if left[i] != right[i]:
            return False
    return True

class TestContainer(unittest.TestCase):
    def checkSimple(self, Type):
        # teste leeren Container
        c = Type()
        assert c.size() == 0
        assert c.size() <= c.capacity()

        # teste push() in leeren Container
        c.push(1)
        assert c.size() == 1
        assert c.size() <= c.capacity()
        assert c.first() == 1
        assert c.last() == 1
        assert c[0] == 1
        assert c[0] == c.first() and c[c.size()-1] == c.last()

        # teste popLast() bei size==1
        c.popLast()
        assert c.size() == 0
        assert c.size() <= c.capacity()

        # teste push() von zwei Elementen, gefolgt von popLst()
        c.push(1)
        c_old = copy.deepcopy(c)
        c.push(2)
        assert c.size() == 2
        assert c.size() <= c.capacity()
        assert c.first() == 1
        assert c.last() == 2
        assert c[0] == 1
        assert c[1] == 2
        assert c[0] == c.first() and c[c.size()-1] == c.last()
        c.popLast()
        assert containersEqual(c, c_old)

        # teste popFirst() bei zwei Elementen
        c.push(2)
        c.popFirst()
        assert c.size() == 1
        assert c.size() <= c.capacity()
        assert c.first() == 2
        assert c.last() == 2
        assert c[0] == 2
        assert c[0] == c.first() and c[c.size()-1] == c.last()
        c.popFirst()
        assert c.size() == 0
        assert c.size() <= c.capacity()

        # teste c[k] = v bei vier Elementen
        c.push(2)
        c.push(3)
        c.push(4)
        c.push(5)
        for k in range(c.size()):
            c_old = copy.deepcopy(c)
            c[k] = k + 6
            for i in range(c.size()):
                if i != k:
                    assert c[i] == c_old[i]
                else:
                    assert c[i] == k + 6
            assert c[0] == c.first() and c[c.size()-1] == c.last()

        # teste popFirst() bei vier Elementen
        c_old = copy.deepcopy(c)
        c.popFirst()
        assert c.size() == 3
        assert c.size() <= c.capacity()
        assert c.first() == 7
        assert c.last() == 9
        for i in range(c.size()):
            assert c[i] == c_old[i+1]
        assert c[0] == c.first() and c[c.size()-1] == c.last()

        # teste popLast() bei drei Elementen
        c_old = copy.deepcopy(c)
        c.popLast()
        assert c.size() == 2
        assert c.size() <= c.capacity()
        assert c.first() == 7
        assert c.last() == 8
        for i in range(c.size()):
            assert c[i] == c_old[i]
        assert c[0] == c.first() and c[c.size()-1] == c.last()

    def testContainer1(self):
        self.checkSimple(UniversalContainer1)

    def testContainer2(self):
        self.checkSimple(UniversalContainer2)

    def testContainer3(self):
        self.checkSimple(UniversalContainer3)

    # Konstruktor und das Verhalten bei leerer UniversalContainer3 werden getestet
    def testConstructor(self):
        q = UniversalContainer3()
        self.assertEqual(q.capacity(), 1)
        self.assertEqual(q.size(), 0)
        self.assertRaises(RuntimeError, q.popFirst)
        self.assertRaises(RuntimeError, q.popLast)

    # push() wird getestet
    def testPush(self):
        for y in range(0,100):
            q = UniversalContainer3()

            for i in range(0, y):
                q.push(i)
                self.assertEqual(q.size(), i+1)
                self.assertTrue(q.size() <= q.capacity())

    # UniversalContainer3 wird n-mal gepushed und mit popLast() (n+1)-mal gepopped.
    # Das letzte popLast() muss eine Exception ausloesen (leere UniversalContainer3).
    def testPopLast(self):
        for y in range(0,100):
            q = UniversalContainer3()
            for i in range(0, y):
                q.push(i)

            for i in range(y, 0, -1):
                self.assertEqual(q.size(), i)
                self.assertEqual(q.last(), i-1)
                q.popLast()

            self.assertEqual(q.size(), 0)
            self.assertRaises(RuntimeError, q.popLast)

    # UniversalContainer3 wird n-mal gepushed und mit popFirst() (n+1)-mal gepopped.
    # Das letzte popFirst() muss eine Exception ausloesen (leere UniversalContainer3).
    def testPopFirst(self):
        for y in range(0,100):
            q = UniversalContainer3()
            for i in range(0, y):
                q.push(i)

            for i in range(y, 0, -1):
                self.assertEqual(q.size(), i)
                self.assertEqual(q.first(), y-i)
                q.popFirst()

            self.assertEqual(q.size(), 0)
            self.assertRaises(RuntimeError, q.popFirst)

    # push(), popFirst() und popLast() werden in zufaelliger Kombination
    # getestet. Dies wird 10-mal wiederholt.
    # (Wir fuellen die UniversalContainer3 am Anfang mit 115 Elementen, so dass ein
    #  Fehler wegen leerer UniversalContainer3 praktisch ausgeschlossen ist.)
    def testRand(self):
        for k in range(10):
            q = UniversalContainer3()
            sizeCount = 115
            for i in range(sizeCount):
                q.push(i)
            self.assertEqual(q.size(), sizeCount)

            for i in range(400):
                dec = random.randint(0,3)
                if dec <= 1:
                    q.push(None)
                    sizeCount += 1
                elif dec == 2:
                    q.popFirst()
                    sizeCount -= 1
                elif dec == 3:
                    q.popLast()
                    sizeCount -= 1
                self.assertEqual(q.size(), sizeCount)

    # Teste, ob die Implementation des Rings korrekt ist.
    def testShiftRight(self):
        q = UniversalContainer3()

        # 10 Elemente einfuegen
        for i in range(0,10):
            q.push(i)
        self.assertEqual(q.capacity(), 16)
        self.assertEqual(q.size(), 10)
        self.assertEqual(q.first_, 0)
        self.assertEqual(q.last_, 10)

        # die ersten 6 Elemente entfernen
        for i in range(0,6):
            q.popFirst()
        self.assertEqual(q.size(), 4)
        self.assertLess(q.first_, q.last_)

        # weitere 10 Elemente einfuegen => last_
        # ueberschreitet die Arraygrenze und ist jetzt
        # kleiner als first_
        for i in range(0,10):
            q.push(i)
        self.assertEqual(q.capacity(), 16)
        self.assertEqual(q.size(), 14)
        self.assertGreater(q.first_, q.last_)

        # 6 Elemente am Ende entfernen => last_
        # ueberschreitet die Arraygrenze in der anderen
        # Richtung und ist wieder groesser als first_
        for i in range(0,6):
            q.popLast()
        self.assertEqual(q.capacity(), 16)
        self.assertEqual(q.size(), 8)
        self.assertLess(q.first_, q.last_)

        # die uebrigen Elemente am Ende entfernen =>
        # UniversalContainer3 muss jetzt leer sein
        for i in range(0,8):
            q.popLast()
        self.assertEqual(q.capacity(), 16)
        self.assertEqual(q.size(), 0)
        self.assertEqual(q.first_, q.last_)

        # weiteres Entfernen muss Exception ausloesen
        self.assertRaises(RuntimeError, q.popFirst)
        self.assertRaises(RuntimeError, q.popLast)

        # 14 neue Elemente einfuegen => last_
        # ueberschreitet die Arraygrenze erneut und
        # ist kleiner als first_
        for i in range(0,14):
            q.push(i)
        self.assertEqual(q.capacity(), 16)
        self.assertEqual(q.size(), 14)
        self.assertGreater(q.first_, q.last_)

        # 11 Elemente am Anfang entfernen => first_
        # ueberschreitet die Arraygrenze ebenfalls und
        # ist nun wieder kleiner als last_
        for i in range(0,11):
            q.popFirst()
        self.assertEqual(q.capacity(), 16)
        self.assertEqual(q.size(), 3)
        self.assertLess(q.first_, q.last_)

        # die uebrigen Elemente am Anfang entfernen =>
        # UniversalContainer3 muss jetzt leer sein
        for i in range(0,3):
            q.popFirst()
        self.assertEqual(q.capacity(), 16)
        self.assertEqual(q.size(), 0)
        self.assertEqual(q.first_, q.last_)

        # weiteres Entfernen muss Exception ausloesen
        self.assertRaises(RuntimeError, q.popFirst)
        self.assertRaises(RuntimeError, q.popLast)

        # 20 neue Elemente einfuegen => das interne Array wird
        # verdoppelt, first_ und last_ daher zurueckgesetzt
        for i in range(0,20):
            q.push(i)
        self.assertEqual(q.capacity(), 32)
        self.assertEqual(q.size(), 20)
        self.assertEqual(q.first_, 0)
        self.assertEqual(q.last_, 20)

def examples():
    test = UniversalContainer3()
    test.push(1)
    test.push(2)
    test.push(3)
    print("before:", test, "first:", test.first())
    test.popFirst()
    print(" after popFirst():", test)
    test.push(4)
    print(" after push(4):", test, "first:", test.first())
    test.popFirst()
    print(" after popFirst():", test)
    test.push(5)
    print(" after push(5):", test, "first:", test.first())
    test.popFirst()
    print(" after popFirst():", test)
    test.push(6)
    print(" after push(6):", test, "last:", test.last())
    test.popLast()
    print(" after popLast():", test, "last:", test.last())
    test.popLast()
    try:
        print(" after popLast():", test, "last:", test.last())
    except:
        print("UniversalContainer3 empty!")

def timingPush():
    push = '''
for i in range(N):
    c.push(i)
'''
    pop = '''
for i in range(N):
    c.popFirst()
'''
    repeats = 5
    scope = globals()
    for m in range(1,4):
        variant = "ringbuffer.UniversalContainer%d" % m
        print(variant, "push")
        for k in range(5,11):
            N = 2**k
            scope['N'] = N
            t = timeit.Timer(push, "c = %s()" % variant , globals=scope)
            time = min(t.repeat(repeats, 1))
            print("N = %4d" % N, "total: %f ms," % (time*1000), "amortized: %f us" % (time/N*1e6))
    for m in range(1,4):
        variant = "ringbuffer.UniversalContainer%d" % m
        print(variant, "popFirst")
        for k in range(5,11):
            N = 2**k
            scope['N'] = N
            t = timeit.Timer(pop, ("c = %s()\n" % variant) + push, globals=scope)
            time = min(t.repeat(repeats, 1))
            print("N = %4d" % N, "total: %f ms," % (time*1000), "amortized: %f us" % (time/N*1e6))

if __name__ == "__main__":
    print("Running UniversalContainer3 examples:")
    examples()

    print("\nTiming\n------")
    timingPush()

    print("\nRunning tests\n-------------")
    unittest.main()
