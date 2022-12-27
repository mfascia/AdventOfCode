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
enablePart2 = True
#-----------------------------------------------------------------------------------------------


class Node:
	def __init__(self, data):
		self.data = data
		self.next = None
		self.prev = None

class DequeIterator:
	def __init__(self, deque):
		self.deque = deque
		self.curr = deque.anchor

	def __next__(self):
		self.curr = self.curr.next
		if self.curr == self.deque.anchor:
			raise StopIteration
		else:
			return self.curr.data

class Deque:
	def __init__(self):
		self.size = 0
		self.anchor = Node(None)
		self.anchor.next = self.anchor 
		self.anchor.prev = self.anchor 

	def __iter__(self):
		return DequeIterator(self)

	def head(self):
		if self.size > 0:
			return self.anchor.prev
		else:
			return None

	def push(self, data):
		i = Node(data)
		i.prev = self.anchor.prev
		self.anchor.prev.next = i
		self.anchor.prev = i
		i.next = self.anchor
		self.size += 1

	def insert_node_after(self, ins, node):
		ins.next.prev = node
		node.next = ins.next
		ins.next = node
		node.prev = ins
		self.size += 1

	def remove(self, node):
		node.prev.next = node.next
		node.next.prev = node.prev
		node.prev = None
		node.next = None
		self.size -= 1


def read_values(inp, multiplier):
	initial = []
	queue = Deque()
	for line in inp:
		queue.push(int(line)*multiplier)
		n = queue.head()
		initial.append(n)
	return initial, queue


def mix(initial, queue):
	for i in initial:
		j = abs(i.data) % (queue.size-1) # mod size -1 because the item being moved does not count
		if i.data > 0:
			n = i
			for k in range(j):
				n = n.next
				if n == queue.anchor:
					n = n.next
		else:
			n = i
			for k in range(j):
				n = n.prev
				if n == queue.anchor:
					n = n.prev
			n = n.prev
			if n == queue.anchor:
				n = n.prev
		queue.remove(i)
		queue.insert_node_after(n, i)



def main_1(inp):
	initial, queue = read_values(inp, 1)
	mix(initial, queue)

	values = [x for x in queue]
	i = values.index(0)
	print("found 0 at index", i)
	print((i+1000) % len(values), "-->", values[(i+1000) % len(values)])
	print((i+2000) % len(values), "-->", values[(i+2000) % len(values)])
	print((i+3000) % len(values), "-->", values[(i+3000) % len(values)])
	print("sum:", values[(i+1000) % len(values)] + values[(i+2000) % len(values)] + values[(i+3000) % len(values)])


def main_2(inp):
	initial, queue = read_values(inp, 811589153)
	for m in range(10):
		mix(initial, queue)

	values = [x for x in queue]
	i = values.index(0)
	print("found 0 at index", i)
	print((i+1000) % len(values), "-->", values[(i+1000) % len(values)])
	print((i+2000) % len(values), "-->", values[(i+2000) % len(values)])
	print((i+3000) % len(values), "-->", values[(i+3000) % len(values)])
	print("sum:", values[(i+1000) % len(values)] + values[(i+2000) % len(values)] + values[(i+3000) % len(values)])


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