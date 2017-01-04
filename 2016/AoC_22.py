import sys
import re
import itertools


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream


def create_grid(text):
    max_x = 0
    max_y = 0
    grid = []
    nodes = []
    for line in text:
        if line.startswith("/"):
            # node: 0, 1, 2,    3,    4,     5
            #       X, Y, Size, Used, Avail, Use%
            p = [int(x) for x in re.match("/dev/grid/node-x([0-9]*)-y([0-9]*) *([0-9]*)T *([0-9]*)T *([0-9]*)T *([0-9]*)%", line).groups()]
            max_x = max(max_x, p[0])
            max_y = max(max_y, p[1])
            nodes.append(p)
    
    width = max_x + 1
    height = max_y + 1

    grid = [None for n in nodes]
    for n in nodes:
        grid[n[0] + n[1] * width] = n

    return grid, width, height


def get_valid_pairs(grid, width, height):
    print len(grid), str(width*height)
    valid_pairs = []
    all_pairs = itertools.permutations(xrange(0, width * height), 2)
    for pair in all_pairs:
        a = grid[pair[0]]
        b = grid[pair[1]]
        if a[3] > 0 and a[3] <= b[4]:
            valid_pairs.append(pair)

    return valid_pairs


def print_grid(grid, width, height):
    grid_len = len(grid)
    tn = grid[width-1]
    for y in xrange(0, height):
        line = ""
        for x in xrange(0, width):
            n = grid[x + y*width]
            if n[2] < tn[3]:
                line += "-" + str(n[2]) + "-\t"
            else:
                line += str(n[3]) + "/" + str(n[2]) + "\t"
        print line


def main_1(text):
    grid, width, height = create_grid(text)
    valid_pairs = get_valid_pairs(grid, width, height)
    print "grid dimensions (x, y):", width, height
    print "nb valid pairs:", len(valid_pairs)
    


