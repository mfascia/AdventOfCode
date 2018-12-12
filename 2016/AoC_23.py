import sys


sourcecode = '''cpy a b
dec b
cpy a d
cpy 0 a
cpy b c
inc a
dec c
jnz c -2
dec d
jnz d -5
dec b
cpy b c
cpy c d
dec d
inc c
jnz d -2
tgl c
cpy -16 c
jnz 1 c
cpy 83 c
jnz 78 d
inc a
inc d
jnz d -2
inc c
jnz c -5'''


def main(src, initial_a):
	regs = {
		"pc": 0,
		"a": initial_a,
		"b": 0,
		"c": 0,
		"d": 0
	}

	code = src.split("\n")

	while regs["pc"] < len(code):
		old = regs["d"]

		line = code[regs["pc"]]
		tokens = line.split(" ")

		if tokens[0] == "inc":
			regs[tokens[1]] += 1

		elif tokens[0] == "dec":
			regs[tokens[1]] -= 1
			
		elif tokens[0] == "jnz":
			comp = 0
			if tokens[1].lstrip("-").isdigit():
				comp = int(tokens[1])
			else:
				comp = regs[tokens[1]] 
			if comp != 0:
				offset = 0
				if tokens[2].lstrip("-").isdigit():
					offset = int(tokens[2])
				else:
					offset = regs[tokens[2]] 

				regs["pc"] += offset - 1

		elif tokens[0] == "cpy":
			if not tokens[2].lstrip("-").isdigit():
				if tokens[1].lstrip("-").isdigit():
					regs[tokens[2]] = int(tokens[1])
				else:
					regs[tokens[2]] = regs[tokens[1]]

		elif tokens[0] == "tgl":
			target_address = regs["pc"]
			if tokens[1].lstrip("-").isdigit():
				target_address += int(tokens[1])
			else:
				target_address += regs[tokens[1]]

			if target_address < len(code):
				target_code = code[target_address]
				target_tokens = target_code.split(" ")
				newline = ""
				if len(target_tokens) == 2:
					if "inc" in target_code:
						newline = "dec" + " " + target_tokens[1]
					else:
						newline = "inc" + " " + target_tokens[1]
				elif len(target_tokens) == 3:
					if "jnz" in target_code:
						newline = "cpy" + " " + target_tokens[1] + " " + target_tokens[2]
					else:
						newline = "jnz" + " " + target_tokens[1] + " " + target_tokens[2]
				code = code[:target_address] + [newline] + code[target_address+1:]

		regs["pc"] += 1
		
		# to help with part 2, dump the registers whenever register d resets
		if old < regs["d"]:
			print old, regs

	print regs


# looking at the output for n=6, 7 and 8 (see AoC_23_output.txt)
# It turns out that the program is computing the following for the input value n:
#  n! + (94 * 82)
## UPDATED
#  n! + (83 * 78)

def fast_part2(n):
	r = 2
	for i in xrange(3, n+1):
		r = r*i
	r += 83 * 78

	return r


if __name__ == "__main__":
	print ("Part 1 ---------------------------------------------------------------------------------------------------------")
	main(sourcecode, 7)

	print

	print ("Part 2 ---------------------------------------------------------------------------------------------------------")
	# generate output for lower n in order to deduce the formula    
	main(sourcecode, 6)
	#print
	#main(sourcecode, 7)
	#print
	#main(sourcecode, 8)

	print fast_part2(12)


'''
--- Day 23: Safe Cracking ---

This is one of the top floors of the nicest tower in EBHQ. The Easter Bunny's private office is here, complete with a safe hidden behind a painting, and who wouldn't hide a star in a safe behind a painting?

The safe has a digital screen and keypad for code entry. A sticky note attached to the safe has a password hint on it: "eggs". The painting is of a large rabbit coloring some eggs. You see 7.

When you go to type the code, though, nothing appears on the display; instead, the keypad comes apart in your hands, apparently having been smashed. Behind it is some kind of socket - one that matches a connector in your prototype computer! You pull apart the smashed keypad and extract the logic circuit, plug it into your computer, and plug your computer into the safe.

Now, you just need to figure out what output the keypad would have sent to the safe. You extract the assembunny code from the logic chip (your puzzle input).

The code looks like it uses almost the same architecture and instruction set that the monorail computer used! You should be able to use the same assembunny interpreter for this as you did there, but with one new instruction:

tgl x toggles the instruction x away (pointing at instructions like jnz does: positive means forward; negative means backward):

	For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
	For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
	The arguments of a toggled instruction are not affected.
	If an attempt is made to toggle an instruction outside the program, nothing happens.
	If toggling produces an invalid instruction (like cpy 1 2) and an attempt is later made to execute that instruction, skip it instead.
	If tgl toggles itself (for example, if a is 0, tgl a would target itself and become inc a), the resulting instruction is not executed until the next time it is reached.

For example, given this program:

cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a

	cpy 2 a initializes register a to 2.
	The first tgl a toggles an instruction a (2) away from it, which changes the third tgl a into inc a.
	The second tgl a also modifies an instruction 2 away from it, which changes the cpy 1 a into jnz 1 a.
	The fourth line, which is now inc a, increments a to 3.
	Finally, the fifth line, which is now jnz 1 a, jumps a (3) instructions ahead, skipping the dec a instructions.

In this example, the final value in register a is 3.

The rest of the electronics seem to place the keypad entry (the number of eggs, 7) in register a, run the code, and then send the value left in register a to the safe.

What value should be sent to the safe?

Your puzzle answer was 12748.
--- Part Two ---

The safe doesn't open, but it does make several angry noises to express its frustration.

You're quite sure your logic is working correctly, so the only other thing is... you check the painting again. As it turns out, colored eggs are still eggs. Now you count 12.

As you run the program with this new input, the prototype computer begins to overheat. You wonder what's taking so long, and whether the lack of any instruction more powerful than "add one" has anything to do with it. Don't bunnies usually multiply?

Anyway, what value should actually be sent to the safe?

Your puzzle answer was 479009308.
'''