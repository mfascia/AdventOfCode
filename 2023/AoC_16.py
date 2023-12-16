import os
import sys
import copy


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


def parse_grid(text):
	grid = []
	for line in text:
		grid.append([x for x in line])
	return grid, len(grid[0]), len(grid)




class Grid:
	def __init__(self, text):
		self.floor = []
		for line in text:
			self.floor.append([x for x in line])

		self.width = len(self.floor[0])
		self.height = len(self.floor)

		self.lava = [ ["." for x in range(self.width)] for y in range(self.height)]

		self.beams = [Beam(0, 0, 1, 0, set())]


	def tick(self):
		active = 0
		i = 0
		while i < len(self.beams):
			b = self.beams[i]
			if b.active:
				active += 1

				self.lava[b.y][b.x] = "#"
				split = b.step(self)
				if split:
					self.beams.append(split)
				i +=1
			else:
				self.beams.pop(i)
		if isTest:
			self.dump()
			print("active beams =", active)
		
		return active > 0


	def count_lava(self):
		count = 0
		for row in self.lava:
			count += sum([1 if x=="#" else 0 for x in row])
		return count


	def dump(self):
		for y in range(self.height):
			line = "".join([x for x in self.floor[y]]) + "    " + "".join([x for x in self.lava[y]])
			for b in self.beams:
				if not b.active or b.x < 0 or b.x >= self.width or b.y < 0 or b.y >= self.height:
					continue

				if b.y == y:
					c = ""
					dir = [b.dx, b.dy]
					if dir == [0, 1]:
						c = "v"
					elif dir == [0, -1]:
						c = "^"
					elif dir == [1, 0]:
						c = ">"
					elif dir == [-1, 0]:
						c = "<"
					if line[b.x] not in ".\\/-|":
						if c in "<>^v":
							v = 1
						else:
							v = int(line[b.x])
						c = str(v+1)
					line = line[0:b.x] + c + line[b.x+1:]	
			print(line)
		print()


class Beam:
	def __init__(self, x, y, dx, dy, history):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.history = set(copy.deepcopy(history))
		self.active = True


	def step(self, grid):
		if not self.active:
			return
		
		h = self.x * 100000000 + self.y * 10000 + self.dx * 10 + self.dy
		
		if h in self.history:
			self.active = False
			return
		else:
			self.history.add(h)
		
		c = grid.floor[self.y][self.x]

		split = None

		if c != ".":
			if c == "/":
				tmp = self.dx
				self.dx = -self.dy
				self.dy = -tmp
			elif c == "\\":
				tmp = self.dx
				self.dx = self.dy
				self.dy = tmp
			elif c == "|" and self.dx != 0:
				self.dx = 0
				self.dy = 1
				split = Beam(self.x, self.y, 0, -1, [h for h in self.history])
			elif c == "-" and self.dy != 0:
				self.dx = 1
				self.dy = 0
				split = Beam(self.x, self.y, -1, 0, [h for h in self.history])

		self.x = self.x + self.dx
		self.y = self.y + self.dy

		if self.y == 10:
			pass

		if self.x < 0 or self.x >= grid.width or self.y < 0 or self.y >= grid.height:
			self.active = False
		
		return split


def main_1(inp):
	grid = Grid(inp)

	while True:
		if not grid.tick():
			break

	print("Lava =", grid.count_lava())
		

def main_2(inp):
	pass


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