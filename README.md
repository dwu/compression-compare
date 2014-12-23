# Compression benchmark

## Background

I needed to archive a large amount of plain text logs and wanted to get an
understanding of how different common compression tools perform on plain text
log files in terms of both compression ratio and compression/decompression
speed.

## Benchmarks

The benchmark script is executed via `python run_benchmark.py <input file>`.
The script performs three compression/decompression cycles for each benchmarked
compression tool and computes the average of the measured duration results.

The script currently supports the following compression tools (which are
available in the Debian package archive):

* gzip
* bzip2
* xz
* 7z
* lzop
* plzip
* zpaq

The benchmark results are stored in CSV files.

Running `python create_diagrams.py` turns the CSV files into diagrams using
Pandas.

The repository contains a `Vagrantfile` which sets up a virtual machine
containing the required environment for running the benchmark. As the version
of *zpaq* in the Debian archive is rather old, a more recent version is
downloaded and compiled automatically during VM provisioning.

## References

The canonical reference for benchmarking text compression tools is
http://www.mattmahoney.net/dc/text.html which provides benchmark results for a
large number of compressors (including less common ones) as well as a detailed
explanation of the compression parameters.

## Sample Reports

The sample benchmark was performed inside the provided virtual machine on an
i7-3632QM and a physical hard drive using a 117mb plain text log file as input.

![Compression Ratio](/sample_reports/compression_ratio.png?raw=true "Compression Ratio")

![Compression Duration](/sample_reports/compression_duration.png?raw=true "Compression Duration")
