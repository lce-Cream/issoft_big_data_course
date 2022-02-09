import csv
from .decorators import request_time_used
# movies: movieId,title,genres
# ratings: userId,movieId,rating,timestamp

_DEBUG = True

@request_time_used(_DEBUG)
def make_cache(config: dict) -> None:
    '''Maps every movie id to it's average rating and writes it in csv file.'''
    with open(config['movies_path'], 'r', encoding='utf-8') as movies_file:
        movie_rating_dict = {}
        next(movies_file)
        for movie in movies_file:
            movie_id = int(movie.split(',')[0])
            movie_rating_dict[movie_id] = [0, 0]

    with open(config['ratings_path'], 'r') as ratings_file:
        next(ratings_file)
        for line in ratings_file:
            line = line.split(',')
            movie_id = int(line[1])
            movie_rating = float(line[2])
            movie_rating_dict[movie_id][0] += movie_rating # sum of all ratings
            movie_rating_dict[movie_id][1] += 1            # count of these ratings

    for record in movie_rating_dict.values():
        rating_sum = record[0]
        rating_count = record[1] if record[1] else 1
        average_rating = round(rating_sum/rating_count, 1)
        record[0] = average_rating

    with open(config['cache_path'], 'w', newline='') as cache:
        writer = csv.writer(cache)
        writer.writerow(('movieid', 'rating'))
        for item in movie_rating_dict.items():
            movie_id = item[0]
            average_rating = item[1][0]
            writer.writerow((movie_id, average_rating))
