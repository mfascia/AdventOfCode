import sys
import re


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream


def decode_rect(text):
	rect = []
	match = re.match("#([0-9]*) @ ([0-9]*),([0-9]*): ([0-9]*)x([0-9]*)", text)
	#               0: id          1: x           	2: y                 3: w          4: h
	i = int(match.group(1))
	rect = [int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5))]
	return i, rect


def main(text):
	n = 1000

	rects = []
	for line in text:
		i, r = decode_rect(line)
		rects.append(r)

	fabric = []
	for y in xrange(0, n):
		row = []
		for x in xrange(0, n):
			row.append(0)
		fabric.append(row)

	print ("Part 1 ---------------------------------------------------------------------------------------------------------")
	for r in rects:
		for y in xrange(r[1], r[1] + r[3]):
			for x in xrange(r[0], r[0] + r[2]):
				fabric[y][x] += 1

	overlap = 0
	for y in xrange(0, n):
		for x in xrange(0, n):
			if fabric[y][x] > 1:
				overlap += 1

	print overlap

	print 

	print ("Part 2 ---------------------------------------------------------------------------------------------------------")
	for k in xrange(0, len(rects)):
		r = rects[k]
		next = False
		for y in xrange(r[1], r[1] + r[3]):
			for x in xrange(r[0], r[0] + r[2]):
				if fabric[y][x] > 1:
					next = True
					break
			if next:
				break
		
		if next:
			continue

		print k+1, r  # ids are 1-based


if __name__ == "__main__":
	in_text = read_input(sys.argv[0].replace(".py", "_input.txt"))

	main(in_text)
