import random
from collections import deque

def print_pos(p):
    # Variante 1 mit f-Strings
    for i in range(0,16,4):
        print(f"{p[i]:2} {p[i+1]:2} {p[i+2]:2} {p[i+3]:2}")

    # Variante 2 mit format-Strings
    #for i in range(4):
    #    print("{:2} {:2} {:2} {:2}".format(p[4*i], p[4*i+1], p[4*i+2], p[4*i+3]))

    # Variante 3 "handgemachtes Padding"
    #output = ""
    #for i in range(16):
    #    char = str(p[i])
    #    if len(char) == 1:
    #        output += " " + char
    #    else:
    #        output += char

    #    if i%4 == 3:
    #        output += "\n"
    #    else:
    #        output += " "
    #print(output)

def shuffle_pos(p, n):
    prev = None
    k = 0
    while k < n:
        luecke = p.index(' ')

        # 0: left
        # 1: up
        # 2: right
        # 3: down
        move = random.randint(0,3)


        # "right" in rechter Spalte nicht erlaubt
        if move == 0 and prev != 2 and (luecke % 4) != 3:
            p[luecke], p[luecke+1] = p[luecke+1], p[luecke]
            prev = 0
            k += 1

        # "up" in oberster Reihe nicht erlaubt
        elif move == 1 and prev != 3 and luecke > 3:
            p[luecke], p[luecke-4] = p[luecke-4], p[luecke]
            prev = 1
            k += 1

        # "left" in linker Spalte nicht erlaubt
        elif move == 2 and prev != 0 and (luecke % 4) != 0:
            p[luecke], p[luecke-1] = p[luecke-1], p[luecke]
            prev = 2
            k += 1

        # "down" in unterste Reihe nicht erlaubt
        elif prev != 1 and luecke < 12:
            p[luecke], p[luecke+4] = p[luecke+4], p[luecke]
            prev = 3
            k += 1

def solve_bfs(p, maxlevel):
    parents = {str(p): ''}
    target = str([x if x != 16 else " " for x in range(1, 17)])

    q = deque()
    # Wir speichern zusätzlich zum Knoten auch das "Level" des Knoten, um
    # einfach die Abbruch-Bedingung prüfen zu können: Knoten in zu tiefem Level
    # werden nicht angehängt.
    q.append((p, 0))
    while len(q) > 0:
        p, level = q.popleft()
        luecke = p.index(' ')
        if (luecke % 4) != 3:
            # left
            pp = list(p) # Explizite Kopie von p
            pp[luecke], pp[luecke+1] = pp[luecke+1], pp[luecke]
            pps = str(pp)
            if parents.get(pps) is None:
                parents[pps] = p
                if pp == target:
                    break
                if level < maxlevel:
                    q.append((pp, level+1))
        if luecke > 3:
            # down
            pp = list(p) # Explizite Kopie von p
            pp[luecke], pp[luecke-4] = pp[luecke-4], pp[luecke]
            pps = str(pp)
            if parents.get(pps) is None:
                parents[pps] = p
                if pp == target:
                    break
                if level < maxlevel:
                    q.append((pp, level+1))
        if (luecke % 4) != 0:
            # right
            pp = list(p) # Explizite Kopie von p
            pp[luecke], pp[luecke-1] = pp[luecke-1], pp[luecke]
            pps = str(pp)
            if parents.get(pps) is None:
                parents[pps] = p
                if pp == target:
                    break
                if level < maxlevel:
                    q.append((pp, level+1))
        if luecke < 12:
            # up
            pp = list(p) # Explizite Kopie von p
            pp[luecke], pp[luecke+4] = pp[luecke+4], pp[luecke]
            pps = str(pp)
            if parents.get(pps) is None:
                parents[pps] = p
                if pp == target:
                    break
                if level < maxlevel:
                    q.append((pp, level+1))
        if level == maxlevel:
            pp = None
            break

    res = []
    pp = target
    while pp != '':
        res.append(pp)
        pp = parents[str(pp)]

    if res:
        print("moves:", len(res)-1, '\n')
        res.reverse()
        for p in res:
            if type(p) == list:
                print_pos(p)
                print()
            else:
                # Die letzte Position ist das target, das wieder von str nach
                # list umgewandelt werden muss.
                l = [int(x.strip('[], ')) if "' '" not in x else ' ' for x in p.split(',')]
                print_pos(l)
    else:
        print("unsolved\n")

    return

if __name__ == "__main__":
    A = [x if x != 16 else " " for x in range(1,17)]
    given = [3,7,11,4,2,5,6,8,1,9,12,' ',13,10,14,15]

    print("--- Solving given puzzle ---")
    solve_bfs(given,20)

    print("--- Solving some others ---")
    for _ in range(5):
        n = random.randint(1,12)
        orig = list(A)
        shuffle_pos(orig, n)
        solve_bfs(orig, n+1)

