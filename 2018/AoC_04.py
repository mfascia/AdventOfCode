import sys
import re
from datetime import datetime
from datetime import timedelta


AWAKE = -1
SLEEP = -2


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream


def process_input(text):
	data = []
	for line in text:
		timestamp = line[:18]
		d = datetime.strptime(timestamp[1:-1], "%Y-%m-%d %H:%M")
		# clamp each day event in the [00:00, 01:00[ interval]
		if d.hour > 12:
			# evening event gets pushed to 00:00 of the next day
			d = d + timedelta(days=1)
			d = d.replace(hour=0, minute=0)
		elif d.hour > 0 and d.hour < 12:
			# morning event gets pushed back to 01:00 of same day
			d = d.replace(hour=1, minute=0)

		words = line[19:].split(" ")
		if words[0] == "Guard":
			data.append([d, int(words[1][1:])])
		elif words[0] == "falls":
			data.append([d, SLEEP])
		if words[0] == "wakes":
			data.append([d, AWAKE])
	
	data.sort(key=lambda x: x[0])
	return data


def mark_interval(interval, start, end, val):
	for t in xrange(start, end):
		interval[t] = val


def main(data):

	guards = {}
	for d in data:
		if d[1] >= 0 and not guards.has_key(d[1]):
			guards[d[1]] = {}
	
	currData = None
	currGuardId = 0
	sleeptime = 0
	waketime = 0

	for d in data:
		if d[1] >= 0:
			if waketime == -1 and sleeptime >= 0:
				mark_interval(currData, sleeptime, 60, "#")

			currGuardId = d[1]
			currData = ["." for x in xrange(0, 60)]
			guards[currGuardId][d[0]] = currData

		elif d[1] == SLEEP:
			sleeptime = d[0].minute

		elif d[1] == AWAKE:
			waketime = d[0].minute
			mark_interval(currData, sleeptime, waketime, "#")


	for i, entries in guards.items():
		print "Guard #" + str(i)
		sleep = [0 for x in xrange(0, 60)]
		for d, s in entries.items():
			print "  [" + format(d.year, "04d") + "-" + format(d.month, "02d") + "-" + format(d.day, "02d") + "]: " + "".join(s)
		print sleep

	print
	print ("Part 1 ---------------------------------------------------------------------------------------------------------")

	sleepiest_id = -1
	sleepiest_min = -1
	sleepiest_val = -1

	for i, entries in guards.items():
		sleep = [0 for x in xrange(0, 60)]
		for d, s in entries.items():
			for m in xrange(0, 60):
				if s[m] == "#":
					sleep[m] += 1
					if sleep[m] > sleepiest_val:
						sleepiest_val = sleep[m]
						sleepiest_min = m
						sleepiest_id = i

	print sleepiest_id, sleepiest_min, sleepiest_val
	print sleepiest_id * sleepiest_min

	print
	print ("Part 2 ---------------------------------------------------------------------------------------------------------")
	
	sleepiest_id = -1
	sleepiest_min = -1
	sleepiest_sleeptotal = 0

	for i, entries in guards.items():
		sleep = [0 for x in xrange(0, 60)]
		sleeptotal = 0
		for d, s in entries.items():
			for m in xrange(0, 60):
				if s[m] == "#":
					sleep[m] += 1
					sleeptotal += 1

		if sleeptotal > sleepiest_sleeptotal:
			sleepiest_id = i
			sleepiest_sleeptotal = sleeptotal

			sleepiest_val = 0
			for m in xrange(0, 60):
				if sleep[m] > sleepiest_val:
					sleepiest_min = m
					sleepiest_val = sleep[m]
	
	print sleepiest_id, sleepiest_min, sleepiest_val
	print sleepiest_id * sleepiest_min


if __name__ == "__main__":
	print ("--------------------------------------------------------------------------------------------------------------")
	print ("TEST ---------------------------------------------------------------------------------------------------------")
	print ("--------------------------------------------------------------------------------------------------------------")
	in_text = read_input(sys.argv[0].replace(".py", "_test.txt"))
	sortedData = process_input(in_text)
	main(sortedData)

	print 
	print ("--------------------------------------------------------------------------------------------------------------")
	print ("REAL ---------------------------------------------------------------------------------------------------------")
	print ("--------------------------------------------------------------------------------------------------------------")
	in_text = read_input(sys.argv[0].replace(".py", "_input.txt"))
	sortedData = process_input(in_text)
	main(sortedData)

