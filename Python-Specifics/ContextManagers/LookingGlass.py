import sys
import contextlib

class LG:

    def __enter__(self):
        self.original_writing = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'Breakerrrrs'

    def reverse_write(self, text):
        return self.original_writing(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.write = self.original_writing
        if exc_type is ZeroDivisionError:
            print('IDIOT!')
            return True
'''
with LG() as what:
    print('Kuchence naobratno')
    print(what)
    print(2/0)
print('tva veche tr da e ok')
'''

@contextlib.contextmanager
def looking_glass():
    original_out = sys.stdout.write

    def reverse(text):
        return original_out(text[::-1])

    sys.stdout.write = reverse
    msg = ''
    try:
        yield 'Sth'

    except ZeroDivisionError:
        msg = 'Do not divide by zero!'

    finally:
        sys.stdout.write = original_out
        if msg:
            print(msg)

