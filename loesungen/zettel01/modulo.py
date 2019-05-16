for i in range(-10,11):
    #Formatieren mit .format()
    print("{} %5= {}".format(i, i%5))

for i in range(-10,11):
    #Formatieren mit f-strings
    print(f"{i} %5= {i%5}")
