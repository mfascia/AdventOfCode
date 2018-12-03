import sys


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream


def main_1(text):
	doubles = 0
	triples = 0
	for line in text:
		d = 0
		t = 0
		alphabet = {}
		for c in line:
			if alphabet.has_key(c):
				alphabet[c] += 1
			else:
				alphabet[c] = 1
		print alphabet
		for k, v in alphabet.items():
			if v == 2:
				d += 1
			elif v == 3:
				t += 1

		if d > 0:
			doubles +=1
		if t > 0:
			triples +=1
			
	print doubles, triples
	print doubles * triples
  

def main_2(text):
	for i in xrange(0, len(text)):
		line1 = text[i]
		for j in xrange(i+1, len(text)):
			line2 = text[j]
			same = []
			diffs = 0
			for k in xrange(0, len(line1)):
				if line1[k] == line2[k]:
					same.append(line1[k])
				else: 
					diffs += 1

			if diffs == 1:
				print i, line1
				print j, line2
				print "".join(same)
				return


if __name__ == "__main__":
	in_text = read_input(sys.argv[0].replace(".py", "_input.txt"))

	print ("Part 1 ---------------------------------------------------------------------------------------------------------")
	main_1(in_text)

	print 

	print ("Part 2 ---------------------------------------------------------------------------------------------------------")
	main_2(in_text)
