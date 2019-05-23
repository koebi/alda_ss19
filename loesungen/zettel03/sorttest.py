import unittest
from random import randint
import copy

class Student:
    def __init__(self, name, mark):
        '''Construct new Student object with given 'name' and 'mark'.'''
        self.name = name
        self.mark = mark

    def getName(self):
        '''Access the name.'''
        return self.name

    def getMark(self):
        '''Access the mark.'''
        return self.mark

    def __repr__(self):
        '''Convert Student object to a string.'''
        return "%s: %3.1f" % (self.name, self.mark)

    def __eq__(self, other):
        '''Check if two Student objects are equal.'''
        # Wird für die Nutzung von assertCountEqual gebraucht
        if isinstance(other, Student):
            return self.name == other.name and self.mark == other.mark
        return False

##################################################################

def insertionSort(a, key=lambda x: x):
    '''
    Sort the array 'a' in-place.

    Parameter 'key' must hold a function that, given a complicated
    object, extracts the property to be sorted by. By default, this
    is the object itself (useful to sort integers). To sort Students
    by name, for example, you would call:
        insertionSort(students, key=Student.getName)
    whereas to sort by mark, you use
        insertionSort(students, key=Student.getMark)
    This corresponds to the behavior of Python's built-in sorting functions.
    '''
    for i in range(1, len(a)):
        current = a[i]
        j = i
        while j > 0:
            # Mit <= ist insertionSort stabil, da gleiche Elemente in der
            # Reihenfolge bleiben, in der sie sind.
            if key(a[j-1]) <= key(current):
                break
            else:
                a[j] = a[j-1]
            j -= 1
        a[j] = current

##################################################################

def mergeSort(a, key=lambda x: x):
    N = len(a)
    if N <= 1:
        return a

    # Key muss hier mit-iteriert werden
    left  = mergeSort(a[:N//2], key)
    right = mergeSort(a[N//2:], key)

    res = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    return res + left[i:] + right[j:]

##################################################################

class TestSortingFunctions(unittest.TestCase):

    def setUp(self):
        '''Testdaten erstellen.'''

        # Integer-Arrays
        self.int_arrays = [
            [],           # leeres Array
            [1],          # ein Element
            [2,1],        # zwei Elemente
            [3,2,3,1],    # Array vom Blatt
            [randint(0, 4) for k in range(10)], # 10 zufällige Zahlen, viel Dopplung
            [randint(0, 1000) for k in range(100)]  # 100 zufällige Zahlen, wenig Dopplung
        ]

        # Studi-Arrays
        self.student_arrays = [
           [Student('Adam', 1.3),
            Student('Bert', 2.0),
            Student('Elsa', 1.0),
            Student('Greg', 1.7),
            Student('Jill', 2.7),
            Student('Judy', 3.0),
            Student('Mike', 2.3)
            Student('Patt', 5.0)], # keine doppelten Noten

           [Student('Adam', 1.3),
            Student('Bert', 2.0),
            Student('Elsa', 1.3),
            Student('Greg', 1.0),
            Student('Jill', 1.7),
            Student('Judy', 1.0),
            Student('Mike', 2.3),
            Student('Patt', 1.3)], # doppelte Noten, alphabetisch

           [Student('Bert', 2.0),
            Student('Mike', 2.3),
            Student('Elsa', 1.3),
            Student('Judy', 1.0),
            Student('Patt', 2.0),
            Student('Greg', 1.0),
            Student('Jill', 1.7),
            Student('Adam', 1.3)] # doppelte Noten, irgendwie
        ]

    def testBuiltinSort(self):
        # Integer-Arrays testen
        for a in self.int_arrays:
            original = copy.deepcopy(a)
            # ACHTUNG: in-place!!
            a.sort()
            self.checkIntegerSorting(original, a)

        # Studi-Arrays testen
        for a in self.student_arrays:
            original = copy.deepcopy(a)
            a.sort(key=Student.getMark) # nach Note sortieren
            self.checkStudentSorting(original, a)

    def testInsertionSort(self):
        # Integer-Arrays testen
        for a in self.int_arrays:
            original = copy.deepcopy(a)
            insertionSort(a)
            self.checkIntegerSorting(original, a)

        # Studi-Arrays testen
        for a in self.student_arrays:
            original = copy.deepcopy(a)
            insertionSort(a, key=Student.getMark)
            self.checkStudentSorting(original, a)

    def testMergeSort(self):
        # Integer-Arrays testen
        for original in self.int_arrays:
            a = mergeSort(original)
            self.checkIntegerSorting(original, a)

        # Studi-Arrays testen
        for original in self.student_arrays:
            a = mergeSort(original, key=Student.getMark)
            self.checkStudentSorting(original, a)

    def checkIntegerSorting(self, original, result):
        '''Parameter 'original' contains the array before sorting,
        parameter 'result' contains the result of the sorting algorithm.'''
        # Testet gleiche Anzahl für alle Elemente
        self.assertCountEqual(original, result)

        # Alternativ:

        # self.assertEqual(len(original), len(result))
        # kopie = copy.deepcopy(result)
        # for x in original:
        #     result.remove(x)
        # self.assertEqual(len(kopie), 0) # In kopie könnten noch Elemente stehen.

        # Werte sollten sortiert sein
        for k in range(len(result)-1):
            self.assertLessEqual(result[k], result[k+1])

    def checkStudentSorting(self, original, result):
        '''Parameter 'original' contains the array before sorting,
        parameter 'result' contains the result of the sorting algorithm.'''
        self.assertCountEqual(original, result)

        # Array sollte sortiert sein
        for k in range(len(result)-1):
            self.assertLessEqual(result[k].getMark(), result[k+1].getMark())
            # Falls sich aufeinanderfolgende Noten gleichen, Stabilität prüfen
            if result[k].getMark() == result[k+1].getMark():
                self.assertLess(original.index(result[k]), original.index(result[k+1]))

##################################################################

if __name__ == '__main__':
    unittest.main()
