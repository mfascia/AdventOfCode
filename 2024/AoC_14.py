import os
import sys
from PIL import Image, ImageDraw


import AoC as aoc


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = False
doInput = True
enablePart1 = False
enablePart2 = True
#-----------------------------------------------------------------------------------------------


def parse(inp):
	width = 11 if isTest else 101 
	height = 7 if isTest else 103 

	robots = []
	for line in inp:
		tp, tv = line.split(" ")
		p = aoc.Vector.from_list([int(x) for x in tp[2:].split(",")])
		v = aoc.Vector.from_list([int(x) for x in tv[2:].split(",")])
		robots.append([p, v])
	return robots, width, height


def gen_image(robots, width, height, time):
	im = Image.new(mode="RGB", size=(width, height))	
	draw = ImageDraw.Draw(im)

	for r in robots:
		im.putpixel((r[0].x, r[0].y), (255, 255, 255))

	filename = sys.argv[0][:-3]
	if isTest:
		filename += "-test-{:04d}".format(time) + ".png"
	else:
		filename += "-input-{:04d}".format(time) + ".png"

	im.save(filename)


def main_1(inp):
	robots, width, height = parse(inp)
	# for r in robots:
	# 	print(r)

	quad = [0, 0, 0, 0]		# top-left, top-right, bottom-left, bottom-right
	for r in robots:
		r[0].x = (r[0].x + (r[1].x * 100)) % width
		r[0].y = (r[0].y + (r[1].y * 100)) % height
		if not (width % 2 == 1 and r[0].x == int(width/2)) and not (height % 2 == 1 and r[0].y == int(height/2)):
			if r[0].x < width/2:
				if r[0].y < height/2:
					quad[0] += 1
				else:
					quad[2] += 1
			else:
				if r[0].y < height/2:
					quad[1] += 1
				else:
					quad[3] += 1

	# for y in range(height):
	# 	line = ""
	# 	for x in range(width):
	# 		count = 0
	# 		p = aoc.Vector(x, y)
	# 		for r in robots:
	# 			if r[0] == p:
	# 				count += 1
	# 		if count > 0:
	# 			line += str(count)
	# 		else:
	# 			line += "."	
	# 	print(line) 

	safety = 1
	for q in quad:
		safety *= q
	print(safety)


def main_2(inp):
	robots, width, height = parse(inp)

	# for t in range(0, 10000):
	# 	for r in robots:
	# 		r[0].x = (r[0].x + (r[1].x)) % width
	# 		r[0].y = (r[0].y + (r[1].y)) % height
	# 	gen_image(robots, width, height, t)

	print("8280")

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
					tests.append([x for x in read_input(testfile)])
				else:
					break
		
	if doInput:
		# read input
		if len(inp) == 0:
			inp = [x for x in read_input(sys.argv[0].replace(".py", "_input.txt"))]

	if doTests:
		# run tests
		isTest = True
		print ("--------------------------------------------------------------------------------")
		print ("- TESTS")
		print ("--------------------------------------------------------------------------------")
		for t in range(0, len(tests)):
			if enablePart1:
				print ("--- Test #" + str(t+1) + ".1 ------------------------------")
				main_1(tests[t])
			if enablePart2:
				print ("--- Test #" + str(t+1) + ".2 ------------------------------")
				main_2(tests[t])
			print ()

	if doInput:
		# process input
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		if enablePart1:
			print ("--- Part 1 ------------------------------")
			main_1(inp)
		if enablePart2:
			print ("--- Part 2 ------------------------------")
			main_2(inp)