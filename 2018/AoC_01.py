import sys


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream


def main_1(text):
	freq = 0
	for line in text:
		freq += int(line)

	print freq



def main_2(text):
	freq = 0
	history = {}

	while True:
		for line in text:
			freq += int(line)
			if history.has_key(freq):
				print freq
				return
			else:
				history[freq] = 1


if __name__ == "__main__":
	in_text = read_input(sys.argv[0].replace(".py", "_input.txt"))

	print ("Part 1 ---------------------------------------------------------------------------------------------------------")
	main_1(in_text)

	print 

	print ("Part 2 ---------------------------------------------------------------------------------------------------------")
	main_2(in_text)
