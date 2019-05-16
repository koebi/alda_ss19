def sieve(n):
    primes = list(range(2,n))

    for p in primes:
        for i in range(p * 2, n, p):
            try:
                primes.remove(i)
                # ACHTUNG: i wird in primes nicht mehr auftauchen
                #          Insbesondere hat das auch Auswirkungen auf die Schleife.
                #          Das ist hier gewollt, aber kann ggf. zu Fehlern führen.
            except ValueError:
                continue

    return primes

# Der folgende Code wird dann spannend, wenn ihr via "import sieve" dieses file selber einbindet.
# Dann wird er nämlich nicht mehr ausgeführt :))
if __name__=="__main__":
    print(sieve(1000))
    print(len(sieve(1000)))
