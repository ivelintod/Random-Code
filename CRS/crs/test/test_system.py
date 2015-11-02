from crs.settings import DB_TEST
from crs.system import InteractiveSystem
from crs.make_db import create_db
import os


def pytest_funcarg__IS(request):
    #path = os.path.dirname(os.path.realpath(__file__))
    #create_db(path)
    def setup():
        path = os.path.dirname(os.path.realpath(__file__))
        create_db(path)
        intsys = InteractiveSystem(DB_TEST)
        return intsys

    def cleanup(intsys):
        os.remove(DB_TEST)

    return request.cached_setup(
            setup=setup,
            teardown=cleanup,
            scope='session')


def test_nonum_validizer(IS):
    assert IS._nonum_validizer('Ivo12') == False
    assert IS._nonum_validizer('Ivo') == True


def test_noletters_validizer(IS):
    assert IS._noletters_validizer('1234214') == True
    assert IS._noletters_validizer('1213Ivo12') == False


#def test_register_name_tickets(IS):
#    IS.register_name_tickets()
#    assert IS.self.reservation_info['name'] == 'Ivelin'
#    assert IS.self.reservation_info['tickets'] == 2


def test_show_movie_projections(IS):
    title = 'Projections for movie Sicario on date 2015-11-02\n'
    mov1 = '[2] - 16:30 (2D)\n'
    mov2 = '[5] - 20:35 (3D)'
    assert IS.show_movie_projections(2, '2015-11-02') == title + mov1 + mov2

    title = 'Projections for movie Sicario\n'
    mov1 = '[2] - 2015-11-02 16:30 (2D) - 100 spots available\n'
    mov2 = '[5] - 2015-11-02 20:35 (3D) - 100 spots available'
    assert IS.show_movie_projections(2, spots=True) == title + mov1 + mov2


def test_show_movies(IS):
    title = 'Current movies:\n'
    mov1 = '[1] - The Intern (7.4)\n'
    mov2 = '[2] - Sicario (8.0)\n'
    mov3 = '[3] - The Martian (8.2)'
    assert IS.show_movies() == title + mov1 + mov2 + mov3


def test_insufficient_spots_for_tickets(IS):
    IS.reservation_info['tickets'] = 58
    test = IS.insufficient_spots_for_tickets(5)
    assert test is True
    IS.reservation_info['tickets'] = 134
    test = IS.insufficient_spots_for_tickets(2)
    assert test is False


def test_show_reserved_seats(IS):
    result = IS.show_reserved_seats(4)
    anticipated_result = IS.hall
    assert result == anticipated_result