def main_2(text):
    grid, width, height = create_grid(text)
    print_grid(grid, width, height)
    
    '''
        |  0       1       2       3       4       5       6       7       8       9       10      11      12      13      14      15      16      17      18      19      20      21      22      23      24      25      26      27      28      29      30      31      32      33      34      35
        |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    0   |  66/91	70/90	65/94	66/87	69/88	65/92	66/93	64/92	65/93	70/85	65/93	68/87	68/85	67/93	65/91	65/88	65/90	66/89	70/91	72/90	68/90	72/94	65/91	73/87	64/88	73/85	72/89	66/90	65/91	68/88	65/93	72/94	68/94	69/93	70/90	*65/92*	
    1   |  68/87	69/88	70/88	70/88	72/91	69/94	67/85	67/93	65/85	71/88	71/93	64/87	69/86	65/92	72/94	68/86	73/88	73/87	69/89	69/87	64/87	71/85	72/92	66/85	67/91	66/90	73/93	72/92	73/92	64/87	68/86	71/89	69/88	70/88	67/88	66/92	
    2   |  73/93	68/90	68/87	73/86	66/92	70/93	70/89	70/85	64/88	66/90	66/94	68/87	64/88	73/86	69/93	67/91	73/93	65/93	67/93	65/91	64/86	71/90	66/91	64/91	73/85	71/93	65/88	72/93	70/93	73/91	64/90	64/88	65/88	68/92	72/92	72/94	
    3   |  69/89	73/86	70/89	69/86	72/94	71/85	64/88	70/88	70/87	69/85	65/89	71/88	71/88	70/94	70/85	70/92	71/93	64/91	69/93	66/87	69/86	66/87	69/94	69/87	64/89	65/85	66/87	71/86	72/87	71/86	72/87	70/85	72/93	70/91	72/87	71/86	
    4   |  67/88	72/86	73/85	71/93	65/89	67/86	67/93	67/90	69/91	70/94	66/88	66/86	71/86	66/85	67/88	64/86	71/92	68/94	66/90	68/86	66/93	73/86	72/91	72/90	73/89	67/92	67/91	68/93	65/88	69/90	66/94	66/86	70/90	73/86	67/92	68/85	
    5   |  72/87	69/86	70/90	70/92	66/91	71/94	70/92	69/88	72/86	67/89	70/88	72/87	67/93	73/94	70/89	67/92	73/85	64/92	68/90	71/86	68/85	73/85	71/89	66/88	67/91	68/92	68/92	72/93	69/87	69/87	65/90	66/92	73/85	67/94	65/90	72/91	
    6   |  67/85	73/93	69/89	68/92	73/94	64/94	70/91	72/92	72/94	64/88	73/94	67/86	65/87	67/91	64/89	72/88	67/93	73/89	73/92	69/85	68/90	64/93	68/92	66/91	65/85	65/91	73/86	67/86	69/89	72/94	68/89	65/85	68/90	65/89	68/85	72/92	
    7   |  65/86	71/85	67/85	65/94	66/91	65/87	72/85	66/91	66/94	72/85	69/94	66/90	73/93	69/93	67/93	64/86	72/85	64/92	69/93	72/89	66/87	67/93	68/87	72/85	68/88	69/85	73/91	68/93	72/89	71/86	71/85	65/91	72/94	65/87	64/91	72/89	
    8   |  70/93	72/86	64/88	72/92	72/89	73/94	70/85	73/94	64/85	66/92	66/94	66/86	72/90	66/87	66/87	66/88	73/85	66/87	72/93	73/89	65/87	65/92	72/89	68/94	73/92	71/86	71/88	70/93	64/87	73/89	72/88	66/88	71/87	67/94	66/94	70/90	
    9   |  72/85	68/88	71/93	70/90	72/87	72/89	70/92	69/94	68/87	72/92	69/89	71/86	64/92	67/91	68/90	72/94	70/94	69/91	69/90	64/92	68/88	66/94	72/85	67/91	64/94	72/88	64/94	68/87	73/90	71/85	73/89	67/93	66/86	73/91	67/87	71/89	
    10  |  72/88	69/92	71/93	66/89	64/94	64/87	70/88	72/86	70/88	70/89	66/88	72/90	69/89	72/92	65/92	66/92	67/92	72/88	64/89	73/94	68/91	73/85	64/90	69/91	71/92	73/92	69/94	72/87	72/86	71/94	72/93	67/88	73/85	73/94	72/93	67/92	
    11  |  72/86	66/92	73/91	64/94	69/86	64/87	70/90	72/85	71/86	66/88	73/88	67/93	70/86	67/90	73/93	66/87	70/89	68/86	72/94	70/86	71/87	66/86	69/85	72/87	69/93	65/94	65/92	71/91	73/93	69/90	64/87	72/89	71/86	65/90	66/87	68/87	
    12  |  68/89	69/88	65/93	64/93	69/87	73/93	67/89	70/89	66/89	72/89	70/88	68/88	73/90	69/90	73/86	66/88	71/88	69/86	73/94	73/86	69/93	64/92	70/91	69/85	70/88	71/87	67/92	65/94	66/94	73/87	64/93	71/89	70/85	73/88	69/85	71/89	
    13  |  65/85	64/90	71/90	69/85	69/90	68/94	64/93	72/85	69/86	64/93	67/91	68/89	72/87	68/86	66/86	68/91	65/93	73/91	73/91	71/92	70/86	64/94	72/94	64/91	72/87	71/85	72/88	71/94	70/92	66/93	70/93	66/87	65/90	69/89	68/88	64/85	
    14  |  68/90	70/87	70/91	72/85	72/87	73/91	66/89	67/85	72/94	73/92	65/89	69/94	69/88	69/86	72/93	73/85	71/90	67/93	67/94	72/88	73/85	69/89	71/86	66/94	73/94	67/86	66/92	68/86	70/85	71/92	72/88	71/90	72/93	72/89	68/85	68/92	
    15  |  71/93	71/86	72/88	72/94	69/93	73/88	72/87	65/85	73/88	71/94	67/86	66/91	73/87	72/88	72/88	69/94	71/94	67/88	71/88	72/94	68/87	68/92	66/93	64/88	70/91	70/86	69/93	70/87	65/91	66/90	65/91	72/88	72/93	69/90	73/87	65/94	
    16  |  71/94	70/94	72/94	73/87	73/87	66/93	71/87	68/89	68/90	65/88	68/85	64/93	66/93	70/91	65/92	72/88	66/85	66/89	71/92	71/92	72/88	64/89	68/93	69/94	69/91	69/93	71/93	73/88	71/88	66/85	65/88	64/89	71/90	69/93	66/89	65/89	
    17  |  71/88	70/91	494/501	495/510	498/501	494/501	491/502	494/501	498/508	496/508	495/506	493/506	496/504	494/505	497/506	492/503	498/502	494/507	491/502	497/505	498/506	492/509	497/501	494/508	491/510	497/509	494/504	498/504	495/507	498/505	497/509	498/503	498/509	498/506	494/506	496/502	
    18  |  73/90	64/93	65/94	69/85	65/88	70/92	72/91	66/91	65/92	64/89	69/93	67/90	64/86	66/85	73/87	66/91	71/92	68/93	71/94	69/86	67/87	70/94	70/90	65/94	65/87	65/90	73/90	68/87	67/86	67/87	68/92	73/92	70/89	68/87	65/91	72/91	
    19  |  68/92	71/87	66/89	70/94	67/90	67/86	73/91	64/94	65/86	73/91	69/86	66/93	68/87	72/90	64/93	70/88	72/90	72/90	64/85	67/85	72/89	68/89	66/94	64/90	68/93	65/86	65/91	68/92	69/92	70/91	69/88	64/92	69/89	68/94	72/86	67/91	
    20  |  68/89	69/87	64/91	70/92	72/90	70/87	67/85	71/87	72/94	71/93	65/91	69/87	66/92	65/88	72/90	64/93	69/92	68/90	64/94	69/88	70/86	71/85	72/91	65/91	70/88	69/87	67/89	70/88	69/91	72/94	64/85	70/88	64/87	72/89	73/94	72/92	
    21  |  73/93	70/89	73/89	66/85	71/86	64/94	73/90	72/93	65/90	65/89	70/88	69/85	68/90	64/91	67/88	64/86	70/85	66/87	70/90	67/89	72/85	68/87	71/85	69/88	64/90	64/85	67/94	69/91	72/87	68/92	70/89	69/94	71/88	65/90	66/90	69/86	
    22  |  71/94	71/86	65/89	67/93	71/87	68/86	70/90	72/86	69/87	67/92	70/88	69/94	64/91	69/89	71/93	72/94	69/94	64/86	72/85	66/89	66/86	73/94	67/90	66/92	72/92	70/85	67/85	70/88	73/92	69/94	68/89	72/92	65/88	71/86	68/85	65/94	
    23  |  68/89	72/90	71/94	72/86	70/88	71/89	70/87	71/94	66/89	71/88	68/85	64/90	65/86	64/90	72/94	67/93	70/85	66/91	69/86	64/85	67/92	73/92	70/85	69/85	71/86	71/91	73/90	65/92	66/94	72/93	68/94	66/89	69/94	73/89	70/87	66/92	
    24  |  73/93	69/86	72/93	70/92	66/89	67/89	64/89	64/94	73/87	73/87	72/92	70/90	65/91	66/88	68/91	71/92	72/93	73/94	73/86	66/91	66/86	72/91	66/91	65/92	67/89	67/85	65/87	67/93	67/85	65/93	69/87	69/89	66/88	71/91	73/85	67/87	
    25  |  71/85	64/94	65/91	68/85	64/88	73/92	70/93	73/93	67/92	70/88	68/92	72/91	71/93	68/91	69/86	69/94	68/87	66/87	64/92	68/89	65/89	68/87	64/90	71/85	67/88	69/94	64/87	65/87	68/86	65/89	66/87	73/88	71/94	72/94	68/93	73/85	
    26  |  65/93	73/85	67/94	72/93	66/93	72/92	71/94	68/87	64/87	67/86	65/94	67/91	65/92	70/94	65/91	68/88	73/86	73/88	67/89	71/88	68/91	73/92	70/86	67/94	64/89	70/86	68/91	64/87	71/89	70/87	67/94	67/85	66/85	66/89	70/89	72/89	
    27  |  67/90	66/88	68/94	69/92	73/89	68/94	70/91	71/94	69/89	65/88	67/87	71/94	64/94	72/92	68/89	66/92	72/91	71/92	69/88	65/87	66/87	69/88	70/85	68/93	72/86	70/92	70/86	70/89	65/91	68/88	73/87	71/87	66/88	72/85	69/94	( 0/89 )
    28  |  67/87	66/90	73/87	73/93	66/91	69/92	68/90	67/89	69/88	72/94	69/87	65/92	66/88	64/91	67/85	68/93	70/87	66/94	70/86	73/92	64/93	66/85	68/85	66/93	69/88	73/86	67/88	68/86	66/86	65/94	73/86	73/90	70/87	64/93	67/88	66/93	
    29  |  72/89	68/88	65/89	69/88	71/86	73/87	68/85	65/88	73/91	68/87	66/94	70/91	69/85	67/85	64/85	64/90	72/86	68/85	72/88	68/86	70/86	72/85	70/93	65/88	70/90	67/85	73/91	67/93	68/90	67/86	70/85	69/91	69/94	65/86	68/88	65/85	
    '''
    
    # Use the empty cell at (35, 27)
    # 1. shift the empty cell from (35, 27) to (35, 0) going around the "wall" of large cells
    #       - 34 shifts to the left
    #       - 27 shifts up
    #       - 34 shifts to the right
    # ==> Now the empty cell is in (35, 0) and our payload is in (34, 0)
    # 2. With 5 shifts of the empty cell in a "circle" pattern around the payload, we can slide the payload and empty cell left by 1
    # We need 34 shifts for the payload to reach (0, 0)
    #       - 34 cycles of length 5 = 170
    # Total shifts: 34 + 27 + 34 + 5x34 = 265 
    
    print 265


