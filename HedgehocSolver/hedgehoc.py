import enum
from functools import partial

# inp_badgers = input('Enter num of badgers:')
# print('Enter x,y coordinates of each badger')
# badgers_coords = [input() for i in range(int(inp_badgers))]


def transform_inp_coords(inp):
    return tuple([(int(x), int(y)) for x, y in [coord.split(',') for coord in inp]])


class UnallowedPosition(BaseException):
    pass


class IllegalPosition(BaseException):
    pass


class Orientations(enum.Enum):
    """Enum used for the orientations
       of each state as well as the four
       move directions
    """
    horizontal = 1
    vertical = 2
    left = 3
    up = 4
    right = 5
    down = 6


class Grid:

    SUCCESS_COORDS = ((3, 5), (3, 6), (4, 5), (4, 6))

    def __init__(self, hedgehoc_coords, badgers_coords,
                 hedgehoc_state_class, orientation):
        self.coords = hedgehoc_coords
        self.badgers_coords = badgers_coords
        self.grid = [[None] * 7 for i in range(7)]
        self.populate_grid(self.badgers_coords, self.coords)
        self.hedgehoc = Hedgehog(self.coords,
                                 hedgehoc_state_class,
                                 orientation,
                                 self)

    def __str__(self):
        return '\n'.join(str(row) for row in grid.grid)

    def populate_grid(self, badgers_coords=None, hedgehoc_coords=None, old_coords=None):
        if badgers_coords:
            for x, y in badgers_coords:
                self.grid[x][y] = 'X'

        if hedgehoc_coords:
            for x, y in hedgehoc_coords:
                self.grid[x][y] = 'O'

        if old_coords:
            for x, y in old_coords:
                self.grid[x][y] = None

    def update_grid(self, old_coords, hedgehoc_coords):
        """Remove old coordinates and apply new ones"""
        actual_old_coords = [coord for coord in old_coords
                             if coord not in hedgehoc_coords]
        self.populate_grid(hedgehoc_coords=hedgehoc_coords,
                           old_coords=actual_old_coords)


class Hedgehog:

    MOVE_OPTIONS = (Orientations.left, Orientations.up,
                    Orientations.right, Orientations.down)
    OPPOSITES = {
        Orientations.left: Orientations.right,
        Orientations.up: Orientations.down,
        Orientations.right: Orientations.left,
        Orientations.down: Orientations.up
    }

    def __init__(self, coords, state_class, orientation, grid):
        self.grid = grid
        # self.create_move_methods()
        self.position = Position(coords, orientation)
        self.position.set_initial_actual_position(state_class)
        self.escape_routes = []
        self.visited_positions = set()

    def create_move_methods(self):
        """Dynamically created move methods; unused"""
        move_methods = ('move_left', 'move_up', 'move_right', 'move_down')
        for name in move_methods:
            direction = Orientations[name.split('_')[1]]
            setattr(self, name, lambda: self.move(direction))

    def move(self, direction, checks=True):
        """Actual movement of the hedgehocs, optional
           checks flag to disable validation when performing
           reversal move
        """
        old_coords = self.position._position.coords
        self.position.set_move_options()
        if checks:
            valid_pos = self.position.is_valid_position(
                direction, self.grid.badgers_coords
            )
            potential_coords = self.position._position.moves[direction].coords
            visited_coords = potential_coords in self.visited_positions
            if not valid_pos or visited_coords:
                return False
        self.position.switch_position(direction)
        self.grid.update_grid(old_coords,
                              self.position._position.coords)
        return True

    def escape(self, route=None):
        """Escape algorithm; DFS currently
           Returns a list with tuples of tuples
           of the coordinates of each state in the run
        """
        self.visited_positions.add(self.position.get_coords())
        if not route:
            route = [self.position._position.coords]
        if route[-1] == self.grid.SUCCESS_COORDS:
            return route
        for move_opt in self.MOVE_OPTIONS:
            move_outcome = self.move(move_opt)
            if move_outcome:
                route.append(self.position.get_coords())
                self.escape_routes.append(str(self.grid))
                route = self.escape(route)
                if route[-1] == self.grid.SUCCESS_COORDS:
                    return route
                self.move(self.OPPOSITES[move_opt], checks=False)

        self.escape_routes = self.escape_routes[:-1]
        return route[:-1]


