# Description
get-movies-hadoop.sh combines mapper.py and reducer.py under one interface for usage under Hadoop.

## Requirements
All usage cases were tested on Hadoop 2.10.1 and Python 3.7. It's strongly recommended to use
these versions or higher for stable work.

## Usage
```bash
Usage: get-movies-hadoop [OPTION]
Hadoop MapReduce orchestration script.

  -d, --data            path to data file
  -g, --genres          genres to filter for
  -e, --regex           regex to filter for
  -f, --year_from       command to run benchmark for
  -t, --year_to         display this help message
  -n, --number          number of values to reduce
  -s, --streaming       path to hadoop-streaming.jar file
  -m, --mapper          path to mapper file
  -r, --reducer         path to reducer file
  -h, --help            print this help message

Examples:
$ ./get-movies-hadoop.sh -d small_movies.csv -e toy -t 2000 -n 1 -m mapper.py -r reducer.py
```

### input
```bash
$ ./get-movies-hadoop.sh -d small_movies_10k.csv -e toy -t 2015 -n 2
```

Translates into equivalent command, which could be understood by hadoop streaming as:
```bash
hadoop fs -rm /user/aleksandr_zhukov8/output/*; \
hadoop fs -rmdir /user/aleksandr_zhukov8/output/; \
yarn jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input /user/aleksandr_zhukov8/small_movies_10k.csv \
-output /user/aleksandr_zhukov8/output \
-file /home/aleksandr_zhukov8/mapper.py \
-file /home/aleksandr_zhukov8/reducer.py \
-mapper "$PYSPARK_PYTHON mapper.py -r toy -t 2015" \
-reducer "$PYSPARK_PYTHON reducer.py -n 2"
```

Actual result could be viewed like this:

### input
```bash
$ hadoop fs -ls /user/$USER/output/
```

### output
```bash
Found 4 items
-rw-r--r--   1 aleksandr_zhukov8 hadoop          0 2021-12-15 20:04 /user/aleksandr_zhukov8/output/_SUCCESS
-rw-r--r--   1 aleksandr_zhukov8 hadoop        226 2021-12-15 20:04 /user/aleksandr_zhukov8/output/part-00000
-rw-r--r--   1 aleksandr_zhukov8 hadoop         90 2021-12-15 20:04 /user/aleksandr_zhukov8/output/part-00001
-rw-r--r--   1 aleksandr_zhukov8 hadoop        148 2021-12-15 20:04 /user/aleksandr_zhukov8/output/part-00002
```

### input
```bash
$ hadoop fs -cat /user/$USER/output/*
```

### output
```bash
Adventure       ["('Toy Story', 1995)", "('Toy Story 2', 1999)"]
Children        ["('Toy Story 3', 2010)", "('Babes in Toyland', 1961)"]
Drama           ["('Toy Soldiers', 1991)"]
Musical         ["('Babes in Toyland', 1961)", "('Babes in Toyland', 1934)"]
Animation       ["('Toy Story', 1995)", "('Toy Story 3', 2010)"]
IMAX            ["('Toy Story 3', 2010)"]
Action          ["('Toy Soldiers', 1991)"]
Comedy          ["('Toy, The', 1982)", "('Toy Story 2', 1999)"]
Fantasy         ["('Toy Story 3', 2010)", "('Toy Story 2', 1999)"]
```


