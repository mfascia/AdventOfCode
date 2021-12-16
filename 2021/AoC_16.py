import os
import sys


# GLOBALS --------------------------------------------------------------------------------------

# for short input sets, it can be declared here instead of in seperate files
# otherwise, tests go in files named AoC_xx_test_x.txt and input goes in AoC_xx_input.txt
tests = [
	"D2FE28",
	"38006F45291200",
	"EE00D40C823060",
	"8A004A801A8002F478",
	"620080001611562C8802118E34",
	"C0015000016115A2E0802F182340",
	"A0016C880162017C3686B18A3D4780",
	"C200B40A82",
	"04005AC33890",
	"880086C3E88112",
	"CE00C43D881120",
	"D8005AC2A8F0",
	"F600BC2D8F",
	"9C005AC2F8F0",
	"9C0141080250320F1802104A08",
]

inp = "020D708041258C0B4C683E61F674A1401595CC3DE669AC4FB7BEFEE840182CDF033401296F44367F938371802D2CC9801A980021304609C431007239C2C860400F7C36B005E446A44662A2805925FF96CBCE0033C5736D13D9CFCDC001C89BF57505799C0D1802D2639801A900021105A3A43C1007A1EC368A72D86130057401782F25B9054B94B003013EDF34133218A00D4A6F1985624B331FE359C354F7EB64A8524027D4DEB785CA00D540010D8E9132270803F1CA1D416200FDAC01697DCEB43D9DC5F6B7239CCA7557200986C013912598FF0BE4DFCC012C0091E7EFFA6E44123CE74624FBA01001328C01C8FF06E0A9803D1FA3343E3007A1641684C600B47DE009024ED7DD9564ED7DD940C017A00AF26654F76B5C62C65295B1B4ED8C1804DD979E2B13A97029CFCB3F1F96F28CE43318560F8400E2CAA5D80270FA1C90099D3D41BE00DD00010B893132108002131662342D91AFCA6330001073EA2E0054BC098804B5C00CC667B79727FF646267FA9E3971C96E71E8C00D911A9C738EC401A6CBEA33BC09B8015697BB7CD746E4A9FD4BB5613004BC01598EEE96EF755149B9A049D80480230C0041E514A51467D226E692801F049F73287F7AC29CB453E4B1FDE1F624100203368B3670200C46E93D13CAD11A6673B63A42600C00021119E304271006A30C3B844200E45F8A306C8037C9CA6FF850B004A459672B5C4E66A80090CC4F31E1D80193E60068801EC056498012804C58011BEC0414A00EF46005880162006800A3460073007B620070801E801073002B2C0055CEE9BC801DC9F5B913587D2C90600E4D93CE1A4DB51007E7399B066802339EEC65F519CF7632FAB900A45398C4A45B401AB8803506A2E4300004262AC13866401434D984CA4490ACA81CC0FB008B93764F9A8AE4F7ABED6B293330D46B7969998021C9EEF67C97BAC122822017C1C9FA0745B930D9C480"
isTest = False

doTests = True
doInput = True
#-----------------------------------------------------------------------------------------------


INDENT = "  "

class Packet:
	def __init__(self, parent=None, hex="", bin=""):
		self.hex = hex
		self.bin = bin
		self.version = -1
		self.type = -1
		self.subLen = -1
		self.subCount = -1
		self.nested = -1
		self.subs = []
		self.value = -1
		self.consumed = -1

		if len(hex) > 0:
			self.bin = ""
			for h in hex:
				self.bin += format(int(h, 16), "#06b")[2:]

		if parent:
			self.nested = parent.nested + 1
		else:
			self.nested = 0

		if sum([int(x) for x in self.bin]) == 0:
			self.consumed = len(self.bin)
			return

		self.version = int(self.bin[0:3], 2)
		self.type = int(self.bin[3:6], 2)
		self.consumed = 6

		if self.type == 0:
			self.decode_subs()
			self.value = 0
			for s in self.subs:
				self.value += s.value

		elif self.type == 1:
			self.decode_subs()
			self.value = 1
			for s in self.subs:
				self.value *= s.value

		elif self.type == 2:
			self.decode_subs()
			self.value = min([x.value for x in self.subs])

		elif self.type == 3:
			self.decode_subs()
			self.value = max([x.value for x in self.subs])

		elif self.type == 4:
			self.decode_imediate_value()

		elif self.type == 5:
			self.decode_subs()
			if self.subs[0].value > self.subs[1].value:
				self.value = 1
			else:
				self.value = 0

		elif self.type == 6:
			self.decode_subs()
			if self.subs[0].value < self.subs[1].value:
				self.value = 1
			else:
				self.value = 0

		elif self.type == 7:
			self.decode_subs()
			if self.subs[0].value == self.subs[1].value:
				self.value = 1
			else:
				self.value = 0

		else:
			print("Unknown packet type:", self.type )


	def decode_imediate_value(self):
		loop = True
		value = ""
		while loop:
			block = self.bin[self.consumed:self.consumed+5]
			loop = block[0] == "1"
			value += block[1:]
			self.consumed += 5
		self.value = int(value, 2)


	def decode_subs(self):
		if self.bin[self.consumed] == "0":
			self.consumed += 1
			self.subLen = int(self.bin[self.consumed:self.consumed+15], 2)
			self.consumed += 15
			end = self.consumed + self.subLen
			while self.consumed < end:
				sub = Packet(parent=self, bin=self.bin[self.consumed:])
				self.consumed += sub.consumed
				if sub.type != -1:
				 	self.subs.append(sub)
		else:
			self.consumed += 1
			self.subCount = int(self.bin[self.consumed:self.consumed+11], 2)
			self.consumed += 11
			for s in range(0, self.subCount):
				sub = Packet(parent=self, bin=self.bin[self.consumed:])
				self.consumed += sub.consumed
				if sub.type != -1:
					self.subs.append(sub)


	def __str__(self):
		if isTest:
			d = "".join([INDENT for x in range(0, self.nested)]) + f"< version={self.version}, type={self.type}, value={self.value}, subLen={self.subLen}, subCount={self.subCount}, nested={self.nested}, hex={self.hex}, bin={self.bin} >"
		else:
			d = "".join([INDENT for x in range(0, self.nested)]) + f"< version={self.version}, type={self.type}, value={self.value}, subLen={self.subLen}, subCount={self.subCount}, nested={self.nested} >"
		for s in self.subs:
			d += "\n" + s.__str__()
		return d



def main(inp):
	outer = Packet(hex=inp)
	sumVer = 0
	packets = [outer]
	while packets:
		p = packets.pop()
		packets += p.subs
		sumVer += p.version

	#print(outer)

	print("checksum:", sumVer)
	print("value:", outer.value)



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