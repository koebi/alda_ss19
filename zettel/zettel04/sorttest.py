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
        return self.name == other.name and self.mark == other.mark

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
            if key(a[j-1]) < key(current):
                break
            else:
                a[j] = a[j-1]
            j -= 1
        a[j] = current

##################################################################

class TestSortingFunctions(unittest.TestCase):

    def setUp(self):
        '''Create test data.'''

        # integer arrays
        self.int_arrays = [
            [],           # empty array
            [1],          # one element
            [2,1],        # two elements
            [3,2,3,1],    # the array from the exercise text
            [randint(0, 4) for k in range(10)], # 10 random ints
            [randint(0, 4) for k in range(10)]  # another 10 random ints
        ]

        # Student arrays
        self.student_arrays = [
           [Student('Adam', 1.3),
            Student('Bert', 2.0),
            Student('Elsa', 1.0),
            Student('Greg', 1.7),
            Student('Jill', 2.7),
            Student('Judy', 3.0),
            Student('Mike', 2.3),
            Student('Patt', 5.0)], # without replicated marks

           [Student('Adam', 1.3),
            Student('Bert', 2.0),
            Student('Elsa', 1.3),
            Student('Greg', 1.0),
            Student('Jill', 1.7),
            Student('Judy', 1.0),
            Student('Mike', 2.3),
            Student('Patt', 1.3)], # with replicated marks, alphabetic

           [Student('Bert', 2.0),
            Student('Mike', 2.3),
            Student('Elsa', 1.3),
            Student('Judy', 1.0),
            Student('Patt', 2.0),
            Student('Greg', 1.0),
            Student('Jill', 1.7),
            Student('Adam', 1.3)] # with replicated marks, random order
        ]

    def testBuiltinSort(self):
        # test the integer arrays
        for a in self.int_arrays:
            ... # your code here (test that array is sorted)

        # test the Student arrays
        for a in self.student_arrays:
            ... # your code here (test that array is sorted and stable)

    def testInsertionSort(self):
        # test the integer arrays
        for a in self.int_arrays:
            ... # your code here (test that array is sorted)

        # test the Student arrays
        for a in self.student_arrays:
            ... # your code here (test that array is sorted and stable)

    def checkIntegerSorting(self, original, result):
        '''Parameter 'original' contains the array before sorting,
        parameter 'result' contains the result of the sorting algorithm.'''
        ... # your code here

    def checkStudentSorting(self, original, result):
        '''Parameter 'original' contains the array before sorting,
        parameter 'result' contains the result of the sorting algorithm.'''
        ... # your code here

##################################################################

if __name__ == '__main__':
    unittest.main()
