class Hall(list):

    def __init__(self):
        self.extend([['.'] * 10 for i in range(10)])

    def __repr__(self):
        return('Hall()')

    def __str__(self):
        res = '{0:<3}'.format('')
        res += '  '.join([str(x) for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]) + '\n'
        for row in range(len(self)):
            if row == len(self) - 1:
                formatter = str(row + 1) + ' '
            else:
                formatter = str(row + 1) + '  '
            res += ('{}' + '  '.join(self[row]) + '\n').format(formatter)
        return res

    def check_seat(self, row, col):
        try:
            if self[row][col] == '.':
                return True
            return False
        except IndexError:
            return False

    def take_seat(self, row, col):
        if self.check_seat(row, col):
            self[row][col] = 'X'
        else:
            print('Seat already taken!')

    def update_hall_map(self, iter):
        for x in iter:
            row = x[0] - 1
            col = x[1] - 1
            self.take_seat(row, col)


def main():
    h = Hall()
    h[3][3] = 'X'
    h.take_seat(4, 4)
    print(h)


if __name__ == '__main__':
    main()
