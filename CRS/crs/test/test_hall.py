from crs.make_hall import Hall

def pytest_funcarg__hall(request):
    h = Hall()
    return h

def test_repr(hall):
    assert repr(hall) == 'Hall()'

def test_check_seat(hall):
    assert hall.check_seat(1, 2) == True
    assert hall.check_seat(12, 10) == False

def test_take_seat(hall):
    hall.take_seat(9, 9)
    assert hall.check_seat(9, 9) == False
    assert hall[9][9] == 'X'

