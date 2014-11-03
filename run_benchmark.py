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

def calc(origfile, compfile, duration):
	origsize = os.path.getsize(origfile)
	compsize = os.path.getsize(compfile)
	ratio = compsize / origsize
	time_efficiency = (origsize / compsize) / duration

	return {
		"origsize" : origsize,
		"compsize" : compsize,
		"ratio" : ratio,
		"time_efficiency" : time_efficiency,
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

with open("results.csv", "w") as csvfile:
	csv = csv.writer(csvfile, delimiter = ",")
	csv.writerow(["compressor", "method", "origsize", "compsize", "ratio", "duration", "time_efficiency"])

	# gzip
	for i in xrange(1, 10):
		duration = []
		for j in xrange(0, num_iterations):
			print "gzip (level {0}), round {1}".format(i, j)
			duration.append(call("gzip -c -{0} {1} >{1}.{0}.gz".format(i, sys.argv[1])))
		duration_avg = numpy.mean(duration)
		result = calc(sys.argv[1], "{1}.{0}.gz".format(i, sys.argv[1]), duration_avg)
		csv.writerow(["gzip", "level {0}".format(i), result['origsize'], result['compsize'], result['ratio'], result['duration'], result['time_efficiency']])
		pprint(result)

	# bzip2
	for i in xrange(1, 10):
		duration = []
		for j in xrange(0, num_iterations):
			print "bzip2 (level {0}), round {1}".format(i, j)
			duration.append(call("bzip2 -z -k -c -{0} {1} >{1}.{0}.bz2".format(i, sys.argv[1])))
		duration_avg = numpy.mean(duration)
		result = calc(sys.argv[1], "{1}.{0}.bz2".format(i, sys.argv[1]), duration_avg)
		csv.writerow(["bzip2", "level {0}".format(i), result['origsize'], result['compsize'], result['ratio'], result['duration'], result['time_efficiency']])
		pprint(result)

	# xz
	for i in xrange(1, 10):
		duration = []
		for j in xrange(0, num_iterations):
			print "xz (level {0}), round {1}".format(i, j)
			duration.append(call("xz -z -k -c -{0} {1} >{1}.{0}.xz".format(i, sys.argv[1])))
		duration_avg = numpy.mean(duration)
		result = calc(sys.argv[1], "{1}.{0}.xz".format(i, sys.argv[1]), duration_avg)
		csv.writerow(["xz", "level {0}".format(i), result['origsize'], result['compsize'], result['ratio'], result['duration'], result['time_efficiency']])
		pprint(result)

	# 7z
	for i in xrange(1, 10):
		duration = []
		for j in xrange(0, num_iterations):
			print "7z (level {0}), round {1}".format(i, j)
			duration.append(call("7za a -bd -t7z -mx{0} {1}.{0}.7z {1}".format(i, sys.argv[1])))
		duration_avg = numpy.mean(duration)
		result = calc(sys.argv[1], "{1}.{0}.7z".format(i, sys.argv[1]), duration_avg)
		csv.writerow(["7z", "level {0}".format(i), result['origsize'], result['compsize'], result['ratio'], result['duration'], result['time_efficiency']])
		pprint(result)

	# lzop
	for i in xrange(1, 10):
		duration = []
		for j in xrange(0, num_iterations):
			print "lzop (level {0}), round {1}".format(i, j)
			duration.append(call("lzop -{0} -f -o {1}.{0}.lzop {1}".format(i, sys.argv[1])))
		duration_avg = numpy.mean(duration)
		result = calc(sys.argv[1], "{1}.{0}.lzop".format(i, sys.argv[1]), duration_avg)
		csv.writerow(["lzop", "level {0}".format(i), result['origsize'], result['compsize'], result['ratio'], result['duration'], result['time_efficiency']])
		pprint(result)

