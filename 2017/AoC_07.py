import sys
import re


def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream

def aggregate_weight(node, tree, weights):
    w = 0
    sub_w = []

    # Find all subtrees from a node
    children = [k for k,v in tree.items() if v == node]
    if len(children) == 0:
        return weights[node]
    for c in children:
        # find whether a child is a leaf or a tree
        agg = aggregate_weight(c, tree, weights)
        sub_w.append(agg)
        w += agg
    
    # if the children are unbalanced, try and find 
    if w != len(children) * sub_w[0]:
        weight_lut = {}
        for k in sub_w:
            if weight_lut.has_key(k):
                weight_lut[k] += 1
            else:
                weight_lut[k] = 1
        correct_weight = [k for k, v in weight_lut.items() if v > 1][0] 
        bad_weight = [k for k, v in weight_lut.items() if v == 1][0]
        diff = bad_weight - correct_weight

        n = 0
        for n in xrange(0, len(children)):
            if sub_w[n] == bad_weight:
                break
        
        corrected_weight = weights[children[n]] - diff 
        print children[n], corrected_weight

    w += weights[node]
    return w


def build_tree(node, parents, weights):
    node["children"] = []
    children = [k for k, v in parents.items() if v == node["name"]]
    for child in children:
        sub = {
            "name": child,
            "weight": weights[child]
        }
        node["children"].append(sub)
        build_tree(sub, parents, weights)


def sum_weights(node):
    total = node["weight"]
    for child in node["children"]:
        sum_weights(child)
        total += child["weight_above"]
    node["weight_above"] = total
    return total


def print_tree(node, level):
    spaces = ""
    for i in xrange(0, level):
        spaces += "    "
    print spaces + "%s (%d | %d)" % (node["name"], node["weight_above"], node["weight"])
    for child in node["children"]:
        print_tree(child, level+1)


def main_1(inp):
    parents = {}
    weights = {}
    for line in inp:
        parts = re.match("([a-z]*) \(([0-9]*)\)(?: -> (.*))?", line)

        name = parts.group(1)
        weight = int(parts.group(2))
        weights[name] = weight
        
        if not parents.has_key(name):
            parents[name] = None

        if parts.group(3) > None:
            children = parts.group(3).split(", ")
            for child in children:
                parents[child] = name

    root = None

    for p in parents:
        if parents[p] == None:
            root = p
            break

    print root

    tree = {
        "name": root,
        "weight": weights[root]
    }

    build_tree(tree, parents, weights)
    sum_weights(tree)
    print_tree(tree, 0)

    aggregate_weight( root, parents, weights )



def main_2(inp):
    pass

if __name__ == "__main__":
    
    inp = ""
    if len(inp) == 0:
        inp = read_input_file(sys.argv[0].replace(".py", "_input.txt"))

    print "--------------------------------------"
    print "- 1:"
    print "--------------------------------------"
    main_1(inp)

    print "--------------------------------------"
    print "- 2:"
    print "--------------------------------------"
    main_2(inp)