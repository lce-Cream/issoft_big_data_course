## Description
This application allows to make queries to csv film files. It's designed to make some cash csv files first  
to save time on not doing heavy calculations on every query. (Medium data files are excluded to save space  
in remote directory).  

## Installation
If yaml is not in your standard python library, then install it by running this command.

```bash
$pip install pyyaml
```

### config
```bash
sort_rules: year, rating, title
movies_path: ./data/movies.csv
ratings_path: ./data/ratings.csv
cache_path: ./data/cache.csv
all_genres: Adventure|Comedy|Action|Drama|Crime|Children|Mystery|Animation|Documentary|Thriller|Horror|Fantasy|Western|Film-Noir|Romance|Sci-Fi|Musical|War|(no genres listed)|IMAX
```
### caching
On first launch program should ask to make cache like listed below.
```bash
cash file not found, start caching now? (y/n)
caching may require up to couple of hours depending on size of the data...
```

If caching was successful, output looks like that.
```bash
operation took 2.366 seconds
the script is ready now
```

## Usage
After caching script can be used to perform queries. Below are listed some example inputs and according outputs.

Get help message.
### input
```bash
  $ py get-movies.py --help
```

### output
```bash
usage: client.py [-h] [-n <int>] [-g <regexp>] [-f <int>] [-t <int>] [-r <regexp>]  

allows to perform queries to csv movies file  

optional arguments:
  -h,          --help              show this help message and exit
  -n <int>,    --number <int>      number of movies to retrieve
  -g <regexp>, --genres <regexp>   get movies by genres in x|y|z format
  -f <int>,    --year_from <int>   get movies from this year
  -t <int>,    --year_to <int>     get movies to this year
  -r <regexp>, --title <regexp>    get movies by title regexp
```
  
Get one latest and best rated movie for every genre.
### input
```bash
$ py get-movies.py -n 1
```

### output
```bash
genre,title,year,rating
Adventure,The Man Who Killed Don Quixote,2018,4.5
Comedy,Tom Segura: Disgraceful,2018,4.5
Action,Game Night,2018,4.0
Drama,Love, Simon,2018,4.0
Crime,Game Night,2018,4.0
Children,Solo: A Star Wars Story,2018,3.9
Mystery,Annihilation,2018,3.8
Animation,Isle of Dogs,2018,3.5
Documentary,Won't You Be My Neighbor?,2018,5.0
Thriller,Alpha,2018,4.5
Horror,Game Night,2018,4.0
Fantasy,The Man Who Killed Don Quixote,2018,4.5
Western,The Dark Tower,2017,3.5
Film-noir,Bullet to the Head,2012,1.5
Romance,Mamma Mia: Here We Go Again!,2018,4.5
Sci-fi,Sorry to Bother You,2018,4.5
Musical,Strange Magic,2015,3.0
War,War Machine,2017,4.0
(no genres listed),Too Funny to Fail: The Life and Death of The Dana Carvey Show,2017,4.5
Imax,Star Wars: Episode VII - The Force Awakens,2015,3.9
```
  
Get 5 best rated drama and comedy movies with the word 'city' in them.
### input
```bash
$ py get-movies.py -n 5 -g 'drama|comedy' -r city
```

### output
```bash
genre,title,year,rating
Drama,Sex and the City 2,2010,1.0
Drama,City Island,2009,4.0
Drama,City of Men (Cidade dos Homens),2007,4.0
Drama,City of God (Cidade de Deus),2002,4.1
Drama,City by the Sea,2002,2.8
Comedy,Unicorn City,2012,5.0
Comedy,Sex and the City 2,2010,1.0
Comedy,City Island,2009,4.0
Comedy,Sex and the City,2008,2.4
Comedy,Detroit Rock City,1999,2.9
```

Get all movies about Shrek before 2008 year.
### input
```bash
py get-movies.py -t 2008 -r shrek
```

### output
```bash
genre,title,year,rating
Adventure,Shrek the Third,2007,3.0
Adventure,Shrek the Halls,2007,2.5
Adventure,Shrek 2,2004,3.6
Adventure,Shrek,2001,3.9
Comedy,Shrek the Third,2007,3.0
Comedy,Shrek the Halls,2007,2.5
Comedy,Shrek 2,2004,3.6
Comedy,Shrek,2001,3.9
Children,Shrek the Third,2007,3.0
Children,Shrek 2,2004,3.6
Children,Shrek,2001,3.9
Animation,Shrek the Third,2007,3.0
Animation,Shrek the Halls,2007,2.5
Animation,Shrek 2,2004,3.6
Animation,Shrek,2001,3.9
Fantasy,Shrek the Third,2007,3.0
Fantasy,Shrek the Halls,2007,2.5
Fantasy,Shrek,2001,3.9
Romance,Shrek 2,2004,3.6
Romance,Shrek,2001,3.9
Musical,Shrek 2,2004,3.6
```
