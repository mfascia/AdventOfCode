import sys
from Queue import PriorityQueue

key = 1364


class Cell:
    x = 0
    y = 0

    def __init__(self, ix, iy):
        self.x = ix
        self.y = iy

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self == other
    
    def __hash__(self):
        return hash(tuple((self.x, self.y)))

    def neighbours(self):
        neighbours = []
        if is_open(self.x+1, self.y):
            neighbours.append(Cell(self.x+1, self.y))
        if is_open(self.x, self.y+1):
            neighbours.append(Cell(self.x, self.y+1))
        if self.x > 0 and is_open(self.x-1, self.y):
            neighbours.append(Cell(self.x-1, self.y))
        if self.y > 0 and is_open(self.x, self.y-1):
            neighbours.append(Cell(self.x, self.y-1))
        return neighbours


def maze(w, h):
    maze = []
    for j in xrange(0, h):
        line = ""
        for i in xrange(0, w):
            line += "." if is_open(i, j) else "#"
        maze.append(line)
    return maze


def count_bits(n):
#    return bin(n).count("1")
  n = (n & 0x5555555555555555) + ((n & 0xAAAAAAAAAAAAAAAA) >> 1)
  n = (n & 0x3333333333333333) + ((n & 0xCCCCCCCCCCCCCCCC) >> 2)
  n = (n & 0x0F0F0F0F0F0F0F0F) + ((n & 0xF0F0F0F0F0F0F0F0) >> 4)
  n = (n & 0x00FF00FF00FF00FF) + ((n & 0xFF00FF00FF00FF00) >> 8)
  n = (n & 0x0000FFFF0000FFFF) + ((n & 0xFFFF0000FFFF0000) >> 16)
  n = (n & 0x00000000FFFFFFFF) + ((n & 0xFFFFFFFF00000000) >> 32)
  return n


def is_open(x, y):
    v = x*x + 3*x + 2*x*y + y + y*y + key
    nb_bits = count_bits(v)
    return True if nb_bits % 2 == 0 else False


def manhattan_distance(a, b):
   return abs(a.x - b.x) + abs(a.y - b.y)


def astar_pathfind(start, goal, neighbours_fn, cost_fn, heuristic_fn):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break

        neighbours = neighbours_fn(current) 
        for next in neighbours:
            new_cost = cost_so_far[current] + cost_fn(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic_fn(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    current = goal 
    path = [current]
    while current != start: 
        current = came_from[current]
        path.append(current)
    path.reverse() 

    return path


def all_reachable(start, max_cost, neighbours_fn, cost_fn):
    frontier = [start]
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    edge = []

    while len(frontier):
        current = frontier.pop()
        
        neighbours = neighbours_fn(current) 
        for next in neighbours:
            new_cost = cost_so_far[current] + cost_fn(current, next)
            if new_cost > max_cost:
                continue
            
            if new_cost == max_cost:
                edge.append(next)

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                frontier.append(next)
                came_from[next] = current

    print cost_so_far

    return cost_so_far, edge


def dump(c):
    print c.x, c.y

def main_1():
    c = Cell(1, 1)
    path = astar_pathfind( Cell(1, 1), Cell(31, 39), Cell.neighbours, manhattan_distance, manhattan_distance)
    
    map(lambda x: dump(x), path)
    print "Path length (incl end point):", len(path)


def main_2():
    c = Cell(1, 1)
    all, edge = all_reachable( Cell(1, 1), 50, Cell.neighbours, manhattan_distance)
    print "Can reach:", len(all), "node(s). Incl"
    map(lambda x: dump(x), all)
    


if __name__ == "__main__":
    main_1()
    print
    main_2()


'''
--- Day 13: A Maze of Twisty Little Cubicles ---

You arrive at the first floor of this new building to discover a much less welcoming environment than the shiny atrium of the last one. Instead, you are in a maze of twisty little cubicles, all alike.

Every location in this area is addressed by a pair of non-negative integers (x,y). Each such coordinate is either a wall or an open space. You can't move diagonally. The cube maze starts at 0,0 and seems to extend infinitely toward positive x and y; negative values are invalid, as they represent a location outside the building. You are in a small waiting area at 1,1.

While it seems chaotic, a nearby morale-boosting poster explains, the layout is actually quite logical. You can determine whether a given x,y coordinate will be a wall or an open space using a simple system:

    Find x*x + 3*x + 2*x*y + y + y*y.
    Add the office designer's favorite number (your puzzle input).
    Find the binary representation of that sum; count the number of bits that are 1.
        If the number of bits that are 1 is even, it's an open space.
        If the number of bits that are 1 is odd, it's a wall.

For example, if the office designer's favorite number were 10, drawing walls as # and open spaces as ., the corner of the building containing 0,0 would look like this:

  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###

Now, suppose you wanted to reach 7,4. The shortest route you could take is marked as O:

  0123456789
0 .#.####.##
1 .O#..#...#
2 #OOO.##...
3 ###O#.###.
4 .##OO#OO#.
5 ..##OOO.#.
6 #...##.###

Thus, reaching 7,4 would take a minimum of 11 steps (starting from your current location, 1,1).

What is the fewest number of steps required for you to reach 31,39?

Your puzzle answer was 86.
--- Part Two ---

How many locations (distinct x,y coordinates, including your starting location) can you reach in at most 50 steps?

Your puzzle answer was 127.
'''