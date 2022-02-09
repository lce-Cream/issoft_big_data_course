USE {DATABASE_PLACEHOLDER};
DROP PROCEDURE IF EXISTS sp_get_movies;
CREATE PROCEDURE sp_get_movies(
IN rows_limit 	SMALLINT,
IN input_genres TINYTEXT,
IN year_FROM 	SMALLINT,
IN year_to 		SMALLINT,
IN title_regex 	TINYTEXT
)
BEGIN

    CREATE TEMPORARY TABLE IF NOT EXISTS tmp_movies_with_parsed_genres
        WITH RECURSIVE movies_with_parsed_genres(movieid, genre, tail) AS
                (
                        SELECT 
                            movieid,
                            substring_index(concat(genres, '|'), '|', 1) AS genre,
                            substring(concat(genres, '|'), locate('|', concat(genres, '|')) + 1, length(concat(genres, '|'))) AS tail
                        FROM
                            movies
                        
                        UNION ALL
                        
                        SELECT
                            movieid,
                            substring_index(tail, '|', 1), substring(tail, locate('|', tail) + 1, length(tail))
                        FROM
                            movies_with_parsed_genres
                        WHERE
                            locate('|', tail) <> 0

                    ) SELECT movieid, genre FROM movies_with_parsed_genres;

    IF input_genres IS NULL THEN
    SET input_genres = (
                    SELECT GROUP_CONCAT(genre SEPARATOR '|')
                    FROM
                        (
                            SELECT DISTINCT genre
                            FROM tmp_movies_with_parsed_genres
                            GROUP BY genre ORDER BY genre
                        ) 	AS unique_genres
                    );
    END IF;

    DROP TEMPORARY TABLE IF EXISTS tmp_parsed_input_genres;
    CREATE TEMPORARY TABLE tmp_parsed_input_genres
                WITH RECURSIVE parsed_input_genres(n, genre, input_tail) AS
                (
                    SELECT 
                        1 AS n,
                        substring_index(concat(input_genres, '|'), '|', 1) AS genre,
                        substring(concat(input_genres, '|'), locate('|', concat(input_genres, '|')) + 1, length(concat(input_genres, '|'))) AS input_tail

                    UNION ALL

                    SELECT
                        n + 1,
                        substring_index(input_tail, '|', 1),
                        substring(input_tail, locate('|', input_tail)+1, length(input_tail))
                    FROM
                        parsed_input_genres
                    WHERE
                        locate('|', input_tail) <> 0

                ) SELECT * FROM parsed_input_genres;

    SELECT genre, title, year, averagerating FROM
        (
            SELECT
                movieid,
                genre,
                title,
                year,
                averagerating,
                n,
                ROW_NUMBER() OVER(PARTITION BY genre ORDER BY year DESC, averagerating DESC, title ASC) AS row_n
            FROM
                tmp_movies_with_parsed_genres
            JOIN 
                tmp_parsed_input_genres
                USING(genre)
            JOIN
                movies_ratings
                USING(movieid)
            WHERE
                    ((year_FROM IS NULL) 	OR 	 (year >= year_FROM))
                AND ((year_to IS NULL) 		OR 	 (year <= year_to))
                AND ((title_regex IS NULL)  OR 	 (title REGEXP title_regex))

        ) AS result
    WHERE ((rows_limit IS NULL) OR (row_n <= rows_limit))
    ORDER BY n, year desc, averagerating desc, title;

END