class Position:
    """Position interface
       Holds an instance of the real position object
       which is a child of Position in every case
    """
    orientations = Orientations

    def __init__(self, hedgehoc_coords, orientation):
        # print('Orientation', orientation)
        self.coords = hedgehoc_coords
        self.moves = {
            Orientations.left: None,
            Orientations.up: None,
            Orientations.right: None,
            Orientations.down: None
        }
        if orientation not in self.orientations:
            print(self, orientation, self.orientations)
            raise UnallowedPosition
        self.orientation = orientation
        self._position = None

    def set_initial_actual_position(self, state_class):
        self._position = state_class(self.coords, self.orientation)

    def get_coords(self):
        return self._position.coords

    def switch_position(self, direction):
        self._position = self._position.moves[direction]

    def set_move_options(self):
        """Actual implementation is in the derived classes
           All it does is to initialize the states in which
           the hedgehoc would find itself in after movement.
           Couldn't think of a better way, since the initial
           position and state could be any, so no dynamic
           optimizing involved;
           Flat, SideRaised and FlatReversed probably use
           a dumber, lengthier way to calculate the positions
           in comparison with FullyRaised (still bad);
        """
        self._position.set_move_options()

    def is_valid_position(self, move, badgers_coords):
        for coord in self._position.moves[move].coords:
            if any(c < 0 or c >= 7 for c in coord) or coord in badgers_coords:
                return False
        return True


class Flat(Position):
    """
        XX       XXX
        XX  or   XXX
        XX
    """
    orientations = (Orientations.horizontal, Orientations.vertical)

    def set_move_options(self):
        if self.orientation == Orientations.horizontal:
            new_coords_left = (
                (self.coords[0][0], self.coords[0][1] - 1),
                self.coords[0],
                (self.coords[3][0], self.coords[3][1] - 1),
                self.coords[3]
            )
            self.moves[Orientations.left] = FullyRaised(new_coords_left,
                                                        Orientations.left)

            new_coords_up = (
                (self.coords[0][0] - 1, self.coords[0][1]),
                (self.coords[2][0] - 1, self.coords[2][1]),
                self.coords[0],
                self.coords[1],
                self.coords[2]
            )
            self.moves[Orientations.up] = SideRaised(new_coords_up,
                                                     Orientations.up)

            new_coords_right = (
                self.coords[2],
                (self.coords[2][0], self.coords[2][1] + 1),
                self.coords[5],
                (self.coords[5][0], self.coords[5][1] + 1)
            )
            self.moves[Orientations.right] = FullyRaised(new_coords_right,
                                                         Orientations.right)

            new_coords_down = (
                self.coords[3],
                self.coords[4],
                self.coords[5],
                (self.coords[3][0] + 1, self.coords[3][1]),
                (self.coords[5][0] + 1, self.coords[5][1])
            )
            self.moves[Orientations.down] = SideRaised(new_coords_down,
                                                       Orientations.down)
        else:
            new_coords_left = (
                (self.coords[0][0], self.coords[0][1] - 1),
                self.coords[0],
                self.coords[2],
                (self.coords[4][0], self.coords[4][1] - 1),
                self.coords[4]
            )
            self.moves[Orientations.left] = SideRaised(new_coords_left,
                                                       Orientations.left)

            new_coords_up = (
                (self.coords[0][0] - 1, self.coords[0][1]),
                (self.coords[1][0] - 1, self.coords[1][1]),
                self.coords[0],
                self.coords[1]
            )
            self.moves[Orientations.up] = FullyRaised(new_coords_up,
                                                      Orientations.up)

            new_coords_right = (
                self.coords[1],
                (self.coords[1][0], self.coords[1][1] + 1),
                self.coords[3],
                self.coords[5],
                (self.coords[5][0], self.coords[5][1] + 1)
            )
            self.moves[Orientations.right] = SideRaised(new_coords_right,
                                                        Orientations.right)

            new_coords_down = (
                self.coords[4],
                self.coords[5],
                (self.coords[4][0] + 1, self.coords[4][1]),
                (self.coords[5][0] + 1, self.coords[5][1])
            )
            self.moves[Orientations.down] = FullyRaised(new_coords_down,
                                                        Orientations.down)


