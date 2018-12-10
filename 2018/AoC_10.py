import os
import sys
import re
from PIL import Image



# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = True
#-----------------------------------------------------------------------------------------------


def decode_input(text):
	pos = []
	vel = []
	for line in text:
		matches = re.match("position=<( *-*[0-9]*), ( *-*[0-9]*)> velocity=<( *-*[0-9]*),( *-*[0-9]*)>", line)
		pos.append([int(matches.group(1))+1000, int(matches.group(2))+1000])
		vel.append([int(matches.group(3)), int(matches.group(4))])
	return pos, vel
	

def save_image(name, pos, w, h, ox, oy, sx, sy):
	im = Image.new(mode="1", size=(w, h))	
	for p in pos:
		x = (p[0] + ox) * sx
		y = (p[1] + oy) * sy
		if x >= 0 and x < w and y >= 0 and y < h:
			im.putpixel((int(x), int(y)), 1)
	im.save(name)


def main(inp, suffix):
	pos, vel = decode_input(inp)

	min_area = (1<<63)
	min_x = (1<<63)
	max_x = (1<<63)
	min_y = (1<<63)
	max_y = (1<<63)
	a = min_area - 1
	t = 0
	while a <= min_area:
		npos = map(lambda x: [x[0][0]+x[1][0], x[0][1]+x[1][1]], zip(pos, vel)) 
		all_x = [p[0] for p in npos]
		all_y = [p[1] for p in npos]
		min_x = min(all_x)
		max_x = max(all_x)
		min_y = min(all_y)
		max_y = max(all_y)
		a = (max_x - min_x) * (max_y - min_y)
		if a <= min_area:
			min_area = a
			pos = [p for p in npos]
			t += 1 

	name = sys.argv[0].replace(".py", ("_" + suffix + "_%d-sec.png" % t))
	w = max_x - min_x + 1
	h = max_y - min_y + 1
	save_image(name, pos, 64, 16, -min_x, -min_y, 64.0/w, 16.0/h )

	print "Part 1: see", name, "for output text"
	print "Part 2:", t, "seconds before text appears"


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream
	

if __name__ == "__main__":
	if doTests:
		# read tests
		if len(tests) == 0:
			i = 0
			while True:
				i += 1
				testfile = sys.argv[0].replace(".py", ("_test_%d.txt" % i))
				if os.path.isfile(testfile):
					tests.append(read_input(testfile))
				else:
					break
		
	if doInput:
		# read input
		if len(inp) == 0:
			inp = read_input(sys.argv[0].replace(".py", "_input.txt"))

	if doTests:
		# run tests
		print "--------------------------------------------------------------------------------"
		print "- TESTS"
		print "--------------------------------------------------------------------------------"
		for t in xrange(0, len(tests)):
			print "--- Test #" + str(t+1) + " ------------------------------"
			main(tests[t], "test") 
			print 

	if doInput:
		# process input
		print "--------------------------------------------------------------------------------"
		print "- INPUT"
		print "--------------------------------------------------------------------------------"
		main(inp, "input")
