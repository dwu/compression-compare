#!/usr/bin/env python

from __future__ import division

from pandas import *
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

def gen_quot(row):
	row['quot'] = row['compsize'] / row['duration']

df = read_csv("results.csv", sep=",")

# colors
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

## duration figure
color = 0
fig = plt.figure(figsize=(10,6))
fig.suptitle("Duration", fontsize=18)
for key, group in df.groupby('compressor'):
    ax = group.plot(x='method', y='duration', label=key, color=tableau20[color], linewidth=3, kind='line', marker='o')
    ax.xaxis.set_tick_params(pad=15)
    ax.yaxis.set_tick_params(pad=15)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: x / 1000))
    ax.set_ylabel("Duration (s)", fontsize=14)
    ax.set_xlabel("Compression level", fontsize=14)
    color += 2

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(12)

lgd = plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.5))
fig.savefig('duration.png', bbox_extra_artists=(lgd,), bbox_inches='tight')

## compsize figure
color = 0
fig = plt.figure(figsize=(10,6))
fig.suptitle("Compressed size (bytes)", fontsize=18)
for key, group in df.groupby('compressor'):
    ax = group.plot(x='method', y='compsize', label=key, color=tableau20[color], linewidth=3, kind='line', marker='o')
    ax.xaxis.set_tick_params(pad=15)
    ax.yaxis.set_tick_params(pad=15)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: x / 1000000))
    ax.set_ylabel("Compressed size (mb)", fontsize=14)
    ax.set_xlabel("Compression level", fontsize=14)
    color += 2

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(12)

lgd = plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.5))
fig.savefig('compsize.png', bbox_extra_artists=(lgd,), bbox_inches='tight')

## ratio figure
color = 0
fig = plt.figure(figsize=(10,6))
fig.suptitle("Compression Ratio", fontsize=18)
for key, group in df.groupby('compressor'):
    ax = group.plot(x='method', y='ratio', label=key, color=tableau20[color], linewidth=3, kind='line', marker='o')
    ax.xaxis.set_tick_params(pad=15)
    ax.yaxis.set_tick_params(pad=15)
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.set_ylabel("Compression Ratio", fontsize=14)
    ax.set_xlabel("Compression level", fontsize=14)
    color += 2

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(12)

lgd = plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.5))
fig.savefig('ratio.png', bbox_extra_artists=(lgd,), bbox_inches='tight')

## time_efficiency figure
color = 0
fig = plt.figure(figsize=(10,6))
fig.suptitle("Time efficiency ((origsize / compsize) / duration)", fontsize=18)
for key, group in df.groupby('compressor'):
    ax = group.plot(x='method', y='time_efficiency', label=key, color=tableau20[color], linewidth=3, kind='line', marker='o')
    ax.xaxis.set_tick_params(pad=15)
    ax.yaxis.set_tick_params(pad=15)
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.set_ylabel("Time efficiency ((origsize / compsize) / duration)", fontsize=14)
    ax.set_xlabel("Compression level", fontsize=14)
    color += 2

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(12)

lgd = plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.5))
fig.savefig('time_efficiency.png', bbox_extra_artists=(lgd,), bbox_inches='tight')
