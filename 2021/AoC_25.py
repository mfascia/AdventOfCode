import os
import sys
import tempfile
from PIL import Image, ImageDraw
import moviepy.video.io.ImageSequenceClip


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = []
inp = ""
isTest = False

doTests = True
doInput = True
doVideo = False
#-----------------------------------------------------------------------------------------------


def gen_image(grid, sx, sy, prefix, index):
	im = Image.new(mode="RGB", size=(sx, sy))	
	for y in range(sy):
		for x in range(sx):
			if grid[y][x] == ">":
				im.putpixel((x, y), (255, 0, 0))
			elif grid[y][x] == "v":
				im.putpixel((x, y), (0, 255, 0))
			else:
				im.putpixel((x, y), (128, 128, 255))
	im.save(prefix + "{:03d}".format(index) + ".png")


def main(inp):
	sy = len(inp)
	sx = len(inp[0])

	grid1 = [[x for x in y] for y in inp]
	grid2 = [["." for x in y] for y in inp]

	src = grid1
	dst = grid2
	
	loops = 0
	moves = 1

	if doVideo:
		base = tempfile.mkdtemp(prefix="AoC_2021_25")
		prefix = base + "\\AoC_2021_25_"
		print("Image and video here:", base)
		gen_image(src, sx, sy, prefix, loops)

	if isTest:
		print("Initial:")
		for row in src:
			print("".join(row))
		print()

	while moves > 0:
		moves = 0
		loops += 1
		if isTest:
			print("Step:", loops) 

		# east 
		if isTest:
			print("  East")
		for y in range(sy):
			x = 0
			while x<sx:
				nx = (x+1) % sx
				if src[y][x] == ">":
					if src[y][nx] == ".":
						dst[y][x] = "."
						dst[y][nx] = ">"
						x += 1
						moves += 1
					else:
						dst[y][x] = src[y][x]
				else:
					dst[y][x] = src[y][x]
				x += 1

		if isTest:
			for row in dst:
				print("".join(row))
			print()

		tmp = src
		src = dst
		dst = tmp

		# south 
		if isTest:
			print("  South")
		for x in range(sx):
			y = 0
			while y<sy:
				ny = (y+1) % sy
				if src[y][x] == "v":
					if src[ny][x] == ".":
						dst[y][x] = "."
						dst[ny][x] = "v"
						moves += 1
						y += 1
					else:
						dst[y][x] = src[y][x]
				else:
					dst[y][x] = src[y][x]
				y += 1

		if isTest:
			for row in dst:
				print("".join(row))
			print()

		if doVideo:
			gen_image(dst, sx, sy, prefix, loops)

		tmp = src
		src = dst
		dst = tmp

	if isTest:
		for row in dst:
			print("".join(row))
		print()

	print("loops:", loops) 

	if doVideo:
		fps=12
		image_files = [os.path.join(base,img)
					for img in os.listdir(base)
					if img.endswith(".png")]
		clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
		clip.write_videofile(prefix + '.mp4')


def read_input(filename):
	with open(filename, "r") as f:
		raw = f.readlines()
	stream = map(lambda x: x.strip(" \n\t"), raw)
	return stream
	

if __name__ == "__main__":
	if doTests:
		# read tests
		if len(tests) == 0:
			i = 0
			while True:
				i += 1
				testfile = sys.argv[0].replace(".py", ("_test_%d.txt" % i))
				if os.path.isfile(testfile):
					tests.append([x for x in read_input(testfile)])
				else:
					break
		
	if doInput:
		# read input
		if len(inp) == 0:
			inp = [x for x in read_input(sys.argv[0].replace(".py", "_input.txt"))]

	if doTests:
		# run tests
		isTest = True
		print ("--------------------------------------------------------------------------------")
		print ("- TESTS")
		print ("--------------------------------------------------------------------------------")
		for t in range(0, len(tests)):
			print ("--- Test #" + str(t+1) + "---------------------------------")
			main(tests[t])
			print ()

	if doInput:
		# process input
		isTest = False
		print ("--------------------------------------------------------------------------------")
		print ("- INPUT")
		print ("--------------------------------------------------------------------------------")
		main(inp)