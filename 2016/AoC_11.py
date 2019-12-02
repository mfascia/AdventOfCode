import sys
import copy
import itertools
from Queue import PriorityQueue


materials = ["promethium", "ruthenium", "cobalt", "curium", "plutonium", "elerium", "dilithium"]
materials_short = ["pro", "rut", "cob", "cur", "plu", "ele", "dil"]

init_floors_test = [
#   generator       microchip
    1,              0,          # polonium
    2,              0,          # thulium
]


init_floors_1 = [
#   generator       microchip
    0,              0,          # promethium
    1,              2,          # ruthenium
    1,              2,          # cobalt
    1,              2,          # curium
    1,              2,          # plutonium
]

init_floors_2 = [
#   generator       microchip
    0,              1,          # promethium
    0,              0,          # ruthenium
    0,              0,          # cobalt
    1,              0,          # curium
    1,              0,          # plutonium
    0,              0,          # elerium
    0,              0,          # dilithium
]

init_elevator = 0

# building = [ floors_state, lift_pos ]


def print_state(state, elevator):
    print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    for i in xrange(3, -1, -1):
        text = "" 
        text += "F" + str(i) + (" | E | " if elevator == i else " |   | ")
        for j in xrange(0, len(state)):
            if state[j] == i:
                text += materials_short[j/2] + ("_G" if j%2==0 else "_M") + " "
            else:
                text += "      " 
        print text
    print "=================================================================================="
    print 


def is_goal(state):
    return len(state) * 3 == sum(state)


next_states_cache = {}

def next_valid_states(building):

    hash = hash_building(building)
    if next_states_cache.has_key(hash):
        return next_states_cache[hash]

    state = building[0]
    elevator = building[1]

    on_floor = []
    for i in xrange(0, len(state)):
        if state[i] == elevator:
            on_floor.append(i)

    possible_moves = [list(i) for i in itertools.combinations(on_floor, 2)] + [[i] for i in on_floor]

    valid_next_states = []
    moved_pair = False
    for move in possible_moves:
        # Only move a Chip with its generator
        if len(move)==2 and ((move[1]%2==1 and move[1]-1 != move[0]) or (move[0]%2==1 and move[0]-1 != move[1])):
            continue

        # Moving a single chip is never a good option
        #if len(move)==1 and move[0]%2==1:
        #    continue
       
        if elevator < 3:
            new_state = [x for x in state]
            for item in move:
                if new_state[item] == elevator:
                    new_state[item] += 1
            if check_state(new_state):
                valid_next_states.append([new_state, elevator+1])
        
        if elevator > 0:
            new_state = [x for x in state]
            for item in move:
                if new_state[item] == elevator:
                    new_state[item] -= 1
            if check_state(new_state):
                valid_next_states.append([new_state, elevator-1])

    next_states_cache[hash] = valid_next_states

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
    hash = build[1]
    for i in xrange(0, len(build[0])):
        hash |= build[0][i] << 2*(i+1) 
    return hash


def astar_pathfind(start, neighbours_fn, cost_fn, heuristic_fn, goal_fn):
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

        if goal_fn(current[0]):
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

    path = astar_pathfind([state, 0], next_valid_states, cost_one, cost, is_goal)
    
    print "=== PATH =========================="
    print "Path len:", str(len(path)-1)    
    for p in path:
        print_state(p[0], p[1])


if __name__ == "__main__":
    print "TEST"
    next_states_cache = {}
    print_state(init_floors_test, init_elevator)
    main(init_floors_test, init_elevator)
    print
    print "PART 1"
    next_states_cache = {}
    print_state(init_floors_1, init_elevator)
    main(init_floors_1, init_elevator)
    print
    print "PART 2"
    next_states_cache = {}
    print_state(init_floors_2, init_elevator)
    main(init_floors_2, init_elevator)


