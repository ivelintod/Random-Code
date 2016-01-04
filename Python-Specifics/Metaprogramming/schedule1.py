import warnings

import loader


DB_NAME = 'data/schedule1_db'
CONFERENC = 'conference.115'


class Record:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def load_db(db):
    raw_data = loader.load()
    warnings.warn('loading...' + DB_NAME)
    for col, rec_list in raw_data['Schedule'].items():
        record_type = col[:len(col) - 1]
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = Record(**record)
