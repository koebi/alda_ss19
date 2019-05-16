import copy
from timeit import Timer
import random

def insertionSort(a):
    count = 0

    for i in range(len(a)):
        current = a[i] # aktuelles Element merken
        # Position für aktuelles Element finden
        j = i
        while j > 0:
            count+=1
            if current < a[j-1]: # a[j-1] sollte rechts des aktuellen Elements sein
                a[j] = a[j-1]    # a[j-1] nach rechts bewegen
            else:
                break            # Lücke an korrekter Position
            j -= 1               # Lücke nach links bewegen
        a[j] = current           # aktuelles Element in Lücke stecken

    return a, count


def merge(left, right):
    count = 0

    # Ergebnisliste anlegen
    result = []

    # Solange beide Inputs nicht leer
    while len(left) > 0 and len(right) > 0:
        # kleineres erstes Element an Ergebnis anhängen und aus Input entfernen
        if left[0] > right [0]:
            result.append(right.pop(0))
        else:
            result.append(left.pop(0))
        count += 1

    # potentielle übrige Listen anhängen
    result.extend(right)
    result.extend(left)
    return result, count


def mergeSort(a):
    count = 0

    # Falls nur ein Element: Rückgabe
    if len(a) <= 1:
        return a, 0
    else:
        # Liste teilen
        left = a[:len(a) // 2]
        right = a[len(a) // 2:]

        # rekursiver Aufruf
        left, leftCount = mergeSort(left)
        right, rightCount = mergeSort(right)
        count += leftCount + rightCount

    result, mergeCount = merge(left, right)

    return result, count + mergeCount

def quickSort(a):
    count = 0

    # falls nichts zu sortieren ist, immer noch Rückgabe
    if not a:
        return [], 1

    # Partitionierung mit erstem Element als pivot
    left = [x for x in a if x < a[0]]
    same = [x for x in a if x == a[0]]
    right = [x for x in a if x > a[0]]

    # Für jedes Element jedes Arrays war ein Vergleich notwendig
    count += len(left) + len(right) + len(same)

    left, countleft = quickSort(left)
    right, countright = quickSort(right)

    return left + same + right, count + countleft + countright

def checkSorting(arrayBefore, arrayAfter):
    # Axiom 1: Gleiche Länge
    if len(arrayBefore) != len(arrayAfter):
        return False

    # Kopie des Originals
    kopie = copy.deepcopy(arrayBefore)
    # Enthalten die Arrays die gleichen elemente, sollte es möglich sein, aus
    # der Kopie alle Elemente des "sortierten" Arrays zu löschen und das danach
    # leer zu haben
    for x in arrayAfter:
        try:
            kopie.remove(x)
        except:
            return False

    if len(kopie) != 0:
        return False

    # Sortierung prüfen
    # Ist die Liste zu kurz (also hat 0 oder Element) wird range(0) oder
    # range(-1) ausgeführt, was keinen Effekt hat :)
    for i in range(len(arrayAfter) - 1):
        if arrayAfter[i] > arrayAfter[i + 1]:
            return False

    # Falls alles gut, True zurückgeben
    return True

#*****************************************************************************#
#         Algorithmen anwenden und Daten für die Plots sammeln                #
#*****************************************************************************#
if __name__ == "__main__":
    # Arraylängen zwischen 2 und 500
    for i in range(2, 500):
        # Zufällige Listen anlegen
        a = list(range(i))
        random.shuffle(a)
        b = copy.deepcopy(a)
        c = copy.deepcopy(a)

        # Ausgabe aufs Terminal, mittels "> result.txt" in Datei schreiben,
        # danach Datei beim Übergang von 499 zu 2 in erster Spalte teilen.
        print(str(i) + "," + \
                str(insertionSort(a)[1]) + "," + \
                str(mergeSort(b)[1]) + "," + \
                str(quickSort(c)[1]))

    # Auch für timing Arraylängen zwischen 2 und 500
    for i in range(2, 500):
        # Zufällige Listen anlegen
        a = list(range(i))
        random.shuffle(a)
        b = copy.deepcopy(a)
        c = copy.deepcopy(a)

        print(str(i) + ", " + \
                str(Timer("insertionSort("+str(a)+")", 'from __main__ import insertionSort').timeit(1)) + ", " + \
                str(Timer("mergeSort("+str(b)+")", 'from __main__ import mergeSort').timeit(1)) + ", " + \
                str(Timer("quickSort("+str(c)+")", 'from __main__ import quickSort').timeit(1)));

    # Tests für CheckSorting
    for i in range(200,500,100):
        a = list(range(i))
        random.shuffle(a)
        b = copy.deepcopy(a)
        c = copy.deepcopy(a)
        assert checkSorting(list(range(i)), insertionSort(a)[0])
        assert checkSorting(list(range(i)), quickSort(b)[0])
        assert checkSorting(list(range(i)), mergeSort(c)[0])
