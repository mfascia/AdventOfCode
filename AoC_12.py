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
    