from crs import db_manager, make_db
from crs.settings import DB_NAME, DB_TEST
import os


def pytest_funcarg__manager(request):

    def setup():
        path = os.path.dirname(os.path.realpath(__file__))
        make_db.create_db(path)
        m = db_manager.Manager(DB_TEST)
        return m

    def cleanup(m):
        os.remove(DB_TEST)

    return request.cached_setup(
            setup=setup,
            teardown=cleanup,
            scope='session')


def test__normalize_db_input(manager):
    test_inp = manager._normalize_db_input('This', 'input is', 5, 'elements', 'long')
    assert test_inp == ['This', 'input is', '5', 'elements', 'long']


def test_show_movies(manager):
    count_movies = 0
    for x in manager.show_movies():
        count_movies += 1
    assert count_movies == 3


def test_select_moviname_by_id(manager):
    assert manager.select_moviename_by_id(1) == 'The Intern'
    assert manager.select_moviename_by_id(2) == 'Sicario'
    assert manager.select_moviename_by_id(3) == 'The Martian'


def test_show_movie_proj_by_id(manager):
    details = manager.show_movie_proj_by_id(1)
    assert len(details) == 1
    details = manager.show_movie_proj_by_id(2)
    assert len(details) == 2
    details = manager.show_movie_proj_by_id(3)
    assert len(details) == 2


def test_check_id_validity(manager):
    result = manager.check_id_validity('PROJECTIONS', 5)
    assert result is True
    result = manager.check_id_validity('MOVIES', 4)
    assert result is False


def test_show_movie_projections(manager):
    movie_projections_no_date = 0
    for x in manager.show_movie_projections(2):
        movie_projections_no_date += 1
    assert movie_projections_no_date == 2

    movie_projections_with_date = 0
    for x in manager.show_movie_projections(2, '2015-11-01'):
        movie_projections_with_date += 1
    assert movie_projections_with_date == 0


def test_show_number_of_seats(manager):
    assert manager.show_number_of_seats(1) == 100
    assert manager.show_number_of_seats(2) == 100
    assert manager.show_number_of_seats(3) == 100
    assert manager.show_number_of_seats(4) == 100
    assert manager.show_number_of_seats(5) == 100


def test_make_reservation(manager):
    manager.make_reservation('Ivo', 4, 3, 5)
    assert manager.show_number_of_seats(4) == 99


def test_get_reserved_seats_for_projection(manager):
    result = manager.get_reserved_seats_for_projection(4)
    for r in result:
        assert r == (3, 5)
