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
num_iterations = 3

with open("results_compress.csv", "w") as compress_csvfile, open("results_decompress.csv", "w") as decompress_csvfile:
	compress_csv = csv.writer(compress_csvfile, delimiter = ",")
	decompress_csv = csv.writer(decompress_csvfile, delimiter = ",")
	compress_csv.writerow(["compressor", "method", "origsize", "compsize", "duration"])
	decompress_csv.writerow(["compressor", "method", "duration"])

	# --------------------------------------------------------------------------------
	# gzip compression
	for i in xrange(1, 10):
		duration = []
		for j in xrange(0, num_iterations):
			print "gzip compression (level {0}), round {1}".format(i, j)
			duration.append(call("gzip -c -{0} {1} >{1}.{0}.gz".format(i, sys.argv[1])))
		duration_avg = numpy.mean(duration)
		result = calc_compress(sys.argv[1], "{1}.{0}.gz".format(i, sys.argv[1]), duration_avg)
		compress_csv.writerow(["gzip", "level {0}".format(i), result['origsize'], result['compsize'], result['duration']])
		pprint(result)

	# gzip decompression
	for i in xrange(1, 10):
		print "gzip decompression (level {0})".format(i)
		duration = call("gzip -d -c {1}.{0}.gz >{1}.{0}.gz.uncompressed".format(i, sys.argv[1]))
		decompress_csv.writerow(["gzip", "level {0}".format(i), duration])
		pprint({"duration": duration})

	# --------------------------------------------------------------------------------
	# bzip2 compression
	for i in xrange(1, 10):
		duration = []
		for j in xrange(0, num_iterations):
			print "bzip2 compression (level {0}), round {1}".format(i, j)
			duration.append(call("bzip2 -z -k -c -{0} {1} >{1}.{0}.bz2".format(i, sys.argv[1])))
		duration_avg = numpy.mean(duration)
		result = calc_compress(sys.argv[1], "{1}.{0}.bz2".format(i, sys.argv[1]), duration_avg)
		compress_csv.writerow(["bzip2", "level {0}".format(i), result['origsize'], result['compsize'], result['duration']])
		pprint(result)

	# bzip2 decompression
	for i in xrange(1, 10):
		print "bzip2 decompression (level {0})".format(i)
		duration = call("bzip2 -d -c {1}.{0}.bz2 >{1}.{0}.bz2.uncompressed".format(i, sys.argv[1]))
		decompress_csv.writerow(["bzip2", "level {0}".format(i), duration])
		pprint({"duration": duration})

	# --------------------------------------------------------------------------------
	# xz compression
	for i in xrange(1, 10):
		duration = []
		for j in xrange(0, num_iterations):
			print "xz (level {0}), round {1}".format(i, j)
			duration.append(call("xz -z -k -c -{0} {1} >{1}.{0}.xz".format(i, sys.argv[1])))
		duration_avg = numpy.mean(duration)
		result = calc_compress(sys.argv[1], "{1}.{0}.xz".format(i, sys.argv[1]), duration_avg)
		compress_csv.writerow(["xz", "level {0}".format(i), result['origsize'], result['compsize'], result['duration']])
		pprint(result)

	# xz decompression
	for i in xrange(1, 10):
		print "xz decompression (level {0})".format(i)
		duration = call("xz -d -c {1}.{0}.xz >{1}.{0}.xz.uncompressed".format(i, sys.argv[1]))
		decompress_csv.writerow(["xz", "level {0}".format(i), duration])
		pprint({"duration": duration})

	# --------------------------------------------------------------------------------
	# 7z compression
	for i in xrange(1, 10):
		duration = []
		for j in xrange(0, num_iterations):
			print "7z (level {0}), round {1}".format(i, j)
			duration.append(call("7za a -bd -t7z -mx{0} {1}.{0}.7z {1}".format(i, sys.argv[1])))
		duration_avg = numpy.mean(duration)
		result = calc_compress(sys.argv[1], "{1}.{0}.7z".format(i, sys.argv[1]), duration_avg)
		compress_csv.writerow(["7z", "level {0}".format(i), result['origsize'], result['compsize'], result['duration']])
		pprint(result)

	# 7z decompression
	for i in xrange(1, 10):
		print "7z decompression (level {0})".format(i)
		duration = call("7z e {1}.{0}.7z -so *.* >{1}{0}.7z.uncompressed".format(i, sys.argv[1]))
		decompress_csv.writerow(["7z", "level {0}".format(i), duration])
		pprint({"duration": duration})

	# --------------------------------------------------------------------------------
	# lzop compression
	for i in xrange(1, 10):
		duration = []
		for j in xrange(0, num_iterations):
			print "lzop (level {0}), round {1}".format(i, j)
			duration.append(call("lzop -{0} -f -o {1}.{0}.lzop {1}".format(i, sys.argv[1])))
		duration_avg = numpy.mean(duration)
		result = calc_compress(sys.argv[1], "{1}.{0}.lzop".format(i, sys.argv[1]), duration_avg)
		compress_csv.writerow(["lzop", "level {0}".format(i), result['origsize'], result['compsize'], result['duration']])
		pprint(result)

	# lzop decompression
	for i in xrange(1, 10):
		print "lzop decompression (level {0})".format(i)
		duration = call("lzop -d -c {1}.{0}.lzop >{1}.{0}.lzop.uncompressed".format(i, sys.argv[1]))
		decompress_csv.writerow(["lzop", "level {0}".format(i), duration])
		pprint({"duration": duration})
