import math

def mysqrt(x):
    if x < 0:
        print("mysqrt() funktioniert nicht für negative Zahlen, du Dussel!")
    else:
        return math.sqrt(x)

def mysqrt_te(x):
    try:
        return math.sqrt(x)
    except ValueError:
        print("mysqrt() funktioniert nicht für negative Zahlen, du Dussel!")

mysqrt(-1)
mysqrt_te(-1)

math.sqrt(-1)
