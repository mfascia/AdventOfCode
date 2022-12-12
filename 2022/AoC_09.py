import os
import sys
import tempfile
from PIL import Image
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

MOVES = {
	"U": [0, 1],
	"D": [0, -1],
	"L": [-1, 0],
	"R": [1, 0],
}

def move_knot(head, knot):
	delta = [head[0]-knot[0], head[1]-knot[1]]
	moveTail = False
	if delta[0] == 2:
		delta[0] = 1
		moveTail = True
	if delta[0] == -2:
		delta[0] = -1
		moveTail = True
	if delta[1] == 2:
		delta[1] = 1
		moveTail = True
	if delta[1] == -2:
		delta[1] = -1
		moveTail = True
	if moveTail:
		knot = (knot[0] + delta[0], knot[1] + delta[1])
	return knot


COLORS = [
	(255, 0, 0),
	(180, 180, 180),
	(180, 180, 180),
	(180, 180, 180),
	(180, 180, 180),
	(180, 180, 180),
	(180, 180, 180),
	(180, 180, 180),
	(180, 180, 180),
	(0, 0, 255)
]

def generateFrame(prefix, frame, rope, minPos, maxPos):
	sx = maxPos[0] - minPos[0] + 10
	sy = maxPos[1] - minPos[1] + 10

	im = Image.new(mode="RGB", size=(sx, sy))	

	for k, v in rope.items():
		im.putpixel((k[0]-minPos[0], maxPos[1] - k[1] + minPos[1]), COLORS[v])

	im.save(prefix + "{:06d}".format(frame) + ".png")


def simulate_rope(inp, nbKnots, doVideo=False):
	knots = [(0, 0) for x in range(0, nbKnots)]
	mem = set()
	mem.add((0, 0))
	minPos = [100000, 100000]
	maxPos = [-100000, -100000]

	ropeSteps = []
	for line in inp:

		if isTest:
			print(line)

		direction, count = line.split(" ")
		for c in range(int(count)):
			knots[0] = (knots[0][0] + MOVES[direction][0], knots[0][1] + MOVES[direction][1]) 

			if doVideo:	
				rope = {}
				rope[knots[0]] = 0

			for k in range(1, nbKnots):
				knots[k] = move_knot(knots[k-1], knots[k])

				if doVideo:	
					if not knots[k] in rope:
						rope[knots[k]] = k

			if isTest or doVideo:
				minPos[0] = min(minPos[0], knots[k][0])
				minPos[1] = min(minPos[1], knots[k][1])
				maxPos[0] = max(maxPos[0], knots[k][0])
				maxPos[1] = max(maxPos[1], knots[k][1])

			mem.add(knots[-1])
			if doVideo:	
				ropeSteps.append(rope)

	if isTest:
		for y in range(maxPos[1], minPos[1]-1, -1):
			line = ""
			for x in range(minPos[0], maxPos[0]+1):
				if (x, y) in mem:
					line += "#"
				else:
					line += "."
			print(line)

	if doVideo:	
		tempDirName = sys.argv[0].split("\\")[-1].replace(".py", "")
		if isTest:
			tempDirName += "_test"
		else:
			tempDirName += "_input"
		base = tempfile.mkdtemp(prefix=tempDirName)
		prefix = base + "\\rope_"
		print("Image and video here:", base)
		for f in range(0, len(ropeSteps)):
			generateFrame(prefix, f, ropeSteps[f], minPos, maxPos)

		fps=120
		image_files = [os.path.join(base,img)
					for img in os.listdir(base)
					if img.endswith(".png")]
		clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
		if isTest:
			clip.write_videofile(sys.argv[0].replace(".py", "_test.mp4"))
		else:
			clip.write_videofile(sys.argv[0].replace(".py", "_input.mp4"))

	print("visited:", len(mem))


def main_1(inp):
	simulate_rope(inp, 2)


def main_2(inp):
	simulate_rope(inp, 10, not isTest)


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