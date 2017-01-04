import sys
import re

def print_screen(buf):
    txt = ""
    for i in xrange(0, len(buf)):
        if i % 50 == 0:
            print txt
            txt = ""
        txt += buf[i]
    print txt

def set_rect(buf, w, h):
    for y in xrange(0, h):
        for x in xrange(0, w):
            buf[50*y + x] = "#"

def rotate_row(buf, r, offset):
    line = buf[50*r:50*(r+1)]
    newline = line[-offset:] + line[:-offset]
    for i in xrange(0, 50):
        buf[50*r + i] = newline[i]

def rotate_column(buf, c, offset):
    col = buf[c : 50*6+c : 50]
    print col
    newcol = col[-offset:] + col[:-offset]
    print newcol
    for i in xrange(0, 6):
        buf[c + 50*i] = newcol[i]

def read_input_stream(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream

def main_1(input_stream):
    buffer = [ " " for i in xrange(0, 50*6) ]
    for cmd in input_stream:
        if "rect" in cmd:
            size = map(lambda x: int(x), re.match("rect ([0-9]*)x([0-9]*)", cmd).groups() )
            set_rect(buffer, size[0], size[1])
        else:
            params = re.match("rotate (.*) (?:x|y)=([0-9]*) by ([0-9]*)", cmd).groups()
            if params[0] == "row":
                rotate_row(buffer, int(params[1]), int(params[2]))
            else:
                rotate_column(buffer, int(params[1]), int(params[2]))
        print_screen(buffer)
        
    count = 0
    for c in buffer:
        if c == "#":
            count += 1

    print count
            

def main_2(input_stream):
    pass

if __name__ == "__main__":
    input_stream = read_input_stream("AoC_08_input.txt")
    main_1(input_stream)
    print
    main_2(input_stream)


'''
--- Day 8: Two-Factor Authentication ---

You come across a door implementing what you can only assume is an implementation of two-factor authentication after a long game of requirements telephone.

To get past the door, you first swipe a keycard (no problem; there was one on a nearby desk). Then, it displays a code on a little screen, and you type that code on a keypad. Then, presumably, the door unlocks.

Unfortunately, the screen has been smashed. After a few minutes, you've taken everything apart and figured out how it works. Now you just have to work out what the screen would have displayed.

The magnetic strip on the card you swiped encodes a series of instructions for the screen; these instructions are your puzzle input. The screen is 50 pixels wide and 6 pixels tall, all of which start off, and is capable of three somewhat peculiar operations:

    rect AxB turns on all of the pixels in a rectangle at the top-left of the screen which is A wide and B tall.
    rotate row y=A by B shifts all of the pixels in row A (0 is the top row) right by B pixels. Pixels that would fall off the right end appear at the left end of the row.
    rotate column x=A by B shifts all of the pixels in column A (0 is the left column) down by B pixels. Pixels that would fall off the bottom appear at the top of the column.

For example, here is a simple sequence on a smaller screen:

    rect 3x2 creates a small rectangle in the top-left corner:

    ###....
    ###....
    .......

    rotate column x=1 by 1 rotates the second column down by one pixel:

    #.#....
    ###....
    .#.....

    rotate row y=0 by 4 rotates the top row right by four pixels:

    ....#.#
    ###....
    .#.....

    rotate column x=1 by 1 again rotates the second column down by one pixel, causing the bottom pixel to wrap back to the top:

    .#..#.#
    #.#....
    .#.....

As you can see, this display technology is extremely powerful, and will soon dominate the tiny-code-displaying-screen market. That's what the advertisement on the back of the display tries to convince you, anyway.

There seems to be an intermediate check of the voltage used by the display: after you swipe your card, if the screen did work, how many pixels should be lit?

Your puzzle answer was 128.
--- Part Two ---

You notice that the screen is only capable of displaying capital letters; in the font it uses, each letter is 5 pixels wide and 6 tall.

After you swipe your card, what code is the screen trying to display?

Your puzzle answer was EOARGPHYAO.
'''