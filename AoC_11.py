import sys
import copy
import itertools
from Queue import PriorityQueue


materials = ["polonium", "thulium", "promethium", "ruthenium", "cobalt", "elerium", "dilithium"]
materials_short = ["pol", "thu", "pro", "rut", "cob", "ele", "dil"]

init_floors_test = [
#   generator       microchip
    1,              0,          # polonium
    2,              0,          # thulium
]


init_floors_1 = [
#   generator       microchip
    0,              1,          # polonium
    0,              0,          # thulium
    0,              1,          # promethium
    0,              0,          # ruthenium
    0,              0,          # cobalt
]

init_floors_2 = [
#   generator       microchip
    0,              1,          # polonium
    0,              0,          # thulium
    0,              1,          # promethium
    0,              0,          # ruthenium
    0,              0,          # cobalt
    0,              0,          # elerium
    0,              0,          # dilithium
]

init_elevator = 0

# state = [ floors, lift_pos ]


def print_state(state, elevator):
    print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    for i in xrange(3, -1, -1):
        text = "" 
        text += "F" + str(i) + (" | E | " if elevator == i else " |   | ")
        for j in xrange(0, len(state)):
            if state[j] == i:
                text += materials_short[j/2] + ("_G" if j%2==0 else "_P") + " "
            else:
                text += "      " 
        print text
    print "=================================================================================="
    print


def is_goal(state):
    return len(state) * 3 == sum(state)


def next_valid_states(building):
    state = building[0]
    elevator = building[1]

    on_floor = []
    for i in xrange(0, len(state)):
        if state[i] == elevator:
            on_floor.append(i)

    possible_moves = [list(i) for i in itertools.combinations(on_floor, 2)] + [[i] for i in on_floor]

    valid_next_states = []
    for move in possible_moves:
        if elevator < 3:
            new_state = copy.deepcopy(state)
            for item in move:
                if new_state[item] == elevator:
                    new_state[item] += 1
            if check_state(new_state):
                valid_next_states.append([new_state, elevator+1])
        
        if elevator > 0:
            new_state = copy.deepcopy(state)
            for item in move:
                if new_state[item] == elevator:
                    new_state[item] -= 1
            if check_state(new_state):
                valid_next_states.append([new_state, elevator-1])

    return valid_next_states


def cost(building):
    state = building[0]
    c = len(state) * 3 - sum(state)
    return c*c


def check_state(state):
    generators = state[0::2]
    chips = state[1::2]
    for i in xrange(0, len(chips)):
        if chips[i] in generators and generators[i] != chips[i]:
            return False 
    
    return True


def cost_one(a, b):
    return 1

def hash_building(build):
    return hash( (tuple(build[0]), build[1]) )


def astar_pathfind(start, neighbours_fn, cost_fn, heuristic_fn):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    hash = hash_building(start)
    came_from[hash] = None
    cost_so_far[hash] = 0

    while not frontier.empty():
        current = frontier.get()
        hash_current = hash_building(current)

        if is_goal(current[0]):
            break

        neighbours = neighbours_fn(current) 
        for next in neighbours:
            hash_next = hash_building(next)
            new_cost = cost_so_far[hash_current] + cost_fn(current, next)
            if hash_next not in cost_so_far or new_cost < cost_so_far[hash_next]:
                cost_so_far[hash_next] = new_cost
                priority = new_cost + heuristic_fn(next)
                frontier.put(next, priority)
                came_from[hash_next] = current

    path = [current]
    while current != start: 
        hash_current = hash_building(current)
        current = came_from[hash_current]
        path.append(current)
    path.reverse() 

    return path


def main(state, elevator):

    path = astar_pathfind([state, 0], next_valid_states, cost_one, cost)
    
    print "=== PATH =========================="
    print "Path len:", str(len(path)-1)    
    for p in path:
        print_state(p[0], p[1])

def main_2():
    pass


if __name__ == "__main__":
    print_state(init_floors_1, init_elevator)
    main(init_floors_1, init_elevator)


'''
'''

