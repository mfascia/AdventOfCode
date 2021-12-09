import os
import sys
import math
import random
from PIL import Image, ImageDraw


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""

doTests = True
doInput = True
enablePart1 = True
enablePart2 = True

isTest = True
#-----------------------------------------------------------------------------------------------


def main_1(inp):
	terrain = []
	for line in inp:
		terrain.append([int(x) for x in line])
	
	minima = []

	sx = len(terrain[0])
	sy = len(terrain)
	for y in range(0, sy):
		for x in range(0, sx):
			minimum = True
			xs = []
			if x > 0:
				xs.append(x-1)
			if x < sx-1:
				xs.append(x+1)
			ys = []
			if y > 0:
				ys.append(y-1)
			if y < sy-1:
				ys.append(y+1)
			
			for a in xs:
				if terrain[y][x] >= terrain[y][a]:
					minimum = False
					break
			if minimum == True:
				for b in ys:	
					if terrain[y][x] >= terrain[b][x]:
						minimum = False
						break
			if minimum == True:
				minima.append([x, y, terrain[y][x]+1])
	
	risk = sum([x[2] for x in minima])
	print(risk)



def main_2(inp):
	terrain = []
	basins = []
	for line in inp:
		terrain.append([int(x) for x in line])

	sx = len(terrain[0])
	sy = len(terrain)
	
	terrainCopy = [[x for x in y] for y in terrain]

	for y in range(0, sy):
		for x in range(0, sx):
			if terrain[y][x] >= 0 and terrain[y][x] < 9:
				# new basin!
				basinID = -len(basins)-1
				toVisit = [[x, y]]
				basin = []
				while len(toVisit)>0:
					pos = toVisit.pop()
					if terrain[pos[1]][pos[0]] >= 0 and terrain[pos[1]][pos[0]] < 9 and pos not in basin:
						basin.append([pos[0], pos[1], terrain[pos[1]][pos[0]]])
						xs = []
						if pos[0] > 0:
							xs.append(pos[0]-1)
						if pos[0] < sx-1:
							xs.append(pos[0]+1)
						ys = []
						if pos[1] > 0:
							ys.append(pos[1]-1)
						if pos[1] < sy-1:
							ys.append(pos[1]+1)
				
						for a in xs:
							toVisit.append([a, pos[1]])
						for b in ys:	
							toVisit.append([pos[0], b])

						terrain[pos[1]][pos[0]] = basinID
				
				basins.append(basin)

	sortedBasins = sorted([[len(x), x] for x in basins], key=lambda x: x[0], reverse=True)
	val = sortedBasins[0][0] * sortedBasins[1][0] * sortedBasins[2][0]
	print(val)

	im = Image.new(mode="RGB", size=(sx, sy))	
	draw = ImageDraw.Draw(im)
	for b in basins:
		c = (int(random.random()*128.0)+127, int(random.random()*128.0)+127, int(random.random()*128.0)+127) 
		for p in b:
			im.putpixel((p[0], p[1]), (int(c[0]*1.0/float(p[2]+1)), int(c[1]*1.0/float(p[2]+1)), int(c[2]*1.0/float(p[2]+1))))

	filename = sys.argv[0][:-3]
	if isTest:
		filename += "-test.png"
	else:
		filename += "-input.png"

	im.save(filename)



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
		print ("--------------------------------------------------------------------------------")
		print ("- TESTS")
		print ("--------------------------------------------------------------------------------")
		isTest = True
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
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		isTest = False
		if enablePart1:
			print ("--- Part 1 ------------------------------")
			main_1(inp)
		if enablePart2:
			print ("--- Part 2 ------------------------------")
			main_2(inp)