### hadoop log message
```bash
Deleted /user/aleksandr_zhukov8/output/_SUCCESS
Deleted /user/aleksandr_zhukov8/output/part-00000
Deleted /user/aleksandr_zhukov8/output/part-00001
Deleted /user/aleksandr_zhukov8/output/part-00002
21/12/15 20:03:25 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
packageJobJar: [/home/aleksandr_zhukov8/tasks/task_5/get_movies_hadoop/mapper.py, /home/aleksandr_zhukov8/tasks/task_5/get_movies_hadoop/reducer.py] [/usr/lib/hadoop-mapreduce/hadoop-streaming-2.10.1.
jar] /tmp/streamjob4916849386566532346.jar tmpDir=null
21/12/15 20:03:26 INFO client.RMProxy: Connecting to ResourceManager at cluster-ffc4-m/10.128.0.2:8032
21/12/15 20:03:26 INFO client.AHSProxy: Connecting to Application History server at cluster-ffc4-m/10.128.0.2:10200
21/12/15 20:03:27 INFO client.RMProxy: Connecting to ResourceManager at cluster-ffc4-m/10.128.0.2:8032
21/12/15 20:03:27 INFO client.AHSProxy: Connecting to Application History server at cluster-ffc4-m/10.128.0.2:10200
21/12/15 20:03:27 INFO mapred.FileInputFormat: Total input files to process : 1
21/12/15 20:03:27 INFO mapreduce.JobSubmitter: number of splits:9
21/12/15 20:03:28 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1639592889336_0007
21/12/15 20:03:28 INFO conf.Configuration: resource-types.xml not found
21/12/15 20:03:28 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
21/12/15 20:03:28 INFO resource.ResourceUtils: Adding resource type - name = memory-mb, units = Mi, type = COUNTABLE
21/12/15 20:03:28 INFO resource.ResourceUtils: Adding resource type - name = vcores, units = , type = COUNTABLE
21/12/15 20:03:28 INFO impl.YarnClientImpl: Submitted application application_1639592889336_0007
21/12/15 20:03:28 INFO mapreduce.Job: The url to track the job: http://cluster-ffc4-m:8088/proxy/application_1639592889336_0007/
21/12/15 20:03:28 INFO mapreduce.Job: Running job: job_1639592889336_0007
21/12/15 20:03:36 INFO mapreduce.Job: Job job_1639592889336_0007 running in uber mode : false
21/12/15 20:03:36 INFO mapreduce.Job:  map 0% reduce 0%
21/12/15 20:03:44 INFO mapreduce.Job:  map 22% reduce 0%
21/12/15 20:03:45 INFO mapreduce.Job:  map 33% reduce 0%
21/12/15 20:03:52 INFO mapreduce.Job:  map 56% reduce 0%
21/12/15 20:03:52 INFO mapreduce.Job:  map 56% reduce 0%
21/12/15 20:03:53 INFO mapreduce.Job:  map 67% reduce 0%
21/12/15 20:04:00 INFO mapreduce.Job:  map 100% reduce 0%
21/12/15 20:04:07 INFO mapreduce.Job:  map 100% reduce 33%
21/12/15 20:04:09 INFO mapreduce.Job:  map 100% reduce 67%
21/12/15 20:04:10 INFO mapreduce.Job:  map 100% reduce 100%
21/12/15 20:04:12 INFO mapreduce.Job: Job job_1639592889336_0007 completed successfully
21/12/15 20:04:12 INFO mapreduce.Job: Counters: 50
        File System Counters
                FILE: Number of bytes read=929
                FILE: Number of bytes written=2673277
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=528252
                HDFS: Number of bytes written=464
                HDFS: Number of read operations=42
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=9
        Job Counters 
                Killed reduce tasks=1
                Launched map tasks=9
                Launched reduce tasks=3
                Data-local map tasks=9
                Total time spent by all maps in occupied slots (ms)=177093
                Total time spent by all reduces in occupied slots (ms)=44637
                Total time spent by all map tasks (ms)=59031
                Total time spent by all reduce tasks (ms)=14879
                Total vcore-milliseconds taken by all map tasks=59031
                Total vcore-milliseconds taken by all reduce tasks=14879
                Total megabyte-milliseconds taken by all map tasks=181343232
                Total megabyte-milliseconds taken by all reduce tasks=45708288
        Map-Reduce Framework
                Map input records=9743
                Map output records=28
                Map output bytes=855
                Map output materialized bytes=1073
                Input split bytes=1053
                Combine input records=0
                Combine output records=0
                Reduce input groups=9
                Reduce shuffle bytes=1073
                Reduce input records=28
                Reduce output records=9
                Spilled Records=56
                Shuffled Maps =27
                Failed Shuffles=0
                Merged Map outputs=27
                GC time elapsed (ms)=2015
        CPU time spent (ms)=17430
                Physical memory (bytes) snapshot=5692411904
                Virtual memory (bytes) snapshot=52849508352
                Total committed heap usage (bytes)=5120720896
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters 
                Bytes Read=527199
        File Output Format Counters 
                Bytes Written=464
```
