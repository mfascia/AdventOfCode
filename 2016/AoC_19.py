import sys
import math


nb_elves = 3014387


# Theoretical answer: if n = 2^a + b, solution is 2b+1. See https://www.youtube.com/watch?v=uCsD3ZGzMgE or lookup Josephus problem
# Dec to bin, drop the MSB, add 1 as a LSB, bin to dec, done! 
# For 3001330 elves, solution is 1808357
def main_1(nb):
    b1 = bin(nb)
    b2 = "0b" + b1[3:] + "1"
    d = int(b2, 2)
    return d



# Generate first 100 solutions
def test_2():
    for i in xrange(1, 100):
        elves = [x for x in xrange(0, i)]
        e = 0
        while len(elves) > 1:
            k = (e + len(elves)//2) % len(elves)
            elves.pop(k)
            if k>=e:
                e = e+1
            e = e%len(elves)
        print "nb elves: " + str(i) + ", last: " + str(elves[0]+1)


# Solution deduced from looking at first 100 solutions
#   3^t if == i
#   the max of 
#       i - 3**t
#       2*n - 3*3^t
def main_2(n):
        # extract the largest power of 3. t is the exponent
        t = int(math.log(n,3))

        if 3**t == n:
            return n
        else:
            return max(n-3**t, 2*n - 3*3**t)
        

if __name__ == "__main__":
    print ("Part 1 ---------------------------------------------------------------------------------------------------------")
    print main_1(nb_elves)
    
    print
    
    print ("Part 2 ---------------------------------------------------------------------------------------------------------")
    test_2()
    print main_2(nb_elves)


'''
--- Day 19: An Elephant Named Joseph ---

The Elves contact you over a highly secure emergency channel. Back at the North Pole, the Elves are busy misunderstanding White Elephant parties.

Each Elf brings a present. They all sit in a circle, numbered starting with position 1. Then, starting with the first Elf, they take turns stealing all the presents from the Elf to their left. An Elf with no presents is removed from the circle and does not take turns.

For example, with five Elves (numbered 1 to 5):

  1
5   2
 4 3

    Elf 1 takes Elf 2's present.
    Elf 2 has no presents and is skipped.
    Elf 3 takes Elf 4's present.
    Elf 4 has no presents and is also skipped.
    Elf 5 takes Elf 1's two presents.
    Neither Elf 1 nor Elf 2 have any presents, so both are skipped.
    Elf 3 takes Elf 5's three presents.

So, with five Elves, the Elf that sits starting in position 3 gets all the presents.

With the number of Elves given in your puzzle input, which Elf gets all the presents?

Your puzzle answer was 1808357.
--- Part Two ---

Realizing the folly of their present-exchange rules, the Elves agree to instead steal presents from the Elf directly across the circle. If two Elves are across the circle, the one on the left (from the perspective of the stealer) is stolen from. The other rules remain unchanged: Elves with no presents are removed from the circle entirely, and the other elves move in slightly to keep the circle evenly spaced.

For example, with five Elves (again numbered 1 to 5):

    The Elves sit in a circle; Elf 1 goes first:

      1
    5   2
     4 3

    Elves 3 and 4 are across the circle; Elf 3's present is stolen, being the one to the left. Elf 3 leaves the circle, and the rest of the Elves move in:

      1           1
    5   2  -->  5   2
     4 -          4

    Elf 2 steals from the Elf directly across the circle, Elf 5:

      1         1 
    -   2  -->     2
      4         4 

    Next is Elf 4 who, choosing between Elves 1 and 2, steals from Elf 1:

     -          2  
        2  -->
     4          4

    Finally, Elf 2 steals from Elf 4:

     2
        -->  2  
     -

So, with five Elves, the Elf that sits starting in position 2 gets all the presents.

With the number of Elves given in your puzzle input, which Elf now gets all the presents?

Your puzzle answer was 1407007.
'''