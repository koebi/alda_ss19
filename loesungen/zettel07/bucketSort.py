import random
import math
import unittest
from copy import deepcopy

def createData(N):
    a = []
    while len(a) < N:
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        r = math.sqrt(x**2 + y**2)
        if r < 1.0:
            a.append(r)
    return a

def naiveBucketMap(r, M):
    return int(r*M)

def bucketMap(r, M):
    return int(r**2 * M)

def chi2Test(bucket_lens, N):
    M = len(bucket_lens)
    mean = float(N) / M
    c2 = 0.0
    for k in bucket_lens:
        c2 += (k - mean)**2 / mean
    p = math.sqrt(2.0*c2) - math.sqrt(2.0*M-3.0)
    return (p <= 3)

def insertionSort(b):
    N = len(b)
    for k in range(1, N):
        v = b[k]
        j = k
        while j > 0 and b[j-1] > v:
            b[j] = b[j-1]
            j -= 1
        b[j] = v

def bucketSort(a, bmap, c = 3.0):
    N = len(a)
    M = int(math.floor(N / 4)) + 1
    buckets = [[] for k in range(M)]
    buckets = [[]]*M

    for k in a:
        buckets[bmap(k, M)].append(k)

    i = 0
    for k in buckets:
        insertionSort(k)
        a[i:i+len(k)] = k
        i += len(k)

    return buckets

class TestBucketSort(unittest.TestCase):

    def setUp(self):
        # kleine arrays
        self.testArrays = [
            [],           # leeres array
            [0.1],        # ein element
            [0.91,0.13],  # zwei elemente
            [0.74,0.77,0.23,0.22,0.28,0.04,0,0.35] # mehrere elemente im gleichen bucket
        ]

    def testBucketSort(self):
        # kleine Arrays
        for a in self.testArrays:
            original = deepcopy(a)
            a.sort()
            bucketSort(original,bucketMap)
            self.assertEqual(original, a)

        # zufällige arrays
        for n in range(100,1000,50):
            a = createData(n)
            original = deepcopy(a)
            a.sort()
            bucketSort(original,bucketMap)
            self.assertEqual(original, a)


if __name__ == '__main__':
    unittest.main(exit=False)

    for n in range(100,1000,50):
        a = createData(n)
        bucketsNaive = bucketSort(a,naiveBucketMap)
        bucketsKorrekt = bucketSort(a,bucketMap)
        print ('n = '+ str(n) + \
        '\t naive Formel: ' + str(chi2Test([len(k) for k in bucketsNaive], n)) + \
        '\t korrekte Formel: ' + str(chi2Test([len(k) for k in bucketsKorrekt], n)))

    import timeit
    import matplotlib.pyplot as plt

    t = []
    t_naive = []
    size = []
    for n in range(1000,10001,1000):
        timer_1 = timeit.Timer(stmt= 'bucketSort(a,bucketMap)',
                                setup = 'from __main__ import insertionSort,'+
                                'bucketSort, bucketMap, createData \n' +
                                'a = createData('+ str(n) + ')\n')
        timer_2 = timeit.Timer(stmt= 'bucketSort(a,naiveBucketMap)',
                                setup = 'from __main__ import insertionSort,'+
                                'bucketSort, naiveBucketMap, createData \n' +
                                'a = createData('+ str(n) + ')\n')
        time_1 = timer_1.repeat(repeat = 10, number = 1)
        time_2 = timer_2.repeat(repeat = 10, number = 1)
        t.append(min(time_1))
        t_naive.append(min(time_2))
        size.append(n)

    plt.xlabel('Anzahl der Elemente')
    plt.ylabel('Laufzeit [s]')
    plt.title('Laufzeit bucketSort')
    plt.axis([0,10100,0,0.008])
    plt.plot(size,t,'ro', label='bucketMap')
    plt.plot(size,t_naive,'b*', label='naiveBucketMap')
    plt.legend(loc='upper left')
    plt.show()
