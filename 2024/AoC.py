class Vector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	
	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y)

	def __mul__(self, scalar):
		return Vector(self.x * scalar, self.y * scalar)

	def __rmul__(self, scalar):
		return Vector(self.x * scalar, self.y * scalar)
	
	def __str__(self):
		return "({0},{1})".format(self.x, self.y)

	def __invert__(self):
		return Vector(-self.x, -self.y)
	
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __lt__(self, other):
		return (self.x, self.y) < (other.x, other.y)

	def __repr__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"
	
	def __hash__(self):
		return hash(self.x) + hash(self.y)

	# Clips against bmin (inclusive) and bmax (exclusive)
	def clip(self, bmin, bmax):  
		clipped = False
		if self.x < bmin.x:
			self.x = bmin.x
			clipped = True
		if self.x >= bmax.x:
			self.x = bmax.x-1
			clipped = True
		if self.y < bmin.y:
			self.y = bmin.y
			clipped = True
		if self.y >= bmax.y:
			self.y = bmax.y-1
			clipped = True
		return clipped

	# Tests against bmin (inclusive) and bmax (exclusive)
	def is_inside(self, bmin, bmax):
		return self.x >= bmin.x and self.x < bmax.x and self.y >= bmin.y and self.y < bmax.y

	def from_list(list):
		return Vector(list[0], list[1])

	def neighbours(self, points, bmin=None, bmax=None):
		neigh = []
		for a in points:
			n = self+a
			if bmin and bmax:
				if self.clip(bmin, bmax):
					neigh.append(n)
			else:
				neigh.append(n)
		return neigh


ADJ_4 = [Vector(0, 1), Vector(0, -1), Vector(1, 0), Vector(-1, 0)]
ADJ_DIAGS = [Vector(1, 1), Vector(1, -1), Vector(-1, 1), Vector(-1, -1)]
ADJ_8 = ADJ_4 + ADJ_DIAGS
