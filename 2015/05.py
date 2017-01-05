import sys
import itertools
import re


def read_input(filename):
    with open(filename, "r") as f:
        raw = f.readlines()
    stream = map(lambda x: x.strip(" \n\t"), raw)
    return stream


def main_1(text):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    doubles = [x+x for x in alphabet]
    print doubles
    vowels = "aeiou"
    nice_strings = []
    for line in text:
        if "ab" in line or "cd" in line or "pq" in line or "xy" in line:
            continue
        
        vows = 0
        for v in vowels:
            vows += line.count(v)
            if vows > 2:
                break
        if vows < 3:
            continue

        found_double = False
        for d in doubles:
            if d in line:
                found_double = True
                break
        if not found_double:
            continue

        nice_strings.append(line)
    
    print len(nice_strings)


def main_2(text):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    digraphs = ["".join(x) for x in itertools.product(alphabet, alphabet)]
    trigraphs = [x + "." + x for x in alphabet]
    print digraphs
    print trigraphs

    nice_strings = []

    for line in text:
        found = False
        for t in trigraphs:
            matches = [x.start() for x in re.finditer(t, line)]
            if len(matches) > 0:
                for d in digraphs:
                    matches = [x.start() for x in re.finditer(d, line)]
                    if len(matches) > 1:
                        print line
                        nice_strings.append(line)
                        found = True
                    if found:
                        break
            if found:
                break

    print len(nice_strings)


if __name__ == "__main__":
	in_text = read_input("2015/05_in.txt")

	print ("Part 1 ---------------------------------------------------------------------------------------------------------")
	main_1(in_text)

	print 

	print ("Part 2 ---------------------------------------------------------------------------------------------------------")
	main_2(in_text)


"""
--- Day 5: Doesn't He Have Intern-Elves For This? ---

Santa needs help figuring out which strings in his text file are naughty or nice.

A nice string is one with all of the following properties:

    It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.

For example:

    ugknbfddgicrmopn is nice because it has at least three vowels (u...i...o...), a double letter (...dd...), and none of the disallowed substrings.
    aaa is nice because it has at least three vowels and a double letter, even though the letters used by different rules overlap.
    jchzalrnumimnmhp is naughty because it has no double letter.
    haegwjzuvuyypxyu is naughty because it contains the string xy.
    dvszwmarrgswjxmb is naughty because it contains only one vowel.

How many strings are nice?

Your puzzle answer was 258.
--- Part Two ---

Realizing the error of his ways, Santa has switched to a better model of determining whether a string is naughty or nice. None of the old rules apply, as they are all clearly ridiculous.

Now, a nice string is one with all of the following properties:

    It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.

For example:

    qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and a letter that repeats with exactly one letter between them (zxz).
    xxyxx is nice because it has a pair that appears twice and a letter that repeats with one between, even though the letters used by each rule overlap.
    uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a single letter between them.
    ieodomkazucvgmuy is naughty because it has a repeating letter with one between (odo), but no pair that appears twice.

How many strings are nice under these new rules?

Your puzzle answer was 53.
"""