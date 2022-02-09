USE {DATABASE_PLACEHOLDER};
CREATE TABLE IF NOT EXISTS movies_ratings
(
MovieId            INT           PRIMARY KEY,
Title              TINYTEXT      NULL,
Year               SMALLINT      NULL,
Genres             TINYTEXT      NULL,
AverageRating      FLOAT(2,1)    NOT NULL
) ENGINE='MyISAM';
