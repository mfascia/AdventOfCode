import sys
import re


in_1 = "abcdefgh"
in_2 = "fbgdceah"


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream


def main_1(pwd, text):
	print pwd
	print "-->"

	ct = pwd
	for line in text:
		if "swap" in line:
			if "position" in line:
				p = [int(x) for x in re.match("swap position ([0-9]*) with position ([0-9]*)", line).groups()]
				p.sort()
				ct = ct[:p[0]] + ct[p[1]] + ct[p[0]+1:p[1]] + ct[p[0]] + ct[p[1]+1:]
			elif "letter" in line:
				p = re.match("swap letter ([a-z]*) with letter ([a-z]*)", line).groups()
				ct = ct.replace(p[0], "#")
				ct = ct.replace(p[1], p[0])
				ct = ct.replace("#", p[1])
		elif "move" in line:
			p = [int(x) for x in re.match("move position ([0-9]*) to position ([0-9]*)", line).groups()]
			if p[0] < p[1]:
				ct = ct[:p[0]] + ct[p[0]+1:p[1]+1] + ct[p[0]] + ct[p[1]+1:]
			else:
				ct = ct[:p[1]] + ct[p[0]] + ct[p[1]:p[0]] + ct[p[0]+1:]
		elif "reverse" in line:
			p = [int(x) for x in re.match("reverse positions ([0-9]*) through ([0-9]*)", line).groups()]
			p.sort()
			ct = ct[:p[0]] + (ct[p[1]:p[0]-1:-1] if p[0] > 0 else ct[p[1]::-1]) + ct[p[1]+1:]
		elif "rotate" in line:
			if "based" in line:
				p = re.match("rotate based on position of letter ([a-z]*)", line).groups()
				pos = ct.find(p[0])
				pos += 2 if pos >= 4 else 1
				pos = pos % len(ct)
				ct = ct[-pos:] + ct[:-pos]
			elif "right" in line:
				p = [int(x) for x in re.match("rotate right ([0-9]*) steps?", line).groups()]
				ct = ct[-p[0]:] + ct[:-p[0]]
			elif "left" in line:
				p = [int(x) for x in re.match("rotate left ([0-9]*) steps?", line).groups()]
				ct = ct[p[0]:] + ct[:p[0]]
		elif line == "":
			break

	print ct


def main_2(pwd, text):
	print pwd
	print "-->"

	text = list(reversed(text))
	ct = pwd

	rot_lut = []
	for i in xrange(0, len(ct)):
		rot_lut.append((2 * i + (1 if i<4 else 2)) % len (ct))

	for line in text:
		if "swap" in line:
			if "position" in line:
				p = [int(x) for x in re.match("swap position ([0-9]*) with position ([0-9]*)", line).groups()]
				p.sort()
				ct = ct[:p[0]] + ct[p[1]] + ct[p[0]+1:p[1]] + ct[p[0]] + ct[p[1]+1:]
			elif "letter" in line:
				p = re.match("swap letter ([a-z]*) with letter ([a-z]*)", line).groups()
				ct = ct.replace(p[0], "#")
				ct = ct.replace(p[1], p[0])
				ct = ct.replace("#", p[1])
		elif "move" in line:
			p = [int(x) for x in re.match("move position ([0-9]*) to position ([0-9]*)", line).groups()]
			p = list(reversed(p))
			if p[0] < p[1]:
				ct = ct[:p[0]] + ct[p[0]+1:p[1]+1] + ct[p[0]] + ct[p[1]+1:]
			else:
				ct = ct[:p[1]] + ct[p[0]] + ct[p[1]:p[0]] + ct[p[0]+1:]
		elif "reverse" in line:
			p = [int(x) for x in re.match("reverse positions ([0-9]*) through ([0-9]*)", line).groups()]
			p.sort()
			ct = ct[:p[0]] + (ct[p[1]:p[0]-1:-1] if p[0] > 0 else ct[p[1]::-1]) + ct[p[1]+1:]
		elif "rotate" in line:
			if "based" in line:
				p = re.match("rotate based on position of letter ([a-z]*)", line).groups()
				pos = ct.find(p[0]) 
				should_be_at = rot_lut.index(pos)
				pos = (should_be_at + len(ct) - pos) % len(ct)
				ct = ct[-pos:] + ct[:-pos]
			elif "right" in line:
				p = [int(x) for x in re.match("rotate right ([0-9]*) steps?", line).groups()]
				ct = ct[p[0]:] + ct[:p[0]]
			elif "left" in line:
				p = [int(x) for x in re.match("rotate left ([0-9]*) steps?", line).groups()]
				ct = ct[-p[0]:] + ct[:-p[0]]
		elif line == "":
			break

	print ct

if __name__ == "__main__":
	text = read_input("2016\\AoC_21_input.txt")

	print ("Part 1 ---------------------------------------------------------------------------------------------------------")
	main_1(in_1, text)

	print

	print ("Part 2 ---------------------------------------------------------------------------------------------------------")
	main_2(in_2, text)


'''
--- Day 21: Scrambled Letters and Hash ---

The computer system you're breaking into uses a weird scrambling function to store its passwords. It shouldn't be much trouble to create your own scrambled password so you can add it to the system; you just have to implement the scrambler.

The scrambling function is a series of operations (the exact list is provided in your puzzle input). Starting with the password to be scrambled, apply each operation in succession to the string. The individual operations behave as follows:

    swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
    swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in the string).
    rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
    rotate based on position of letter X means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4.
    reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
    move position X to position Y means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.

For example, suppose you start with abcde and perform the following operations:

    swap position 4 with position 0 swaps the first and last letters, producing the input for the next step, ebcda.
    swap letter d with letter b swaps the positions of d and b: edcba.
    reverse positions 0 through 4 causes the entire string to be reversed, producing abcde.
    rotate left 1 step shifts all letters left one position, causing the first letter to wrap to the end of the string: bcdea.
    move position 1 to position 4 removes the letter at position 1 (c), then inserts it at position 4 (the end of the string): bdeac.
    move position 3 to position 0 removes the letter at position 3 (a), then inserts it at position 0 (the front of the string): abdec.
    rotate based on position of letter b finds the index of letter b (1), then rotates the string right once plus a number of times equal to that index (2): ecabd.
    rotate based on position of letter d finds the index of letter d (4), then rotates the string right once, plus a number of times equal to that index, plus an additional time because the index was at least 4, for a total of 6 right rotations: decab.

After these steps, the resulting scrambled password is decab.

Now, you just need to generate a new scrambled password and you can access the system. Given the list of scrambling operations in your puzzle input, what is the result of scrambling abcdefgh?

Your puzzle answer was aefgbcdh.
--- Part Two ---

You scrambled the password correctly, but you discover that you can't actually modify the password file on the system. You'll need to un-scramble one of the existing passwords by reversing the scrambling process.

What is the un-scrambled version of the scrambled password fbgdceah?

Your puzzle answer was egcdahbf.
'''