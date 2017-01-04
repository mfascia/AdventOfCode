import sys


sourcecode = '''cpy a d
cpy 7 c
cpy 362 b
inc d
dec b
jnz b -2
dec c
jnz c -5
cpy d a
jnz 0 0
cpy a b
cpy 0 a
cpy 2 c
jnz b 2
jnz 1 6
dec b
dec c
jnz c -4
inc a
jnz 1 -7
cpy 2 b
jnz c 2
jnz 1 4
dec b
dec c
jnz 1 -4
jnz 0 0
out b
jnz a -19
jnz 1 -21'''


def execute(src, init_a = 0):
	regs = {
		"pc": 0,
		"a": init_a,
		"b": 0,
		"c": 0,
		"d": 0
	}

	code = src.split("\n")

	while regs["pc"] < len(code):
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
		
		elif tokens[0] == "out":
			if tokens[1].lstrip("-").isdigit():
				print tokens[1]
			else:
				print regs[tokens[1]]
			#print regs

		regs["pc"] += 1
		


# The code calculates a value v = a + (7*362) and then integer-divides it by 2 up to 0
# at each division step, it outputs 1 if the current v is even, 0 if it is odd
# This is the sequence of nuber we need as it produces alternanting "doubles" that will alternate between odd and even:
# 	0 1 2 5 10 21 42 85 170 341 682 1365 2730 5461 10922 ...
# We need to start on an the smallest even number greater than 7*362=2534
# 	--> 2730
# Therefore register a should contain 2730 - (7*362) = 196

if __name__ == "__main__":
	print ("Part 1 ---------------------------------------------------------------------------------------------------------")
	a = 196
	print "a = " + str(a)
	execute(sourcecode, a)


'''
--- Day 25: Clock Signal ---

You open the door and find yourself on the roof. The city sprawls away from you for miles and miles.

There's not much time now - it's already Christmas, but you're nowhere near the North Pole, much too far to deliver these stars to the sleigh in time.

However, maybe the huge antenna up here can offer a solution. After all, the sleigh doesn't need the stars, exactly; it needs the timing data they provide, and you happen to have a massive signal generator right here.

You connect the stars you have to your prototype computer, connect that to the antenna, and begin the transmission.

Nothing happens.

You call the service number printed on the side of the antenna and quickly explain the situation. "I'm not sure what kind of equipment you have connected over there," he says, "but you need a clock signal." You try to explain that this is a signal for a clock.

"No, no, a clock signal - timing information so the antenna computer knows how to read the data you're sending it. An endless, alternating pattern of 0, 1, 0, 1, 0, 1, 0, 1, 0, 1...." He trails off.

You ask if the antenna can handle a clock signal at the frequency you would need to use for the data from the stars. "There's no way it can! The only antenna we've installed capable of that is on top of a top-secret Easter Bunny installation, and you're definitely not-" You hang up the phone.

You've extracted the antenna's clock signal generation assembunny code (your puzzle input); it looks mostly compatible with code you worked on just recently.

This antenna code, being a signal generator, uses one extra instruction:

    out x transmits x (either an integer or the value of a register) as the next value for the clock signal.

The code takes a value (via register a) that describes the signal to generate, but you're not sure how it's used. You'll have to find the input to produce the right signal through experimentation.

What is the lowest positive integer that can be used to initialize register a and cause the code to output a clock signal of 0, 1, 0, 1... repeating forever?

Your puzzle answer was 196.
--- Part Two ---

The antenna is ready. Now, all you need is the fifty stars required to generate the signal for the sleigh, but you don't have enough.

You look toward the sky in desperation... suddenly noticing that a lone star has been installed at the top of the antenna! Only 49 more to go.
'''