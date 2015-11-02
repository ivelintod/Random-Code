from crs.db_manager import Manager
from crs.make_hall import Hall
from crs.settings import DB_NAME
import sys
import re


class InteractiveSystem:

    def __init__(self, db_name):
        self.manager = Manager(db_name)
        self.hall = Hall()
        self.reservation_info = {}

    def _nonum_validizer(self, inp):
        if re.findall('\d+', inp) or inp == '':
            return False
        return True

    def _noletters_validizer(self, inp):
        if re.findall('[a-zA-Z]', inp) or inp == '':
            return False
        return True

    def register_name_tickets(self):
        name = input('Enter name: ')
        while not self._nonum_validizer(name):
            print('Invalid name input')
            name = input('Enter name: ')

        tickets = input('Enter number ot tickets: ')
        while not self._noletters_validizer(tickets):
            print('Invalid ticket input')
            tickets = input('Enter number of tickets')

        self.reservation_info['username'] = name
        self.reservation_info['tickets'] = int(tickets)

    def show_movies(self):
        movie_info = '[{id}] - {name} ({rating})'
        movies = [movie_info.format(**movie) for movie in self.manager.show_movies()]
        movies.insert(0, 'Current movies:')
        return '\n'.join(movies)

    def prompt_for_movie_choice(self):
        ids = [movie['id'] for movie in self.manager.show_movies()]
        choice = input('Choose a movie: ')
        while not self._noletters_validizer(choice) or int(choice) not in ids:
            print('Invalid input!')
            choice = input('Choose a movie: ')
        self.reservation_info['movie_id'] = choice


    def show_movie_projections(self, movie_id, date=None, spots=False):
        movie_id = int(movie_id)
        if self.manager.check_id_validity('PROJECTIONS', movie_id):
            movie_name = self.manager.select_moviename_by_id(movie_id)
            self.reservation_info['movie_name'] = movie_name
            projections = self.manager.show_movie_projections(movie_id, date)
            output = []
            if date:
                message = '\nProjections for movie {} on date {}'
                projection_info = '[{id}] - {time} ({type})'
                output.append(message.format(movie_name, date))

                for proj in projections:
                    output.append(projection_info.format(**proj))
            else:
                message = '\nProjections for movie {}'
                output.append(message.format(movie_name))
                if spots:
                    projection_info = '[{id}] - {date} {time} ({type}) - {sp} spots available'
                    for proj in projections:
                        proj_spots = self.manager.show_number_of_seats(proj['id'])
                        proj.update(sp=proj_spots)
                        output.append(projection_info.format(**proj))
                else:
                    projection_info = '[{id}] - {date} {time} ({type})'
                    for proj in projections:
                        output.append(projection_info.format(**proj))

        return '\n'.join(output)

    def prompt_for_proj_choice(self, movie_id):
        projs = self.manager.show_movie_projections(movie_id)
        projections = [x['id'] for x in projs]
        choice = input('\nChoose a projection: ')
        while not self._noletters_validizer(choice) or int(choice) not in projections:
            print('Invalid input!')
            choice = input('\nChoose projection ID: ')
        self.reservation_info['projection_id'] = choice
        self.reservation_info['projection_details'] = {}
        for proj in projs:
            if proj['id'] == int(choice):
                self.reservation_info.update(proj)

    def insufficient_spots_for_tickets(self, proj_id):
        proj_spots = self.manager.show_number_of_seats(proj_id)
        if int(proj_spots) < self.reservation_info['tickets']:
            return False
        return True

    def show_reserved_seats(self, proj_id):
        reserved_seats = self.manager.get_reserved_seats_for_projection(proj_id)
        self.hall.update_hall_map(reserved_seats)
        return self.hall

    def process_tickets(self):
        self.reservation_info['seats'] = []
        for t in range(self.reservation_info['tickets']):
            seats = input('\nChoose seat {} in the form (row, col): '.format(t + 1))
            seats = re.findall('\d+', seats)
            seats = [int(x) for x in seats]
            while not self.hall.check_seat(*seats):
                print('Invalid row/col or seat already taken!')
                seats = input('{}. Choose seats (row, col): '.format(t))
                seats = re.findall('\d+', seats)
            self.reservation_info['seats'].append(seats)

    def show_reservation_info(self):
        info = []
        info.append('\nThis is your resevation:')
        info.append('Movie: {}'.format(self.reservation_info['movie_name']))
        info.append('Date and Time: {} {} {}'.format(self.reservation_info['date'], self.reservation_info['time'], self.reservation_info['type']))
        seats = ''
        for seat in self.reservation_info['seats']:
            seats += '{}, '.format(seat)
        seats.strip(',')
        info.append('Seats: {}'.format(seats))
        return '\n'.join(info)

    def finalize(self):
        prompt = input('Enter "finalize" in order to complete resevation: ')
        if prompt == 'finalize':
            name = self.reservation_info['username']
            projection_id = self.reservation_info['projection_id']
            for i in self.reservation_info['seats']:
                self.manager.make_reservation(name, projection_id, i[0], i[1])
            print('Reservation complete! Enjoy!')
        else:
            print('Reservation not successful...')
            second_chance = input('Try again? Y/N')
            if second_chance == 'Y':
                self.finalize()

    def give_up_reservation_prompt(self, func):
        command = input('\nType "cancel" if you want to give up the reservation: ')
        if command == 'cancel':
            func()

    def exit(self):
        print('Thanks for visiting us!')
        sys.exit(1)


def main():
    IS = InteractiveSystem(DB_NAME)
    IS.show_movies()
    print(IS.show_movie_projections(2, '2015-11-02'))
    print(IS.show_movie_projections(2))
    print(IS.show_movie_projections(2, spots=True))
    print(IS.show_reserved_seats(2))

if __name__ == '__main__':
    main()
