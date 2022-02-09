# Description
get-movies.sh is a script to simplify interaction with the main programm get-movies.py.  

## Requirements
All usage cases were tested on Hadoop 2.10.1 and Python 3.7. It's strongly recommended to use
these versions or higher for stable work.

## Usage
```bash
Usage: get-movies [OPTION]
Spark job orchestration script for movie retrieval.

  -g, --genres          genres to filter by
  -r, --regex           regex to filter by
  -f, --year_from       year to filter movies from
  -t, --year_to         year to filter movies to
  -n, --number          number of movies in each genre
  -u, --user            username to execute program from
  -m, --movies          movies csv file
  -a, --ratings         ratings csv file
  -h, --help            print this help message

Examples:
$ ./get-movies.sh -m small_movies.csv -a small_ratings.csv -r toy -t 2000 -n 1
```

### input
```bash
$ ./get-movies.sh -r sun -n 3
```

### output
```bash
genre,title,year,rating
Action,Lost in the Sun,2015,2.0
Action,After the Sunset,2004,3.6
Action,Tears of the Sun,2003,2.6
Adventure,Sunshine,2007,3.6
Adventure,Little Miss Sunshine,2006,3.9
Adventure,After the Sunset,2004,3.6
Comedy,First Sunday,2008,3.5
Comedy,Sunshine Cleaning,2008,3.4
Comedy,Little Miss Sunshine,2006,3.9
Crime,First Sunday,2008,3.5
Crime,After the Sunset,2004,3.6
Crime,Sympathy for Mr. Vengeance (Boksuneun naui geot),2002,3.8
Documentary,Mayor of the Sunset Strip,2003,3.5
Documentary,Murder on a Sunday Morning (Un coupable idéal),2001,3.5
Documentary,Dream of Light (a.k.a. Quince Tree Sun, The) (Sol del membrillo, El),1992,5.0
Drama,Lost in the Sun,2015,2.0
Drama,Sunset Limited, The,2011,4.0
Drama,Sunshine Cleaning,2008,3.4
Film-Noir,Sunset Blvd. (a.k.a. Sunset Boulevard),1950,4.3
Horror,The Town that Dreaded Sundown,2014,3.0
Mystery,Rising Sun,1993,3.3
Romance,Eternal Sunshine of the Spotless Mind,2004,4.2
Romance,Before Sunset,2004,3.7
Romance,Under the Tuscan Sun,2003,3.3
Sci-Fi,Sunshine,2007,3.6
Sci-Fi,Eternal Sunshine of the Spotless Mind,2004,4.2
Thriller,Lost in the Sun,2015,2.0
Thriller,The Town that Dreaded Sundown,2014,3.0
Thriller,Sunshine,2007,3.6
War,Empire of the Sun,1987,4.0
War,White Sun of the Desert, The (Beloe solntse pustyni),1970,4.0
Western,Butch Cassidy and the Sundance Kid,1969,3.9
Western,Duel in the Sun,1946,5.0
```

### input
```bash
$ hadoop fs -ls ./output/
```

### output
```bash
Found 9 items
-rw-r--r--   1 aleksandr_zhukov8 hadoop          0 2021-12-26 17:17 output/_SUCCESS
-rw-r--r--   1 aleksandr_zhukov8 hadoop          0 2021-12-26 17:17 output/part-00000
-rw-r--r--   1 aleksandr_zhukov8 hadoop          0 2021-12-26 17:17 output/part-00001
-rw-r--r--   1 aleksandr_zhukov8 hadoop          0 2021-12-26 17:17 output/part-00002
-rw-r--r--   1 aleksandr_zhukov8 hadoop         24 2021-12-26 17:17 output/part-00003
-rw-r--r--   1 aleksandr_zhukov8 hadoop        302 2021-12-26 17:17 output/part-00004
-rw-r--r--   1 aleksandr_zhukov8 hadoop        396 2021-12-26 17:17 output/part-00005
-rw-r--r--   1 aleksandr_zhukov8 hadoop        314 2021-12-26 17:17 output/part-00006
-rw-r--r--   1 aleksandr_zhukov8 hadoop        345 2021-12-26 17:17 output/part-00007
```

### Spark log message
```bash
21/12/26 17:17:11 INFO org.spark_project.jetty.util.log: Logging initialized @3292ms to org.spark_project.jetty.util.log.Slf4jLog
21/12/26 17:17:11 INFO org.spark_project.jetty.server.Server: jetty-9.4.z-SNAPSHOT; built: unknown; git: unknown; jvm 1.8.0_275-b01
21/12/26 17:17:11 INFO org.spark_project.jetty.server.Server: Started @3392ms
21/12/26 17:17:11 INFO org.spark_project.jetty.server.AbstractConnector: Started ServerConnector@1087e178{HTTP/1.1, (http/1.1)}{0.0.0.0:36123}
21/12/26 17:17:14 INFO org.apache.hadoop.mapred.FileInputFormat: Total input files to process : 1
21/12/26 17:17:16 INFO org.apache.hadoop.mapred.FileInputFormat: Total input files to process : 1
21/12/26 17:17:19 INFO org.spark_project.jetty.server.AbstractConnector: Stopped Spark@1087e178{HTTP/1.1, (http/1.1)}{0.0.0.0:0}
```
