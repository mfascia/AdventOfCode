import os
import sys


def run_code(input, code):
	pc = 0
	i = 0

	registers = {
		"w": 0,
		"x": 0,
		"y": 0,
		"z": 0
	}

	while pc < len(code):
		line = code[pc]

		if line.startswith("inp"):
			instr, a = line.split(" ")
		else:
			instr, a, b = line.split(" ")
			if b in "wxyz":
				v = registers[b]
			else:
				v = int(b)
		
		if instr == "inp":
			if i<len(input):
				registers[a] = int(input[i])
				i += 1
				print(registers)
			else:
				print(registers)
				break

		elif instr == "add":
			registers[a] = registers[a] + v

		elif instr == "mul":
			registers[a] = registers[a] * v

		elif instr == "div":
			if v != 0:
				registers[a] = int(registers[a] / v)

		elif instr == "mod":
			if v != 0 and registers[a] != 0:
				registers[a] = registers[a] % v

		elif instr == "eql":
			registers[a] = 1 if registers[a] == v else 0

		pc += 1


# Looking at the assembly code for the ALU, it turs out it performs the following for each of the 14 digits:
# 	next_Z = prev_Z div AAA
# 	if (prev_Z mod 26) + BBB != input_digit:
#		next_Z = next_Z * 26 + input_digit + CCC
#
# Here are the manually extracted parameters
AAA = [1, 1, 1, 1, 26, 1, 1, 26, 1, 26, 26, 26, 26, 26]
BBB = [12, 12, 13, 12, -3, 10, 14, -16, 12, -8, -12, -7, -6, -11]
CCC = [7, 8, 2, 11, 6, 12, 14, 13, 15, 10, 6, 10, 8, 5]


def run_model(comp):
	prevZ = {0: 0}
	for digit in range(0, 14):
		print("Digit", digit, "# prevZ values:", len(prevZ))
		nextZ = {}
		a = AAA[digit]
		b = BBB[digit]
		c = CCC[digit]
		for pZ, pSerial in prevZ.items():
			for v in range(1, 10):
				nSerial = pSerial * 10 + v
				nZ = int(pZ / a)
				if ((pZ % 26) + b) != v:
					nZ = nZ * 26 + v + c
				if nZ in nextZ:
					nextZ[nZ] = comp(nextZ[nZ], nSerial)
				else:
					nextZ[nZ] = nSerial
		prevZ = nextZ

	print(prevZ[0])		


if __name__ == "__main__":
	print("Searching for MAX valid serial:")
	run_model(max)
	print("")
	print("Searching for MIN valid serial:")
	run_model(min)