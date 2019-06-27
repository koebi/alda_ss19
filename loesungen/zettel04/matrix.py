import timeit

# Im Folgenden sind mehrere Möglichkeiten dargestellt, die Aufgabe zu lösen.

# Setup: String um die benötigten Listen (Matrizen zu erzeugen)
setup = '''\
size = 100
size2 = size*size
A = [0]*(size**2)
B = [0]*(size**2)
C = [0]*(size**2)
'''

# naive: Naive Implementierung der Matrizenmuliplikation
naive = '''\
for i in range(size):
    for j in range(size):
        for k in range(size):
            C[i+j*size] += A[i+k*size]*B[k+j*size] # 8 Rechenoperationen, 3 Listenzugriffe
'''

# ijk: Invariante Teilausdrücke vorgezogen
ijk = '''\
for i in range(size):
    for j in range(size):
        ij = i+j*size
        js = j*size
        for k in range(size):
            C[ij] += A[i+k*size]*B[k+js] # 5 Rechenoperationen, 3 Listenzugriffe
'''

# ikj: Schleifen umgestellt
ikj = '''\
for i in range(size):
    for k in range(size):
        a = A[i+k*size]
        for js in range(0, size2, size):
            C[i+js] += a*B[k+js] # 4 Rechenoperationen, 3 Listenzugriffe
'''

# jik: Erste Schleifen getauscht
jik = '''\
for j in range(size):
    for i in range(size):
        ij = i+j*size
        js = j*size
        for k in range(size):
            C[ij] += A[i+k*size]*B[k+js] # 5 Rechenoperationen, 3 Listenzugriffe
'''

# jki: Schleifen umgestellt
jki = '''\
for j in range(size):
    sj = j*size
    for k in range(size):
        sk = k*size
        b = B[k+j*size]
        for i in range(size):
            C[i+sj] += A[i+sk]*b # 4 Rechenoperationen, 2 Listenzugriffe
'''

# kij: Schleifen umgestellt
kij = '''\
for k in range(size):
    for i in range(size):
        a = A[i+k*size]
        for js in range(0, size2, size):
            C[i+js] += a*B[k+js] # 4 Rechenoperationen, 2 Listenzugriffe
'''

# kji: Schleifen umgestellt
kji = '''\
for k in range(size):
    for j in range(size):
        sj = j*size
        sk = k*size
        b = B[k+j*size]
        for i in range(size):
            C[i+sj] += A[i+sk]*b # 4 Rechenoperationen, 2 Listenzugriffe
'''

# Zeitmessung der verschiedenen Varianten
# Timer Instanzen anlegen
tnaive = timeit.Timer(stmt=naive, setup=setup)
tijk = timeit.Timer(stmt=ijk, setup=setup)
tikj = timeit.Timer(stmt=ikj, setup=setup)
tjik = timeit.Timer(stmt=jik, setup=setup)
tjki = timeit.Timer(stmt=jki, setup=setup)
tkij = timeit.Timer(stmt=kij, setup=setup)
tkji = timeit.Timer(stmt=kji, setup=setup)
# Ausgabe der Ergebnisse
print()
print("matrix multiplication:")
repeats = 5
# Zeitmessung 5-mal mit Minimum aus 3 Wiederholungen (Resultate: Python 3.5 auf Windows)
print("naive:", min(tnaive.repeat(number=repeats)) / repeats) # naive: 0.5246211177571919
print("ijk:", min(tijk.repeat(number=repeats)) / repeats)     # ijk: 0.39169394584571454
print("ikj:", min(tikj.repeat(number=repeats)) / repeats)     # ikj: 0.3199294242736325
print("jik:", min(tjik.repeat(number=repeats)) / repeats)     # jik: 0.39610200092970943
print("jki:", min(tjki.repeat(number=repeats)) / repeats)     # jki: 0.28425693879071046
print("kij:", min(tkij.repeat(number=repeats)) / repeats)     # kij: 0.32087279675577635
print("kji:", min(tkji.repeat(number=repeats)) / repeats)     # kji: 0.28381304109983035