class SideRaised(Position):
    """
        XX        XXX        X X        XX
        X    or   X X   or   XXX   or    X
        XX                              XX
    """
    orientations = (Orientations.left, Orientations.up,
                    Orientations.right, Orientations.down)

    def set_move_options(self):
        if self.orientation == Orientations.left:

            new_coords_left = (
                (self.coords[0][0], self.coords[0][1] - 1),
                self.coords[0],
                (self.coords[3][0], self.coords[3][1] - 1),
                self.coords[3]
            )
            self.moves[Orientations.left] = FlatReversed(new_coords_left,
                                                         Orientations.vertical)

            new_coords_up = (
                (self.coords[0][0] - 1, self.coords[0][1]),
                (self.coords[1][0] - 1, self.coords[1][1]),
                self.coords[0],
                self.coords[1]
            )
            self.moves[Orientations.up] = FullyRaised(new_coords_up,
                                                      Orientations.left)

            new_coords_right = (
                self.coords[1],
                (self.coords[1][0], self.coords[1][1] + 1),
                self.coords[2],
                (self.coords[2][0], self.coords[2][1] + 1),
                self.coords[4],
                (self.coords[4][0], self.coords[4][1] + 1)
            )
            self.moves[Orientations.right] = Flat(new_coords_right,
                                                  Orientations.vertical)

            new_coords_down = (
                self.coords[3],
                self.coords[4],
                (self.coords[3][0] - 1, self.coords[3][1]),
                (self.coords[4][0] - 1, self.coords[4][1])
            )
            self.moves[Orientations.down] = FullyRaised(new_coords_down,
                                                        Orientations.left)

        elif self.orientation == Orientations.up:

            new_coords_left = (
                (self.coords[0][0], self.coords[0][1] - 1),
                self.coords[0],
                (self.coords[2][0], self.coords[2][1] - 1),
                self.coords[2]
            )
            self.moves[Orientations.left] = FullyRaised(new_coords_left,
                                                        Orientations.up)

            new_coords_up = (
                (self.coords[0][0] - 1, self.coords[0][1]),
                (self.coords[1][0] - 1, self.coords[1][1]),
                self.coords[0],
                self.coords[1]
            )
            self.moves[Orientations.up] = FlatReversed(new_coords_up,
                                                       Orientations.horizontal)

            new_coords_right = (
                self.coords[1],
                (self.coords[1][0], self.coords[1][1] + 1),
                self.coords[4],
                (self.coords[4][0], self.coords[4][1] + 1)
            )
            self.moves[Orientations.right] = FullyRaised(new_coords_right,
                                                         Orientations.up)

            new_coords_down = (
                self.coords[2],
                self.coords[3],
                self.coords[4],
                (self.coords[2][0] + 1, self.coords[2][1]),
                (self.coords[3][0] + 1, self.coords[3][1]),
                (self.coords[4][0] + 1, self.coords[4][1])
            )
            self.moves[Orientations.down] = Flat(new_coords_down,
                                                 Orientations.horizontal)

        elif self.orientation == Orientations.right:

            new_coords_left = (
                (self.coords[0][0], self.coords[0][1] - 1),
                self.coords[0],
                (self.coords[2][0], self.coords[2][1] - 1),
                self.coords[2],
                (self.coords[3][0], self.coords[3][1] - 1),
                self.coords[3]
            )
            self.moves[Orientations.left] = Flat(new_coords_left,
                                                 Orientations.vertical)

            new_coords_up = (
                (self.coords[0][0] - 1, self.coords[0][1]),
                (self.coords[1][0] - 1, self.coords[1][1]),
                self.coords[0],
                self.coords[1]
            )
            self.moves[Orientations.up] = FullyRaised(new_coords_up,
                                                      Orientations.right)

            new_coords_right = (
                self.coords[1],
                (self.coords[1][0], self.coords[1][1] + 1),
                self.coords[4],
                (self.coords[4][0], self.coords[4][1] + 1)
            )
            self.moves[Orientations.right] = FlatReversed(new_coords_right,
                                                          Orientations.horizontal)

            new_coords_down = (
                self.coords[3],
                self.coords[4],
                (self.coords[3][0] + 1, self.coords[3][1]),
                (self.coords[4][0] + 1, self.coords[4][1])
            )
            self.moves[Orientations.down] = FullyRaised(new_coords_down,
                                                        Orientations.right)

        elif self.orientation == Orientations.down:

            new_coords_left = (
                (self.coords[0][0], self.coords[0][1] - 1),
                self.coords[0],
                (self.coords[3][0], self.coords[3][1] - 1),
                self.coords[3]
            )
            self.moves[Orientations.left] = FullyRaised(new_coords_left,
                                                        Orientations.up)

            new_coords_up = (
                (self.coords[0][0] - 1, self.coords[0][1]),
                (self.coords[1][0] - 1, self.coords[1][1]),
                (self.coords[2][0] - 1, self.coords[2][1]),
                self.coords[0],
                self.coords[1],
                self.coords[2]
            )
            self.moves[Orientations.up] = Flat(new_coords_up,
                                               Orientations.horizontal)

            new_coords_right = (
                self.coords[2],
                (self.coords[2][0], self.coords[2][1] + 1),
                self.coords[4],
                (self.coords[4][0], self.coords[4][1] + 1)
            )
            self.moves[Orientations.right] = FullyRaised(new_coords_right,
                                                         Orientations.down)

            new_coords_down = (
                self.coords[3],
                self.coords[4],
                (self.coords[3][0] + 1, self.coords[3][1]),
                (self.coords[4][0] + 1, self.coords[4][1])
            )
            self.moves[Orientations.down] = FlatReversed(new_coords_down,
                                                         Orientations.horizontal)


