#!/usr/bin/env python

from __future__ import division

from pandas import *
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

# functions
def create_diagram(df, title, filename, y_axis_value, y_axis_label, colors):
	color = 0
	fig = plt.figure(figsize=(10,6))
	title = fig.suptitle(title, fontsize=18)
	for key, group in df.groupby('compressor'):
		ax = group.plot(x='method', y=y_axis_value, label=key, color=colors[color], linewidth=3, kind='line', marker='o')
		ax.xaxis.set_tick_params(pad=15)
		ax.yaxis.set_tick_params(pad=15)
		ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: x / 1000000))
		ax.set_ylabel(y_axis_label, fontsize=14)
		ax.set_xlabel("Compression level", fontsize=14)
		color += 2
	
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_fontsize(12)
	
	lgd = plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.5))
	fig.savefig(filename, bbox_extra_artists=(lgd,title), bbox_inches='tight')

# colors
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

## import and process compression csv
df = read_csv("results_compress.csv", sep=",")
df['ratio'] = df['compsize'] / df['origsize']
df['time_efficiency'] = (df['origsize'] / df['compsize']) / df['duration']
create_diagram(df, "Compressed size (bytes)", "compression_size.png", "compsize", "Compressed size (mb)", tableau20)
create_diagram(df, "Compression Ratio", "compression_ratio.png", "ratio", "Compression ratio", tableau20)
create_diagram(df, "Comp. Time efficiency ((origsize / compsize) / duration)", "comp_time_efficiency.png", "time_efficiency", "Compression time efficiency", tableau20)
create_diagram(df, "Compression duration (s)", "compression_duration.png", "duration", "Compression duration (s)", tableau20)

## import and process decompression csv
df = read_csv("results_decompress.csv", sep=",")
create_diagram(df, "Decompression Duration(s)", "decompression_duration.png", "duration", "Decompression duration (s)", tableau20)

