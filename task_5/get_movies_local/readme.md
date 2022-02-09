# Description
get-movies-local.sh combines mapper.py and reducer.py under one interface for local
emulation of MapReduce.

## Requirements
Python 3.8 or higher.

## Usage
```bash
get-movies-local [OPTION]
Local MapReduce emulator orchestration script.

  -d, --data            path to data file
  -g, --genres          genres to filter for
  -r, --regex           regex to filter for
  -f, --year_from       year to filter from
  -t, --year_to         year to filter to
  -n, --number          number of values to reduce
  -h, --help            display this help message
```


### input
```bash
$ ./get-movies-local.sh -d small_movies_10.csv -r toy -t 2000 -n 1
```

### output
```bash
Action           [('Toy Soldiers', 1991)]
Adventure        [('Toy Story 2', 1999)]
Animation        [('Toy Story 2', 1999)]
Children         [('Babes in Toyland', 1934)]
Comedy           [('Babes in Toyland', 1934)]
Drama            [('Toy Soldiers', 1991)]
Fantasy          [('Babes in Toyland', 1934)]
Musical          [('Babes in Toyland', 1934)]
```


### input
```bash
$ ./get-movies-local.sh -d ./data/small_movies_10k.csv -f 2000 -t 2005 -g "comedy|adventure" -n 3
```

### output
```bash
Adventure       [("'Hellboy': The Seeds of Creation", 2004), ("Charlie's Angels: Full Throttle", 2003), ("Emperor's New Groove, The", 2000)]
Comedy          [("'Hellboy': The Seeds of Creation", 2004), ("Adam and Eve (National Lampoon's Adam & Eve)", 2005), ("Adam's Apples (Adams æbler)", 2005)]
```
