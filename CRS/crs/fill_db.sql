DROP TABLE IF EXISTS MOVIES;
DROP TABLE IF EXISTS PROJECTIONS;
DROP TABLE IF EXISTS RESERVATIONS;

CREATE TABLE MOVIES (
    id          INTEGER AUTO_INCREMENT PRIMARY KEY,
    name        TEXT,
    rating      REAL
);

CREATE TABLE PROJECTIONS (
    id          INTEGER PRIMARY KEY,
    movie_id    INTEGER,
    type        TEXT,
    date        DATE,
    time        DATETIME,
    FOREIGN KEY(movie_id) REFERENCES MOVIES(id)
);

CREATE TABLE RESERVATIONS (
    username        TEXT,
    projection_id   INTEGER,
    row             INTEGER,
    col             INTEGER,
    FOREIGN KEY(projection_id) REFERENCES PROJECTIONS(id)
);

INSERT INTO MOVIES(id, name, rating) VALUES(1, 'The Intern', 7.4);
INSERT INTO MOVIES(id, name, rating) VALUES(2, 'Sicario', 8.0);
INSERT INTO MOVIES(id, name, rating) VALUES(3, 'The Martian', 8.2);

INSERT INTO PROJECTIONS(movie_id, type, date, time) VALUES(1, '2D', '2015-11-01', '22:40');
INSERT INTO PROJECTIONS(movie_id, type, date, time) VALUES(2, '2D', '2015-11-02', '16:30');
INSERT INTO PROJECTIONS(movie_id, type, date, time) VALUES(3, '3D', '2015-11-03', '19:25');
INSERT INTO PROJECTIONS(movie_id, type, date, time) VALUES(3, '4DX', '2015-11-03', '21:15');
INSERT INTO PROJECTIONS(movie_id, type, date, time) VALUES(2, '3D', '2015-11-02', '20:35');
