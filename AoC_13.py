import sys
from Queue import PriorityQueue

key = 10
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
    path.append(start) 
    path.reverse() 

    return path

def dump(c):
    print c.x, c.y

def main_1():
    c = Cell(1, 1)
    m = maze(10,6)
    for l in m:
        print l
    print
    path = astar_pathfind( Cell(1, 1), Cell(31, 39), Cell.neighbours, manhattan_distance, manhattan_distance)
    
    map(lambda x: dump(x), path)
    print len(path)


def main_2():
    pass


if __name__ == "__main__":
    main_1()
    print
    main_2()
