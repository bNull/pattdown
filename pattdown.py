#!/usr/bin/python

# Prototype script to identify recurring byte patterns in a file

from struct import unpack
from os import path
from optparse import OptionParser
import operator

def findpatt(handle,fsize,psize,offset=0):
	# Read in a file handle, file size, pattern size, and offset and go find patterns.
	curpos = offset;
	pattdict = {}

	for pos in range(offset,fsize-psize):

		handle.seek(curpos)
		fmt = ">"
		fmt += "B"*psize
		pattern = flattenpatt(unpack(fmt, handle.read(psize)))
		
		if pattdict.has_key(pattern):
			pattdict[pattern] +=1
		else:
			pattdict[pattern] = 1

		# Verbosity for debugging
		# print "Position:", curpos, "Pattern:", pattern
		
		curpos += 1

	# return a dictionary containing pattern pairs.
	return pattdict

def flattenpatt(pattern_tuple):
	# flatten our pattern tuple produced by "unpack()" in "findpatt()"
	patternstring = ""
	for byte in pattern_tuple:
		patternstring += "%0.2x" % byte
	return patternstring

def main():
	parser = OptionParser()
	# File to parse
	parser.add_option("-f", "--file", action="store", dest="file_to_parse")

	# Number of bytes in a pattern
	parser.add_option("-n", "--number", action="store", dest="pattern_size", default=4)

	# Filter out the number of repeats
	parser.add_option("-r", "--repeats", action="store", dest="repeats", default=20)

	# Specify an offset to start from
	parser.add_option("-o", "--offset", action="store", dest="offset", default=0)

	(options, args) = parser.parse_args()

	if not options.file_to_parse:
		parser.print_help()
		parser.error("File name required.")

	else:
		f = open(options.file_to_parse, 'rb')
		print "Parsing..."

		# prototype, not worried about error handling
		patterns = findpatt(f,path.getsize(options.file_to_parse),int(options.pattern_size),options.offset)

		print "Sorting..."
		sorted_patterns = sorted(patterns.iteritems(), key=operator.itemgetter(1))

		#for key in patterns.keys():
		for patt in sorted_patterns:
			if not patt[1] < int(options.repeats):
				print "Pattern: %s\tCount: %d" % (patt[0],patt[1])
		print "Done parsing."
		f.close()


if __name__ == "__main__":
	main()