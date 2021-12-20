import os
import sys
from PIL import Image


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True
#-----------------------------------------------------------------------------------------------

NEIGHBOURS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]


# def enhance(image, algo, iter):
# 	sx = len(image[0])
# 	sy = len(image)
# 	enhanced = [[0 for x in range(sx)] for y in range(sy)]
# 	for y in range(sy):
# 		for x in range(sx):
# 			neighbours = [n for n in map(lambda k: [x+k[0], y+k[1]], NEIGHBOURS) if n[0]>=0 and n[0]<sx and n[1]>=0 and n[1]<sy]
# 			bits = []
# 			for n in neighbours:
# 				bits.append(image[n[1]][n[0]])
# 			lookup = int( "".join([str(b) for b in bits]),2)
# 			enhanced[y][x] = algo[lookup]
# 	return enhanced


def enhance(image, algo, rect, pad, bkg):
	enhanced = {}
	for y in range(rect[1]-pad, rect[3]+pad):
		for x in range(rect[0]-pad, rect[2]+pad):
			neighbours = [n for n in map(lambda k: (x+k[0], y+k[1]), NEIGHBOURS)]
			bits = ""
			for n in neighbours:
				if n in image:
					bits += "1"
				elif n[0]>=rect[0] and n[0]<rect[2] and n[1]>=rect[1] and n[1]<rect[3]:
					bits += "0"
				else:
					bits += bkg
			lookup = int("".join(bits), 2)
			if algo[lookup] == 1:
				enhanced[(x,y)] = 1
	rect = [rect[0]-pad, rect[1]-pad, rect[2]+pad, rect[3]+pad]
	return enhanced, rect


def print_image(image, rect, pad, bkg):
	for y in range(rect[1]-pad, rect[3]+pad):
		line = ""
		for x in range(rect[0]-pad, rect[2]+pad):
			if (x, y) in image:
				line += "#"
			elif x>=rect[0] and x<rect[2] and y>=rect[1] and y<rect[3]:
				line += "."
			else:
				line += "#" if bkg == 1 else "."
		print(line)
	print()



def main(inp, loop):
	algo = [1 if x == "#" else 0 for x in inp[0]]
	
	image = {}

	y = 0
	for line in inp[2:]:
		x = 0
		for c in line:
			if c == "#":
				image[(x, y)] = 1
			x += 1
		y += 1

	bkg = 0
	rect = (0, 0, x, y)

	for i in range(1, loop+1):
		print("enhance pass:", i)
		image, rect = enhance(image, algo, rect, 1, str(bkg))
		bkg = algo[0] if bkg == 0 else algo[511]
		# print_image(image, rect, 5, bkg)
	
	print("lit pixels:", len(image))

	im = Image.new(mode="RGB", size=(rect[2]-rect[0], rect[3]-rect[1]))	
	py = 0
	for y in range(rect[1], rect[3]):
		px = 0
		for x in range(rect[0], rect[2]):
			if (x,y) in image:
				im.putpixel((px, py), (255, 255, 255))
			else:
				im.putpixel((px, py), (0, 0, 0))
			px += 1
		py += 1

	print_image(image, rect, 0, bkg)

	filename = sys.argv[0][:-3]
	if isTest:
		filename += "-test-" + str(loop) + " passes.png"
	else:
		filename += "-input-" + str(loop) + " passes.png"
	im.save(filename)
	

def main_1(inp):
	main(inp, 2)


def main_2(inp):
	main(inp, 50)


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