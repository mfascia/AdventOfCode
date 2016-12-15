import sys
import re

sourcecode = '''
cpy 1 a
cpy 1 b
cpy 26 d
jnz c 2
jnz 1 5
cpy 7 c
inc d
dec c
jnz c -2
cpy a c
inc a
dec b
jnz b -2
cpy c b
dec d
jnz d -6
cpy 17 c
cpy 18 d
inc a
dec d
jnz d -2
dec c
jnz c -5
'''

def main(src, initial_c):
    regs = {
        "pc": 0,
        "a": 0,
        "b": 0,
        "c": initial_c,
        "d": 0
    }

    code = src.split("\n")

    while regs["pc"] < len(code):
        line = code[regs["pc"]]
        tokens = line.split(" ")

        if tokens[0] == "inc":
            #print regs, "INC", tokens[1]
            regs[tokens[1]] += 1

        elif tokens[0] == "dec":
            #print regs, "DEC", tokens[1]
            regs[tokens[1]] -= 1
            
        elif tokens[0] == "jnz":
            #print regs, "JNZ", tokens[1], "OFFSET", tokens[2]
            comp = 0
            if tokens[1].isdigit():
                comp = int(tokens[1])
            else:
                comp = regs[tokens[1]] 
            if comp != 0:
                regs["pc"] += int(tokens[2]) - 1

        elif tokens[0] == "cpy":
            print regs, "CPY", tokens[1], "in", tokens[2]
            if tokens[1].isdigit():
                regs[tokens[2]] = int(tokens[1])
            else:
                regs[tokens[2]] = regs[tokens[1]]

        regs["pc"] += 1
        
    print regs



if __name__ == "__main__":
    #main(sourcecode, 0)
    print
    main(sourcecode, 1)
    

'''
--- Day 12: Leonardo's Monorail ---

You finally reach the top floor of this building: a garden with a slanted glass ceiling. Looks like there are no more stars to be had.

While sitting on a nearby bench amidst some tiger lilies, you manage to decrypt some of the files you extracted from the servers downstairs.

According to these documents, Easter Bunny HQ isn't just this building - it's a collection of buildings in the nearby area. They're all connected by a local monorail, and there's another building not far from here! Unfortunately, being night, the monorail is currently not operating.

You remotely connect to the monorail control systems and discover that the boot sequence expects a password. The password-checking logic (your puzzle input) is easy to extract, but the code it uses is strange: it's assembunny code designed for the new computer you just assembled. You'll have to execute the code and get the password.

The assembunny code you've extracted operates on four registers (a, b, c, and d) that start at 0 and can hold any integer. However, it seems to make use of only a few instructions:

    cpy x y copies x (either an integer or the value of a register) into register y.
    inc x increases the value of register x by one.
    dec x decreases the value of register x by one.
    jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.

The jnz instruction moves relative to itself: an offset of -1 would continue at the previous instruction, while an offset of 2 would skip over the next instruction.

For example:

cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a

The above code would set register a to 41, increase its value by 2, decrease its value by 1, and then skip the last dec a (because a is not zero, so the jnz a 2 skips it), leaving register a at 42. When you move past the last instruction, the program halts.

After executing the assembunny code in your puzzle input, what value is left in register a?

Your puzzle answer was 318117.
--- Part Two ---

As you head down the fire escape to the monorail, you notice it didn't start; register c needs to be initialized to the position of the ignition key.

If you instead initialize register c to be 1, what value is now left in register a?

Your puzzle answer was 9227771.
'''