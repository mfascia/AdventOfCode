import os
import sys
import json


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
enablePart1 = False
enablePart2 = True
#-----------------------------------------------------------------------------------------------


class Pair:
	def __init__(self, text, parent=None):
		self.parent = parent
		if parent == None:
			self.depth = 0
		else:
			self.depth = parent.depth + 1
		self.parse_pair(text)

	def split_number(text):
		opened = 0
		p = 0
		while p<len(text):
			if text[p] == "," and opened == 0:
				return text[0:p], text [p+1:]
			elif text[p] == "[":
				opened += 1
			elif text[p] == "]":
				opened -= 1
			p +=1
		return text, ""

	def parse_pair(self, text):
		if text.isdigit():
			self.data = text
			self.left = None
			self.right = None
		else: 
			left, right = Pair.split_number(text[1:-1])
			self.left = Pair(left, parent=self) 
			self.right = Pair(right, parent=self) 
			self.data = None

	def __str__(self):
		if self.data:
			return self.data
		else:
			return f"[{self.left},{self.right}]"

	def rec_preorder(pair, fct):
		if pair:
			fct(pair)
			Pair.rec_preorder(pair.left, fct)
			Pair.rec_preorder(pair.right, fct)


	def preorder(self, fct):
		return Pair.rec_preorder(self, fct)


	def collect_values(pair, values):
		if pair and pair.data:
			values.append(pair)

	def expand(self):
		while True:
			while self.explode():
				pass
			if not self.split():
				break
		print(self)

	def do_explosion(pair, values, flags):
		if len(flags) == 0:
			if pair.depth == 4 and pair.data == None:
				a = values.index(pair.left)
				if a > 0:
					values[a-1].data = str(int(values[a-1].data) + int(values[a].data))
				b = values.index(pair.right)
				if b < len(values)-1:
					values[b+1].data = str(int(values[b+1].data) + int(values[b].data))
				if pair.parent.left == pair:
					pair.parent.left = Pair("0", pair.parent)
				else:
					pair.parent.right = Pair("0", pair.parent)
				flags.append(False)

	def explode(self):
		values = []
		flags = []
		self.preorder(lambda p: Pair.collect_values(p, values))
		self.preorder(lambda p: Pair.do_explosion(p, values, flags))
		return len(flags) > 0

	def do_split(pair, flags):
		if len(flags) == 0:
			if pair.data != None and int(pair.data) > 9:
				v = int(pair.data) 
				if v % 2 == 0:
					pair.left = Pair(str(int(v/2)), pair)
					pair.right = Pair(str(int(v/2)), pair)
				else:
					pair.left = Pair(str(int((v-1)/2)), pair)
					pair.right = Pair(str(int((v+1)/2)), pair)
				pair.data = None
				flags.append(False)

	def split(self):
		flags = []
		self.preorder(lambda p: Pair.do_split(p, flags))
		return len(flags) > 0


	def add(a, b):
		c = Pair("[" + str(a) + "," + str(b) + "]")
		c.expand()
		return c

	def mag(self):
		if self.data:
			return int(self.data)
		else:
			return 3*self.left.mag() + 2*self.right.mag()


def main_1(inp):
	n = Pair(inp[0])

	for i in range(1, len(inp)):
		m = Pair(inp[i])
		n = Pair.add(n, m)

	print(n.mag())


def main_2(inp):
	numbers = []
	for i in inp:
		numbers.append(Pair(i))

	maxMag = 0
	for i in range(0, len(numbers)):
		for j in range(0, len(numbers)):
			if i == j:
				continue
			maxMag = max(maxMag, Pair.add(numbers[i], numbers[j]).mag())
	print(maxMag)
		


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