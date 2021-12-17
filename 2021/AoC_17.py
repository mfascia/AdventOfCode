import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = [[20, 30, -10, -5]]
inp = [269, 292, -68, -44]
isTest = False

doTests = False
doInput = True
#-----------------------------------------------------------------------------------------------

#state: px, py, vx, vy
# target: xmin, xmax, ymin, ymax

def step(state):
	state[0] += state[2]
	state[1] += state[3]
	state[3] -= 1
	if state[2] > 0:
		state[2] -= 1
	elif state[2] < 0:
		state[2] += 1


def inside_target_zone(state, target):
	return target[0] <= state[0] and target[1] >= state[0] and target[2] <= state[1] and target[3] >= state[1]

def missed_target(state, target):
	return state[0] > target[1] or state[1] < target[2]


def main(inp):
	overallMaxY = -10000
	maxVx = 0
	maxVy = 0
	hits = set()
	for vx in range(0, 300):
		for vy in range(-70, 500):
			state = [0, 0, vx, vy]
			maxY = -10000	
			while not inside_target_zone(state, inp) and not missed_target(state, inp):
				step(state)
				maxY = max(state[1], maxY)
			if inside_target_zone(state, inp):
				hits.add((vx, vy, state[0], state[1]))
				if maxY > overallMaxY:
					maxVx = vx
					maxVy = vy
					overallMaxY = maxY

	allVx = [h[0] for h in hits]
	allVy = [h[1] for h in hits]

	print("max Y:", overallMaxY, "reached for initial V: (", maxVx, maxVy, ")")
	print("Found", len(hits), "initial velocities that can hit the targer zone")


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
			print ("--- Test #" + str(t+1) + "---------------------------------")
			main(tests[t])
			print ()

	if doInput:
		# process input
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		main(inp)