if __name__ == "__main__":
	text = read_input("AoC_22_input.txt")

	print ("Part 1 ---------------------------------------------------------------------------------------------------------")
	main_1(text)

	print

	print ("Part 2 ---------------------------------------------------------------------------------------------------------")
	main_2(text)


'''
--- Day 22: Grid Computing ---

You gain access to a massive storage cluster arranged in a grid; each storage node is only connected to the four nodes directly adjacent to it (three if the node is on an edge, two if it's in a corner).

You can directly access data only on node /dev/grid/node-x0-y0, but you can perform some limited actions on the other nodes:

    You can get the disk usage of all nodes (via df). The result of doing this is in your puzzle input.
    You can instruct a node to move (not copy) all of its data to an adjacent node (if the destination node has enough space to receive the data). The sending node is left empty after this operation.

Nodes are named by their position: the node named node-x10-y10 is adjacent to nodes node-x9-y10, node-x11-y10, node-x10-y9, and node-x10-y11.

Before you begin, you need to understand the arrangement of data on these nodes. Even though you can only move data between directly connected nodes, you're going to need to rearrange a lot of the data to get access to the data you need. Therefore, you need to work out how you might be able to shift data around.

To do this, you'd like to count the number of viable pairs of nodes. A viable pair is any two nodes (A,B), regardless of whether they are directly connected, such that:

    Node A is not empty (its Used is not zero).
    Nodes A and B are not the same node.
    The data on node A (its Used) would fit on node B (its Avail).

How many viable pairs of nodes are there?

Your puzzle answer was 1045.
--- Part Two ---

Now that you have a better understanding of the grid, it's time to get to work.

Your goal is to gain access to the data which begins in the node with y=0 and the highest x (that is, the node in the top-right corner).

For example, suppose you have the following grid:

Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%

In this example, you have a storage grid 3 nodes wide and 3 nodes tall. The node you can access directly, node-x0-y0, is almost full. The node containing the data you want to access, node-x2-y0 (because it has y=0 and the highest x value), contains 6 terabytes of data - enough to fit on your node, if only you could make enough space to move it there.

Fortunately, node-x1-y1 looks like it has enough free space to enable you to move some of this data around. In fact, it seems like all of the nodes have enough space to hold any node's data (except node-x0-y2, which is much larger, very full, and not moving any time soon). So, initially, the grid's capacities and connections look like this:

( 8T/10T) --  7T/ 9T -- [ 6T/10T]
    |           |           |
  6T/11T  --  0T/ 8T --   8T/ 9T
    |           |           |
 28T/32T  --  7T/11T --   6T/ 9T

The node you can access directly is in parentheses; the data you want starts in the node marked by square brackets.

In this example, most of the nodes are interchangable: they're full enough that no other node's data would fit, but small enough that their data could be moved around. Let's draw these nodes as .. The exceptions are the empty node, which we'll draw as _, and the very large, very full node, which we'll draw as #. Let's also draw the goal data as G. Then, it looks like this:

(.) .  G
 .  _  .
 #  .  .

The goal is to move the data in the top right, G, to the node in parentheses. To do this, we can issue some commands to the grid and rearrange the data:

    Move data from node-y0-x1 to node-y1-x1, leaving node node-y0-x1 empty:

    (.) _  G
     .  .  .
     #  .  .

    Move the goal data from node-y0-x2 to node-y0-x1:

    (.) G  _
     .  .  .
     #  .  .

    At this point, we're quite close. However, we have no deletion command, so we have to move some more data around. So, next, we move the data from node-y1-x2 to node-y0-x2:

    (.) G  .
     .  .  _
     #  .  .

    Move the data from node-y1-x1 to node-y1-x2:

    (.) G  .
     .  _  .
     #  .  .

    Move the data from node-y1-x0 to node-y1-x1:

    (.) G  .
     _  .  .
     #  .  .

    Next, we can free up space on our node by moving the data from node-y0-x0 to node-y1-x0:

    (_) G  .
     .  .  .
     #  .  .

    Finally, we can access the goal data by moving the it from node-y0-x1 to node-y0-x0:

    (G) _  .
     .  .  .
     #  .  .

So, after 7 steps, we've accessed the data we want. Unfortunately, each of these moves takes time, and we need to be efficient:

What is the fewest number of steps required to move your goal data to node-x0-y0?

Your puzzle answer was 265.
'''