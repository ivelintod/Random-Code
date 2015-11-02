import sqlite3


class Manager:

    DEFAULT_NUM_SEATS = 100

    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name)
        self.con.row_factory = sqlite3.Row
        self.cursor = self.con.cursor()

    def _normalize_db_input(self, *inp):
        inp = list(inp)
        for x in range(len(inp)):
            if not isinstance(inp[x], str):
                inp[x] = str(inp[x])
        return inp

    def show_movies(self):
        script = 'SELECT * FROM MOVIES ORDER BY rating'
        self.cursor.execute(script)
        return [{
                'id': row['id'],
                'name': row['name'],
                'rating': row['rating']
                    } for row in self.cursor]

    def select_moviename_by_id(self, id):
        #if self.check_id_validity('MOVIES', id):
        script = 'SELECT name FROM MOVIES WHERE id=?'
        self.cursor.execute(script, (id,))
        return self.cursor.fetchone()['name']

    def show_movie_proj_by_id(self, movie_id):
        script = '''SELECT PROJECTIONS.id, PROJECTIONS.date, PROJECTIONS.time, PROJECTIONS.type
                    FROM PROJECTIONS
                    INNER JOIN MOVIES
                    ON PROJECTIONS.movie_id = MOVIES.id
                    WHERE MOVIES.id=?'''
        self.cursor.execute(script, (movie_id,))
        return self.cursor.fetchall()

    def check_id_validity(self, table_name, id):
        script = 'SELECT COUNT(*) FROM {}'.format(table_name)
        self.cursor.execute(script)
        projs = int(self.cursor.fetchone()['COUNT(*)'])
        if id < 0 or id > projs:
            return False
        return True

    def show_movie_projections(self, movie_id, date=None):
        #self._normalize_db_input(movie_id)
        if date:
            script = 'SELECT * FROM PROJECTIONS WHERE movie_id=? AND date=? ORDER BY date'
            self.cursor.execute(script, (movie_id, date,))
        else:
            script = 'SELECT * FROM PROJECTIONS WHERE movie_id=?'
            self.cursor.execute(script, (movie_id,))
        return [{
                'id': row['id'],
                'movie_id': row['movie_id'],
                'type': row['type'],
                'date': row['date'],
                'time': row['time']} for row in self.cursor]

    def show_number_of_seats(self, projection_id):
        #self._normalize_db_input(projection_id)
        #if self.check_id_validity('PROJECTIONS', projection_id):
        script = 'SELECT COUNT(*) FROM RESERVATIONS WHERE projection_id=?'
        self.cursor.execute(script, (projection_id,))
        return self.DEFAULT_NUM_SEATS - int(self.cursor.fetchone()['COUNT(*)'])

    def make_reservation(self, name, projection_id, row, col):
        self.cursor.execute('SELECT row, col FROM RESERVATIONS WHERE row=? AND col=?', (row, col,))
        if len(self.cursor.fetchall()) == 0:
            script = 'INSERT INTO RESERVATIONS(username, projection_id, row, col) VALUES (?, ?, ?, ?)'
            self.cursor.execute(script, (name, projection_id, row, col,))
            self.con.commit()

    def get_reserved_seats_for_projection(self, projection_id):
        script = 'SELECT row, col FROM RESERVATIONS WHERE projection_id=?'
        self.cursor.execute(script, (projection_id,))
        return ((int(r['row']), int(r['col'])) for r in self.cursor.fetchall())


def main():
    from crs.settings import DB_NAME
    m = Manager(DB_NAME)
    m.show_movie_proj_by_id(2)
    m.make_reservation('Ivo', 2, 4, 5)

if __name__ == '__main__':
    main()
