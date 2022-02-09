## Description
This application is devided into client and server parts. Server manages database setup and ETL operations.  
Client provides a CLI interface, which allows to run queries on a database already configurated by server.  

## Installation
Run MySQL Server, create your database. Edit config.yaml file for your needs. Example config files for server and cliend are listed below.

### server config
```
connection:
 host: localhost
 user: user
 password: user
 database: movies_database

paths:
 csv_movies:  ./data/movies.csv
 csv_ratings: ./data/ratings.csv

 table_movies:          ./sql/table_movies.sql
 table_ratings:         ./sql/table_ratings.sql
 table_movies_ratings:  ./sql/table_movies_ratings.sql

 insert_movies:         ./sql/insert_movies.sql
 insert_ratings:        ./sql/insert_ratings.sql
 insert_movies_ratings: ./sql/insert_movies_ratings.sql

 procedure: ./sql/sp_get_movies.sql
```

### client config
```
connection:
 host: localhost
 user: user
 password: user
 database: movies_database

variables:
 procedure_name: sp_get_movies
```
  
After that run the following commands.
```bash
$ pip install -r requirements.txt  
$ py setup.py  
```
  
If installation was successful, setup.py output looks like that.
```bash
SERVER::INFO:: database movies_database connected successfully
SERVER::INFO:: creating table movies: OK
SERVER::INFO:: creating table ratings: OK
SERVER::INFO:: creating joined table movies_ratings: OK
SERVER::INFO:: filling table movies: OK
SERVER::INFO:: filling table ratings: OK
SERVER::INFO:: filling table movies_ratings: OK
SERVER::INFO:: create procedure: OK
SERVER::INFO:: everything is ready
SERVER::INFO:: setup time: 2.031 seconds
```

## Usage
After installation you can interact with database through get-movies.py. Below are listed some example inputs and according outputs.
  
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
  
Get one latest best and best rated movie for every genre.
### input
```bash
$ py get-movies.py -n 1
```

### output
```bash
genre,title,year,rating
Adventure,Alpha,2018,4.5
Comedy,Mamma Mia: Here We Go Again!,2018,4.5
Action,Avengers: Infinity War - Part I,2018,4.0
Drama,Death Wish,2018,4.0
Crime,Death Wish,2018,4.0
Children,Solo: A Star Wars Story,2018,3.9
Mystery,Annihilation,2018,3.8
Animation,Bungo Stray Dogs: Dead Apple,2018,3.5
Documentary,Won't You Be My Neighbor?,2018,5.0
Thriller,Alpha,2018,4.5
Horror,Game Night,2018,4.0
Fantasy,Sorry to Bother You,2018,4.5
Western,The Dark Tower,2017,3.5
Film-Noir,Bullet to the Head,2012,1.5
Romance,Mamma Mia: Here We Go Again!,2018,4.5
Sci-Fi,Sorry to Bother You,2018,4.5
Musical,Strange Magic,2015,3.0
War,War Machine,2017,4.0
(no genres listed),Too Funny to Fail: The Life and Death of The Dana Carvey Show,2017,4.5
IMAX,Star Wars: Episode VII - The Force Awakens,2015,3.9
```
  
Get 3 best reated animation and adventure movies before and including 2010.
### input
```bash
$ py get-movies.py -n 3 -g 'animation|adventure' -t 2010
```
### output
```bash
genre,title,year,rating
Animation,Colourful (Karafuru),2010,5.0
Animation,Scooby-Doo! Abracadabra-Doo,2010,5.0
Animation,Day & Night,2010,4.1
Adventure,Scooby-Doo! Curse of the Lake Monster,2010,5.0
Adventure,The Pacific,2010,4.8
Adventure,Toy Story 3,2010,4.1
```
