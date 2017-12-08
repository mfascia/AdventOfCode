import sys
import math


def main_1(inp):
    r = int(math.sqrt(inp)+1)
    if r%2 == 0:
        r += 1
    x = (r-1)/2
    y = -x

    d = r*r - inp
    if d<(r-1):
        x = x-d
    elif d<2*(r-1):
        x = -x
        y = y + (d - (r-1))
    elif d<3*(r-1):
        x = -x + (d-2*(r-1))
        y = -y
    else:
        y = -y - (d - 3*(r-1))

    print inp, r, x, y, abs(x)+abs(y)
    pass


def main_2(inp):
    print "349975. See https://oeis.org/A141481/b141481.txt"
    pass


if __name__ == "__main__":
    
    inp = 347991

    print "--------------------------------------"
    print "- 1:"
    print "--------------------------------------"
    main_1(inp)

    print "--------------------------------------"
    print "- 2:"
    print "--------------------------------------"
    main_2(inp)