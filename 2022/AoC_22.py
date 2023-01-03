import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
enablePart1 = True
enablePart2 = False
#-----------------------------------------------------------------------------------------------

DIRS = "ESWN"
STEPS = {
	"W": (-1, 0),
	"E": (+1, 0),
	"N": (0, -1),
	"S": (0, +1)
}


def step(board, horiz, verts, pos, dir):
	if dir in "EW":
		nx = pos[0]+STEPS[dir][0]
		ny = pos[1]
		if nx < horiz[ny][0]:
			nx = horiz[ny][1]
		elif nx > horiz[ny][1]:
			nx = horiz[ny][0]
	else:
		nx = pos[0]
		ny = pos[1]+STEPS[dir][1]
		if ny < verts[nx][0]:
			ny = verts[nx][1]
		elif ny > verts[nx][1]:
			ny = verts[nx][0]
	if board[ny][nx] == "#":
		return pos
	else:
		return (nx, ny)


def main_1(inp):
	w = 0
	for line in inp[0:-2]:
		w = max(w, len(line))
	h = len(inp[0:-2])

	board = []
	for y in range(h):
		row = []
		line = inp[y]
		for x in range(min(len(line), w)):
			row.append(line[x])
		for x in range(min(len(line), w), w):
			row.append(" ")
		board.append(row)

	horiz = []
	for y in range(h):
		i = []
		x = 0
		while board[y][x] == " ":
			x += 1	
		i.append(x)
		x = w-1
		while board[y][x] == " ":
			x -= 1	
		i.append(x)
		horiz.append(i)

	verts = []
	for x in range(w):
		i = []
		y = 0
		while board[y][x] == " ":
			y += 1	
		i.append(y)
		y = h-1
		while board[y][x] == " ":
			y -= 1	
		i.append(y)
		verts.append(i)

	if isTest:
		for y in range(h):
			print("".join(board[y]), horiz[y])
		print(verts)

	code = inp[-1]
	moves = []

	i = 0
	while i < len(code):
		if code[i].isalpha():
			moves.append(code[i])
			i += 1
		else:
			nb = ""
			while i < len(code) and code[i].isdigit():
				nb += code[i]
				i += 1
			moves.append(int(nb))

	if isTest:
		print(moves)


	p = (horiz[0][0], 0)
	positions = [p]
	d = 0
	for m in moves:
		if isTest:
			print("Move:", m)
		if m == "L":
			d = (d + 3) % 4
			if isTest:
				print(p, DIRS[d])
		elif m == "R":
			d = (d + 1) % 4
			if isTest:
				print(p, DIRS[d])
		else:
			for n in range(m):
				p = step(board, horiz, verts, p, DIRS[d])
				positions.append(p)
				if isTest:
					print(p, DIRS[d])

	if isTest:
		for y in range(h):
			line = ""
			for x in range(w):
				if (x, y) in positions:
					line += "o"
				else:
					line += board[y][x]
			print(line)

	c = p[0] + 1
	r = p[1] + 1
	print(1000*r + 4*c + d)


def main_2(inp):
	pass


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip("\n\t"), raw)
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