class FlatReversed(Position):
    """
        XX       X  X
            or   X  X
        XX
    """
    orientations = (Orientations.horizontal, Orientations.vertical)

    def set_move_options(self):
        if self.orientation == Orientations.horizontal:

            new_coords_left = (
                (self.coords[0][0], self.coords[0][1] - 1),
                self.coords[0],
                (self.coords[2][0], self.coords[2][1] - 1),
                self.coords[2]
            )
            self.moves[Orientations.left] = FullyRaised(new_coords_left,
                                                        Orientations.right)

            new_coords_up = (
                (self.coords[0][0] - 1, self.coords[0][1]),
                (self.coords[0][0] - 1, self.coords[0][1] + 1),
                (self.coords[1][0] - 1, self.coords[1][1]),
                self.coords[0],
                self.coords[1]
            )
            self.moves[Orientations.up] = SideRaised(new_coords_up,
                                                     Orientations.down)

            new_coords_right = (
                self.coords[1],
                self.coords[3],
                (self.coords[1][0], self.coords[1][1] + 1),
                (self.coords[3][0], self.coords[3][1] + 1)
            )
            self.moves[Orientations.right] = FullyRaised(new_coords_right,
                                                         Orientations.left)

            new_coords_down = (
                self.coords[2],
                self.coords[3],
                (self.coords[2][0] + 1, self.coords[2][1]),
                (self.coords[2][0] + 1, self.coords[2][1] + 1),
                (self.coords[3][0] + 1, self.coords[3][1])
            )
            self.moves[Orientations.down] = SideRaised(new_coords_down,
                                                       Orientations.up)

        else:

            new_coords_left = (
                (self.coords[0][0], self.coords[0][1] - 1),
                self.coords[0],
                (self.coords[0][0] - 1, self.coords[0][1] - 1),
                (self.coords[2][0], self.coords[2][1] - 1),
                self.coords[2]
            )
            self.moves[Orientations.left] = SideRaised(new_coords_left,
                                                       Orientations.right)

            new_coords_up = (
                (self.coords[0][0] - 1, self.coords[0][1]),
                (self.coords[1][0] - 1, self.coords[1][1]),
                self.coords[0],
                self.coords[1]
            )
            self.moves[Orientations.up] = FullyRaised(new_coords_up,
                                                      Orientations.down)

            new_coords_right = (
                self.coords[1],
                (self.coords[1][0], self.coords[1][1] + 1),
                (self.coords[1][0] + 1, self.coords[1][1] + 1),
                self.coords[3],
                (self.coords[3][0], self.coords[3][1] + 1)
            )

            self.moves[Orientations.right] = SideRaised(new_coords_right,
                                                        Orientations.left)

            new_coords_down = (
                self.coords[2],
                self.coords[3],
                (self.coords[2][0] + 1, self.coords[2][1]),
                (self.coords[3][0] + 1, self.coords[3][1])
            )
            self.moves[Orientations.down] = FullyRaised(new_coords_down,
                                                        Orientations.up)


