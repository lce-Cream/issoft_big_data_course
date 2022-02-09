USE {DATABASE_PLACEHOLDER};
CREATE TABLE IF NOT EXISTS movies
(
MovieId     INT             PRIMARY KEY,
Title       TINYTEXT        NULL,
Year        SMALLINT        NULL,
Genres      TINYTEXT        NULL
) ENGINE='MyISAM';
