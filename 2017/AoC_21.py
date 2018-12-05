import os
import sys
import math
from PIL import Image


def generate_perms(p):
    perms = [p]
    if len(p) == 5:
        perms.append( p[3]+p[0]+"/"+p[4]+p[1] )      # CW 90
        perms.append( p[4]+p[3]+"/"+p[1]+p[0] )      # CW 180
        perms.append( p[1]+p[4]+"/"+p[0]+p[3] )      # CW 270
        perms.append( p[1]+p[0]+"/"+p[4]+p[3] )      # H flip
        perms.append( p[0]+p[3]+"/"+p[1]+p[4] )      # CW 90 + H flip
        perms.append( p[3]+p[4]+"/"+p[0]+p[1] )      # CW 180 + H flip
        perms.append( p[4]+p[1]+"/"+p[3]+p[0] )      # CW 270 + H flip
    else:
        perms.append( p[8]+p[4]+p[0]+"/"+p[9]+p[5]+p[1]+"/"+p[10]+p[6]+p[2] )     # CW 90
        perms.append( p[10]+p[9]+p[8]+"/"+p[6]+p[5]+p[4]+"/"+p[2]+p[1]+p[0] )     # CW 180
        perms.append( p[2]+p[6]+p[10]+"/"+p[1]+p[5]+p[9]+"/"+p[0]+p[4]+p[8] )     # CW 270
        perms.append( p[2]+p[1]+p[0]+"/"+p[6]+p[5]+p[4]+"/"+p[10]+p[9]+p[8] )     # H flip
        perms.append( p[0]+p[4]+p[8]+"/"+p[1]+p[5]+p[9]+"/"+p[2]+p[6]+p[10] )     # CW 90 + H flip
        perms.append( p[8]+p[9]+p[10]+"/"+p[4]+p[5]+p[6]+"/"+p[0]+p[1]+p[2] )     # CW 180 + H flip
        perms.append( p[10]+p[6]+p[2]+"/"+p[9]+p[5]+p[1]+"/"+p[8]+p[4]+p[0] )     # CW 270 + H flip
    return perms


def process_rules(inp):
    rules = {}
    for line in inp:
        p, e = line.split( " => ")
        rules[p] = e
    return rules


def image_to_blocks(image):
    size = len(image)
    step = 2 if size % 2 == 0 else 3
    blocks = []
    for y in xrange(0, size, step):
        for x in xrange(0, size, step):
            blockData = []
            block = [[x, y], blockData]
            for j in xrange(0, step):
                for i in xrange(0, step):
                    blockData.append(image[y+j][x+i])
                blockData.append("/")
            blocks.append([[x, y], "".join(blockData[:-1])])
    return blocks


def blocks_to_image(blocks):
    step = 3 if len(blocks[0][1]) == 11 else 4
    size = int(math.sqrt(len(blocks)*step*step))
    image = []
    for y in xrange(0, size):
        image.append([" " for x in xrange(0, size)])

    for block in blocks:
        k = 0
        for y in xrange(0, step):
            for x in xrange(0, step):
                image[block[0][1]+y][block[0][0]+x]  = block[1][k]
                k += 1
            k += 1 #skip "/"
    return image


def print_image(image):
    for y in xrange(0, len(image)):
        print "".join(image[y])


def save_image(image, name):
    im = Image.new(mode="1", size=(len(image), len(image)))
    for y in xrange(0, len(image)):
        for x in xrange(0, len(image)):
            im.putpixel((x, y), 1 if image[y][x] == "#" else 0)
    im.save(name)


def count_image_lit_pixels(image):
    count = 0
    for y in xrange(0, len(image)):
        for x in xrange(0, len(image)):
            if image[y][x] == "#":
                count += 1
    return count


def evolve_blocks(blocks, ruleset):
    newBlocks = []
    for block in blocks:
        coord, data = block
        perms = generate_perms(data)
        for perm in perms:
            if ruleset.has_key(perm):
                newData = ruleset[perm]
                if len(newData) == 11:
                    newCoord = [coord[0]*3/2, coord[1]*3/2]
                    newBlocks.append([newCoord, newData])
                    break
                else:
                    newCoord = [coord[0]*4/3, coord[1]*4/3]
                    newBlocks.append([newCoord, newData])
                    break
    return newBlocks


def main(inp, loops):
    rules = process_rules(inp)
    for old, new in rules.items():
        print old, "=>", new

    blocks = [[[0, 0], ".#./..#/###"]]
    image = blocks_to_image(blocks)
    print "-------------------------------"
    print "Iteration #0"
    print "-------------------------------"
    print_image(image)

    for i in xrange(0, loops):
        print
        print "-------------------------------"
        print "Iteration #" + str(i+1)
        print "-------------------------------"
        grownBlocks = evolve_blocks(blocks, rules)
        image = blocks_to_image(grownBlocks)
        
        #print_image(image)
        
        # write images on disk
        #n = sys.argv[0].replace(".py", "_" + str(i) + ".png")
        #save_image(image, n)
        
        blocks = image_to_blocks(image)
        lit = count_image_lit_pixels(image)
        print ">>>", lit, "lit pixel(s)"
        

def read_input_file(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


if __name__ == "__main__":
    
    # read tests
    tests = []
    if len(tests) == 0:
        i = 0
        while True:
            i += 1
            testfile = sys.argv[0].replace(".py", ("_test_%d.txt" % i))
            if os.path.isfile(testfile):
                tests.append(read_input_file(testfile))
            else:
                break

    # read input
    inp = []
    if len(inp) == 0:
        inp = read_input_file(sys.argv[0].replace(".py", "_input.txt"))

    # run tests
    if False:
        print "--------------------------------------"
        print "- TESTS"
        print "--------------------------------------"
        for test in tests:
            print "Part 1:"
            main(test, 2)
            print "---"

    if True:
        print "--------------------------------------"
        print "- INPUT"
        print "--------------------------------------"
        print "Part 1:"
        main(inp, 5)
        print
        print "Part 2:"
        main(inp, 18)