from collections import namedtuple
import queue
import random

Event = namedtuple('Event', 'time ident action')

DEFAULT_SEARCH_TIME = 5
DEFAULT_TRIP_TIME = 10
DEFAULT_NUM_OF_TAXIS = 3
DEFAULT_SIM_TIME = 150


def taxi_process(ident, trips, start_time):
    time = yield Event(start_time, ident, 'leaving garage')
    for i in range(trips):
        time = yield Event(time, ident, 'picking up passenger')
        time = yield Event(time, ident, 'dropping passenger')
    yield Event(time, ident, 'going home')


taxis = {i: taxi_process(i, i + 2, i * 2)
         for i in range(1, DEFAULT_NUM_OF_TAXIS + 1)}


class Simulator:

    def __init__(self, taxis):
        self.taxis = dict(taxis)
        self.events = queue.PriorityQueue()

    def process_simulation(self):
        for _, taxi in self.taxis.items():
            taxi = next(taxi)
            self.events.put(taxi)

        time = 0
        while time < DEFAULT_SIM_TIME:
            if self.events.qsize() == 0:
                print('No more events')
                break
            current_event = self.events.get()
            time, ident, action = current_event
            msg = 'taxi {} {} {}'.format(ident, '\t' * ident, current_event)
            print(msg)
            interval = self.additional_time(time, action)
            try:
                next_event = self.taxis[ident].send(interval)
            except StopIteration:
                del self.taxis[ident]
            else:
                self.events.put(next_event)
        else:
            msg = 'Simulation ended: {} events pending'
            print(msg.format(self.events.qsize()))

    def additional_time(self, time, action):
        if action in ['leaving garage', 'dropping passenger']:
            interval = time + DEFAULT_SEARCH_TIME
        if action == 'picking up passenger':
            interval = time + DEFAULT_TRIP_TIME
        if action == 'going home':
            interval = 1

        return interval + random.randrange(10)


if __name__ == '__main__':
    Simulator(taxis).process_simulation()
