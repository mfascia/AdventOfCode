import sys


def main(inp):
    hist = [list(inp)]
    state = list(inp)
    iter = 0
    while True:
        iter += 1
        mv = max(state)
        mi = [i for i in xrange(0, len(inp)) if state[i]==mv][0]
        state[mi] = 0
        while mv > 0:
            mi = (mi + 1) % len(inp)
            state[mi] += 1
            mv = mv-1
        print state
        if state in hist:
            print "1: " + str(iter)
            for h in xrange(0, len(hist)):
                if state == hist[h]:
                    print "2: " + str(iter - h)
            break
        else:
            hist.append(list(state))


if __name__ == "__main__":
    
    inp = [5, 1, 10, 0, 1, 7, 13, 14, 3, 12, 8, 10, 7, 12, 0, 6]

    main(inp)