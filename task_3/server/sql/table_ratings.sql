USE {DATABASE_PLACEHOLDER};
CREATE TABLE IF NOT EXISTS ratings
(
UserId      INT           NOT NULL,
MovieId     INT           NOT NULL,
Rating      FLOAT(2,1)    NOT NULL,

FOREIGN KEY (MovieId) REFERENCES movies(MovieId),
PRIMARY KEY (UserId, MovieId)
) ENGINE='MyISAM';
