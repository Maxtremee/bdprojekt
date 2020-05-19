def move (y, x):
    print("\033[%d;%dH" % (y, x))

move(10, 10)
print('SIEMA')