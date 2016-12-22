import sys
import re


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream


def main_1(text):
    max_x = 0
    max_y = 0
    nodes = []
    for line in text:
        if line.startswith("/"):
            p = [int(x) for x in re.match("/dev/grid/node-x([0-9]*)-y([0-9]*) *([0-9]*)T *([0-9]*)T *([0-9]*)T *([0-9]*)%", line).groups()]
            max_x = max(max_x, p[0])
            max_y = max(max_y, p[1])
            nodes.append(p)
    
    grid = [[] fox x in nodes]
    for n in nodes:
        grid[max_x*p[1] + p[0]] = n

    


    pass


def main_2(text):
    pass

if __name__ == "__main__":
	text = read_input("AoC_22_input.txt")

	print ("Part 1 ---------------------------------------------------------------------------------------------------------")
	main_1(text)

	print

	print ("Part 2 ---------------------------------------------------------------------------------------------------------")
	main_2(text)


'''

'''