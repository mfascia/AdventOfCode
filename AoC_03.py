import sys

'''
--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways and office furniture that makes up this part of Easter Bunny HQ. This must be a graphic design department; the walls are covered in specifications for triangles.

Or are they?

The design document gives the side lengths of each triangle it describes, but... 5 10 25? Some of these aren't triangles. You can't help but mark the impossible ones.

In a valid triangle, the sum of any two sides must be larger than the remaining side. For example, the "triangle" given above is impossible, because 5 + 10 is not larger than 25.

In your puzzle input, how many of the listed triangles are possible?

Your puzzle answer was 869.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

Now that you've helpfully marked up their design documents, it occurs to you that triangles are specified in groups of three vertically. Each set of three numbers in a column specifies a triangle. Rows are unrelated.

For example, given the following specification, numbers with the same hundreds digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603

In your puzzle input, and instead reading by columns, how many of the listed triangles are possible?
'''

def fn(s, a):
    s.append(a[0])
    s.append(a[1])
    s.append(a[2])

def read_input_stream(filename):
    with open(filename, "r") as f:
        raw = f.read()
        stream = []
        map( lambda c: fn(stream, c), 
                map(lambda a: 
                        map(lambda b: 
                                int(b), a.split()), 
                        raw.split("\n")))
        return stream
    
def main_1(input_stream):
    count = 0
    for i in xrange(0, len(input_stream)/3):
        a = input_stream[3*i]
        b = input_stream[3*i+1]
        c = input_stream[3*i+2]
        if a + b > c and a + c > b and b + c > a:
          count += 1

    print count


def main_2(input_stream):
    count = 0
    for i in xrange(0, len(input_stream)/9):
        a = input_stream[9*i]
        b = input_stream[9*i+3]
        c = input_stream[9*i+6]
        if a + b > c and a + c > b and b + c > a:
          count += 1
        a = input_stream[9*i+1]
        b = input_stream[9*i+4]
        c = input_stream[9*i+7]
        if a + b > c and a + c > b and b + c > a:
          count += 1
        a = input_stream[9*i+2]
        b = input_stream[9*i+5]
        c = input_stream[9*i+8]
        if a + b > c and a + c > b and b + c > a:
          count += 1

    print count

if __name__ == "__main__":
    input_stream = read_input_stream("AoC_03_input.txt")
    main_1(input_stream)
    print
    main_2(input_stream)