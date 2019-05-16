import copy

class UniversalContainer:
    def __init__(self): # constructor for empty container
        self.capacity_ = 1 # we reserve memory for at least one item
        self.data_ = [None]*self.capacity_ # the internal memory
        self.size_ = 0 # no item has been inserted yet

    def size(self):
        return self.size_

    def capacity(self):
        return self.capacity_

    def push(self, item): # add item at the end
        if self.capacity_ == self.size_: # internal memory is full
            self.capacity_ *= 2
            self.data_ += [None]*self.size_
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

    def __getitem__(self, index): # __getitem__ implements v = c[index]
        if index < 0 or index >= self.size_:
            raise RuntimeError("index out of range")
        return self.data_[index]

    def __setitem__(self, index, v): # __setitem__ implements c[index] = v
        if index < 0 or index >= self.size_:
            raise RuntimeError("index out of range")
        self.data_[index] = v

    def first(self):
        #alternativ auch mit self.data_[0]
        return self.__getitem__(0)

    def last(self):
        #alternativ auch mit self.data_[self.size_ -1]
        return self.__getitem__(self.size_ - 1)

def containersEqual(left, right):
    if left.size() != right.size():
        return False
    for i in range(left.size()):
        if left[i] != right[i]:
            return False
    return True

#TODO: Sinnvolle Kommentare
def testContainer():
    # Axiom 1
    c = UniversalContainer()
    assert c.size() == 0
    assert c.size() <= c.capacity()

    # Axiom 3
    c.push(1)
    assert c.size() <= c.capacity() # Axiom 2
    assert c[0] == c.first() and c[c.size()-1] == c.last() # Axiom 7

    assert c.size() == 1 # (i)
    assert c.last() == 1 # (ii)
    assert c.first() == 1 # (iv)
    c.popLast() # (v)  (Container vorher leer)
    assert c.size() <= c.capacity() # Axiom 2
    assert c.size() == 0 # (v)

    # Axiom 3 (v)
    c.push(1)
    c_old = copy.deepcopy(c)
    c.push(2)
    assert c[0] == 1 # (iii)
    c.popLast()
    assert containersEqual(c, c_old)

    # Axiom 6
    c.push(2)
    c.popFirst()
    assert c.size() == 1 # (i)
    assert c.first() == 2 # (ii)

    assert c[0] == c.first() and c[c.size()-1] == c.last() # Axiom 7
    assert c.size() <= c.capacity()

    # Leerer Container für folgende Tests
    c.popFirst()
    assert c.size() == 0

    # Bisschen Inhalt für folgende Tests
    c.push(2)
    c.push(3)
    c.push(4)
    c.push(5)
    assert c.size() == 4

    # Axiom 4
    for k in range(c.size()):
        c_old = copy.deepcopy(c)
        c[k] = k + 6
        assert c.size() == c_old.size() # (i)
        for i in range(c.size()):
            if i != k:
                assert c[i] == c_old[i] # (iii)
            else:
                assert c[i] == k + 6 # (ii)

    assert c.size() <= c.capacity() # Axiom 2

    # Axiom 6
    c_old = copy.deepcopy(c)
    c.popFirst()
    assert c.size() == 3 # (i)
    for i in range(c.size()): # (ii)
        assert c[i] == c_old[i+1]


    # Axiom 5
    c_old = copy.deepcopy(c)
    c.popLast()
    assert c.size() == 2 # (i)
    for i in range(c.size()): # (ii)
        assert c[i] == c_old[i]

    # Axiom 7
    assert c[0] == c.first() and c[c.size()-1] == c.last()

    print("All tests succeeded")

# make universal-container.py executable
if __name__ == "__main__":
    testContainer()
