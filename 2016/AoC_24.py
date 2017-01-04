import sys
import itertools
import copy
from Queue import PriorityQueue


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream    


def interest_points(grid):
    points = {}
    y = 0
    for line in grid:
        x = 0
        for c in line:
            if c.isdigit():
                points[int(c)] = [x, y]
            x += 1
        y += 1
    return points


def hash_pair(cell):
    return 1000*cell[1] + cell[0]


def neighbours(grid, cell):
    cells = []
    width = len(grid[0])
    height = len(grid)
    if cell[0] > 0:
        if grid[cell[1]][cell[0]-1] != "#":
            cells.append([cell[0]-1, cell[1]])
    if cell[0] < width-1:
        if grid[cell[1]][cell[0]+1] != "#":
            cells.append([cell[0]+1, cell[1]])
    if cell[1] > 0:
        if grid[cell[1]-1][cell[0]] != "#":
            cells.append([cell[0], cell[1]-1])
    if cell[1] < height-1:
        if grid[cell[1]+1][cell[0]] != "#":
            cells.append([cell[0], cell[1]+1])
    return cells


def manhattan_distance(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])


def cost_one(a, b):
   return 1


def astar_pathfind(grid, start, goal, hash_fn, neighbours_fn, cost_fn, heuristic_fn):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    start_hash = hash_fn(start)
    came_from[start_hash] = None
    cost_so_far[start_hash] = 0
    goal_hash = hash_fn(goal)
    found = False

    while not frontier.empty():
        current = frontier.get()
        current_hash = hash_fn(current)
        
        if current_hash == goal_hash:
            found = True
            #break

        neighbours = neighbours_fn(grid, current) 
        for next in neighbours:
            new_cost = cost_so_far[current_hash] + cost_fn(current, next)
            next_hash = hash_fn(next)
            if next_hash not in cost_so_far or new_cost < cost_so_far[next_hash]:
                cost_so_far[next_hash] = new_cost
                priority = new_cost + heuristic_fn(goal, next)
                frontier.put(next, priority)
                came_from[next_hash] = current

    if found:
        current  = goal
        path = [current]
        while hash_fn(current) != start_hash: 
            current = came_from[hash_fn(current)]
            path.append(current)
        path.pop()
        path.reverse() 
        return path
    else:
        return []


def build_cache(text):
    cache = {}
    points = interest_points(text)
    keys = [k for k, v in points.iteritems()]
    for pair in itertools.permutations(keys, 2):
        pair_hash = hash_pair([pair[0], pair[1]])
        length = -1
        if cache.has_key(pair_hash):
            length = len(cache[pair_hash])
        else:
            path = astar_pathfind(text, points[pair[0]], points[pair[1]], hash_pair, neighbours, cost_one, manhattan_distance)
            print str(pair) + "[" + str(points[pair[0]]) + ", " + str(points[pair[1]]) + "] -> " + str(len(path))
            cache[pair_hash] = path
    
    return cache, points


def main_1(text, cache, points):
    keys = [k for k, v in points.iteritems()][1:]
    shortest = 100000000
    for perm in itertools.permutations(keys, len(keys)):
        perm = [0] + list(perm)
        total_length = 0
        for i in xrange(0, len(perm)-1):
            pair_hash = hash_pair([perm[i], perm[i+1]])
            path = cache[pair_hash]
            total_length += len(path)
        shortest = min(total_length, shortest)
    print "Shortest path: " + str(shortest)


def main_2(text, cache, points):
    keys = [k for k, v in points.iteritems()][1:]
    shortest = 100000000
    for perm in itertools.permutations(keys, len(keys)):
        perm = [0] + list(perm) + [0]
        total_length = 0
        for i in xrange(0, len(perm)-1):
            pair_hash = hash_pair([perm[i], perm[i+1]])
            path = cache[pair_hash]
            total_length += len(path)
        shortest = min(total_length, shortest)
    print "Shortest path: " + str(shortest)


if __name__ == "__main__":
    text = read_input("AoC_24_input.txt")
    cache, points = build_cache(text)
    
    print " Part 1 ------------------------------------------------------------"
    main_1(text, cache, points)
    
    print
    
    print " Part 2 ------------------------------------------------------------"
    main_2(text, cache, points)


'''
--- Day 24: Air Duct Spelunking ---

You've finally met your match; the doors that provide access to the roof are locked tight, and all of the controls and related electronics are inaccessible. You simply can't reach them.

The robot that cleans the air ducts, however, can.

It's not a very fast little robot, but you reconfigure it to be able to interface with some of the exposed wires that have been routed through the HVAC system. If you can direct it to each of those locations, you should be able to bypass the security controls.

You extract the duct layout for this area from some blueprints you acquired and create a map with the relevant locations marked (your puzzle input). 0 is your current location, from which the cleaning robot embarks; the other numbers are (in no particular order) the locations the robot needs to visit at least once each. Walls are marked as #, and open passages are marked as .. Numbers behave like open passages.

For example, suppose you have a map like the following:

###########
#0.1.....2#
#.#######.#
#4.......3#
###########

To reach all of the points of interest as quickly as possible, you would have the robot take the following path:

    0 to 4 (2 steps)
    4 to 1 (4 steps; it can't move diagonally)
    1 to 2 (6 steps)
    2 to 3 (2 steps)

Since the robot isn't very fast, you need to find it the shortest route. This path is the fewest steps (in the above example, a total of 14) required to start at 0 and then visit every other location at least once.

Given your actual map, and starting from location 0, what is the fewest number of steps required to visit every non-0 number marked on the map at least once?

Your puzzle answer was 428.
--- Part Two ---

Of course, if you leave the cleaning robot somewhere weird, someone is bound to notice.

What is the fewest number of steps required to start at 0, visit every non-0 number marked on the map at least once, and then return to 0?

Your puzzle answer was 680.
'''