class FullyRaised(Position):
    """
        XX
        XX  (with four orientations)
    """
    orientations = (Orientations.left, Orientations.up,
                    Orientations.right, Orientations.down)

    def set_move_options(self):
        if self.orientation == Orientations.left:
            temp_dict = {
                Orientations.left: (((0, -2), (0, 0), (1, -2), (1, 0)), FlatReversed, Orientations.horizontal),
                Orientations.up: (((-2, 0), (-2, 1), (-1, 1), (0, 0), (0, 1)), SideRaised, Orientations.left),
                Orientations.right: (((0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3)), Flat, Orientations.horizontal),
                Orientations.down: (((1, 0), (1, 1), (2, 1), (3, 0), (3, 1)), SideRaised, Orientations.left)
            }

        elif self.orientation == Orientations.up:
            temp_dict = {
                Orientations.left: (((0, -2), (0, 0), (1, -2), (1, -1), (1, 0)), SideRaised, Orientations.up),
                Orientations.up: (((-2, 0), (-2, 1), (0, 0), (0, 1)), FlatReversed, Orientations.vertical),
                Orientations.right: (((0, 1), (0, 3), (1, 1), (1, 2), (1, 3)), SideRaised, Orientations.up),
                Orientations.down: (((1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)), Flat, Orientations.vertical)
            }

        elif self.orientation == Orientations.right:
            temp_dict = {
                Orientations.left: (((0, -2), (0, -1), (0, 0), (1, -2), (1, -1), (1, 0)), Flat, Orientations.horizontal),
                Orientations.up: (((-2, 0), (-2, 1), (-1, 0), (0, 0), (0, 1)), SideRaised, Orientations.right),
                Orientations.right: (((0, 1), (0, 3), (1, 1), (1, 3)), FlatReversed, Orientations.horizontal),
                Orientations.down: (((1, 0), (1, 1), (2, 0), (3, 0), (3, 1)), SideRaised, Orientations.right)
            }

        elif self.orientation == Orientations.down:
            temp_dict = {
                Orientations.left: (((0, -2), (0, -1), (0, 0), (1, -2), (1, 0)), SideRaised, Orientations.down),
                Orientations.up: (((-2, 0), (-2, 1), (-1, 0), (-1, 1), (0, 0), (0, 1)), Flat, Orientations.vertical),
                Orientations.right: (((0, 1), (0, 2), (0, 3), (1, 1), (1, 3)), SideRaised, Orientations.down),
                Orientations.down: (((1, 0), (1, 1), (3, 0), (3, 1)), FlatReversed, Orientations.vertical)
            }

        for key, val in temp_dict.items():
            coord_offsets, clz, orientation = val
            new_coords = [(self.coords[0][0] + x, self.coords[0][1] + y) for x, y in coord_offsets]
            self.moves[key] = clz(tuple(new_coords), orientation)


if __name__ == '__main__':


    # NO INPUT VALIDATION !!!!!!!!!


    inp_badgers = input('Enter num of badgers:\n')
    badgers_coords = [input('Enter x,y coordinates of badger {}: '.format(i + 1))
                      for i in range(int(inp_badgers))]
    badgers_coords = transform_inp_coords(badgers_coords)

    hedgehoc_state_inp_str = """
        Enter 1 for Flat:       XXX  or  XX
                                XXX      XX
                                         XX

        Enter 2 for SideRaised: XXX  or  X X  or  XX  or  XX
                                X X      XXX      X        X
                                                  XX      XX

        Enter 3 for FlatReversed: X X  or  XX
                                  X X
                                           XX

        Enter 4 for FullyRaised: XX (with 4 orientations)
                                 XX
    """

    hedgehoc_state = input(hedgehoc_state_inp_str)

    if int(hedgehoc_state) in (2, 4):
        hedgehoc_orientation_inp_str = """
            Enter 1 for Left orientation
            Enter 2 for Up orientation
            Enter 3 for Right orientation
            Enter 4 for Down orientation
        """
        hedgehoc_orientation = input(hedgehoc_orientation_inp_str)
        orientation = {
            1: Orientations.left,
            2: Orientations.up,
            3: Orientations.right,
            4: Orientations.down
        }[int(hedgehoc_orientation)]

    else:
        hedgehoc_orientation_inp_str = """
            Enter 1 for Horizontal orientation
            Enter 2 for Vertical orientation
        """
        hedgehoc_orientation = input(hedgehoc_orientation_inp_str)
        orientation = {
            1: Orientations.horizontal,
            2: Orientations.vertical
        }[int(hedgehoc_orientation)]

    num_hedgehocs, hedgehoc_state_class = {
        1: (6, Flat),
        2: (5, SideRaised),
        3: (4, FlatReversed),
        4: (4, FullyRaised),
    }[int(hedgehoc_state)]

    hedgehoc_coords = [input('Enter x,y coordinates of hedgehoc {}: '.format(i + 1))
                       for i in range(int(num_hedgehocs))]
    hedgehoc_coords = transform_inp_coords(hedgehoc_coords)

    # hedgehoc_coords = ((1, 3), (1, 4), (2, 3), (3, 3), (3, 4))
    # badgers_coords = ((1, 2), (1, 6), (2, 0), (4, 3))

    grid = Grid(hedgehoc_coords, badgers_coords,
                hedgehoc_state_class, orientation)

    res = grid.hedgehoc.escape()

    for row in grid.hedgehoc.escape_routes:
        print(row)
        print('\n')
    print(res)
