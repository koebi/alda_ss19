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

        moves = ["right", "up", "down", "left"]
        this = moves[random.randint(0,3)]


        # "right" in rechter Spalte nicht erlaubt
        if this == "right" and prev != "left" and isNotRight(luecke):
            p = move(p, luecke, "right")
            prev = "right"
            k += 1

        # "up" in oberster Reihe nicht erlaubt
        elif this == "up" and prev != "down" and isNotTop(luecke):
            p = move(p, luecke, "up")
            prev = "up"
            k += 1

        # "left" in linker Spalte nicht erlaubt
        elif this == "left" and prev != "right" and isNotLeft(luecke):
            p = move(p, luecke, "left")
            prev = "left"
            k += 1

        # "down" in unterste Reihe nicht erlaubt
        elif prev != "up" and isNotBottom(luecke):
            p = move(p, luecke, "down")
            prev = "down"
            k += 1

    return p

# Hilfsfunktionen, um solve_bfs lesbarer zu machen

def isNotTop(luecke):
    return luecke>3

def isNotRight(luecke):
    return luecke%4 != 3

def isNotLeft(luecke):
    return luecke%4 != 0

def isNotBottom(luecke):
    return luecke<12

def move(p, luecke, move):
    if move == "right":
        pp = list(p)
        pp[luecke], pp[luecke+1] = pp[luecke+1], pp[luecke]
        return pp
    if move == "down":
        pp = list(p) # Explizite Kopie von p
        pp[luecke], pp[luecke+4] = pp[luecke+4], pp[luecke]
        return pp
    if move == "up":
        pp = list(p) # Explizite Kopie von p
        pp[luecke], pp[luecke-4] = pp[luecke-4], pp[luecke]
        return pp
    if move == "left":
        pp = list(p) # Explizite Kopie von p
        pp[luecke], pp[luecke-1] = pp[luecke-1], pp[luecke]
        return pp

def solve_bfs(p, maxlevel):
    parents = {str(p): ''}
    target = str([x if x != 16 else " " for x in range(1, 17)])
    level = 0
    pp = list(p)

    q = deque()
    # Wir speichern zusätzlich zum Knoten auch das "Level" des Knoten, um
    # einfach die Abbruch-Bedingung prüfen zu können: Knoten in zu tiefem Level
    # werden nicht angehängt.
    q.append((p, level))

    while len(q) > 0:
        if pp == target:
            break;

        if level == maxlevel:
            pp = None
            break

        p, level = q.popleft()
        luecke = p.index(' ')

        if isNotRight(luecke):
            pp = move(p, luecke, "right")
            pps = str(pp)
            if parents.get(pps) is None:
                parents[pps] = p
                q.append((pp, level+1))

        if isNotTop(luecke):
            pp = move(p, luecke, "up")
            pps = str(pp)
            if parents.get(pps) is None:
                parents[pps] = p
                q.append((pp, level+1))

        if isNotLeft(luecke):
            pp = move(p, luecke, "left")
            pps = str(pp)
            if parents.get(pps) is None:
                parents[pps] = p
                q.append((pp, level+1))


        if isNotBottom(luecke):
            pp = move(p, luecke, "down")
            pps = str(pp)
            if parents.get(pps) is None:
                parents[pps] = p
                q.append((pp, level+1))

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
        orig = shuffle_pos(orig, n)
        solve_bfs(orig, n+1)
