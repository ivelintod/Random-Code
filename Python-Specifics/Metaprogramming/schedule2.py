import warnings
import inspect

import loader

DB_NAME = 'data/schedule2_db'
CONFERENCE = 'conference.115'


class Record:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        return NotImplemented


class MissingDatabaseError(RuntimeError):
    """Raised when no database is set"""


class DbRecord(Record):

    __db = None

    @staticmethod
    def set_db(db):
        DbRecord.__db = db

    @staticmethod
    def get_db():
        return DbRecord.__db

    @classmethod
    def fetch(cls, key):
        db = cls.get_db()
        try:
            return db[key]
        except TypeError:
            if db is None:
                msg = 'Database not set; call {}.set_db(my_db)'
                raise MissingDatabaseError(msg.format(cls.__name__))
            else:
                raise


    def __repr__(self):
        if hasattr(self, 'serial'):
            cls_name = self.__class__.__name__
            return '<{} serial={!r}'.format(cls_name, self.serial)
        else:
            return super().__repr__()


class Event(DbRecord):

    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)

    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'):
            spkr_serials = self.__dict__['speakers']
            self._speaker_objs = [self.__class__.fetch('speaker.{}'.format(spkr))
                                  for spkr in spkr_serials]
        return self._speaker_objs

    def __repr__(self):
        if hasattr(self, 'name'):
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__()


def load_db(db):
    data = loader.load()
    for key, rec_list in data['Schedule'].items():
        record_type = key[:-1]
        class_candidate = record_type.capitalize()
        cls = globals().get(class_candidate, DbRecord)
        if inspect.isclass(cls) and issubclass(cls, DbRecord):
            factory = cls
        else:
            factory = DbRecord
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = factory(**record)
