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
    input_stream = read_input_stream("AoC_8_input.txt")
    main_1(input_stream)
    print
    main_2(input_stream)


'''
'''