USE {DATABASE_PLACEHOLDER};
INSERT INTO movies_ratings (MovieId, Title, Year, Genres, AverageRating)
    SELECT movieid, title, year, genres, averagerating
    FROM movies
    JOIN
        (
            SELECT MovieId, ROUND(AVG(Rating), 1) as AverageRating
            FROM ratings
            GROUP BY (MovieId)
        ) as ratings
    USING (MovieId);
