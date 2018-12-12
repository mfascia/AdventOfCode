import sys
import hashlib
from Queue import PriorityQueue


key = "edjrjqaa"


class State:
    path_so_far = ""
    x = 0
    y = 0
    nblink = 0

    def __init__(self, x, y, path):
        self.x = x
        self.y = y
        self.path_so_far = path

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.path_so_far == other.path_so_far

    def __neq__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.x, self.y, self.path_so_far))

    def next_valid_states(self):
        dirs = hashlib.md5(self.path_so_far).hexdigest()[:4]
        states = []
        if dirs[0] in "bcdef" and self.y > 0:
            states.append(State(self.x, self.y - 1, self.path_so_far + "U"))
        if dirs[1] in "bcdef" and self.y < 3:
            states.append(State(self.x, self.y + 1, self.path_so_far + "D"))
        if dirs[2] in "bcdef" and self.x > 0:
            states.append(State(self.x - 1, self.y, self.path_so_far + "L"))
        if dirs[3] in "bcdef" and self.x < 3:
            states.append(State(self.x + 1, self.y, self.path_so_far + "R"))
        return states

    def is_goal(self):
        return self.x == 3 and self.y == 3

    def dump(self):
        print "x:", self.x, "y:", self.y, "path:", self.path_so_far[len(key):], "(length:", len(self.path_so_far[len(key):]), ")"
            

def manhattan_distance(a, b):
   return abs(a.x - b.x) + abs(a.y - b.y)


def cost_one(a, b):
   return 1


def find_longest_path(start, is_goal_fn, neighbours_fn):
    to_visit = [start]
    longest_path = start
    
    while len(to_visit):
        curr = to_visit.pop()

        if is_goal_fn(curr):
            if len(curr.path_so_far) > len(longest_path.path_so_far):
                longest_path = curr
        else:
            to_visit = to_visit + neighbours_fn(curr)

    return longest_path


def astar_pathfind(start, goal, is_goal_fn, neighbours_fn, cost_fn, heuristic_fn):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        
        if is_goal_fn(current):
            break

        neighbours = neighbours_fn(current) 
        for next in neighbours:
            new_cost = cost_so_far[current] + cost_fn(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic_fn(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    path = [current]
    while current != start: 
        current = came_from[current]
        path.append(current)
    path.reverse() 

    return path



def main_1():
    path = astar_pathfind(State(0, 0, key), State(3, 3, ""), State.is_goal, State.next_valid_states, cost_one, manhattan_distance)
    for p in path:
        p.dump()


def main_2():
    longest = find_longest_path(State(0, 0, key), State.is_goal, State.next_valid_states)
    longest.dump()
    pass


if __name__ == "__main__":
    main_1()
    print
    main_2()
    print "--- END ---"

'''
--- Day 17: Two Steps Forward ---

You're trying to access a secure vault protected by a 4x4 grid of small rooms connected by doors. You start in the top-left room (marked S), and you can access the vault (marked V) once you reach the bottom-right room:

#########
#S| | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | |  
####### V

Fixed walls are marked with #, and doors are marked with - or |.

The doors in your current room are either open or closed (and locked) based on the hexadecimal MD5 hash of a passcode (your puzzle input) followed by a sequence of uppercase characters representing the path you have taken so far (U for up, D for down, L for left, and R for right).

Only the first four characters of the hash are used; they represent, respectively, the doors up, down, left, and right from your current position. Any b, c, d, e, or f means that the corresponding door is open; any other character (any number or a) means that the corresponding door is closed and locked.

To access the vault, all you need to do is reach the bottom-right room; reaching this room opens the vault and all doors in the maze.

For example, suppose the passcode is hijkl. Initially, you have taken no steps, and so your path is empty: you simply find the MD5 hash of hijkl alone. The first four characters of this hash are ced9, which indicate that up is open (c), down is open (e), left is open (d), and right is closed and locked (9). Because you start in the top-left corner, there are no "up" or "left" doors to be open, so your only choice is down.

Next, having gone only one step (down, or D), you find the hash of hijklD. This produces f2bc, which indicates that you can go back up, left (but that's a wall), or right. Going right means hashing hijklDR to get 5745 - all doors closed and locked. However, going up instead is worthwhile: even though it returns you to the room you started in, your path would then be DU, opening a different set of doors.

After going DU (and then hashing hijklDU to get 528e), only the right door is open; after going DUR, all doors lock. (Fortunately, your actual passcode is not hijkl).

Passcodes actually used by Easter Bunny Vault Security do allow access to the vault if you know the right path. For example:

    If your passcode were ihgpwlah, the shortest path would be DDRRRD.
    With kglvqrro, the shortest path would be DDUDRLRRUDRD.
    With ulqzkmiv, the shortest would be DRURDRUDDLLDLUURRDULRLDUUDDDRR.

Given your vault's passcode, what is the shortest path (the actual path, not just the length) to reach the vault?

Your puzzle answer was RDURRDDLRD.
--- Part Two ---

You're curious how robust this security solution really is, and so you decide to find longer and longer paths which still provide access to the vault. You remember that paths always end the first time they reach the bottom-right room (that is, they can never pass through it, only end in it).

For example:

    If your passcode were ihgpwlah, the longest path would take 370 steps.
    With kglvqrro, the longest path would be 492 steps long.
    With ulqzkmiv, the longest path would be 830 steps long.

What is the length of the longest path that reaches the vault?

Your puzzle answer was 526.
'''