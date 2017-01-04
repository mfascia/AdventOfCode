import sys


def read_input(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


def main_1(text):
    pass


def main_2(text):
    pass


if __name__ == "__main__":
	in_text = read_input()

	print ("Part 1 ---------------------------------------------------------------------------------------------------------")
	main_1(in_text)

	print 

	print ("Part 2 ---------------------------------------------------------------------------------------------------------")
	main_2(in_text)