'''
--- Day 11: Radioisotope Thermoelectric Generators ---

You come upon a column of four floors that have been entirely sealed off from the rest of the building except for a small dedicated lobby. There are some radiation warnings and a big sign which reads "Radioisotope Testing Facility".

According to the project status board, this facility is currently being used to experiment with Radioisotope Thermoelectric Generators (RTGs, or simply "generators") that are designed to be paired with specially-constructed microchips. Basically, an RTG is a highly radioactive rock that generates electricity through heat.

The experimental RTGs have poor radiation containment, so they're dangerously radioactive. The chips are prototypes and don't have normal radiation shielding, but they do have the ability to generate an electromagnetic radiation shield when powered. Unfortunately, they can only be powered by their corresponding RTG. An RTG powering a microchip is still dangerous to other microchips.

In other words, if a chip is ever left in the same area as another RTG, and it's not connected to its own RTG, the chip will be fried. Therefore, it is assumed that you will follow procedure and keep chips connected to their corresponding RTG when they're in the same room, and away from other RTGs otherwise.

These microchips sound very interesting and useful to your current activities, and you'd like to try to retrieve them. The fourth floor of the facility has an assembling machine which can make a self-contained, shielded computer for you to take with you - that is, if you can bring it all of the RTGs and microchips.

Within the radiation-shielded part of the facility (in which it's safe to have these pre-assembly RTGs), there is an elevator that can move between the four floors. Its capacity rating means it can carry at most yourself and two RTGs or microchips in any combination. (They're rigged to some heavy diagnostic equipment - the assembling machine will detach it for you.) As a security measure, the elevator will only function if it contains at least one RTG or microchip. The elevator always stops on each floor to recharge, and this takes long enough that the items within it and the items on that floor can irradiate each other. (You can prevent this if a Microchip and its Generator end up on the same floor in this way, as they can be connected while the elevator is recharging.)

You make some notes of the locations of each component of interest (your puzzle input). Before you don a hazmat suit and start moving things around, you'd like to have an idea of what you need to do.

When you enter the containment area, you and the elevator will start on the first floor.

For example, suppose the isolated area has the following arrangement:

The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.

As a diagram (F# for a Floor number, E for Elevator, H for Hydrogen, L for Lithium, M for Microchip, and G for Generator), the initial state looks like this:

F4 .  .  .  .  .  
F3 .  .  .  LG .  
F2 .  HG .  .  .  
F1 E  .  HM .  LM 

Then, to get everything up to the assembling machine on the fourth floor, the following steps could be taken:

    Bring the Hydrogen-compatible Microchip to the second floor, which is safe because it can get power from the Hydrogen Generator:

    F4 .  .  .  .  .  
    F3 .  .  .  LG .  
    F2 E  HG HM .  .  
    F1 .  .  .  .  LM 

    Bring both Hydrogen-related items to the third floor, which is safe because the Hydrogen-compatible microchip is getting power from its generator:

    F4 .  .  .  .  .  
    F3 E  HG HM LG .  
    F2 .  .  .  .  .  
    F1 .  .  .  .  LM 

    Leave the Hydrogen Generator on floor three, but bring the Hydrogen-compatible Microchip back down with you so you can still use the elevator:

    F4 .  .  .  .  .  
    F3 .  HG .  LG .  
    F2 E  .  HM .  .  
    F1 .  .  .  .  LM 

    At the first floor, grab the Lithium-compatible Microchip, which is safe because Microchips don't affect each other:

    F4 .  .  .  .  .  
    F3 .  HG .  LG .  
    F2 .  .  .  .  .  
    F1 E  .  HM .  LM 

    Bring both Microchips up one floor, where there is nothing to fry them:

    F4 .  .  .  .  .  
    F3 .  HG .  LG .  
    F2 E  .  HM .  LM 
    F1 .  .  .  .  .  

    Bring both Microchips up again to floor three, where they can be temporarily connected to their corresponding generators while the elevator recharges, preventing either of them from being fried:

    F4 .  .  .  .  .  
    F3 E  HG HM LG LM 
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

    Bring both Microchips to the fourth floor:

    F4 E  .  HM .  LM 
    F3 .  HG .  LG .  
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

    Leave the Lithium-compatible microchip on the fourth floor, but bring the Hydrogen-compatible one so you can still use the elevator; this is safe because although the Lithium Generator is on the destination floor, you can connect Hydrogen-compatible microchip to the Hydrogen Generator there:

    F4 .  .  .  .  LM 
    F3 E  HG HM LG .  
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

    Bring both Generators up to the fourth floor, which is safe because you can connect the Lithium-compatible Microchip to the Lithium Generator upon arrival:

    F4 E  HG .  LG LM 
    F3 .  .  HM .  .  
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

    Bring the Lithium Microchip with you to the third floor so you can use the elevator:

    F4 .  HG .  LG .  
    F3 E  .  HM .  LM 
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

    Bring both Microchips to the fourth floor:

    F4 E  HG HM LG LM 
    F3 .  .  .  .  .  
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

In this arrangement, it takes 11 steps to collect all of the objects at the fourth floor for assembly. (Each elevator stop counts as one step, even if nothing is added to or removed from it.)

In your situation, what is the minimum number of steps required to bring all of the objects to the fourth floor?

Your puzzle answer was 47.
--- Part Two ---

You step into the cleanroom separating the lobby from the isolated area and put on the hazmat suit.

Upon entering the isolated containment area, however, you notice some extra parts on the first floor that weren't listed on the record outside:

    An elerium generator.
    An elerium-compatible microchip.
    A dilithium generator.
    A dilithium-compatible microchip.

These work just like the other generators and microchips. You'll have to get them up to assembly as well.

What is the minimum number of steps required to bring all of the objects, including these four new ones, to the fourth floor?

Your puzzle answer was 71.
'''

