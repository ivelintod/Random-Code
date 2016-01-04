import sys, locale

expressions = '''
        locale.getpreferredencoding()
        type(my_file)
        sys.stdout.isatty()
        sys.stdout.encoding
        sys.stdin.isatty()
        sys.stdin.encoding
        sys.stderr.isatty()
        sys.stderr.encoding
        sys.getdefaultencoding()
        sys.getfilesystemencoding()
    '''

my_file = open('dummy', 'w')
for expression in expressions.split():
    value = eval(expression)
#    print(expression.rjust(30), '->', value)


from unicodedata import normalize

s1 = 'café'
s2 = 'cafe\u0301'


import unicodedata
import string


def shave_marks(txt):
    norm_txt = normalize('NFD', txt)
    shaved = ''.join(x for x in norm_txt if not unicodedata.combining(x))
    return normalize('NFC', shaved)

def shave_marks_latin(txt):
    norm_txt = normalize('NFD', txt)
    latin_base = False
    keepers = []
    for c in norm_txt:
        if unicodedata.combining(c) and latin_base:
            continue
        keepers.append(c)
        if not unicodedata.combining(c):
            latin_base = c in string.ascii_letters
    shaved = ''.join(keepers)
    return unicodedata.normalize('NFC', shaved)


single_map = str.maketrans("""‚ƒ„†ˆ‹‘’“”•–—˜›""",
                           """'f"*^<''""---~>""")


multi_map = str.maketrans({
 '€': '<euro>',
 '…': '...',
 'Œ': 'OE',
 '™': '(TM)',
 'œ': 'oe',
 '‰': '<per mille>',
 '‡': '**',
})


multi_map.update(single_map)


def dewinize(txt):
    return txt.translate(multi_map)


def asciize(txt):
    no_marks = shave_marks_latin(dewinize(txt))
    no_marks = no_marks.replace('ß', 'ss')
    return no_marks



