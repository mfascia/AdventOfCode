import os
import sys
from PIL import Image, ImageDraw
import moviepy.video.io.ImageSequenceClip


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

NEIGHBOURS =[[-1, -1], [0, -1], [1, -1], [-1, 0], [0, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
PIX_SIZE = 64


def printGrid(grid):
	for row in grid:
		print("".join([str(x) for x in row]))
	print()


def generateFrame(grid, prefix, nb):
	sx = len(grid[0])
	sy = len(grid)

	im = Image.new(mode="RGB", size=(sx*PIX_SIZE, sy*PIX_SIZE))	
	draw = ImageDraw.Draw(im)

	for y in range(0, sy):
		for x in range(0, sx):
			c = 255
			if grid[y][x] != 0:
				c = grid[y][x]*18
			color = (c,c,c)
			draw.rectangle([x*PIX_SIZE, y*PIX_SIZE, (x+1)*PIX_SIZE, (y+1)*PIX_SIZE], fill=color)
	im.save(prefix + "{:03d}".format(nb) + ".png")


def step(grid):
	sx = len(grid[0])
	sy = len(grid)
	for y in range(0, sy):
		for x in range(0, sx):
			grid[y][x] += 1 
			
	blow = True
	flashes = 0
	while blow:
		blow = False			
		for y in range(0, sy):
			for x in range(0, sx):
				if grid[y][x] >= 10:
					blow = True
					flashes +=1
					grid[y][x] = -10
					neigh = [n for n in map(lambda k: [x+k[0], y+k[1]], NEIGHBOURS) if n[0]>=0 and n[0]<sx and n[1]>=0 and n[1]<sy]
					for p in neigh:
						 grid[p[1]][p[0]] += 1
	for y in range(0, sy):
		for x in range(0, sx):
			if grid[y][x] < 0:
				grid[y][x] = 0
	return flashes

def main_1(inp):
	octopusses = []
	for line in inp:
		octopusses.append([int(x) for x in line])

	flashes = 0
	print("Initial:")
	printGrid(octopusses)
	for s in range(0, 100):
		flashes += step(octopusses)

	print("Step", s+1, ":")
	printGrid(octopusses)
	print("Total flashes:", flashes)


def main_2(inp):
	octopusses = []
	for line in inp:
		octopusses.append([int(x) for x in line])

	# prefix = sys.argv[0].replace(".py", "") + ("\\test\\" if isTest else "\\input\\")

	i = 0
	# generateFrame(octopusses, prefix, 0)
	while True:
		step(octopusses)
		i += 1
		# generateFrame(octopusses, prefix, i)
		check = sum([sum(row) for row in octopusses])
		if check == 0:
			print("All octopusses flashed together at step", i)
			break

	# fps=12
	# image_files = [os.path.join(prefix,img)
	# 			for img in os.listdir(prefix)
	# 			if img.endswith(".png")]
	# clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
	# clip.write_videofile(prefix + '___.mp4')



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