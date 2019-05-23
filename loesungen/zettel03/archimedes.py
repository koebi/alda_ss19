from math import sqrt

def archimedes1(k):
    s,t,n = sqrt(2),2,4 #Startwerte: Quadrat
    print ('n:',n,' s:', n/2*s,'< pi < t:',n/2*t,'Dif:',n/2*t-n/2*s)
    for i in range(k):
        # Prüfung, ob iterierter Wert und Formel nach 2d) übereinstimmen
        if abs(t - 2.0*s / sqrt(4.0 - s**2)) < 1e-15:
            n *= 2
            s = sqrt(2.0 - sqrt(4.0 - s**2))
            t = 2.0 / t * (sqrt(4.0 + t**2) - 2.0)
            print ('n:',n,' s:', n/2*s,'< pi < t:',n/2*t,'Dif:',n/2*t-n/2*s)
        else:
           print ('Fehler bei n =', n)
           break


def archimedes2(k):
    s,t,n = sqrt(2),2,4 #Startwerte: Quadrat
    print ('n:',n,' s:', n/2*s,'< pi < t:',n/2*t,'Dif:',n/2*t-n/2*s)
    for i in range(0,k):
        # Prüfung, ob iterierter Wert und Formel nach 2d) übereinstimmen
        if abs(t - 2.0*s / sqrt(4.0 - s**2)) < 1e-15:
            n *= 2
            s = s / sqrt(2.0 + sqrt(4.0 - s**2))
            t = (2.0*t) / (sqrt(4.0 + t**2) + 2.0)
            print ('n:',n,' s:', n/2*s,'< pi < t:',n/2*t,'Dif:',n/2*t-n/2*s)
        else:
           print ('Fehler bei n =', n)
           break

print ("Ursprüngliche Implementation")
archimedes1(30)
print ("Implementation nach 2c)")
archimedes2(30)
