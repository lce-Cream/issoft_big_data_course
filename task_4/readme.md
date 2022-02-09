## Description
This folder contains two bash scripts. Datasets could be downloaded using download.sh and benchmarked with  
benchmark.sh. Result log files and plots are stored in two subfolders. Final report in results.xlsx  
is a table compilation of files in those folders.  

# Installation
Run the following command.
```bash
$ pip install cmdbench
```

# Usage
Download needed dataser and run benchmark on it.

Download datasets with download.sh.
### input
```bash
$ ./download.sh -s small -d ./data/
```

### output
```bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  264M  100  264M    0     0  42265      0  1:49:16  1:49:16 --:--:-- 82161

Archive:  ./dataset.zip
  inflating: ./links.csv
  inflating: ./tags.csv
  inflating: ./genome-tags.csv
  inflating: ./ratings.csv
  inflating: ./README.txt
  inflating: ./genome-scores.csv
  inflating: ./movies.csv
```


Benchmark application with benchmark.sh.
### input
```bash
$ ./benchmark.sh -i 10 -p plot.png -l statistics.log -c "py get-movies.py -r shrek -t 2008"
```

### output
```bash
$ Last runtime:  1.202 seconds: 100%|##########| 10/10 [00:15<00:00,  1.51s/it]
```
statistics.log file content is:
```bash
Process: 
    Stdout: None
    Stderr: None
    Runtime: (mean: 43.800999999999995, stdev: 0.2709108094311978, min: 43.418, max: 44.001) second(s)
    Exit code: (mean: 0.0, stdev: 0.0, min: 0, max: 0)

CPU (seconds): 
    User time: (mean: 37.932291666666664, stdev: 0.32907435414440234, min: 37.484375, max: 38.265625)
    System time: (mean: 2.7135416666666665, stdev: 0.1741484739302134, min: 2.484375, max: 2.90625)
    Total time: (mean: 40.645833333333336, stdev: 0.5026513902685328, min: 39.96875, max: 41.171875)

Memory (bytes): 
    Maximum: (mean: 25245013.333333332, stdev: 47335.93142165427, min: 25178112, max: 25280512)
    Maximum per process: (mean: 19006805.333333332, stdev: 47335.93142165427, min: 18939904, max: 19042304)

Disk: 
    Read (bytes): (mean: 4096.0, stdev: 0.0, min: 4096, max: 4096)
    Write (bytes): (mean: 0.0, stdev: 0.0, min: 0, max: 0)
    Total (bytes): (mean: 4096.0, stdev: 0.0, min: 4096, max: 4096)
    Other (bytes): (mean: 414.0, stdev: 0.0, min: 414, max: 414)

Time series: 
    Sampling milliseconds: (mean: 21853.51697462155, stdev: 12638.196604923092, min: 7, max: 43980)
    CPU (percentages): (mean: 43.39268143365984, stdev: 49.64911508427325, min: 0.0, max: 104.2)
    Memory (bytes): (mean: 22833037.107747108, stdev: 728725.0484542849, min: 1093632, max: 25280512)

```
