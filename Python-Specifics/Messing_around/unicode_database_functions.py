import unicodedata
import string
import re


re_digit = re.compile(r'\d')

sample = '1\xbc\xb2\u0969\u136b\u216b\u2466\u2480\u3285'

for char in sample:
    print('U+%04x' % ord(char),
          char.center(6),
          're_dig' if re_digit.match(char) else '-',
          'isdig' if char.isdigit() else '-',
          'isnum' if char.isnumeric() else '-',
          format(unicodedata.numeric(char), '5.2f'),
          unicodedata.name(char),
          sep='\t')


re_numbers_str = re.compile(r'\d+')
re_words_str = re.compile(r'\w+')
re_numbers_bytes = re.compile(rb'\d+')
re_words_bytes = re.compile(rb'\w+')

text_str = ("Ramanujan saw \u0be7\u0bed\u0be8\u0bef"
            " as 1729 = 1³ + 12³ = 9³ + 10³.")

text_bytes = text_str.encode('utf_8')

print('Numbers')
print('str:'.center(12), re_numbers_str.findall(text_str))
print('bytes:'.center(12), re_numbers_bytes.findall(text_bytes))
print('Words')
print('str:'.center(12), re_words_str.findall(text_str))
print('bytes:'.center(12), re_words_bytes.findall(text_bytes))


def shave_marks_latin(txt):
    process_txt = unicodedata.normalize('NFD', txt)
    keepers = []
    latin_base = False
    for char in process_txt:
        if not unicodedata.combining(char) or not latin_base:
            keepers.append(char)
        elif unicodedata.combining(char) and not latin_base:
            keepers.append(char)
        elif not unicodedata.combining(char) and latin_base:
            keepers.append(char)
        if not unicodedata.combining(char):
            latin_base = char in string.ascii_letters
    text = ''.join(keepers)
    return unicodedata.normalize('NFC', text)

print('\u0031')

print('two'>'three')

