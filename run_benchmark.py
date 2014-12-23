#!/usr/bin/env python

from __future__ import division

import sys
import os
import csv
import numpy
from pprint import pprint
from datetime import datetime

## functions
def call(cmd):
	ts_start = datetime.now()
	os.system(cmd)
	ts_end = datetime.now()
	ts_diff = ts_end - ts_start

	return (ts_diff.days * 24 * 60 * 60 + ts_diff.seconds) * 1000 + ts_diff.microseconds / 1000.0

def calc_compress(origfile, compfile, duration):
	origsize = os.path.getsize(origfile)
	compsize = os.path.getsize(compfile)

	return {
		"origsize" : origsize,
		"compsize" : compsize,
		"duration" : duration
	}

## command line arguments
if len(sys.argv) < 2:
	print "usage: bench.py <infile>"
	sys.exit(1)
elif len(sys.argv) == 2 and not os.path.isfile(sys.argv[1]):
	print "ERROR: cannot open infile"
	sys.exit(1)

## main
infile = sys.argv[1]
num_iterations = 3
compressors = [
	{
		"name" : "gzip",
		"levels" : xrange(1, 10),
		"compressed_filename" : lambda level, input: "{1}.{0}.gz".format(level, input),
		"decompressed_filename" : lambda level, input: "{1}.{0}.gz.uncompressed".format(level, input),
		"compress_func" : lambda level, input: call("gzip -c -{0} {1} >{1}.{0}.gz".format(level, input)),
		"decompress_func" : lambda level, input: call("gzip -d -c {1}.{0}.gz >{1}.{0}.gz.uncompressed".format(level, input))
	},
	{
		"name" : "bzip2",
		"levels" : xrange(1, 10),
		"compressed_filename" : lambda level, input: "{1}.{0}.bz2".format(level, input),
		"decompressed_filename" : lambda level, input: "{1}.{0}.bz2.uncompressed".format(level, input),
		"compress_func" : lambda level, input: call("bzip2 -z -k -c -{0} {1} >{1}.{0}.bz2".format(level, input)),
		"decompress_func" : lambda level, input: call("bzip2 -d -c {1}.{0}.bz2 >{1}.{0}.bz2.uncompressed".format(level, input))
	},
	{
		"name" : "xz",
		"levels" : xrange(1, 10),
		"compressed_filename" : lambda level, input: "{1}.{0}.xz".format(level, input),
		"decompressed_filename" : lambda level, input: "{1}.{0}.xz.uncompressed".format(level, input),
		"compress_func" : lambda level, input: call("xz -z -k -c -{0} {1} >{1}.{0}.xz".format(level, input)),
		"decompress_func" : lambda level, input: call("xz -d -c {1}.{0}.xz >{1}.{0}.xz.uncompressed".format(level, input))
	},
	{
		"name" : "7z",
		"levels" : xrange(1, 10),
		"compressed_filename" : lambda level, input: "{1}.{0}.7z".format(level, input),
		"decompressed_filename" : lambda level, input: "{1}.{0}.7z.uncompressed".format(level, input),
		"compress_func" : lambda level, input: call("7za a -bd -t7z -mx{0} {1}.{0}.7z {1}".format(level, input)),
		"decompress_func" : lambda level, input: call("7z e {1}.{0}.7z -so *.* >{1}{0}.7z.uncompressed".format(level, input))
	},
	{
		"name" : "lzop",
		"levels" : xrange(1, 10),
		"compressed_filename" : lambda level, input: "{1}.{0}.lzop".format(level, input),
		"decompressed_filename" : lambda level, input: "{1}.{0}.lzop.uncompressed".format(level, input),
		"compress_func" : lambda level, input: call("lzop -{0} -f -o {1}.{0}.lzop {1}".format(level, input)),
		"decompress_func" : lambda level, input: call("lzop -d -c {1}.{0}.lzop >{1}.{0}.lzop.uncompressed".format(level, input))
	},
	{
		"name" : "plzip",
		"levels" : xrange(1, 10),
		"compressed_filename" : lambda level, input: "{1}.{0}.lz".format(level, input),
		"decompressed_filename" : lambda level, input: "{1}.{0}.lz.uncompressed".format(level, input),
		"compress_func" : lambda level, input: call("plzip -{0} -c {1} >{1}.{0}.lz".format(level, input)),
		"decompress_func" : lambda level, input: call("plzip -d {1}.{0}.lz -c >{1}.{0}.lz.uncompressed".format(level, input))
	},
	{
		"name" : "zpaq",
		"levels" : xrange(1, 6),
		"compressed_filename" : lambda level, input: "{1}.{0}.zpaq".format(level, input),
		"decompressed_filename" : lambda level, input: "{1}.{0}.zpaq.uncompressed".format(level, input),
		"compress_func" : lambda level, input: call("/tmp/zpaq a {1}.{0}.zpaq {1} -method {0} ".format(level, input)),
		"decompress_func" : lambda level, input: call("/tmp/zpaq x {1}.{0}.zpaq {1} -to {1}.{0}.zpaq.uncompressed".format(level, input))
	}
	# currently removed due to slow decompression
	# {
		# "name" : "rzip",
		# "levels" : xrange(1, 2),
		# "compressed_filename" : lambda level, input: "{1}.{0}.rz".format(level, input),
		# "compress_func" : lambda level, input: call("rzip -{0} -k -o {1}.{0}.rz {1}".format(level, input)),
		# "decompress_func" : lambda level, input: call("rzip -d {1}.{0}.rz -o {1}.{0}.rz.uncompressed".format(level, input))
	# },
]

with open("results_compress.csv", "w") as compress_csvfile, open("results_decompress.csv", "w") as decompress_csvfile:
	compress_csv = csv.writer(compress_csvfile, delimiter = ",")
	decompress_csv = csv.writer(decompress_csvfile, delimiter = ",")
	compress_csv.writerow(["compressor", "method", "origsize", "compsize", "duration"])
	decompress_csv.writerow(["compressor", "method", "duration"])

	for compressor in compressors:
		for level in compressor["levels"]:
			duration = []
			for iteration in xrange(0, num_iterations):
				print "{0} compression (level {1}), round {2}".format(compressor["name"], level, iteration)
				if os.path.exists(compressor["compressed_filename"](level, infile)):
					print "{0} already exists, removing...".format(compressor["compressed_filename"](level, infile))
				duration.append(compressor["compress_func"](level, infile))
			duration_avg = numpy.mean(duration)
			result = calc_compress(infile, compressor["compressed_filename"](level, infile), duration_avg)
			compress_csv.writerow([compressor["name"], "level {0}".format(level), result['origsize'], result['compsize'], result['duration']])
			pprint(result)

		for level in compressor["levels"]:
			duration = []
			for iteration in xrange(0, num_iterations):
				print "{0} decompression (level {1}), round {2}".format(compressor["name"], level, iteration)
				if os.path.exists(compressor["decompressed_filename"](level, infile)):
					print "{0} already exists, removing...".format(compressor["decompressed_filename"](level, infile))
				duration.append(compressor["decompress_func"](level, infile))
			duration_avg = numpy.mean(duration)
			decompress_csv.writerow([compressor["name"], "level {0}".format(level), duration_avg])
			pprint({"duration": duration_avg})
