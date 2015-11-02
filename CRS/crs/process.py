from crs import system
from crs.settings import DB_NAME


class ReservationProcess:

    def __init__(self, db_name):
        self.sys = system.InteractiveSystem(db_name)

    @staticmethod
    def input_helper(inp, func):
        inp = inp.split()
        try:
            if len(inp) == 4:
                print(func(inp[2], inp[3]))
            else:
                print(func(inp[2]))
        except:
            ReservationProcess.input_helper(input('Try again!\nEnter command: '), func)

    def process_comands(self):
        commands = '''
            List of commands:
            1. movies
            2. movie projections {id}
            3. reservation
            4. help
            '''

        while True:

            command = input('Enter command: ')

            if command == 'help':
                print(commands)

            if command == 'movies':
                print(self.sys.show_movies())

            if 'movie projections' in command:
                ReservationProcess.input_helper(command, self.sys.show_movie_projections)

            if command == 'reservation':
                self.sys.register_name_tickets()

                self.sys.give_up_reservation_prompt(self.process_comands)

                print(self.sys.show_movies())
                self.sys.prompt_for_movie_choice()
                movie_id = self.sys.reservation_info['movie_id']

                self.sys.give_up_reservation_prompt(self.process_comands)

                print(self.sys.show_movie_projections(movie_id, spots=True))
                self.sys.prompt_for_proj_choice(movie_id)
                projection_id = self.sys.reservation_info['projection_id']
                print('\nAvalilable seats(marked with a dot):')
                print(self.sys.show_reserved_seats(projection_id))

                while not self.sys.insufficient_spots_for_tickets(projection_id):
                    print('Not enough seats for chosen projection')
                    self.sys.prompt_for_proj_choice(movie_id)
                    projection_id = self.sys.reservation_info['projection_id']
                    print('\nAvalilable seats(marked with a dot):')
                    print(self.sys.show_reserved_seats(projection_id))

                self.sys.give_up_reservation_prompt(self.process_comands)

                self.sys.process_tickets()
                print(self.sys.show_reservation_info())

                self.sys.give_up_reservation_prompt(self.process_comands)

                self.sys.finalize()

            if command == 'exit':
                self.sys.exit()

    def process(self):
        print('Welcome to our magic Cinema Resevation System!')
        print(30 * '*')
        print('Type "help" to see comands')
        self.process_comands()


if __name__ == '__main__':
    ReservationProcess(DB_NAME).process()




