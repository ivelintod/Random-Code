import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        #self.words = RE_WORD.findall(self.text)

    def __repr__(self):
        cls = type(self)
        return '{.__name__}({})'.format(cls, reprlib.repr(self.text))

    def __iter__(self):
        #return SentenceIterator(self.words)
        #for word in self.words:
        #    yield word
        #return
        return (match.group() for match in RE_WORD.finditer(self.text))


class SentenceIterator:

    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self
