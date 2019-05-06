import random

def f(x):
    a = 2
    b = 3
    c = 0.5
    return a*x**2 + b*x + c + (random.randint(-2,2))

for i in range(30):
    x = random.randrange(-100,100)
    print("{},{}".format(x,f(x)))
