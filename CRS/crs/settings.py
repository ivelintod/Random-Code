import os

path = os.path.dirname(os.path.realpath(__file__))
DB_NAME = 'movie_database.db'
DB_TEST = '{}/test/movie_database.db'.format(path)
SQL_COMMANDS = '{}/fill_db.sql'.format(path)
TEST_PATH = '{}/test'.format(path)

