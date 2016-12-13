import sys
import itertools

input_string = '''The first floor contains a polonium generator, a thulium generator, a thulium-compatible microchip, a promethium generator, a ruthenium generator, a ruthenium-compatible microchip, a cobalt generator, and a cobalt-compatible microchip.
The second floor contains a polonium-compatible microchip and a promethium-compatible microchip.
The third floor contains nothing relevant.
The fourth floor contains nothing relevant.'''

initial_state = {
    "floors": [
        [ "Pol_Gene", "Thu_Gene", "Thu_Chip", "Pro_Gene", "Rut_Gene", "Rut_Chip", "Cob_Gene", "Cob_Chip" ], # Floor 1 = Elevator 0
        [ "Pol_Chip", "Pro_Chip"],                                                                          # Floor 2 = Elevator 1
        [],                                                                                                 # Floor 3 = Elevator 2
        []],                                                                                                 # Floor 4 = Elevator 3
    "elevator": 0
}

'''The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.'''
test_state = { 
    "floors": [  
        [ "Hyd_Chip", "Lit_Chip"],
        [ "Hyd_Gene"],
        [ "Lit_Gene"],
        [] ],
    "elevator": 0
}

test_state2 = { 
    "floors": [  
        [],
        [],
        [ "Hyd_Gene", "Hyd_Chip", "Lit_Gene"],
        [ "Lit_Chip"] ],
    "elevator": 2
}


def print_state(state):
    print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    for i in reversed(xrange(0, len(state["floors"]))):
        print "F" + str(i) + (" | E |" if state["elevator"] == i else "      ") + " " + " ".join(state["floors"][i])
    print "=============================================================="
    print


def cost(state):
    c = (len(state["floors"][2]) + 2*len(state["floors"][1]) + 3*len(state["floors"][0]) + 3 - state["elevator"])
    return c * c

def is_goal_state(state):
    return len(state["floors"][0])==0 and len(state["floors"][1])==0 and len(state["floors"][2])==0 and len(state["floors"][3])>0

def conform_state(state):
    state["floors"] = [sorted(f) for f in state["floors"]] 


def check_floor(floor):
 
    joined = " ".join(floor)
    if not "Gene" in joined:
        return True

    for item in floor:
        if "Chip" in item:
            matching_gen = item.split("_")[0] + "_Gene"
            if not matching_gen in floor:
                return False
    return True


def next_valid_states_from_state(state):
    elevator = state["elevator"]
    floors = state["floors"]     
    floor = floors[elevator]
    next_states = []
    all_move_candidates = [[i] for i in floor] + [list(i) for i in itertools.combinations(floor, 2)]

    min_floor = 0
    for f in xrange(0, elevator):
        min_floor = f
        if len(floors[f]):
            break

    # elevator going up
    if elevator < 3:
        for move in all_move_candidates:
            new_src_floor = [item for item in floor if item not in move]
            new_dst_floor = floors[elevator + 1] + move
            if check_floor(new_src_floor) and check_floor(new_dst_floor):
                next_floors = [f for f in floors]
                next_floors[elevator] = new_src_floor
                next_floors[elevator + 1] = new_dst_floor
                next_state = { "floors": next_floors, "elevator": elevator + 1}
                conform_state(next_state)
                next_states.append(next_state) 
                #print_state(next_state)

    # elevator going down
    if elevator > min_floor:
        for move in all_move_candidates:
            new_src_floor = [item for item in floor if item not in move]
            new_dst_floor = floors[elevator - 1] + move
            if check_floor(new_src_floor) and check_floor(new_dst_floor):
                next_floors = [f for f in floors]
                next_floors[elevator] = new_src_floor
                next_floors[elevator - 1] = new_dst_floor
                next_state = { "floors": next_floors, "elevator": elevator - 1}
                conform_state(next_state)
                next_states.append(next_state) 
                #print_state(next_state)

    return next_states


def make_node(state, parent):
    c = cost(state)
    g = (parent["g"] + 1) if parent else 1
    return {
        "state": state, 
        "parent": parent, 
        "g": g, 
        "h": c,
        "f": g + c,
        }


def print_path(node):
    print "=== PATH =========================="
    path = []
    while node["parent"]:
        path.append(node["state"])
        node = node["parent"]
    for p in reversed(path):
        print_state(p)
    print "Length:", str(len(path))


def search(state):
    close_list = []
    open_list = [make_node(state, None)]
    
    loop = True
    while loop and len(open_list):
        
        print str(len(open_list)), str(len(close_list))

        open_list = sorted(open_list, key=lambda x: x["f"], reverse=True)
        curr = open_list.pop()

        neighbours = next_valid_states_from_state(curr["state"])
        new_nodes = [make_node(neighbour, curr) for neighbour in neighbours]
        for nn in new_nodes:
            skip = False
            if is_goal_state(nn["state"]):
                loop = False
                print_path(nn)
                break
        
            for oln in open_list:
                if nn["state"] == oln["state"] and oln["f"] < nn["f"]:
                    skip = True
                    break
            if skip:
                continue 

            for cln in close_list:
                if nn["state"] == cln["state"] and cln["f"] < nn["f"]:
                    skip = True
                    break
            if skip:
                continue 

            open_list.append(nn)
        close_list.append(curr)
    print "Search is over"


def main_1():
    conform_state(initial_state)
    print_state(initial_state)
    search(initial_state)

def main_2():
    pass


if __name__ == "__main__":
    main_1()
    print
    main_2()


'''
'''

